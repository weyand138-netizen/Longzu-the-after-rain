# ADR-0005: Counterevidence Ledger and Detectable State Initialization

## Status

Accepted

## Date

2026-07-23

Amended through the SYS-ENDING targeted axis/history-replay, pre-terminal qualification identity, presentation-safe fallback, detectable ending-lifecycle and provisional-downstream-gate closure on 2026-07-27; synchronized with ADR-0006 ending completion boundary on 2026-08-09.

## Engine Compatibility

| Field | Value |
|---|---|
| **Engine** | Ren'Py 8.5.3 |
| **Domain** | Core / Scripting / Save Lifecycle |
| **Knowledge Risk** | HIGH — pinned engine post-dates the baseline |
| **References Consulted** | `docs/engine-reference/renpy/VERSION.md`, pinned SDK `doc/save_load_rollback.html`, Ren'Py special-label documentation, ADR-0001/0002/0004 |
| **Post-Cutoff APIs Used** | None |
| **Verification Required** | Missing-variable default behavior on load, `after_load` routing, rollback coherence, exact detached snapshot validation |

## ADR Dependencies

| Field | Value |
|---|---|
| **Depends On** | ADR-0001, ADR-0002, ADR-0004 |
| **Enables** | Fourth through ninth `SYS-STATE` review remediation; later `SYS-SAVE`, `SYS-ENDING`, `SYS-NARRATIVE`, `SYS-TEST` GDDs |
| **Blocks** | `SYS-ENDING` design and semantic-state implementation stories until synchronized |
| **Ordering Note** | Token metadata, load sentinel, GDD AC, architecture, and tests must move together |

## Context

### Problem Statement

The three-state qualification fold accepted in ADR-0004 had two semantic failures:

- `grant → revoke → grant` restored validity without an explicit repair.
- `revoke_a → revoke_b → repair` collapsed multiple harms into one repaired state.

It also risked becoming a second hidden checklist because no cap limited qualification count or granularity.

The schema 2 load contract was also not detectable as written. Ren'Py can apply `default` values for variables absent from an older save. If `default semantic_state` already contains a valid schema 2 envelope, `after_load` may see a newly supplied valid state and cannot tell that the loaded save had no marker.

### Constraints

- Five axes remain monotonic positive evidence in domain `0–3`.
- Ordered stable choice history remains the sole saved semantic event ledger.
- No extra positive hidden checklist may duplicate the five axes.
- One repair must not erase multiple distinct route-critical harms.
- Old, unsupported, and corrupt saves must never resume into an inconsistent scene.
- Persistent unlocks remain independent from incompatible per-run state.
- Ren'Py owns live rollback state; imported Python receives only immutable exact built-in transfer values or an already detached exact built-in snapshot.

### Requirements

- Preserve every unresolved route-critical reversal until its own explicit repair.
- Bound the number and granularity of counterevidence definitions.
- Prevent reaction/payoff identity from defeating strict-dominance analysis.
- Make missing-marker old saves observable despite Ren'Py `default` behavior.
- Define one safe destination and one deterministic type/value error contract.
- Prevent irreversible counterevidence from becoming a last-choice ending switch.
- Keep validation finite under unknown or cyclic extra values.
- Require every ending to dramatize its decisive causes and higher-priority exclusions.

## Decision

### Event-level counterevidence tokens

Remove the `grant/revoke/repair` qualification state machine. There is no `grant`.

The immutable content catalog maps every major `choice_id` to exactly one of:

- `null`;
- a `revoke` record that creates one globally unique `repairable` or audited `irreversible` token; or
- a `repair` record that targets exactly one known token.

The pure resolver folds ordered history into unresolved set `U`:

```text
U0 = empty
revoke(t): U <- U union {t}
repair(t), t in U: U <- U minus {t}
repair(t) whose build-valid target is absent/already-repaired in this history prefix: ValueError
ordinary choice: U unchanged
```

A positive choice, repeated axis evidence, reaction, payoff, or later `grant`-like event cannot clear a token. `revoke_a → revoke_b → repair_a` leaves `{revoke_b}`.

