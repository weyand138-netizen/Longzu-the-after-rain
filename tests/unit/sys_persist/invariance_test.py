import unittest

from game.modules.persist_merge import make_new_game_envelope
from game.modules.persist_schema import build_fresh_persist_root


class InvarianceTests(unittest.TestCase):
    def test_new_game_copies_epoch_without_run_mutation(self):
        root = build_fresh_persist_root(); root["collection_epoch_id"] = 4
        envelope = make_new_game_envelope(root, {"choice_history": ["x"]})
        self.assertEqual(envelope["run_envelope"]["collection_epoch_id"], 4)
        self.assertEqual(root["collection_epoch_id"], 4)


if __name__ == "__main__":
    unittest.main()
