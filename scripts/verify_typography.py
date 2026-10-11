"""Measure the built decks and Runbooks in headless Chrome against the reading parameters
(course-authoring "Reading parameters"). Exits non-zero with one line per violation.

Deck (1920×1080): no fit-zoom < 1 or overflow past the 1728px content block, visible text ≥ 24px, titles ≤ 2 lines,
checkpoint card main 1 line / detail ≤ 2, 為什麼・你要判斷 1 line.
Runbook (1440px, every group unlocked): body paragraphs 32–40 CJK chars per line and
line-height ≥ 1.75, visible text ≥ 12px.
Run: uv run --no-project --python 3.13 python -X utf8 scripts/verify_typography.py
"""
import html
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDITIONS = {"main": ROOT / "agentic-workshop/materials", "dlc": ROOT / "agentic-workshop/materials-dlc"}
BROWSERS = (Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
            Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"))
SLIDE_MIN_PX, RUNBOOK_MIN_PX = 24, 12
MAX_LINES = {"title": 2, "main": 1, "detail": 2, "why": 1, "judge": 1}
CONTENT_W = 1728  # px, widest content block on a 1920px slide
MEASURE = (32, 40)  # CJK chars per line, Runbook body at 1440px
MIN_LINE_HEIGHT = 1.75

DECK_PROBE = r"""
const slides = [...document.querySelectorAll('#dk-stage > section.slide')], out = [];
const lines = e => { const s = getComputedStyle(e);
  const h = e.clientHeight - parseFloat(s.paddingTop) - parseFloat(s.paddingBottom);
  return Math.round(h / parseFloat(s.lineHeight)); };
const LINES = {title: '.title', main: '.cp-flow > li > b', detail: '.cp-flow > li > span', why: '.cp-why', judge: '.cp-judge'};
for (let i = 0; i < slides.length; i++) {
  location.hash = '#/' + (i + 1) + '.99'; await sleep(60);
  const s = slides[i], kids = [...s.children].filter(c => c.tagName !== 'ASIDE');
  const zoom = Math.min(1, ...kids.map(c => parseFloat(c.style.zoom) || 1));
  const top = s.getBoundingClientRect().top, k = s.getBoundingClientRect().height / s.offsetHeight || 1;
  const flow = kids.filter(c => !['absolute', 'fixed'].includes(getComputedStyle(c).position));
  const bottom = Math.max(0, ...flow.map(c => c.getBoundingClientRect().bottom));
  const right = Math.max(0, ...flow.map(c => c.getBoundingClientRect().right));
  const edge = s.getBoundingClientRect().left + (1920 + CONTENT_W) / 2 * k;  // right edge of the centred content block
  const limit = s.clientHeight - parseFloat(getComputedStyle(s).paddingBottom);
  const small = [], seen = new Set();
  const walk = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
  for (let t; (t = walk.nextNode());) {
    const e = t.parentElement;
    if (!t.textContent.trim() || seen.has(e) || e.closest('aside') || !e.getClientRects().length) continue;
    seen.add(e);
    const cs = getComputedStyle(e);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    const px = parseFloat(cs.fontSize);
    if (px < MIN_PX - 0.01) small.push({text: t.textContent.trim().slice(0, 30), px});
  }
  const measured = [];
  for (const [kind, sel] of Object.entries(LINES))
    for (const e of s.querySelectorAll(sel)) measured.push({kind, text: e.textContent.trim().slice(0, 40), lines: lines(e)});
  out.push({n: i + 1, title: s.getAttribute('data-title') || '', zoom,
            overflowY: Math.round((bottom - top) / k - limit), overflowX: Math.round((right - edge) / k), small, lines: measured});
}
return out;
"""

RUNBOOK_PROBE = r"""
for (const [gid, code] of Object.entries(CODES)) {
  const form = document.querySelector('.rb-lock[data-group="' + gid + '"] form');
  if (!form) continue;
  form.querySelector('input').value = code; form.requestSubmit(); await sleep(80);
}
const locked = [...document.querySelectorAll('.rb-lock-form')].map(f => f.closest('[data-page]')?.getAttribute('data-page'));
document.querySelectorAll('.rb-page, .rb-step').forEach(e => { e.hidden = false; });
await sleep(50);
const paras = [];
for (const p of document.querySelectorAll('.rb-page-body > p, .rb-step > p')) {
  if (!p.getClientRects().length || p.classList.contains('rb-block-label')) continue;
  const cs = getComputedStyle(p), fs = parseFloat(cs.fontSize), ls = parseFloat(cs.letterSpacing) || 0;
  paras.push({page: p.closest('[data-page]').getAttribute('data-page'), chars: +(p.clientWidth / (fs + ls)).toFixed(1),
              lh: +(parseFloat(cs.lineHeight) / fs).toFixed(2), text: p.textContent.trim().slice(0, 30)});
}
const small = [], seen = new Set();
const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
for (let t; (t = walk.nextNode());) {
  const e = t.parentElement;
  if (!t.textContent.trim() || seen.has(e) || !e.getClientRects().length) continue;
  seen.add(e);
  const px = parseFloat(getComputedStyle(e).fontSize);
  if (px < MIN_PX - 0.01) small.push({text: t.textContent.trim().slice(0, 30), px, cls: e.tagName.toLowerCase() + "." + (e.className || e.parentElement.className)});
}
return {locked, paras, small};
"""


def wrap(body: str, min_px: int, extra: str = "") -> str:
    """Probe <script>: runs `body` after load, then replaces the DOM with the JSON report (small --dump-dom)."""
    return ("<script>window.addEventListener('load', () => setTimeout(async () => {"
            "const sleep = ms => new Promise(r => setTimeout(r, ms)); const MIN_PX = " + str(min_px) + ";" + extra +
            "let report; try { report = await (async () => {" + body + "})(); } catch (e) { report = {error: String(e)}; }"
            "document.documentElement.innerHTML = '<body><pre id=\"typo-report\"></pre></body>';"
            "document.getElementById('typo-report').textContent = JSON.stringify(report);"
            "}, 400));</script>")


def probe(page: Path, script: str, size: str, work: Path) -> subprocess.Popen:
    target = work / (page.parent.parent.name + "-" + page.name)
    head, _, tail = page.read_text(encoding="utf-8").rpartition("</body>")
    target.write_text(head + script + "</body>" + tail, encoding="utf-8")
    browser = next(p for p in BROWSERS if p.exists())
    return subprocess.Popen([str(browser), "--headless", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
                             "--disable-background-networking", "--allow-file-access-from-files",
                             "--hide-scrollbars", "--force-device-scale-factor=1",
                             f"--window-size={size}", "--virtual-time-budget=120000", "--dump-dom",
                             "--user-data-dir=" + str(work / ("profile-" + target.stem)), target.as_uri()],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8",
                            errors="replace", creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))


