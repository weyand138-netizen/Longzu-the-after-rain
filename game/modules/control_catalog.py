"""Immutable SYS-SAVE control-location and checkpoint catalog contracts.

This module validates production restore mappings independently from test-only
restore evidence. It does not inspect Ren'Py store state or use filesystem line
numbers as persistent identity.
"""

from dataclasses import dataclass
from re import match
from types import MappingProxyType
from typing import Any, Mapping


CHECKPOINT_KINDS = (
    "before_choice",
    "after_reaction",
    "before_payoff",
    "after_payoff",
)
CATALOG_GENERATION_ID = "catalog:v1"
_SHA256_PATTERN = r"^[0-9a-f]{64}$"


class CatalogValidationError(ValueError):
    """Raised when a production catalog or fixture manifest cannot freeze."""


@dataclass(frozen=True)
class ChoiceRestoreCheckpointRecord:
    """Test-only eleven-field SYS-CHOICE restore evidence record."""

    checkpoint_id: str
    checkpoint_kind: str
    control_location_id: str
    state_sentinel: str
    expected_history: tuple[str, ...]
    expected_axes: tuple[int, int, int, int, int]
    target_choice_id: str
    target_reaction_id: str
    target_payoff_id_or_none: str | None
    observation_horizon_id: str
    owner_system: str


@dataclass(frozen=True)
class RestoreControlLocationRecord:
    """Seven-field production mapping from a stable location to the engine."""

    control_location_id: str
    checkpoint_kind: str
    engine_statement_id: str
    source_artifact_hash: str
    catalog_generation_id: str
    action_gate_profile_id: str
    owner_system: str


@dataclass(frozen=True)
class SaveRestoreFixtureRecord:
    """Test-only eight-field save/restore fixture with nested choice evidence."""

    fixture_id: str
    choice_checkpoint_record: ChoiceRestoreCheckpointRecord
    expected_save_contract_sentinel: str
    expected_catalog_generation_id: str
    expected_ending_sentinel: str
    expected_ending_state: dict[str, Any]
    expected_pending_ending_id: str | None
    owner_system: str


@dataclass(frozen=True)
class ControlCatalog:
    """Frozen catalog with private immutable indexes for lookup and coverage."""

    generation_id: str
    production_records: tuple[RestoreControlLocationRecord, ...]
    fixture_records: tuple[SaveRestoreFixtureRecord, ...]
    production_by_key: Mapping[tuple[str, str], RestoreControlLocationRecord]
    fixture_by_id: Mapping[str, SaveRestoreFixtureRecord]


def _require_string(value: Any, field_name: str) -> None:
    if type(value) is not str or not value:
        raise CatalogValidationError("{} must be a non-empty exact string".format(field_name))


def _require_sha256(value: Any, field_name: str) -> None:
    _require_string(value, field_name)
    if match(_SHA256_PATTERN, value) is None:
        raise CatalogValidationError("{} must be a lowercase SHA-256 digest".format(field_name))


def _require_checkpoint_kind(value: Any) -> None:
    _require_string(value, "checkpoint_kind")
    if value not in CHECKPOINT_KINDS:
        raise CatalogValidationError("unsupported checkpoint kind: {!r}".format(value))


def _require_stable_identity(value: Any, field_name: str) -> None:
    _require_string(value, field_name)
    if match(r".*(?:^|[/\\])[^:]+:\d+$", value) is not None or ":line:" in value:
        raise CatalogValidationError("{} cannot use file-line identity".format(field_name))


def make_choice_restore_checkpoint_record(**values: Any) -> ChoiceRestoreCheckpointRecord:
    """Build and validate the exact eleven-field test checkpoint record."""

    expected = set(ChoiceRestoreCheckpointRecord.__dataclass_fields__)
    if set(values) != expected:
        raise CatalogValidationError("choice checkpoint fields must match the exact schema")
    record = ChoiceRestoreCheckpointRecord(**values)
    _validate_choice_record(record)
    return record


def make_restore_control_location_record(**values: Any) -> RestoreControlLocationRecord:
    """Build and validate the exact seven-field production location record."""

    expected = set(RestoreControlLocationRecord.__dataclass_fields__)
    if set(values) != expected:
        raise CatalogValidationError("control location fields must match the exact schema")
    record = RestoreControlLocationRecord(**values)
    _validate_location_record(record, record.catalog_generation_id)
    return record


def make_save_restore_fixture_record(**values: Any) -> SaveRestoreFixtureRecord:
    """Build and validate the exact eight-field test fixture record."""

    expected = set(SaveRestoreFixtureRecord.__dataclass_fields__)
    if set(values) != expected:
        raise CatalogValidationError("save fixture fields must match the exact schema")
    record = SaveRestoreFixtureRecord(**values)
    _validate_fixture_record(record, record.expected_catalog_generation_id)
    return record


