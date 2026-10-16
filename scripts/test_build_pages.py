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

    def test_leaks_skips_facilitator_decks(self):
        with tempfile.TemporaryDirectory() as tmp:
            deck = Path(tmp) / "materials" / "facilitator-deck" / "facilitator-deck.html"
            deck.parent.mkdir(parents=True)
            deck.write_text("G0-START-07", encoding="utf-8")
            self.assertEqual(build_pages.leaks(Path(tmp), ["G0-START-07"]), [])

    def test_build_hides_facilitator_links_and_keeps_learner_pages_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "_site"
            build_pages.build(out)
            pages = {p.relative_to(out).as_posix() for p in out.rglob("*.html")}
            self.assertIn("materials-dlc/participant-runbook/runbook.html", pages)
            self.assertIn("materials/facilitator-deck/facilitator-deck.html", pages)
            index = (out / "index.html").read_text(encoding="utf-8")
            self.assertEqual(index.count('class="admin" hidden'), 2)
            self.assertEqual(build_pages.leaks(out, build_pages.unlock_codes()), [])


if __name__ == "__main__":
    unittest.main()
