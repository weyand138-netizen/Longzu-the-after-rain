# 玩家可见 Content Lock

> **Lock ID**: `content_lock:player_visible:v6:2026-08-14`
> **Status**: FROZEN FOR UX REVIEW
> **Owner**: SYS-NARRATIVE for narrative copy; UX for screen copy; SYS-BUILD for hash/provenance enforcement
> **Boundary**: this is a copy freeze, not an `Approved` decision for any UX screen or a claim that the narrative baseline has passed its independent re-review.

本文件冻结当前 production scope 内所有玩家可见文案的来源、边界和变更规则。冻结意味着没有未经登记的逐句修改；它不把内部 ID、debug 文本、测试 fixture、transcript 诊断字段或引擎日志变成玩家可见内容。

## 1. Frozen source manifest

下表中的文件内容以 UTF-8 和 SHA-256 exact match 作为当前 lock 输入。任一文件发生玩家可见文本变化，都必须生成新的 Lock ID、更新 hash、重跑内容约束与定点 `/ux-review all`；不得只改 UI 或只改章节脚本而保留旧 lock。

| Source | Locked player-visible boundary | Lines at lock | SHA-256 |
|---|---|---:|---|
| `game/screens.rpy` | 主菜单、快捷菜单、游戏菜单、存取档、设置、手册、章节完成、确认和通知文案；包含当前字体/字号呈现约束 | 377 | `72d963e5c0df442dec889d1024f82a8951af573575ad5ebd84a8c0e5a7e5a291` |
| `game/script.rpy` | 启动免责声明与入口可见文案 | 18 | `e8c0b143f937aff62f8cce2f3b43160ea4721f4c6edba0f5b0524bc89cf66f12` |
| `game/chapters/prologue.rpy` | 序章旁白、角色对白、正式选项、章节完成文案 | 138 | `d5135e3c124c0cd6ee3455d78210fb45eba5e0e082402ade1961ee1a7b480895` |
| `game/chapters/day1.rpy` | Day 1 衣物、食物、收据名字与既有正式选项的玩家可见文本 | 128 | `8172d12c3676e5b55487ffe76dbb1eb2cbec7e7fd74994e0f9ffe61c1afb01ba` |
| `game/chapters/day2.rpy` | Day 2 昵称、游戏币和末机台场景的玩家可见文本 | 135 | `fafd4643d207450842c6bbfc0a2c57432a4cd006540c0672b035a0578ff02ec1` |
| `game/chapters/day3.rpy` | Day 3 空教室证据、分享/隐瞒和 truth-pacing 场景的玩家可见文本 | 131 | `6bd6d5ed98983bf28027d96d5e61905a67053b2511ff9ca0a2d68cdedfddfb16` |
| `game/chapters/day4.rpy` | Day 4 购票、路线准备、联系人和海边列车场景的玩家可见文本 | 196 | `3ba9867967660d9aeeb16354ed8f0ed0e264f88c2b4761e4b61ef083e9435a4b` |
| `game/chapters/day5.rpy` | Day 5 家族档案、路线回应、责任与修复场景的玩家可见文本 | 249 | `2d1de1d4f10c3fea6df9c514eb7deeba52a4561705328812f30d718eff9d4c05` |
| `game/chapters/day6.rpy` | Day 6 安全屋失效、代价承担与路线承诺场景的玩家可见文本 | 300 | `dbe1f47ce705bc73520c0aa3b6115cd2f803f292605dd2b79a2854adf0ff98be` |
| `game/chapters/day7.rpy` | Day 7 红井前因果回收与唯一 ending handoff 的玩家可见文本 | 50 | `e8c802dfb3ffef5f3e234ce95b810d4af323d5f46c48420183251a43b1eef7b8` |
| `game/11_achievements.rpy` | 当前运行时成就标题/描述/玩家可见提示 | 47 | `18bca7c444314b451f41ab094656f6f8346273ae5a2b22c0fc58dfe8eca5d17c` |
| `game/chapters/endings.rpy` | 六个固定结局闭合与 `rain_stops` 既有 arcade epilogue 的玩家可见文本；Story 扩展只允许在现有 lights-out 之后追加受限短尾声 | 113 | `136055f969ced13e5a1baa60c88b54714dd981ada4232440bfc4b2955bfe5a6c` |
| `design/narrative/seven-day-content-baseline.md` | 七日章节、choice、reaction、payoff、六结局与真结局尾声的 canonical player-facing content identity 和安全信息边界 | 393 | `87e54f616076ef91883ebb687b05468978a7956ecc66bafad512c2797398a85f` |
| `design/narrative/achievement-catalog.md` | 成就目录的玩家可见分组、标题、描述、顺序与禁止暴露的内部语义 | 64 | `02b3aba5cb0f2b71eefbe49b364471fadc9369027e435b8cf50ac635400dd67e` |

