# Story 002: 读档预检与兼容性分类

> **Epic**: SYS-SAVE — 存档、读档与回退
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Integration
> **Estimate**: 4 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/save-load-rollback.md`  
**Requirement**: `TR-SAVE-002` — Legacy, unsupported, and corrupt loads enter a blocking safe flow

**ADR Governing Implementation**: ADR-0005: Counterevidence Ledger and Detectable State Initialization  
**Secondary ADRs**: ADR-0002, ADR-0004
**ADR Decision Summary**: 用 `None` sentinel 使 legacy state 可检测；`after_load` 必须先按固定优先级分类，再决定是否继续。缺失、未知、损坏或不一致状态不得被修复或猜测，失败必须进入 blocking safe flow。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: 必须验证 missing-variable defaults、detached save-data inspection、`after_load` 路由、rollback coherence 和 exact validation precedence。

**Control Manifest Rules (this layer)**:
- Required: 先验证 sentinel，再验证 schema-known slots；严格遵守固定分类优先级。
- Required: legacy、unsupported、corrupt loads 只能进入主菜单或明确新游戏出口。
- Forbidden: 不得恢复到 loaded scene，不得静默修复 invalid state。
- Guardrail: 未支持结果的分类必须在 loaded scene 显示前完成。

---

## Acceptance Criteria

- [x] `SAVE-LOAD-000`: 空 UI slot 返回 `EMPTY_SLOT_NOOP`，detached inspection、native load 与 classifier 调用数均为 0，焦点保持在该 slot。
- [x] `SAVE-LOAD-001`: 已占用但不可读取的容器在 state installation 前返回 `UNREADABLE_SAVE`，不进入 loaded scene。
- [x] `SAVE-LOAD-002`: 任一 required sentinel/generation 为 `None` 时返回 `LEGACY_INCOMPATIBLE`，不继续 semantic、ending 或 location 验证。
- [x] `SAVE-LOAD-003`: semantic sentinel 为未知精确值时返回 `UNSUPPORTED_VERSION`，不运行 semantic validator。
- [x] `SAVE-LOAD-004` / `004A`: ending、save-contract 或 catalog generation 未知或 wrong exact type 时返回 `UNSUPPORTED_VERSION`，semantic、ending 与 location validators 不被调用。
- [x] `SAVE-LOAD-005` / `006`: semantic envelope 或 ending lifecycle 非法时返回 `CORRUPT_STATE`。
- [x] `SAVE-LOAD-007`: current statement 无 production location 映射时返回 `UNSUPPORTED_CONTROL_LOCATION`。
- [x] `SAVE-LOAD-007A`: 多重映射、catalog 非法或 source hash 不匹配时返回 `INTERNAL_LOAD_VALIDATION_FAILURE`。
- [x] `SAVE-LOAD-008`: location 可映射但 checkpoint kind 与 restored state 不相容时返回 `CORRUPT_STATE`，且不读取单一 test fixture snapshot。
- [x] `SAVE-LOAD-009`: 所有 required checks 通过时唯一结果为 `SUPPORTED`，之后才允许显示 loaded scene。
- [x] `SAVE-LOAD-010`: 参数化 cross-product 严格遵守 GDD 规定的分类优先级，缺失 manifest、空 dimension 或 case count 不符均失败。

## Implementation Notes

- `default semantic_state = None`、`default state_schema_sentinel = None`；不得用默认值伪造 active state。
- 执行固定顺序：输入 shape → missing sentinel → exact type/version → current catalog/source → semantic/ending validity → location count → checkpoint coherence。
- 预检不得改变当前 run 或 persistent；仅当预检未阻断且玩家确认后才调用 native load。
- 不对 unknown/custom object 求真、迭代、表示、比较或哈希。
- 不支持迁移旧开发存档；不存在 migration ADR 时直接分类为 incompatible。

## Out of Scope

- Story 003：production control-location catalog 的构建与 fixture join。
- Story 007：分类失败后的 blocking screen 与出口。
- Story 004：成功加载后的 checkpoint restore semantics。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_save/load_classification_test.py` — empty/unreadable、sentinel、version、state、location、precedence 与 no-install assertions。

**Status**: [x] Created

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 11/11 passing
**Deviations**: None. Story 004 post-load restore semantics and Story 007 blocking safe-flow UI remain explicitly downstream.
**Test Evidence**: Integration test at `tests/integration/sys_save/load_classification_test.py` (14 tests passed); Ren’Py global suite 6/6 testcases and 21/21 assertions passed; lint/compile passed.
**Code Review**: Complete; falsey-validator and complexity findings were fixed and revalidated.

## Dependencies

- Depends on: Story 003
- Unlocks: Story 004, Story 007
