# 确定性结局判定

> **Status**: Approved with provisional downstream gates — Targeted Core Contract Closure 5/5 PASS
> **System ID**: SYS-ENDING
> **Author**: Andwey + Codex
> **Last Updated**: 2026-08-04
> **Implements Pillar**: 温柔必须被挣来；悲剧也是完整答案；用普通生活抵抗宏大命运
> **Review Mode**: Full independent review completed; targeted closure authorized
> **Creative Director Review (CD-GDD-ALIGN)**: MAJOR REVISION NEEDED on 2026-07-27; core architecture retained
> **Journal Projection Amendment**: 2026-08-03 — adds static `journal_ending_catalog:v1` without changing resolver predicates、priority or runtime `display_cause_ids`

## Overview

SYS-ENDING 是第七日自动执行的确定性结局判定系统。它接收 SYS-STATE 提供的独立五轴与有序选择历史快照，按照固定优先级解析未解决反证、路线事实和资格，生成唯一且可解释的结构化结局记录，并进入对应的六个结局之一。玩家不直接操作判定器，却会通过此前每次观察、尊重、坦白、准备与承担代价的选择感受到它的结果：成功与悲剧都必须准确回收真实因果，而不是由最后一次选择、隐藏好感度或随机数决定。具体纯度、状态边界与记录契约遵循 ADR-0001、ADR-0004 和 ADR-0005。

## Player Fantasy

玩家应感到自己不是在破解一张隐藏的结局条件表，而是在用七天的行动建立一条会被世界准确记住的因果链。第七日揭晓时，理想感受依次是期待、辨认与承担：玩家能从结局原因中认出自己曾经观察、询问、隐瞒、准备、越界或付出的具体时刻，并理解为什么这些行为共同导向当前答案。

真结局带来的满足不是“数值刷满”，而是确认普通未来确实被逐日挣来；悲剧结局也不是系统惩罚，而是对尚未解决的伤害、缺失的准备或被转嫁代价的完整回收。系统因此直接服务于“温柔必须被挣来”“悲剧也是完整答案”和“用普通生活抵抗宏大命运”三项创作支柱。判定机制本身保持不可见，玩家只接触可理解的原因、代价与叙事结果。

*2026-07-27 独立审查确认 ordered-history → fold/projection → predicate → cause/payoff 骨架成立；本轮只闭合五项核心合同，不重新运行完整发散审查。*

## Detailed Design

### Core Rules

1. SYS-ENDING 只在第七日终局入口运行。入口必须先由 SYS-STATE 验证 active sentinel 与 rollback-owned live state，再取得完全 detached 的 schema 2 snapshot。Resolver 不得接收 live `RunMap`、`RunList` 或其他可变 store 对象。

2. `resolve_ending_record(snapshot)` 是唯一 canonical 判定入口。兼容入口 `resolve_ending(snapshot)` 只能调用 canonical 入口一次并读取一次 `.ending_id`，不得形成第二条判定路径。

3. 每次判定固定依次执行九个阶段：

   `snapshot type sweep → snapshot value/shape → catalog coverage + semantic replay → token fold → route-fact fold → qualification derivation → priority predicate evaluation → cause extraction → record construction`

   `catalog coverage + semantic replay` 必须为 history 中每个 choice 找到唯一冻结语义记录，按 SYS-STATE 的 canonical cap 规则从零重放 axis deltas，并要求重放结果与 snapshot axes 深值相同。该重放同时冻结每个轴阈值的 ordered contributor choice IDs；不一致时抛出 `ValueError`，token fold 与后续阶段调用数全部为 0。任一阶段失败后，所有后续阶段均不得运行。

4. 有序 history 是唯一动态因果来源。Resolver 必须从冻结目录中重建：

   - unresolved counterevidence tokens；
   - completed events；
   - current resource possession；
   - route qualifications。

   不得读取章节 flag、背包、persistent、成就、UI、时间、随机数或其他 live state。

5. Counterevidence fold 从空集开始按 history 左至右执行。`revoke` 加入唯一 token；build-valid `repair` 只能移除当前仍 unresolved 的同域目标。不存在 positive `grant`。尚未产生或已经解决的 repair target 在运行时触发 `ValueError`。

6. Route-fact fold 按 history 重建 event/resource facts。重复 acquire 已持有资源或 consume 不存在资源均触发 `ValueError`，且 qualification、predicate、cause 与 record 阶段不得运行。

7. 四项 terminal route qualification 的 ID、record schema 与终局前语义由 SYS-ENDING 拥有；后续 SYS-CHOICE/SYS-NARRATIVE 只能提供符合该 schema 的非空 source bindings：

| Qualification ID | Kind | 语义 |
|---|---|---|
| `qualification_independent_contact_route` | `route_membership` | 在 ending entry 前已选择可独立执行的离开方案，并建立绘梨衣同意的持续联系渠道与完整风险交接 |
| `qualification_shared_escape_route` | `route_membership` | 在 ending entry 前两人已共同承诺同一逃离方案，并各自承担已登记的必要资源、风险或代价 |
| `qualification_solo_departure_route` | `route_membership` | 在 ending entry 前绘梨衣持有可独立执行的离开方案，但不存在共同逃离或持续联系承诺 |
| `qualification_old_order_return_route` | `route_membership` | ending entry 前最后一个有效路线承诺或不可撤销约束指向旧秩序 |

Qualification 只描述终局前已发生的承诺、资源与约束，不得把“最终安全离开”“最终失散”或其他由 ending 演出产生的命运结果反向作为 source。每项必须只从 ordered choice history 及其派生 event/resource facts 得出。合法 terminal path 上四项资格必须互斥；不得保存独立 `qualified_*` 布尔值。

每个 source 在派生时冻结为 conceptual `QualificationSourceFact := (source_kind, source_id, truth, contributor_choice_ids)`，其 concrete representation 是 exact immutable tuple，不新增 runtime record class；false source 也必须保留 source kind/ID 与 contributor lineage。Cause identity 必须编码决定性 source facts，不能只编码 qualification ID 与最终 bool。具体 source IDs 在 SYS-CHOICE/SYS-NARRATIVE 设计时绑定，在内容冻结前必须成为 exact、非空且引用完整的 records。

8. 结局按固定优先级求值。每个已到达的 predicate tree 必须完整执行全部 clause，不得 short-circuit；首个 root 为 true 的结局被选中。

| 优先级 | Ending ID | Exact semantic predicate |
|---|---|---|
| 1 | `rain_stops` | 五轴均为 exact int 3，且 unresolved-token set 为空；禁止读取任何 qualification |
| 2 | `her_own_name` | `autonomy ≥ 3`、`truth ≥ 3`、`understanding ≥ 2`；`qualification_independent_contact_route` present；所有 autonomy/truth domain token absent |
| 3 | `see_the_sea` | `autonomy/preparation/sacrifice ≥ 2`、`understanding/truth ≥ 1`；`qualification_shared_escape_route` present；所有 autonomy/truth/sacrifice domain token absent |
| 4 | `one_person_train` | `qualification_solo_departure_route` present；且 `understanding ≤ 1`、`preparation ≤ 1` 或存在 unresolved understanding/preparation/truth token 至少一项 |
| 5 | `golden_cage` | `qualification_old_order_return_route` present；至少一个 autonomy domain token unresolved |
| 6 | `unsent_postcard` | unconditional `always_true` fallback |

Domain-level token 条件在内容构建时展开为冻结目录中对应 token ID 的 exact `present`/`absent` atomic clauses。目录变化必须重新验证完整 predicate graph 与 canonical witnesses。

9. Canonical resolver 返回唯一 deep-immutable `EndingResolutionRecord`，其中包含 ending ID、fold 后事实、资格、完整 clause trace、当前结局 matched causes、所有更高优先级结局的 exclusion causes、unresolved-token audit causes，以及玩家可展示的 cause IDs。

10. Cause extraction 只能读取 cause-ready `FrozenResolutionEvaluation`，不得重新读取 snapshot、history、catalog 或 evaluator。相同 snapshot 必须产生深值相同的 resolution record。

11. `display_cause_ids` 必须包含一个 presentation-safe selected-ending anchor，并可再包含最多两个按冻结 total order 选出的 presentation-safe matched、unresolved 或 exclusion causes。除 `unsent_postcard` 外，anchor 固定为当前结局首个 safe matched cause。任何进入候选集的 cause template 必须解析到 exact immutable `player_cause_summary_record(player_summary_id, locale, text_id, presentation_safe, spoiler_class)`；build validator 只把 `presentation_safe=true` 且 `spoiler_class="reached_path_only"` 的 template IDs 编译进 private frozen safe index。Audit-only 或尚无安全摘要的 cause 不得进入候选集。UI 不得自行过滤、替换或重排 resolver 已批准的 IDs。

   `unsent_postcard` 的 constant root matched cause 只提供 totality并保留在审计 record，不得成为泛化的玩家首卡。Display selection 必须从已冻结的 concrete failure/unresolved causes 中按 `understanding → truth → preparation → unresolved consequence → latest failed commitment` 的 ending-specific 顺序选择一个 `fallback_decisive_loss` presentation anchor；该既有 cause 必须带实际 source IDs/anchors 或明确的已登记证据缺失，且拥有 presentation-safe summary。此规则不创建第二个 cause record，也不改写其 identity。

   `display_cause_ids` 只服务当前 ending presentation，不进入 SYS-PERSIST。供跨周目 Journal 使用的 `journal_ending_catalog:v1` 是独立的 immutable presentation catalog：每个 ending record 恰含 `(ending_id, journal_display_rank, title_id, summary_id, journal_cause_ids)`。中立策展 rank 冻结为 `one_person_train=10`、`her_own_name=20`、`rain_stops=30`、`unsent_postcard=40`、`see_the_sea=50`、`golden_cage=60`；这是“移动→名字→天气→书信→远方→空间”的母题序列，不得改成 resolver priority、stable-ID UTF-8、结局类型或获得顺序。`journal_cause_ids` 含 1–3 个静态 cause summaries；build validator 必须通过全部 terminal equivalence classes 的 cause/outcome intersection，证明每个 summary 对该 ending 的所有合法 classes 都为真，且 `cause_scope` 只为 `CURRENT_ENDING_FACT` 或 `CURRENT_ENDING_UNRESOLVED_CONSEQUENCE`。Higher-priority exclusion、未到达路线、阈值与逐 traversal contributors 不得进入此 catalog。Journal 不从 `display_cause_ids` 运行时过滤或推导该投影。

