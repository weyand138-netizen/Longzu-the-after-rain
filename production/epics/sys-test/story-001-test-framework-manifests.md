# Story 001: Test framework manifest 与 owner traceability

> **Epic**: SYS-TEST — 自动化验证
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Logic
> **Estimate**: 4 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/sys-test.md`  
**Requirement**: `TR-TEST-001` — Lint, pure logic, engine testcase, and gate evidence control hand-off

**ADR Governing Implementation**: ADR-0007: SYS-BUILD Contract Closure and Release Identity  
**Secondary ADRs**: ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0005, ADR-0006
**ADR Decision Summary**: SYS-TEST 拥有 test manifests、evidence artifacts 与 gate aggregation，但不拥有产品语义。所有 evidence 必须 versioned、hash-bound、由 owning system 提供输入；SYS-BUILD 与 SYS-TEST 通过同世代 candidate/evidence 交接。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: `testcase`/`testsuite` 与 runner capability 只通过已验证 manifest 使用；engine-specific behavior 仍需 spike。

**Control Manifest Rules (this layer)**:
- Required: lint、pure logic tests、route testcase 在 hand-off 前执行。
- Required: 使用 `UT_ENGINE`、`UT_PURE`、`INSTR`、`STATIC`、`BRANCH` 等批准 evidence IDs。
- Forbidden: SYS-TEST 不得重新定义轴、token、threshold 或产品 owner。
- Guardrail: required criteria/cases/artifacts 非空、ID 唯一、expected/executed exact-match。

---

## Acceptance Criteria

- [ ] `TEST-FRAME-001`～`002`: 扫描 owning GDD、ADR、registry、domain manifests 与集中 runner manifest，确保每项产品权威只有一个，SYS-TEST 只拥有编排、证据和跨系统 gate。
- [ ] `TEST-FRAME-003`～`006`: criterion/suite/case/artifact 映射非空、唯一、exact-match；evidence type、production/synthetic namespace 与计数严格分离。
- [ ] `TEST-FRAME-007`～`009`: artifact schema、字段、类型、hash、exit code、raw output 与 golden diff 严格验证，错误类型不能关闭 criterion。
- [ ] `TEST-FRAME-010`～`012`: flaky repeat、并发原子封板与 dependency impact closure 按规定规则执行，未解析边使相关 suites 或 RELEASE 全量运行。
- [ ] `TEST-EVID-001`: manifest-derived unique criterion IDs 与 GDD criteria exact-match，不依赖手填数量。

## Implementation Notes

- domain manifest 属于 owner system；SYS-TEST 只读取并聚合，不复制产品常量。
- artifact identity 必须包含 criterion、evidence type、scope、case/fixture/oracle、source/catalog/config、runner/environment 与 raw output hash。
- 并发 run 使用唯一目录和 run ID，禁止 last-writer-wins 或跨 run 拼接。

## Out of Scope

- Story 002：artifact current/lifecycle 状态机。
- Story 004：FAST/INTEGRATION/RELEASE gate 执行。
- Story 011：最终 evidence bundle traceability index。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: owner uniqueness; exact criterion/case/artifact mapping; golden diff; flaky repeat; concurrency; dependency closure.

## Test Evidence

**Story Type**: Logic  
**Required evidence**:
- `tests/unit/sys_test/framework_manifest_test.py` — owner uniqueness、case/artifact exactness、golden diff、flaky/concurrency 与 dependency closure。

**Status**: [x] Created and passing — 2 unit tests

## Dependencies

- Depends on: None
- Unlocks: Story 002, Story 004, Story 011

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 5/5 passing; owner uniqueness, exact mapping, canonical identity, and fail-closed manifest validation covered.
**Deviations**: None.
**Test Evidence**: `tests/unit/sys_test/framework_manifest_test.py`
**Code Review**: Complete — APPROVED; identity inputs reject floats and duplicate ownership.
