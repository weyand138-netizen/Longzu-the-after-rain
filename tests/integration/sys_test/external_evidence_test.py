import unittest

from game.modules.external_evidence import *


class ExternalEvidenceTests(unittest.TestCase):
    def test_missing_adjudication_stays_blocked(self):
        item = ExternalEvidence("x", "HUMAN", "r", "p", "env", "a" * 64, None, False, False)
        self.assertEqual(external_criterion_status(item), "BLOCKED_INPUT")

    def test_test_only_media_is_rejected(self):
        item = ExternalEvidence("x", "VISUAL", "r", "p", "env", "a" * 64, "PASS", True, True)
        self.assertFalse(validate_external_evidence(item))


if __name__ == "__main__":
    unittest.main()
