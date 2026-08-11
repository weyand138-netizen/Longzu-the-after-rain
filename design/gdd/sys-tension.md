# 可选紧张模式

> **Status**: Deferred to post-MVP
> **Author**: Andwey + Codex
> **Last Updated**: 2026-08-05
> **Implements Pillar**: 温柔必须被挣来；悲剧也是完整答案
> **Creative Director Review (CD-GDD-ALIGN)**: Full review completed 2026-08-05 — historical verdict `NEEDS REVISION`; its six GDD blockers were revised and are closed by the targeted closure record below
> **Targeted Closure Re-review**: 2026-08-05 — historical verdict `APPROVED WITH DOWNSTREAM IMPLEMENTATION GATES`; 2026-08-09 scope decision defers the feature to post-MVP, so its remaining implementation gates are not current Production gates

## Overview

SYS-TENSION 是默认关闭的可选紧张模式，在少数经批准的危机场景中为选择加入清晰、可访问且可暂停的时间压力，使玩家在世界信息仍有限、但当前决定所需事实已经完整交付且后果逼近时，感受到犹豫本身也会成为决定。玩家可主动启用或关闭该模式；启用后，主动确认与超时都会解析为预先登记的 canonical choice，并执行相同的提交、即时反应与延迟回收流程。系统始终保留完整的非限时正式路径，不改变选项语义、隐藏状态或结局规则。这里“可追溯”只指已提交的 canonical hesitation choice 及其 reaction/payoff，不记录玩家是主动选择还是自然 timeout。没有本系统，游戏仍保持完整可玩，但会失去这种可选的危机节奏。

### Scope Decision — post-MVP

为最快进入当前 Production，SYS-TENSION 整体延期至 post-MVP。当前 MVP/Production 不创建 `tension_mode_enabled` 持久化设置、不增加 SYS-PERSIST 第六项设置、不创建替代 preference owner，也不要求 SYS-SAVE 为 active timer 提供 phase×action×source 矩阵。以下偏好存储、active-timer recovery、UX、engine、content 与 test 条款保留为 post-MVP 目标合同；它们不阻断当前 P0 Production gate。

## Player Fantasy

玩家启用紧张模式后，应感到危机正在逼近，而自己的沉默、确认与迟疑都具有叙事重量；这种压力来自角色处境和有限决策时间，而不是对阅读速度、记忆、选项位置、输入设备或身体能力的考验。理想时刻是：当前决定摘要已让玩家理解全部相关选项，却仍必须在“替她决定、询问她、回避问题或承担后果”之间迅速面对自己的倾向；如果未能确认，游戏也诚实地提交场景中已登记、可由玩家主动选择的迟疑结果，而非操作失败或即时死亡。叙事追踪该 canonical 结果，不追踪或评价 timeout origin。

系统直接服务“温柔必须被挣来”：善意不能因危机而自动变得正确，快速行动也不等于尊重绘梨衣的自主。同时，它服务“悲剧也是完整答案”：超时造成的迟疑必须获得完整的即时反应、延迟回收与情感闭环。玩家关闭紧张模式时仍获得语义、内容和结局可能性完整等价的正式体验，因此启用该模式代表主动选择更紧迫的节奏，而不是选择更高价值或更“真实”的路线。

> 2026-08-05 full review 中 `creative-director` 批准保留 canonical parity 与 self-voicing pause accommodation，并要求以 narrative eligibility contract、确定性 arbitration、输入等价和可测试 AC 关闭 blockers；本次 targeted closure re-review 已确认这些 GDD 合同关闭。未产出的 engine、ADR、UX、集成、性能和玩家测试证据仍是 downstream implementation gates。

## Detailed Design

### Core Rules

1. **默认关闭且明确自愿（post-MVP）**：post-MVP 的 `tension_mode_enabled` 首次启动默认为 `false`。玩家的选择跨新游戏与应用重启保留，但不属于局内存档、读档或 rollback 状态；该目标不属于当前 MVP 持久化合同，具体存储机制须由未来架构决策确定。
2. **安全状态才能改动**：玩家只能在主菜单或 `PlayableStable` 设置界面启用或关闭紧张模式。已进入限时关键交互后，完整设置入口保持不可用。
3. **场景必须显式登记**：紧张模式只作用于批准清单中的危机场景。每项登记必须唯一声明场景 ID、choice surface、倒计时配置、`timeout_choice_id`、非限时正式版本及可访问提示绑定。
4. **非限时版本是正式内容，等价指语义而非操作面完全相同**：紧张模式关闭时使用同一选项文本、顺序、canonical IDs、reaction、payoff 和 terminal outcome set。Timed 版本只可额外加入倒计时、自动 timeout activation、计时状态输出及本节明确列出的 critical-interaction action gate；不得把 save/load/rollback/history/skip/auto 的暂时不可用描述成两版本操作面完全相同。所有受限操作必须在进入 timed surface 前可预见，并由配对 surface manifest 的 `timed_only_affordance_delta` 精确列出。
5. **迟疑结果仍可主动选择**：每个 `timeout_choice_id` 必须同时是该场景中可由玩家普通确认的 canonical choice，表达符合场景语境的沉默、犹豫或未能决定。关闭紧张模式后，该结果仍能通过普通输入到达。
6. **超时不是即时死亡**：timeout 不得仅因计时归零直接杀死角色、跳至结局或修改 ending predicate；它可以像其他选择一样通过已登记的后续因果产生严重结果。
7. **集成前置验证**：场景缺少非限时版本、canonical timeout choice、reaction/payoff coverage、可访问剩余时间或唯一登记时，内容冻结失败。发行运行时若仍检测到无效数据，则无语义写入地退回非限时 surface。
8. **稳定且信息完整后才计时**：选项文本、顺序、焦点、可访问描述、剩余时间通道与当前决定所需的全部事实全部建立后，倒计时才可开始。若所需事实来自先前正文，timed surface 必须提供不泄露隐藏状态的只读“当前决定摘要”，并把该摘要计入 `C`；不得要求玩家依靠已被 gate 的 history/backlog 回忆关键信息。Self-voicing 正在进行初次朗读时保持暂停。
9. **暂停不重置**：Self-voicing 朗读限时提示、允许的无障碍输出快捷操作、窗口失焦、应用不可见或批准的系统级中断期间，剩余时间保持不变；恢复稳定焦点后从原值继续。
10. **普通决策时间继续流逝，但输入位置不得制造劣势**：玩家阅读、思考、移动鼠标或进行普通键盘焦点导航时，倒计时继续。每个 timed surface 只能包含 `2–4` 个同时完整可见的选项，并提供 `1–4` 数字键直接 activation；普通焦点导航与数字键、鼠标必须进入同一解析队列。输入设备只改变 activation 方式，不改变剩余时间、选项语义或结果；全部 choice position × input device 必须通过最坏路径 activation 预算。
11. **剩余时间不得单通道表达**：运行与暂停状态必须同时提供可读文字和非颜色独占的视觉状态；声音、闪烁、震动或动画只能作为附加反馈。
12. **唯一解析闩锁**：玩家确认与计时归零竞争时，只允许一个结果取得解析权。取得闩锁后立即停止计时、锁定重复输入，并忽略后续 activation；同帧边界的精确裁决由 Formulas 与 Edge Cases 冻结。
13. **统一选择提交并区分 activation origin**：普通确认把对应 canonical choice 交给 SYS-CHOICE；timeout 把已登记的 `timeout_choice_id` 交给同一入口。两者均执行 `resolution_acceptance → history commit → immediate reaction → later control flow`。`activation_origin=manual|timeout` 只用于本次 arbitration 与测试 trace，进入 SYS-CHOICE 前移除，不进入 history、reaction、payoff、save、persistent 或 ending predicate。
14. **关键交互操作门槛**：限时 surface 活动期间，完整设置、存档、读档、rollback、skip、auto 和其他会转移叙事控制的操作不可见或 disabled/unfocusable。被拒绝的快捷操作不得消耗额外时间。
15. **没有旁路语义状态**：SYS-TENSION 不直接写五轴、choice history、counterevidence、路线资格、结局状态或匿名 `hesitated` flag，也不维护独立 reaction/payoff ledger。
16. **不进行能力评分**：系统不得根据阅读速度、输入速度、历史 timeout 次数、路线表现或无障碍模式动态缩短时间、重排选项、推荐答案或改变因果价值。
17. **不提供限时独占奖励**：紧张模式不得解锁独占剧情、成就、结局、数值优势或“真实模式”标识；它只改变自愿选择的危机节奏及 timeout 的自动 activation。
18. **恢复从选择前安全点开始**：应用异常退出或外部恢复不能序列化并继续一个活动倒计时。重新进入该内容时从批准的选择前控制位置重新建立 surface，并使用完整初始时间；不得自动提交 timeout。
19. **不记录行为遥测**：timeout、暂停次数与决策耗时只可存在于本地测试证据中，不得进入发行版遥测、玩家评分或跨周目画像。
20. **完整复核门槛（post-MVP）**：本节历史上完成 game design、narrative、systems、UX、无障碍、QA、engine、performance、audio 与 creative-direction 的 full review及独立 targeted closure re-review，当前 `unresolved_blocking_findings=()`。未通过的 engine spike、未批准的 SYS-TENSION ADR 或 Q1–Q11 对应实现期证据只阻止 post-MVP implementation/content/UI/release gate；它们不属于当前 P0 Production gate。

### Timed-Scene Narrative Eligibility

结构合法并不自动代表场景适合限时。每个 production timed scene 必须额外提交唯一 `tension_narrative_eligibility_record`：

`scene_id, diegetic_deadline_id, decision_context_summary_id, decision_information_complete, agency_answer_state, agency_answer_determined_or_not_applicable, timeout_causal_bridge_id, min_intervening_narrative_event_count, next_player_choice_id, reviewer_ids, source_hash`

其中 `agency_answer_state` 是 exact string：agency transaction 必须解析到 SYS-NARRATIVE 已登记且不等于 `undetermined`/`not_applicable` 的 `answer_state_id`；非 agency transaction 必须 exact-equal `not_applicable`。`agency_answer_determined_or_not_applicable` 是由 validator 计算、不得由作者自由填写的 exact bool：

`agency_answer_determined_or_not_applicable = (is_agency_transaction ∧ registered_answer_state ∧ agency_answer_state ∉ {undetermined, not_applicable}) ∨ (¬is_agency_transaction ∧ agency_answer_state = not_applicable)`

只有该值为 `true` 才合法。`reviewer_ids` 必须是恰含两个不同 canonical person identities 的 exact tuple，角色分别为 Narrative Director 与 Creative Director；两者都必须对同一 `source_hash` 签署，且不得由 alias 伪装为不同人员。`source_hash` 是覆盖 scene declaration、配对 surfaces、decision summary、answer state、causal bridge 与 continuation witness 的 lowercase 64-hex SHA-256；任一被覆盖输入变化都会使旧 review record stale。

只有以下条件全部成立才允许进入 `Validating`：

