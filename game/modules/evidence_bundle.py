"""SYS-TEST content-addressed evidence bundle and traceability index."""

from dataclasses import dataclass
from typing import Iterable

from .artifact_lifecycle import BLOCKED_INPUT, STALE
from .test_manifest import sha256_hex


@dataclass(frozen=True)
class EvidenceArtifact:
    artifact_id: str
    criterion_id: str
    generation: str
    source_hash: str
    catalog_hash: str
    fixture_hash: str
    runner_hash: str
    environment_hash: str
    raw_output_hash: str
    status: str


@dataclass(frozen=True)
class EvidenceBundle:
    candidate_identity: str
    generation: str
    artifacts: tuple[EvidenceArtifact, ...]


def build_evidence_bundle(candidate_identity: str, generation: str, artifacts: Iterable[EvidenceArtifact]) -> EvidenceBundle:
    values = tuple(artifacts)
    if not candidate_identity or not generation or not values:
        raise ValueError("bundle identity and artifacts are required")
    ids = [item.artifact_id for item in values]
    if len(ids) != len(set(ids)):
        raise ValueError("artifact IDs must be unique")
    if any(item.generation != generation for item in values):
        raise ValueError("cross-generation evidence is forbidden")
    hash_fields = ("source_hash", "catalog_hash", "fixture_hash", "runner_hash", "environment_hash", "raw_output_hash")
    if any(len(getattr(item, field)) != 64 for item in values for field in hash_fields):
        raise ValueError("all evidence inputs require SHA-256 hashes")
    return EvidenceBundle(candidate_identity, generation, values)


def bundle_status(bundle: EvidenceBundle, *, required_criterion_ids: Iterable[str]) -> str:
    required = set(required_criterion_ids)
    present = {item.criterion_id for item in bundle.artifacts if item.status == "PASS"}
    if any(item.status in (STALE, BLOCKED_INPUT) for item in bundle.artifacts) or not required.issubset(present):
        return BLOCKED_INPUT
    return "PASS"


def failure_summary(bundle: EvidenceBundle) -> tuple[dict[str, str], ...]:
    return tuple({"finding_id": f"FAIL-{item.artifact_id}", "criterion_id": item.criterion_id, "status": item.status} for item in bundle.artifacts if item.status != "PASS")


def traceability_index(bundle: EvidenceBundle) -> dict[str, tuple[str, ...]]:
    result: dict[str, list[str]] = {}
    for item in bundle.artifacts:
        result.setdefault(item.criterion_id, []).append(item.artifact_id)
    return {criterion: tuple(sorted(ids)) for criterion, ids in sorted(result.items())}
