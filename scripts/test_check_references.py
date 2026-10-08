import unittest

import check_references as cr


class AllowedAndRetired(unittest.TestCase):
    def test_retired_column_is_not_allowed(self):
        allowed, retired = cr.allowed_and_retired(
            "| Topic | Cite | Retired |\n|---|---|---|\n| Model | A〈New title〉 | 〈Old title〉 |\n- Book〈Chapter〉\n")
        self.assertIn("New title", allowed)
        self.assertIn("Chapter", allowed)
        self.assertEqual(retired, {"Old title"})
        self.assertNotIn("Old title", allowed)


if __name__ == "__main__":
    unittest.main()
