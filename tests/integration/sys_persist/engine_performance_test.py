import unittest

from game.modules.persist_performance import evaluate_performance


class EnginePerformanceTests(unittest.TestCase):
    def test_budget_pass_and_fail(self):
        self.assertEqual(evaluate_performance((1, 2, 3), percentile=.95, percentile_budget_ms=4, maximum_budget_ms=4).status, "PASS")
        self.assertEqual(evaluate_performance((1, 5), percentile=.95, percentile_budget_ms=4, maximum_budget_ms=4).status, "FAIL")


if __name__ == "__main__":
    unittest.main()
