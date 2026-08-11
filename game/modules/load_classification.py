"""Detached SYS-SAVE load preflight and classification contracts.

The functions in this module are deliberately independent from Ren'Py store
state.  A decoded envelope is inspected and classified before any native load
or state installation is allowed.  Unknown values are never normalised,
iterated, hashed, or compared outside the exact checks that own them.
"""

from dataclasses import dataclass
from typing import Any, Callable

from .control_catalog import CATALOG_GENERATION_ID


EMPTY_SLOT_NOOP = "EMPTY_SLOT_NOOP"
UNREADABLE_SAVE = "UNREADABLE_SAVE"
LEGACY_INCOMPATIBLE = "LEGACY_INCOMPATIBLE"
UNSUPPORTED_VERSION = "UNSUPPORTED_VERSION"
CORRUPT_STATE = "CORRUPT_STATE"
UNSUPPORTED_CONTROL_LOCATION = "UNSUPPORTED_CONTROL_LOCATION"
INTERNAL_LOAD_VALIDATION_FAILURE = "INTERNAL_LOAD_VALIDATION_FAILURE"
SUPPORTED = "SUPPORTED"

SUPPORTED_SAVE_CONTRACT_SENTINEL = "save_contract:v1"
SUPPORTED_SEMANTIC_STATE_SENTINEL = "semantic_state:v2"
SUPPORTED_ENDING_FLOW_SENTINEL = "ending_flow:v1"

_CLASSIFICATION_CODES = frozenset(
    (
        EMPTY_SLOT_NOOP,
        UNREADABLE_SAVE,
        LEGACY_INCOMPATIBLE,
        UNSUPPORTED_VERSION,
        CORRUPT_STATE,
        UNSUPPORTED_CONTROL_LOCATION,
        INTERNAL_LOAD_VALIDATION_FAILURE,
        SUPPORTED,
    )
)


class LoadClassificationError(ValueError):
    """Raised when the detached load input shape is not the exact contract."""


@dataclass(frozen=True)
class LoadPreflightInput:
    """Decoded save fields needed for staged classification.

    The state values remain opaque until the validator that owns their stage
    receives them.  In particular, this record contains no fixture snapshot;
    checkpoint coherence is evaluated against the current runtime state.
    """

    save_contract_sentinel: Any
    catalog_generation_id: Any
    state_schema_sentinel: Any
    ending_flow_sentinel: Any
    semantic_state: Any
    ending_state: Any
    control_location_id: Any
    checkpoint_kind: Any
    catalog_valid: Any
    source_artifact_match: Any
    location_match_count: Any
    checkpoint_state_coherent: Any


@dataclass(frozen=True)
class LoadClassificationResult:
    """Classification plus the only safe downstream permissions."""

    classification: str
    install_allowed: bool
    loaded_scene_allowed: bool


@dataclass(frozen=True)
class LoadOperationResult:
    """Observable detached-load outcome used by the UI adapter and tests."""

    classification: str
    focus_slot: str
    install_allowed: bool
    loaded_scene_allowed: bool
    detached_inspection_calls: int
    classifier_calls: int
    native_load_calls: int


def make_load_preflight_input(**values: Any) -> LoadPreflightInput:
    """Build a decoded envelope only when all required dimensions are present."""

    expected = set(LoadPreflightInput.__dataclass_fields__)
    if set(values) != expected:
        raise LoadClassificationError(
            "load preflight fields must match the exact schema"
        )
    return LoadPreflightInput(**values)


def _result(classification: str) -> LoadClassificationResult:
    if classification not in _CLASSIFICATION_CODES:
        raise LoadClassificationError("unknown classification code")
    allowed = classification == SUPPORTED
    return LoadClassificationResult(classification, allowed, allowed)


def _validate_hook(name: str, hook: Any) -> None:
    if hook is not None and not callable(hook):
        raise TypeError("{} must be callable or None".format(name))


def _default_state_validator(_value: Any) -> Any:
    # A caller must supply the owner-system validator.  The fail-closed
    # fallback keeps a detached classifier from treating opaque state as valid.
    return None


def _default_location_matcher(record: LoadPreflightInput) -> Any:
    return record.location_match_count


def _default_checkpoint_validator(record: LoadPreflightInput) -> Any:
    return record.checkpoint_state_coherent


def _is_supported_exact_sentinel(value: Any, expected: str) -> bool:
    return type(value) is str and value == expected


