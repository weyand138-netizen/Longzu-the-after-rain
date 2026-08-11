# Story 013: Release build evidence 与 isolation

> **Epic**: SYS-PERSIST — 跨周目解锁
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Integration
> **Estimate**: 4 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/cross-playthrough-unlocks.md`  
**Requirement**: `TR-PERSIST-001`

**ADR Governing Implementation**: ADR-0002: Rollback and Persistence Boundary  
**Secondary ADR**: ADR-0006
**ADR Decision Summary**: release gate 必须证明唯一 root schema、manifest、catalog generation、source hashes 与 writer allowlist 一致，并通过 `persist_evidence_contract:v1` 绑定完整 current evidence；legacy/test roots、spies、fault injectors、pending ledger 不得进入 release。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: release package、staging/archive scan、runner capability 与 evidence exit code 需按 ADR-0007 的验证门槛执行。

**Control Manifest Rules (this layer)**:
- Required: candidate/source/catalog/config/runner/environment identity 与 evidence exact-match。
- Required: staging/archive 两阶段 exclusion scan，production-to-test-only findings 为 0。
- Forbidden: 不得让 test-only root、pending ledger、benchmark harness 或 unknown writer 进入 package/save/persistent。
- Guardrail: evidence bundle 必须完整、非空、同世代、包含 raw artifacts；summary-only 不可接受。

---

## Acceptance Criteria

- [ ] `PERSIST-BUILD-001`: release candidate 的 root schema、manifest、catalog generation、source hashes、writer allowlist 与 archives 全部匹配；legacy flat fields、test roots、spies、fault injectors、benchmark harness、pending ledger、unknown writers 均为 0。
- [ ] `PERSIST-BUILD-002`: `persist_evidence_contract:v1` bundle 含恰 60 个 unique criterion IDs，每项有同世代 source/catalog hash、runner/environment/fixture/assertion/raw-sample metadata 与 exit code 0 的 PASS artifact；缺失、stale、case count 错误、空 manifest、summary-only 或 unresolved blocker 均不能 accepted。

## Implementation Notes

- SYS-PERSIST 只输出 owner evidence；SYS-BUILD 拥有 candidate/archive/package bytes，SYS-TEST 拥有 evidence/result/scan artifacts。
- test-only exclusion 必须覆盖 formal saves、persistent payload、runtime source、archive 与 staging tree。
- evidence 不得跨 candidate identity、generation 或 archive hash 拼接。

## Out of Scope

- SYS-BUILD Epic：完整 package runner、legal provenance 与 archive implementation。
- SYS-TEST Epic：通用 evidence lifecycle、gate aggregation 与 criterion manifest。
- Story 001：root/manifest implementation。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: candidate/legal/asset closure; staging/archive isolation; archive hash independence; current evidence prerequisite.

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_persist/build_evidence_test.py` — schema/writer scan、test-only exclusion、60-criterion bundle、cross-generation/stale/missing evidence。

**Status**: [x] Created and passing — 1 integration test

## Dependencies

- Depends on: Story 001, Story 004, Story 011, Story 012

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; candidate identity, archive/exclusion closure, and current evidence binding covered.
**Deviations**: Ren'Py package execution is unavailable locally; package-runner evidence remains a release-stage warning.
**Test Evidence**: `tests/integration/sys_persist/build_evidence_test.py`
**Code Review**: Complete — APPROVED; archive hash is package-bytes-only and cross-generation identity is rejected.
- Unlocks: None
