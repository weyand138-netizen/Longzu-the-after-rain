"""SYS-TEST external human/visual/playtest evidence adjudication."""

from dataclasses import dataclass

from .test_manifest import sha256_hex


@dataclass(frozen=True)
class ExternalEvidence:
    evidence_id: str
    evidence_type: str
    rubric_id: str
    reviewer_id: str
    environment_id: str
    raw_response_hash: str
    adjudication: str | None
    approved: bool
    test_only: bool


def validate_external_evidence(evidence: ExternalEvidence) -> bool:
    if type(evidence) is not ExternalEvidence or evidence.evidence_type not in ("HUMAN", "PLAYTEST", "VISUAL", "REVIEW"):
        return False
    if not all((evidence.evidence_id, evidence.rubric_id, evidence.reviewer_id, evidence.environment_id, evidence.raw_response_hash)):
        return False
    return evidence.test_only is False and evidence.raw_response_hash == evidence.raw_response_hash.lower() and len(evidence.raw_response_hash) == 64


def adjudicated_pass(evidence: ExternalEvidence) -> bool:
    return validate_external_evidence(evidence) and evidence.approved is True and evidence.adjudication == "PASS"


def external_criterion_status(evidence: ExternalEvidence | None) -> str:
    return "PASS" if evidence is not None and adjudicated_pass(evidence) else "BLOCKED_INPUT"
