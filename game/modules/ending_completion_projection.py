"""Durable SYS-PERSIST ending-completion boundary."""

from dataclasses import dataclass
from typing import Any, Callable

from .ending_rules import ENDING_PRIORITY
from .persist_batch import APPLIED_FLUSHED, COMMIT_STATUS_UNKNOWN
from .persist_schema import snapshot_persist_root, validate_persist_root


@dataclass(frozen=True)
class EndingCompletionEvent:
    """Exact event record emitted once at terminal completion."""

    ending_id: str
    completed_event_id: str
    checkpoint_id: str
    checkpoint_occurrence_id: str
    collection_epoch_id: int
    catalog_generation_id: str
    stable_completion_boundary: bool
    owner_system: str = "SYS-ENDING"


@dataclass(frozen=True)
class EndingCompletionResult:
    """Projection result including duplicate and call-count evidence."""

    status: str
    event: EndingCompletionEvent | None
    resolver_calls: int
    completion_calls: int


def commit_ending_completion(
    root: dict[str, Any],
    *,
    ending_id: str,
    checkpoint_id: str,
    checkpoint_occurrence_id: str,
    catalog_generation_id: str,
    replace_root: Callable[[dict[str, Any]], Any],
    flush: Callable[[], Any],
) -> EndingCompletionResult:
    """Emit one completion event and persist ending membership exactly once."""

    validate_persist_root(root)
    if ending_id not in ENDING_PRIORITY:
        raise ValueError("unknown ending")
    if any(type(value) is not str or not value for value in (checkpoint_id, checkpoint_occurrence_id, catalog_generation_id)):
        raise TypeError("completion identity fields must be non-empty strings")
    if ending_id in root["ending_ids"]:
        return EndingCompletionResult("DUPLICATE_NOOP", None, 0, 0)
    event = EndingCompletionEvent(
        ending_id,
        f"ending_completed:{ending_id}",
        checkpoint_id,
        checkpoint_occurrence_id,
        root["collection_epoch_id"],
        catalog_generation_id,
        True,
    )
    candidate = snapshot_persist_root(root)
    candidate["ending_ids"] = sorted((*candidate["ending_ids"], ending_id))
    replace_root(candidate)
    flush()
    return EndingCompletionResult(APPLIED_FLUSHED, event, 0, 1)


def completion_before_terminal(root: dict[str, Any], ending_id: str) -> bool:
    """Return whether an ending still lacks its durable completion membership."""

    validate_persist_root(root)
    return ending_id not in root["ending_ids"]