def report_of(proc: subprocess.Popen) -> dict | list:
    out, err = proc.communicate(timeout=120)
    m = re.search(r'<pre id="typo-report">(.*?)</pre>', out, re.S)
    if not m:
        raise RuntimeError("browser produced no report: " + err[-1500:])
    data = json.loads(html.unescape(m.group(1)))
    if isinstance(data, dict) and "error" in data:
        raise RuntimeError("probe failed: " + data["error"])
    return data


def deck_problems(edition: str, slides: list[dict]) -> list[str]:
    out = []
    for s in slides:
        at = f"{edition} deck #{s['n']} 「{s['title']}」"
        if s["zoom"] < 1:
            out.append(f"{at}: fit-zoom {s['zoom']:.2f} < 1 (content too tall)")
        if s["overflowY"] > 1 or s["overflowX"] > 1:
            out.append(f"{at}: overflow {s['overflowY']}px down / {s['overflowX']}px right")
        out += [f"{at}: text {t['px']:g}px < {SLIDE_MIN_PX}px 「{t['text']}」" for t in s["small"]]
        out += [f"{at}: {m['kind']} {m['lines']} lines > {MAX_LINES[m['kind']]} 「{m['text']}」"
                for m in s["lines"] if m["lines"] > MAX_LINES[m["kind"]]]
    return out


def runbook_problems(edition: str, report: dict) -> list[str]:
    out = [f"{edition} runbook: page {p} still locked" for p in report["locked"]]
    widths: dict[str, set] = {}
    for p in report["paras"]:
        if not MEASURE[0] <= p["chars"] <= MEASURE[1]:
            widths.setdefault(p["page"], set()).add(p["chars"])
        if p["lh"] < MIN_LINE_HEIGHT:
            out.append(f"{edition} runbook {p['page']}: line-height {p['lh']} < {MIN_LINE_HEIGHT} 「{p['text']}」")
    out += [f"{edition} runbook {page}: {sorted(c)} CJK chars per line, want {MEASURE[0]}–{MEASURE[1]}"
            for page, c in widths.items()]
    seen = set()
    for t in report["small"]:
        key = (t["cls"], t["px"])
        if key not in seen:  # one line per styled element class, not per occurrence
            seen.add(key)
            out.append(f"{edition} runbook: text {t['px']:g}px < {RUNBOOK_MIN_PX}px ({t['cls']}) 「{t['text']}」")
    return out


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        jobs = []
        for edition, base in EDITIONS.items():
            codes = {g["id"]: g["code"] for g in json.loads((base / "unlock-codes.json").read_text(encoding="utf-8"))["groups"]}
            jobs.append((edition, deck_problems, probe(base / "facilitator-deck/facilitator-deck.html",
                                                       wrap(DECK_PROBE, SLIDE_MIN_PX, f"const CONTENT_W = {CONTENT_W};"), "1920,1080", work)))
            jobs.append((edition, runbook_problems, probe(base / "participant-runbook/runbook.html",
                                                          wrap(RUNBOOK_PROBE, RUNBOOK_MIN_PX, "const CODES = " + json.dumps(codes) + ";"),
                                                          "1440,900", work)))
        found = [line for edition, check, proc in jobs for line in check(edition, report_of(proc))]
    print("\n".join(found) or "TYPOGRAPHY PASS")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