Counterevidence is bounded:

- exactly five domains, one per semantic axis;
- at most ten revoke-token definitions across the full game;
- at most two token definitions per domain;
- at most one effect per major choice;
- exactly one target per repair.

A repair must occur after the token-specific consequence is observable, match the target token domain, target a token still unresolved on every reaching prefix, and reference one `repair_cost_tag` registered as `kind: repair_cost` with concrete evidence. Unknown target, wrong domain/mode, irreversible target, or any invalid reference fails the pure catalog validator before `_COUNTEREVIDENCE_INDEX` exists and has no normal runtime branch. Runtime fold legality only rejects a build-valid target that is absent because it has not yet been produced or was already resolved. Changing text, showing a new reaction, apologizing without consequence, or repeating the original positive action is not a repair.

Every token declares `resolution_mode`:

- `repairable`: at least one registered repair choice and a complete revoke → visible consequence → still-unresolved pre-repair → removed post-repair witness;
- `irreversible`: no repair; requires an accepted Creative Director approval whose `author_id`/`reviewer_id` resolve through the project identity registry to different `canonical_person_id` values, plus fixed severity criteria. For every reachable prehistory and every continuation, the shortest later-major-choice count is at least two and a later agency node maps every direct `branch_choice_id` to registered `outcome_reference_ids`; at least two branches must change ending selection, character fate, cost bearer, or tragedy closure while the token remains unresolved. Each outcome reference has exact kind, subject, state, source events, and owner. The token also requires token-specific payoff evidence for every reachable ending and may not be created by the Day 7 ending-commit choice.

### Semantic value allowlist

`immediate_reaction_id` and `payoff_ids` never count as unique value in dominance analysis. Production scanning classifies every narrative menu/timed/accessibility-equivalent option as a player-facing choice; only system navigation may be explicitly allowlisted. Every such choice commits through `SYS-STATE.apply_choice` after confirmation and before reaction; `narrative_only` uses an empty `RunMap`, appends history without changing axes, and shares save/load/rollback restoration. Exact reaction/payoff joins, cardinality, proof-kind nullability and reverse event metadata remain a provisional downstream gate owned by `SYS-CHOICE`/`SYS-NARRATIVE`, outside `SYS-STATE` approval.

Only `unique_value_tags` registered as `kind: semantic_value` with a concrete evidence reference may distinguish an option. The choice graph must be a finite DAG. For every reachable prehistory `h`, dominance first proves full continuation-language inclusion `L_A(h) ⊆ L_B(h)`: every legal A suffix must remain executable in the same choice-ID order after B. Only then may it compare aligned prefixes with `U_B(h,s,k) ⊆ U_A(h,s,k)`. Sparse resources use key union/missing zero; incomparable token sets are not ordered; at least one language/token/cost/axis/value dimension improves strictly.

### Frozen catalog construction

Build-time authoring data compiles to an exact tuple of immutable `NamedTuple` records containing only scalars and tuples. Private `_validate_counterevidence_records` validates all IDs, kinds, schemas, caps, domains, modes, and repair references once, then constructs private `_COUNTEREVIDENCE_INDEX` using `types.MappingProxyType`. A failure prevents module initialization, test collection, and build; no partial index exists. Resolver calls validate only snapshot history coverage and fold legality, not frozen catalog schema/reference invariants. Invalid-catalog fixtures call the pure private validator or initialize an isolated module; no runtime mutation, registration, resolver parameter, global replacement, or failure-hook seam exists.

### Six-ending causality records

Every ending owns one frozen acyclic predicate tree. `clause_kind` is closed to `group_all`, `group_any`, and `atomic`; the exact source/comparator table is exhaustive, `required_truth_value` is always true, axis thresholds are 1–3, and constant is allowed only for the `unsent_postcard` true root. `clause_order` is an exact integer, unique and contiguous `0..N-1` per ending with root 0; operands are same-ending only and sorted by order. Cycles, shared/dangling/cross-ending operands, illegal combinations and unreachable clauses fail before freeze. All evaluated nodes execute exactly once without language short-circuit.