12. 每条合法 terminal path 必须属于一个 `terminal_cause_equivalence_class`。Class identity 由 ending、完整 causes/exclusions、unresolved tokens 与 terminal outcome signature 共同决定，不得为了预算合并不同命运、代价承担者或悲剧闭环。每个结局目标为 1–6 classes，7–12 触发范围复核，超过 12 阻断内容构建。Resolver core approval 只冻结 class-key 算法和预算 oracle；实际 class 数量、witness、payoff 与 player summary 是 SYS-CHOICE/SYS-NARRATIVE 完成后的 provisional downstream gate，在通过全图枚举前不得锁定生产内容。

13. 非法 snapshot、目录、predicate graph 或 fold 不得改判为 fallback。`unsent_postcard` 只处理合法但未命中更高优先级结局的快照。

14. SYS-ENDING 不负责创作 choice、reaction、payoff scene、achievement condition 或章节内容；它只定义这些内容必须满足的结局、资格、因果和输出契约。

### Five Core Closure Contracts

1. **Qualification ownership**：SYS-ENDING 冻结 qualification IDs、终局前语义、source-fact schema、派生/互斥规则与 failure identity；SYS-CHOICE/SYS-NARRATIVE 只填 exact bindings。
2. **Predicate and terminal compatibility**：Runtime selection 保持固定优先级；content validator 另外验证所选 ending 与 terminal outcome signature 相容，不能让谓词优先级掩盖命运矛盾。
3. **Snapshot/cause coherence**：每个合法 snapshot 的 axes 必须可由同一 ordered history 与冻结 axis projections 重放；每个 matched/exclusion cause 必须拥有可构造的 contributor lineage。
4. **Class-budget boundary**：Resolver 冻结 class identity 与 deterministic enumeration contract；实际全路径数量属于 CHOICE/NARRATIVE 下游门槛，不倒灌为伪造的当前证据。
5. **Presentation/lifecycle/test oracle**：只有 presentation-safe causes 可进入展示；Day 7 flow 使用唯一 rollback-owned lifecycle 与 label map；所有组件 AC 必须能由 frozen contract fixtures 独立执行。

### States and Transitions

Rollback-owned lifecycle 由三个 Ren’Py `default` 变量表达：

```renpy
default ending_flow_sentinel = None
default ending_flow_state = None
default pending_ending_id = None
```

新游戏初始化与 SYS-STATE schema 2 初始化在同一原子叙事入口把 sentinel/state/pending 设置为 `"ending_flow:v1"`、`"Active"`、`None`。受支持的 load 必须验证 sentinel 为 exact string `"ending_flow:v1"` 且 state 为 exact string `"Active"`/`"Ended"`：`"Active"` 时 pending 只能为 `None` 或六个 ending IDs 之一，`"Ended"` 时 pending 必须为六个 IDs 之一；缺失、wrong type、unknown version、非法 state 或非法组合进入与 SYS-SAVE 共用的 blocking safe flow。这样旧存档不会因 `default "Active"` 被静默伪装成已初始化状态。

唯一映射 `ENDING_LABEL_MAP` 固定为：

| Ending ID | Stable label |
|---|---|
| `rain_stops` | `ending_rain_stops` |
| `her_own_name` | `ending_her_own_name` |
| `see_the_sea` | `ending_see_the_sea` |
| `one_person_train` | `ending_one_person_train` |
| `golden_cage` | `ending_golden_cage` |
| `unsent_postcard` | `ending_unsent_postcard` |

唯一编排入口为 `day7_resolve_ending`：先验证 lifecycle 为 `Active`，取得一次 snapshot，调用 canonical resolver 一次，验证 ending ID 属于完整一对一 mapping，再执行一次固定 label jump。每个 ending entry 的第一项共同调用 `commit_ending_entry(expected_ending_id)`，它验证当前 label 与 pending ID 匹配后以 replacement assignment 把 `ending_flow_state` 从 `"Active"` 改为 `"Ended"`；不得修改 `semantic_state`。`commit_ending_entry` 只标记已进入结局，不产生 persistent unlock。

#### Ending completion boundary

`SYS-ENDING` 同时拥有唯一的 `commit_ending_completion` completion boundary。六个 ending label 各自的唯一调用位置是该 label 的 terminal completion node：最后一段 ending narration 与最后一个玩家可见 closure 完成之后、离开 label 或返回章节控制流之前。该 node 只调用 `commit_ending_completion(ending_id, completion_checkpoint)` 一次；resolver、entry 首句、UI/Journal callback 和 SYS-PERSIST adapter 均不得调用它。

调用结果是 rollback-owned `ending_completion_event_record`，字段固定为 `ending_id, completed_event_id, checkpoint_id, checkpoint_occurrence_id, collection_epoch_id, catalog_generation_id, stable_completion_boundary, owner_system`；`completed_event_id` 为 `ending_completed:{ending_id}`，`stable_completion_boundary=True`，`owner_system=SYS-ENDING`。唯一 persistence checkpoint coordinator 将该记录转换为 SYS-PERSIST ending request；SYS-PERSIST 只验证 owner、catalog、epoch、checkpoint 与 completion reference，不重新执行 resolver 或 ending predicate。

`commit_ending_entry` 之后、completion node 之前，ending lifecycle 为 `Ended` 但 ending membership、completed-event request 与 persistent write count 必须为 0。completion 的 `APPLIED_FLUSHED` 只使 canonical root 增加该 ending membership；per-run save/load/rollback 只恢复 lifecycle、completion event 与控制位置，不撤销已落盘 membership。回退到 completion node 前恢复“未完成” event state；再次前进可重放同一 occurrence，已存在 membership 返回 `DUPLICATE_NOOP`，不产生第二次通知。

| 当前状态 | 触发 | 结果 | 所有者与约束 |
|---|---|---|---|
| `"Active"` | `day7_resolve_ending` 请求判定 | 执行一次纯 resolver call；无持久化 `Resolving` 状态 | SYS-ENDING；不得修改 `semantic_state` |
| `"Active"` | Resolver 返回合法 record | 记录 rollback-owned pending ending ID，并按固定映射 jump | mapping 缺失/重复/未知 ID 时 fail closed |
| `"Active"` | 实际进入合法 ending label 首句 | `"Active" → "Ended"` | 仅 `commit_ending_entry` 可以触发 |
| `"Active"` | Resolver、mapping 或 presentation preflight 失败 | 保持 `"Active"` 并进入 blocking development/safe-flow boundary | label、cause UI、persistent、achievement、journal 调用数全为 0 |
| `"Ended"` | 再次请求结局判定 | 抛出固定 `RuntimeError("ending already committed")` | canonical resolver call count 为 0；completion 仍只能在唯一 terminal completion node 执行 |
| 回退至 ending entry 之前 | Ren’Py rollback 恢复流程 | 恢复 `"Active"` 与 pending 值；相同 snapshot 重算相同 record | Resolver 自身不保存运行状态 |

`Active → Ended` 是唯一由本系统拥有的叙事流程转换。进入结局之后的 persistent unlock、achievement grant 和 journal admission 是下游行为，不属于判定本身。

### Interactions with Other Systems

| 系统 | 方向 | 接口与所有权 |
|---|---|---|
| SYS-STATE | 输入 | 提供经过 active validation 的 detached schema 2 axes+history snapshot；SYS-ENDING 只读，并用冻结 choice axis projections 重放验证 axes/history 一致性 |
| SYS-CHOICE | 构建期输入 | 提供 stable choice declarations、axis/counterevidence/route-fact projections、reaction/payoff joins；当前 exact records 是 provisional downstream gate |
| SYS-NARRATIVE | 构建期输入/内容消费 | 提供 event/resource/outcome/payoff records、terminal witnesses 与 qualification source bindings；消费 selected ending 进入对应演出 |
| SYS-SAVE / Ren’Py rollback | 外围状态 | 恢复 SYS-STATE、`ending_flow_sentinel/state`、pending ending ID 与 rollback-owned completion event；不得序列化 resolver 临时状态或让 imported module 持有 live state；不得回退 canonical persistent membership |
| SYS-TEST | 验证输出 | 消费完整 immutable record、canonical witnesses、boundary fixtures、AST instrumentation 与 purity evidence |
| SYS-JOURNAL | 下游只读 | 消费 `journal_ending_catalog:v1` 的静态摘要、`journal_display_rank` 与跨全部terminal classes成立的 `journal_cause_ids`；不得读取逐traversal hidden record、`display_cause_ids`或自行重判结局 |
| SYS-PERSIST | 下游只读 | 仅在唯一 terminal completion node 后记录 ending unlock；persistent 状态不得成为 resolver 输入 |
| SYS-ACHIEVE | 下游只读 | 只在叙事条件完成后处理成就；不得以轴值、token emptiness 或 predicate 作为反向结局条件 |
| SYS-ACCESS | 演出约束 | 原因摘要必须支持键盘与文本访问；无障碍等价 choice 必须保留相同语义 history |
| Day 7 orchestrator | 控制流 | `day7_resolve_ending` 调用 canonical resolver 一次并执行固定映射；六个 entry 只通过 `commit_ending_entry` 完成唯一 `Active → Ended`，六个 terminal completion node 只通过 `commit_ending_completion` 发出完成事件 |

