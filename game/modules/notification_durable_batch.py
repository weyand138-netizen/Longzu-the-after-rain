"""Pure notification-membership planning and one-owner commit coordination.

The live Ren'Py owner is ``10_state.rpy``. It stores one instance of
``NotificationMembershipOperationCoordinator`` in ``renpy.session`` and is
the only runtime caller of its write path. This module stays engine-free so
its catalog checks, candidate construction, failure freeze, and exact result
shape can be tested without a Ren'Py store.
"""

from __future__ import annotations

from dataclasses import dataclass
import threading
from typing import Any, Callable, Iterable

from .ending_rules import ENDING_PRIORITY
from .notification_contract import (
    NotificationRawGroup,
    make_notification_raw_group,
    utf8_byte_sort,
)
from .persist_batch import (
    APPLIED_FLUSHED,
    COMMIT_STATUS_UNKNOWN,
    PERSIST_FLUSH_FAILED_SAFE,
    REJECTED_REENTRANT,
    PersistBatchResult,
)
from .durable_flush_bridge import DurableFlushBridge, DurableFlushPreflight
from .persist_projections import ACHIEVEMENT_IDS
from .persist_schema import snapshot_persist_root, validate_persist_root


DUPLICATE_NOOP = "DUPLICATE_NOOP"
MEMORY_IDS = tuple("MEMORY_DAY_{}".format(day) for day in range(1, 8))


@dataclass(frozen=True)
class DurableNotificationResult:
    """Exact detached result; raw identity is never placed in the product root."""

    status: str
    checkpoint_occurrence_id: str
    collection_epoch_id: int
    added_achievement_ids: tuple[str, ...]
    existing_achievement_ids: tuple[str, ...]
    added_ending_ids: tuple[str, ...]
    added_memory_ids: tuple[str, ...]
    newly_seen_achievement_ids: tuple[str, ...]
    raw_group: NotificationRawGroup | None
    batch_result: PersistBatchResult | None

    @property
    def notification_group_id(self) -> str:
        return "" if self.raw_group is None else self.raw_group.notification_group_id


@dataclass(frozen=True)
class DurableSeenResult:
    """Result of the dedicated owner-routed achievement seen acknowledgement.

    A seen acknowledgement changes the canonical persistent root but is not a
    newly unlocked membership. It therefore never carries a raw notification
    group or any presentation instruction.
    """

    status: str
    newly_seen_achievement_ids: tuple[str, ...]
    batch_result: PersistBatchResult | None


@dataclass(frozen=True)
class NotificationMembershipPlan:
    """Validated detached delta prepared before the single owner writes."""

    checkpoint_occurrence_id: str
    collection_epoch_id: int
    added_achievement_ids: tuple[str, ...]
    existing_achievement_ids: tuple[str, ...]
    added_ending_ids: tuple[str, ...]
    added_memory_ids: tuple[str, ...]
    candidate_root: dict[str, Any] | None


def _normalise_requested(values: Iterable[str], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, (tuple, list)):
        raise TypeError(field_name + " must be a tuple/list")
    requested = tuple(values)
    if any(type(value) is not str or not value for value in requested):
        raise TypeError(field_name + " must contain non-empty exact strings")
    if len(requested) != len(set(requested)):
        raise ValueError(field_name + " must not contain duplicates")
    return requested


def _authorise_requested(
    requested: tuple[str, ...], allowed: tuple[str, ...], field_name: str
) -> tuple[str, ...]:
    unknown = utf8_byte_sort(set(requested).difference(allowed))
    if unknown:
        raise ValueError(
            field_name + " contains IDs outside the frozen catalog: " + ", ".join(unknown)
        )
    return requested


