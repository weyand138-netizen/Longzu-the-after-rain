import unittest

from game.modules.achievement_ui import *
from game.modules.persist_projections import AchievementProjectionResult


class AchievementStateUITests(unittest.TestCase):
    def test_locked_rows_are_not_rendered_and_new_rows_are_ordered(self):
        rows = build_achievement_rows(["CHOICE_ASK_FIRST"], [])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].state, "new")

    def test_unsafe_boundary_defers_presentation(self):
        result = AchievementProjectionResult("APPLIED_FLUSHED", "occ", 0, ("CHOICE_ASK_FIRST",), (), "notify:occ")
        self.assertEqual(presentation_decision(result, False)[0], "DEFER")


if __name__ == "__main__":
    unittest.main()
