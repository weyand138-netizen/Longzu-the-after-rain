"""Pure, deterministic schema-2 ending resolution for *Rain After*.

This module owns no Ren'Py state.  Its only runtime input is an exact detached
schema-2 snapshot; all terminal facts are rebuilt from its ordered history and
the frozen catalog below.
"""

from __future__ import annotations

from hashlib import sha256
from types import MappingProxyType
from typing import Any, NamedTuple


AXES = (
    "understanding",
    "autonomy",
    "truth",
    "preparation",
    "sacrifice",
)
SNAPSHOT_KEYS = ("schema_version", "axes", "choice_history")
SCHEMA_VERSION = 2

ENDING_PRIORITY = (
    "rain_stops",
    "her_own_name",
    "see_the_sea",
    "one_person_train",
    "golden_cage",
    "unsent_postcard",
)
ENDING_PENDING_ID_PREFIX = "ending."
ENDING_PENDING_IDS = tuple(
    ENDING_PENDING_ID_PREFIX + ending_id for ending_id in ENDING_PRIORITY
)

ENDING_TITLES = {
    "rain_stops": "雨停之后",
    "her_own_name": "她自己的名字",
    "see_the_sea": "去看海吧",
    "one_person_train": "一个人的列车",
    "golden_cage": "金色的笼子",
    "unsent_postcard": "未寄出的明信片",
}


class ChoiceProjectionRecord(NamedTuple):
    choice_id: str
    axis_deltas: tuple[int, int, int, int, int]
    completed_event_ids: tuple[str, ...]
    resource_effects: tuple[tuple[str, str], ...]


class EndingPredicateClauseRecord(NamedTuple):
    ending_id: str
    clause_id: str
    clause_order: int
    clause_kind: str
    operand_clause_ids: tuple[str, ...]
    source_kind: str | None
    source_reference_ids: tuple[str, ...]
    comparator: str | None
    expected_int: int | None
    required_truth_value: bool
    match_cause_template_id: str | None
    failure_cause_template_id: str | None


class EndingCauseTemplateRecord(NamedTuple):
    cause_template_id: str
    ending_id_or_none: str | None
    clause_id_or_none: str | None
    token_id_or_none: str | None
    polarity: str
    cause_kind: str
    source_kind: str
    player_summary_id: str


class EndingCauseRecord(NamedTuple):
    cause_id: str
    cause_kind: str
    cause_template_id: str
    ending_id: str
    clause_id: str | None
    polarity: str
    source_kind: str
    source_reference_ids: tuple[str, ...]
    observed_value: bool | int | str | None
    required_value: bool | int | str | None
    anchor_bucket: int
    history_anchor_start: int | None
    history_anchor_end: int | None


class ClauseEvaluationTraceEntry(NamedTuple):
    ending_id: str
    clause_id: str
    clause_order: int
    clause_kind: str
    comparator_result: bool | None
    satisfaction_result: bool
    contributing_clause_ids: tuple[str, ...]
    source_reference_ids: tuple[str, ...]
    observed_value: bool | int | str | None
    required_value: bool | int | str | None
    anchor_bucket: int | None
    history_anchor_start: int | None
    history_anchor_end: int | None
    cause_template_id_or_none: str | None
    polarity_or_none: str | None
    cause_kind_or_none: str | None
    source_kind_or_none: str | None


class UnresolvedAuditFact(NamedTuple):
    cause_template_id: str
    token_id: str
    polarity: str
    cause_kind: str
    source_kind: str
    source_reference_ids: tuple[str, ...]
    observed_value: bool
    required_value: bool
    anchor_bucket: int
    history_anchor_start: int
    history_anchor_end: int


class FrozenResolutionEvaluation(NamedTuple):
    selected_ending_id: str
    clause_evaluation_trace: tuple[ClauseEvaluationTraceEntry, ...]
    unresolved_audit_facts: tuple[UnresolvedAuditFact, ...]


class HigherPriorityExclusionEntry(NamedTuple):
    ending_id: str
    causes: tuple[EndingCauseRecord, ...]


class EndingResolutionRecord(NamedTuple):
    ending_id: str
    unresolved_token_ids: tuple[str, ...]
    unresolved_token_causes: tuple[EndingCauseRecord, ...]
    completed_event_ids: tuple[str, ...]
    resource_possession_ids: tuple[str, ...]
    qualification_ids: tuple[str, ...]
    clause_evaluation_trace: tuple[ClauseEvaluationTraceEntry, ...]
    matched_causes: tuple[EndingCauseRecord, ...]
    higher_priority_exclusions: tuple[HigherPriorityExclusionEntry, ...]
    display_cause_ids: tuple[str, ...]


def _projection(
    choice_id: str,
    deltas: tuple[int, int, int, int, int] = (0, 0, 0, 0, 0),
    events: tuple[str, ...] = (),
    resources: tuple[tuple[str, str], ...] = (),
) -> ChoiceProjectionRecord:
    return ChoiceProjectionRecord(choice_id, deltas, events, resources)


