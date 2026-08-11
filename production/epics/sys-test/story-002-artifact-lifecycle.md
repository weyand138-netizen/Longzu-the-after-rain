# Story 002: Artifact identity 与 lifecycle

> **Epic**: SYS-TEST — 自动化验证
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Logic
> **Estimate**: 4 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/sys-test.md`  
**Requirement**: `TR-TEST-001`

**ADR Governing Implementation**: ADR-0007: SYS-BUILD Contract Closure and Release Identity  
**ADR Decision Summary**: evidence 必须绑定 exact identity generation、source/catalog/config/fixture/runner/environment hashes 和 raw output；输入改变时 artifact 立即 stale，失败或中断不能恢复为 PASS。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: host/Ren’Py process termination、runner exit code 与 cleanup behavior 需要 pinned capability evidence。

**Control Manifest Rules (this layer)**:
- Required: lifecycle 只允许 `READY → RUNNING → PASSED_CURRENT`，失败进入 `FAILED`，identity 改变进入 `STALE`。
- Required: `BLOCKED_INPUT`、`REPORT_ONLY` 不能成为成功结果。
- Forbidden: partial output 不得被恢复为 PASS，stale PASS 不得参与 gate。
- Guardrail: criterion pass 必须同时满足 nonempty、exact cases、evidence coverage、current、PASS、无 blocking finding。

---

## Acceptance Criteria

- [ ] `TEST-LIFE-001`: 缺失 manifest 或外部输入分别进入 `UNBOUND`/`BLOCKED_INPUT`，不能进入 `RUNNING`/`PASSED_CURRENT`。
- [ ] `TEST-LIFE-002`～`003`: 有效 run 严格完成 `READY → RUNNING → PASSED_CURRENT`；assertion、runner、case-count、hash、exit-code 或 cleanup failure 进入 `FAILED`，修复后必须重新运行。
- [ ] `TEST-LIFE-004`: source/catalog/config/fixture/runner/environment identity 任一改变，artifact 立即 `STALE`，不能参与 gate。
- [ ] `TEST-LIFE-005`: 宿主或 Ren’Py 进程中止后 partial output 仅作诊断，artifact=`ERROR`、lifecycle=`FAILED`。
- [ ] `TEST-LIFE-006`～`008`: `test_artifact_current`、`test_criterion_pass`、`test_gate_pass` 的 truth tables 严格执行，required artifacts/cases/evidence 全部 current/PASS 且无 blocking finding 才通过。

## Implementation Notes

- 用 exact identity key set、generation、完整 SHA-256 和 raw output presence 计算 current。
- `criterion_status=BLOCKED_INPUT` 与 formula False 同时保留，不把缺输入伪装成 FAIL 或 PASS。
- scope 修复后必须从 READY 重新开始，不允许手工覆盖失败 artifact。

## Out of Scope

- Story 001：manifest 生成与 owner traceability。
- Story 004：gate runner orchestration。
- Story 009：benchmark protocol 细节。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: UNBOUND/BLOCKED_INPUT; current/stale lifecycle; formula truth table; partial/error/report-only handling.

## Test Evidence

**Story Type**: Logic  
**Required evidence**:
- `tests/unit/sys_test/artifact_lifecycle_test.py` — lifecycle transitions、stale/current、formula truth tables、partial/error 与 blocked input。

**Status**: [x] Created and passing — 2 unit tests

## Dependencies

- Depends on: Story 001

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; UNBOUND/BLOCKED_INPUT, current/stale, and non-promoting lifecycle states covered.
**Deviations**: None.
**Test Evidence**: `tests/unit/sys_test/artifact_lifecycle_test.py`
**Code Review**: Complete — APPROVED; blocked and stale artifacts cannot become PASS.
- Unlocks: Story 004, Story 011
