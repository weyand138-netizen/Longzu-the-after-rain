import hashlib
import re
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SOURCE_PATH = PROJECT_ROOT / "game" / "chapters" / "day1.rpy"
BASELINE_PATH = PROJECT_ROOT / "design" / "narrative" / "seven-day-content-baseline.md"
EVIDENCE_PATH = (
    PROJECT_ROOT / "production" / "qa" / "evidence" / "day1-authored-source-evidence.md"
)

EXPECTED_DAY1_CHOICES = {
    "day1_accept_clothing",
    "day1_choose_safe_clothing",
    "day1_repair_first_destination",
    "day1_keep_first_override",
    "day1_read_food_gesture",
    "day1_assume_food_consent",
}
FORBIDDEN_PLAYER_TERMS = (
    "隐藏分数",
    "路线标签",
    "结局条件",
    "正确选项",
    "预测",
)


def source_hash(contents=None):
    """Return the canonical SHA-256 for the Day 1 authored source."""

    if contents is None:
        contents = SOURCE_PATH.read_bytes()
    return hashlib.sha256(contents).hexdigest()


class Day1AuthoredSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE_PATH.read_text(encoding="utf-8")
        cls.baseline = BASELINE_PATH.read_text(encoding="utf-8")
        cls.evidence = EVIDENCE_PATH.read_text(encoding="utf-8")

    def test_source_declares_the_canonical_day1_unit_without_changing_baseline(self):
        units = re.findall(r"^\d+\. `(chapter_[^`]+|ending_[^`]+|epilogue_[^`]+)`$", self.baseline, re.MULTILINE)
        self.assertEqual(15, len(units))
        self.assertIn("chapter_day1_her_own_name", units)
        self.assertIn("label chapter_day1_her_own_name:", self.source)
        self.assertIn('DAY1_SOURCE_UNIT_ID = "chapter_day1_her_own_name"', self.source)

    def test_source_contains_the_required_day1_beats(self):
        for scene_id in (
            "scene_day1_clothing_answer",
            "scene_day1_food_gesture",
            "scene_day1_receipt_name",
        ):
            self.assertIn(scene_id, self.source)
        self.assertIn("收据", self.source)
        self.assertIn("名字", self.source)

    def test_choice_records_exact_match_the_approved_day1_subset(self):
        records_block = self.source.split("DAY1_CHOICE_RECORDS = (", 1)[1].split(
            "DAY1_PLAYER_SAFE_CATALOG_INPUTS", 1
        )[0]
        discovered = set(re.findall(r'"(day1_[a-z_]+)"', records_block))
        self.assertEqual(EXPECTED_DAY1_CHOICES, discovered)
        for choice_id in discovered:
            self.assertIn("`{}`".format(choice_id), self.baseline)

    def test_each_choice_has_canonical_reaction_and_payoff_identity(self):
        records = re.findall(
            r'\(\n\s+"(day1_[a-z_]+)",\n\s+"(reaction_day1_[a-z_]+)",\n\s+"(payoff_[a-z0-9_]+)",',
            self.source,
        )
        self.assertEqual(len(EXPECTED_DAY1_CHOICES), len(records))
        for choice_id, reaction_id, payoff_id in records:
            self.assertEqual("reaction_" + choice_id, reaction_id)
            self.assertIn("`{}`".format(payoff_id), self.baseline)

    def test_erii_expression_is_action_or_object_led_with_only_simple_speech(self):
        erii_lines = re.findall(r'^\s*erii\s+"([^"]*)"', self.source, re.MULTILINE)
        self.assertEqual(["嗯。", "嗯。"], erii_lines)
        for observable in ("手指", "衣角", "药盒", "收据"):
            self.assertIn(observable, self.source)

    def test_player_visible_source_uses_no_hidden_state_or_score_language(self):
        for forbidden in FORBIDDEN_PLAYER_TERMS:
            self.assertNotIn(forbidden, self.source)

    def test_player_safe_catalog_inputs_contain_only_observable_day1_facts(self):
        catalog_source = self.source.split("label chapter_day1_her_own_name:", 1)[0]
        self.assertIn('"catalog_kind": "chapter"', catalog_source)
        self.assertIn('"catalog_kind": "memory"', catalog_source)
        self.assertIn('"memory_day1_receipt_name"', catalog_source)
        self.assertNotIn("choice_history", catalog_source)
        self.assertNotIn("persistent.", catalog_source)
        self.assertNotIn("live_flags", catalog_source)

    def test_owner_evidence_binds_the_current_source_hash(self):
        recorded_hash = re.search(r"^\*\*Source SHA-256\*\*: `([0-9a-f]{64})`$", self.evidence, re.MULTILINE)
        self.assertIsNotNone(recorded_hash)
        self.assertEqual(source_hash(), recorded_hash.group(1))

    def test_stale_hash_input_is_rejected(self):
        self.assertNotEqual(source_hash(), source_hash(SOURCE_PATH.read_bytes() + b"\n# stale"))


if __name__ == "__main__":
    unittest.main()
