import unittest

from game.modules.save_performance import evaluate_save_latency


class SaveLoadPerformanceTests(unittest.TestCase):
    def test_save_budget_and_report_only(self):
        self.assertEqual(evaluate_save_latency((100, 120, 150)).status, "PASS")
        self.assertEqual(evaluate_save_latency((100,), approved_threshold=False).status, "REPORT_ONLY")


if __name__ == "__main__":
    unittest.main()