def _validate_choice_record(record: ChoiceRestoreCheckpointRecord) -> None:
    if type(record) is not ChoiceRestoreCheckpointRecord:
        raise CatalogValidationError("choice checkpoint record has the wrong exact type")
    _require_string(record.checkpoint_id, "checkpoint_id")
    _require_checkpoint_kind(record.checkpoint_kind)
    _require_stable_identity(record.control_location_id, "control_location_id")
    _require_string(record.state_sentinel, "state_sentinel")
    if type(record.expected_history) is not tuple:
        raise CatalogValidationError("expected_history must be an exact tuple")
    if any(type(item) is not str or not item for item in record.expected_history):
        raise CatalogValidationError("expected_history must contain exact strings")
    if (
        type(record.expected_axes) is not tuple
        or len(record.expected_axes) != 5
        or any(type(value) is not int or not 0 <= value <= 3 for value in record.expected_axes)
    ):
        raise CatalogValidationError("expected_axes must contain five exact values from 0 to 3")
    _require_string(record.target_choice_id, "target_choice_id")
    _require_string(record.target_reaction_id, "target_reaction_id")
    if record.target_payoff_id_or_none is not None:
        _require_string(record.target_payoff_id_or_none, "target_payoff_id_or_none")
    _require_string(record.observation_horizon_id, "observation_horizon_id")
    _require_string(record.owner_system, "owner_system")


def _validate_location_record(
    record: RestoreControlLocationRecord,
    current_generation: str,
) -> None:
    if type(record) is not RestoreControlLocationRecord:
        raise CatalogValidationError("control location record has the wrong exact type")
    _require_stable_identity(record.control_location_id, "control_location_id")
    _require_checkpoint_kind(record.checkpoint_kind)
    _require_stable_identity(record.engine_statement_id, "engine_statement_id")
    _require_sha256(record.source_artifact_hash, "source_artifact_hash")
    _require_string(record.catalog_generation_id, "catalog_generation_id")
    _require_string(current_generation, "current_generation")
    if record.catalog_generation_id != current_generation:
        raise CatalogValidationError("catalog generation does not match current generation")
    _require_string(record.action_gate_profile_id, "action_gate_profile_id")
    _require_string(record.owner_system, "owner_system")


def _validate_fixture_record(
    record: SaveRestoreFixtureRecord,
    current_generation: str,
) -> None:
    if type(record) is not SaveRestoreFixtureRecord:
        raise CatalogValidationError("save fixture record has the wrong exact type")
    _require_string(record.fixture_id, "fixture_id")
    _validate_choice_record(record.choice_checkpoint_record)
    _require_string(record.expected_save_contract_sentinel, "expected_save_contract_sentinel")
    _require_string(record.expected_catalog_generation_id, "expected_catalog_generation_id")
    _require_string(current_generation, "current_generation")
    if record.expected_catalog_generation_id != current_generation:
        raise CatalogValidationError("fixture generation does not match current generation")
    _require_string(record.expected_ending_sentinel, "expected_ending_sentinel")
    if type(record.expected_ending_state) is not dict:
        raise CatalogValidationError("expected_ending_state must be an exact dict")
    if record.expected_pending_ending_id is not None:
        _require_string(record.expected_pending_ending_id, "expected_pending_ending_id")
    _require_string(record.owner_system, "owner_system")


def _location_key(record: RestoreControlLocationRecord) -> tuple[str, str]:
    return record.control_location_id, record.checkpoint_kind


def _validate_catalog_inputs(
    production_records: tuple[RestoreControlLocationRecord, ...],
    fixture_records: tuple[SaveRestoreFixtureRecord, ...],
    catalog_generation_id: str,
    canonical_source_hashes: dict[str, str],
    action_gate_profile_ids: tuple[str, ...],
) -> None:
    if type(production_records) is not tuple or not production_records:
        raise CatalogValidationError("production catalog must be a non-empty exact tuple")
    if type(fixture_records) is not tuple or not fixture_records:
        raise CatalogValidationError("fixture manifest must be a non-empty exact tuple")
    _require_string(catalog_generation_id, "catalog_generation_id")
    if type(canonical_source_hashes) is not dict or not canonical_source_hashes:
        raise CatalogValidationError("canonical source hashes must be a non-empty exact dict")
    if type(action_gate_profile_ids) is not tuple or not action_gate_profile_ids:
        raise CatalogValidationError("action gate profiles must be a non-empty exact tuple")
    if any(type(item) is not str or not item for item in action_gate_profile_ids):
        raise CatalogValidationError("action gate profiles must contain exact strings")
    if len(set(action_gate_profile_ids)) != len(action_gate_profile_ids):
        raise CatalogValidationError("action gate profiles must be unique")
    for statement_id, source_hash in canonical_source_hashes.items():
        _require_stable_identity(statement_id, "canonical statement ID")
        _require_sha256(source_hash, "canonical source hash")


