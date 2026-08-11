import unittest

from game.modules.evidence_bundle import *


def artifact(status="PASS", generation="g"):
    return EvidenceArtifact("a1", "C1", generation, "a" * 64, "b" * 64, "c" * 64, "d" * 64, "e" * 64, "f" * 64, status)


class EvidenceBundleTraceabilityTests(unittest.TestCase):
    def test_manifest_derived_traceability_and_current_status(self):
        bundle = build_evidence_bundle("candidate", "g", (artifact(),))
        self.assertEqual(bundle_status(bundle, required_criterion_ids=("C1",)), "PASS")
        self.assertEqual(traceability_index(bundle), {"C1": ("a1",)})

    def test_cross_generation_and_stale_are_blocked(self):
        with self.assertRaises(ValueError):
            build_evidence_bundle("candidate", "g", (artifact(generation="h"),))
        bundle = build_evidence_bundle("candidate", "g", (artifact(status="STALE"),))
        self.assertEqual(bundle_status(bundle, required_criterion_ids=("C1",)), "BLOCKED_INPUT")


if __name__ == "__main__":
    unittest.main()
