# Epic: SYS-TEST — 自动化验证

> **Layer**: Foundation
> **GDD**: design/gdd/sys-test.md
> **Architecture Module**: SYS-TEST
> **Status**: Complete
> **Stories**: Not yet created — run `/create-stories sys-test`

## Overview

建立覆盖 lint、纯逻辑、静态扫描、Ren’Py engine testcase、集成流程、性能、无障碍、视觉与外部证据的自动化验证系统。SYS-TEST 负责版本化 manifest、fixture、runner 结果、原始输出、current/stale 判定、严格 AND 聚合、生命周期和 evidence bundle；它验证各 owner system 的合同，但不重新定义产品语义、不拥有 production state、不替换 catalog，也不向 production 增加测试 seam。SYS-BUILD 先提供 candidate/staging identity，SYS-TEST 返回 staging evidence；归档生成后再返回 archive evidence，二者必须绑定同一候选世代。

## Governing ADRs

| ADR | Decision Summary | Engine Risk |
|-----|------------------|-------------|
| ADR-0001: Deterministic Ending Resolution | 固定结局 resolver、纯度、canonical vectors、cause/trace 与 ending completion 相关验证边界。 | LOW/HIGH integration |
| ADR-0002: Rollback and Persistence Boundary | 定义 rollback-owned 状态、persistent root、存档安全流程与 `APPLIED_FLUSHED` 边界的验证对象。 | HIGH |
| ADR-0003: Content and Presentation Boundary | 定义章节、稳定资源名、presentation 与 test-only source 隔离的验证边界。 | MEDIUM |
| ADR-0004: Semantic Ending Snapshot and Rollback State Envelope | 定义 detached snapshot、严格类型/状态验证与 imported Python 纯度边界。 | HIGH |
| ADR-0005: Counterevidence Ledger and Detectable State Initialization | 定义状态初始化、resolver 静态闭包、失败前置和测试观察边界。 | HIGH |
| ADR-0006: Ending Completion Boundary | 定义唯一 completion callsite、event shape、回放与 rollback 矩阵的验证边界。 | HIGH |
| ADR-0007: SYS-BUILD Contract Closure and Release Identity | 定义 candidate identity、canonical evidence、staging/archive 双阶段绑定、法律 provenance 与 test-only isolation。 | HIGH |

## GDD Requirements

| TR-ID | Requirement | ADR Coverage |
|-------|-------------|--------------|
| TR-TEST-001 | Lint, pure logic, engine testcase, and gate evidence control hand-off | ADR-0007 — Partial ✓ |

## Definition of Done

This epic is complete when:

- All stories are implemented, reviewed, and closed via `/story-done`
- All acceptance criteria from `design/gdd/sys-test.md` are verified
- All Logic and Integration stories have passing test files in `tests/`
- All Visual/Feel and UI stories have evidence docs with sign-off in `production/qa/evidence/`

## Known Gates

- The architecture review requires a dedicated SYS-TEST evidence-lifecycle ADR before the full hand-off contract can be considered closed.
- `tests/unit/`, `tests/integration/` and `.github/workflows/tests.yml` are currently missing and require `/test-setup`.
- Ren’Py 8.5.3 `testcase`/`testsuite`, runner exit-code behavior, save/persistent fault injection, and environment capability checks remain HIGH-risk implementation gates.
- SYS-TEST must keep component PASS separate from `BLOCKED_INPUT`, `STALE`, integration status and RELEASE status.
- The staging and archive exclusion scans must independently prove zero test-only, production-to-test-only, network, telemetry, undeclared and unallowlisted findings.

## Stories

| # | Story | Type | Status | ADR |
|---|-------|------|--------|-----|
| 001 | [Test framework manifest 与 owner traceability](story-001-test-framework-manifests.md) | Logic | Complete | ADR-0007 |
| 002 | [Artifact identity 与 lifecycle](story-002-artifact-lifecycle.md) | Logic | Complete | ADR-0007 |
| 003 | [Toolchain runner 与 production isolation](story-003-toolchain-isolation.md) | Integration | Complete | ADR-0007 |
| 004 | [FAST、INTEGRATION、RELEASE gate 执行](story-004-gate-execution.md) | Integration | Complete | ADR-0007 |
| 005 | [Player-critical causal evidence](story-005-player-critical-evidence.md) | Integration | Complete | ADR-0001 |
| 006 | [Core/feature contract coverage](story-006-core-feature-coverage.md) | Integration | Complete | ADR-0001 |
| 007 | [Foundation/presentation contract coverage](story-007-foundation-presentation-coverage.md) | Integration | Complete | ADR-0002 |
| 008 | [Release handshake 与 terminal path inventory](story-008-release-handshake-inventory.md) | Integration | Complete | ADR-0007 |
| 009 | [Performance、flaky 与 evidence retention protocol](story-009-performance-flaky-retention.md) | Logic | Complete | ADR-0007 |
| 010 | [External evidence 完整性与人工 adjudication](story-010-external-evidence-adjudication.md) | Integration | Complete | ADR-0003 |
| 011 | [Evidence bundle 与 registry traceability](story-011-evidence-bundle-traceability.md) | Logic | Complete | ADR-0007 |

## Next Step

Run `/story-readiness production/epics/sys-test/story-001-test-framework-manifests.md` before implementation.
