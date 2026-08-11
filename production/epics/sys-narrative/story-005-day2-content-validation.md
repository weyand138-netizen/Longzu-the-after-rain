# Story 005: Day 2 Content Validation and Accessibility Evidence

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production  
> **Status**: Complete  
> **Layer**: Feature  
> **Type**: Integration  
> **Estimate**: 1 day  
> **Manifest Version**: 2026-08-04.1  
> **Last Updated**: 2026-08-11

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`  
**Requirement**: `TR-NAR-005` — Day 2 engine-route validation proves canonical
choice paths, accessible presentation, current source-hash evidence, and no
expansion of the Day 1-only partial manifest. `TR-NAR-001` remains the partial
parent requirement for the full seven-day content lock; this story does not
claim full-terminal validation.

**Governing ADRs**: ADR-0003 (primary), ADR-0008  
**Engine**: Ren'Py 8.5.3 | **Risk**: High

## Acceptance Criteria

- [ ] Add an engine-hosted Day 2 route testcase and integration validation
  that reaches the last-machine handoff with no traceback and the current Day
  2 source hash.
- [ ] Validate both ordinary alias responses, the conditional
  `day2_admit_alias_unknown` route, and both two-token responses against their
  canonical Day 2 IDs and player-visible immediate reactions.
- [ ] Capture Day 2 evidence at the 1280x720 physical baseline, keyboard-only,
  silent, reduced-motion, 1.5x font, and high-contrast configurations; all
  required choice captions must be visible, focusable, and readable.
- [ ] Prove that no decision-relevant fact depends only on audio, motion,
  colour, hover, or the code-defined arcade presentation; the alias and token
  trade-off must remain visible/localizable text and keyboard-operable choices.
- [ ] Record current source hash, runner output, visual captures, and content
  review in a Day 2 evidence bundle.
- [ ] Do not expand or repurpose ADR-0009's Day 1-only partial manifest; full
  manifest and terminal witnesses remain deferred until their approved scope
  exists.

## Implementation Notes

- Extend `game/testcases.rpy` with deterministic Day 2 routes for the normal
  alias path, the unresolved-silence repair path, and the two-token decision.
  Pin the physical screenshot surface to 1280x720 and set
  `renpy.game.preferences.self_voicing=False` before captures, matching the
  stable Day 1 baseline harness.
- The alias choice surface must retain stable first keyboard focus and must not
  reveal axis/token/resource/route semantics. Critical interactions must keep
  quick-menu controls absent or unfocusable according to the approved gate.
- Reduced motion and silent output may alter presentation only; they must not
  change canonical choice IDs, response availability, the visible final state,
  or continuation.
- Evidence is bound to the Day 2 source SHA-256. Runtime must consume authored
  content only; source scanning, CFG construction, and path enumeration remain
  build/test concerns.
- Apply the Feature and Presentation rules in
  `docs/architecture/control-manifest.md`: retain the stable Day 2 chapter
  label; let screens render state but never choose a narrative outcome; keep a
  keyboard-operable, non-timed path through every decision; and verify readable
  captions and stable focus at the 1280×720 physical baseline. No
  decision-relevant fact may depend solely on colour, hover, sound, motion, or
  an arcade presentation effect.

## Performance Notes

No material gameplay performance impact is expected. Day 2 route execution,
source-hash validation, screenshot capture, and focus enumeration run only in
the test workflow. Runtime adds no source scan, CFG construction, path
enumeration, polling loop, or per-frame allocation; capture runs pin the
physical surface to 1280×720.

## Out of Scope

- Full 15-unit manifest, Day 2 partial-manifest schema, terminal continuation
  witnesses, ending validation, and release evidence.
- Day 3 content, final art/audio production, new asset admission, and a new
  UI information architecture.

## QA Test Cases

- **AC-1 — canonical engine routes**
  - Given: the current Day 2 source and a deterministic Day 1-compatible test
    setup.
  - When: the normal, conditional-repair, save-token, and spend-token routes
    are exercised through keyboard activation.
  - Then: each reaches the last-machine handoff without traceback and records
    only the expected canonical Day 2 choices.
  - Edge cases: unavailable conditional response, duplicate activation, or
    unknown choice identity fails the integration test.
- **AC-2 — accessibility baseline**
  - Given: 1280x720 physical output with keyboard-only, silent,
    reduced-motion, then 1.5x/high-contrast variants.
  - When: each Day 2 choice surface is captured and focus is enumerated.
  - Then: every required caption is visible/readable, the first choice has
    stable focus, and no quick-menu control is focusable during critical input.
  - Edge cases: clipped glyph, focus trap, persisted clipboard-voicing overlay,
    colour-only focus, audio-only fact, or motion-only fact fails the case.
- **AC-3 — evidence integrity and boundary**
  - Given: the Day 2 evidence bundle and its source validation record.
  - When: artifact hashes, runner output, capture dimensions, content review,
    and manifest-scope assertions are checked.
  - Then: every record matches the current Day 2 source and no Day 2 data has
    been admitted to the Day 1-only partial manifest or a terminal validator.
  - Edge cases: stale source hash, missing evidence, wrong capture dimensions,
    or Day 2 partial-manifest claim fails closed.

**Required test path**:
`tests/integration/sys_narrative/day2_content_validation_test.py`; engine
testcases in `game/testcases.rpy`.

## Test Evidence

- Integration validation:
  `tests/integration/sys_narrative/day2_content_validation_test.py`
- Engine routes and visual baselines: `game/testcases.rpy`
- Evidence bundle: `production/qa/evidence/day2-content-validation-<date>/`

## Dependencies

- Depends on: Story 004.
- Unlocks: Day 3 source planning and a future approved incremental/full
  narrative-manifest decision.

## Completion Notes

**Completed**: 2026-08-11  
**Criteria**: 6/6 passing.  
**Deviations**: None. The native Ren'Py choice surface uses down-arrow traversal;
the route test verifies this actual keyboard behavior without assigning focus.  
**Test Evidence**: `tests/integration/sys_narrative/day2_content_validation_test.py`
(10/10 passing); preserved engine evidence at
`production/qa/evidence/day2-content-validation-2026-08-11/` (18/18 testcases,
102/102 assertions); lint/compile and content-constraint scan passed.  
**Code Review**: Approved after coverage fixes for immediate reactions,
conditional availability, automatic focus, keyboard traversal, and evidence
integrity.