def _classify_missing_sentinels(record: LoadPreflightInput) -> str | None:
    """Return the legacy result when any required marker is absent."""

    if any(
        value is None
        for value in (
            record.save_contract_sentinel,
            record.catalog_generation_id,
            record.state_schema_sentinel,
            record.ending_flow_sentinel,
        )
    ):
        return LEGACY_INCOMPATIBLE
    return None


def _classify_exact_versions(
    record: LoadPreflightInput,
    supported_catalog_generation: str,
) -> str | None:
    """Return unsupported version for any unknown or wrong-type marker."""

    expected_values = (
        (record.save_contract_sentinel, SUPPORTED_SAVE_CONTRACT_SENTINEL),
        (record.catalog_generation_id, supported_catalog_generation),
        (record.state_schema_sentinel, SUPPORTED_SEMANTIC_STATE_SENTINEL),
        (record.ending_flow_sentinel, SUPPORTED_ENDING_FLOW_SENTINEL),
    )
    for value, expected in expected_values:
        if not _is_supported_exact_sentinel(value, expected):
            return UNSUPPORTED_VERSION
    return None


def _classify_catalog_integrity(record: LoadPreflightInput) -> str | None:
    """Return internal failure for malformed or drifting catalog evidence."""

    if type(record.catalog_valid) is not bool:
        return INTERNAL_LOAD_VALIDATION_FAILURE
    if type(record.source_artifact_match) is not bool:
        return INTERNAL_LOAD_VALIDATION_FAILURE
    if not record.catalog_valid or not record.source_artifact_match:
        return INTERNAL_LOAD_VALIDATION_FAILURE
    return None


def _classify_state_validity(
    record: LoadPreflightInput,
    semantic_validator: Callable[[Any], bool] | None,
    ending_validator: Callable[[Any], bool] | None,
) -> str | None:
    """Run semantic then ending validation without interpreting opaque state."""

    semantic_check = (
        semantic_validator
        if semantic_validator is not None
        else _default_state_validator
    )
    ending_check = (
        ending_validator
        if ending_validator is not None
        else _default_state_validator
    )
    try:
        semantic_valid = semantic_check(record.semantic_state)
    except Exception:
        return INTERNAL_LOAD_VALIDATION_FAILURE
    if type(semantic_valid) is not bool:
        return INTERNAL_LOAD_VALIDATION_FAILURE
    if not semantic_valid:
        return CORRUPT_STATE

    try:
        ending_valid = ending_check(record.ending_state)
    except Exception:
        return INTERNAL_LOAD_VALIDATION_FAILURE
    if type(ending_valid) is not bool:
        return INTERNAL_LOAD_VALIDATION_FAILURE
    if not ending_valid:
        return CORRUPT_STATE
    return None


def _classify_location(
    record: LoadPreflightInput,
    location_matcher: Callable[[LoadPreflightInput], Any] | None,
) -> str | None:
    """Classify zero, one, or multiple production location matches."""

    location_check = (
        location_matcher
        if location_matcher is not None
        else _default_location_matcher
    )
    try:
        location_count = location_check(record)
    except Exception:
        return INTERNAL_LOAD_VALIDATION_FAILURE
    if type(location_count) is not int or location_count < 0:
        return INTERNAL_LOAD_VALIDATION_FAILURE
    if location_count == 0:
        return UNSUPPORTED_CONTROL_LOCATION
    if location_count != 1:
        return INTERNAL_LOAD_VALIDATION_FAILURE
    return None


def _classify_checkpoint(
    record: LoadPreflightInput,
    checkpoint_validator: Callable[[LoadPreflightInput], bool] | None,
) -> str | None:
    """Classify runtime checkpoint coherence after a unique location match."""

    checkpoint_check = (
        checkpoint_validator
        if checkpoint_validator is not None
        else _default_checkpoint_validator
    )
    try:
        checkpoint_coherent = checkpoint_check(record)
    except Exception:
        return INTERNAL_LOAD_VALIDATION_FAILURE
    if type(checkpoint_coherent) is not bool:
        return INTERNAL_LOAD_VALIDATION_FAILURE
    if not checkpoint_coherent:
        return CORRUPT_STATE
    return None


def _validate_preflight_args(
    slot_id: str,
    slot_present: bool,
    detached_reader: Any,
    classifier: Any,
    classifier_kwargs: Any,
) -> None:
    """Validate the adapter boundary before touching a slot or reader."""

    if type(slot_id) is not str or not slot_id:
        raise TypeError("slot_id must be a non-empty exact string")
    if type(slot_present) is not bool:
        raise TypeError("slot_present must be an exact bool")
    if not callable(detached_reader):
        raise TypeError("detached_reader must be callable")
    if not callable(classifier):
        raise TypeError("classifier must be callable")
    if classifier_kwargs is not None and type(classifier_kwargs) is not dict:
        raise TypeError("classifier_kwargs must be an exact dict or None")


