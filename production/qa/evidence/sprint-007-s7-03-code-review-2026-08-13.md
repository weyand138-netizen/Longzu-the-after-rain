# Code Review: Sprint 7 Story 003 Six Ending Closures and Rain-Stops Epilogue

**Date**: 2026-08-13
**Review mode**: solo
**Story**: S7-03 / `TR-END-005`

## Reviewed Surface

- `game/chapters/endings.rpy`
- `game/testcases.rpy`
- `tests/integration/sys_ending/ending_closure_source_test.py`
- `production/qa/evidence/story-readiness-s7-03-2026-08-13.md`

## Findings and Resolution

| Severity | Finding | Resolution |
| --- | --- | --- |
| P1 (resolved) | Initial engine assertions attempted to observe terminal state after a direct-jumped label returned; Ren'Py correctly resumed `start`, which reset run state before the test observed it. | Tests now observe every real label at its first player-visible line after the owned entry transition. The rain path advances into the real epilogue and observes its completion record before epilogue events. Static tests independently prove every completion node follows all visible closure text and occurs exactly once. |
| P2 (resolved) | The first static asset scan treated words in comments and default declarations as active presentation instructions. | The scan now evaluates executable non-comment lines and permits only seven uses of existing code-defined `bg warm_room`; it rejects image/show/audio/movie/transition/menu additions. |

## Review Result

All six mapped labels are real, begin with their exact owned entry operation,
present their frozen semantic closure before one completion boundary, and have no
resolver, choice, token, qualification, or persistent-state access. Only
`ending_rain_stops` jumps after its completion into
`epilogue_rain_stops_arcade`; it contains the existing second-coin/nickname
echo plus the first-guest and lights-out visible event boundaries. The other
five labels return after their own closure.

The source uses only already admitted code-defined `bg warm_room` and standard
accessible dialogue flow. It introduces no external asset, choice, route fact,
predicate, Golden Cage change, or ending-meaning revision. Runtime content stays
under `game/`; no empty `src/` directory was created.

Automated evidence: terminal source suite 11/11; full Python suite 257/257;
Ren'Py 8.5.3.26051504 global suite 52/52 testcases and 431/431 assertions;
`lint --compile`; and `git diff --check` all passed.

## Verdict: APPROVED FOR S7-04
