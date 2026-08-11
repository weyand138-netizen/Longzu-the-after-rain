"""Build-time validation for the non-production Day 1 handoff artifact.

This module intentionally has no runtime integration points. The full production
``narrative_flow_manifest:v1`` remains owned by ADR-0008 and is not represented
here.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import re
from typing import Iterable


PARTIAL_MANIFEST_SCHEMA = "narrative_partial_day1_manifest:v1"
PARTIAL_ARTIFACT_KIND = "partial_day1"
DAY1_SOURCE_UNIT_ID = "chapter_day1_her_own_name"
DAY1_NODE_ID = "node_day1_authored_source"
DAY1_HANDOFF_NODE_ID = "node_day1_handoff"
TERMINAL_WITNESS_NOT_APPLICABLE = "not_applicable"

DAY1_EXPECTED_BINDINGS = (
    (
        "day1_accept_clothing",
        "reaction_day1_accept_clothing",
        "payoff_day1_clothing_day4",
    ),
    (
        "day1_choose_safe_clothing",
        "reaction_day1_choose_safe_clothing",
        "payoff_day1_safe_clothing_day5",
    ),
    (
        "day1_repair_first_destination",
        "reaction_day1_repair_first_destination",
        "payoff_repair_first_destination",
    ),
    (
        "day1_keep_first_override",
        "reaction_day1_keep_first_override",
        "payoff_keep_first_override",
    ),
    (
        "day1_read_food_gesture",
        "reaction_day1_read_food_gesture",
        "payoff_day1_food_day5",
    ),
    (
        "day1_assume_food_consent",
        "reaction_day1_assume_food_consent",
        "payoff_day1_assume_day5",
    ),
)

_RECORD_PATTERN = re.compile(
    r'\(\s*"(day1_[a-z_]+)"\s*,\s*"(reaction_day1_[a-z_]+)"\s*,\s*"(payoff_[a-z0-9_]+)"\s*,?\s*\)',
    re.MULTILINE,
)


class PartialManifestValidationError(ValueError):
    """The partial artifact is incomplete, stale, or outside the Day 1 boundary."""


@dataclass(frozen=True)
class ChoiceBinding:
    canonical_choice_id: str
    immediate_reaction_id: str
    delayed_payoff_id: str


@dataclass(frozen=True)
class Day1HandoffWitness:
    witness_id: str
    starting_state_id: str
    ordered_choice_history: tuple[str, ...]
    handoff_node_id: str


@dataclass(frozen=True)
class PartialDay1Manifest:
    schema: str
    artifact_kind: str
    source_unit_id: str
    source_hash: str
    node_id: str
    bindings: tuple[ChoiceBinding, ...]
    successor_node_ids: tuple[str, ...]
    day1_handoff_node_id: str
    witness_ids: tuple[str, ...]
    full_production_manifest: bool
    terminal_witness_coverage: str
    runtime_source_scan_count: int
    runtime_cfg_enumeration_count: int


def source_sha256(source_bytes: bytes) -> str:
    """Return the canonical owner hash for a source file at build/test time."""

    return sha256(source_bytes).hexdigest()


def scan_day1_source(source_path: Path) -> tuple[str, tuple[tuple[str, str, str], ...]]:
    """Read the Day 1 source only during build/test validation.

    This scanner is deliberately not imported or called by Ren'Py runtime labels.
    """

    source_bytes = source_path.read_bytes()
    source_text = source_bytes.decode("utf-8")
    if source_text.count("label {}:".format(DAY1_SOURCE_UNIT_ID)) != 1:
        raise PartialManifestValidationError("Day 1 source unit is missing or duplicated")
    records = tuple(_RECORD_PATTERN.findall(source_text))
    if not records:
        raise PartialManifestValidationError("Day 1 choice records are missing")
    return source_sha256(source_bytes), records


def _require_exact_day1_bindings(records: Iterable[tuple[str, str, str]]) -> tuple[ChoiceBinding, ...]:
    records = tuple(records)
    if len(records) != len(set(records)):
        raise PartialManifestValidationError("duplicate Day 1 choice binding")
    if tuple(records) != DAY1_EXPECTED_BINDINGS:
        raise PartialManifestValidationError("Day 1 bindings do not exact-match the approved subset")
    bindings = tuple(ChoiceBinding(*record) for record in records)
    for binding in bindings:
        if binding.immediate_reaction_id != "reaction_" + binding.canonical_choice_id:
            raise PartialManifestValidationError("immediate reaction identity is not canonical")
        if not binding.delayed_payoff_id.startswith("payoff_"):
            raise PartialManifestValidationError("delayed payoff identity is not canonical")
    return bindings


def _reject_forbidden_reference(value: str) -> None:
    lowered = value.lower()
    forbidden_terms = (
        "ending",
        "terminal",
        "test_only",
        "test-only",
        "future",
        "placeholder",
    )
    if any(term in lowered for term in forbidden_terms):
        raise PartialManifestValidationError("partial artifact contains a forbidden reference")


def build_partial_day1_manifest(
    source_path: Path,
    *,
    source_hash: str | None = None,
    records: Iterable[tuple[str, str, str]] | None = None,
    successor_node_ids: tuple[str, ...] = (DAY1_HANDOFF_NODE_ID,),
    handoff_node_id: str = DAY1_HANDOFF_NODE_ID,
) -> PartialDay1Manifest:
    """Build the bounded Sprint 1 handoff artifact or fail without emitting one."""

    scanned_hash, scanned_records = scan_day1_source(source_path)
    if source_hash is not None and source_hash != scanned_hash:
        raise PartialManifestValidationError("stale source hash")
    bindings = _require_exact_day1_bindings(scanned_records if records is None else records)
    for value in successor_node_ids + (handoff_node_id,):
        _reject_forbidden_reference(value)
    if handoff_node_id != DAY1_HANDOFF_NODE_ID:
        raise PartialManifestValidationError("unexpected Day 1 handoff node")
    if successor_node_ids != (DAY1_HANDOFF_NODE_ID,):
        raise PartialManifestValidationError("successors must contain only the controlled Day 1 handoff")
    return PartialDay1Manifest(
        schema=PARTIAL_MANIFEST_SCHEMA,
        artifact_kind=PARTIAL_ARTIFACT_KIND,
        source_unit_id=DAY1_SOURCE_UNIT_ID,
        source_hash=scanned_hash,
        node_id=DAY1_NODE_ID,
        bindings=bindings,
        successor_node_ids=successor_node_ids,
        day1_handoff_node_id=handoff_node_id,
        witness_ids=("witness_day1_handoff_v1",),
        full_production_manifest=False,
        terminal_witness_coverage=TERMINAL_WITNESS_NOT_APPLICABLE,
        runtime_source_scan_count=0,
        runtime_cfg_enumeration_count=0,
    )


def replay_day1_handoff_witness(
    manifest: PartialDay1Manifest,
    witness: Day1HandoffWitness,
) -> str:
    """Validate a source-local Day 1 path and return its non-terminal handoff."""

    if witness.witness_id not in manifest.witness_ids:
        raise PartialManifestValidationError("unknown Day 1 handoff witness")
    if witness.starting_state_id != "canonical_prologue_state":
        raise PartialManifestValidationError("witness does not begin from canonical prologue state")
    if witness.handoff_node_id != manifest.day1_handoff_node_id:
        raise PartialManifestValidationError("witness does not reach controlled handoff")
    legal_histories = {
        ("day1_accept_clothing", "day1_read_food_gesture"),
        ("day1_choose_safe_clothing", "day1_assume_food_consent"),
    }
    if witness.ordered_choice_history not in legal_histories:
        raise PartialManifestValidationError("witness history is not an enabled Day 1 source path")
    binding_ids = {binding.canonical_choice_id for binding in manifest.bindings}
    if not set(witness.ordered_choice_history).issubset(binding_ids):
        raise PartialManifestValidationError("witness contains an unresolved choice")
    return manifest.day1_handoff_node_id


def reject_full_production_promotion(manifest: PartialDay1Manifest) -> None:
    """Fail closed when a Sprint 1 partial artifact reaches a production gate."""

    if manifest.schema != PARTIAL_MANIFEST_SCHEMA:
        raise PartialManifestValidationError("unexpected manifest schema")
    raise PartialManifestValidationError("partial Day 1 artifact cannot satisfy a full production gate")
