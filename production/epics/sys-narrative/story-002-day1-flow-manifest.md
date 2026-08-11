# Story 002: Day 1 Flow Manifest and Reachability Witness

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production  
> **Status**: Complete  
> **Last Updated**: 2026-08-10  
> **Layer**: Feature  
> **Type**: Integration  
> **Estimate**: 1 day  
> **Manifest Version**: 2026-08-04.1

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`  
**Requirement**: `TR-NAR-001` — Seven-day chapter paths and six endings are valid and content-locked; `TR-CHOICE-002` — exact reaction/payoff joins and terminal continuation witness coverage. Sprint 1 validates the formally present Day 1 subset only and does not claim either full requirement has completed.  
**Governing ADRs**: ADR-0008 (full production contract), ADR-0009 (partial Day 1 handoff boundary)  
**Engine**: Ren'Py 8.5.3 | **Risk**: High

**Traceability status**: `TR-NAR-001` remains `partial` because full production coverage is intentionally deferred; `TR-CHOICE-002` is covered. ADR-0009 authorizes the bounded Sprint 1 handoff artifact without weakening the full-production contract.

## Implementation Notes

- Produce `narrative_partial_day1_manifest:v1`, never `narrative_flow_manifest:v1`. It must declare `artifact_kind=partial_day1`, `full_production_manifest=false`, and `terminal_witness_coverage=not_applicable`.
- Exact-cover only `chapter_day1_her_own_name`, its owner source hash, Day 1 node/choice/reaction/delayed-payoff identities, source-local successors, and one `day1_handoff_node_id`.
- The handoff witness proves guards, joins, present-source successors, and arrival at the controlled Day 1 handoff only. It has no terminal-entry or ending semantics.
- Reject future units/placeholders, ending IDs, terminal entry IDs, direct ending edges, unresolved references, production-to-test-only edges, stale hashes, and runtime source scan or CFG/path enumeration.

## Out of Scope

- A full `narrative_flow_manifest:v1`, 15-unit exact equality, terminal ending witnesses, SYS-BUILD admission, release evidence, future chapters/endings, and any runtime graph scanner or enumerator.
- New player-visible prose, UI/layout changes, asset admission, and changes to SYS-CHOICE authoritative state ownership.

## Performance Notes

No runtime performance impact is permitted. The partial manifest is immutable build/test-time data; runtime source scan, CFG construction, and path enumeration counts must remain zero.

## Acceptance Criteria

- [ ] Produce `narrative_partial_day1_manifest:v1` with the Day 1 source hash, canonical choice IDs, immediate reactions, registered delayed-payoff identities, present-source successors, handoff node, and witness references; it must explicitly be non-production.
- [ ] Validate exact joins from every Day 1 choice to one immediate reaction and one registered strictly later payoff identity without claiming payoff execution or a terminal continuation.
- [ ] Add a replayable Day 1 handoff witness proving enabled guards, no unresolved present-source successor, and arrival at exactly one controlled Day 1 handoff node.
- [ ] Reject future placeholder, ending, terminal-entry, direct-ending, and production-to-test-only edges; prohibit runtime CFG/path enumeration and reject the partial artifact from full-production/release validators.

## QA Test Cases

- **AC-1**: Given the Day 1 source, when scanner and `narrative_partial_day1_manifest:v1` generation run, then `artifact_kind=partial_day1`, source hash, node ID, canonical choice ID, immediate reaction ID, delayed payoff ID, present-source successor IDs, `day1_handoff_node_id`, and witness IDs are present and resolve; `full_production_manifest=false` and `terminal_witness_coverage=not_applicable` are exact.
- **AC-2**: Given missing, duplicated, generic, stale, or unresolved reaction/payoff binding mutants, when validation runs, then it fails closed with no repaired or emitted partial artifact.
- **AC-3**: Given the canonical Day 1 handoff witness, when replayed from the canonical prologue state through the formally present Day 1 source, then every guard and present-source successor is valid, each choice has one immediate reaction and a registered strictly later payoff identity, and exactly one controlled Day 1 handoff node is reached.
- **AC-4**: Given a future placeholder, ending ID, terminal-entry ID, direct-ending, production-to-test-only edge, dangling successor, or mutated guard, when validation runs, then the artifact is rejected; runtime source scanning and CFG/path enumeration remain zero; full-production/release validators reject the partial schema.

**Required test path**: `tests/integration/sys_narrative/day1_flow_manifest_test.py`

## Test Evidence

- Integration validation: `tests/integration/sys_narrative/day1_flow_manifest_test.py`
- Content-constraint scan: `tools/test-content-constraints.ps1`
- Owner source hash: `production/qa/evidence/day1-authored-source-evidence.md`
- Partial-manifest evidence: `production/qa/evidence/day1-flow-manifest-evidence.md`

## Dependencies

- Depends on: Story 001.
- Unlocks: Story 003 and SYS-BUILD Day 1 admission work.

## Completion Notes

**Completed**: 2026-08-10  
**Criteria**: 4/4 passing  
**Deviations**: None. ADR-0009 explicitly scopes this artifact as partial and non-production; full 15-unit manifest and terminal witnesses remain deferred.  
**Test Evidence**: Integration test at `tests/integration/sys_narrative/day1_flow_manifest_test.py` (15/15 passing); owner hash evidence at `production/qa/evidence/day1-authored-source-evidence.md`; partial-manifest evidence at `production/qa/evidence/day1-flow-manifest-evidence.md`; content-constraint scan, Ren'Py global tests, and lint/compile passed.  
**Code Review**: Skipped — Solo review mode.