*2026-07-27 定点修订已冻结 lifecycle、label map 与失败 oracle；SYS-SAVE GDD 仍须把这些字段纳入正式 load/rollback 集成门槛。*

## Formulas

### Route Qualification Truth

The `route_qualification_truth` formula is defined as:

`Q(q) = ∧ (f.truth for f in S_q)` when `derivation_operator = all`; otherwise `Q(q) = ∨ (f.truth for f in S_q)`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Qualification | `q` | stable ID | 四项注册资格之一 | 当前派生目标 |
| Source truths | `S_q` | exact tuple of `QualificationSourceFact` | 1–N 项 | 来自 history membership、completed event 或 resource possession 的完整 truth/source/contributor facts |
| Operator | — | exact string | `all` / `any` | 资格记录声明的派生方式 |
| Qualification truth | `Q(q)` | exact bool | `False` / `True` | 当前 snapshot 是否具备该资格 |

**Output Range:** exact `False` 或 `True`。即使逻辑结果已确定，全部 source 仍必须被检查并冻结 contributors，不得 short-circuit。

对于 failure cause，决定性 source facts 固定为：`all=false` 取全部 false facts；`any=false` 取全部 facts；`all=true` 取全部 facts；`any=true` 取全部 true facts。Cause payload 编码每项 `(source_kind, source_id, truth, contributor_choice_ids)`，因此“缺 A 与 B”和“只有 B 缺失”不会产生相同 cause identity。

**Example:** 若 `qualification_shared_escape_route` 使用 `all`，其三个 source truth 为 `(True, True, True)`，则 `Q = True`；若为 `(True, False, True)`，则 `Q = False`。

合法 terminal path 还必须满足：

`Σ int(Q(q)) ≤ 1`

其中 `q` 遍历四项 terminal route qualifications。

### Ending Predicate Truth

The `ending_predicate_truth` formula is defined as:

```text
P_rain =
    u = 3 ∧ a = 3 ∧ t = 3 ∧ p = 3 ∧ s = 3 ∧ |U| = 0

P_name =
    a ≥ 3 ∧ t ≥ 3 ∧ u ≥ 2
    ∧ Q(qualification_independent_contact_route)
    ∧ U ∩ (T_autonomy ∪ T_truth) = ∅

P_sea =
    a ≥ 2 ∧ p ≥ 2 ∧ s ≥ 2 ∧ u ≥ 1 ∧ t ≥ 1
    ∧ Q(qualification_shared_escape_route)
    ∧ U ∩ (T_autonomy ∪ T_truth ∪ T_sacrifice) = ∅

P_train =
    Q(qualification_solo_departure_route)
    ∧ (
        u ≤ 1 ∨ p ≤ 1
        ∨ |U ∩ (T_understanding ∪ T_preparation ∪ T_truth)| ≥ 1
    )

P_cage =
    Q(qualification_old_order_return_route)
    ∧ |U ∩ T_autonomy| ≥ 1

P_postcard = True
```

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Understanding | `u` | exact int | 0–3 | 理解正向证据 |
| Autonomy | `a` | exact int | 0–3 | 自主正向证据 |
| Truth | `t` | exact int | 0–3 | 真相正向证据 |
| Preparation | `p` | exact int | 0–3 | 准备正向证据 |
| Sacrifice | `s` | exact int | 0–3 | 承担代价正向证据 |
| Unresolved tokens | `U` | exact immutable set during evaluation | 0–10 项 | 从 ordered history 折叠出的未解决反证 |
| Domain token catalog | `T_domain` | frozen token-ID set | 0–2 项/域 | 某一语义域注册的全部 revoke tokens |
| Qualification truth | `Q(q)` | exact bool | `False` / `True` | 从 history facts 派生的路线资格 |

**Output Range:** 每个 `P_*` 输出 exact `False` 或 `True`；`P_postcard` 对所有合法 snapshots 恒为 `True`。

**Example:** 输入 `(u,a,t,p,s) = (2,3,3,1,1)`，具备 `qualification_independent_contact_route`，且没有 unresolved autonomy/truth token，则 `P_name = True`；即使其他低优先级 predicate 也成立，仍选择 `her_own_name`。

### Terminal Outcome Compatibility

Runtime predicate selection 与 content-build compatibility 分离，避免把下游命运结果反向塞进纯 resolver 输入。每条 terminal path 在内容冻结前必须满足：

```text
compatible(rain_stops) =
    qualification ∉ {solo_departure, old_order_return}
    ∧ terminal_outcome_signature contains
        erii_ordinary_future
        lmf_relinquishes_power
        lmf_relinquishes_old_identity

compatible(her_own_name) =
    independent_contact commitment and informed-contact outcome agree

compatible(see_the_sea) =
    shared-escape commitment, informed joint risk, and shared cost outcomes agree

compatible(one_person_train) =
    solo-departure outcome and at least one relationship/preparation loss agree

compatible(golden_cage) =
    old-order-return outcome and unresolved autonomy harm agree

compatible(unsent_postcard) =
    fallback_decisive_loss presentation anchor resolves to understanding, truth, preparation,
    unresolved consequence, or failed commitment evidence
```

任何 predicate 已选中但 compatibility 为 false 的路径均使内容构建失败；priority 不得掩盖该矛盾。`rain_stops` runtime predicate 仍不读取 qualification，符合 ADR-0001；qualification 只在非运行时 terminal-path validator 中用于发现作者内容冲突。

### Ending Selection

The `ending_selection` formula is defined as:

`selected_ending = ENDING_PRIORITY[min { i | P_i = True }]`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Priority table | `ENDING_PRIORITY` | exact tuple of stable IDs | 固定 6 项 | `rain_stops` 到 `unsent_postcard` |
| Predicate result | `P_i` | exact bool | `False` / `True` | 第 `i` 个结局 root 的完整求值结果 |
| Selected index | `i` | exact int | 0–5 | 第一个 predicate 为 true 的位置 |

**Output Range:** 六个注册 ending ID 中恰好一个。由于最终 predicate 恒为 true，合法 snapshot 不存在空结果。

**Example:** 若 predicate results 为 `(False, False, True, True, False, True)`，最小 true index 为 2，输出 `see_the_sea`。

### Display Cause Selection

The `display_cause_selection` formula is defined as:

```text
safe_matched = presentation_safe(matched_causes)
anchor =
    safe_matched[0] when selected_ending != unsent_postcard
    otherwise first_safe_by_postcard_anchor_order(failure_and_unresolved_causes)
candidates = stable_unique(
    total_order(
        presentation_safe(
            concat(
                remaining(safe_matched),
                unresolved_token_causes,
                higher_priority_exclusion_causes
            )
        )
    )
)
display_cause_ids = (anchor.cause_id,) + cause_ids(take_first_2(candidates))
```

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Matched causes | `M` | exact tuple | 至少 1 项 | 当前结局成立的实际路径原因；postcard constant match 可为 audit-only |
| Unresolved causes | `U_c` | exact tuple | 0–10 项 | 未解决反证原因 |
| Exclusion causes | `X` | exact tuple | 0–N 项 | 更高优先级结局未成立的原因 |
| Total-order key | `k(c)` | exact tuple | 固定字段顺序 | anchor、history span、cause/source rank 与 cause ID |
| Display IDs | `D` | exact tuple of strings | 1–3 项 | 玩家演出可使用的原因 ID |

**Output Range:** 1–3 个 cause IDs；第一项始终是 presentation-safe selected-ending anchor，除 postcard 外必须是当前结局 matched cause。每个 ID 必须在 record 的 cause collections 并集中恰好解析一次，且其 `player_summary_id` 在冻结 summary catalog 中恰有一项 approved/non-spoiler 记录。

**Example:** `M = (m1, m2)`，其余候选按 total order 为 `(u1, m2, x1)`，则 `D = (m1, u1, m2)`。

### Terminal Cause Class Identity

The `terminal_cause_class_identity` formula is defined as:

```text
class_key = (
    ending_id,
    ordered_matched_cause_ids,
    ordered_higher_priority_exclusions,
    ordered_unresolved_token_ids,
    terminal_outcome_signature
)
```

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Ending | `e` | stable ID | 六结局之一 | 当前结局 |
| Matched causes | `M_id` | exact tuple | 非空 | 完整、规范排序的 matched cause IDs |
| Exclusions | `X_id` | exact tuple | 0–5 个 ending entries | 每个更高优先级结局及其规范 cause IDs |
| Unresolved tokens | `U_id` | exact tuple | 0–10 项 | 按首次 revoke history index 后 stable ID 排序 |
| Outcome signature | `O` | exact immutable record | 1 项 | ending selection、character fates、cost bearers、tragedy closure |

**Output Range:** 每个合法 terminal path 恰对应一个 class key。任何字段不同都产生不同 class，不得因 ending ID 相同而合并。

**Example:** 两条路径都得到 `see_the_sea`，但一条由路明非承担身份代价、另一条由盟友承担掩护代价，则 `cost_bearer_outcome_ids` 不同，必须属于两个 terminal-cause classes。

### Resolver Complexity Contract

The `resolver_complexity_contract` formula is defined as:

`Time = O(B_in + P + Q + C + B + L·R log R + L·F log F + K log K)`

`Space = O(B_in + P + Q + C + B + R + F + K)`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| History items | `H` | exact int | 0–content bound | ordered choice count |
| Input bytes inspected | `B_in` | exact int | 0–content bound | snapshot keys、axis/history IDs 与被查验 catalog IDs 的 UTF-8 bytes；覆盖字符串 hash/equality/format 成本 |
| Projection effects | `P` | exact int | 0–catalog bound | applied axis/event/resource effects |
| Qualification inspections | `Q` | exact int | 0–catalog bound | source checks与冻结 contributors |
| Evaluated clauses | `C` | exact int | 1–predicate bound | 到 selected ending 为止的完整 clauses |
| Encoded bytes | `B` | exact int | 0–record bound | cause canonical encoding bytes |
| Max ID byte length | `L` | exact int | ≥1 | `max(1, 被排序 source/fact stable ID 的最大 UTF-8 byte length)`；空集合时固定为 1 |
| Cause-ready references | `R` | exact int | 0–record bound | 含 qualification contributor references |
| Fact IDs | `F` | exact int | 0–record bound | 输出 event/resource/qualification IDs |
| Emitted causes | `K` | exact int | ≥1 | matched、unresolved 与 exclusion causes |

**Output Range:** 不设玩家可调数值；必须保持在上述渐进界限内，且不得宣称排序阶段为线性时间。

**Example:** 当 history 与 cause 数量翻倍、ID 最大字节长度不变时，fold 部分近似线性增长，排序部分按 `N log N` 增长；不得通过 mutable cache 或外部索引规避纯度边界。

`unresolved_counterevidence` 与 resource fold 的具体公式继续以 SYS-STATE GDD 为唯一来源，本节只消费其输出。

*复杂度合同只批准渐进形式；实际内容上限与 benchmark profile 由 Q5/Q7 provisional downstream gates 冻结。*

## Edge Cases

- **If snapshot root、axes、history 或任一 schema-known scalar 不是规定的 exact CPython built-in type**：在 snapshot type sweep 抛出 `TypeError`；不访问自定义 protocol，也不运行后续阶段。
- **If snapshot 的 exact types 合法，但 schema version、键集、轴顺序、轴范围、history ID 格式或唯一性非法**：在 snapshot value/shape 阶段抛出 `ValueError`；不返回部分 record。
- **If snapshot 含额外未知键**：抛出 `ValueError`；不得忽略、保留或规范化未知内容。
- **If 调用者传入 Mapping/Sequence subclass 或自定义容器**：抛出 `TypeError`；不得转换为 dict/list 后继续。
- **If history 中任一 choice ID 未被 counterevidence 与 route-projection 冻结目录覆盖**：在 catalog coverage 阶段抛出 `ValueError`；fold 不得开始。
- **If history 全部有冻结记录，但按 choice axis projections 从零重放后的 axes 与 snapshot axes 不同**：在 catalog coverage + semantic replay 阶段抛出 `ValueError`；不得生成 axis contributors、token fold、fallback 或部分快照。`history=()` 与任一非零轴是该规则的最小负例。
- **If authoring catalog 含未知 repair target、wrong domain/mode、irreversible target 或非法引用**：在 import/build-time validation 失败并阻止目录冻结；这些缺陷不得成为 resolver runtime branch。
- **If build-valid repair 在目标尚未产生或已经解决后执行**：在 token fold 阶段抛出 `ValueError`；route facts 与所有后续阶段调用数为 0。
- **If route projection 对已持有资源再次 acquire**：在 route-fact fold 阶段抛出 `ValueError`；qualification 与后续阶段调用数为 0。
- **If route projection consume 当前未持有的资源**：在 route-fact fold 阶段抛出 `ValueError`；不得把资源状态修正为空集后继续。
- **If qualification 缺少 source、引用未知 choice/event/resource，或使用非法 operator/kind**：内容构建失败；不得生成半冻结 qualification index。
- **If 同一 terminal path 派生出两项以上 terminal route qualifications**：qualification derivation 抛出 `ValueError`，同时内容路径验证失败；固定 ending priority 不得用来掩盖互斥合同破坏。
- **If 某个 qualification 的 `all` source 中有一项为 false**：资格为 false，但仍检查并冻结全部 source truth 与 contributors。
- **If 某个 qualification 的 `any` source 中已有一项为 true**：资格为 true，但仍检查并冻结全部 source truth 与 contributors。
- **If autonomy 或 truth domain 暂无注册 token**：对应“全部 absent”条件按空集恒真处理；`golden_cage` 的“至少一个 unresolved autonomy token”恒假。
- **If `qualification_old_order_return_route` 成立但没有 unresolved autonomy token**：runtime 中 `golden_cage` predicate 为 false并继续到 fallback；内容路径验证同时将该 terminal route 标为语义矛盾并阻止内容冻结。
- **If 一条声明为 `her_own_name`、`see_the_sea`、`one_person_train` 或 `golden_cage` 的 witness 最终只命中 fallback**：内容路径验证失败；不得通过改写 witness 标签解决。
- **If `rain_stops` 与任何较低优先级 predicate 同时为 true**：选择 `rain_stops`；它不得因存在 route qualification 而失败。
- **If `rain_stops` 被选中，但 terminal path 同时携带 solo-departure/old-order-return qualification，或 outcome signature 缺少 ordinary-future / relinquished-power / relinquished-old-identity records**：runtime selection 保持确定，但 content compatibility validation 失败并阻止内容冻结。
- **If 两个其他合法 predicate 因未来目录修订发生重叠**：选择固定优先级更高者，并为所有在其之前但失败的结局生成完整 exclusions；目录修订还必须重新运行互斥与 witness 验证。
- **If 轴值恰好等于 predicate 阈值**：该 atomic clause 为 true；低 1 时为 false。
- **If 轴值小于 0 或大于 3**：输入非法并在 snapshot value/shape 阶段抛出 `ValueError`；不得当作普通 predicate failure。
- **If 所有前五个 ending roots 均为 false**：`unsent_postcard` 的 `always_true` root 成为唯一选择；constant matched cause 保留为 audit-only，display selection 必须从 frozen concrete failure/unresolved causes 选择具体 `fallback_decisive_loss` anchor。
- **If snapshot 本身非法**：不得进入 `unsent_postcard`；fallback 只对合法 snapshot 提供 totality。
- **If predicate tree 缺失唯一 root、形成 cycle、共享 child、clause order 不连续或使用非法 source/comparator**：构建失败并阻止 predicate catalog freeze。
- **If 已到达的 group predicate 可从首个 child 推断结果**：仍完整求值所有 children；每个 clause 的 observation count 恰为 1。
- **If selected ending 没有 matched cause**：构建/测试失败；constant postcard match 仍必须存在于审计 record。
- **If 非 postcard ending 没有 presentation-safe matched cause，或 postcard 没有 presentation-safe concrete failure/unresolved anchor，或任一候选 `player_summary_id` 缺失/重复/未通过 spoiler 与 anti-hidden-score 检查**：summary catalog freeze 失败；不得让 UI 临时过滤或用内部 ID 兜底。
- **If runtime cause payload 不同却产生相同 digest**：cause digest bijection validation 失败；不得截断 hash、随机加盐或选择其中一项。
- **If 多个 cause collections 引用同一 cause ID**：record validation 失败；每个 `display_cause_id` 必须在并集中恰好解析一次。
- **If 除 anchor 外没有其他可展示原因**：`display_cause_ids` 只包含一项；不得填充重复或泛化原因。
- **If 只有一个额外原因可用**：输出两项；不得为了固定长度补第三项。
- **If 候选原因超过两个**：按冻结 total-order 取最前两项；不得由章节脚本重排。
- **If 两条路径 ending ID 相同但 causes、exclusions、unresolved tokens、character fate、cost bearer 或 tragedy closure 任一不同**：生成不同 terminal-cause classes。
- **If 某个 reachable ending 没有 terminal-cause class 或 witness**：内容构建失败。
- **If 单个 ending 有 7–12 个 classes**：触发 Producer/Creative Director 范围复核，在完成复核前不得锁定内容。
- **If 单个 ending 超过 12 个 classes**：内容构建失败；不得通过合并不同 signatures 满足预算。
- **If `ENDING_LABEL_MAP` 与六项固定 label 任一缺失、重复、未知或目标 label 不存在**：构建失败；不得在运行时猜测目标 label。
- **If `ending_flow_sentinel/state` 缺失、类型错误、版本未知或 state 不属于 `"Active"`/`"Ended"`**：load/entry validation 进入 blocking safe flow；不得把缺失字段默认为 `"Active"`。
- **If resolver 抛出 `TypeError` 或 `ValueError`**：叙事流程保持 `Active`，不得进入任何 ending label，也不得写入 persistent/achievement。
- **If 已处于 `Ended` 时再次请求判定**：编排器拒绝请求且 canonical resolver call count 为 0。
- **If 玩家回退到 ending entry 之前**：Ren’Py 恢复 `Active` 和对应 SYS-STATE snapshot；相同 snapshot 重算出深值相同的 record。
- **If 相同 snapshot 在不同 persistent、UI、章节 flag、系统时间或随机状态下求值**：结果必须深值相同，外部读取次数为 0。
- **If 调用者尝试修改 resolution record、nested tuple 或 frozen catalog**：分别抛出适用的 `AttributeError` 或 `TypeError`；后续解析结果不得改变。
- **If history 或 cause 数量达到内容上限**：仍按已批准复杂度完成判定；不得引入 mutable cache、I/O 或近似选择来规避成本。

