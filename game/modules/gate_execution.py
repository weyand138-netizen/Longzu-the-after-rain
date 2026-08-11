"""SYS-TEST FAST/INTEGRATION/RELEASE gate aggregation."""

from dataclasses import dataclass

from .artifact_lifecycle import BLOCKED_INPUT


@dataclass(frozen=True)
class GateResult:
    scope: str
    status: str
    executed_case_ids: tuple[str, ...]
    failures: tuple[str, ...]
    blocked_reasons: tuple[str, ...]


def execute_gate(scope: str, case_ids: tuple[str, ...], results: dict[str, str], *, required_inputs_present: bool = True, timeout: bool = False) -> GateResult:
    if scope not in ("FAST", "INTEGRATION", "RELEASE"):
        raise ValueError("unknown gate scope")
    if not required_inputs_present:
        return GateResult(scope, BLOCKED_INPUT, (), (), ("required current input missing",))
    if timeout:
        return GateResult(scope, "TIMEOUT/ERROR", case_ids, ("timeout",), ())
    failures = tuple(case_id for case_id in case_ids if results.get(case_id) != "PASS")
    return GateResult(scope, "PASS" if not failures else "FAIL", case_ids, failures, ())


def aggregate_release(component: GateResult, integration: GateResult, release: GateResult) -> str:
    if any(item.status == BLOCKED_INPUT for item in (component, integration, release)):
        return BLOCKED_INPUT
    return "PASS" if all(item.status == "PASS" for item in (component, integration, release)) else "FAIL"
