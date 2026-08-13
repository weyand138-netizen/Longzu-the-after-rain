"""Pure Day 5 route-answer derivation from visible Day 4 route facts.

The Day 5 agency answer must be derived from the already established route
resources, never from live Ren'Py store, axes, counterevidence, qualifications,
ending predicates, or developer state. This module accepts only a closed set of
primitive facts and returns a serializable record for the chapter to assign to
rollback-owned state.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final


DERIVATION_ID: Final = "erii_route_answer_derivation:v1"
TRANSACTION_ID: Final = "agency_day5_response"
PRIORITY_RULE_ID: Final = "two_tickets_then_contact_then_single_then_continue_v1"
ROUTE_FACT_IDS: Final = (
    "resource_two_tickets",
    "resource_contact_card",
    "event_contact_risk_handover_complete",
    "resource_single_ticket",
)
ALLOWED_ANSWER_STATE_IDS: Final = (
    "shared_escape",
    "independent_contact",
    "solo_departure",
    "continue_without_executable_route",
)
ACTION_OBJECT_ID_BY_STATE: Final = {
    "shared_escape": "action_erii_places_two_tickets_on_map",
    "independent_contact": "action_erii_secures_contact_card",
    "solo_departure": "action_erii_places_single_ticket_in_document_case",
    "continue_without_executable_route": "action_erii_returns_empty_route_map",
}


@dataclass(frozen=True)
class RouteAnswerDerivation:
    """Detached result for one Day 5 answer derivation."""

    input_fact_values: tuple[tuple[str, bool], ...]
    selected_answer_state_id: str
    observable_action_or_object_id: str | None
    unresolved_defect_ids: tuple[str, ...]

    @property
    def is_determined(self) -> bool:
        """Return whether the source may expose a Day 5 response menu."""

        return self.selected_answer_state_id != "undetermined"

    def as_store_record(self, source_hash: str) -> dict[str, object]:
        """Return only primitive values safe for rollback-owned assignment."""

        if not _is_sha256(source_hash):
            raise ValueError("Day 5 derivation source hash must be lowercase SHA-256.")
        return {
            "derivation_id": DERIVATION_ID,
            "transaction_id": TRANSACTION_ID,
            "input_fact_ids": ROUTE_FACT_IDS,
            "input_fact_values": self.input_fact_values,
            "allowed_answer_state_ids": ALLOWED_ANSWER_STATE_IDS,
            "selected_answer_state_id": self.selected_answer_state_id,
            "observable_action_or_object_ids": (
                ()
                if self.observable_action_or_object_id is None
                else (self.observable_action_or_object_id,)
            ),
            "priority_rule_id": PRIORITY_RULE_ID,
            "source_hash": source_hash,
            "forbidden_hidden_input_count": 0,
            "unresolved_defect_ids": self.unresolved_defect_ids,
        }


def derive_route_answer(route_facts: Mapping[str, bool]) -> RouteAnswerDerivation:
    """Derive exactly one approved Day 5 answer from typed Day 4 facts.

    Invalid fact shapes fail closed as ``undetermined``. A two-ticket route may
    also retain a contact card, so the explicit priority rule correctly selects
    shared escape before considering the contact candidate.
    """

    normalized, defect_ids = _normalize_route_facts(route_facts)
    if defect_ids:
        return RouteAnswerDerivation((), "undetermined", None, defect_ids)

    two_tickets = normalized["resource_two_tickets"]
    contact_card = normalized["resource_contact_card"]
    contact_handover = normalized["event_contact_risk_handover_complete"]
    single_ticket = normalized["resource_single_ticket"]

    if two_tickets and single_ticket:
        return _undetermined(normalized, "contradictory_ticket_resources")
    if contact_card != contact_handover:
        return _undetermined(normalized, "incomplete_contact_handover_facts")
    if single_ticket and contact_card:
        return _undetermined(normalized, "contradictory_solo_contact_resources")

    if two_tickets:
        return _determined(normalized, "shared_escape")
    if contact_card:
        return _determined(normalized, "independent_contact")
    if single_ticket:
        return _determined(normalized, "solo_departure")
    return _determined(normalized, "continue_without_executable_route")


def derive_route_answer_record(
    route_facts: Mapping[str, bool], source_hash: str
) -> dict[str, object]:
    """Build a detached, serializable character-answer derivation record."""

    return derive_route_answer(route_facts).as_store_record(source_hash)


def _normalize_route_facts(
    route_facts: Mapping[str, bool],
) -> tuple[dict[str, bool], tuple[str, ...]]:
    """Reject non-mapping, incomplete, or unknown Day 4 route inputs.

    Ren'Py wraps source literals in a rollback-aware mapping before it calls
    Python helpers. Accepting ``Mapping`` preserves that runtime boundary while
    the exact key order and primitive-value checks keep the input contract
    closed.
    """

    if not isinstance(route_facts, Mapping):
        return {}, ("route_facts_not_mapping",)
    if tuple(route_facts.keys()) != ROUTE_FACT_IDS:
        return {}, ("route_fact_ids_not_exact",)
    if any(type(value) is not bool for value in route_facts.values()):
        return {}, ("route_fact_values_not_exact_bool",)
    return dict(route_facts), ()


def _determined(
    normalized: dict[str, bool], state_id: str
) -> RouteAnswerDerivation:
    """Build one allowed, action-bound derivation result."""

    return RouteAnswerDerivation(
        tuple((fact_id, normalized[fact_id]) for fact_id in ROUTE_FACT_IDS),
        state_id,
        ACTION_OBJECT_ID_BY_STATE[state_id],
        (),
    )


def _undetermined(
    normalized: dict[str, bool], defect_id: str
) -> RouteAnswerDerivation:
    """Build a failure-closed derivation without visible answer evidence."""

    return RouteAnswerDerivation(
        tuple((fact_id, normalized[fact_id]) for fact_id in ROUTE_FACT_IDS),
        "undetermined",
        None,
        (defect_id,),
    )


def _is_sha256(value: str) -> bool:
    """Accept only a lower-case SHA-256 string supplied by authored source."""

    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )
