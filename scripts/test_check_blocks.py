import unittest

import check_blocks as cb

GOOD = ("## 檢查點 1 · 做事（第 1–2 分鐘）\n\n① 為什麼做這一步\n\n因為。\n\n② 貼給 Agent\n\n```text\n做\n```\n\n"
        "③ 確認結果\n\n```text\n符合只回「成功」，否則回「失敗：」加原因。\n```\n\n失敗時：\n\n```text\n補\n```\n")


class Problems(unittest.TestCase):
    def test_four_blocks_pass(self):
        self.assertEqual(cb.problems(GOOD + "\n## 完成後想一想\n\n1. 想\n"), [])

    def test_missing_or_misordered_labels(self):
        self.assertEqual(len(cb.problems(GOOD.replace("② 貼給 Agent", "貼給 Agent"))), 1)
        self.assertEqual(len(cb.problems(GOOD.replace("① ", "④ ", 1))), 1)

    def test_check_prompt_and_rescue_required(self):
        self.assertEqual(len(cb.problems(GOOD.replace("「成功」", "好"))), 1)
        self.assertEqual(len(cb.problems(GOOD.replace("失敗時：", "其他："))), 1)

    def test_heading_inside_fence_does_not_end_section(self):
        self.assertEqual(cb.problems(GOOD.replace("```text\n做\n```", "```prompt\n## 交接單格式\n做\n```")), [])


if __name__ == "__main__":
    unittest.main()
