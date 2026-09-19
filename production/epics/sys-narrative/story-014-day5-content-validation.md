# Story 014: Day 5 Route, Accessibility, and Evidence Validation

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Complete
> **Layer**: Feature
> **Type**: Integration
> **Estimate**: 2 days
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-13

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Requirement**: `TR-NAR-014` — Day 5 engine-route validation proves truth,
liability, derived-response, and repair paths with accessible presentation and
current source-hash evidence, without partial-manifest, terminal, or later-day
expansion.

**Governing ADRs**: ADR-0003 (primary), ADR-0008
**Engine**: Ren'Py 8.5.3 | **Risk**: High

**Engine Notes**: Use the pinned Ren'Py 8.5 testcase wrapper, isolated saves,
physical 1280x720 captures, and current-source-hash evidence. No test-only
production edge or post-cutoff API is permitted.

**Control Manifest Rules (Feature and Presentation layers)**:

- Required: keyboard focus and readable decision text at 1280x720; a non-timed
  path through every exposed Day 5 node; exact canonical choices, reactions,
  derived answers, outcomes, and continuation seam.
- Forbidden: quick-menu focus during a critical decision, hover/sound/colour/
  motion-only facts, production references to test-only state, Day 6 commitment,
  partial-manifest expansion, or terminal/ending/release claim.
- Performance: testcase traversal/capture is test-time only and adds no runtime
  polling, path enumeration, or per-frame source scanning.

## Acceptance Criteria

- [ ] Add deterministic engine and integration coverage from Day 4-compatible
  setups for full archive/safe summary, liability/self-blame, each valid derived
  answer, honor/replace response, and eligible daily/school repair branches.
- [ ] Assert exact history, branch availability, immediate reactions, axes,
  tokens, resources/events/outcomes, derived record fields, response partition,
  and continuation seam. Invalid Day 4 facts expose no response surface.
- [ ] Prove `shared_escape`, `independent_contact`, `solo_departure`, and
  `continue_without_executable_route` are selected only from the frozen resource
  order and each visible action/object evidence matches its state.
- [ ] Capture Day 5 truth/route-response surfaces at physical 1280x720,
  keyboard-only, silent/reduced-motion and at 1.5x font, high-contrast,
  reduced-motion; captions and actions are visible, readable, focused, and
  unclipped, with no quick-menu focus target.
- [ ] Prove silent/reduced-motion and high-contrast presentation change neither
  canonical IDs, availability, reaction, answer derivation, outcome, resource,
  event, token, or continuation semantics.
- [ ] Bind runner output, result record, capture metadata, screenshots, source
  hash, and content review in one evidence bundle without a Day 1 partial-
  manifest, Day 6+, terminal, ending, epilogue, or release assertion.

## Implementation Notes

- Extend `game/testcases.rpy` and the integration verifier with deterministic
  Day 5 routes and the existing physical-surface/self-voicing controls.
- Native choices keep keyboard focus. The focus test observes engine focus; it
  must not assign focus as an artificial test seam.
- Source/evidence validation fails closed on absent output, stale hash, wrong
  capture dimensions, mismatched derivation, a missing response outcome, or
  forbidden content scope.

## Out of Scope

- Authoring Day 5 source/derivation and asset records, owned by Stories 012 and
  013; traceability, owned by Story 015.
- Day 6/Day 7 source, commitment, terminal witnesses, ending resolution,
  epilogue, release validation, UI redesign, or partial-manifest work.

## QA Test Cases

- **AC-1: Canonical engine routes and derivation**
  - Given: Day 4-compatible shared, contact, solo, fallback, pre-existing daily
    token, and pre-existing school token states.
  - When: each Day 5 surface is traversed with keyboard activation.
  - Then: source order, exact history, current state, derivation record,
    response partition, reactions, outcomes, token effects, and handoff match.
  - Edge cases: missing/duplicate activation, invalid resource facts, response
    for `undetermined`, wrong action evidence, early repair, wrong history,
    unavailable sibling, or traceback fails.
- **AC-2: Accessibility and input equivalence**
  - Given: both required display/preference baselines.
  - When: critical truth and route-answer surfaces are captured/traversed.
  - Then: critical facts are textual, focus is distinct and keyboard-operable,
    text is unclipped, and quick-menu targets are absent.
  - Edge cases: focus trap, colour-only focus, clipped text, sound/hover/motion-
    only fact, or changed semantic outcome fails.
- **AC-3: Evidence integrity and scope**
  - Given: the Day 5 evidence bundle and authored-source record.
  - When: source hash, runner results, hashes, captures, and scope assertions
    are validated.
  - Then: all required artifacts identify the tested source generation and no
    forbidden scope is claimed.
  - Edge cases: absent file, stale hash, wrong dimensions, altered runner hash,
    partial manifest, Day 6+, terminal, ending, epilogue, or release text fails.

## Test Evidence

- `tests/integration/sys_narrative/day5_content_validation_test.py`
- Engine routes and captures in `game/testcases.rpy`
- `production/qa/evidence/day5-content-validation-2026-08-13-reviewed-verified/`

## Dependencies

- Depends on: Stories 012 and 013 are Complete.
- Unlocks: Story 015 and Sprint 4 smoke/QA hand-off.

## Completion Notes

**Completed**: 2026-08-13
**Criteria**: 6/6 accepted. The engine covers all four valid derived answers,
the invalid closed-input omission, both truth/liability sides, honor/replace,
and eligible school/daily repair boundaries. The verifier hash-binds the
reviewed source, testcase definition, runner output, and four 1280x720 captures.
**Deviations**: None. Intermediate raw runs remain preserved but are not used as
passing evidence.
**Test Evidence**: `tests/integration/sys_narrative/day5_content_validation_test.py`
(4/4); `production/qa/evidence/day5-content-validation-2026-08-13-reviewed-verified/`
(Ren'Py global 37/37 testcases, 345/345 assertions).
**Code Review**: APPROVED after remediation: each liability event is now set
after its immediate narrative reaction, and the test routes observe it through
an already-eligible repair node rather than a test-only runtime seam.
