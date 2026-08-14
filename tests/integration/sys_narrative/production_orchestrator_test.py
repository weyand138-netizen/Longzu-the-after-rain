import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "game" / "script.rpy"
ORCHESTRATOR = ROOT / "game" / "production_orchestrator.rpy"
DAY7 = ROOT / "game" / "chapters" / "day7.rpy"
CHAPTERS = ROOT / "game" / "chapters"

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


def label_block(source, label):
    match = re.search(
        r"^label {}:\n(?P<body>.*?)(?=^label |\Z)".format(label),
        source,
        re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError("missing label: {}".format(label))
    return match.group("body")


class ProductionOrchestratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SCRIPT.read_text(encoding="utf-8")
        cls.orchestrator = ORCHESTRATOR.read_text(encoding="utf-8")
        cls.day7 = DAY7.read_text(encoding="utf-8")

    def test_start_has_one_production_entry_and_no_direct_chapter_jump(self):
        start = label_block(self.script, "start")
        self.assertEqual(1, start.count("call production_end_to_end_orchestrator"))
        self.assertNotIn("jump prologue_start", start)
        self.assertIn("if renpy.is_in_test():", start)
        self.assertIn("call prologue_start", start)
        self.assertIn("$ reset_run_state()", start)
        self.assertIn("return", start)

    def test_orchestrator_has_exact_fixed_chapter_order(self):
        body = label_block(self.orchestrator, "production_end_to_end_orchestrator")
        calls = tuple(re.findall(r"^    call (\w+)$", body, re.MULTILINE))
        self.assertEqual(EXPECTED_ORDER, calls)
        self.assertEqual(1, body.count("return"))
        self.assertNotIn("menu:", body)
        self.assertNotRegex(body, r"^    \$ ")
        self.assertNotIn("jump ", body)

    def test_chapter_labels_remain_independent_and_day7_owns_terminal_handoff(self):
        for chapter_id in EXPECTED_ORDER:
            if chapter_id == "prologue_start":
                source_path = CHAPTERS / "prologue.rpy"
            else:
                day = re.search(r"day(\d+)", chapter_id).group(1)
                source_path = CHAPTERS / "day{}.rpy".format(day)
            source = source_path.read_text(encoding="utf-8")
            self.assertIn("label {}:".format(chapter_id), source)

        self.assertEqual(1, self.day7.count("jump day7_resolve_ending"))
        self.assertNotIn("production_end_to_end_orchestrator", self.day7)


if __name__ == "__main__":
    unittest.main()
