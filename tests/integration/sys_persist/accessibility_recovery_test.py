import unittest

from game.modules.save_ui import build_slot_presentation


class AccessibilityRecoveryTests(unittest.TestCase):
    def test_slot_is_keyboard_and_non_timed(self):
        slot = build_slot_presentation("manual-1", {"location": "Station"})
        self.assertTrue(slot.focusable)
        self.assertFalse(slot.timed)
        self.assertFalse(slot.hover_required)


if __name__ == "__main__":
    unittest.main()
