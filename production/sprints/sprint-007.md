# Sprint 7 — 2026-11-02 to 2026-11-15

## Sprint Goal

Close the approved SYS-ENDING dependency that blocks Day 7: deliver the
canonical ordered-history resolver, the single Day 7 lifecycle/completion
boundary, six fixed ending closures, and the existing rain-stops arcade
epilogue without changing any frozen terminal meaning or claiming later scope.

## Capacity

- Total days: 14
- Buffer (20%): 3 days
- Available: 11 days
- Planned critical-path effort: 10 days
- Planned supporting effort: 1 day
- Review mode: Solo

## Tasks

### Must Have (Critical Path)

| ID | Task | Owner | Est. Days | Dependencies | Acceptance Criteria |
|---|---|---:|---:|---|---|
| S7-01 | Canonical schema-2 ending resolution record | Andwey | 4 | frozen SYS-STATE/choice contracts | Replay, folds, qualifications, fixed priority, immutable record, fail-closed pure tests. |
| S7-02 | Terminal lifecycle and completion boundary | Andwey | 3 | S7-01; existing save/persist contracts | One adapter/map/entry transition/completion event with rollback and idempotency evidence. |
| S7-03 | Six ending closures and rain-stops epilogue | Andwey | 3 | S7-02 | Six real labels, frozen closures, completion after closure, rain-only arcade epilogue. |

### Should Have

| ID | Task | Owner | Est. Days | Dependencies | Acceptance Criteria |
|---|---|---:|---:|---|---|
| S7-04 | Terminal validation and traceability | Andwey | 1 | S7-01–S7-03 | One verified generation and honest scope/evidence boundary. |

### Nice to Have

None. Retained capacity must not begin Day 7 prose, terminal full-manifest
enumeration, journal/gallery, external asset work, release, packaging, or
stage promotion.

## Scope Check

**Verdict: PASS — zero unapproved scope delta.** The runtime gaps are approved
SYS-ENDING contract work and the direct blocker to Sprint 6 Day 7. See
`production/qa/evidence/scope-check-sprint-007-terminal-closure-2026-08-13.md`.

## Definition of Done

- [x] All Must Have stories pass readiness, dev, code review, and story-done.
- [x] Resolver, lifecycle, completion, labels, and epilogue conform to the
  frozen GDD/ADR contract and use `game/` as the Ren'Py runtime root.
- [x] Full Python, global Ren'Py, lint/compile, constraints, smoke, and team QA
  evidence pass without weakening tests or acceptance criteria.
- [x] Status, traceability, scope, QA, and sign-off records bind one source
  generation and state the deferred/full-manifest/release exclusions.
- [x] Sprint 6 can move from Blocked to story-readiness after this Sprint's QA
  approval; no project stage promotion occurs here.
