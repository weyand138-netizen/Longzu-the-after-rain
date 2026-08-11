# ADR-0009: Partial Day 1 Manifest and Handoff Boundary

## Status

Accepted

## Date

2026-08-10

## Engine Compatibility

| Field | Value |
|---|---|
| **Engine** | Ren'Py 8.5.3 |
| **Domain** | Scripting / build-time narrative content validation |
| **Knowledge Risk** | HIGH — pinned version is newer than the May 2025 baseline |
| **References Consulted** | `docs/engine-reference/renpy/VERSION.md`, `modules/scripting.md`, `breaking-changes.md`, `deprecated-apis.md` |
| **Post-Cutoff APIs Used** | None; the artifact uses the existing pinned-SDK validation workflow only |
| **Verification Required** | Python validation tests, source-hash verification, Ren'Py global testcases, lint/compile, and production/test-edge scan |

## ADR Dependencies

| Field | Value |
|---|---|
| **Depends On** | ADR-0003, ADR-0008 |
| **Enables** | Sprint 1 Story 002 Day 1 flow-manifest and handoff implementation |
| **Blocks** | Full `narrative_flow_manifest:v1` and terminal ending witnesses until every canonical source unit exists |
| **Ordering Note** | The partial artifact may be implemented only after its source unit and owner hash exist; it is replaced by the full production manifest after all 15 canonical units exist. |

## Context

### Problem Statement

ADR-0008 defines `narrative_flow_manifest:v1` as a complete production artifact: it must exact-match all 15 canonical units and prove terminal continuation witnesses. Sprint 1 has only the prologue and Day 1 source units. Requiring the complete artifact now would force future placeholders, a direct ending edge, or test-only material, all of which violate the content-lock boundary.

### Constraints

- The existing `narrative_flow_manifest:v1` contract remains a complete production contract and is not weakened.
- Sprint 1 validates only source that formally exists; it must not invent future chapters, ending units, or test-only successors.
- Every Day 1 choice still requires its canonical immediate reaction and registered strictly-later payoff identity.
- Runtime performs no source scan or CFG/path enumeration; this artifact is build/test-time data only.
- The product remains UTF-8, offline, and uses only the pinned Ren'Py 8.5.3 workflow.

### Requirements

- Provide a deterministic, source-hash-bound Day 1 handoff artifact for Sprint 1.
- Fail closed on missing, duplicate, stale, unresolved, future, ending, or test-only references.
- Make it impossible to submit the partial artifact to a production-manifest, release, or terminal-witness gate.

## Decision

Sprint 1 may produce exactly one `narrative_partial_day1_manifest:v1` artifact. It is a non-production handoff artifact, not a subtype, temporary alias, or relaxed variant of `narrative_flow_manifest:v1`.

The partial artifact exact-covers the formally present Day 1 source unit `chapter_day1_her_own_name`, its owner source hash, Day 1 node IDs, canonical choice IDs, immediate reaction IDs, delayed-payoff IDs, and one controlled `day1_handoff_node_id`. The handoff node represents the boundary after Day 1 source; it is not an ending entry and has no terminal semantics.

The artifact must not contain a `terminal_entry_id`, ending ID, terminal witness, future source unit, future placeholder, direct ending edge, production-to-test-only edge, or runtime scanner/enumerator dependency. Its validation result must state `full_production_manifest=false` and `terminal_witness_coverage=not_applicable`.

Only after all 15 canonical source units exist may the project generate `narrative_flow_manifest:v1`, exact-match it to `narrative_content_baseline:v1.2`, and run terminal ending witnesses under ADR-0008. A partial artifact is rejected if passed to any full-production, SYS-BUILD admission, release, or terminal-witness validator.

### Architecture Diagram

```text
Day 1 source + owner hash
          |
          v
narrative_partial_day1_manifest:v1
          |
          +--> controlled Day 1 handoff node (non-terminal)
          |
          +--> Sprint 1 source/join validation only

All 15 formal source units + canonical records
          |
          v
narrative_flow_manifest:v1 --> terminal witnesses --> SYS-BUILD / SYS-TEST
```

### Key Interfaces

- `narrative_partial_day1_manifest:v1`: immutable build/test artifact owned by SYS-NARRATIVE and consumed only by Sprint 1 validation.
- Required identity fields: `artifact_kind=partial_day1`, `source_unit_id`, `source_hash`, `node_id`, `canonical_choice_id`, `immediate_reaction_id`, `delayed_payoff_id`, `successor_node_ids`, `day1_handoff_node_id`, and `witness_ids`.
- Required boundary fields: `full_production_manifest=false` and `terminal_witness_coverage=not_applicable`.
- `day1_handoff_witness`: a replayable ordered Day 1 history that proves enabled guards, exact joins, resolved present-source successors, and arrival at the controlled handoff node only.
- `narrative_flow_manifest:v1`: unchanged complete-production interface from ADR-0008; its `terminal_entry_id` and terminal witness requirements remain mandatory.

