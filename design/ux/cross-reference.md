# UX Cross-Reference：关键屏幕与 GDD 覆盖

> **Status**：Approved
> **Platform Target**：Windows 10/11 x86-64；鼠标 + 完整键盘；部分 Ren'Py 默认手柄映射不作为独立验收路径；无触控
> **Template**：UX Cross-Reference
> **Last Updated**：2026-08-09
> **Accessibility tier**：`P0-ACCESS-KEYBOARD-MOUSE-SAPI-EQUIVALENCE`

## Coverage Matrix

| GDD / contract | Covered by | Result |
|---|---|---|
| SYS-CHOICE choice surface、focus、reaction gate | `narrative-choice.md`、`interaction-patterns.md` | Approved; implementation/evidence bound |
| SYS-JOURNAL hierarchy、四区、空态、详情、seen pending、recovery | `journal.md`、`game-menu.md` | Approved; player-visible copy frozen in `design/content-lock.md`; catalog/evidence gates remain downstream |
| SYS-SAVE slot browser、overwrite/load confirm、LoadedUnvalidated、blocking restore | `save-load.md`、`game-menu.md` | Approved; engine integration evidence remains downstream |
| SYS-ACCESS 五项设置、preview/apply/cancel、focus、font 1.5 | `settings.md`、`interaction-patterns.md` | Approved; tier frozen, engine evidence bound |
| Frozen P0 Accessibility Tier、证据矩阵与三层 gate | `design/accessibility-requirements.md`、`sys-access.md`、`sys-test.md` | Approved contract; evidence remains explicitly downstream |
| SYS-ENDING 1–3 cause cards、顺序、无评分/剧透 | `ending.md`、`journal.md` | Approved; copy lock registered in `design/content-lock.md`; catalog/evidence gates remain downstream |
| Main menu / caller focus / safe entry | `main-menu.md`、`game-menu.md` | Approved; production screen now exposes stable journal/focus entry |
| Art direction / layout readability | `design/art/art-bible.md` | Reference only; not a UX approval |

## Navigation Consistency

```text
应用启动
  └─ 主菜单
      ├─ 开始 → 序章
      ├─ 读取 → Load Browser → validation → stable scene / blocking restore
      ├─ 愿望手册 → Validating → Contents → List → Detail
      ├─ 设置 → PreviewDirty / Apply / Cancel / Recovery
      └─ 退出 → Quit Confirmation

稳定叙事帧
  └─ 游戏菜单
      ├─ 继续
      ├─ 保存 / 读取
      ├─ 愿望手册
      ├─ 设置
      └─ 回到标题
```

当前文档之间没有发现入口/出口冲突。所有 modal 使用取消默认焦点；所有 Journal 返回均恢复 caller 或批准 fallback；critical/recovery 状态不保留菜单旁路。

## Accessibility Check

- 唯一层级：`P0-ACCESS-KEYBOARD-MOUSE-SAPI-EQUIVALENCE` 已由 `design/accessibility-requirements.md` 冻结；它是 P0 屏幕的唯一 accessibility tier，不代表运行时证据已经完成。
- 键盘：所有关键屏幕均定义 focus 顺序、Enter/Space、Escape/右键与 viewport 行为。
- 平台：所有关键屏幕现在声明 Windows 10/11、鼠标/完整键盘、无触控与无 hover 依赖；部分手柄映射不作为独立验收路径。
- 鼠标：与键盘复用 canonical action；不依赖 hover 或精确指针。
- 视觉：焦点、选中、错误、禁用和新记录均有文字/轮廓/形状备份。
- 听觉：self-voicing 为输出通道，不自动 activation；静音不损失关键语义。
- 动效：reduced-motion、闪烁、震动分别降级；结局卡在 reduced-motion 下 0 ms 替换。
- 尺寸：所有规格以 1280×720、字体 1.0/1.25/1.5 为布局基线，并为 1920×1080 留白扩展。

## Gaps / Open Questions

1. `design/player-journey.md` 已补齐并作为七屏 context-arrival 共享输入。
2. Ren'Py 8.5.3 accessibility spike rerun-27 已通过 focus、Tab traversal、读序、1.5 字体布局与 offscreen viewport 自动滚入；SAPI 当前仍只记录 capability enumeration，未宣称人工听测 PASS。
3. `design/content-lock.md` 已冻结当前 runtime/source copy；逐屏 production 截图、SAPI 人工听测、语义等价和最终 release evidence 仍属于下游 gate。
4. timed choice 属于 SYS-TENSION post-MVP，不在本 P0 规格内；完整手柄/触控 tier 也不属于当前 P0 支持声明。

## Review Readiness

在创建 UI epics/stories 前，应对以下文件运行 `/ux-review`：

- `design/accessibility-requirements.md`（作为共享 P0 tier 与证据/gate 入口）

- `main-menu.md`
- `game-menu.md`
- `narrative-choice.md`
- `journal.md`
- `save-load.md`
- `settings.md`
- `ending.md`

本报告记录七个关键屏幕已经通过本轮 UX review；逐屏实现、截图/transcript、SAPI 人工听测、语义等价和 release 字体授权仍按 `design/accessibility-requirements.md` 的下游 gate 继续验证，不得把本 UX approval 扩大为 Production/Release approval。
