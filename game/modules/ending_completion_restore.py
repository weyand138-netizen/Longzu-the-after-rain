"""SYS-SAVE restore contract for the ADR-0006 ending boundary.

The module owns no ending decision, persistence writer, Ren'Py store state, or
resolver callback.  It validates detached completion evidence and models the
state that SYS-SAVE must restore around a terminal completion node.
"""

from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from .control_catalog import CATALOG_GENERATION_ID
from .ending_rules import ENDING_PRIORITY


ENDING_LIFECYCLES = ("Active", "Ended")
ENDING_COMPLETION_EVENT_FIELDS = (
    "ending_id",
    "completed_event_id",
    "checkpoint_id",
    "checkpoint_occurrence_id",
    "collection_epoch_id",
    "catalog_generation_id",
    "stable_completion_boundary",
    "owner_system",
)

PERSISTENT_ROOT_KEYS = (
    "schema_version",
    "catalog_generation_id",
    "collection_epoch_id",
    "achievement_ids",
    "seen_achievement_ids",
    "ending_ids",
    "memory_ids",
    "settings",
)
PERSISTENT_SETTING_KEYS = (
    "font_scale",
    "high_contrast",
    "reduced_motion",
    "flash_effects_enabled",
    "screen_shake_enabled",
)
PERSISTENT_LEAF_COUNT = 12

APPLIED_FLUSHED = "APPLIED_FLUSHED"
DUPLICATE_NOOP = "DUPLICATE_NOOP"
READY_TO_APPLY = "READY_TO_APPLY"


class EndingCompletionRestoreError(ValueError):
    """Raised when detached completion or persistent evidence is invalid."""


class _FrozenDict(dict):
    """Dict-compatible immutable container for detached persistent evidence."""

    def _reject_mutation(self, *args: Any, **kwargs: Any) -> None:
        raise TypeError("detached persistent evidence is immutable")

    __setitem__ = __delitem__ = clear = pop = popitem = setdefault = update = _reject_mutation
    __ior__ = _reject_mutation

    def __deepcopy__(self, memo: dict[int, Any]) -> "_FrozenDict":
        return self


class _FrozenList(list):
    """List-compatible immutable container for nested detached evidence."""

    def _reject_mutation(self, *args: Any, **kwargs: Any) -> None:
        raise TypeError("detached persistent evidence is immutable")

    __setitem__ = __delitem__ = append = clear = extend = insert = pop = remove = reverse = sort = _reject_mutation
    __iadd__ = __imul__ = _reject_mutation

    def __deepcopy__(self, memo: dict[int, Any]) -> "_FrozenList":
        return self


