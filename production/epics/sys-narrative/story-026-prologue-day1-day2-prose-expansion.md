# Story 026: Prologue and Day 1–2 Prose Expansion

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
**Governing ADRs**: ADR-0003, ADR-0008
**Design impact**: `docs/architecture/change-impact-2026-08-14-prose-expansion.md`
**Sprint**: `production/sprints/sprint-009.md`
**Engine**: Ren'Py 8.5.3 | **Risk**: Low/Medium

Expand only existing Prologue, Day 1 and Day 2 scene prose. The work may add
physical action, observation, immediate reaction, transitions, and already
frozen payoff texture. It must not change any control contract or add assets.

## Acceptance Criteria

- [x] Existing labels, menu count/order, choice ID order, axis deltas, token
  effects, resource writes, chapter-completion boundary, and next-chapter flow
  are unchanged.
- [x] New text is limited to existing Prologue/Day 1–2 labels and uses only
  narrator or already-existing character presentation; no new active character.
- [x] Expansion enriches the station/train transition, clothing/food/receipt
  observation, alias/game-token beats, and immediate consequences without
  explaining hidden state or predicting a route/ending.
- [x] No new `label`, `menu`, `apply_choice`, `$` state write, `jump`, `call`,
  `scene`, `show`, `hide`, image, audio, music, voice, or UI asset is added.
- [x] Content-lock v3 records the final hashes for the affected chapter files
  and the v1.4 baseline; no unrelated source hash is silently changed.
- [x] Focused and full Python tests, Ren'Py global tests, lint/compile, Erii
  constraints and `git diff --check` pass. Manual playtest, SAPI/semantic,
  copyright and subjective review remain NOT RUN.

## Implementation Notes

- Modify only `game/chapters/prologue.rpy`, `game/chapters/day1.rpy`, and
  `game/chapters/day2.rpy` for player-facing prose, plus the direct test,
  content-lock, sprint/status and QA evidence files.
- Keep all existing `apply_choice` calls and state writes byte-for-byte in
  order; prose additions must sit around existing beats.
- Do not add images, audio, voice, UI bitmap, or formal asset-register work.

## Out of Scope

Day 3 onward, endings, route logic, hidden rules, choice IDs, balance changes,
new characters, new canonical units, asset production, manual playtest, SAPI,
copyright/正典裁决, Polish promotion, and stage changes.

## Dependencies

- Story 025 — Complete
- `docs/architecture/change-impact-2026-08-14-prose-expansion.md` — reviewed
- ADR-0003, ADR-0008 — Accepted

## QA Test Cases

- **AC-1:** exact control skeleton and choice/axis/token/resource signatures.
- **AC-2/3:** only approved labels receive new prose; required scene anchors
  and frozen payoff references remain present; internal-state disclosure scan.
- **AC-4:** reject new control nodes, state writes, labels, jumps/calls and
  asset references in the three affected files.
- **AC-5:** require current source hashes in content-lock v3.
- **AC-6:** focused/full engine and content checks with explicit human deferral.

## Test Evidence

- `tests/integration/sys_narrative/prose_expansion_sprint009_test.py`
- `production/qa/evidence/prose-expansion-sprint-009-2026-08-14.md`

## Definition of Done

- [x] Readiness was READY and the QA plan predates implementation.
- [x] Implementation, focused tests, code review, story-done, smoke and team
  QA are recorded.
- [x] Story is Complete only with manual review still explicitly deferred.

## Completion Notes

- Closed 2026-08-14 with prose-only changes in the existing Prologue, Day 1,
  and Day 2 labels.
- Focused structural suite: 3/3 PASS; full Python suite: 291/291 PASS.
- Ren'Py global: 56/56 testcases and 474/474 assertions PASS; lint/compile,
  Erii constraints, compileall, and diff check PASS.
- Content-lock v3 binds the current Prologue/Day 1/Day 2 source hashes and the
  v1.4 baseline hash.
- Existing Day 1/Day 2 direct source evidence was refreshed to the current
  hashes; unrelated historical Day 5/Day 6 evidence remains untracked.
- Manual GUI/playtest/SAPI/semantic/copyright/subjective checks remain NOT RUN.
