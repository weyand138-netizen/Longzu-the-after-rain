# 选择与因果记录

> **Status**: Approved with provisional downstream gates
> **System ID**: SYS-CHOICE
> **Author**: Andwey + Codex
> **Last Updated**: 2026-08-04
> **Implements Pillar**: 看见未说出口的话；温柔必须被挣来；悲剧也是完整答案
> **Review Mode**: Fixed-scope revision after full review
> **Upstream Contracts**: SYS-STATE Approved；SYS-ENDING Approved with provisional downstream gates
> **Targeted Closure**: 2026-07-28 fixed Required 1–7 — 7/7 PASS；no new blocker categories admitted
> **Deferred Gates**: Agency transaction → SYS-NARRATIVE；accessible causal presentation → SYS-ACCESS/UX；Player Fantasy → no-debug playtest

## Overview

SYS-CHOICE 定义游戏中每个玩家叙事选项如何成为可追踪的因果决定：玩家确认选择后，系统以稳定身份记录该行为，连接当下可感知的角色反应、严格较晚的叙事回收，以及供 SYS-STATE 与 SYS-ENDING 使用的语义投影。它不直接决定结局或创作剧情结果，而是保证每次询问、隐瞒、准备、越界或承担都能在回退兼容的有序历史中被准确记住，并在未来得到具体回应，使玩家感到世界记得自己做过什么，而不是在操作隐藏分数。记录边界遵循 ADR-0001、ADR-0004 与 ADR-0005。

## Player Fantasy

玩家应感到自己不是在猜“正确选项”，而是在作出会被角色和世界记住的决定。一次选择的满足感来自两个相连的瞬间：当下，人物通过目光、动作、停顿或简短回应承认玩家的行为；后来，早先的询问、隐瞒、准备、越界或承担以具体情节结果重新出现，让玩家认出“这是我造成的”。

这种因果回收服务于“看见未说出口的话”“温柔必须被挣来”和“悲剧也是完整答案”：善意必须尊重对方的自主，代价不能被隐藏分数替代；即使走向失败，玩家也应理解自己的选择如何构成完整结局，而不是感到决定被系统抹去。

> 2026-07-28 creative-director已完成首次完整审查；Player Fantasy体验验证转为closed vertical slice无调试playtest下游门槛。

## Detailed Design

### Core Rules

1. **覆盖范围与选项分类**

   每次 production freeze 必须以一个 nonempty exact `production_choice_source_manifest_record` 作为唯一扫描宇宙：

   `manifest_id, scanner_contract_version, source_root_ids, generated_source_ids, exclusion_records, expected_chapter_ids, source_hash, owner_system`

   - `source_root_ids` 必须覆盖全部 production `.rpy/.py` 源、screen/action 声明及已批准的 generated content registries；`expected_chapter_ids` 必须非空且全部解析。
   - 每项排除必须是 exact `(source_id, exclusion_reason_id, approving_contract_id)`；test/dev-only、构建产物与第三方引擎文件只能通过已登记理由排除。未解析动态源、production→test-only 边或 manifest 外生产源均使扫描失败。
   - `scanner_contract_version` 冻结为 `choice_source_scanner:v1`。`source_hash` 是 lowercase full SHA-256 of canonical bytes：`encode(("choice_source_manifest_v1", scanner_contract_version, UTF8-byte-sorted (source_id, source_bytes_sha256), generated_source_ids, exclusion_records, expected_chapter_ids))`；不得使用时间戳、文件系统枚举顺序或截断 digest。
   - scanner 必须保存 exact manifest hash、scanner contract version、发现的 source/surface IDs及全部排除记录。空 source roots、空 expected chapters、零 discovered narrative surfaces 或 hash 不匹配均为构建失败。

   扫描发现的每个 production interaction surface 必须拥有稳定 `surface_id`，并恰有一个 exact `choice_surface_assignment_record`：

   `surface_id, surface_kind, target_kind, target_id, source_location_id, equivalent_to_surface_id_or_none, owner_system`

   `target_kind` 只能为 `player_choice` 或 `non_narrative_allowlist`。同一 `surface_id` 的 raw assignment 数必须恰为 1；不得先集合化再检查重复。

   发行构建中的每个玩家叙事选项，包括 `menu`、导向叙事节点的按钮或热点、限时结果及无障碍等价输入，其 assignment 必须解析到恰好一个 exact `player_facing_choice_record`：

   `choice_id, choice_node_id, choice_class, immediate_reaction_id, payoff_ids, owner_system`

   `choice_class` 只能是：

   - `semantic_major`：必须且只能关联一个 `major_choice_metadata_record`，可声明轴增量、反证效果与路线事实。
   - `narrative_only`：仍拥有稳定 `choice_id`、即时反应及非空 payoff 声明，但 `axis_deltas` 必须为空、`counterevidence_effect` 必须为 `null`。

   无障碍等价输入的 assignment 必须反向引用原 `surface_id`，并解析到同一 record 与 `choice_id`，不得创建新的语义分支。只有系统导航可进入 `non_narrative_interaction_allowlist`；章节内的行动、沉默、超时或路线选择不得豁免。

2. **唯一执行顺序**

   每次选择只能按以下顺序执行：

   `玩家确认 → SYS-STATE.apply_choice → immediate reaction → 后续控制流`

   - `semantic_major` 将声明的 exact `RunMap` 传给 `apply_choice`；`narrative_only` 传 empty `RunMap`。
   - history 提交成功后才能执行即时反应；反应完成前不得进入下一次 menu、jump/call、return、章节出口或 ending entry。
   - 提交与反应之间不得设置玩家可访问的保存点或产生其他交互边界。
   - `APPLIED` 是正常执行结果。`DUPLICATE_NOOP` 只能作为幂等防线，不得再次发出反应；任何生产可达的 duplicate path 都属于构建或流程验证失败。
   - SYS-CHOICE 不得直接修改 axes 或 `choice_history`，也不得绕过 `apply_choice`。

3. **每项选择的语义投影**

   每个正式 `choice_id` 必须恰有一个 immutable `choice_semantic_projection_record`：

   `choice_id, axis_deltas, completed_event_ids, resource_effects`

   - `axis_deltas` 按五轴 canonical order 编码为 exact tuple；每项增量固定为 `1`，最多涉及两轴，并与传给 `apply_choice` 的 declaration 深值相等。
   - 每个 choice 在 counterevidence catalog 中也必须恰有一项：`null`、一个 `revoke`，或一个定向 `repair`。单项选择不得携带多个 effect，也不存在 `grant`。
   - `completed_event_ids` 与 `resource_effects` 均必须显式存在，可以为空。`resource_effects` 必须为 exact tuple；每项必须复用 SYS-STATE 已批准的 exact `route_resource_effect_record(resource_id, operation)`，其中 `operation` 只能为 `acquire` 或 `consume`。不得接受裸 pair、dict 或其他结构等价替代。
   - `narrative_only` 的 axis projection 必须为空、counterevidence projection 必须为 `null`；event/resource 项仍须显式声明。非空项只表达具体路线事实，不构成隐藏分数或 `semantic_value`。
   - event/resource ID 必须已登记；同一 projection 不得重复 axis、event 或 resource。路径不得重复 acquire 已持有资源，也不得 consume 不存在的资源。
   - 全部记录由offline compiler验证并生成source-hash-bound compiled artifact；runtime import只执行有界schema/hash验证后建立private immutable indexes。运行时history中只保存`choice_id`，不保存派生事件、资源、token或资格布尔值。

4. **Choice → Reaction 一对一 exact join**

   每个 choice 必须恰有一个 `choice_reaction_binding_record`：

   `reaction_binding_id, choice_id, choice_node_id, reaction_id, reaction_event_id, reaction_node_id, owner_system`

   - choice record 的 `immediate_reaction_id` 必须与 binding 的 `reaction_id` exact-equal。
   - 每个 `choice_id`、`reaction_binding_id`、`reaction_id` 与 `reaction_event_id` 在该连接中只能出现一次，不得共享或形成一对多连接。
   - reaction event metadata 必须反向引用同一 `choice_id` 与 `reaction_binding_id`。
   - CFG 必须证明 reaction event 在 commit 后执行，并在任何下一控制转移前 postdominate 对应 choice edge。
   - 缺失、重复、悬空、反向引用不一致或反应早于 commit，均使内容构建失败。

5. **Choice → Payoff 一对多及 continuation 证明**

   每个 choice 的 `payoff_ids` 必须为非空、内部唯一的 exact list。每个 `(choice_id, payoff_id)` 必须恰有一个 `choice_payoff_binding_record`：

   `causal_binding_id, choice_id, payoff_id, payoff_event_id, proof_kind, guard_reference_id_or_none, counterfactual_witness_id_or_none, outcome_reference_ids, owner_system`

   Proof-kind 可空矩阵冻结为：

   | `proof_kind` | Guard | Counterfactual witness | Outcome references |
   |---|---|---|---|
   | `history_guard` | 必须非空 | 必须为 `None` | 必须为空 tuple |
   | `counterfactual_outcome` | 必须为 `None` | 必须非空 | 若证明结果差异则非空；仅在证明 event 不发生时可为空 |

   `guard_reference_id_or_none` 只能解析到 exact `choice_history_guard_record`：

   `guard_reference_id, choice_id, payoff_event_id, predicate_kind, required_membership, false_path_event_count, owner_system`

   - `predicate_kind` 必须为 `history_contains_choice`，`required_membership` 必须为 exact `True`，`false_path_event_count` 必须为 exact `0`。
   - record 必须与 binding 的 `choice_id`、`payoff_event_id` 双向一致；生产 CFG 必须证明 false path 不发出该 event。

   `counterfactual_witness_id_or_none` 只能解析到 exact `choice_counterfactual_witness_record`：

   `counterfactual_witness_id, choice_id, prehistory_id, observed_continuation_id, alternate_choice_id, alternate_continuation_id, aligned_suffix_choice_ids, payoff_event_id, observed_event_occurs, alternate_event_occurs, observed_outcome_reference_ids, alternate_outcome_reference_ids, owner_system`

   - observed/alternate 路径必须共享同一 prehistory；`alternate_choice_id` 必须是同一 `choice_node_id` 下已登记且不同于 `choice_id` 的 sibling choice，只替换当前 choice，并在 `aligned_suffix_choice_ids` 上保持相同合法顺序。
   - `observed_event_occurs` 必须为 exact `True`。若 `alternate_event_occurs` 为 `False`，允许两组 outcome references 均为空；否则两组 nonempty registered outcome tuples 必须深值不同。
   - choice、continuation、event 与 outcome references 必须全部双向解析；悬空、错 owner、未对齐或只有文本/镜头差异均失败。

   每个 causal binding 还必须恰有一个 exact `choice_payoff_semantic_evidence_record`，不改变上游 binding record 的字段顺序：

   `payoff_evidence_id, causal_binding_id, choice_id, payoff_id, affected_subject_id, established_element_id, before_state_id, after_state_id, outcome_reference_ids, perceptible_summary_id, owner_system`

   `affected_subject_id`、`established_element_id`、before/after states 与 `perceptible_summary_id` 必须已登记；`before_state_id` 与 `after_state_id` 必须不同，或 `outcome_reference_ids` 必须含至少一个 registered outcome。该记录必须证明人物、物件、信息、承诺、资源或结局损失发生了玩家可感知的具体变化。只读取 history、只换文本/镜头/ID 或通用 later event 均不能通过。

   对每个 choice `c`、每个可达完整前史 `h` 及每条合法 terminal continuation `s`，必须至少存在一个 exact `choice_payoff_witness_record`：

   `witness_id, choice_id, prehistory_id, continuation_id, continuation_choice_ids, payoff_id, payoff_node_id, payoff_event_id, causal_binding_id, timing_kind, owner_system`

   - payoff 必须位于真实 continuation 上，严格晚于 choice，并且不晚于 ending entry。
   - 每个声明的 `payoff_id` 至少被一个属于同一 `choice_id`、同一 binding 且位于某个合法 `(c,h,s)` 的 witness 使用。
   - payoff event metadata 必须反向引用同一 `choice_id`、`payoff_id` 与 `causal_binding_id`。
   - 共享 event 可服务多个 choices，但每个 choice 必须拥有独立 binding、独立 semantic evidence，并由独立 history guard 或可观察的 registered outcome 差异证明因果关系。
   - 通用 later event、同节点反馈、单向引用或只改变文本而不改变登记结果的反事实均不合格。

6. **向 SYS-ENDING 提供 qualification sources**

   SYS-CHOICE 在构建期向 SYS-ENDING 提供：

   - 完整且唯一的 stable choice declarations；
   - choice → axis/counterevidence/event/resource 的冻结投影；
   - choice、event 与 resource 的 reference-integrity report；
   - 可由 ordered history 确定性重建的 completed-event set 与 resource-possession set。

   SYS-ENDING 继续拥有 exact `route_qualification_record`：

   `qualification_id, qualification_kind, source_choice_ids, source_event_ids, source_resource_ids, derivation_operator, owner_system`

   `source_choice_ids` 必须解析到 SYS-CHOICE catalog；event/resource sources 必须解析到已登记记录，并可由 choice projections 从同一 ordered history 重建。三组 source 的并集必须非空，operator 只能为 `all` 或 `any`。SYS-CHOICE 不保存或授予 qualification bool，也不读取 resolver predicate。

   本节冻结接口与验证责任；四项 terminal qualification 的具体 source IDs 仍由 SYS-CHOICE 与 SYS-NARRATIVE 在内容绑定阶段共同提交，作为 `ENDING-Q1` 的下游 gate。

