# Story 013: Day 5 Asset Admission Records

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Complete
> **Layer**: Presentation
> **Type**: Config/Data
> **Estimate**: 1 day
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-13

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Requirement**: `TR-NAR-013` — Day 5 runtime assets are provenance-admitted
with stable semantic paths and accessible bindings; missing or unregistered
assets are not admitted.

**Governing ADRs**: ADR-0003 (primary), ADR-0008
**Engine**: Ren'Py 8.5.3 | **Risk**: Medium

**Engine Notes**: This is a source/inventory/legal-record audit. It requires
no new engine API and is checked by source records and the Day 5 engine route.

**Control Manifest Rules (Presentation layer)**:

- Required: stable semantic aliases and source/semantic binding before
  admission; keyboard-readable presentation at 1280x720.
- Forbidden: an official/source-unknown asset or a meaning available only via
  hover, sound, animation, flashing, colour, or timed input.
- Performance: record-only work and existing code-defined primitives introduce
  no runtime memory or frame cost.

## Acceptance Criteria

- [ ] Audit every actual Day 5 runtime asset reference and register each
  admitted source in both `design/assets/entity-inventory.md` and
  `docs/legal/asset-register.md`.
- [ ] Every admission has an ID, provenance, licence/permission basis,
  SHA-256, stable runtime path, and self-voicing alternative-text or semantic
  binding.
- [ ] Code-defined assets identify their owning sources and hashes; intended,
  missing, generated, external, unregistered, or unused assets remain
  explicitly unadmitted and unreferenced.
- [ ] No final character art, CG, external image, audio, video, logo, font, or
  prop is added merely to decorate the family-archive chapter.

## Implementation Notes

- ADR-0003 requires semantic alias reuse so future replacement cannot rewrite
  Day 5 branching.
- Admission follows actual runtime references only. The chapter may reuse the
  admitted Source Han font, code-defined warm-room background, and shared
  choice surface; no planned asset is admitted by intent.

## Out of Scope

- Day 5 source/derivation, route evidence, and traceability, owned by Stories
  012, 014, and 015.
- New art/audio sourcing, external material, Day 6+, ending/epilogue, manifest,
  terminal, or release work.

## QA Test Cases

- **AC-1: Runtime-reference admission consistency**
  - Given: Day 5 runtime source and inventory/legal records.
  - When: all scene/show/play references and shared source hashes are audited.
  - Then: every actual reference has exactly matching provenance, licence, hash,
    stable path, ID, and semantic binding in both records.
  - Edge cases: missing field, stale shared-source hash, mutable prose path,
    duplicate record, or an unregistered runtime reference fails.
- **AC-2: Non-admission boundary**
  - Given: planned, missing, generated, unused, code-defined, and external
    asset fixtures.
  - When: admission assertions run.
  - Then: only actual admitted reusable sources pass; all other fixtures remain
    unadmitted and unavailable to Day 5.
  - Edge cases: a new final character image, CG, audio, video, or official/
    source-unknown material fails the audit.

## Test Evidence

- `tests/unit/sys_narrative/day5_asset_admission_test.py`
- `design/assets/entity-inventory.md`
- `docs/legal/asset-register.md`

## Dependencies

- Depends on: Story 012 is Complete.
- Unlocks: Story 014 and Story 015.

## Completion Notes

**Completed**: 2026-08-13
**Criteria**: 4/4 passing.
**Deviations**: None. Day 5 adds no asset identity and admits only actual reuse
of the already registered font, code-defined warm-room background, and shared
choice surface.
**Test Evidence**: `tests/unit/sys_narrative/day5_asset_admission_test.py` —
3/3 passing within the 22/22 focused Day 5 suite; inventory and legal register
contain the current source hashes and semantic bindings.
**Code Review**: Approved. Record-only changes preserve ADR-0003 semantic paths
and add no runtime dependency, external asset, or presentation-only meaning.
