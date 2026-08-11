"""SYS-TEST artifact lifecycle and criterion status truth tables."""

from dataclasses import dataclass
from typing import Any


UNBOUND = "UNBOUND"
BLOCKED_INPUT = "BLOCKED_INPUT"
RUNNING = "RUNNING"
PASSED_CURRENT = "PASSED_CURRENT"
STALE = "STALE"
REPORT_ONLY = "REPORT_ONLY"
ERROR = "ERROR"


@dataclass(frozen=True)
class ArtifactState:
    status: str
    criterion_status: str
    identity_generation: str | None


def start_artifact(*, manifest_present: bool, external_input_present: bool, generation: str | None) -> ArtifactState:
    if not manifest_present:
        return ArtifactState(UNBOUND, UNBOUND, None)
    if not external_input_present:
        return ArtifactState(BLOCKED_INPUT, BLOCKED_INPUT, generation)
    return ArtifactState(RUNNING, RUNNING, generation)


def finish_artifact(state: ArtifactState, *, passed: bool, current_generation: str | None) -> ArtifactState:
    if state.status in (UNBOUND, BLOCKED_INPUT):
        return state
    if state.identity_generation != current_generation:
        return ArtifactState(STALE, STALE, state.identity_generation)
    if not passed:
        return ArtifactState(ERROR, ERROR, state.identity_generation)
    return ArtifactState(PASSED_CURRENT, PASSED_CURRENT, state.identity_generation)


def gate_formula(*, lint: bool, pure: bool, engine: bool, static: bool, blocked_input: bool = False) -> str:
    if blocked_input:
        return BLOCKED_INPUT
    return "PASS" if all((lint, pure, engine, static)) else "FAIL"
