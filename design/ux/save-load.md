# UX Spec：存档、读档与阻断恢复

> **Status**：Approved
> **Author**：Andwey + Codex
> **Last Updated**：2026-08-09
> **Journey Phase(s)**：安全暂停、重返、失败恢复
> **Requirements**：SYS-SAVE、SYS-STATE、SYS-ENDING、SYS-ACCESS
> **Platform Target**：Windows 10/11 x86-64；鼠标 + 完整键盘；部分 Ren'Py 默认手柄映射不作为独立验收路径；无触控
> **Template**：UX Spec
> **Accessibility tier**：`P0-ACCESS-KEYBOARD-MOUSE-SAPI-EQUIVALENCE`（见 `design/accessibility-requirements.md`）

## Purpose & Player Need

Save Browser 只在 `PlayableStable` 游戏菜单可用；Load Browser 可从主菜单或安全游戏菜单进入。界面帮助玩家识别存档并选择安全恢复位置，不透露路线、选择、五轴、结局或隐藏进度。

## Player Context on Arrival

Save Browser 的玩家刚完成一段稳定叙事并希望保留当前进度；Load Browser 的玩家希望从已存在的槽位恢复。失败或不兼容时，玩家应能继续选择其他槽位或安全返回，而不会看到半加载场景。

## Navigation Position

`Main Menu / PlayableStable Game Menu → Save/Load Browser → Confirmation → LoadedUnvalidated → Stable Scene 或 Blocking Restore Error`。Save 只允许从 `PlayableStable` 进入；Load 可从两个安全入口进入。

### Surface Behavior

| Surface | Entry | Player Action | Safe Exit |
|---|---|---|---|
| Save Browser | PlayableStable game menu | 仅 manual slots 可写；占用槽位先覆盖确认 | caller 或 browser |
| Load Browser | Main Menu / PlayableStable game menu | 三类占用槽位可请求加载；先 detached preflight | caller 或 blocking restore |
| Blocking Restore Error | LoadedUnvalidated validation failure | 只返回主菜单或明确开始新游戏 | 不返回 loaded scene |

## Entry & Exit Points

| Entry Source | Trigger | Player Context |
|---|---|---|
| Main Menu | Load | 无当前 run；slot metadata 仅作提示 |
| PlayableStable Game Menu | Save/Load | 当前 run 仍安全；Save 写入前需覆盖确认 |
| LoadedUnvalidated | 引擎安装存档后 | 不显示 loaded scene；只等待验证结果 |

| Exit Destination | Trigger | Notes |
|---|---|---|
| 安全 caller | Escape/右键/返回 | 恢复 caller semantic focus |
| Stable Scene | 支持的 Load 验证完成 | 只显示首个稳定帧 |
| Blocking Restore Error | 验证失败 | 仅返回主菜单或明确开始新游戏 |

## Layout Specification

```text
┌────────────────────────────────────────────────────────────┐
│ 保存 / 读取                                                 │
│ [手动存档] [快速存档] [自动存档]                             │
│ ┌──────┐ ┌──────┐ ┌──────┐                                  │
│ │ Slot │ │ Slot │ │ Slot │  ← 当前分区 slots，阅读顺序       │
│ └──────┘ └──────┘ └──────┘                                  │
│ ┌──────┐ ┌──────┐ ┌──────┐                                  │
│ │ Slot │ │ Slot │ │ Slot │                                  │
│ └──────┘ └──────┘ └──────┘                                  │
│ [上一页]     第 1 / 3     [下一页]       [返回]              │
└────────────────────────────────────────────────────────────┘
```

手动分区每页6 slots、默认3页；quick 3 slots、auto 6 slots。Slot card只显示章节标题、累计时长、本地时间和非权威兼容性提示；空 slot 不可加载。

### Component Inventory

| Zone | Component | Interactive | Pattern | Data Owner |
|---|---|---:|---|---|
| 分区区 | 手动/快速/自动分区 | 是 | Semantic Button | SYS-SAVE |
| 槽位区 | slot card | Save/Load 条件可用 | List / Grid Card | SYS-SAVE detached metadata |
| 分页区 | 上一页/下一页/当前页 | 是 | Fixed Action Rail | screen-local pagination |
| Modal | 覆盖/加载确认 | 是 | Safe Confirmation Modal | SYS-SAVE action gate |
| 阻断面 | 安全说明与两个出口 | 是 | Blocking Safe Flow | SYS-SAVE / recovery owner |

## States & Variants

| State | Behavior |
|---|---|
| Empty | 空槽显示“空存档”，不可执行 load |
| Overwrite Confirmation | 摘要→取消→确认覆盖；取消默认焦点 |
| Load Confirmation | 摘要→取消→确认加载；说明会放弃未保存进度，取消默认焦点 |
| Unsupported/Unreadable | 留在 browser，焦点回失败 slot，可换槽或返回 |
| LoadedUnvalidated | 不显示 loaded scene；转内部验证 |
| Blocking Restore Error | 标题→安全说明→返回主菜单→明确开始新游戏；首焦点返回主菜单 |
| Loading/Preflight | 读取 detached metadata 或验证中 | 静态状态文案；旧 caller 不可被加载场景替换 |

