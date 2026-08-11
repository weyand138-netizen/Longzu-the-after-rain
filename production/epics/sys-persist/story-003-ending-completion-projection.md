# Story 003: Ending completion projection 边界

> **Epic**: SYS-PERSIST — 跨周目解锁
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Integration
> **Estimate**: 3 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/cross-playthrough-unlocks.md`  
**Requirement**: `TR-PERSIST-002` — Ending completion emits one durable completed-event boundary

**ADR Governing Implementation**: ADR-0006: Ending Completion Boundary  
**Secondary ADR**: ADR-0002
**ADR Decision Summary**: SYS-ENDING 是 `commit_ending_completion` 唯一 owner；completion event 经过单一 persistence coordinator 转换为 ending request。entry、resolver、UI、Journal 与 SYS-PERSIST adapter 都不能提前发放 ending membership。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: terminal completion node、rollback-owned event 与 persistent flush 的调用次数需在 Ren’Py 8.5.3 中验证。

**Control Manifest Rules (this layer)**:
- Required: completion event 包含 owner、ending、completed event、checkpoint、epoch、generation 与 stable boundary。
- Required: completion 前 request/assignment/flush 为 0，成功结果为 `APPLIED_FLUSHED`。
- Forbidden: 不得在 `commit_ending_entry`、resolver 或 UI callback 中投影 ending。
- Guardrail: 已存在 ending membership 返回 `DUPLICATE_NOOP`，不重复 notification。

---

## Acceptance Criteria

- [ ] `PERSIST-UPD-001`: ending request 只有在唯一 terminal completion node、`commit_ending_completion` 完成后才出现；entry path request/assignment/flush count 为 0。
- [ ] `PERSIST-UPD-007`: caller 不能注入 owner ID；CFG 证明 completion dominates request callsite，before-completion 与 ending-entry path 的 request/assignment/flush/popup counts 为 0。
- [ ] `PERSIST-PROJ-005`: ending completion replay、load、rollback、blocking exit 与 new game 不产生 achievement popup 或 unlock audio，且 persistent membership 按 owner 合同保持。

## Implementation Notes

- SYS-PERSIST 只验证 event owner、generation、epoch、checkpoint 和 completed-event reference，不重新运行 resolver 或读取 live ending state。
- `completed_event_id` 必须为 `ending_completed:{ending_id}`；completion event 不是第 13 个 persistent leaf。
- ending entry 只代表 rollback-owned `Active → Ended`，不能视为 durable completion。

## Out of Scope

- SYS-ENDING Epic：六个 terminal completion node 与 callsite 实现。
- Story 002：通用 batch/flush/fault handling。
- Story 006：per-run save/load/rollback invariance。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: exact ending completion event; one writer/flush; no resolver rerun; duplicate no-op; no fifth-axis proxy.

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_persist/ending_completion_projection_test.py` — owner/callsite、pre/post completion side effects、duplicate replay 与 event shape。

**Status**: [x] Created and passing — 1 integration test

## Dependencies

- Depends on: Story 002

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; exact completion event, one writer/flush, resolver isolation, and duplicate no-op covered.
**Deviations**: None.
**Test Evidence**: `tests/integration/sys_persist/ending_completion_projection_test.py`
**Code Review**: Complete — APPROVED; durable boundary is separate from per-run restore.
- Unlocks: Story 006
