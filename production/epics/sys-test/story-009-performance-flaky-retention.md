# Story 009: Performance、flaky 与 evidence retention protocol

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
**Secondary ADR**: ADR-0002
**ADR Decision Summary**: benchmark protocol、raw samples、identity/threshold binding、hard timeout、flaky diagnosis 与 retention 必须确定性地生成 evidence；报告不足 threshold 时只能 `REPORT_ONLY`，不能关闭 required criterion。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: runner timeout、Ren’Py hosted benchmark、environment identity 与 process cleanup 需目标环境复跑。

**Control Manifest Rules (this layer)**:
- Required: nearest-rank percentile、完整 raw samples、approved threshold 与 benchmark identity。
- Required: diagnostic repeat count 只诊断 flaky，不覆盖原失败。
- Forbidden: 不得用通过率、插值、偶然重复 PASS 或缺 threshold 生成 PASS。
- Guardrail: hard timeout 产生 `TIMEOUT/ERROR`；release/human/playtest evidence 不受 retention 清理。

---

## Acceptance Criteria

- [ ] `TEST-PERF-001`: nearest-rank percentile 对奇偶样本与边界值返回 `sort(X)[ceil(p×n)-1]`，不插值。
- [ ] `TEST-PERF-002`～`004`: performance pass 只有全部 metric/operator/threshold 通过才为 True；无 approved threshold 为 `REPORT_ONLY`；NaN/∞/negative/wrong type/missing/不足样本固定失败。
- [ ] `TEST-PERF-005`: FAST hard timeout 产生 `TIMEOUT/ERROR`、scope failure 与 raw output；feedback target 不能改变 hard timeout/case count。
- [ ] `TEST-PERF-006`: diagnostic repeat count 2/3/10 精确执行，越界预检失败，重复 PASS 不覆盖原失败。
- [ ] `TEST-PERF-007`: retention 只删除超出目标的非-release diagnostic artifacts，保留 release、human/playtest 与公开追溯 evidence。

## Implementation Notes

- benchmark threshold 必须由 owning system 批准，SYS-TEST 不自行发明预算。
- raw sample、protocol、runner、environment 与 input identity 同世代绑定。
- `REPORT_ONLY` 只存诊断数据，永远不能关闭 required criterion。

## Out of Scope

- Story 004：gate aggregation。
- SYS-SAVE/SYS-PERSIST Epic：具体 performance benchmark 实现。
- Story 011：最终 bundle traceability。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: nearest-rank performance; threshold validation; bounded flaky repeats; retention cleanup and release evidence preservation.

## Test Evidence

**Story Type**: Logic  
**Required evidence**:
- `tests/unit/sys_test/performance_flaky_retention_test.py` — percentile、threshold、invalid protocol、timeout、repeat 与 retention safety。

**Status**: [x] Created and passing — 1 unit test

## Dependencies

- Depends on: Story 001, Story 002

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; nearest-rank, threshold/report-only, and invalid-sample boundaries covered.
**Deviations**: Long-run retention cleanup and real flaky history require CI/release artifacts.
**Test Evidence**: `tests/unit/sys_test/performance_flaky_retention_test.py`
**Code Review**: Complete — APPROVED; unapproved performance thresholds cannot produce PASS.
- Unlocks: Story 004, Story 008, Story 011