- `diegetic_deadline_id` 解析到场景内可感知、与 UI 无关的时间压力来源；纯粹为了增加难度的任意倒计时不合格。
- `decision_information_complete=true`，且 `decision_context_summary_id` 覆盖当前选择所需的全部已知事实；摘要不得泄露隐藏轴、token、qualification、未来结果或绘梨衣未表达的内心。
- 若场景属于 request/answer/response transaction，`agency_answer_state` 必须解析到已登记且非 `undetermined`/`not_applicable` 的 answer；answer 尚未形成、仍含混或正在表达时不得启动倒计时。非 agency transaction 必须显式使用 `not_applicable`，并由上述派生式证明 `agency_answer_determined_or_not_applicable=true`。
- `timeout_causal_bridge_id` 必须把 canonical hesitation choice 的即时反应连接到严格较晚 payoff；不得为 timeout 新建语义状态、特殊反应或 ending shortcut。
- `min_intervening_narrative_event_count ≥ 1`：resolution 后至少完成一个不可交互、可感知且 source-bound 的 reaction/bridge event，才可出现下一项玩家选择；该要求不规定固定毫秒停顿。
- Day 6 route commitment、Day 7 ending entry、单项强制 acknowledgement、直接 terminal control transfer，以及会把沉默误读为同意的节点默认无 timed eligibility；例外必须由 Narrative Director 与 Creative Director 双签并提供独立 agency/silence review。

Validator 使用以下完整、无短路豁免的 exact bool；所有 conjunct 都必须来自同一 `source_hash` 覆盖的 immutable records：

`tension_narrative_eligibility_valid = unique_record ∧ diegetic_deadline_valid ∧ decision_information_complete ∧ decision_context_summary_valid ∧ agency_answer_determined_or_not_applicable ∧ timeout_causal_bridge_valid ∧ min_intervening_narrative_event_count≥1 ∧ next_player_choice_valid ∧ terminal_policy_valid ∧ reviewer_pair_valid ∧ source_hash_current`

任一字段缺失、wrong type、unknown reference、重复 raw record、reviewer identity/role 不合法或 stale hash 都返回 exact `false`；不得以默认值补全或把失败降级为人工 warning。

第一个 production timed scene 冻结前，必须先用 test-only example manifest 证明上述字段、配对 surface、context summary、canonical timeout choice 与 later payoff 能完整 join；test-only example 不进入 production catalog，也不创建第二份叙事权威。

#### Test-Only Example Manifest

以下记录只定义 validator fixture 形状，不是 production 场景、正式文案或新增叙事选择：

| Field | Test-only valid value | Required proof |
|---|---|---|
| `scene_id` | `test_tension_departure_example` | production source exclusion exact-match test manifest |
| Surface pair | `test_timed_departure` / `test_untimed_departure` | 两者 choice tuple、文本、普通导航、初始焦点与 causal projection exact-match |
| Choice tuple | `test_depart_now`, `test_wait_without_answer` | 两项均有 test-only canonical records；第二项是可主动确认的 `timeout_choice_id` |
| `diegetic_deadline_id` | `test_train_door_closure` | 玩家可感知的场景事件，不由 timer UI 自身创造 |
| `decision_context_summary_id` | `test_departure_decision_summary` | 覆盖车门即将关闭、当前已知路线与两项行动含义；`C` 计入其文字 |
| Agency state | `agency_answer_state=not_applicable`、派生 bool=`true` | fixture 不属于 Erii request/answer transaction；将 state 翻转为 `undetermined`、把派生结果伪造为作者字段或使两者不一致都必须失败 |
| `timeout_causal_bridge_id` | `test_wait_reaction_bridge` | timeout 与主动选择 `test_wait_without_answer` 使用同一 reaction/payoff joins |
| Next agency distance | `min_intervening_narrative_event_count=1` | reaction bridge 完成后才出现 `test_next_player_choice` |
| Accessibility/input | readable text=`true`、non-color visual=`true`、`N=2`、direct keys=`1/2` | 移除任一 mandatory channel 或 direct binding 的 one-defect fixture 必须失败 |

该 fixture 的 `source_hash`、review records、positive join report 与逐字段 one-defect negatives 属于 SYS-TEST；任何 production scanner 发现上述 `test_*` ID 均必须构建失败。

### States and Transitions

| State | Meaning | Allowed transitions |
|---|---|---|
| `Disabled` | 模式关闭或场景不在批准清单中 | 直接建立普通非限时 surface；不生成计时状态 |
| `Validating` | 模式开启，正在验证场景登记与跨系统绑定 | 合法 → `Presenting`；不合法 → `FallbackUntimed` |
| `Presenting` | 限时 surface 已出现，但决定摘要、可访问内容或稳定焦点尚未就绪；timer 尚未开始 | 全部就绪且无暂停原因 → 记录唯一 `t₀` 并进入 `Running`；暂停原因存在 → 保持 `Presenting` 且 `timer_started=false`；验证失效 → `FallbackUntimed` |
| `Running` | 倒计时正在消耗，玩家可确认选择 | 玩家确认 → `ResolvingConfirmed`；时间归零 → `ResolvingTimeout`；暂停原因出现 → `Paused` |
| `Paused` | 只可从 `Running` 进入；`t₀` 已存在，剩余时间冻结，当前语义 surface 与焦点身份保留 | 暂停原因全部解除且焦点稳定 → `Running`；数据失效 → `FallbackUntimed` |
| `ResolvingConfirmed` | 玩家 activation 已取得唯一解析闩锁 | canonical choice 接受提交 → `HandedOff`；提交失败 → 阻断式安全流程 |
| `ResolvingTimeout` | timeout activation 已取得唯一解析闩锁 | `timeout_choice_id` 接受提交 → `HandedOff`；提交失败 → 阻断式安全流程 |
| `HandedOff` | SYS-CHOICE 已接管 commit、reaction 与后续流程 | reaction 建立后关闭 SYS-TENSION surface → `Closed` |
| `FallbackUntimed` | 限时合同不可安全成立且尚无语义写入 | 建立配对的普通非限时 surface → `Closed`；记录本地诊断 |
| `Closed` | 当前 choice surface 已结束 | 下一个批准场景可重新进入 `Disabled` 或 `Validating` |

补充转换约束：

- `Running` 与 `Paused` 之间的转换不能改变选项、顺序、焦点语义 ID 或剩余时间之外的任何状态。
- `Paused` 必须满足 `timer_started=true` 且存在唯一 `t₀`；计时开始前的暂停原因只能让状态保持 `Presenting`，不得伪造 pause interval 或 `active_elapsed` 边界。
- `ResolvingConfirmed` 与 `ResolvingTimeout` 互斥；任一状态建立后，另一转换的执行次数必须为零。
- `FallbackUntimed` 只能发生在 choice commit 前；commit 后的错误必须进入既有阻断式安全流程，不能换成另一项选择。
- `HandedOff` 后 SYS-TENSION 不再控制 reaction、payoff、save/load 或 rollback。

### Interactions with Other Systems

| System | Input to SYS-TENSION | SYS-TENSION output / boundary |
|---|---|---|
| SYS-CHOICE | Canonical choice records、presentation states、唯一提交顺序与 coverage validators | 普通或 timeout activation；不改写 choice record，不建立第二提交入口 |
| SYS-NARRATIVE | 批准的危机场景、选项文本、场景语境中的迟疑选择、reaction/payoff 内容 | 计时表现和 timeout activation；不创作匿名结果或改变情节分支 |
| SYS-ACCESS | 安全设置入口、稳定焦点、self-voicing 状态、可访问文本与多通道表现要求 | 模式值、运行/暂停/剩余时间状态；不生成可访问内容或语义选择 |
| SYS-STATE | 唯一合法 choice commit 所需的 rollback-owned 状态入口，由 SYS-CHOICE 间接调用 | 无直接写入；不得读取隐藏轴以调整时间 |
| SYS-SAVE | Critical-interaction action gate 与选择前恢复位置 | 活动期间禁止存读档和 rollback；不序列化活动计时器 |
| SYS-ENDING | 已冻结的结局 predicate 与 lifecycle 边界 | 无直接接口；timeout 只能通过普通 choice 因果间接影响结局 |
| Ren’Py 8.5.3 | Screen interaction、焦点、应用可见性、时间与 preference 能力 | 只消费批准能力；精确计时、暂停和存储方式须通过 engine spike 与 ADR 冻结 |
| SYS-TEST | 版本化场景、输入、暂停、竞争与恢复 fixtures | 输出状态转换、剩余时间、唯一 dispatch 和无旁路语义证据 |
| UX specification | 倒计时布局、暂停说明、最大字体与焦点图 | 必须满足本 GDD 的时间可读性、输入等价及非限时路径要求 |

## Formulas

所有数值均为 full review 后仍保留的暂定设计假设；合法范围已证明 finite/non-degenerate，但必须经 Ren’Py crisis-scene spike、危机场景 prototype、人工无障碍复核和 playtest 后才能锁定。

### Initial Countdown Duration

The `tension_initial_duration` formula is defined as:

`D = clamp((B + C / V + K × N) × P, D_min, D_max)`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Base decision time | `B` | float seconds | `6–12`; target `8` | 与文本长度无关的基础思考时间 |
| Readable character count | `C` | int | `1–120` | 当前 choice surface 新呈现的决策关键简体中文字符数，包括当前决定摘要、指示文字和所有选项；不重复计算 markup 或 alt 副本。未在 surface 摘要中重现的既有正文不能被视为已计时补偿 |
| Reading-rate baseline | `V` | float chars/second | `4–6`; target `5` | 用于分配阅读时间的项目基线；不得按玩家动态改变 |
| Per-option comparison time | `K` | float seconds | `1–2.5`; target `1.5` | 每个可确认选项的比较与焦点移动预算 |
| Option count | `N` | int | `2–4` | 当前限时 surface 中同时完整可见、可用普通导航或 `1–4` 数字键确认的 canonical choices 数量 |
| Pressure factor | `P` | exact float enum | `0.90, 1.00, 1.10` | 急迫、标准、缓和三个作者配置档位；不得根据玩家表现动态改变 |
| Minimum duration | `D_min` | float seconds | `15–24`; target `18` | 初始时长下限 |
| Maximum duration | `D_max` | float seconds | `32–50`; target `40` | 初始时长上限 |
| Initial duration | `D` | float seconds | `D_min–D_max` | 本次进入 choice surface 的完整初始时间 |

**Output Range:** 目标配置为 `18` 至 `40` 秒；任一批准配置的绝对安全边界为 `15` 至 `50` 秒。计算结果低于或高于当前配置范围时分别钳制到 `D_min` 或 `D_max`。`C` 或 `N` 超出允许范围时不能靠钳制继续，场景失去限时资格并退回非限时版本。

**Example:** 目标配置 `B=8`、`V=5`、`K=1.5`、`D_min=18`、`D_max=40` 下，`C=60`、`N=3`、`P=1.00` 时，`D=(8+12+4.5)×1=24.5` 秒。

### Effective Paused Duration