*本节已纳入 2026-07-27 集中修订；定点封板只验证上述新增 oracle，不重新扩散领域审查。*

## Dependencies

### Dependency Map

| Dependency | Strength | Direction | Required Interface | Current Status |
|---|---|---|---|---|
| SYS-STATE | Hard runtime | SYS-STATE → SYS-ENDING | 经过 active validation 的 detached schema 2 axes+ordered-history snapshot；counterevidence fold contract；exact validation precedence | Approved |
| Ren’Py 8.5.3 / Day 7 adapter | Hard runtime | Engine → SYS-ENDING | rollback-owned live state、唯一 snapshot adapter、ending-ID-to-label mapping、`Active → Ended` 入口 | Engine pinned；adapter contract defined |
| SYS-SAVE | Hard integration | SYS-SAVE ↔ SYS-ENDING | save/load/rollback 后恢复一致的 semantic snapshot 与叙事流程；不得保存 resolver 临时状态 | Not Started；接口预定义 |
| SYS-CHOICE | Hard build-time | SYS-CHOICE → SYS-ENDING | stable choice declarations、axis/counterevidence/route-fact projections、reaction/payoff exact joins | Not Started；source bindings provisional |
| SYS-NARRATIVE | Hard content-build | SYS-NARRATIVE ↔ SYS-ENDING | event/resource/outcome/payoff records、qualification sources、canonical witnesses、terminal cause classes、ending labels | Not Started；内容锁定 blocker |
| SYS-TEST | Hard verification | SYS-ENDING → SYS-TEST | canonical/boundary vectors、九阶段 observation、purity closure、branch evidence、terminal-path enumeration | Not Started；core contract fixtures 可先建，production evidence provisional |
| SYS-PERSIST | Downstream required | SYS-ENDING → SYS-PERSIST | 进入 ending label 后的 stable ending ID；不得回读 persistent unlock 参与判定 | Not Started |
| SYS-ACHIEVE | Downstream required | SYS-ENDING → SYS-ACHIEVE | 已叙事完成的 event/ending outcome；不得读取轴、token emptiness 或 predicate | Not Started |
| SYS-JOURNAL | Downstream presentation | SYS-ENDING → SYS-JOURNAL | `journal_ending_catalog:v1`、中立display rank与跨class安全原因；不得自行重判 | In Revision；2026-08-03 Journal contract amendment待targeted validation |
| SYS-ACCESS | Cross-cutting required | SYS-ACCESS → ending presentation | 键盘可达、文本可读、非限时原因展示、0 ms reduced-motion、可访问summary semantic-fact边界；等价 choice 保留相同 semantic history | Designed；full re-review pending |

### Architecture Dependencies

- ADR-0001 固定六结局优先级、纯 resolver、structured record 与单一 canonical pass。
- ADR-0004 固定 detached snapshot、Ren’Py rollback 边界与 exact validation。
- ADR-0005 固定 counterevidence、route facts、qualification derivation、cause-ready artifact 与 purity closure。
- Core control-manifest rules是实现与验收的强制边界，不属于可调设计建议。

### Provisional Downstream Gates

SYS-ENDING 的批准分为两层：

- **Core resolver contract approval**：冻结输入/输出 schema、九阶段、axis replay、fold、qualification source-fact schema、predicate、cause identity、presentation-safe selection、lifecycle 与错误 oracle。可用 isolated frozen contract fixtures 实现和验证，不依赖生产内容 ID。
- **Production integration/content lock**：必须在 SYS-CHOICE/SYS-NARRATIVE 完成后通过以下 gates；在此之前状态只能是 `Approved with provisional downstream gates`，不得宣称 production content 已锁定。

以下字段必须由 SYS-CHOICE/SYS-NARRATIVE 后续提供，当前不得伪造占位 ID：

- 每项 qualification 的非空 `source_choice_ids`、`source_event_ids`、`source_resource_ids` 与 `derivation_operator`；
- 每个 production choice 的 exact axis/counterevidence/route-fact projection；
- choice-to-reaction/payoff exact joins、cardinality 与 proof-kind nullability；
- route-fact projection records；
- presentation-safe outcome references、payoff scenes 与玩家摘要；
- 每条合法 terminal path 的 witness 与 terminal outcome signature。
- maximum-content fixture、benchmark profile 与全 terminal-class enumeration。

这些 provisional bindings 不阻止 SYS-ENDING core resolver contract 获批或使用 isolated fixtures 实现；任何缺失都会阻止 production catalog freeze、正式内容锁定、端到端验收与发布。后续验证名为 `SYS-CHOICE/SYS-NARRATIVE → SYS-ENDING Cross-System Integration Validation`，不重开 SYS-ENDING 全文审查，除非下游要求修改已锁定 invariant。

### Bidirectional Consistency Requirements

- SYS-NARRATIVE 的系统索引依赖应更新为 `SYS-CHOICE + SYS-ENDING`，因为它既提供 ending content records，也消费 selected ending。
- SYS-TEST 的系统索引应明确包含 SYS-ENDING 验证依赖。
- SYS-SAVE GDD 必须引用 SYS-ENDING 的 `Active/Ended` rollback contract。
- SYS-PERSIST 与 SYS-ACHIEVE 必须把 `EndingResolutionRecord` 视为只读上游结果；SYS-JOURNAL 只消费 persistent ending membership 与 `journal_ending_catalog:v1`，不读取逐 traversal record。三者均不得建立反向判定边。
- SYS-CHOICE/SYS-NARRATIVE 若需要修改 qualification 语义或 predicate thresholds，必须同步修订本 GDD、ADR-0001/0005、registry 与 canonical tests。

## Tuning Knobs

### Designer-Adjustable Content Controls

| Knob | Target | Safe Range | Too Low | Too High | Required Validation |
|---|---|---|---|---|---|
| `terminal_cause_classes_per_ending` | 1–6 | 1–12 | 0 表示 reachable ending 缺少 witness、payoff 或 causal coverage，构建失败 | 7–12 触发 Producer/Creative Director 范围复核；超过 12 构建失败 | 全 terminal-path enumeration、signature uniqueness、payoff coverage |
| `qualification_source_bindings` | 最小且语义充分的非空 source set | 每项至少 1 个合法 choice/event/resource source | 空集或证据不足会使资格无来源或过易成立，构建失败 | 过多 source 会使路线不可达、contributors 膨胀或产生过多 terminal classes | reference integrity、route reachability、mutual exclusivity、canonical witnesses |
| `qualification_derivation_operator` | 按资格语义选择 `all` 或 `any` | 仅 `all` / `any` | 错用 `any` 会让单一偶然事实提前建立路线资格 | 错用 `all` 会让路线因非核心 source 缺失而不可达 | 全 source evaluation、边界路径、反事实 source-removal witnesses |

### Interaction Rules

- 修改 qualification source set 时，必须同时重跑四项 terminal route qualifications 的互斥验证。
- `all → any` 或 `any → all` 会改变 contributor sets、cause anchors 和 terminal-cause class identity，因此不是纯难度调整。
- 增加 narrative branches 不得通过合并 signatures 压回 class budget；应减少真实分歧、共享合法 payoff，或提交范围复核。
- 本节的可配置项不得创建 persisted qualification booleans，也不得把五轴、token 或 achievement 转换成路线代理清单。

### Locked Invariants

以下项目不是日常调参项：

- 六结局 ID 与固定优先级；
- `rain_stops` 的五轴全 3 且 unresolved set 为空；
- `her_own_name`、修订后的 `see_the_sea` token exclusions、修订后的 `one_person_train` loss gate、`golden_cage` 的已批准谓词阈值与资格语义；
- `unsent_postcard` 的 unconditional fallback；
- 五轴域 `0–3`；
- counterevidence token 总上限 10、每域上限 2、repair 一对一及无 positive `grant`；
- terminal route qualification 在合法 terminal path 上互斥；
- 九阶段判定顺序、catalog coverage 中的 axis semantic replay 及首个失败后的零调用要求；
- exact `TypeError`/`ValueError` 失败政策；
- canonical resolver 与 `.ending_id` wrapper 的单一路径；
- `display_cause_ids` 必含一个 presentation-safe selected-ending anchor 且总数为 1–3；除 postcard 外 anchor 必须 matched，postcard constant root 不得作为泛化首卡；
- cause identity、total ordering、record field order 与 deep immutability；
- resolver purity 与复杂度合同；
- SYS-ENDING 对 `Active → Ended` 的独占所有权、`ending_flow:v1` lifecycle 与六项固定 label map。

任何 locked invariant 变化都必须同步修订本 GDD、相关 ADR、control manifest、entity registry、canonical witnesses、boundary tests 与 purity/instrumentation evidence；仅修改数据文件无效。

## Visual/Audio Requirements

### Reveal Sequence

1. 进入 ending label 后，先以场景行为确认叙事结果，再显示结局名称。
2. 当前结局的 presentation-safe selected-ending anchor 作为首个原因；五个非 fallback ending 使用 matched cause，postcard 使用 concrete failure/unresolved cause；最多两个补充原因在自然停顿后依次出现。
3. 原因不得使用数值跳动、星级、评级、进度条或“成功/失败”音效表现。
4. 玩家可以按正常文本节奏推进、回看或跳过已读内容；动画与音频不得阻断输入。

### Ending Tone Direction

