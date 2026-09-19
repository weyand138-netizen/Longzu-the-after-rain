# Story 017: Day 6 Asset Admission Records

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Complete
> **Layer**: Presentation
> **Type**: Config/Data
> **Estimate**: 1 day
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-13

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Requirement**: `TR-NAR-017` — Day 6 runtime assets are provenance-admitted
with stable semantic paths and accessible bindings; missing or unregistered
assets are not admitted.

**Governing ADRs**: ADR-0003 (primary), ADR-0008
**Engine**: Ren'Py 8.5.3 | **Risk**: Medium

## Acceptance Criteria

- [ ] Audit every actual Day 6 runtime asset reference in inventory and legal
  records with stable path, provenance, licence/permission basis, SHA-256, and
  semantic/self-voicing binding.
- [ ] Keep code-defined assets tied to their source hashes; admit no intended,
  missing, generated, external, official/source-unknown, or unused asset.
- [ ] Do not add final character art, CG, image, audio, video, logo, font, or
  prop merely to decorate the safehouse chapter.

## Out of Scope

- Day 6 source/derivation, route evidence, and traceability, owned by Stories
  016, 018, and 019; all Day 7+, ending, epilogue, manifest, and release work.

## QA Test Cases

- **AC-1:** every runtime reference has one matching record in inventory and
  legal registers; stale/missing/duplicate records fail.
- **AC-2:** planned, missing, generated, external, and unused fixtures remain
  unadmitted; any new final/official asset fails.

## Test Evidence

- `tests/unit/sys_narrative/day6_asset_admission_test.py`
- `design/assets/entity-inventory.md`
- `docs/legal/asset-register.md`

## Dependencies

- Depends on: Story 016 is Complete.
- Unlocks: Stories 018 and 019.

## Completion Notes

**Completed**: 2026-08-13
**Criteria**: 3/3 asset-admission assertions pass. Day 6 admits only existing
font, code-defined warm-room, and shared choice-surface references with current
source hashes and semantic bindings.
**Deviations**: None. No binary, external, planned, generated, official, or
unused asset was added.
**Test Evidence**: `tests/unit/sys_narrative/day6_asset_admission_test.py`;
`design/assets/entity-inventory.md`; `docs/legal/asset-register.md`.
**Code Review**: Approved. The shared screen update is hash-synchronized across
all reuse records and adds Day 6 keyboard underline semantics only.
