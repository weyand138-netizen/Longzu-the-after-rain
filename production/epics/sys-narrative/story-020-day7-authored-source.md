# Story 020: Day 7 Authored Source and Resolver Handoff

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Complete
> **Layer**: Feature
> **Type**: Config/Data
> **Estimate**: 2 days
> **Last Updated**: 2026-08-14

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Requirement**: `TR-NAR-020` — Canonical Day 7 source presents the three
frozen acknowledgement scenes and hands off only through the owned terminal
resolver interface.

**Governing ADRs**: ADR-0003, ADR-0006, ADR-0008
**Engine**: Ren'Py 8.5.3 | **Risk**: High
**Manifest Version**: 2026-08-04.1

The normative source is `narrative_content_baseline:v1.2`. Day 7 is
`chapter_day7_before_red_well` with responsibility
`responsibility_day7_acknowledge_and_resolve`; its only required scenes are
`scene_day7_red_well_approach`, `scene_day7_causal_recall`, and
`scene_day7_ending_entry`.

## Acceptance Criteria

- [ ] Add exactly one Day 7 chapter unit with the three required scenes and no
  production choice record, axis delta, token repair/revoke, qualification
  mutation, route resource, or ending source fact.
- [ ] Make the causal-recall surface acknowledge only player-visible Day 1-6
  facts and preserve Erii's approved action/object expression boundary.
- [ ] Call the existing SYS-ENDING `day7_resolve_ending` entry exactly once at
  the ending-entry scene; the chapter does not import the resolver, select a
  label, mutate lifecycle or persistence, or call ending completion.
- [ ] Bind current source SHA-256 and player-safe chapter/memory inputs without
  exposing scores, tokens, qualifications, predicates, causes, or ending hints.

## Blocking Dependency

Resolved 2026-08-14: QA-approved Sprint 7 (`71fbfc5`) supplies the owned
`day7_resolve_ending` adapter, six stable labels, and ADR-0006 completion
boundary. This story may call the one owned handoff and may not duplicate it.

## Out of Scope

Six ending prose and completion, the true-ending epilogue, resolver predicate
or priority changes, qualification implementation, terminal-witness/full-
manifest expansion, external assets, release work, and stage changes.

## QA Test Cases

- **AC-1:** static source scan proves exact unit/scenes, zero new Day 7 choices
  or state-mutating source facts, and no hidden-score/player-facing leak.
- **AC-2:** engine flow reaches the owned handoff exactly once; `TypeError` and
  `ValueError` remain Active and enter no ending/persistence/journal path.

## Test Evidence

- Readiness: `production/qa/evidence/story-readiness-s6-01-2026-08-14.md`.
- Implementation and review evidence will bind the Day 7 source SHA-256, static
  source test, owned-handoff engine testcase, and the full suites.

## Dependencies

- Depends on: Sprint 5 approved and a complete SYS-ENDING terminal adapter.
- Unlocks: Stories 021-023 after source handoff is executable.

## Completion Notes

**Completed**: 2026-08-14
**Criteria**: 4/4 passing.
**Deviations**: None; the Sprint 7 dependency was delivered without a frozen
design, projection, topology, or ending-predicate change.
**Test Evidence**: `tests/unit/sys_narrative/day7_authored_source_test.py`,
`game/testcases.rpy`, and
`production/qa/evidence/day7-authored-source-evidence-2026-08-14.md`.
**Code Review**: Approved —
`production/qa/evidence/sprint-006-s6-01-code-review-2026-08-14.md`.
