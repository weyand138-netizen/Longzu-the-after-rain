# ADR-0004: Semantic Ending Snapshot and Rollback State Envelope

## Status

Accepted

Amended through the SYS-ENDING targeted axis/history-replay, detectable ending-lifecycle and input-byte-complexity closure on 2026-07-27; synchronized with ADR-0006 ending completion boundary on 2026-08-09.

## Date

2026-07-23

## Engine Compatibility

| Field | Value |
|---|---|
| **Engine** | Ren'Py 8.5.3 |
| **Domain** | Core / Scripting |
| **Knowledge Risk** | HIGH — pinned engine post-dates the baseline |
| **References Consulted** | `docs/engine-reference/renpy/VERSION.md`, pinned SDK `doc/save_load_rollback.html`, ADR-0001, ADR-0002 |
| **Post-Cutoff APIs Used** | None; uses established `default`, rollback, save/load, `after_load`, and pure Python boundaries |
| **Verification Required** | Save/load/rollback coherence, active sentinel checks, two-pass validation precedence, immutable import transfer, detached snapshot purity, explicit unsupported-schema failure |

## ADR Dependencies

| Field | Value |
|---|---|
| **Depends On** | ADR-0001, ADR-0002 |
| **Enables** | `SYS-STATE` approval; later `SYS-ENDING`, `SYS-SAVE`, and `SYS-TEST` GDDs; completion event stays rollback-owned |
| **Blocks** | `SYS-ENDING` design and Core implementation stories until synchronized |
| **Ordering Note** | GDD, Master Architecture, resolver contract, and tests must move together |

## Context

### Problem Statement

Five axes only increase and cap at 3. If ending resolution reads only those five final integers, later contradictory behavior is forgotten: a player can establish autonomy early, repeatedly override Erii later, and still retain the same true-ending input. The prior GDD also described strict validation and atomic commit while the Master Architecture still specified clamping, a `None` return, separate store variables, and an axes-only snapshot.

### Constraints

- Ren'Py must own all rollback-active mutable state.
- Imported Python may perform pure computation but may not own live store state.
- Five axes remain hidden, monotonic positive-evidence counters in domain `0–3`.
- Ending resolution remains deterministic, pure, mutually exclusive, and explainable.
- Save data uses primitives and built-in collections only.
- The shipped game remains offline and performs no state I/O from the state adapter.

### Requirements

- Preserve event order so later revoke and repair behavior is distinguishable.
- Commit schema, axes, and history atomically at the design contract level.
- Use one validation order and one error oracle across write, snapshot, and load.
- Keep snapshots detached from live Ren'Py state.
- Make unsupported development saves fail explicitly.

## Decision

The rollback-owned unit is one exact rollback-transformed `RunMap` named `semantic_state`. `RunMap` and `RunList` are concrete contract aliases for the runtime types produced by `{}` and `[]` inside Ren'Py 8.5.3 `.rpy` Python; arbitrary Mapping/Sequence implementations and imported CPython containers are rejected as live state.

```text
{
  "schema_version": 2,
  "axes": {
    "understanding": 0..3,
    "autonomy": 0..3,
    "truth": 0..3,
    "preparation": 0..3,
    "sacrifice": 0..3
  },
  "choice_history": [stable_choice_id, ...]
}
```

`apply_choice` validates the active lifecycle sentinel and existing envelope, validates the payload, builds a complete candidate locally, and commits with one replacement assignment. It returns stable status `APPLIED` or `DUPLICATE_NOOP`; it never clamps invalid input.

Every production player-facing narrative choice calls this same entry after player confirmation and before immediate reaction. `narrative_only` supplies an empty `RunMap`, so it appends its stable ID without changing axes and inherits the envelope's save/load/rollback behavior.