def _membership_delta(
    root: dict[str, Any], field_name: str, requested: tuple[str, ...]
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    existing_set = set(root[field_name])
    existing = utf8_byte_sort(value for value in requested if value in existing_set)
    added = utf8_byte_sort(value for value in requested if value not in existing_set)
    return added, existing


def _root_membership_order(values: Iterable[str]) -> list[str]:
    """Keep the schema's frozen root ordering.

    All currently admitted catalog IDs are ASCII, so the schema's lexicographic
    order is exactly its UTF-8 byte order. Raw notification identities use the
    byte ordering explicitly through ``utf8_byte_sort`` above.
    """

    return sorted(set(values))


def plan_notification_durable_membership(
    root: dict[str, Any],
    *,
    checkpoint_occurrence_id: str,
    achievement_ids: Iterable[str] = (),
    ending_ids: Iterable[str] = (),
    memory_ids: Iterable[str] = (),
) -> NotificationMembershipPlan:
    """Validate catalog membership and build a detached complete-root candidate.

    Planning never creates a raw notification identity and never invokes a
    persistence callback. Only the session-owned runtime coordinator may turn
    this plan into a successful durable result.
    """

    validate_persist_root(root)
    if type(checkpoint_occurrence_id) is not str or not checkpoint_occurrence_id:
        raise TypeError("checkpoint_occurrence_id must be a non-empty exact string")
    try:
        checkpoint_occurrence_id.encode("utf-8")
    except UnicodeEncodeError as error:
        raise ValueError("checkpoint_occurrence_id must contain Unicode scalar values") from error
    achievements = _authorise_requested(
        _normalise_requested(achievement_ids, "achievement_ids"),
        ACHIEVEMENT_IDS,
        "achievement_ids",
    )
    endings = _authorise_requested(
        _normalise_requested(ending_ids, "ending_ids"),
        ENDING_PRIORITY,
        "ending_ids",
    )
    memories = _authorise_requested(
        _normalise_requested(memory_ids, "memory_ids"),
        MEMORY_IDS,
        "memory_ids",
    )
    added_achievements, existing_achievements = _membership_delta(
        root, "achievement_ids", achievements
    )
    added_endings, _existing_endings = _membership_delta(root, "ending_ids", endings)
    added_memories, _existing_memories = _membership_delta(root, "memory_ids", memories)
    candidate = None
    if added_achievements or added_endings or added_memories:
        candidate = snapshot_persist_root(root)
        candidate["achievement_ids"] = _root_membership_order(
            candidate["achievement_ids"] + list(added_achievements)
        )
        candidate["ending_ids"] = _root_membership_order(
            candidate["ending_ids"] + list(added_endings)
        )
        candidate["memory_ids"] = _root_membership_order(
            candidate["memory_ids"] + list(added_memories)
        )
        validate_persist_root(candidate)
    return NotificationMembershipPlan(
        checkpoint_occurrence_id,
        root["collection_epoch_id"],
        added_achievements,
        existing_achievements,
        added_endings,
        added_memories,
        candidate,
    )


def _result_for_plan(
    plan: NotificationMembershipPlan,
    status: str,
    batch_result: PersistBatchResult | None,
) -> DurableNotificationResult:
    raw_group = None
    if status == APPLIED_FLUSHED:
        raw_group = make_notification_raw_group(
            collection_epoch_id=plan.collection_epoch_id,
            checkpoint_occurrence_id=plan.checkpoint_occurrence_id,
            added_achievement_ids=plan.added_achievement_ids,
            added_ending_ids=plan.added_ending_ids,
            added_memory_ids=plan.added_memory_ids,
        )
    return DurableNotificationResult(
        status,
        plan.checkpoint_occurrence_id,
        plan.collection_epoch_id,
        plan.added_achievement_ids,
        plan.existing_achievement_ids,
        plan.added_ending_ids,
        plan.added_memory_ids,
        (),
        raw_group,
        batch_result,
    )


class NotificationMembershipOperationCoordinator:
    """Serialize the one runtime owner's read/plan/replace/flush/result unit.

    The instance deliberately owns no persistent or save data. ``10_state``
    keeps it in ``renpy.session`` with its ``RLock``. If a replace or flush
    outcome is unknown, both detached roots remain on this session instance and
    every later request is consumed as ``COMMIT_STATUS_UNKNOWN`` without a
    projection, write, raw group, or success feedback.
    """

    def __init__(
        self,
        root_reader: Callable[[], dict[str, Any]],
        replace_root: Callable[[dict[str, Any]], Any],
        flush: Callable[[], Any] | DurableFlushBridge,
        *,
        operation_lock: Any | None = None,
    ):
        bridge_flush = isinstance(flush, DurableFlushBridge)
        if not callable(root_reader) or not callable(replace_root) or (not callable(flush) and not bridge_flush):
            raise TypeError("root_reader and replace_root must be callable; flush must be callable or a DurableFlushBridge")
        self._root_reader = root_reader
        self._replace_root = replace_root
        self._flush = flush
        self._operation_lock = threading.RLock() if operation_lock is None else operation_lock
        if not hasattr(self._operation_lock, "__enter__"):
            raise TypeError("operation_lock must be a context manager")
        # Admission is intentionally independent from the lock held across a
        # root replacement and its durable flush.  If the same lock guarded
        # both, a second request that arrives during a long flush could wait
        # until the first body released it, then race ``end_external_operation``
        # and be admitted as a later write.  The frozen contract rejects such
        # requests without a queue or replay, so this tiny gate only protects
        # the active reservation while ``_operation_lock`` still protects the
        # actual root transaction.
        self._admission_lock = threading.RLock()
        self._write_frozen = False
        self._operation_active = False
        self._frozen_previous_root: dict[str, Any] | None = None
        self._frozen_candidate_root: dict[str, Any] | None = None

    @property
    def write_frozen(self) -> bool:
        with self._operation_lock:
            return self._write_frozen

    def begin_external_operation(self) -> bool:
        """Reserve the shared owner for a non-membership root request.

        SYS-ACCESS uses this for its one settings batch.  It is deliberately a
        boolean reservation rather than a queue: an attempted nested request
        is rejected synchronously and is never replayed after the active body.
        """

        with self._admission_lock:
            if self._operation_active:
                return False
            self._operation_active = True
            return True

    def end_external_operation(self) -> None:
        """Release a previously admitted external operation exactly once."""

        with self._admission_lock:
            if not self._operation_active:
                raise RuntimeError("no persistent operation is active")
            self._operation_active = False

    def _reentrant_result(self, checkpoint_occurrence_id: str) -> DurableNotificationResult:
        """Return the non-queued result for an attempted nested membership call."""

        root = snapshot_persist_root(self._root_reader())
        return DurableNotificationResult(
            REJECTED_REENTRANT,
            checkpoint_occurrence_id,
            root["collection_epoch_id"],
            (),
            (),
            (),
            (),
            (),
            None,
            None,
        )

    def _reentrant_seen_result(self) -> DurableSeenResult:
        """Reject a nested seen acknowledgement without a replacement."""

        return DurableSeenResult(REJECTED_REENTRANT, (), None)

    def frozen_root_copies(self) -> tuple[dict[str, Any], dict[str, Any]] | None:
        """Return detached diagnostics only; never re-enable a frozen writer."""

        with self._operation_lock:
            if self._frozen_previous_root is None or self._frozen_candidate_root is None:
                return None
            return (
                snapshot_persist_root(self._frozen_previous_root),
                snapshot_persist_root(self._frozen_candidate_root),
            )

    def freeze_unknown_root_write(
        self,
        previous_root: dict[str, Any],
        candidate_root: dict[str, Any],
    ) -> bool:
        """Freeze the shared owner after any root replacement has an unknown outcome.

        ``10_state`` also uses the coordinator lock for SYS-ACCESS settings.
        A settings replacement or flush can therefore make the durable root
        indeterminate just as a notification-membership batch can.  Preserve
        the exact detached before/after candidates and refuse all later root
        writes in that session.  ``False`` means an earlier unknown write was
        already retained and remains the authoritative recovery diagnostic.
        """

        previous = snapshot_persist_root(previous_root)
        candidate = snapshot_persist_root(candidate_root)
        with self._operation_lock:
            if self._write_frozen:
                return False
            self._write_frozen = True
            self._frozen_previous_root = previous
            self._frozen_candidate_root = candidate
            return True

    def _frozen_result(self, checkpoint_occurrence_id: str) -> DurableNotificationResult:
        previous = self._frozen_previous_root
        if previous is None:
            raise RuntimeError("frozen notification coordinator lacks its previous root")
        batch = PersistBatchResult(
            COMMIT_STATUS_UNKNOWN,
            0,
            0,
            True,
            snapshot_persist_root(previous),
        )
        return DurableNotificationResult(
            COMMIT_STATUS_UNKNOWN,
            checkpoint_occurrence_id,
            previous["collection_epoch_id"],
            (),
            (),
            (),
            (),
            (),
            None,
            batch,
        )

    def _freeze(
        self,
        previous: dict[str, Any],
        candidate: dict[str, Any],
        replacement_count: int,
        flush_count: int,
        plan: NotificationMembershipPlan,
    ) -> DurableNotificationResult:
        self._write_frozen = True
        self._frozen_previous_root = snapshot_persist_root(previous)
        self._frozen_candidate_root = snapshot_persist_root(candidate)
        batch = PersistBatchResult(
            COMMIT_STATUS_UNKNOWN,
            replacement_count,
            flush_count,
            True,
            snapshot_persist_root(previous),
        )
        return _result_for_plan(plan, COMMIT_STATUS_UNKNOWN, batch)

    def _frozen_seen_result(self) -> DurableSeenResult:
        """Return the common unknown result without admitting a seen write."""

        previous = self._frozen_previous_root
        if previous is None:
            raise RuntimeError("frozen notification coordinator lacks its previous root")
        return DurableSeenResult(
            COMMIT_STATUS_UNKNOWN,
            (),
            PersistBatchResult(
                COMMIT_STATUS_UNKNOWN,
                0,
                0,
                True,
                snapshot_persist_root(previous),
            ),
        )

    def _freeze_seen(
        self,
        previous: dict[str, Any],
        candidate: dict[str, Any],
        replacement_count: int,
        flush_count: int,
    ) -> DurableSeenResult:
        """Freeze the shared owner after an ambiguous seen-state write."""

        self._write_frozen = True
        self._frozen_previous_root = snapshot_persist_root(previous)
        self._frozen_candidate_root = snapshot_persist_root(candidate)
        return DurableSeenResult(
            COMMIT_STATUS_UNKNOWN,
            (),
            PersistBatchResult(
                COMMIT_STATUS_UNKNOWN,
                replacement_count,
                flush_count,
                True,
                snapshot_persist_root(previous),
            ),
        )

    def commit(
        self,
        *,
        checkpoint_occurrence_id: str,
        achievement_ids: Iterable[str] = (),
        ending_ids: Iterable[str] = (),
        memory_ids: Iterable[str] = (),
        safe_recovery: Callable[[dict[str, Any]], Any] | None = None,
    ) -> DurableNotificationResult:
        """Run one complete root operation under the session-local lock."""

        if safe_recovery is not None and not callable(safe_recovery):
            raise TypeError("safe_recovery must be callable when supplied")
        if type(checkpoint_occurrence_id) is not str or not checkpoint_occurrence_id:
            raise TypeError("checkpoint_occurrence_id must be a non-empty exact string")
        if not self.begin_external_operation():
            return self._reentrant_result(checkpoint_occurrence_id)
        try:
            return self._commit_admitted(
                checkpoint_occurrence_id=checkpoint_occurrence_id,
                achievement_ids=achievement_ids,
                ending_ids=ending_ids,
                memory_ids=memory_ids,
                safe_recovery=safe_recovery,
            )
        finally:
            self.end_external_operation()

    def _commit_admitted(
        self,
        *,
        checkpoint_occurrence_id: str,
        achievement_ids: Iterable[str],
        ending_ids: Iterable[str],
        memory_ids: Iterable[str],
        safe_recovery: Callable[[dict[str, Any]], Any] | None,
    ) -> DurableNotificationResult:
        """Perform an already-reserved membership operation under the owner lock."""

        with self._operation_lock:
            # A frozen session refuses even a different later batch. It cannot
            # safely re-read, diff, queue, or acknowledge anything as durable.
            if self._write_frozen:
                return self._frozen_result(checkpoint_occurrence_id)
            root = snapshot_persist_root(self._root_reader())
            plan = plan_notification_durable_membership(
                root,
                checkpoint_occurrence_id=checkpoint_occurrence_id,
                achievement_ids=achievement_ids,
                ending_ids=ending_ids,
                memory_ids=memory_ids,
            )
            if plan.candidate_root is None:
                return _result_for_plan(plan, DUPLICATE_NOOP, None)
            preflight: DurableFlushPreflight | None = None
            if isinstance(self._flush, DurableFlushBridge):
                preflight = self._flush.preflight()
                if not preflight.ready:
                    batch = PersistBatchResult(
                        PERSIST_FLUSH_FAILED_SAFE,
                        0,
                        0,
                        False,
                        snapshot_persist_root(root),
                    )
                    return _result_for_plan(plan, PERSIST_FLUSH_FAILED_SAFE, batch)
            previous = snapshot_persist_root(root)
            candidate = snapshot_persist_root(plan.candidate_root)
            replacement_count = 0
            flush_count = 0
            try:
                # Keep the retained candidate detached from a callback that
                # mutates its input while the persistence outcome is unknown.
                self._replace_root(snapshot_persist_root(candidate))
                replacement_count = 1
                if isinstance(self._flush, DurableFlushBridge):
                    flush_result = self._flush.flush_after_replacement(
                        preflight,
                        snapshot_persist_root(candidate),
                    )
                    if not flush_result.verified:
                        raise OSError("durable flush bridge could not verify the candidate")
                else:
                    self._flush()
                flush_count = 1
            except Exception:
                # A DurableFlushBridge reaches this block only after the
                # complete root replacement. Its result is therefore
                # indeterminate by ADR-0012: an older callback cannot restore
                # memory and relabel it as a proven pre-write safe failure.
                if not isinstance(self._flush, DurableFlushBridge) and safe_recovery is not None:
                    try:
                        safe_recovery(snapshot_persist_root(previous))
                        batch = PersistBatchResult(
                            PERSIST_FLUSH_FAILED_SAFE,
                            replacement_count,
                            flush_count,
                            False,
                            snapshot_persist_root(previous),
                        )
                        return _result_for_plan(plan, PERSIST_FLUSH_FAILED_SAFE, batch)
                    except Exception:
                        pass
                return self._freeze(
                    previous,
                    candidate,
                    replacement_count,
                    flush_count,
                    plan,
                )
            batch = PersistBatchResult(
                APPLIED_FLUSHED,
                replacement_count,
                flush_count,
                False,
                snapshot_persist_root(candidate),
            )
            return _result_for_plan(plan, APPLIED_FLUSHED, batch)

    def mark_achievements_seen(
        self,
        *,
        achievement_ids: Iterable[str],
    ) -> DurableSeenResult:
        """Durably acknowledge unlocked achievements through the sole owner.

        This deliberately is not a generic root mutator: callers may only
        mark already-unlocked catalog achievement IDs as seen. A changing
        acknowledgement follows the same preflight, one replacement, strict
        bridge, and unknown-freeze contract as membership. It has no raw group
        because acknowledgement is never an unlock/presentation event.
        """

        requested = _normalise_requested(achievement_ids, "achievement_ids")
        if not self.begin_external_operation():
            return self._reentrant_seen_result()
        try:
            return self._mark_seen_admitted(requested)
        finally:
            self.end_external_operation()

    def _mark_seen_admitted(self, requested: tuple[str, ...]) -> DurableSeenResult:
        """Perform an already-reserved seen acknowledgement under the owner lock."""

        with self._operation_lock:
            if self._write_frozen:
                return self._frozen_seen_result()
            root = snapshot_persist_root(self._root_reader())
            unknown = utf8_byte_sort(set(requested).difference(root["achievement_ids"]))
            if unknown:
                raise ValueError(
                    "achievement_ids must already belong to achievement membership: "
                    + ", ".join(unknown)
                )
            newly_seen = utf8_byte_sort(
                set(requested).difference(root["seen_achievement_ids"])
            )
            if not newly_seen:
                return DurableSeenResult(DUPLICATE_NOOP, (), None)
            preflight: DurableFlushPreflight | None = None
            if isinstance(self._flush, DurableFlushBridge):
                preflight = self._flush.preflight()
                if not preflight.ready:
                    return DurableSeenResult(
                        PERSIST_FLUSH_FAILED_SAFE,
                        (),
                        PersistBatchResult(
                            PERSIST_FLUSH_FAILED_SAFE,
                            0,
                            0,
                            False,
                            snapshot_persist_root(root),
                        ),
                    )
            previous = snapshot_persist_root(root)
            candidate = snapshot_persist_root(root)
            candidate["seen_achievement_ids"] = _root_membership_order(
                candidate["seen_achievement_ids"] + list(newly_seen)
            )
            validate_persist_root(candidate)
            replacement_count = 0
            flush_count = 0
            try:
                self._replace_root(snapshot_persist_root(candidate))
                replacement_count = 1
                if isinstance(self._flush, DurableFlushBridge):
                    flush_result = self._flush.flush_after_replacement(
                        preflight,
                        snapshot_persist_root(candidate),
                    )
                    if not flush_result.verified:
                        raise OSError("durable flush bridge could not verify the candidate")
                else:
                    self._flush()
                flush_count = 1
            except Exception:
                return self._freeze_seen(
                    previous,
                    candidate,
                    replacement_count,
                    flush_count,
                )
            return DurableSeenResult(
                APPLIED_FLUSHED,
                newly_seen,
                PersistBatchResult(
                    APPLIED_FLUSHED,
                    replacement_count,
                    flush_count,
                    False,
                    snapshot_persist_root(candidate),
                ),
            )


def apply_notification_durable_batch(
    root: dict[str, Any],
    *,
    checkpoint_occurrence_id: str,
    achievement_ids: Iterable[str] = (),
    ending_ids: Iterable[str] = (),
    memory_ids: Iterable[str] = (),
    replace_root: Callable[[dict[str, Any]], Any],
    flush: Callable[[], Any],
    safe_recovery: Callable[[dict[str, Any]], Any] | None = None,
) -> DurableNotificationResult:
    """Compatibility harness for pure tests, not a live runtime owner.

    It still performs a real callback replacement and flush before exposing a
    raw group. Product code must instead use the session-owned coordinator in
    ``10_state.rpy`` so consecutive operations share its lock and freeze state.
    """

    return NotificationMembershipOperationCoordinator(
        lambda: root,
        replace_root,
        flush,
    ).commit(
        checkpoint_occurrence_id=checkpoint_occurrence_id,
        achievement_ids=achievement_ids,
        ending_ids=ending_ids,
        memory_ids=memory_ids,
        safe_recovery=safe_recovery,
    )
