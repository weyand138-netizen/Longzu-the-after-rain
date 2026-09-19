# Team QA Sign-off — Sprint 008 / Story 025

**Date**: 2026-08-14
**Review mode**: solo
**Scope**: `rain_stops` in-unit years-later tail
**Verdict**: **APPROVED WITH CONDITIONS**

## Objective evidence

| Area | Result | Record |
|---|---|---|
| Story readiness | PASS | Story 025 contains GDD/baseline, TRs, ADRs, control-manifest constraints, estimate, dependencies, ACs and exact test-evidence paths. |
| Implementation | PASS | Only the existing `epilogue_rain_stops_arcade` tail and its focused integration test were added for the feature. |
| Focused Python | PASS — 7/7 | `tests/integration/sys_narrative/rain_stops_tail_test.py` |
| Full Python | PASS — 288/288 | `uv run python -m unittest discover -s tests -p '*_test.py'` |
| Ren'Py global | PASS — 56/56 testcases, 474/474 assertions | `tools/run-renpy-tests.ps1 -Suite global -TimeoutSeconds 120` |
| Lint/compile | PASS | Ren'Py 8.5.3 pinned SDK |
| Content constraints | PASS | `tools/test-content-constraints.ps1` |
| Smoke | PASS WITH WARNINGS | `production/qa/smoke-sprint-008-2026-08-14.md` |
| Code review | APPROVED WITH SUGGESTIONS | Exact current hash and frozen contract assertions are present; no blocking ADR/GDD deviation remains. |

## Conditions retained

The following are not run and are not claimed as PASS: non-test GUI start,
manual playtest, SAPI listening, semantic-equivalence review, copyright/source
review, subjective narrative/readability review, performance observation, and
final narrative/正典 sign-off. These conditions block Polish promotion but do
not block this scoped automated Story 025 close-out.

No asset directory, audio/voice/UI bitmap path, or `production/stage.txt` was
changed.
