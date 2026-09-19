# Story 018: Day 6 Route, Accessibility, and Evidence Validation

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Complete
> **Layer**: Feature
> **Type**: Integration
> **Estimate**: 2 days
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-13

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Requirement**: `TR-NAR-018` — Day 6 engine-route validation proves
conditional repair, cost reconsideration, mutually exclusive route commitment,
accessible presentation, and current source-hash evidence without Day 7 or
ending expansion.

**Governing ADRs**: ADR-0003 (primary), ADR-0008
**Engine**: Ren'Py 8.5.3 | **Risk**: High

## Acceptance Criteria

- [ ] Add deterministic engine and integration coverage for every legal backup,
  late-truth, direct cost, shifted-cost/reconsideration, and five-way guarded
  commitment/fallback partition; invalid facts expose no unauthorized action.
- [ ] Assert exact history, reactions, axes, tokens, contributor-aware repairs,
  resources, events, outcomes, commitment derivation record, active count,
  and Day 7 continuation seam without entering it.
- [ ] Capture cost and route-commitment surfaces at physical 1280x720
  keyboard-only silent/reduced-motion and 1.5x high-contrast/reduced-motion;
  focus is distinct, text unclipped, and quick menu has no focus target.
- [ ] Bind source/testcase/output/result/capture hashes into one evidence bundle
  and reject Day 1 partial-manifest, Day 7, terminal, ending, epilogue, or
  release scope.

## Out of Scope

- Day 6 source/asset/traceability records owned by Stories 016, 017, and 019;
  Day 7, terminal, ending, epilogue, resolver, qualification, release, UI
  redesign, and partial-manifest work.

## QA Test Cases

- **AC-1:** resource, repair, cost/reconsideration, and commitment route
  contracts; guards, outcomes, and scope failure cases.
- **AC-2:** keyboard focus, silence/reduced-motion and high-contrast semantic
  equivalence, captures, no quick-menu focus, and no clipped decision text.
- **AC-3:** evidence source/testcase/output/capture hashes and scope boundary.

## Test Evidence

- `tests/integration/sys_narrative/day6_content_validation_test.py`
- Engine routes and captures in `game/testcases.rpy`
- `production/qa/evidence/day6-content-validation-<date>-verified/`

## Dependencies

- Depends on: Stories 016 and 017 are Complete.
- Unlocks: Story 019 and Sprint 5 smoke/QA hand-off.

## Completion Notes

**Completed**: 2026-08-13
**Criteria**: 4/4 integration assertions plus the pinned global Ren'Py suite
pass. The final verified run records 45/45 testcases and 386/386 assertions,
including guarded partitions, invalid facts, keyboard traversal, and four
1280x720 captures.
**Deviations**: None. An intermediate evidence run is preserved separately; the
final verified run is authoritative after the source-order review correction.
**Test Evidence**: `tests/integration/sys_narrative/day6_content_validation_test.py`;
`production/qa/evidence/day6-content-validation-2026-08-13-final-verified/`.
**Code Review**: Approved. Commitment events are observed only after their
immediate player-visible reactions; no test weakens an acceptance criterion.
