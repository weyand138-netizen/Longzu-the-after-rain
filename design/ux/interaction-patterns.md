# 《雨停之后》交互规范库

> **Status**: Approved
> **Scope**: P0 shared interaction patterns
> **Input**: 鼠标 + 完整键盘；部分 Ren'Py 默认手柄映射不作为独立验收路径
> **Baseline**: 1280×720、字体 1.0/1.25/1.5、Windows 10/11、无 hover 依赖
> **Platform Target**：Windows 10/11 x86-64；无触控
> **Accessibility tier**：`P0-ACCESS-KEYBOARD-MOUSE-SAPI-EQUIVALENCE`（见 `design/accessibility-requirements.md`）
> **Template**：Interaction Pattern Library

## Pattern Catalog

| Pattern | Category | Used in |
|---|---|---|
| Semantic Button | Navigation/Input | 所有屏幕 |
| Choice Surface | Narrative/Input | 叙事与选择 |
| Fixed Action Rail | Navigation | 主菜单、列表、设置、存读档 |
| Keyboard Viewport | Layout/Input | 愿望手册、设置、详情、长文本 |
| Safe Confirmation Modal | Modal | 覆盖、读档、放弃设置、退出 |
| Blocking Safe Flow | Recovery | 读档失败、持久化/内容错误 |
| Static Announcement | Feedback | 新旅途记录、状态提示、错误提示 |
| Causal Card | Data Display | 结局页、结局详情 |
| Toggle | Input | 设置开关、二态偏好 |
| Slider | Input | Ren'Py 文字/自动/跳过速度、音量 |
| Dropdown | Input | 仅当值域过长且可键盘展开时使用；当前 P0 暂无生产实例 |
| List | Navigation/Data | Journal、Save/Load 槽位列表 |
| Grid | Navigation/Data | Save/Load 卡片布局；导航仍按阅读顺序 |
| Dialog | Modal | 信息说明与非破坏性阻断 |
| Toast | Feedback | 仅非关键、可重访状态；不得作为唯一证据 |
| Tooltip | Feedback | 仅补充解释；不得承载唯一操作或语义 |
| Progress Bar | Data Display | 当前 P0 不用于五轴、完成率或隐藏进度；保留为受限模式 |
| Input Field | Input | 当前 P0 暂无玩家文本输入；如新增需单独审查 |
| Tab Bar | Navigation | 分类切换；必须有键盘 focus 与 selected 文本 |
| Scroll | Navigation/Layout | Keyboard Viewport 内的正文/列表滚动 |

## Global Rules

- 所有 interactive element 有稳定 semantic ID、可见文字、键盘 focus、非颜色 focus 状态和 canonical action。
- `hover` 只能提供补充视觉反馈，不改变焦点、不触发 self-voicing、不执行 action。
- 同一 interaction 内的鼠标、Enter、Space、快捷键或替代 activation 经 activation latch 合并为一次提交。
- `Escape`/右键只执行当前屏幕批准的返回动作一次，不向底层传播；modal trap focus。
- 输出通道（字幕、self-voicing、替代文本）绝不自动推进、确认、滚动或改变焦点。
- `reduced_motion` 直接到最终状态；`flash_effects_enabled=false` 与 `screen_shake_enabled=false` 只移除各自效果，不丢语义。

## Accessibility Baseline

项目唯一 accessibility tier 已冻结为 `P0-ACCESS-KEYBOARD-MOUSE-SAPI-EQUIVALENCE`：普通文本至少 4.5:1，大文本至少 3:1，焦点边框/控件边界至少 3:1；任何状态仍需文字、形状或位置等非颜色编码。SAPI 支持矩阵与 transcript 的实测结论仍由独立 evidence gate 记录。

## Pattern Specifications

### Semantic Button

**Visual**: 平面矩形、文字为主、选中/聚焦使用高对比边框与轻微填充变化。

**Input**: Tab/Shift+Tab 或上下键移动；Enter/Space/鼠标点击激活；端点不循环，除非屏幕明确声明循环列表。

**Feedback**: pressed 只表示输入收到，不预测选择结果；声音/动画可选。

**Accessibility**: accessible name 包含动作与当前值；disabled 控件不可 focus；无 hover 前置条件。

#### Button Variants

