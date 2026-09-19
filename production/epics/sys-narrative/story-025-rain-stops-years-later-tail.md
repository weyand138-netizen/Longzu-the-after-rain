# Story 025: rain_stops Years-Later Tail

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Complete
> **Layer**: Feature
> **Type**: Integration
> **Estimate**: 2 days
> **Last Updated**: 2026-08-14
> **Manifest Version**: 2026-08-04.1

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Baseline**: `design/narrative/seven-day-content-baseline.md` — `narrative_content_baseline:v1.3`
**Requirements**: `TR-NAR-001`, `TR-END-005`
**Governing ADRs**: ADR-0003, ADR-0006, ADR-0008
**Engine**: Ren'Py 8.5.3 | **Risk**: Medium
**Design impact**: `docs/architecture/change-impact-2026-08-14-rain-stops-epilogue.md`

The existing `epilogue_rain_stops_arcade` needs a short, restrained years-later
tail after its current lights-out scene. The input DOCX is an unconfirmed
fan-adaptation reference; implementation may use only its high-level structure
and theme, never line-by-line wording or unconfirmed named-world-state claims.

## Acceptance Criteria

- [x] The 15 canonical production units remain an exact set; the six ending IDs,
  resolver, priority, canonical witnesses, five axes, token definitions,
  qualification bindings, ending predicates, and completion boundary are
  unchanged.
- [x] Only `rain_stops` reaches the existing
  `epilogue_rain_stops_arcade`; the new tail occurs after the existing
  lights-out scene and after `event_epilogue_lights_out_completed`, without
  moving, duplicating, or adding completion events.
- [x] The tail contains both approved structural elements: a short ordinary
  neighborhood-observer view of the small arcade using only unnamed old
  friends/ordinary customers, and a clearly marked written note by 绘梨衣.
  Complex note content is not an `erii` spoken-dialogue line.
- [x] The source introduces no player choice, route, ending, achievement,
  Gallery entry, persistent field, resolver input, axis/token/resource/
  qualification change, or new canonical unit; no new asset path is added.
- [x] Forbidden extra world-state claims are not confirmed: no named extra
  character return, family conversion of 路鸣泽, pregnancy, twins, or other
  major canon assertion is required by the tail.
- [x] Focused tests, full Python tests, pinned Ren'Py global tests,
  lint/compile, Erii content constraints, source/content-lock identity checks,
  and `git diff --check` pass. Deferred GUI playtest, SAPI listening,
  semantic-equivalence, copyright, and subjective narrative review remain
  explicitly manual and are not claimed as PASS.

## Implementation Notes

- Modify only the existing `rain_stops` epilogue body in
  `game/chapters/endings.rpy`, plus the directly required tests and evidence.
- Use ordinary `narrator` presentation with an explicit written-note marker;
  do not add `erii` speech, a menu, a choice, a new label, or a new state
  assignment.
- Keep the existing `commit_ending_completion` callsite and both existing
  epilogue completion event assignments in their current order.
- Use no asset references. No work under formal asset directories is in scope.
- Refresh `design/content-lock.md` with the final `endings.rpy` and baseline
  hashes under lock v2 after implementation.

## Out of Scope

All other endings, Day 7 source, choices, axes, tokens, resources,
qualifications, resolver/predicate/priority logic, persistence, achievements,
Gallery, new canonical units/events, named-character reunions, pregnancy or
twins, official-canon claims, line-by-line DOCX reuse, all visual/audio/voice
assets, UI bitmap work, release/package work, stage changes, and human
playtest/SAPI/semantic/subjective sign-off.

## Dependencies

- `production/epics/sys-ending/story-003-six-endings-and-rain-epilogue.md` — Complete
- `production/epics/sys-narrative/story-024-production-end-to-end-orchestrator.md` — Complete
- None beyond these completed terminal and Production traversal boundaries.

## QA Test Cases

- **AC-1/2:** Parse the baseline, ending labels, resolver map, completion
  calls/events, and epilogue source; assert exact invariant sets and order.
- **AC-3:** Assert the tail is inside the existing rain-stops label, after
  lights-out completion, contains an ordinary-observer marker and a written-
  note marker, and has no `erii` speech line.
- **AC-4/5:** Scan the changed source and baseline for new choices, IDs,
  state/achievement/persistence writes, asset paths, named extra-world-state
  claims, and canonical-unit count changes.
- **AC-6:** Run focused Story 025 tests, full Python, Ren'Py global, lint/
  compile, Erii constraints, source hashes/content lock, and diff check.

## Performance / Engine Notes

No performance impact is expected: this is a short text-only continuation
using existing Ren'Py narration and the existing `bg warm_room` primitive.
No new engine API is used. Runtime execution remains non-timed and keyboard-
independent; manual timing/performance observation is deferred.

## Control Manifest Constraints

- Feature-layer required rules: keep chapter prose in the existing chapter
  file, keep stable labels/IDs, and express complex Erii intent through
  approved non-spoken presentation.
- Feature-layer forbidden rules: no duplicated ending conditions, no new
  hidden-state narrative input, no complete spoken Erii sentences, and no
  achievement/ending proxy logic.
- Manifest version checked: `2026-08-04.1`.

## Test Evidence

- `tests/integration/sys_narrative/rain_stops_tail_test.py`
- `production/qa/evidence/rain-stops-tail-2026-08-14.md`

## Definition of Done

- [x] All acceptance criteria are covered by automated tests or explicitly
  documented deferred/manual evidence.
- [x] Story-specific Integration test exists at the exact path above and
  passes; full Python/Ren'Py/lint/content checks pass.
- [x] Content-lock v2 records final source identities and the no-copy design
  boundary; no asset directory is changed.
- [x] Code review is APPROVED WITH SUGGESTIONS with no blocking
  ADR/GDD deviation.
- [x] Story is marked Complete only after `/story-done`; manual review remains
  noted rather than fabricated.

## Completion Notes

- Automated implementation boundary closed on 2026-08-14.
- Focused integration suite: 7/7 PASS; full Python suite: 288/288 PASS.
- Ren'Py global: 56/56 testcases and 474/474 assertions PASS; lint/compile and
  Erii constraints PASS.
- Content-lock v2 now binds the final 105-line `game/chapters/endings.rpy`
  source identity and the v1.3 baseline hash.
- Review suggestions were resolved by exact current-hash enforcement and
  frozen token/qualification/predicate/witness assertions.
- Manual GUI/playtest/SAPI/semantic/copyright/subjective checks remain
  explicitly deferred and are not a Polish gate PASS.
