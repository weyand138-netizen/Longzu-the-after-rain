# UX Spec：游戏菜单 / 快捷控制

> **Status**：Approved
> **Author**：Andwey + Codex
> **Last Updated**：2026-08-09
> **Journey Phase(s)**：稳定叙事间隙、暂停阅读
> **Requirements**：SYS-CHOICE、SYS-NARRATIVE、SYS-JOURNAL、SYS-SAVE、SYS-ACCESS
> **Platform Target**：Windows 10/11 x86-64；鼠标 + 完整键盘；部分 Ren'Py 默认手柄映射不作为独立验收路径；无触控
> **Template**：UX Spec
> **Accessibility tier**：`P0-ACCESS-KEYBOARD-MOUSE-SAPI-EQUIVALENCE`（见 `design/accessibility-requirements.md`）
> **Related**：main-menu、journal、save-load、settings、narrative-choice

## Purpose & Player Need

游戏菜单只在 `PlayableStable` 打开，为玩家提供不改变叙事语义的安全控制：继续、保存、读取、愿望手册、设置、回到标题。它不能在 choice commit、reaction、LoadedUnvalidated 或 BlockingSafeFlow 中作为旁路。

```text
叙事稳定帧 → 游戏菜单 → 继续 / 保存 / 读取 / 愿望手册 / 设置 / 回到标题
```

## Player Context on Arrival

玩家刚完成一段可暂停的稳定叙事内容，可能需要继续阅读、保存进度或调整阅读设置。菜单不得假设玩家愿意离开当前章节，也不得展示隐藏因果或路线信息。

## Navigation Position

`PlayableStable 叙事帧 → 游戏菜单`。这是上下文相关的暂停层，只能从安全稳定帧进入；它不是主菜单的替代根节点。

## Entry & Exit Points

| Entry Source | Trigger | Player Context |
|---|---|---|
| PlayableStable 叙事帧 | 菜单快捷键/按钮 | 当前控制位置、章节和安全保存位置 |
| 叙事恢复完成 | after-reaction checkpoint 建立后 | 当前场景仍为稳定可交互帧 |

| Exit Destination | Trigger | Notes |
|---|---|---|
| 当前叙事帧 | 继续阅读或 Escape/右键 | 恢复 opener semantic ID；不推进叙事 |
| Save Browser | 保存 | 仅 PlayableStable；成功后留在 browser 或明确返回 |
| Load Browser | 读取 | 失败留在 browser；成功先进入 LoadedUnvalidated |
| Journal / Settings | 对应按钮 | 关闭后恢复 caller focus |
| Main Menu | 回到标题并确认 | 不绕过未保存进度确认合同 |

## Layout Specification

```text
┌──────────────────────────┐
│ 游戏菜单                 │
│                          │
│ [继续阅读]               │
│ [保存]                   │
│ [读取]                   │
│ [愿望手册]               │
│ [设置]                   │
│ [回到标题]               │
│                          │
│ [Esc] 返回               │
└──────────────────────────┘
```

主操作区使用深蓝平面；不显示轴、选择历史、评分、结局预测或“最佳路线”。主菜单与游戏菜单的 Journal 使用不同 caller focus/fallback，但进入同一 Journal flow。

### Component Inventory

| Zone | Component | Interactive | Pattern | Data Owner |
|---|---|---:|---|---|
| 菜单列表 | 继续阅读、保存、读取、愿望手册、设置、回到标题 | 是 | Semantic Button | SYS-SAVE / SYS-ACCESS / SYS-JOURNAL / narrative controller |
| 固定操作区 | 返回 | 是 | Fixed Action Rail | 当前 screen navigation contract |
| 状态区 | Applying/Loading 文案 | 否 | Static Announcement | 发起操作的 owner system |

## States & Variants

| State | Visible actions | Initial focus |
|---|---|---|
| Stable | 继续、保存、读取、手册、设置、回标题 | 继续阅读 |
| CriticalInteraction | 菜单不可见/不可聚焦 | 无 |
| Applying/Loading | 仅状态文案 | 无 |
| ExitConfirm | 取消、回到标题 | 取消 |
| Empty/No available actions | action gate 暂无可用操作 | 仅显示安全状态文案；无伪按钮 |
| Error/Recovery | 保存、读取或 persistence 操作失败 | 转对应安全流程；不返回 critical caller |

