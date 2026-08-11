# Story 006 Action Gates and Mutex — Engine Evidence

> **Date**: 2026-08-10  
> **Story**: `production/epics/sys-save/story-006-action-gates-mutex.md`  
> **Engine**: Ren'Py 8.5.3.26051504 / Python 3.12.7  
> **Platform**: Windows 11 10.0.22631  
> **Verdict**: PASS

## Implemented Boundary

`game/modules/action_gates.py` exposes a two-phase pure admission contract.
`admit_action_request` returns an immutable claimed `OperationMutexState` and
never invokes an engine callback. The Ren'Py test adapter publishes that state
before entering the callback, so callback-time requests observe the claimed
five-operation mutex. Rejected work has no queue or deferred replay path.

The records used by request, UI, mutex, and admission contracts are frozen
slotted dataclasses. Exact validators return `False` for missing, extra,
unknown, or wrong-type inputs without truthiness or custom protocol dispatch.

## Automated Results

### Story unit contract

Command:

```powershell
python -m unittest tests.unit.sys_save.action_gates_test
```

Result: **14/14 tests passed**, 0 failures, 0 errors.

Coverage includes:

- all 7 registered phases × all 6 request actions;
- all 7 phases × all 5 player-facing UI actions;
- visible/enabled/focusable exact-boolean gates and autosave UI exclusion;
- missing/extra/wrong-type and same-type deleted-field corruption;
- protocol bombs across request fields and each UI visible/enabled/focusable
  flag, with zero truthiness/equality/hash/call dispatch;
- 4 request sources × all 5 player-facing actions during critical interaction;
- all 5 active operations × all 5 immediate callback-time follow-up operations;
- zero queue and no replay after completion.

### Python regression suites

```powershell
python -m unittest discover -s tests -p '*_test.py'
python -m unittest tests.test_ending_rules
```

Results:

- `*_test.py`: **64/64 passed**, 0 failures, 0 errors.
- `tests.test_ending_rules`: **6/6 passed**, 0 failures, 0 errors.

### Ren'Py global testcase suite

Command:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools/run-renpy-tests.ps1 -Suite global -TimeoutSeconds 55
```

Result: **PASS**.

- Test suites: **1/1 passed**.
- Test cases: **11/11 passed**.
- Assertions: **57/57 passed**.
- Total reported time: **0.919 s**.
- `action_gate_mutex_contract`: **passed in 0.091 s**.

The Story 006 testcase proves:

- one accepted request publishes `manual_save` ownership before its callback;
- callback-time nested manual save, quick save, autosave, load, and rollback are
  all denied while the first operation remains active;
- nested denial count is 5, engine invocation count remains 1, and queue length
  remains 0;
- separate single-purpose test screens receive real `keysym` events for quick
  shortcut (`q`), `V`, `Shift+C`, and alternative input (`a`); each action
  records once and returns from its own interaction;
- quick-shortcut and alternative-input requests in `CriticalInteraction` have
  zero engine invocations and zero queue;
- actual `V` and `Shift+C` key events switch only their approved output channel
  and do not add a save/load/rollback invocation;
- a `CriticalInteraction` player action with a false UI flag is not constructed:
  `renpy.get_displayable("action_gate_unavailable_ui_surface",
  "action_gate_unavailable") is None`, proving the unavailable action has no
  displayable or focus target on the engine surface.

### Ren'Py lint and compilation

Command:

```powershell
renpy.py E:\Longzu lint --compile
```

Result: **exit code 0**, no lint or compile errors. The report identified 19
screens, including the single-purpose test-only action-gate surfaces.

## Performance Boundary

The gate uses only fixed-size closed tuples/dicts and exact scalar/record checks.
It performs no I/O, no network work, and no per-frame scan. Interactive frame
performance was **not profiled** by this automated run; the 16.6 ms confirmation
remains a manual smoke item. Dedicated SAVE-PERF frame instrumentation remains
outside this story's pure action-gate scope.

## Ownership and Packaging

The production pure module owns no Ren'Py store, persistent, rollback, queue, or
global mutable runtime state. `_ActionGateEngineTestAdapter`, its observer, and
the test screen exist only in `game/testcases.rpy` as testcase evidence and are
not production action-gate state.
