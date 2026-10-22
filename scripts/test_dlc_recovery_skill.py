"""The dlc-recovery Skill carries Recovery step 1 (the Agent runs it before RECOVERY.md is unpacked); it must
stay identical to make_recovery's SAVE_PS／SAVE_SH, and every RECOVERY.md must match its template."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECOVERY = ROOT / "agentic-workshop/07-dlc-ddd/facilitator/recovery"
sys.path.insert(0, str(RECOVERY))
import make_recovery as mr  # noqa: E402

SKILL = (ROOT / "agentic-workshop/07-dlc-ddd/participant/skills/dlc-recovery/SKILL.md").read_text(encoding="utf-8")


class DlcRecoverySkill(unittest.TestCase):
    def test_step1_scripts_match(self):
        self.assertIn(mr.SAVE_PS.format(seg="SEG"), SKILL)
        self.assertIn(mr.subshell(mr.SAVE_SH.format(seg="SEG")), SKILL)

    def test_recovery_md_matches_template(self):
        for seg, (solution, message) in mr.SEGMENTS.items():
            text = (RECOVERY / seg / "RECOVERY.md").read_text(encoding="utf-8")
            self.assertEqual(text, mr.recovery_md(seg, solution, message), seg)


if __name__ == "__main__":
    unittest.main()
