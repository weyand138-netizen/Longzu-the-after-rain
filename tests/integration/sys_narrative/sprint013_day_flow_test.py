import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "game" / "script.rpy"
ORCHESTRATOR = ROOT / "game" / "production_orchestrator.rpy"
CHAPTERS = ROOT / "game" / "chapters"
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
LOCK_ROW = re.compile(r"\| `([^`]+)` \|[^|]*\| (\d+) \| `([0-9a-f]{64})` \|")


def label_body(source, label):
    match = re.search(
        r"^label {}:\n(?P<body>.*?)(?=^label |\Z)".format(label),
        source,
        re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError("missing label: {}".format(label))
    return match.group("body")


class Sprint013DayFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SCRIPT.read_text(encoding="utf-8")
        cls.orchestrator = ORCHESTRATOR.read_text(encoding="utf-8")
        cls.lock = CONTENT_LOCK.read_text(encoding="utf-8")

    def test_production_entry_is_the_only_non_test_day_flow_owner(self):
        start = label_body(self.script, "start")
        body = label_body(self.orchestrator, "production_end_to_end_orchestrator")
        self.assertEqual(1, start.count("call production_end_to_end_orchestrator"))
        self.assertIn("if renpy.is_in_test():", start)
        self.assertEqual(
            EXPECTED_ORDER,
            tuple(re.findall(r"^    call (\w+)$", body, re.MULTILINE)),
        )
        self.assertNotIn("menu:", body)
        self.assertNotRegex(body, r"^    \$ ")

    def test_each_production_day_label_and_scene_source_is_present(self):
        for day, label in enumerate(EXPECTED_ORDER[1:], start=1):
            source = (CHAPTERS / "day{}.rpy".format(day)).read_text(encoding="utf-8")
            self.assertIn("label {}:".format(label), source)
            self.assertIn("scene bg", source)
        prologue = (CHAPTERS / "prologue.rpy").read_text(encoding="utf-8")
        self.assertIn("label prologue_start:", prologue)
        self.assertIn("scene bg", prologue)

    def test_current_content_lock_binds_the_flow_source_generation(self):
        drift = []
        for path_text, locked_lines, locked_hash in LOCK_ROW.findall(self.lock):
            path = ROOT / Path(path_text)
            actual_lines = len(path.read_text(encoding="utf-8").splitlines())
            actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual_lines != int(locked_lines) or actual_hash != locked_hash:
                drift.append(path_text)
        self.assertEqual([], drift, "content-lock drift blocks current Day 1-Day 7 evidence: {}".format(drift))


if __name__ == "__main__":
    unittest.main()
