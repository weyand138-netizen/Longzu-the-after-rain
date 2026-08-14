# QA Plan: Production End-to-End Orchestrator

**Date**: 2026-08-14
**Review mode**: solo
**Scope**: Story 024 — Production End-to-End Orchestrator
**Engine**: Ren'Py 8.5.3
**Story**: `production/epics/sys-narrative/story-024-production-end-to-end-orchestrator.md`

## Strategy

| Story | Type | Automated Required | Manual Required | Blocker? |
| --- | --- | --- | --- | --- |
| Story 024 — Production End-to-End Orchestrator | Integration | Yes — fixed-order source contract and full regression suite | Advisory — non-test GUI start/performance observation | No for automated handoff |

## Smoke Check

**PASS WITH WARNINGS** — `production/qa/smoke-production-orchestrator-2026-08-14.md`.
Automated source, Python, Ren'Py global, lint/compile, content constraints, and
whitespace checks pass. The report records that a GUI/non-test Production start
and performance observation were not run in this headless pass.

## Automated Test Requirements

- `tests/integration/sys_narrative/production_orchestrator_test.py`
- `uv run python -m unittest discover -s tests -p '*_test.py'`
- `tools/run-renpy-tests.ps1 -Suite global -TimeoutSeconds 120`
- Ren'Py `lint --compile`
- `tools/test-content-constraints.ps1`

## Manual QA Scope

No new player-facing surface or choice was introduced. The advisory manual
follow-up is to start a non-test Production session and observe the existing
chapter-complete handoffs through the fixed chapter order; no state or copy
inspection is required. Performance was not profiled in this cycle.

## Out of Scope

Choice semantics, axes, tokens, resources, qualifications, ending predicates,
ending closures, player copy, persistence semantics, assets, release, and stage
promotion.

## Entry Criteria

- Smoke report exists and is PASS WITH WARNINGS or better.
- Existing Ren'Py global suite and lint/compile are passing.
- Story 024 implementation and integration test are present.
- The change does not modify the frozen semantic contracts.

## Exit Criteria

Automated acceptance criteria pass, no S1/S2 bugs are open, and the only
remaining manual item is documented as an advisory condition.
