"""Classification boundary for Sprint 013 preflight and Production RC closeout.

The ordinary regression suite validates this module's classification contract.
It does not promote missing human, legal, performance, or archive evidence.
The explicit closeout runner is the only caller that turns these classifications
into a non-PASS gate result.
"""

from __future__ import annotations

from dataclasses import dataclass


PASS = "PASS"
BLOCKED_INPUT = "BLOCKED_INPUT"
REPORT_ONLY = "REPORT_ONLY"


@dataclass(frozen=True)
class ExternalEvidence:
    """Evidence state consumed by the preflight/closeout boundary."""

    name: str
    present: bool
    report_only: bool = False


def classify_external_evidence(evidence: ExternalEvidence) -> str:
    """Return the honest status without making ordinary tests fail.

    Missing required inputs are BLOCKED_INPUT. Measurements that are valid as a
    protocol/report but lack approved runtime samples are REPORT_ONLY.
    """

    if type(evidence) is not ExternalEvidence:
        raise TypeError("evidence must be an ExternalEvidence record")
    if evidence.present:
        return PASS
    return REPORT_ONLY if evidence.report_only else BLOCKED_INPUT


def final_gate_status(evidence: tuple[ExternalEvidence, ...]) -> str:
    """Aggregate a final Production closeout gate, fail-closed."""

    statuses = tuple(classify_external_evidence(item) for item in evidence)
    if BLOCKED_INPUT in statuses:
        return BLOCKED_INPUT
    if REPORT_ONLY in statuses:
        return REPORT_ONLY
    return PASS


__all__ = [
    "BLOCKED_INPUT",
    "ExternalEvidence",
    "PASS",
    "REPORT_ONLY",
    "classify_external_evidence",
    "final_gate_status",
]
