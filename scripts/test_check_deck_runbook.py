import unittest

import check_deck_runbook as cd

PLAN = (("seg", 0, 10, "段"),)
PAGE = ("---\nid: p\ntitle: 任務：甲\nminute: 00-10\ngroup: seg\n---\n\n"
        "## 檢查點 1 · 先做（第 0–4 分鐘）\n\n## 檢查點 2 · 再做（第 4–10 分鐘）\n\n## 甲決定\n\n"
        '```form\n{"id": "f", "title": "甲決定（T-1）", "fields": []}\n```\n')


def slide(n, name, total, a, b, nxt, extra=""):
    return (f'<section class="slide" data-seg="seg" data-title="檢查點 {n} · {name}">'
            f'<p class="kicker">檢查點 {n} / {total} · 第 {a}–{b} 分鐘</p><h2 class="title">{name}</h2>'
            f'<p class="cp-next">{nxt}</p>{extra}<aside class="notes"><p>說</p></aside></section>\n')


GOOD = (slide(1, "先做", 2, "00", "04", "第 4 分前完成 → 下一步：檢查點 2 再做", "<li>Runbook『任務』› 檢查點 1</li>")
        + slide(2, "再做", 2, 4, 10, "第 10 分前在「甲決定」選 → 下一步：Runbook『任務：甲』"))


def run(slides=GOOD, page=PAGE, md=None):
    return cd.problems([cd.parse_page("p.md", page)], cd.parse_slides("s.html", slides), PLAN, md)


class Problems(unittest.TestCase):
    def test_matching_deck_passes(self):
        self.assertEqual(run(), [])

    def test_missing_and_extra_checkpoint_slides(self):
        self.assertEqual(len(run(GOOD.replace("檢查點 2 · 再做", "檢查點 3 · 再做"))), 2)

    def test_kicker_title_and_deadline(self):
        self.assertEqual(len(run(GOOD.replace("檢查點 2 / 2", "檢查點 2 / 3"))), 1)
        self.assertEqual(len(run(GOOD.replace('<h2 class="title">再做', '<h2 class="title">別做'))), 1)
        self.assertEqual(len(run(GOOD.replace("第 4 分前完成", "第 5 分前完成"))), 1)
        # The footer may wrap its deadline and next step in inline tags (zoned checkpoint layout).
        self.assertEqual(run(GOOD.replace("第 4 分前完成 → 下一步：檢查點 2 再做",
                                          "<b>第 4 分前完成</b><span>→ 下一步：檢查點 2 再做</span>")), [])
        self.assertEqual(len(run(GOOD.replace("第 4 分前完成 → 下一步：檢查點 2 再做",
                                              "<b>第 4 分前完成</b><span>→ 下一步：檢查點 2 偷做</span>"))), 1)

    def test_next_step_and_page_references(self):
        self.assertEqual(len(run(GOOD.replace("檢查點 2 再做", "檢查點 2 偷做"))), 1)
        # （…） glosses are stripped from both the footer label and the Runbook name.
        glossed = GOOD.replace("再做", "再做（Port）邊界")
        self.assertEqual(run(glossed, PAGE.replace("再做（第", "再做（Port）邊界（第")), [])
        self.assertEqual(len(run(GOOD.replace("『任務』› 檢查點 1", "『任務』› 檢查點 9"))), 1)
        self.assertEqual(len(run(GOOD.replace("『任務：甲』", "『任務：乙』"))), 1)

    def test_form_names(self):
        self.assertEqual(len(run(GOOD.replace("「甲決定」", "「乙決定」"))), 1)

    def test_projected_file_must_be_in_runbook(self):
        bad = GOOD.replace("<li>Runbook", "<li>skills/old.md</li><li>Runbook", 1)
        self.assertEqual(len(run(bad)), 1)
        self.assertIn("skills/old.md", run(bad)[0])

    def test_layout_limits(self):
        self.assertEqual(cd.width("貼 ③ ab"), 4)
        ok = ('<p class="cp-why"><b>為什麼</b>' + "字" * 30 + '</p><p class="cp-judge"><b>你要判斷</b>' + "字" * 36
              + '</p><ol class="cp-flow"><li><b>' + "字" * 13 + "ab</b><span>" + "字" * 24 + "</span></li></ol>")
        self.assertEqual(run(GOOD.replace("<li>Runbook", ok + "<li>Runbook", 1)), [])
        for old, new in (("字" * 30 + "<", "字" * 31 + "<"), ("字" * 36 + "<", "字" * 37 + "<"),
                         ("ab</b>", "abc</b>"), ("字" * 24 + "</span>", "字" * 25 + "</span>")):
            self.assertEqual(len(run(GOOD.replace("<li>Runbook", ok.replace(old, new, 1) + "<li>Runbook", 1))), 1, new)
        four = '<ol class="cp-flow">' + "<li><b>甲</b></li>" * 4 + "</ol>"
        self.assertEqual(run(GOOD.replace("<li>Runbook", four + "<li>Runbook", 1)), [])
        self.assertEqual(len(run(GOOD.replace("<li>Runbook", four.replace("</b></li>", "</b><span>乙</span></li>", 1)
                                              + "<li>Runbook", 1))), 1)

    def test_checkpoints_md(self):
        md = "## 甲（段落 `seg`）\n\n1. 檢查點 1 · 先做（第 0–4 分鐘）\n2. 檢查點 2 · 再做（第 4–10 分鐘）\n"
        self.assertEqual(run(md=md), [])
        self.assertEqual(len(run(md=md.replace("再做", "別做"))), 2)


if __name__ == "__main__":
    unittest.main()