| Ending | Visual Direction | Audio Direction |
|---|---|---|
| `rain_stops` | 雨后空间重新打开，重点是可触碰的普通生活，而非力量或胜利奇观 | 从雨声过渡到克制的日常环境声；音乐只承担释然，不承担判定信息 |
| `her_own_name` | 清晰但保留距离感，以独立行动和仍可保持的联系为视觉核心 | 留白较多，使用分离后仍有回应的简短主题回声 |
| `see_the_sea` | 移动、开阔视野与不确定前路并存 | 交通与海风环境层优先；音乐表达共同承担而非安全抵达 |
| `one_person_train` | 空座、远离和仍在继续的旅程形成苦涩感 | 稳定行进声与逐渐拉远的主题；不使用死亡或失败提示音 |
| `golden_cage` | 表面温暖、构图受限；“安全”与失去自主同时可读 | 环境声被压窄或重复，但不得以刺耳效果惩罚玩家 |
| `unsent_postcard` | 未完成的物件与迟到的行动成为视觉锚点 | 保留雨声、纸张或空间空响；结尾完整收束而非突然中断 |

### Accessibility and Safety

- 每项原因必须有可读文本；颜色、镜头、音乐和音效只作补充。
- 静音、缺失音频、关闭动画或 reduced-motion 模式下，结局与全部原因仍可完整理解。
- 禁止强闪烁、突发惊吓、不可跳过的高强度震动或限时确认。
- 自动播放与跳过遵守全局设置；默认只跳过已读文本。
- 高对比度模式不得改变原因顺序或隐藏 matched-cause anchor。
- 所有最终视觉和音频资产必须使用原创或来源可追踪内容，并登记授权与替代文本。

*Art Director 与 Audio Director 未参与——Solo 模式；本节在资产制作前需结合 Art Bible 人工复核。*

## UI Requirements

### Presentation Flow

1. Ending scene establishes the narrative outcome.
2. Ending title appears as a non-interactive heading.
3. UI resolves `display_cause_ids` through the approved localized summary catalog and presents 1–3 inline cause cards in the supplied order.
4. Player advances each card with the normal dialogue controls.
5. After the final card, normal ending narration continues; no separate score-confirmation step is required.

### Cause Card Contract

Each card contains:

- one concise, player-facing causal statement；
- mandatory reference to a concrete remembered action、event、object、registered evidence absence or unresolved consequence；`unsent_postcard` 的首卡不得只表达“未命中其他结局”；
- semantic heading such as“你曾经做到的事”“仍未解决的事”或“另一条路为何没有发生”，而不是内部 cause kind；
- normal history/backlog text representation。

Cards must not expose:

- axis names or values；
- threshold comparisons；
- token、qualification、clause 或 cause IDs；
- percentage、rank、grade、route completion or “差几步”提示；
- locked-ending requirements or future-route spoilers；
- full exclusion matrix。

The first card always represents the selected ending’s presentation anchor. For five non-fallback endings it is a matched cause；for `unsent_postcard` it is a concrete failure/unresolved cause selected by the resolver while the constant matched cause remains audit-only. Additional cards may express another matched cause、an unresolved consequence or a higher-priority exclusion, but UI不得改变 resolver 提供的顺序、数量或 identity。

每个可进入 `display_cause_ids` 的 cause template 必须在 build-time summary catalog 中声明 `presentation_safe: true`，并通过三项检查：不含内部数值/ID；不泄露未到达 ending 的要求；在脱离开发 trace 时仍能独立解释已发生的玩家行为或后果。无法安全概括的 exclusion 固定为 `audit_only`，resolver 在候选阶段排除，而不是交给 UI 临时删卡。

### Layout and Interaction

- At 1280×720, ending title、current cause card and continue affordance must remain readable without overlap.
- Font scaling may reflow cards vertically; it must not truncate text or require pointer hover.
- Cause cards use normal keyboard focus and advance controls. Every action must be possible without mouse、timed input、sound or animation.
- One-card results display one card only; UI不得补空白卡或复制 anchor。
- Cards may appear sequentially, but reduced-motion mode uses immediate `0 ms` text replacement；dissolve、short fade或其他 substitute transition 均不允许。
- Backlog records only the text actually presented; it does not expose hidden record fields.
- Color may distinguish tone but never cause category or pass/fail meaning without a text label.
- Invalid resolver results never open this UI；错误处理保持在 blocking development/safe-flow boundary。

### Journal Handoff

After the player has legitimately reached an ending, SYS-JOURNAL may later expose:

- ending title；
- approved player-facing summary；
- `journal_ending_catalog:v1` 中对该 ending 全部 terminal classes 都成立的 1–3 个静态 cause summaries；
- unlock state if owned by SYS-PERSIST。

SYS-JOURNAL不得声称静态 summaries 是本次 traversal 的完整个性化原因，不得重新运行 resolver、读取当前 `display_cause_ids`、展示完整 predicate matrix、推导缺失阈值或泄露未到达结局条件。首发 root 不保存 completion date、逐 traversal cause IDs 或获得顺序。

*本节的 contract-level AC 已在集中修订中补齐；具体 flow、wireframe 与 visual treatment 仍由后续 `/ux-design` 完成，不阻止 resolver core approval。*

## Acceptance Criteria

除明确标为 production downstream gate 的项目外，所有 resolver component AC 使用一个 isolated frozen contract-fixture module：它包含引用完整的 choice axis/counterevidence/route projections、qualification bindings、predicate catalog 与 player-summary records，且只能在测试/设计验证构建中创建。Production resolver 仍不得暴露 catalog injection seam。每条 GIVEN 必须列出完整 axes、ordered history 与 fixture record IDs，不得直接注入 `qualification=true` 或把“更高 predicate 为 false”当作未证明前提。

### Deterministic Selection

| ID | Evidence | Criterion |
|---|---|---|
| `ENDING-FUNC-001` | `UT_PURE + INSTR` | **GIVEN** 完整 history 重放得到五轴全 3、unresolved set 为空，**WHEN** 调用 canonical resolver，**THEN** 选择 `rain_stops`，qualification read count 为 0且五轴 matched causes 均有真实 contributors。 |
| `ENDING-FUNC-002` | `UT_PURE` | **GIVEN** 完整 fixture history 重放得到 `(u,a,t,p,s)=(2,3,3,1,1)`、派生 independent-contact=true且无 unresolved autonomy/truth token，**WHEN** 求值，**THEN** trace 证明 `rain_stops` 因非全 3 失败并选择 `her_own_name`。 |
| `ENDING-FUNC-003` | `UT_PURE` | **GIVEN** 完整 fixture history 重放得到 `(1,2,1,2,2)`、派生 shared-escape=true且无 unresolved autonomy/truth/sacrifice token，**WHEN** 求值，**THEN** trace 证明前两项失败并选择 `see_the_sea`。 |
| `ENDING-FUNC-004` | `UT_PURE` | **GIVEN** 完整 fixture history 派生 solo-departure=true，且 `u≤1`、`p≤1` 或 unresolved understanding/preparation/truth token 至少一项，**WHEN** 求值，**THEN** trace 证明更高项失败并选择 `one_person_train`；移除全部 loss facts 后该 predicate 为 false。 |
| `ENDING-FUNC-005` | `UT_PURE` | **GIVEN** 完整 fixture history 派生 old-order-return=true且至少一个 autonomy token unresolved，**WHEN** 求值，**THEN** trace 证明前四项失败并选择 `golden_cage`。 |
| `ENDING-FUNC-006` | `UT_PURE` | **GIVEN** 完整 fixture history 使前五个 roots 均为 false，且 frozen evaluation 含具体 understanding/truth/preparation failure 或 unresolved/failed-commitment fact，**WHEN** 求值，**THEN** 选择 `unsent_postcard`，constant matched cause 为 audit-only，且 `display_cause_ids[0]` 是带 source/anchor 的既有 `fallback_decisive_loss` cause。 |
| `ENDING-FUNC-007` | `UT_PURE + INSTR` | **GIVEN** qualification 使用 `all` 或 `any` 且含多个 sources，**WHEN** 派生 truth，**THEN** 结果符合布尔公式，全部 sources 均被检查一次并冻结 contributors。 |
| `ENDING-FUNC-008` | `UT_PURE` | **GIVEN** 每个数值 atomic 分别处于阈值恰好命中和低 1，**WHEN** 求值，**THEN** 前者为 true、后者为 false；超出 `0–3` 则在 predicate 前抛出 `ValueError`。 |
| `ENDING-FUNC-009` | `UT_PURE` | **GIVEN** `rain_stops` 与一个或多个较低 predicates 同时为 true，**WHEN** 按固定 priority 求值，**THEN** 只选择 `rain_stops`。 |
| `ENDING-FUNC-010` | `STATIC + BRANCH` | **GIVEN** production terminal-path fixture 派生出两项以上 terminal route qualifications，**WHEN** 内容构建验证执行，**THEN** 构建失败且不冻结 content index。 |
| `ENDING-FUNC-011` | `UT_PURE + INSTR` | **GIVEN** 结构合法的 isolated runtime fixture 在 qualification stage 派生出两项以上资格，**WHEN** canonical resolver 执行，**THEN** 抛出 `ValueError`，predicate/cause/record stage counts 为 0。 |

### Validation and Fold Semantics

