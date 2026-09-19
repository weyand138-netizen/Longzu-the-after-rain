# Story 012: Day 5 Authored Source and Derived Route Answer

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Complete
> **Layer**: Feature
> **Type**: Config/Data
> **Estimate**: 3 days
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-13

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Requirement**: `TR-NAR-012` — Canonical Day 5 source owns the family-archive
scene set, exact choice/reaction/payoff bindings, and a visible-resource-only
route-answer derivation without partial-manifest, terminal, or later-day scope.

**Governing ADRs**: ADR-0008 (primary), ADR-0003, ADR-0006 (boundary only)
**Engine**: Ren'Py 8.5.3 | **Risk**: High

**Engine Notes**: The pure derivation module must not mutate Ren'Py state. The
chapter uses ordinary Ren'Py labels and choices; lint/compile, the pinned global
testcase wrapper, source-hash validation, and the content-constraint scan remain
mandatory.

**Control Manifest Rules (Feature layer)**:

- Required: stable chapter labels; one canonical choice commit per response;
  every choice has an immediate reaction and a strictly later payoff identity.
- Required: an agency answer is action/object-led, frozen before the response
  surface, and its accepting/overriding partitions are exact and non-empty.
- Forbidden: screens selecting outcomes, copied ending conditions, imported
  modules mutating store state, hidden score/token/qualification/ending input,
  full Erii dialogue, a partial-manifest update, or a Day 6+ branch.
- Performance: derivation and source scans stay bounded and are not per-frame;
  the pure derivation has no I/O, random state, network, or persistent state.

**Normative source**: `design/narrative/seven-day-content-baseline.md`,
`narrative_content_baseline:v1.2`, Day 5 topology, agency table, and
`erii_route_answer_derivation:v1` record in `design/registry/entities.yaml`.

## Acceptance Criteria

- [ ] Add `game/chapters/day5.rpy` with exactly
  `chapter_day5_family_lie`, `scene_day5_family_archive`,
  `scene_day5_truth_delivery`, `scene_day5_response_answer`, and
  `scene_day5_shared_liability`.
- [ ] Declare only the ten approved Day 5 choice/reaction/payoff records and
  implement their frozen axes, token revocations/repairs, immediate reactions,
  and later payoff identities. Narrative-only blame remains zero-axis.
- [ ] Add a pure `erii_route_answer_derivation:v1` implementation that accepts
  only exact typed Day 4 resource facts and returns the unique ordered answer:
  `shared_escape`, `independent_contact`, `solo_departure`, or
  `continue_without_executable_route`; contradictory, incomplete, or untyped
  input returns `undetermined` and exposes no Day 5 response choice.
- [ ] Freeze a `character_answer_derivation_record`-equivalent Day 5 record
  containing its derivation ID, transaction ID, input fact IDs, allowed states,
  selected state, visible action/object ID, priority rule, source hash, and
  forbidden-hidden-input count. The chapter's action/object evidence matches
  the selected state before `event_erii_selects_route_response` and
  `cp_day5_route_answer_expressed` are recorded.
- [ ] Register `agency_day5_response` only for a non-undetermined answer;
  its response set is exactly honor/replace, each response has the frozen
  non-empty outcome, and a replacement creates old-order override without an
  autonomy increase.
- [ ] Show a school-evidence repair node only for a pre-existing unresolved
  Day 3 token; show a daily-choice repair node only when its token was
  unresolved before entering the route-answer scene, never immediately after
  a new replacement token. Both repair and keep branches remain exact records.
- [ ] Bind a current Day 5 source SHA-256 and player-safe chapter/memory catalog
  inputs to evidence. No player-visible hidden-state terms, full Erii dialogue,
  Day 1 partial-manifest expansion, Day 6+, terminal, ending, epilogue, or
  release claim is introduced.

## Implementation Notes

- ADR-0003 keeps Day 5 prose/local branching in its own chapter and restricts
  `game/screens.rpy` to presentation; use existing semantic asset aliases.
- ADR-0008 requires canonical choice commits, exact response/outcome joins,
  source-hash evidence, and failure-closed response omission for an
  undetermined answer.
- ADR-0006 reserves ending entry and completion to SYS-ENDING. This chapter
  may only return through the existing continuation seam; it cannot invoke a
  resolver, ending-entry helper, completion helper, or persistent grant.

## Out of Scope

- Day 5 asset admission and route/accessibility evidence, owned by Stories 013
  and 014; traceability record, owned by Story 015.
- Day 6/Day 7 source, route commitment, terminal witnesses, ending logic,
  epilogue, resolver/qualification changes, a partial-manifest expansion,
  final art/audio, release validation, or packaging.

## QA Test Cases

- **AC-1: Source unit, scenes, and exact records**
  - Given: the frozen baseline and Day 5 source scanner.
  - When: it enumerates units, scenes, choices, reactions, payoffs, axes, and
    token projections.
  - Then: it finds one approved unit, four scenes, ten exact records, and no
    unapproved ID or same-scene payoff identity.
  - Edge cases: absent/duplicate/unknown labels, scenes, choices, records,
    reactions, payoffs, or token repair/revoke mappings fail closed.
- **AC-2: Pure route-answer derivation**
  - Given: valid Day 4 resource fact tuples and malformed/contradictory tuples.
  - When: `erii_route_answer_derivation:v1` runs.
  - Then: valid input selects exactly one state in frozen priority order with
    its required action/object evidence; bad input returns `undetermined`.
  - Edge cases: two ticket kinds, incomplete contact handover, mismatched
    card/event, unknown key, non-bool value, and hidden-state-shaped input fail
    without a selected response state.
- **AC-3: Agency, repair, and scope boundary**
  - Given: source order and representative histories.
  - When: source and state contracts are checked.
  - Then: answer registration/evidence precede responses; honor/replace form
    the exact partition; repairs obey their pre-existing-token guards; source
    hash/catalog evidence and player-safe wording agree.
  - Edge cases: author-assigned answer, a response for `undetermined`, early
    daily repair, an empty outcome, hidden terms, full Erii prose, partial
    manifest, Day 6+, terminal, ending, epilogue, or release text fails.

## Test Evidence

- `tests/unit/sys_narrative/day5_authored_source_test.py`
- `tests/unit/sys_narrative/day5_route_derivation_test.py`
- `production/qa/evidence/day5-authored-source-evidence.md`

## Dependencies

- Depends on: Stories 009–011 are Complete and their Day 4 resource state and
  accessibility harness remain current.
- Unlocks: Stories 013, 014, and 015.

## Completion Notes

**Completed**: 2026-08-13
**Criteria**: 7/7 passing. The unit, pure derivation, exact response/repair
boundaries, hash/catalog inputs, and source scope have direct unit coverage.
**Deviations**: None.
**Test Evidence**: `tests/unit/sys_narrative/day5_authored_source_test.py` and
`tests/unit/sys_narrative/day5_route_derivation_test.py` — 19/19 focused PASS;
the full Python suite passed 211/211 before the final hash-consistency assertion,
which was then re-run in the focused suite.
**Code Review**: Approved. The pure derivation has a closed primitive input set,
does not mutate Ren'Py state, fails closed, and the chapter remains within the
ADR-0003/0006/0008 ownership boundaries.
