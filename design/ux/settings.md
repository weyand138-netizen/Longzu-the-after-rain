# UX Spec：设置与无障碍

> **Status**：Approved
> **Author**：Andwey + Codex
> **Last Updated**：2026-08-09
> **Journey Phase(s)**：首次配置、阅读中调整、安全恢复
> **Requirements**：SYS-ACCESS、SYS-PERSIST、Art Bible
> **Platform Target**：Windows 10/11 x86-64；鼠标 + 完整键盘；部分 Ren'Py 默认手柄映射不作为独立验收路径；无触控
> **Template**：UX Spec
> **Accessibility tier**：`P0-ACCESS-KEYBOARD-MOUSE-SAPI-EQUIVALENCE`（见 `design/accessibility-requirements.md`）

## Purpose & Player Need

设置让玩家控制字体、对比度、动效、闪烁、屏幕震动，以及 Ren'Py 引擎的阅读/音频偏好。五项项目设置在 Apply 时批量持久化；阅读与音频偏好即时生效，不混入项目设置草稿。

## Player Context on Arrival

玩家可能在首次启动时配置阅读环境，也可能在叙事稳定帧中暂停调整。玩家需要知道哪些修改立即生效、哪些必须应用保存，并能在保存失败或冲突时安全恢复，而不丢失未确认的意图。

## Navigation Position

`Main Menu / PlayableStable Game Menu → Settings`。设置页不可从 `CriticalInteraction`、`LoadedUnvalidated` 或 `BlockingSafeFlow` 作为旁路打开；输出型 self-voicing 仍可按上游合同使用。

## Entry & Exit Points

| Entry Source | Trigger | Player Context |
|---|---|---|
| Main Menu | 设置 | 无运行中叙事 caller |
| PlayableStable Game Menu | 设置 | 需要返回当前稳定叙事帧 |
| Recovery Handoff | persistence/settings failure | 普通草稿与 caller focus 已销毁 |

| Exit Destination | Trigger | Notes |
|---|---|---|
| Caller | 返回/取消无 dirty | 恢复 opener semantic ID |
| ExitConfirm | 返回/Escape/right-click 有 dirty | 默认焦点为返回设置，不静默丢弃 |
| SYS-PERSIST Recovery | commit unknown/recovery | 不返回普通 Settings |

## Layout Specification

```text
┌──────────────────────────────────────┐
│ 设置                                 │
│ 显示设置需应用；阅读与音频立即生效。  │
│                                      │
│ 显示与效果                           │
│ 字体大小       [100%][125%][150%]    │
│ 高对比度       [开/关]               │
│ 减弱动态效果   [开/关]               │
│ 允许闪烁效果   [开/关]               │
│ 允许屏幕震动   [开/关]               │
│                                      │
│ 阅读与音频                           │
│ 自发声、文字速度、自动/跳过、音量     │
│                                      │
│ [取消显示更改] [应用] [返回]          │
└──────────────────────────────────────┘
```

1280×720、字体1.5使用单列和两个独立 viewport；固定操作区保持可见。初始焦点 `settings_font_scale`。

### Component Inventory

| Zone | Component | Interactive | Pattern | Data Owner |
|---|---|---:|---|---|
| 显示与效果 | 字体、高对比、减弱动效、闪烁、震动 | 是 | Semantic Button / Toggle / Radio Group | SYS-ACCESS project settings |
| 阅读与音频 | self-voicing、文字/自动/跳过速度、音量 | 是 | Slider / Toggle | Ren'Py engine preferences |
| 状态区 | dirty/applying/error/conflict 文案 | 否 | Static Announcement | SYS-ACCESS / SYS-PERSIST |
| 固定操作区 | 取消显示更改、应用、返回 | 是 | Fixed Action Rail | Settings screen contract |

## States & Variants

| State | Visible behavior | Focus |
|---|---|---|
| OpenClean | 项目 Apply/取消 disabled、不可聚焦；引擎偏好可调 | font scale |
| PreviewDirty | 立即预览；返回/Escape进入 ExitConfirm | 当前控件 |
| Applying/Loading | 静态“正在保存显示设置……”；全部输入 gate | 无 |
| SaveFailed | “显示设置未能保存，已恢复到上次保存的状态。” | 重试 |
| StaleConflict | “设置已在其他位置改变，请重新载入后继续。” | 重新载入 |
| RecoveryHandoff | 清除草稿并交给 SYS-PERSIST recovery | 上游首个安全动作 |
| Empty/Defaults | 无合法设置 snapshot | 使用临时安全 profile；显示安全状态文案，不显示 schema |
| ExitConfirm | dirty 状态返回/Escape/右键 | 返回设置、应用、放弃显示更改；取消默认焦点 |
| SettingsUnavailable | 设置 root 不可用 | 仅关闭；不显示 schema/字段/result enum |
| Engine preference persistence failure | 引擎偏好无法持久化 | 显示安全提示；不回滚或改写五项项目设置 |

## Interaction Map

