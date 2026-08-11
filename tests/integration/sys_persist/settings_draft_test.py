import unittest

from game.modules.persist_schema import build_fresh_persist_root
from game.modules.settings_flow import *


class SettingsDraftTests(unittest.TestCase):
    def test_draft_apply_replaces_settings_once(self):
        root = build_fresh_persist_root()
        draft = update_draft(make_settings_draft(root, 1), high_contrast=True)
        candidate = apply_settings_draft(root, draft, 1)
        self.assertTrue(candidate["settings"]["high_contrast"])

    def test_external_conflict_blocks_apply(self):
        root = build_fresh_persist_root(); draft = update_draft(make_settings_draft(root, 1), reduced_motion=True)
        latest = build_fresh_persist_root(); latest["settings"]["high_contrast"] = True
        rebased, state = rebase_draft(draft, latest, 2)
        self.assertEqual(state, STALE_DRAFT_CONFLICT)
        self.assertEqual(rebased.base_revision, 2)


if __name__ == "__main__":
    unittest.main()