7. **Rollback / Save / Load 连续性**

   `choice_history` 与 Ren’Py 叙事控制位置必须处于同一 rollback/save/load 时间线：

   - rollback 至选择前：移除该 choice 及其后续语义影响；重新选择时产生一次 `APPLIED` 和一次 reaction。
   - rollback 或 load 至 reaction 后：history 保留，已发生 reaction 不得再次发出。
   - load 至 payoff 前：history guard 与真实 continuation 仍能触发一次合法 payoff。
   - load 至 payoff 后：已发生 payoff 不得因恢复而重复发出。
   - 不得使用 persistent、独立 reaction/payoff ledger 或导入 Python mutable state进行补记或去重。
   - 构建验证必须覆盖选择前、reaction 后、payoff 前和 payoff 后四类恢复点，证明每次恢复后的单次合法 traversal 中 history、reaction 与 payoff既不丢失也不重复。

   四类恢复证据必须使用 exact `choice_restore_checkpoint_record`：

   `checkpoint_id, checkpoint_kind, control_location_id, state_sentinel, expected_history, expected_axes, target_choice_id, target_reaction_id, target_payoff_id_or_none, observation_horizon_id, owner_system`

   `checkpoint_kind` 只能为 `before_choice`、`after_reaction`、`before_payoff`、`after_payoff`。计数 spy 必须在恢复动作后清零，并只观察到 `observation_horizon_id`；不得把保存前已经发生的调用计入恢复 traversal。

8. **权限边界与禁止行为**

   SYS-CHOICE 只声明、提交并验证选择因果数据，不得：

   - 直接选择 `ending_id`、跳转 ending label 或触发 `Active → Ended`；
   - 修改、包装或建立第二条 resolver 判定路径；
   - 写入 persisted qualification、当前 token 集或其他可由 history 派生的缓存状态；
   - 将 `reaction_id`、`payoff_id`、文本差异、镜头差异或 ID 前缀当作 `semantic_value`；
   - 让普通正向选择自动清除 counterevidence；
   - 读取 persistent、achievement、章节 flag、背包或其他 live state参与结局语义；
   - 用缺失、重复、悬空或无法证明的记录降级运行；这些情况必须在冻结 catalog 前使构建失败。

9. **Ren’Py 可分析子集与 commit→reaction authoring contract**

   Production choice flow 只能使用 scanner contract 登记的 Ren’Py 8.5.3 子集：

   - 静态 `menu`、静态 label/local label、静态 `jump/call/return`，或使用唯一 rollback-aware `ConfirmChoice`/`Return(canonical_choice_id)` action 的 choice screen；
   - `.rpy` inline Python 仅可调用已登记的纯 helper 与 `SYS-STATE.apply_choice`；choice edge、commit→reaction region 与 payoff guard 内禁止 `jump expression`、`call expression`、`renpy.jump/call`、reflection/dynamic lookup、自定义 Python statement、`call_in_new_context` 及未登记 Action；
   - 自定义 choice screen 必须位于 base context，拥有稳定 screen/location ID、roll-forward data 与一次性 UI activation gate。所有输入只返回 canonical `choice_id`；语义提交只在返回后的 `.rpy` 控制流执行。

   每个 choice 必须使用以下逻辑模板：

   `choice interaction → disable repeated activation → return canonical ID → apply_choice → noninteractive reaction-state establishment → one bounded reaction presentation interaction with quick actions/save/load/rollback/skip disabled → first permitted checkpoint/control transfer`

   `Committed` 与 reaction-state establishment 之间不得出现 interaction。reaction presentation 期间不得保存；其完成后的下一合法 interaction 才是 `after_reaction` checkpoint。reaction 的事实 identity 由静态 reaction node与控制位置证明，不新增 semantic ledger。

   CFG normalizer 必须冻结 Ren’Py AST/lexer version与 hash，edge-split commit node、reaction node、正常/异常 exit及 first-transfer frontier。对每条 production choice edge，必须证明 commit dominates reaction，reaction 在所有正常路径上 postdominate commit，且在 frontier 前执行恰一次；任何未解析 edge 固定失败。

   `INSTR` 使用离线 compiler 插入的 test-only、source-hash-verified AST trace adapter。observer 位于测试 harness，不进入 store/persistent、发行包或 production imports；它记录 canonical confirmation、`APPLIED`/`DUPLICATE_NOOP`、reaction establishment、payoff node 与 control transfer identity。

10. **离线编译、输出敏感预算与 runtime import**

   Source scan、CFG/DAG、join、完整 `(c,h,s)` 枚举与 witness 验证只允许在离线 compiler 执行。发行包中的 runtime import 只读取 source-hash-bound compiled catalogs，执行有界 exact schema/hash验证并建立 immutable indexes；不得扫描源文件、枚举路径或执行外部 I/O。

   作者可以为相同因果条件的路径提交一个 `payoff_witness_template`，但 compiler 必须展开并验证每个 canonical `(c,h,s)`，不得合并不同 `choice_id`、payoff、registered outcome、terminal cause/loss 或玩家可感知 semantic evidence。完整编译硬预算冻结为：

   | Budget | Hard Maximum |
   |---|---:|
   | reachable terminal paths | `4096` |
   | expanded `(choice,prehistory,continuation)` triples | `65536` |
   | total `continuation_choice_ids` entries | `1048576` |
   | compiled witness artifact bytes | `67108864`（64 MiB） |

   任一预算超过上限必须在 witness expansion 前或最早可判定阶段以固定 error code 失败，不得截断、采样或静默合并。compiler 使用确定性顺序、shared-prefix traversal 与一次性 SCC/DAG、dominator/postdominator indexes；其复杂度必须为输出敏感 `O(B + V + E + W + Σ|s|)`，其中 `B` 为输入 bytes、`W` 为展开 witness 数。时间/硬件 benchmark 继续由 `CHOICE-Q10` 关闭，但不得修改上述内容硬上限。

   所有 build failure 使用 exact `ChoiceBuildValidationError`，并携带 exact：

   `error_code, stage, offending_ids, source_location_ids`

   每个 one-defect fixture 必须冻结首失败 stage、排序后的 offending IDs、`freeze_count = 0` 与 `published_index = None`；后续 validator counters 必须为 0。

> 2026-07-28 完整专项审查已完成；本轮只按固定 Required 1–7 修订并执行一次定点封板检查。

### States and Transitions

这些状态是用于内容验证与测试取证的概念阶段，不新增 persisted lifecycle enum。运行时事实源仍只有 Ren’Py 控制位置与 `semantic_state.choice_history`。

#### 状态定义

| 状态 | 定义 | 可稳定保存 |
|---|---|---|
| `Presented` | 玩家可见选项；history 尚不包含该 `choice_id` | 是 |
| `Confirmed` | 输入已规范化为唯一 `choice_id`，尚未提交 | 否；瞬时阶段 |
| `Committed` | `apply_choice` 返回 `APPLIED`；history 与 axis 写入已完成 | 否；必须立即进入 reaction |
| `Reacted` | 一对一绑定的即时 reaction event 已执行 | 是 |
| `Continuing` | 已允许进入后续叙事控制流，等待适用 payoff | 是 |
| `PaidOff` | 某个声明的 payoff 已在当前合法 continuation 上发生 | 是；每个不同 payoff 单独取证 |
| `Terminal` | 已到达 ending entry，当前 choice 的 continuation witness 义务全部满足 | 是；不等于游戏 ending lifecycle |

`PaidOff` 不是一次性终态。同一 choice 可以依次经历多次 `Continuing → PaidOff → Continuing`，但每个 `payoff_id` 在一次合法 traversal 中只能按其真实内容节点发生一次。

#### 合法转移

| ID | From → To | 触发条件 | 必须成立 |
|---|---|---|---|
| `CHOICE-T01` | `Presented → Confirmed` | 玩家确认普通、限时或无障碍等价输入 | 输入解析为该选项唯一 canonical `choice_id` |
| `CHOICE-T02` | `Confirmed → Committed` | 调用 `SYS-STATE.apply_choice` | 返回 `APPLIED`；重大选择使用声明的 delta，`narrative_only` 使用 empty `RunMap` |
| `CHOICE-T03` | `Committed → Reacted` | 执行 exact reaction binding | 不经过其他交互或控制转移；reaction event 恰执行一次 |
| `CHOICE-T04` | `Reacted → Continuing` | 即时反应完成 | 才可 menu、jump/call、return、离章或进入其他叙事节点 |
| `CHOICE-T05` | `Continuing → PaidOff` | history guard 成立，或已登记反事实绑定在真实路径上成立 | payoff 严格晚于 choice，event/binding 双向引用一致 |
| `CHOICE-T06` | `PaidOff → Continuing` | 当前 payoff 完成且 continuation 尚未结束 | 保留同一 ordered history，可等待其他 payoff |
| `CHOICE-T07` | `Continuing/PaidOff → Terminal` | 到达 ending entry | 对该 `(choice, prehistory, continuation)` 至少有一个有效 payoff witness；所有声明 payoff 均在全图中至少被使用一次 |

#### 恢复转移

| 恢复位置 | 恢复结果 |
|---|---|
| rollback/load 至选择前 | history 不含该 ID；重新进入 `Presented`，后续可重新产生一次完整 commit 与 reaction |
| rollback 至选择确认点 | 选择及其后续影响全部撤销；不得留下 axis、token、event/resource 或 payoff 残留 |
| 尝试恢复至 `Confirmed` 或 `Committed` | 不存在合法稳定检查点；提交与 reaction 必须处于同一无交互控制段 |
| load 至 reaction 后 | 从 `Reacted` 或 `Continuing` 恢复；不得重复 reaction |
| load 至 payoff 前 | 从 `Continuing` 恢复；到达绑定节点时正常发生一次 payoff |
| load 至 payoff 后 | 从 `PaidOff` 后的实际控制位置恢复；已经发生的 payoff 不得重放 |
| rollback 至 payoff 前 | 撤销该 payoff 及其后续流程；再次前进时可在新的 traversal 中重新发生一次 |
| unsupported/corrupt state | 不进入任何 SYS-CHOICE 状态；交由 SYS-STATE 的阻断式安全流程 |

反复载入同一个“payoff 前”存档后再次前进，每次恢复 traversal 都会重新到达一次 payoff，这属于预期重演；同一次 traversal 内重复触发才是违规。

#### 非法转移

- `Confirmed → Reacted`：绕过 `apply_choice`，禁止。
- `Committed → Continuing`：绕过即时反应，禁止。
- `DUPLICATE_NOOP → Reacted`：重复 history 不得产生第二次反应；生产可达时视为流程缺陷。
- `Presented/Confirmed → PaidOff`：即时或同节点伪回收，禁止。
- `Continuing → Terminal` 且缺少适用 witness：内容构建失败。
- 从任何状态直接进入 ending label 或写入 `Active → Ended`：越权，由 SYS-ENDING 拒绝。
- 通过独立 dedupe flag、persistent 或 imported mutable state修补非法转移：禁止。

### Interactions with Other Systems

#### 接口矩阵

| 系统 | 方向 | 数据与调用 | 所有权与禁止边界 | 状态 |
|---|---|---|---|---|
| Ren’Py 8.5.3 | Engine ↔ SYS-CHOICE | 提供 choice interaction、叙事控制位置及 rollback/save/load 恢复 | Ren’Py 拥有 live rollback state；SYS-CHOICE 不建立外部存档、后台任务或 imported mutable state | 已固定 |
| SYS-STATE | SYS-CHOICE → SYS-STATE | `apply_choice(choice_id, axis_deltas)`；接收 `APPLIED` / `DUPLICATE_NOOP` | SYS-CHOICE 拥有 declaration 与调用顺序；SYS-STATE 独占 validation、history、axes 与原子 replacement assignment | Approved |
| SYS-NARRATIVE | 双向，内容构建与运行时演出 | 提供 choice nodes、reaction/payoff events、event metadata、outcome references、continuation witnesses及 qualification source 内容；消费稳定 choice IDs执行演出 | SYS-CHOICE 拥有分类、schema、join/cardinality 和 graph validators；SYS-NARRATIVE 拥有具体文本、事件、节点及内容 records | Provisional / Not Started |
| SYS-ENDING | SYS-CHOICE → SYS-ENDING，构建期 | 提供冻结 choice declarations、axis/counterevidence/event/resource projections、qualification source reference integrity及 reaction/payoff join report | SYS-ENDING 独占 resolver、predicate、cause records、ending selection 与 `"Active" → "Ended"`；SYS-CHOICE 不向 resolver 注入 live catalog或运行时 callback | Core Approved；下游 gates provisional |
| SYS-SAVE | 双向恢复边界 | 恢复 Ren’Py 控制位置、state sentinel 与完整 `semantic_state` | 不为 choice/reaction/payoff增加独立 serialization 或 dedupe ledger；unsupported/corrupt load 交由阻断式安全流程 | Provisional / Not Started |
| SYS-ACCESS | SYS-ACCESS → SYS-CHOICE | 鼠标、键盘及已登记替代 activation映射到同一 canonical choice；self-voicing仅消费可读文本/因果摘要 | 等价 activation复用相同 `choice_id`、reaction 与 payoff coverage；self-voicing不得触发 confirmation；不得创建 scanner 外分支或读取隐藏轴 | Designed（完整复审待完成）；implementation evidence pending |
| SYS-TENSION | SYS-TENSION → SYS-CHOICE | post-MVP 可选限时模式把 timeout 结果映射为已声明的普通 choice record | 默认关闭；当前不进入 P0 Production；post-MVP 始终提供非限时路径，不得直接改轴、写 history、生成匿名“迟疑”状态或改变 ending predicate | Deferred to post-MVP |
| SYS-TEST | 只读验证 | 消费 source manifest、choice graph、冻结 catalogs、join reports、negative fixtures及 rollback/save/load traces | SYS-TEST 不注册生产 choice、不替换 catalog，也不向 resolver增加测试注入 seam | Required / Not Started |
| SYS-PERSIST / SYS-ACHIEVE / SYS-JOURNAL | 无直接判定接口 | 只能在叙事结果完成后消费其各自获准的下游事件或摘要 | 不得读取 choice axes、token emptiness、qualification 或 payoff coverage来反向改变选择与结局 | Explicit boundary |

