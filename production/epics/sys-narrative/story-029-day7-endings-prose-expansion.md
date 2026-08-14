# Story 029: Day 7, Endings, and `rain_stops` Prose Expansion

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Complete
> **Layer**: Feature
> **Type**: Content
> **Estimate**: 3 days
> **Last Updated**: 2026-08-14
> **Manifest Version**: 2026-08-04.1

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Baseline**: `design/narrative/seven-day-content-baseline.md` — `narrative_content_baseline:v1.4`
**Requirements**: `TR-NAR-001`
**Governing ADRs**: ADR-0003, ADR-0006, ADR-0008
**Design impact**: `docs/architecture/change-impact-2026-08-14-prose-expansion.md`
**Dependencies**: Story 028 — Complete; Story 025 — Complete
**Sprint**: `production/sprints/sprint-012.md`
**Engine**: Ren'Py 8.5.3 | **Risk**: Medium/High

Expand only existing Day 7, six ending, and existing `rain_stops` epilogue
labels. Preserve the resolver handoff, ending IDs, priority, canonical
witnesses, five-axis/token/qualification predicates, completion boundary, and
the Story 025 ordinary-observer/written-note tail constraints.

## Acceptance Criteria

- [x] Existing labels, ending IDs, resolver calls, priority, witness history,
  axis/token/resource effects, qualification predicates and completion writes
  are unchanged and remain in their original order.
- [x] Added text enriches Day 7 causal recall, each existing ending's immediate
  consequence, and the existing rain-stops arcade tail without adding canon
  facts, new routes, or ending predictions.
- [x] No new choice/menu/apply_choice/state write/jump/call/scene/asset or
  active character is added; no new canonical unit or completion event exists.
- [x] `rain_stops` still has only the existing epilogue tail after lights-out;
  the observer remains ordinary/unnamed and complex Erii content remains a
  clearly marked written note, never complete spoken dialogue.
- [x] Content-lock v6 binds final Day 7/endings hashes and the v1.4 baseline.
- [x] Focused/full Python, Ren'Py global, lint/compile, Erii constraints and
  diff check pass; manual review remains NOT RUN.

## Implementation Boundary

- Modify only `game/chapters/day7.rpy` and `game/chapters/endings.rpy` for
  player-facing prose, plus direct source identities, structural tests, sprint
  status and QA records.
- Keep completion calls and the `rain_stops` post-lights-out tail order intact;
  additions must not interrupt state-sensitive terminal assertions.
- Do not add images, audio, voice, UI bitmap, active character, canonical unit,
  route, ending, achievement, Gallery, persistent field, or world-state fact.

## QA Test Cases

- **AC-1:** exact Day 7 handoff and all six ending control/completion signatures.
- **AC-2:** additions are local, player-safe, and contain no hidden-rule or
  ending-predicate vocabulary or asset references.
- **AC-3:** no new control nodes, state writes, labels, jumps/calls, scenes,
  active characters, canonical units, or completion events.
- **AC-4:** content-lock v6 binds final Day 7/endings hashes and line counts.
- **AC-5:** focused/full engine and content checks with explicit human
  deferral, including the Story 025 written-note/observer boundary.

## Test Evidence

- `tests/integration/sys_narrative/prose_expansion_sprint012_test.py`
- `production/qa/evidence/prose-expansion-sprint-012-2026-08-14.md`
- `production/qa/evidence/prose-expansion-sprint-012-code-review-2026-08-14.md`

## Definition of Done

- [x] Readiness, implementation, review, story-done, smoke and team QA complete.
- [x] Local close commit exists with no asset or stage changes.

## Completion Notes

- Closed 2026-08-14 after readiness, implementation, code review, story-done,
  smoke and solo team-QA records were written.
- Focused structural suite: 3/3 PASS; full Python suite: 300/300 PASS.
- Ren'Py global: 56/56 testcases and 474/474 assertions PASS; lint/compile,
  Erii constraints, compileall, and diff check PASS.
- Content-lock v6 binds the final Day 7/endings source identities. The six
  ending IDs, resolver handoff, terminal completion boundary, and Story 025
  observer/written-note tail contract remain unchanged.
- GUI/playtest/SAPI/semantic/copyright/subjective/performance/正典 checks
  remain NOT RUN. Polish promotion and `production/stage.txt` changes remain
  blocked.
