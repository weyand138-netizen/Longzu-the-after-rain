import unittest

from game.modules.save_ui import *


class SaveLoadUITests(unittest.TestCase):
    def test_metadata_and_keyboard_path_are_accessible(self):
        first = build_slot_presentation("slot-1", {"location": "Station", "day": "1"})
        second = build_slot_presentation("slot-2", {"location": "Archive"})
        self.assertEqual(keyboard_path((first, second), 1).slot_id, "slot-2")
        self.assertFalse(first.hover_required or first.timed)


if __name__ == "__main__":
    unittest.main()
