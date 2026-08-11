"""Pure SYS-SAVE request gates, UI affordances, and operation mutex.

Ren'Py adapters own live store and rollback state.  This module receives exact
transient facts, returns immutable results, and never queues rejected work.
"""

from dataclasses import dataclass
from typing import Any


PLAYABLE_STABLE = "PlayableStable"
MAIN_MENU = "MainMenu"
CRITICAL_INTERACTION = "CriticalInteraction"
LOAD_PREFLIGHT = "LoadPreflight"
LOADED_UNVALIDATED = "LoadedUnvalidated"
BLOCKING_SAFE_FLOW = "BlockingSafeFlow"
SAVING = "Saving"

PHASES = (
    PLAYABLE_STABLE,
    MAIN_MENU,
    CRITICAL_INTERACTION,
    LOAD_PREFLIGHT,
    LOADED_UNVALIDATED,
    BLOCKING_SAFE_FLOW,
    SAVING,
)

MANUAL_SAVE = "manual_save"
QUICK_SAVE = "quick_save"
AUTO_SAVE = "auto_save"
LOAD_SLOT = "load_slot"
QUICK_LOAD = "quick_load"
ROLLBACK = "rollback"

ACTIONS = (
    MANUAL_SAVE,
    QUICK_SAVE,
    AUTO_SAVE,
    LOAD_SLOT,
    QUICK_LOAD,
    ROLLBACK,
)
PLAYER_FACING_ACTIONS = (
    MANUAL_SAVE,
    QUICK_SAVE,
    LOAD_SLOT,
    QUICK_LOAD,
    ROLLBACK,
)

PLAYER_SOURCE = "player"
SHORTCUT_SOURCE = "shortcut"
SCRIPT_SOURCE = "script"
ALTERNATIVE_INPUT_SOURCE = "alternative_input"
AUTOSAVE_CYCLE_SOURCE = "autosave_cycle"

REQUEST_SOURCES = (
    PLAYER_SOURCE,
    SHORTCUT_SOURCE,
    SCRIPT_SOURCE,
    ALTERNATIVE_INPUT_SOURCE,
    AUTOSAVE_CYCLE_SOURCE,
)

LOAD_OPERATION = "load"
OPERATIONS = (
    MANUAL_SAVE,
    QUICK_SAVE,
    AUTO_SAVE,
    LOAD_OPERATION,
    ROLLBACK,
)

_ACTION_TO_OPERATION = {
    MANUAL_SAVE: MANUAL_SAVE,
    QUICK_SAVE: QUICK_SAVE,
    AUTO_SAVE: AUTO_SAVE,
    LOAD_SLOT: LOAD_OPERATION,
    QUICK_LOAD: LOAD_OPERATION,
    ROLLBACK: ROLLBACK,
}

_PLAYER_SOURCES = (
    PLAYER_SOURCE,
    SHORTCUT_SOURCE,
    SCRIPT_SOURCE,
    ALTERNATIVE_INPUT_SOURCE,
)
_ACTION_SOURCES = {
    MANUAL_SAVE: _PLAYER_SOURCES,
    QUICK_SAVE: _PLAYER_SOURCES,
    AUTO_SAVE: (AUTOSAVE_CYCLE_SOURCE,),
    LOAD_SLOT: _PLAYER_SOURCES,
    QUICK_LOAD: _PLAYER_SOURCES,
    ROLLBACK: _PLAYER_SOURCES,
}

_STABLE_ALLOWED = frozenset(ACTIONS)
_MAIN_MENU_ALLOWED = frozenset((LOAD_SLOT, QUICK_LOAD))


@dataclass(frozen=True, slots=True)
class RequestProfile:
    """Exact transient facts used by the engine request-permission contract."""

    request_enabled: bool
    location_registered: bool
    source: str


@dataclass(frozen=True, slots=True)
class UIActionProfile:
    """Exact player-facing UI flags plus their independent request profile."""

    request_profile: RequestProfile
    visible: bool
    enabled: bool
    focusable: bool


@dataclass(frozen=True, slots=True)
class OperationMutexState:
    """Transient ownership of the one canonical five-operation mutex."""

    active_operation: str | None


@dataclass(frozen=True, slots=True)
class ActionAdmissionResult:
    """Pure admission result; the adapter must publish state before invoking."""

    mutex_state: OperationMutexState
    queue_length: int
    admitted: bool


def make_request_profile(
    *,
    request_enabled: bool,
    location_registered: bool,
    source: str,
) -> RequestProfile:
    """Build a request profile; invalid values remain detectable by the gate."""

    return RequestProfile(request_enabled, location_registered, source)


