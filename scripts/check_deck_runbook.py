"""Check that the facilitator deck and the participant Runbook fit together (course-authoring 「Facilitator deck」).

Per edition (main, dlc):
1. Every Runbook `## 檢查點 N · 名稱（第 a–b 分鐘）` has exactly one slide `data-title="檢查點 N · 名稱"` in the
   segment whose plan minutes contain a, with `<h2>` 名稱 and kicker `檢查點 N / 總數 · 第 a–b 分鐘`;
   no checkpoint slide lacks a Runbook checkpoint. DLC: CHECKPOINTS.md lists the same checkpoints.
2. Runbook pages named on slides (`Runbook『…』`, `打開『…』`, `『…』›`, `『…』頁`) exist (title, its short form
   before 「：」／space, or a `## ` section); `『頁』› 檢查點 n` and `Runbook › 檢查點 n` exist.
3. Footer `cp-next` and opening timeline deadlines fall inside the checkpoint (`第 x 分前完成` must be b);
   a 「下一步：檢查點 m …」 names the next checkpoint and a prefix of its Runbook name.
   Checkpoint slides stay readable (user rule, 2026-10-11; width counts CJK as 1, ASCII as ½):
   為什麼 ≤ 30, 你要判斷 ≤ 36, at most 4 step cards (4 only when none has a detail line),
   card main line ≤ 14 and detail ≤ 24.
4. A form named on a slide (「X」 followed by 選／記／勾／填／表單) is a form title (minus （…）), page title or
   `## ` section of a Runbook page in that segment.
Unlock slides vs unlock-codes.json (group and minute) are already checked by build_materials.validate_slides.
Run: uv run --no-project --python 3.13 python -X utf8 scripts/check_deck_runbook.py
"""
import html
import re
import sys
from pathlib import Path

from build_materials import load_edition
from check_blocks import sections

ROOT = Path(__file__).resolve().parents[1]
CP = re.compile(r"## 檢查點 (\d+) · (.+)（第 (\d+)–(\d+) 分鐘）$")
SECTION = re.compile(r'(?s)<section\b([^>]*)>(.*?)</section>')
PAGE_REF = re.compile(r"(?:Runbook\s*|打開\s*)『([^』]+)』|『([^』]+)』(?=\s*(?:›|頁))")
FORM_REF = re.compile(r"「([^」]+)」\s*(?=選|記|勾|填|表單)")
MINUTE = re.compile(r"第 ?(\d+) ?分(前完成)?")


LIMITS = {"why": 30, "judge": 36, "main": 14, "detail": 24}


FILE_REF = re.compile(r"[\w./{}-]*[\w}-]\.(?:md|json|py|sh|ps1|zip|txt|ya?ml)\b")


