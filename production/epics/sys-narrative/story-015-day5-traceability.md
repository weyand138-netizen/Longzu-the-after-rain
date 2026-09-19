# Story 015: Day 5 Story and Evidence Traceability

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Complete
> **Layer**: Feature
> **Type**: Config/Data
> **Estimate**: 1 day
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-13

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Requirement**: `TR-NAR-015` — Day 5 story, source, asset, test, and QA
records identify one verified content generation and do not claim Day 6+,
terminal, ending, or release delivery.

**Governing ADRs**: ADR-0003, ADR-0008
**Engine**: Ren'Py 8.5.3 | **Risk**: Medium

**Engine Notes**: No engine API is introduced. Traceability is a build/test-time
record audit over the production `game/` runtime root, not an empty `src/`
directory convention.

**Control Manifest Rules (Feature layer)**:

- Required: preserve source ownership and source-hash evidence for every
  production record; source checks remain build/test-time only.
- Forbidden: an orphaned story/test/evidence link, a partial-manifest expansion,
  production-to-test leak, terminal/ending ownership claim, or hidden-state copy.
- Performance: traceability has no runtime work.

## Acceptance Criteria

- [ ] Create a Day 5 link matrix binding Stories 012–014, the source hash,
  route-answer derivation, inventory/legal records, tests, evidence bundle,
  QA plan, smoke report, and QA sign-off to one generation.
- [ ] Verify the EPIC and `sprint-status.yaml` statuses agree with story files
  and do not report missing work as complete or complete work as Ready.
- [ ] State the runtime convention explicitly: this Ren'Py project's active
  implementation root is `game/`, so no empty `src/` directory is created to
  manufacture gate compliance.
- [ ] Keep the record Day 5-only. It must not claim Day 6+, terminal witnesses,
  ending, epilogue, release, or partial-manifest delivery.

## Implementation Notes

- Traceability references source/test/evidence paths but does not rewrite their
  content. A stale or absent hash/link is a failure, not a reason to infer PASS.

## Out of Scope

- All runtime code, assets, Day 6+, terminal, ending, epilogue, release, and
  gate stage changes.

## QA Test Cases

- **AC-1: Matrix integrity**
  - Given: all Day 5 source, story, record, test, and evidence paths.
  - When: the traceability audit reads their IDs and hashes.
  - Then: every completed record identifies one generation and no required link
    is missing.
  - Edge cases: stale source hash, missing story/test/evidence, mismatched status,
    or an unrelated generation fails.
- **AC-2: Scope and runtime-root boundary**
  - Given: the matrix prose and current project layout.
  - When: scope and implementation-root assertions run.
  - Then: it documents `game/` and rejects Day 6+, terminal, ending, epilogue,
    release, partial-manifest, or empty-`src/` compliance claims.

## Test Evidence

- `production/qa/evidence/day5-traceability-2026-08-13.md`
- `tests/integration/sys_narrative/day5_traceability_test.py`
- Sprint 4 smoke and QA hand-off artifacts

## Dependencies

- Depends on: Stories 012–014 are Complete.
- Unlocks: Sprint 4 close-out.

## Completion Notes

**Completed**: 2026-08-13
**Criteria**: 4/4 accepted. The matrix binds source generation, stories,
admitted assets, automated route/accessibility evidence, code review, smoke,
and QA hand-off; it explicitly records `game/` as the runtime root and never
creates an empty `src/` directory.
**Deviations**: None. The required solo human narrative/readability review is
recorded in the approved Sprint 4 QA sign-off.
**Test Evidence**: traceability test 4/4; final Python suite 223/223; pinned
Ren'Py global suite 37/37 testcases and 345/345 assertions.
**Code Review**: Approved for objective QA hand-off; no code defect remains open.
