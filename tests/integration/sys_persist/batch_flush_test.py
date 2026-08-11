import unittest

from game.modules.persist_batch import *
from game.modules.persist_schema import build_fresh_persist_root


class BatchFlushTests(unittest.TestCase):
    def test_one_replacement_and_one_flush_success(self):
        root = build_fresh_persist_root()
        calls = []
        candidate = build_fresh_persist_root()
        candidate["collection_epoch_id"] = 1
        result = apply_complete_root_batch(root, candidate, replace_root=lambda value: calls.append(("replace", value)), flush=lambda: calls.append(("flush",)))
        self.assertEqual(result.status, APPLIED_FLUSHED)
        self.assertEqual([call[0] for call in calls], ["replace", "flush"])

    def test_safe_failure_and_unknown_commit_are_distinct(self):
        root = build_fresh_persist_root()
        candidate = build_fresh_persist_root()
        failed = apply_complete_root_batch(root, candidate, replace_root=lambda value: None, flush=lambda: (_ for _ in ()).throw(OSError()), safe_recovery=lambda value: None)
        self.assertEqual(failed.status, PERSIST_FLUSH_FAILED_SAFE)
        unknown = apply_complete_root_batch(root, candidate, replace_root=lambda value: (_ for _ in ()).throw(OSError()), flush=lambda: None)
        self.assertEqual(unknown.status, COMMIT_STATUS_UNKNOWN)
        self.assertTrue(unknown.write_frozen)


if __name__ == "__main__":
    unittest.main()