def text(markup: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", markup))


def width(s: str) -> float:
    """Visible width: ASCII counts half, everything else (CJK, full-width punctuation) one."""
    s = re.sub(r"\s+", " ", s).strip()
    return sum(0.5 if ord(c) < 128 else 1 for c in s)


def layout_problems(where: str, s: dict) -> list[str]:
    out = []
    for key, label in (("why", "為什麼"), ("judge", "你要判斷")):
        if s[key] and width(s[key]) > LIMITS[key]:
            out.append(f"{where}: {label} is {width(s[key]):g} wide (max {LIMITS[key]}): 「{s[key]}」")
    cards = s["cards"]
    if len(cards) > 4 or (len(cards) == 4 and any(d for _, d in cards)):
        out.append(f"{where}: {len(cards)} step cards; use at most 3 (4 only without detail lines)")
    for main, detail in cards:
        if width(main) > LIMITS["main"]:
            out.append(f"{where}: card main line is {width(main):g} wide (max {LIMITS['main']}): 「{main}」")
        if width(detail) > LIMITS["detail"]:
            out.append(f"{where}: card detail is {width(detail):g} wide (max {LIMITS['detail']}): 「{detail}」")
    return out


def parse_page(name: str, src: str) -> dict:
    meta = dict(re.findall(r"(?m)^(\w+): *(.*)$", src.split("\n---", 1)[0]))
    cps = [CP.match(h) for h, _ in sections(src)]
    cps = [(int(m[1]), m[2], int(m[3]), int(m[4])) for m in cps if m]
    return {"file": name, "src": src, "title": meta.get("title", ""), "start": int(meta.get("minute", "0").split("-")[0]),
            "cps": cps, "sections": set(re.findall(r"(?m)^## (.+?)\s*$", src)),
            "forms": {re.sub(r"（.*）$", "", t) for t in re.findall(r'"title":\s*"([^"]+)"', "".join(
                re.findall(r"(?s)```form\n(.*?)```", src)))}}


def parse_slides(name: str, src: str) -> list[dict]:
    out = []
    for attrs, body in SECTION.findall(src):
        a = dict(re.findall(r'([\w-]+)="([^"]*)"', attrs))
        notes = "".join(re.findall(r'(?s)<aside class="notes">(.*?)</aside>', body))
        shown = re.sub(r'(?s)<aside class="notes">.*?</aside>', "", body)
        grab = lambda cls: text("".join(b for _, b in re.findall(
            rf'(?s)<(\w+) class="{cls}"[^>]*>(.*?)</\1>', shown))).strip()
        labelled = lambda cls: re.sub(r"^\s*<b>[^<]*</b>", "", "".join(re.findall(
            rf'(?s)<p class="{cls}"[^>]*>(.*?)</p>', shown)))
        flow = "".join(re.findall(r'(?s)<ol class="cp-flow"[^>]*>(.*?)</ol>', shown))
        cards = [(text("".join(re.findall(r"(?s)<b>(.*?)</b>", li))),
                  text("".join(re.findall(r"(?s)<span>(.*?)</span>", li))))
                 for li in re.findall(r"(?s)<li(?=[\s>])[^>]*>(.*?)</li>", flow)]
        out.append({"where": f"{name} 「{a.get('data-title', '?')}」", "seg": a.get("data-seg"),
                    "why": text(labelled("cp-why")).strip(), "judge": text(labelled("cp-judge")).strip(),
                    "cards": cards,
                    "title": a.get("data-title", ""), "kicker": grab("kicker"), "h2": grab("title"),
                    "next": grab("cp-next"), "shown": text(re.sub(r"<", " <", shown)), "text": text(shown) + "\n" + text(notes),
                    "timeline": re.findall(r'(?s)<li data-seg="[^"]*">.*?<b>(\d+) · .*?</b>'
                                           r'<span class="tl-due">(.*?)</span>', shown)})
    return out


def segment_of(minute: int, plan) -> str | None:
    return next((seg for seg, start, end, _ in plan if start <= minute < end), None)


def deadline_problems(where: str, phrase: str, a: int, b: int) -> list[str]:
    m = MINUTE.search(phrase)
    if not m:
        return []
    x = int(m[1])
    if (m[2] and x != b) or not a < x <= b:
        return [f"{where}: deadline 「{m[0]}」 does not fit checkpoint 第 {a}–{b} 分鐘"]
    return []


def problems(pages: list[dict], slides: list[dict], plan, checkpoints_md: str | None = None) -> list[str]:
    out = []
    by_seg: dict[str, list[dict]] = {}
    cps: dict[tuple, tuple] = {}  # (seg, n) -> (name, a, b, total)
    for p in pages:
        seg = segment_of(p["cps"][0][2] if p["cps"] else p["start"], plan)
        by_seg.setdefault(seg, []).append(p)
        for n, name, a, b in p["cps"]:
            if (seg, n) in cps:
                out.append(f"{p['file']}: 檢查點 {n} duplicates another page in segment {seg}")
            cps[(seg, n)] = (name, a, b, len(p["cps"]))
    titles = {p["title"] for p in pages}
    all_sections = set().union(*(p["sections"] for p in pages)) if pages else set()

    def page_matches(ref: str, seg: str) -> list[dict]:
        hits = [p for p in pages if p["title"] == ref] or [
            p for p in pages if re.match(re.escape(ref) + r"[：: ]", p["title"])]
        return [p for p in hits if p in by_seg.get(seg, [])] or hits if len(hits) > 1 else hits

    runbook_src = "".join(p.get("src", "") for p in pages)
    claimed = set()
    for s in slides:
        seg, where = s["seg"], s["where"]
        out += layout_problems(where, s)
        m = re.fullmatch(r"檢查點 (\d+) · (.+)", s["title"])
        if m:
            n = int(m[1])
            if (seg, n) not in cps or cps[(seg, n)][0] != m[2]:
                out.append(f"{where}: no Runbook 檢查點 {n} · {m[2]} in segment {seg}")
            else:
                name, a, b, total = cps[(seg, n)]
                if (seg, n) in claimed:
                    out.append(f"{where}: second slide for 檢查點 {n} in segment {seg}")
                claimed.add((seg, n))
                k = re.fullmatch(r"檢查點 (\d+) / (\d+) · 第 (\d+)–(\d+) 分鐘", s["kicker"])
                if not k or tuple(map(int, k.groups())) != (n, total, a, b):
                    out.append(f"{where}: kicker 「{s['kicker']}」, want 「檢查點 {n} / {total} · 第 {a}–{b} 分鐘」")
                if s["h2"] != name:
                    out.append(f"{where}: <h2> 「{s['h2']}」 differs from Runbook name 「{name}」")
                out += deadline_problems(f"{where} footer", s["next"], a, b)
                nxt = re.search(r"下一步：.*?檢查點 (\d+) ?([^，。→]*)", s["next"])
                if nxt:
                    k, label = int(nxt[1]), re.sub(r"（.*?）", "", nxt[2]).strip()
                    target = cps.get((seg, k))
                    if k != n + 1 or not target:
                        out.append(f"{where}: 下一步 names 檢查點 {k}, want 檢查點 {n + 1} of segment {seg}")
                    elif label not in re.sub(r"（.*?）", "", target[0]):
                        out.append(f"{where}: 下一步 「{label}」 is not part of 「{target[0]}」")
        for n, due in s["timeline"]:
            if (seg, int(n)) not in cps:
                out.append(f"{where}: timeline lists 檢查點 {n}, missing in segment {seg}")
            else:
                _, a, b, _ = cps[(seg, int(n))]
                out += deadline_problems(f"{where} timeline {n}", due, a, b)
        if s["timeline"] and len(s["timeline"]) != sum(1 for k in cps if k[0] == seg):
            out.append(f"{where}: timeline has {len(s['timeline'])} checkpoints, Runbook segment {seg} has "
                       f"{sum(1 for k in cps if k[0] == seg)}")
        for m in PAGE_REF.finditer(s["text"]):
            ref = m[1] or m[2]
            hits = page_matches(ref, seg)
            if len(hits) != 1 and ref not in all_sections:
                out.append(f"{where}: 『{ref}』 is {'ambiguous' if hits else 'not a Runbook page or section'}")
            after = re.match(r"\s*›\s*檢查點 ?(\d+)", s["text"][m.end():])
            if after and len(hits) == 1 and int(after[1]) not in {c[0] for c in hits[0]["cps"]}:
                out.append(f"{where}: 『{ref}』 has no 檢查點 {after[1]}")
        for k in re.findall(r"Runbook\s*›\s*檢查點 ?(\d+)", s["text"]):
            if (seg, int(k)) not in cps:
                out.append(f"{where}: Runbook › 檢查點 {k} missing in segment {seg}")
        for f in sorted(set(FILE_REF.findall(s.get("shown", "")))):  # learners only know files the Runbook names
            if f not in runbook_src:
                out.append(f"{where}: projected file 「{f}」 is not mentioned in the Runbook")
        seg_pages = by_seg.get(seg, [])
        known = set().union(*(p["forms"] | p["sections"] | {p["title"]} for p in seg_pages)) if seg_pages else set()
        for ref in FORM_REF.findall(s["text"]):
            if ref.endswith(("決定", "確認", "核對", "對照", "回顧")) and ref not in known and ref not in titles:
                out.append(f"{where}: form 「{ref}」 is not a form, page or section of segment {seg}")
    for (seg, n), (name, *_r) in sorted(cps.items(), key=lambda kv: (str(kv[0][0]), kv[0][1])):
        if (seg, n) not in claimed:
            out.append(f"Runbook 檢查點 {n} · {name} (segment {seg}) has no matching slide")
    if checkpoints_md is not None:
        listed, seg = set(), None
        for line in checkpoints_md.splitlines():
            if line.startswith("## "):
                m = re.search(r"段落 `([^`]+)`", line)
                seg = m[1] if m else None
            m = re.match(r"\d+\. 檢查點 (\d+) · (.+)（第 (\d+)–(\d+) 分鐘）$", line)
            if m and seg:
                listed.add((seg, int(m[1]), m[2], int(m[3]), int(m[4])))
        runbook = {(seg, n, name, a, b) for (seg, n), (name, a, b, _t) in cps.items()}
        for row in sorted(runbook - listed, key=str):
            out.append(f"CHECKPOINTS.md lacks {row[0]} 檢查點 {row[1]} · {row[2]}（第 {row[3]}–{row[4]} 分鐘）")
        for row in sorted(listed - runbook, key=str):
            out.append(f"CHECKPOINTS.md lists {row[0]} 檢查點 {row[1]} · {row[2]}, not in the Runbook")
    return out


def check_edition(name: str) -> list[str]:
    ed = load_edition(name)
    content = ed.materials / "participant-runbook/content"
    pages = [parse_page(p.name, p.read_text(encoding="utf-8")) for p in sorted(content.glob("*.md"))]
    slides = [s for p in sorted((ed.materials / "facilitator-deck/src/slides").glob("*.html"))
              if not p.name.startswith("00-engine-demo") for s in parse_slides(p.name, p.read_text(encoding="utf-8"))]
    md = ed.materials / "CHECKPOINTS.md"
    return [f"{name}: {m}" for m in problems(pages, slides, ed.plan, md.read_text(encoding="utf-8")
                                                     if md.exists() else None)]


if __name__ == "__main__":
    editions = sys.argv[1:] or ["main", "dlc"]
    found = [m for e in editions for m in check_edition(e)]
    print("\n".join(found) or "DECK–RUNBOOK PASS")
    sys.exit(1 if found else 0)
