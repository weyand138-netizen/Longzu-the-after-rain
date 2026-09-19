import hashlib
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "game"))

from modules.narrative_token_projection import (  # noqa: E402
    has_unresolved_token,
    unresolved_token_ids,
)


SOURCE_PATH = ROOT / "game" / "chapters" / "day5.rpy"
BASELINE_PATH = ROOT / "design" / "narrative" / "seven-day-content-baseline.md"
PARTIAL_MANIFEST_PATH = ROOT / "game" / "modules" / "narrative_partial_manifest.py"
DERIVATION_PATH = ROOT / "game" / "modules" / "day5_route_derivation.py"
EVIDENCE_PATH = ROOT / "production" / "qa" / "evidence" / "day5-authored-source-evidence.md"
SOURCE_GENERATION_PATH = ROOT / "game" / "modules" / "day5_source_generation.py"

EXPECTED_RECORDS = (
    ("day5_share_full_archive", "reaction_day5_share_full_archive", "payoff_day5_full_archive_day7"),
    ("day5_give_safe_summary", "reaction_day5_give_safe_summary", "payoff_day5_summary_day7"),
    ("day5_include_self_in_truth", "reaction_day5_include_self_in_truth", "payoff_day5_self_liability_ending"),
    ("day5_blame_family_only", "reaction_day5_blame_family_only", "payoff_day5_blame_day6"),
    ("day5_honor_erii_response", "reaction_day5_honor_erii_response", "payoff_day5_honor_day6"),
    ("day5_replace_erii_response", "reaction_day5_replace_erii_response", "payoff_day5_replace_ending"),
    ("day5_repair_daily_choice", "reaction_day5_repair_daily_choice", "payoff_repair_daily_choice"),
    ("day5_keep_daily_override", "reaction_day5_keep_daily_override", "payoff_keep_daily_override"),
    ("day5_repair_school_evidence", "reaction_day5_repair_school_evidence", "payoff_repair_school_truth"),
    ("day5_keep_school_evidence_hidden", "reaction_day5_keep_school_evidence_hidden", "payoff_keep_school_truth_hidden"),
)
FORBIDDEN_PLAYER_TERMS = (
    "隐藏分数",
    "路线标签",
    "结局条件",
    "正确选项",
    "预测",
    "持久状态",
    "测试夹具",
)