# This is the frozen semantic projection of the approved narrative baseline.
_PROJECTION_RECORDS = (
    _projection("prologue_read_note", (1, 0, 0, 0, 0)),
    _projection("prologue_hurry_to_train", events=("event_headstart",)),
    _projection("prologue_ask_destination", events=("event_destination_requested",)),
    _projection("prologue_accept_destination", (0, 1, 0, 0, 0)),
    _projection("prologue_override_destination"),
    _projection("prologue_choose_route", events=("event_fast_departure",)),
    _projection("prologue_notice_service_exit", (0, 0, 0, 1, 0), resources=(("resource_service_exit", "acquire"),)),
    _projection("prologue_notice_tracker", (0, 0, 1, 0, 0), events=("event_tracker_direction_shared",)),
    _projection("prologue_promise_cost", events=("event_shared_cost_promised",)),
    _projection("day1_accept_clothing", (0, 1, 0, 0, 0)),
    _projection("day1_choose_safe_clothing"),
    _projection("day1_repair_first_destination"),
    _projection("day1_keep_first_override", events=("event_first_override_unrepaired",)),
    _projection("day1_read_food_gesture", (1, 0, 0, 0, 0)),
    _projection("day1_assume_food_consent"),
    _projection("day2_accept_alias", (1, 1, 0, 0, 0)),
    _projection("day2_assign_alias"),
    _projection("day2_admit_alias_unknown", (1, 0, 0, 0, 0)),
    _projection("day2_save_second_token", (0, 0, 0, 1, 0), resources=(("resource_arcade_token", "acquire"),)),
    _projection("day2_spend_both_tokens", (0, 0, 0, 0, 1), events=("event_both_tokens_spent",)),
    _projection("day3_share_school_evidence", (0, 0, 1, 0, 0)),
    _projection("day3_hide_school_evidence"),
    _projection("day3_honor_pause", (1, 1, 0, 0, 0)),
    _projection("day3_force_explanation"),
    _projection("day4_buy_two_tickets_real_name", (0, 0, 0, 1, 1), ("event_identity_exposed", "event_two_window_tickets_acquired"), (("resource_two_tickets", "acquire"),)),
    _projection("day4_buy_single_ticket_cash", (0, 0, 0, 1, 0), resources=(("resource_single_ticket", "acquire"),)),
    _projection("day4_register_independent_contact", (0, 0, 1, 0, 0), ("event_contact_risk_handover_complete",), (("resource_arcade_token", "consume"), ("resource_contact_card", "acquire"))),
    _projection("day4_decline_independent_contact", events=("event_contact_channel_declined",)),
    _projection("day4_follow_one_route_no_backup"),
    _projection("day5_share_full_archive", (0, 0, 1, 0, 0), ("event_full_archive_shared",)),
    _projection("day5_give_safe_summary"),
    _projection("day5_include_self_in_truth", (0, 0, 0, 1, 1), ("event_self_liability_disclosed",)),
    _projection("day5_blame_family_only", events=("event_external_blame_only",)),
    _projection("day5_honor_erii_response", (0, 1, 0, 0, 0), ("event_route_preference_honored",)),
    _projection("day5_replace_erii_response", events=("event_route_preference_overridden_to_old_order",)),
    _projection("day5_repair_daily_choice"),
    _projection("day5_keep_daily_override", events=("event_daily_override_unrepaired",)),
    _projection("day5_repair_school_evidence"),
    _projection("day5_keep_school_evidence_hidden", events=("event_school_evidence_stays_hidden",)),
    _projection("day6_reopen_service_exit", (0, 0, 0, 1, 0)),
    _projection("day6_abandon_backup"),
    _projection("day6_use_service_exit", events=("event_service_exit_used",)),
    _projection("day6_keep_backup_abandoned", events=("event_backup_stays_abandoned",)),
    _projection("day6_disclose_withheld_archive", (0, 0, 1, 0, 0)),
    _projection("day6_keep_archive_withheld", events=("event_family_truth_stays_withheld",)),
    _projection("day6_burn_old_identity", (0, 0, 0, 0, 1), ("event_shared_cost_acknowledged",)),
    _projection("day6_shift_cost_to_erii"),
    _projection("day6_take_cost_back", (0, 0, 0, 0, 1), ("event_shared_cost_acknowledged", "event_achievement_refusal_honored")),
    _projection("day6_leave_cost_shifted", events=("event_shifted_cost_confirmed",)),
    _projection("day6_commit_independent_contact", events=("event_independent_route_committed",)),
    _projection("day6_commit_shared_escape", events=("event_shared_route_committed",)),
    _projection("day6_commit_solo_departure", events=("event_solo_route_committed", "event_no_continuing_contact_commitment")),
    _projection("day6_commit_old_order_return", events=("event_old_order_route_committed",)),
    _projection("day6_no_executable_route", events=("event_route_collapse",)),
)


_TOKEN_EFFECTS = MappingProxyType({
    "prologue_override_destination": ("revoke", "token_override_first_destination"),
    "prologue_choose_route": ("revoke", "token_override_first_destination"),
    "day1_choose_safe_clothing": ("revoke", "token_override_daily_choice"),
    "day1_repair_first_destination": ("repair", "token_override_first_destination"),
    "day1_keep_first_override": ("revoke", "token_override_daily_choice"),
    "day1_assume_food_consent": ("revoke", "token_silence_as_consent"),
    "day2_assign_alias": ("revoke", "token_override_daily_choice"),
    "day2_admit_alias_unknown": ("repair", "token_silence_as_consent"),
    "day3_hide_school_evidence": ("revoke", "token_hide_school_evidence"),
    "day3_force_explanation": ("revoke", "token_override_daily_choice"),
    "day4_decline_independent_contact": ("revoke", "token_abandon_backup_plan"),
    "day4_follow_one_route_no_backup": ("revoke", "token_abandon_backup_plan"),
    "day5_give_safe_summary": ("revoke", "token_withhold_family_truth"),
    "day5_replace_erii_response": ("revoke", "token_override_daily_choice"),
    "day5_repair_daily_choice": ("repair", "token_override_daily_choice"),
    "day5_repair_school_evidence": ("repair", "token_hide_school_evidence"),
    "day6_reopen_service_exit": ("repair", "token_abandon_backup_plan"),
    "day6_abandon_backup": ("revoke", "token_abandon_backup_plan"),
    "day6_disclose_withheld_archive": ("repair", "token_withhold_family_truth"),
    "day6_shift_cost_to_erii": ("revoke", "token_shift_promised_cost"),
    "day6_take_cost_back": ("repair", "token_shift_promised_cost"),
})

