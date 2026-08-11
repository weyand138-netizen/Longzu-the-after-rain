# Story 008: Day 3 Asset Admission Records

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production  
> **Status**: Complete  
> **Layer**: Presentation  
> **Type**: Config/Data  
> **Estimate**: 1 day  
> **Manifest Version**: 2026-08-04.1  
> **Last Updated**: 2026-08-11

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`  
**Requirement**: `TR-NAR-008` — Day 3 runtime assets are provenance-admitted
with stable semantic paths and accessible bindings; missing or unregistered
assets are not admitted.

**Governing ADRs**: ADR-0003 (primary), ADR-0008  
**Engine**: Ren'Py 8.5.3 | **Risk**: Medium

**Engine Notes**: N/A — this is a records and runtime-reference audit; no new
engine API is introduced. Its verification is source/inventory consistency
validation plus the Day 3 engine route.

**Control Manifest Rules (Presentation layer)**:

- Required: use stable semantic asset names; register source and planned
  alternative text before admission.
- Forbidden: rely on hover, sound, animation, flashing, vibration, or timed
  input for meaning; admit official or source-unknown Dragon Raja assets.
- Performance: no runtime performance impact is expected because this story
  changes inventory/legal records only.

## Acceptance Criteria

- [ ] Audit every actual Day 3 runtime asset reference after Story 006 and
  register each admitted asset in `design/assets/entity-inventory.md` and
  `docs/legal/asset-register.md`.
- [ ] Each admitted asset has an asset ID, source/provenance, licence or
  permission basis, SHA-256, verified stable runtime path, and a planned
  self-voicing alternative-text or semantic binding.
- [ ] Code-defined Ren'Py assets name their owning source file and source hash;
  they are not represented as absent binary files.
- [ ] Planned, missing, generated, unregistered, or unused assets are marked
  not admitted and are not referenced at runtime.
- [ ] Do not introduce final character art, CGs, external images, audio, or
  video merely to fill Day 3.

## Implementation Notes

- Use ADR-0003 stable semantic asset names. Do not place mutable file paths
  throughout prose or make asset replacement alter local branching.
- An asset does not gain admission from intent alone: evidence must show its
  actual runtime reference and matching inventory/legal-register records.
- Alternative text and semantic bindings must preserve decision-relevant
  meaning without relying solely on colour, hover, sound, or motion.

## Out of Scope

- Day 3 narrative source and route evidence, owned by Stories 006 and 007.
- New final art/audio production, external asset sourcing, and all later-day
  asset production.

## QA Test Cases

- **AC-1: Runtime-reference admission consistency**
  - Given: Day 3 runtime references and the inventory/legal register.
  - When: the admission audit runs.
  - Then: each actual asset has exactly matching provenance, licence, hash,
    stable path, asset ID, and semantic-binding records.
  - Edge cases: absent provenance/licence/hash/path/ID/binding or a source-hash
    mismatch rejects admission.
- **AC-2: Non-admission and presentation boundary**
  - Given: planned, missing, generated, unused, and code-defined asset
    fixtures.
  - When: the inventory and runtime-reference checks run.
  - Then: only actual registered references are admitted; code-defined assets
    point to their owning source and all other fixtures remain unadmitted.
  - Edge cases: prose-embedded mutable path or unregistered runtime reference
    fails validation.

## Test Evidence

- Asset/inventory consistency validation for Day 3 runtime references
- `design/assets/entity-inventory.md`
- `docs/legal/asset-register.md`
- `production/qa/evidence/day3-asset-admission-check-<date>.md`

## Dependencies

- Depends on: Story 006.
- Unlocks: Story 007.

## Completion Notes

**Completed**: 2026-08-11  
**Criteria**: 5/5 passing.  
**Deviations**: None. Day 3 reuses three existing admitted runtime assets and
adds no asset identity, binary media, or external source.
**Test Evidence**: Runtime-reference and inventory/legal-register consistency
audit at `production/qa/evidence/day3-asset-admission-check-2026-08-11.md`.
The source/data gate found no Day 3 media-path reference; Story 007 remains
responsible for its engine presentation verification.
**Code Review**: Solo Config/Data audit; source, hashes, admission records,
and non-admission scope reviewed directly.
