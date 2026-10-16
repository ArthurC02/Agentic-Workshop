"""Assemble the GitHub Pages site in _site/: learner Runbooks, built speech decks and an index.

Facilitator decks carry unlock codes; they are published too, but the index links them only
with ?role=admin. That hides them from learners, it does not protect them (the repo is public).
The build fails if an unlock code appears in any other page.
Preview: python scripts/build_pages.py && python -m http.server -d _site
"""
from html import escape
from pathlib import Path
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
WORKSHOP = ROOT / "agentic-workshop"
OUT = ROOT / "_site"
EDITIONS = (("materials", "主課程"), ("materials-dlc", "DDD 延伸課（DLC）"))

STYLE = """
:root{--bg:#f7f7f5;--card:#fff;--fg:#1d1d1f;--muted:#5f6368;--line:#dcdcd7;--accent:#0b57d0;--on-accent:#fff}
@media (prefers-color-scheme:dark){:root{--bg:#141414;--card:#1f1f1f;--fg:#ececec;--muted:#a0a0a0;--line:#333;--accent:#8ab4f8;--on-accent:#0b1b33}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,"Noto Sans TC","Microsoft JhengHei",sans-serif}
main{max-width:760px;margin:0 auto;padding:40px 16px 64px}
h1{font-size:1.8rem;margin:0 0 4px}
.lead{color:var(--muted);margin:0 0 32px}
section{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:24px;margin-bottom:24px}
h2{font-size:1.3rem;margin:0 0 16px}
h3{font-size:1rem;color:var(--muted);margin:24px 0 8px}
.cta{display:block;background:var(--accent);color:var(--on-accent);text-decoration:none;font-weight:600;padding:14px 18px;border-radius:8px}
.cta:hover,.cta:focus-visible{filter:brightness(1.1)}
ol{list-style:none;margin:0;padding:0}
li{display:flex;gap:12px;align-items:baseline;padding:10px 0;border-top:1px solid var(--line)}
li:first-child{border-top:0}
.n{color:var(--muted);font-variant-numeric:tabular-nums}
li a{color:var(--fg);flex:1}
.meta{color:var(--muted);font-size:.875rem;white-space:nowrap}
.admin{display:block;margin-top:24px;padding:12px 18px;border:1px dashed var(--accent);border-radius:8px;color:var(--accent);font-weight:600;text-decoration:none}
.admin[hidden]{display:none}
"""
ADMIN_SCRIPT = ("<script>if(new URLSearchParams(location.search).get('role')==='admin')"
                "document.querySelectorAll('.admin').forEach(a=>a.hidden=false)</script>")


def collect(folder):
    """Return (runbook, [(deck, stage_meta)]) for one edition."""
    base = WORKSHOP / folder
    decks = []
    for stage in sorted(base.glob("speech/*/src/stage.json")):
        meta = json.loads(stage.read_text(encoding="utf-8"))
        deck = stage.parent.parent / meta["deck"]
        if not deck.exists():  # ponytail: an unbuilt stage simply stays off the site
            continue
        decks.append((deck, meta))
    return base / "participant-runbook" / "runbook.html", decks, base / "facilitator-deck" / "facilitator-deck.html"


def leaks(site, codes):
    """Unlock codes found in published learner HTML (facilitator decks excluded), as 'path: code' strings."""
    found = []
    for page in sorted(site.rglob("*.html")):
        if "facilitator-deck" in page.parts:
            continue
        text = page.read_text(encoding="utf-8").upper()
        found += [f"{page.relative_to(site).as_posix()}: {c}" for c in codes if c.upper() in text]
    return found


def unlock_codes():
    codes = []
    for folder, _ in EDITIONS:
        data = json.loads((WORKSHOP / folder / "unlock-codes.json").read_text(encoding="utf-8"))
        codes += [g["code"] for g in data["groups"]]
    return codes


def section(label, runbook, decks, facilitator):
    rel = lambda p: escape(p.relative_to(WORKSHOP).as_posix())
    items = []
    for i, (deck, meta) in enumerate(decks, 1):
        items.append(f'<li><span class="n">{i:02d}</span><a href="{rel(deck)}" target="_blank">{escape(meta["title"])}</a>'
                     f'<span class="meta">{meta["minutes"]} 分鐘</span></li>')
    talks = f'<h3>演講簡報（照上課順序）</h3><ol>{"".join(items)}</ol>' if items else ""
    return (f'<section><h2>{escape(label)}</h2>'
            f'<a class="cta" href="{rel(runbook)}" target="_blank">學員 Runbook：{escape(label)} →</a>{talks}'
            f'<a class="admin" hidden href="{rel(facilitator)}" target="_blank">主持簡報：{escape(label)} →</a></section>')


def build(out=OUT):
    if out.exists():
        shutil.rmtree(out)
    sections = []
    for folder, label in EDITIONS:
        runbook, decks, facilitator = collect(folder)
        for page in [runbook, facilitator] + [d for d, _ in decks]:
            target = out / page.relative_to(WORKSHOP)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(page, target)
        sections.append(section(label, runbook, decks, facilitator))
    found = leaks(out, unlock_codes())
    if found:
        shutil.rmtree(out)
        sys.exit("Unlock codes would be published:\n" + "\n".join(found))
    (out / "index.html").write_text(
        '<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>Smart Ticket 工作坊</title><style>{STYLE}</style></head><body><main>'
        '<h1>Smart Ticket 工作坊</h1>'
        '<p class="lead">和 Coding Agent 一起從零做出系統、接手舊系統。先選你參加的課程，再打開學員 Runbook。</p>'
        f'{"".join(sections)}</main>{ADMIN_SCRIPT}</body></html>\n', encoding="utf-8")
    print(f"Built {sum(1 for _ in out.rglob('*.html'))} pages in {out}")


if __name__ == "__main__":
    build()
