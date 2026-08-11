# Second Independent Design Re-review — SYS-STATE

**Date**: 2026-07-23  
**Document**: `design/gdd/five-axis-state.md`  
**Verdict**: **MAJOR REVISION NEEDED**  
**Scope Signal**: **XL**  
**Review mode**: Full adversarial re-review

## Review Panel

- Game Designer
- Systems Designer
- QA Lead
- Creative Director synthesis

## Blocking Findings

1. **Monotonic axes forget later reverse behavior.** Five axes only increased and the ending resolver only read the five final integers. A player could cap `autonomy`, repeatedly override Erii later, and retain the same true-ending input.
2. **GDD and Master Architecture contradicted each other.** The architecture still specified `apply_choice(...) -> None`, clamping, separate store values, axes-only snapshots, and unconditional ID recording while the GDD required strict rejection, result statuses, duplicate no-op, and atomic state replacement. Schema lifecycle and load validation were also undefined.
3. **Several acceptance criteria lacked one executable oracle.** `TypeError`/`ValueError` classifications conflicted, abstract container protocols were mixed with exact-type wording, one failure path was not constructible, global ID uniqueness lacked a dedicated criterion, recovery quantifiers were ambiguous, and owners were incomplete.
4. **Anti-hidden-score validation lacked a machine-readable comparison model.** The strict-dominance rule referred to route retention, risk, resource cost, character cost, and unique value without defining fields or component-wise comparison. The prologue “remember the red mud” branch also did not satisfy the `truth` requirement to verify and share information.

## Accepted Remediation Decisions

### 1. Preserve axes; expand ending input

- Five axes remain monotonic `0–3` positive-evidence counters.
- The ending snapshot now contains schema, axes, and ordered semantic choice history.
- `SYS-ENDING` folds history through immutable `grant/revoke/repair` qualification metadata.
- All-five-at-3 is necessary but no longer sufficient for `rain_stops`; no required qualification may remain unresolved.
- This decision is recorded in ADR-0004 and amends ADR-0001/0002.

### 2. Adopt one rollback state envelope

- Schema 2 uses one exact Ren'Py rollback-transformed `semantic_state` `RunMap` containing `schema_version`, axes `RunMap`, and `choice_history` `RunList`.
- `apply_choice` validates current state, validates the payload, builds a full candidate locally, and commits with one replacement assignment.
- The public result is `APPLIED` or `DUPLICATE_NOOP`; invalid input is never clamped.
- Writes, snapshots, and `after_load` share one validator.
- Development schema 1 or marker-less saves are explicitly incompatible; any post-release schema migration requires a new accepted ADR and fixtures.

### 3. Replace ambiguous acceptance oracles

- Exact-type failures use `TypeError`; valid types with bad schema, shape, format, uniqueness, or range use `ValueError`.
- Snapshot failure criteria are split by error class.
- Atomicity is tested against every specified constructible failure; no synthetic candidate-failure hook is required.
- Global `choice_id` uniqueness, persistence ownership, load rejection, and full-snapshot consumption have independent criteria.
- True-ending recovery now requires at least four independent opportunities per axis and five axis-specific “miss earliest, recover with the next three” witnesses.
- Erii dialogue constraints are owned by Narrative/Choice content validation rather than UX.

### 4. Make anti-dominance data executable

Every major option now declares:

- `choice_id`
- `axis_deltas`
- `next_node_ids`
- `risk_vector`
- `resource_costs`
- `character_costs`
- `unique_value_tags`
- `qualification_effects`
- `immediate_reaction_id`
- `payoff_ids`

The validator enumerates route/qualification preservation and compares risk and cost vectors component-wise, axis deltas by set inclusion, and unique value by stable tags. Failures must name the dominating option and comparison dimensions.

The prologue truth action is revised from merely remembering red mud to cross-checking the mud evidence and sharing the pursuit direction with Erii.

## Files Synchronized

- `design/gdd/five-axis-state.md`
- `design/gdd/game-concept.md`
- `design/narrative/branch-map.md`
- `design/registry/entities.yaml`
- `docs/architecture/architecture.md`
- `docs/architecture/adr-0001-deterministic-ending-resolution.md`
- `docs/architecture/adr-0002-rollback-and-persistence-boundary.md`
- `docs/architecture/adr-0004-semantic-ending-snapshot-and-state-envelope.md`
- `design/gdd/systems-index.md`
- `production/session-state/active.md`

## Remediation Status

All four second-review blocking packages were revised on 2026-07-23. The **MAJOR REVISION NEEDED** verdict remains in force until a fresh independent review approves the synchronized documents. `SYS-ENDING` must not begin before that review.

## Remaining Maturity Gaps

These are downstream implementation or dependent-GDD work, not unresolved `SYS-STATE` specification blockers:

- Production `state.rpy` and `ending_rules.py` still implement the earlier prototype contract.
- The complete qualification catalog belongs to the future `SYS-ENDING` and `SYS-NARRATIVE` GDDs.
- Schema 2 implementation, migration rejection UI, static metadata validator, and full save/load/rollback evidence do not yet exist.
- The complete seven-day graph and six axes-plus-history witness paths do not yet exist.

## Superseded by Third Review

A subsequent independent review found six additional blocking issues in the revised contract. See [five-axis-state-third-review-2026-07-23.md](five-axis-state-third-review-2026-07-23.md). This file remains the historical record of the second review and must not be interpreted as the current approval state.
