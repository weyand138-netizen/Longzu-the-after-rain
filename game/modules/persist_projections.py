"""SYS-PERSIST durable ending and achievement projection helpers."""

from dataclasses import dataclass
from typing import Any, Iterable

from .persist_schema import PERSIST_CATALOG_GENERATION_ID, snapshot_persist_root, validate_persist_root


ACHIEVEMENT_IDS = (
    "CHOICE_READ_THE_NOTE", "CHOICE_ASK_FIRST", "CHOICE_ACCEPT_NO",
    "CHOICE_SHARE_TRUTH", "CHOICE_KEEP_PROMISE", "ROUTE_ARCADE_ALIAS",
    "ROUTE_EMPTY_SCHOOL", "ROUTE_SEASIDE_TICKET", "ROUTE_BACKUP_EXIT",
    "EPILOGUE_FIRST_GUEST", "EPILOGUE_LIGHTS_OUT",
)


@dataclass(frozen=True)
class AchievementCondition:
    """Frozen condition record owned by SYS-ACHIEVE."""

    achievement_id: str
    condition_event_ids: tuple[str, ...]
    condition_operator: str
    zero_delta_witness_path_ids: tuple[str, ...]
    non_best_ending_witness_path_ids: tuple[str, ...]
    reveal_policy: str
    display_order_group: str
    owner_system: str = "SYS-ACHIEVE"


def build_achievement_catalog() -> tuple[AchievementCondition, ...]:
    """Build the exact eleven-record catalog from stable event IDs."""

    records = []
    for index, achievement_id in enumerate(ACHIEVEMENT_IDS):
        records.append(AchievementCondition(
            achievement_id,
            (f"event_{achievement_id.lower()}",),
            "all",
            (f"witness_{achievement_id.lower()}",),
            (),
            "ON_UNLOCK",
            "01_scene_echoes" if index < 5 else "02_route_discoveries" if index < 9 else "03_true_epilogue",
        ))
    return tuple(records)


ACHIEVEMENT_CATALOG = build_achievement_catalog()


def validate_achievement_catalog(catalog: Any) -> None:
    """Reject missing, mirrored, duplicated, or non-canonical records."""

    if type(catalog) is not tuple or len(catalog) != 11:
        raise ValueError("achievement catalog must contain exactly 11 records")
    ids = tuple(record.achievement_id for record in catalog if type(record) is AchievementCondition)
    if ids != ACHIEVEMENT_IDS or len(set(ids)) != 11:
        raise ValueError("achievement catalog IDs must match the approved v2 catalog")
    for record in catalog:
        if not record.condition_event_ids or record.condition_operator != "all" or record.reveal_policy != "ON_UNLOCK" or record.owner_system != "SYS-ACHIEVE":
            raise ValueError("achievement condition record violates the frozen contract")
        if record.achievement_id.startswith(("ENDING_", "MEMORY_")):
            raise ValueError("ending/memory IDs cannot be mirrored as achievements")


@dataclass(frozen=True)
class AchievementSnapshot:
    """Detached event snapshot supplied to the evaluator."""

    catalog_generation_id: str
    collection_epoch_id: int
    checkpoint_occurrence_id: str
    checkpoint_id: str
    completed_event_ids: tuple[str, ...]
    newly_completed_event_ids: tuple[str, ...]
    stable_completion_boundary: bool


def evaluate_achievement_candidates(
    snapshot: AchievementSnapshot,
    membership: Iterable[str],
    *,
    catalog: tuple[AchievementCondition, ...] = ACHIEVEMENT_CATALOG,
    expected_generation: str = PERSIST_CATALOG_GENERATION_ID,
    expected_epoch: int | None = None,
) -> tuple[str, ...]:
    """Return only newly satisfied IDs in approved UTF-8 stable order."""

    validate_achievement_catalog(catalog)
    if type(snapshot) is not AchievementSnapshot or type(snapshot.catalog_generation_id) is not str or snapshot.catalog_generation_id != expected_generation:
        return ()
    if type(snapshot.collection_epoch_id) is not int or expected_epoch is not None and snapshot.collection_epoch_id != expected_epoch:
        return ()
    if type(snapshot.stable_completion_boundary) is not bool or not snapshot.stable_completion_boundary:
        return ()
    if type(snapshot.checkpoint_occurrence_id) is not str or not snapshot.checkpoint_occurrence_id:
        return ()
    completed = set(snapshot.completed_event_ids)
    newly = set(snapshot.newly_completed_event_ids)
    existing = set(membership)
    result = []
    for record in catalog:
        required = set(record.condition_event_ids)
        if required.issubset(completed) and record.condition_event_ids[-1] in newly and record.achievement_id not in existing:
            result.append(record.achievement_id)
    return tuple(sorted(result))


@dataclass(frozen=True)
class AchievementProjectionResult:
    """Detached achievement planning record used by non-runtime presentation tests."""

    status: str
    checkpoint_occurrence_id: str
    collection_epoch_id: int
    added_achievement_ids: tuple[str, ...]
    existing_achievement_ids: tuple[str, ...]
    notification_group_id: str


def project_achievements(
    root: dict[str, Any],
    achievement_ids: Iterable[str],
    *,
    checkpoint_occurrence_id: str,
) -> tuple[dict[str, Any], AchievementProjectionResult]:
    """Plan new achievements without claiming durable notification output.

    This is retained as a detached planning helper for existing presentation
    tests. It is not a persistence adapter: it performs no root replacement or
    flush and therefore must never manufacture a raw notification identity.
    Live callers use the session-owned 10_state coordinator instead.
    """

    validate_persist_root(root)
    if type(checkpoint_occurrence_id) is not str or not checkpoint_occurrence_id:
        raise TypeError("checkpoint occurrence must be a non-empty string")
    requested = tuple(achievement_ids)
    if len(requested) != len(set(requested)) or any(item not in ACHIEVEMENT_IDS for item in requested):
        raise ValueError("achievement request contains duplicate or unknown IDs")
    current = set(root["achievement_ids"])
    existing = tuple(sorted(item for item in requested if item in current))
    added = tuple(sorted(item for item in requested if item not in current))
    candidate = snapshot_persist_root(root)
    candidate["achievement_ids"] = sorted(current.union(added))
    result = AchievementProjectionResult(
        "PLANNED",
        checkpoint_occurrence_id,
        root["collection_epoch_id"],
        added,
        existing,
        "",
    )
    return candidate, result


def mark_achievements_seen(root: dict[str, Any], ids: Iterable[str]) -> dict[str, Any]:
    """Idempotently add only already-unlocked IDs to the seen subset."""

    validate_persist_root(root)
    requested = tuple(ids)
    if any(item not in root["achievement_ids"] for item in requested):
        raise ValueError("cannot mark an unknown achievement as seen")
    candidate = snapshot_persist_root(root)
    candidate["seen_achievement_ids"] = sorted(set(root["seen_achievement_ids"]).union(requested))
    return candidate
