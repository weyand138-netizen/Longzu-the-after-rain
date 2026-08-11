# ADR-0001: Deterministic Ending Resolution

- Status: Accepted
- Date: 2026-07-23
- Amended: 2026-07-27 by the SYS-ENDING targeted contract closure for axis/history replay, terminal compatibility, presentation-safe display, detectable ending lifecycle, provisional downstream gates, and input-byte complexity
- Amended: 2026-08-09 by ADR-0006 for the frozen ending completion boundary
- Engine: Ren'Py 8.5.3
- GDD requirements: SYS-STATE, SYS-ENDING, SYS-TEST

## Context

Six endings must be reachable on a first playthrough, mutually exclusive, explainable after reveal, and independent of randomness or external guides. Chapter scripts must not duplicate ending conditions.

## Decision

Use five integer semantic axes with a formal domain of 0–3:

`understanding`, `autonomy`, `truth`, `preparation`, `sacrifice`.

At the end of Day 7, a pure function receives a detached schema 2 ending snapshot containing both the five axes and ordered semantic choice history. It folds history through an immutable bounded counterevidence catalog, then evaluates endings in this fixed priority:

1. `rain_stops`
2. `her_own_name`
3. `see_the_sea`
4. `one_person_train`
5. `golden_cage`
6. `unsent_postcard`

Axis values represent accumulated positive evidence, not irrevocable moral credit. A route-critical reverse behavior adds a unique unresolved token even after an axis reaches 3. Each token is explicitly `repairable` or independently reviewed `irreversible`; a repair removes exactly its named unresolved repairable token after the consequence becomes observable and only when domains match. There is no positive `grant` operation. `rain_stops` requires all five axes at 3 and an empty unresolved-token set.

The final fallback is unconditional, so every valid axes-plus-history input resolves exactly once. Completed axes, events, resource possession, and route qualifications are rebuilt only from ordered history plus frozen choice projections; the replayed axes must equal the snapshot axes before folds begin. They are not additional live inputs. Qualification source facts describe only pre-terminal commitments/resources/constraints and freeze exact source kind, ID, truth, and contributor lineage. `rain_stops` is exactly five axes at 3 plus an empty unresolved-token set and never reads a qualification; a separate build-time terminal-compatibility validator rejects downstream fate/outcome signatures that contradict the selected ending. The canonical pure resolver returns an immutable structured record containing the ending ID, folded facts, complete clause trace and path-specific causes; the legacy string function is only an `.ending_id` wrapper. The resolver has no access to Ren'Py state, persistence, inventory, event managers, UI, files, network, environment, time, randomness or mutable cache.

Display selection consumes only cause templates whose summaries passed build-time spoiler/anti-hidden-score validation. The `unsent_postcard` constant match remains an audit record; its first player-facing card is a concrete existing failure/unresolved cause selected by the ending-specific fallback anchor order. Core resolver approval freezes these algorithms and exact fixture oracles. Production qualification bindings, terminal-path enumeration, localized summaries, maximum-content fixtures, and benchmarks remain explicit SYS-CHOICE/SYS-NARRATIVE/SYS-TEST downstream gates.

## Implementation Guidelines

