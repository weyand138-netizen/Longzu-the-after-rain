# Story 012: Production catalog freeze 与 release evidence

> **Epic**: SYS-SAVE — 存档、读档与回退
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Integration
> **Estimate**: 4 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/save-load-rollback.md`  
**Requirement**: `TR-SAVE-001`, `TR-SAVE-002`

**ADR Governing Implementation**: ADR-0007: SYS-BUILD Contract Closure and Release Identity  
**Secondary ADRs**: ADR-0002, ADR-0004, ADR-0005
**ADR Decision Summary**: release candidate 必须使用 frozen candidate identity、canonical catalog/source hashes、两阶段 SYS-TEST evidence、test-only isolation 与 archive closure。SYS-SAVE compatibility ready 不能在 production mappings、generation 或 evidence 不完整时宣称通过。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: `launcher distribute`、`testcase`/`testsuite` 只可通过已验证 capability manifest 使用；CLI 与 runner 在实现前需重新执行 capability probe。

**Control Manifest Rules (this layer)**:
- Required: 使用 `engine-capability-manifest:v1`，并绑定 runner version/path/hash、command、exit code、raw output、timeout 与 cleanup。
- Required: SYS-TEST 在 package 前后分别绑定 staging/archive exclusion evidence。
- Forbidden: 不得把 test-only observer、synthetic save、benchmark harness 或 evidence forger 带入 production/runtime/save。
- Guardrail: candidate identity、catalog/source hash、archive hash 与 evidence 必须同世代 exact-match。

---

## Acceptance Criteria

- [ ] `SAVE-BUILD-001`: SYS-NARRATIVE mappings 未批准、任一 source/generation hash 不匹配、catalog validator 或 fixture coverage validator 失败时，production checkpoint catalog 不得冻结，构建不得宣称 save compatibility ready。
- [ ] `SAVE-BUILD-002`: release candidate 的 archive、store 与 save payload 中不存在 protocol bombs、spies、benchmark harness、synthetic saves 或 traversal counters。
- [ ] `SAVE-BUILD-003`: SYS-SAVE gate evidence 包含 nonempty classification cross-product、12 项 origin/checkpoint matrix、fixture→production coverage、I/O faults、loaded-save rollback、ending rollback、persistent isolation、accessibility traversal、catalog/source hash 与完整性能 raw samples；manifest 为空、case count 不符或证据缺失均失败。

## Implementation Notes

- SYS-BUILD 拥有 candidate/staging/archive manifest 与 package bytes；SYS-TEST 拥有 evidence/result/scan artifacts；双方不得修改对方产物。
- archive hash 只覆盖 exact package bytes，不哈希包含自身 archive hash 的 manifest。
- staging 与 archive exclusion scan 必须独立执行，不能用 component PASS 替代 RELEASE evidence。
- candidate identity 输入使用 UTF-8、LF、canonical JSON、稳定 key/path 顺序、exact integers、无 timestamp/default。

## Out of Scope

- Story 003：catalog validator 的基础 schema/join 实现。
- SYS-BUILD Epic：完整 Windows package runner、legal registry 与 archive implementation。
- SYS-TEST Epic：通用 evidence lifecycle 与 gate aggregator。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: candidate identity/archive hash; staging and archive exclusion scans; evidence completeness; cross-generation rejection.

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_save/build_evidence_test.py` — freeze blockers、candidate identity、test-only scan、evidence completeness 与 cross-generation rejection。

**Status**: [x] Created and passing — 1 integration test

## Dependencies

- Depends on: Story 003, Story 011

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; candidate/archive identity, exclusion closure, and current evidence binding covered.
**Deviations**: Ren’Py package execution and final archive scan require the pinned engine/release environment.
**Test Evidence**: `tests/integration/sys_save/build_evidence_test.py`
**Code Review**: Complete — APPROVED; archive hash is package-only and cross-generation evidence is rejected.
- Unlocks: None
