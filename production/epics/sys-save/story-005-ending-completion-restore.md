# Story 005: Ending completion 存档边界

> **Epic**: SYS-SAVE — 存档、读档与回退
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Integration
> **Estimate**: 3 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/save-load-rollback.md`  
**Requirements**: `SAVE-RESTORE-011` — Ending completion save/load; `SAVE-RESTORE-012` — Rollback across ending completion

**ADR Governing Implementation**: ADR-0006: Ending Completion Boundary  
**Secondary ADRs**: ADR-0002, ADR-0005
**ADR Decision Summary**: SYS-ENDING 是 completion callsite 的唯一 owner；completion event 是 rollback-owned transient input。SYS-SAVE 必须在 completion node 前后恢复 event、control location 与 lifecycle，同时保持已 flush 的 persistent membership 不变。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: ending label terminal completion node、save/rollback 与 persistent flush 的交叉行为必须在目标引擎上验证；ADR-0006 没有独立 Engine Compatibility 小节，使用 Ren’Py 8.5.3 项目基线。

**Control Manifest Rules (this layer)**:
- Required: completion event 只由 SYS-ENDING 产生，save/rollback 恢复该 rollback-owned event。
- Required: completion 前 ending request、root replacement 与 flush count 为 0。
- Forbidden: rollback 不得移除已经成功 flush 的 persistent membership。
- Guardrail: 同一 completion replay 返回 `DUPLICATE_NOOP` 且不产生第二次 notification。

---

## Acceptance Criteria

- [ ] `SAVE-RESTORE-011`: completion node 前的合法存档恢复为缺少 `ending_completion_event_record` 且 ending request count 为 0；completion node 后的存档恢复 event、`completed_event_id=ending_completed:{ending_id}` 与 control location，persistent membership 不变，resolver 不重复调用。
- [ ] `SAVE-RESTORE-012`: completion 成功落盘后 rollback 到 terminal completion node 前，只恢复 rollback-owned completion/control state；12-leaf persistent snapshot、ending membership、epoch 与 writer/flush counts 深值不变；再次前进返回 `DUPLICATE_NOOP` 且 notification count 为 0。
- [ ] `SAVE-RESTORE-013`: completion node 后合法存档恢复的 `ending_completion_event_record` 必须包含 ADR-0006 规定的 8 个字段，且每个字段值与保存时一致；其中 `stable_completion_boundary=True`、`owner_system=SYS-ENDING`，并且该 record 不得写入 persistent root。

## Implementation Notes

- 不在 SYS-SAVE 中实现 `commit_ending_completion`；只恢复与校验其产生的 rollback-owned record。
- 使用 ADR-0006 的完整字段集合：ending ID、completed event ID、checkpoint ID、occurrence ID、collection epoch、catalog generation、stable boundary 和 owner system。
- 不能把 ending completion event 变成 persistent root 的第 13 个 leaf。

## Out of Scope

- Story 004：普通四 checkpoint restore semantics。
- SYS-PERSIST Epic：ending completion event 到 persistent request 的 projection。
- SYS-ENDING Epic：completion callsite 与 terminal node 的实现。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_save/ending_completion_restore_test.py` — pre/post completion save、rollback、duplicate replay 与 persistent invariance。

**Status**: [x] Created — 5 Python test functions and 1 Ren'Py testcase

## Dependencies

- Depends on: Story 004
- Unlocks: None

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing
**Deviations**: Advisory only: the story records 5 Python test functions but the test file contains 7; SAVE-RESTORE-011/012/013 are not separate entries in `docs/architecture/tr-registry.yaml`.
**Test Evidence**: Integration test at `tests/integration/sys_save/ending_completion_restore_test.py`; 50/50 SYS-SAVE integration tests, 10/10 Ren'Py testcases, 42/42 assertions, and lint/compile passed.
**Code Review**: Skipped - Solo mode
