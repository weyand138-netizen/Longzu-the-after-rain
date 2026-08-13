# Story 001: Canonical Schema-2 Ending Resolution Record

> **Epic**: SYS-ENDING — Terminal Narrative Closure
> **Status**: Complete
> **Layer**: Core
> **Type**: Logic
> **Estimate**: 4 days
> **Last Updated**: 2026-08-13

## Context

**GDD**: `design/gdd/deterministic-ending-resolution.md`
**Requirements**: `TR-END-001`, `TR-END-003`
**Governing ADRs**: ADR-0001, ADR-0004, ADR-0005, ADR-0008
**Engine**: Ren'Py 8.5.3 / Python 3.12 | **Risk**: High

The current axes-only resolver is a partial legacy implementation. The frozen
contract requires one pure, schema-2 canonical record builder that validates a
detached axes/history snapshot, replays frozen choice projections, folds
counterevidence and route facts from ordered history, derives the four owned
qualifications, evaluates the fixed priority once, and emits immutable causes
and trace fields. `resolve_ending` remains only the one-call `.ending_id`
compatibility wrapper.

## Acceptance Criteria

- [x] `resolve_ending_record(snapshot)` accepts only a detached schema-2 exact
  axes/history shape; rejects live/malformed/unknown/inconsistent input before
  later folds and never owns mutable Ren'Py state.
- [x] Every supported choice ID has one frozen semantic projection. Replay uses
  the canonical cap rule and must exactly equal supplied axes; tokens, events,
  resources, and route qualifications derive only from ordered history.
- [x] Implement the nine frozen stages, priority
  `rain_stops -> her_own_name -> see_the_sea -> one_person_train -> golden_cage
  -> unsent_postcard`, fixed six predicates, and legal fail-closed behaviour.
- [x] Return the exact immutable `EndingResolutionRecord` shape and subordinate
  immutable trace/cause/audit records required by the entity registry; no
  presentation layer re-resolves or modifies its result.
- [x] `resolve_ending(snapshot)` calls the canonical function once and reads
  only `.ending_id`; pure tests cover the six canonical witnesses, cap/replay
  mismatch, revoke/repair ordering, qualification exclusivity, and malformed
  input.

## Out of Scope

Ren'Py lifecycle writes, label jumps, persistent completion, ending prose,
epilogue content, full terminal-manifest enumeration, journal/achievement work,
external assets, release work, and changes to frozen resolver policy.

## QA Test Cases

- **AC-1/2:** Unit tests use canonical histories and adversarial detached
  snapshots to prove replay/fold order and no live-state input.
- **AC-3/4:** Table-driven tests prove all six fixed endings, record field
  identity/immutability, causes, exclusions, and deterministic totality.
- **AC-5:** Static/pure tests observe exactly one wrapper canonical call and
  run the global Python and Ren'Py suites after the logical batch.

## Dependencies

- Depends on: approved SYS-STATE schema-2 envelope and frozen choice baseline.
- Unlocks: Stories 002 and 004; removes the implementation blocker from Sprint
  6 Story 020.

## Readiness Correction

The prior readiness block misread `witness_golden_cage_v1`. Its authoritative
ordered history contains only `day5_replace_erii_response`, not
`day5_honor_erii_response`. The frozen Day 5 sibling topology remains mutually
exclusive; replace remains a zero-axis revoke; and the declared final axes
remain `3/2/3/2/1`. This correction changes no GDD, projection, topology, or
golden-cage predicate.

## Completion Notes

**Completed**: 2026-08-13
**Criteria**: The immutable resolver catalog covers all 54 frozen choice IDs,
replays axes under the canonical cap rule, folds tokens/resources/events in
history order, derives mutually exclusive route qualifications, evaluates the
six fixed predicate trees, and builds exact immutable audit/trace/cause records.
The compatibility wrapper is statically verified as one canonical call plus one
`ending_id` read.

**Golden-vector correction**: With owner authorization, the obsolete
`axis_match_v1` digest that referenced retired choice IDs was regenerated from
the current authoritative `rain_stops` witness and synchronized in the active
GDD and entity registry. The fallback vector and all frozen ending predicates
remain unchanged.

**Test evidence**: Focused resolver suite 9/9; Python 246/246; pinned Ren'Py
global suite 45/45 testcases and 386/386 assertions; isolated `lint --compile`;
pinned-Python module compilation; and `git diff --check` all pass. Review:
`production/qa/evidence/sprint-007-s7-01-code-review-2026-08-13.md`.
