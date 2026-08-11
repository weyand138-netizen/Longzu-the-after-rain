"""Pure save-slot operations used by the SYS-SAVE foundation contract.

The helpers in this module do not own Ren'Py store state and do not define a
serialization format. Ren'Py remains responsible for serializing the actual
save envelope; these functions validate and arrange the transient operation
inputs around that engine boundary.
"""

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence


QUICKSAVE_SLOT_COUNT = 3
AUTOSAVE_SLOT_COUNT = 6
AUTOSAVE_CHECKPOINT_KINDS = frozenset(("after_reaction", "after_payoff"))


class SaveOperationError(ValueError):
    """Raised when a save operation cannot preserve its atomicity contract."""


@dataclass(frozen=True)
class SaveSlotRecord:
    """Immutable transient description of one slot's engine payload."""

    slot_id: str
    payload: bytes
    metadata: tuple[tuple[str, str], ...]
    sequence: int


def make_slot_record(
    slot_id: str,
    payload: bytes,
    metadata: Mapping[str, str],
    sequence: int,
) -> SaveSlotRecord:
    """Create a canonical, immutable slot record."""

    if type(slot_id) is not str or not slot_id:
        raise TypeError("slot_id must be a non-empty exact string")
    if type(payload) is not bytes:
        raise TypeError("payload must be exact bytes")
    if type(sequence) is not int or sequence < 0:
        raise TypeError("sequence must be a non-negative exact int")
    if type(metadata) is not dict:
        raise TypeError("metadata must be an exact dict")
    if any(type(key) is not str or type(value) is not str for key, value in metadata.items()):
        raise TypeError("metadata keys and values must be exact strings")
    return SaveSlotRecord(slot_id, payload, tuple(sorted(metadata.items())), sequence)


def snapshot_save_envelope(
    *,
    save_contract_sentinel: str,
    catalog_generation_id: str,
    semantic_state: Mapping[str, Any],
    ending_state: Mapping[str, Any],
    rollback_fields: Mapping[str, Any],
) -> dict[str, Any]:
    """Deep-copy the complete per-run save envelope at one stable point.

    The returned mapping is transient and must be handed to Ren'Py's native
    save machinery. It is not a second save format or a persistent root.
    """

    if type(save_contract_sentinel) is not str or not save_contract_sentinel:
        raise TypeError("save_contract_sentinel must be a non-empty exact string")
    if type(catalog_generation_id) is not str or not catalog_generation_id:
        raise TypeError("catalog_generation_id must be a non-empty exact string")
    for name, value in (
        ("semantic_state", semantic_state),
        ("ending_state", ending_state),
        ("rollback_fields", rollback_fields),
    ):
        if not isinstance(value, Mapping):
            raise TypeError("{} must be a mapping".format(name))

    return deepcopy(
        {
            "save_contract_sentinel": save_contract_sentinel,
            "catalog_generation_id": catalog_generation_id,
            "semantic_state": dict(semantic_state),
            "ending_state": dict(ending_state),
            "rollback_fields": dict(rollback_fields),
        }
    )


def _validate_slot_records(records: Sequence[SaveSlotRecord], capacity: int) -> None:
    if type(records) is not tuple:
        raise TypeError("records must be an exact tuple")
    if type(capacity) is not int or capacity <= 0:
        raise TypeError("capacity must be a positive exact int")
    if len(records) > capacity:
        raise SaveOperationError("slot collection exceeds capacity")
    ids = [record.slot_id for record in records]
    if len(ids) != len(set(ids)):
        raise SaveOperationError("slot IDs must be unique")
    if any(type(record) is not SaveSlotRecord for record in records):
        raise TypeError("records must contain SaveSlotRecord values")


def _next_sequence(records: Sequence[SaveSlotRecord]) -> int:
    return max((record.sequence for record in records), default=-1) + 1


def rotate_slots(
    records: tuple[SaveSlotRecord, ...],
    new_record: SaveSlotRecord,
    capacity: int,
) -> tuple[SaveSlotRecord, ...]:
    """Append a record, replacing only the oldest record when full."""

    _validate_slot_records(records, capacity)
    if type(new_record) is not SaveSlotRecord:
        raise TypeError("new_record must be a SaveSlotRecord")
    if new_record.slot_id in {record.slot_id for record in records}:
        raise SaveOperationError("rotating a duplicate slot ID is not allowed")

    current = list(records)
    if len(current) >= capacity:
        oldest_index = min(range(len(current)), key=lambda index: current[index].sequence)
        current.pop(oldest_index)
    current.append(
        SaveSlotRecord(
            new_record.slot_id,
            new_record.payload,
            new_record.metadata,
            _next_sequence(records),
        )
    )
    return tuple(sorted(current, key=lambda record: record.sequence))


def overwrite_slot(
    records: tuple[SaveSlotRecord, ...],
    slot_id: str,
    new_record: SaveSlotRecord,
    *,
    confirmed: bool,
) -> tuple[SaveSlotRecord, ...]:
    """Replace one manual slot only after explicit confirmation."""

    _validate_slot_records(records, max(1, len(records)))
    if type(slot_id) is not str or type(new_record) is not SaveSlotRecord:
        raise TypeError("slot_id and new_record have invalid types")
    if not confirmed:
        return records
    if slot_id not in {record.slot_id for record in records}:
        raise SaveOperationError("cannot overwrite an unknown slot")
    return tuple(
        new_record if record.slot_id == slot_id else record
        for record in records
    )


def autosave_trigger_allowed(
    *,
    checkpoint_kind: str,
    location_registered: bool,
    save_request_allowed: bool,
) -> bool:
    """Return whether an already-gated stable checkpoint may autosave."""

    return (
        type(checkpoint_kind) is str
        and checkpoint_kind in AUTOSAVE_CHECKPOINT_KINDS
        and location_registered is True
        and save_request_allowed is True
    )


def atomic_replace(
    store: Any,
    slot_id: str,
    payload: bytes,
) -> None:
    """Perform a temp-write/replace operation and verify its terminal state.

    ``store`` is an adapter around the engine/filesystem boundary. A failed
    operation may leave only the complete previous payload or the complete new
    payload; any other observed state raises ``SaveOperationError``.
    """

    if type(slot_id) is not str or type(payload) is not bytes:
        raise TypeError("slot_id and payload have invalid types")
    previous = store.read(slot_id) if store.exists(slot_id) else None
    try:
        store.write_temp(slot_id, payload)
        store.replace_temp(slot_id)
    except Exception:
        store.discard_temp(slot_id)
        current = store.read(slot_id) if store.exists(slot_id) else None
        if current not in (previous, payload):
            raise SaveOperationError("failed save left a partial slot")
        raise

    current = store.read(slot_id) if store.exists(slot_id) else None
    if current != payload:
        raise SaveOperationError("successful save did not produce the complete payload")


def classify_payload_without_metadata(
    payload: bytes,
    metadata: Any,
    decoder: Callable[[bytes], Any],
    validator: Callable[[Any], str],
) -> str:
    """Classify the authoritative payload while ignoring display metadata."""

    if type(payload) is not bytes:
        raise TypeError("payload must be exact bytes")
    if not callable(decoder) or not callable(validator):
        raise TypeError("decoder and validator must be callable")
    return validator(decoder(payload))
