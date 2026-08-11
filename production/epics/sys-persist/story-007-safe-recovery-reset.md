# Story 007: Safe recovery 与 collection reset

> **Epic**: SYS-PERSIST — 跨周目解锁
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Integration
> **Estimate**: 4 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/cross-playthrough-unlocks.md`  
**Requirement**: `TR-PERSIST-001`

**ADR Governing Implementation**: ADR-0002: Rollback and Persistence Boundary  
**ADR Decision Summary**: invalid persistent root、merge marker、flush uncertainty 和 reset partial state 必须进入可识别 safe recovery；collection reset 只在二次明确确认后清除 product collections、递增 epoch、保留 settings，并能在中断后安全重试。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: persistent recovery、reset multi-phase transaction、restart/retry 与 screen gating 需在 Ren’Py 8.5.3 验证。

**Control Manifest Rules (this layer)**:
- Required: recovery active 时 unlock/setting writes 返回 `PERSISTENCE_UNAVAILABLE`。
- Required: reset 只在所有 phase PASS 后可用，保留 settings 并递增 epoch。
- Forbidden: recovery 不得进入 normal collection UI，不得宣称单侧清除成功。
- Guardrail: destructive reset 默认焦点为 Cancel，第一次取消/Escape/right-click 不调用 reset。

---

## Acceptance Criteria

- [ ] `PERSIST-REC-002`: safe recovery active 时 unlock/setting request 返回 `PERSISTENCE_UNAVAILABLE`，assignment/flush/projection/popup/pending/backfill counts 为 0。
- [ ] `PERSIST-REC-003`: main menu、quit 与 persistence-unavailable new game 路径可达且不进入 collection screens；新游戏前显示无收藏写入警告且可取消。
- [ ] `PERSIST-REC-004`: reset engine fixtures 或 exception/hard-kill matrix 未全 PASS 时 reset action visible/enabled/focusable 均为 false。
- [ ] `PERSIST-REC-005`: 只有第二层明确确认调用 reset 一次；第一层取消、Escape、right-click 等路径 reset count 为 0，default focus 为 Cancel。
- [ ] `PERSIST-REC-006`: reset 成功时 epoch 恰增 1，三类 memberships、seen 与 backend progress 清除，settings 深值保留，旧 epoch save 不能复活旧 membership。
- [ ] `PERSIST-REC-007`: reset 各 boundary exception/hard-kill 后进入可识别 ResetRecovery，只允许 retry same reset/main menu/quit，最终双侧收敛+settings preserved 才是 success。

## Implementation Notes

- 将 `PERSISTENCE_SAFE_RECOVERY`、`RESET_RECOVERY` 与 `COMMIT_STATUS_UNKNOWN` 作为不同可观察状态。
- recovery 中不得运行 resolver、per-run state read/write 或 collection projection。
- reset transaction 必须明确 `Idle → Confirmed → ClearingProduct → ClearingBackend → RestartPending → Verified`。

## Out of Scope

- Story 005：startup marker/merge marker 的产生。
- Story 008：Settings draft screen。
- Story 010：recovery screen 的完整 layout/accessibility evidence。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: safe/reset/unknown state distinction; write freeze; projection/feedback suppression; cleanup preservation.

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_persist/safe_recovery_reset_test.py` — recovery states、reset confirmation、phase failure、retry、restart 与 no-write assertions。

**Status**: [x] Created and passing — 2 integration tests

## Dependencies

- Depends on: Story 001, Story 005

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; safe/reset/unknown states, write freeze, and feedback suppression covered.
**Deviations**: None.
**Test Evidence**: `tests/integration/sys_persist/recovery_reset_test.py`
**Code Review**: Complete — APPROVED; COMMIT_STATUS_UNKNOWN cannot be conflated with safe recovery.
- Unlocks: Story 008, Story 010