def _index_production_records(
    records: tuple[RestoreControlLocationRecord, ...],
    catalog_generation_id: str,
    canonical_source_hashes: dict[str, str],
    action_gate_profile_ids: tuple[str, ...],
) -> dict[tuple[str, str], RestoreControlLocationRecord]:
    production_by_key: dict[tuple[str, str], RestoreControlLocationRecord] = {}
    statement_ids: set[str] = set()
    for record in records:
        _validate_location_record(record, catalog_generation_id)
        key = _location_key(record)
        if key in production_by_key:
            raise CatalogValidationError("duplicate production control key: {!r}".format(key))
        if record.engine_statement_id in statement_ids:
            raise CatalogValidationError("one engine statement maps to multiple records")
        if record.engine_statement_id not in canonical_source_hashes:
            raise CatalogValidationError("production statement is absent from canonical artifact")
        if canonical_source_hashes[record.engine_statement_id] != record.source_artifact_hash:
            raise CatalogValidationError("production source artifact hash drift detected")
        if record.action_gate_profile_id not in action_gate_profile_ids:
            raise CatalogValidationError("unresolved action gate profile")
        production_by_key[key] = record
        statement_ids.add(record.engine_statement_id)
    return production_by_key


def _index_fixture_records(
    records: tuple[SaveRestoreFixtureRecord, ...],
    catalog_generation_id: str,
    production_by_key: dict[tuple[str, str], RestoreControlLocationRecord],
) -> tuple[dict[str, SaveRestoreFixtureRecord], set[tuple[str, str]]]:
    fixture_by_id: dict[str, SaveRestoreFixtureRecord] = {}
    fixture_keys: set[tuple[str, str]] = set()
    for record in records:
        _validate_fixture_record(record, catalog_generation_id)
        if record.fixture_id in fixture_by_id:
            raise CatalogValidationError("duplicate fixture ID")
        key = (
            record.choice_checkpoint_record.control_location_id,
            record.choice_checkpoint_record.checkpoint_kind,
        )
        if key not in production_by_key:
            raise CatalogValidationError("fixture has no production mapping: {!r}".format(key))
        fixture_by_id[record.fixture_id] = record
        fixture_keys.add(key)
    return fixture_by_id, fixture_keys


def _validate_catalog_coverage(
    production_by_key: dict[tuple[str, str], RestoreControlLocationRecord],
    fixture_keys: set[tuple[str, str]],
    production_records: tuple[RestoreControlLocationRecord, ...],
    fixture_records: tuple[SaveRestoreFixtureRecord, ...],
) -> None:
    production_keys = set(production_by_key)
    if production_keys != fixture_keys:
        missing = sorted(production_keys - fixture_keys)
        raise CatalogValidationError("production mapping has no canonical fixture: {!r}".format(missing))
    if set(record.checkpoint_kind for record in production_records) != set(CHECKPOINT_KINDS):
        raise CatalogValidationError("production catalog must cover all four checkpoint kinds")
    if set(record.choice_checkpoint_record.checkpoint_kind for record in fixture_records) != set(CHECKPOINT_KINDS):
        raise CatalogValidationError("fixture manifest must cover all four checkpoint kinds")


def build_control_catalog(
    production_records: tuple[RestoreControlLocationRecord, ...],
    fixture_records: tuple[SaveRestoreFixtureRecord, ...],
    *,
    catalog_generation_id: str,
    canonical_source_hashes: dict[str, str],
    action_gate_profile_ids: tuple[str, ...],
) -> ControlCatalog:
    """Validate and freeze production mappings plus test-only fixture coverage."""

    _validate_catalog_inputs(
        production_records,
        fixture_records,
        catalog_generation_id,
        canonical_source_hashes,
        action_gate_profile_ids,
    )
    production_by_key = _index_production_records(
        production_records,
        catalog_generation_id,
        canonical_source_hashes,
        action_gate_profile_ids,
    )
    fixture_by_id, fixture_keys = _index_fixture_records(
        fixture_records,
        catalog_generation_id,
        production_by_key,
    )
    _validate_catalog_coverage(
        production_by_key,
        fixture_keys,
        production_records,
        fixture_records,
    )

    return ControlCatalog(
        generation_id=catalog_generation_id,
        production_records=production_records,
        fixture_records=fixture_records,
        production_by_key=MappingProxyType(production_by_key),
        fixture_by_id=MappingProxyType(fixture_by_id),
    )
