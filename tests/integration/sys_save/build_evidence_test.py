import unittest

from game.modules.build_evidence import *


class SaveBuildEvidenceTests(unittest.TestCase):
    def test_archive_hash_is_package_only_and_evidence_is_current(self):
        self.assertEqual(len(archive_hash(b"package")), 64)
        identity = candidate_identity({"source": "save", "catalog": "v2"})
        candidate = CandidateManifest(identity, "g", "s", "c", "renpy", "release", "run")
        self.assertTrue(evidence_complete(candidate=candidate, evidence_candidate_identity=identity, required_ids=("SAVE",), provided_ids=("SAVE",), generation="g"))


if __name__ == "__main__":
    unittest.main()
