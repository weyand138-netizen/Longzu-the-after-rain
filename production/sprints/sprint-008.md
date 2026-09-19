# Sprint 8 — 2026-08-15 to 2026-08-16

## Sprint Goal

Implement and objectively verify the scoped `rain_stops` years-later tail
without changing any ending/state contract or creating asset work.

## Capacity

- Total days: 2
- Buffer (20%): 0.4 days
- Available: 1.6 days
- Review mode: Solo

## Tasks

### Must Have (Critical Path)

| ID | Task | Owner | Est. Days | Dependencies | Acceptance Criteria |
|---|---|---:|---:|---|---|
| S8-01 | Story 025 — `rain_stops` years-later tail | Andwey | 2 | SYS-ENDING Story 003; Story 024 | Existing epilogue only; two structural viewpoints; no new canonical/state/asset contract; focused and full evidence pass. |

### Should Have

None. Human narrative/copyright/accessibility review is explicitly deferred.

### Nice to Have

None. Do not pull in prose for other days, assets, UI bitmaps, audio, voice,
Gallery, achievements, or stage/polish work.

## Scope Check

**Verdict**: PASS — design impact is limited to the existing `rain_stops`
epilogue unit and does not add a choice, route, ending, achievement, Gallery,
persistent field, canonical unit, or asset identity. Re-run `/scope-check`
after implementation if any file outside Story 025's stated boundary changes.

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Reference wording or named-world-state claims leak into source | Medium | High | Use only high-level structure; static forbidden-term/source-boundary tests; no line-by-line copy. |
| Written note is presented as spoken Erii dialogue | Medium | High | Explicit written-note marker; no `erii` line; Erii constraint scan. |
| Completion or ending semantics move while adding prose | Low | High | Assert existing call/event order and six-ending map; review ADR-0006. |
| Human review gap is mistaken for PASS | High | High | QA/smoke/gate reports keep manual items deferred and block Polish. |

## QA Plan

`production/qa/qa-plan-sprint-008-2026-08-14.md` must exist before
implementation begins.

## Definition of Done

- [x] Story 025 passes readiness.
- [x] Story 025 implementation and integration tests pass.
- [x] Full Python, Ren'Py global, lint/compile, Erii constraints, source
  identity and diff checks pass.
- [x] Smoke report is PASS WITH WARNINGS at most, explicitly retaining the
  deferred GUI/performance checks.
- [x] QA sign-off records automated approval with human review deferred.
- [x] Code review and story-done are complete; story marked Complete with notes.
- [x] No assets or `production/stage.txt` are changed.
