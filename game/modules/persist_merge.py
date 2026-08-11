"""SYS-PERSIST epoch merge, startup validation, reset, and New Game contracts."""

from typing import Any, Iterable

from .persist_schema import snapshot_persist_root, validate_persist_root


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


def validate_startup_root(root: Any) -> bool:
    """Return False for legacy/invalid state without repairing or reading unknown values."""

    try:
        validate_persist_root(root)
    except (TypeError, ValueError):
        return False
    return True


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
