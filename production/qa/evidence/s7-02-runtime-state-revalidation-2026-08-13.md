# S7-02 Runtime State Revalidation

**Date:** 2026-08-13
**Story:** S7-02 — Terminal Lifecycle and Completion Boundary
**Reason:** Schema-2 integration moves all Day 4/Day 6 history membership
reads from legacy standalone state to the validated `semantic_state` envelope.
This is a runtime-state access correction record whose Day 4 source identity is
refreshed again for the later Sprint 010 prose-only expansion; no Day 4/Day 6
choice, reaction, payoff, route fact, asset, or ending predicate is changed.

## Current source identities

| Artifact | SHA-256 |
|---|---|
| `game/10_state.rpy` | `ff0444e7a0c129fafc15e7cf6f49771288e5720ce233a0523953385415049e34` |
| `game/chapters/day5.rpy` | `2d1de1d4f10c3fea6df9c514eb7deeba52a4561705328812f30d718eff9d4c05` |
| `game/chapters/day4.rpy` | `3ba9867967660d9aeeb16354ed8f0ed0e264f88c2b4761e4b61ef083e9435a4b` |
| `game/chapters/day6.rpy` | `dbe1f47ce705bc73520c0aa3b6115cd2f803f292605dd2b79a2854adf0ff98be` |
| `game/testcases.rpy` | `3824e0756da12701a0ff7cb018c0ff9a80953bd82892bdbc21d0cce5147982d6` |

## Objective revalidation

- Focused S7-02 static/integration suite: 6/6 PASS.
- Full Python suite: 252/252 PASS.
- Pinned Ren'Py 8.5.3 global suite: 46/46 testcases, 405/405 assertions,
  PASSED.
- Historical Day 4 and Day 6 evidence directories remain preserved and are not
  overwritten. Their original capture hashes continue to describe the same
  admitted visual surfaces; this state-only change adds no player-visible
  source or presentation primitive.
- The shared testcase fixture was later extended by S7-03 terminal-flow cases
  and S6-01's owned Day 7 handoff case. This row binds its current source
  identity only; it does not rewrite the historical Day 4/Day 6 capture
  evidence or their stated verification runs.

## Boundary confirmation

`semantic_state` is the single rollback-owned mutable semantic unit. The
schema-2 adapter is the only production caller of the private detached snapshot
builder; all Day 4/Day 6 membership guards use `current_choice_history()`.
The legacy axes-only resolver call is removed. No `src/` directory is used:
this Ren'Py project's runtime root is `game/`.

The safe-load boundary additionally validates a present rollback-owned
`ending_completion_event_record` against its pending ending ID, exact ADR-0006
identity fields, persistent epoch/catalog, and durable ending membership. A
rollback snapshot from before completion may still have no event while retaining
an already-flushed membership, so that valid replay path remains unmodified.
The approved `Active + pending ending ID + no event` resolver-handoff state is
also explicitly valid; only an `Active` completion event is malformed.
