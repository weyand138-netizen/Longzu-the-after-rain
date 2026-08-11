import unittest

from game.modules.external_evidence import ExternalEvidence, external_criterion_status


class PlayerCriticalEvidenceTests(unittest.TestCase):
    def test_unapproved_human_evidence_is_blocked(self):
        evidence = ExternalEvidence("e", "PLAYTEST", "rubric", "reviewer", "env", "0" * 64, None, False, False)
        self.assertEqual(external_criterion_status(evidence), "BLOCKED_INPUT")

    def test_approved_adjudication_passes(self):
        evidence = ExternalEvidence("e", "PLAYTEST", "rubric", "reviewer", "env", "0" * 64, "PASS", True, False)
        self.assertEqual(external_criterion_status(evidence), "PASS")


if __name__ == "__main__":
    unittest.main()
