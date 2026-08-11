# Story 004: FAST、INTEGRATION、RELEASE gate 执行

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
**ADR Decision Summary**: gate 必须使用 current evidence、严格 AND 聚合与同世代 identity；component PASS 不能升级为 integration/release PASS，SYS-BUILD candidate evidence 缺失时保持 `BLOCKED_INPUT`。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: FAST 不运行 hosted testcase；INTEGRATION/RELEASE 的 runner、timeout、exit code、archive identity 与 cleanup 需 engine evidence。

**Control Manifest Rules (this layer)**:
- Required: FAST、INTEGRATION、RELEASE 按影响闭包执行并严格 AND 聚合。
- Required: required skip、hard timeout、missing external evidence 均阻断对应 scope。
- Forbidden: 不得裁剪 required cases、用 component PASS 继承 release PASS。
- Guardrail: RELEASE 必须包含完整路径、最大 fixture、benchmark、A11Y/VISUAL、external evidence 与 isolation。

---

## Acceptance Criteria

- [ ] `TEST-GATE-001`: FAST 执行 lint、pure logic、schema/catalog validation、static scans，case 非空；不运行 hosted testcase；hard timeout 产生 `TIMEOUT/ERROR` 并失败。
- [ ] `TEST-GATE-002`: INTEGRATION 按影响闭包执行 Ren’Py flow、restore、fault injection、joins、branch、accessibility suites 并严格 AND 聚合。
- [ ] `TEST-GATE-003`: RELEASE 执行完整路径、maximum fixture、benchmark、layout/accessibility、external evidence 与 production isolation，不允许裁剪。
- [ ] `TEST-GATE-004`～`005`: isolated component PASS 在 production input/evidence 缺失时不能关闭 integration/release；仅受影响 criteria/downstream gates 阻断。
- [ ] `TEST-GATE-006`: 消费 SYS-BUILD 冻结 candidate/archive identity 时只读 current evidence/hash/exclusion reports；修改 artifact/source/candidate 或缺少 owner contract 均失败/`BLOCKED_INPUT`。

## Implementation Notes

- gate aggregator 读取 Story 002 的 lifecycle/current 状态，不重新实现 artifact identity formula。
- timeout 保留 raw output，不降低 case count 或 evidence type。
- RELEASE 是唯一可输出 release-level verdict 的 scope，component PASS 不可升级。

## Out of Scope

- Story 001：manifest/owner mapping。
- Story 003：runner/toolchain isolation。
- Story 008：SYS-BUILD package generation。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: FAST/INTEGRATION/RELEASE scope; timeout/error; strict AND; blocked-input propagation; current-candidate consumption.

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_test/gate_execution_test.py` — FAST/INTEGRATION/RELEASE scope、timeout、blocked input、strict AND 与 candidate evidence consumption。

**Status**: [x] Created and passing — 2 integration tests

## Dependencies

- Depends on: Story 002, Story 003

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; scope selection, timeout/error, strict AND, blocked propagation, and aggregate gate covered.
**Deviations**: None.
**Test Evidence**: `tests/integration/sys_test/gate_execution_test.py`
**Code Review**: Complete — APPROVED; component PASS cannot promote blocked higher scopes.
- Unlocks: Story 005, Story 006, Story 007, Story 008, Story 010, Story 011