- The resolver must require exact CPython built-in snapshot types and validate schema, shape, axis keys/ranges, ordered history, catalog coverage, replayed-axis equality, and fold legality.
- Resolver runtime stages are fixed through priority predicate evaluation, cause extraction from `FrozenResolutionEvaluation`, then immutable record construction. Every evaluated clause executes once; cause extraction cannot read snapshot/catalog or call the evaluator. Exact-type failures raise `TypeError`; a type-clean graph with invalid values/shape/coverage or an invalid fold operation raises `ValueError`. Duplicate resource acquire and absent consume stop all later stages.
- The immutable semantic catalog maps stable choice IDs to `null`, one unique revoke token, or one targeted repair.
- The catalog is capped at ten revoke tokens total and two per semantic domain.
- Catalog authoring records are immutable tuples/`NamedTuple`s; a private import/build-time validator checks choice/effect schema, caps, domains, modes, and repair references before creating a private `MappingProxyType` index. These frozen invariants are not revalidated per resolver call, and the resolver exposes no catalog-injection seam.
- Catalog build validation rejects unknown targets, wrong domain/mode, irreversible targets, and invalid repair references before freeze. A runtime repair can fail only because its build-valid target is not unresolved at that history prefix. Irreversible tokens require an accepted approval whose author/reviewer identities resolve to different canonical people and, on every continuation, two later major choices plus a complete agency-node branch-to-registered-outcome mapping and per-ending payoff.
- Chapter code must update axes through one helper and must never assign an ending.
- The Day 7 `SYS-ENDING` orchestrator alone maps `resolution_record.ending_id` through the fixed six-label map and owns `Active → Ended`; detectable rollback-owned `ending_flow_sentinel/state` use `None` defaults followed by explicit `"ending_flow:v1"` / `"Active"` initialization. Only the first statement of a mapped ending label may call `commit_ending_entry`; the label's one terminal completion node later calls `commit_ending_completion` after final player-visible closure, and neither mutates the semantic snapshot.
- Clause templates use `(ending, clause, polarity)` lineage; per-token audit templates use `(token, audit)` and bind runtime selected ending plus token/revoke source. The exhaustive payload matrix fixes every source/value/anchor field, including earliest-required axis increments. Golden hashes remain fixed. A non-production build-layer digest-bijection checker supplies executable synthetic collision proof without replacing `_hashlib`.
- `resolve_ending_record(snapshot) -> EndingResolutionRecord` is the only canonical pass. `resolve_ending(snapshot) -> str` must be exactly the record's `.ending_id` wrapper and cannot duplicate evaluation.
- Every canonical witness therefore provides implementation-order-independent matched causes, complete exclusions for every higher-priority ending, a terminal outcome signature, and a concrete payoff scene. All legal terminal paths are partitioned into classes keyed by ending, ordered causes/exclusions/unresolved tokens, character fates, cost bearers, and tragedy closure. Per ending, 1–6 classes is target, 7–12 triggers scope review, and more than 12 fails content build without allowing signature merges. Player presentation includes at least one matched cause and at most two additional fixed-order causes; bare thresholds and full matrices are not player-facing.
- Four returned record classes plus audit/evaluation artifacts have exact `ending_rules` module/qualname/field order. Atomic trace entries freeze template/polarity/kind/source identity plus value/anchors; audit facts freeze template identity and exact `audit`/`unresolved_counterevidence`/`unresolved_token` values. Cause extraction accepts only `FrozenResolutionEvaluation`. The wrapper's sole canonical call is exempt from the “no self-evaluation” rule. A source-hash-verified test-only AST copy observes exact stage/clause/call/field-read counts without a production seam.
- Purity policy v2 covers explicit leaves, CPython 3.12 implicit opcode/operand dispatch, six record constructors, exact tuple `__new__`, and frozen-code TypeError/ValueError construction. Unlisted implicit/native/custom-protocol dispatch fails before execution.
- Every production player-facing narrative choice, including narrative-only/timed/accessibility-equivalent options, commits through `SYS-STATE.apply_choice` after confirmation and before reaction; narrative-only passes an empty `RunMap`, appends history without changing axes, and shares save/load/rollback restoration. Exact reaction/payoff joins, cardinality, proof-kind nullability and reverse event metadata remain a provisional downstream gate owned by `SYS-CHOICE`/`SYS-NARRATIVE`, outside `SYS-STATE` approval.
- Every changed threshold requires canonical path tests and boundary tests.
- Scores remain invisible to players.

## Alternatives Considered

- Final single choice: rejected because it erases the seven-day causal chain.
- Weighted affection total: rejected because it collapses semantically different actions.
- Random tie-breaks: rejected because they make outcomes non-explainable.
- Unordered route flags only: rejected because they erase event order and cannot distinguish an unrepaired reversal from a later explicit repair.
- Axes-only snapshot: rejected because monotonic capped values forget later contradictory behavior.

## Performance Implications

Module initialization performs one bounded catalog validation. Each resolver call is `O(B_in + P + Q + C + B + L·R log R + L·F log F + K log K)` with `O(B_in + P + Q + C + B + R + F + K)` extra space; `B_in` is total inspected input/catalog ID bytes, `L=max(1,max sorted source/fact stable-ID byte length)`, and `R` includes qualification contributor references. It must not load assets or perform I/O. A resolver-specific measured budget is set only after the downstream benchmark manifest is frozen; the 16.6 ms whole-frame budget is not automatically assigned to this function.

## Engine Compatibility

Pure Python is compatible with Ren'Py 8.5.3/Python 3.12. Imported modules are deliberately immutable with respect to store state because imported Python is not rollback-transformed.
