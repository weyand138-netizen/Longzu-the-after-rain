# 五轴局内状态系统：第六次独立复审

> **Date**: 2026-07-24  
> **Reviewed file**: `design/gdd/five-axis-state.md`  
> **Prior verdict**: NEEDS REVISION  
> **Verdict**: NEEDS REVISION  
> **Rough scope signal**: XL（本轮剩余修订量 S）  
> **Review mode**: Full independent review

## Review Panel

- Game Designer
- Systems Designer
- QA Lead
- Creative Director

## Completeness

8/8 required sections were present. The sixth version preserved the approved axes + ordered history + bounded counterevidence architecture. Fifth-review continuation-language, pathwise irreversible agency, six-ending canonical causality, achievement ownership, private builder, and immutable catalog recommendations were substantially closed.

## Implementation-blocking Findings

### 1. `apply_choice` validation precedence still conflicted

The main rule and `STATE-COMP-010/019` required all known state/payload type slots to be scanned before values, but the choice-ID Edge Case said an invalid `choice_id` must be rejected before deltas were evaluated. The required unique order is:

```text
global state+payload type sweep
→ state value/shape
→ choice-ID value
→ delta value/shape/count
```

### 2. Frozen catalog type and lifecycle were inconsistent

The formula table called `C` an immutable built-in dict although construction required a private `MappingProxyType`. The resolver acceptance order also reintroduced token schema/reference failure after those invariants had already been validated and frozen at initialization.

Catalog schema, token definitions, caps/domains/modes, and repair references must fail at import/build-time. Runtime resolver work is limited to snapshot validation, history coverage, fold legality, and ending priority. A catalog failure fixture must not create a mutable runtime injection seam.

### 3. Unknown-value zero-read was not an observable oracle

A self-reference plus finite watchdog only proved termination and lack of recursive traversal. It did not prove that the implementation never fetched or otherwise evaluated an unknown value. Acceptance needed a controlled read trace, protocol-bomb sentinel, or equivalent instrumentation with an exact zero-access result.

## Recommended Revisions

- Add explicit `author_id` so non-author approval can prove `reviewer_id != author_id`.
- Add complete `branch_choice_id → outcome_reference_ids` evidence to each agency witness.
- Cover non-canonical paths through terminal-cause equivalence classes owned by `SYS-ENDING`/`SYS-NARRATIVE`.
- Move resolver composite-invalid coverage out of `STATE-COMP-019` into a downstream owner.
- Add a separate wrong-type sentinel AC that returns `UNSUPPORTED_VERSION` without state validation.
- Give the private snapshot builder one exact invalid-direct-call contract.
- Present only one to three decisive ending causes to players; keep the full exclusion matrix in audit/test evidence.

## Seventh Revision Decisions

### One `apply_choice` order

The GDD now fixes the global type sweep before every value check, followed by state values, choice-ID value, and delta value/shape/count. `validate_axis_deltas` and `apply_choice` share the same pure primitives without letting the public helper reorder the global sweep.

### Catalog lifecycle split

`C` is now the private read-only `MappingProxyType` view. Catalog schema/reference defects fail before freezing at import/build-time. Runtime resolver stages are snapshot type, snapshot value/shape, history coverage, fold legality, and ending priority. Invalid fixtures use the pure private validator or isolated module initialization; resolver injection is forbidden.

### Observable zero access

Known-value reads pass through a private traceable accessor in test builds. Exact container validation remains mandatory. Unknown fixtures combine a self-reference and protocol bomb; acceptance requires zero unknown-key `__getitem__` reads, zero protocol calls, and an allowlist-exact read trace.

### Recommendations incorporated

Approval records now carry comparable author/reviewer IDs. Agency witnesses name a node and map every direct branch choice to registered outcomes. Terminal paths receive downstream causal-equivalence coverage. Resolver composite defects, wrong-type load sentinels, private-builder misuse, and player-facing causal compression each have separate acceptance criteria.

## Files Revised

- `design/gdd/five-axis-state.md`
- `design/gdd/game-concept.md`
- `design/gdd/systems-index.md`
- `design/gdd/reviews/five-axis-state-sixth-review-2026-07-24.md`
- `design/narrative/branch-map.md`
- `design/registry/entities.yaml`
- `docs/architecture/architecture.md`
- `docs/architecture/adr-0001-deterministic-ending-resolution.md`
- `docs/architecture/adr-0004-semantic-ending-snapshot-and-state-envelope.md`
- `docs/architecture/adr-0005-counterevidence-ledger-and-detectable-state-initialization.md`
- `docs/architecture/control-manifest.md`
- `production/session-state/active.md`

## Remediation Status

All three implementation blockers and seven recommendations were incorporated into the seventh synchronized revision. The sixth review’s **NEEDS REVISION** verdict remains the latest independent verdict until a fresh reviewer examines the new documents. This remediation record is not self-approval.

## Remaining Maturity Gaps

- Production state/resolver code still implements the earlier prototype contract.
- Catalog, approval, agency, terminal-cause, ending, and achievement records await their downstream GDDs and full content.
- The new validation instrumentation, import-time catalog validator, and exhaustive path tools are specified but not implemented.

## Superseded by Seventh Review

The seventh independent review is recorded in [five-axis-state-seventh-review-2026-07-24.md](five-axis-state-seventh-review-2026-07-24.md). This file remains the historical sixth-review remediation record.