_TOKEN_DOMAINS = MappingProxyType({
    "token_override_first_destination": "autonomy",
    "token_override_daily_choice": "autonomy",
    "token_silence_as_consent": "understanding",
    "token_hide_school_evidence": "truth",
    "token_withhold_family_truth": "truth",
    "token_abandon_backup_plan": "preparation",
    "token_shift_promised_cost": "sacrifice",
})

_QUALIFICATION_BINDINGS = (
    (
        "qualification_independent_contact_route",
        ("day6_commit_independent_contact",),
        ("event_independent_route_committed", "event_contact_risk_handover_complete", "event_route_preference_honored"),
        ("resource_contact_card",),
    ),
    (
        "qualification_shared_escape_route",
        ("day6_commit_shared_escape",),
        ("event_shared_route_committed", "event_shared_cost_acknowledged", "event_route_preference_honored"),
        ("resource_two_tickets",),
    ),
    (
        "qualification_solo_departure_route",
        ("day6_commit_solo_departure",),
        ("event_solo_route_committed", "event_no_continuing_contact_commitment", "event_route_preference_honored"),
        ("resource_single_ticket",),
    ),
    (
        "qualification_old_order_return_route",
        ("day6_commit_old_order_return",),
        ("event_old_order_route_committed",),
        (),
    ),
)


def _clause(
    ending_id: str,
    clause_id: str,
    clause_order: int,
    clause_kind: str,
    operands: tuple[str, ...] = (),
    source_kind: str | None = None,
    source_references: tuple[str, ...] = (),
    comparator: str | None = None,
    expected_int: int | None = None,
) -> EndingPredicateClauseRecord:
    full_clause_id = "{}_{}".format(ending_id, clause_id)
    full_operands = tuple("{}_{}".format(ending_id, operand) for operand in operands)
    if ending_id == "unsent_postcard" and clause_id == "root":
        match_template = "cause_unsent_postcard_fallback"
        failure_template = None
    elif clause_kind == "atomic":
        match_template = "cause_{}_match".format(full_clause_id)
        failure_template = "cause_{}_failure".format(full_clause_id)
    else:
        match_template = None
        failure_template = None
    return EndingPredicateClauseRecord(
        ending_id,
        full_clause_id,
        clause_order,
        clause_kind,
        full_operands,
        source_kind,
        source_references,
        comparator,
        expected_int,
        True,
        match_template,
        failure_template,
    )


_PREDICATE_CLAUSE_RECORDS = (
    _clause("rain_stops", "root", 0, "group_all", (
        "axis_understanding_at_least_3", "axis_autonomy_at_least_3",
        "axis_truth_at_least_3", "axis_preparation_at_least_3",
        "axis_sacrifice_at_least_3", "tokens_all_absent",
    )),
    *tuple(_clause("rain_stops", "axis_{}_at_least_3".format(axis), index + 1,
                  "atomic", source_kind="axis_value", source_references=(axis,),
                  comparator="at_least", expected_int=3) for index, axis in enumerate(AXES)),
    _clause("rain_stops", "tokens_all_absent", 6, "atomic",
            source_kind="unresolved_token", source_references=tuple(_TOKEN_DOMAINS),
            comparator="absent"),
    _clause("her_own_name", "root", 0, "group_all", (
        "axis_autonomy_at_least_3", "axis_truth_at_least_3",
        "axis_understanding_at_least_2", "qualification_independent_present",
        "tokens_autonomy_truth_absent",
    )),
    _clause("her_own_name", "axis_autonomy_at_least_3", 1, "atomic", source_kind="axis_value", source_references=("autonomy",), comparator="at_least", expected_int=3),
    _clause("her_own_name", "axis_truth_at_least_3", 2, "atomic", source_kind="axis_value", source_references=("truth",), comparator="at_least", expected_int=3),
    _clause("her_own_name", "axis_understanding_at_least_2", 3, "atomic", source_kind="axis_value", source_references=("understanding",), comparator="at_least", expected_int=2),
    _clause("her_own_name", "qualification_independent_present", 4, "atomic", source_kind="route_qualification", source_references=("qualification_independent_contact_route",), comparator="present"),
    _clause("her_own_name", "tokens_autonomy_truth_absent", 5, "atomic", source_kind="unresolved_token", source_references=("token_override_first_destination", "token_override_daily_choice", "token_hide_school_evidence", "token_withhold_family_truth"), comparator="absent"),
    _clause("see_the_sea", "root", 0, "group_all", (
        "axis_autonomy_at_least_2", "axis_preparation_at_least_2",
        "axis_sacrifice_at_least_2", "axis_understanding_at_least_1",
        "axis_truth_at_least_1", "qualification_shared_present",
        "tokens_autonomy_truth_sacrifice_absent",
    )),
    _clause("see_the_sea", "axis_autonomy_at_least_2", 1, "atomic", source_kind="axis_value", source_references=("autonomy",), comparator="at_least", expected_int=2),
    _clause("see_the_sea", "axis_preparation_at_least_2", 2, "atomic", source_kind="axis_value", source_references=("preparation",), comparator="at_least", expected_int=2),
    _clause("see_the_sea", "axis_sacrifice_at_least_2", 3, "atomic", source_kind="axis_value", source_references=("sacrifice",), comparator="at_least", expected_int=2),
    _clause("see_the_sea", "axis_understanding_at_least_1", 4, "atomic", source_kind="axis_value", source_references=("understanding",), comparator="at_least", expected_int=1),
    _clause("see_the_sea", "axis_truth_at_least_1", 5, "atomic", source_kind="axis_value", source_references=("truth",), comparator="at_least", expected_int=1),
    _clause("see_the_sea", "qualification_shared_present", 6, "atomic", source_kind="route_qualification", source_references=("qualification_shared_escape_route",), comparator="present"),
    _clause("see_the_sea", "tokens_autonomy_truth_sacrifice_absent", 7, "atomic", source_kind="unresolved_token", source_references=("token_override_first_destination", "token_override_daily_choice", "token_hide_school_evidence", "token_withhold_family_truth", "token_shift_promised_cost"), comparator="absent"),
    _clause("one_person_train", "root", 0, "group_all", ("qualification_solo_present", "loss_any")),
    _clause("one_person_train", "qualification_solo_present", 1, "atomic", source_kind="route_qualification", source_references=("qualification_solo_departure_route",), comparator="present"),
    _clause("one_person_train", "loss_any", 2, "group_any", ("understanding_at_most_1", "preparation_at_most_1", "loss_tokens_present")),
    _clause("one_person_train", "understanding_at_most_1", 3, "atomic", source_kind="axis_value", source_references=("understanding",), comparator="at_most", expected_int=1),
    _clause("one_person_train", "preparation_at_most_1", 4, "atomic", source_kind="axis_value", source_references=("preparation",), comparator="at_most", expected_int=1),
    _clause("one_person_train", "loss_tokens_present", 5, "atomic", source_kind="unresolved_token", source_references=("token_silence_as_consent", "token_hide_school_evidence", "token_withhold_family_truth", "token_abandon_backup_plan"), comparator="present"),
    _clause("golden_cage", "root", 0, "group_all", ("qualification_old_order_present", "tokens_autonomy_present")),
    _clause("golden_cage", "qualification_old_order_present", 1, "atomic", source_kind="route_qualification", source_references=("qualification_old_order_return_route",), comparator="present"),
    _clause("golden_cage", "tokens_autonomy_present", 2, "atomic", source_kind="unresolved_token", source_references=("token_override_first_destination", "token_override_daily_choice"), comparator="present"),
    _clause("unsent_postcard", "root", 0, "atomic", source_kind="constant", comparator="always_true"),
)


