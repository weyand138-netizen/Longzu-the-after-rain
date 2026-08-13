# Story 003: Six Ending Closures and Rain-Stops Epilogue

> **Epic**: SYS-ENDING — Terminal Narrative Closure
> **Status**: Complete
> **Layer**: Feature
> **Type**: Config/Data
> **Estimate**: 3 days
> **Last Updated**: 2026-08-13

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`,
`design/gdd/deterministic-ending-resolution.md`
**Requirement**: `TR-END-005`
**Governing ADRs**: ADR-0003, ADR-0006, ADR-0008
**Engine**: Ren'Py 8.5.3 | **Risk**: High

Implement the already frozen closures, not new endings: independent continuing
contact, paid shared escape, solo separation, safety-over-autonomy return,
unexecutable-route postcard tragedy, and the rain-stops ordinary future. Only
the approved rain-stops path continues into its arcade epilogue.

## Acceptance Criteria

- [x] Add six real stable labels named exactly by `ENDING_LABEL_MAP`; each
  begins with the owned entry helper, contains player-visible closure before
  its unique completion node, and has no selector/predicate/persistent copy.
- [x] Preserve the approved meaning of every ending, including the named loss
  or agency outcome, rather than turning a tragedy into a retry, repair token,
  hidden qualification, or altered route.
- [x] `ending_rain_stops` transitions only after its terminal completion into
  `epilogue_rain_stops_arcade`, which presents the frozen second-coin/nickname
  echo, first guest, and lights-out ordinary-future closure.
- [x] Use only existing admitted project runtime presentation primitives under
  `game/`; no external, official, generated, unregistered, or planned assets
  are added or implied.
- [x] Automated text/source and engine-flow tests prove label identity, entry
  and completion order, exact epilogue exclusivity, accessible keyboard flow,
  and no hidden internal state exposed to players.

## Out of Scope

Day 7 authored acknowledgement scenes, full terminal-manifest enumeration,
new art/audio/video, journal/gallery UI, achievements beyond existing downstream
events, release packaging, stage change, or any ending-content revision.

## QA Test Cases

- **AC-1/2:** Source tests bind each label to its frozen semantic outcome and
  reject copied selectors, empty labels, or a completion before closure.
- **AC-3:** Engine tests reach all six labels from owned pending IDs and prove
  only rain-stops reaches the arcade epilogue.
- **AC-4/5:** Asset/accessibility tests inspect runtime references, keyboard
  focus, high-contrast/reduced-motion text equivalence, and player-safe copy.

## Dependencies

- Depends on: Story 002 lifecycle and completion boundary.
- Unlocks: Story 004 and execution of Sprint 6 Day 7 stories.

## Readiness Evidence

**Verdict**: READY (2026-08-13). S7-02 is complete and its stable six-label
map exactly matches the frozen IDs. The authoritative narrative baseline binds
each closure to a required outcome meaning; it authorizes no new route fact,
choice, selector, predicate, asset, or ending meaning. `bg warm_room` and
standard text/menu presentation are existing admitted code-defined runtime
primitives. See
`production/qa/evidence/story-readiness-s7-03-2026-08-13.md`.

## Completion Notes

**Completed**: 2026-08-13
**Criteria**: `game/chapters/endings.rpy` contains the six exact stable labels.
Each begins with its matching owned entry transition, contains player-visible
closure before one terminal completion, and contains no duplicated resolver or
state-selection logic. `rain_stops` alone enters the approved ordinary arcade
epilogue after terminal completion; its first-guest and lights-out events follow
their visible scene boundaries.

**Test evidence**: Terminal source suite 11/11; Python 257/257; pinned Ren'Py
global suite 52/52 testcases and 431/431 assertions; `lint --compile`; and
`git diff --check` pass. Code review:
`production/qa/evidence/sprint-007-s7-03-code-review-2026-08-13.md`.
