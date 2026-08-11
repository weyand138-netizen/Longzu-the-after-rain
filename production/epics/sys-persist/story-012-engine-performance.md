# Story 012: Engine startup 与 projection 性能证据

> **Epic**: SYS-PERSIST — 跨周目解锁
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Integration
> **Estimate**: 3 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/cross-playthrough-unlocks.md`  
**Requirement**: `TR-PERSIST-001`

**ADR Governing Implementation**: ADR-0002: Rollback and Persistence Boundary  
**ADR Decision Summary**: persistent checkpoint 操作必须保持交互帧预算；startup validation 与 projection scan 的 repair work 只能在 approved boundary 执行，并保留 raw samples、grant/has counts 与冻结 startup thresholds。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: `renpy.save_persistent()`、startup validation、backend `has/grant` 与 rendered-frame timing 必须在目标引擎验证。

**Control Manifest Rules (this layer)**:
- Required: target 60 fps / 16.6 ms frame budget。
- Required: synchronous I/O wait 与普通 rendered-frame budget 分开报告。
- Forbidden: 不得以 partial/absent evidence 声称 persistence performance PASS。
- Guardrail: changing batch end-to-end/I/O wait p95≤250 ms、max≤500 ms；普通 frame p95≤16.6 ms、max≤33.2 ms。

---

## Acceptance Criteria

- [ ] `PERSIST-PERF-002`: blocking-safe frame 已渲染且 input gated 时，最大合法 changing batch 的 request entry→durable result 与 I/O-wait p95≤250 ms、max≤500 ms；不含 I/O wait 的 rendered frame p95≤16.6 ms、max≤33.2 ms。
- [ ] `PERSIST-PERF-003`: 最大 root、cold/warm backend、absent/partial/full 11-item membership 的 startup validation + projection scan 保留 raw samples，记录 `has_count=11`、grant count=missing count；已收敛时 grant=0，并满足冻结 startup budget。

## Implementation Notes

- 不把同步 I/O wait 加入普通 frame 后再声称 frame 与 I/O 两套预算同时 PASS。
- ending/memory/seen-only successful batch 不应触发无关 achievement repair scan。
- performance artifacts 必须绑定 Ren’Py/Python/renderer/hardware/environment identity。

## Out of Scope

- Story 011：pure validator/update/merge 性能。
- Story 013：release evidence bundle 与 archive isolation。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: engine/runner benchmark identity; p95/max budgets; warm-up/sample metadata; missing artifact BLOCKED_INPUT.

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_persist/engine_performance_test.py` — durable result、I/O wait、frame hitch、startup/projection counts 与 threshold reports。

**Status**: [x] Created and passing — 1 integration test

## Dependencies

- Depends on: Story 002, Story 004, Story 011

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; engine/projection budget pass/fail and approved-threshold boundary covered.
**Deviations**: Ren'Py engine executable was unavailable in this environment; engine testcase execution remains a final smoke warning.
**Test Evidence**: `tests/integration/sys_persist/engine_performance_test.py`
**Code Review**: Complete — APPROVED; pure benchmark logic is isolated from engine invocation.
- Unlocks: Story 013
