# Story 019: Day 6 Story and Evidence Traceability

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Complete
> **Layer**: Feature
> **Type**: Config/Data
> **Estimate**: 1 day
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-13

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Requirement**: `TR-NAR-019` — Day 6 story, source, asset, test, and QA
evidence records identify one verified content generation and do not claim Day
7, terminal, ending, epilogue, or release work.

**Governing ADRs**: ADR-0003, ADR-0008
**Engine**: Ren'Py 8.5.3 | **Risk**: Medium

## Acceptance Criteria

- [ ] Create a Day 6 link matrix binding Stories 016–018, source hash,
  commitment derivation, inventory/legal records, tests, evidence, QA plan,
  code review, smoke report, and QA sign-off to one generation.
- [ ] Verify Epic, story, and `sprint-status.yaml` states agree without
  reporting unavailable Day 7 or QA work as complete.
- [ ] State the Ren'Py runtime convention: implementation root is `game/`, so
  no empty `src/` directory is created to manufacture compliance.
- [ ] Keep the record Day 6-only and reject Day 7, terminal, ending, epilogue,
  release, or partial-manifest claims.

## Out of Scope

- All Day 6 runtime source/assets, Day 7+, terminal, ending, epilogue, release,
  and stage changes.

## QA Test Cases

- **AC-1:** matrix links, hashes, records, and current statuses are complete
  and mutually consistent; stale/missing/mismatched paths fail.
- **AC-2:** runtime-root and Day 6-only boundary are explicit and enforceable.

## Test Evidence

- `production/qa/evidence/day6-traceability-<date>.md`
- `tests/integration/sys_narrative/day6_traceability_test.py`

## Dependencies

- Depends on: Stories 016–018 are Complete.
- Unlocks: Sprint 5 close-out.
