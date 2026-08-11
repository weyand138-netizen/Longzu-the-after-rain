import unittest

from game.modules.persist_schema import build_fresh_persist_root
from game.modules.persistent_boundary import *


class PersistentBoundaryTests(unittest.TestCase):
    def test_run_restore_does_not_mutate_persistent_root(self):
        root = build_fresh_persist_root(); before = capture_isolation_snapshot({"choice": "a"}, root)
        after = restore_run_only(before, {"choice": "b"})
        self.assertTrue(persistent_unchanged(before, after))
        self.assertEqual(after.run_state["choice"], "b")


if __name__ == "__main__":
    unittest.main()
