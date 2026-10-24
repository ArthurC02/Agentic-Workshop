"""Every Skill the course ships or tells the Agent to copy meets agentskills.io 〈Specification〉 (checked 2026-10-24):
frontmatter from line 1; name 1-64 chars of a-z 0-9 '-', no leading/trailing/double hyphen, equal to the folder name;
description 1-1024 chars; body under 500 lines.
Run: uv run --no-project --python 3.13 python -X utf8 -m unittest discover -s scripts -p test_skill_spec.py
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AW = ROOT / "agentic-workshop"
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def shipped() -> dict[str, str]:
    """folder name -> SKILL.md text, for every Skill the learner's Agent installs."""
    out = {p.parent.name: p.read_text(encoding="utf-8") for p in (AW / "07-dlc-ddd/participant/skills").glob("*/SKILL.md")}
    out["b3-work-order"] = (AW / "04-digital-worker/participant/b3-work-order.md").read_text(encoding="utf-8")
    guide = (AW / "01-greenfield/participant/04-agent-usage-guide.md").read_text(encoding="utf-8")
    out["check (main)"] = re.search(r"```markdown\n(---\nname: check\n.*?)```", guide, re.S).group(1)
    return out


def problems(folder: str, text: str) -> list[str]:
    folder = folder.split(" ")[0]
    lines = text.replace("\r\n", "\n").split("\n")
    if lines[0] != "---" or "---" not in lines[1:]:
        return ["frontmatter must start on line 1"]
    end = lines.index("---", 1)
    meta = dict(l.split(":", 1) for l in lines[1:end] if ":" in l and not l.startswith(" "))
    name, desc = meta.get("name", "").strip(), meta.get("description", "").strip()
    out = []
    if not (1 <= len(name) <= 64 and NAME.match(name)):
        out.append(f"name {name!r} breaks the naming rule")
    if name != folder:
        out.append(f"name {name!r} != folder {folder!r}")
    if not 1 <= len(desc) <= 1024:
        out.append(f"description length {len(desc)}")
    if len(lines) - end - 1 >= 500:
        out.append("body has 500 lines or more")
    return out


class SkillSpec(unittest.TestCase):
    def test_shipped_skills_meet_spec(self):
        skills = shipped()
        self.assertGreaterEqual(len(skills), 7)
        for folder, text in skills.items():
            with self.subTest(folder):
                self.assertEqual(problems(folder, text), [])

    def test_rule_catches_bad_names(self):
        self.assertTrue(problems("Bad--Name", "---\nname: Bad--Name\ndescription: x\n---\n"))
        self.assertTrue(problems("a", "---\nname: b\ndescription: x\n---\n"))
        self.assertTrue(problems("a", "\n---\nname: a\ndescription: x\n---\n"))
        self.assertEqual(problems("a-1", "---\nname: a-1\ndescription: x\n---\n"), [])


if __name__ == "__main__":
    unittest.main()
