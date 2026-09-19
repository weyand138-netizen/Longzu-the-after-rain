"""SYS-PERSIST epoch merge, startup validation, reset, and New Game contracts."""

from typing import Any, Iterable

from .persist_schema import snapshot_persist_root, validate_persist_root


# This is the only merge-created non-root value admitted for the product
# persistent field.  It is deliberately an exact built-in tuple: startup must
# classify it before it gives the value to the ordinary root validator.
MERGE_SAFE_RECOVERY_MARKER = (
    "PERSISTENCE_SAFE_RECOVERY",
    "merge_invalid_or_incompatible",
    "persist_catalog:v2",
)
STARTUP_PERSIST_READY = "READY"
STARTUP_PERSIST_SAFE_RECOVERY = "PERSISTENCE_SAFE_RECOVERY"


def is_merge_safe_recovery_marker(root: Any) -> bool:
    """Recognise only the GDD's exact merge-recovery marker.

    The exact-type guard prevents arbitrary persistent objects from running a
    custom equality method during startup classification.
    """

    return type(root) is tuple and root == MERGE_SAFE_RECOVERY_MARKER


def merge_persist_roots(roots: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Merge only roots from the maximum collection epoch."""

    candidates = tuple(roots)
    if not candidates:
        raise ValueError("at least one root is required")
    for root in candidates:
        validate_persist_root(root)
    max_epoch = max(root["collection_epoch_id"] for root in candidates)
    current = [root for root in candidates if root["collection_epoch_id"] == max_epoch]
    result = snapshot_persist_root(current[0])
    for field in ("achievement_ids", "seen_achievement_ids", "ending_ids", "memory_ids"):
        result[field] = sorted({item for root in current for item in root[field]})
    result["seen_achievement_ids"] = sorted(set(result["seen_achievement_ids"]).intersection(result["achievement_ids"]))
    return result


def merge_sys_persist_state(old: Any, new: Any, current: Any) -> dict[str, Any] | tuple[str, str, str]:
    """Merge the registered persistent field or return the exact safe marker.

    Ren'Py supplies the older and newer values in its documented order.  The
    project deliberately reads neither timestamp nor source identity.  The
    current object may be retained by the engine, so its settings must already
    equal one complete source settings tuple before a replacement value can be
    admitted.
    """

    try:
        validate_persist_root(old)
        validate_persist_root(new)
        validate_persist_root(current)
        if (
            old["schema_version"] != new["schema_version"]
            or old["schema_version"] != current["schema_version"]
            or old["catalog_generation_id"] != new["catalog_generation_id"]
            or old["catalog_generation_id"] != current["catalog_generation_id"]
        ):
            return MERGE_SAFE_RECOVERY_MARKER
        if current["settings"] != old["settings"] and current["settings"] != new["settings"]:
            return MERGE_SAFE_RECOVERY_MARKER

        sources = (old, new, current)
        maximum_epoch = max(root["collection_epoch_id"] for root in sources)
        maximum_epoch_sources = tuple(
            root for root in sources if root["collection_epoch_id"] == maximum_epoch
        )

        # Start from `new` so the GDD's all-or-nothing newer settings tuple is
        # retained.  Collection values are then rebuilt only from max-epoch
        # roots; lower-epoch memberships may never revive through a merge.
        merged = snapshot_persist_root(new)
        merged["collection_epoch_id"] = maximum_epoch
        for field in ("achievement_ids", "ending_ids", "memory_ids", "seen_achievement_ids"):
            merged[field] = sorted(
                {
                    item
                    for root in maximum_epoch_sources
                    for item in root[field]
                }
            )
        merged["seen_achievement_ids"] = sorted(
            set(merged["seen_achievement_ids"]).intersection(merged["achievement_ids"])
        )
        validate_persist_root(merged)
        return merged
    except (TypeError, ValueError):
        # Wrong type, schema, key order, member, generation, or settings
        # provenance is a safe-recovery classification, never a partial union.
        return MERGE_SAFE_RECOVERY_MARKER


def classify_startup_persist_root(root: Any) -> str:
    """Classify a startup persistent value before ordinary root validation."""

    if is_merge_safe_recovery_marker(root):
        return STARTUP_PERSIST_SAFE_RECOVERY
    try:
        validate_persist_root(root)
    except (TypeError, ValueError):
        return STARTUP_PERSIST_SAFE_RECOVERY
    return STARTUP_PERSIST_READY


def validate_startup_root(root: Any) -> bool:
    """Return False for legacy/invalid state without repairing or reading unknown values."""

    return classify_startup_persist_root(root) == STARTUP_PERSIST_READY


def reset_collection(root: dict[str, Any]) -> dict[str, Any]:
    """Increment epoch and clear collection memberships while preserving settings."""

    validate_persist_root(root)
    result = snapshot_persist_root(root)
    result["collection_epoch_id"] += 1
    for field in ("achievement_ids", "seen_achievement_ids", "ending_ids", "memory_ids"):
        result[field] = []
    return result


def make_new_game_envelope(root: dict[str, Any], run_state: dict[str, Any] | None = None) -> dict[str, Any]:
    """Copy the current epoch into a fresh rollback-owned run envelope."""

    validate_persist_root(root)
    envelope = {"collection_epoch_id": root["collection_epoch_id"], "semantic_state": run_state or {}}
    return snapshot_persist_root(root) | {"run_envelope": envelope}
