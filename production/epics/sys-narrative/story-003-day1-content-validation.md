# Story 003: Day 1 Content Validation and Accessibility Evidence

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production  
> **Status**: Complete  
> **Layer**: Feature  
> **Type**: Integration  
> **Estimate**: 1 day  
> **Manifest Version**: 2026-08-04.1

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`  
**Requirement**: `TR-NAR-001`  
**Governing ADRs**: ADR-0003, ADR-0008, ADR-0009  
**Engine**: Ren'Py 8.5.3 | **Risk**: High

## Acceptance Criteria

- [x] Add an engine-hosted Day 1 route testcase and relevant pure/source validation tests.
- [x] Capture Day 1 evidence at 1280×720, 1.5x font, high contrast, keyboard-only, silent, and reduced-motion baselines.
- [x] Verify the HUD/choice surface exposes no hidden state and removes quick-menu focus during the critical choice interaction.
- [x] Record source hashes, raw runner output, visual captures, and a content-review result in the Sprint 1 QA evidence bundle.

## QA Test Cases

- **AC-1**: Given the canonical Day 1 route, when the Ren'Py testcase and pure/source validation run, then the route reaches the expected delayed payoff with no traceback and all validated artifacts use the current source hash.
- **AC-2**: Given 1280x720, 1.5x font, high contrast, keyboard-only, silent, and reduced-motion baselines, when the Day 1 scene is reached, then required actions are visible, focusable, and readable; no glyph is clipped; and no decision-relevant fact depends only on audio or motion.
- **AC-3**: Given a critical Day 1 choice, when focus is enumerated through the bounded reaction interaction, then quick-menu affordances are absent/unfocusable and choices have a stable first keyboard focus.
- **AC-4**: Given the Sprint 1 evidence bundle, when it is validated, then source hashes, raw runner output, visual captures, and content-review result are present, nonempty, and match the tested source generation.

**Required test path**: `tests/integration/sys_narrative/day1_content_validation_test.py`; engine route testcase in `game/testcases.rpy`

## Dependencies

- Depends on: Story 002.
- Unlocks: Sprint 1 completion and Day 2 content planning.

## Implementation Notes

- `game/testcases.rpy` provides the engine-hosted Day 1 keyboard route and two native Ren'Py visual baseline captures.
- `game/screens.rpy` applies persisted 1.5x font and high-contrast settings to the Day 1 narrative and choice surfaces; the quick menu is absent during critical choice interaction.
- `game/chapters/day1.rpy` omits the opening dissolve when reduced motion is enabled. Day 1 contains no decision-relevant audio cue.
- `tests/integration/sys_narrative/day1_content_validation_test.py` validates source/UI contracts, while the evidence runner preserves raw output and captured PNGs.

## Out of Scope

- Full 15-unit manifest generation, terminal ending witnesses, and future-Day source content remain deferred under ADR-0009.

## Performance Notes

- The added checks run only in the test harness; the UI setting reads are bounded per screen render and add no runtime source enumeration.

## Test Evidence

- Automated: `tests/integration/sys_narrative/day1_content_validation_test.py`, `game/testcases.rpy::day1_authored_route_contract`, and `game/testcases.rpy::day1_accessibility_visual_baselines`.
- Evidence bundle: `production/qa/evidence/day1-content-validation-2026-08-10-r9/`.

## Completion Notes

- Closed on 2026-08-10 after explicit user confirmation.
- Final engine evidence: 13/13 Ren'Py testcases and 63/63 assertions passed; the final capture set contains two verified 1280×720 PNGs.
- Final static evidence: 30 targeted Story 001–003 Python tests, Ren'Py lint/compile, and the content-constraint scan passed.
- Solo review mode: QA coverage and lead-programmer director gates were skipped; no technical debt was logged.
