"""SYS-JOURNAL entry and recovery preemption gate."""

from dataclasses import dataclass


@dataclass(frozen=True)
class JournalGateState:
    visible: bool
    enabled: bool
    focusable: bool
    recovery_active: bool
    entry_count: int


def journal_gate(*, blocked: bool, recovery_active: bool, caller_context_safe: bool, entry_count: int = 1) -> JournalGateState:
    """Expose Journal only at a safe boundary and never during recovery."""

    allowed = not blocked and not recovery_active and caller_context_safe
    return JournalGateState(allowed, allowed, allowed, recovery_active, entry_count if allowed else 0)


def recovery_preempts_journal(state: JournalGateState) -> bool:
    return state.recovery_active and not state.visible and not state.enabled and not state.focusable
