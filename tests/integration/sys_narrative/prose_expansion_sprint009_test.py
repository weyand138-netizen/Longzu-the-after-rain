import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHAPTERS = ROOT / "game" / "chapters"
GDD = ROOT / "design" / "gdd" / "seven-day-chapter-script.md"
BASELINE = ROOT / "design" / "narrative" / "seven-day-content-baseline.md"
LOCK = ROOT / "design" / "content-lock.md"
STORY = ROOT / "production" / "epics" / "sys-narrative" / "story-026-prologue-day1-day2-prose-expansion.md"

SOURCES = {
    "game/chapters/prologue.rpy": CHAPTERS / "prologue.rpy",
    "game/chapters/day1.rpy": CHAPTERS / "day1.rpy",
    "game/chapters/day2.rpy": CHAPTERS / "day2.rpy",
}
EXPECTED_CHOICES = {
    "prologue.rpy": (
        ("prologue_read_note", ("understanding",)),
        ("prologue_hurry_to_train", ()),
        ("prologue_ask_destination", ()),
        ("prologue_accept_destination", ("autonomy",)),
        ("prologue_override_destination", ()),
        ("prologue_choose_route", ()),
        ("prologue_notice_service_exit", ("preparation",)),
        ("prologue_notice_tracker", ("truth",)),
        ("prologue_promise_cost", ()),
    ),
    "day1.rpy": (
        ("day1_accept_clothing", ("autonomy",)),
        ("day1_choose_safe_clothing", ()),
        ("day1_read_food_gesture", ("understanding",)),
        ("day1_assume_food_consent", ()),
    ),
    "day2.rpy": (
        ("day2_accept_alias", ("understanding", "autonomy")),
        ("day2_assign_alias", ()),
        ("day2_admit_alias_unknown", ("understanding",)),
        ("day2_save_second_token", ("preparation",)),
        ("day2_spend_both_tokens", ("sacrifice",)),
    ),
}
EXPECTED_CONTROL_COUNTS = {
    "prologue.rpy": {"label": 1, "menu": 4, "scene": 3, "call": 1, "jump": 0},
    "day1.rpy": {"label": 1, "menu": 2, "scene": 2, "call": 0, "jump": 0},
    "day2.rpy": {"label": 1, "menu": 2, "scene": 1, "call": 0, "jump": 0},
}
FORBIDDEN_PLAYER_RULES = re.compile(
    r"(?:axis|token|qualification|resolver|persistent|hidden\s+(?:score|state|number)|ending\s+(?:condition|prediction))",
    re.IGNORECASE,
)
FORBIDDEN_ASSETS = re.compile(r"(?:image|audio|music|voice|ui|assets?)/", re.IGNORECASE)


def player_lines(source):
    return tuple(
        line.strip()
        for line in source.splitlines()
        if re.match(r"^(?:narrator|lm|erii)\s+\"", line.strip())
    )


class ProseExpansionSprint009Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {name: path.read_text(encoding="utf-8") for name, path in SOURCES.items()}
        cls.lock = LOCK.read_text(encoding="utf-8")
        cls.baseline = BASELINE.read_text(encoding="utf-8")
        cls.gdd = GDD.read_text(encoding="utf-8")
        cls.story = STORY.read_text(encoding="utf-8")

    def test_existing_control_contracts_are_exact(self):
        for filename, expected in EXPECTED_CHOICES.items():
            source = self.sources["game/chapters/{}".format(filename)]
            actual = tuple(
                (choice_id, tuple(re.findall(r'"([a-z_]+)"\s*:\s*1', delta_text)))
                for choice_id, delta_text in re.findall(
                    r'apply_choice\("([a-z0-9_]+)",\s*\{([^}]*)\}\)', source
                )
            )
            self.assertEqual(expected, actual, filename)
            for control, expected_count in EXPECTED_CONTROL_COUNTS[filename].items():
                self.assertEqual(
                    expected_count,
                    len(re.findall(r"^\s*{}\b".format(control), source, re.MULTILINE)),
                    (filename, control),
                )

        self.assertEqual(1, self.sources["game/chapters/prologue.rpy"].count('label prologue_start:'))
        self.assertEqual(1, self.sources["game/chapters/day1.rpy"].count('label chapter_day1_her_own_name:'))
        self.assertEqual(1, self.sources["game/chapters/day2.rpy"].count('label chapter_day2_two_game_tokens:'))
        self.assertIn('resource_service_exit = True', self.sources["game/chapters/prologue.rpy"])
        self.assertIn('renpy.save_persistent()', self.sources["game/chapters/prologue.rpy"])

    def test_only_observable_prose_expands_without_hidden_rule_disclosure(self):
        for filename, source in self.sources.items():
            self.assertNotRegex(source, FORBIDDEN_ASSETS, filename)
            for line in player_lines(source):
                self.assertNotRegex(line, FORBIDDEN_PLAYER_RULES, (filename, line))

        self.assertIn("Formal Prose Expansion Boundary", self.gdd)
        self.assertIn("| 009 |", self.baseline)
        self.assertIn("Story 026", self.story)

    def test_current_content_lock_hashes_bind_all_sprint_sources(self):
        self.assertIn("content_lock:player_visible:v6:2026-08-14", self.lock)
        for source_name, path in SOURCES.items():
            pattern = r"\| `{}` \|.*?\|\s*(\d+)\s*\|\s*`([0-9a-f]{{64}})`\s*\|".format(
                re.escape(source_name)
            )
            match = re.search(pattern, self.lock)
            self.assertIsNotNone(match, source_name)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), match.group(2), source_name)
            self.assertEqual(len(path.read_text(encoding="utf-8").splitlines()), int(match.group(1)), source_name)

        baseline_hash = hashlib.sha256(BASELINE.read_bytes()).hexdigest()
        self.assertIn(baseline_hash, self.lock)


if __name__ == "__main__":
    unittest.main()
