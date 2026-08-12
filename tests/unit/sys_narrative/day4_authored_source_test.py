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


SOURCE_PATH = PROJECT_ROOT / "game" / "chapters" / "day4.rpy"
BASELINE_PATH = PROJECT_ROOT / "design" / "narrative" / "seven-day-content-baseline.md"
PARTIAL_MANIFEST_PATH = (
    PROJECT_ROOT / "game" / "modules" / "narrative_partial_manifest.py"
)
EVIDENCE_PATH = (
    PROJECT_ROOT / "production" / "qa" / "evidence" / "day4-authored-source-evidence.md"
)

EXPECTED_DAY4_RECORDS = (
    (
        "day4_buy_two_tickets_real_name",
        "reaction_day4_buy_two_tickets_real_name",
        "payoff_day4_two_tickets_day6",
    ),
    (
        "day4_buy_single_ticket_cash",
        "reaction_day4_buy_single_ticket_cash",
        "payoff_day4_single_ticket_ending",
    ),
    (
        "day4_register_independent_contact",
        "reaction_day4_register_independent_contact",
        "payoff_day4_contact_ending",
    ),
    (
        "day4_decline_independent_contact",
        "reaction_day4_decline_independent_contact",
        "payoff_day4_decline_contact_ending",
    ),
    (
        "day4_follow_one_route_no_backup",
        "reaction_day4_follow_one_route_no_backup",
        "payoff_day4_no_backup_day6",
    ),
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


class Day4AuthoredSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE_PATH.read_text(encoding="utf-8")
        cls.baseline = BASELINE_PATH.read_text(encoding="utf-8")
        cls.partial_manifest = PARTIAL_MANIFEST_PATH.read_text(encoding="utf-8")
        cls.evidence = EVIDENCE_PATH.read_text(encoding="utf-8")

    def test_source_declares_only_the_canonical_day4_unit_and_scenes(self):
        self.assertEqual(1, self.source.count("label chapter_day4_seaside_train:"))
        self.assertIn('DAY4_SOURCE_UNIT_ID = "chapter_day4_seaside_train"', self.source)
        labels = tuple(re.findall(r"^label\s+([a-z0-9_]+):", self.source, re.MULTILINE))
        self.assertEqual(("chapter_day4_seaside_train",), labels)
        for scene_id in (
            "scene_day4_ticket_counter",
            "scene_day4_route_answer",
            "scene_day4_contact_channel",
            "scene_day4_sea_window",
        ):
            self.assertIn(scene_id, self.source)
            self.assertIn("`{}`".format(scene_id), self.baseline)

    def test_choice_records_exactly_match_the_approved_day4_choices(self):
        records_block = self.source.split("DAY4_CHOICE_RECORDS = (", 1)[1].split(
            "DAY4_CHOICE_EFFECTS", 1
        )[0]
        records = tuple(
            re.findall(
                r'\(\s*"(day4_[a-z_]+)"\s*,\s*"(reaction_day4_[a-z_]+)"\s*,\s*"(payoff_[a-z0-9_]+)"',
                records_block,
            )
        )
        self.assertEqual(EXPECTED_DAY4_RECORDS, records)
        for choice_id, reaction_id, payoff_id in records:
            self.assertEqual("reaction_" + choice_id, reaction_id)
            self.assertIn("`{}`".format(choice_id), self.baseline)
            self.assertIn("`{}`".format(payoff_id), self.baseline)

    def test_route_answer_is_perceptible_and_registered_before_response_choices(self):
        answer_presentation = "她用指尖分别压住车次、窗口座位和联系人纸片"
        answer_assignment = (
            "agency_day4_route_preparation_answer = DAY4_ROUTE_PREPARATION_ANSWER_STATE"
        )
        first_response = 'apply_choice("day4_buy_two_tickets_real_name"'
        self.assertIn(answer_presentation, self.source)
        self.assertIn(answer_assignment, self.source)
        self.assertLess(self.source.index(answer_presentation), self.source.index(answer_assignment))
        self.assertLess(self.source.index(answer_assignment), self.source.index(first_response))
        self.assertIn(
            'DAY4_ROUTE_PREPARATION_ANSWER_STATE = "preserve_executable_self_controlled_option"',
            self.source,
        )
        self.assertIn('agency_day4_route_preparation_outcome = "outcome_shared_option_prepared"', self.source)
        self.assertIn('agency_day4_route_preparation_outcome = "outcome_solo_option_prepared"', self.source)
        self.assertIn('agency_day4_route_preparation_outcome = "outcome_self_controlled_option_not_prepared"', self.source)

    def test_two_ticket_completion_follows_perceptible_ticket_and_identity_cost(self):
        presentation = "两张靠窗票落进她掌心"
        completion_event = "$ event_two_window_tickets_acquired = True"
        checkpoint = "$ cp_day4_two_tickets_complete = True"
        self.assertIn(presentation, self.source)
        self.assertLess(self.source.index(presentation), self.source.index(completion_event))
        self.assertLess(self.source.index(completion_event), self.source.index(checkpoint))
        self.assertIn("event_identity_exposed = True", self.source)
        self.assertIn("resource_two_tickets = True", self.source)

    def test_independent_contact_requires_the_retained_day2_token_and_alias(self):
        contact_guard = '''if (
        "day2_save_second_token" in choice_history
        and (
            "day2_accept_alias" in choice_history
            or "day2_admit_alias_unknown" in choice_history
        )
    ):'''
        self.assertIn(contact_guard, self.source)
        self.assertIn("她自己念出昵称的读法", self.source)
        self.assertIn("resource_contact_card = True", self.source)
        self.assertIn("event_contact_risk_handover_complete = True", self.source)
        self.assertIn("event_contact_channel_declined = True", self.source)
        self.assertEqual(
            ("token_abandon_backup_plan",),
            unresolved_token_ids(("day4_follow_one_route_no_backup",)),
        )
        self.assertTrue(
            has_unresolved_token(
                ("day4_decline_independent_contact",), "token_abandon_backup_plan"
            )
        )

    def test_player_safe_catalog_inputs_and_copy_exclude_live_or_terminal_state(self):
        catalog_source = self.source.split("label chapter_day4_seaside_train:", 1)[0]
        self.assertIn('"catalog_kind": "chapter"', catalog_source)
        self.assertIn('"catalog_kind": "memory"', catalog_source)
        self.assertIn('"memory_day4_seaside_window"', catalog_source)
        for prohibited in ("persistent.", "live_flags", "ending_"):
            self.assertNotIn(prohibited, catalog_source)
        visible_lines = "\n".join(
            line
            for line in self.source.splitlines()
            if line.lstrip().startswith(("narrator ", "lm ", '"'))
        )
        for forbidden in FORBIDDEN_PLAYER_TERMS:
            self.assertNotIn(forbidden, visible_lines)

    def test_evidence_binds_current_hash_and_day1_only_manifest_is_unchanged(self):
        recorded_hash = re.search(
            r"^\*\*Source SHA-256\*\*: `([0-9a-f]{64})`$",
            self.evidence,
            re.MULTILINE,
        )
        self.assertIsNotNone(recorded_hash)
        self.assertEqual(
            hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest(), recorded_hash.group(1)
        )
        self.assertIn('PARTIAL_MANIFEST_SCHEMA = "narrative_partial_day1_manifest:v1"', self.partial_manifest)
        self.assertNotIn("day4_", self.partial_manifest)
        self.assertIn("No Day 4 partial manifest", self.evidence)


if __name__ == "__main__":
    unittest.main()
