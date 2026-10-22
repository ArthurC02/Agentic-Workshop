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

    def test_sync_cues(self):
        cue = '<p class="sync-cue" data-sync="{}">⏸ 看投影</p>'
        stop = ('<section class="slide" data-seg="reveal" data-reveal-of="seg" data-title="請先停手" data-minute="10">'
                + cue.format("停手") + "</section>\n")
        unlock = ('<section class="slide" data-seg="seg" data-title="解鎖" data-minute="0" data-unlock="seg">'
                  + cue.format("解鎖碼") + "</section>\n")
        page = PAGE + "\n```callout sync\n⏸ 看投影：第 10 分鐘請先停手\n```\n"
        self.assertEqual(run(GOOD + stop + unlock, page), [])  # the unlock key is answered by the lock card
        self.assertEqual(len(run(GOOD + stop, PAGE)), 1)  # marked slide without a Runbook callout
        self.assertEqual(len(run(GOOD, page)), 1)  # Runbook callout without a marked slide
        self.assertEqual(len(run(GOOD + stop.replace('data-minute="10"', 'data-minute="11"'), page)), 2)  # out of window
        self.assertEqual(len(run(GOOD + stop.replace('data-sync="停手"', 'data-sync="揭曉"'), page)), 2)  # key not named
        self.assertEqual(len(run(GOOD + stop.replace(cue.format("停手"), ""), page)), 2)  # reveal slide unmarked
        self.assertEqual(len(run(GOOD + stop + unlock.replace(cue.format("解鎖碼"), ""), page)), 1)
        self.assertEqual(len(run(GOOD + stop.replace("⏸ 看投影</p>", "看簡報</p>"), page)), 1)
        self.assertEqual(len(run(GOOD + stop, page.replace("⏸ 看投影：", "看投影："))), 1)

    def test_checkpoints_md(self):
        md = "## 甲（段落 `seg`）\n\n1. 檢查點 1 · 先做（第 0–4 分鐘）\n2. 檢查點 2 · 再做（第 4–10 分鐘）\n"
        self.assertEqual(run(md=md), [])
        self.assertEqual(len(run(md=md.replace("再做", "別做"))), 2)


class B3Package(unittest.TestCase):
    WO = ("| 1 需求理解 |\n| 2 設計與修改範圍 |\n| 3 交付 |\n## 9. 時間\n第 66 分 Gate 1；第 69–70 分例外\n## 10. 交接\n第 99 分")
    CARD = "| 1 需求理解 |\n| 2 設計與修改範圍 |\n| 3 交付 |"
    PAGE = ("path=b3-docs/task-card.md\n第 64–66 分鐘、第 69 分鐘、第 70 分\nGate 1 需求理解 Gate 2 設計與修改範圍 "
            "Gate 3 交付\n讀 b3-docs/b3-work-order.md")
    DEST = {"b3-docs/task-card.md", "b3-docs/b3-work-order.md"}

    def test_consistent_package_passes(self):
        self.assertEqual(cd.b3_package_problems({"60-b3.md": self.PAGE}, self.DEST, self.WO, self.CARD), [])

    def test_missing_file_minute_and_gate_name(self):
        page = self.PAGE.replace("第 69 分鐘", "").replace("b3-work-order.md", "05-old.md")
        found = cd.b3_package_problems({"60-b3.md": page, "70-delivery.md": "b3-docs/gone.md"}, self.DEST,
                                       self.WO, self.CARD.replace("2 設計與修改範圍", "2 Impact and Design"))
        self.assertEqual(len(found), 4, found)  # 05-old.md, gone.md, 第 69 分, task card Gate 2


if __name__ == "__main__":
    unittest.main()