`current_ending_snapshot` validates the active sentinel and live `RunMap`/`RunList` values entirely on the `.rpy` side. It then extracts only the schema exact int, five axis exact ints in canonical order, and an exact built-in tuple of history exact strings. The imported private `_build_detached_ending_snapshot` receives only those immutable built-ins and creates the detached exact CPython dict/list graph. It is not a public API and may be called only by the validated adapter. A static scan covers all `game/**/*.rpy` and `game/**/*.py`, resolves aliases and the full builder reference/escape closure (assignment, pass/return, closure, container, wrapper, reflection and dynamic lookup), rejects unresolved forms and production-to-test-only leakage, and requires exactly one callsite: `game/10_state.rpy::current_ending_snapshot`. CFG analysis proves active validation dominates that call on every path. Test-only direct fixtures are classified separately and may not export or pass production wrappers. No live `RunMap`, `RunList`, or mutable nested store object crosses the import boundary. Per ADR-0005, the pure resolver folds choice IDs into bounded counterevidence and route-fact sets, constructs a complete immutable resolution record, and exposes the string result only through an `.ending_id` wrapper. There is no `grant`; runtime repair legality only asks whether a build-valid target is currently unresolved, while duplicate resource acquire and absent consume are both route-fact-fold `ValueError`s.

Five axes remain positive-evidence counters. They are necessary but not sufficient for outcomes whose meaning can be contradicted later. An unresolved route-critical revoke prevents `rain_stops` even when all axes equal 3.

### Architecture Diagram

```text
chapter choice
  -> apply_choice(id, deltas)
  -> validate live envelope + payload
  -> replace semantic_state once
  -> Ren'Py rollback/save snapshot

Day 7
  -> validate sentinel + live state in .rpy
  -> extract ints + tuple[str, ...]
  -> imported private _build_detached_ending_snapshot(...)
  -> detached {schema, axes, ordered history}
  -> frozen choice-axis replay equals detached axes
  -> pure token/route-fact folds + qualification derivation
  -> freeze cause-ready trace + unresolved audit facts
  -> cause extraction from FrozenResolutionEvaluation only
  -> immutable ending resolution record
  -> record.ending_id
```

### Key Interfaces

```python
apply_choice(
    choice_id: str,
    axis_deltas: RunMap,
) -> Literal["APPLIED", "DUPLICATE_NOOP"]

validate_active_semantic_state(
    sentinel: object,
    state: object,
) -> None

current_ending_snapshot() -> dict[str, object]

_build_detached_ending_snapshot(
    schema_version: int,
    axis_values: tuple[int, int, int, int, int],
    history_ids: tuple[str, ...],
) -> dict[str, object]

resolve_ending_record(
    snapshot: dict[str, object],
) -> EndingResolutionRecord

resolve_ending(
    snapshot: dict[str, object],
) -> str
```

Validation remains two-pass, finite, and schema-known. Resolver stages freeze atomic template/polarity/kind/source identity plus value/anchors and freeze audit template identity with exact `audit`/`unresolved_counterevidence`/`unresolved_token` values into `FrozenResolutionEvaluation`; cause extraction has no snapshot/catalog/evaluator input. Concrete record module/qualname/field order is fixed. A source-hash-verified test-only AST build observes nine stage counts, clause counts, wrapper canonical-call count and field reads; it is excluded from production. Purity policy v2 covers explicit calls, CPython 3.12 implicit opcode/operand dispatch, exact record constructors and frozen-code exception construction. The wrapper may transitively reach helpers only through its one canonical call.

Component evidence uses canonical machine IDs `UT_ENGINE`, `UT_PURE`, `INSTR`, `STATIC`, and `BRANCH`. Atomic replacement has assignment instrumentation; the Ren'Py delta helper uses `UT_ENGINE`; shared primitives require a static callgraph; private status links `STATE-COMP-022` to the full export/escape scan in `023`. Private-builder misuse is covered both dynamically for invalid arguments and statically for production callers.

## Alternatives Considered

### Axes-Only Snapshot

- **Description**: Keep the existing five integers as the only ending input.
- **Pros**: Smallest API and existing implementation.
- **Cons**: Forgets all later contradictory behavior once an axis caps.
- **Rejection Reason**: Violates the complete-causal-chain pillar and permits semantically false true endings.

### Negative Axis Deltas

