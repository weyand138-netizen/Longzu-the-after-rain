import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "game"))

from modules.day6_commitment_derivation import (  # noqa: E402
    ACTION_OBJECT_ID_BY_STATE,
    ALLOWED_COMMITMENT_STATE_IDS,
    DERIVATION_ID,
    PRIORITY_RULE_ID,
    ROUTE_FACT_IDS,
    derive_commitment,
    derive_commitment_record,
)


def facts(
    answer="continue_without_executable_route",
    outcome="outcome_route_preference_honored_continue_without_executable_route",
    honored=True,
    overridden=False,
    contact_card=False,
    contact_handover=False,
    two_tickets=False,
    shared_cost=False,
    single_ticket=False,
    unresolved_override=False,
):
    """Return the complete, ordered and closed Day 6 derivation facts."""

    return {
        "day5_answer_state_id": answer,
        "day5_response_outcome_id": outcome,
        "event_route_preference_honored": honored,
        "event_route_preference_overridden_to_old_order": overridden,
        "resource_contact_card": contact_card,
        "event_contact_risk_handover_complete": contact_handover,
        "resource_two_tickets": two_tickets,
        "event_shared_cost_acknowledged": shared_cost,
        "resource_single_ticket": single_ticket,
        "token_override_daily_choice_unresolved": unresolved_override,
    }


class Day6CommitmentDerivationTests(unittest.TestCase):
    def test_each_frozen_commitment_partition_selects_one_visible_action(self):
        cases = (
            (
                facts(
                    answer="independent_contact",
                    outcome="outcome_route_preference_honored_independent_contact",
                    contact_card=True,
                    contact_handover=True,
                ),
                "independent_contact",
            ),
            (
                facts(
                    answer="shared_escape",
                    outcome="outcome_route_preference_honored_shared_escape",
                    two_tickets=True,
                    shared_cost=True,
                ),
                "shared_escape",
            ),
            (
                facts(
                    answer="solo_departure",
                    outcome="outcome_route_preference_honored_solo_departure",
                    single_ticket=True,
                ),
                "solo_departure",
            ),
            (
                facts(
                    answer="independent_contact",
                    outcome="outcome_route_preference_overridden_to_old_order",
                    honored=False,
                    overridden=True,
                    unresolved_override=True,
                ),
                "old_order_return",
            ),
            (facts(), "no_executable_route"),
        )
        for route_facts, expected in cases:
            with self.subTest(expected=expected):
                result = derive_commitment(route_facts)
                self.assertTrue(result.is_determined)
                self.assertEqual(expected, result.selected_commitment_state_id)
                self.assertEqual(ACTION_OBJECT_ID_BY_STATE[expected], result.observable_action_or_object_id)
                self.assertEqual((), result.unresolved_defect_ids)

    def test_invalid_or_contradictory_day5_facts_fail_closed_before_a_choice_exists(self):
        cases = (
            (facts(honored=True, overridden=True), "contradictory_day5_response_events"),
            (facts(outcome="outcome_route_preference_overridden_to_old_order"), "day5_honored_outcome_event_mismatch"),
            (
                facts(
                    answer="shared_escape",
                    outcome="outcome_route_preference_honored_independent_contact",
                ),
                "day5_answer_outcome_mismatch",
            ),
            (facts(two_tickets=True, single_ticket=True), "contradictory_ticket_resources"),
            (facts(contact_card=True), "incomplete_contact_handover_facts"),
        )
        for route_facts, defect_id in cases:
            with self.subTest(defect_id=defect_id):
                result = derive_commitment(route_facts)
                self.assertFalse(result.is_determined)
                self.assertEqual("undetermined", result.selected_commitment_state_id)
                self.assertIsNone(result.observable_action_or_object_id)
                self.assertEqual((defect_id,), result.unresolved_defect_ids)

    def test_unknown_shape_or_type_cannot_be_interpreted_as_route_facts(self):
        unknown = facts()
        unknown["unapproved_fact"] = True
        self.assertEqual(("route_fact_ids_not_exact",), derive_commitment(unknown).unresolved_defect_ids)

        untyped = facts()
        untyped["resource_two_tickets"] = 1
        self.assertEqual(("route_fact_values_not_exact_bool",), derive_commitment(untyped).unresolved_defect_ids)
        self.assertEqual(("route_facts_not_mapping",), derive_commitment(()).unresolved_defect_ids)

    def test_store_record_is_detached_primitive_data_with_zero_hidden_inputs(self):
        source_hash = "a" * 64
        record = derive_commitment_record(
            facts(
                answer="shared_escape",
                outcome="outcome_route_preference_honored_shared_escape",
                two_tickets=True,
                shared_cost=True,
            ),
            source_hash,
        )
        self.assertEqual(DERIVATION_ID, record["derivation_id"])
        self.assertEqual(ROUTE_FACT_IDS, record["input_fact_ids"])
        self.assertEqual(ALLOWED_COMMITMENT_STATE_IDS, record["allowed_commitment_state_ids"])
        self.assertEqual("shared_escape", record["selected_commitment_state_id"])
        self.assertEqual(PRIORITY_RULE_ID, record["priority_rule_id"])
        self.assertEqual(source_hash, record["source_hash"])
        self.assertEqual(0, record["forbidden_hidden_input_count"])
        self.assertEqual((), record["unresolved_defect_ids"])
        self.assertEqual(
            (ACTION_OBJECT_ID_BY_STATE["shared_escape"],),
            record["observable_action_or_object_ids"],
        )

    def test_invalid_source_hash_is_rejected_before_a_store_record_is_emitted(self):
        with self.assertRaises(ValueError):
            derive_commitment_record(facts(), "not-a-sha256")


if __name__ == "__main__":
    unittest.main()