## Interaction Map

| Action | Input | Outcome |
|---|---|---|
| 选择分区 | 键盘/鼠标 | 切换分区，焦点落首个可用 slot |
| 选择 slot | 键盘/鼠标 | Save 写入/Load 进入确认；无 hover 前置 |
| 翻页 | 键盘/鼠标 | 非循环分页，焦点落新页首 slot |
| 确认覆盖/加载 | Enter/Space/鼠标 | latch一次；成功保存留在 browser，成功 load 进入验证 |
| Escape/右键 | 任意普通层 | 返回上一层一次；modal中取消 |

## Data Requirements

UI只消费 detached slot metadata 与 compatibility classification；不显示 raw metadata。load 成功安装后必须进入 `LoadedUnvalidated`，只有 `SUPPORTED` 才显示首个稳定帧。任何 unsupported/corrupt 状态只允许安全出口，不能回到当前叙事 caller。

| Displayed Data | Source System | Read / Write | Update / Null Handling |
|---|---|---|---|
| 分区与页码 | SYS-SAVE slot catalog / screen-local pagination | Read | 分区切换和翻页后更新焦点；页码缺失时隐藏分页而不循环 |
| 章节标题/时长/时间戳 | SYS-SAVE detached slot metadata + approved catalogs | Read | 缺失或篡改显示中性未知提示，不阻止真实 validation |
| 兼容性状态 | SYS-SAVE compatibility classification | Read | unknown/unsupported/unreadable 显示安全文案，不显示 raw enum |
| Save/Load action availability | SYS-SAVE request permission + UI affordance | Read | 不可用 action 隐藏、disabled、unfocusable，不排队 |
| LoadedUnvalidated result | SYS-SAVE validation contract | Read | 未通过前不显示 loaded scene；失败转 blocking surface |

## Events Fired

| Player Action | Event / State Change | Payload / Notes |
|---|---|---|
| 打开 Save/Load Browser | `save_browser_opened` / `load_browser_opened` | caller semantic ID；无 telemetry |
| 选择槽位 | `slot_selected` 或 no event | 只携带 detached slot identity，不显示 raw metadata |
| 确认覆盖 | `save_requested` | SYS-SAVE 执行一次写入；UI 不拥有保存状态 |
| 确认加载 | `load_requested` | 进入 `LoadedUnvalidated`；不得先显示 loaded scene |
| 失败/阻断 | `restore_blocked` | 玩家文案使用安全 message identity，不显示错误码 |
| Escape/取消 | no event | 只执行一次返回/取消 |

## Transitions & Animations

- Browser enter：从 caller 直接挂载首帧；焦点必须在页面稳定后立即可用。
- Confirmation：立即 modal trap focus；取消恢复原槽位焦点，确认 latch 后禁用重复输入。
- LoadedUnvalidated：隐藏场景并显示内部 gated 状态；验证完成后一次性切换到 stable frame。
- Blocking Restore Error：直接进入安全阻断面；`reduced_motion` 下不等待淡入、截图缩放或转场。

## Performance

- 普通 Save 完成目标 ≤ 500 ms；Load Browser 首帧与 slot metadata 展示 p95 ≤ 500 ms；目标硬件、slot fixture 和测量方式待 SYS-SAVE/engine evidence 冻结。

## Accessibility Requirements

- Tab顺序：标题→分区→当前分区 slots→分页→返回；slot card所有字段可朗读。
- 1280×720、字体1.5下卡片内允许纵向重排；操作区固定可见；self-voicing不读内部错误码。
- 高对比使用卡片轮廓+状态文字；reduced-motion无截图缩放/转场依赖。
- 章节标题、时间和本地化日期必须允许更长字符串；禁止把 route/choice ID 当作 fallback 文案。
- 使用项目唯一冻结层级 `P0-ACCESS-KEYBOARD-MOUSE-SAPI-EQUIVALENCE`；存档、读档、阻断恢复的键盘、状态与 transcript 规则以 requirements 文件为准。

## Localization Considerations

章节标题、兼容性状态、时长、时间戳和确认/阻断文案按至少 40% 文本扩展预留；未知 metadata 不使用 route/choice ID 作为 fallback。

## Acceptance Criteria

- [ ] Save 只在 PlayableStable 可用，Load 可从主菜单/安全游戏菜单打开。
- [ ] 1280×720、字体1.5下6个手动 slot、分页和返回均可见且键盘可达。
- [ ] 覆盖与加载确认默认焦点均为取消，Escape/右键不执行破坏性 action。
- [ ] 失败 slot 不破坏当前安全上下文，并把焦点恢复到该 slot。
- [ ] 成功 load 在验证完成前不显示 loaded scene；阻断恢复只提供两个批准安全出口。
- [ ] slot card 不显示选择、路线、五轴、token、reaction/payoff、结局或隐藏进度。
- [ ] 空手动/快速/自动分区、Unreadable/Unsupported slot、LoadedUnvalidated 与 Blocking Restore Error 均有明确玩家安全文案。

## Open Questions

- 最终兼容性提示文案在 SAVE-Q3 关闭前保持 provisional；需要引擎运行证据确认 FileAction/validation 边界。