#### SYS-NARRATIVE 联合所有权

SYS-NARRATIVE 为每个玩家叙事选项提交内容 records；SYS-CHOICE 在冻结前执行联合验证：

1. `player_facing_choice_record.owner_system` 必须为 `SYS-NARRATIVE`。
2. `semantic_major` 恰关联一个 major metadata；`narrative_only` 不得拥有 axis 或 counterevidence effect。
3. reaction binding 与反向 event metadata 必须形成一对一 exact join。
4. 每个 `(choice_id, payoff_id)` 恰有一个 causal binding；每个合法 `(choice, prehistory, continuation)` 至少有一个 witness。
5. event、resource、outcome、node 与 payoff references 全部解析且 owner 正确。
6. 任一缺失、重复、孤儿、wrong-owner 或 proof-kind nullability 错误都阻止 catalog freeze。

**Agency transaction 联合设计规则（SYS-NARRATIVE 下游门槛）**：涉及绘梨衣自主性的生产内容必须把 `request/answer/response` 建模为可追踪顺序。单纯“询问”只能完成 request/answer event，不得自动获得 autonomy delta；只有玩家随后接受、遵循或明确维护已登记 answer 的 choice，才可投影 autonomy 正向证据。忽视、替代或推翻 answer 的 choice 必须声明对应的零增量或 counterevidence。该规则由 SYS-NARRATIVE 内容设计与 SYS-CHOICE validation联合关闭，不阻止本轮 SYS-CHOICE合同封板。

具体叙事 records 未完成前，SYS-CHOICE 只能使用 isolated contract fixtures验证 schema，不得提交伪造的 production IDs。

#### SYS-ENDING 下游门槛

SYS-CHOICE 向 SYS-ENDING 提供两类构建产物：

- **运行时语义目录**：choice → axis/counterevidence/event/resource 的 private immutable indexes，供 resolver 从 ordered history重放。
- **内容锁定报告**：完整 choice coverage、reaction/payoff exact joins、qualification source reference integrity及 terminal continuation witness coverage。

`ENDING-Q2` 的 choice-side schema、cardinality 和 proof-kind nullability由本 GDD 冻结；只有 SYS-NARRATIVE 提交完整 records 并通过 missing/duplicate/orphan fixtures 后才算联合关闭。

`ENDING-Q1` 的接口与引用规则由本 GDD 冻结；四项 terminal qualification 的具体 choice/event/resource IDs 与 `all/any` operator仍待 SYS-NARRATIVE 内容完成。不得用占位 ID提前宣称关闭。

#### 集成顺序

1. SYS-NARRATIVE 提交 choice、event、resource、reaction、payoff、semantic evidence与 outcome records。
2. SYS-CHOICE offline compiler 对 exact source manifest执行覆盖、schema、join、CFG/DAG、continuation、预算及恢复合同验证。
3. 验证通过后生成 source-hash-bound compiled catalogs、witness artifact与 reference-integrity reports；runtime import只执行有界 schema/hash验证。
4. SYS-ENDING 使用冻结产物执行 qualification、terminal-path和 cause-class验证。
5. SYS-TEST 完成最大路径枚举及跨系统恢复 fixtures。
6. 执行一次 `SYS-CHOICE/SYS-NARRATIVE → SYS-ENDING Cross-System Integration Validation`。

该流程不得重开 SYS-ENDING 全文审查；只有下游要求修改已锁定 resolver invariant时，才对受影响合同发起修订。

## Formulas

本系统不计算分数、权重、概率或成长曲线。所有公式均为构建期验证关系；SYS-STATE 与 SYS-ENDING 已定义的 replay/fold 语义只被引用，不在此重定义。

### Choice Surface Partition

The `choice_surface_partition_valid` formula is defined as:

`choice_surface_partition_valid(M,D_C,D_A,E) = manifest_valid(M) ∧ (|S(M)| ≥ 1) ∧ (surface_ids(D_C) ∪ surface_ids(D_A) = S(M)) ∧ (∀x ∈ S(M): count(D_C,x) + count(D_A,x) = 1) ∧ (∀e ∈ E: equivalent_input_valid(e,D_C))`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| source manifest | `M` | exact record | one production manifest | 冻结 source roots、expected chapters、exclusions、scanner version 与 source hash |
| discovered surfaces | `S(M)` | nonempty finite set | `1..N` stable IDs | 从 exact manifest 扫描发现的全部 production interaction `surface_id` |
| raw choice assignments | `D_C` | exact tuple | `0..N` records | `target_kind = player_choice` 的未去重 assignment records |
| raw allowlist assignments | `D_A` | exact tuple | `0..N` records | `target_kind = non_narrative_allowlist` 的未去重 assignment records |
| equivalent inputs | `E` | exact tuple | `0..N` records | 复用原 surface 与 canonical choice 的无障碍/替代输入 assignments |
| assignment multiplicity | `count(D,x)` | exact int | `0..N` | raw tuple 中 `surface_id == x` 的记录数，不得在计数前集合化 |

`manifest_valid(M)` 要求 source roots 与 expected chapters 非空、hash/version相等、所有 production/test边与 exclusions 已解析，且 scanner unresolved count 为 0。`equivalent_input_valid` 要求等价输入反向引用存在的原 surface，并与其解析到同一 canonical `choice_id`。

**Output Range:** exact `False` 或 `True`；空扫描、manifest不完整、未分类、raw duplicate、双重分类或等价输入悬空均为 `False`。  
**Example:** exact manifest扫描到14个 nonempty surfaces；raw assignments中11项指向 choices、3项指向 allowlist且每个 surface multiplicity恰为1；4个等价输入均反向引用原 surface并复用其 choice ID，则结果为 `True`。

### Semantic Projection Consistency

The `choice_projection_consistency_valid` formula is defined as:

`choice_projection_consistency_valid(h, a) = (∀c ∈ C: |Proj(c)| = 1 ∧ |Counter(c)| = 1) ∧ (replay_axes_SYS_STATE(h, Proj) = a)`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| catalog choices | `C` | finite set | `0..N` choice IDs | 全部正式 choices |
| ordered history | `h` | exact tuple | `0..|C|` unique IDs | 当前选择历史 |
| semantic projections | `Proj` | exact mapping | 每个 choice 恰一项 | axis/event/resource 投影 |
| counterevidence entries | `Counter` | exact mapping | 每个 choice 恰一项 | `null`、`revoke` 或 `repair` |
| snapshot axes | `a` | 5-tuple of exact int | 每项 `0..3` | SYS-STATE 当前五轴 |

**Output Range:** exact `False` 或 `True`；缺失/重复 projection 或 replay 后 axes 不相等时为 `False`。  
**Example:** 三项 fixture choices 分别提供 `understanding +1`、`autonomy +1`、`understanding +1`，其余轴为 0；SYS-STATE canonical replay 得到 `(2,1,0,0,0)`。当 snapshot axes 相同时结果为 `True`。

### Route Projection Legality

The `route_projection_replay_valid` formula is defined as:

`route_projection_replay_valid(h) = references_registered(h) ∧ events_union_valid(h) ∧ resources_stepwise_legal(h)`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| ordered history | `h` | exact tuple | `0..N` choice IDs | 按提交顺序排列的 history |
| completed events | `E(h)` | finite set | `0..N` event IDs | 对各 projection 的 `completed_event_ids` 求 union |
| resource possession | `R(h)` | finite set | `0..N` resource IDs | 按顺序执行 acquire/consume 后的集合 |
| resource operation | `op` | enum | `acquire` / `consume` | 当前路线资源操作 |

**Output Range:** exact `False` 或 `True`；未知引用、重复 acquire 或 absent consume 时为 `False`，且不得继续 qualification validation。  
**Example:** history 依次执行“取得车票、完成学校事件、消耗车票”，初始资源为空；所有引用已登记且每步合法，最终 event set 大小为 1、resource set 为空，结果为 `True`。

### Reaction Exact Join

The `reaction_join_valid` formula is defined as:

`reaction_join_valid(c) = (|R(c)| = 1) ∧ (reaction_id(R(c)[0]) = immediate_reaction_id(c)) ∧ reverse_match(R(c)[0])`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| choice | `c` | exact record | one catalog choice | 被验证的 choice |
| matching bindings | `R(c)` | finite set | `0..N` records | `choice_id == c.choice_id` 的 reaction bindings |
| reaction ID | `reaction_id` | exact string | one registered ID | binding 声明的反应 |
| reverse metadata match | `reverse_match` | bool | `False` / `True` | event metadata 是否反向匹配 choice 与 binding |

**Output Range:** exact `False` 或 `True`；binding 数不是 1、ID 不等或反向 metadata 不一致时为 `False`。  
**Example:** fixture choice 声明 `reaction_fixture_note_seen`，恰有一个 binding 指向同一 ID，event metadata 反向列出同一 choice/binding，则结果为 `True`。

### Payoff Exact Join

The `payoff_join_valid` formula is defined as:

`payoff_join_valid(c) = (|L_P(c)| ≥ 1) ∧ (|L_P(c)| = |unique(L_P(c))|) ∧ (∀p ∈ L_P(c): |B(c,p)| = 1) ∧ (|B(c)| = |L_P(c)|) ∧ (∀b ∈ B(c): proof_fields_valid(b) ∧ proof_reference_join_valid(b) ∧ |Evidence(b)| = 1 ∧ payoff_semantic_evidence_valid(Evidence(b)[0]))`

其中：

`proof_fields_valid(b) = history_guard_fields(b) XOR counterfactual_outcome_fields(b)`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| choice | `c` | exact record | one catalog choice | 被验证的 choice |
| raw declared payoff IDs | `L_P(c)` | exact list | `0..N` IDs | choice record中的原始 payoff list；唯一性检查前不得集合化 |
| matching bindings | `B(c,p)` | finite set | `0..N` records | 同时匹配 choice 与 payoff 的 bindings |
| all choice bindings | `B(c)` | finite set | `0..N` records | 该 choice 的全部 payoff bindings |
| proof-field validity | `proof_fields_valid` | bool | `False` / `True` | 是否满足唯一 proof-kind 可空矩阵 |
| proof-reference join | `proof_reference_join_valid` | bool | `False` / `True` | guard/counterfactual exact record、owner、event、choice及双向引用是否一致 |
| semantic evidence | `Evidence(b)` | finite set | `0..N` records | `causal_binding_id` 匹配的 payoff semantic evidence |

`payoff_semantic_evidence_valid(e)` 要求 `before_state_id != after_state_id` 或 nonempty registered outcomes，并要求 affected subject、established element 与 perceptible summary 全部解析；只有文本、镜头、ID或 history membership差异时为 `False`。

**Output Range:** exact `False` 或 `True`；空/重复 raw声明、缺失/重复/orphan binding、proof 字段不互斥、引用 record悬空或 semantic evidence缺失时为 `False`。  
**Example:** fixture choice 声明 2 个 payoff IDs，存在恰好 2 个 bindings：一个合法 `history_guard`、一个合法 `counterfactual_outcome`，则结果为 `True`。

### Continuation Payoff Coverage

The `continuation_payoff_coverage_valid` formula is defined as:

`continuation_payoff_coverage_valid = (∀c ∈ C, h ∈ H_reach(c), s ∈ L_terminal(c,h): |W_valid(c,h,s)| ≥ 1) ∧ (∀c ∈ C, p ∈ L_P(c): ∃h ∈ H_reach(c), s ∈ L_terminal(c,h), w ∈ W_valid(c,h,s): choice_id(w)=c ∧ payoff_id(w)=p ∧ binding_choice_id(w)=c)`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| choice | `c` | exact choice ID | one catalog choice | 当前 choice |
| reachable prehistories | `H_reach(c)` | finite set of exact tuples | `1..N` histories | 从 manifest entry到达 choice `c` 前的全部完整合法 ordered histories |
| legal terminal continuations | `L_terminal(c,h)` | finite set of exact tuples | `1..N` suffixes | 在完整前史 `h` 后选择 `c`，再到 ending entry 的全部合法 choice-ID suffix |
| applicable witnesses | `W_valid(c,h,s)` | finite set | `0..N` records | choice、hash、binding、真实 path、strict timing、reverse metadata与 semantic evidence均有效的 witnesses |
| declared payoffs | `L_P(c)` | exact list | `1..N` IDs | 同一 choice 的已验证 nonempty unique raw payoff list |

