import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_PATH = ROOT / "game" / "chapters" / "day6.rpy"
BASELINE_PATH = ROOT / "design" / "narrative" / "seven-day-content-baseline.md"
DERIVATION_PATH = ROOT / "game" / "modules" / "day6_commitment_derivation.py"
SOURCE_GENERATION_PATH = ROOT / "game" / "modules" / "day6_source_generation.py"
EVIDENCE_PATH = ROOT / "production" / "qa" / "evidence" / "day6-authored-source-evidence.md"

EXPECTED_RECORDS = (
    ("day6_reopen_service_exit", "reaction_day6_reopen_service_exit", "payoff_day6_exit_ending"),
    ("day6_abandon_backup", "reaction_day6_abandon_backup", "payoff_day6_abandon_ending"),
    ("day6_use_service_exit", "reaction_day6_use_service_exit", "payoff_day6_use_exit_ending"),
    ("day6_keep_backup_abandoned", "reaction_day6_keep_backup_abandoned", "payoff_day6_keep_backup_ending"),
    ("day6_disclose_withheld_archive", "reaction_day6_disclose_withheld_archive", "payoff_day6_late_truth_ending"),
    ("day6_keep_archive_withheld", "reaction_day6_keep_archive_withheld", "payoff_day6_keep_truth_ending"),
    ("day6_burn_old_identity", "reaction_day6_burn_old_identity", "payoff_day6_identity_cost_ending"),
    ("day6_shift_cost_to_erii", "reaction_day6_shift_cost_to_erii", "payoff_day6_shift_cost_ending"),
    ("day6_take_cost_back", "reaction_day6_take_cost_back", "payoff_day6_take_back_ending"),
    ("day6_leave_cost_shifted", "reaction_day6_leave_cost_shifted", "payoff_day6_leave_cost_ending"),
    ("day6_commit_independent_contact", "reaction_day6_commit_independent_contact", "payoff_route_independent_ending"),
    ("day6_commit_shared_escape", "reaction_day6_commit_shared_escape", "payoff_route_shared_ending"),
    ("day6_commit_solo_departure", "reaction_day6_commit_solo_departure", "payoff_route_solo_ending"),
    ("day6_commit_old_order_return", "reaction_day6_commit_old_order_return", "payoff_route_old_order_ending"),
    ("day6_no_executable_route", "reaction_day6_no_executable_route", "payoff_route_collapse_ending"),
)