Clause cause templates use ending/clause/polarity lineage; unresolved audit templates use token/audit lineage and bind the runtime selected ending, token and revoke choice. The exhaustive payload matrix freezes contributor selection, values and anchors for every source/comparator/result; an axis match uses the earliest required actual increments. Runtime still uses typed `cause_payload_v1` full SHA-256 and the two approved golden vectors. An isolated build-layer payload↔digest bijection checker accepts synthetic collision pairs without replacing or injecting the production hash leaf.

`resolve_ending_record` is the single canonical pass. Exact `ending_rules` module/qualname/field orders cover four returned records plus `UnresolvedAuditFact` and `FrozenResolutionEvaluation`. Atomic trace entries freeze template/polarity/kind/source identity plus source/value/anchor data; audit facts freeze template identity and exact `audit`/`unresolved_counterevidence`/`unresolved_token` values. Cause extraction accepts the frozen artifact only. The wrapper's “no helper” rule excludes helpers reached through its sole canonical call. A source-hash-verified test-only AST copy returns a fixed observation record and is absent from production imports/package.

Canonical witnesses are only the minimum reachability set. `SYS-ENDING`/`SYS-NARRATIVE` partition every legal terminal path into `terminal_cause_equivalence_class` records whose stable signature is ending ID plus total-order-key-sorted matched/exclusion causes, history-ordered unresolved token IDs, and stable-ID-sorted character fates, cost bearers, and tragedy closure. A changed signature creates a distinct class with at least one witness, applicable payoff scene, and player summary. Per ending, 1–6 classes is the target, 7–12 triggers Producer/Creative Director scope review, and more than 12 fails content build; signature distinctions may not be merged to meet budget.

Runtime display consumes only causes whose `player_summary_id` passed build-time spoiler/anti-hidden-score validation. Five non-fallback endings begin with a presentation-safe matched anchor. `unsent_postcard` keeps its constant fallback match in audit data but begins presentation with an existing concrete failure/unresolved cause selected by the frozen postcard anchor order. Core resolver approval freezes this algorithm; production bindings, full path/class enumeration, summaries and benchmarks remain downstream gates.

### Route qualification derivation

Formal route qualifications are pure predicates over ordered stable choice IDs and event/resource facts reconstructed from that same history. They describe only pre-terminal commitments, resources and constraints; selected-ending fate/payoff outcomes cannot be qualification sources. A frozen private projection catalog maps every formal choice to axis deltas, completed event IDs and resource acquire/consume effects. Catalog coverage replays axis deltas from zero with the canonical cap rule and requires exact equality with snapshot axes before token fold. Path validation rejects missing projections, bad references, duplicate acquire, and absent consume. Runtime route-fact fold also rejects duplicate acquire and absent consume with `ValueError`, then records zero calls to qualification, priority predicate evaluation, cause extraction and record construction.

Every inspected qualification source freezes exact `(source_kind, source_id, truth, contributor_choice_ids)`. Failure identity includes decisive false facts for `all` and all inspected facts for failed `any`; different missing source IDs cannot collapse into a boolean-only cause. Resolver calls read no store, persistent, event manager, inventory, chapter flag, environment, time, randomness or mutable cache. Qualifications may express route membership, exclusive commitment, or concrete resource possession only. No persisted `qualified_*` boolean, anonymous positive flag, five-axis proxy list, or qualification-based `rain_stops` gate exists.

### Detectable state initialization

Use deliberately invalid defaults:

```renpy
default semantic_state = None
default state_schema_sentinel = None
```

Only the explicit new-game initializer may write:

```text
state_schema_sentinel = "semantic_state:v2"
semantic_state = schema 2 RunMap
```

`after_load` classifies before any initialization or repair:

| Condition | Result | Destination |
|---|---|---|
| sentinel is `None` | `LEGACY_INCOMPATIBLE` | blocking safe flow |
| sentinel is an unknown exact string or wrong type | `UNSUPPORTED_VERSION` without state validation | blocking safe flow |
| sentinel is v2 and state is invalid | `CORRUPT_STATE` | blocking safe flow |
| sentinel is v2 and state is valid | `SUPPORTED` | resume |

