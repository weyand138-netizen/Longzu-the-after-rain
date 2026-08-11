import unittest

from game.modules.persist_performance import *


class PurePerformanceTests(unittest.TestCase):
    def test_nearest_rank_and_report_only(self):
        self.assertEqual(nearest_rank_percentile((1, 3, 2, 4), 0.5), 2)
        self.assertEqual(evaluate_performance((1, 2), percentile=0.95, percentile_budget_ms=1, maximum_budget_ms=2, approved_threshold=False).status, "REPORT_ONLY")


if __name__ == "__main__":
    unittest.main()