The `tension_effective_paused_duration` formula is defined as:

`P_t = measure(union([s_i, min(e_i, t)] for each approved pause interval i))`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Pause start | `s_i` | float seconds | `t₀–t` | 第 `i` 个批准暂停原因开始的单调时间戳 |
| Pause end | `e_i` | float seconds | `s_i–t` | 暂停原因结束时间；尚未结束时使用当前时间 `t` |
| Current time | `t` | float seconds | `≥t₀` | 当前单调时间戳 |
| Effective paused duration | `P_t` | float seconds | `0–(t−t₀)` | 所有暂停区间并集的长度 |

**Output Range:** `0` 至当前原始经过时间。多个同时存在的暂停原因只计算一次，不得重复增加剩余时间。

**Preconditions:** 所有时间戳必须是同一批准单调时钟产生的 finite exact numeric values；每个 interval 必须满足 `t₀ ≤ s_i ≤ min(e_i,t) ≤ t`，开放 interval 以显式 `end=None` 表示并在 snapshot 中临时取 `t`。倒置、越界、重复 identity、NaN、Infinity、wrong type 或 `P_t > t-t₀` 一律返回 validation failure；不得依靠后续 `clamp` 把损坏输入变成合法剩余时间。

**Example:** Self-voicing 在 `5–9` 秒暂停，窗口失焦在 `7–12` 秒暂停，并集为 `5–12`，因此 `P_t=7` 秒，而不是 `4+5=9` 秒。

### Remaining Time

The `tension_remaining_time` formula is defined as:

`R(t) = clamp(D - ((t - t₀) - P_t), 0, D)`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Initial duration | `D` | float seconds | `15–50` | `tension_initial_duration` 在批准配置下的输出 |
| Timer start | `t₀` | float seconds | monotonic timestamp | `Presenting → Running` 时记录的起点 |
| Current time | `t` | float seconds | `≥t₀` | 当前单调时间戳 |
| Effective paused duration | `P_t` | float seconds | `0–(t−t₀)` | 暂停区间并集长度 |
| Remaining time | `R` | float seconds | `0–D` | 当前可消费的剩余时间 |

**Output Range:** `0` 至 `D`。处于 `Paused` 时输出保持不变；达到 `0` 后不得再次增加或恢复 `Running`。

`R(t)` 只在 `D`、`t₀`、`t` 与 pause intervals 全部通过前置验证后计算。`t<t₀`、`P_t<0` 或 `P_t>t-t₀` 是 validation failure，不得被钳制为 `D`。

**Example:** `D=24.5`、原始经过 `10` 秒、有效暂停 `3` 秒时，`R=24.5−(10−3)=17.5` 秒。

### Warning Phase

The `tension_warning_phase` formula is defined as:

`Q = R / D`

`phase(Q) = stable if U < Q ≤ 1; urgent if H < Q ≤ U; critical if 0 < Q ≤ H; expired if Q = 0`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Remaining time | `R` | float seconds | `0–D` | 当前剩余时间 |
| Initial duration | `D` | float seconds | `15–50` | 本次初始时间 |
| Remaining ratio | `Q` | float | `0–1` | 剩余时间占比 |
| Urgent threshold | `U` | float ratio | `0.40–0.60`; target `0.50` | `stable` 与 `urgent` 的边界 |
| Critical threshold | `H` | float ratio | `0.15–0.25`; target `0.20` | `urgent` 与 `critical` 的边界；必须满足 `H < U` |
| Warning phase | `phase` | enum | `stable/urgent/critical/expired` | 只控制提示强度和状态文案 |

**Output Range:** 四个有限枚举值。阶段变化不得改变选项、焦点、时间速度、语义结果或输入可用性。

**Example:** `D=24.5`、`R=4` 时，`Q≈0.163`，输出 `critical`。

### Confirmation and Timeout Resolution

The `tension_resolution` formula consumes one immutable `tension_arbitration_snapshot`:

`S = (surface_id, t₀, snapshot_time, D, validated_pause_intervals, state_events, activation_events, latch_open)`

`active_elapsed(x) = (x - t₀) - paused_union_length_at(x)`

`eligible_activations = sort((t_received, receive_seq, choice_id) where activation_valid ∧ state_at_receipt=Running ∧ t₀ ≤ t_received ≤ snapshot_time ∧ active_elapsed(t_received) ≤ D)`

`resolved_choice_id = first(eligible_activations).choice_id if latch_open ∧ eligible_activations≠(); timeout_choice_id if latch_open ∧ state_after_events=Running ∧ active_elapsed(snapshot_time) ≥ D; unresolved otherwise`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Resolution latch | `latch_open` | exact bool | `false/true` | 当前 surface 是否尚未产生结果 |
| Activation validity | `activation_valid` | exact bool | `false/true` | activation 是否解析到当前可用 canonical choice |
| Snapshot time | `snapshot_time` | float seconds | monotonic timestamp | 本次 arbitration snapshot 的唯一当前时间；公式内不得再次读取时钟 |
| Activation events | — | exact tuple | zero or more exact records | 每项包含 `t_received`、稳定 `receive_seq`、`choice_id`、`activation_valid` 与 `state_at_receipt` |
| State events | — | exact tuple | zero or more exact records | 同一时钟域内的 pause start/end、focus-ready 与 visibility 事件 |
| Confirmed choice | `confirmed_choice_id` | exact string | registered ID | `first(eligible_activations).choice_id` 派生的 canonical choice |
| Timeout choice | `timeout_choice_id` | exact string | registered ID | 场景预登记的迟疑选择 |
| Resolved choice | `resolved_choice_id` | enum/string | `unresolved` 或两个注册 ID 之一 | 交给 SYS-CHOICE 的唯一结果 |

**Output Range:** `unresolved`、最早合法 activation 的 canonical choice ID 或唯一 `timeout_choice_id`。取得结果与关闭 latch 是同一原子状态转换；后续输入和 timeout dispatch 数均为零。`activation_origin=manual|timeout` 只存在于本次 arbitration trace 与本地测试证据中，交给 SYS-CHOICE 的 payload 只含 canonical choice，不持久化 origin，也不改变 reaction/payoff。

**Stable event order:** 所有事件先按 `timestamp`、再按以下 kind priority、最后按 `receive_seq` 排序：pause/focus/visibility state update → activation → timeout observation。同刻 pause 状态先建立；若该时刻仍为 `Running`，合法 activation 在 timeout 前获胜；若 pause 已建立，activation 不合格。Pause end 与 activation 同刻时先恢复稳定焦点，只有恢复成功才允许 activation。多个合法 activation 使用最早 `t_received`，同刻使用最小 `receive_seq`。任何 `t_received<t₀`、`t_received>snapshot_time`、非 finite 时间、重复 receive sequence 或无法证明 `state_at_receipt` 的记录均使 pre-latch arbitration validation failure。

`resume_activation_intent` 只能在 self-voicing pause 建立时的冻结 `R_pause>0`（等价于 `active_elapsed_at_pause<D`）时创建。若 pause 在 `R_pause=0` 建立，则 Paused 中的全部 activation 均不得创建 intent；恢复后的首个合法 snapshot 必须先解析唯一 timeout。该 deadline-zero guard 高于“恢复 Running 后 activation 先于 timeout observation”的普通顺序，避免一个在时间已到后产生的 Paused intent 被重新时间戳为合法确认。

**Example:** 无同刻 pause 时，合法 activation 的 `active_elapsed=D`，玩家确认获胜；`active_elapsed>D` 时它不进入 eligible set，timeout choice 获胜。若 pause start 与该 activation 同刻，pause 先建立，activation 不合格，恢复后在 `active_elapsed≥D` 的首个合法 snapshot 解析 timeout。

### Timed-Scene Manifest Validity

The `tension_scene_manifest_valid` formula is defined as:

`tension_scene_manifest_valid = unique_scene ∧ exact_surface_pair ∧ same_choice_sequence ∧ same_initial_focus_rule ∧ same_navigation_semantics ∧ same_causal_projection ∧ declared_affordance_delta ∧ registered_timeout ∧ timeout_manual_reachable ∧ reaction_payoff_covered ∧ readable_time_text_ready ∧ noncolor_visual_time_state_ready ∧ stable_focus_bound ∧ direct_keyboard_activation_bound ∧ narrative_eligibility_valid ∧ duration_inputs_valid`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Unique scene declaration | `unique_scene` | exact bool | `false/true` | scene ID 恰有一项 raw declaration |
| Surface pairing | `exact_surface_pair` | exact bool | `false/true` | 恰有一个 timed 与一个正式 non-timed surface |
| Semantic sequence equality | `same_choice_sequence` | exact bool | `false/true` | 两个 surface 的 choice IDs、文本和顺序完全一致 |
| Initial focus equality | `same_initial_focus_rule` | exact bool | `false/true` | 两个 surface 使用相同 canonical 初始焦点规则 |
| Navigation semantics | `same_navigation_semantics` | exact bool | `false/true` | 普通键鼠导航解析到相同 canonical choices；timed-only 数字键只提供等价 direct activation |
| Causal projection | `same_causal_projection` | exact bool | `false/true` | reaction、payoff、qualification effects 与 terminal outcome set exact-match |
| Declared affordance delta | `declared_affordance_delta` | exact bool | `false/true` | timed-only countdown、提示与 action-gate 差异完整列入批准 allowlist |
| Registered timeout | `registered_timeout` | exact bool | `false/true` | timeout ID 解析到该 surface 的 canonical choice |
| Manual reachability | `timeout_manual_reachable` | exact bool | `false/true` | 非限时版本可通过普通 activation 到达同一 choice |
| Causal coverage | `reaction_payoff_covered` | exact bool | `false/true` | timeout choice 满足 SYS-CHOICE 的 reaction/payoff 合同 |
| Readable time text | `readable_time_text_ready` | exact bool | `false/true` | 每个运行/暂停状态都有可读文字 |
| Non-color visual state | `noncolor_visual_time_state_ready` | exact bool | `false/true` | 每个运行/暂停状态都有不依赖颜色的形状、轮廓或纹理标识 |
| Stable focus binding | `stable_focus_bound` | exact bool | `false/true` | 初始及暂停恢复焦点均有稳定语义 ID |
| Direct keyboard activation | `direct_keyboard_activation_bound` | exact bool | `false/true` | `N≤4` 且 `1–N` direct activation 与普通导航/鼠标 exact-map 到相同 choices |
| Narrative eligibility | `narrative_eligibility_valid` | exact bool | `false/true` | 唯一 narrative eligibility record 通过全部 diegetic、information、agency 与 causal-bridge gates |
| Duration inputs | `duration_inputs_valid` | exact bool | `false/true` | `B`、`V`、`K`、`C`、`N`、`P`、`D_min` 与 `D_max` 均在批准范围内且 `D_min < D_max` |

**Output Range:** exact bool。输出 `false` 时禁止进入 `Running`；构建期失败，运行时只能无语义写入地退回非限时 surface。

