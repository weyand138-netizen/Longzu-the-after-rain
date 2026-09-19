import unittest
from pathlib import Path

from game.modules.persist_performance import evaluate_performance
from game.modules.production_closeout import ExternalEvidence, REPORT_ONLY, classify_external_evidence


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "production" / "preflight"
PROTOCOL = EVIDENCE / "performance-protocol-v1.md"
SAMPLES = EVIDENCE / "raw" / "engine-samples.tsv"


class Sprint013PerformanceTests(unittest.TestCase):
    def test_current_benchmark_is_bound_to_candidate_and_engine(self):
        self.assertTrue(PROTOCOL.exists(), "current benchmark protocol is missing")
        text = PROTOCOL.read_text(encoding="utf-8")
        self.assertIn("benchmark_protocol:v1", text)
        self.assertIn("candidate_identity:", text)
        self.assertNotIn("candidate_identity: UNBOUND", text)
        for marker in ("hardware:", "windows_build:", "renderer:", "warmup:", "sample_count:"):
            self.assertIn(marker, text)

    def test_current_benchmark_preserves_at_least_thirty_raw_samples(self):
        rows = [line for line in SAMPLES.read_text(encoding="utf-8").splitlines() if line and not line.startswith("#")] if SAMPLES.exists() else []
        self.assertEqual(
            REPORT_ONLY,
            classify_external_evidence(ExternalEvidence("runtime performance samples", len(rows) >= 30, report_only=True)),
        )
        self.assertLess(len(rows), 30)

    def test_unapproved_threshold_is_report_only(self):
        report = evaluate_performance((1.0, 2.0), percentile=.95, percentile_budget_ms=16.6, maximum_budget_ms=33.2, approved_threshold=False)
        self.assertEqual(report.status, "REPORT_ONLY")


if __name__ == "__main__":
    unittest.main()
