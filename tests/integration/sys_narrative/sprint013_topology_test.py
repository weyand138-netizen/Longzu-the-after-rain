import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "game" / "script.rpy"
ORCHESTRATOR = ROOT / "game" / "production_orchestrator.rpy"
DAY7 = ROOT / "game" / "chapters" / "day7.rpy"
STATE = ROOT / "game" / "10_state.rpy"
BASELINE = ROOT / "design" / "narrative" / "seven-day-content-baseline.md"
CONTENT_LOCK = ROOT / "design" / "content-lock.md"

EXPECTED_ORDER = (
    "prologue_start",
    "chapter_day1_her_own_name",
    "chapter_day2_two_game_tokens",
    "chapter_day3_empty_school",
    "chapter_day4_seaside_train",
    "chapter_day5_family_lie",
    "chapter_day6_no_safe_house",
    "chapter_day7_before_red_well",
)
EXPECTED_ENDINGS = (
    "rain_stops",
    "her_own_name",
    "see_the_sea",
    "one_person_train",
    "golden_cage",
    "unsent_postcard",
)
LOCK_ROW = re.compile(r"\| `([^`]+)` \|[^|]*\| (\d+) \| `([0-9a-f]{64})` \|")


def label_block(source, label):
    match = re.search(
        r"^label {}:\n(?P<body>.*?)(?=^label |\Z)".format(label),
        source,
        re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError("missing label: {}".format(label))
    return match.group("body")


class Sprint013TopologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SCRIPT.read_text(encoding="utf-8")
        cls.orchestrator = ORCHESTRATOR.read_text(encoding="utf-8")
        cls.day7 = DAY7.read_text(encoding="utf-8")
        cls.state = STATE.read_text(encoding="utf-8")
        cls.baseline = BASELINE.read_text(encoding="utf-8")
        cls.content_lock = CONTENT_LOCK.read_text(encoding="utf-8")

    def test_normal_entry_has_one_fixed_production_route(self):
        start = label_block(self.script, "start")
        body = label_block(self.orchestrator, "production_end_to_end_orchestrator")
        self.assertEqual(1, start.count("call production_end_to_end_orchestrator"))
        self.assertIn("if renpy.is_in_test():", start)
        self.assertIn("call prologue_start", start)
        self.assertEqual(
            EXPECTED_ORDER,
            tuple(re.findall(r"^    call (\w+)$", body, re.MULTILINE)),
        )
        self.assertNotIn("menu:", body)
        self.assertNotRegex(body, r"^    \$ ")
        self.assertNotIn("jump ", body)

    def test_day7_has_one_handoff_and_six_label_map_is_one_to_one(self):
        self.assertEqual(1, self.day7.count("jump day7_resolve_ending"))
        mapping = tuple(re.findall(r'^        \("([^\"]+)", "([^\"]+)"\),$', self.state, re.MULTILINE))
        self.assertEqual(EXPECTED_ENDINGS, tuple(ending for ending, _ in mapping))
        self.assertEqual(
            tuple("ending_" + ending for ending in EXPECTED_ENDINGS),
            tuple(label for _, label in mapping),
        )
        self.assertEqual(len(mapping), len(set(label for _, label in mapping)))

    def test_baseline_declares_exact_fifteen_canonical_units(self):
        match = re.search(
            r"`canonical_production_units_v1`.*?以下 15 项.*?[:：]\r?\n\r?\n(?P<body>.*?)(?=\r?\n\r?\nProduction manifest)",
            self.baseline,
            re.DOTALL,
        )
        self.assertIsNotNone(match)
        units = tuple(re.findall(r"^\d+\. `([^`]+)`", match.group("body"), re.MULTILINE))
        self.assertEqual(15, len(units))
        self.assertEqual(15, len(set(units)))

    def test_content_lock_rows_match_current_source_generation(self):
        drift = []
        for path_text, locked_lines, locked_hash in LOCK_ROW.findall(self.content_lock):
            path = ROOT / Path(path_text)
            if not path.exists():
                drift.append((path_text, "MISSING"))
                continue
            actual_lines = len(path.read_text(encoding="utf-8").splitlines())
            actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual_lines != int(locked_lines) or actual_hash != locked_hash:
                drift.append(
                    (path_text, f"lock={locked_lines}/{locked_hash}; actual={actual_lines}/{actual_hash}")
                )
        self.assertEqual([], drift, "content-lock source drift: {}".format(drift))


if __name__ == "__main__":
    unittest.main()
