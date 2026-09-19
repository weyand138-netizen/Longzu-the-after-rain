# Story 028: Day 5–6 Prose Expansion

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
**Dependencies**: Story 027 — Complete
**Sprint**: `production/sprints/sprint-011.md`
**Engine**: Ren'Py 8.5.3 | **Risk**: Medium

Expand only existing Day 5 and Day 6 scene prose. Preserve the family-archive
transaction, route-answer derivation, token repair choices, cost-bearer
transaction, commitment guards, and chapter boundary.

## Acceptance Criteria

- [x] Existing labels, menu/choice order, choice IDs, axis deltas,
  token/resource effects, agency answer IDs, qualification guards and all
  chapter/ending boundaries are unchanged.
- [x] Added text enriches the archive handoff, route response, safehouse
  failure, cost ownership and commitment observations without exposing hidden
  state or predicting an ending.
- [x] No new label/menu/apply_choice/state write/jump/call/scene/asset or active
  character is added.
- [x] Content-lock v5 binds current Day 5/Day 6 hashes and the v1.4 baseline.
- [x] Focused/full Python, Ren'Py global, lint/compile, Erii constraints and
  diff check pass; manual review remains NOT RUN.

## Implementation Boundary

- Modify only `game/chapters/day5.rpy` and `game/chapters/day6.rpy` for prose,
  plus the direct structural test, content-lock, sprint/status and QA records.
- Add narration after relevant existing state writes when a branch has a
  state-sensitive assertion; never move a write or choice surface.
- Do not add images, audio, voice, UI bitmap, new active character, canonical
  unit, hidden rule, route, ending, or asset-register entry.

## QA Test Cases

- **AC-1:** exact Day 5/Day 6 choice, effect, state, agency, guard, and control
  signatures.
- **AC-2:** prose additions are local to approved labels and contain no internal
  axis/token/qualification/ending vocabulary or asset references.
- **AC-3:** no new control nodes, state writes, labels, jumps/calls, scenes or
  active character presentation.
- **AC-4:** content-lock v5 binds final source hashes and line counts.
- **AC-5:** focused/full engine and content checks with explicit human deferral.

## Definition of Done

- [x] Readiness, implementation, review, story-done, smoke and team QA complete.
- [x] Local close commit exists with no asset or stage changes.

## Completion Notes

- Closed 2026-08-14 after readiness, implementation, code review, story-done,
  smoke and solo team-QA records were written.
- Focused structural suite: 3/3 PASS; full Python suite: 297/297 PASS.
- Ren'Py global: 56/56 testcases and 474/474 assertions PASS; lint/compile,
  Erii constraints, compileall, and diff check PASS.
- Content-lock v5 binds the final Day 5/Day 6 source identities. Direct source
  generation and revalidation records were refreshed; historical evidence
  remains identified as historical rather than silently rewritten.
- GUI/playtest/SAPI/semantic/copyright/subjective/performance/正典 checks
  remain NOT RUN. Polish promotion and `production/stage.txt` changes remain
  blocked.