def _freeze_predicate_catalog() -> tuple[MappingProxyType, MappingProxyType]:
    clauses: dict[tuple[str, str], EndingPredicateClauseRecord] = {}
    templates: dict[str, EndingCauseTemplateRecord] = {}
    grouped: dict[str, list[EndingPredicateClauseRecord]] = {ending_id: [] for ending_id in ENDING_PRIORITY}
    for record in _PREDICATE_CLAUSE_RECORDS:
        if record.ending_id not in grouped or (record.ending_id, record.clause_id) in clauses:
            raise ValueError("invalid frozen predicate clause")
        if type(record.clause_order) is not int or type(record.required_truth_value) is not bool or not record.required_truth_value:
            raise ValueError("invalid frozen predicate clause")
        clauses[(record.ending_id, record.clause_id)] = record
        grouped[record.ending_id].append(record)
        for template_id, polarity in ((record.match_cause_template_id, "match"), (record.failure_cause_template_id, "failure")):
            if template_id is None:
                continue
            if template_id in templates:
                raise ValueError("duplicate frozen cause template")
            cause_kind = "fallback" if template_id == "cause_unsent_postcard_fallback" else ("matched_evidence" if polarity == "match" else "evidence_shortfall")
            templates[template_id] = EndingCauseTemplateRecord(template_id, record.ending_id, record.clause_id, None, polarity, cause_kind, record.source_kind or "constant", "summary_" + template_id)
    for ending_id, records in grouped.items():
        ordered = tuple(sorted(records, key=lambda item: item.clause_order))
        if not ordered or tuple(item.clause_order for item in ordered) != tuple(range(len(ordered))):
            raise ValueError("invalid frozen predicate order")
        if ordered[0].clause_id != "{}_root".format(ending_id):
            raise ValueError("invalid frozen predicate root")
    for token_id in _TOKEN_DOMAINS:
        template_id = "cause_audit_" + token_id
        templates[template_id] = EndingCauseTemplateRecord(template_id, None, None, token_id, "audit", "unresolved_counterevidence", "unresolved_token", "summary_" + template_id)
    return MappingProxyType(clauses), MappingProxyType(templates)


_PREDICATE_INDEX, _CAUSE_TEMPLATE_INDEX = _freeze_predicate_catalog()


def _freeze_projection_index() -> MappingProxyType:
    index: dict[str, ChoiceProjectionRecord] = {}
    for record in _PROJECTION_RECORDS:
        if type(record.choice_id) is not str or not record.choice_id:
            raise ValueError("invalid frozen choice projection")
        if record.choice_id in index or len(record.axis_deltas) != len(AXES):
            raise ValueError("invalid frozen choice projection")
        if any(type(value) is not int or value < 0 or value > 1 for value in record.axis_deltas):
            raise ValueError("invalid frozen choice projection")
        if any(operation not in ("acquire", "consume") for _resource, operation in record.resource_effects):
            raise ValueError("invalid frozen choice projection")
        index[record.choice_id] = record
    if set(_TOKEN_EFFECTS) - set(index):
        raise ValueError("token effect lacks projection")
    if set(_TOKEN_DOMAINS) != {token_id for _mode, token_id in _TOKEN_EFFECTS.values()}:
        raise ValueError("invalid frozen token catalog")
    return MappingProxyType(index)


_PROJECTION_INDEX = _freeze_projection_index()


def _build_detached_ending_snapshot(
    schema_version: int,
    axis_values: tuple[int, int, int, int, int],
    history_ids: tuple[str, ...],
) -> dict[str, object]:
    """Build the exact pure snapshot transferred by the validated RPY adapter."""

    if type(schema_version) is not int or type(axis_values) is not tuple or type(history_ids) is not tuple:
        raise TypeError("ending snapshot transfer has invalid exact types")
    if len(axis_values) != len(AXES):
        raise ValueError("ending snapshot transfer has invalid axis count")
    return {
        "schema_version": schema_version,
        "axes": {axis: axis_values[index] for index, axis in enumerate(AXES)},
        "choice_history": history_ids,
    }


