"""Check that every knowledge-point callout in the learner Runbooks cites a verified source.

Rules (see .claude/skills/course-authoring/references.md):
- every ```callout whose title starts with 技巧／新概念 contains a 📖 line;
- every 〈title〉 in a 📖 line appears in references.md, and no retired title is used;
- a page introduces at most MAX_NEW knowledge points.
Run: uv run --no-project --python 3.13 python -X utf8 scripts/check_references.py
"""
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / ".claude/skills/course-authoring/references.md"
CONTENT = [ROOT / "agentic-workshop/materials/participant-runbook/content",
           ROOT / "agentic-workshop/materials-dlc/participant-runbook/content"]
TITLE = re.compile(r"〈([^〉]+)〉")
PLUGIN_ZIP = next((ROOT / "agentic-workshop/07-dlc-ddd/participant/vendor").glob("domain-memory-*.zip"), None)
MAX_NEW = 3  # course-authoring: at most 3 new points per page; 加深一層 callouts revisit and don't count
PLUGIN_DOC = re.compile(r"`(?:vendor/)?domain-memory/references/([\w-]+\.md)`")


def plugin_headings() -> dict[str, set[str]]:
    """Section headings of each plugin reference doc shipped in the learner package."""
    if not PLUGIN_ZIP:
        return {}
    with zipfile.ZipFile(PLUGIN_ZIP) as z:
        return {Path(n).name: {h.strip() for h in re.findall(r"^#+\s*(.+)$", z.read(n).decode("utf-8"), re.M)}
                for n in z.namelist() if "/references/" in n and n.endswith(".md")}


def course_titles() -> set[str]:
    """H1 headings and frontmatter titles of course documents, for 「📖 定義出處：本課程〈…〉」."""
    titles = set()
    for doc in (ROOT / "agentic-workshop").rglob("*.md"):
        if "evaluation" in doc.parts or "repository" in doc.parts:
            continue
        text = doc.read_text(encoding="utf-8", errors="ignore")
        titles |= {t.strip() for t in re.findall(r"^(?:# |title: )(.+)$", text, re.M)}
    return titles


def allowed_and_retired(text: str) -> tuple[set[str], set[str]]:
    allowed, retired = set(), set()
    for line in text.splitlines():
        cells = line.split("|")
        if len(cells) >= 4 and line.startswith("|"):  # table row: | topic | cite | retired |
            allowed |= set(TITLE.findall(cells[2]))
            retired |= set(TITLE.findall(cells[3]))
        else:
            allowed |= set(TITLE.findall(line))
    return allowed - retired, retired


def problems() -> list[str]:
    allowed, retired = allowed_and_retired(REFS.read_text(encoding="utf-8"))
    headings = plugin_headings()
    course = course_titles()
    out = []
    for folder in CONTENT:
        for page in sorted(folder.glob("*.md")):
            text = page.read_text(encoding="utf-8")
            where = page.relative_to(ROOT).as_posix()
            new_points = []
            for m in re.finditer(r"```callout[^\n]*\n(.*?)```", text, re.S):
                title = m.group(1).split("\n", 1)[0].strip()
                if re.match(r"(技巧|新概念)", title) and "📖" not in m.group(1):
                    out.append(f"{where}: 「{title}」 has no 📖 reference")
                if re.match(r"(技巧|新概念)", title) and "加深一層" not in title:
                    new_points.append(title)
            if len(new_points) > MAX_NEW:
                out.append(f"{where}: {len(new_points)} new knowledge points (max {MAX_NEW}): {'、'.join(new_points)}")
            for line in re.findall(r"📖[^\n]*", text):
                docs = PLUGIN_DOC.findall(line)
                for doc in docs:
                    if doc not in headings:
                        out.append(f"{where}: plugin doc {doc} not in the vendored package")
                sections = set().union(*(headings.get(d, set()) for d in docs))
                own = line.startswith("📖 定義出處")
                for t in TITLE.findall(line):
                    if t in sections:
                        continue
                    if own:
                        if t not in course:
                            out.append(f"{where}: course document title 〈{t}〉 not found")
                        continue
                    if t in retired:
                        out.append(f"{where}: retired title 〈{t}〉")
                    elif t not in allowed:
                        out.append(f"{where}: unverified title 〈{t}〉")
        glossary = folder / "88-glossary.md"
        where = glossary.relative_to(ROOT).as_posix()
        for row in glossary.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            if not row.startswith("|") or len(cells) < 2 or set(cells[0]) <= set("-: ") or "出處" in cells:
                continue  # not a table row, a separator, or the header
            source = cells[-1]
            if not (TITLE.search(source) or PLUGIN_DOC.search(source)):
                out.append(f"{where}: glossary term 「{cells[0]}」 has no source in its last column")
                continue
            sections = set().union(*(headings.get(d, set()) for d in PLUGIN_DOC.findall(source)))
            for t in TITLE.findall(source):
                if t in sections or t in allowed or ("本課程" in source and t in course):
                    continue
                out.append(f"{where}: glossary term 「{cells[0]}」 cites unverified 〈{t}〉")
    return out


if __name__ == "__main__":
    found = problems()
    print("\n".join(found) or "REFERENCES PASS")
    sys.exit(1 if found else 0)