The blocking safe flow cannot return to the loaded scene. Rollback, quick save/load, skip, history return, and screen return are disabled. It offers only main menu or explicit new game. Explicit new game replaces incompatible per-run state but preserves valid persistent unlocks.

### Detectable ending lifecycle

SYS-ENDING applies the same missing-field-detectability rule:

```renpy
default ending_flow_sentinel = None
default ending_flow_state = None
default pending_ending_id = None
```

Explicit new-game initialization writes exact `"ending_flow:v1"`, `"Active"` and `pending_ending_id=None`. Supported loads accept only exact `"Active"`/`"Ended"` plus the valid pending combinations frozen by the SYS-ENDING GDD; missing, wrong-type, unknown-version or illegal values enter the blocking safe flow. The fixed Day 7 orchestrator maps six ending IDs to six stable labels and calls the canonical resolver once. Each mapped entry label commits `"Active" → "Ended"` only through `commit_ending_entry` replacement assignment; its unique terminal completion node later emits the rollback-owned `ending_completion_event_record` through `commit_ending_completion`. Rollback across entry or completion restores the corresponding lifecycle, pending and completion event state; imported resolver code never owns this live state, and rollback never removes flushed persistent membership.

### Exact resolver boundary

The `.rpy` adapter validates active sentinel and live state, then extracts only exact ints and a detached exact built-in tuple of history strings. Imported private `_build_detached_ending_snapshot` creates the exact CPython built-in dict/list graph and never receives a live `RunMap`/`RunList`; it is callable only by the validated adapter. A static scan covers all `game/**/*.rpy` and `game/**/*.py`, resolves the full alias/reference/escape closure including assignment, arguments, returns, closures, containers, wrappers, reflection and dynamic lookup, rejects production-to-test-only dependency, and requires exactly one direct call in `game/10_state.rpy::current_ending_snapshot`. CFG proof requires active validation to dominate it on all paths; unresolved forms fail the build. Test-only fixtures remain outside that allowlist. `resolve_ending_record` and its string wrapper reject arbitrary Mapping/Sequence implementations:

- exact-type violations: `TypeError`;
- schema, shape, range, ID, history uniqueness, catalog coverage, replayed-axis mismatch, or invalid token-fold operation: `ValueError`;
- only a fully valid snapshot reaches ending fallback priority.

Validation stages are fixed and finite. Active APIs inspect only schema-known slots and key objects; unknown-key values receive no protocol access. Resolver order ends with priority predicate evaluation → cause extraction from `FrozenResolutionEvaluation` → immutable record construction. Stage/clause counters prove later stages stay zero after failure and each evaluated clause count is one. `after_load` remains the compatibility-classification exception.

Resolver purity uses `UT_PURE + INSTR + STATIC + BRANCH`. Policy v2 classifies explicit leaves, CPython 3.12 implicit opcode/operand pairs, six exact record constructors (including generated `__new__`/`tuple.__new__`) and fixed-code TypeError/ValueError construction. Protocol/native dispatch mutants must fail before custom code. The report retains the same runtime pin and adds opcode-policy/constructor-expansion hashes.

### Architecture Diagram

```text
Ren'Py defaults: state=None, sentinel=None
       |
       +-- new game --> explicit initializer --> v2 sentinel + RunMap
       |
       +-- after_load --> classify sentinel/state
                            | supported -> resume
                            \ failure -> blocking safe flow

Day 7 RunMap
  -> validate sentinel + live state in .rpy
  -> immutable ints + history tuple
  -> imported builder -> pure built-in snapshot
  -> exact resolver validation
  -> ordered history + bounded catalog
  -> replay axes and freeze threshold contributors
  -> unresolved token set
  -> route facts + qualifications
  -> priority predicate evaluation (freeze trace once)
  -> cause extraction from FrozenResolutionEvaluation
  -> immutable resolution record
  -> record.ending_id
```

### Key Interfaces