| Variant | When to Use | When NOT to Use | Required State Difference |
|---|---|---|---|
| Primary safe | 当前屏幕主要安全推进动作 | 破坏性确认或纯说明 | 文字层级更高；仍需非颜色 focus |
| Secondary | 返回、查看、次级导航 | 唯一必须完成的提交 | 与 primary 保持相同语义状态 |
| Destructive | 退出、覆盖、放弃进度 | 普通导航或不改变数据的动作 | 完整动作标签 + Safe Confirmation Modal |
| Disabled | gate 明确禁止操作 | 隐藏内部状态或“错误答案” | disabled 文案/状态可理解且移出 focus graph |

### Choice Surface

**Visual**: 单列、canonical 顺序、整行可点击；当前 choice prompt 位于选项之前；quick actions 不与 choice 争夺主要注意力。

**Input**: 初始焦点第一项；Up/Down 或 Tab/Shift+Tab移动；Enter/Space/鼠标共用 canonical `choice_id`；不显示 semantic_major/narrative_only、轴、token、成本或预测。

**Feedback**: confirmed 后立即锁定选项，退场进入 reaction；reaction 期间不允许 save/load/rollback/skip 或另一个 choice。

**Accessibility**: 文本完整换行；focus 使用边框+形状/填充；self-voicing 读提示、序号、完整文本，不能自动确认。

### Fixed Action Rail

**Visual**: 固定在 viewport 外，尺寸低于主要叙事/正文；在字体 1.5 下保持可见。

**Input**: 位于屏幕 focus graph 末尾，按阅读顺序；Escape/右键按 screen contract 处理。

**Use**: 返回、关闭、应用、分页等安全动作。禁止把隐藏 debug、内部状态或不安全入口放入 rail。

### Keyboard Viewport

**Visual**: 内容滚动区与固定 action rail 分离；不使用滚动条颜色作为唯一状态。

**Input**: PageUp/PageDown 滚动；Tab/Shift+Tab 或 self-voicing 导致焦点越界时先自动滚入视野；焦点使用 semantic ID 恢复。

**Use**: 长章节、详情、设置；滚动不触发 rollback/rollforward 或 activation。

### Safe Confirmation Modal

**Visual**: 中央深色/纸色面板，影响摘要先于操作；取消是默认焦点，破坏性动作使用完整标签。

**Input**: Modal trap focus；Escape/右键回到上一层；确认只提交一次。

**Use**: 覆盖存档、放弃未保存进度、放弃设置、退出。

### Blocking Safe Flow

**Visual**: 中性、无技术栈细节、无路线剧透；标题→安全说明→安全出口。

**Input**: 只保留批准的安全操作；阻断期间禁止返回 caller、save/load/rollback/quick actions/skip/auto。

**Use**: unsupported/corrupt load、持久化恢复、内容 bundle handoff。

### Static Announcement

**Visual**: 静态文本/小型 modal；不使用 toast 作为唯一证据，不覆盖当前 choice/reaction。

**Input**: 由玩家继续/关闭；Escape 行为由调用方声明。

**Accessibility**: self-voicing 恰宣布一次；关闭/继续后恢复 stable semantic focus。

### Causal Card

**Visual**: 结局标题后出现 1–3 张米白/深蓝信息卡，保持 resolver 原序；没有评分、百分比、缺口提示。

**Input**: 正常叙事推进与键盘 focus；无 timed input。

**Accessibility**: 文字明确引用具体行动/物件/后果；不出现 axis、token、cause ID、条件或未到达路线要求；reduced-motion 为 0 ms 替换。

## Pattern Usage and Exclusion Matrix

| Pattern | When to Use | When NOT to Use | Required States / Implementation Boundary |
|---|---|---|---|
| Semantic Button | 单一安全 action 或导航 | 长正文、隐藏 debug、需要输入值 | idle/focused/pressed/disabled；owner system 执行 action |
| Choice Surface | 叙事 choice 且选项同层级 | 菜单导航、评分或设置 | idle/focused/pressed/confirmed/disabled/loading；只消费 canonical choice |
| Fixed Action Rail | 返回、关闭、应用、分页 | 主要正文、隐藏状态或不安全入口 | visible/disabled/focused；固定在 viewport 外 |
| Keyboard Viewport | 长文本、列表或设置溢出 | 唯一安全出口、短按钮列表 | top/middle/bottom；滚动不触发 action |
| Safe Confirmation Modal | 覆盖、放弃、退出、加载确认 | 普通说明或无需确认的导航 | open/focused/confirming/error；取消默认焦点并 trap |
| Blocking Safe Flow | 不安全状态必须 fail closed | 普通错误提示、可继续的局部错误 | blocking/retry/safe-exit；销毁旧 caller |
| Static Announcement | 可重访的状态/错误/待处理说明 | 唯一成功证据或需要自动 dismiss 的关键状态 | visible/dismissed；静态文本与 transcript 等价 |
| Causal Card | 玩家安全的结局原因摘要 | 内部 cause、分数、阈值或预测 | 1–3 cards，保持 resolver 顺序；不重排 |

