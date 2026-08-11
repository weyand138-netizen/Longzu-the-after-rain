# P0 Accessibility Requirements：唯一无障碍层级

> **Status**：Frozen P0 contract；2026-08-09 UX gate PASS，Production/Release evidence remains downstream
> **Owner**：SYS-ACCESS；验证由 SYS-TEST 编排，逐屏实现由 UX/Engine/UI owners 负责
> **Last Updated**：2026-08-09
> **Applies to**：Windows 10/11 x86-64、Ren'Py 8.5.3、离线运行的 P0 build
> **Tier name**：`P0-ACCESS-KEYBOARD-MOUSE-SAPI-EQUIVALENCE`

## 1. Purpose and authority

本文件冻结项目唯一的 P0 Accessibility Tier。所有 P0 屏幕、交互模式、可访问因果摘要、设置入口、自动化测试和发布证据都必须引用本文件；不得再创建第二套字体、对比度、朗读、焦点或无障碍设置合同。

权威输入为：

- `design/gdd/sys-access.md`：五项设置、语义等价、稳定焦点、viewport、SAPI preflight、恢复默认值和非视觉边界；
- `design/gdd/sys-test.md`：证据类型、`FAST`/`INTEGRATION`/`RELEASE` 生命周期、current/stale、阻断聚合和 `TEST-DOM-009`；
- `design/ux/interaction-patterns.md`：控件、focus graph、状态、滚动、动效和声音的共享规则；
- `design/ux/cross-reference.md`：七个关键屏幕的映射与当前 review 状态；
- `design/art/art-bible.md`：视觉层级、字体/授权前提、颜色备份、1280×720、1.5 倍字体和动效约束。

本文件是要求与验收规则，不是 Ren'Py 实测报告、截图基线、SAPI 听测结果或最终字体授权证明。凡标记为“必需证据”的项目，在证据产生前只能是 `BLOCKED_INPUT` 或未验收，不能写成 PASS。

## 2. Frozen tier: support boundary

### 2.1 P0 must support

P0 必须在下列范围内提供语义等价的完整体验：

| 范围 | 冻结要求 |
|---|---|
| OS/runtime | Windows 10/11 x86-64；Ren'Py 8.5.3；离线运行；目标环境必须由 version-pinned environment manifest 标识 |
| Primary input | 鼠标与完整键盘均可独立完成所有 P0 核心流程；鼠标和键盘调用同一个 canonical action，不得存在鼠标专属或键盘专属结果 |
| Keyboard | 主菜单、游戏菜单、叙事推进、选择、存档、读档、愿望手册、设置、结局、确认、错误和恢复均可只用键盘完成；不得要求精确指针、hover、拖拽或同时依赖鼠标 |
| Visual modes | `font_scale ∈ {1.0, 1.25, 1.5}`；`high_contrast`、`reduced_motion`、`flash_effects_enabled`、`screen_shake_enabled` 均为项目设置的唯一权威 |
| Non-visual output | 首发支持至少一个 Windows 10/11 + 简体中文 Windows SAPI 可用配置；self-voicing 读出已批准的语义内容、当前焦点和状态，不自动执行动作 |
| Causality | 视觉、静态文字/字幕、self-voicing、reduced-motion 和静音路径消费同一 canonical semantic identity；反应、payoff、章节摘要和结局原因不得因通道改变 |
| Safety | loading、empty、error、disabled 和 recovery 都有可理解、可重访、可键盘到达的状态；阻断状态 fail closed，不返回隐藏 caller 或旁路操作 |

### 2.2 Deferred to post-MVP

以下项目可以延期，但延期必须在产品、UX、测试和发布文案中保持一致，不得被当前 P0 暗示为已支持：

- `SYS-TENSION` timed-choice、活动计时器、暂停区间、timeout choice 及其完整的 self-voicing/focus/recovery 矩阵；
- 与 timed surface 绑定的存档、回退、输入竞态和计时性能证据；
- 完整手柄 tier、触控 tier、其他操作系统或其他屏幕阅读器的专门交互合同；
- 除当前批准的简体中文 SAPI 配置外的语音语言、语音质量和语音供应商矩阵。

### 2.3 Explicitly not supported by this tier

下列项目不属于本 P0 tier，不能以“默认可用”“Ren'Py 默认行为”或单次演示替代支持声明：

