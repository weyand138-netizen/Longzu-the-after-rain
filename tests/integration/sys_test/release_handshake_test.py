import unittest

from game.modules.build_evidence import *


class ReleaseHandshakeTests(unittest.TestCase):
    def test_candidate_evidence_identity_and_zero_findings(self):
        identity = candidate_identity({"source": "a"})
        manifest = CandidateManifest(identity, "g", "a", "c", "e", "release", "run")
        clean = ExclusionReport(0, 0, 0, 0, 0, 0)
        self.assertTrue(validate_exclusion_reports(clean, clean))
        self.assertTrue(evidence_complete(candidate=manifest, evidence_candidate_identity=identity, required_ids=("C",), provided_ids=("C",), generation="g"))


if __name__ == "__main__":
    unittest.main()
