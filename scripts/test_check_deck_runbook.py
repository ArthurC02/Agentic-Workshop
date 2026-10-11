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

    def test_next_step_and_page_references(self):
        self.assertEqual(len(run(GOOD.replace("檢查點 2 再做", "檢查點 2 偷做"))), 1)
        # （…） glosses are stripped from both the footer label and the Runbook name.
        glossed = GOOD.replace("再做", "再做（Port）邊界")
        self.assertEqual(run(glossed, PAGE.replace("再做（第", "再做（Port）邊界（第")), [])
        self.assertEqual(len(run(GOOD.replace("『任務』› 檢查點 1", "『任務』› 檢查點 9"))), 1)
        self.assertEqual(len(run(GOOD.replace("『任務：甲』", "『任務：乙』"))), 1)

    def test_form_names(self):
        self.assertEqual(len(run(GOOD.replace("「甲決定」", "「乙決定」"))), 1)

    def test_checkpoints_md(self):
        md = "## 甲（段落 `seg`）\n\n1. 檢查點 1 · 先做（第 0–4 分鐘）\n2. 檢查點 2 · 再做（第 4–10 分鐘）\n"
        self.assertEqual(run(md=md), [])
        self.assertEqual(len(run(md=md.replace("再做", "別做"))), 2)


if __name__ == "__main__":
    unittest.main()
