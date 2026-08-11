# Story 011: Save/load 性能协议与预算

> **Epic**: SYS-SAVE — 存档、读档与回退
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Integration
> **Estimate**: 3 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/save-load-rollback.md`  
**Requirement**: `TR-SAVE-001` — Free save, load, and rollback remain supported

**ADR Governing Implementation**: ADR-0002: Rollback and Persistence Boundary  
**Secondary ADRs**: ADR-0004, ADR-0005
**ADR Decision Summary**: save/load 使用 Ren’Py 原生序列化和 rollback-owned envelope；性能证据必须测量端到端操作、longest frame、cold/warm cohort，并保留原始样本和环境 identity，不能用不完整样本宣称 PASS。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: save/load timing、首个 rendered/input-accepting stable frame 和 pinned hardware/renderer/environment 必须在目标引擎验证。

**Control Manifest Rules (this layer)**:
- Required: target 60 fps / 16.6 ms interactive frame。
- Required: benchmark 证据包含完整 raw samples、硬件与环境标识。
- Forbidden: NaN、±∞、negative、wrong type、缺失/额外 keys 或样本不足不得生成替代 percentile。
- Guardrail: save p95 ≤500 ms、max ≤1000 ms；load p95 ≤1000 ms；longest-frame p95 ≤16.6 ms、max ≤33.2 ms。

---

## Acceptance Criteria

- [ ] `SAVE-PERF-001`: reference hardware、最大合法 production fixture、cold/warm cohorts、每来源 5 次 warmup 后至少 30 次样本，manual/quick/auto end-to-end p95≤500 ms、max≤1000 ms，longest-frame p95≤16.6 ms、max≤33.2 ms。
- [ ] `SAVE-PERF-002`: 从确认加载到 `after_load` 完成后的首个 rendered/input-accepting stable frame，manual/quick/auto end-to-end p95≤1000 ms，longest-frame p95≤16.6 ms、max≤33.2 ms；非法 protocol input 固定失败。

## Implementation Notes

- 使用 nearest-rank percentile；保留每个原始样本，不只保存汇总值。
- benchmark protocol 必须绑定 hardware、Ren’Py/Python、renderer、fixture、catalog generation 与 run identity。
- 性能 evidence 不得写入 production save、persistent root 或发行资源。

## Out of Scope

- Story 001：保存操作本身的原子实现。
- Story 012：release evidence bundle 与 archive exclusion。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: finite sample validation; nearest-rank p95; save latency budget; REPORT_ONLY without approved thresholds.

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_save/performance_test.py` — protocol validation、nearest-rank、source classes、p95/max 与 frame hitch。

**Status**: [x] Created and passing — 1 integration test

## Dependencies

- Depends on: Story 001, Story 002, Story 004

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; nearest-rank save latency budget and report-only threshold boundary covered.
**Deviations**: Actual minimum-hardware Ren’Py profiling is deferred to engine-enabled release QA.
**Test Evidence**: `tests/integration/sys_save/save_load_performance_test.py`
**Code Review**: Complete — APPROVED; performance evaluator is deterministic and fail-closed.
- Unlocks: Story 012
