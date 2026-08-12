# Story 011: Day 4 Asset Admission Records

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Complete
> **Layer**: Presentation
> **Type**: Config/Data
> **Estimate**: 1 day
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-11

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Requirement**: `TR-NAR-011` — Day 4 runtime assets are provenance-admitted
with stable semantic paths and accessible bindings; missing or unregistered
assets are not admitted.

**Governing ADRs**: ADR-0003 (primary), ADR-0008
**Engine**: Ren'Py 8.5.3 | **Risk**: Medium

**Engine Notes**: N/A — this is a records and runtime-reference audit; it uses
source/inventory consistency checks and the Day 4 engine route, not a new API.

**Control Manifest Rules (Presentation layer)**:

- Required: use stable semantic asset names; register source and planned
  alternative text before admission.
- Forbidden: rely on hover, sound, animation, flashing, vibration, or timed
  input for meaning; admit official or source-unknown Dragon Raja assets.
- Performance: no runtime performance impact is expected because this changes
  inventory/legal records only.

## Acceptance Criteria

- [x] Audit every actual Day 4 runtime asset reference and register each
  admitted asset in `design/assets/entity-inventory.md` and
  `docs/legal/asset-register.md`.
- [x] Every admitted asset has an ID, provenance, licence/permission basis,
  SHA-256, stable runtime path, and self-voicing alternative-text or semantic
  binding.
- [x] Code-defined Ren'Py assets identify their owning source and hash; planned,
  missing, generated, unregistered, or unused assets remain unadmitted and are
  not referenced at runtime.
- [x] No final character art, CG, external image, audio, or video was added only
  to fill Day 4.

## Implementation Notes

- Apply ADR-0003 stable semantic names; asset replacement must not alter local
  branching.
- Admission requires an actual runtime reference plus matching inventory and
  legal-register records; intent alone is insufficient.

## Out of Scope

- Day 4 narrative source and route evidence, owned by Stories 009 and 010.
- New final art/audio production, external sourcing, and later-day assets.

## QA Test Cases

- **AC-1: Runtime-reference admission consistency**
  - Given: Day 4 runtime references and the inventory/legal register.
  - When: the admission audit runs.
  - Then: every actual asset has matching provenance, licence, hash, stable
    path, ID, and semantic-binding records.
  - Edge cases: missing provenance/licence/hash/path/ID/binding or a source-hash
    mismatch rejects admission.
- **AC-2: Non-admission and presentation boundary**
  - Given: planned, missing, generated, unused, and code-defined asset fixtures.
  - When: inventory and runtime-reference checks run.
  - Then: only actual registered references are admitted and all other fixtures
    remain unadmitted.
  - Edge cases: prose-embedded mutable path or unregistered runtime reference
    fails validation.

## Test Evidence

- `tests/unit/sys_narrative/day4_asset_admission_test.py`
- `design/assets/entity-inventory.md`
- `docs/legal/asset-register.md`
- `production/qa/evidence/day4-authored-source-evidence.md`

## Dependencies

- Depends on: Story 009.
- Unlocks: Story 010.

## Completion Notes

**Completed**: 2026-08-11.
**Evidence**: `tests/unit/sys_narrative/day4_asset_admission_test.py` reports
3/3 passing; inventory and legal-register records have been updated.
