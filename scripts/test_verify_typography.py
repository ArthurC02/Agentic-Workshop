import unittest

import verify_typography as vt

SLIDE = {"n": 3, "title": "檢查點 1 · 做事", "zoom": 1, "overflowY": -20, "overflowX": 0, "small": [],
         "lines": [{"kind": "title", "text": "做事", "lines": 2}, {"kind": "main", "text": "貼 ②", "lines": 1},
                   {"kind": "detail", "text": "Runbook", "lines": 2}]}


class DeckProblems(unittest.TestCase):
    def test_within_limits_pass(self):
        self.assertEqual(vt.deck_problems("main", [SLIDE]), [])

    def test_each_limit_reported(self):
        bad = dict(SLIDE, zoom=0.85, overflowX=12, small=[{"text": "NOW", "px": 18}],
                   lines=[{"kind": "main", "text": "貼 ②", "lines": 2}, {"kind": "why", "text": "因為", "lines": 2}])
        found = vt.deck_problems("dlc", [bad])
        self.assertEqual(len(found), 5)
        self.assertTrue(all(f.startswith("dlc deck #3") for f in found))

    def test_orphan_reported(self):
        self.assertEqual(len(vt.deck_problems("main", [dict(SLIDE, orphans=["實作工作坊"])])), 1)


class RunbookProblems(unittest.TestCase):
    def test_measure_line_height_and_small_text(self):
        report = {"locked": [], "small": [{"text": "a", "px": 11, "cls": "code."}, {"text": "b", "px": 11, "cls": "code."}],
                  "paras": [{"page": "b1", "chars": 36, "lh": 1.8, "text": "好"},
                            {"page": "b2", "chars": 47.1, "lh": 1.8, "text": "寬"},
                            {"page": "b2", "chars": 36, "lh": 1.6, "text": "擠"}]}
        found = vt.runbook_problems("main", report)
        self.assertEqual(len(found), 3)  # b2 too wide, b2 line-height, one small-text class
        self.assertEqual(vt.runbook_problems("main", dict(report, small=[], paras=report["paras"][:1])), [])

    def test_orphan_reported(self):
        report = {"locked": [], "paras": [], "small": [], "orphans": [{"where": "b1", "text": "第 2 題。"}]}
        self.assertEqual(vt.runbook_problems("main", report), ["main runbook b1: orphan last line 「…第 2 題。」"])

    def test_sidebar_orphan_reported(self):
        report = {"locked": [], "paras": [], "small": [], "orphans": [{"where": "sidebar", "text": "2 · 規定只有夥伴核准才算數"}]}
        self.assertEqual(vt.runbook_problems("dlc", report), ["dlc runbook sidebar: orphan last line 「…2 · 規定只有夥伴核准才算數」"])

    def test_probe_walks_sidebar(self):  # the sidebar is an <aside>; only deck notes are skipped
        self.assertIn("aside:not(.rb-sidebar)", vt.ORPHANS_JS)
        self.assertIn(".rb-sidebar", vt.RUNBOOK_PROBE)

    def test_locked_page_reported(self):
        self.assertEqual(len(vt.runbook_problems("dlc", {"locked": ["d1"], "paras": [], "small": []})), 1)


if __name__ == "__main__":
    unittest.main()
