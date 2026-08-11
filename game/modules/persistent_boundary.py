"""SYS-SAVE per-run and persistent-root isolation helpers."""

from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from .persist_schema import snapshot_persist_root, validate_persist_root


@dataclass(frozen=True)
class SaveIsolationSnapshot:
    run_state: dict[str, Any]
    persistent_root: dict[str, Any]


def capture_isolation_snapshot(run_state: dict[str, Any], persistent_root: dict[str, Any]) -> SaveIsolationSnapshot:
    validate_persist_root(persistent_root)
    return SaveIsolationSnapshot(deepcopy(run_state), snapshot_persist_root(persistent_root))


def restore_run_only(snapshot: SaveIsolationSnapshot, restored_run_state: dict[str, Any]) -> SaveIsolationSnapshot:
    validate_persist_root(snapshot.persistent_root)
    return SaveIsolationSnapshot(deepcopy(restored_run_state), snapshot_persist_root(snapshot.persistent_root))


def persistent_unchanged(before: SaveIsolationSnapshot, after: SaveIsolationSnapshot) -> bool:
    return before.persistent_root == after.persistent_root
