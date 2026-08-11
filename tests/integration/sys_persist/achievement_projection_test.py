import unittest

from game.modules.persist_projections import *
from game.modules.persist_schema import build_fresh_persist_root


class AchievementProjectionTests(unittest.TestCase):
    def test_eleven_catalog_records_and_event_tail(self):
        validate_achievement_catalog(ACHIEVEMENT_CATALOG)
        snapshot = AchievementSnapshot("catalog:v2", 0, "occ", "cp", ("event_choice_read_the_note",), ("event_choice_read_the_note",), True)
        self.assertEqual(evaluate_achievement_candidates(snapshot, ()), ("CHOICE_READ_THE_NOTE",))

    def test_projection_is_idempotent_and_seen_is_subset(self):
        root = build_fresh_persist_root()
        candidate, result = project_achievements(root, ("CHOICE_READ_THE_NOTE",), checkpoint_occurrence_id="occ")
        self.assertEqual(result.added_achievement_ids, ("CHOICE_READ_THE_NOTE",))
        seen = mark_achievements_seen(candidate, ("CHOICE_READ_THE_NOTE",))
        self.assertEqual(seen["seen_achievement_ids"], ["CHOICE_READ_THE_NOTE"])
        _, duplicate = project_achievements(seen, ("CHOICE_READ_THE_NOTE",), checkpoint_occurrence_id="occ")
        self.assertEqual(duplicate.added_achievement_ids, ())


if __name__ == "__main__":
    unittest.main()
