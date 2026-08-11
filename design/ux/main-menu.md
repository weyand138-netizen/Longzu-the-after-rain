# UX Spec：主菜单

> **Status**：Approved
> **Author**：Andwey + Codex
> **Last Updated**：2026-08-09
> **Journey Phase(s)**：进入、重返、结束
> **Requirements**：SYS-STATE、SYS-SAVE、SYS-PERSIST、SYS-ACCESS
> **Platform Target**：Windows 10/11 x86-64；鼠标 + 完整键盘；部分 Ren'Py 默认手柄映射不作为独立验收路径；无触控
> **Template**：UX Spec
> **Accessibility tier**：`P0-ACCESS-KEYBOARD-MOUSE-SAPI-EQUIVALENCE`（见 `design/accessibility-requirements.md`）
> **Related**：game-menu、journal、save-load、settings

## Purpose & Player Need

玩家在开始或重返《雨停之后》时，需要快速理解作品气质并安全选择“开始、读取、愿望手册、设置或退出”。主菜单只提供导航，不解释隐藏因果、不展示完成率，不把“开始”包装成最佳路线。

## Player Context on Arrival

首次到达时玩家好奇且未建立信任；重返时玩家可能带着上一轮结局或手册内容。背景使用雨后车站/城市的静态低动效画面，标题与按钮应在 5 秒内可见。

## Navigation Position

`应用启动 → 主菜单`。可进入：`开始 → 序章`、`读取 → Load Browser`、`愿望手册 → Journal Contents`、`设置 → Settings`、`退出 → Quit Confirmation`。

## Entry & Exit Points

| Entry Source | Trigger | Player Context |
|---|---|---|
| 应用启动 | Ren'Py 启动完成 | 首次玩家或重返玩家；persistent 状态尚未向玩家呈现 |
| 安全恢复 | 上游 persistent/recovery gate | 只允许安全出口，不携带可疑收藏或运行时状态 |

| Exit Destination | Trigger | Notes |
|---|---|---|
| 序章 | 开始 | 初始化新游戏；不读取旧 run 的 UI cache |
| Load Browser | 读取 | 主菜单加载不警告当前未保存进度，但仍显示槽位身份 |
| Journal Contents | 愿望手册 | 进入前必须通过 `journal_menu_gate:v1` |
| Settings | 设置 | 仅从安全主菜单进入 |
| Quit Confirmation | 退出 | modal trap focus；取消为默认焦点 |

## Layout Specification

```text
┌────────────────────────────────────────────────────────────┐
│ 雨后车站 / 城市夜景                         版本(非交互)   │
│                                                            │
│  雨停之后                                                   │
│  在东京最后的七天里……                                      │
│                                                            │
│  [开始]                                                     │
│  [读取]                                                     │
│  [愿望手册]                                                 │
│  [设置]                                                     │
│  [退出]                                                     │
│                                                            │
│ 免费·非商业·非官方同人 / 制作信息（低优先级）               │
└────────────────────────────────────────────────────────────┘
```

左侧标题/导航区宽度约 34% 视口；背景关键人物/物件不得被面板遮挡。1920×1080只增加留白；1280×720与字体1.5改为单列并允许标题换行。

### Component Inventory

| Zone | Component | Interactive | Pattern | Data Owner |
|---|---|---:|---|---|
| 标题区 | 标题、副标题 | 否 | Static Announcement | SYS-NARRATIVE / content catalog |
| 导航区 | 开始、读取、愿望手册、设置、退出 | 是 | Semantic Button | 对应调用系统；UI 不拥有游戏状态 |
| 辅助区 | 版本、制作/发行说明 | 否 | Static Announcement | Build metadata / static content |

## States & Variants

| State | Trigger | Change |
|---|---|---|
| Default | 正常启动 | 开始为首焦点；所有可用入口可达 |
| Persistence recovery | persistent 无效 | 进入上游安全恢复；不显示手册/解锁状态 |
| Load unavailable | 无可读存档 | 读取仍可进入，Load Browser显示安全空态 |
| Empty/No readable save | 没有可读取槽位 | 读取入口仍可达，Load Browser 显示安全空态 |
| Quit confirm | 退出 | modal trap focus，取消为默认焦点 |
| Loading | 启动或 catalog/gate 尚未完成 | 显示静态加载状态；首个焦点建立前不接受隐藏输入 |

## Interaction Map

| Action | Input | Feedback | Outcome |
|---|---|---|---|
| 开始 | Enter/Space/鼠标 | pressed→短淡出 | Start，新游戏初始化 |
| 读取 | 键盘/鼠标 | focus + pressed | Load Browser |
| 愿望手册 | 键盘/鼠标 | focus + pressed | Journal Contents；仅安全状态可用 |
| 设置 | 键盘/鼠标 | focus + pressed | Settings |
| 退出 | 键盘/鼠标 | modal | Quit Confirmation |
| 返回 | Escape/右键 | 无 modal 时无动作 | 不传播到 OS；退出由显式按钮完成 |