def validate_snapshot(snapshot: Any) -> dict[str, object]:
    """Validate and return a detached schema-2 snapshot without normalising it."""

    if type(snapshot) is not dict:
        raise TypeError("ending snapshot must be an exact dict")
    if tuple(snapshot.keys()) != SNAPSHOT_KEYS:
        raise ValueError("ending snapshot keys are invalid")
    schema_version = snapshot["schema_version"]
    axes = snapshot["axes"]
    history = snapshot["choice_history"]
    if type(schema_version) is not int or type(axes) is not dict or type(history) is not tuple:
        raise TypeError("ending snapshot fields have invalid exact types")
    if schema_version != SCHEMA_VERSION:
        raise ValueError("ending snapshot schema is unsupported")
    if tuple(axes.keys()) != AXES:
        raise ValueError("ending snapshot axis keys are invalid")
    normalized_axes: dict[str, int] = {}
    for axis in AXES:
        value = axes[axis]
        if type(value) is not int:
            raise TypeError("ending axis must be an exact int")
        if not 0 <= value <= 3:
            raise ValueError("ending axis is outside 0..3")
        normalized_axes[axis] = value
    if any(type(choice_id) is not str for choice_id in history):
        raise TypeError("choice history must contain exact strings")
    if any(not choice_id for choice_id in history) or len(set(history)) != len(history):
        raise ValueError("choice history is invalid")
    return {
        "schema_version": schema_version,
        "axes": normalized_axes,
        "choice_history": history,
    }


def _replay_axes(history: tuple[str, ...]) -> tuple[dict[str, int], dict[str, tuple[tuple[str, int], ...]]]:
    axes = {axis: 0 for axis in AXES}
    contributors: dict[str, list[tuple[str, int]]] = {axis: [] for axis in AXES}
    for history_index, choice_id in enumerate(history):
        record = _PROJECTION_INDEX.get(choice_id)
        if record is None:
            raise ValueError("choice history has no frozen projection")
        for axis_index, axis in enumerate(AXES):
            delta = record.axis_deltas[axis_index]
            before = axes[axis]
            after = min(3, before + delta)
            axes[axis] = after
            if after > before:
                contributors[axis].append((choice_id, history_index))
    return axes, {axis: tuple(items) for axis, items in contributors.items()}


def _fold_tokens(history: tuple[str, ...]) -> tuple[tuple[str, ...], dict[str, tuple[tuple[str, int], ...]], dict[str, int]]:
    unresolved: dict[str, list[tuple[str, int]]] = {}
    first_revoke_index: dict[str, int] = {}
    for history_index, choice_id in enumerate(history):
        effect = _TOKEN_EFFECTS.get(choice_id)
        if effect is None:
            continue
        mode, token_id = effect
        if mode == "revoke":
            unresolved.setdefault(token_id, []).append((choice_id, history_index))
            first_revoke_index.setdefault(token_id, history_index)
        elif token_id not in unresolved:
            raise ValueError("repair target is not unresolved")
        else:
            del unresolved[token_id]
            del first_revoke_index[token_id]
    token_ids = tuple(sorted(unresolved, key=lambda token_id: (first_revoke_index[token_id], token_id.encode("utf-8"))))
    return token_ids, {token_id: tuple(unresolved[token_id]) for token_id in token_ids}, first_revoke_index


def _fold_route_facts(history: tuple[str, ...]) -> tuple[tuple[str, ...], tuple[str, ...], dict[str, tuple[str, ...]], dict[str, tuple[str, ...]]]:
    events: dict[str, list[str]] = {}
    resources: dict[str, list[str]] = {}
    for choice_id in history:
        record = _PROJECTION_INDEX[choice_id]
        for event_id in record.completed_event_ids:
            events.setdefault(event_id, []).append(choice_id)
        for resource_id, operation in record.resource_effects:
            if operation == "acquire":
                if resource_id in resources:
                    raise ValueError("resource is acquired more than once")
                resources[resource_id] = [choice_id]
            elif resource_id not in resources:
                raise ValueError("resource is consumed before acquisition")
            else:
                del resources[resource_id]
    return (
        tuple(sorted(events, key=lambda item: item.encode("utf-8"))),
        tuple(sorted(resources, key=lambda item: item.encode("utf-8"))),
        {item: tuple(events[item]) for item in events},
        {item: tuple(resources[item]) for item in resources},
    )


def _history_positions(history: tuple[str, ...]) -> dict[str, int]:
    return {choice_id: index for index, choice_id in enumerate(history)}


def _derive_qualifications(
    history: tuple[str, ...],
    event_contributors: dict[str, tuple[str, ...]],
    resource_contributors: dict[str, tuple[str, ...]],
) -> tuple[tuple[str, ...], dict[str, tuple[tuple[str, str, bool, tuple[str, ...]], ...]]]:
    positions = _history_positions(history)
    history_ids = set(history)
    qualifications: list[str] = []
    source_facts: dict[str, tuple[tuple[str, str, bool, tuple[str, ...]], ...]] = {}
    for qualification_id, choice_ids, event_ids, resource_ids in _QUALIFICATION_BINDINGS:
        facts: list[tuple[str, str, bool, tuple[str, ...]]] = []
        for choice_id in choice_ids:
            facts.append(("history_choice", choice_id, choice_id in history_ids, (choice_id,) if choice_id in history_ids else ()))
        for event_id in event_ids:
            contributors = event_contributors.get(event_id, ())
            facts.append(("completed_event", event_id, bool(contributors), contributors))
        for resource_id in resource_ids:
            contributors = resource_contributors.get(resource_id, ())
            facts.append(("resource_possession", resource_id, bool(contributors), contributors))
        frozen_facts = tuple(facts)
        source_facts[qualification_id] = frozen_facts
        if all(fact[2] for fact in frozen_facts):
            qualifications.append(qualification_id)
    if len(qualifications) > 1:
        raise ValueError("terminal route qualifications are not mutually exclusive")
    return tuple(qualifications), source_facts