**Example:** 其他字段全部合法，但只提供可读文字与音频、缺少非颜色视觉状态，则输出 `false`；音频通道不参与 mandatory validity。

> 2026-08-05 `systems-designer`/engine adversarial review 已完成公式边界审计；合法数值无 division-by-zero 或非有限输出。Targeted closure re-review 已关闭 event-order 与 deadline-zero 设计歧义；Ren’Py 8.5.3 spike 仍须证明运行时 capability，属于 downstream implementation gate。

## Edge Cases

- **If `tension_mode_enabled` 缺失、类型错误或无法读取**：本次启动将其有效值视为 `false`，不自动写回修复值；所有场景使用非限时正式版本并记录本地诊断。
- **If 模式开启但场景不在批准清单中**：直接建立非限时 surface，countdown、timeout presentation 和 timeout dispatch 数均为零。
- **If 同一 scene ID 存在零项或多项 raw declaration**：构建期失败；发行运行时若仍遇到该情况，在解析闩锁建立前退回非限时版本。
- **If timed/non-timed surface 的选项 ID、文本或顺序不完全一致**：该场景失去限时资格；不得在运行时猜测等价关系。
- **If `timeout_choice_id` 未登记、不是当前 surface 的 choice，或不能在非限时版本中主动到达**：构建期失败；运行时不启动计时。
- **If timeout choice 缺少 reaction、payoff 或完整 continuation coverage**：内容冻结失败；不得以匿名“迟疑”状态代替。
- **If `C`、`N` 或 `P` 超出公式允许范围**：`duration_inputs_valid=false`，不使用钳制后的时长继续；场景退回非限时版本。
- **If 时长计算产生 NaN、Infinity、负值或非 exact numeric input**：不进入 `Running`；保留相同选项并退回非限时版本。
- **If pause interval 倒置、越过 `t₀/t`、包含非 finite 时间、重复 identity，或计算出 `P_t>t-t₀`**：arbitration validation failure；latch 前退回非限时版本，latch 后进入阻断式安全流程，不得依靠 `clamp` 继续。
- **If 暂停原因在计时开始前出现**：保持完整初始时间，直到可访问内容交付完成、暂停原因解除且稳定焦点恢复后才进入 `Running`。
- **If 多个暂停原因相互重叠**：只计算暂停区间并集；任一原因仍活动时保持 `Paused`，不得因另一原因结束而提前恢复。
- **If 暂停无限持续**：保持剩余时间与选项不变，不自动 timeout、不隐藏选项，也不因“滥用暂停”施加惩罚。
- **If self-voicing 初始化或朗读失败，导致提示无法完整交付或焦点无法稳定恢复**：当前场景退回非限时版本，并按 SYS-ACCESS 的能力失败流程提示；不得在未完成可访问交付时恢复计时。
- **If 玩家反复移动焦点并触发 self-voicing**：每次实际朗读期间暂停，朗读结束且焦点稳定后继续；允许因此延长决策时间，不记录能力评分。
- **If 窗口失焦、最小化或应用不可见**：立即进入 `Paused`；重新获得焦点后先恢复同一 stable semantic focus ID，再继续原剩余时间。
- **If 批准的暂停事件与 `active_elapsed=D` 使用相同时间戳**：按稳定 event order 先登记暂停状态，再处理 activation 与 timeout；若剩余时间已精确为零，则保持 `Paused`，并在恢复后的首个合法 snapshot 进入 timeout resolution，不重新增加时间。
- **If 合法 activation 的 `active_elapsed` 等于 `D`，且同刻 state updates 后仍为 `Running`**：玩家确认获胜，关闭解析闩锁，timeout dispatch 数为零。
- **If activation 的 `active_elapsed` 晚于 `D`，即使其事件先于 timeout callback 被处理**：它不进入 eligible set，timeout choice 获胜；不得依赖帧内 callback 顺序。
- **If 两个或更多合法 activation 在 `active_elapsed≤D` 时到达**：最早 `t_received` 获胜；时间戳相同时使用输入系统分配的稳定 `receive_seq`，只有第一项取得闩锁。
- **If activation 在 self-voicing 导致的 `Paused` 中到达且该 pause 的冻结 `R_pause>0`**：第一个合法鼠标、普通确认键或 `1–N` direct activation 只建立一个 transient `resume_activation_intent` 并停止当前朗读；重复 intent 被明确拒绝且不替换第一项。焦点稳定恢复后，先进入 `Running`，再在同一 snapshot 生成对应 canonical activation，最后处理 timeout observation。若朗读或焦点恢复失败并进入 fallback，则清除 intent、semantic write count 为零。
- **If activation 在 self-voicing 导致的 `Paused` 中到达且该 pause 的冻结 `R_pause=0`**：不得建立或保留 `resume_activation_intent`；恢复稳定焦点后的首个合法 snapshot 直接取得 timeout latch，manual dispatch count 为零。
- **If activation 在失焦、不可见或系统级中断导致的 `Paused` 中到达**：不得建立 intent 或 activation；恢复后用可访问状态文案说明输入未执行。窗口不可见时不要求音频反馈。
- **If activation 指向 disabled、unfocusable、隐藏或非当前 surface 的 choice**：忽略该 activation；它不能关闭闩锁或改变 active elapsed。
- **If 帧卡顿使下一次 update 跨过 `active_elapsed=D`**：使用 immutable snapshot 和已记录的 input receipt timestamp 裁决；在 `active_elapsed≤D` 时已接收且当时为 `Running` 的合法输入仍获胜，否则恰提交一次 timeout choice。
- **If 单调时钟倒退、跳变为非有限值或失去版本承诺**：解析闩锁建立前冻结计时并退回非限时版本；闩锁建立后则进入阻断式安全流程，不改选。
- **If 玩家在限时 surface 使用设置、存档、读档、rollback、skip、auto 或其他受禁操作**：action dispatch 与控制转移数均为零；处理该拒绝操作的区间不消耗倒计时，随后恢复原焦点。
- **If 外部或测试代码在活动 surface 中改写模式偏好**：当前 surface 使用进入时捕获的有效模式，不中途改变；新值只影响下一场景，并记录 reentrant-contract 诊断。
- **If 应用在 `Presenting`、`Running` 或 `Paused` 中退出或崩溃**：不保存活动计时器、解析闩锁或暂停区间；下次恢复从批准的选择前位置重新建立完整初始时间。
- **If 玩家试图通过 rollback 回到活动限时 surface**：限时期间 rollback action 保持禁用；从更早合法控制位置重新进入时视为新 surface，重新验证并使用完整初始时间。
- **If 普通确认或 timeout 已取得解析闩锁，而 SYS-CHOICE 提交抛出异常**：进入既有阻断式安全流程；不得重新开放选项、改交另一 choice 或删除已形成的诊断事实。
- **If SYS-CHOICE 对 production 可达提交返回 `DUPLICATE_NOOP`**：reaction dispatch 数为零并 fail closed；不得把 duplicate 当作已成功处理。
- **If reaction 在 `APPLIED` 后失败**：不补偿删除 history、不恢复倒计时、不重新选择；保留 rollback 恢复能力并停止后续控制流。
- **If timeout、暂停或决策耗时被发行代码用于成就、难度、路线推荐或跨周目画像**：构建失败；这些观测只允许存在于本地测试证据。
- **If 玩家反复失焦或使用批准暂停机制延长时间**：按规则正常暂停，不降低奖励、不缩短后续场景时间，也不标记作弊；紧张模式是自愿节奏层，不是能力测验。

> 2026-08-05 `systems-designer`/engine/QA adversarial review 已纳入；targeted closure re-review 已确认计时竞争、恢复、pause interval 与无障碍 activation 的 GDD 规则无未决歧义。Engine spike 与自动化证据仍是 downstream implementation gates。

## Dependencies

| Dependency | Strength / Direction | Required contract | Current status / gate |
|---|---|---|---|
| Game Concept | Hard design → SYS-TENSION | 默认关闭、超时视为迟疑、无障碍不可削减、非限时内容完整 | Approved |
| Ren’Py 8.5.3 | Hard runtime → SYS-TENSION | 单调计时、screen interaction、稳定输入时间戳、焦点、应用可见性和 preference 行为 | Pinned；组合行为必须通过 crisis-scene spike |
| SYS-CHOICE | Hard semantic / SYS-TENSION → SYS-CHOICE | Canonical choice records、`timeout` presentation state、唯一解析与提交顺序、reaction/payoff coverage | Approved with provisional downstream gates |
| SYS-NARRATIVE | Hard content / bidirectional | 危机场景登记、相同 timed/non-timed choice sequence、场景语境中的迟疑选项及完整因果内容 | In Revision；具体 timed scenes 尚未登记 |
| SYS-ACCESS | Hard input/presentation / bidirectional | 安全设置入口、stable semantic focus、self-voicing pause、剩余时间多通道表达及非限时入口 | Designed；完整复审、engine spike 与 UX evidence pending |
| SYS-SAVE | Post-MVP integration / bidirectional | 限时关键交互 action gate、选择前合法恢复位置、活动计时器不序列化 | Deferred；不属于当前 P0 Production gate |
| SYS-TEST | Post-MVP verification / observe SYS-TENSION | Manifest、绝对时间、暂停区间、竞争输入、dispatch、恢复及负面 fixtures | Deferred；不属于当前 P0 Production gate |
| Timed-choice UX specification | Hard pre-implementation | 1280×720 与字体 `1.5` 布局、倒计时文案、阶段状态、焦点图、self-voicing 读序和暂停说明 | Not Started |
| SYS-STATE | Explicit semantic boundary / no direct flow | 只能经 SYS-CHOICE 的合法 commit 接收 canonical choice | Approved；SYS-TENSION 不读写 axes/history |
| SYS-ENDING | Explicit outcome boundary / no direct flow | 只消费已提交 choice 形成的冻结因果，不接受 timer 或 pause 输入 | Approved with provisional downstream gates |
| SYS-PERSIST | Explicit storage boundary | 当前 12-leaf/5-setting root 不含 tension preference；不得加入第六项设置 | Deferred；post-MVP 必须另行批准 owner/path，当前不改 persistence contract |
| SYS-ACHIEVE | Explicit downstream boundary | 不得以 timeout、反应时间、暂停次数或模式状态定义成就 | Approved；无直接接口 |
| SYS-AUDIO | Soft presentation / SYS-TENSION → SYS-AUDIO | 可选阶段提示音、暂停/恢复反馈；静音时信息和操作完整保留 | Not Started |
| Art Bible | Soft visual direction | 稳定、急迫、临界、暂停和 expired 状态的非颜色单通道视觉语言 | Not Started；不得阻止占位实现与静态可玩性 |
| New SYS-TENSION ADR | Post-MVP architecture gate | 冻结计时来源、输入时间戳、同刻优先级、暂停检测、偏好存储及异常恢复实现边界 | Deferred；不阻断当前 Production |

### Interface Ownership

