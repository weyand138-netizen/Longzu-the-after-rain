# Story 024: Production End-to-End Orchestrator

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Complete
> **Layer**: Feature
> **Type**: Integration
> **Estimate**: 1 day
> **Last Updated**: 2026-08-14

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Requirement**: `TR-NAR-001` — The seven-day chapter paths and endings are
valid and content-locked.

**Governing ADRs**: ADR-0003, ADR-0006, ADR-0008
**Engine**: Ren'Py 8.5.3 | **Risk**: Medium

Production needs one runtime owner for the fixed chapter traversal. Each
chapter label remains independently callable for authored-source and route
validation tests. Existing SYS-CHOICE, SYS-ENDING, SYS-PERSIST, and player-copy
contracts are inputs to this control-flow change, not implementation scope.

## Acceptance Criteria

- [x] In a non-test Production run, `start` resets the run once and enters only
  `production_end_to_end_orchestrator`.
- [x] The Production orchestrator calls exactly this ordered chapter chain:
  `prologue_start`, Day 1 through Day 7 in canonical order; Day 7 remains the
  owner of the single `day7_resolve_ending` handoff and existing ending map.
- [x] The change adds no player choice, axis delta, token, resource,
  qualification, ending condition, player-facing copy, or persistence write;
  existing chapter labels remain independent entry points.
- [x] Static integration coverage and current Python/Ren'Py/lint evidence bind
  the exact source change and preserve the existing chapter/terminal tests.

## Out of Scope

Choice projections, axes, tokens, resources, qualifications, ending
predicates, ending labels/closures, player-facing copy, persistence semantics,
chapter prose, assets, and release/package work.

## QA Test Cases

- **AC-1/2:** Parse `start` and the Production orchestrator; assert one
  Production entry and the exact fixed call order.
- **AC-3:** Assert no semantic statements exist in the orchestrator, each
  chapter label remains present, and Day 7 retains the sole resolver handoff.
- **AC-4:** Run the focused Python test, full Python suite, pinned Ren'Py
  global suite, lint/compile, and content constraints.

## Test Evidence

- `tests/integration/sys_narrative/production_orchestrator_test.py`
- `production/qa/evidence/production-orchestrator-2026-08-14.md`

## Implementation Files

- `game/script.rpy`
- `game/production_orchestrator.rpy`
- `tests/integration/sys_narrative/production_orchestrator_test.py`

## Completion Notes

**Completed**: 2026-08-14
**Criteria**: 4/4 passing.
**Deviations**: None. Ren'Py's public `is_in_test()` guard only preserves the
existing independent chapter-test entry behavior; the non-test Production path
always enters the one fixed orchestrator.
**Test Evidence**:
`tests/integration/sys_narrative/production_orchestrator_test.py` and
`production/qa/evidence/production-orchestrator-2026-08-14.md`; full Python
281/281, Ren'Py global 56/56 with 474/474 assertions, lint/compile, content
constraints, and diff check pass.
**Code Review**: Approved — current implementation reviewed against
ADR-0003, ADR-0006, and ADR-0008.
