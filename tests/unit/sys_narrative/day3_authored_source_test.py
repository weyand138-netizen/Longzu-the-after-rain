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


SOURCE_PATH = PROJECT_ROOT / "game" / "chapters" / "day3.rpy"
BASELINE_PATH = PROJECT_ROOT / "design" / "narrative" / "seven-day-content-baseline.md"
PARTIAL_MANIFEST_PATH = (
    PROJECT_ROOT / "game" / "modules" / "narrative_partial_manifest.py"
)
EVIDENCE_PATH = (
    PROJECT_ROOT / "production" / "qa" / "evidence" / "day3-authored-source-evidence.md"
)

EXPECTED_DAY3_RECORDS = (
    (
        "day3_share_school_evidence",
        "reaction_day3_share_school_evidence",
        "payoff_day3_share_day5",
    ),
    (
        "day3_hide_school_evidence",
        "reaction_day3_hide_school_evidence",
        "payoff_day3_hide_day5",
    ),
    ("day3_honor_pause", "reaction_day3_honor_pause", "payoff_day3_pause_day5"),
    (
        "day3_force_explanation",
        "reaction_day3_force_explanation",
        "payoff_day3_force_day6",
    ),
)
EXPECTED_DAY3_PAYOFF_UNITS = {
    "payoff_day3_share_day5": "chapter_day5_family_lie",
    "payoff_day3_hide_day5": "chapter_day5_family_lie",
    "payoff_day3_pause_day5": "chapter_day5_family_lie",
    "payoff_day3_force_day6": "chapter_day6_no_safe_house",
}
FORBIDDEN_PLAYER_TERMS = (
    "隐藏分数",
    "路线标签",
    "结局条件",
    "正确选项",
    "预测",
    "持久状态",
    "测试夹具",
)


def source_hash(contents=None):
    """Return the canonical SHA-256 for the Day 3 authored source."""

    if contents is None:
        contents = SOURCE_PATH.read_bytes()
    return hashlib.sha256(contents).hexdigest()


