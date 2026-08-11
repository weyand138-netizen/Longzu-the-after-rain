import unittest

from game.modules.journal_gate import *


class JournalGateTests(unittest.TestCase):
    def test_dual_entry_and_focus_are_closed_during_recovery(self):
        state = journal_gate(blocked=False, recovery_active=False, caller_context_safe=True)
        self.assertTrue(state.visible and state.enabled and state.focusable)
        blocked = journal_gate(blocked=True, recovery_active=True, caller_context_safe=False)
        self.assertTrue(recovery_preempts_journal(blocked))
        self.assertEqual(blocked.entry_count, 0)


if __name__ == "__main__":
    unittest.main()
