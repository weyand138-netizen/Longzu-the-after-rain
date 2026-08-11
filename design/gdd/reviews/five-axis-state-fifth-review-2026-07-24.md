# 五轴局内状态系统：第五次独立复审

> **Date**: 2026-07-24  
> **Reviewed file**: `design/gdd/five-axis-state.md`  
> **Prior verdict**: NEEDS REVISION  
> **Verdict**: NEEDS REVISION  
> **Rough scope signal**: XL（剩余文档修订约 M）  
> **Review mode**: Full independent review

## Review Panel

- Game Designer
- Systems Designer
- QA Lead
- Creative Director

## Completeness

8/8 required sections were present. The fifth version retained the stable axes + ordered history + token-ledger architecture and did not reintroduce any fourth-review blocker.

## Implementation-blocking Findings

### 1. Validation traversal and precedence conflict

The two-pass rule did not say whether unknown-field values were recursively traversed. An extra value pointing to its own root could make a generic traversal non-terminating. `STATE-COMP-010` also said state errors always win, while `STATE-COMP-019` said a graph-wide type error wins over value errors. The contract needed a finite schema-known traversal and a single result for state-value + payload-type.

### 2. Dominance did not prove continuation-language inclusion

Equal reachable-node sets do not prove that the same future choice-ID sequences remain executable. Dominance must require B to accept every legal continuation accepted after A for every reachable prehistory; one rejected suffix makes the pair non-dominating.

### 3. Irreversible timing was not pathwise

Two later nodes counted across the graph could be bypassed on one ending path or filled by unrelated cosmetic choices. Every continuation needs a shortest-path count and at least one later branching choice that materially changes ending selection, character fate, cost bearer, or tragedy closure. Approval ownership and severity criteria also needed a machine schema.

### 4. Decisive causality covered only two endings

`STATE-CONTENT-019` covered `golden_cage` and `unsent_postcard` only. All six canonical witnesses need matched causes, exact exclusions for every higher-priority ending, and a scene payoff that explains the outcome without exposing raw thresholds.

### 5. Achievement AC lacked owner and executable schema

The hard achievement AC had no `SYS-ACHIEVE` owner, stable condition events, or zero-delta/non-best-ending witness IDs. It had to become an owned machine contract or be downgraded to a provisional downstream gate.

## Recommended Revisions

- Make the detached snapshot builder private or give it a separate input contract.
- Define immutable catalog construction and runtime mutation prevention.
- Set a recommended irreversible-token count below the absolute catalog cap.
- Provide complete machine-record examples for validation, dominance, and irreversible witnesses.

## Sixth Revision Decisions

### Finite schema-known validation

Validators inspect declared containers/slots and all key objects only. Unknown-key values are never read and arbitrary recursion is forbidden. All state and payload known type slots precede the value sweep, so state-value + payload-type deterministically yields payload `TypeError`.

### Continuation-language dominance

The major-choice graph must be a finite DAG. For every reachable prehistory `h`, dominance first proves `L_A(h) ⊆ L_B(h)` over complete stable choice-ID suffixes. Only then are aligned token prefixes, costs, axes, and semantic values compared.

### Pathwise irreversible agency

Every irreversible continuation records a shortest later-choice count of at least two and a substantive agency witness. Admission also requires a non-author accepted Creative Director review using fixed severity criteria and a token-specific payoff for every reachable ending.

### Six-ending causal closure

Every canonical witness carries an `ending_causality_record` with matched cause IDs, one exact exclusion entry for each higher-priority ending, and a concrete payoff scene/summary.

### Owned downstream achievement gate

Achievement anti-proxy rules now belong to `SYS-ACHIEVE`, with an exact event-condition schema and stable zero-delta/non-best witness IDs. This provisional downstream gate does not block standalone `SYS-STATE` approval before the achievement GDD exists.

### Private builder and frozen catalog

`_build_detached_ending_snapshot` is private to the validated adapter. Counterevidence authoring data compiles to immutable tuple/`NamedTuple` records and a private `MappingProxyType` index after initialization validation; no runtime mutation API exists.

## Files Revised

- `design/gdd/five-axis-state.md`
- `design/gdd/game-concept.md`
- `design/gdd/systems-index.md`
- `design/narrative/branch-map.md`
- `design/narrative/achievement-catalog.md`
- `design/registry/entities.yaml`
- `docs/architecture/architecture.md`
- `docs/architecture/adr-0001-deterministic-ending-resolution.md`
- `docs/architecture/adr-0004-semantic-ending-snapshot-and-state-envelope.md`
- `docs/architecture/adr-0005-counterevidence-ledger-and-detectable-state-initialization.md`
- `docs/architecture/control-manifest.md`
- `production/session-state/active.md`

## Remediation Status

All five implementation blockers and four recommendations were incorporated into the sixth synchronized revision. The original **NEEDS REVISION** verdict remains active until a fresh independent review examines the revised documents. This remediation record is not self-approval.

## Remaining Maturity Gaps

- Production state/resolver code still implements the earlier prototype contract.
- Full token, approval, agency-witness, ending-causality, achievement-condition, and payoff records await downstream GDDs and content.
- Finite validator fixtures, frozen catalog implementation, continuation-language tooling, and full seven-day path enumeration do not yet exist.

## Superseded by Sixth Review

The sixth independent review is recorded in [five-axis-state-sixth-review-2026-07-24.md](five-axis-state-sixth-review-2026-07-24.md). This file remains the historical fifth-review remediation record.
