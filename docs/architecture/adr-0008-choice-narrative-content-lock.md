# ADR-0008: SYS-CHOICE / SYS-NARRATIVE Content Lock and Reachability Boundary

## Status

Accepted

## Date

2026-08-10

## Engine Compatibility

| Field | Value |
|---|---|
| **Engine** | Ren'Py 8.5.3 |
| **Domain** | Scripting / narrative flow / UI entry |
| **Knowledge Risk** | HIGH — 8.5.3 is newer than the May 2025 baseline |
| **References Consulted** | `docs/engine-reference/renpy/VERSION.md`, `modules/scripting.md`, `breaking-changes.md`, `deprecated-apis.md`, pinned SDK `doc/testcases.html`, `doc/persistent.html`, `doc/screen_actions.html` |
| **Post-Cutoff APIs Used** | Ren'Py 8.5 testcase framework; verified through the pinned SDK wrapper |
| **Verification Required** | Global testcase, lint/compile, source-manifest scan, CFG/reachability witnesses, and content-constraint scan for every locked unit |

## ADR Dependencies

| Field | Value |
|---|---|
| **Depends On** | ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0005, ADR-0006, ADR-0007 |
| **Enables** | Formal seven-day content production, narrative CFG manifests, SYS-JOURNAL owner catalogs |
| **Blocks** | SYS-NARRATIVE production stories until this Accepted decision is followed |
| **Ordering Note** | Content source is authored only after the required unit, choice, and terminal witness contracts are locked; SYS-BUILD validates but never rewrites it. |

## Context

### Problem Statement

SYS-CHOICE already commits authoritative choice records and SYS-NARRATIVE owns player-visible prose, but no accepted ADR previously owned their exact reaction/payoff joins, CFG shape, terminal continuation witnesses, and content-lock admission boundary.

### Constraints

- Exactly 15 canonical production units defined by `narrative_content_baseline:v1.3` are allowed. The v1.3 amendment extends only the existing `rain_stops` epilogue within its existing unit; it does not add a unit, choice, join, witness, or terminal contract.
- Every player-facing choice has one canonical ID, one immediate reaction identity, and a strictly later perceptible payoff or an explicitly recorded terminal payoff.
- Narrative may not read/write persistent state, hidden axes/tokens, resolver internals, test fixtures, network state, or player-facing score hints.
- Erii's complex intent is conveyed by approved action/object/context evidence rather than full spoken dialogue.
- The product remains offline, non-commercial, UTF-8, and compatible with Ren'Py 8.5.3 rollback/save semantics.

## Decision

SYS-NARRATIVE is the sole owner of player-visible unit text, scene beats, chapter/memory catalogs, and common-path truth approvals. SYS-CHOICE is the sole owner of canonical choice records and commits them through the rollback-owned state boundary. A build-time `narrative_flow_manifest:v1` is the only integration handoff between them and has these required projections:

```text
unit_id, source_hash, node_id, canonical_choice_id,
immediate_reaction_id, delayed_payoff_id, successor_node_ids,
terminal_entry_id, witness_ids
```

The manifest must exact-match the 15-unit baseline, contain no duplicate IDs, no unresolved successor/reference, no production-to-test-only edge, and one reachable terminal ending entry per terminal path. `delayed_payoff_id` must resolve after its choice commit in the same or a later unit; an ending-entry payoff is permitted only when its witness proves the player-visible closure occurs before `commit_ending_completion`.

```text
Narrative source (.rpy / owner catalogs)
          │
          ▼
SYS-CHOICE canonical records ──► narrative_flow_manifest:v1 ──► SYS-BUILD validation
          │                              │                         │
          ▼                              ▼                         ▼
rollback-owned state                 witnesses                 package/evidence
          │
          └──► SYS-ENDING deterministic resolver / completion boundary
```

### Key Interfaces

- `narrative_flow_manifest:v1`: immutable build input; owned by SYS-NARRATIVE; consumed by SYS-BUILD and SYS-TEST.
- `choice_source_scanner:v1`: deterministic scanner output owned by SYS-CHOICE; it identifies canonical choices and CFG edges but never copies player-visible prose.
- `reaction_payoff_binding`: exact tuple `(canonical_choice_id, immediate_reaction_id, delayed_payoff_id, source_unit_id, payoff_unit_id)`; duplicate or absent joins fail validation.
- `terminal_continuation_witness`: replayable ordered choice history proving node guards, joins, chapter boundaries, and exactly one ending entry.

