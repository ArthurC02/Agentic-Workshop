import unittest

import check_zh_tw as z


class Problems(unittest.TestCase):
    def test_flags_simplified_and_mainland_terms(self):
        hits = z.problems("这是軟件的不變量與錯誤代碼")
        self.assertIn("非台灣繁體字「这」", hits)
        self.assertIn("「軟件」→「軟體」", hits)
        self.assertEqual(len(hits), 2)  # 不變量、錯誤代碼 are Taiwan usage

    def test_taiwan_text_passes(self):
        self.assertEqual(z.problems("請 Agent 在伺服器執行測試，結果寫進資料夾。"), [])


if __name__ == "__main__":
    unittest.main()
