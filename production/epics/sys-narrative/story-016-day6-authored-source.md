# Story 016: Day 6 Authored Source and Guarded Route Commitment

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Complete
> **Layer**: Feature
> **Type**: Config/Data
> **Estimate**: 4 days
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-13

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Requirement**: `TR-NAR-016` — Canonical Day 6 source declares the safehouse
failure scenes, exact resource/cost/commitment choice bindings, and one guarded
route commitment or fallback without entering Day 7 or ending scope.

**Governing ADRs**: ADR-0008 (primary), ADR-0003, ADR-0006 (boundary only)
**Engine**: Ren'Py 8.5.3 | **Risk**: High

**Normative source**: `design/narrative/seven-day-content-baseline.md`,
`narrative_content_baseline:v1.2`, Day 6 topology, agency table,
counterevidence catalog, route qualification bindings, and achievement event
catalog. This story consumes those frozen facts; it must not redefine them.

## Acceptance Criteria

- [ ] Add `game/chapters/day6.rpy` with exactly `chapter_day6_no_safe_house`,
  `scene_day6_safehouse_failure`, `scene_day6_backup_exit`,
  `scene_day6_cost_inventory`, and `scene_day6_route_commitment`.
- [ ] Declare only the fifteen approved Day 6 choice/reaction/payoff records
  and implement their frozen axes, resource/event effects, revocations,
  repairs, immediate reactions, and later payoff identities.
- [ ] Implement the exact conditional backup node: reopen/keep only for a
  discovered exit plus unresolved backup token; keep-only when the token is
  unresolved but no exit exists; use/abandon when the exit exists without that
  token; no fabricated resource or repair option.
- [ ] Implement late-truth and cost nodes with exact preconditions. The cost
  reconsideration response appears only after shift, visible consequence,
  renewed request/answer, and refusal; take-back retains the frozen residual
  outcome while repairing only `token_shift_promised_cost`.
- [ ] Implement a pure, closed Day 6 commitment derivation from allowed Day 5
  answer/outcome plus resource/event/token facts. It selects exactly one of
  independent contact, shared escape, solo departure, old-order return, or no
  executable route; malformed/contradictory facts fail closed before any
  commitment choice is exposed.
- [ ] Record only Day 6 commitment facts/events/outcomes. Do not write a route
  qualification, call the resolver, enter/complete an ending, grant persistence,
  create a terminal witness, or branch to Day 7.
- [ ] Bind the current source SHA-256 and player-safe chapter/memory catalog
  inputs to evidence. Player-visible content excludes hidden state, full Erii
  dialogue, partial-manifest, Day 7, terminal, ending, epilogue, and release
  claims.

## Implementation Notes

- ADR-0003 keeps prose/local branching in the chapter and presentation in
  screens. Reuse existing semantic assets only.
- ADR-0008 requires one canonical choice commit, immediate reaction, later
  payoff, and source-hash evidence per record; all source scans are test-time.
- ADR-0006 reserves ending entry and completion to SYS-ENDING. Day 6 can only
  stage its frozen state for later ownership; it cannot consume that ownership.

## Out of Scope

- Day 6 asset admission, route/accessibility evidence, and traceability, owned
  by Stories 017–019.
- Day 7 source, terminal witnesses, resolver or qualification changes, all
  ending labels/completion, epilogue, manifest expansion, external assets,
  release validation, packaging, and stage changes.

## QA Test Cases

- **AC-1: Unit, scenes, and exact choice records** — scanners find only one
  approved unit, four scenes, fifteen approved records, exact projections, and
  strictly later payoffs; duplicates/unknowns/same-scene payoffs fail closed.
- **AC-2: Conditional resource, repair, and cost nodes** — valid and invalid
  resource/token histories prove each authorized sibling set and no fabricated
  option; reconsideration cannot appear before the required visible chain.
- **AC-3: Commitment derivation and boundary** — every valid partition selects
  exactly one action; malformed facts expose none; source has no resolver,
  ending, qualification, persistence, terminal, Day 7, or partial-manifest
  reference.

## Test Evidence

- `tests/unit/sys_narrative/day6_authored_source_test.py`
- `tests/unit/sys_narrative/day6_commitment_derivation_test.py`
- `production/qa/evidence/day6-authored-source-evidence.md`

## Dependencies

- Depends on: Stories 012–015 are Complete and their Day 5 answer/outcome
  contracts remain current.

## Completion Notes

**Completed**: 2026-08-13
**Criteria**: 15/15 focused source, derivation, and asset checks pass. The
canonical unit, four scenes, exact fifteen records, frozen conditional nodes,
closed commitment derivation, source hash, catalog inputs, and ADR-0008
reaction-before-event order have direct coverage.
**Deviations**: None. The narrow prologue facts provide only frozen Day 6
preconditions; no Day 7 or SYS-ENDING ownership was added.
**Test Evidence**: `tests/unit/sys_narrative/day6_authored_source_test.py` and
`tests/unit/sys_narrative/day6_commitment_derivation_test.py`.
**Code Review**: Approved. The pure derivation is closed, primitive, detached,
and failure-closed; the chapter stages facts only and has no resolver,
qualification, persistence, terminal, or ending access.
- Unlocks: Stories 017–019.
