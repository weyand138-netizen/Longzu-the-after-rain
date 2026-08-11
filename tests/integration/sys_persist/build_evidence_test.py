import unittest

from game.modules.build_evidence import *


class BuildEvidenceTests(unittest.TestCase):
    def test_candidate_and_exclusion_closure(self):
        identity = candidate_identity({"source": "s", "catalog": "c"})
        manifest = CandidateManifest(identity, "g1", "s", "c", "renpy", "release", "run")
        clean = ExclusionReport(0, 0, 0, 0, 0, 0)
        self.assertTrue(validate_exclusion_reports(clean, clean))
        self.assertTrue(evidence_complete(candidate=manifest, evidence_candidate_identity=identity, required_ids=("A",), provided_ids=("A",), generation="g1"))
        with self.assertRaises(ValueError):
            reject_cross_generation("g1", "g2")


if __name__ == "__main__":
    unittest.main()