## Alternatives Considered

### Alternative 1: Narrative-local choice and payoff bookkeeping

- **Description**: Each `.rpy` label tracks its own choice/reaction/payoff relationships.
- **Pros**: Fast initial authoring.
- **Cons**: Duplicates SYS-CHOICE authority and cannot prove global reachability or terminal coverage.
- **Rejection Reason**: Violates state ownership and makes content locks non-auditable.

### Alternative 2: Build system repairs incomplete content

- **Description**: SYS-BUILD fills missing IDs, ranks, or payoff links during packaging.
- **Pros**: Produces a package from incomplete source.
- **Cons**: Makes the build system a narrative owner and hides authoring defects.
- **Rejection Reason**: Conflicts with ADR-0003 and ADR-0007; incomplete source must fail closed.

## Consequences

### Positive

- Creates accepted coverage for `TR-CHOICE-002` and the content-lock portion of `TR-NAR-001`.
- Gives every Day 1–7 unit an auditable route from prose to state change to later payoff or ending.
- Keeps source ownership, build validation, and test evidence separate.

### Negative

- Authoring requires a manifest and witnesses alongside prose; freeform late edits are deliberately more expensive.

### Risks

- A valid-looking source change can invalidate a join or witness. Mitigation: source hashes and exact manifest validation fail closed.
- A content description can overstate mutually exclusive route facts. Mitigation: common-path truth approvals are owned by SYS-NARRATIVE and reviewed per unit.

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|---|---|---|
| `choice-and-causality-record.md` | TR-CHOICE-002 exact reaction/payoff joins and terminal continuation witness coverage | Defines authoritative tuple, CFG, and witness contracts. |
| `seven-day-chapter-script.md` | TR-NAR-001 canonical 15 units, valid paths, and content lock | Makes exact unit equality, source hash, and terminal reachability build-time gates. |
| `deterministic-ending-resolution.md` | One deterministic terminal resolver and completion boundary | Requires one ending entry per terminal path and preserves ADR-0006 ownership. |
| `sys-journal.md` | Owner-signed player-safe catalog inputs | Leaves source copy/truth approvals with SYS-NARRATIVE and forbids Journal rewrites. |
| `sys-build.md` | Validate source provenance without rewriting content | Constrains SYS-BUILD to validation, packaging, and evidence binding. |

## Performance Implications

- **CPU**: Source scanning is build/test-time only; gameplay does not enumerate paths.
- **Memory**: Runtime consumes compiled immutable catalogs only.
- **Load Time**: No dynamic CFG construction during startup.
- **Network**: None; network and telemetry remain forbidden.

## Migration Plan

1. Keep the existing prologue as the baseline unit and produce `narrative_flow_manifest:v1` during Sprint 1.
2. Add Day 1 source, bindings, and witnesses without changing the 15-unit contract.
3. Reject content changes lacking a new content-lock hash, tests, and required reviews.

### 2026-08-14 Amendment Check

The `rain_stops` years-later tail is an in-unit, post-lights-out prose
extension. It leaves the exact 15-unit manifest, canonical choices, joins,
terminal witnesses, resolver inputs, and completion ownership unchanged.
ADR-0008 remains **Accepted**; the amendment requires the existing source-hash,
content-identity, Erii constraint, and human review gates to be rerun before
the narrative expansion can be treated as final content.

## Validation Criteria

- The scanner finds exactly 15 canonical units and no production-to-test-only edge.
- Each discovered choice has one exact immediate reaction and one valid later/terminal payoff.
- Each terminal witness replay reaches exactly one ending entry and preserves ADR-0006 completion order.
- Lint, global Ren'Py testcases, content constraints, and owner source-hash checks pass.

## Related Decisions

- ADR-0001 through ADR-0007
- `design/gdd/choice-and-causality-record.md`
- `design/gdd/seven-day-chapter-script.md`
- `design/narrative/seven-day-content-baseline.md` (`narrative_content_baseline:v1.3`)
