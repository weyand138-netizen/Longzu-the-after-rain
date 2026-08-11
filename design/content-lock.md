# 玩家可见 Content Lock

> **Lock ID**: `content_lock:player_visible:v1:2026-08-09`
> **Status**: FROZEN FOR UX REVIEW
> **Owner**: SYS-NARRATIVE for narrative copy; UX for screen copy; SYS-BUILD for hash/provenance enforcement
> **Boundary**: this is a copy freeze, not an `Approved` decision for any UX screen or a claim that the narrative baseline has passed its independent re-review.

本文件冻结当前 production scope 内所有玩家可见文案的来源、边界和变更规则。冻结意味着没有未经登记的逐句修改；它不把内部 ID、debug 文本、测试 fixture、transcript 诊断字段或引擎日志变成玩家可见内容。

## 1. Frozen source manifest

下表中的文件内容以 UTF-8 和 SHA-256 exact match 作为当前 lock 输入。任一文件发生玩家可见文本变化，都必须生成新的 Lock ID、更新 hash、重跑内容约束与定点 `/ux-review all`；不得只改 UI 或只改章节脚本而保留旧 lock。

| Source | Locked player-visible boundary | Lines at lock | SHA-256 |
|---|---|---:|---|
| `game/screens.rpy` | 主菜单、快捷菜单、游戏菜单、存取档、设置、手册、章节完成、确认和通知文案；包含当前字体/字号呈现约束 | 284 | `a9306f29b5b60c922830f333a867081b0c2d09e2b96c80e25be2d2bcbf91e22c` |
| `game/script.rpy` | 启动免责声明与入口可见文案 | 11 | `72f9bd53c52bf953cb1efd3b6f57310cf81ff9ede197dfbf23fd9b76b48f8f0b` |
| `game/chapters/prologue.rpy` | 序章旁白、角色对白、正式选项、章节完成文案 | 97 | `0120f229c00eb2e069712b3881f5134c5d4610f790b8adb133ebb0525d3c161a` |
| `game/11_achievements.rpy` | 当前运行时成就标题/描述/玩家可见提示 | 86 | `0bd4b9b8b0d28f44e61fd2281a06ee884dc59e0921e092345465aca7a1a37b04` |
| `design/narrative/seven-day-content-baseline.md` | 七日章节、choice、reaction、payoff、六结局与真结局尾声的 canonical player-facing content identity 和安全信息边界 | 356 | `2db74f5135321def9c722873ea7eafb42b8103602557b881390421fccdb82ac2` |
| `design/narrative/achievement-catalog.md` | 成就目录的玩家可见分组、标题、描述、顺序与禁止暴露的内部语义 | 64 | `02b3aba5cb0f2b71eefbe49b364471fadc9369027e435b8cf50ac635400dd67e` |

`design/ux/*.md` 和 `design/ux/interaction-patterns.md` 是 layout/state/semantic contract；其中出现的示例状态词只有在进入上述 production source 或另行登记的 catalog 后才是 runtime copy。未登记的 UX 示例不得直接进入 build。

## 2. Exact UI copy currently in runtime

以下短文案是当前 screen source 中的可见字符串，作为审阅索引；完整文本仍以 source manifest 为唯一 exact bytes authority。

| Surface | Frozen copy |
|---|---|
| Title / identity | `雨停之后`；`《龙族》非官方同人视觉小说`；`免费 · 非商业 · 非官方同人`；`制作：Andwey` |
| Main menu | `开始`；`读取`；`设置`；`退出` |
| Quick menu | `回退`；`快存`；`快读`；`手册`；`设置` |
| Menu navigation | `保存`；`读取`；`返回` |
| Save/load empty slot | `空存档` |
| Preferences | `显示与无障碍`；`字体大小`；`100%`；`125%`；`150%`；`窗口`；`全屏`；`辅助开关`；`高对比度：开/关`；`减弱动效：开/关`；`闪烁效果：开/关`；`屏幕震动：开/关`；`文字速度`；`慢`；`标准`；`即时`；`自发声开关`；`应用无障碍设置` |
| Journal | `绘梨衣的愿望手册`；`已经记住的章节`；`还没有。`；`合上手册` |
| Chapter completion | `序章完成`；`有些选择不会立刻告诉你答案。它们会在之后重新出现。`；`回到标题` |
| Confirm | `确定`；`取消` |
| Splash disclaimer | `非官方 · 免费 · 非商业同人`；`本作不代表原作者、出版社或任何官方授权方。`；`请勿将本作内容视为原作正典。` |

高对比度入口不再标记为“预留”；它与字体、减弱动效、闪烁和震动一起进入五项项目设置的单次 batch apply。真实渲染矩阵和语义等价证据仍必须按 evidence matrix 关闭。

## 3. Narrative and catalog freeze rules

- 序章及后续章节的玩家可见对白、旁白、正式 choice caption、reaction/payoff 与 ending/journal 摘要必须来自已登记 source catalog；不以 stable ID、route、axis、token、qualification、predicate、threshold、schema 或错误码作为 fallback 文案。
- `design/narrative/seven-day-content-baseline.md` 与 `achievement-catalog.md` 的当前文本已冻结为 UX review 输入；其既有 `pending re-review` 或下游 gate 状态仍然有效，不得因为本次 copy freeze 被改写成内容 Approved。
- 成就玩家可见分组固定为“场景回声 → 路线发现 → 后来留下的回声”；内部 group key、完成组语义和隐藏评分语义不进入 render 或 self-voicing。
- Journal 的中性首开、四类空页、CategoryUnavailable、ContentHandoff、SeenAckPending、恢复与关闭文案必须在 catalog lock 中登记后才可实现；缺失时 fail closed，不用内部 ID 或泛化错误文案补位。

## 4. Change control

允许的变更只有：

1. 新建递增 Lock ID，并说明玩家可见差异、原因、owner 和 source hash；
2. 重跑 anti-hidden-score / content-identity / source-manifest 检查；
3. 重跑截图、transcript、字体倍率与人工语义等价证据；
4. 重新运行定点 `/ux-review all`，并在逐屏明确得到 `Approved` 后更新 screen status；UX approval 不等同于 Production/Release approval。

在当前 lock 下，未经上述流程不得修改任何玩家可见句子、标点、大小写、选项顺序、状态文案或 self-voicing 读词。内部 debug evidence 可以变化，但不能作为玩家文案的来源。

## 5. Current blockers retained by the lock

- Ren’Py accessibility spike rerun-26 已通过：focus、Tab traversal、读序、1.5 字体截图和 offscreen viewport 自动滚入均通过；原始结果保留在 `docs/engine-reference/renpy/evidence/2026-08-09-accessibility-spike-rerun-26/run/`。
- SAPI 只完成 capability enumeration；未进行人工听测，因此没有伪造 transcript 质量或听测通过。
- `SourceHanSansLite.ttf` 已登记、hash 已核对并附本地 OFL 1.1 文本；本项目 UX gate 视来源与授权记录已关闭，release archive 仍需复核同一 hash。
- 本 lock 允许七个 UX 文档在本轮 review 后标记 `Approved`，但不构成 `/create-epics` 或 Production/Release 授权。
