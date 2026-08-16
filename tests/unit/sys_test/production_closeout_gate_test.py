import unittest

from game.modules.production_closeout import (
    BLOCKED_INPUT,
    ExternalEvidence,
    PASS,
    REPORT_ONLY,
    classify_external_evidence,
    final_gate_status,
)


class ProductionCloseoutGateTests(unittest.TestCase):
    def test_missing_human_input_is_blocked_without_being_a_test_failure(self):
        self.assertEqual(
            BLOCKED_INPUT,
            classify_external_evidence(ExternalEvidence("playtest", False)),
        )

    def test_missing_runtime_samples_are_report_only(self):
        self.assertEqual(
            REPORT_ONLY,
            classify_external_evidence(ExternalEvidence("performance", False, report_only=True)),
        )

    def test_present_preflight_contract_is_pass(self):
        self.assertEqual(PASS, classify_external_evidence(ExternalEvidence("manifest", True)))

    def test_final_gate_only_aggregates_external_non_pass(self):
        self.assertEqual(
            BLOCKED_INPUT,
            final_gate_status((ExternalEvidence("playtest", False), ExternalEvidence("performance", False, report_only=True))),
        )
        self.assertEqual(
            PASS,
            final_gate_status((ExternalEvidence("manifest", True), ExternalEvidence("source", True))),
        )


if __name__ == "__main__":
    unittest.main()
