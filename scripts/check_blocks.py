"""Check that every Runbook checkpoint uses the four blocks (course-authoring "Every segment page").

Each `## 檢查點 N · …` / `## 步驟 N · …` section has block labels ① ② ③ (④ optional) in order, a ```text (or OS-tabbed ```prompt)
prompt under ③ asking for 「成功」／「失敗」, and a 「失敗時」 rescue prompt.
Run: uv run --no-project --python 3.13 python -X utf8 scripts/check_blocks.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = [ROOT / "agentic-workshop/materials/participant-runbook/content",
           ROOT / "agentic-workshop/materials-dlc/participant-runbook/content"]
HEAD = re.compile(r"(?m)^(## (?:檢查點|步驟) \d+ · .*)$")


def sections(text: str):
    """Yield (heading, body) per checkpoint; `## ` lines inside ``` fences don't end a section."""
    head, body, fenced = None, [], False
    for line in text.splitlines():
        if line.startswith("```"):
            fenced = not fenced
        if not fenced and line.startswith("## "):
            if head:
                yield head, "\n".join(body)
            head, body = (line if HEAD.match(line) else None), []
        elif head:
            body.append(line)
    if head:
        yield head, "\n".join(body)


def problems(text: str) -> list[str]:
    out = []
    for head, body in sections(text):
        labels = re.findall(r"(?m)^([①②③④]) ", body)
        check = re.search(r"(?ms)^③ .*?```(?:text|prompt)\n(.*?)```", body)
        if labels[:3] != ["①", "②", "③"] or labels != sorted(set(labels)):
            out.append(f"{head}: block labels {labels}, want ① ② ③ (④) in order")
        elif not (check and "成功" in check.group(1) and "失敗" in check.group(1)):
            out.append(f"{head}: ③ needs a ```text／```prompt prompt asking for 「成功」／「失敗」")
        elif "失敗時" not in body:
            out.append(f"{head}: no 「失敗時」 rescue prompt")
    return out


if __name__ == "__main__":
    found = [f"{p.relative_to(ROOT).as_posix()}: {m}" for folder in CONTENT
             for p in sorted(folder.glob("*.md")) for m in problems(p.read_text(encoding="utf-8"))]
    print("\n".join(found) or "BLOCKS PASS")
    sys.exit(1 if found else 0)
