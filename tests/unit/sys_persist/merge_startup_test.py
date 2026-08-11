import unittest

from game.modules.persist_merge import *
from game.modules.persist_schema import build_fresh_persist_root


class MergeStartupTests(unittest.TestCase):
    def test_merge_uses_only_max_epoch(self):
        old = build_fresh_persist_root(); old["achievement_ids"] = ["CHOICE_READ_THE_NOTE"]
        new = build_fresh_persist_root(); new["collection_epoch_id"] = 1; new["achievement_ids"] = ["CHOICE_ASK_FIRST"]
        self.assertEqual(merge_persist_roots((old, new))["achievement_ids"], ["CHOICE_ASK_FIRST"])

    def test_reset_increments_epoch_and_preserves_settings(self):
        root = build_fresh_persist_root(); root["achievement_ids"] = ["CHOICE_READ_THE_NOTE"]; root["settings"]["high_contrast"] = True
        reset = reset_collection(root)
        self.assertEqual(reset["collection_epoch_id"], 1)
        self.assertTrue(reset["settings"]["high_contrast"])
        self.assertTrue(validate_startup_root(reset))


if __name__ == "__main__":
    unittest.main()
