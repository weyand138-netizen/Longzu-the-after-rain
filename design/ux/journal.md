# UX Spec：愿望手册

> **Status**：Approved
> **Author**：Andwey + Codex
> **Last Updated**：2026-08-09
> **Journey Phase(s)**：回顾、理解回收、跨周目重返
> **Requirements**：SYS-JOURNAL、SYS-PERSIST、SYS-ACHIEVE、SYS-ACCESS、SYS-SAVE
> **Platform Target**：Windows 10/11 x86-64；鼠标 + 完整键盘；部分 Ren'Py 默认手柄映射不作为独立验收路径；无触控
> **Template**：UX Spec
> **Accessibility tier**：`P0-ACCESS-KEYBOARD-MOUSE-SAPI-EQUIVALENCE`（见 `design/accessibility-requirements.md`）

## Purpose & Player Need

愿望手册让玩家重新阅读已发生的章节事实、回忆片段、旅途记录与已完成结局。它是只读/受控确认的玩家安全 read model，不是完成率面板，不运行 resolver，不显示五轴、条件或未解锁路线。

`主菜单/游戏菜单 → Validating → Contents → Category List → Item Detail`。新 open cycle 始终从 Contents 开始；关闭后恢复 caller semantic focus。

## Player Context on Arrival

玩家通常在一段叙事结束后、重新启动游戏时，或跨周目返回时打开手册，目标是回顾已经发生的事实，而不是寻找攻略或计算完成率。手册必须把已验证内容与暂不可用内容分开，避免玩家误以为数据丢失。

## Navigation Position

手册位于主菜单或 `PlayableStable` 游戏菜单之下；普通入口受 `journal_menu_gate:v1` 约束。层级为 `Entry → Validating → Contents → Category List → Item Detail`。

## Entry & Exit Points

| Entry Source | Trigger | Player Context |
|---|---|---|
| Main Menu | `main_menu_journal` | 无 per-run caller；恢复失败使用 `main_menu_start` |
| Game Menu | `game_menu_journal` | 携带 `PlayableStable` caller；关闭后恢复 `game_menu_return` |
| Persistence/Content Recovery | 上游 gate 抢占 | 普通手册被销毁，不保留旧焦点或滚动缓存 |

| Exit Destination | Trigger | Notes |
|---|---|---|
| 上一层列表/目录 | Escape、右键或固定 action | 每层只执行一次，恢复 semantic ID 与 session scroll position |
| Caller | 关闭 | 仅 caller 仍 mounted 时恢复；否则使用批准 fallback |
| Recovery surface | bundle/root/commit 故障 | 不返回普通 Journal caller |

## Layout Specification

```text
Contents                         Category List
┌──────────────────────┐         ┌──────────────────────────┐
│ 愿望手册             │         │ 章节                     │
│ 章节                 │         │ [Day 1 标题]             │
│ 回忆                 │         │ [Day 2 标题]             │
│ 旅途记录             │         │ ...                      │
│ 结局                 │         │                          │
│                      │         │ [返回目录] [关闭]         │
│                      │         └──────────────────────────┘
│ [关闭]               │
└──────────────────────┘
```

列表/详情正文进入独立 Keyboard Viewport；固定 action rail 在 viewport 外。四入口同尺寸/层级/对比/装饰预算；不显示空槽、百分比、分母或 locked hints。

### Information Hierarchy

页面标题与安全说明优先于分类；分类优先于条目列表；条目标题/状态优先于详情正文；返回与关闭始终在 viewport 外可见。

## Component Inventory

| Zone | Component | Interactive | Pattern |
|---|---|---:|---|
| Contents | 四个 category rows | 是 | Semantic Button |
| List | 已解锁条目 rows | 是 | Semantic Button + Viewport |
| List | 返回目录/关闭 | 是 | Fixed Action Rail |
| Detail | 正文 viewport | 否但可滚动 | Keyboard Viewport |
| Detail | 返回列表/关闭 | 是 | Fixed Action Rail |
| Pending | “正在整理手册……” | 否 | Static Announcement |

### Category Content Mapping

| Category | List Content | Detail Content | Empty / Fault Behavior |
|---|---|---|---|
| 章节 | 已完成 Day 1–7 标题与短摘要 | 玩家安全章节概览 | 合法空页；单区故障进入 CategoryUnavailable |
| 回忆 | 已解锁的物件、行动或情感片段 | 批准的纯文字回忆正文 | 合法空页；不显示 per-memory image/alt 字段 |
| 旅途记录 | 成就名称 + “新记录/曾经走过” | 批准描述 | 空组不显示；seen 提交失败保留“新记录” |
| 结局 | 已完成结局标题与短摘要 | 静态摘要及原序 1–3 条原因 | 未解锁不显示；catalog 故障进入 ContentHandoff |

## States & Variants

| State | Trigger | Actions / Focus |
|---|---|---|
| Loading/Validating | 打开手册 | 无旧 snapshot；验证后进入 Contents |
| Contents | bundle valid | chapter 首焦点；四入口可达 |
| Category empty | 合法空数据 | 只显示 section_back、journal_close；首焦点返回目录 |
| Category unavailable | 单区加载失败 | retry、返回目录、关闭；首焦点 retry |
| Content handoff | 顶层 bundle 无效 | reload、返回安全菜单、退出 |
| Item Detail | 选择 row | 首焦点返回列表；保存 row/scroll anchor |
| SeenAckPending | 离开旅途记录/关闭 | gate 输入，静态显示“正在整理手册……” |
| Persistence recovery | root 无效/commit unknown | 清除普通 Journal，由 SYS-PERSIST 接管 |