- 触控输入；
- 完整手柄作为独立验收路径，或需要手柄震动/haptic 才能理解信息；
- 依赖外部屏幕阅读器运行本项目专属语音合成的保证；clipboard voicing 可与外部工具互操作，但不是项目单独保证的 TTS 后备；
- Windows 10/11 之外的平台、在线语音服务、联网下载语音或静默切换到未知服务；
- Ren'Py engine 的第二套字体倍率、高对比设置、`Preference("accessibility menu")`、默认 `Shift+A` 控制转移，或任何未登记的快捷键旁路。

## 3. Interaction and layout contract

### 3.1 Complete keyboard, stable focus and viewport

1. 每个 interactive element 必须有稳定 `semantic_id`、可访问名称、canonical action 和非颜色焦点状态。Tab/Shift+Tab、方向键、Enter、Space、Escape、PageUp、PageDown、Home、End 以及屏幕声明的快捷键必须覆盖其所属 focus graph；端点不循环，除非该屏幕明确注册循环列表。
2. 每个普通 surface 必须有且只有一个合法初始焦点；modal 必须 trap focus，关闭后恢复 opener 的 stable semantic ID，若 opener 已不存在则使用 owning screen 的冻结 fallback 顺序。
3. 动态重排、字体切换、对比模式切换、列表刷新和 recovery handoff 后，焦点按 stable semantic ID 恢复；不得用坐标、旧 displayable identity 或“最接近控件”猜测。
4. 焦点移动到 viewport 外的内容时，系统必须先将该内容完整滚入视野，再接受 activation。自动滚入不得提交 action、改变叙事进度、触发 rollback/rollforward 或抢走焦点。
5. 长文本、列表、详情和设置必须使用 keyboard-operable viewport；固定 action rail 与正文滚动区分离。字体 1.5 下主要操作、当前焦点、错误和安全出口不得被滚出唯一可达区域。
6. 鼠标 hover 只能提供补充视觉反馈，不得是信息、焦点、self-voicing、确认或 action 的前置条件。右键与 Escape 只执行当前 surface 批准的返回动作一次，不能向底层传播。

### 3.2 Viewport and font gates

以下组合是所有 P0 屏幕的硬布局矩阵：

| Viewport | Font scale | Gate |
|---|---:|---|
| 1280×720 | 1.0 | 必须完整可读、可键盘操作、无裁切 |
| 1280×720 | 1.25 | 必须完成语义重排或 viewport 滚动；不允许隐藏主操作 |
| 1280×720 | 1.5 | 硬基线；零 clipped glyph、零不可达内容、零被滚出唯一可达区的 required action |
| 1920×1080 | 1.0/1.25/1.5 | 留白扩展允许变化，但不得改变阅读顺序、focus graph 或 canonical action |

截图和自动化布局记录必须证明：所有可见文本换行完整；控件边界不重叠；初始焦点可见；每个 required action 键盘可达；viewport 自动滚入；固定 action rail 在三档字体下仍可操作。不得把“看起来没有溢出”当作 Ren'Py 实测证据。

## 4. Visual, motion, flash, shake and sound rules

### 4.1 Contrast and non-color semantics

- 普通文本目标对比度至少 `4.5:1`，大文本至少 `3:1`；焦点边框与控件边界至少 `3:1`。最终渲染值必须由目标引擎截图测量确认；Art Bible 的色票本身不是测量结果。
- `high_contrast=true` 提升文字、焦点、边界和状态分离，移除不必要纹理/雨痕等装饰；不改变 choice、因果、结局或数据语义。
- 错误、警告、选中、新记录、禁用、loading、empty 和 recovery 必须至少同时使用文字 + 轮廓/形状/位置中的一种备份。红色、青色、暖色、亮度和图标都不能单独承载结果。
- 焦点必须由轮廓、填充、位置或文字状态表达；不得只换颜色。图标必须配文字或 accessible name。

### 4.2 Reduced motion, flashing and shake

三个开关互相独立，默认均为关闭/安全值：

| Setting | When enabled/true | When disabled/false | Prohibited |
|---|---|---|---|
| `reduced_motion` | 非必要转场立即到 authored final state；循环与装饰运动停止；保留最终语义 | 使用批准的默认短转场 | 等待旧动画完成后才接受输入或恢复焦点 |
| `flash_effects_enabled` | 允许已批准且非唯一的信息闪光 | 立即停止闪光，使用静态文字/边框/形状替代 | 闪光作为唯一成功、危险、因果或可操作提示 |
| `screen_shake_enabled` | 允许已批准的画面位移 | 立即停止、复位视口，保留同一内容和焦点 | 震动/位移作为唯一语义；把 haptic 当作本 P0 支持 |

