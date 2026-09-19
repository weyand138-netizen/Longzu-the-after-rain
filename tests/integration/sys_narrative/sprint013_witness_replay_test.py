import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
STATE = ROOT / "game" / "10_state.rpy"
ENDINGS = ROOT / "game" / "chapters" / "endings.rpy"
DAY7 = ROOT / "game" / "chapters" / "day7.rpy"
TESTCASES = ROOT / "game" / "testcases.rpy"
LOCK = ROOT / "design" / "content-lock.md"
ENDING_IDS = (
    "rain_stops",
    "her_own_name",
    "see_the_sea",
    "one_person_train",
    "golden_cage",
    "unsent_postcard",
)
LOCK_ROW = re.compile(r"\| `([^`]+)` \|[^|]*\| (\d+) \| `([0-9a-f]{64})` \|")


class Sprint013WitnessReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = STATE.read_text(encoding="utf-8")
        cls.endings = ENDINGS.read_text(encoding="utf-8")
        cls.day7 = DAY7.read_text(encoding="utf-8")
        cls.testcases = TESTCASES.read_text(encoding="utf-8")
        cls.lock = LOCK.read_text(encoding="utf-8")

    def test_fixed_ending_map_is_exact_and_one_to_one(self):
        mapping = tuple(re.findall(r'^        \("([^\"]+)", "([^\"]+)"\),$', self.state, re.MULTILINE))
        self.assertEqual(ENDING_IDS, tuple(ending for ending, _ in mapping))
        self.assertEqual(
            tuple("ending_" + ending for ending in ENDING_IDS),
            tuple(label for _, label in mapping),
        )
        self.assertEqual(len(mapping), len(set(label for _, label in mapping)))

    def test_each_ending_owns_entry_completion_and_only_rain_tail(self):
        for ending_id in ENDING_IDS:
            label = "ending_{}".format(ending_id)
            self.assertIn("label {}:".format(label), self.endings)
            block = self.endings.split("label {}:".format(label), 1)[1]
            self.assertIn('commit_ending_entry("{}")'.format(ending_id), block)
            self.assertIn('commit_ending_completion("{}"'.format(ending_id), block)
        self.assertEqual(1, self.endings.count("jump epilogue_rain_stops_arcade"))
        self.assertNotIn("jump epilogue_rain_stops_arcade", self.endings.split("label ending_rain_stops:", 1)[0])
        self.assertEqual(1, self.day7.count("jump day7_resolve_ending"))

    def test_automated_witness_cases_cover_all_six_ids(self):
        self.assertIn("day7_six_canonical_history_handoffs", self.testcases)
        for ending_id in ENDING_IDS:
            self.assertIn('"{}"'.format(ending_id), self.testcases)

    def test_current_lock_identity_is_required_for_witness_replay(self):
        drift = []
        for path_text, locked_lines, locked_hash in LOCK_ROW.findall(self.lock):
            path = ROOT / Path(path_text)
            actual_lines = len(path.read_text(encoding="utf-8").splitlines())
            actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual_lines != int(locked_lines) or actual_hash != locked_hash:
                drift.append(path_text)
        self.assertEqual([], drift, "current witness identity is blocked by lock drift: {}".format(drift))


if __name__ == "__main__":
    unittest.main()