- SYS-TENSION 独占模式启用语义、场景计时状态、暂停区间、arbitration snapshot/event order 和 timeout activation。
- SYS-CHOICE 独占 canonical choice schema、choice catalog、commit、reaction/payoff joins 和后续控制流。
- SYS-NARRATIVE 独占具体危机场景、选项文本、迟疑行为、即时反应和延迟回收内容。
- SYS-ACCESS 独占无障碍输入/输出合同、stable focus、self-voicing 状态和安全设置入口；不得生成 timeout choice。
- SYS-SAVE 独占存读档、rollback 与恢复流程；post-MVP SYS-TENSION 只能声明活动 surface 的 action gate 和“不保存活动计时器”要求。
- 当前 MVP 不存在 tension preference storage owner；未来 Ren’Py preference 或其他存储机制只能在批准的 post-MVP ADR 中保存模式值，不得取得模式规则所有权。
- UX 与 Art Bible 可以决定布局和视觉 token，但不能修改时间公式、选项语义、暂停资格或裁决结果。

### Required Ordering

1. post-MVP scope re-entry 时重新确认 SYS-TENSION GDD。
2. 用 Ren’Py 8.5.3 制作最小危机场景 spike，验证计时、输入时间戳、self-voicing、焦点、窗口失焦、帧卡顿和 interaction restart。
3. 根据 spike 创建 post-MVP SYS-TENSION ADR，冻结运行时计时和偏好存储边界。
4. post-MVP 时修订 SYS-SAVE action gate，并把 SYS-TENSION 加入 SYS-TEST 的直接验证依赖；当前不执行。
5. 完成 timed-choice UX specification、可访问读序和非颜色状态设计。
6. 由 SYS-NARRATIVE 登记首个 timed/non-timed 配对危机场景及 canonical timeout choice。
7. post-MVP 实现 manifest validator、状态机与测试矩阵；全部证据通过后才允许 timed choice 进入 post-MVP production catalog。

### Bidirectional Consistency Findings

1. SYS-CHOICE、SYS-STATE、SYS-NARRATIVE 与 SYS-ACCESS 已声明 SYS-TENSION 边界，当前方向一致；本 GDD 按 scope decision 标为 post-MVP deferred。
2. SYS-SAVE 尚未声明活动限时 surface 的 action gate、选择前恢复点和 timer non-serialization；该项随 SYS-TENSION 延期，不阻断当前 P0 Production。
3. SYS-TEST 的 timed-choice criteria 与 fixtures 改为 post-MVP scope；当前 SYS-TEST 不把 SYS-TENSION 列为 P0 Production 直接依赖。
4. 系统索引列出 Ren’Py、SYS-CHOICE、SYS-NARRATIVE、SYS-ACCESS、SYS-SAVE/SYS-TEST 集成门槛；本次批准同步其 verdict、42 AC、11 项 downstream gates 与剩余 gate 摘要。
5. Architecture 将 `TR-TENSION-001` 延后至首个危机场景，和本节 spike-first 顺序一致。
6. `tension_mode_enabled` 的跨应用存储行为仅作为 post-MVP target；当前不授予 storage owner，也不修改 SYS-PERSIST 12-leaf/5-setting 权威。
7. 当前 Production catalog 不得包含 timed choice；post-MVP 重新纳入时，仍须在 SYS-TENSION、UX、SYS-ACCESS 和 SYS-TEST 证据完成前阻断构建。

## Tuning Knobs

| Knob | Symbol / Type | Target | Safe range | Too low | Too high |
|---|---|---:|---:|---|---|
| `base_decision_seconds` | `B` / float seconds | `8` | `6–12` | 短文本也会变成反应速度测试 | 大部分短选择失去紧迫感 |
| `reading_chars_per_second` | `V` / float | `5` | `4–6` | 计算出的阅读时间过长，削弱危机节奏 | 分配时间过短，惩罚阅读速度较慢的玩家 |
| `per_option_seconds` | `K` / float seconds | `1.5` | `1–2.5` | 没有为选项比较和焦点移动留足时间 | 选项数量主导总时长，多选项场景过慢 |
| `minimum_duration_seconds` | `D_min` / float seconds | `18` | `15–24` | 短场景容易成为操作能力测试 | 大量场景被钳制为同一较长时长 |
| `maximum_duration_seconds` | `D_max` / float seconds | `40` | `32–50` | 长文本频繁撞上上限并失去阅读补偿 | 危机场景可被拖至近一分钟，压力消失 |
| `pressure_factor` | `P` / exact enum | `0.90/1.00/1.10` | 固定三档 | 不允许低于 `0.90`，否则急迫档可能越过安全底线 | 不允许高于 `1.10`，否则缓和档接近非限时体验 |
| `urgent_threshold` | `U` / ratio | `0.50` | `0.40–0.60` | 急迫提示出现太晚，玩家难以感知节奏变化 | 大部分倒计时都处于警示状态，造成疲劳 |
| `critical_threshold` | `H` / ratio | `0.20` | `0.15–0.25` | 临界提示短到无法被稳定感知 | 临界状态持续过久，视觉和心理压力过重 |

目标配置下的初始时长公式为：

`D = clamp((8 + C / 5 + 1.5 × N) × P, 18, 40)`

### Knob Interactions

- 必须始终满足 `0 < H < U < 1` 和 `0 < D_min < D_max`；违反时配置验证失败。
- 增加 `B`、`K` 或降低 `V` 都会延长时长；三者不得只做单项测试。
- `D_min` 过高会掩盖 `B/V/K` 对短场景的影响；`D_max` 过低会掩盖它们对长场景的影响。
- `P` 在钳制前应用；若多数急迫或缓和场景最终仍撞到同一边界，说明内容长度或边界配置无效，不能继续靠扩大倍率解决。
- `U` 与 `H` 只改变提示阶段，不得改变时间流速、输入、声音必要性或结果。
- 修改任何时长参数后，必须重跑全部批准场景的 `C/N/P` 清单、目标时长分布、最大字体布局和无调试 playtest。
- 修改阈值后，必须重跑静音、高对比、reduced-motion、self-voicing 和色觉无关状态辨识测试。
- 场景作者只能选择压力档，不能逐场填写任意秒数；例外必须修订 GDD，而不是添加隐藏 override。

### Locked Invariants — Not Tuning Knobs

- 紧张模式首次启动默认关闭。
- 每个 timed scene 都有语义完整的非限时正式版本。
- Timeout 解析到可主动到达的 canonical choice。
- 暂停原因、同刻确认优先级和唯一解析闩锁不可调。
- SYS-CHOICE 提交顺序、reaction/payoff coverage 和 ending boundary 不可调。
- 不提供限时独占内容、成就、奖励或动态玩家适应。
- `C` 和 `N` 是由批准内容派生的输入，不是设计师手填参数。

> 2026-08-05 systems review 与 targeted closure re-review 结论：合法参数范围 finite/non-degenerate，GDD 合同已批准；任何数值锁定仍须危机场景 playtest 与分 cohort 无障碍证据，二者属于 downstream implementation/content gates。

## Visual/Audio Requirements

### Visual State Language

| State | Required visual treatment |
|---|---|
| `stable` | 固定位置的静态进度条或刻度条、常规细轮廓和连续纹理；不使用脉冲。 |
| `urgent` | 保持相同布局，轮廓增加第二线条或单个缺口，纹理发生一次离散变化；颜色只能辅助。 |
| `critical` | 使用较粗静态轮廓、双角标或斜线纹理；不得闪烁、抖动、放大数字、遮暗全屏或改变选项价值层级。 |
| `paused` | 显示静态暂停符号和冻结的进度条；保留原选项、焦点、画面亮度与构图，不使用模糊或全屏灰幕。 |
| `expired` | 内部单 snapshot 过渡状态：记录归零条/闭合端点 token 并立即锁定输入；不要求玩家在独立帧中辨认，不得出现红叉、“失败”、惩罚滤镜或额外强制停顿。玩家可感知输出由紧随其后的 timeout-confirmed 状态承担。 |
| `timeout` | 对应迟疑选项使用与玩家主动确认该选项完全相同的 confirmed 反馈，随后退场并进入同一 reaction；不增加 timeout 徽章或特殊角色反应。 |

所有状态必须同时具有可读文字与非颜色独占的形状、轮廓或纹理差异。计时状态区占用稳定 UI 留白，不得遮挡人物动作、物件、字幕或 commit 后 reaction。

### Motion and Composition

- 使用克制的视觉小说表现：稳定构图、轻量轮廓变化和单次状态切换。
- 禁止 QTE 式缩放、逐秒跳动、心跳脉冲、警报扫光、镜头推拉、暗角收缩、抖屏和粒子爆发。
- 阶段变化不得改变选项尺寸、位置、顺序、颜色价值层级或 focus 优先级。
- `reduced_motion=true` 时所有阶段以 `0 ms` 直接建立最终静态状态；不得用短 fade 或 dissolve 代替。
- 闪烁与震动继续服从各自独立开关；SYS-TENSION 不要求任何必须使用的闪烁或震动。
- 紧迫感来自剩余时间、场景节奏和日常物件构图，不得把绘梨衣的姿态、表情或画面色调编码为“正确/错误”提示。
- 优先使用雨、车票、纸张、衣物、门窗、站台和列车等日常细节；不采用宏大灾变式 HUD，也不要求每个阶段制作独立 CG 或角色表情。

### Optional Audio

- `urgent` 与 `critical` 可各播放一次低干扰、中性的短提示音；不得使用逐秒 ticking、循环心跳或警报。
- `expired` 可使用一次柔和闭合音，但静音时必须由文字和静态视觉完整替代。
- Timeout 后的声音属于 canonical choice reaction，必须与玩家主动选择迟疑时完全一致。
- 优先采用雨声、呼吸、衣料、纸张、脚步、门窗或列车等情境内声音。
- 音高、音色、空间声和音乐动机不得暗示道德价值、路线优劣、隐藏评分或结局资格。
- Self-voicing 活动时，所有可选 UI 提示音服从 SYS-ACCESS 的抑制规则。

### Art and Asset Gates

- 正式资产制作前，Art Bible 必须统一冻结默认/高对比色板、字体、轮廓、纹理、暂停图标和静态替代语言；不得创建 SYS-TENSION 专属无障碍色板。
- Timed indicator 必须在 1280×720、字体 `1.5`、高对比、reduced-motion、flash-off、shake-off 和静音组合下通过视觉验收。
- `expired` 只是计时表现状态，canonical timeout choice 才是叙事结果；两者不得合并为新的失败演出。
- 视觉只能消费公开 warning phase，不得直接读取或泄露场景压力档 `P`。

> Art Director 已参与本节；建议已结合“温柔必须被挣来”“悲剧也是完整答案”“看见未说出口的话”和日常生活意象。最终 token 仍待 Art Bible。

## UI Requirements

### Settings Entry

post-MVP 紧张模式入口只出现在主菜单和 `PlayableStable` 设置页，归入独立分组“游戏节奏（立即生效）”。它使用唯一身份 `tension_mode_enabled`，不混入 SYS-ACCESS 五项项目设置草稿，也不创建第二设置权威。当前 MVP 不渲染该入口，也不注册该 setting。

