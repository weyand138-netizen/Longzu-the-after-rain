"""Shared SYS-SAVE/SYS-PERSIST candidate and release evidence boundaries."""

import hashlib
from dataclasses import dataclass
from typing import Iterable

from .test_manifest import canonical_json, sha256_hex


@dataclass(frozen=True)
class CandidateManifest:
    candidate_identity: str
    identity_generation: str
    source_identity: str
    catalog_identity: str
    engine_capability_id: str
    build_mode: str
    build_run_id: str


@dataclass(frozen=True)
class ExclusionReport:
    test_only_findings: int
    production_to_test_only_edges: int
    network_findings: int
    telemetry_findings: int
    undeclared_findings: int
    unallowlisted_findings: int

    @property
    def clean(self) -> bool:
        return all(value == 0 for value in self.__dict__.values())


def candidate_identity(core: dict) -> str:
    """Hash identity-affecting inputs only; run IDs/timestamps are excluded by caller."""

    return sha256_hex(canonical_json(core))


def archive_hash(package_bytes: bytes) -> str:
    """Hash exact package bytes only, never the release directory."""

    if type(package_bytes) is not bytes:
        raise TypeError("package must be exact bytes")
    return hashlib.sha256(package_bytes).hexdigest()


def validate_exclusion_reports(staging: ExclusionReport, archive: ExclusionReport) -> bool:
    return staging.clean and archive.clean


def evidence_complete(*, candidate: CandidateManifest, evidence_candidate_identity: str, required_ids: Iterable[str], provided_ids: Iterable[str], generation: str) -> bool:
    return candidate.identity_generation == generation and candidate.candidate_identity == evidence_candidate_identity and set(required_ids) == set(provided_ids)


def reject_cross_generation(candidate_generation: str, evidence_generation: str) -> None:
    if candidate_generation != evidence_generation:
        raise ValueError("cross-generation evidence is rejected")
