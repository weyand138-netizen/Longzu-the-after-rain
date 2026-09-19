# Story 027: Day 3–4 Prose Expansion

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
**Dependencies**: Story 026 — Complete
**Sprint**: `production/sprints/sprint-010.md`

Expand only existing Day 3 and Day 4 scene prose. Preserve the evidence/pause
transaction, ticket/contact preparation, qualification guards, and all current
choice/state contracts.

## Acceptance Criteria

- [x] Existing labels, menu/choice order, axis deltas, token/resource effects,
  agency answer IDs, qualification guards and chapter boundary are unchanged.
- [x] Added text enriches the empty-school evidence, pause response, ticket,
  route and contact observations without exposing hidden state or predicting an
  ending.
- [x] No new label/menu/apply_choice/state write/jump/call/scene/asset or active
  character is added.
- [x] Content-lock v4 binds current Day 3/Day 4 hashes and the v1.4 baseline.
- [x] Focused/full Python, Ren'Py global, lint/compile, Erii constraints and
  diff check pass; manual review remains NOT RUN.

## Test Evidence

- `tests/integration/sys_narrative/prose_expansion_sprint010_test.py`
- `production/qa/evidence/prose-expansion-sprint-010-2026-08-14.md`
- `production/qa/evidence/prose-expansion-sprint-010-code-review-2026-08-14.md`

## Definition of Done

- [x] Readiness, implementation, review, story-done, smoke and team QA complete.
- [x] Local close commit exists with no asset or stage changes.

## Completion Notes

- Closed 2026-08-14 after readiness, implementation, code review, story-done,
  smoke and solo team-QA records were written.
- Focused structural suite: 3/3 PASS; full Python suite: 294/294 PASS.
- Ren'Py global: 56/56 testcases and 474/474 assertions PASS; lint/compile,
  Erii constraints, compileall, and diff check PASS.
- Content-lock v4 binds the final Day 3/Day 4 source identities. The final
  Day 4 source hash was refreshed after the last prose placement correction;
  no control or state contract changed.
- GUI/playtest/SAPI/semantic/copyright/subjective/performance/正典 checks
  remain NOT RUN. Polish promotion and `production/stage.txt` changes remain
  blocked.
