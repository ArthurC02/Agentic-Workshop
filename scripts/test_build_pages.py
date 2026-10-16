import tempfile
import unittest
from pathlib import Path

import build_pages


class BuildPagesTest(unittest.TestCase):
    def test_leaks_finds_codes_case_insensitively(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            (site / "a").mkdir()
            (site / "a" / "deck.html").write_text("<p>輸入 g0-start-07</p>", encoding="utf-8")
            (site / "clean.html").write_text("<p>nothing</p>", encoding="utf-8")
            self.assertEqual(build_pages.leaks(site, ["G0-START-07"]), ["a/deck.html: G0-START-07"])

    def test_build_publishes_no_facilitator_deck_or_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "_site"
            build_pages.build(out)
            pages = {p.relative_to(out).as_posix() for p in out.rglob("*.html")}
            self.assertIn("index.html", pages)
            self.assertIn("materials-dlc/participant-runbook/runbook.html", pages)
            self.assertFalse(any("facilitator" in p for p in pages))
            self.assertEqual(build_pages.leaks(out, build_pages.unlock_codes()), [])


if __name__ == "__main__":
    unittest.main()
