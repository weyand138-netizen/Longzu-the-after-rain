# Story 023: Day 7 Story and Evidence Traceability

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Complete
> **Layer**: Feature
> **Type**: Config/Data
> **Estimate**: 1 day
> **Last Updated**: 2026-08-14

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Requirement**: `TR-NAR-023` — Day 7 stories, source, assets, terminal-
handoff tests, evidence, review, smoke, and QA identify one verified generation.

**Governing ADRs**: ADR-0003, ADR-0006, ADR-0008
**Engine**: Ren'Py 8.5.3 | **Risk**: Medium
**Manifest Version**: 2026-08-04.1

## Acceptance Criteria

- [x] Create a link matrix for Stories 020-022, Day 7 source hash, asset/legal
  records, terminal handoff tests, captures, code review, smoke, and QA sign-
  off.
- [x] Verify Epic, story, and sprint status agree without claiming six ending,
  epilogue, full-manifest, release, or stage delivery.
- [x] Explicitly state the Ren'Py implementation root is `game/`; no empty
  `src/` directory is created to manufacture gate compliance.

## Blocking Dependency

Stories 020-022 must be Complete. The traceability record cannot make a
blocked terminal handoff appear verified.

## Test Evidence

- `tests/integration/sys_narrative/day7_traceability_test.py` verifies the
  final matrix links and that `game/` is the Ren'Py runtime implementation
  root; no empty `src/` directory is used.
- `production/qa/evidence/day7-traceability-2026-08-14.md` holds the final
  generation matrix. Its smoke and QA rows are written only after those actual
  close-out records exist.

## QA Test Cases

- **AC-1:** reject a missing, stale, or inconsistent Day 7 source/test/evidence
  link, including the frozen replace-only Golden Cage generation identity.
- **AC-2:** require all four Story/Epic/sprint records and actual smoke/QA
  records to agree only after Sprint 6 QA has approved them.
- **AC-3:** reject a manufactured `src/` runtime claim or any ending, epilogue,
  full-manifest, release, or stage-delivery assertion.

## Completion Notes

**Completed**: 2026-08-14
**Criteria**: 3/3 passing. The final matrix binds the exact Day 7 source hash,
all Story 020-023 records, asset/source/test/evidence/review files, actual
smoke, evidence review, and solo QA approval.
**Deviations**: None. No endpoint, ending, epilogue, full-manifest, release,
or stage claim was added.
**Test Evidence**:
`tests/integration/sys_narrative/day7_traceability_test.py` and
`production/qa/evidence/day7-traceability-2026-08-14.md`.
**Code Review**: Complete —
`production/qa/evidence/sprint-006-s6-04-code-review-2026-08-14.md`.
