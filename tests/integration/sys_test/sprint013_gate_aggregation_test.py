import unittest
from pathlib import Path

from game.modules.gate_execution import aggregate_release, execute_gate


ROOT = Path(__file__).resolve().parents[3]
STATUS = ROOT / "production" / "sprint-status.yaml"
STAGE = ROOT / "production" / "stage.txt"
REPORT = ROOT / "production" / "gate-checks" / "production-to-polish-2026-08-15-final.md"


class Sprint013GateAggregationTests(unittest.TestCase):
    def test_blocked_input_cannot_aggregate_to_release_pass(self):
        component = execute_gate("FAST", ("N13-01",), {"N13-01": "PASS"})
        integration = execute_gate("INTEGRATION", ("N13-02",), {"N13-02": "FAIL"})
        release = execute_gate("RELEASE", ("N13-11",), {}, required_inputs_present=False)
        self.assertEqual(aggregate_release(component, integration, release), "BLOCKED_INPUT")

    def test_current_must_have_statuses_are_fail_closed(self):
        text = STATUS.read_text(encoding="utf-8")
        for package_id in ("N13-01", "N13-02", "N13-03", "N13-04", "N13-05", "N13-06", "N13-07", "N13-08", "N13-09", "N13-10", "N13-11"):
            self.assertIn(f'id: "{package_id}"', text)
        self.assertIn("status: blocked", text)

    def test_gate_report_and_stage_are_current_and_not_promoted(self):
        self.assertEqual(STAGE.read_text(encoding="utf-8").strip(), "Production")
        self.assertTrue(REPORT.exists(), "current final gate report is missing")
        report = REPORT.read_text(encoding="utf-8")
        self.assertIn("BLOCKED_INPUT", report)
        self.assertIn("stage.txt", report)
        self.assertIn("not modified", report.lower())
        self.assertNotIn("Final verdict: PASS", report)


if __name__ == "__main__":
    unittest.main()
