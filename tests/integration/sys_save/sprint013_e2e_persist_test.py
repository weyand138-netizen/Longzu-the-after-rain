import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCREENS = ROOT / "game" / "screens.rpy"
STATE = ROOT / "game" / "10_state.rpy"
ACHIEVEMENTS = ROOT / "game" / "11_achievements.rpy"
LOCK = ROOT / "design" / "content-lock.md"
LOCK_ROW = re.compile(r"\| `([^`]+)` \|[^|]*\| (\d+) \| `([0-9a-f]{64})` \|")


class Sprint013PersistenceFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.screens = SCREENS.read_text(encoding="utf-8")
        cls.state = STATE.read_text(encoding="utf-8")
        cls.achievements = ACHIEVEMENTS.read_text(encoding="utf-8")
        cls.lock = LOCK.read_text(encoding="utf-8")

    def test_runtime_surfaces_bind_save_load_journal_and_achievement_state(self):
        for marker in ("screen save():", "screen load():", "screen wish_journal()"):
            self.assertIn(marker, self.screens)
        for marker in ("renpy.save_persistent()", "label after_load:", "persistent.sys_persist_state"):
            self.assertIn(marker, self.state)
        for marker in ("grant_local_achievement", "achievement_popup_queue", "persistent.sys_persist_state"):
            self.assertIn(marker, self.achievements)

    def test_persistent_updates_are_not_owned_by_journal_or_external_module(self):
        self.assertIn("persistent.sys_persist_state", self.state)
        self.assertNotIn("persistent.sys_persist_state =", self.screens)
        self.assertIn("persistent.sys_persist_state = candidate", self.achievements)

    def test_current_lock_identity_is_required_for_e2e_persistence(self):
        drift = []
        for path_text, locked_lines, locked_hash in LOCK_ROW.findall(self.lock):
            path = ROOT / Path(path_text)
            actual_lines = len(path.read_text(encoding="utf-8").splitlines())
            actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual_lines != int(locked_lines) or actual_hash != locked_hash:
                drift.append(path_text)
        self.assertEqual([], drift, "persistence evidence blocked by content-lock drift: {}".format(drift))


if __name__ == "__main__":
    unittest.main()