def _operation_result(
    classification: str,
    slot_id: str,
    detached_inspection_calls: int,
    classifier_calls: int,
) -> LoadOperationResult:
    """Build a no-install operation result with native load permanently gated."""

    outcome = _result(classification)
    return LoadOperationResult(
        outcome.classification,
        slot_id,
        outcome.install_allowed,
        outcome.loaded_scene_allowed,
        detached_inspection_calls,
        classifier_calls,
        0,
    )


def _operation_from_outcome(
    outcome: LoadClassificationResult,
    slot_id: str,
) -> LoadOperationResult:
    """Attach detached/classifier counts to one validated classifier result."""

    if type(outcome) is not LoadClassificationResult:
        return _operation_result(
            INTERNAL_LOAD_VALIDATION_FAILURE,
            slot_id,
            1,
            1,
        )
    return LoadOperationResult(
        outcome.classification,
        slot_id,
        outcome.install_allowed,
        outcome.loaded_scene_allowed,
        1,
        1,
        0,
    )


def classify_load(
    record: LoadPreflightInput,
    *,
    supported_catalog_generation: str = CATALOG_GENERATION_ID,
    semantic_validator: Callable[[Any], bool] | None = None,
    ending_validator: Callable[[Any], bool] | None = None,
    location_matcher: Callable[[LoadPreflightInput], Any] | None = None,
    checkpoint_validator: Callable[[LoadPreflightInput], bool] | None = None,
) -> LoadClassificationResult:
    """Classify one detached envelope in the mandated fixed precedence.

    The order is input shape, missing sentinels, exact versions, catalog/source
    integrity, semantic/ending validity, location cardinality, then runtime
    checkpoint coherence.  This function never mutates live or persistent
    state and never performs a native load.
    """

    if type(record) is not LoadPreflightInput:
        raise TypeError("record must be an exact LoadPreflightInput")
    if type(supported_catalog_generation) is not str or not supported_catalog_generation:
        raise TypeError("supported_catalog_generation must be a non-empty exact string")
    _validate_hook("semantic_validator", semantic_validator)
    _validate_hook("ending_validator", ending_validator)
    _validate_hook("location_matcher", location_matcher)
    _validate_hook("checkpoint_validator", checkpoint_validator)

    # Empty and unreadable containers are handled by preflight_load_slot.  The
    # detached classifier starts after a readable, exact envelope exists.
    classification = _classify_missing_sentinels(record)
    if classification is not None:
        return _result(classification)
    classification = _classify_exact_versions(record, supported_catalog_generation)
    if classification is not None:
        return _result(classification)
    classification = _classify_catalog_integrity(record)
    if classification is not None:
        return _result(classification)
    classification = _classify_state_validity(
        record, semantic_validator, ending_validator
    )
    if classification is not None:
        return _result(classification)
    classification = _classify_location(record, location_matcher)
    if classification is not None:
        return _result(classification)
    classification = _classify_checkpoint(record, checkpoint_validator)
    if classification is not None:
        return _result(classification)
    return _result(SUPPORTED)


def preflight_load_slot(
    slot_id: str,
    slot_present: bool,
    *,
    detached_reader: Callable[[], Any],
    classifier: Callable[..., LoadClassificationResult] = classify_load,
    classifier_kwargs: dict[str, Any] | None = None,
) -> LoadOperationResult:
    """Gate a slot before installation, leaving native load to a later confirm.

    An empty slot returns immediately and preserves focus on that slot.  For an
    occupied slot, exactly one detached read is attempted; unreadable data is
    classified without invoking the classifier.  This preflight adapter never
    calls native load and never installs state.
    """

    _validate_preflight_args(
        slot_id,
        slot_present,
        detached_reader,
        classifier,
        classifier_kwargs,
    )

    if not slot_present:
        return _operation_result(EMPTY_SLOT_NOOP, slot_id, 0, 0)

    try:
        record = detached_reader()
    except Exception:
        return _operation_result(UNREADABLE_SAVE, slot_id, 1, 0)

    if type(record) is not LoadPreflightInput:
        return _operation_result(UNREADABLE_SAVE, slot_id, 1, 0)

    try:
        outcome = classifier(record, **(classifier_kwargs or {}))
    except Exception:
        return _operation_result(
            INTERNAL_LOAD_VALIDATION_FAILURE,
            slot_id,
            1,
            1,
        )
    return _operation_from_outcome(outcome, slot_id)
