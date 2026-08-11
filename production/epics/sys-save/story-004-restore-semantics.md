# Story 004: 四类恢复点语义与回退

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

**ADR Governing Implementation**: ADR-0002: Rollback and Persistence Boundary  
**Secondary ADR**: ADR-0004: Semantic Ending Snapshot and Rollback State Envelope
**ADR Decision Summary**: rollback 恢复一个完整的 rollback-owned envelope；checkpoint kind 决定 choice、reaction、payoff 是否已经发生。恢复后必须开启新的 observation window，不得用独立 dedupe ledger 改变语义。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: 必须在 Ren’Py 8.5.3 中验证 save/load/rollback 控制位置、rollback-transformed collections、reaction/payoff call counts 与 loaded-save rollback boundary。

**Control Manifest Rules (this layer)**:
- Required: schema、五轴和 ordered history 作为一个 rollback/save envelope 恢复。
- Required: 所有 semantic state 更新继续通过完整 candidate 的一次 replacement assignment。
- Forbidden: 不得创建 reaction/payoff dedupe ledger，不得让 imported Python 持有 live rollback state。
- Guardrail: rollback 到耗尽时动作不可见、不可用、不可聚焦且不改变状态。

---

## Acceptance Criteria

- [ ] `SAVE-RESTORE-001`: 从 `before_choice` 恢复后，choice/reaction 在当前 observation window 各发生一次。
- [ ] `SAVE-RESTORE-002`: 从 `after_reaction` 恢复后，history/axes 与快照相等，目标 commit/reaction 不重复。
- [ ] `SAVE-RESTORE-003`: 从 `before_payoff` 恢复后，目标 payoff 在当前 horizon 恰好发生一次，commit/reaction 不重复。
- [ ] `SAVE-RESTORE-004`: 从 `after_payoff` 恢复后，目标 payoff 不重复，history/axes 不被修改。
- [ ] `SAVE-RESTORE-005`: manual、quick、auto 三种来源在四类 checkpoint 的 12 个 canonical saves 均保持相同恢复语义。
- [ ] `SAVE-RESTORE-006`: 同一 `before_payoff` 存档在独立运行中反复加载，每次 traversal 均产生一次目标 payoff。
- [ ] `SAVE-RESTORE-007`: ending entry 后的存档恢复 `Ended` 与 pending ending ID，resolver 不重复调用。
- [ ] `SAVE-RESTORE-008`: rollback 穿过 ending entry 时 lifecycle、pending 值和 semantic state 恢复到对应 `Active` 快照，并再次得到相同结局。
- [ ] `SAVE-RESTORE-009`: loaded-save rollback 只恢复该 save 的 rollback-owned 状态，不恢复 load 前另一局状态。
- [ ] `SAVE-RESTORE-010`: rollback history 耗尽时 action 为 `false/false/false`，invocation count 为 0，状态不变。

## Implementation Notes

- `before_choice`、`after_reaction`、`before_payoff`、`after_payoff` 必须以 control location 与 lifecycle 状态共同决定行为。
- 不能把 fixture 中的 expected history/axes 变成 runtime reject rule；它们只用于 test evidence。
- `after_load` 临时诊断和 action gates 不得进入 store/rollback log。
- 回退到较早 checkpoint 后重新前进应是新的 observation window，而不是被 persistent 或隐藏 ledger 去重。

## Out of Scope

- Story 005：ending completion event 的前后存档与回退。
- Story 006：操作请求 gate 与 mutex。
- Story 009：persistent root 深值不变性证明。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_save/restore_semantics_test.py` — 四 checkpoint、三来源、重复 payoff、ending entry、loaded-save rollback 与 exhausted rollback。

**Status**: [x] Created and verified

## Dependencies

- Depends on: Story 002, Story 003
- Unlocks: Story 005, Story 009

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 10/10 passing
**Deviations**: Advisory: QA Test Cases remain undefined because Solo mode skipped the QA coverage gate; the original Test Evidence status is stale. No GDD or ADR deviation found.
**Test Evidence**: Integration test at `tests/integration/sys_save/restore_semantics_test.py`; Python 16/16 passed, Ren'Py global 9/9 testcases and 34/34 assertions passed, lint/compile passed.
**Code Review**: Skipped — Solo mode.
