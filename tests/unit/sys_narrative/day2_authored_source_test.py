import hashlib
import re
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
GAME_DIR = PROJECT_ROOT / "game"
sys.path.insert(0, str(GAME_DIR))

from modules.narrative_token_projection import (  # noqa: E402
    has_unresolved_token,
    unresolved_token_ids,
)


SOURCE_PATH = PROJECT_ROOT / "game" / "chapters" / "day2.rpy"
BASELINE_PATH = PROJECT_ROOT / "design" / "narrative" / "seven-day-content-baseline.md"
EVIDENCE_PATH = (
    PROJECT_ROOT / "production" / "qa" / "evidence" / "day2-authored-source-evidence.md"
)

EXPECTED_DAY2_RECORDS = (
    ("day2_accept_alias", "reaction_day2_accept_alias", "payoff_day2_alias_day4"),
    ("day2_assign_alias", "reaction_day2_assign_alias", "payoff_day2_assigned_alias_day6"),
    (
        "day2_admit_alias_unknown",
        "reaction_day2_admit_alias_unknown",
        "payoff_day2_admit_day5",
    ),
    (
        "day2_save_second_token",
        "reaction_day2_save_second_token",
        "payoff_day2_token_day6",
    ),
    (
        "day2_spend_both_tokens",
        "reaction_day2_spend_both_tokens",
        "payoff_day2_spend_day4",
    ),
)
FORBIDDEN_PLAYER_TERMS = ("隐藏分数", "路线标签", "结局条件", "正确选项", "预测")


def source_hash(contents=None):
    """Return the canonical SHA-256 for the Day 2 authored source."""

    if contents is None:
        contents = SOURCE_PATH.read_bytes()
    return hashlib.sha256(contents).hexdigest()


class Day2AuthoredSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE_PATH.read_text(encoding="utf-8")
        cls.baseline = BASELINE_PATH.read_text(encoding="utf-8")
        cls.evidence = EVIDENCE_PATH.read_text(encoding="utf-8")

    def test_source_declares_only_the_canonical_day2_unit(self):
        units = re.findall(
            r"^\d+\. `(chapter_[^`]+|ending_[^`]+|epilogue_[^`]+)`$",
            self.baseline,
            re.MULTILINE,
        )
        self.assertEqual(15, len(units))
        self.assertIn("chapter_day2_two_game_tokens", units)
        self.assertEqual(1, self.source.count("label chapter_day2_two_game_tokens:"))
        self.assertIn('DAY2_SOURCE_UNIT_ID = "chapter_day2_two_game_tokens"', self.source)

    def test_source_contains_the_required_day2_scene_beats(self):
        for scene_id in (
            "scene_day2_alias_answer",
            "scene_day2_two_tokens",
            "scene_day2_last_machine",
        ):
            self.assertIn(scene_id, self.source)
        for observable in ("昵称", "两枚游戏币", "最里面那台机器"):
            self.assertIn(observable, self.source)

    def test_choice_records_exact_match_the_approved_day2_bindings(self):
        records_block = self.source.split("DAY2_CHOICE_RECORDS = (", 1)[1].split(
            "DAY2_CHOICE_EFFECTS", 1
        )[0]
        records = tuple(
            re.findall(
                r'\(\s*"(day2_[a-z_]+)"\s*,\s*"(reaction_day2_[a-z_]+)"\s*,\s*"(payoff_[a-z0-9_]+)"',
                records_block,
            )
        )
        self.assertEqual(EXPECTED_DAY2_RECORDS, records)
        for choice_id, reaction_id, payoff_id in records:
            self.assertEqual("reaction_" + choice_id, reaction_id)
            self.assertIn("`{}`".format(choice_id), self.baseline)
            self.assertIn("`{}`".format(payoff_id), self.baseline)

    def test_alias_repair_is_available_only_for_the_unresolved_silence_token(self):
        self.assertFalse(has_unresolved_token((), "token_silence_as_consent"))
        revoked_history = ("day1_assume_food_consent",)
        self.assertEqual(("token_silence_as_consent",), unresolved_token_ids(revoked_history))
        self.assertTrue(has_unresolved_token(revoked_history, "token_silence_as_consent"))
        repaired_history = revoked_history + ("day2_admit_alias_unknown",)
        self.assertEqual((), unresolved_token_ids(repaired_history))
        self.assertFalse(has_unresolved_token(repaired_history, "token_silence_as_consent"))
        self.assertEqual(
            ("token_override_daily_choice",),
            unresolved_token_ids(("day2_assign_alias",)),
        )
        self.assertIn('if has_unresolved_token("token_silence_as_consent"):', self.source)

    def test_erii_expression_and_player_visible_source_stay_safe(self):
        erii_lines = re.findall(r'^\s*erii\s+"([^"]*)"', self.source, re.MULTILINE)
        self.assertEqual(["嗯。"], erii_lines)
        for forbidden in FORBIDDEN_PLAYER_TERMS:
            self.assertNotIn(forbidden, self.source)

    def test_player_safe_catalog_inputs_are_common_facts_not_live_history(self):
        catalog_source = self.source.split("label chapter_day2_two_game_tokens:", 1)[0]
        self.assertIn('"catalog_kind": "chapter"', catalog_source)
        self.assertIn('"catalog_kind": "memory"', catalog_source)
        self.assertIn('"memory_day2_arcade_alias"', catalog_source)
        self.assertNotIn("choice_history", catalog_source)
        self.assertNotIn("persistent.", catalog_source)
        self.assertNotIn("live_flags", catalog_source)

    def test_owner_evidence_binds_the_current_source_hash(self):
        recorded_hash = re.search(
            r"^\*\*Source SHA-256\*\*: `([0-9a-f]{64})`$",
            self.evidence,
            re.MULTILINE,
        )
        self.assertIsNotNone(recorded_hash)
        self.assertEqual(source_hash(), recorded_hash.group(1))

    def test_stale_hash_input_is_rejected(self):
        self.assertNotEqual(source_hash(), source_hash(SOURCE_PATH.read_bytes() + b"\n# stale"))


if __name__ == "__main__":
    unittest.main()
