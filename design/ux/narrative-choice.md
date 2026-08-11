# UX Spec：叙事对话与选择

> **Status**：Approved
> **Author**：Andwey + Codex
> **Last Updated**：2026-08-09
> **Journey Phase(s)**：观察→询问/决定→即时反应→延迟回收
> **Requirements**：SYS-CHOICE、SYS-NARRATIVE、SYS-ACCESS、Art Bible
> **Platform Target**：Windows 10/11 x86-64；鼠标 + 完整键盘；部分 Ren'Py 默认手柄映射不作为独立验收路径；无触控
> **Template**：UX Spec
> **Accessibility tier**：`P0-ACCESS-KEYBOARD-MOUSE-SAPI-EQUIVALENCE`（见 `design/accessibility-requirements.md`）

## Purpose & Player Need

玩家要先读懂场景、人物动作和物件，再选择如何对待绘梨衣。choice surface 的工作是呈现可理解、无价值暗示的行动，不告诉玩家哪个“正确”，也不显示五轴/分数/成本/预测。

## Player Context on Arrival

玩家刚阅读完场景正文、人物动作或物件信息，处于观察与决定之间；选择可能来自普通对话推进，也可能来自完成一个 reaction/payoff 后的下一控制点。玩家不应被要求记忆内部状态或预先知道结果。

## Navigation Position

`稳定叙事帧 → 对话/旁白 → Choice Surface → Reaction → after_reaction checkpoint`。Choice Surface 是上下文内决策层，不是独立菜单。

## Entry & Exit Points

| Entry Source | Trigger | Player Context |
|---|---|---|
| 对话/旁白 | approved content 到达 choice 节点 | 当前 prompt、选项文本、canonical 顺序 |
| Rollback/Load | 恢复到 choice 前控制位置 | 重新读取真实选项与焦点，不继承旧确认外观 |

| Exit Destination | Trigger | Notes |
|---|---|---|
| Reaction | 一次 canonical choice commit | Choice 面板先退场；reaction 期间控制转移入口关闭 |
| Stable narrative frame | 无 choice 的对话推进 | 不运行 resolver 或写隐藏状态 |
| Safe recovery | presentation/preflight 无效 | 不显示旧选项，只提供上游批准的安全出口 |

## Layout Specification