任一运动、闪光或震动没有静态语义等价物时，内容/构建验证失败；不得静默删除唯一反馈。静音、self-voicing 或 reduced-motion 只改变输出载体，不得改变 action、顺序、结果或可重访性。

### 4.3 Mute and causal equivalence

- 静音后，所有关键事实仍必须通过可见文字、字幕、状态文本、轮廓/位置和可访问 transcript 理解；声音不得是确认、错误、反应、payoff 或结局原因的唯一通道。
- self-voicing 开启时可抑制非必要提示音；不得抑制语义文本或把提示音当作成功证明。
- 任何只由声音、动画、人物距离、视线、物件变化或演出感知的 production reaction/payoff，必须绑定批准的 `accessible_causal_summary_id`。视觉文本、descriptive subtitle、self-voicing 和 reduced-motion 变体必须引用同一 identity。
- 摘要只能陈述已观察或已确认的事实，保留原有不确定性，不得泄露轴、token、内部 cause ID、资格条件、未来路线、分数或测试状态。

## 5. Self-voicing, SAPI and transcript contract

### 5.1 Support and preflight

发行支持矩阵至少冻结一个 Windows 10/11 + 简体中文 Windows SAPI 可用配置。首次启用 self-voicing 或执行非视觉验收前，preflight 必须区分：

1. voice 缺失；
2. voice 初始化失败；
3. 运行中 speech 失败；
4. clipboard 不可用。

失败时保留完整视觉/键盘路径，显示玩家安全的本地化提示，并在 clipboard 可用时复制同一提示；不得宣称该机器通过独立非视觉支持，不得联网下载语音或静默改用未知服务。这里的支持矩阵、可用性和听测结果必须由证据确认，本文件不预先声明任何机器已通过。

### 5.2 Reading order and behavior

- 读序遵循 surface 的 canonical reading order：屏幕标题/状态 → 当前上下文或说明 → 主内容 → 当前焦点控件的 accessible name、位置/序号、当前值和可用状态 → 固定 action rail；具体 screen 可在不改变语义的前提下注册更细的顺序。
- focus 移动时只宣布新焦点及其必要状态；切换 surface 时宣布标题和当前焦点一次。self-voicing 绝不自动 activation、确认、推进、滚动至新内容或改变焦点。
- Choice Surface 必须读 prompt、选项序号和完整选项文本，不读隐藏轴、token、成本、预测或内部 ID；确认后读批准的 reaction/payoff 摘要。
- loading/empty/error/disabled/recovery 必须有可朗读的标题、当前状态、原因范围和批准动作；状态变化可宣布一次并可重访，不能用自动 dismiss 让玩家错过关键事实。
- transcript 的顺序必须与键盘 walk 和可见阅读顺序一致。transcript 记录的是本地化玩家可见语义，不是内部 debug trace、TTS 引擎日志或未经批准的推断。

### 5.3 Transcript minimum record

每个 self-voicing/transcript case 至少记录：`surface_id`、`state_id`、`mode`、`font_scale`、`high_contrast`、`reduced_motion`、静音状态、环境 identity、语音 capability/preflight result、focus/action sequence、按顺序的 `localized_text_id` 或 approved text、announcement count、是否自动执行 action，以及 raw transcript/hash。缺少原始 transcript 或读序无法审阅时，criterion 为 `BLOCKED_INPUT`，不能由截图或摘要补齐。

## 6. Required state behavior

所有 P0 屏幕必须覆盖下列状态；每个状态均须有文字、焦点、键盘动作、静音表现和 transcript 行为：

| State | Required behavior |
|---|---|
| `loading` | 显示静态“正在加载/处理中”语义；spinner/动画不是唯一证据；禁止重复提交、隐藏焦点或自动推进 |
| `empty` | 明确说明没有内容及安全下一步；焦点落在安全返回/关闭/继续动作，不能落在空容器 |
| `error` | 用玩家可理解的标题、影响范围和可批准动作说明失败；不得只显示技术错误、声音或颜色；不得自动 dismiss |
| `disabled` | 明确显示不可操作及必要原因；移出 focus graph；快捷键、鼠标、右键和替代 activation 不得绕过 disabled gate |
| `recovery` | fail closed；清除不可信 draft/pending action，使用安全恢复默认值（高对比、字体 1.5、reduced-motion 开、闪烁关、震动关），保留批准的安全出口；不得返回旧 caller 或写回临时默认值 |

