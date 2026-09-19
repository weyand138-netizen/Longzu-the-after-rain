import sys
import ast
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GAME_DIR = PROJECT_ROOT / "game"
sys.path.insert(0, str(GAME_DIR))

from modules.ending_rules import (  # noqa: E402
    AXES,
    ClauseEvaluationTraceEntry,
    EndingResolutionRecord,
    ENDING_PRIORITY,
    _CAUSE_TEMPLATE_INDEX,
    _PREDICATE_INDEX,
    resolve_ending,
    resolve_ending_record,
    validate_snapshot,
)


def snapshot(history, axis_values):
    return {
        "schema_version": 2,
        "axes": dict(zip(AXES, axis_values)),
        "choice_history": tuple(history),
    }


WITNESSES = {
    "rain_stops": (
        ("prologue_read_note", "prologue_ask_destination", "prologue_accept_destination", "prologue_notice_tracker", "day1_accept_clothing", "day1_read_food_gesture", "day2_accept_alias", "day2_save_second_token", "day3_share_school_evidence", "day3_honor_pause", "day4_buy_two_tickets_real_name", "day4_register_independent_contact", "day5_share_full_archive", "day5_include_self_in_truth", "day5_honor_erii_response", "day6_burn_old_identity", "day6_commit_shared_escape"),
        (3, 3, 3, 3, 3),
    ),
    "her_own_name": (
        ("prologue_read_note", "prologue_ask_destination", "prologue_accept_destination", "prologue_notice_tracker", "day1_accept_clothing", "day1_read_food_gesture", "day2_accept_alias", "day2_save_second_token", "day3_share_school_evidence", "day3_honor_pause", "day4_follow_one_route_no_backup", "day4_register_independent_contact", "day5_share_full_archive", "day5_blame_family_only", "day5_honor_erii_response", "day6_keep_backup_abandoned", "day6_burn_old_identity", "day6_commit_independent_contact"),
        (3, 3, 3, 1, 1),
    ),
    "see_the_sea": (
        ("prologue_hurry_to_train", "prologue_ask_destination", "prologue_accept_destination", "prologue_promise_cost", "day1_accept_clothing", "day1_assume_food_consent", "day2_accept_alias", "day2_save_second_token", "day3_share_school_evidence", "day3_honor_pause", "day4_buy_two_tickets_real_name", "day4_register_independent_contact", "day5_share_full_archive", "day5_include_self_in_truth", "day5_honor_erii_response", "day6_burn_old_identity", "day6_commit_shared_escape"),
        (2, 3, 3, 3, 3),
    ),
    "one_person_train": (
        ("prologue_read_note", "prologue_ask_destination", "prologue_accept_destination", "prologue_promise_cost", "day1_accept_clothing", "day1_assume_food_consent", "day2_accept_alias", "day2_spend_both_tokens", "day3_share_school_evidence", "day3_honor_pause", "day4_buy_single_ticket_cash", "day5_give_safe_summary", "day5_blame_family_only", "day5_honor_erii_response", "day6_keep_archive_withheld", "day6_burn_old_identity", "day6_commit_solo_departure"),
        (3, 3, 1, 1, 2),
    ),
    "golden_cage": (
        ("prologue_hurry_to_train", "prologue_choose_route", "prologue_promise_cost", "day1_keep_first_override", "day1_read_food_gesture", "day2_accept_alias", "day2_save_second_token", "day3_share_school_evidence", "day3_honor_pause", "day4_buy_single_ticket_cash", "day4_register_independent_contact", "day5_share_full_archive", "day5_blame_family_only", "day5_replace_erii_response", "day5_keep_daily_override", "day6_burn_old_identity", "day6_commit_old_order_return"),
        (3, 2, 3, 2, 1),
    ),
    "unsent_postcard": (
        ("prologue_hurry_to_train", "prologue_choose_route", "prologue_promise_cost", "day1_keep_first_override", "day1_assume_food_consent", "day2_assign_alias", "day2_spend_both_tokens", "day3_hide_school_evidence", "day3_force_explanation", "day4_follow_one_route_no_backup", "day5_give_safe_summary", "day5_blame_family_only", "day5_honor_erii_response", "day5_keep_school_evidence_hidden", "day5_keep_daily_override", "day6_keep_backup_abandoned", "day6_keep_archive_withheld", "day6_shift_cost_to_erii", "day6_leave_cost_shifted", "day6_no_executable_route"),
        (0, 1, 0, 0, 1),
    ),
}


