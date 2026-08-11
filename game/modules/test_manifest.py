"""SYS-TEST frozen manifest and canonical identity helpers."""

import hashlib
import json
import math
from dataclasses import dataclass
from typing import Any, Iterable


EVIDENCE_TYPES = frozenset(("UT_ENGINE", "UT_PURE", "INSTR", "STATIC", "BRANCH", "A11Y", "VISUAL", "BENCH", "HUMAN", "PLAYTEST", "REVIEW"))


class TestManifestError(ValueError):
    """Raised for duplicate, non-canonical, or incomplete test manifests."""


def _identity_safe(value: Any) -> Any:
    if value is None or type(value) is bool or type(value) is int or type(value) is str:
        return value
    if type(value) is float:
        raise TestManifestError("floats are forbidden in identity inputs")
    if type(value) is list:
        return [_identity_safe(item) for item in value]
    if type(value) is dict:
        if len(value) != len(set(value)) or any(type(key) is not str for key in value):
            raise TestManifestError("identity object keys must be unique exact strings")
        return {key: _identity_safe(value[key]) for key in sorted(value)}
    raise TestManifestError("identity input contains an unsupported type")


def canonical_json(value: Any) -> bytes:
    """Encode identity data as UTF-8 canonical JSON bytes."""

    safe = _identity_safe(value)
    return json.dumps(safe, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def sha256_hex(value: bytes | Any) -> str:
    raw = value if type(value) is bytes else canonical_json(value)
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class CriterionRecord:
    criterion_id: str
    owner_system: str
    evidence_type: str
    scope: str
    case_ids: tuple[str, ...]
    artifact_ids: tuple[str, ...]


def validate_criterion_records(records: Iterable[CriterionRecord]) -> tuple[CriterionRecord, ...]:
    values = tuple(records)
    ids = [record.criterion_id for record in values]
    if len(ids) != len(set(ids)) or any(type(record) is not CriterionRecord for record in values):
        raise TestManifestError("criterion IDs must be unique and exact")
    for record in values:
        if not record.criterion_id or not record.owner_system or record.evidence_type not in EVIDENCE_TYPES or not record.scope or not record.case_ids or not record.artifact_ids:
            raise TestManifestError("criterion records cannot be empty")
        if len(record.case_ids) != len(set(record.case_ids)) or len(record.artifact_ids) != len(set(record.artifact_ids)):
            raise TestManifestError("case and artifact IDs must be unique")
    return values


def build_test_framework_manifest(records: Iterable[CriterionRecord], *, runner_id: str, generation: str) -> dict[str, Any]:
    """Build owner-traceable manifest without duplicating product semantics."""

    frozen = validate_criterion_records(records)
    if type(runner_id) is not str or not runner_id or type(generation) is not str or not generation:
        raise TypeError("runner_id and generation must be non-empty strings")
    return {"schema": "test_framework_manifest:v1", "generation": generation, "runner_id": runner_id, "criteria": [record.__dict__ for record in frozen]}