| Element | Required copy |
|---|---|
| Label | `紧张模式` |
| Default | `关闭` |
| Description | `在少数危机场景中加入倒计时；时间结束时，故事会按场景中的“迟疑”选项继续。关闭后不会减少剧情、选项或结局可能性。` |
| Enabled feedback | `紧张模式已开启，将从下一个符合条件的危机场景生效。` |
| Disabled feedback | `紧张模式已关闭，之后的选择不再限时。` |

不得使用“困难”“真实”“推荐”“奖励”或类似价值暗示。`CriticalInteraction` 中不显示、不聚焦该入口，也不能通过快捷键打开。

### Timed Choice Layout

- 在 1280×720、`font_scale=1.5` 下使用单列选择面板，左右安全边距至少 `64 px`，上下至少 `48 px`。
- 固定阅读顺序为：场景选择提示 → 当前决定摘要 → 计时状态区 → 选项列表 → 输入提示。
- 计时状态区预留固定高度；阶段文案变化不得推动选项位置。
- 选项严格按 canonical 顺序纵向排列，每项高度至少 `64 px`，允许简体中文换行，不省略唯一行动文本。
- Timed surface 最多四项，四项最长批准文案必须全部同时完整可见；若在目标布局中需要 viewport、裁切或滚动，该场景失去 timed eligibility 并使用非限时版本。
- 倒计时开始后不得再出现新的决策关键信息、对白或动画。
- `R>0` 时显示的整数秒向上取整；只有实际进入 `expired` 才显示 `0` 或“时间已到”。

### State Copy and Cues

| State | Required player-facing presentation |
|---|---|
| `stable` | `剩余 X 秒`；静态完整边框或刻度条 |
| `urgent` | `时间开始紧迫｜剩余 X 秒`；增加非颜色缺口或第二层轮廓。该文案不声称已经过半，因此对 `U=0.40–0.60` 的全部合法配置均为真。 |
| `critical` | `时间将尽｜剩余 X 秒`；较粗静态轮廓或双线框 |
| `paused` | `计时已暂停｜剩余 X 秒`；静态暂停图形，选项与焦点保持原位 |
| `expired` / timeout-confirmed | arbitration snapshot 记录 `expired` 后立即显示 `时间已到，故事将按「[选项文本]」继续`；全部输入锁定，`timeout_choice_id` 对应选项使用普通 confirmed 状态，不显示内部 ID，也不为独立 expired 帧增加强制停顿 |
| `FallbackUntimed` | `本次选择将不计时，请按自己的节奏继续。`；移除整个计时状态区，保留选项、顺序和焦点 |

`expired` 不要求二次确认或额外停顿；锁定后立即执行 canonical timeout choice。颜色、声音和动画只能增强，不能替代文字与形状。

### Keyboard, Mouse and Focus

- 初始焦点是 canonical 顺序第一项；不得为 timeout 结果设置特殊默认焦点，除非它本来就是第一项。
- Stable semantic focus identity 直接绑定 canonical `choice_id`。
- `Tab/Down` 前进，`Shift+Tab/Up` 后退，`Enter/Space` 确认；列表端点不循环。
- `1–4` 仅对当前实际存在的对应序号提供 direct activation，并与鼠标/Enter/Space 共用同一 latch；未绑定数字键无操作。Timed surface 不使用 viewport，`PageUp/PageDown` 不滚动、不 activation，也不触发 rollback 或 rollforward。
- 鼠标 hover 可以显示指针反馈，但不得成为理解或操作的必要条件，也不得触发 self-voicing；点击通过同一 activation latch 提交同一 `choice_id`。
- 暂停、失焦恢复与 pre-latch fallback 后恢复同一 canonical focus ID。
- 取得解析闩锁后，全部选项立即锁定；重复点击、键盘确认和 timeout 不再产生反馈或第二提交。
- Self-voicing 导致的 `Paused` 仅在冻结 `R_pause>0` 时按前述 `resume_activation_intent` 合同处理确认：停止朗读、恢复稳定焦点、进入 `Running` 后在同一 snapshot 生成唯一 activation；不得静默吞掉或立即在 Paused 中提交。`R_pause=0` 时不建立 intent，恢复后唯一结果为 timeout。其他暂停原因拒绝 activation 并在可输出时提供一次状态反馈。

### Self-Voicing Contract

初次读取顺序固定为：

1. `限时选择，计时已暂停`；
2. 场景选择提示；
3. 总可用时间；
4. 选项数量；
5. 当前决定摘要；
6. 所有选项文本及对应 `1–N` 数字键，严格按 canonical 顺序；
7. 操作提示；
8. `朗读结束，倒计时开始`；
9. 初始焦点项。

- 初次完整朗读结束且焦点稳定后才进入 `Running`。
- 移动焦点时只朗读“第 N 项，共 M 项”与当前选项文本；实际朗读期间暂停，结束后恢复原时间。
- Self-voicing pause 是明确批准的 accommodation，允许其消除部分或全部 elapsed-time pressure；这不属于作弊，也不声称与视觉模式具有相同 wall-clock pressure。验收必须把 self-voicing cohort 单独报告。
- 禁止每秒自动播报。`urgent`、`critical` 各最多自动播报一次；批准的输出快捷操作可按需播报剩余时间。
- Timeout 时播报“时间已到，故事将按「[选项文本]」继续”，随后进入同一 canonical choice 的 reaction 可访问输出；不得要求二次确认。
- Self-voicing 失败时退回非限时版本，并复用 SYS-ACCESS 批准的 localized failure identity，通过仍可用的视觉文本、系统剪贴板/外部 screen-reader 通道（若 capability preflight 已证明可用）输出：`自发声暂时不可用，本次选择已改为不计时。现有选项和结果没有改变。` 不得仅告知非视觉用户“可使用键盘或鼠标”。

### Critical Interaction Gate

活动限时 surface 中，完整 Settings、save、load、rollback、history、skip、auto、quick menu 和其他控制转移入口必须隐藏并移出 focus graph。只读“当前决定摘要”属于本 surface 的冻结内容，不是 history/backlog 入口；可重复朗读且按 self-voicing pause 规则处理。

- 保留 output-only 的 `V` 与 `Shift+C`，但它们不得 activation。
- Escape、右键或受禁快捷键只显示一次：`此时无法打开菜单；计时未消耗。`
- 该提示处理期间冻结时间，随后恢复原焦点。
- Disabled 控件、底层 screen、默认引擎映射及残留手柄映射均不得绕过 gate。

### Timed/Non-Timed Equivalence

- 两版本 exact-match canonical choice IDs、文本、顺序、初始焦点规则、普通键鼠导航、reaction/payoff 和 terminal outcome set。
- 非限时版本完全移除计时区、阶段播报与自动 timeout activation；不得保留空占位或“简单模式”标签。
- `timeout_choice_id` 对应选项在非限时版本中仍正常可见、可聚焦和可主动确认。
- Timed 版本不得用颜色、默认焦点、排序、图标或措辞强调任何选项。
- Timed-only 允许差异严格限于 countdown/phase 输出、`1–N` 等价 direct activation、`resume_activation_intent`、自动 timeout activation 与 Critical Interaction Gate；这些差异必须进入 `timed_only_affordance_delta` allowlist，不得声称为操作面 exact parity。

### UX Gates and Risks

- SYS-ACCESS 设置页需增加独立“游戏节奏”分组，但不得改变其五项项目设置事务或持久化权威。
- 秒数取整、阶段切换与 self-voicing 播报必须使用同一 `R/phase` 快照，避免视觉与朗读跨边界不一致。
- 四项最长中文选项及当前决定摘要必须在 720p、字体 `1.5` 下同时完整可见并通过焦点和读序证据；需要 viewport 即失去 timed eligibility。
- 反复焦点朗读造成的时间延长是批准行为，不得在 QA 中判定为作弊。
- 提交前 fallback 可保留选择；提交后故障不得重新开放 surface，只能进入批准的安全恢复流程。
- UI stories 创建前必须完成独立 timed-choice UX specification。

> UX 专家已参与本节；精确 wireframe、focus graph 和最终文案仍需后续 `/ux-design` 批准。

## Acceptance Criteria

### Core Behavior