> **Story 024 非文案变更说明（2026-08-14）**：`game/script.rpy` 的 source identity/hash 因 Production 入口控制流改为调用唯一固定编排器而刷新；启动免责声明及入口相关玩家可见字符串与 HEAD 完全一致，未发生 copy change。`renpy.is_in_test()` 分支仅保留现有独立章节测试入口，不进入非测试 Production 路径。

> **Story 025 设计变更说明（2026-08-14）**：Lock ID 递增为 v2，因为 `rain_stops` 的既有玩家可见尾声增加了受限的多年以后短尾声。新增内容只使用高层结构与主题，不逐句复制未确认同人参考；不新增 choice、route、ending、achievement、Gallery、persistent 字段或 canonical unit。实现后已刷新 `game/chapters/endings.rpy` 的 hash；仍须将人工 UX/版权/叙事签字列为未完成，不把该扩展宣称为最终文案批准。

> **Sprint 009 文案变更说明（2026-08-14）**：Lock ID 递增为 v3，因为序章、Day 1 和 Day 2 在既有 labels 内增加了场景观察、动作、即时反应与已冻结 payoff 回收。choice/menu/axis/token/resource/route/ending/hidden-rule 合同未变；新增文本不含资产引用，不把人工 playtest、SAPI/semantic、版权或主观叙事评审宣称为完成。

> **Sprint 010 文案变更说明（2026-08-14）**：Lock ID 递增为 v4，因为 Day 3 和 Day 4 在既有 labels 内增加了证据核对、暂停回应、票务准备和联系人风险观察。choice/menu/agency answer/qualification/route/ending/hidden-rule 合同未变；人工体验和最终叙事签字仍未运行。

> **Sprint 011 文案变更说明（2026-08-14）**：Lock ID 递增为 v5，因为 Day 5 和 Day 6 在既有 labels 内增加了档案来源、路线回应、安全屋失效、代价承担与承诺观察。choice/menu/agency answer/qualification/route/ending/hidden-rule 合同未变；人工体验和最终叙事签字仍未运行。

> **Sprint 012 文案变更说明（2026-08-14）**：Lock ID 递增为 v6，因为 Day 7、六个既有 ending 与 `rain_stops` 既有尾声在既有 labels 内增加了因果回收、即时后果和普通生活观察。ending ID/resolver/priority/canonical witness/五轴/token/qualification/predicate/completion boundary 未变；人工体验和最终叙事签字仍未运行。

> **Sprint 013 source identity refresh（2026-08-16）**：以可信提交 `ff00c7a` 为基线，对 `game/screens.rpy` 与 `game/11_achievements.rpy` 做玩家可见文本语义 diff；工作树相对该 HEAD 的 copy delta 为 **0**。本次仅刷新两行的当前行数与 SHA-256，登记为结构/实现 identity refresh，不回退现有实现、不递增 Lock ID、不改变玩家可见文案，也不把旧 v6 hash 当作可恢复源。定点 UX/content/source-manifest 检查需在当前自动化预检中重跑；人工 GUI、SAPI、语义、性能和最终 archive 仍属于未来 Production RC 收尾 Sprint。

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
