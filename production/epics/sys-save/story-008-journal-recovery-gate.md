# Story 008: Journal 安全入口与 recovery 抢占

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
**Secondary ADR**: ADR-0005
**ADR Decision Summary**: Journal 入口只在安全主菜单和 `PlayableStable` 游戏菜单可用；critical、loaded-unvalidated、blocking recovery 阶段必须关闭入口。recovery 抢占时销毁旧 caller context，不恢复旧 focus intent。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: Ren’Py screen mounting、focus restore、blocking recovery preemption 与 shortcut/direct-action invocation 需在目标引擎验证。

**Control Manifest Rules (this layer)**:
- Required: Presentation 只能读取 read model，不得拥有 save/persistent controller。
- Required: blocking recovery 抢占时所有旧 caller restore intent 必须被销毁。
- Forbidden: Journal 不得绕过 save action gate 或使 loaded scene 重新可达。
- Guardrail: blocked phase 中 Journal visible/enabled/focusable 必须为 `false/false/false`。

---

## Acceptance Criteria

- [ ] `SAVE-JOURNAL-001`: 安全主菜单与 `PlayableStable` 游戏菜单分别使用固定 semantic IDs，open request 各一次，caller context exact 记录，save/rollback/persistent 深值不变。
- [ ] `SAVE-JOURNAL-002`: caller mounted 时正常关闭按固定 fallback 顺序恢复 focus；mount 前不调用 focus，不能跨 catalog target 或使用 stale displayable。
- [ ] `SAVE-JOURNAL-003`: critical、loaded-unvalidated、blocking safe flow 与 unsupported/corrupt load 中 Journal visible/enabled/focusable 全为 false，open request 与 queue length 为 0。
- [ ] `SAVE-JOURNAL-004`: Journal 打开后进入 blocking recovery 时 controller、caller context 与 restore intent 各清除一次；只显示 blocking surface，新安全主菜单 interaction 不恢复旧 caller。

## Implementation Notes

- 复用 `journal_menu_gate:v1` 与 `journal_caller_focus_catalog:v1`，不要创建第二套 caller policy。
- 只在 caller 已 mounted 后恢复 focus；不得按坐标或旧 displayable 猜测。
- recovery 抢占优先于 Journal close callback 与 bottom action。

## Out of Scope

- SYS-JOURNAL Epic：Journal 内容 bundle/read model。
- Story 007：blocking safe flow 的 root context。
- Story 010：save/load screen 的完整 UI layout。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: dual Journal entry; focus restoration; blocked/recovery visibility; recovery preemption and no loaded-scene return.

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_save/journal_gate_test.py` — dual entry、focus restore、blocked phase 与 recovery preemption。

**Status**: [x] Created and passing — 1 integration test

## Dependencies

- Depends on: Story 006, Story 007

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; dual Journal gate, focus suppression, blocked/recovery preemption covered.
**Deviations**: None.
**Test Evidence**: `tests/integration/sys_save/journal_gate_test.py`
**Code Review**: Complete — APPROVED; Journal cannot resume a loaded scene during recovery.
- Unlocks: None