键盘 Tab/Shift+Tab 顺序为：开始 → 读取 → 愿望手册 → 设置 → 退出；方向键遵循同一线性焦点图。鼠标必须调用相同 semantic action；hover 只能提供视觉补充。

## Events Fired

| Player Action | Event / State Change | Payload / Notes |
|---|---|---|
| 开始 | `new_game_requested` | 无隐藏路线或历史 payload；由 SYS-NARRATIVE/SYS-STATE 处理 |
| 读取 | `load_browser_opened` | 不修改当前状态；无 telemetry |
| 愿望手册 | `journal_open_requested` | 仅在 gate 通过时派发；caller=`main_menu_journal` |
| 设置 | `settings_open_requested` | 不修改项目设置 |
| 退出 | `quit_confirmation_opened` | 不退出应用；等待玩家确认 |
| 返回/取消 | no event | 只执行当前 screen contract 的返回动作 |

## Transitions & Animations

- Enter：启动完成后直接挂载首帧；若启用默认动效，可使用短淡入，但首个焦点必须在 5 秒目标内可用。
- Exit：进入序章或其他页面时短淡出；`reduced_motion` 下 0 ms 直接切换到目标稳定帧。
- Quit Confirmation：立即覆盖并 trap focus；取消关闭 modal 后恢复原焦点，不播放自动 dismiss。
- Loading/error：不使用 spinner、声音或闪烁作为唯一状态证据，至少显示静态状态文案。

## Data Requirements

| Displayed Data | Source System | Read / Write | Null / Failure Handling |
|---|---|---|---|
| 标题与副标题 | SYS-NARRATIVE / static catalog | Read | 缺失时使用批准的静态安全标题；不得显示 ID |
| 版本信息 | SYS-BUILD metadata | Read | 缺失时隐藏非必要版本文本 |
| Journal 可用性 | SYS-SAVE gate + SYS-PERSIST validation | Read | 无法判断时隐藏入口并进入安全恢复，不显示内部错误 |
| Load 可用性 | SYS-SAVE detached slot/readability result | Read | 无可读槽位显示安全空态，入口仍可进入 |

## Localization Considerations

- 菜单按钮按至少 40% 文本扩展预留；`愿望手册`、`设置`、`退出`允许换行但不得截断。
- 副标题最多 2 行；版本和发行说明为非必要信息，溢出时可隐藏。
- 版本号、日期与法律文本必须使用本地化格式；不得以 route/choice ID 作为 fallback。

## Performance

- 目标：在目标机启动后 5 秒内显示主菜单；主菜单首个可交互焦点在稳定帧内建立，不等待淡入动画。
- Ren'Py 8.5.3 accessibility spike rerun-27 已验证键盘初始焦点、安全退出与 offscreen viewport 自动滚入；逐屏截图矩阵继续验证三档字体。

## Accessibility Requirements

- 初始焦点为“开始”；Tab/Shift+Tab按视觉阅读顺序；所有控件有文字名称和非颜色 focus ring。
- self-voicing 顺序：标题→副标题→菜单项→法律/发行说明；不自动激活。
- 高对比移除背景雨纹；reduced-motion 使用静态背景/0 ms切屏。
- 菜单按钮预留至少 40% 中文扩展；副标题允许两行，发行说明不得成为必要信息。

## Acceptance Criteria

- [ ] 最低目标硬件上主菜单在 5 秒内出现首个可交互焦点。
- [ ] 主菜单从启动完成到首个稳定可交互帧的 p95 不超过 5 秒；测试需在项目声明的最低目标硬件执行。
- [ ] 键盘可按“开始→读取→愿望手册→设置→退出”顺序到达全部入口。
- [ ] Journal 仅在安全状态可打开，critical/recovery 状态 action count 为 0。
- [ ] 1280×720、字体1.5下标题、菜单和退出按钮均不裁切且可见。
- [ ] 退出确认默认焦点为取消，Escape/右键不直接退出。
- [ ] 静音、高对比、reduced-motion下仍能完成启动与进入序章。
- [ ] 无 persistence/slot/catalog 数据时，安全空态或恢复态仍提供可键盘到达的安全出口，并不显示内部 ID。

## Open Questions

- 主菜单使用已登记的 Solid 背景与 Source Han Sans Lite 字体；字体来源、hash 与 OFL 文本记录于 `docs/legal/asset-register.md`。
- Ren'Py 8.5.3 shared focus/viewport spike 已通过；逐屏截图与 self-voicing/SAPI 人工听测仍属于实现 evidence gate。