def make_ui_action_profile(
    *,
    request_profile: RequestProfile,
    visible: bool,
    enabled: bool,
    focusable: bool,
) -> UIActionProfile:
    """Build UI gate facts without changing engine request permission."""

    return UIActionProfile(request_profile, visible, enabled, focusable)


def idle_operation_mutex() -> OperationMutexState:
    """Return a fresh idle mutex value for an engine-owned adapter field."""

    return OperationMutexState(None)


def registered_request_matrix() -> tuple[tuple[str, str, bool], ...]:
    """Return the complete nonempty GDD phase-by-action closed matrix."""

    rows = []
    for phase in PHASES:
        for action in ACTIONS:
            rows.append((phase, action, _phase_action_allowed(phase, action)))
    return tuple(rows)


def save_request_allowed(phase: Any, action: Any, profile: Any) -> bool:
    """Return exact engine permission, failing closed for every invalid input."""

    if type(phase) is not str or type(action) is not str:
        return False
    if phase not in PHASES or action not in ACTIONS:
        return False
    if not _request_profile_is_exact(profile):
        return False
    if profile.request_enabled is not True:
        return False
    if profile.source not in _ACTION_SOURCES[action]:
        return False
    if phase == PLAYABLE_STABLE and profile.location_registered is not True:
        return False
    return _phase_action_allowed(phase, action)


def ui_action_affordance(phase: Any, action: Any, profile: Any) -> bool:
    """Return whether one player action is visible, enabled, and focusable."""

    if type(phase) is not str or type(action) is not str:
        return False
    if phase not in PHASES or action not in PLAYER_FACING_ACTIONS:
        return False
    if not _ui_profile_is_exact(profile):
        return False
    if not save_request_allowed(phase, action, profile.request_profile):
        return False
    return (
        profile.visible is True
        and profile.enabled is True
        and profile.focusable is True
    )


def admit_action_request(
    mutex_state: Any,
    *,
    phase: Any,
    action: Any,
    request_profile: Any,
) -> ActionAdmissionResult:
    """Claim the mutex for one request without invoking or retaining work.

    An admitted caller must first publish ``result.mutex_state`` into its own
    transient Ren'Py adapter state, and only then invoke the engine action.
    This two-phase boundary closes callback-time reentrancy.  The caller later
    uses :func:`complete_operation` at the engine operation's terminal boundary.
    """

    if not _mutex_state_is_exact(mutex_state):
        return ActionAdmissionResult(idle_operation_mutex(), 0, False)
    if mutex_state.active_operation is not None:
        return ActionAdmissionResult(mutex_state, 0, False)
    if not save_request_allowed(phase, action, request_profile):
        return ActionAdmissionResult(mutex_state, 0, False)

    operation = _ACTION_TO_OPERATION[action]
    return ActionAdmissionResult(OperationMutexState(operation), 0, True)


def complete_operation(mutex_state: Any, operation: Any) -> OperationMutexState:
    """Release the active operation; rejected requests have nothing to replay."""

    if not _mutex_state_is_exact(mutex_state):
        return idle_operation_mutex()
    if type(operation) is not str or operation not in OPERATIONS:
        return mutex_state
    if mutex_state.active_operation != operation:
        return mutex_state
    return idle_operation_mutex()


def _phase_action_allowed(phase: str, action: str) -> bool:
    if phase == PLAYABLE_STABLE:
        return action in _STABLE_ALLOWED
    if phase == MAIN_MENU:
        return action in _MAIN_MENU_ALLOWED
    return False


def _request_profile_is_exact(profile: Any) -> bool:
    if type(profile) is not RequestProfile:
        return False
    try:
        request_enabled = profile.request_enabled
        location_registered = profile.location_registered
        source = profile.source
    except (AttributeError, TypeError):
        return False
    return (
        type(request_enabled) is bool
        and type(location_registered) is bool
        and type(source) is str
        and source in REQUEST_SOURCES
    )


def _ui_profile_is_exact(profile: Any) -> bool:
    if type(profile) is not UIActionProfile:
        return False
    try:
        request_profile = profile.request_profile
        visible = profile.visible
        enabled = profile.enabled
        focusable = profile.focusable
    except (AttributeError, TypeError):
        return False
    return (
        _request_profile_is_exact(request_profile)
        and type(visible) is bool
        and type(enabled) is bool
        and type(focusable) is bool
    )


def _mutex_state_is_exact(state: Any) -> bool:
    if type(state) is not OperationMutexState:
        return False
    try:
        active_operation = state.active_operation
    except (AttributeError, TypeError):
        return False
    return (
        active_operation is None
        or (
            type(active_operation) is str
            and active_operation in OPERATIONS
        )
    )