class Day5AuthoredSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE_PATH.read_text(encoding="utf-8")
        cls.baseline = BASELINE_PATH.read_text(encoding="utf-8")
        cls.partial_manifest = PARTIAL_MANIFEST_PATH.read_text(encoding="utf-8")
        cls.derivation = DERIVATION_PATH.read_text(encoding="utf-8")
        cls.evidence = EVIDENCE_PATH.read_text(encoding="utf-8")
        cls.source_generation = SOURCE_GENERATION_PATH.read_text(encoding="utf-8")

    def test_source_declares_only_the_canonical_day5_unit_and_scenes(self):
        self.assertEqual(1, self.source.count("label chapter_day5_family_lie:"))
        labels = tuple(re.findall(r"^label\s+([a-z0-9_]+):", self.source, re.MULTILINE))
        self.assertEqual(("chapter_day5_family_lie",), labels)
        self.assertIn('DAY5_SOURCE_UNIT_ID = "chapter_day5_family_lie"', self.source)
        for scene_id in (
            "scene_day5_family_archive",
            "scene_day5_truth_delivery",
            "scene_day5_response_answer",
            "scene_day5_shared_liability",
        ):
            self.assertIn(scene_id, self.source)
            self.assertIn("`{}`".format(scene_id), self.baseline)

    def test_choice_records_exactly_match_the_ten_approved_day5_choices(self):
        records_block = self.source.split("DAY5_CHOICE_RECORDS = (", 1)[1].split("DAY5_CHOICE_EFFECTS", 1)[0]
        records = tuple(
            re.findall(
                r'\(\s*"(day5_[a-z_]+)"\s*,\s*"(reaction_day5_[a-z_]+)"\s*,\s*"(payoff_[a-z0-9_]+)"',
                records_block,
            )
        )
        self.assertEqual(EXPECTED_RECORDS, records)
        for choice_id, reaction_id, payoff_id in records:
            self.assertEqual("reaction_" + choice_id, reaction_id)
            self.assertIn("`{}`".format(choice_id), self.baseline)
            self.assertIn("`{}`".format(payoff_id), self.baseline)

    def test_route_derivation_uses_only_the_closed_day4_resource_fact_set(self):
        derivation_call = self.source.split("derive_route_answer_record(", 1)[1].split(")\n    $ agency_day5_response_answer", 1)[0]
        for fact_id in (
            "resource_two_tickets",
            "resource_contact_card",
            "event_contact_risk_handover_complete",
            "resource_single_ticket",
        ):
            self.assertIn('"{}"'.format(fact_id), derivation_call)
        for forbidden in ("understanding", "autonomy", "truth", "preparation", "sacrifice", "persistent", "ending_"):
            self.assertNotIn(forbidden, derivation_call)
        self.assertIn("DAY5_SOURCE_SHA256", derivation_call)
        self.assertNotIn("renpy", self.derivation)
        self.assertNotIn("persistent", self.derivation)

    def test_visible_answer_action_precedes_registered_response_transaction(self):
        answer_assignment = 'agency_day5_response_answer = agency_day5_response_derivation_record["selected_answer_state_id"]'
        first_visible_action = 'narrator "她把两张票并排压在路线图上'
        request_assignment = "event_family_response_requested = True"
        first_response = 'apply_choice("day5_honor_erii_response"'
        self.assertLess(self.source.index(answer_assignment), self.source.index(first_visible_action))
        self.assertLess(self.source.index(first_visible_action), self.source.index(request_assignment))
        self.assertLess(self.source.index(request_assignment), self.source.index(first_response))
        self.assertIn("cp_day5_route_answer_expressed = True", self.source)

    def test_response_partition_and_outcomes_are_exact_and_nonempty(self):
        response_block = self.source.split("if agency_day5_response_answer != \"undetermined\":", 1)[1].split("    # scene_day5_shared_liability", 1)[0]
        self.assertEqual(1, response_block.count('apply_choice("day5_honor_erii_response"'))
        self.assertEqual(1, response_block.count('apply_choice("day5_replace_erii_response"'))
        self.assertIn('"outcome_route_preference_honored_" + agency_day5_response_answer', response_block)
        self.assertIn('"outcome_route_preference_overridden_to_old_order"', response_block)
        self.assertIn("event_route_preference_honored = True", response_block)
        self.assertIn("event_route_preference_overridden_to_old_order = True", response_block)
        self.assertIn('{"autonomy": 1}', response_block)
        self.assertIn('apply_choice("day5_replace_erii_response", {})', response_block)

    def test_repair_nodes_require_a_preexisting_token_and_project_canonical_history(self):
        self.assertIn('day5_daily_override_was_unresolved = has_unresolved_token("token_override_daily_choice")', self.source)
        self.assertIn("if day5_daily_override_was_unresolved:", self.source)
        self.assertIn('if has_unresolved_token("token_hide_school_evidence"):', self.source)
        history = (
            "day2_assign_alias",
            "day3_hide_school_evidence",
            "day5_replace_erii_response",
            "day5_repair_school_evidence",
            "day5_repair_daily_choice",
        )
        self.assertEqual((), unresolved_token_ids(history))
        self.assertFalse(has_unresolved_token(history, "token_hide_school_evidence"))
        self.assertFalse(has_unresolved_token(history, "token_override_daily_choice"))

    def test_truth_and_liability_events_follow_perceptible_reactions(self):
        for presentation, event in (
            ("她把原页、被划去的日期和没有答案的空白一并摊开", "event_full_archive_shared = True"),
            ("他在档案旁写下自己的名字和要承担的步骤", "event_self_liability_disclosed = True"),
        ):
            self.assertLess(self.source.index(presentation), self.source.index(event))
        self.assertLess(self.source.index("event_full_archive_shared = True"), self.source.index("cp_day5_full_archive_shared = True"))
        self.assertIn("event_external_blame_only = True", self.source)

    def test_player_safe_catalog_and_visible_copy_exclude_terminal_or_hidden_state(self):
        catalog_source = self.source.split("label chapter_day5_family_lie:", 1)[0]
        self.assertIn('"catalog_kind": "chapter"', catalog_source)
        self.assertIn('"catalog_kind": "memory"', catalog_source)
        self.assertIn('"memory_day5_route_answer"', catalog_source)
        for prohibited in ("choice_history", "persistent.", "live_flags", "ending_"):
            self.assertNotIn(prohibited, catalog_source)
        erii_lines = re.findall(r'^\s*erii\s+"([^"]*)"', self.source, re.MULTILINE)
        self.assertEqual([], erii_lines)
        visible_lines = "\n".join(line for line in self.source.splitlines() if line.lstrip().startswith(("narrator ", "lm ", '"')))
        for forbidden in FORBIDDEN_PLAYER_TERMS:
            self.assertNotIn(forbidden, visible_lines)

    def test_evidence_hash_matches_current_source_and_partial_manifest_stays_day1_only(self):
        recorded = re.search(r"^\*\*Source SHA-256\*\*: `([0-9a-f]{64})`$", self.evidence, re.MULTILINE)
        self.assertIsNotNone(recorded)
        self.assertEqual(hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest(), recorded.group(1))
        generated = re.search(r'^DAY5_SOURCE_SHA256 = "([0-9a-f]{64})"$', self.source_generation, re.MULTILINE)
        self.assertIsNotNone(generated)
        self.assertEqual(recorded.group(1), generated.group(1))
        self.assertIn('PARTIAL_MANIFEST_SCHEMA = "narrative_partial_day1_manifest:v1"', self.partial_manifest)
        self.assertNotIn("day5_", self.partial_manifest)
        self.assertIn("No Day 5 partial manifest", self.evidence)


if __name__ == "__main__":
    unittest.main()
