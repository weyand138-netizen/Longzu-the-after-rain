# Story 008: Release handshake 与 terminal path inventory

> **Epic**: SYS-TEST — 自动化验证
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Integration
> **Estimate**: 4 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/sys-test.md`  
**Requirement**: `TR-TEST-001`

**ADR Governing Implementation**: ADR-0007: SYS-BUILD Contract Closure and Release Identity  
**Secondary ADRs**: ADR-0001, ADR-0002, ADR-0003, ADR-0006
**ADR Decision Summary**: SYS-BUILD 创建 candidate/staging identity，SYS-TEST 绑定 staging evidence；package/archive 完成后 SYS-TEST 再绑定 archive evidence。terminal path inventory 与 source/catalog/archive hash 必须同世代，不能自引用或拼接。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: package runner、archive inventory、archive hash、两阶段 exclusion 与 offline Windows build 需按 capability manifest 验证。

**Control Manifest Rules (this layer)**:
- Required: `candidate_manifest:v1`、`STAGING_EVIDENCE_BOUND`、`ARCHIVE_EVIDENCE_BOUND` 双阶段握手。
- Required: archive hash 只覆盖 exact package bytes；release identity 不含自引用 hash。
- Forbidden: 不得跨 candidate/generation 拼接 evidence，不能把 component PASS 升级为 RELEASE PASS。
- Guardrail: source roots/nodes/edges/terminal entries/path count 与 inventory exact-match。

---

## Acceptance Criteria

- [ ] `TEST-DOM-012`: 冻结 source/graph/catalog/maximum fixture 的 terminal path inventory exact-match；每条 path 绑定一个 ending/class/witness/payoff/summary。
- [ ] `TEST-GATE-006`: 消费 SYS-BUILD candidate/archive identity 时只读 current artifacts、hash 与 exclusion reports；修改 artifact/source/candidate 或缺少 owner contract 均失败。
- [ ] `TEST-ISO-005`: staging 与 archive 独立扫描 test-only 类型/IDs，所有排除规则 exact-match 且计数为 0。
- [ ] release handshake 在 staging evidence 未绑定前不运行 package runner，archive evidence 未绑定前不进入 READY。

## Implementation Notes

- candidate identity 不吸收 final archive/provenance hash；archive hash 不哈希包含自身 hash 的 manifest。
- archive scan 必须覆盖 formal saves、persistent root、test namespaces、observers、spies、synthetic artifacts 与 evidence forgers。
- terminal inventory 是 SYS-TEST evidence，不拥有 narrative/ending semantics。

## Out of Scope

- SYS-BUILD Epic：candidate/package/archive 实现。
- Story 003：general runner capability/isolation。
- Story 011：evidence bundle criterion traceability。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: staging-before-package and archive-after-package handshake; terminal inventory; identity binding; missing owner blocker.

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_test/release_handshake_inventory_test.py` — candidate generation、staging/archive evidence、terminal path inventory、archive hash/self-reference 与 exclusion scan。

**Status**: [x] Created and passing — 1 integration test

## Dependencies

- Depends on: Story 003, Story 004, Story 006, Story 007

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; candidate/evidence identity binding and zero-finding exclusion closure covered.
**Deviations**: Actual package-before/after handshake remains release-environment evidence.
**Test Evidence**: `tests/integration/sys_test/release_handshake_test.py`
**Code Review**: Complete — APPROVED; evidence identity cannot drift across candidate generations.
- Unlocks: Story 011
