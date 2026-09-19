# Regression Suite Manifest — Sprint 013 Preflight

Date: 2026-08-16
Trusted baseline: `HEAD ff00c7a`
Command: `python -m unittest discover`

This manifest adds coverage for the automation-only preflight while preserving every existing test file and historical evidence record. The root discovery bridge delegates to the established `tests/**/*_test.py` suite.

| Critical path | Registered coverage | Layer |
|---|---|---|
| Fixed seven-day topology and 15-unit source contract | `tests/integration/sys_narrative/sprint013_topology_test.py`, `sprint013_day_flow_test.py` | Integration |
| Six endings and single resolver handoff | `tests/integration/sys_narrative/sprint013_witness_replay_test.py`, topology tests | Integration |
| Save/persistence boundary | `tests/integration/sys_save/sprint013_e2e_persist_test.py` | Integration |
| Accessibility and semantic pairing classification | `tests/integration/sys_access/sprint013_production_matrix_test.py`, `tests/unit/sys_access/semantic_equivalence_contract_test.py` | Contract |
| Candidate/source identity and evidence classification | `tests/integration/sys_build/sprint013_release_evidence_test.py`, `tests/integration/sys_test/sprint013_evidence_completeness_test.py` | Integration |
| Performance protocol boundary | `tests/integration/sys_test/sprint013_performance_test.py` | Protocol / REPORT_ONLY |
| Production closeout classification | `tests/unit/sys_test/production_closeout_gate_test.py` | Unit |

## Layer boundary

Ordinary regression validates code contracts and fail-closed classification. Missing GUI runs, human witnesses, SAPI transcripts, semantic equivalence review, new-player playtest, formal performance samples, legal-owner input, and archive are not converted to PASS; they are asserted as `BLOCKED_INPUT` or `REPORT_ONLY` and are evaluated by the explicit Production closeout gate only.

The complete historical Sprint 013 test and evidence records remain present. No test is deleted or skipped to obtain a green ordinary regression result.