**Output Range:** exact `False` 或 `True`；任一合法三元组无 witness，或任一声明 payoff 从未被使用时为 `False`。  
**Example:** 一个 fixture choice 有 2 个 prehistories，每个各有 2 条 terminal continuations；四个组合的 witness 数分别为 `1,1,2,1`，并共同使用全部 2 个声明 payoff，则结果为 `True`。

### Restored-Traversal Occurrence

The `restored_traversal_occurrence_valid` formula is defined by checkpoint kind:

`restored_traversal_occurrence_valid(c,t,k) = counts(c,t) = expected_counts(c,k) ∧ (∀p ∈ L_P(c): N_payoff(c,p,t) ∈ {0,1})`

| `checkpoint_kind` `k` | `N_commit` after reset | `N_reaction` after reset | Required payoff observation |
|---|---:|---:|---|
| `before_choice` followed by confirmation | `1` | `1` | each payoff `0..1`; if horizon reaches terminal, sum ≥1 |
| `after_reaction` | `0` | `0` | only future bound payoff may be `0..1`; completed reaction stays 0；若horizon抵达terminal，future payoff总数≥1 |
| `before_payoff` | `0` | `0` | target payoff exactly `1` by its frozen horizon |
| `after_payoff` | `0` | `0` | already completed target payoff exactly `0` by next control boundary |

Rollback from `after_payoff` to a distinct `before_payoff` checkpoint starts a new observation window using the `before_payoff` row; it is not combined with the original load observation.

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| choice | `c` | exact choice ID | one catalog choice | 当前被观察的 choice |
| restored traversal | `t` | execution trace | restore 后 spy reset至 frozen horizon | 单次恢复后的实际流程；不含保存前调用 |
| checkpoint kind | `k` | enum | four frozen kinds | exact `choice_restore_checkpoint_record.checkpoint_kind` |
| commit count | `N_commit` | exact int | `0..N` | `APPLIED` 次数 |
| reaction count | `N_reaction` | exact int | `0..N` | 即时 reaction event 次数 |
| payoff count | `N_payoff` | exact int | `0..N` | 指定 payoff event 次数 |
| terminal reached | `terminal(t)` | bool | `False` / `True` | traversal 是否到达 ending entry |

**Output Range:** exact `False` 或 `True`；计数与 checkpoint row不符、同一 payoff在单个观察窗口重复，或 before-choice traversal抵达 terminal却没有 payoff时为 `False`。  
**Example:** reaction后存档载入时先清零 spy，再推进至下一个控制边界；commit与reaction均为0。若尚未到 payoff，所有 payoff也为0，结果为 `True`。

### Qualification Source Reference Integrity

The `qualification_source_binding_valid` formula is defined as:

`qualification_source_binding_valid(q) = (operator(q) ∈ {all,any}) ∧ (|Sc(q) ∪ Se(q) ∪ Sr(q)| ≥ 1) ∧ references_resolve(q) ∧ route_facts_derivable(q)`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| qualification record | `q` | exact record | one SYS-ENDING qualification | 被检查的 source binding |
| source choices | `Sc(q)` | exact tuple | `0..N` unique IDs | 必须解析到 choice catalog |
| source events | `Se(q)` | exact tuple | `0..N` unique IDs | 必须解析到 event registry |
| source resources | `Sr(q)` | exact tuple | `0..N` unique IDs | 必须解析到 resource registry |
| derivation operator | `operator(q)` | enum | `all` / `any` | SYS-ENDING 拥有的派生方式 |
| reference validity | `references_resolve` | bool | `False` / `True` | 所有 source 是否存在且类型正确 |
| derivability | `route_facts_derivable` | bool | `False` / `True` | event/resource 是否可从 choice projections 重建 |

**Output Range:** exact `False` 或 `True`；空 source 并集、非法 operator、悬空引用或依赖外部 live state 时为 `False`。  
**Example:** fixture qualification 使用 `all`，含 1 个 choice source 与 1 个可由该 choice projection取得的 resource source；所有引用已登记，则结果为 `True`。

> 2026-07-28 systems-designer已完成公式边界审查；本轮公式仅按固定Required清单定点修订。

## Edge Cases

### 选择发现与分类

- **If production source manifest 的 roots/expected chapters为空、hash/version不匹配、发现零叙事 surfaces或存在 unresolved/production→test-only edge**：扫描在分类前失败，报告 exact error record且不生成 catalog。
- **If 任一 production `menu` option、叙事按钮、hotspot、限时结果或等价输入未被分类**：内容构建失败，不生成 choice catalogs。
- **If 同一 `surface_id` 的 raw assignment 数不是 1，或同时指向 player choice 与 non-narrative allowlist**：内容构建失败；不得集合化后继续验证。
- **If 章节内的行动、沉默、超时或路线选择被放入 non-narrative allowlist**：内容构建失败；不得以“非重大”名义绕过因果覆盖。
- **If 两个 production declarations 使用相同 `choice_id`**：内容构建失败；不得按文件顺序覆盖。
- **If source scanner 无法静态解析动态 option、action、label 或 production→test-only reference**：内容构建失败；不得猜测目标或忽略该 surface。
- **If 无障碍等价输入映射到新的或不同的 `choice_id`**：内容构建失败；等价输入必须复用原始 choice record、reaction 与 payoff coverage。
- **If 紧张模式关闭**：场景只提供非限时 canonical path，不产生 timeout choice。
- **If 紧张模式开启并发生 timeout**：timeout 必须映射到预先登记的 canonical choice，并执行完整 commit→reaction→payoff 合同；不得匿名写入“迟疑”flag。

### 提交与执行顺序

- **If `apply_choice` 因 sentinel、state 或 payload 非法抛出 `TypeError`/`ValueError`**：不执行 reaction，不进入后续控制流，`semantic_state` 保持深值不变。
- **If production 可达路径收到 `DUPLICATE_NOOP`**：不发出第二次 reaction，并进入 fail-closed development boundary；该路径视为构建/流程缺陷，不得静默继续。
- **If `APPLIED` 后 reaction event 抛出未处理异常**：不得补偿性删除 history 或修改 axes；停止后续控制流并保留 rollback 恢复能力。
- **If 内容试图在 `Committed` 与 `Reacted` 之间显示菜单、暂停交互或建立可访问保存点**：静态 CFG 验证失败。
- **If ending lifecycle 已为 `"Ended"` 时仍尝试提交 choice**：active-state validation 拒绝写入；reaction、payoff 与 ending resolver 调用数均为 0。
- **If 同一玩家输入同时满足普通输入与 accessibility-equivalent handler**：先规范化为同一 canonical action，只允许一次 confirmation 与一次 `apply_choice`。

### 语义投影与目录

- **If `semantic_major.axis_deltas` 含非 canonical axis、非 `+1` 增量、重复 axis 或超过两轴**：构建失败，不冻结 projection。
- **If `narrative_only` 含非空 axis delta 或非 `null` counterevidence effect**：构建失败；不得自动升级分类或静默删除 effect。
- **If 一个 choice 含多个 counterevidence effects、`grant`、wildcard repair 或跨 domain repair**：构建失败。
- **If repair target 未产生、已解决或在任一可达 repair 前史中并非 unresolved**：路径验证失败；运行时防御性 fold 必须抛出 `ValueError` 并停止后续 stages。
- **If resource projection 使用裸 pair、dict或非 exact `route_resource_effect_record`，或 event/resource projection 含未知 ID、重复条目或非法 operation**：构建失败。
- **If 路径重复 acquire 已持有资源或 consume 不存在的资源**：内容路径验证失败；运行时 route fold 防御性抛出 `ValueError`，qualification 与后续 stages 调用数为 0。
- **If history 中任一 choice 缺少 projection 或 counterevidence catalog entry**：catalog coverage 失败；不得使用空默认记录。
- **If projection replay 与 SYS-STATE snapshot axes 不相等**：在 semantic replay 阶段失败；不得继续 token、route或 ending 判定。
- **If catalog 冻结后源 records、registry references 或 production source manifest发生变化**：旧构建产物失效，必须重新验证并冻结；不得热替换 private index。

### Immediate Reaction

- **If choice 没有 reaction binding 或拥有多个 reaction bindings**：内容构建失败。
- **If reaction ID、choice ID、binding ID 或反向 event metadata 任一不一致**：exact join 验证失败。
- **If 两个 choices 共享 reaction ID、reaction event ID 或 reaction binding ID**：一对一 cardinality 失败；必须拆分为独立记录。
- **If reaction event 未在全部 choice edges 上 postdominate commit，或可能在下一控制转移后发生**：CFG 验证失败。
- **If reaction 在 history commit 前发生**：执行顺序验证失败，即使最终 history 内容相同也不得接受。
- **If 绘梨衣的 reaction 通过完整口语解释玩家得分或正确性**：内容约束验证失败；必须改为视线、动作、停顿、物件操作或简单单音节。

### Later Payoff

- **If raw `payoff_ids` 为空或内部重复**：在建立任何 set view前内容构建失败。
- **If 任一 `(choice_id, payoff_id)` 没有 binding、拥有多个 bindings或存在未被声明的 orphan binding**：内容构建失败。
- **If `history_guard` 缺 guard、携带 counterfactual witness或拥有非空 outcome tuple**：proof-kind nullability 验证失败。
- **If `counterfactual_outcome` 缺 witness、携带 history guard，或空 outcome tuple 同时不能证明 event absence**：proof-kind nullability 验证失败。
- **If guard/counterfactual referenced record缺失、错 owner、choice/event不匹配、反向引用不一致或 counterfactual suffix未对齐**：proof-reference join失败。
- **If causal binding没有恰好一个 semantic evidence，或 evidence只证明history/text/camera/ID差异而没有registered subject/element state变化或 outcome**：内容构建失败。
- **If history guard 为 false 但 payoff event 仍发出**：因果绑定失败。
- **If history guard 为 true且 witness 声明 event 位于该路径，但 event 未发生**：该 continuation witness 无效，覆盖验证失败。
- **If counterfactual paths 只改变文本、镜头、reaction ID 或未登记状态**：不构成结果差异，binding 验证失败。
- **If 多个 choices 共享一个 payoff event，但没有逐 choice guard 或逐 choice registered outcome差异**：所有相关 bindings 均无效。
- **If payoff 与 choice 位于同一节点、紧邻 commit充当即时反馈，或发生在 choice 之前**：严格较晚约束失败。
- **If 任一声明 payoff 未被同一 choice、同一 binding且位于某个合法 `(c,h,s)` 的 witness 使用**：内容构建失败。
- **If 任一 `(choice, prehistory, legal terminal continuation)` 没有适用 witness**：内容构建失败；不得以其他 continuation 的回收代替。
- **If prehistory/continuation hash 与完整 ordered IDs 不匹配**：witness 被拒绝，不尝试规范化或重新猜测身份。
- **If choice graph 存在 cycle、悬空 edge 或无法到达 ending entry 的路径**：先使图构建失败，不运行 continuation coverage。

### Qualification Sources

- **If qualification 的三组 source IDs 并集为空、operator 不属于 `all/any` 或任一引用悬空**：reference-integrity validation 失败。
- **If source event/resource 不能从同一 ordered history 的 choice projections重建**：binding 无效；不得读取 live event manager、背包或章节 flag补足。
- **If qualification source 使用 axis 名、阈值、counterevidence domain、achievement或抽象“正确选择”标签**：内容构建失败。
- **If qualification 被保存为独立 bool或由 SYS-CHOICE 直接授予**：静态状态扫描失败。
- **If 同一 terminal path 派生出两项以上 terminal route qualifications**：内容兼容性验证失败；不得依靠 ending priority掩盖矛盾。
- **If `rain_stops` predicate 被添加 route qualification source**：锁定 invariant 冲突，停止集成并修订受影响合同；不得只改数据文件。

### Rollback / Save / Load

- **If rollback 至选择前**：choice ID、axis delta及其后续 reaction/payoff流程一并撤销；重新选择时重新执行一次完整 traversal。
- **If load 至 reaction 后**：恢复对应 history 与控制位置，reaction 不得再次发出。
- **If load 至 payoff 前**：恢复 `Continuing`；到达合法节点时 payoff在该 traversal 中发生一次。
- **If load 至 payoff 后**：恢复 payoff 后控制位置，已发生 payoff不得重放。
- **If rollback 至 payoff 前再前进**：payoff 可在新的 traversal 中再次发生；这不属于同一 traversal 内重复。
- **If 反复加载同一个 payoff 前存档**：每次恢复 traversal 均可重新看到 payoff；不得用 persistent dedupe导致后续载入丢失内容。
- **If loaded state 的 sentinel/schema 不支持或 state 损坏**：不恢复任何 choice lifecycle；进入 SYS-STATE/SYS-SAVE 阻断式安全流程。
- **If 检测到独立 reaction/payoff ledger、persistent choice state或 imported mutable rollback state**：静态验证失败；必须回到 Ren’Py 控制位置加 ordered history合同。
- **If restore instrumentation未在恢复动作后清零，checkpoint缺 exact control location/horizon，或把保存前调用计入当前 traversal**：该恢复证据无效。