- **Description**: Let reverse behavior subtract from five axes.
- **Pros**: Resolver remains axes-only.
- **Cons**: Converts semantic evidence into a hidden morality balance, obscures which behavior caused the loss, and weakens rollback/content explanation.
- **Rejection Reason**: Conflicts with the approved positive-evidence model and anti-hidden-score goal.

### Independent Mutable Qualification Flags

- **Description**: Store current booleans next to axes and let choices flip them.
- **Pros**: Fast resolution.
- **Cons**: Duplicates derivable state, adds rollback synchronization risk, and erases the ordered reason a flag changed.
- **Rejection Reason**: Ordered history is already required for narrative payoff and is the authoritative source.

## Consequences

### Positive

- Later reverse behavior remains meaningful after axis caps.
- Ending explanations can cite exact events and explicit repairs.
- Save/load/rollback restore one coherent semantic unit.
- API, GDD, ADRs, and Master Architecture share one test oracle.

### Negative

- Resolver validation and tests become more involved.
- Content must maintain a stable bounded counterevidence catalog alongside choice IDs.
- Pre-remediation development saves are intentionally incompatible.

### Risks

- A catalog entry may drift from narrative metadata. Mitigation: compile from one machine-readable content source and fail on missing or duplicate IDs.
- One state dict may be mutated in place accidentally. Mitigation: code review rule and replacement-assignment tests.
- Counterevidence may become a second hidden checklist. Mitigation: ADR-0005 removes `grant`, caps tokens at ten total/two per domain, and requires event-specific one-to-one repair.

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|---|---|---|
| `five-axis-state.md` | Complete causal chain determines ending | Adds ordered history to ending input |
| `five-axis-state.md` | Atomic rollback-compatible state update | Defines one replacement-owned state envelope |
| `five-axis-state.md` | Strict validation and observable errors | Defines exact types, order, and error classes |
| `game-concept.md` | True ending requires five complete causal dimensions | Prevents capped axes from masking unresolved reverse behavior |

## Performance Implications

- **CPU**: `O(B_in + P + Q + C + B + L·R log R + L·F log F + K log K)` once at ending resolution; `B_in` is total inspected input/catalog ID bytes, `L=max(1,max sorted source/fact stable-ID byte length)` and `R` includes qualification contributor references.
- **Resolver memory**: `O(B_in + P + Q + C + B + R + F + K)` including frozen qualification contributors and cause-ready artifacts.
- **Memory**: One stable string per selected major choice; bounded by authored content.
- **Load Time**: One linear validation of the saved history in `after_load`.
- **Network**: None.

## Migration Plan

1. Treat all existing schema-less/schema 1 saves as development-only and explicitly incompatible.
2. Replace separate store variables with schema 2 `semantic_state` when implementation begins.
3. Update state tests, Ren'Py flow tests, ending vectors, and content validation together.
4. Do not ship schema 3 or later without a separate accepted migration ADR and fixtures for every supported public version.

## Validation Criteria

- A reverse autonomy event after `autonomy == 3` prevents `rain_stops` until an explicit repair appears later in history.
- Save/load/rollback reproduce schema, axes, and ordered history at one coherent point using the pinned engine's rollback-transformed containers.
- Catalog coverage replays frozen per-choice axis projections and rejects any detached snapshot whose axes are not the exact replay result; this supplies source contributors for ending causes without adding live inputs.
- Every public failure case has one deterministic `TypeError` or `ValueError` oracle and leaves live state deep-value equivalent.
- Static analysis finds exactly one production builder call, proves active validation dominates it, and rejects every symbol escape, unresolved reflection/dynamic lookup, wrapper export, and production-to-test-only path.
- Component evidence host/types prove atomic replacement count, Ren'Py helper behavior, shared-primitive callgraph, and private non-export status with the required evidence rather than unit-test labels alone.
- Mutating any returned snapshot field cannot affect live state or a later snapshot.
- All six canonical paths resolve uniquely from axes plus history.

## Related Decisions

- [ADR-0001](adr-0001-deterministic-ending-resolution.md)
- [ADR-0002](adr-0002-rollback-and-persistence-boundary.md)
- [SYS-STATE GDD](../../design/gdd/five-axis-state.md)
