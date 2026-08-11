"""Observable persistence recovery states and write-freeze policy."""

from dataclasses import dataclass


PERSISTENCE_SAFE_RECOVERY = "PERSISTENCE_SAFE_RECOVERY"
RESET_RECOVERY = "RESET_RECOVERY"
COMMIT_STATUS_UNKNOWN = "COMMIT_STATUS_UNKNOWN"


@dataclass(frozen=True)
class RecoveryState:
    """Recovery state presented to the UI and coordinator."""

    state: str
    writes_frozen: bool
    projection_allowed: bool
    feedback_allowed: bool


def classify_recovery(state: str) -> RecoveryState:
    """Map failure states without conflating safe recovery and unknown commit."""

    if state == PERSISTENCE_SAFE_RECOVERY:
        return RecoveryState(state, False, False, False)
    if state == RESET_RECOVERY:
        return RecoveryState(state, False, False, False)
    if state == COMMIT_STATUS_UNKNOWN:
        return RecoveryState(state, True, False, False)
    raise ValueError("unknown recovery state")


def can_accept_write(state: RecoveryState) -> bool:
    return state.writes_frozen is False