```python
initialize_new_semantic_state() -> None

classify_loaded_semantic_state(
    sentinel: object,
    state: object,
) -> Literal[
    "SUPPORTED",
    "LEGACY_INCOMPATIBLE",
    "UNSUPPORTED_VERSION",
    "CORRUPT_STATE",
]

validate_axis_deltas(axis_deltas: RunMap) -> int

_build_detached_ending_snapshot(
    schema_version: int,
    axis_values: tuple[int, int, int, int, int],
    history_ids: tuple[str, ...],
) -> dict[str, object]

resolve_ending_record(snapshot: dict[str, object]) -> EndingResolutionRecord

resolve_ending(snapshot: dict[str, object]) -> str
```

## Alternatives Considered

### Three-state qualification per domain

- **Description**: `UNSET`, `VALID`, `REVOKED` with grant/revoke/repair.
- **Pros**: Small state space.
- **Cons**: Repeated grant bypasses repair; multiple harms collapse; encourages a second hidden checklist.
- **Rejection Reason**: Produces false true endings under adversarial sequences.

### Numeric debt counter

- **Description**: Increment on revoke, decrement on repair.
- **Pros**: Represents multiplicity.
- **Cons**: Becomes another hidden score and loses event-specific explanation.
- **Rejection Reason**: Conflicts with semantic, explainable causality.

### Valid schema 2 object in `default`

- **Description**: Let Ren'Py always supply a ready state envelope.
- **Pros**: Minimal start code.
- **Cons**: Old saves missing the field become indistinguishable from initialized schema 2 saves.
- **Rejection Reason**: Cannot implement the required incompatible-save detection.

### Reaction/payoff identity as unique value

- **Description**: Treat any distinct presentation ID as unique option value.
- **Pros**: Almost every option passes dominance.
- **Cons**: Makes the validator vacuous; superficial rewrites hide dominated choices.
- **Rejection Reason**: Does not prove semantic player value.

## Consequences

### Positive

- Every serious reversal remains until its own visible, costly repair.
- Positive choices cannot wash away unresolved harm.
- Token caps prevent an unbounded hidden checklist.
- Dominance checks compare audited semantics instead of identifier inequality.
- Legacy saves remain detectable even after Ren'Py applies missing-variable defaults.

### Negative

- Narrative authors must create token-specific consequences and repairs.
- Load flow needs a dedicated blocking screen/label and automated fixtures.
- Resolver and static content validation require more catalog checks.

### Risks

- Token caps may be pressured by later content. Mitigation: any cap change reopens independent GDD review.
- Authors may label trivial choices as route-critical. Mitigation: every revoke cites one pillar, one domain, and a concrete consequence.
- A repair may be mechanically targeted but emotionally cheap. Mitigation: require registered cost evidence and narrative review after consequence.
- Failure UI might accidentally permit rollback or return. Mitigation: testcase asserts only main-menu/new-game actions exist.

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|---|---|---|
| `five-axis-state.md` | Later reverse behavior remains meaningful | Uses event-specific unresolved tokens |
| `five-axis-state.md` | One repair cannot erase multiple harms | Requires exactly one target token |
| `five-axis-state.md` | No second hidden score/checklist | Removes grant and caps tokens |
| `five-axis-state.md` | Strict-dominance verification remains meaningful | Uses registered semantic values only |
| `five-axis-state.md` | Dominance preserves actual future choices | Requires continuation-language inclusion before prefix comparison |
| `five-axis-state.md` | Irreversible harm preserves later agency | Requires pathwise timing and substantive agency witnesses |
| `five-axis-state.md` | All endings explain decisive causality | Requires six ending-causality records and payoff scenes |
| `five-axis-state.md` | Unsupported saves fail safely | Uses invalid defaults, explicit initializer, sentinel classification |

## Performance Implications

- **CPU**: Ending resolution is `O(B_in + P + Q + C + B + L·R log R + L·F log F + K log K)` with `O(B_in + P + Q + C + B + R + F + K)` extra space; `B_in` is total inspected input/catalog ID bytes, `L=max(1,max sorted source/fact stable-ID byte length)` and `R` includes qualification contributor references.
- **Memory**: No token set is saved; it is derived from existing history.
- **Load Time**: Constant-time sentinel classification plus linear validation of saved history.
- **Network**: None.

