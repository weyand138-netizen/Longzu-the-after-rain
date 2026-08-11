"""SYS-PERSIST batch replacement, flush, and failure-state contracts."""

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable

from .persist_schema import snapshot_persist_root, validate_persist_root


APPLIED_FLUSHED = "APPLIED_FLUSHED"
PERSIST_FLUSH_FAILED_SAFE = "PERSIST_FLUSH_FAILED_SAFE"
COMMIT_STATUS_UNKNOWN = "COMMIT_STATUS_UNKNOWN"


class PersistBatchError(ValueError):
    """Raised for malformed persistence requests."""


@dataclass(frozen=True)
class PersistBatchResult:
    """Observable result of one complete-root replacement attempt."""

    status: str
    replacement_count: int
    flush_count: int
    write_frozen: bool
    root: dict[str, Any]


class PersistCoordinator:
    """Coordinate exactly one root replacement and one required flush per batch."""

    def __init__(self, root: dict[str, Any], replace_root: Callable[[dict[str, Any]], Any], flush: Callable[[], Any]):
        validate_persist_root(root)
        if not callable(replace_root) or not callable(flush):
            raise TypeError("replace_root and flush must be callable")
        self.root = snapshot_persist_root(root)
        self._replace_root = replace_root
        self._flush = flush
        self.replacement_count = 0
        self.flush_count = 0
        self.write_frozen = False

    def apply(self, candidate: dict[str, Any], *, safe_recovery: Callable[[dict[str, Any]], Any] | None = None) -> PersistBatchResult:
        """Replace and flush once; distinguish proven safe failure from unknown commit."""

        if self.write_frozen:
            return PersistBatchResult(COMMIT_STATUS_UNKNOWN, 0, 0, True, snapshot_persist_root(self.root))
        validate_persist_root(candidate)
        previous = snapshot_persist_root(self.root)
        next_root = snapshot_persist_root(candidate)
        try:
            self._replace_root(next_root)
            self.replacement_count += 1
            self._flush()
            self.flush_count += 1
        except Exception:
            if safe_recovery is not None:
                try:
                    safe_recovery(previous)
                    self.root = previous
                    return PersistBatchResult(PERSIST_FLUSH_FAILED_SAFE, self.replacement_count, self.flush_count, False, snapshot_persist_root(previous))
                except Exception:
                    pass
            self.write_frozen = True
            return PersistBatchResult(COMMIT_STATUS_UNKNOWN, self.replacement_count, self.flush_count, True, snapshot_persist_root(previous))
        self.root = next_root
        return PersistBatchResult(APPLIED_FLUSHED, self.replacement_count, self.flush_count, False, snapshot_persist_root(next_root))


def apply_complete_root_batch(
    root: dict[str, Any],
    candidate: dict[str, Any],
    *,
    replace_root: Callable[[dict[str, Any]], Any],
    flush: Callable[[], Any],
    safe_recovery: Callable[[dict[str, Any]], Any] | None = None,
) -> PersistBatchResult:
    """Convenience wrapper used by owner adapters and tests."""

    return PersistCoordinator(root, replace_root, flush).apply(candidate, safe_recovery=safe_recovery)
