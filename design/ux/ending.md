# UX Spec：结局与因果回顾

> **Status**：Approved
> **Author**：Andwey + Codex
> **Last Updated**：2026-08-09
> **Journey Phase(s)**：七日终点、理解代价、尾声入口
> **Requirements**：SYS-ENDING、SYS-STATE、SYS-JOURNAL、SYS-ACCESS
> **Platform Target**：Windows 10/11 x86-64；鼠标 + 完整键盘；部分 Ren'Py 默认手柄映射不作为独立验收路径；无触控
> **Template**：UX Spec
> **Accessibility tier**：`P0-ACCESS-KEYBOARD-MOUSE-SAPI-EQUIVALENCE`（见 `design/accessibility-requirements.md`）

## Purpose & Player Need

结局页让玩家知道发生了什么，以及 1–3 个具体行动/物件/后果如何构成当前答案。它不进行评分、不解释隐藏算法、不告诉玩家差多少分、不泄露未到达结局要求。

## Player Context on Arrival

玩家刚完成 terminal ending narration 和玩家可见 closure，情绪可能是释然、困惑或失落；结局回顾的目标是理解已发生的具体事实，而不是比较路线或寻找隐藏分数。

## Navigation Position

`Terminal completion node → Ending narration → Ending title → Cause Cards → Ending narration/尾声 → Journal unlock`。Cause Card flow 不是独立评分页面。

## Entry & Exit Points

| Entry Source | Trigger | Player Context |
|---|---|---|
| SYS-ENDING terminal node | resolver 返回合法 `display_cause_ids` | 已建立 ending outcome；cause IDs 已按 resolver 原序批准 |
| Journal Detail | 已完成结局后打开静态详情 | 读取 immutable journal catalog，不重跑 resolver |
| Invalid resolver | mapping/preflight 失败 | 不进入普通结局 UI；由 blocking safe flow 接管 |

| Exit Destination | Trigger | Notes |
|---|---|---|
| Ending narration/尾声 | 最后一张卡后继续 | `commit_ending_completion` 在完整玩家可见 closure 后由 terminal node 调用一次 |
| Journal | 后续从菜单进入 | 只消费静态 approved summary |
| Safe recovery | invalid result | 不显示半成品原因卡 |

## Layout Specification

```text
┌────────────────────────────────────────────────────────────┐
│                       雨停之后                             │
│                     [结局标题]                             │
│                                                            │
│  “你曾经做到的事”                                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 具体原因卡 1：记住的行动/物件/后果                     │  │
│  └──────────────────────────────────────────────────────┘  │
│  [继续]                                                     │
└────────────────────────────────────────────────────────────┘
```

Resolver提供 `display_cause_ids` 的原序，UI只通过 approved summary catalog解析，逐卡按正常叙事控制推进。一个原因就只显示一张；不得补空卡或重排。

### Component Inventory

| Zone | Component | Interactive | Pattern | Data Owner |
|---|---|---:|---|---|
| 标题区 | ending title | 否 | Static Announcement | SYS-ENDING catalog |
| 内容区 | 1–3 cause cards | 推进时是 | Causal Card | SYS-ENDING approved summary catalog |
| 正文区 | ending narration/backlog text | 是 | Keyboard Viewport | SYS-NARRATIVE |
| 操作区 | 继续/普通叙事控制 | 是 | Semantic Button / Fixed Action Rail | SYS-NARRATIVE control flow |

## States & Variants

| State | Behavior |
|---|---|
| Title | 非交互 heading；不得成为默认焦点 |
| Cause Card | 文本+语义标题；正常推进；不显示内部cause kind |
| Final Card | 继续到正常 ending narration/尾声 |
| Invalid resolver result | 不打开该 UI，转安全/开发阻断流程 |
| Journal Detail | 只显示静态批准摘要，不声称是本次 traversal 的完整个性化原因 |
| Loading | ending catalog 或 localized summary 尚未验证 | 不显示半成品卡片，等待验证或进入安全流程 |
| Empty/No causes | 合法结果没有可展示 cause | 不补空卡；按 SYS-ENDING contract 阻断 presentation |

## Interaction Map