`Applying`、`StaleConflict`、`SettingsUnavailable`、`LoadedUnvalidated` 等已有 owning GDD 状态必须遵循上述原则，并保留其 owner 定义的唯一动作和错误优先级。

## 7. Evidence matrix

下表定义“证明什么”和“允许的证据类型”。它不表示证据已经产生；每一行都必须绑定 SYS-TEST criterion/case、当前 source/catalog/config/fixture/runner/environment identity 及 raw artifact。`TEST-DOM-009` 是现有跨系统承接点；若新增 requirement ID 未映射到已批准 criterion，必须先更新 SYS-TEST manifest。

| Requirement area | Automation / instrumentation | Screenshot / visual | Transcript | Human acceptance | Blocks |
|---|---|---|---|---|---|
| Windows 10/11、Ren'Py、键盘/鼠标 support matrix | environment preflight、keyboard walk、mouse/canonical-action parity、keymap scan | 每个 screen 的初始焦点和关键状态 | capability/preflight record；无可用 SAPI 时的安全提示 | 人工完成一条只键盘流程和一条只鼠标流程 | UX Stories Ready；Production；Release |
| 完整键盘、stable focus、viewport auto-scroll | focus graph reachability、action count、focus restore、viewport visibility assertions | 1280×720 下焦点前后及自动滚入 capture | 读序与 focus sequence | 人工观察无焦点丢失、无 trap、无 hidden bypass | Production；Release |
| 1280×720 × 1.0/1.25/1.5 | layout matrix、clipped glyph/intersection/unreachable-content assertions | 每屏/每模式截图，含长文和固定 action rail | 三档字体读序 | 人工确认可读性和操作连续性 | UX Stories Ready；Production；Release |
| High contrast、reduced motion、flash、shake | setting tuple、transition duration、flash/shake suppression、semantic equivalence | 模式前后静态替代表现 | 模式切换后同一语义顺序 | 人工确认静音/动效关闭后仍能理解 | Production；Release |
| Self-voicing/SAPI | preflight、toggle、no-auto-action、keyboard/TTS replay | voice failure 的视觉安全提示 | raw transcript、读序、announcement count、hash | 简体中文听测：标题、焦点、状态、choice、reaction/payoff、recovery | UX Stories Ready；Production；Release |
| 静音、非颜色和因果等价 | remove-audio/remove-color/remove-motion/reduced-mode replay；semantic tuple compare | 高对比、静音、非颜色状态截图 | 同一 `accessible_causal_summary_id` 的 transcript | 人工复述具体行动、反应、payoff 和结局原因，不接触隐藏状态 | Production；Release |
| loading/empty/error/disabled/recovery | state cross-product、blocked action、retry/safe-exit、recovery invariants | 每种状态的静态 capture | 每种状态一次可重访的文本输出 | 人工确认安全出口、原因和可恢复性 | UX Stories Ready；Production；Release |
| Evidence integrity | non-empty case set、exact case count、current/stale/hash、archive/staging identity | capture raw bytes/hash | transcript raw bytes/hash | reviewer、rubric、adjudication metadata 完整 | Release |

### Evidence status rules

- `UT_PURE`、`UT_ENGINE`、`STATIC`、`INSTR`、`A11Y`、`VISUAL`、`HUMAN`、`REVIEW` 等证据类型不得互相冒充；自动化截图不能替代人工可理解性结论，Python 测试不能替代 Ren'Py-hosted keyboard/focus/TTS 行为。
- 证据必须非空、可重放、与当前输入同世代且 raw output/hash 存在。source、catalog、config、fixture、runner 或 environment 变化后，旧 PASS 为 `STALE`。
- 缺失必需证据、case 数不匹配、运行异常、人工裁定缺失、SAPI voice 未通过 preflight、截图没有 1280×720×1.5、transcript 缺少读序，均使对应 criterion 失败或 `BLOCKED_INPUT`。
- 不得伪造 Ren'Py 实测结果：在真实 engine spike、目标环境截图、focus trace 或 SAPI transcript 产生前，只能写“待验证”。
- 不得伪造最终字体授权：字体文件、简体中文覆盖、嵌入/分发许可和来源 hash 必须由 `docs/legal/asset-register.md` 及批准的字体证据关闭；Art Bible 的字体方向不是授权证明。

