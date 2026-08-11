import unittest

from game.modules.gate_execution import *


class GateExecutionTests(unittest.TestCase):
    def test_strict_and_and_blocked_input(self):
        passed = execute_gate("FAST", ("A", "B"), {"A": "PASS", "B": "PASS"})
        failed = execute_gate("INTEGRATION", ("A", "B"), {"A": "PASS", "B": "FAIL"})
        blocked = execute_gate("RELEASE", ("A",), {}, required_inputs_present=False)
        self.assertEqual(passed.status, "PASS")
        self.assertEqual(failed.status, "FAIL")
        self.assertEqual(aggregate_release(passed, failed, blocked), "BLOCKED_INPUT")

    def test_timeout_is_not_pass(self):
        self.assertEqual(execute_gate("FAST", ("A",), {}, timeout=True).status, "TIMEOUT/ERROR")


if __name__ == "__main__":
    unittest.main()