## Alternatives Considered

### Alternative 1: Wait for all 15 source units

- **Description**: Defer all manifest work until Day 2–7, endings, and epilogue source units are authored.
- **Pros**: Requires no interim interface.
- **Cons**: Prevents Sprint 1 from validating Day 1 identity, joins, and provenance at the time the content is authored.
- **Rejection Reason**: It delays a useful, bounded validation handoff and removes the source-hash gate from the first production unit.

### Alternative 2: Use future placeholders or direct ending edges

- **Description**: Add synthetic successors for unimplemented chapters or jump Day 1 directly to an ending entry.
- **Pros**: Makes a superficially complete graph available immediately.
- **Cons**: Invents production content, produces false terminal coverage, and risks production-to-test-only leakage.
- **Rejection Reason**: Violates ADR-0008 and the content-lock contract.

### Alternative 3: Let the partial artifact masquerade as the production manifest

- **Description**: Use `narrative_flow_manifest:v1` with relaxed unit and terminal requirements during Sprint 1.
- **Pros**: Reuses one schema name.
- **Cons**: Makes build/release consumers unable to distinguish incomplete coverage from a valid production contract.
- **Rejection Reason**: Weakens the accepted production interface and can falsely promote incomplete evidence.

## Consequences

### Positive

- Day 1 gains immediate source-hash and exact-join validation without claiming full game coverage.
- The full production manifest remains strict, auditable, and unambiguous.
- The handoff node makes the incomplete boundary explicit to SYS-NARRATIVE, SYS-CHOICE, SYS-BUILD, and SYS-TEST.

### Negative

- Sprint 1 maintains a distinct, deliberately non-promotable validation schema.
- The partial artifact must be retired/replaced once all formal source units exist.

### Risks

- A consumer might accidentally accept the partial artifact as release evidence. Mitigation: schema name, required false/not-applicable boundary fields, and explicit rejection in full-production validators.
- A future source reference could slip into the Day 1 graph. Mitigation: exact present-source set validation and fail-closed diagnostics.
- A stale source edit could invalidate joins. Mitigation: owner source hash is required and stale hashes reject emission.

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|---|---|---|
| `seven-day-chapter-script.md` | `NARR-MANIFEST-001/002`: production manifest exact-matches all canonical units and rejects unresolved/test-only edges | Preserves that requirement exclusively for the full production manifest and prevents the partial artifact from being used as a PASS for it. |
| `seven-day-chapter-script.md` | `NARR-FLOW-001`, `NARR-PAYOFF-001`: each production choice has one reaction and a strictly later payoff | Requires exact Day 1 joins and a controlled handoff witness without inventing terminal continuation coverage. |
| `choice-and-causality-record.md` | `TR-CHOICE-002`: exact reaction/payoff joins and terminal continuation witnesses | Keeps terminal witnesses deferred to the full artifact while validating Day 1 joins now. |

## Performance Implications

- **CPU**: Build/test-time scanning and validation only; no runtime source scan or CFG/path enumeration.
- **Memory**: Immutable records only; no runtime mutable state.
- **Load Time**: No startup graph construction or catalog injection.
- **Network**: None.

## Migration Plan

1. Implement and validate `narrative_partial_day1_manifest:v1` from the completed Day 1 source and owner hash.
2. Preserve it only as Sprint 1 validation evidence; do not submit it to production or release gates.
3. After all 15 formal source units exist, generate the unchanged full `narrative_flow_manifest:v1`, execute terminal witnesses, and mark partial evidence superseded.

## Validation Criteria

- The artifact exact-matches the present Day 1 unit, its current hash, declared Day 1 nodes, and all canonical Day 1 choice/reaction/payoff bindings.
- A missing, duplicate, stale, unresolved, future, ending, direct-terminal, or production-to-test-only reference fails closed and emits no artifact.
- The handoff witness replays only through present Day 1 source and ends at exactly one controlled `day1_handoff_node_id`.
- The artifact exposes no `terminal_entry_id` and is rejected by full-manifest, terminal-witness, SYS-BUILD admission, and release validators.
- Targeted Python tests, content-constraint scan, Ren'Py global tests, and lint/compile pass using the pinned SDK.

## Related Decisions

- ADR-0003: Content and Presentation Boundary
- ADR-0008: SYS-CHOICE / SYS-NARRATIVE Content Lock and Reachability Boundary
- `design/gdd/seven-day-chapter-script.md`
- `design/gdd/choice-and-causality-record.md`