## Interaction Map

| Action | Input | Outcome | Event |
|---|---|---|---|
| 进入分区 | 键盘/鼠标 | Category List | `journal_category_opened`（本地测试可选；无 telemetry） |
| 打开条目 | 键盘/鼠标 | Detail + scroll anchor | `journal_item_opened`（可选） |
| 返回 | Escape/右键/按钮 | 上一层一次 | no analytics |
| 关闭 | Escape/按钮 | caller restore | `journal_close_requested`（可选） |
| 标记已见 | 退出旅途记录/关闭 | one bounded batch | SYS-PERSIST request；不可显示成功 toast |

键盘 Tab/Shift+Tab 顺序：页面标题（不可聚焦）→当前分区/条目→viewport 内可见交互项→固定 action rail。方向键、PageUp/PageDown 和鼠标复用同一 semantic action；viewport 外目标必须先自动滚入视野。

## Events Fired

| Player Action | Event / State Change | Payload / Notes |
|---|---|---|
| 进入分区 | `journal_category_opened` 或 no event | 本地测试可选；无 telemetry |
| 打开条目 | `journal_item_opened` 或 no event | 不含内部条件或 hidden content |
| 返回/关闭 | `journal_close_requested` 或 no event | 关闭后恢复 caller/fallback |
| 标记已见 | SYS-PERSIST bounded request | 只在离开旅途记录/关闭时提交；失败保留新记录 |

## Data Requirements

| Displayed Data | Source System | Read / Write | Update / Null Handling |
|---|---|---|---|
| 四个分类入口 | SYS-JOURNAL catalog | Read | bundle 未验证前不显示普通目录 |
| 章节与回忆条目 | SYS-NARRATIVE player-safe catalogs + SYS-JOURNAL read model | Read | 空分区显示中性空页；缺失条目不显示内部 ID |
| 旅途记录与 seen 状态 | SYS-ACHIEVE + SYS-PERSIST snapshot | Read / bounded seen request | persistence unavailable 不伪装成全部未解锁 |
| 结局标题与静态原因摘要 | SYS-ENDING journal catalog + SYS-PERSIST membership | Read | 未解锁不显示；catalog 无效进入 content handoff |
| scroll position / caller focus | session-local navigation state | Ephemeral read/write | 进程退出清除，不写 save/persistent |

## Accessibility Requirements

- Self-voicing顺序固定：标题→说明→分区/条目→状态→操作；不朗读隐藏条目、分母、内部ID。
- 最大 7/7/11/6 条目连续可达，不分页；1280×720、字体1.5下固定 action rail可见。
- 列表状态使用“新记录/曾经走过”文字+非颜色标识；高对比移除纸纹；reduced-motion 首帧直接稳定。
- 章节与回忆使用不同标题、说明与内容目录，避免玩家误认为重复收藏。
- 标题/正文允许40%扩展；详情正文只在 viewport 内滚动，返回操作不随文本滚走。
- 使用项目唯一冻结层级 `P0-ACCESS-KEYBOARD-MOUSE-SAPI-EQUIVALENCE`；焦点、viewport、状态、读序和恢复规则以 requirements 文件为准。

## Transitions & Animations

- Enter：先显示 `Validating` 静态状态，再以单次替换进入 `Contents`；不得展示旧 snapshot。
- Category/List/Detail：默认可使用短切换，但 `reduced_motion` 直接呈现最终稳定帧；不依赖纸页位移或 spinner。
- SeenAckPending：静态 pending frame 立即替换当前内容并 gate 输入；结束后移除状态或转 recovery。
- Exit：按层级直接返回并恢复语义焦点与滚动位置；不可用时回到批准 fallback。

## Performance

- `Validating` 到首个可交互 `Contents` 的 p95 目标 ≤ 500 ms；seen acknowledgement 的正常保存目标 ≤ 500 ms；最低硬件与测试 fixture 待 Ren'Py evidence 冻结。

## Localization Considerations

四类入口、章节标题、状态标签、空页、故障和 self-voicing transcript 按至少 40% 文本扩展预留；日期和时长按本地化格式显示，不使用内部 ID fallback。

## Acceptance Criteria

- [ ] 从主菜单和安全游戏菜单打开时均先进入 Validating，再显示新 Contents，不显示旧 snapshot。
- [ ] 四入口、四区列表、详情、空页与错误页均可通过键盘和鼠标完成。
- [ ] 最大集合7/7/11/6项在1280×720、字体1.5下无截断、分页或隐藏焦点。
- [ ] Escape/右键每层只执行一次并正确恢复 caller/列表滚动位置。
- [ ] 旅途记录标记已见只发生一次受控提交，失败仍保留“新记录”，不显示成功提示。
- [ ] persistence/content recovery抢占时普通Journal、旧焦点与返回旁路不可达。
- [ ] Validating、合法空页、CategoryUnavailable、ContentHandoff、SeenAckPending 与 persistence recovery 均能显示安全且可 self-voicing 的状态文案。

## Open Questions

- 四类空页文案、category unavailable文案和 self-voicing transcript 需在 ux-review 中做最终 spoiler 审查。
