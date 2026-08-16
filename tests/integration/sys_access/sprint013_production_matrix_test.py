import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCREENS = ROOT / "game" / "screens.rpy"
OPTIONS = ROOT / "game" / "options.rpy"
FOCUS = ROOT / "game" / "modules" / "accessibility_focus.py"
LOCK = ROOT / "design" / "content-lock.md"
LOCK_ROW = re.compile(r"\| `([^`]+)` \|[^|]*\| (\d+) \| `([0-9a-f]{64})` \|")


class Sprint013AccessibilityMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.screens = SCREENS.read_text(encoding="utf-8")
        cls.options = OPTIONS.read_text(encoding="utf-8")
        cls.focus = FOCUS.read_text(encoding="utf-8")
        cls.lock = LOCK.read_text(encoding="utf-8")

    def test_current_source_declares_keyboard_mouse_and_accessibility_surfaces(self):
        for marker in (
            "screen choice(items):",
            "screen quick_menu():",
            "screen save():",
            "screen load():",
            "screen wish_journal():",
            "default_focus",
            "key \"focus_graph_next\"",
            "key \"focus_graph_previous\"",
            "accessibility_high_contrast",
            "settings_reduced_motion",
            "settings_flash_effects",
            "settings_screen_shake",
        ):
            self.assertIn(marker, self.screens)
        for marker in ("1.0", "1.25", "1.5", "high_contrast", "reduced_motion"):
            self.assertIn(marker, self.options + self.screens)
        for marker in ("ensure_initial_focus", "move", "viewport", "scroll"):
            self.assertIn(marker, self.focus)

    def test_current_source_keeps_actions_keyboard_and_mouse_addressable(self):
        self.assertIn("textbutton", self.screens)
        self.assertIn("action", self.screens)
        self.assertIn("focus_graph_bindings", self.screens)
        self.assertNotIn("hover-only", self.screens.lower())

    def test_current_lock_identity_is_required_for_production_matrix(self):
        drift = []
        for path_text, locked_lines, locked_hash in LOCK_ROW.findall(self.lock):
            path = ROOT / Path(path_text)
            actual_lines = len(path.read_text(encoding="utf-8").splitlines())
            actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual_lines != int(locked_lines) or actual_hash != locked_hash:
                drift.append(path_text)
        self.assertEqual([], drift, "accessibility matrix blocked by content-lock drift: {}".format(drift))


if __name__ == "__main__":
    unittest.main()