| Action | Input | Feedback | Outcome |
|---|---|---|---|
| 修改项目设置 | Left/Right/Up/Down/Enter/Space/鼠标 | 当前值变化、即时预览 | 进入 PreviewDirty，不写 persistent |
| 修改引擎偏好 | 键盘/鼠标 | 新值与效果说明 | Ren'Py preference 即时生效 |
| 应用 | Enter/Space/鼠标 | Applying → 成功/失败状态 | 一次 canonical batch |
| 取消显示更改 | Enter/Space/鼠标 | 恢复 snapshot | 不 assignment/flush |
| 返回/Escape/右键 | 键盘/鼠标 | clean 关闭或 dirty 进入确认 | caller restore 或 recovery |

控件顺序固定为五项项目设置→引擎偏好→取消/应用/返回。Apply最多发送一次 canonical batch；Cancel恢复最新合法 snapshot，不写 assignment/flush。

## Events Fired

| Player Action | Event / State Change | Payload / Notes |
|---|---|---|
| 修改项目设置 | `settings_preview_changed` | screen-local draft；不写 persistent |
| 修改引擎偏好 | Ren'Py preference action | 即时生效；不进入 project settings batch |
| 应用 | `settings_batch_requested` | 五项项目设置一次性提交；不含 engine preferences |
| 取消 | `settings_draft_cancelled` 或 no event | 恢复最新合法 snapshot；assignment/flush count=0 |
| 重载最新设置 | `settings_reload_requested` | 清除冲突草稿后重建焦点 |
| Recovery Handoff | `settings_recovery_requested` | 由 SYS-PERSIST 接管，不返回旧 caller |

## Transitions & Animations

- Enter：直接显示当前 canonical settings；焦点为 `settings_font_scale`。
- PreviewDirty：字体/对比度立即重排；其他效果只影响后续表现，不播放演示动画。
- Applying：静态状态文案替换操作区并 gate 输入；成功/失败一次性替换。
- ExitConfirm：modal 立即 trap focus；取消回到同一控件，应用保留退出意图。
- `reduced_motion`、闪烁和震动开关只删除对应效果；不得改变信息或语义结果。

## Data Requirements

| Displayed Data | Source System | Read / Write | Null / Failure Handling |
|---|---|---|---|
| 五项项目设置 | SYS-ACCESS/SYS-PERSIST canonical root | Read / batch Write | 缺失或 invalid 使用临时安全 profile，不显示 schema |
| 引擎阅读/音频偏好 | Ren'Py preferences | Read / immediate Write | 持久化失败显示安全提示，不回写五项项目设置 |
| dirty/base fingerprint | SYS-ACCESS draft controller | Ephemeral | stale conflict 禁用 Apply，要求 Reload latest 或 Cancel |
| 应用/失败状态 | SYS-PERSIST result contract | Read | 只显示玩家安全 message identity |

## Performance

- 打开 Settings 首个可交互帧 p95 ≤ 250 ms；Apply 正常完成目标 ≤ 500 ms；最终测试硬件和 Ren'Py engine evidence 待冻结。

## Accessibility Requirements

- 标签→当前值→效果说明→生效方式均可 self-voicing；朗读不激活控件。
- high contrast、reduced motion、静音组合均可完成设置；focus以轮廓+位置/填充表示。
- 标签与说明允许40%扩展；字段不得用省略号丢失“应用后保存/立即生效”语义。
- 引擎滑杆步长和最终文案尚未由引擎 spike 封板，必须避免把临时范围写死到内容层。
- 使用项目唯一冻结层级 `P0-ACCESS-KEYBOARD-MOUSE-SAPI-EQUIVALENCE`；五项项目设置的 preview/apply/cancel、焦点与状态规则以 requirements 文件为准。

## Localization Considerations

设置标签、当前值、效果说明、应用/取消/冲突/恢复文案按至少 40% 文本扩展预留；“应用后保存”和“立即生效”不得被省略号替代。

## Acceptance Criteria

- [ ] 五项项目设置按冻结顺序可通过键盘/鼠标操作，且全部值可 self-voicing。
- [ ] 字体、对比度预览即时重排；Apply以一次 batch 持久化，Cancel不写 persistent。
- [ ] dirty 状态按返回/Escape进入确认，不静默丢弃或自动应用。
- [ ] 1280×720、字体1.5下两个 viewport和固定操作区均不重叠、不裁切。
- [ ] SaveFailed/StaleConflict/RecoveryHandoff只显示玩家安全文案，不泄露 schema/字段/result enum。
- [ ] reduced-motion/关闭闪烁/关闭震动分别只移除对应表现，不改变信息或语义结果。
- [ ] `ExitConfirm`、`SaveFailed`、`StaleConflict`、`SettingsUnavailable` 与 `RecoveryHandoff` 均提供明确的玩家安全出口。

## Open Questions

- self-voicing 的 SAPI 能力与人工听测仍属于独立 evidence gate；本 UX spec 不把 capability enumeration 写成听测 PASS。
- 引擎偏好的控件步长、最终中文文案和 Simplified Chinese SAPI transcript 需要 Ren'Py 8.5.3 spike。
