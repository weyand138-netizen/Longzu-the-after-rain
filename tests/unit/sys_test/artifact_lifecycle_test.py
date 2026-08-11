import unittest

from game.modules.artifact_lifecycle import *


class ArtifactLifecycleTests(unittest.TestCase):
    def test_unbound_and_blocked_inputs_cannot_pass(self):
        self.assertEqual(start_artifact(manifest_present=False, external_input_present=True, generation="g").status, UNBOUND)
        blocked = start_artifact(manifest_present=True, external_input_present=False, generation="g")
        self.assertEqual(blocked.status, BLOCKED_INPUT)
        self.assertEqual(finish_artifact(blocked, passed=True, current_generation="g").status, BLOCKED_INPUT)

    def test_current_and_stale(self):
        running = start_artifact(manifest_present=True, external_input_present=True, generation="g")
        self.assertEqual(finish_artifact(running, passed=True, current_generation="g").status, PASSED_CURRENT)
        self.assertEqual(finish_artifact(running, passed=True, current_generation="h").status, STALE)


if __name__ == "__main__":
    unittest.main()