class EndingRuleTests(unittest.TestCase):
    def test_all_frozen_canonical_witnesses_resolve_once(self):
        observed = set()
        for expected, (history, axes) in WITNESSES.items():
            with self.subTest(expected=expected):
                value = snapshot(history, axes)
                record = resolve_ending_record(value)
                self.assertIs(type(record), EndingResolutionRecord)
                self.assertEqual(expected, record.ending_id)
                self.assertEqual(expected, resolve_ending(value))
                self.assertGreaterEqual(len(record.display_cause_ids), 1)
                self.assertLessEqual(len(record.display_cause_ids), 3)
                observed.add(record.ending_id)
        self.assertEqual(set(ENDING_PRIORITY), observed)

    def test_golden_cage_uses_only_replace_and_keeps_its_zero_axis_projection(self):
        history, axes = WITNESSES["golden_cage"]
        self.assertIn("day5_replace_erii_response", history)
        self.assertNotIn("day5_honor_erii_response", history)
        record = resolve_ending_record(snapshot(history, axes))
        self.assertEqual(record.ending_id, "golden_cage")
        self.assertEqual(axes, (3, 2, 3, 2, 1))

    def test_record_is_immutable_and_has_exact_public_field_order(self):
        history, axes = WITNESSES["rain_stops"]
        record = resolve_ending_record(snapshot(history, axes))
        self.assertEqual(tuple(record._fields), (
            "ending_id", "unresolved_token_ids", "unresolved_token_causes",
            "completed_event_ids", "resource_possession_ids", "qualification_ids",
            "clause_evaluation_trace", "matched_causes",
            "higher_priority_exclusions", "display_cause_ids",
        ))
        with self.assertRaises(AttributeError):
            record.ending_id = "unsent_postcard"
        self.assertTrue(all(type(item) is ClauseEvaluationTraceEntry for item in record.clause_evaluation_trace))
        self.assertTrue(all(type(item.source_reference_ids) is tuple for item in record.clause_evaluation_trace))

    def test_frozen_predicate_catalog_is_complete_and_golden_hashes_remain_stable(self):
        for ending_id in ENDING_PRIORITY:
            records = tuple(sorted(
                (record for (ending, _clause_id), record in _PREDICATE_INDEX.items() if ending == ending_id),
                key=lambda record: record.clause_order,
            ))
            self.assertEqual(tuple(record.clause_order for record in records), tuple(range(len(records))))
            self.assertEqual(records[0].clause_id, "{}_root".format(ending_id))
            self.assertEqual(sum(record.clause_id.endswith("_root") for record in records), 1)
        self.assertEqual(
            _PREDICATE_INDEX[("unsent_postcard", "unsent_postcard_root")].match_cause_template_id,
            "cause_unsent_postcard_fallback",
        )
        record = resolve_ending_record(snapshot(*WITNESSES["rain_stops"]))
        understanding = next(
            cause for cause in record.matched_causes
            if cause.clause_id == "rain_stops_axis_understanding_at_least_3"
        )
        self.assertEqual(understanding.cause_id, "cause_8d6112f9e5f8292f03db2560738b124cbe429e2d1ea40095e979bfd29ebaee0c")
        postcard = resolve_ending_record(snapshot(*WITNESSES["unsent_postcard"]))
        fallback = next(cause for cause in postcard.matched_causes if cause.cause_kind == "fallback")
        self.assertEqual(fallback.cause_template_id, "cause_unsent_postcard_fallback")
        self.assertEqual(fallback.cause_id, "cause_f57b3ae4a102befa05f8e5a51b1be688338ad1daf3708963d676cb12c7ecac8b")
        self.assertNotIn(fallback.cause_id, postcard.display_cause_ids)
        self.assertTrue(all(type(record) is type(next(iter(_CAUSE_TEMPLATE_INDEX.values()))) for record in _CAUSE_TEMPLATE_INDEX.values()))

    def test_repairs_fold_in_order_and_conflicting_qualifications_fail_closed(self):
        repair_history = (
            "prologue_override_destination", "day1_repair_first_destination",
            "day1_choose_safe_clothing", "day2_assign_alias",
            "day3_force_explanation", "day5_repair_daily_choice",
        )
        resolved = resolve_ending_record(snapshot(repair_history, (0, 0, 0, 0, 0)))
        self.assertEqual(resolved.unresolved_token_ids, ())
        with self.assertRaisesRegex(ValueError, "repair target"):
            resolve_ending(snapshot(("day5_repair_daily_choice",), (0, 0, 0, 0, 0)))

        conflicting = (
            "prologue_read_note", "prologue_ask_destination",
            "prologue_accept_destination", "prologue_notice_tracker",
            "day1_accept_clothing", "day1_read_food_gesture",
            "day2_accept_alias", "day2_save_second_token",
            "day3_share_school_evidence", "day3_honor_pause",
            "day4_buy_two_tickets_real_name",
            "day4_register_independent_contact", "day5_share_full_archive",
            "day5_include_self_in_truth", "day5_honor_erii_response",
            "day6_burn_old_identity", "day6_commit_shared_escape",
            "day6_commit_independent_contact",
        )
        with self.assertRaisesRegex(ValueError, "mutually exclusive"):
            resolve_ending(snapshot(conflicting, (3, 3, 3, 3, 3)))

    def test_qualification_failure_causes_encode_the_missing_source_fact(self):
        first = resolve_ending_record(snapshot(
            (
                "prologue_read_note", "prologue_ask_destination",
                "prologue_accept_destination", "prologue_notice_tracker",
                "day1_accept_clothing", "day1_read_food_gesture",
                "day2_accept_alias", "day2_save_second_token",
                "day3_share_school_evidence", "day3_honor_pause",
                "day4_buy_two_tickets_real_name", "day5_share_full_archive",
                "day5_honor_erii_response", "day6_burn_old_identity",
                "day6_commit_shared_escape",
            ),
            (3, 3, 3, 2, 2),
        ))
        second = resolve_ending_record(snapshot(
            (
                "prologue_read_note", "prologue_ask_destination",
                "prologue_accept_destination", "prologue_notice_tracker",
                "day1_accept_clothing", "day1_read_food_gesture",
                "day2_accept_alias", "day2_save_second_token",
                "day3_share_school_evidence", "day3_honor_pause",
                "day4_buy_two_tickets_real_name",
                "day4_register_independent_contact", "day5_share_full_archive",
                "day6_burn_old_identity", "day6_commit_shared_escape",
            ),
            (3, 3, 3, 2, 2),
        ))
        first_cause = next(
            cause for entry in first.higher_priority_exclusions
            if entry.ending_id == "her_own_name"
            for cause in entry.causes
            if cause.clause_id == "her_own_name_qualification_independent_present"
        )
        second_cause = next(
            cause for entry in second.higher_priority_exclusions
            if entry.ending_id == "her_own_name"
            for cause in entry.causes
            if cause.clause_id == "her_own_name_qualification_independent_present"
        )
        self.assertNotEqual(first_cause.cause_id, second_cause.cause_id)
        self.assertTrue(any("event_contact_risk_handover_complete:false:" in value for value in first_cause.source_reference_ids))
        self.assertTrue(any("event_route_preference_honored:false:" in value for value in second_cause.source_reference_ids))

    def test_wrapper_is_the_single_canonical_call_and_field_read(self):
        source = (GAME_DIR / "modules" / "ending_rules.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        wrapper = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "resolve_ending")
        calls = [node for node in ast.walk(wrapper) if isinstance(node, ast.Call)]
        attributes = [node.attr for node in ast.walk(wrapper) if isinstance(node, ast.Attribute)]
        self.assertEqual(len(calls), 1)
        self.assertEqual(getattr(calls[0].func, "id", None), "resolve_ending_record")
        self.assertEqual(attributes, ["ending_id"])

    def test_history_replay_and_fold_fail_closed(self):
        with self.assertRaises(ValueError):
            resolve_ending(snapshot((), (1, 0, 0, 0, 0)))
        with self.assertRaises(ValueError):
            resolve_ending(snapshot(("unknown_choice",), (0, 0, 0, 0, 0)))
        with self.assertRaises(ValueError):
            resolve_ending(snapshot(("day2_admit_alias_unknown",), (1, 0, 0, 0, 0)))
        with self.assertRaises(ValueError):
            resolve_ending(snapshot(("prologue_read_note", "prologue_read_note"), (2, 0, 0, 0, 0)))

    def test_schema_shape_and_axis_values_are_strict(self):
        value = snapshot((), (0, 0, 0, 0, 0))
        del value["axes"]["truth"]
        with self.assertRaises(ValueError):
            validate_snapshot(value)
        value = snapshot((), (0, 0, 0, 0, 0))
        value["axes"]["affection"] = 99
        with self.assertRaises(ValueError):
            validate_snapshot(value)
        with self.assertRaises(TypeError):
            validate_snapshot(snapshot((), (True, 0, 0, 0, 0)))
        with self.assertRaises(ValueError):
            validate_snapshot(snapshot((), (4, 0, 0, 0, 0)))
        with self.assertRaises(TypeError):
            validate_snapshot({"schema_version": 2, "axes": {}, "choice_history": []})


if __name__ == "__main__":
    unittest.main()
