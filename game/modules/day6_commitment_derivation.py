"""Pure Day 6 route-commitment derivation from frozen narrative facts.

The Day 6 chapter may stage one commitment or fallback action, but SYS-ENDING
remains the only owner of qualifications, resolver calls, ending entry,
completion, and persistence. This module accepts only the closed Day 5 answer/
outcome, resource, event, and token facts needed for that local decision.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final


DERIVATION_ID: Final = "erii_day6_commitment_derivation:v1"
PRIORITY_RULE_ID: Final = "honored_contact_then_shared_then_solo_then_old_order_then_fallback_v1"
ROUTE_FACT_IDS: Final = (
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
)
ALLOWED_COMMITMENT_STATE_IDS: Final = (
    "independent_contact",
    "shared_escape",
    "solo_departure",
    "old_order_return",
    "no_executable_route",
)
ACTION_OBJECT_ID_BY_STATE: Final = {
    "independent_contact": "action_erii_secures_contact_card_for_independent_departure",
    "shared_escape": "action_erii_confirms_two_tickets_and_shared_route",
    "solo_departure": "action_erii_keeps_single_ticket_without_contact_promise",
    "old_order_return": "action_erii_leaves_old_order_route_sheet_untaken",
    "no_executable_route": "action_erii_returns_empty_route_map_without_forcing_answer",
}
_ANSWER_IDS: Final = (
    "shared_escape",
    "independent_contact",
    "solo_departure",
    "continue_without_executable_route",
    "undetermined",
)
_OUTCOME_BY_HONORED_ANSWER: Final = {
    answer_id: "outcome_route_preference_honored_" + answer_id
    for answer_id in _ANSWER_IDS
    if answer_id != "undetermined"
}
_OVERRIDE_OUTCOME: Final = "outcome_route_preference_overridden_to_old_order"


@dataclass(frozen=True)
class CommitmentDerivation:
    """Detached Day 6 route-commitment result."""

    input_fact_values: tuple[tuple[str, object], ...]
    selected_commitment_state_id: str
    observable_action_or_object_id: str | None
    unresolved_defect_ids: tuple[str, ...]

    @property
    def is_determined(self) -> bool:
        """Return whether exactly one Day 6 action may be exposed."""

        return self.selected_commitment_state_id != "undetermined"

    def as_store_record(self, source_hash: str) -> dict[str, object]:
        """Return detached primitive data for rollback-owned chapter assignment."""

        if not _is_sha256(source_hash):
            raise ValueError("Day 6 commitment source hash must be lowercase SHA-256.")
        return {
            "derivation_id": DERIVATION_ID,
            "input_fact_ids": ROUTE_FACT_IDS,
            "input_fact_values": self.input_fact_values,
            "allowed_commitment_state_ids": ALLOWED_COMMITMENT_STATE_IDS,
            "selected_commitment_state_id": self.selected_commitment_state_id,
            "observable_action_or_object_ids": (
                () if self.observable_action_or_object_id is None else (self.observable_action_or_object_id,)
            ),
            "priority_rule_id": PRIORITY_RULE_ID,
            "source_hash": source_hash,
            "forbidden_hidden_input_count": 0,
            "unresolved_defect_ids": self.unresolved_defect_ids,
        }


def derive_commitment(route_facts: Mapping[str, object]) -> CommitmentDerivation:
    """Select one frozen Day 6 commitment/fallback or fail closed.

    The fallback is a determined local narrative fact. Invalid input shape,
    incompatible Day 5 answer/outcome records, and contradictory resources are
    not fallback stories: they are undetermined and expose no commitment action.
    """

    normalized, defect_ids = _normalize_route_facts(route_facts)
    if defect_ids:
        return CommitmentDerivation((), "undetermined", None, defect_ids)

    invalid = _semantic_defect(normalized)
    if invalid is not None:
        return _undetermined(normalized, invalid)

    answer = normalized["day5_answer_state_id"]
    outcome = normalized["day5_response_outcome_id"]
    honored = normalized["event_route_preference_honored"]
    overridden = normalized["event_route_preference_overridden_to_old_order"]

    if (
        answer == "independent_contact"
        and honored
        and outcome == _OUTCOME_BY_HONORED_ANSWER[answer]
        and normalized["resource_contact_card"]
        and normalized["event_contact_risk_handover_complete"]
    ):
        return _determined(normalized, "independent_contact")
    if (
        answer == "shared_escape"
        and honored
        and outcome == _OUTCOME_BY_HONORED_ANSWER[answer]
        and normalized["resource_two_tickets"]
        and normalized["event_shared_cost_acknowledged"]
    ):
        return _determined(normalized, "shared_escape")
    if (
        answer == "solo_departure"
        and honored
        and outcome == _OUTCOME_BY_HONORED_ANSWER[answer]
        and normalized["resource_single_ticket"]
        and not normalized["resource_contact_card"]
    ):
        return _determined(normalized, "solo_departure")
    if (
        overridden
        and outcome == _OVERRIDE_OUTCOME
        and normalized["token_override_daily_choice_unresolved"]
    ):
        return _determined(normalized, "old_order_return")
    return _determined(normalized, "no_executable_route")


def derive_commitment_record(
    route_facts: Mapping[str, object], source_hash: str
) -> dict[str, object]:
    """Build the serializable Day 6 commitment derivation record."""

    return derive_commitment(route_facts).as_store_record(source_hash)


def _normalize_route_facts(
    route_facts: Mapping[str, object],
) -> tuple[dict[str, object], tuple[str, ...]]:
    if not isinstance(route_facts, Mapping):
        return {}, ("route_facts_not_mapping",)
    if tuple(route_facts.keys()) != ROUTE_FACT_IDS:
        return {}, ("route_fact_ids_not_exact",)
    normalized = dict(route_facts)
    if normalized["day5_answer_state_id"] not in (*_ANSWER_IDS, None):
        return {}, ("day5_answer_state_not_allowed",)
    if normalized["day5_response_outcome_id"] not in (*_OUTCOME_BY_HONORED_ANSWER.values(), _OVERRIDE_OUTCOME, None):
        return {}, ("day5_response_outcome_not_allowed",)
    for fact_id in ROUTE_FACT_IDS[2:]:
        if type(normalized[fact_id]) is not bool:
            return {}, ("route_fact_values_not_exact_bool",)
    return normalized, ()


def _semantic_defect(normalized: dict[str, object]) -> str | None:
    answer = normalized["day5_answer_state_id"]
    outcome = normalized["day5_response_outcome_id"]
    honored = normalized["event_route_preference_honored"]
    overridden = normalized["event_route_preference_overridden_to_old_order"]
    if honored and overridden:
        return "contradictory_day5_response_events"
    if honored != (outcome in _OUTCOME_BY_HONORED_ANSWER.values()):
        return "day5_honored_outcome_event_mismatch"
    if overridden != (outcome == _OVERRIDE_OUTCOME):
        return "day5_override_outcome_event_mismatch"
    if honored and outcome != _OUTCOME_BY_HONORED_ANSWER.get(answer):
        return "day5_answer_outcome_mismatch"
    if answer == "undetermined" and outcome is not None:
        return "undetermined_answer_has_response_outcome"
    if normalized["resource_two_tickets"] and normalized["resource_single_ticket"]:
        return "contradictory_ticket_resources"
    if normalized["resource_contact_card"] != normalized["event_contact_risk_handover_complete"]:
        return "incomplete_contact_handover_facts"
    return None


def _determined(normalized: dict[str, object], state_id: str) -> CommitmentDerivation:
    return CommitmentDerivation(
        tuple((fact_id, normalized[fact_id]) for fact_id in ROUTE_FACT_IDS),
        state_id,
        ACTION_OBJECT_ID_BY_STATE[state_id],
        (),
    )


def _undetermined(normalized: dict[str, object], defect_id: str) -> CommitmentDerivation:
    return CommitmentDerivation(
        tuple((fact_id, normalized[fact_id]) for fact_id in ROUTE_FACT_IDS),
        "undetermined",
        None,
        (defect_id,),
    )


def _is_sha256(value: str) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )
