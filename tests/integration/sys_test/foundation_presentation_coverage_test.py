import unittest

from game.modules.save_ui import build_slot_presentation


class FoundationPresentationCoverageTests(unittest.TestCase):
    def test_keyboard_layout_contract_is_reachable(self):
        item = build_slot_presentation("slot", {"location": "Station"})
        self.assertTrue(item.focusable and not item.hover_required and not item.timed)


if __name__ == "__main__":
    unittest.main()