| ID | Evidence | Criterion |
|---|---|---|
| `TENSION-CORE-001` | `UT_ENGINE + STATIC` | **GIVEN**ADR 批准的 versioned `tension_preference_contract` 及 fresh/missing/wrong-type/unreadable fixtures，**WHEN**启动游戏并枚举冻结 production scene catalog，**THEN**effective `tension_mode_enabled=false`，持久化写回数为零，全部场景的 countdown、timeout presentation 和 timeout dispatch 数均为零。 |
| `TENSION-CORE-002` | `UT_ENGINE + INSTR` | **GIVEN**批准 owner/path/flush contract 与 durable value `false` 或 `true`，**WHEN**按冻结 transition matrix 执行安全设置更新、New Game、应用重启、save、load 与 rollback，**THEN**restart/New Game 后 durable/effective value exact preserved，save/load/rollback 前后值不变，且 writer/flush count exact-match批准合同。 |
| `TENSION-CORE-003` | `UT_ENGINE` | **GIVEN**批准的 state×input-source preference gate matrix，**WHEN**从主菜单、`PlayableStable`、`Presenting/Running/Paused/Resolving*` 的 mouse/key/direct mapping 尝试修改模式，**THEN**前两种安全状态的 visible/enabled/focusable/update counts exact-match合同；活动 surface 的入口、底层传播和更新 dispatch 数均为零。 |
| `TENSION-CORE-004` | `STATIC` | **GIVEN**production scene manifest、narrative eligibility catalog 与 test-only example exclusions，**WHEN**生成 eligibility set，**THEN**输出 exact-equal 于 raw declaration 恰为一项且 narrative record 全字段合法的 production scene IDs；未登记、重复、answer `undetermined/not_applicable` 用错、派生 bool 不为 true、reviewer role/cardinality/identity 非法、source hash stale、非 diegetic、信息不完整、terminal-prohibited 与 test-only IDs 均不进入集合。 |
| `TENSION-CORE-005` | `STATIC + BRANCH` | **GIVEN**每个批准 timed/non-timed surface pair，**WHEN**比较冻结 structured projections，**THEN**choice IDs、显示文本、顺序、初始焦点规则、普通导航、reaction、payoff 与 terminal outcome set 完全一致；差异 exact-equal 于批准 `timed_only_affordance_delta` allowlist。 |
| `TENSION-CORE-006` | `STATIC + UT_ENGINE` | **GIVEN**任一 `timeout_choice_id`，**WHEN**遍历配对的非限时 surface，**THEN**同一 canonical choice 可通过普通 activation 到达，并使用相同 reaction/payoff bindings。 |
| `TENSION-CORE-007` | `STATIC + INSTR` | **GIVEN**全部 timeout paths，**WHEN**扫描 direct writes、ending APIs 与 control transfers，**THEN**即时死亡、直接 ending jump、predicate mutation、axes/history write 和匿名 `hesitated` flag 数均为零。 |
| `TENSION-CORE-008` | `STATIC + UT_ENGINE` | **GIVEN**逐项缺少 surface pair、timeout choice、causal projection、readable time text、non-color visual state、stable focus、direct keyboard binding、declared affordance delta 或 narrative eligibility 的 one-defect fixtures，**WHEN**验证，**THEN**每项分别产生冻结 build error；对应 runtime fixture 在 latch 前只进入 `FallbackUntimed`，semantic write count 为零。 |
| `TENSION-CORE-009` | `UT_ENGINE + INSTR` | **GIVEN**timed surface 正在建立，**WHEN**决定摘要、选项、焦点、时间提示或初次可访问交付任一未就绪或 pause reason 活动，**THEN**`timer_started=false`、`countdown_consumed=0` 且状态保持 `Presenting`；全部 readiness flags 为 true 且无 pause reason 后才记录唯一 `t₀` 并进入 `Running`。 |
| `TENSION-CORE-010` | `UT_ENGINE + A11Y + INSTR` | **GIVEN**Self-voicing 初次/焦点朗读、朗读 failure、确认输入及 `R_pause>0/R_pause=0` fixtures，**WHEN**从 speech start 遍历到 completion/failure 与 focus restore，**THEN**朗读期间 `remaining_time_delta=0`；无输入且 `R_pause>0` 时恢复原焦点后继续；`R_pause>0` 的首个确认建立唯一 transient intent、停止朗读并在恢复 `Running` 的同一 snapshot 生成一次 activation；`R_pause=0` 时 intent/manual dispatch count 均为零且恢复后恰 timeout 一次；failure 时清 intent、fallback 且 semantic write count 为零。 |
| `TENSION-CORE-011` | `UT_ENGINE + INSTR` | **GIVEN**活动倒计时，**WHEN**窗口失焦、最小化或应用不可见后再恢复，**THEN**暂停区间不计入 elapsed，choice sequence 与 stable focus ID 不变。 |
| `TENSION-CORE-012` | `UT_ENGINE` | **GIVEN**无暂停原因的 `Running` surface 与版本化 mouse-motion、Tab/arrow、`1–N`、Enter/Space traces，**WHEN**执行各 trace，**THEN**active elapsed 单调增加；每个 choice position 均可由鼠标、普通导航与 direct key 解析到同一 canonical ID，且最坏 activation path 不超过批准输入预算。 |
| `TENSION-CORE-013` | `STATIC + VISUAL + A11Y + INSTR` | **GIVEN**`stable/urgent/critical/paused`、`U=0.40/0.50/0.60` 边界配置与 expired→timeout-confirmed transition，**WHEN**在静音、无动画和色觉无关配置下按批准 token/capture rubric 检查，**THEN**前四态各具可读文字和非颜色视觉标识，urgent 文案 exact-match `时间开始紧迫｜剩余 X 秒` 且不含 elapsed-fraction claim；expired 只需产生一次 instrumented transition snapshot，timeout-confirmed 提供可感知文字与普通 confirmed 反馈。可选 urgent/critical/expired cues 每 phase entry 至多一次，pause/resume 不重播，静音或 self-voicing 时 dispatch 为零，且不得延迟 focus、speech、latch 或 reaction。 |
| `TENSION-CORE-014` | `UT_ENGINE + INSTR` | **GIVEN**版本化 pause/focus/visibility、鼠标、普通键盘、`1–N` 与 timeout 事件矩阵，**WHEN**按 timestamp→kind priority→receive sequence 归约，**THEN**恰有一个结果原子关闭 latch，winning choice dispatch count 为 `1`，全部 losing activation 与 duplicate timeout dispatch count 为 `0`。 |
| `TENSION-CORE-015` | `UT_ENGINE + INSTR` | **GIVEN**manual 与 timeout 两类 activation origin，**WHEN**解析并提交，**THEN**两者均严格执行 `resolution_acceptance → apply_choice → immediate reaction → later control flow`；SYS-CHOICE payload exact-equal 对应 canonical choice record且不含 origin，commit 与 reaction 之间的交互或存档边界数为零。 |
| `TENSION-CORE-016` | `UT_ENGINE + A11Y` | **GIVEN**完整 phase×action×input-source gate matrix，**WHEN**在 `Presenting/Running/Paused/Resolving*` 调用 Settings、save/load/rollback/history、skip、auto、quick menu、direct engine mappings 与决定摘要，**THEN**受禁控制转移 visible/enabled/focusable/request counts exact-match冻结矩阵且均不执行；决定摘要只读可达；拒绝处理区间不消耗时间。 |
| `TENSION-CORE-017` | `STATIC` | **GIVEN**SYS-TENSION production closure，**WHEN**扫描写入与 ledger，**THEN**对 axes、history、counterevidence、qualification、ending state、reaction/payoff ledger 和跨周目画像的直接访问数均为零。 |
| `TENSION-CORE-018` | `STATIC + UT_ENGINE` | **GIVEN**不同阅读速度、输入设备、历史 timeout 次数、路线和无障碍模式 fixtures，**WHEN**计算相同场景配置并执行相同 semantic activation sequence，**THEN**`D`、choice order、value-neutral presentation token set、reward set 和 causal outputs 完全一致；input-specific focus indicator 可不同但不得编码价值。 |
| `TENSION-CORE-019` | `STATIC + BRANCH` | **GIVEN**模式关闭与开启的完整 choice graph，**WHEN**比较内容、成就、结局和 canonical outcome set，**THEN**两者集合完全一致；限时独占记录数为零。 |
| `TENSION-CORE-020` | `UT_ENGINE` | **GIVEN**版本化选择前 checkpoint，**WHEN**分别在 `Presenting`、`Running` 与 `Paused` 强制终止进程并从该 checkpoint 重启，**THEN**活动 timer/latch/pause/intent serialization 数为零，surface 重新验证并建立完整 `D`，自动 timeout 数为零。 |
| `TENSION-CORE-021` | `STATIC` | **GIVEN**发行源代码与构建清单，**WHEN**扫描 timeout、暂停和 decision-time consumers，**THEN**遥测、评分、成就、动态难度和跨周目画像 consumers 数均为零。 |
| `TENSION-CORE-022` | `REVIEW` | **GIVEN**完成的 Core Rules、状态机和 engine spike，**WHEN**进入 implementation-ready gate，**THEN**每项设计、UX/无障碍和程序复核记录均包含 named reviewer、role、document/source hash、rubric version、findings、dispositions、sign-off 与 `unresolved_blocking_findings=()`；缺字段、hash stale 或任一 blocker 未关闭均不通过。 |

### Formula Verification

| ID | Evidence | Criterion |
|---|---|---|
| `TENSION-FORM-001` | `UT_PURE` | **GIVEN**目标配置、`C=60,N=3,P=1.00`、合法最小 raw fixture 与合法最大 raw fixture，**WHEN**计算 `tension_initial_duration`，**THEN**分别输出 `24.5s`、当前 `D_min` 与当前 `D_max`；对合法 domain 的 property samples，增加 `B/C/K/N/P` 或降低 `V` 时 unclamped raw duration 单调不减，最终输出只按批准边界钳制。 |
| `TENSION-FORM-002` | `UT_PURE` | **GIVEN**`C/N/P/B/V/K/D_min/D_max` 的边界、越界、错误类型、NaN 与 Infinity fixtures，**WHEN**验证，**THEN**合法输入产生有限时长，非法输入返回 validation failure 而不是隐式转换或继续钳制。 |
| `TENSION-FORM-003` | `UT_PURE` | **GIVEN**暂停区间 `5–9` 与 `7–12`，以及 empty、nested、adjacent、duplicate-ID、open-ended、reversed、pre-`t₀`、post-`t`、NaN/Infinity fixtures，**WHEN**计算 `tension_effective_paused_duration`，**THEN**合法示例分别输出冻结并集长度且主例精确为 `7s`；非法 fixture 返回各自 validation error，不产生 `P_t`。 |
| `TENSION-FORM-004` | `UT_PURE` | **GIVEN**`D=24.5`、原始经过 `10s`、有效暂停 `3s` 与 property-generated valid domain samples，**WHEN**计算 `tension_remaining_time`，**THEN**主例精确为 `17.5s`，合法输出始终位于 `0–D` 且 active elapsed 增加时单调不增；`t<t₀`、`P_t<0` 或 `P_t>t-t₀` 返回 validation failure。 |
| `TENSION-FORM-005` | `UT_PURE` | **GIVEN**exact finite `D/R/H/U` 与 `Q` 位于 `1,U,H,0` 及各边界两侧，以及 wrong-type、NaN、Infinity、`D=0`、`R<0`、`R>D`、`H≥U` fixtures，**WHEN**计算 warning phase，**THEN**合法项返回唯一 `stable/urgent/critical/expired`，非法项在除法或比较前返回冻结 validation error。 |
| `TENSION-FORM-006` | `UT_PURE + UT_ENGINE` | **GIVEN**immutable arbitration snapshots 覆盖 activation 的 active elapsed 早于/等于/晚于 `D`、同刻 pause start/end、`R_pause>0` Paused intent、`R_pause=0` Paused activation、多个时间戳、同刻 receive sequence、frame stall 与 closed latch，**WHEN**执行 `tension_resolution`，**THEN**按冻结 event order 返回唯一 manual choice、timeout choice 或 unresolved；`R_pause=0` 案必须拒绝 intent并唯一 timeout，每案至多关闭一次 latch且 invalid/stale event 不进入 eligible set。 |
| `TENSION-FORM-007` | `UT_PURE + STATIC` | **GIVEN**一个完整合法 manifest 以及逐项翻转每个 conjunct 的 one-defect fixtures，**WHEN**计算 `tension_scene_manifest_valid`，**THEN**只有完整 fixture 返回 exact `true`；缺 readable text、缺 non-color visual、仅 text+audio、缺 narrative eligibility、`N>4` 或任一其他单缺陷均返回 exact `false`。 |

### Cross-System, Recovery and Accessibility

