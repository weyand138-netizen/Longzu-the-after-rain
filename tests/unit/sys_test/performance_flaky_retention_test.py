import unittest

from game.modules.persist_performance import evaluate_performance, nearest_rank_percentile


class PerformanceFlakyRetentionTests(unittest.TestCase):
    def test_nearest_rank_and_unapproved_threshold(self):
        self.assertEqual(nearest_rank_percentile((4, 1, 2, 3), .75), 3)
        self.assertEqual(evaluate_performance((1, 2), percentile=.95, percentile_budget_ms=1, maximum_budget_ms=2, approved_threshold=False).status, "REPORT_ONLY")


if __name__ == "__main__":
    unittest.main()
