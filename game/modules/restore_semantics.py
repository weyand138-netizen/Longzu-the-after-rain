"""Pure SYS-SAVE checkpoint restore and loaded-save rollback semantics.

This module describes what a stable checkpoint permits the next observation
window to do.  It does not own Ren'Py store state, persistent data, rollback
history, or a reaction/payoff dedupe ledger; engine adapters apply the returned
plan at their controlled boundary.
"""

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable

from .control_catalog import CHECKPOINT_KINDS
from .ending_rules import ENDING_PENDING_IDS


RESTORE_SOURCES = ("manual", "quick", "auto")
ACTIVE_LIFECYCLE = "Active"
ENDED_LIFECYCLE = "Ended"
VALID_PENDING_ENDING_IDS = frozenset(
    ENDING_PENDING_IDS
)


class RestoreSemanticsError(ValueError):
    """Raised when a restore snapshot or loaded-save session is malformed."""


class _FrozenDict(dict):
    """Dict-compatible immutable container for detached semantic state."""

    def _reject_mutation(self, *args: Any, **kwargs: Any) -> None:
        raise TypeError("detached semantic state is immutable")

    __setitem__ = __delitem__ = clear = pop = popitem = setdefault = update = _reject_mutation
    __ior__ = _reject_mutation

    def __deepcopy__(self, memo: dict[int, Any]) -> "_FrozenDict":
        return self


class _FrozenList(list):
    """List-compatible immutable container for detached semantic state."""

    def _reject_mutation(self, *args: Any, **kwargs: Any) -> None:
        raise TypeError("detached semantic state is immutable")

    __setitem__ = __delitem__ = append = clear = extend = insert = pop = remove = reverse = sort = _reject_mutation
    __iadd__ = __imul__ = _reject_mutation

    def __deepcopy__(self, memo: dict[int, Any]) -> "_FrozenList":
        return self