| ID | Evidence | Criterion |
|---|---|---|
| `ENDING-VALID-001` | `UT_PURE + INSTR` | **GIVEN** root、container、scalar 或 item 含 exact-type defect，**WHEN** 调用任一公共 resolver 入口，**THEN** 在固定首个 type stage 抛出同一 `TypeError`，后续 stage counts 全为 0。 |
| `ENDING-VALID-002` | `UT_PURE + INSTR` | **GIVEN** types 全部合法但 schema、键集、范围、ID 格式或 history 唯一性非法，**WHEN** 求值，**THEN** 在 value/shape 阶段抛出 `ValueError`，不运行 catalog coverage。 |
| `ENDING-VALID-003` | `UT_PURE + INSTR` | **GIVEN** history choice 缺少 counterevidence 或 route projection coverage，**WHEN** 求值，**THEN** 在 catalog coverage 阶段抛出 `ValueError`，两个 folds 均不运行。 |
| `ENDING-VALID-004` | `UT_PURE + INSTR` | **GIVEN** build-valid repair 的目标尚未产生或已解决，**WHEN** token fold 执行，**THEN** 抛出 `ValueError`，route-fact 与后续 stages 全为 0。 |
| `ENDING-VALID-005` | `UT_PURE + INSTR` | **GIVEN** resource effect 重复 acquire 或 absent consume，**WHEN** route-fact fold 执行，**THEN** 抛出 `ValueError`，qualification、predicate、cause 与 record stages 全为 0。 |
| `ENDING-VALID-006` | `STATIC + UT_PURE` | **GIVEN** catalog 含未知 repair target、wrong domain/mode、irreversible target 或非法引用，**WHEN** import/build validation 执行，**THEN** 冻结失败，runtime resolver 不存在对应 failure hook。 |
| `ENDING-VALID-007` | `STATIC + UT_PURE` | **GIVEN** predicate graph 有多 root、cycle、shared child、非连续 clause order 或非法 source/comparator，**WHEN** 构建 catalog，**THEN** 构建失败且不产生可用 index。 |
| `ENDING-VALID-008` | `UT_PURE` | **GIVEN**非法 snapshot，**WHEN**调用 resolver，**THEN**抛出规定异常；不得返回 `unsent_postcard` 或任何 fallback record。 |
| `ENDING-VALID-009` | `UT_PURE + INSTR` | **GIVEN** snapshot types/shape 合法且 history 全覆盖，但 axis projections 从零重放结果与 snapshot axes 不同，**WHEN** canonical resolver 执行，**THEN** 在 catalog coverage + semantic replay 抛出 `ValueError`，token/route/qualification/predicate/cause/record counts 全为 0。 |

### Trace, Causes, and Record

| ID | Evidence | Criterion |
|---|---|---|
| `ENDING-CAUSE-001` | `INSTR` | **GIVEN** 合法 snapshot，**WHEN** priority evaluation 运行到 selected ending，**THEN** 从最高优先级到 selected ending 的每个 reached clause 恰执行一次，未到达的低优先级 clauses 执行 0 次。 |
| `ENDING-CAUSE-002` | `UT_PURE + INSTR` | **GIVEN** priority stage 完成，**WHEN** cause extraction 运行，**THEN**其唯一输入为 `FrozenResolutionEvaluation`，snapshot、history、catalog 与 evaluator 读取次数均为 0。 |
| `ENDING-CAUSE-003` | `UT_PURE + STATIC` | **GIVEN**合法结果，**WHEN**检查 `EndingResolutionRecord`，**THEN** module、qualname、field order、nested tuple types 与排序全部符合冻结 schema，任何 mutation attempt 失败。 |
| `ENDING-CAUSE-004` | `UT_PURE` | **GIVEN** 同时含 presentation-safe 与 audit-only 的 matched、unresolved、exclusion causes，**WHEN**构造 `display_cause_ids`，**THEN**非 postcard 第一项为首个 safe matched cause；postcard 第一项按专用顺序来自 concrete failure/unresolved causes；总数为 1–3，audit-only 从不入选且无重复。 |
| `ENDING-CAUSE-005` | `UT_PURE` | **GIVEN** selected ending 之前存在失败的高优先级 endings，**WHEN**构造 record，**THEN**每个高优先级 ending 恰有一个 nonempty exclusion entry，顺序与 priority 一致。 |
| `ENDING-CAUSE-006` | `UT_PURE` | **GIVEN** unresolved tokens，**WHEN**构造 record，**THEN**每个 token 恰有一个 audit cause，按 revoke history index 后 stable ID 排序。 |
| `ENDING-CAUSE-007` | `UT_PURE + STATIC + BRANCH` | **GIVEN**批准的 known-answer vectors、全部当前 production payload 枚举及 independent synthetic collision pairs，**WHEN**编码并计算完整 SHA-256、再运行 build-layer bijection checker，**THEN**固定 hashes 匹配、当前枚举中 canonical bytes 与 digest 均无冲突、unequal payload/same digest synthetic fixture 被拒绝；不得声称有限样本证明 SHA-256 全域双射。 |
| `ENDING-CAUSE-008` | `UT_PURE` | **GIVEN**同一 ending 的两条路径在 causes、exclusions、unresolved tokens 或 outcome signature 任一字段不同，**WHEN**计算 class key，**THEN**得到两个不同 terminal-cause classes。 |
| `ENDING-CAUSE-009` | `UT_PURE` | **GIVEN**深值相同的合法 snapshot，**WHEN**重复调用 canonical resolver，**THEN**返回 deep-value-equivalent records，且无 mutable cache 改变结果。 |

### Purity and Entrypoints

| ID | Evidence | Criterion |
|---|---|---|
| `ENDING-PURE-001` | `UT_PURE + STATIC + BRANCH` | **GIVEN**相同 snapshot 与不同 store、persistent、UI、chapter flags、environment、time、random fixtures，**WHEN**求值，**THEN**records 深值相同且全部外部读取次数为 0。 |
| `ENDING-PURE-002` | `INSTR + STATIC` | **GIVEN**合法 snapshot，**WHEN**调用 `resolve_ending`，**THEN**canonical call count 恰为 1、field reads 恰为 `("ending_id",)`，wrapper 没有其他 helper edge。 |
| `ENDING-PURE-003` | `STATIC + BRANCH` | **GIVEN**production resolver 的完整传递 callgraph，**WHEN**按 purity policy v2 分类 explicit、implicit、constructor 与 exception edges，**THEN**所有 edges 均在 allowlist，任何 unresolved/custom/native dispatch 精确定位并失败。 |
| `ENDING-PURE-004` | `STATIC` | **GIVEN**production 与 source-hash-verified instrumented AST，**WHEN**比较 CFG 与 expressions，**THEN**唯一差异为 observation callbacks，production 不 import test source。 |
| `ENDING-PURE-005` | `INSTR + STATIC` | **GIVEN**非法 snapshot，**WHEN**调用 `resolve_ending`，**THEN**canonical call count 恰为 1、field reads 为空 tuple、原始 `TypeError`/`ValueError` 原样传播，wrapper 没有 fallback 或其他 helper edge。 |

### Engine and Flow Integration

| ID | Evidence | Criterion |
|---|---|---|
| `ENDING-INTEG-001` | `UT_ENGINE` | **GIVEN**`ending_flow_sentinel="ending_flow:v1"`、state=`"Active"` 且 snapshot 合法，**WHEN**`day7_resolve_ending` 求值，**THEN**canonical resolver 只调用一次并 jump 到固定 mapping 的唯一 label。 |
| `ENDING-INTEG-002` | `UT_ENGINE + STATIC` | **GIVEN**六个固定 ending IDs/labels，**WHEN**扫描 `ENDING_LABEL_MAP` 与 source callsites，**THEN**映射完整、一对一、目标 labels 全存在，且只有 `day7_resolve_ending`/`commit_ending_entry` 拥有 resolve/entry 入口；每个 ending label 恰有一个 terminal completion node 调用 `commit_ending_completion`。 |
| `ENDING-INTEG-003` | `UT_ENGINE` | **GIVEN**进入 mapping 对应 label 首句且 pending ID 匹配，**WHEN**调用 `commit_ending_entry`，**THEN**state 从 `"Active"` replacement-assigned 为 `"Ended"`，`semantic_state` 深值不变。 |
| `ENDING-INTEG-004` | `UT_ENGINE + INSTR` | **GIVEN**resolver、mapping 或 presentation preflight 抛出规定错误，**WHEN**orchestrator fail closed，**THEN**state 保持 `"Active"`，label/cause UI/persistent/achievement/journal call counts 全为 0。 |
| `ENDING-INTEG-005` | `UT_ENGINE + INSTR` | **GIVEN**state 已为 `"Ended"`，**WHEN**再次请求判定，**THEN**抛出 exact `RuntimeError("ending already committed")`，canonical resolver call count 为 0。 |
| `ENDING-INTEG-006` | `UT_ENGINE + UT_PURE` | **GIVEN**玩家回退到 ending entry 之前，**WHEN**Ren’Py 恢复 lifecycle、pending 与 snapshot 并重新求值，**THEN**state 为 `"Active"` 且 resolution record 与首次深值相同。 |
| `ENDING-INTEG-007` | `STATIC` | **GIVEN**SYS-PERSIST、SYS-ACHIEVE 或 SYS-JOURNAL consumer，**WHEN**扫描依赖方向，**THEN**它们只能读取获准输出，不存在反向写入 predicate、axis、token 或 qualification 的边。 |
| `ENDING-INTEG-008` | `UT_ENGINE + INSTR` | **GIVEN**save/load/quick-load fixtures 分别含合法 lifecycle、missing sentinel、unknown sentinel、wrong state type/value，**WHEN**load validation 执行，**THEN**合法 fixture 恢复 exact state/pending；其余进入 blocking safe flow且不能返回 loaded scene。 |
| `ENDING-INTEG-009` | `UT_ENGINE + STATIC + INSTR` | **GIVEN**六个 ending label 的 terminal completion node、completion event catalog 与 persistent request coordinator，**WHEN**分别覆盖 entry-before-completion、completion success、pre-write failure、commit-unknown、load 与 rollback，**THEN**completion callsite 恰为六个、entry-before-completion 的 request/assignment/flush 为 `0/0/0`、成功只提交 `ending_completed:{ending_id}` 一次，回退只恢复 rollback-owned event/control state，canonical membership 不被撤销，重放已存在 membership 返回 `DUPLICATE_NOOP`。 |

