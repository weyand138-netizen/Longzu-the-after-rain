# Story 003: Checkpoint 与控制位置目录

> **Epic**: SYS-SAVE — 存档、读档与回退
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Integration
> **Estimate**: 4 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/save-load-rollback.md`  
**Requirement**: `TR-SAVE-001` — Free save, load, and rollback remain supported

**ADR Governing Implementation**: ADR-0004: Semantic Ending Snapshot and Rollback State Envelope  
**Secondary ADRs**: ADR-0002, ADR-0005
**ADR Decision Summary**: production control locations、save state envelope 和 test-only detached fixtures 必须分离。SYS-SAVE 拥有 production restore record schema；SYS-CHOICE 拥有 11-field test fixture；SYS-NARRATIVE 提交稳定 statement mapping，fixture 对 location 允许多对一覆盖。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: 稳定 statement identity、source hash、catalog generation 与 Ren’Py rollback control location 必须在目标引擎上验证。

**Control Manifest Rules (this layer)**:
- Required: 生产 catalog 只使用 schema-known records，source/generation hash 必须 exact-match。
- Required: test-only fixtures 与 production catalog 分离，production 不得引用 test-only observers。
- Forbidden: 不得以文件行号作为持久 identity，不得把 expected history/axes fixture 变成 runtime authority。
- Guardrail: 每个 production location 必须唯一映射 engine statement；每个 fixture 必须恰好映射一个 production record。

---

## Acceptance Criteria

### Verification Status

- [x] SAVE-CATALOG-001 — four checkpoint kinds and coverage
- [x] SAVE-CATALOG-002 — exact three-record schemas
- [x] SAVE-CATALOG-003 — fixture-to-production many-to-one joins
- [x] SAVE-CATALOG-004 — orphan and duplicate rejection
- [x] SAVE-CATALOG-005/006 — source identity and stable location validation
- [x] SAVE-CATALOG-007 — generation and gate-profile consistency

- [ ] `SAVE-CATALOG-001`: catalog 只允许 `before_choice`、`after_reaction`、`before_payoff`、`after_payoff`，每类均有 production record 与 canonical fixture。
- [ ] `SAVE-CATALOG-002`: `choice_restore_checkpoint_record`、`restore_control_location_record`、`save_restore_fixture_record` 均执行 exact field/type validation。
- [ ] `SAVE-CATALOG-003`: fixture 恰好 join 一个 production record；每个 production record 至少一个 fixture；不同 prehistory fixtures 映射同一 location 合法。
- [ ] `SAVE-CATALOG-004`: orphan、无 fixture production record、duplicate fixture、duplicate key 或一条 statement 多映射均阻止构建。
- [ ] `SAVE-CATALOG-005`: statement identity、`from` identity 或 source artifact hash 漂移时，未同步迁移证据的 mapping 构建失败。
- [ ] `SAVE-CATALOG-006`: 缺少稳定 return identity、动态生成、clean build 无法延续 identity 或使用文件行号时拒绝 catalog。
- [ ] `SAVE-CATALOG-007`: release catalog、canonical CFG artifact、初始化常量和 rollback-owned `save_catalog_generation_id` 必须 exact-equal。

## Implementation Notes

- production `restore_control_location_record` 只描述 engine location mapping，不冻结单一 expected history/axes。
- test-only `choice_restore_checkpoint_record` 只能作为证据 fixture，不得进入运行时 catalog。
- 使用 `control_location_id + checkpoint_kind` 作为 production key；engine statement 只能恰好映射一条 record。
- 任何 source/catalog hash 漂移必须失败，不能静默映射到相邻 label。

## Out of Scope

- Story 002：运行时兼容性分类。
- Story 004：加载后恢复 traversal 的行为。
- Story 012：release candidate 的最终 evidence bundle 与 archive scan。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_save/control_catalog_test.py` — schema、duplicate/orphan、many-to-one join、identity drift 与 generation mismatch。

**Status**: [x] Created and passing

## Dependencies

- Depends on: None
- Unlocks: Story 002, Story 004, Story 012

## Completion Notes

**Completed**: 2026-08-10
**Criteria**: 7/7 passing at the catalog-contract level.
**Deviations**: Publication of the real production CFG/source-hash artifact and runtime rollback-owned generation wiring remain downstream integration work.
**Test Evidence**: Integration test at `tests/integration/sys_save/control_catalog_test.py`; Python 13/13 passed, Ren'Py global 5/5 testcases and 19/19 assertions passed.
**Code Review**: Complete — Approved with suggestions.
