# Code Review: Sprint 7 Story 002 Terminal Lifecycle and Completion Boundary

**Date**: 2026-08-13
**Review mode**: solo
**Story**: S7-02 / `TR-END-002`, `TR-END-004`

## Reviewed Surface

- `game/10_state.rpy`
- `game/modules/ending_completion_projection.py`
- `game/chapters/day4.rpy` and `game/chapters/day6.rpy`
- `game/testcases.rpy`
- `tests/integration/sys_ending/terminal_lifecycle_source_test.py`
- `production/qa/evidence/s7-02-runtime-state-revalidation-2026-08-13.md`

## Findings and Resolution

| Severity | Finding | Resolution |
| --- | --- | --- |
| P1 (resolved) | A one-time durable completion was invoked inside `assert eval`; Ren'Py may evaluate such an expression again while reporting, so the test could replay the action itself. | The testcase invokes the boundary once through `Function`, then asserts only observable ADR-0006 state. |
| P1 (resolved) | The load-safe boundary originally did not prove a stored completion event matched the durable root. | It now validates type, pending ending, event/checkpoint identity, epoch, catalog, ADR-0006 fields, and durable membership before returning from `after_load`. |
| P1 (resolved) | A review patch briefly rejected the contractually valid `Active + pending ID + no event` resolver-handoff state. | The final validator permits that staging state and rejects only an `Active` completion event; an engine assertion and source check cover it. |

## Review Result

Schema-2 `semantic_state` is the single rollback-owned semantic unit. The sole
adapter validates it, builds one detached snapshot, calls the canonical resolver
once, and maps only its six frozen IDs to stable labels. Entry changes lifecycle
only through `commit_ending_entry`; completion uses the existing durable
coordinator once and preserves duplicate no-op behavior. Day 4/Day 6 read
history only through the validated state accessor.

No ending prose or label implementation is claimed here: materialising the six
mapped labels and the rain-only epilogue is explicitly S7-03 work. The runtime
implementation root remains `game/`; no empty `src/` directory was created.

Automated evidence: focused terminal source suite 6/6; full Python suite
252/252; Ren'Py 8.5.3.26051504 global suite 46/46 testcases and 405/405
assertions; `lint --compile`; and `git diff --check` all passed.

## Verdict: APPROVED FOR S7-03