### UI and Accessibility

| ID | Evidence | Criterion |
|---|---|---|
| `ENDING-UI-001` | `UT_ENGINE + STATIC` | **GIVEN**分别含 1/2/3 个 approved `display_cause_ids` 的 records，**WHEN**渲染 ending cause flow，**THEN**卡片数量、identity、顺序与 record 完全相同，首卡为 safe selected-ending anchor且不补空卡。 |
| `ENDING-UI-002` | `STATIC + BRANCH` | **GIVEN**全部可展示 cause templates 与 localized summary catalog，**WHEN**运行 presentation-safety validator，**THEN**每项恰有一个 summary，不含轴/阈值/内部 ID/未来 ending requirement；fallback anchor 引用具体行为、证据缺失或未解决后果。 |
| `ENDING-ACCESS-001` | `UT_ENGINE` | **GIVEN**1280×720、最大批准字体缩放与 keyboard-only 输入，**WHEN**推进 1/2/3 卡 flow，**THEN**标题、正文与 continue affordance 无截断/重叠，所有动作无需鼠标、hover 或限时输入。 |
| `ENDING-ACCESS-002` | `UT_ENGINE` | **GIVEN**静音、missing-audio、reduced-motion、高对比度四组 fixtures，**WHEN**呈现同一 record，**THEN**全部文本语义、card identity/order 与推进能力保持相同，无闪烁或不可跳过效果。 |
| `ENDING-UI-003` | `UT_ENGINE + STATIC` | **GIVEN**cause flow与journal/backlog consumers，**WHEN**记录已展示内容并提交ending unlock，**THEN**SYS-PERSIST只保存ending ID；display/journal cause IDs、contributors、complete exclusions、completion date与未到达ending条件写入数均为0。 |
| `ENDING-UI-004` | `STATIC + BRANCH + UT_PURE` | **GIVEN**`journal_ending_catalog:v1`与每个ending的全部terminal equivalence classes，**WHEN**验证每个`journal_cause_id`，**THEN**它在该ending全部classes的cause/outcome intersection中成立、scope属于两项允许enum、数量1–3、higher-priority exclusion与path-specific contributor命中数0；`journal_display_rank`唯一且与resolver priority/stable-ID UTF-8序均不相等。 |

### Provisional Downstream Content and Performance Gates

本节不计入 SYS-ENDING core resolver contract approval；它在 SYS-CHOICE/SYS-NARRATIVE 完成后由跨系统集成验证关闭。

| ID | Evidence | Criterion |
|---|---|---|
| `ENDING-CONTENT-001` | `STATIC + BRANCH` | **GIVEN**四项 qualifications，**WHEN**冻结内容 catalog，**THEN**每项具有非空、引用完整的 source bindings 与合法 operator，且所有 terminal paths 上互斥。 |
| `ENDING-CONTENT-002` | `BRANCH` | **GIVEN**全部合法 terminal paths，**WHEN**枚举求值，**THEN**每条路径恰解析为一个 ending、一个 terminal-cause class、至少一个 witness、一个适用 payoff 与一个玩家摘要。 |
| `ENDING-CONTENT-003` | `BRANCH` | **GIVEN**old-order-return qualification 为 true但无 unresolved autonomy token 的 terminal path，**WHEN**执行内容验证，**THEN**以语义矛盾失败，不允许内容锁定。 |
| `ENDING-CONTENT-004` | `BRANCH` | **GIVEN**每个 reachable ending 的 class 集合，**WHEN**检查预算，**THEN**1–6 通过、7–12 要求记录范围复核、超过 12 构建失败，且不同 signatures 从不合并。 |
| `ENDING-CONTENT-005` | `BRANCH + UT_PURE` | **GIVEN**六条 canonical witnesses 与每个 atomic threshold 的边界 witnesses，**WHEN**运行测试，**THEN**各自命中预期 ending，并正确记录 matched causes 与全部高优先级 exclusions。 |
| `ENDING-PERF-001` | `UT_PURE` | **GIVEN**Q7 冻结的 minimum hardware、build、timer、GC/background policy、warm-up discard、sample count、p95 algorithm、maximum-content fixture 与独立 `resolver_budget_ms`，**WHEN**运行 benchmark，**THEN**p95 不超过该 resolver 子预算且全部 records 深值相同；16.6 ms 整帧预算不得自动当作 resolver 子预算。 |
| `ENDING-PERF-002` | `STATIC + UT_PURE` | **GIVEN**按 `B_in/P/Q/C/R/F/K` 构造的 n/2n/4n fixtures 与 operation counters，**WHEN**分析 callgraph、比较次数、bytes 与 allocations，**THEN**增长符合已批准复杂度合同，不使用 I/O、network、mutable cache 或近似选择。 |

### Targeted Core Contract Closure

| ID | Evidence | Criterion |
|---|---|---|
| `ENDING-CLOSE-001` | `STATIC + UT_PURE` | Qualification schema、终局前语义、source-fact identity 与 isolated fixture 求值一致；production exact bindings 明确留在 Q1/Q2。 |
| `ENDING-CLOSE-002` | `UT_PURE + BRANCH` | 六 predicate boundary fixtures 与 terminal-compatibility negative fixtures得到规定 selection/build-fail oracle。 |
| `ENDING-CLOSE-003` | `UT_PURE + INSTR` | axes/history replay 相等时 contributors 完整；不等时在第三阶段停止。 |
| `ENDING-CLOSE-004` | `STATIC + BRANCH` | class-key 算法与 1–6/7–12/>12 oracle 已冻结；实际枚举明确属于 Q5 integration gate。 |
| `ENDING-CLOSE-005` | `UT_ENGINE + STATIC` | presentation-safe selection、fallback concrete anchor、lifecycle/label map、合法/非法 wrapper 与 performance ownership AC 均无循环或不可证全称声明。 |

## Open Questions

| ID | Open Question | Owner | Target Date | Closure Evidence |
|---|---|---|---|---|
| `ENDING-Q1` | **Provisional downstream gate**：四项 terminal route qualifications 的 exact `source_choice_ids`、`source_event_ids`、`source_resource_ids` 与 `all/any` operator 分别是什么？ | SYS-CHOICE + SYS-NARRATIVE / Andwey | SYS-CHOICE/SYS-NARRATIVE 设计期 | 四项 build-valid records、reference-integrity report、互斥 terminal-path witnesses |
| `ENDING-Q2` | **Provisional downstream gate**：Choice declarations、immediate reactions、later payoffs、proof-kind nullability 与 reverse event metadata 的 exact joins/cardinality 如何冻结？ | SYS-CHOICE + SYS-NARRATIVE / Andwey | SYS-CHOICE/SYS-NARRATIVE 设计期 | schema、join validator、missing/duplicate/orphan negative fixtures |
| `ENDING-Q3` | **Provisional downstream gate**：最多 10 个 route-critical revoke tokens 的具体 IDs、domains、consequences、resolution modes，以及 repair/irreversible evidence 是什么？ | SYS-CHOICE + SYS-NARRATIVE / Andwey | SYS-NARRATIVE 内容期 | Counterevidence catalog、repair witnesses、irreversible approvals、agency/payoff evidence |
| `ENDING-Q5` | **Provisional downstream gate**：全部合法 terminal paths 将形成多少 terminal-cause classes；每个 class 的 outcome signature、witness、payoff 与 player summary 是什么？ | SYS-CHOICE + SYS-NARRATIVE + SYS-TEST / Andwey | 两系统设计完成后 | 全图 enumeration report、逐 ending class forecast、1–6/7–12/>12 verdict |
| `ENDING-Q6` | **Provisional downstream gate**：每个 cause template 与 terminal class 的最终 presentation-safe 玩家摘要、原因卡标题及简体中文文案是什么？ | SYS-NARRATIVE + UX / Andwey | 内容与 UX 期 | Localized summary catalog、spoiler/anti-hidden-score review、cause-card UX spec |
| `ENDING-Q7` | **Provisional downstream gate**：最大 reachable fixture、minimum hardware/build/timer/GC/sample/p95 protocol 与独立 resolver 子预算分别是什么？ | SYS-TEST + Engine Programmer / Andwey | 最大内容可枚举后 | Benchmark manifest、n/2n/4n complexity report、p95 profile |

## Closed Decisions

| ID | Closed On | Decision | Evidence |
|---|---|---|---|
| `ENDING-Q4` | 2026-07-27 | Lifecycle 使用 detectable `ending_flow:v1` sentinel、rollback-owned exact `"Active"`/`"Ended"` state、固定六 label map、唯一 `day7_resolve_ending` 与 `commit_ending_entry`。2026-08-09 targeted closure 另冻结 `SYS-ENDING` owner、六个 terminal completion nodes、`ending_completion_event_record` 与 persistent/rollback 语义。 | States and Transitions；`ENDING-INTEG-001`–`009` |
| `ENDING-Q8` | 2026-07-27 | 已完成 game/system/QA/narrative/UX/engine/performance/creative-director 独立审查；采纳“核心因果架构保留、五项合同集中修订”的 senior synthesis。 | `reviews/deterministic-ending-resolution-review-log.md` |

上述 Q1/Q2/Q3/Q5/Q6/Q7 不属于未决 resolver 行为，而是明确的 provisional downstream gates。核心合同批准后，下一步进入 SYS-CHOICE；SYS-CHOICE/SYS-NARRATIVE 完成后执行一次跨系统集成验证，不重开 SYS-ENDING 全文审查，除非它们要求修改本 GDD 的 locked invariants。
