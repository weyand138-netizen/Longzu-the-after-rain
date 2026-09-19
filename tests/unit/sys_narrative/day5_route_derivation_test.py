import unittest
from collections.abc import Mapping
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "game"))

from modules.day5_route_derivation import (  # noqa: E402
    ACTION_OBJECT_ID_BY_STATE,
    ALLOWED_ANSWER_STATE_IDS,
    DERIVATION_ID,
    PRIORITY_RULE_ID,
    ROUTE_FACT_IDS,
    TRANSACTION_ID,
    derive_route_answer,
    derive_route_answer_record,
)


def facts(two_tickets=False, contact_card=False, contact_handover=False, single_ticket=False):
    """Return the closed, canonical Day 4 route-fact tuple."""

    return {
        "resource_two_tickets": two_tickets,
        "resource_contact_card": contact_card,
        "event_contact_risk_handover_complete": contact_handover,
        "resource_single_ticket": single_ticket,
    }


class Day5RouteDerivationTests(unittest.TestCase):
    def test_rollback_aware_mapping_is_accepted_only_when_it_has_the_closed_contract_shape(self):
        class RollbackAwareFacts(Mapping):
            def __init__(self, values):
                self.data = values

            def __getitem__(self, key):
                return self.data[key]

            def __iter__(self):
                return iter(self.data)

            def __len__(self):
                return len(self.data)

        result = derive_route_answer(
            RollbackAwareFacts(facts(contact_card=True, contact_handover=True))
        )
        self.assertEqual("independent_contact", result.selected_answer_state_id)

    def test_shared_escape_has_priority_over_an_also_valid_contact_card(self):
        result = derive_route_answer(facts(two_tickets=True, contact_card=True, contact_handover=True))
        self.assertTrue(result.is_determined)
        self.assertEqual("shared_escape", result.selected_answer_state_id)
        self.assertEqual(ACTION_OBJECT_ID_BY_STATE["shared_escape"], result.observable_action_or_object_id)

    def test_contact_card_selects_independent_contact_without_two_tickets(self):
        result = derive_route_answer(facts(contact_card=True, contact_handover=True))
        self.assertEqual("independent_contact", result.selected_answer_state_id)
        self.assertEqual(ACTION_OBJECT_ID_BY_STATE["independent_contact"], result.observable_action_or_object_id)

    def test_single_ticket_selects_solo_departure_only_without_contact_card(self):
        result = derive_route_answer(facts(single_ticket=True))
        self.assertEqual("solo_departure", result.selected_answer_state_id)
        self.assertEqual(ACTION_OBJECT_ID_BY_STATE["solo_departure"], result.observable_action_or_object_id)

    def test_empty_route_facts_select_continue_without_executable_route(self):
        result = derive_route_answer(facts())
        self.assertEqual("continue_without_executable_route", result.selected_answer_state_id)
        self.assertEqual(ACTION_OBJECT_ID_BY_STATE["continue_without_executable_route"], result.observable_action_or_object_id)

    def test_mismatched_contact_card_and_handover_fail_closed(self):
        result = derive_route_answer(facts(contact_card=True))
        self.assertFalse(result.is_determined)
        self.assertEqual("undetermined", result.selected_answer_state_id)
        self.assertEqual(("incomplete_contact_handover_facts",), result.unresolved_defect_ids)

    def test_contradictory_ticket_resources_fail_closed(self):
        result = derive_route_answer(facts(two_tickets=True, single_ticket=True))
        self.assertEqual("undetermined", result.selected_answer_state_id)
        self.assertEqual(("contradictory_ticket_resources",), result.unresolved_defect_ids)

    def test_solo_ticket_and_contact_card_fail_closed(self):
        result = derive_route_answer(facts(contact_card=True, contact_handover=True, single_ticket=True))
        self.assertEqual("undetermined", result.selected_answer_state_id)
        self.assertEqual(("contradictory_solo_contact_resources",), result.unresolved_defect_ids)

    def test_unknown_or_untyped_inputs_cannot_be_interpreted_as_route_facts(self):
        unknown = facts(); unknown["understanding"] = True
        self.assertEqual(("route_fact_ids_not_exact",), derive_route_answer(unknown).unresolved_defect_ids)
        untyped = facts(); untyped["resource_two_tickets"] = 1
        self.assertEqual(("route_fact_values_not_exact_bool",), derive_route_answer(untyped).unresolved_defect_ids)
        self.assertEqual(("route_facts_not_mapping",), derive_route_answer(tuple()).unresolved_defect_ids)

    def test_store_record_is_detached_primitive_data_with_zero_hidden_inputs(self):
        source_hash = "a" * 64
        record = derive_route_answer_record(facts(contact_card=True, contact_handover=True), source_hash)
        self.assertEqual(DERIVATION_ID, record["derivation_id"])
        self.assertEqual(TRANSACTION_ID, record["transaction_id"])
        self.assertEqual(ROUTE_FACT_IDS, record["input_fact_ids"])
        self.assertEqual(ALLOWED_ANSWER_STATE_IDS, record["allowed_answer_state_ids"])
        self.assertEqual("independent_contact", record["selected_answer_state_id"])
        self.assertEqual(PRIORITY_RULE_ID, record["priority_rule_id"])
        self.assertEqual(source_hash, record["source_hash"])
        self.assertEqual(0, record["forbidden_hidden_input_count"])
        self.assertEqual((), record["unresolved_defect_ids"])
        self.assertEqual(
            (ACTION_OBJECT_ID_BY_STATE["independent_contact"],),
            record["observable_action_or_object_ids"],
        )

    def test_invalid_source_hash_is_rejected_before_a_store_record_is_emitted(self):
        with self.assertRaises(ValueError):
            derive_route_answer_record(facts(), "not-a-sha256")


if __name__ == "__main__":
    unittest.main()
