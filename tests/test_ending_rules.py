import itertools
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GAME_DIR = PROJECT_ROOT / "game"
sys.path.insert(0, str(GAME_DIR))

from modules.ending_rules import (  # noqa: E402
    AXES,
    ENDING_PRIORITY,
    resolve_ending,
    validate_snapshot,
)


def state(understanding, autonomy, truth, preparation, sacrifice):
    return {
        "understanding": understanding,
        "autonomy": autonomy,
        "truth": truth,
        "preparation": preparation,
        "sacrifice": sacrifice,
    }


class EndingRuleTests(unittest.TestCase):
    def test_canonical_paths(self):
        cases = {
            "rain_stops": state(3, 3, 3, 3, 3),
            "her_own_name": state(2, 3, 3, 1, 1),
            "see_the_sea": state(2, 2, 1, 3, 2),
            "one_person_train": state(1, 2, 2, 1, 1),
            "golden_cage": state(2, 0, 2, 1, 0),
            "unsent_postcard": state(0, 0, 0, 0, 0),
        }
        for expected, snapshot in cases.items():
            with self.subTest(expected=expected):
                self.assertEqual(expected, resolve_ending(snapshot))

    def test_all_legal_states_resolve_to_known_ending(self):
        observed = set()
        for values in itertools.product(range(4), repeat=len(AXES)):
            snapshot = dict(zip(AXES, values))
            ending = resolve_ending(snapshot)
            self.assertIn(ending, ENDING_PRIORITY)
            observed.add(ending)
        self.assertEqual(set(ENDING_PRIORITY), observed)

    def test_true_ending_has_highest_priority(self):
        self.assertEqual("rain_stops", resolve_ending(state(3, 3, 3, 3, 3)))

    def test_missing_axis_is_rejected(self):
        snapshot = state(0, 0, 0, 0, 0)
        del snapshot["truth"]
        with self.assertRaises(ValueError):
            validate_snapshot(snapshot)

    def test_extra_axis_is_rejected(self):
        snapshot = state(0, 0, 0, 0, 0)
        snapshot["affection"] = 99
        with self.assertRaises(ValueError):
            validate_snapshot(snapshot)

    def test_non_integer_and_out_of_range_values_are_rejected(self):
        with self.assertRaises(TypeError):
            validate_snapshot(state(True, 0, 0, 0, 0))
        with self.assertRaises(ValueError):
            validate_snapshot(state(4, 0, 0, 0, 0))
        with self.assertRaises(ValueError):
            validate_snapshot(state(-1, 0, 0, 0, 0))


if __name__ == "__main__":
    unittest.main()