### Source Compiler and CFG

- **If production choice 使用未登记 Action、dynamic jump/call、reflection、Python-defined statement、new context或 analyzer无法解析的 edge**：离线构建以 exact error code失败。
- **If commit→reaction region出现 interaction、save/load/rollback/skip入口或未登记控制转移**：CFG验证失败。
- **If choice screen不使用唯一 rollback-aware canonical-ID return gate，或允许多输入在同一 interaction重复 activation**：构建/engine fixture失败；不得依赖 `DUPLICATE_NOOP`修复。
- **If runtime import尝试扫描源文件、构建CFG、枚举路径、读取外部文件或超过有界 compiled-artifact validation**：静态边界与启动验证失败。
- **If terminal path、expanded triples、continuation-ID entries或compiled witness bytes超过任一冻结硬预算**：离线 compiler固定失败，不截断、不采样、不合并不同 semantic evidence。
- **If build failure未返回 exact error code/stage/sorted offending IDs/source locations，或失败后存在 published partial index**：build-error oracle失败。

### 变更与集成

- **If SYS-NARRATIVE 修改 choice、reaction、payoff、event/resource 或 outcome records**：重新运行完整 SYS-CHOICE catalog/join/path validation。
- **If 修改只改变文案且 stable IDs、metadata、控制流及 registered outcomes不变**：无需改变语义 projection，但仍运行内容约束和 source-manifest检查。
- **If 下游改动改变 qualification semantics、resolver stages、predicate、cause identity或 ending lifecycle**：视为 locked invariant变更，修订受影响 SYS-ENDING 合同、ADR、registry与 canonical tests。
- **If SYS-CHOICE 与 SYS-NARRATIVE 完成且未改变 locked resolver invariants**：只执行既定跨系统集成验证，不重开 SYS-ENDING 全文审查。

> 2026-07-28 systems/performance/engine专项已完成边界审查；后续只按Q6/Q10收集集成证据。

## Dependencies

### Dependency Map

| Dependency | Strength | Direction | Required Interface | Owner / Constraint | Current Status |
|---|---|---|---|---|---|
| Ren’Py 8.5.3 store/rollback | Hard runtime | Engine ↔ SYS-CHOICE | choice interaction、控制位置、rollback/save/load 恢复 | 引擎拥有 live state；选择提交与 reaction 必须处于同一无交互控制段 | Pinned |
| SYS-STATE | Hard runtime | SYS-CHOICE → SYS-STATE | `apply_choice(choice_id, axis_deltas)`；`APPLIED` / `DUPLICATE_NOOP` | SYS-STATE 独占 sentinel、axes、history validation 与 replacement assignment | Approved |
| SYS-NARRATIVE | Hard content-build | Bidirectional | choice declarations、nodes、reaction/payoff events、event metadata、outcomes、witnesses及 qualification source 内容 | SYS-NARRATIVE 拥有内容 records；SYS-CHOICE 拥有 schema、join、graph和 coverage validation | Not Started / Provisional |
| SYS-ENDING | Hard build-time | SYS-CHOICE → SYS-ENDING | immutable axis/counterevidence/route projections、qualification source integrity、join及 terminal coverage reports | SYS-ENDING 独占 resolver、predicate、cause、ending selection和 lifecycle | Approved with provisional downstream gates |
| SYS-SAVE | Cross-cutting runtime | Bidirectional | 恢复 semantic envelope 与叙事控制位置；执行 supported/unsupported/corrupt load classification | 不得增加 choice/reaction/payoff专用存档或 dedupe ledger | Not Started / Provisional |
| SYS-ACCESS | Cross-cutting input | SYS-ACCESS → SYS-CHOICE | 等价输入映射到 canonical choice record | 必须复用相同 ID、reaction及 payoff coverage；不读取隐藏语义 | Designed（完整复审待完成）；implementation evidence pending |
| SYS-TEST | Cross-cutting verification | Observe SYS-CHOICE | source scan、catalog、join、CFG、DAG、continuation及恢复 evidence | 不得注册生产数据、替换目录或增加 resolver test seam | Not Started / Required |
| SYS-TENSION | Optional extension | SYS-TENSION → SYS-CHOICE | post-MVP 将 timeout 结果映射为已登记 choice | 默认关闭；当前不阻断 P0；重新纳入时必须保留非限时路径且不得直接写 axes/history | Post-MVP deferred |
| Imported Python | Explicit technical boundary | Source-hash-bound immutable compiled data only | runtime只执行有界schema/hash验证并读取immutable compiled records；离线compiler拥有source/CFG/path工作 | runtime不得扫描源文件、执行外部I/O、枚举路径，或持有 live `RunMap`/`RunList`、控制位置、mutable rollback state | Fixed by ADR-0002/0004 |
| SYS-PERSIST | Explicit boundary | No semantic input | 仅处理已完成叙事产生的跨周目解锁 | choice、axes、token或 qualification不得跨周目保存 | Not Started |
| SYS-ACHIEVE | Explicit boundary | No reverse dependency | 只在叙事条件完成后消费获准事件 | 不得用 choice catalog或未解锁槽位形成隐藏语义代理 | Not Started |
| SYS-JOURNAL | Explicit boundary | Downstream presentation only | 可消费获准摘要或已完成事件 | 不读取 axes、token、qualification，也不重建 ending logic | Not Started |

### Governing Contracts

| Contract | Status | SYS-CHOICE Requirement |
|---|---|---|
| ADR-0001 — Deterministic Ending Resolution | Accepted | 不建立第二条 ending 判定路径；向 resolver提供确定性的冻结投影与 source lineage |
| ADR-0002 — Rollback and Persistence Boundary | Accepted | 每个玩家叙事选择在确认后、reaction 前经 `apply_choice` 提交；所有局内因果随 rollback/save/load |
| ADR-0004 — Semantic Ending Snapshot and Rollback State Envelope | Accepted | 只通过公共写入入口修改语义状态；projection replay 必须与 snapshot axes一致 |
| ADR-0005 — Counterevidence Ledger and Detectable State Initialization | Accepted | 反证只允许 null/revoke/定向 repair；目录构建后 immutable；禁止 `grant`与运行时 catalog seam |
| Control Manifest | Active implementation rules | 实现与内容验收必须同时满足 Required/Forbidden 条款；GDD不得将其降级为建议 |

### Dependency Ordering

正式内容的依赖顺序固定为：

`SYS-STATE → SYS-ENDING core contract → SYS-CHOICE schema/validators → SYS-NARRATIVE records → SYS-CHOICE catalog freeze → SYS-ENDING integration → SYS-TEST evidence`

其中：

- SYS-CHOICE 可使用 isolated fixtures完成 schema与 validator设计，不依赖生产 narrative IDs。
- SYS-NARRATIVE 在 SYS-CHOICE exact schemas冻结前不得锁定 choice/reaction/payoff records。
- Production catalogs 在 SYS-NARRATIVE records、双向 metadata及完整 continuation witnesses提交前不得冻结。
- SYS-ENDING 只能消费验证后的 immutable catalogs；不得在运行时向 SYS-CHOICE请求 callbacks或 live state。
- SYS-SAVE、SYS-ACCESS和 SYS-TEST 从第一段生产内容开始贯穿集成，不得推迟到内容完成后补接。
- SYS-TENSION 未完成不阻止 P0 非限时内容，但任何限时选项在其 GDD获批前不得进入 production catalog。

### Bidirectional Consistency Requirements

- SYS-STATE 必须继续把 SYS-CHOICE 视为唯一合法选择写入调用方；SYS-CHOICE 必须把 SYS-STATE 视为唯一语义状态写入目标。
- SYS-NARRATIVE 的 choice record、reaction/payoff metadata与 SYS-CHOICE compiled records必须按 exact IDs双向一致。
- SYS-ENDING qualification sources必须解析到 SYS-CHOICE declarations及可重建的 event/resource projections。
- SYS-SAVE 必须同时恢复 `semantic_state` 与正确叙事控制位置，不能只恢复其中一方。
- SYS-ACCESS与 SYS-TENSION只能规范化输入，不能创建旁路语义状态或改变 payoff义务。
- SYS-TEST必须把 SYS-CHOICE列为直接依赖；该索引关系已同步。
- 任一依赖要求修改 resolver stages、qualification semantics、predicate、cause identity或 ending lifecycle时，必须先修订对应 locked contracts；其余内容变更只重跑跨系统集成验证。

### Production Blockers

以下依赖不阻止 SYS-CHOICE 合同设计完成，但会阻止 production catalog lock：

- SYS-NARRATIVE 的完整 production records与 reverse metadata；
- 四项 terminal qualification 的具体 source bindings；
- 全部合法 continuation 的 payoff witnesses；
- SYS-SAVE 四恢复点集成证据；
- SYS-ACCESS 等价输入 coverage；
- SYS-TEST 的全图枚举、negative fixtures及最大内容 evidence。

## Tuning Knobs

SYS-CHOICE 没有全局分数倍率或运行时难度参数。可调项都是受 schema 限制的内容声明；任何调整都必须重新运行对应验证。

### Choice Authoring Knobs

| Knob | Owner | Allowed / Safe Range | 过低或最小值 | 过高或最大值 | Required Validation |
|---|---|---|---|---|---|
| `choice_class` | SYS-NARRATIVE | `semantic_major` / `narrative_only` | 过度使用 `narrative_only` 会使关键行为缺少正式语义证据 | 过度使用 `semantic_major` 会稀释重大选择并扩大验证图 | classification、major-metadata cardinality |
| `axis_deltas` | SYS-NARRATIVE + SYS-CHOICE | `0..2` 个 canonical axes；每项固定 `+1` | 全空可能使轴或结局不可达 | 每项都给两轴会过早封顶并削弱选择差异 | SYS-STATE replay、reachability、dominance |
| `counterevidence_effect` | SYS-NARRATIVE + SYS-CHOICE | `null`、一个 `revoke` 或一个定向 `repair` | 全部为 `null` 会让重大反向行为缺少持久后果 | 过密会增加 repair、agency及 terminal-class负担 | token cap、domain/mode、repair-path及 approval validation |
| `next_node_ids` | SYS-NARRATIVE | 非空、内部唯一、全部可解析 | 只有一个目标会减少后续路线差异 | 过多分支会扩大 continuation language与 witness 数量 | DAG、reachability、continuation enumeration |
| `risk_vector` | SYS-NARRATIVE | `physical/exposure/time` 各为 exact int `0..3` | 全 0 可能让选项在成本比较中异常占优 | 全 3 需要具体情节证明，否则成为伪高风险 | schema、evidence及 dominance validation |
| `resource_costs` | SYS-NARRATIVE | registered resource → nonnegative exact int | 全 0 表示无可消耗成本 | 超过实际可获得量会使路线不可达 | resource registry、path availability及 dominance |
| `character_costs` | SYS-NARRATIVE | 四个固定字段各为 exact int `0..3` | 全 0 仅适用于确无人物负担的行为 | 高值必须有可观察的人物后果 | schema、content evidence及 dominance |
| `unique_value_tags` | SYS-NARRATIVE | `0..N` 个已登记 `semantic_value` IDs | 空列表不能证明额外独特价值 | 标签过多不能抵消路线、成本或 token 劣势 | registry reference及 concrete evidence |
| `completed_event_ids` | SYS-NARRATIVE | `0..N` 个内部唯一 registered events | 空表示该 choice 不直接完成路线事件 | 过多会让单次行为承担不可信的路线语义 | reference、route reachability及 qualification impact |
| `resource_effects` | SYS-NARRATIVE | exact tuple；`0..N` 个唯一 `route_resource_effect_record`，operation为`acquire/consume` | 空表示不改变路线资源 | 过多会增加顺序错误与路线互斥 | exact-type、reference及stepwise resource legality |
| `payoff_ids` | SYS-NARRATIVE | `1..N` 个内部唯一 IDs；每项必须实际使用 | `0` 直接构建失败；只有 1 项时仍须覆盖全部 continuations | 数量增加会扩大 bindings、witnesses及内容维护成本 | join、declared-use及 continuation coverage |
| `proof_kind` | SYS-NARRATIVE + SYS-CHOICE | `history_guard` / `counterfactual_outcome` | 不存在默认值 | 滥用 counterfactual 会增加成对路径和 outcome evidence | nullability、guard或 counterfactual proof |
| `timing_kind` | SYS-NARRATIVE | `later_node` / `chapter_terminal` | 过早节点可能违反 strictly-later | 过晚且越过 ending entry 无效 | CFG ordering及 terminal-path presence |

`N` 不是任意无限预算，而是当前已登记且可达的有限内容集合。任何新增记录都受 terminal-class预算、完整witness coverage，以及4096 paths / 65536 triples / 1048576 continuation entries / 64 MiB artifact硬上限约束。

### External Knobs

