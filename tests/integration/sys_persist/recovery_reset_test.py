import unittest

from game.modules.persist_recovery import *


class RecoveryResetTests(unittest.TestCase):
    def test_unknown_commit_freezes_writes(self):
        state = classify_recovery(COMMIT_STATUS_UNKNOWN)
        self.assertFalse(can_accept_write(state))
        self.assertFalse(state.feedback_allowed)

    def test_safe_recovery_is_not_unknown(self):
        self.assertFalse(classify_recovery(PERSISTENCE_SAFE_RECOVERY).writes_frozen)


if __name__ == "__main__":
    unittest.main()
