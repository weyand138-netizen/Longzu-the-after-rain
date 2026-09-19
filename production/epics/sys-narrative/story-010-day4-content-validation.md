# Story 010: Day 4 Route, Accessibility, and Evidence Validation

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Complete
> **Layer**: Feature
> **Type**: Integration
> **Estimate**: 1.5 days
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-11

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Requirement**: `TR-NAR-010` — Day 4 engine-route validation proves canonical
ticket, contact, and no-backup paths, accessible presentation, current
source-hash evidence, and no partial-manifest or terminal-scope expansion.

**Governing ADRs**: ADR-0003 (primary), ADR-0008
**Engine**: Ren'Py 8.5.3 | **Risk**: High

**Engine Notes**: The pinned Ren'Py 8.5 testcase wrapper is required. Route
captures must use the established physical surface and isolated-save controls;
lint/compile, global testcases, and current-source-hash evidence remain
mandatory.

**Control Manifest Rules (Feature and Presentation layers)**:

- Required: keyboard focus and readable layout at 1280x720; a non-timed path
  through every scene; exact immediate-reaction and later-payoff checks.
- Forbidden: hover, sound, animation, flashing, colour, or timed input as the
  only way to continue or understand a decision-relevant fact; production
  references to test-only code/data.
- Performance: route execution and capture are test-time only; add no runtime
  source scan, CFG construction, path enumeration, or per-frame work.

## Acceptance Criteria

- [x] Add deterministic engine and integration coverage reaching Day 4 from
  Day 3-compatible setups, then entering the existing continuation seam without
  traceback.
- [x] Exercise two-ticket, single-ticket, independent-contact registration,
  contact decline, and guarded no-backup branches through keyboard activation;
  assert exact canonical history, sibling availability, reactions,
  resources/events/outcomes, and continuation seam.
- [x] Prove the self-controlled route-preparation answer precedes every related
  response node, and that contact registration requires both approved alias
  and retained arcade-token inputs.
- [x] Capture each critical Day 4 choice surface at physical 1280x720,
  keyboard-only, silent, reduced-motion and at 1.5x font, high-contrast,
  reduced-motion; captions and decisions are readable, focusable, and unclipped.
- [x] Prove colour, hover, sound, motion, and presentation effects are not the
  sole source of a decision-relevant fact; both baselines preserve canonical
  IDs, availability, reactions, resources/events/outcomes, and continuation.
- [x] During critical choices, focus is distinct and keyboard-operable; no
  quick-menu target is focusable.
- [x] Bind runner output, result record, capture metadata, screenshots, content
  review, and current Day 4 source hash in one evidence bundle; do not expand
  the Day 1-only partial manifest or claim terminal, ending, or release work.

## Implementation Notes

- Extend `game/testcases.rpy` and the integration test with deterministic Day
  4 routes; use the established physical-surface and self-voicing controls.
- Native choice surfaces must provide keyboard focus and actual traversal; do
  not create test-only production edges or bypass the narrative outcome.
- Source scanning and CFG/path enumeration stay out of gameplay. Evidence is
  test-time only and fails closed on hash or required-artifact mismatch.

## Out of Scope

- Authoring Day 4 prose/bindings (Story 009) and admitting its assets (Story
  011).
- Any partial-manifest expansion, Day 5+ source, terminal witness, ending,
  release validation, or UI redesign.

## QA Test Cases

- **AC-1: Canonical engine routes**
  - Given: Day 3-compatible deterministic setups and each valid Day 4 guard.
  - When: every approved ticket, contact, and no-backup branch is submitted by
    keyboard activation.
  - Then: it reaches the existing continuation seam without traceback with exact history,
    availability, reaction, resources/events/outcomes, and continuation.
  - Edge cases: wrong/missing history, invalid guard, unavailable sibling,
    duplicate activation, missing reaction, wrong fact, handoff, or traceback
    fails the route.
- **AC-2: Agency preconditions and accessibility baselines**
  - Given: the two required display/preference baselines.
  - When: critical Day 4 surfaces are captured and traversed by keyboard.
  - Then: the route answer precedes response, contact requires alias/token,
    captions are readable, focus is distinct, and no quick-menu target is
    focusable.
  - Edge cases: absent route answer, invalid contact guard, clipping, focus
    trap, colour-only focus, or audio/hover/motion-only fact fails validation.
- **AC-3: Evidence integrity and scope**
  - Given: the Day 4 evidence bundle and authored-source record.
  - When: their hashes, runner output, capture metadata, screenshots, and scope
    assertions are verified.
  - Then: every artifact identifies the tested source generation and no
    partial-manifest, terminal, ending, or release scope is claimed.
  - Edge cases: missing record, mismatched hash, wrong dimensions, or forbidden
    scope reference fails closed.

## Test Evidence

- `tests/integration/sys_narrative/day4_content_validation_test.py`
- Engine routes and captures in `game/testcases.rpy`
- `production/qa/evidence/day4-content-validation-<date>/`

## Dependencies

- Depends on: Story 009 and Story 011 complete.
- Unlocks: Sprint 3 smoke check and QA hand-off.

## Completion Notes

**Completed**: 2026-08-11
**Criteria**: 7/7 passing.
**Deviations**: Authorized acceptance clarification: Day 5 source is outside
this story's scope, so the verified target is the existing Day 4 continuation
seam rather than a literal Day 5 label. No Day 5, partial-manifest, terminal,
ending, or release scope was added.
**Test Evidence**: `tests/integration/sys_narrative/day4_content_validation_test.py`,
`game/testcases.rpy`, and
`production/qa/evidence/day4-content-validation-2026-08-11/` — preserved pinned
Ren'Py global suite PASS (30/30 testcases; 255/255 assertions); current-test-
definition revalidation is recorded in
`production/qa/evidence/day4-qa-revalidation-2026-08-12.md` (30/30; 256/256).
**Code Review**: Approved with suggestions; standalone execution of the static
integration verifier is environment-limited, while the pinned engine suite and
hash-bound evidence cover the story's runtime assertions.