| Knob | Owner | SYS-CHOICE Contract |
|---|---|---|
| timeout duration与警示方式 | SYS-TENSION | 本 GDD不设秒数；默认关闭并始终提供非限时路径。timeout结果必须映射到 canonical choice |
| accessibility presentation | SYS-ACCESS | 可改变输入方式、朗读及视觉提示；不得改变 choice ID、commit、reaction或 payoff semantics |
| qualification source sets | SYS-NARRATIVE + SYS-ENDING | choice/event/resource sources并集非空、引用完整且可从 history重建 |
| qualification operator | SYS-ENDING | 只允许 `all/any`；改变 operator会改变 contributors、cause identity与路线可达性 |
| reaction/payoff文案与演出 | SYS-NARRATIVE | 可改文本、动作、镜头和节奏，但不得改变 stable IDs、控制流或 registered outcome而不重跑验证 |
| terminal-class budget | SYS-ENDING + SYS-TEST | 每 ending `1–6` 正常、`7–12` 预警、`>12` 构建失败；SYS-CHOICE不得另设重复预算 |

### Locked Invariants — Not Tuning Knobs

以下值或行为不得由内容配置调整：

- 五轴 domain `0..3`、每次增量固定 `+1`、每项 choice 最多两轴；
- counterevidence 总 cap `10`、每 domain cap `2`、每 choice最多一个 effect；
- `semantic_major` / `narrative_only` 两类闭集；
- `确认 → apply_choice → reaction → 后续控制流`；
- choice → reaction 一对一 cardinality；
- choice → payoff 非空一对多及每条合法 continuation至少一个 witness；
- payoff 必须严格晚于 choice；
- raw `payoff_ids` 唯一性必须在任何 set view前验证；每个 witness必须绑定同一 choice/binding与一项 player-perceptible semantic evidence；
- production source manifest非空且source-hash-bound；同一 surface raw assignment恰为1；
- runtime import只验证compiled artifact，不执行source scan/CFG/path enumeration；
- 内容硬上限为4096 terminal paths、65536 expanded triples、1048576 continuation-ID entries与64 MiB witness artifact；
- ordered history为运行时权威，不保存独立 qualification、reaction或 payoff ledger；
- `DUPLICATE_NOOP` 不得触发 reaction；
- SYS-ENDING resolver、predicate、priority、cause identity及 `"Active" → "Ended"` lifecycle；
- 禁止将 reaction/payoff IDs当作未登记的 `semantic_value`。

改变上述任一项都属于合同修订，不是调参。

### Knob Interactions

- 增加 `next_node_ids` 会扩大 continuation language，并直接增加 payoff witness义务。
- 增加 `payoff_ids` 不会降低单条 continuation coverage；每个声明 payoff仍必须至少使用一次。
- 增加 axis delta不能修复 unresolved token；只有合法定向 repair可以移除 token。
- event/resource projections会改变 qualification source truth，必须重跑 terminal route互斥及 cause-class验证。
- `all → any` 或 `any → all` 会改变 cause lineage，不得视为普通难度调整。
- `unique_value_tags` 只能证明已登记的独特语义价值，不能抵消非法成本、不可达路线或缺失 payoff。
- 修改 reaction/payoff文案若不改变 IDs、metadata、控制流和 outcomes，只需内容约束复核；改变其中任一项必须重跑完整 joins与 path validation。

> 2026-07-28 systems-designer已完成调参边界审查；内容硬预算现为locked invariants。

## Visual/Audio Requirements

本节约束反馈语法，不锁定具体镜头、立绘、音频文件或场景资产。具体资产须待 SYS-NARRATIVE records 与 Art Bible 获批后定义。

### Choice Presentation

- 所有选项使用同一中性视觉层级。`semantic_major` 与 `narrative_only` 不得通过颜色、尺寸、位置、图标、边框、动画或音效暴露分类。
- 不显示“正确/错误”“善/恶”“关系上升/下降”、轴/token 图标、预测结局或数值变化。
- hover、focus、pressed 与 confirmed 只表达交互状态；同一状态在所有 choices 上使用同一套反馈。
- accessibility-equivalent input 必须呈现同一个 canonical choice，不得生成不同强调或确认演出。
- 确认后 UI 应清楚退场，但不得使用奖励粒子、全屏闪光、颜色判定或关系弹窗替代角色反应。

### Immediate Reaction

- 每个 choice 的 exact reaction 必须形成一个独立、可观察的微节拍，发生在 commit 后、下一控制转移前。
- 反应优先使用视线、姿势、呼吸与停顿、手部动作、人物距离或物件操作。
- 绘梨衣不得用完整口语解释玩家行为或正确性；只使用身体语言、目光、物件互动或简单单音节。
- 关键反应在静音状态下仍须可理解；声音若承载变化，必须同时存在可见动作、物件或环境结果。
- 不建立可复用的正向/负向奖惩 VFX。光晕、抖屏、色闪、粒子或提示音不得成为隐藏语义代理。
- rollback 至选择前时，pose、overlay、transition 与音频状态必须完整撤销；load 至 reaction 后不得重新播放。

### Later Payoff

- payoff 应让先前建立的具体元素再次出现并发生变化，例如物件状态、人物站位、重复动作、环境细节、构图或 registered outcome。
- 不显示“你的选择被记住了”等元提示；玩家应从场景关系中认出因果。
- 关键事实必须视觉可辨，声音只能加强回忆，不能成为唯一证据。
- 悲剧路线必须拥有与成功路线同等级的构图、动画和声音完成度；不得以统一去饱和、红闪或失败蜂鸣代替情绪闭环。
- 共享 payoff event 服务多个 choices 时，可观察差异必须来自已登记的动作、物件、人物关系或场景结果，不能只更换滤镜或提示音。
- payoff 的视听状态只能随真实叙事控制位置恢复，不得使用 persistent overlay、跨存档音轨或外部 VFX ledger 去重。

### Animation and Visual Style

- 微反应采用克制、清晰的 pose change 与短 hold；避免夸张表情符号、弹跳、QTE 成功动画或好感度闪光。
- 镜头保持观察者姿态，优先使用中近景、手部和物件细节、留白及人物间距离；不得用突兀特写替玩家判断道德意义。
- 雨势、光线与色彩可以表达氛围，但不得形成稳定的“某颜色＝某 axis/token/ending/正确性”编码。
- 收伞、递物、候车、整理衣物、停步等普通生活动作，应优先于宏大奇观成为因果反馈载体。
- reaction/payoff 动画、转场和声音必须由 Ren’Py 场景控制位置确定性进入与退出，并保持 rollback/save/load 安全。

### Audio and Accessibility

- choice confirmation 只可使用统一中性 UI 声，不得按分类、风险或后果改变音高、和声或强度。
- reaction 音频优先使用情境内声音：衣料、呼吸、脚步、纸张、门窗、雨、列车或物件接触；允许有意静默。
- payoff 可重用环境声或音乐动机，但不得成为隐藏 qualification 或 ending 密码。
- 静音、关闭音乐或关闭语音时，choice、reaction 与 payoff 的因果信息仍须完整可读，流程及时序不得改变。
- 所有语音和绘梨衣单音节提供字幕；承担因果信息的重要非语音声音提供可关闭的简短描述性字幕。
- 关键信息不得只靠左右声道、音高、音色或颜色区分。
- skip/auto 不得跳过唯一因果事实；至少保留可识别的最终 pose、物件状态或字幕事件。

### Future Art Bible Gates

未来 Art Bible 必须冻结：

1. 交互状态与道德/语义状态严格分离的视觉信息伦理。
2. 绘梨衣的非语言表演词典与禁用表达。
3. “建立元素→延迟重现→状态变化→玩家辨认”的因果回返语法。
4. 普通生活动作、触感物件和城市细节的视觉优先级。
5. 悲剧与成功路线的等价完成度。
6. 雨、光与色彩不得编码隐藏系统的边界。
7. 微反应 pose、停顿、hold、镜头距离及 rollback-safe 入退场规则。
8. 颜色、声音和空间声均不得单独承担因果信息的无障碍冗余规则。

### Deferred Asset Specifications

以下内容推迟至 SYS-NARRATIVE 与 Art Bible 获批后处理：

- 每个 `reaction_id` 的具体 pose、动作、镜头与情境音；
- 每个 `payoff_id` 的回返物件、环境变化、构图及声音动机；
- 东京七日各场景的雨、光线、交通与室内环境资产；
- 绘梨衣 pose 表与物件互动动画；
- 字幕样式、声音描述文案与混音参数。

> art-director 已咨询；当前无 Art Bible，以上八项作为未来 Art Bible 的强制输入。

## UI Requirements

本节只定义 choice surface 的行为与无障碍合同，不拥有叙事分支、语义状态或 ending 判定。具体布局、尺寸、响应式规则和焦点几何由后续 UX spec 冻结。

### Choice Surface

- 每个 production player-facing choice 必须以可读文本呈现，并与唯一 canonical `choice_id` 绑定。
- `semantic_major` 与 `narrative_only` 使用相同视觉层级；不得显示分类、轴、token、风险、成本、资格或预测后果。
- 选项顺序由 SYS-NARRATIVE 内容声明决定；UI 不得根据隐藏状态重新排序、推荐或突出选项。
- 文本必须支持换行与字体缩放，不得因固定高度截断关键含义。
- 在 1280×720 下，choice text、focus state 与当前场景正文必须保持可读。
- 系统 quick actions 必须在视觉上从属于当前叙事选择，不得与 choice surface重叠或竞争主要注意力。
- 现有切片中“顶部 quick actions过大”和“正文过重”只作为待修问题，不得视为 production UI基线。

### Interaction States

choice UI 只允许以下 presentation states：

| State | Required Behavior |
|---|---|
| `idle` | 选项可见、未聚焦，不表达语义倾向 |
| `focused` | 使用非颜色单一编码的清晰焦点指示 |
| `pressed` | 仅确认当前输入被接收，不预测结果 |
| `confirmed` | 锁定重复输入并立即退出 choice surface |
| `disabled` | 仅用于系统不可交互状态，不得表示“错误答案” |
| `timeout` | 仅在 SYS-TENSION启用时规范化为已登记 choice；不直接写语义状态 |

hover、focus、pressed 与 confirmed 的颜色、声音及动画必须在所有 choice classes间一致。

### Input and Focus

- 鼠标、键盘及已登记替代 activation 必须触发相同 canonical action；gamepad只遵守项目技术偏好的Ren’Py默认partial support，除非SYS-ACCESS另行升级合同。
- focus顺序必须与视觉阅读顺序一致；不得需要 hover才能发现、理解或确认选项。
- 任一时刻只允许一个 choice处于确认路径；重复键盘、手柄或鼠标事件必须在 UI层规范化为一次 confirmation。
- 确认后立即阻止第二次 activation，直至 choice surface退出；不得依赖 `DUPLICATE_NOOP`处理正常双击。
- 返回或取消行为不得在 commit后重新打开当前 choice surface。
- self-voicing是输出通道而非activation：必须朗读完整 choice text及当前focus位置，但不得触发confirmation，也不得朗读隐藏分类或后果。

### Timed Choices

- 紧张模式默认关闭；每个场景始终存在完整非限时路径。
- 启用时必须清楚告知当前选择受限时影响，并提供不依赖颜色、声音或动画的剩余时间信息。
- 限时提示不得改变选项顺序、文本、视觉价值层级或 reaction/payoff绑定。
- timeout必须转换为预先登记的 canonical choice，再执行标准提交顺序。
- 闪烁、震动与限时选择分别受独立设置控制；关闭任一反馈不得改变语义结果。
- 不得因暂停、设置、自发声或无障碍操作消耗未声明的选择时间；具体暂停规则由 SYS-TENSION UX合同冻结。

### Confirmation and Immediate Reaction

- choice surface必须在 reaction可读前完成退场，不能遮挡人物动作、物件状态或字幕。
- UI退场不得插入评分、关系变化、成就式弹窗或“选择已记录”提示。
- commit与 reaction之间不得显示菜单、确认对话框或可访问保存交互。
- reaction结束前，quick actions不得允许玩家跳过至下一 choice或其他叙事控制点。
- reaction为静音可读；重要单音节和非语音声音必须按设置提供字幕。

### Later Payoff

- SYS-CHOICE 不显示独立的 payoff HUD、历史徽章、因果通知或任务式完成提示。
- payoff通过实际场景、人物、物件与 registered outcome呈现。
- 如果 UI必须展示已完成叙事事件，只能消费 SYS-NARRATIVE批准的玩家可见摘要，不得显示内部 choice/reaction/payoff IDs。
- 共享 event服务多个 choices时，UI不得用颜色、图标或音效代替具体内容差异。

### Accessibility

- 支持字体缩放、高对比度、键盘导航、自发声及图片替代文本。
- focus不能只靠颜色区分；选项含义不能只靠图标、位置、声音、动画、闪烁或震动表达。
- 语音和绘梨衣单音节必须有字幕；重要非语音因果声音可提供描述性字幕。
- auto/skip速度可调，默认只跳过已读文本。
- skip不得删除唯一 reaction/payoff事实；至少保留最终 pose、物件状态或字幕事件。
- UI在静音、关闭动画、关闭闪烁及关闭震动时仍须完整可操作、可理解。
- 无障碍等价输入不得生成不同 choice record或改变 witness义务。
- 每个以视线、动作、停顿、人物距离、物件或环境变化承载因果信息的 production reaction/payoff，必须在 SYS-ACCESS/UX gate 中绑定一个玩家安全的 `accessible_causal_summary_id`；self-voicing、静音、reduced-motion与描述字幕模式必须消费同一 summary identity，不得暴露 axis/token/class/qualification。

