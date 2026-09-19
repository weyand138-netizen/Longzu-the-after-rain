import unittest
from pathlib import Path

from game.modules.production_closeout import BLOCKED_INPUT, ExternalEvidence, classify_external_evidence


ROOT = Path(__file__).resolve().parents[3]
DOSSIER = ROOT / "production" / "session-logs" / "playtest-sprint-013-n13-08.md"
STATUS = ROOT / "production" / "sprint-status.yaml"
ORCHESTRATOR = ROOT / "game" / "production_orchestrator.rpy"


class Sprint013PlaytestDossierTests(unittest.TestCase):
    def test_normal_orchestrator_contains_no_debug_or_test_dispatch(self):
        source = ORCHESTRATOR.read_text(encoding="utf-8")
        self.assertNotIn("renpy.is_in_test", source)
        self.assertNotIn("debug", source.lower())
        self.assertNotIn("testcase", source.lower())

    def test_current_dossier_has_raw_player_and_observer_evidence(self):
        self.assertTrue(DOSSIER.exists(), "current N13-08 dossier is missing")
        dossier = DOSSIER.read_text(encoding="utf-8")
        complete = all(marker in dossier.lower() for marker in ("candidate_identity", "raw answers", "observer", "unbriefed")) and "BLOCKED_INPUT" not in dossier
        self.assertEqual(
            BLOCKED_INPUT,
            classify_external_evidence(ExternalEvidence("clean-player comprehension dossier", complete)),
        )
        self.assertIn("BLOCKED_INPUT", dossier)

    def test_sprint_status_has_a_bound_candidate_before_playtest_close(self):
        status = STATUS.read_text(encoding="utf-8")
        self.assertIn("candidate_identity:", status)
        self.assertNotIn("candidate_identity: UNBOUND", status)
        self.assertIn("N13-08", status)
        self.assertIn("deferred_rc_closeout:", status)


if __name__ == "__main__":
    unittest.main()
