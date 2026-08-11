import unittest

from game.modules.test_manifest import *


class FrameworkManifestTests(unittest.TestCase):
    def test_exact_owner_and_artifact_mapping(self):
        record = CriterionRecord("TEST-1", "SYS-STATE", "UT_PURE", "FAST", ("CASE-1",), ("ART-1",))
        manifest = build_test_framework_manifest((record,), runner_id="runner:v1", generation="g1")
        self.assertEqual(manifest["criteria"][0]["owner_system"], "SYS-STATE")
        with self.assertRaises(TestManifestError):
            validate_criterion_records((record, record))

    def test_canonical_identity_rejects_float(self):
        with self.assertRaises(TestManifestError):
            canonical_json({"threshold": 1.0})


if __name__ == "__main__":
    unittest.main()