### Rollback / Save / Load

- rollback至选择前时，choice surface按恢复后的真实控制位置重新出现；已撤销选项不得保留 confirmed或 disabled外观。
- load至 choice前时，显示该节点当前合法选项；不得从外部 UI cache恢复旧确认状态。
- load至 reaction后或 payoff后时，不得重新打开已完成的 choice surface。
- `Confirmed` 与 `Committed` 之间不存在可保存 UI状态。
- UI不得以 persistent、screen-local mutable cache或 imported object记录语义选择结果。
- unsupported/corrupt load直接进入 SYS-SAVE阻断界面，不显示当前 choice surface。

### UX Handoff

后续 UX spec 至少需要冻结：

- choice surface在 1280×720及字体缩放下的布局；
- 长选项换行、最大可见数量与滚动策略；
- 键盘/手柄焦点顺序和可见焦点样式；
- quick actions与 choice surface的视觉优先级；
- timed choice提示、暂停及无障碍行为；
- reaction微节拍期间的 UI退场和输入锁定；
- auto/skip对关键 reaction/payoff的保留规则。
- activation输入与self-voicing输出的支持矩阵；
- 每个reaction/payoff的`accessible_causal_summary_id`、视觉/字幕/self-voicing exact join及四恢复点同步；
- choice/reaction各阶段quick actions、save/load/rollback/skip的visible/enabled/focusable矩阵。

**SYS-ACCESS/UX downstream gate**：上述summary catalog、1280×720与最大字体缩放wireframes、keyboard focus walk、quick-action phase matrix、skip/auto可感知窗口及四恢复点UI evidence全部通过前，不得创建production UI epics。该门槛不重新打开本轮固定Required 1–7。

> 2026-07-28 ux-designer/ui-programmer专项审查已完成；具体screen flow与wireframe仍须在epics前通过`/ux-design`关闭下游门槛。

### No-Debug Player Fantasy Playtest Gate

该门槛在 closed vertical slice 可玩、至少覆盖一条成功结局与一条苦涩/悲剧结局后执行，不属于本轮SYS-CHOICE合同封板 blocker：

- 至少8名未接触调试ID、轴/token说明或路线表的参与者；
- 每人完成后抽取3个早期choice/payoff pairs；至少75%的参与者正确连接其中至少2组；
- 至少75%的参与者能指出当前结局的一项决定性损失、代价或未兑现承诺；
- 至少75%的参与者能举出一处绘梨衣表达并影响后续行动的自主决定；
- 报告必须保存匿名任务版本、路径/ending class、问题脚本、原始回答编码与失败样本。未达门槛只生成SYS-NARRATIVE/UX内容修订，不修改已封板的choice schema、resolver invariant或新增SYS-CHOICE blocker类别。

## Acceptance Criteria

证据类型沿用项目标准：`UT_ENGINE`、`UT_PURE`、`STATIC`、`BRANCH`、`INSTR`。所有 production-content 条目必须使用 exact `production_choice_source_manifest_record`、保存 manifest/scanner/CFG-normalizer/source hashes及完整排除记录；isolated fixtures只能验证合同，不得冒充生产内容证据。所有 negative fixture必须一次只含一个缺陷，并断言 exact `ChoiceBuildValidationError(error_code,stage,sorted offending_ids,source_location_ids)`、`freeze_count=0`、`published_index=None`及后续stage counters为0。

### Choice Coverage and Classification

| ID | Evidence | Criterion |
|---|---|---|
| `CHOICE-COVER-000` | `STATIC` | **GIVEN** exact production source manifest，**WHEN** 扫描 source roots、generated registries、expected chapters、exclusions与production/test边，**THEN** roots/chapters/discovered narrative surfaces均非空，source hash与scanner contract version相等，manifest外production source、unresolved edge及未登记exclusion计数均为0，并留存完整发现清单。 |
| `CHOICE-COVER-001` | `STATIC` | **GIVEN** `CHOICE-COVER-000`通过后的raw `choice_surface_assignment_record` tuples，**WHEN** 扫描 menu options、叙事buttons/hotspots、timed outcomes及accessibility-equivalent inputs，**THEN** 每个discovered `surface_id`的raw assignment count恰为1，target恰为一个player choice或合法allowlist；未分类、重复及双重分类数均为0。 |
| `CHOICE-COVER-002` | `STATIC` | **GIVEN** 空manifest、零叙事surface、未分类、raw duplicate、双重分类、章节叙事误列allowlist、动态不可解析action及production→test-only one-defect fixtures，**WHEN** 构建catalogs，**THEN** 每案返回其冻结error code/stage/offending IDs且不产生可用index。 |
| `CHOICE-COVER-003` | `STATIC + UT_ENGINE` | **GIVEN** 鼠标、键盘及已登记替代activation进入同一叙事分支，且self-voicing只朗读文本/焦点而不激活，**WHEN** 分别确认选择，**THEN** activation输入均解析为同一canonical `choice_id`、各traversal只提交一次，self-voicing confirmation count为0。 |
| `CHOICE-COVER-004` | `STATIC + UT_ENGINE` | **GIVEN** 一个 `narrative_only` choice，**WHEN** 玩家确认，**THEN** 以 empty `RunMap` 调用 `apply_choice`，history 增加其稳定 ID，五轴不变且 counterevidence effect 为 `null`。 |

### Commit and Control-Flow Order

| ID | Evidence | Criterion |
|---|---|---|
| `CHOICE-EXEC-001` | `UT_ENGINE + INSTR` | **GIVEN** 使用冻结authoring template的合法`semantic_major` choice，**WHEN** 玩家确认，**THEN** observation trace恰为`confirmation → activation disabled → canonical ID return → APPLIED → noninteractive reaction establishment → bounded reaction presentation → next permitted checkpoint/control transfer`，每项一次且顺序固定。 |
| `CHOICE-EXEC-002` | `UT_ENGINE + INSTR` | **GIVEN** sentinel、state或 payload 分别含 type/value缺陷，**WHEN** 尝试提交，**THEN** 抛出 SYS-STATE规定异常，`semantic_state` 深值不变，reaction与后续控制转移调用数为 0。 |
| `CHOICE-EXEC-003` | `UT_ENGINE + INSTR` | **GIVEN** history 已含相同 `choice_id`，**WHEN** 再次提交并收到 `DUPLICATE_NOOP`，**THEN** reaction调用数为 0且流程进入固定 fail-closed development boundary。 |
| `CHOICE-EXEC-004` | `STATIC + BRANCH` | **GIVEN** source-hash-bound Ren’Py AST、冻结normalizer version/hash与全部production choice edges，**WHEN** 构建edge-split commit node、reaction node、异常exit及first-transfer frontier，**THEN** commit dominates reaction、reaction在每条正常路径上postdominate commit且frontier前执行一次；region中menu/pause/jump/call/return/chapter exit/ending entry/save-load-rollback-skip入口与unresolved edge数均为0，并保存最短counterexample path。 |
| `CHOICE-EXEC-005` | `STATIC` | **GIVEN** 全部 production `.rpy/.py` source，**WHEN** 扫描 axes与 `choice_history` 写入，**THEN** 每项玩家选择只通过 `SYS-STATE.apply_choice` 修改状态，直接 mutation或替代入口数为 0。 |

### Semantic and Route Projections

| ID | Evidence | Criterion |
|---|---|---|
| `CHOICE-PROJ-001` | `UT_PURE + STATIC` | **GIVEN** 完整 choice catalog与任一合法 ordered history，**WHEN** 验证 projection coverage并按 SYS-STATE规则重放 axes，**THEN** 每个 choice恰有一个 semantic projection和一个 counterevidence entry，且 replay结果与 snapshot axes深值相等。 |
| `CHOICE-PROJ-002` | `UT_PURE` | **GIVEN** 使用exact `route_resource_effect_record`的合法event/resource projections与独立known-answer vectors，**WHEN** 按history顺序执行event union与acquire/consume fold，**THEN** 返回exact expected completed-event set和resource-possession set；裸pair/dict exact-type fixtures固定失败。 |
| `CHOICE-PROJ-003` | `UT_PURE + INSTR` | **GIVEN** duplicate acquire与 absent consume fixtures，**WHEN** route fold执行，**THEN** 固定抛出 `ValueError`，qualification、predicate、cause及 record阶段调用数均为 0。 |
| `CHOICE-PROJ-004` | `STATIC + UT_PURE` | **GIVEN** 非 `+1` delta、超过两轴、重复 axis、`grant`、multi-effect、wrong-domain repair及 narrative-only非空 axis/token fixtures，**WHEN** 验证 authoring records，**THEN** 每案构建失败且不冻结 catalogs。 |
| `CHOICE-PROJ-005` | `UT_PURE` | **GIVEN** 已冻结 projection/counterevidence records与 indexes，**WHEN** 尝试修改 mapping、record字段或 nested tuple，**THEN** 分别抛出规定 `TypeError`/`AttributeError`，调用前后深值相等。 |

### Reaction Exact Join

| ID | Evidence | Criterion |
|---|---|---|
| `CHOICE-REACT-001` | `STATIC` | **GIVEN** 完整 production choice与 reaction records，**WHEN** 运行 exact join validator，**THEN** 每个 choice恰有一个 binding，声明 reaction ID与 binding相等，event metadata反向匹配同一 choice及 binding。 |
| `CHOICE-REACT-002` | `STATIC` | **GIVEN** missing、duplicate、orphan、shared ID及 reverse-mismatch fixtures，**WHEN** 验证 reaction joins，**THEN** 每案固定失败且报告确切 offending IDs。 |
| `CHOICE-REACT-003` | `STATIC + BRANCH` | **GIVEN** `CHOICE-EXEC-004`冻结的CFG与每个production choice edge，**WHEN**查询共享dominator/postdominator index，**THEN**对应reaction node在commit后、first-transfer frontier前执行恰一次；所有异常/未解析edge已在前置gate失败。 |
| `CHOICE-REACT-004` | `STATIC + manual review` | **GIVEN** 全部绘梨衣 reaction content，**WHEN** 扫描并人工复核，**THEN** 只使用视线、动作、停顿、物件操作或简单单音节，不存在解释隐藏评分的完整口语。 |

### Payoff Join and Continuation Coverage

| ID | Evidence | Criterion |
|---|---|---|
| `CHOICE-PAY-001` | `STATIC` | **GIVEN** untrusted raw `payoff_ids` lists与全部bindings，**WHEN** 在任何set view前验证声明并运行join validator，**THEN** 每个raw list非空且内部唯一、每个`(choice_id,payoff_id)`恰有一个binding，binding数与raw list长度相等；empty/duplicate声明固定失败。 |
| `CHOICE-PAY-002` | `STATIC` | **GIVEN** 两种合法proof-kind records、exact guard/counterfactual referenced records及one-defect nullability/join mutants，**WHEN**验证字段矩阵和双向引用，**THEN**合法records通过；wrong-nullability、悬空、错owner、choice/event mismatch、unaligned suffix或伪event-absence分别返回冻结error oracle。 |
| `CHOICE-PAY-003` | `STATIC + BRANCH` | **GIVEN** source-hash-bound finite DAG，**WHEN**枚举所有`c∈C, h∈H_reach(c), s∈L_terminal(c,h)`，**THEN**每个组合至少有一个同choice/binding、真实路径、strictly-later且semantic-evidence-valid的witness；每个声明payoff至少由同一choice的合法witness使用一次，并输出graph hash、path/triple/continuation-entry/artifact-byte counts。 |
| `CHOICE-PAY-004` | `STATIC + BRANCH` | **GIVEN** same-node、choice-before-payoff顺序颠倒、ending-entry后 payoff及 generic unrelated event fixtures，**WHEN** 验证 witness，**THEN** 每案失败且不得计入 coverage。 |
| `CHOICE-PAY-005` | `STATIC + UT_PURE` | **GIVEN** 多个choices共享一个payoff event，**WHEN**验证causal bindings，**THEN**每个choice均有独立guard或不同registered outcome及独立`choice_payoff_semantic_evidence_record`；缺少逐choice证明或可感知状态变化时全部相关bindings失败。 |
| `CHOICE-PAY-006` | `UT_PURE` | **GIVEN** SYS-STATE批准的canonical byte encoder/version、相同node不同history及相同history不同terminal suffix，**WHEN**生成canonical prehistory/continuation IDs，**THEN** IDs均不同；相同完整输入重复生成时bytes与IDs完全相同。 |
| `CHOICE-PAY-007` | `STATIC` | **GIVEN** cycle、dangling edge及不能到达 ending entry的 graph fixtures，**WHEN** 构建 continuation languages，**THEN** 图验证先失败且 payoff coverage不运行。 |
| `CHOICE-PAY-008` | `STATIC` | **GIVEN** 每个causal binding的semantic evidence及history-only、text-only、camera-only、ID-only、unchanged-state mutants，**WHEN**验证evidence join，**THEN**合法record恰解析到affected subject、established element、不同before/after state或registered outcome及perceptible summary；所有伪回收mutants固定失败。 |
| `CHOICE-PAY-009` | `STATIC + BRANCH` | **GIVEN** 最大合法content fixture与四项硬预算，**WHEN** compiler执行shared-prefix枚举及witness expansion，**THEN** path≤4096、triple≤65536、continuation entries≤1048576、artifact bytes≤67108864；每个单项超限fixture在最早可判定stage固定失败且无截断/采样/partial artifact。 |