## Migration Plan

1. Keep schema version 2; the saved envelope shape is unchanged.
2. Change design defaults from a ready object to `None` and add the separate sentinel.
3. Implement explicit new-game initialization and blocking `after_load` flow before schema 2 ships.
4. Replace qualification effects with null/revoke/targeted-repair catalog entries.
5. Treat all prior schema-less development saves as incompatible; no public migration is implied.

## Validation Criteria

- `grant` does not exist in the catalog schema.
- `revoke_a → positive → grant-like positive` still leaves `revoke_a`.
- `revoke_a → revoke_b → repair_a` leaves exactly `revoke_b`.
- Unknown, multiple, wildcard, wrong-domain/mode, irreversible-target, and other invalid repair references fail pure catalog validation/import before freeze and have no runtime resolver branch.
- A build-valid repair whose target has not yet appeared or was already resolved raises fold-legality `ValueError`; every legal repair path proves the target unresolved immediately before repair.
- Every irreversible token has accepted approval whose author/reviewer identities resolve to different canonical people and, on every continuation, shortest later-choice count ≥2, a complete agency-node `branch_choice_id → outcome_reference_ids` mapping with at least two materially different registered outcomes, and an ending payoff; it is not created at ending commit.
- Distinct reaction/payoff IDs without different registered semantic values do not prevent dominance.
- Sparse costs use key-union/missing-zero comparison; equal-size incomparable token sets never establish dominance.
- Matching reachable node sets without `L_A(h) ⊆ L_B(h)` never establishes dominance.
- All six canonical ending witnesses validate complete typed predicate/cause records, exact higher-priority exclusions, terminal outcome signatures, and concrete payoff scenes; two same-predicate/different-evidence paths produce distinct source-specific causes, all legal terminal paths use the fixed total-order key, and `unsent_postcard` keeps its fallback match as audit-only while display begins with a concrete presentation-safe failure/unresolved anchor. Coverage never merges different fates, cost bearers, or tragedy closure. Content budget is 1–6 target/7–12 warning/>12 failure per ending.
- A marker-less save whose missing variables receive `None` defaults is classified `LEGACY_INCOMPATIBLE`.
- No non-supported load result can return to the loaded scene.
- No imported helper receives a live `RunMap` or `RunList`.
- Static source scanning closes all aliases, escapes, wrappers, reflection/dynamic lookup and production-to-test paths; it finds exactly one production callsite and proves active validation dominates it. Test-only direct calls do not enter the allowlist.
- Composite-invalid fixtures prove finite schema-known traversal, state-value + payload-type → `TypeError`, illegal choice ID + delta value defect → choice-ID `ValueError`, and read-trace/protocol-bomb counts of zero for unknown values. Resolver runtime stages stop after the first failing stage.
- Catalog mutation attempts fail for both the private `MappingProxyType` index and immutable records.
- Invalid catalog fixtures fail only during pure validator or isolated import/build-time validation; the runtime resolver has no catalog-schema failure hook.
- Axes, route facts and qualifications recompute only from snapshot history plus the frozen projection catalog; replayed axes equal the snapshot, qualification facts retain exact decisive source identity, read zero external live state, never gate `rain_stops`, and never create persisted or axis-proxy positive flags.
- Duplicate resource acquire and absent consume both stop at route-fact fold with `ValueError`; all later stage counters remain zero.
- Two paths satisfying the same predicate with different evidence generate different source-specific cause IDs but the same ending; multi-source and no-history causes have one total order. The `unsent_postcard` constant match remains in audit data but cannot be the first player-facing card.
- Static resolver purity closure covers all branches and transitive helpers; mutable globals/caches, external state, reflection and unresolved edges fail with precise locations.

## Related Decisions

- [ADR-0001](adr-0001-deterministic-ending-resolution.md)
- [ADR-0002](adr-0002-rollback-and-persistence-boundary.md)
- [ADR-0004](adr-0004-semantic-ending-snapshot-and-state-envelope.md)
- [SYS-STATE GDD](../../design/gdd/five-axis-state.md)