class Day3AuthoredSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE_PATH.read_text(encoding="utf-8")
        cls.baseline = BASELINE_PATH.read_text(encoding="utf-8")
        cls.partial_manifest = PARTIAL_MANIFEST_PATH.read_text(encoding="utf-8")
        cls.evidence = EVIDENCE_PATH.read_text(encoding="utf-8")

    def test_source_declares_only_the_canonical_day3_unit(self):
        units = re.findall(
            r"^\d+\. `(chapter_[^`]+|ending_[^`]+|epilogue_[^`]+)`$",
            self.baseline,
            re.MULTILINE,
        )
        self.assertEqual(15, len(units))
        self.assertIn("chapter_day3_empty_school", units)
        self.assertEqual(1, self.source.count("label chapter_day3_empty_school:"))
        self.assertIn('DAY3_SOURCE_UNIT_ID = "chapter_day3_empty_school"', self.source)

    def test_source_declares_no_extra_day3_production_labels(self):
        labels = tuple(
            re.findall(r"^label\s+([a-z0-9_]+):", self.source, re.MULTILINE)
        )
        self.assertEqual(("chapter_day3_empty_school",), labels)

    def test_source_contains_required_scenes_and_perceptible_trace_completion_order(self):
        for scene_id in (
            "scene_day3_classroom_trace",
            "scene_day3_evidence_choice",
            "scene_day3_truth_pace_answer",
        ):
            self.assertIn(scene_id, self.source)
        trace_presentation = "门禁、时间和泥印指向同一段来路"
        self.assertIn(trace_presentation, self.source)
        self.assertLess(
            self.source.index(trace_presentation),
            self.source.index("$ event_empty_school_trace_confirmed = True"),
        )
        self.assertLess(
            self.source.index("$ event_empty_school_trace_confirmed = True"),
            self.source.index("$ cp_day3_empty_school_trace_complete = True"),
        )

    def test_choice_records_exactly_match_the_two_approved_day3_nodes(self):
        records_block = self.source.split("DAY3_CHOICE_RECORDS = (", 1)[1].split(
            "DAY3_CHOICE_EFFECTS", 1
        )[0]
        records = tuple(
            re.findall(
                r'\(\s*"(day3_[a-z_]+)"\s*,\s*"(reaction_day3_[a-z_]+)"\s*,\s*"(payoff_[a-z0-9_]+)"',
                records_block,
            )
        )
        self.assertEqual(EXPECTED_DAY3_RECORDS, records)
        for choice_id, reaction_id, payoff_id in records:
            self.assertEqual("reaction_" + choice_id, reaction_id)
            self.assertIn("`{}`".format(choice_id), self.baseline)
            self.assertIn("`{}`".format(payoff_id), self.baseline)

    def test_payoff_identities_target_baseline_defined_later_units(self):
        unit_ids = tuple(
            re.findall(
                r"^\d+\. `(chapter_[^`]+|ending_[^`]+|epilogue_[^`]+)`$",
                self.baseline,
                re.MULTILINE,
            )
        )
        day3_index = unit_ids.index("chapter_day3_empty_school")
        for _, _, payoff_id in EXPECTED_DAY3_RECORDS:
            self.assertIn(payoff_id, EXPECTED_DAY3_PAYOFF_UNITS)
            self.assertIn("`{}`".format(payoff_id), self.baseline)
            payoff_unit_id = EXPECTED_DAY3_PAYOFF_UNITS[payoff_id]
            self.assertIn(payoff_unit_id, unit_ids)
            self.assertGreater(unit_ids.index(payoff_unit_id), day3_index)

    def test_matching_menu_branch_commits_before_its_immediate_reaction(self):
        expected_reactions = {
            "day3_share_school_evidence": "她把三张纸一张张看完",
            "day3_hide_school_evidence": "她听完结论",
            "day3_honor_pause": "他把档案收在桌边",
            "day3_force_explanation": "他继续把余下的说明念完",
        }
        menu_blocks = self.source.split("    menu:\n")[1:]
        self.assertEqual(2, len(menu_blocks))
        branch_by_choice = {}
        for menu_block in menu_blocks:
            for branch in re.finditer(
                r'(?m)^        "[^\n]+":\n(?P<body>(?:            [^\n]*\n|\n)*)',
                menu_block,
            ):
                body = branch.group("body")
                choice_ids = re.findall(r'apply_choice\("(day3_[a-z_]+)"', body)
                self.assertLessEqual(len(choice_ids), 1)
                if choice_ids:
                    branch_by_choice[choice_ids[0]] = body

        self.assertEqual({record[0] for record in EXPECTED_DAY3_RECORDS}, set(branch_by_choice))
        for choice_id, reaction in expected_reactions.items():
            branch = branch_by_choice[choice_id]
            self.assertLess(
                branch.index('apply_choice("{}"'.format(choice_id)),
                branch.index(reaction),
            )

    def test_day3_revoke_choices_project_their_canonical_unresolved_tokens(self):
        history = (
            "day2_assign_alias",
            "day3_hide_school_evidence",
            "day3_force_explanation",
        )
        self.assertEqual(
            ("token_override_daily_choice", "token_hide_school_evidence"),
            unresolved_token_ids(history),
        )
        self.assertTrue(has_unresolved_token(history, "token_hide_school_evidence"))
        self.assertTrue(has_unresolved_token(history, "token_override_daily_choice"))

    def test_truth_pace_request_answer_contract_is_private_and_exact(self):
        self.assertIn(
            'DAY3_AGENCY_REQUEST_ID = "event_truth_pace_requested"', self.source
        )
        self.assertIn(
            'DAY3_AGENCY_PAUSE_ANSWER_ID = "event_erii_closes_archive"', self.source
        )
        self.assertLess(
            self.source.index("agency_day3_truth_pace_request = DAY3_AGENCY_REQUEST_ID"),
            self.source.index("agency_day3_truth_pace_answer = DAY3_AGENCY_PAUSE_ANSWER_ID"),
        )
        self.assertIn('agency_day3_truth_pace_outcome = "outcome_pause_honored"', self.source)
        self.assertIn(
            'agency_day3_truth_pace_outcome = "outcome_pause_overridden"', self.source
        )

    def test_erii_expression_and_player_visible_copy_remain_safe(self):
        erii_lines = re.findall(r'^\s*erii\s+"([^"]*)"', self.source, re.MULTILINE)
        self.assertEqual([], erii_lines)
        visible_lines = "\n".join(
            line
            for line in self.source.splitlines()
            if line.lstrip().startswith(("narrator ", "lm ", '"'))
        )
        for forbidden in FORBIDDEN_PLAYER_TERMS:
            self.assertNotIn(forbidden, visible_lines)
        for observable in ("红泥", "门禁记录", "档案", "指尖"):
            self.assertIn(observable, self.source)

    def test_player_safe_catalog_inputs_exclude_live_or_terminal_state(self):
        catalog_source = self.source.split("label chapter_day3_empty_school:", 1)[0]
        self.assertIn('"catalog_kind": "chapter"', catalog_source)
        self.assertIn('"catalog_kind": "memory"', catalog_source)
        self.assertIn('"memory_day3_empty_school_trace"', catalog_source)
        for prohibited in ("choice_history", "persistent.", "live_flags", "ending_"):
            self.assertNotIn(prohibited, catalog_source)

    def test_evidence_binds_current_hash_and_day1_only_partial_manifest_is_unchanged(self):
        recorded_hash = re.search(
            r"^\*\*Source SHA-256\*\*: `([0-9a-f]{64})`$",
            self.evidence,
            re.MULTILINE,
        )
        self.assertIsNotNone(recorded_hash)
        self.assertEqual(source_hash(), recorded_hash.group(1))
        self.assertNotEqual(source_hash(), source_hash(SOURCE_PATH.read_bytes() + b"\n# stale"))
        self.assertIn('PARTIAL_MANIFEST_SCHEMA = "narrative_partial_day1_manifest:v1"', self.partial_manifest)
        self.assertNotIn("day3_", self.partial_manifest)
        self.assertIn("No Day 3 partial manifest", self.evidence)


if __name__ == "__main__":
    unittest.main()