### Qualification Source Bindings

| ID | Evidence | Criterion |
|---|---|---|
| `CHOICE-QUAL-001` | `STATIC + UT_PURE` | **GIVEN** build-valid qualification record，**WHEN** 验证 sources，**THEN** operator属于 `all/any`、source并集非空、全部引用解析且 event/resource均可由 choice projections重建。 |
| `CHOICE-QUAL-002` | `STATIC` | **GIVEN** empty sources、unknown IDs、wrong kinds、live-state source、axis/token/achievement proxy及 illegal operator fixtures，**WHEN** 验证 bindings，**THEN** 每案固定失败且不冻结 production catalog。 |
| `CHOICE-QUAL-003` | `STATIC + BRANCH` | **GIVEN** 全部合法 terminal paths，**WHEN** 派生四项 terminal qualifications，**THEN** 每条路径最多命中一项；`rain_stops` predicate不读取任何 route qualification。 |

### Rollback, Save, and Load

| ID | Evidence | Criterion |
|---|---|---|
| `CHOICE-RESTORE-001` | `UT_ENGINE + INSTR` | **GIVEN** exact `before_choice` checkpoint，**WHEN** rollback/load至该control location、清零spy并重新确认至frozen horizon，**THEN** 原history/effects已撤销，新window恰产生一次`APPLIED`与一次reaction，target payoff各为0..1。 |
| `CHOICE-RESTORE-002` | `UT_ENGINE + INSTR` | **GIVEN** exact `after_reaction` checkpoint，**WHEN** load后清零spy并推进至next frozen control boundary，**THEN** expected history/axes保留，commit与reaction调用数均为0。 |
| `CHOICE-RESTORE-003` | `UT_ENGINE + INSTR` | **GIVEN** exact `before_payoff` checkpoint，**WHEN** load后清零spy并沿同一continuation推进过target payoff horizon，**THEN** commit/reaction为0且target payoff恰为1。 |
| `CHOICE-RESTORE-004A` | `UT_ENGINE + INSTR` | **GIVEN** exact `after_payoff` checkpoint，**WHEN** load后清零spy并推进至next control boundary，**THEN** commit/reaction为0且已完成target payoff为0。 |
| `CHOICE-RESTORE-004B` | `UT_ENGINE + INSTR` | **GIVEN** 从`after_payoff` rollback至一个distinct exact `before_payoff` checkpoint，**WHEN** 在新window清零spy并推进过target payoff node，**THEN** commit/reaction为0且target payoff为1。 |
| `CHOICE-RESTORE-005` | `UT_ENGINE` | **GIVEN** unsupported、legacy及 corrupt state fixtures，**WHEN** load，**THEN** 不恢复 choice lifecycle，进入阻断式安全流程，rollback/quick save-load/skip/history return均不可离开该流程。 |
| `CHOICE-RESTORE-006` | `STATIC` | **GIVEN** production source、save schema、checkpoint records与test-only trace adapter，**WHEN**扫描reaction/payoff ledger、persistent choice state、imported mutable rollback ownership及production observer leakage，**THEN**这些字段/引用均为0；observer只存在于source-hash-verified测试harness。 |

### Authority and Cross-System Integration

| ID | Evidence | Criterion |
|---|---|---|
| `CHOICE-AUTH-001` | `STATIC + INSTR` | **GIVEN** 全部 SYS-CHOICE production paths，**WHEN** 扫描 ending APIs及执行 choices，**THEN** 不存在 resolver wrapper、ending label jump或 `"Active" → "Ended"` mutation，canonical resolver调用数为 0。 |
| `CHOICE-AUTH-002` | `STATIC` | **GIVEN** major metadata、reaction/payoff IDs及 semantic-value registry，**WHEN** 验证 `unique_value_tags`，**THEN** 每项 tag解析到已登记 `semantic_value`与具体证据；仅因 reaction/payoff ID或文本不同的记录失败。 |
| `CHOICE-INTEG-001` | `STATIC + UT_ENGINE` | **GIVEN**完整SYS-NARRATIVE production records与exact source manifest，**WHEN**执行offline freeze pipeline，**THEN** choice、reaction、payoff、semantic evidence、event、resource、outcome及witness joins和硬预算全部通过后才生成source-hash-bound immutable catalogs。 |
| `CHOICE-INTEG-002` | `UT_PURE + STATIC` | **GIVEN**冻结 catalogs与同一 detached snapshot，**WHEN** 在不同外部 live-state fixtures下执行 SYS-ENDING，**THEN** route facts、qualification sources及完整 resolution record深值相等。 |
| `CHOICE-INTEG-003` | `UT_ENGINE + STATIC` | **GIVEN** 已登记activation inputs与tension modes，**WHEN**分别走非限时、限时确认及timeout路径，**THEN**每个实际叙事结果都使用已登记choice record；始终存在非限时可达路径，self-voicing只消费文本/摘要且confirmation count为0。 |
| `CHOICE-INTEG-006` | `STATIC + UT_PURE` | **GIVEN**离线compiler产物与runtime import，**WHEN**执行import closure，**THEN**runtime只验证exact schema/source hash并建立immutable indexes；source scan、CFG/DAG、path enumeration、filesystem/network/environment I/O及test observer imports计数均为0。 |
| `CHOICE-INTEG-004` | `STATIC + BRANCH` | **GIVEN** SYS-CHOICE与 SYS-NARRATIVE完成且 locked resolver invariants未变，**WHEN**执行集成 gate，**THEN**只运行 `SYS-CHOICE/SYS-NARRATIVE → SYS-ENDING Cross-System Integration Validation`，不触发 SYS-ENDING全文审查。 |
| `CHOICE-INTEG-005` | `STATIC` | **GIVEN** 下游提案改变 qualification semantics、resolver stages、predicate、cause identity或 ending lifecycle，**WHEN**评估变更，**THEN** gate阻止集成并要求同步修订 SYS-ENDING GDD、相关 ADR、registry及 canonical tests。 |

### Performance Evidence

| ID | Evidence | Criterion |
|---|---|---|
| `CHOICE-PERF-001` | `UT_ENGINE + INSTR + STATIC` | **GIVEN** 任一合法choice与冻结authoring template，**WHEN**从confirmation执行至reaction完成，**THEN**仅存在一个bounded reaction presentation interaction；后台任务、网络、filesystem、external I/O及未登记control edges计数均为0。 |
| `CHOICE-PERF-002` | `STATIC + BRANCH + SYS-TEST benchmark report` | **GIVEN**最大合法content fixture、硬预算与固定build/hardware/timer/GC/sample policy，**WHEN**offline compiler执行source scan、shared CFG indexes、join validation及完整continuation expansion，**THEN**operation counts符合`O(B+V+E+W+Σ|s|)`并报告maximum/p95/time/memory；任何内容硬预算超限均独立FAIL，时间/硬件阈值由`CHOICE-Q10`关闭。 |

> 2026-07-28 qa-lead已完成首次完整审查；本轮仅对固定Required 1–7执行一次定点封板检查。

## Open Questions

以下问题只涉及 production content、跨系统集成和表现层交付；不重新打开本 GDD 已冻结的 choice classes、执行顺序、exact schemas、reaction cardinality、proof-kind nullability、rollback authority或 SYS-ENDING locked invariants。

| ID | Open Question | Owner | Target Resolution | Closure Evidence |
|---|---|---|---|---|
| `CHOICE-Q1` | 四项 terminal route qualifications 的 exact `source_choice_ids`、`source_event_ids`、`source_resource_ids` 与 `all/any` operator分别是什么？ | SYS-CHOICE + SYS-NARRATIVE + SYS-ENDING / Andwey | SYS-NARRATIVE GDD批准前 | 四项 build-valid records、reference-integrity report、source-removal witnesses及 terminal-route互斥报告；关闭 `ENDING-Q1` |
| `CHOICE-Q2` | 全部 production choices、reaction events、payoff events、reverse metadata及 continuation witnesses的具体 IDs和 records是什么？ | SYS-NARRATIVE + SYS-CHOICE / Andwey | Production narrative catalog首次冻结前 | 完整 catalogs、exact join report、missing/duplicate/orphan/wrong-nullability negative fixtures；联合关闭 `ENDING-Q2` |
| `CHOICE-Q3` | 最多 10 个 route-critical revoke tokens的具体 IDs、domains、consequences、resolution modes及 repair/irreversible evidence是什么？ | SYS-NARRATIVE + SYS-CHOICE / Andwey；Creative Director审核 irreversible records | SYS-NARRATIVE GDD批准前 | Counterevidence catalog、repair path witnesses、irreversible approvals、agency branch outcomes及 ending payoffs；关闭 `ENDING-Q3` |
| `CHOICE-Q4` | 完整 choice DAG会形成多少 terminal cause classes，每个 class的 witness、outcome signature与 payoff scene是什么？ | SYS-CHOICE + SYS-NARRATIVE + SYS-TEST / Andwey | 两系统设计完成后的跨系统验证前 | 全图 enumeration report、每 class canonical witness及 `1–6/7–12/>12` verdict；关闭 `ENDING-Q5` |
| `CHOICE-Q5` | 每个 production payoff、terminal class与 ending cause的玩家可见简体中文摘要和安全展示文案是什么？ | SYS-NARRATIVE + UX + Localization / Andwey | 内容与 UX lock前 | Localized summary catalog、spoiler review、anti-hidden-score review及 cause-card UX spec；关闭 `ENDING-Q6` |
| `CHOICE-Q6` | reaction后、payoff前、payoff后及 rollback至选择前四类恢复点如何在正式 SYS-SAVE流程中实现？ | SYS-SAVE + SYS-CHOICE + SYS-TEST / Programmer | SYS-SAVE GDD批准前 | 四类 `UT_ENGINE + INSTR` fixtures、unsupported/corrupt safe-flow evidence及 duplicate/loss report |
| `CHOICE-Q7` | 紧张模式的时间长度、暂停规则、提示方式及 timeout choice records是什么？ | SYS-TENSION + SYS-ACCESS + UX / Designer | 任一 timed choice进入 production前 | SYS-TENSION GDD、timed-choice UX spec、非限时可达性证明及 timeout canonical-ID fixtures |
| `CHOICE-Q8` | Future Art Bible的八项 SYS-CHOICE gates如何具体落地，哪些 reaction/payoff需要独立资产？ | Art Director + SYS-NARRATIVE / Andwey | `/asset-spec` 与 production asset制作前 | Approved Art Bible、逐 `reaction_id`/`payoff_id` asset inventory及 `/asset-spec system:choice-and-causality-record` 输出 |
| `CHOICE-Q9` | choice surface的布局、长文本、焦点、quick actions、timed indicator、skip/auto，以及activation与self-voicing输出矩阵如何实现？ | UX Designer + SYS-ACCESS / Andwey | UI epics创建前 | `design/ux/` 下的choice-surface spec、1280×720与最大字体缩放wireframes、keyboard focus flow、partial-gamepad支持表、accessible causal summary catalog、quick-action phase matrix、四恢复点UI evidence及accessibility review |
| `CHOICE-Q10` | 在已冻结4096/65536/1048576/64MiB内容硬上限内，offline compiler的构建期耗时、峰值内存及参考硬件阈值是什么？ | SYS-TEST + Engine Programmer / Andwey | 最终跨系统集成 gate前 | Benchmark manifest、固定硬件/build/maximum fixture、n/2n/4n operation counts、sample/GC/timer policy、maximum/p95结果及time/memory预算；不得修改本GDD内容硬上限；联合关闭`ENDING-Q7` |
| `CHOICE-Q11` | 无调试信息的玩家能否识别早期choice与后果、理解苦涩/悲剧的决定性损失，并感到绘梨衣的自主决定真实影响后续？ | Narrative Director + UX + Playtest / Andwey | Closed vertical slice内容锁定前 | 至少8名参与者；choice/payoff连接、结局损失与绘梨衣自主性三项各≥75%；保存匿名版本、路径/class、问题脚本、编码结果及失败样本 |

### Explicitly Closed Decisions

以下事项不是 Open Questions，后续系统不得在内容文件中自行改变：

- 所有玩家叙事选项只能是 `semantic_major` 或 `narrative_only`；
- 唯一顺序为确认→`apply_choice`→reaction→后续流程；
- reaction为一对一 exact join，payoff为非空一对多；
- 每个合法 `(choice,prehistory,continuation)` 至少拥有一个严格较晚 witness；
- proof-kind及其可空矩阵已经冻结；
- ordered history是 rollback/save/load权威；
- SYS-CHOICE不选择 ending、不改 resolver、不拥有 `"Active" → "Ended"`；
- SYS-CHOICE/SYS-NARRATIVE完成后只运行既定跨系统集成验证，除非 locked invariant发生变化。
