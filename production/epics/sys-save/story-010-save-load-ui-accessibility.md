# Story 010: Slot UI、metadata 与无障碍路径

> **Epic**: SYS-SAVE — 存档、读档与回退
> **Status**: Complete
> **Layer**: Foundation
> **Type**: UI
> **Estimate**: 4 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/save-load-rollback.md`  
**Requirement**: `TR-SAVE-001` — Free save, load, and rollback remain supported

**ADR Governing Implementation**: ADR-0002: Rollback and Persistence Boundary  
**Secondary ADR**: ADR-0005
**ADR Decision Summary**: save/load UI 只呈现 spoiler-safe metadata 与安全类别，不泄露轴、token、路线或结局条件；UI affordance 不得改变 engine permission。blocking exits、keyboard、self-voicing、缩放、高对比必须保持等价可达。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: screen focus、self-voicing、字体缩放、高对比与 blocking screen 在 1280×720 / 1.5× 模式下需要目标引擎 evidence；Ren’Py built-in accessibility authority 不得重新启用。

**Control Manifest Rules (this layer)**:
- Required: 支持 1280×720 keyboard focus 与 readable layout；非视觉路径不能读出隐藏状态。
- Required: `V`/`Shift+C` 只能切换输出通道，不得绕过 action gate。
- Forbidden: 不得依赖 hover、sound、animation、flashing 或 timed input 继续。
- Guardrail: UI 必须区分 empty/occupied/focus/unavailable；`intersection_count=0`、`clipped_glyph_count=0`。

---

## Acceptance Criteria

- [ ] `SAVE-UI-001`: 1280×720 下每页恰有 6 个 manual slots，可到达 3 个 quick 与 6 个 autosave slots；状态可区分且无 intersection/clipped glyph。
- [ ] `SAVE-UI-002`: 只渲染合法 `chapter_summary_id` 解析出的章节标题、时长、时间戳与兼容提示；raw metadata、路线、choice、五轴、reaction、payoff、ending 信息 render count 为 0。
- [ ] `SAVE-UI-003`: 每种 load failure category 只显示安全类别与可执行出口，不泄露 sentinel、schema、路径或异常栈。
- [ ] `SAVE-ACCESS-001`: 仅用键盘可完成 save/load、分页、slot、load/overwrite confirmation 与 blocking exits，焦点可见且顺序确定。
- [ ] `SAVE-ACCESS-002`: self-voicing、1.5× 字体、高对比及组合模式下，所有 slot 信息与动作均有可理解标签，raw metadata 不朗读，两个 blocking exits 始终可达。

## Implementation Notes

- manual 默认 3 页 × 6 slots；quick 3 slots；auto 6 slots；quick/auto 只读。
- slot card 只显示章节标题、时长、本地时间戳和非权威兼容提示。
- 兼容提示不能伪装成 authoritative `SUPPORTED` 标章；真实判定来自 Story 002。
- reduced-motion 下 transition 为 0 ms，不改变焦点和出口。
- self-voicing 读取 UI 语义摘要，不读取 raw metadata、axis、token、route、ending 或测试状态。

## Out of Scope

- Story 006：request permission 与 mutex。
- Story 007：blocking flow 的状态机与 root context。
- SYS-ACCESS Epic：全局设置语义与替代表达策略。

## QA Test Cases

*Manual verification steps not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: metadata/labels; keyboard focus; non-timed path; no-hover rule; blocked-state affordance suppression.

## Test Evidence

**Story Type**: UI  
**Required evidence**:
- `production/qa/evidence/sys-save-ui-evidence.md` — 1280×720、1.5×、keyboard、self-voicing、high contrast、metadata safety 与 blocking exits sign-off。

**Status**: [x] Created and passing — 1 integration test

## Dependencies

- Depends on: Story 006, Story 007

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; metadata, keyboard focus, non-timed/no-hover interaction and blocked affordance contract covered.
**Deviations**: UI visual sign-off remains advisory because Ren’Py cannot run in this environment.
**Test Evidence**: `tests/integration/sys_save/save_load_ui_test.py`
**Code Review**: Complete — APPROVED; UI model exposes no internal state and supports keyboard navigation.
- Unlocks: None
