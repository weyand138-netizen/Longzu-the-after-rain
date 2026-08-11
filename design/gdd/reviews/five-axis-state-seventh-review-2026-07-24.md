# 五轴局内状态系统：第七次独立复审

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

8/8 required sections were present. The seventh version closed all three sixth-review blockers: `apply_choice` precedence, frozen-catalog lifecycle, and observable unknown-value zero access.

## Implementation-blocking Findings

### 1. Private builder lacked a production-callsite gate

The snapshot contract restricted `_build_detached_ending_snapshot` to the validated adapter, but `STATE-COMP-022` only tested invalid direct arguments. Acceptance also needed a complete production source scan whose allowlist contains only `current_ending_snapshot`; chapter, UI, achievement, ending-orchestrator, other-adapter, alias, or test-wrapper leakage must fail.

### 2. Component evidence classification was incomplete

The Component Contract described only pure/unit tests even though `STATE-COMP-021` required instrumentation, static access scanning, and branch coverage. Every component AC needed an explicit evidence type or combination.

## Recommended Revisions

- Remove catalog schema/reference failures from runtime `STATE-DOWNSTREAM-006`; keep them at import/build-time under `STATE-CONTENT-025`.
- Give terminal cause classes a unique cause-extraction rule and include character fate, cost bearer, and tragedy closure in class identity or payoff variants.
- Register an exact `outcome_reference_record` schema with referential-integrity checks.
- Resolve approval author/reviewer IDs through a canonical identity registry.
- Derive route qualifications and narrative resources only from stable choice/event/resource records; never create a second positive boolean checklist.

## Specialist Disagreement

- Systems Designer approved standalone `SYS-STATE`.
- Game Designer requested more deterministic terminal-cause classification.
- QA Lead retained the two component-verification blockers.
- Creative Director classified terminal-cause/outcome details as downstream `SYS-ENDING`/`SYS-NARRATIVE` gates and retained only the callsite/evidence findings as current blockers.

## Eighth Revision Decisions

### Production callsite allowlist

The production manifest now scans `game/**/*.rpy` and `game/modules/**/*.py`, resolves direct/import/module aliases, and permits exactly one builder call at `game/10_state.rpy::current_ending_snapshot` after active validation. Test-only sources are classified and reported separately; unresolved dynamic aliases and test wrappers entering production fail the build.

### Exhaustive component evidence map

`STATE-COMP-000` through `023` now map exhaustively to engine-hosted unit tests, pure Python unit tests, controlled instrumentation, static source scans, and/or branch coverage.

### Runtime/build-time error separation

`STATE-DOWNSTREAM-006` now covers only snapshot value/shape, history coverage, and fold-legality failures. Catalog schema, token definition, caps/domain/mode, and repair references remain import/build-time failures under `STATE-CONTENT-025`.

### Downstream identity and causality schemas

Terminal classes use the complete normalized cause set consumed by the evaluation trace, not an author-selected decisive subset. Class identity also includes character fates, cost bearers, and tragedy closure. Outcome references and review identities have exact schemas and referential-integrity rules; non-author review compares canonical people.

### Route qualification boundary

Route qualifications are pure derivations over registered choice, event, and resource records. Persisted qualification booleans, five-axis proxy lists, and true-ending bypasses are forbidden.

## Files Revised

- `design/gdd/five-axis-state.md`
- `design/gdd/game-concept.md`
- `design/gdd/systems-index.md`
- `design/gdd/reviews/five-axis-state-sixth-review-2026-07-24.md`
- `design/gdd/reviews/five-axis-state-seventh-review-2026-07-24.md`
- `design/narrative/branch-map.md`
- `design/registry/entities.yaml`
- `docs/architecture/architecture.md`
- `docs/architecture/adr-0001-deterministic-ending-resolution.md`
- `docs/architecture/adr-0004-semantic-ending-snapshot-and-state-envelope.md`
- `docs/architecture/adr-0005-counterevidence-ledger-and-detectable-state-initialization.md`
- `docs/architecture/control-manifest.md`
- `production/session-state/active.md`

## Remediation Status

Both implementation blockers and all five recommendations were incorporated into the eighth synchronized revision. The seventh review’s **NEEDS REVISION** verdict remains the latest independent verdict until a fresh reviewer examines the new documents. This remediation record is not self-approval.

Superseded as latest verdict by the [eighth independent review](five-axis-state-eighth-review-2026-07-24.md), which retained `NEEDS REVISION`.

## Remaining Maturity Gaps

- Production state/resolver code still implements the earlier prototype contract.
- The static callsite scanner, evidence collectors, canonical identity registry, outcome catalog, route qualification records, and exhaustive terminal-cause tooling are specified but not implemented.
- Downstream records await approved `SYS-ENDING`, `SYS-NARRATIVE`, and `SYS-TEST` GDDs and full seven-day content.