def _anchors(history: tuple[str, ...], source_ids: tuple[str, ...]) -> tuple[int, int | None, int | None]:
    positions = [index for index, choice_id in enumerate(history) if choice_id in source_ids]
    if not positions:
        return 1, None, None
    return 0, min(positions), max(positions)


def _atomic_trace(
    clause: EndingPredicateClauseRecord,
    source_reference_ids: tuple[str, ...],
    observed_value: bool | int | str | None,
    required_value: bool | int | str | None,
    satisfied: bool,
    history: tuple[str, ...],
    anchor_choice_ids: tuple[str, ...] | None = None,
) -> ClauseEvaluationTraceEntry:
    bucket, start, end = _anchors(
        history,
        source_reference_ids if anchor_choice_ids is None else anchor_choice_ids,
    )
    polarity = "match" if satisfied else "failure"
    template_id = clause.match_cause_template_id if satisfied else clause.failure_cause_template_id
    cause_kind = "matched_evidence" if satisfied else (
        "exclusion_evidence" if clause.comparator == "absent" and observed_value else "evidence_shortfall"
    )
    if template_id is None:
        raise ValueError("atomic clause has no frozen cause template")
    return ClauseEvaluationTraceEntry(
        clause.ending_id,
        clause.clause_id,
        clause.clause_order,
        "atomic",
        satisfied,
        satisfied,
        (),
        source_reference_ids,
        observed_value,
        required_value,
        bucket,
        start,
        end,
        template_id,
        polarity,
        cause_kind,
        clause.source_kind,
    )


def _group_trace(clause: EndingPredicateClauseRecord, root_result: bool, children: tuple[ClauseEvaluationTraceEntry, ...]) -> ClauseEvaluationTraceEntry:
    return ClauseEvaluationTraceEntry(
        clause.ending_id,
        clause.clause_id,
        clause.clause_order,
        clause.clause_kind,
        None,
        root_result,
        tuple(item.clause_id for item in children),
        (),
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    )


def _token_source_ids(token_ids: tuple[str, ...], token_contributors: dict[str, tuple[tuple[str, int], ...]]) -> tuple[str, ...]:
    values: list[str] = []
    for token_id in token_ids:
        for choice_id, _index in token_contributors.get(token_id, ()):
            if choice_id not in values:
                values.append(choice_id)
    return tuple(values)


_SOURCE_KIND_RANK = MappingProxyType({
    "axis_value": 0,
    "history_choice": 1,
    "completed_event": 2,
    "resource_possession": 3,
    "route_qualification": 4,
    "unresolved_token": 5,
    "constant": 6,
})