## Standard Control Specifications

以下标准控件均继承 Global Rules，并必须提供稳定 semantic ID、键盘焦点、非颜色状态、静音可理解反馈和 1.5 字体布局验证。

### Toggle

- **When to Use**：二态、可即时理解的偏好，例如高对比、减弱动效、闪烁或震动。
- **When NOT to Use**：三档以上值域、破坏性动作或需要确认的持久化批量提交。
- **States**：off、on、focused、disabled、applying、error；状态必须有文字值。
- **Accessibility**：accessible name 朗读标签 + 当前值 + 生效方式；Space/Enter 与鼠标调用同一 action。
- **Implementation**：使用 semantic ID 绑定 canonical setting；不由 UI 直接写 persistent。

### Slider

- **When to Use**：连续或多档有序值，如音量、文字速度、自动/跳过速度。
- **When NOT to Use**：选项数量少且语义离散的字体倍率或二态开关。
- **States**：minimum、intermediate、maximum、focused、disabled、applying、error。
- **Accessibility**：标签、当前值、单位和步长可朗读；Left/Right 调值，Tab 离开控件，不依赖颜色或刻度视觉。
- **Implementation**：范围和步长由 engine/GDD owner 冻结；避免在 UX 层写死临时 spike 值。

### Dropdown

- **When to Use**：值域较长且屏幕空间不足，并且所有选项可键盘展开和朗读。
- **When NOT to Use**：值域 ≤ 3、需要快速比较或字体 1.5 下展开列表会遮挡决策内容。
- **States**：collapsed、expanded、focused、selected、disabled、error。
- **Accessibility**：展开状态、选中值、选项总数和关闭方式可朗读；Escape 只关闭列表，不向底层传播。
- **Implementation**：弹出层 trap focus；选项顺序稳定，不按隐藏状态重排。

### List

- **When to Use**：按阅读顺序展示可选条目，支持空态、错误态和 viewport。
- **When NOT to Use**：条目需要同时比较二维信息且没有明确阅读顺序。
- **States**：populated、empty、loading、unavailable、focused、selected。
- **Accessibility**：首项焦点明确；条目名称、状态和位置可朗读；空态焦点落安全返回。
- **Implementation**：使用稳定 item ID 和 keyboard viewport；外部刷新不得自动抢焦点。

### Grid

- **When to Use**：Save/Load 等卡片需要二维空间利用，但仍能定义从左到右、从上到下的焦点顺序。
- **When NOT to Use**：长文正文、纯线性叙事选择或无法定义一致焦点图的内容。
- **States**：populated、empty、focused、disabled、unreadable/error。
- **Accessibility**：朗读行列位置和卡片安全摘要；键盘顺序不能依赖鼠标坐标。
- **Implementation**：字体 1.5 时允许卡片纵向重排；分页/分区按钮位于固定 action rail。

### Dialog

- **When to Use**：需要玩家阅读说明或处理非破坏性状态的短暂阻断。
- **When NOT to Use**：必须确认数据损失、覆盖或退出的操作；这些使用 Safe Confirmation Modal。
- **States**：open、focused、closed、error、loading。
- **Accessibility**：标题、说明、动作顺序可朗读；trap focus；关闭后恢复 opener。
- **Implementation**：不使用自动 dismiss；Esc 行为由调用方明确声明。

### Toast

- **When to Use**：非关键、可通过当前页面重访的轻量状态反馈。
- **When NOT to Use**：保存成功/失败、seen acknowledgement、阻断恢复或任何玩家必须理解的事实。
- **States**：queued、visible、dismissed、suppressed；若有 auto-dismiss 必须声明时长。
- **Accessibility**：必须有页面内静态文本等价物；self-voicing 不得自动激活或抢焦点。
- **Implementation**：按优先级排队，禁止覆盖 choice/reaction；自发声开启时抑制非必要声音。

### Tooltip