鼠标点击、Enter、Space调用同一 action；Escape/右键执行一次返回并不传播。打开 Settings/Journal 后关闭，恢复到调用方 semantic ID，不按坐标猜测。

键盘 Tab/Shift+Tab 顺序为：继续阅读 → 保存 → 读取 → 愿望手册 → 设置 → 回到标题；方向键遵循同一阅读顺序。disabled/hidden action 不进入 focus graph；hover 不提供唯一信息。

## Interaction Map

| Action | Input | Feedback | Outcome |
|---|---|---|---|
| 继续阅读 | Enter/Space/鼠标 | pressed | 关闭菜单并恢复 caller |
| 保存/读取/手册/设置 | Enter/Space/鼠标 | focus + pressed | 进入对应规范页面 |
| 回到标题 | Enter/Space/鼠标 | modal | 进入退出确认；确认后回主菜单 |
| 返回 | Escape/右键 | 无传播 | 返回叙事 stable frame |

## Events Fired

| Player Action | Event / State Change | Payload / Notes |
|---|---|---|
| 继续阅读 | `game_menu_closed` | 恢复 caller；不触发新的叙事推进 |
| 保存 | `save_browser_opened` | 由 SYS-SAVE 接管；UI 不写 persistent |
| 读取 | `load_browser_opened` | 由 SYS-SAVE 接管；不可在 critical 状态派发 |
| 愿望手册 | `journal_open_requested` | caller=`game_menu_journal` |
| 设置 | `settings_open_requested` | 由 SYS-ACCESS 接管 |
| 回到标题 | `return_to_main_menu_requested` | 先进入确认；确认后的状态变化由 SYS-SAVE/engine 处理 |
| Escape/右键 | no event | 只执行一次 screen-local 返回 |

## Transitions & Animations

- Enter：稳定叙事帧上直接显示菜单；默认可使用短淡入，但 `reduced_motion` 直接显示最终菜单。
- Exit：继续阅读、返回或进入子页面时直接恢复目标 stable frame；不得等待动画完成才能操作。
- Applying/Loading：固定区域显示静态状态文案并 gate 全部输入；成功/失败后一次性替换状态，不使用 toast 作为唯一证据。
- ExitConfirm：modal 立即 trap focus；取消返回菜单并恢复 opener，确认进入目标页面。

## Data Requirements

| Displayed Data | Source System | Read / Write | Null / Failure Handling |
|---|---|---|---|
| 可用 action 列表 | SYS-SAVE/SYS-ACCESS/action gate | Read | gate 不可用时隐藏、禁用并移出 focus graph |
| 当前 caller semantic ID | screen navigation controller | Read | 缺失时使用批准 fallback，不按坐标恢复 |
| Applying/Loading 状态 | 对应操作 owner | Read | 无状态数据时显示中性静态文案 |
| 当前叙事上下文 | SYS-NARRATIVE/SYS-STATE | Read | 不在菜单中复制或展示隐藏状态 |

## Localization Considerations

- 菜单项与状态文案按至少 40% 文本扩展预留；“回到标题”不得因扩展而隐藏。
- 状态文案不得显示内部 state enum、route ID 或错误码；长说明允许换行。

## Performance

- 从 `PlayableStable` 到首个可交互菜单帧目标为 p95 ≤ 250 ms；目标硬件和测量方式待 Ren'Py engine evidence 冻结。

## Accessibility Requirements

Tab顺序等于菜单顺序；self-voicing读标题→说明→操作。高对比必须保留面板边界与 focus；reduced-motion直接显示最终菜单；所有 action 在静音下可理解。

## Acceptance Criteria

- [ ] 仅在 `PlayableStable` 可打开，CriticalInteraction 中 direct/menu/shortcut open count 均为0。
- [ ] 保存、读取、手册、设置分别进入对应规范页面，关闭后恢复 caller focus。
- [ ] 键盘和鼠标均可完成所有操作，Escape/右键不传播至底层叙事。
- [ ] 1280×720、字体1.5下固定返回操作可见且不遮挡菜单。
- [ ] reaction 未完成前无法通过菜单跳过、保存、读取或再次选择。
- [ ] 空 action gate、操作失败和加载中状态均不产生可聚焦的伪按钮，并提供玩家安全文案。

## Open Questions

- Ren'Py 8.5.3 的菜单快捷键、右键行为和 caller focus restoration 仍需逐屏 production evidence；共享焦点与 viewport 合同已由 accessibility spike 验证。