def _qualification_source_references(
    qualification_id: str,
    source_facts: dict[str, tuple[tuple[str, str, bool, tuple[str, ...]], ...]],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    facts = source_facts[qualification_id]
    decisive = facts if all(fact[2] for fact in facts) else tuple(
        fact for fact in facts if not fact[2]
    )
    ordered = tuple(sorted(
        decisive,
        key=lambda fact: (
            _SOURCE_KIND_RANK[fact[0]],
            fact[1].encode("utf-8"),
            fact[3],
        ),
    ))
    references: list[str] = [qualification_id]
    anchors: list[str] = []
    for kind, source_id, truth, contributors in ordered:
        encoded_contributors = ",".join(contributors)
        references.append(
            "fact:{}:{}:{}:{}".format(
                kind,
                source_id,
                "true" if truth else "false",
                encoded_contributors,
            )
        )
        for choice_id in contributors:
            if choice_id not in anchors:
                anchors.append(choice_id)
    return tuple(references), tuple(anchors)


def _predicate_trace(
    axes: dict[str, int],
    history: tuple[str, ...],
    unresolved_token_ids: tuple[str, ...],
    token_contributors: dict[str, tuple[tuple[str, int], ...]],
    qualification_ids: tuple[str, ...],
    qualification_sources: dict[str, tuple[tuple[str, str, bool, tuple[str, ...]], ...]],
    axis_contributors: dict[str, tuple[tuple[str, int], ...]],
) -> FrozenResolutionEvaluation:
    qualifications = set(qualification_ids)
    def trace_atomic(clause: EndingPredicateClauseRecord) -> ClauseEvaluationTraceEntry:
        if clause.source_kind == "axis_value":
            axis = clause.source_reference_ids[0]
            value = axes[axis]
            contributors = axis_contributors[axis]
            if clause.comparator == "at_least":
                required = clause.expected_int
                satisfied = value >= required
                selected_contributors = contributors[:required] if satisfied else contributors
            elif clause.comparator == "at_most":
                required = clause.expected_int
                satisfied = value <= required
                selected_contributors = contributors
            else:
                raise ValueError("invalid frozen axis comparator")
            return _atomic_trace(
                clause,
                tuple(choice_id for choice_id, _index in selected_contributors),
                value,
                required,
                satisfied,
                history,
            )
        if clause.source_kind == "unresolved_token":
            relevant = tuple(token_id for token_id in clause.source_reference_ids if token_id in unresolved_token_ids)
            refs: list[str] = []
            for token_id in relevant:
                refs.append(token_id)
                refs.extend(choice_id for choice_id, _index in token_contributors[token_id])
            present = bool(relevant)
            satisfied = present if clause.comparator == "present" else not present
            return _atomic_trace(clause, tuple(refs), present, clause.comparator == "present", satisfied, history)
        if clause.source_kind == "route_qualification":
            qualification_id = clause.source_reference_ids[0]
            present = qualification_id in qualifications
            refs, anchors = _qualification_source_references(
                qualification_id,
                qualification_sources,
            )
            return _atomic_trace(
                clause,
                refs,
                present,
                True,
                present,
                history,
                anchors,
            )
        if clause.source_kind == "constant" and clause.comparator == "always_true":
            return _atomic_trace(clause, (), True, True, True, history)
        raise ValueError("invalid frozen predicate atomic")

    traces: list[ClauseEvaluationTraceEntry] = []
    selected: str | None = None
    for ending_id in ENDING_PRIORITY:
        records = tuple(sorted(
            (record for (record_ending, _clause_id), record in _PREDICATE_INDEX.items() if record_ending == ending_id),
            key=lambda record: record.clause_order,
        ))
        entries: dict[str, ClauseEvaluationTraceEntry] = {}
        for record in records:
            if record.clause_kind == "atomic":
                entries[record.clause_id] = trace_atomic(record)

        def group_entry(record: EndingPredicateClauseRecord) -> ClauseEvaluationTraceEntry:
            existing = entries.get(record.clause_id)
            if existing is not None:
                return existing
            children = tuple(group_entry(_PREDICATE_INDEX[(ending_id, child_id)]) for child_id in record.operand_clause_ids)
            results = tuple(child.satisfaction_result for child in children)
            satisfied = all(results) if record.clause_kind == "group_all" else any(results)
            if record.clause_kind == "group_all":
                contributing = tuple(child for child in children if child.satisfaction_result == satisfied)
            else:
                contributing = tuple(child for child in children if child.satisfaction_result) if satisfied else children
            entry = _group_trace(record, satisfied, contributing)
            entries[record.clause_id] = entry
            return entry

        root = group_entry(records[0])
        traces.extend(entries[record.clause_id] for record in records)
        if root.satisfaction_result:
            selected = ending_id
            break
    if selected is None:
        raise ValueError("ending priority has no total fallback")
    audit_facts: list[UnresolvedAuditFact] = []
    for token_id in unresolved_token_ids:
        contributor_pairs = token_contributors[token_id]
        refs = (token_id,) + tuple(choice_id for choice_id, _index in contributor_pairs)
        start = contributor_pairs[0][1]
        end = contributor_pairs[-1][1]
        audit_facts.append(UnresolvedAuditFact(
            "cause_audit_" + token_id,
            token_id,
            "audit",
            "unresolved_counterevidence",
            "unresolved_token",
            refs,
            True,
            True,
            0,
            start,
            end,
        ))
    return FrozenResolutionEvaluation(selected, tuple(traces), tuple(audit_facts))


def _encode_canonical(value: bool | int | str | tuple[Any, ...] | None) -> bytes:
    if value is None:
        return b"n;"
    if type(value) is bool:
        return b"b:1;" if value else b"b:0;"
    if type(value) is int:
        return "i:{};".format(value).encode("utf-8")
    if type(value) is str:
        raw = value.encode("utf-8")
        return b"s:" + str(len(raw)).encode("ascii") + b":" + raw + b";"
    if type(value) is tuple:
        return b"t:" + str(len(value)).encode("ascii") + b":[" + b"".join(_encode_canonical(item) for item in value) + b"];"
    raise TypeError("cause payload contains an unsupported value")


def _make_cause(
    *,
    ending_id: str,
    clause_id: str | None,
    polarity: str,
    cause_kind: str,
    cause_template_id: str,
    source_kind: str,
    source_reference_ids: tuple[str, ...],
    observed_value: bool | int | str | None,
    required_value: bool | int | str | None,
    anchor_bucket: int,
    history_anchor_start: int | None,
    history_anchor_end: int | None,
) -> EndingCauseRecord:
    payload = (
        "cause_payload_v1",
        ending_id,
        clause_id,
        polarity,
        cause_kind,
        cause_template_id,
        source_kind,
        source_reference_ids,
        observed_value,
        required_value,
    )
    cause_id = "cause_" + sha256(_encode_canonical(payload)).hexdigest()
    return EndingCauseRecord(cause_id, cause_kind, cause_template_id, ending_id, clause_id, polarity, source_kind, source_reference_ids, observed_value, required_value, anchor_bucket, history_anchor_start, history_anchor_end)


def _cause_total_order(cause: EndingCauseRecord) -> tuple[int, int, int, int, bytes]:
    kind_rank = {
        "matched_evidence": 0,
        "unresolved_counterevidence": 1,
        "exclusion_evidence": 2,
        "evidence_shortfall": 3,
        "fallback": 4,
    }[cause.cause_kind]
    source_rank = {
        "axis_value": 0,
        "history_choice": 1,
        "completed_event": 2,
        "resource_possession": 3,
        "route_qualification": 4,
        "unresolved_token": 5,
        "constant": 6,
    }[cause.source_kind]
    return (
        cause.anchor_bucket,
        -1 if cause.history_anchor_start is None else cause.history_anchor_start,
        -1 if cause.history_anchor_end is None else cause.history_anchor_end,
        kind_rank * 10 + source_rank,
        cause.cause_id.encode("utf-8"),
    )


def _extract_causes(evaluation: FrozenResolutionEvaluation) -> tuple[tuple[EndingCauseRecord, ...], tuple[HigherPriorityExclusionEntry, ...], tuple[EndingCauseRecord, ...]]:
    """Extract all causes from the frozen evaluation artifact only."""

    matched: list[EndingCauseRecord] = []
    exclusion_buckets: dict[str, list[EndingCauseRecord]] = {}
    for entry in evaluation.clause_evaluation_trace:
        if entry.clause_kind != "atomic":
            continue
        if entry.ending_id == evaluation.selected_ending_id and entry.satisfaction_result:
            cause_kind = "fallback" if entry.source_kind_or_none == "constant" else "matched_evidence"
            matched.append(_make_cause(
                ending_id=entry.ending_id,
                clause_id=entry.clause_id,
                polarity="match",
                cause_kind=cause_kind,
                cause_template_id=entry.cause_template_id_or_none or "cause_missing_template",
                source_kind=entry.source_kind_or_none or "constant",
                source_reference_ids=entry.source_reference_ids,
                observed_value=entry.observed_value,
                required_value=entry.required_value,
                anchor_bucket=entry.anchor_bucket if entry.anchor_bucket is not None else 2,
                history_anchor_start=entry.history_anchor_start,
                history_anchor_end=entry.history_anchor_end,
            ))
        elif entry.ending_id != evaluation.selected_ending_id and not entry.satisfaction_result:
            exclusion_buckets.setdefault(entry.ending_id, []).append(_make_cause(
                ending_id=entry.ending_id,
                clause_id=entry.clause_id,
                polarity="failure",
                cause_kind=entry.cause_kind_or_none or "evidence_shortfall",
                cause_template_id=entry.cause_template_id_or_none or "cause_missing_template",
                source_kind=entry.source_kind_or_none or "constant",
                source_reference_ids=entry.source_reference_ids,
                observed_value=entry.observed_value,
                required_value=entry.required_value,
                anchor_bucket=entry.anchor_bucket if entry.anchor_bucket is not None else 1,
                history_anchor_start=entry.history_anchor_start,
                history_anchor_end=entry.history_anchor_end,
            ))
    exclusions: list[HigherPriorityExclusionEntry] = []
    for ending_id in ENDING_PRIORITY:
        if ending_id == evaluation.selected_ending_id:
            break
        causes = tuple(sorted(exclusion_buckets.get(ending_id, ()), key=_cause_total_order))
        if not causes:
            raise ValueError("higher priority exclusion has no cause")
        exclusions.append(HigherPriorityExclusionEntry(ending_id, causes))
    unresolved_causes = tuple(sorted((
        _make_cause(
            ending_id=evaluation.selected_ending_id,
            clause_id=None,
            polarity=audit.polarity,
            cause_kind=audit.cause_kind,
            cause_template_id=audit.cause_template_id,
            source_kind=audit.source_kind,
            source_reference_ids=audit.source_reference_ids,
            observed_value=audit.observed_value,
            required_value=audit.required_value,
            anchor_bucket=audit.anchor_bucket,
            history_anchor_start=audit.history_anchor_start,
            history_anchor_end=audit.history_anchor_end,
        ) for audit in evaluation.unresolved_audit_facts
    ), key=_cause_total_order))
    ordered_matched = tuple(sorted(matched, key=_cause_total_order))
    if not ordered_matched:
        raise ValueError("selected ending has no matched cause")
    return ordered_matched, tuple(exclusions), unresolved_causes


def _display_causes(
    ending_id: str,
    matched: tuple[EndingCauseRecord, ...],
    unresolved: tuple[EndingCauseRecord, ...],
    exclusions: tuple[HigherPriorityExclusionEntry, ...],
) -> tuple[str, ...]:
    exclusion_causes = tuple(cause for entry in exclusions for cause in entry.causes)
    safe_matched = tuple(cause for cause in matched if cause.cause_kind != "fallback")
    if ending_id == "unsent_postcard":
        concrete = tuple(sorted(unresolved + exclusion_causes, key=_cause_total_order))
        if not concrete:
            raise ValueError("postcard has no concrete presentation cause")
        anchor = concrete[0]
        remaining = tuple(cause for cause in concrete if cause.cause_id != anchor.cause_id)
    else:
        if not safe_matched:
            raise ValueError("selected ending has no safe matched cause")
        anchor = safe_matched[0]
        remaining = tuple(cause for cause in safe_matched + unresolved + exclusion_causes if cause.cause_id != anchor.cause_id)
        remaining = tuple(sorted(remaining, key=_cause_total_order))
    return (anchor.cause_id,) + tuple(cause.cause_id for cause in remaining[:2])


def resolve_ending_record(snapshot: dict[str, object]) -> EndingResolutionRecord:
    """Resolve one immutable, explainable ending record from detached history."""

    normalized = validate_snapshot(snapshot)
    history = normalized["choice_history"]
    axes = normalized["axes"]
    if type(history) is not tuple or type(axes) is not dict:
        raise TypeError("validated ending snapshot has invalid exact types")
    replayed_axes, axis_contributors = _replay_axes(history)
    if replayed_axes != axes:
        raise ValueError("choice history does not replay to supplied axes")
    unresolved_ids, token_contributors, _first_indices = _fold_tokens(history)
    completed_events, resources, event_contributors, resource_contributors = _fold_route_facts(history)
    qualification_ids, qualification_sources = _derive_qualifications(history, event_contributors, resource_contributors)
    evaluation = _predicate_trace(replayed_axes, history, unresolved_ids, token_contributors, qualification_ids, qualification_sources, axis_contributors)
    matched, exclusions, unresolved_causes = _extract_causes(evaluation)
    display_ids = _display_causes(evaluation.selected_ending_id, matched, unresolved_causes, exclusions)
    return EndingResolutionRecord(
        evaluation.selected_ending_id,
        unresolved_ids,
        unresolved_causes,
        completed_events,
        resources,
        qualification_ids,
        evaluation.clause_evaluation_trace,
        matched,
        exclusions,
        display_ids,
    )


def resolve_ending(snapshot: dict[str, object]) -> str:
    """Compatibility wrapper: exactly one canonical call and one field read."""

    return resolve_ending_record(snapshot).ending_id
