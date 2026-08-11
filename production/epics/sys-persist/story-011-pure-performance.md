# Story 011: Pure persistence 性能协议

> **Epic**: SYS-PERSIST — 跨周目解锁
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Logic
> **Estimate**: 3 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/cross-playthrough-unlocks.md`  
**Requirement**: `TR-PERSIST-001`

**ADR Governing Implementation**: ADR-0002: Rollback and Persistence Boundary  
**ADR Decision Summary**: persistent writes 在 coarse checkpoint 执行，不能每行对话或每帧写入；性能 artifact 必须有版本化 protocol、完整 raw samples、nearest-rank 与冻结环境/预算。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: pure validator/batch/merge 预算可在 Python 3.12 验证；engine startup/I/O 预算由 Story 012 单独验证。

**Control Manifest Rules (this layer)**:
- Required: raw samples、hardware/environment identity 与 nearest-rank percentile。
- Forbidden: NaN、±∞、negative、missing/extra keys 或样本不足不得替代 PASS。
- Guardrail: validation/update/merge 每类 p95≤2 ms、max≤5 ms，allocation 不超过冻结预算。

---

## Acceptance Criteria

- [ ] `PERSIST-PERF-001`: 最大双侧/三源 24-member roots、24-request batch、11-item seen、最大 epoch 与最长合法 UTF-8 IDs，validation/update/merge 各 5 次 warm-up + 至少 30 次样本，p95≤2 ms、max≤5 ms，raw samples 全部保留。
- [ ] `PERSIST-PERF-001`: protocol 中 NaN、±∞、negative、missing/extra 或不足样本固定失败，不能生成替代 percentile。

## Implementation Notes

- 使用版本化 benchmark manifest 绑定 root、batch、IDs、runner、environment 与 protocol。
- percentile 使用 nearest-rank；不要插值或只保留汇总值。
- benchmark harness 与 raw artifacts 必须保持 test-only，不得进入 persistent root、正式存档或 release archive。

## Out of Scope

- Story 002：实际 flush/I/O fault behavior。
- Story 012：engine startup/projection performance。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: nearest-rank formula; all-metric PASS rule; invalid samples; REPORT_ONLY without approved thresholds.

## Test Evidence

**Story Type**: Logic  
**Required evidence**:
- `tests/unit/sys_persist/pure_performance_test.py` — protocol validation、nearest-rank、root/batch/merge maximum fixtures 与 threshold checks。

**Status**: [x] Created and passing — 1 unit test

## Dependencies

- Depends on: Story 001, Story 002, Story 005

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; nearest-rank formula, all-metric gate, invalid samples, and REPORT_ONLY covered.
**Deviations**: None.
**Test Evidence**: `tests/unit/sys_persist/pure_performance_test.py`
**Code Review**: Complete — APPROVED; no interpolation or unapproved threshold promotion.
- Unlocks: Story 013