## 8. Gate policy

### 8.1 UX stories Ready

每个 UI story 进入 `Ready` 前必须：

1. 引用本文件的 frozen tier 和 owning GDD；
2. 明确所属 screen/state/mode、required actions、初始焦点、focus fallback、阅读顺序、viewport 边界、静音反馈和 transcript 内容范围；
3. 覆盖 loading/empty/error/disabled/recovery（不适用时写明 owner-approved rationale）；
4. 映射键盘、鼠标、字体 1.0/1.25/1.5、高对比、reduced-motion、flash/shake 和 causal summary；
5. 列出所需自动化、截图、transcript、人工证据及其 SYS-TEST criterion/case 归属；
6. 没有未裁决的 P0 语义、动作、读序或安全恢复问题。Ren'Py 行为未知必须有已批准的 engine spike 任务和 `BLOCKED_INPUT` 状态，不能以默认行为假定关闭。

七个关键屏幕必须先通过独立 UX review 才能标记 `Approved`；本轮 review 已在 `production/gate-checks/ux-accessibility-2026-08-09.md` 记录七屏批准。该批准不替代 Production/Release evidence。

### 8.2 P0 Production Gate

Production Gate 被以下任一项阻断：

- 任一 P0 surface 缺少 keyboard walk、稳定焦点、viewport、三档字体或非颜色状态合同；
- 1280×720 × 1.5 存在裁切、重叠、不可达 required action、焦点不可见或自动滚入失败；
- 高对比、reduced-motion、flash、shake、静音或因果摘要移除后丢失唯一语义；
- self-voicing 读序、SAPI preflight、transcript、no-auto-action 或 recovery 行为未完成，或 voice failure 被误记为非视觉 PASS；
- loading/empty/error/disabled/recovery 任一安全状态缺少可理解文本、可键盘动作、稳定焦点或可重访证据；
- 任一 required artifact 缺失、为空、跨世代、stale、hash 不匹配、runner/environment 不匹配或存在 unresolved blocking finding；
- UX review、content-lock、语义等价人工复核或最终字体授权尚未关闭；
- 将 post-MVP timed-choice、手柄/触控或本 tier 明确不支持的能力混入当前 P0 production claim。

### 8.3 Release Gate

Release Gate 除满足 Production Gate 外，还必须完成 `RELEASE` 完整冻结 manifest：

- 七个关键屏幕各自完成 UX review，并由各自 owner 明确批准；本文件不替代逐屏批准；
- staging 与最终 archive 使用同一 candidate identity、source/catalog/config/runner/environment 世代，且 accessibility evidence current；
- 完整截图矩阵、raw transcript、人工 rubric/adjudication、SAPI capability/preflight、字体授权与 `asset-register` 记录齐全；
- release archive、store、正式 save/persistent root 中没有 test observer、spy、fault injector、synthetic fixture、benchmark harness 或 evidence forger；
- SYS-TEST `RELEASE`、视觉/无障碍/人工证据和 SYS-BUILD archive/exclusion reports 全部为 current/PASS；任一缺失只能是 `BLOCKED_INPUT`，不得 partial pass；
- 发行说明只声明本文件 2.1 的支持范围，并显式排除 2.2/2.3 项目。

## 9. Traceability and change control

本文件的 tier 名称、支持边界、三档字体、五项设置、焦点/viewport、读序、静音/非颜色/因果等价和三层 gate 属于冻结合同。任何修改必须同步更新 `sys-access.md`、受影响的 interaction pattern、`cross-reference.md`、SYS-TEST manifest、相关 UX stories 和证据 identity；不得仅修改截图、fixture 或测试期望值来制造 PASS。

当前仍未关闭的是实现/证据工作，不是本 tier 的第二种解释：目标 SAPI transcript 与人工听测、真实逐屏截图矩阵、语义等价人工复核以及 release archive 复核。Ren'Py 8.5.3 shared focus/viewport/self-voicing spike 已由 rerun-27 通过；七个屏幕的 UX review 已在 `production/gate-checks/ux-accessibility-2026-08-09.md` 记录 PASS。剩余项目在关闭前阻断相应 Production/Release criterion，但不应被描述为已经听测或 release 授权。
