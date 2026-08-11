# Design Change Impact Report

> **GDD**: `design/gdd/five-axis-state.md`  
> **Revision**: Twelfth Final Targeted Closure  
> **Date**: 2026-07-27  
> **Baseline**: Eleventh-revision documents and the read-only eleventh independent review  
> **Git note**: No committed prior GDD exists in this repository, so `git show HEAD:design/gdd/five-axis-state.md` cannot provide a historical baseline.

## Change Summary

Changed sections:

- Executable Predicate and Cause: added disjoint audit lineage, exhaustive payload population, deterministic excess-axis contributors and isolated digest-bijection proof.
- Structured Resolution: fixed concrete record identities/order, cause-ready trace/audit artifacts and source-hash-verified observation instrumentation.
- Resolver Purity: replaced policy v1 with explicit + implicit opcode/operand + constructor policy v2.
- Choice Feedback/Payoff: expanded coverage to every production player-facing narrative choice and every legal terminal continuation, with immediate execution and bidirectional causal proof.
- Performance: included canonical bytes, all source/fact/cause sorting and qualification-contributor storage.
- Dependencies/Registry/AC: added SYS-ACCESS ownership, nine registry facts and five focused CONTENT ACs.

Unchanged sections:

- Five-axis meanings and `0–3` domain.
- Rollback-owned schema 2 state envelope and lifecycle sentinel.
- `apply_choice` validation precedence and atomic replacement.
- Counterevidence cap, repair lifecycle, irreversible approval and path witnesses.
- `rain_stops` exact positive predicate.
- Terminal-cause class content budget and UI ownership.

## Architecture Impact

### ADR-0001: Deterministic Ending Resolution

Status: **Updated in place**

The fixed priority and pure detached-input decision remain valid. The twelfth amendment closes audit lineage, payload population, concrete frozen artifacts, policy-v2 purity, observation and complete sorting complexity.

### ADR-0002: Rollback and Persistence Boundary

Status: **Updated in place**

The saved envelope remains schema 2. The targeted closure makes all player-facing narrative choices, including `narrative_only`, use `SYS-STATE.apply_choice`; an empty `RunMap` commits history without changing axes and therefore uses the existing rollback/save/load boundary.

### ADR-0003: Content and Presentation Boundary

Status: **Still Valid**

Chapter/UI ownership is unchanged. Presentation continues to consume selected display causes without owning resolution.

### ADR-0004: Semantic Ending Snapshot and State Envelope

Status: **Updated in place**

The detached snapshot and builder callsite decision remain valid. The amendment adds cause-ready frozen evaluation and non-production AST observation without changing the public boundary.

### ADR-0005: Counterevidence Ledger and Detectable State Initialization

Status: **Updated in place**

The counterevidence and initialization decisions remain valid. The amendment binds audit causes to token/selected ending and applies feedback/payoff proof to every player-facing choice and legal continuation.

## Resolution

- No ADR is superseded.
- ADR-0001, ADR-0002, ADR-0004 and ADR-0005 were amended in place.
- ADR-0003 remains unchanged.
- `docs/architecture/architecture-traceability.md` does not exist; no traceability-index edit was possible.
- The user-directed closure authorizes one four-item targeted validation; no thirteenth full divergent review is required.

## Twelfth Final Targeted Closure

1. `ClauseEvaluationTraceEntry` now freezes template/polarity/kind/source identity for atomic clauses, while `UnresolvedAuditFact` freezes `audit`/`unresolved_counterevidence`/`unresolved_token`; cause extraction can construct records from `FrozenResolutionEvaluation` alone.
2. Every player-facing narrative choice commits through `SYS-STATE.apply_choice` after confirmation and before reaction. `narrative_only` uses an empty `RunMap`, appends history without axis changes, and shares rollback/save/load restoration.
3. Exact choice→reaction/payoff joins, cardinality, proof-kind nullability and reverse event metadata are explicitly transferred to `SYS-CHOICE`/`SYS-NARRATIVE` as a provisional downstream gate excluded from `SYS-STATE` approval.
4. The complexity contract is `O(H + P + Q + C + B + L·R log R + L·F log F + K log K)`, where `L` is maximum sorted source/fact stable-ID UTF-8 byte length and `R` includes qualification contributor references.

No new blocker category is admitted by this closure.

## Twelfth Review Gate Outcome

The fresh independent review ran on 2026-07-27 and returned the historical **NEEDS REVISION** verdict below. Its four findings were subsequently handled by the user-directed twelfth-final targeted closure.

Four focused contract gaps remain:

1. `FrozenResolutionEvaluation` lacks the cause identity/source fields required for catalog-free cause extraction.
2. `narrative_only` choices have no unique rollback/save/history authority model.
3. Choice declarations, reaction/payoff bindings, witnesses and event metadata lack exact joins, cardinality and proof-kind nullability.
4. The resolver complexity bound assumes a global 64-byte stable-ID cap that is not yet defined outside `choice_id`.

Final disposition: the first two state-model contradictions were corrected; the third was transferred to `SYS-CHOICE`/`SYS-NARRATIVE` as an approval-excluded provisional downstream gate; the fourth received the one-line `L` complexity correction. The single targeted validation passed 4/4, so no thirteenth full review is required and `SYS-STATE` is **Approved**.

## Eleventh Revision Addendum

The six tenth-review blockers were remediated without superseding an ADR:

1. Predicate clauses now have an exhaustive legal table, exact contiguous per-ending order, same-ending operands, build-time negative fixtures and a single-evaluation rule.
2. Cause templates and runtime causes have distinct schemas; `cause_payload_v1` has a typed byte grammar, two golden byte/hash vectors and collision failure semantics.
3. Trace, exclusion and resolution records have exact field order, nested exact immutable containers, deterministic ID/cause ordering, one cause per unresolved token and total display-ID resolution.
4. Priority evaluation freezes the only clause trace; cause extraction never reevaluates. The wrapper calls the canonical resolver once and reads only `.ending_id`.
5. Purity closes against trusted-leaf allowlist v1 and the pinned Ren'Py 8.5.3.26051504 / CPython 3.12.7 / cpython-312 interpreter manifest.
6. Every major choice and reachable prehistory now requires a strictly later payoff witness, and every declared payoff must be covered.

## Twelfth Revision Addendum

The five eleventh-review blockers were remediated:

1. Clause and audit templates now have disjoint lineage keys. Audit runtime causes bind token, revoke choice and selected ending. An exhaustive payload matrix fixes contributors, values and anchors; axis matches take the earliest required real increments.
2. Concrete `ending_rules` module/qualname/field order is unique. Atomic trace entries and unresolved audit facts form a cause-ready `FrozenResolutionEvaluation`; a source-hash-verified test-only AST copy supplies exact observation records.
3. Purity policy v2 covers explicit leaves, CPython 3.12 implicit opcode/operand dispatch, six record constructors and fixed-code exception construction, with protocol/native mutants.
4. Coverage now includes every production player-facing narrative choice. Canonical prehistory/full-continuation IDs and bidirectional reaction/payoff bindings prove immediate execution and later causality on every legal terminal continuation.
5. Complexity now includes canonical bytes, all source/fact/cause sorting and qualification contributor storage: `O(H + P + Q + C + B + R log R + F log F + K log K)` time and `O(H + P + Q + C + B + R + F + K)` space.

ADR-0001, ADR-0004 and ADR-0005 were updated in place. ADR-0002/0003 remain valid; no ADR was superseded. `SYS-ACCESS` is now explicit in dependencies and choice-surface ownership. TD-CHANGE-IMPACT was skipped in Solo mode.
