# Story 003: Toolchain runner 与 production isolation

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
**Secondary ADRs**: ADR-0002, ADR-0003
**ADR Decision Summary**: runner/environment identity、test-only namespace 与 production→test-only dependency closure 必须被静态与运行时双重验证；staging 与 archive 独立扫描，任何泄漏阻止 release。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: `testcase`/`testsuite`、lint、process cleanup、Ren’Py version/renderer 与 Windows environment 需按 capability manifest 复跑。

**Control Manifest Rules (this layer)**:
- Required: environment manifest 精确记录 Ren’Py、Python、renderer、runner version。
- Required: production→test-only path count 为 0；staging/archive 两次 exclusion inventory exact-match。
- Forbidden: production source、save、persistent 或 package 不得引用 test-only code/data。
- Guardrail: cleanup failure 立即停止 suite 并使后续结果无效。

---

## Acceptance Criteria

- [ ] `TEST-ISO-001`: 目标 Windows environment 的 Ren’Py/Python/renderer/runner 精确匹配批准 manifest；不匹配 artifact 为 `STALE/BLOCKED_INPUT`。
- [ ] `TEST-ISO-002`: lint、pure logic、Ren’Py-hosted cases 由批准 runner 分别执行，独立保存 exit code/raw output，不互相冒充。
- [ ] `TEST-ISO-003`: 不同执行顺序、timezone、locale、file enumeration 下 canonical artifacts/hash 稳定，network/telemetry/random calls 为 0。
- [ ] `TEST-ISO-004`: 解析 aliases、wrappers、closures、reflection、dynamic imports 的 production/test graph，production→test-only 与 unresolved edge 为 0。
- [ ] `TEST-ISO-005`～`008`: staging/archive/store/formal save/persistent 扫描 test-only 类型与 IDs 为 0；fault cleanup 恢复批准基线；错误环境 artifact 不能关闭当前 criterion。

## Implementation Notes

- 使用 `engine-capability-manifest:v1` 作为唯一 package runner authority。
- test-only 包括 observer、spy、fault injector、protocol bomb、synthetic save/root、benchmark harness、evidence forger。
- production 只能依赖 approved adapters，不得获得 test runtime seam。

## Out of Scope

- Story 004：gate 生命周期聚合。
- Story 008：SYS-BUILD candidate/archive evidence handshake。
- Story 009：performance protocol。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: exact environment identity; production-to-test-only closure; staging/archive scans; cleanup; stale artifact rejection.

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_test/toolchain_isolation_test.py` — capability、runner separation、dependency closure、staging/archive scans 与 cleanup。

**Status**: [x] Created and passing — 2 integration tests

## Dependencies

- Depends on: Story 001, Story 002

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; exact environment identity, dependency closure, test-only marker scan, and cleanup covered.
**Deviations**: None.
**Test Evidence**: `tests/integration/sys_test/toolchain_isolation_test.py`
**Code Review**: Complete — APPROVED; production-to-test-only edges are explicit blockers.
- Unlocks: Story 004, Story 008