| ID | Evidence | Criterion |
|---|---|---|
| `TENSION-INT-001` | `STATIC + UT_ENGINE` | **GIVEN**SYS-CHOICE production catalogs，**WHEN**加入 timeout equivalent activations，**THEN**surface partition、canonical ID、reaction/payoff cardinality 和 reverse metadata validators 全部通过。 |
| `TENSION-INT-002` | `UT_ENGINE + INSTR` | **GIVEN**SYS-SAVE 批准的 phase×action×source matrix 与正常/失败 requests，**WHEN**遍历 `Presenting/Running/Paused/Resolving*`，**THEN**save/load/rollback UI/request/dispatch、timer/intents serialization 和恢复到半途 timer 的计数均为零；选择前 checkpoint recovery 仍可用。 |
| `TENSION-INT-003` | `UT_ENGINE + A11Y + VISUAL` | **GIVEN**批准且 version/hash 匹配的 timed-choice UX spec、字体 metrics、当前决定摘要与四项最长文案 fixtures，以及完整 1280×720×字体 `1.5`×对比×motion×self-voicing×静音 mode matrix，**WHEN**遍历全部 timer states，**THEN**无需 viewport、无裁切/重叠，focus/`1–N`/读序稳定、状态按 rubric 可辨且 semantic outputs exact-match。 |
| `TENSION-INT-004` | `UT_ENGINE + INSTR` | **GIVEN**重叠暂停、至少 `10×D_max` 的持续暂停、反复失焦和 repeated self-voicing fixtures，**WHEN**执行，**THEN**remaining time 只排除合法暂停并集，不自动 timeout、不缩短后续场景，且冻结 ownership/dataflow manifest 中不存在 abuse/cheat 标记 writer 或 consumer。 |
| `TENSION-INT-005` | `UT_ENGINE + FAULT` | **GIVEN**版本化 fault×phase matrix 覆盖时钟倒退、非有限时间、interval 损坏、manifest 损坏和 self-voicing 失败，**WHEN**逐案注入，**THEN**每个 pre-latch fault 进入该行批准的非限时 fallback 且 semantic writes 为零；每个 post-latch fault 进入 SYS-SAVE 拥有的命名 blocking-safe state且不改选。 |
| `TENSION-INT-006` | `UT_ENGINE + INSTR` | **GIVEN**production path 返回 `DUPLICATE_NOOP` 或 reaction 在 `APPLIED` 后失败，**WHEN**处理，**THEN**前者 reaction count 为零并 fail closed；后者不删除 history、不恢复 timer且停止后续控制流。 |
| `TENSION-INT-007` | `SPIKE` | **GIVEN**versioned capability manifest 为每项冻结 fixture、raw trace schema、PASS threshold 与支持的 Windows/renderer/input 配置，**WHEN**在 Ren’Py 8.5.3 验证单调时间、input receipt timestamp、同刻优先、窗口失焦、self-voicing completion/interrupt、interaction restart、帧卡顿和 preference persistence，**THEN**每项 mandatory capability 逐项 PASS；FAIL/UNVERIFIED 阻止 ADR 和 implementation-ready。 |
| `TENSION-INT-008` | `STATIC + REVIEW` | **GIVEN**engine spike、批准的 SYS-TENSION ADR 与 versioned owner/storage manifest，**WHEN**进入 implementation stories，**THEN**exact owner/path/schema generation/transaction/flush/failure contract 均唯一；SYS-PERSIST 仍只有一个 12-leaf/5-setting 权威或已通过正式 amendment，alternate writer/path 与并行设置权威数均为零。 |

### Performance and Player Validation

| ID | Evidence | Criterion |
|---|---|---|
| `TENSION-PERF-001` | `BENCH` | **GIVEN**versioned benchmark manifest 冻结最低硬件、Windows build、renderer、窗口/DPI/vsync、timer、GC、instrumentation boundary、warm-up、sample count 与 percentile method，**WHEN**测量普通 `Running` 更新，**THEN**SYS-TENSION-owned span 的 p95≤`0.5ms/frame`、max≤`1ms/frame`，并保留全部原始样本。 |
| `TENSION-PERF-002` | `BENCH + INSTR` | **GIVEN**确认、timeout、同刻竞争与冻结 stall magnitude 的 fixtures，**WHEN**解析，**THEN**semantic arbitration 在首个可运行 update 中原子关闭 latch并产生唯一 dispatch；无 stall 时 dispatch latency≤`16.6ms`，有 stall 时另报 processing/visible latency且不得改写 timestamp-based winner。 |
| `TENSION-HUMAN-001` | `HUMAN + A11Y` | **GIVEN**冻结 questions/coding rubric、counterbalanced order、至少 8 名无调试参与者且 self-voicing/相关 motor-reading accommodation cohort 单独报告，**WHEN**覆盖默认关闭、标准限时、主动迟疑、自然 timeout、self-voicing 和失焦恢复，**THEN**每个适用 cohort 分别至少 `75%` 能说明模式是可选节奏而非正确答案/速度评分，至少 `75%` 能把 timeout 理解为场景内 canonical 迟疑选择而非 UI 故障；不得用 pooled average 掩盖 cohort failure，也不要求 wall-clock pressure 相等。 |
| `TENSION-HUMAN-002` | `HUMAN + BRANCH` | **GIVEN**冻结 discovery start state、task-success definition、semantic-difference rubric、blinded adjudication 与 counterbalanced timed/non-timed order，**WHEN**参与者体验配对版本，**THEN**非限时入口发现和任务完成率为 `100%`；两版本 choice meaning、reaction、payoff 与 terminal outcomes 无经裁定差异，timed-only affordance differences 被正确理解且单独报告。 |
| `TENSION-EVID-001` | `STATIC` | **GIVEN**SYS-TENSION acceptance bundle，**WHEN**汇总 criterion IDs，**THEN**每个 ID 唯一并关联版本、source/config/catalog hashes、fixture/assertion IDs、环境、原始输出或人工记录、rubric version及 PASS 状态；任一 source/config/catalog hash mismatch 定义为 stale 并失败。 |

> 2026-08-05 `qa-lead` adversarial review 已纳入并重写模糊、不可独立验证或错误合并 origin 的 criteria；fixture generation、性能 manifest 与人工 rubric 仍须由独立 QA 在实施前批准。

## Downstream Implementation Gates

以下 Q1–Q11 均已有 owner、due 与 closure evidence。它们控制各自 implementation、content、UI、asset、QA 或 release gate；证据尚未产出不构成未关闭的 GDD blocker。

| ID | Open Question | Owner | Due | Closure Evidence |
|---|---|---|---|---|
| `TENSION-Q1` | 首批哪些危机场景获得 timed eligibility，各自的 `scene_id`、`P` 档位、`timeout_choice_id`、决定摘要、diegetic deadline、agency answer state、timeout causal bridge、reaction 与 payoff 是什么？ | SYS-NARRATIVE + SYS-CHOICE / Andwey | 任一 timed scene 进入 production catalog 前 | 批准的 narrative eligibility + timed/non-timed scene manifests、canonical choice records、双向 reaction/payoff joins、next-agency distance 与完整 continuation witnesses |
| `TENSION-Q2` | post-MVP Ren’Py 8.5.3 能否提供本 GDD 所需的单调计时、input receipt timestamp、stable receive sequence、同刻 state→activation→timeout order、窗口失焦、self-voicing completion/interrupt、interaction restart 与帧卡顿行为？ | Engine Programmer + SYS-TEST / Andwey | post-MVP SYS-TENSION ADR 前 | 最小 crisis-scene spike、versioned capability manifest、原始 arbitration/input traces、目标 Windows 环境清单与逐 capability PASS |
| `TENSION-Q3` | post-MVP 的 `tension_mode_enabled` 如何跨应用与 New Game 保留，同时保持不受 save/load/rollback 影响且不创建第二持久化权威？ | Architecture + SYS-TENSION + SYS-PERSIST / Andwey | post-MVP implementation stories Ready 前 | 批准 ADR、唯一 owner/storage manifest、restart/new-game/save/load/rollback evidence 与 12-leaf/5-setting non-conflict scan |
| `TENSION-Q4` | SYS-ACCESS 设置页如何加入独立“游戏节奏”分组，并实现立即生效而不污染五项项目设置草稿事务？ | SYS-ACCESS + UX / Andwey | Settings UI stories 前 | 修订后的 SYS-ACCESS 接口、批准 wireframe/focus graph、Apply/Cancel 非干扰测试和唯一 setting identity scan |
| `TENSION-Q5` | post-MVP SYS-SAVE 如何冻结 `Presenting/Running/Paused/Resolving*` 的完整 action gate、选择前恢复位置、命名 post-latch blocking state 和 timer/intent non-serialization？ | SYS-SAVE + SYS-TENSION + SYS-TEST / Andwey | post-MVP timed-choice integration 前 | SYS-SAVE amendment、phase×action×source matrix、save/load/rollback/quit/crash fixtures、半途 timer/intent serialization count `0` |
| `TENSION-Q6` | Timed-choice surface 的精确几何、四项最长中文文案与决定摘要、focus graph、数字键映射、秒数取整、状态播报和 fallback 文案如何落地且无需 viewport？ | UX Designer + SYS-ACCESS / Andwey | UI epics 前 | `/ux-design` 输出；1280×720、字体 `1.5`、四项最长文本+摘要、键鼠/`1–N` 与 self-voicing 全矩阵 |
| `TENSION-Q7` | 默认与高对比色板、轮廓、纹理、暂停图标、状态 token 与可选提示音资产是什么？ | Art Director + Audio Director / Andwey | 正式资产制作前 | 批准 Art Bible、授权/来源记录、静音与 reduced-motion 变体，以及 `/asset-spec system:sys-tension` 输出 |
| `TENSION-Q8` | `B/V/K/D_min/D_max/P/U/H` 的目标值与安全范围能否在首个危机场景中产生压力而不形成速度、选项位置或输入设备测试？ | Systems Design + UX + QA / Andwey | Scene content lock 前 | 公式边界报告、时长分布、choice position×mouse/navigation/`1–N` 最坏路径、分 cohort 至少 8 人无调试 playtest、无障碍复核与批准 tuning revision |
| `TENSION-Q9` | 完整测试环境、时钟 fault injection、竞争事件序列、性能采样与 acceptance bundle 格式如何冻结？ | SYS-TEST + QA + Performance / Andwey | QA plan 前 | 版本化 fixture manifest、环境/renderer/DPI/vsync/GC/timer policy、raw traces、benchmark protocol 与 criterion-to-evidence index |
| `TENSION-Q10` | 玩家能否理解紧张模式是可选节奏层，并把 timeout 理解为场景内 canonical 迟疑选择而非 UI 故障、失败或正确答案评分；self-voicing cohort 是否在不要求 wall-clock 等价的前提下仍理解危机节奏？ | UX Research + Narrative + QA / Andwey | Release content lock 前 | counterbalanced rubric；每个适用 cohort 两项理解率各 `≥75%`，非限时任务完成率 `100%`，保存原始回答、cohort breakdown 与失败样本裁定 |
| `TENSION-Q11` | SYS-TENSION 是否进入首个公开版本；若进入，最小可发布场景数和可删减边界是什么？ | Producer / Andwey | Release scope lock 前 | Crisis-scene prototype、风险/成本评估、P1 scope decision；无论结果如何，默认关闭与非限时完整路径保持不变 |

## Closed Review Questions

| ID | Question | Closure | Closed |
|---|---|---|---|
| `TENSION-Q12` | 2026-08-05 full review 的六项 GDD blockers 是否关闭，且 downstream gates 是否均有具名 owner、due 与 closure evidence？ | Targeted closure matrix 为 `6/6 CLOSED`；三项复审残余正确性 finding 已修订；Q1–Q11 完整保留为 downstream implementation gates；`unresolved_blocking_findings=()`。审计记录见 `design/gdd/reviews/sys-tension-review-log.md`。 | 2026-08-05 / Producer acceptance |