class Day6AuthoredSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE_PATH.read_text(encoding="utf-8")
        cls.chapter = cls.source.split("label chapter_day6_no_safe_house:", 1)[1]
        cls.baseline = BASELINE_PATH.read_text(encoding="utf-8")
        cls.derivation = DERIVATION_PATH.read_text(encoding="utf-8")
        cls.generation = SOURCE_GENERATION_PATH.read_text(encoding="utf-8")
        cls.evidence = EVIDENCE_PATH.read_text(encoding="utf-8")

    def test_source_declares_only_the_canonical_unit_and_four_frozen_scenes(self):
        self.assertEqual(1, self.source.count("label chapter_day6_no_safe_house:"))
        self.assertEqual(
            ("chapter_day6_no_safe_house",),
            tuple(re.findall(r"^label\s+([a-z0-9_]+):", self.source, re.MULTILINE)),
        )
        for scene_id in (
            "scene_day6_safehouse_failure",
            "scene_day6_backup_exit",
            "scene_day6_cost_inventory",
            "scene_day6_route_commitment",
        ):
            self.assertIn(scene_id, self.source)
            self.assertIn("`{}`".format(scene_id), self.baseline)

    def test_choice_records_exactly_match_the_fifteen_approved_day6_choices(self):
        records_block = self.source.split("DAY6_CHOICE_RECORDS = (", 1)[1].split("DAY6_CHOICE_EFFECTS", 1)[0]
        records = tuple(
            re.findall(
                r'\(\s*"(day6_[a-z_]+)"\s*,\s*"(reaction_day6_[a-z_]+)"\s*,\s*"(payoff_[a-z0-9_]+)"',
                records_block,
            )
        )
        self.assertEqual(EXPECTED_RECORDS, records)
        for choice_id, reaction_id, payoff_id in records:
            self.assertEqual("reaction_" + choice_id, reaction_id)
            self.assertIn("`{}`".format(choice_id), self.baseline)
            self.assertIn("`{}`".format(payoff_id), self.baseline)

    def test_backup_truth_and_cost_guards_preserve_the_frozen_branch_topology(self):
        self.assertIn('if has_unresolved_token("token_abandon_backup_plan"):', self.chapter)
        self.assertIn("if resource_service_exit:", self.chapter)
        self.assertIn("elif resource_service_exit:", self.chapter)
        self.assertIn('if has_unresolved_token("token_withhold_family_truth"):', self.chapter)
        self.assertIn('if event_shared_cost_promised and "day6_shift_cost_to_erii" not in choice_history:', self.chapter)
        shift_index = self.chapter.index('apply_choice("day6_shift_cost_to_erii"')
        visible_index = self.chapter.index("event_shifted_cost_consequence_visible = True")
        reconsider_index = self.chapter.index("event_cost_reconsideration_requested = True")
        take_back_index = self.chapter.index('apply_choice("day6_take_cost_back"')
        self.assertLess(shift_index, visible_index)
        self.assertLess(visible_index, reconsider_index)
        self.assertLess(reconsider_index, take_back_index)
        self.assertIn('apply_choice("day6_take_cost_back", {"sacrifice": 1})', self.chapter)
        self.assertIn("event_shifted_cost_confirmed = True", self.chapter)

    def test_derivation_receives_only_closed_day5_route_facts_and_day6_observable_facts(self):
        derivation_call = self.chapter.split("derive_commitment_record(", 1)[1].split("    )\n    $ agency_day6_commitment_state", 1)[0]
        for fact_id in (
            "day5_answer_state_id",
            "day5_response_outcome_id",
            "event_route_preference_honored",
            "event_route_preference_overridden_to_old_order",
            "resource_contact_card",
            "event_contact_risk_handover_complete",
            "resource_two_tickets",
            "event_shared_cost_acknowledged",
            "resource_single_ticket",
            "token_override_daily_choice_unresolved",
        ):
            self.assertIn('"{}"'.format(fact_id), derivation_call)
        self.assertIn("DAY6_SOURCE_SHA256", derivation_call)
        self.assertNotIn("persistent", self.derivation)
        self.assertNotIn("renpy", self.derivation)

    def test_chapter_stages_exactly_one_commitment_without_expanding_later_scope(self):
        for commitment in (
            "independent_contact",
            "shared_escape",
            "solo_departure",
            "old_order_return",
            "no_executable_route",
        ):
            self.assertIn('agency_day6_commitment_state == "{}"'.format(commitment), self.chapter)
            choice_id = "day6_no_executable_route" if commitment == "no_executable_route" else "day6_commit_" + commitment
            self.assertEqual(1, self.chapter.count('apply_choice("{}"'.format(choice_id)))
        self.assertEqual(1, self.chapter.count('apply_choice("day6_no_executable_route"'))
        for forbidden in (
            "Jump(",
            "call ",
            "qualification",
            "persistent",
            "terminal",
            "chapter_day7",
            "ending_",
            "resolver",
        ):
            self.assertNotIn(forbidden, self.chapter)
        self.assertEqual("return", self.chapter.strip().splitlines()[-1].strip())

    def test_commitment_events_follow_their_immediate_player_visible_reactions(self):
        for choice_id, reaction, event in (
            (
                "day6_commit_independent_contact",
                "他没有再替她拿卡",
                "event_independent_route_committed = True",
            ),
            (
                "day6_commit_shared_escape",
                "他把自己的票放在她那张旁边",
                "event_shared_route_committed = True",
            ),
            (
                "day6_commit_solo_departure",
                "他没有替她补上一张联系人卡",
                "event_solo_route_committed = True",
            ),
            (
                "day6_commit_old_order_return",
                "他把旧路线带离桌面",
                "event_old_order_route_committed = True",
            ),
            (
                "day6_no_executable_route",
                "他没有替她补上答案",
                "event_route_collapse = True",
            ),
        ):
            choice_index = self.chapter.index('apply_choice("{}"'.format(choice_id))
            reaction_index = self.chapter.index(reaction, choice_index)
            event_index = self.chapter.index(event, reaction_index)
            self.assertLess(choice_index, reaction_index)
            self.assertLess(reaction_index, event_index)

    def test_generated_hash_matches_current_authored_source(self):
        recorded = re.search(r'^DAY6_SOURCE_SHA256 = "([0-9a-f]{64})"$', self.generation, re.MULTILINE)
        self.assertIsNotNone(recorded)
        self.assertEqual(hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest(), recorded.group(1))
        self.assertIn(recorded.group(1), self.evidence)
        self.assertIn("zero hidden inputs", self.evidence)


if __name__ == "__main__":
    unittest.main()
