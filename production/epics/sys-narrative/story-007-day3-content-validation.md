# Story 007: Day 3 Route, Accessibility, and Evidence Validation

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production  
> **Status**: Complete  
> **Layer**: Feature  
> **Type**: Integration  
> **Estimate**: 1 day  
> **Manifest Version**: 2026-08-04.1  
> **Last Updated**: 2026-08-11

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`  
**Requirement**: `TR-NAR-007` — Day 3 engine-route validation proves all
canonical evidence-and-pause paths, accessible presentation, current
source-hash evidence, and no partial-manifest or terminal-scope expansion.

**Governing ADRs**: ADR-0003 (primary), ADR-0008  
**Engine**: Ren'Py 8.5.3 | **Risk**: High

**Engine Notes**: Uses Ren'Py 8.5 testcase coverage already verified through
the pinned SDK wrapper. Every capture run must use the established physical
surface and isolated-save controls; lint/compile and the global testcase suite
remain mandatory evidence.

**Control Manifest Rules (Feature and Presentation layers)**:

- Required: keyboard focus and readable layout at 1280x720; a non-timed path
  through every scene; exact immediate-reaction and later-payoff checks.
- Forbidden: hover, sound, animation, flashing, colour, or timed input as the
  only means to continue or understand a decision-relevant fact; test-only
  code/data references from production.
- Performance: route execution and screenshot capture are test-time only and
  add no runtime polling, source scan, CFG construction, or per-frame work.

## Acceptance Criteria

- [ ] Add deterministic engine and integration coverage that reaches the Day 3
  handoff from a Day 2-compatible setup without traceback.
- [ ] Exercise all four combinations of share/withhold school evidence and
  honor/force truth pace through keyboard activation, asserting exact
  canonical history, sibling availability, immediate reactions, and handoff.
- [ ] Capture each critical Day 3 choice surface at the physical 1280x720,
  keyboard-only, silent, reduced-motion baseline and at 1.5x font,
  high-contrast, reduced-motion. Captions must be visible, readable,
  focusable, and unclipped.
- [ ] Prove that colour, hover, sound, motion, or presentation effects are not
  the sole source of any decision-relevant fact. Silent/reduced-motion modes
  may change presentation only, never canonical IDs, availability, reaction,
  or continuation.
- [ ] During critical choices, focus must be distinct and keyboard-operable;
  no quick-menu target may be focusable.
- [ ] Bind raw runner output, result record, capture metadata, screenshots,
  content review, and current Day 3 source hash in the evidence bundle.
- [ ] Do not add Day 3 data to `narrative_partial_day1_manifest:v1` and do not
  claim full-manifest, terminal-witness, ending, or release validation.

## Implementation Notes

- Extend `game/testcases.rpy` with deterministic Day 3 routes. Use the proven
  Day 1/Day 2 physical-surface and self-voicing controls before captures.
- Let the native choice surface provide keyboard focus and assert actual
  traversal; do not use a test-only production edge or a scripted narrative
  outcome bypass.
- Keep source scanning and CFG/path enumeration out of gameplay. Evidence is
  test-time only and must fail closed when its hash or required artifacts do
  not match.

## Out of Scope

- Authoring Day 3 prose/bindings (Story 006) and admitting Day 3 assets
  (Story 008).
- Any partial-manifest expansion, terminal witness, ending validation, or
  later-day content.

## QA Test Cases

- **AC-1: Canonical engine routes**
  - Given: a Day 2-compatible deterministic setup.
  - When: all share/withhold × honor/force Day 3 combinations are submitted
    through keyboard activation.
  - Then: each reaches the expected Day 3 handoff without traceback and has
    only the exact expected canonical history, availability, and reaction.
  - Edge cases: wrong/missing history, unavailable sibling, duplicate
    activation, missing reaction, wrong handoff, or traceback fails the route.
- **AC-2: Accessibility baselines**
  - Given: the two required physical display and preference baselines.
  - When: each Day 3 choice surface is captured and traversed by keyboard.
  - Then: captions are visible/readable, focus is distinct, and no quick-menu
    target is focusable during critical input.
  - Edge cases: clipping, focus trap, ambiguous focus, colour-only focus, or
    a decision-relevant audio/hover/motion-only fact fails validation.
- **AC-3: Evidence integrity and scope**
  - Given: the Day 3 evidence bundle and authored-source record.
  - When: their hashes, output, capture metadata, and scope assertions are
    verified.
  - Then: every artifact identifies the tested source generation and no
    partial-manifest or terminal scope is claimed.
  - Edge cases: missing record, mismatched hash, wrong capture dimensions, or
    forbidden manifest/terminal reference fails closed.

## Test Evidence

- `tests/integration/sys_narrative/day3_content_validation_test.py`
- Engine routes and captures in `game/testcases.rpy`
- `production/qa/evidence/day3-content-validation-<date>/`

## Dependencies

- Depends on: Story 006 and Story 008 complete.
- Unlocks: Sprint 2 smoke check and QA hand-off.

## Completion Notes

**Completed**: 2026-08-11  
**Criteria**: 7/7 passing.  
**Deviations**: None. The Day 3-only non-colour focus underline in
`game/screens.rpy` was required to satisfy the existing accessibility acceptance
criterion; it leaves Day 1 and Day 2 baselines unchanged.  
**Test Evidence**: `tests/integration/sys_narrative/day3_content_validation_test.py`
(6/6); isolated Ren'Py capture evidence at
`production/qa/evidence/day3-content-validation-2026-08-11/` (24/24 testcases,
172/172 assertions).  
**Code Review**: Approved after corrective review.
