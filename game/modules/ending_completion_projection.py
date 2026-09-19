"""Durable SYS-PERSIST ending-completion boundary."""

from dataclasses import dataclass
from typing import Any

from .ending_rules import ENDING_PRIORITY
from .notification_durable_batch import (
    DUPLICATE_NOOP,
    DurableNotificationResult,
)
from .persist_batch import APPLIED_FLUSHED
from .persist_schema import validate_persist_root


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
    notification_result: DurableNotificationResult | None = None


def commit_ending_completion(
    root: dict[str, Any],
    *,
    ending_id: str,
    checkpoint_id: str,
    checkpoint_occurrence_id: str,
    catalog_generation_id: str,
    notification_result: DurableNotificationResult,
) -> EndingCompletionResult:
    """Build an exact completion event from the 10_state-owned durable result.

    This pure projection deliberately cannot replace or flush a root. The sole
    runtime persistence owner has already committed (or classified) the ending
    membership before it calls here.
    """

    validate_persist_root(root)
    if ending_id not in ENDING_PRIORITY:
        raise ValueError("unknown ending")
    if any(type(value) is not str or not value for value in (checkpoint_id, checkpoint_occurrence_id, catalog_generation_id)):
        raise TypeError("completion identity fields must be non-empty strings")
    if type(notification_result) is not DurableNotificationResult:
        raise TypeError("notification_result must be a DurableNotificationResult")
    if notification_result.checkpoint_occurrence_id != checkpoint_occurrence_id:
        raise ValueError("durable result does not match the completion occurrence")
    if notification_result.collection_epoch_id != root["collection_epoch_id"]:
        raise ValueError("durable result does not match the collection epoch")
    if notification_result.status not in (APPLIED_FLUSHED, DUPLICATE_NOOP):
        return EndingCompletionResult(notification_result.status, None, 0, 0, notification_result)
    if ending_id not in root["ending_ids"]:
        raise ValueError("durable ending result lacks root membership")
    if notification_result.status == APPLIED_FLUSHED:
        if notification_result.added_ending_ids != (ending_id,) or notification_result.raw_group is None:
            raise ValueError("applied ending result does not prove exactly one new ending")
    elif notification_result.added_ending_ids or notification_result.raw_group is not None:
        raise ValueError("duplicate ending result must not expose a raw notification group")
    event = EndingCompletionEvent(
        ending_id,
        f"ending_completed:{ending_id}",
        checkpoint_id,
        checkpoint_occurrence_id,
        root["collection_epoch_id"],
        catalog_generation_id,
        True,
    )
    return EndingCompletionResult(
        notification_result.status,
        event,
        0,
        1 if notification_result.status == APPLIED_FLUSHED else 0,
        notification_result,
    )


def completion_before_terminal(root: dict[str, Any], ending_id: str) -> bool:
    """Return whether an ending still lacks its durable completion membership."""

    validate_persist_root(root)
    return ending_id not in root["ending_ids"]