```text
┌────────────────────────────────────────────────────────────┐
│                         场景图                              │
│                                                            │
│  [对话/旁白窗口：人物名、当前正文；底部固定]                │
│                                                            │
│                 你要怎么做？                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 1  先捡起那张被雨打湿的纸                             │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │ 2  先带她走到站台尽头，离开监控范围                   │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

1280×720与字体1.5使用单列、左右安全边距≥64 px、选项最小高度64 px；长文案换行不截断。对话窗口不能遮挡当前人物手部、视线或回收物件。

### Component Inventory

| Zone | Component | Interactive | Pattern | Data Owner |
|---|---|---:|---|---|
| 场景区 | 场景图、人物动作、物件 | 否 | Static Announcement | SYS-NARRATIVE / Art Bible |
| 对话区 | 说话者、正文、prompt | 推进时是 | Semantic Button | SYS-NARRATIVE |
| 选择区 | choice rows | 是 | Choice Surface | SYS-CHOICE / SYS-NARRATIVE |
| 辅助区 | 返回/菜单（仅安全稳定帧） | 条件可用 | Fixed Action Rail | SYS-SAVE / navigation gate |

## Interaction Map

| Component | Keyboard/Mouse | Feedback | Outcome |
|---|---|---|---|
| 对话推进 | Enter/Space/鼠标 | 文字完成/推进 | 下一段 approved content |
| choice row | Up/Down/Tab、Enter/Space/鼠标 | focus轮廓→pressed | 一次 canonical choice commit |
| 回退/菜单 | 安全稳定帧才可用 | rail focus | 上游批准的 rollback/game menu |
| self-voicing | 输出快捷键/系统设置 | 读当前内容 | 不确认、不滚动、不改焦点 |

确认流程固定为：`choice interaction → latch → apply_choice → reaction state → reaction presentation → after_reaction checkpoint`。confirmed后重复输入无动作；reaction期间 quick actions/save/load/rollback/skip 均 hidden、disabled、unfocusable。

## Events Fired

| Player Action | Event / State Change | Payload / Notes |
|---|---|---|
| 对话推进 | `dialogue_advanced` 或 no event | 只推进 approved content；无 telemetry 默认 |
| 展示选择 | `choice_presented` | `choice_id` 仅用于本地产品事件/测试；不显示给玩家 |
| 确认选择 | `choice_confirmed` → `apply_choice` | activation latch 保证一次；状态由 SYS-STATE 拥有 |
| 打开菜单/回退 | no event / 上游 action | 只在安全稳定帧可用 |
| self-voicing 输出 | no event | 输出通道不得确认、推进、滚动或改焦点 |

## Transitions & Animations

- Choice enter：approved dialogue 到达 choice 节点时直接挂载 choice surface；不得延迟首焦点或要求动画完成。
- Pressed：仅短暂显示输入已收到；不使用奖励音效或推荐动画。
- Confirmed exit：choice 面板在 reaction-state establishment 前直接退场；`reduced_motion` 为 0 ms。
- Reaction gate：reaction 期间保持静态可读状态；结束后一次性恢复 `after_reaction` checkpoint 的控制。
- Invalid/loading：静态安全文案替换旧选项；不得保留旧选项作为可见或可聚焦 fallback。

## Data Requirements

| Displayed Data | Source System | Read / Write | Null / Failure Handling |
|---|---|---|---|
| prompt 与 choice text | SYS-NARRATIVE approved content | Read | 缺失时进入 blocking safe flow；不得显示 ID |
| choice 顺序与 identity | SYS-CHOICE/SYS-NARRATIVE | Read | 不可解析时不显示旧列表 |
| reaction/payoff summary | SYS-NARRATIVE + SYS-ACCESS catalog | Read | 缺失 summary 时阻止继续并进入安全流程 |
| 当前焦点 | screen-local semantic focus | Read/ephemeral | 恢复失败时聚焦第一项；不写 persistent |

## States & Variants

| State | Behavior |
|---|---|
| Idle | 选项可见，无语义颜色/推荐 |
| Focused | 青色轮廓+填充/形状变化；不改变文字 |
| Pressed | 短暂确认输入收到，不显示“好选择” |
| Confirmed | 选项锁定，面板退出，进入 reaction |
| Disabled | reaction/critical gate 或系统不可交互 | 不进入 focus graph；不得表达“错误答案” |
| Loading/invalid | 不显示旧选项，转安全流程 |
| Empty/No choices | 内容 catalog 返回零项 | 不渲染空 choice 面板，进入 blocking safe flow |
| Timeout | 本 P0 不启用；SYS-TENSION post-MVP |
| Rollback/load before choice | 按恢复状态重新出现，撤销外观不保留 |

## Data / Events

UI只消费 `choice_id`、批准文本、顺序、reaction/payoff presentation identity；状态由 SYS-STATE/SYS-NARRATIVE拥有，UI不得写轴或历史。每次确认发出 `choice_presented`、`choice_confirmed`（仅本地测试/产品事件总线若批准），不引入 telemetry SDK；analytics event 在当前项目默认视为 none。

## Accessibility Requirements

- 键盘焦点顺序与视觉顺序一致；self-voicing读 prompt→数量→所有选项→当前焦点，不能朗读隐藏条件。
- 高对比、静音、reduced-motion下文字/焦点/反应完整可理解；动作、视线、物件变化消费同一 `accessible_causal_summary_id`。
- 禁止 hover-only；禁止用颜色、声音、动画单独表达选择意义。
- 选项按至少 40% 文本扩展预留高度；中文标点、全角数字与换行由文本系统处理。
- 使用项目唯一冻结层级 `P0-ACCESS-KEYBOARD-MOUSE-SAPI-EQUIVALENCE`；对比度、字体、焦点、viewport、读序和状态规则以 requirements 文件为准。

## Localization Considerations

选项、prompt、说话者和 reaction summary 均按至少 40% 文本扩展预留；长选项允许多行并进入 keyboard viewport，不以省略号丢失语义。

## Performance

- Choice surface 首个可交互帧目标 p95 ≤ 250 ms；确认后反应状态不得阻塞输入超过 100 ms。
- 长选项进入 keyboard viewport 时，自动滚入只改变 viewport adjustment，不提交 choice、不触发 reaction，也不改变焦点语义。

## Acceptance Criteria

- [ ] 1280×720、字体1.5下所有批准选项完整可见或进入可键盘滚动 viewport，不截断。
- [ ] 键盘、鼠标、self-voicing输出均可使用同一 canonical choice，输出不触发确认。
- [ ] 确认后重复点击/按键只产生一次 commit，reaction期间所有控制转移入口均不可用。
- [ ] 选项不显示轴、分数、成本、风险、资格或预测后果。
- [ ] 回退/读档到选择前恢复真实选项与焦点；到 reaction 后不重新打开 choice。
- [ ] reduced-motion、静音、高对比下仍可识别即时反应与后续可访问因果摘要。
- [ ] 从 choice 节点到首个可交互 choice surface 的 p95 显示时间不超过 250 ms；目标硬件和测试 fixture 待 Ren'Py evidence 冻结。
- [ ] 无效/缺失 choice catalog 时不显示旧选项，并提供可键盘到达的安全恢复路径。

## Open Questions

- 需要以最终长选项语料冻结最大 choice count 与 exact line height；timed choice 不属于当前 P0。
- 当前规格没有独立空态；若内容 catalog 返回零选项，必须进入上游 blocking safe flow，不得渲染空的可提交面板。
