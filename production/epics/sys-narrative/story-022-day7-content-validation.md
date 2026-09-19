# Story 022: Day 7 Handoff, Accessibility, and Evidence Validation

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Complete
> **Layer**: Feature
> **Type**: Integration
> **Estimate**: 2 days
> **Last Updated**: 2026-08-14

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Requirement**: `TR-NAR-022` — Day 7 route and accessibility evidence proves
zero Day 7 state creation, one owned ending handoff, and failure-closed flow.

**Governing ADRs**: ADR-0003, ADR-0006, ADR-0008
**Engine**: Ren'Py 8.5.3 | **Risk**: High
**Manifest Version**: 2026-08-04.1

## Acceptance Criteria

- [x] Exercise all six canonical Day 1-6 histories through Day 7; each reaches
  its required scenes, preserves the exact prior snapshot/history, and calls
  the owned terminal handoff once.
- [x] Prove Day 7 has zero axis, token, qualification, route-resource,
  persistence, achievement, and journal mutations before terminal ownership
  accepts the handoff.
- [x] Inject resolver `TypeError` and `ValueError`; the flow remains Active,
  enters no label, and writes no persistent/achievement/journal result.
- [x] Capture the causal-recall surface at 1280x720 keyboard-only
  silent/reduced-motion and 1.5x high-contrast/reduced-motion; require
  readable, focused, keyboard-operable text without quick-menu focus.

## Blocking Dependency

Stories 020 and 021 plus the owned executable SYS-ENDING adapter/labels are
required. This story must not supply a test-only terminal substitute.

## Test Evidence

- Six canonical-history tests, real Ren'Py handoff testcases, failure-closure
  tests, accessibility captures, and the full-suite logs will be bound here.

## Objective Completion Notes (2026-08-14)

- `tests/integration/sys_narrative/day7_content_validation_test.py` validates
  all six frozen witnesses against
  `design/narrative/seven-day-content-baseline.md`, including the replace-only
  Golden Cage history and its `3/2/3/2/1` vector. The real Ren'Py routes each
  history through the one owned `day7_resolve_ending` handoff without a
  Day 7-local terminal double.
- The malformed-state testcase calls `prepare_day7_ending_jump()` directly and
  proves `TypeError`/`ValueError` preserve active lifecycle state, no pending
  target or completion event, and empty persistence/achievement/seen/memory
  collections. The production label routes such failure only to its restart
  safe boundary.
- Objective visual capture, dimensions, hash binding, keyboard traversal,
  silent self-voicing, high-contrast/font settings, reduced-motion settings,
  and no quick-menu focus all pass. See
  `production/qa/evidence/day7-content-validation-2026-08-14-verified/`.
- Owner narrative/readability/visual-feel signoff: **Approved by Andwey in the
  active Codex task on 2026-08-14**.

## Out of Scope

Six ending content validation, epilogue validation, resolver semantics,
qualification enumeration, full-manifest work, external assets, release, and
stage changes.

## Completion Notes

**Completed**: 2026-08-14
**Criteria**: 4/4 passing. Six real handoffs, zero Day 7-local mutations,
`TypeError`/`ValueError` failure closure, and both accessibility baselines are
covered by automated evidence plus owner visual/readability approval.
**Deviations**: None. Frozen choice projection, topology, ending predicates,
and Golden Cage's replace-only witness are unchanged.
**Test Evidence**:
`tests/integration/sys_narrative/day7_content_validation_test.py` and
`production/qa/evidence/day7-content-validation-2026-08-14-verified/`.
**Code Review**: Complete —
`production/qa/evidence/sprint-006-s6-03-code-review-2026-08-14.md`.