def _freeze_value(value: Any) -> Any:
    """Recursively freeze only the detached containers used by evidence."""

    if isinstance(value, (_FrozenDict, _FrozenList)):
        return value
    if isinstance(value, dict):
        return _FrozenDict((key, _freeze_value(item)) for key, item in value.items())
    if isinstance(value, list):
        return _FrozenList(_freeze_value(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze_value(item) for item in value)
    if isinstance(value, set):
        return frozenset(_freeze_value(item) for item in value)
    return value


@dataclass(frozen=True)
class EndingCompletionEventRecord:
    """The exact eight-field rollback-owned ADR-0006 completion record."""

    ending_id: str
    completed_event_id: str
    checkpoint_id: str
    checkpoint_occurrence_id: str
    collection_epoch_id: int
    catalog_generation_id: str
    stable_completion_boundary: bool
    owner_system: str


@dataclass(frozen=True)
class PersistentBoundarySnapshot:
    """Detached 12-leaf persistent state observed at a completion boundary."""

    root: dict[str, Any]
    ending_membership: tuple[str, ...]
    collection_epoch_id: int
    writer_count: int
    flush_count: int


@dataclass(frozen=True)
class EndingCompletionSaveSnapshot:
    """Saved rollback-owned state before or after ending completion."""

    ending_id: str
    control_location_id: str
    ending_lifecycle: str
    ending_completion_event_record: EndingCompletionEventRecord | None
    persistent_snapshot: PersistentBoundarySnapshot
    ending_request_count: int
    resolver_call_count: int


@dataclass(frozen=True)
class EndingCompletionRestoreResult:
    """Restored transient state plus the untouched current persistent root."""

    restored_snapshot: EndingCompletionSaveSnapshot
    persistent_snapshot: PersistentBoundarySnapshot
    resolver_call_count: int


@dataclass(frozen=True)
class CompletionReplayClassification:
    """Pure classification of a replayed completion request."""

    status: str
    persistent_snapshot: PersistentBoundarySnapshot
    ending_request_count: int
    writer_count: int
    flush_count: int
    notification_count: int
    resolver_call_count: int


def _require_non_empty_string(value: Any, field_name: str) -> None:
    if type(value) is not str or not value:
        raise EndingCompletionRestoreError(
            "{} must be a non-empty exact string".format(field_name)
        )


def _require_non_negative_int(value: Any, field_name: str) -> None:
    if type(value) is not int or value < 0:
        raise EndingCompletionRestoreError(
            "{} must be a non-negative exact int".format(field_name)
        )


def _validate_id_tuple(value: Any, field_name: str) -> None:
    if type(value) is not tuple:
        raise EndingCompletionRestoreError(
            "{} must be an exact tuple".format(field_name)
        )
    if any(type(item) is not str or not item for item in value):
        raise EndingCompletionRestoreError(
            "{} must contain non-empty exact strings".format(field_name)
        )
    if tuple(sorted(value, key=lambda item: item.encode("utf-8"))) != value:
        raise EndingCompletionRestoreError(
            "{} must use canonical UTF-8 ordering".format(field_name)
        )
    if len(value) != len(set(value)):
        raise EndingCompletionRestoreError(
            "{} must not contain duplicates".format(field_name)
        )


def _validate_persistent_root(root: Any) -> None:
    if type(root) not in (dict, _FrozenDict):
        raise EndingCompletionRestoreError("persistent root must be an exact dict")
    if tuple(root.keys()) != PERSISTENT_ROOT_KEYS:
        raise EndingCompletionRestoreError(
            "persistent root must contain the exact 12-leaf schema"
        )
    if type(root["schema_version"]) is not int or root["schema_version"] != 2:
        raise EndingCompletionRestoreError("persistent schema_version must be exact 2")
    _require_non_empty_string(root["catalog_generation_id"], "catalog_generation_id")
    _require_non_negative_int(root["collection_epoch_id"], "collection_epoch_id")
    for field_name in ("achievement_ids", "seen_achievement_ids", "ending_ids", "memory_ids"):
        _validate_id_tuple(root[field_name], field_name)
    if not set(root["seen_achievement_ids"]).issubset(root["achievement_ids"]):
        raise EndingCompletionRestoreError(
            "seen_achievement_ids must be a subset of achievement_ids"
        )
    settings = root["settings"]
    if type(settings) not in (dict, _FrozenDict) or tuple(settings.keys()) != PERSISTENT_SETTING_KEYS:
        raise EndingCompletionRestoreError(
            "settings must contain the exact five setting leaves"
        )
    if type(settings["font_scale"]) is not float:
        raise EndingCompletionRestoreError("font_scale must be an exact float")
    if settings["font_scale"] not in (1.0, 1.25, 1.5, 1.75, 2.0):
        raise EndingCompletionRestoreError("font_scale is outside the approved values")
    for field_name in PERSISTENT_SETTING_KEYS[1:]:
        if type(settings[field_name]) is not bool:
            raise EndingCompletionRestoreError(
                "{} must be an exact bool".format(field_name)
            )


def _validate_persistent_snapshot(snapshot: Any) -> None:
    if type(snapshot) is not PersistentBoundarySnapshot:
        raise TypeError("persistent_snapshot must be an exact PersistentBoundarySnapshot")
    if type(snapshot.root) is not _FrozenDict:
        raise TypeError("persistent snapshot root must be deeply immutable")
    _validate_persistent_root(snapshot.root)
    _require_non_negative_int(snapshot.collection_epoch_id, "collection_epoch_id")
    _require_non_negative_int(snapshot.writer_count, "writer_count")
    _require_non_negative_int(snapshot.flush_count, "flush_count")
    _validate_id_tuple(snapshot.ending_membership, "ending_membership")
    if snapshot.collection_epoch_id != snapshot.root["collection_epoch_id"]:
        raise EndingCompletionRestoreError("snapshot epoch does not match persistent root")
    if snapshot.ending_membership != snapshot.root["ending_ids"]:
        raise EndingCompletionRestoreError("ending membership does not match persistent root")


def _validate_event_record(record: Any) -> None:
    if type(record) is not EndingCompletionEventRecord:
        raise TypeError("event record must be an exact EndingCompletionEventRecord")
    if type(record.ending_id) is not str or record.ending_id not in ENDING_PRIORITY:
        raise EndingCompletionRestoreError("ending_id is not a canonical ending")
    _require_non_empty_string(record.completed_event_id, "completed_event_id")
    if record.completed_event_id != "ending_completed:" + record.ending_id:
        raise EndingCompletionRestoreError("completed_event_id does not match ending_id")
    _require_non_empty_string(record.checkpoint_id, "checkpoint_id")
    _require_non_empty_string(record.checkpoint_occurrence_id, "checkpoint_occurrence_id")
    _require_non_negative_int(record.collection_epoch_id, "collection_epoch_id")
    _require_non_empty_string(record.catalog_generation_id, "catalog_generation_id")
    if record.stable_completion_boundary is not True:
        raise EndingCompletionRestoreError("stable_completion_boundary must be exact True")
    if type(record.owner_system) is not str or record.owner_system != "SYS-ENDING":
        raise EndingCompletionRestoreError("owner_system must be SYS-ENDING")


def _validate_completion_relationships(snapshot: EndingCompletionSaveSnapshot) -> None:
    """Validate the pre/post completion relationship inside one save snapshot."""

    if snapshot.ending_completion_event_record is None:
        if snapshot.ending_lifecycle != "Active" or snapshot.ending_request_count != 0:
            raise EndingCompletionRestoreError(
                "pre-completion snapshots must be Active with zero ending requests"
            )
        if snapshot.ending_id in snapshot.persistent_snapshot.ending_membership:
            raise EndingCompletionRestoreError(
                "pre-completion snapshot cannot contain current ending membership"
            )
        if snapshot.persistent_snapshot.writer_count != 0 or snapshot.persistent_snapshot.flush_count != 0:
            raise EndingCompletionRestoreError(
                "pre-completion snapshots must have zero writer and flush counts"
            )
        return

    event = snapshot.ending_completion_event_record
    if event.ending_id != snapshot.ending_id:
        raise EndingCompletionRestoreError("event ending_id does not match snapshot")
    if snapshot.ending_lifecycle != "Ended" or snapshot.ending_request_count != 1:
        raise EndingCompletionRestoreError(
            "post-completion snapshots must be Ended with one ending request"
        )
    if snapshot.ending_id not in snapshot.persistent_snapshot.ending_membership:
        raise EndingCompletionRestoreError(
            "post-completion snapshot must contain ending membership"
        )
    if snapshot.persistent_snapshot.writer_count != 1 or snapshot.persistent_snapshot.flush_count != 1:
        raise EndingCompletionRestoreError(
            "post-completion snapshots must have one writer and one flush"
        )
    if event.collection_epoch_id != snapshot.persistent_snapshot.collection_epoch_id:
        raise EndingCompletionRestoreError("event epoch does not match persistent epoch")
    if event.catalog_generation_id != snapshot.persistent_snapshot.root["catalog_generation_id"]:
        raise EndingCompletionRestoreError(
            "event catalog generation does not match persistent root"
        )


def _validate_completion_save_snapshot(snapshot: EndingCompletionSaveSnapshot) -> None:
    """Validate a complete detached save snapshot before restore or storage."""

    if type(snapshot) is not EndingCompletionSaveSnapshot:
        raise TypeError("snapshot must be an exact EndingCompletionSaveSnapshot")
    if type(snapshot.ending_id) is not str or snapshot.ending_id not in ENDING_PRIORITY:
        raise EndingCompletionRestoreError("ending_id is not a canonical ending")
    _require_non_empty_string(snapshot.control_location_id, "control_location_id")
    if type(snapshot.ending_lifecycle) is not str or snapshot.ending_lifecycle not in ENDING_LIFECYCLES:
        raise EndingCompletionRestoreError("unsupported ending lifecycle")
    if snapshot.ending_completion_event_record is not None:
        _validate_event_record(snapshot.ending_completion_event_record)
    _validate_persistent_snapshot(snapshot.persistent_snapshot)
    _require_non_negative_int(snapshot.ending_request_count, "ending_request_count")
    _require_non_negative_int(snapshot.resolver_call_count, "resolver_call_count")
    _validate_completion_relationships(snapshot)


def make_ending_completion_event_record(**values: Any) -> EndingCompletionEventRecord:
    """Build the exact ADR-0006 event record without producing a completion."""

    if set(values) != set(ENDING_COMPLETION_EVENT_FIELDS):
        raise EndingCompletionRestoreError(
            "ending completion event fields must match the exact eight-field schema"
        )
    record = EndingCompletionEventRecord(**values)
    _validate_event_record(record)
    return record


def make_persistent_boundary_snapshot(
    root: dict[str, Any],
    *,
    writer_count: int,
    flush_count: int,
) -> PersistentBoundarySnapshot:
    """Detach a validated persistent root and its write/flush evidence."""

    _validate_persistent_root(root)
    _require_non_negative_int(writer_count, "writer_count")
    _require_non_negative_int(flush_count, "flush_count")
    detached_root = _freeze_value(deepcopy(root))
    return PersistentBoundarySnapshot(
        detached_root,
        detached_root["ending_ids"],
        detached_root["collection_epoch_id"],
        writer_count,
        flush_count,
    )


def make_ending_completion_save_snapshot(
    *,
    ending_id: str,
    control_location_id: str,
    ending_lifecycle: str,
    ending_completion_event_record: EndingCompletionEventRecord | None,
    persistent_snapshot: PersistentBoundarySnapshot,
    ending_request_count: int,
    resolver_call_count: int,
) -> EndingCompletionSaveSnapshot:
    """Build a pre- or post-completion save snapshot with fixed invariants."""

    snapshot = EndingCompletionSaveSnapshot(
        ending_id,
        control_location_id,
        ending_lifecycle,
        ending_completion_event_record,
        persistent_snapshot,
        ending_request_count,
        resolver_call_count,
    )
    _validate_completion_save_snapshot(snapshot)
    return snapshot


def restore_ending_completion_snapshot(
    snapshot: EndingCompletionSaveSnapshot,
    current_persistent_snapshot: PersistentBoundarySnapshot,
) -> EndingCompletionRestoreResult:
    """Restore transient completion/control state without replacing persistent data."""

    _validate_completion_save_snapshot(snapshot)
    _validate_persistent_snapshot(current_persistent_snapshot)
    return EndingCompletionRestoreResult(
        restored_snapshot=snapshot,
        persistent_snapshot=current_persistent_snapshot,
        resolver_call_count=0,
    )


def persistent_boundary_unchanged(
    before: PersistentBoundarySnapshot,
    after: PersistentBoundarySnapshot,
) -> bool:
    """Compare all persistent values that SYS-SAVE is forbidden to mutate."""

    _validate_persistent_snapshot(before)
    _validate_persistent_snapshot(after)
    return (
        before.root == after.root
        and before.ending_membership == after.ending_membership
        and before.collection_epoch_id == after.collection_epoch_id
        and before.writer_count == after.writer_count
        and before.flush_count == after.flush_count
    )


def classify_completion_replay(
    event_record: EndingCompletionEventRecord,
    current_persistent_snapshot: PersistentBoundarySnapshot,
) -> CompletionReplayClassification:
    """Classify a replay without writing, resolving, or notifying.

    The persistence coordinator owns the actual write.  This pure helper proves
    that a flushed membership replay is an idempotent no-op at the restore
    boundary.
    """

    _validate_event_record(event_record)
    _validate_persistent_snapshot(current_persistent_snapshot)
    if event_record.collection_epoch_id != current_persistent_snapshot.collection_epoch_id:
        raise EndingCompletionRestoreError("replay event epoch does not match persistent epoch")
    if event_record.catalog_generation_id != current_persistent_snapshot.root["catalog_generation_id"]:
        raise EndingCompletionRestoreError("replay event catalog generation does not match persistent root")
    if event_record.ending_id in current_persistent_snapshot.ending_membership:
        return CompletionReplayClassification(
            DUPLICATE_NOOP,
            current_persistent_snapshot,
            ending_request_count=0,
            writer_count=0,
            flush_count=0,
            notification_count=0,
            resolver_call_count=0,
        )
    return CompletionReplayClassification(
        READY_TO_APPLY,
        current_persistent_snapshot,
        ending_request_count=1,
        writer_count=1,
        flush_count=1,
        notification_count=1,
        resolver_call_count=0,
    )


def default_persistent_root(
    *,
    catalog_generation_id: str = CATALOG_GENERATION_ID,
    collection_epoch_id: int = 0,
    ending_ids: tuple[str, ...] = (),
) -> dict[str, Any]:
    """Build the exact 12-leaf root used by integration evidence fixtures."""

    root = {
        "schema_version": 2,
        "catalog_generation_id": catalog_generation_id,
        "collection_epoch_id": collection_epoch_id,
        "achievement_ids": (),
        "seen_achievement_ids": (),
        "ending_ids": ending_ids,
        "memory_ids": (),
        "settings": {
            "font_scale": 1.0,
            "high_contrast": False,
            "reduced_motion": False,
            "flash_effects_enabled": False,
            "screen_shake_enabled": False,
        },
    }
    _validate_persistent_root(root)
    return root
