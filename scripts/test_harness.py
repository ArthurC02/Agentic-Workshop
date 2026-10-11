import importlib.util
import tempfile
import unittest
from pathlib import Path

import sync_harness

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("guard_generated", ROOT / ".claude/hooks/guard_generated.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class GuardTest(unittest.TestCase):
    def test_blocks_generated_files_only(self):
        blocked = ["agentic-workshop/materials/participant-runbook/runbook.html",
                   str(ROOT / "agentic-workshop/materials-dlc/facilitator-deck/facilitator-deck.html"),
                   "agentic-workshop\\materials\\speech\\01-greenfield\\greenfield-handout.md",
                   "dist/materials/participant-materials.zip",
                   "agentic-workshop/06-runbook/evaluation/p11-validation-logs/b1-pytest.log",
                   "agentic-workshop/06-runbook/evaluation/consistency-package-validation-evidence.json"]
        allowed = ["agentic-workshop/materials/participant-runbook/content/10-greenfield.md",
                   "agentic-workshop/materials/facilitator-deck/src/slides/20-greenfield.html",
                   "agentic-workshop/06-runbook/evaluation/consistency-correction-report.md",
                   "Agent.md", "docs/dist-notes.md"]
        for path in blocked:
            self.assertTrue(guard.blocked({"file_path": path}), path)
        for path in allowed:
            self.assertFalse(guard.blocked({"file_path": path}), path)

    def test_codex_patch(self):
        patch = "*** Begin Patch\n*** Update File: agentic-workshop/materials/participant-runbook/runbook.html\n@@\n"
        self.assertTrue(guard.blocked({"command": patch}))
        self.assertFalse(guard.blocked({"command": patch.replace("runbook.html", "content/00-welcome.md")}))


class SyncTest(unittest.TestCase):
    def test_sync_and_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".claude/skills/a").mkdir(parents=True)
            (root / ".claude/skills/a/SKILL.md").write_bytes(b"new\r\n")
            (root / ".claude/hooks").mkdir()
            (root / ".claude/hooks/guard_generated.py").write_bytes(b"hook")
            self.assertEqual(sync_harness.main(["--check"], root), 0)  # no mirrors in this clone: skipped
            (root / ".agents/skills/a").mkdir(parents=True)
            (root / ".agents/skills/a/SKILL.md").write_bytes(b"old\n")
            (root / ".agents/skills/stale.md").write_bytes(b"x")
            (root / ".codex").mkdir()
            self.assertEqual(sync_harness.main(["--check"], root), 1)
            self.assertEqual((root / ".agents/skills/a/SKILL.md").read_bytes(), b"old\n")  # --check changes nothing
            self.assertEqual(sync_harness.main([], root), 0)
            self.assertEqual((root / ".agents/skills/a/SKILL.md").read_bytes(), b"new\r\n")
            self.assertFalse((root / ".agents/skills/stale.md").exists())
            self.assertEqual((root / ".codex/hooks/guard_generated.py").read_bytes(), b"hook")
            self.assertEqual(sync_harness.main(["--check"], root), 0)


if __name__ == "__main__":
    unittest.main()