- **When to Use**：补充可选解释，且同一信息已在 accessible name 或正文中出现。
- **When NOT to Use**：操作说明、错误原因、选择语义或任何只在 hover 时可见的信息。
- **States**：hidden、focused、shown、dismissed。
- **Accessibility**：键盘 focus 可触发；不改变焦点、不自动朗读、不依赖精确悬停。
- **Implementation**：不得遮挡主要内容；字体放大时可转为 inline text。

### Progress Bar

- **When to Use**：仅用于有明确玩家可见进度且不属于隐藏状态的任务。
- **When NOT to Use**：五轴、完成率、路线、结局概率或任何会成为隐藏状态代理的内容。
- **States**：empty、partial、complete、indeterminate、error。
- **Accessibility**：必须有数值或文本等价；indeterminate 必须有静态状态说明。
- **Implementation**：当前 P0 无生产使用；新需求必须同时更新 GDD 与 UX review。

### Input Field

- **When to Use**：未来确有玩家文本输入需求并且有本地化、校验和错误文案合同。
- **When NOT to Use**：玩家只需选择固定值或输入会改变隐藏游戏状态的调试字段。
- **States**：empty、focused、filled、invalid、disabled、submitting。
- **Accessibility**：label、placeholder、错误说明和字符上限可朗读；错误不得只用颜色。
- **Implementation**：当前 P0 暂无生产实例；任何新增输入框必须声明 owner、null、校验和事件。

### Tab Bar

- **When to Use**：同层级分类之间需要快速切换，并且每个 tab 有独立可聚焦内容。
- **When NOT to Use**：分类切换会触发破坏性写入、恢复流程或需要多级导航的内容。
- **States**：unselected、focused、selected、disabled、loading、unavailable。
- **Accessibility**：selected 状态有文字/语义标记；Left/Right 或 Tab 顺序稳定；内容变化不自动抢焦点。
- **Implementation**：Journal 四分类可视为 tab-like category rows，但需遵循 Journal 专用 focus contract。

### Scroll

- **When to Use**：正文、详情或超出 720p 的列表内容。
- **When NOT to Use**：把固定返回/关闭操作放入可滚走区域，或要求滚动才能发现唯一错误信息。
- **States**：top、middle、bottom、focused-content、loading、empty。
- **Accessibility**：PageUp/PageDown 和焦点自动滚入视野；滚动条颜色不是唯一状态。
- **Implementation**：使用 Keyboard Viewport；滚动不触发 rollback、rollforward、activation 或提交。

## Animation Standards

| Context | Default | Reduced Motion | Requirement |
|---|---|---|---|
| Screen enter/exit | 短淡入/淡出或直接切换 | 0 ms 直接到稳定帧 | 首焦点不得等待动画 |
| Focus/pressed | 即时边框/填充变化 | 同样即时 | 不用闪烁或声音表达唯一语义 |
| Loading/pending | 静态文案 | 静态文案 | spinner 不能是唯一证据 |
| Error/recovery | 一次性状态替换 | 0 ms 状态替换 | 不自动 dismiss |
| Cause/reaction | 正常叙事推进 | 0 ms 文本替换 | 不插入评分或奖励动画 |

## Sound Standards

| Context | Default | Muted / Self-Voicing | Requirement |
|---|---|---|---|
| Focus/pressed | 可选轻量 cue | 静音或 self-voicing 时可抑制 | 必须有可见状态 |
| Confirmed | 可选确认 cue | 不影响 action | 不得成为唯一确认依据 |
| Error/recovery | 可选提示音 | 保留静态文本与 transcript | 不自动确认或推进 |
| Causal reaction/payoff | 依赖 approved audio binding | 使用字幕/summary 等价呈现 | 不得泄露内部 ID |
| Journal seen pending | 不使用成功 toast 音 | 静态文案 + 一次 transcript | 完成/失败均可重访 |

## Pattern Gaps

- 需要在逐屏 evidence 中用真实 Ren'Py 渲染冻结 focus ring 的精确像素、文本换行与 self-voicing transcript。
- timed choice 属于 post-MVP `SYS-TENSION`，本轮只要求非限时 Choice Surface；若恢复开发，必须另建 timed-choice spec。
- Ren'Py 8.5.3 shared spike 已通过 focus、Tab/Shift+Tab、viewport 自动滚入、控件读序与 1.5 字体布局；逐屏截图、SAPI 人工听测与语义等价证据仍是下游 gate。