def _freeze_value(value: Any) -> Any:
    if isinstance(value, _FrozenDict) or isinstance(value, _FrozenList):
        return value
    if isinstance(value, dict):
        return _FrozenDict(
            (key, _freeze_value(item)) for key, item in value.items()
        )
    if isinstance(value, list):
        return _FrozenList(_freeze_value(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze_value(item) for item in value)
    if isinstance(value, set):
        return frozenset(_freeze_value(item) for item in value)
    return value


def _detach_semantic_state(value: Any) -> _FrozenDict:
    return _freeze_value(deepcopy(value))


@dataclass(frozen=True)
class RestoreSnapshot:
    """Runtime restore facts captured at one stable control location."""

    source: str
    checkpoint_kind: str
    control_location_id: str
    semantic_state: dict[str, Any]
    ending_lifecycle: str
    pending_ending_id: str | None
    observation_horizon_id: str
    target_choice_id: str | None
    target_reaction_id: str | None
    target_payoff_id_or_none: str | None


@dataclass(frozen=True)
class RestorePlan:
    """Counts and identity for one new post-restore observation window."""

    snapshot: RestoreSnapshot
    observation_window_id: str
    choice_commit_calls: int
    reaction_calls: int
    payoff_calls: int
    resolver_calls: int


@dataclass(frozen=True)
class RestoreTraversalTrace:
    """Observed calls made while traversing one restore plan."""

    observation_window_id: str
    choice_commit_calls: int
    reaction_calls: int
    payoff_calls: int
    resolver_calls: int


@dataclass(frozen=True)
class LoadedRestoreSession:
    """Rollback history owned exclusively by the successfully loaded save."""

    snapshots: tuple[RestoreSnapshot, ...]
    current_index: int


@dataclass(frozen=True)
class RestoreActionState:
    """Visibility and invocation permissions at a rollback boundary."""

    save_allowed: bool
    load_allowed: bool
    rollback_allowed: bool


@dataclass(frozen=True)
class RollbackResult:
    """Result of moving within, or safely refusing to leave, loaded history."""

    session: LoadedRestoreSession
    restored_snapshot: RestoreSnapshot
    action_state: RestoreActionState
    invocation_count: int


def _require_optional_string(value: Any, field_name: str) -> None:
    if value is not None and (type(value) is not str or not value):
        raise RestoreSemanticsError(
            "{} must be None or a non-empty exact string".format(field_name)
        )


def _validate_snapshot(snapshot: RestoreSnapshot) -> None:
    if type(snapshot) is not RestoreSnapshot:
        raise TypeError("snapshot must be an exact RestoreSnapshot")
    if type(snapshot.source) is not str or snapshot.source not in RESTORE_SOURCES:
        raise RestoreSemanticsError("unsupported restore source")
    if type(snapshot.checkpoint_kind) is not str or snapshot.checkpoint_kind not in CHECKPOINT_KINDS:
        raise RestoreSemanticsError("unsupported checkpoint kind")
    if type(snapshot.control_location_id) is not str or not snapshot.control_location_id:
        raise RestoreSemanticsError("control_location_id must be a non-empty exact string")
    if type(snapshot.semantic_state) is not _FrozenDict:
        raise TypeError("semantic_state must be a detached immutable dict")
    if type(snapshot.ending_lifecycle) is not str or snapshot.ending_lifecycle not in (
        ACTIVE_LIFECYCLE,
        ENDED_LIFECYCLE,
    ):
        raise RestoreSemanticsError("unsupported ending lifecycle")
    _require_optional_string(snapshot.pending_ending_id, "pending_ending_id")
    if type(snapshot.observation_horizon_id) is not str or not snapshot.observation_horizon_id:
        raise RestoreSemanticsError("observation_horizon_id must be a non-empty exact string")
    _require_optional_string(snapshot.target_choice_id, "target_choice_id")
    _require_optional_string(snapshot.target_reaction_id, "target_reaction_id")
    _require_optional_string(
        snapshot.target_payoff_id_or_none,
        "target_payoff_id_or_none",
    )
    if snapshot.ending_lifecycle == ENDED_LIFECYCLE and snapshot.pending_ending_id is None:
        raise RestoreSemanticsError("Ended snapshots require a pending ending ID")
    if (
        snapshot.pending_ending_id is not None
        and snapshot.pending_ending_id not in VALID_PENDING_ENDING_IDS
    ):
        raise RestoreSemanticsError("pending ending ID is not a supported ending")


def make_restore_snapshot(**values: Any) -> RestoreSnapshot:
    """Build an exact stable restore snapshot without fixture-derived rules."""

    expected = set(RestoreSnapshot.__dataclass_fields__)
    if set(values) != expected:
        raise RestoreSemanticsError("restore snapshot fields must match the exact schema")
    snapshot_values = dict(values)
    snapshot_values["semantic_state"] = _detach_semantic_state(
        snapshot_values["semantic_state"]
    )
    snapshot = RestoreSnapshot(**snapshot_values)
    _validate_snapshot(snapshot)
    return snapshot


def canonical_restore_matrix() -> tuple[tuple[str, str], ...]:
    """Return the twelve source/checkpoint combinations required by SYS-SAVE."""

    return tuple(
        (source, checkpoint_kind)
        for source in RESTORE_SOURCES
        for checkpoint_kind in CHECKPOINT_KINDS
    )


def build_restore_plan(snapshot: RestoreSnapshot) -> RestorePlan:
    """Translate one checkpoint and lifecycle into one observation-window plan."""

    _validate_snapshot(snapshot)
    observation_window_id = "{}::{}::{}".format(
        snapshot.source,
        snapshot.control_location_id,
        snapshot.observation_horizon_id,
    )
    if snapshot.ending_lifecycle == ENDED_LIFECYCLE:
        return RestorePlan(snapshot, observation_window_id, 0, 0, 0, 0)
    if snapshot.checkpoint_kind == "before_choice":
        return RestorePlan(snapshot, observation_window_id, 1, 1, 0, 0)
    if snapshot.checkpoint_kind == "before_payoff":
        return RestorePlan(snapshot, observation_window_id, 0, 0, 1, 0)
    if snapshot.checkpoint_kind in ("after_reaction", "after_payoff"):
        return RestorePlan(snapshot, observation_window_id, 0, 0, 0, 0)
    raise RestoreSemanticsError("checkpoint kind has no restore plan")


def run_observation_window(
    snapshot: RestoreSnapshot,
    *,
    choice_commit: Callable[[RestoreSnapshot], Any],
    reaction: Callable[[RestoreSnapshot], Any],
    payoff: Callable[[RestoreSnapshot], Any],
    resolver: Callable[[RestoreSnapshot], Any],
) -> RestoreTraversalTrace:
    """Execute only the calls permitted by a checkpoint's fresh horizon."""

    callbacks = {
        "choice_commit": choice_commit,
        "reaction": reaction,
        "payoff": payoff,
        "resolver": resolver,
    }
    _validate_callbacks(callbacks)
    plan = build_restore_plan(snapshot)
    counts = _execute_restore_plan(plan, snapshot, callbacks)
    return RestoreTraversalTrace(plan.observation_window_id, *counts)


def _validate_callbacks(callbacks: dict[str, Any]) -> None:
    for name, callback in callbacks.items():
        if not callable(callback):
            raise TypeError("{} must be callable".format(name))


def _execute_restore_plan(
    plan: RestorePlan,
    snapshot: RestoreSnapshot,
    callbacks: dict[str, Callable[[RestoreSnapshot], Any]],
) -> tuple[int, int, int, int]:
    counts = [0, 0, 0, 0]
    permitted = (
        ("choice_commit", plan.choice_commit_calls),
        ("reaction", plan.reaction_calls),
        ("payoff", plan.payoff_calls),
        ("resolver", plan.resolver_calls),
    )
    for index, (name, call_count) in enumerate(permitted):
        if call_count:
            callbacks[name](snapshot)
            counts[index] = 1
    return tuple(counts)


def _validate_loaded_restore_session(session: LoadedRestoreSession) -> None:
    if type(session) is not LoadedRestoreSession:
        raise TypeError("session must be an exact LoadedRestoreSession")
    if type(session.snapshots) is not tuple or not session.snapshots:
        raise RestoreSemanticsError("snapshots must be a non-empty exact tuple")
    if any(type(snapshot) is not RestoreSnapshot for snapshot in session.snapshots):
        raise TypeError("snapshots must contain exact RestoreSnapshot values")
    if type(session.current_index) is not int or not 0 <= session.current_index < len(session.snapshots):
        raise RestoreSemanticsError("current_index is outside loaded history")
    for snapshot in session.snapshots:
        _validate_snapshot(snapshot)


def make_loaded_restore_session(
    snapshots: tuple[RestoreSnapshot, ...],
    current_index: int,
) -> LoadedRestoreSession:
    """Create a session whose rollback scope is only the loaded save history."""

    session = LoadedRestoreSession(snapshots, current_index)
    _validate_loaded_restore_session(session)
    return session


def rollback_loaded_save(
    session: LoadedRestoreSession,
    target_index: int,
) -> RollbackResult:
    """Rollback only inside loaded history and no-op safely when exhausted."""

    _validate_loaded_restore_session(session)
    if type(target_index) is not int:
        raise TypeError("target_index must be an exact int")
    current = session.snapshots[session.current_index]
    if target_index < 0 or target_index >= session.current_index:
        return RollbackResult(
            session,
            current,
            RestoreActionState(False, False, False),
            0,
        )
    restored_session = LoadedRestoreSession(session.snapshots, target_index)
    exhausted = target_index == 0
    return RollbackResult(
        restored_session,
        session.snapshots[target_index],
        RestoreActionState(not exhausted, not exhausted, not exhausted),
        1,
    )
