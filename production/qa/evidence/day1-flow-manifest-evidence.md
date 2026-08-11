# Day 1 Partial Manifest Evidence

**Story**: `production/epics/sys-narrative/story-002-day1-flow-manifest.md`  
**ADR**: ADR-0009  
**Artifact schema**: `narrative_partial_day1_manifest:v1`  
**Recorded**: 2026-08-10

## Boundary

- `artifact_kind`: `partial_day1`
- `source_unit_id`: `chapter_day1_her_own_name`
- **Source SHA-256**: `7bcf51ae66b558703b453125bd7f804346895ce7d24757be3fd0b643dfdf8aa9`
- `day1_handoff_node_id`: `node_day1_handoff`
- `full_production_manifest`: `false`
- `terminal_witness_coverage`: `not_applicable`

## Validation Record

The partial artifact exact-covers six Day 1 choice/reaction/payoff identities and
replays `witness_day1_handoff_v1` from the canonical prologue state to the controlled
Day 1 handoff only. It contains no future placeholder, ending ID, terminal entry,
direct-ending edge, or production-to-test-only edge.

`tests/integration/sys_narrative/day1_flow_manifest_test.py` validates successful
construction and fail-closed handling for duplicate, stale, unresolved, future,
ending, terminal, direct, test-only, invalid-witness, and full-production-promotion
mutants. Full production, terminal-witness, SYS-BUILD admission, and release use are
rejected by `reject_full_production_promotion`.