| Action | Input | Feedback | Outcome |
|---|---|---|---|
| 推进结局正文 | Enter/Space/鼠标 | pressed/文本推进 | 下一段 approved narration |
| 推进原因卡 | Enter/Space/鼠标 | focus + pressed | 下一张卡或 ending narration |
| 阅读正文 | Tab/Shift+Tab/PageUp/PageDown/鼠标 | viewport 自动滚入焦点 | 不改变 resolver 或 history 语义 |
| self-voicing | output-only shortcut/设置 | 朗读当前安全内容 | 不推进、不确认、不滚动 |

## Events Fired

| Player Action | Event / State Change | Payload / Notes |
|---|---|---|
| Cause card presented | `ending_cause_presented` | 仅消费 approved summary identity；不写 persistent |
| Ending narration complete | `ending_narration_completed` | 到达 terminal completion boundary |
| Ending completion | `commit_ending_completion` | 仅 terminal completion node 调用一次；SYS-PERSIST 消费 ending ID |
| Journal detail opened | `journal_ending_detail_opened` 或 no event | 不读取本次 traversal cause IDs |
| Invalid result | `ending_presentation_blocked` | 玩家文案安全；不打开普通 ending UI |

## Transitions & Animations

- Title/cause enter：按正常叙事顺序直接挂载；默认转场不得成为继续操作的前置条件。
- Cause advance：卡片逐张替换；`reduced_motion` 使用 0 ms 文本替换。
- Final card：直接回到正常 ending narration/尾声；不插入评分或解锁 toast。
- Invalid result：直接进入 blocking safe flow，不显示空卡、错误卡或半加载卡。

## Data Requirements

| Displayed Data | Source System | Read / Write | Null / Failure Handling |
|---|---|---|---|
| ending title | SYS-ENDING approved catalog | Read | 缺失时阻断 presentation，不显示 ID |
| `display_cause_ids` 数量/顺序 | SYS-ENDING resolver output | Read | UI 不过滤、不补卡、不重排 |
| cause summary 文案 | frozen localized summary catalog | Read | summary 缺失或不安全时阻断 |
| ending narration | SYS-NARRATIVE | Read | 不以 UI fallback 代替内容 |
| normal history/backlog text | Ren'Py history/backlog + presented text | Read | 只记录实际展示文本；不暴露 hidden record fields |
| completion event | SYS-ENDING terminal node → SYS-PERSIST | Write by owner | UI 不调用 completion API |

## Performance

- Ending title 与首张 cause card 首个可交互帧 p95 ≤ 500 ms；cause card 切换不得阻塞输入超过 100 ms，最终阈值待最大内容 fixture 与 Ren'Py evidence 冻结。

## Accessibility Requirements

- 键盘、鼠标、静音均可继续；self-voicing读标题→语义标题→原因正文→继续。
- 卡片文字必须引用具体行动、事件、物件或未解决后果；不得出现轴、threshold、token、qualification、cause ID、百分比、排名、未来路线条件。
- 字体放大允许纵向重排；reduced-motion使用0 ms文本替换，不能用另一种淡入代替。
- 原因文案按至少40%扩展预留；长文本在正文 viewport内滚动，继续操作保持固定可见。
- 使用项目唯一冻结层级 `P0-ACCESS-KEYBOARD-MOUSE-SAPI-EQUIVALENCE`；原因卡、静音、reduced-motion 和读序规则以 requirements 文件为准。

## Localization Considerations

结局标题、语义标题、原因卡和尾声文案按至少 40% 文本扩展预留；长文案只在正文 viewport 内滚动，不能用内部 ID 或“未命中其他结局”作为 fallback。

## Acceptance Criteria

- [ ] 当前 ending 标题、当前原因卡和继续操作在1280×720、字体1.5下不重叠、不截断。
- [ ] 1/2/3张卡严格匹配 resolver 提供的数量、顺序与 identity。
- [ ] 键盘、鼠标、静音、reduced-motion均可推进，不需要 hover、声音或 timed input。
- [ ] 原因卡不显示轴、数值、条件、缺口、排名、未来路线要求或内部 ID。
- [ ] `unsent_postcard` 首卡引用具体失败/未解决事实，而不是“未命中其他结局”。
- [ ] Journal 中的静态结局摘要不重新运行 resolver、不读取本次 traversal cause IDs。
- [ ] `commit_ending_completion` 只在最后一段 ending narration 与玩家可见 closure 完成后调用一次，UI 不提前提交。

## Open Questions

- 需要 content-lock 后冻结六结局的 summary catalog 与每卡中文长度；当前只冻结结构与信息边界。
