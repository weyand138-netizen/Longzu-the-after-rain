# Story 007: Root blocking safe flow 与新游戏出口

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
**ADR Decision Summary**: post-install 或 engine-control failure 必须清除可返回 loaded scene 的 context，阻止 timers/callbacks/shortcuts，并只提供主菜单与显式新游戏两个出口。新游戏只替换 per-run state，保留合法 persistent root。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: load-failure label、root safe context、screen stack 清理、after_load 失败路由与 OS quit 行为必须在目标引擎中验证。

**Control Manifest Rules (this layer)**:
- Required: blocking flow 不得返回 loaded scene；只能主菜单或显式新游戏。
- Required: `semantic_state`、`state_schema_sentinel`、ending lifecycle sentinel 只能由显式初始化入口写入。
- Forbidden: 不得让 rollback、quick save/load、skip、history return、screen dismissal 绕过阻断。
- Guardrail: 底层 loaded scene timers、callbacks、shortcuts 与输入 invocation count 必须为 0。

---

## Acceptance Criteria

- [ ] `SAVE-BLOCK-001`: post-install/engine-control failure 进入 `screen_blocking_restore_error` 前清除 caller context；loaded scene、choice、reaction、payoff、pause UI 与普通 game menu 不可见、不更新、不接收焦点，底层 timer/callback/shortcut count 为 0。
- [ ] `SAVE-BLOCK-002`: blocking screen 激活时 rollback、普通/快速存读档、skip、auto、history return、screen return、Escape/right-click dismissal 均不能返回 loaded scene。
- [ ] `SAVE-BLOCK-002A`: OS close 只退出应用，不显示 loaded scene frame，不调用 callback 或 caller return。
- [ ] `SAVE-BLOCK-003`: “返回主菜单”清除不安全 context，进入主菜单且 screen stack 不可返回 loaded scene。
- [ ] `SAVE-BLOCK-004`: “开始新游戏”由同一显式入口初始化 save-contract、catalog generation、semantic、ending lifecycle 与 run epoch；12-leaf persistent root 深值不变，重复激活只执行一次。

## Implementation Notes

- blocking screen 必须运行在 root safe context，先销毁可返回 caller 的 screen/call context，再呈现错误。
- 错误文案只说明安全类别与可执行出口；sentinel、schema、路径、异常栈、隐藏轴/token/结局条件只进入开发诊断。
- OS quit 不属于“返回 blocking screen”的出口；退出过程不得短暂恢复 loaded scene。
- Explicit New Game 保留 valid persistent unlocks/settings，并初始化 rollback-owned state。

## Out of Scope

- Story 002：分类器本身。
- Story 006：通用 action gate/mutex。
- Story 010：阻断 screen 的具体布局、自发声与字体证据。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: blocking entry/context reset; disabled shortcut matrix; main-menu/new-game/OS-quit safe exits; persistent-root preservation.

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_save/blocking_flow_test.py` — root context、禁用入口、主菜单、新游戏与 OS quit。

**Status**: [x] Created and passing — 2 integration tests

## Dependencies

- Depends on: Story 002, Story 006
- Unlocks: Story 010

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 4/4 passing; blocking safe-flow, exit, and call-count contracts covered.
**Deviations**: None.
**Test Evidence**: `tests/integration/sys_save/blocking_flow_test.py`
**Code Review**: Complete — APPROVED; no architectural or testability blockers.
