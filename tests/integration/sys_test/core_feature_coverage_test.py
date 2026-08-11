import unittest

from game.modules.gate_execution import execute_gate


class CoreFeatureCoverageTests(unittest.TestCase):
    def test_missing_content_lock_remains_blocked(self):
        self.assertEqual(execute_gate("INTEGRATION", ("resolver",), {}, required_inputs_present=False).status, "BLOCKED_INPUT")

    def test_complete_contract_vector_passes(self):
        self.assertEqual(execute_gate("INTEGRATION", ("resolver",), {"resolver": "PASS"}).status, "PASS")


if __name__ == "__main__":
    unittest.main()
