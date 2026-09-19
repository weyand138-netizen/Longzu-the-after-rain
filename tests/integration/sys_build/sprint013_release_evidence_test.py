import unittest
from pathlib import Path

from game.modules.build_evidence import ExclusionReport, validate_exclusion_reports
from game.modules.production_closeout import BLOCKED_INPUT, ExternalEvidence, PASS, classify_external_evidence


ROOT = Path(__file__).resolve().parents[3]
STATUS = ROOT / "production" / "sprint-status.yaml"
RELEASES = ROOT / "production" / "releases"
PREFLIGHT = ROOT / "production" / "preflight" / "candidate-manifest-v1.json"


class Sprint013ReleaseEvidenceTests(unittest.TestCase):
    def test_preflight_candidate_identity_is_bound_but_archive_remains_rc_input(self):
        self.assertTrue(PREFLIGHT.exists(), "current release preflight is missing")
        text = PREFLIGHT.read_text(encoding="utf-8")
        self.assertIn('"candidate_manifest": "candidate_manifest:v1"', text)
        self.assertRegex(text, r'"candidate_identity": "[0-9a-f]{64}"')
        self.assertIn('"release_candidate": false', text)
        self.assertEqual(
            BLOCKED_INPUT,
            classify_external_evidence(ExternalEvidence("final RC archive", RELEASES.exists() and bool(tuple(RELEASES.rglob("*.zip"))))),
        )

    def test_all_n13_05_to_n13_10_inputs_are_current(self):
        status = STATUS.read_text(encoding="utf-8")
        for package_id in ("N13-05", "N13-06", "N13-07", "N13-08", "N13-09", "N13-10"):
            self.assertIn(f'id: "{package_id}"', status)
        self.assertIn("current_preflight:", status)
        self.assertIn("deferred_rc_closeout:", status)
        self.assertEqual(PASS, classify_external_evidence(ExternalEvidence("automation preflight", "current_preflight:" in status)))
        self.assertIn("BLOCKED_INPUT", status)

    def test_clean_exclusion_contract_is_not_sufficient_without_archive(self):
        clean = ExclusionReport(0, 0, 0, 0, 0, 0)
        self.assertTrue(validate_exclusion_reports(clean, clean))


if __name__ == "__main__":
    unittest.main()
