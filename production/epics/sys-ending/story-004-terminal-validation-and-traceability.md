# Story 004: Terminal Validation and Traceability

> **Epic**: SYS-ENDING — Terminal Narrative Closure
> **Status**: Complete
> **Layer**: Core
> **Type**: Integration
> **Estimate**: 1 day
> **Last Updated**: 2026-08-13

## Context

**GDD**: `design/gdd/deterministic-ending-resolution.md`
**Requirement**: `TR-END-006`
**Governing ADRs**: ADR-0004, ADR-0006, ADR-0008
**Engine**: Ren'Py 8.5.3 | **Risk**: High

The terminal batch is complete only when its stories, source, tests, smoke
evidence, QA sign-off, and status records identify one verified generation.
This story verifies actual contracts and must not manufacture a full-manifest,
release, or stage claim.

## Acceptance Criteria

- [x] Traceability links all six ending contracts, Stories 001-003, test
  evidence, code review, smoke, and team QA; statuses agree with facts.
- [x] Verify current `game/` runtime sources, immutable resolver/record
  contracts, lifecycle/completion callsites, six labels, and rain-only epilogue
  without creating an empty `src/` directory.
- [x] Run full Python, global Ren'Py, lint/compile, content constraints, and
  focused terminal suites. Record exact commands/results and fail honestly on
  missing proof.
- [x] Explicitly exclude Day 7 content QA, full terminal enumeration, release,
  package, and stage promotion from this sprint sign-off.

## Out of Scope

Production gate advancement and all missing future-stage evidence.

## QA Test Cases

- **AC-1/2:** Repository tests verify every claimed artifact and source
  callsite; status/trace links must be bidirectionally consistent.
- **AC-3/4:** Smoke and team QA reports reproduce the complete automated
  evidence and retain all disclosed exclusions.

## Dependencies

- Depends on: Stories 001-003.
- Unlocks: Sprint 7 QA decision and re-running Sprint 6 story readiness.

## Readiness Evidence

**Verdict**: READY (2026-08-13). Stories 001-003 are complete with focused
pure/source tests, code-review records, full Python and global Ren'Py evidence.
The remaining work is a bounded consistency check and an honest Sprint 7
evidence record. It must retain the explicit exclusions for Day 7 content QA,
full terminal enumeration, release/package, and production-stage promotion.
See `production/qa/evidence/story-readiness-s7-04-2026-08-13.md`.

## Completion Notes

**Completed**: 2026-08-13
**Criteria**: The terminal traceability test binds the six delivered terminal
requirements, Stories 001-003, exact current source identities, focused and
full test evidence, reviews, smoke, and QA record locations. It rejects a
fabricated `src/` root and retains all excluded scope.

**Test evidence**: Focused terminal traceability suite 15/15. Final full
Python/global Ren'Py/lint/constraints/smoke results are recorded in
`production/qa/smoke-sprint-007-2026-08-13.md`; team QA record remains the
required final Sprint 7 decision artifact.
