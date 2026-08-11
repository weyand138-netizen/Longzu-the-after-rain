import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "game" / "chapters" / "day1.rpy"
SCREENS = ROOT / "game" / "screens.rpy"


class Day1ContentValidationTests(unittest.TestCase):
    def test_day1_source_has_two_critical_choice_gates(self):
        source = SOURCE.read_text(encoding="utf-8")
        self.assertEqual(2, source.count("$ critical_choice_interaction = True"))
        self.assertEqual(4, source.count("$ critical_choice_interaction = False"))

    def test_quick_menu_is_hidden_during_critical_interaction(self):
        screens = SCREENS.read_text(encoding="utf-8")
        self.assertIn("if not critical_choice_interaction:", screens)
        self.assertIn('id "quick_menu_root"', screens)
        self.assertIn('id "day1_choice_{}".format(index)', screens)

    def test_choice_surface_applies_font_scale_and_high_contrast(self):
        screens = SCREENS.read_text(encoding="utf-8")
        self.assertIn('$ accessibility_settings = persistent.sys_persist_state["settings"]', screens)
        self.assertIn('$ accessibility_scale = accessibility_settings["font_scale"]', screens)
        self.assertIn('$ accessibility_high_contrast = accessibility_settings["high_contrast"]', screens)
        self.assertIn('text_size int(32 * accessibility_scale)', screens)
        self.assertIn('background Solid(("#000000" if accessibility_high_contrast', screens)

    def test_day1_skips_transition_when_reduced_motion_is_enabled(self):
        source = SOURCE.read_text(encoding="utf-8")
        self.assertIn('if persistent.sys_persist_state["settings"]["reduced_motion"]:', source)
        self.assertIn('with dissolve_slow', source)

    def test_source_has_no_hidden_state_copy(self):
        source = SOURCE.read_text(encoding="utf-8")
        for term in ("隐藏分数", "路线标签", "结局条件", "正确选项"):
            self.assertNotIn(term, source)

    def test_source_hash_is_current_and_nonempty(self):
        digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
        self.assertEqual(64, len(digest))
        self.assertNotEqual("0" * 64, digest)
