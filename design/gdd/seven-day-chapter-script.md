# 七日章节脚本

> **Status**: Approved with provisional downstream gates
> **System ID**: SYS-NARRATIVE
> **Author**: Andwey + Codex
> **Last Updated**: 2026-08-14
> **Implements Pillar**: 看见未说出口的话；温柔必须被挣来；悲剧也是完整答案；用普通生活抵抗宏大命运
> **Upstream Contracts**: SYS-CHOICE Approved with provisional downstream gates；SYS-ENDING Approved with provisional downstream gates
> **Review Mode**: Full
> **Design Self-Check**: 2026-07-29 — baseline v1.2；54 choices；9 agency transactions；5 formulas revised against second adversarial review；42 acceptance criteria；6 downstream open questions
> **Creative Director Review (CD-GDD-ALIGN)**: 2026-07-29 — NEEDS REVISION；agency、payoff、qualification、terminal-class、CFG 与 oracle blockers revised, independent re-review required
> **Journal Source Amendment**: 2026-08-04 — freezes `journal_chapter_catalog:v1` / `journal_memory_catalog:v1` ownership, 7×2 common-path truth approvals and no-history downstream boundary
> **Design Change Amendment**: 2026-08-14 — baseline v1.3 extends only the existing `rain_stops` epilogue after lights-out with a short years-later tail; no new canonical unit or semantic contract
> **Formal Prose Expansion Amendment**: 2026-08-14 — four prose-only delivery sprints expand existing units without changing stable IDs, mechanics, ending contracts, or asset scope

## Overview

SYS-NARRATIVE 不是额外玩法系统，而是七日视觉小说的章节、场景与分支内容规范。玩家通过阅读、观察并选择回应方式参与七日旅程；系统将已批准的 SYS-CHOICE 因果合同与 SYS-ENDING 判定合同落实为具体场景、玩家选项、人物反应、延迟回收及六结局路径，使玩家能够从叙事结果中理解自己的行为如何影响绘梨衣的自主决定、人物归宿与最终代价。章节内容遵循 [ADR-0003：内容与表现边界](../../docs/architecture/adr-0003-content-and-presentation-boundary.md)，不新增战斗、任务、可见数值、独立叙事引擎或新的结局规则；没有本系统，既有选择和结局合同将缺少可体验、可追踪且完整回收的故事内容。

## Player Fantasy

玩家幻想不是“正确操纵角色并获得最好结局”，而是在七日相处中逐渐学会看懂绘梨衣没有说出口的回答：观察她的视线、动作与物件表达，等待她形成自己的决定，在不替她安排一切的前提下接受这个决定，并与她共同承担随后发生的后果。该体验直接落实“看见未说出口的话”与“温柔必须被挣来”；玩家最终应感到，自己不是解出隐藏数值，而是真正学会了如何尊重另一个人的自主。

核心玩家时刻来自跨日连续回收：第一日被看见并接受的意愿，在第四日转化为车票、路线或联系人准备，并在第六、七日重新出现，实际改变人物去向、代价承担者与结局。玩家应能自然认出“这是前面那个决定的结果”，却不察觉五轴、token、qualification 或路径验证结构。即使进入悲剧结局，结果也应体现“悲剧也是完整答案”——玩家理解它由自己一路作出的选择、忽视与承诺共同构成，而不是系统在终点突然判错；最后留下的是人物、故事和自己承担过的决定。

## Detailed Design

### Core Rules

1. **双层内容结构**

   SYS-NARRATIVE 使用两层互相引用的内容：

   - 叙事层：按序章、第一日至第七日、六个结局与尾声描述章节目标、场景顺序、人物行动和分支回收。
   - 记录层：用稳定 ID 冻结 chapter、scene、choice、reaction、payoff、event、resource、outcome、agency transaction、qualification source 与 ending witness records。

   本 GDD 冻结系统合同；规范性配套文档 [七日内容基线](../narrative/seven-day-content-baseline.md) `narrative_content_baseline:v1.4` 冻结 15 个 production units、required scene beats、54 项正式玩家选择、9 项 agency transactions、7 项 repairable tokens、四项 route qualification bindings、六条完整 canonical ending histories 与 11 项 terminal cause-family production variants。Cause family 不是 SYS-ENDING equivalence-class identity；实际逐 class records 与 witnesses 必须由全图枚举生成。约 7–9 万字对白、旁白与具体演出脚本保留在 `game/chapters/` 的分章 `.rpy` 文件中。对白可以润色，但不得未经验证改变内容基线的稳定 ID、分支控制流、人物决定、registered outcome 或玩家安全核心含义。

2. **章节记录**

   每个 `narrative_chapter_record` 必须声明：

   `chapter_id, title, entry_scene_id, terminal_scene_ids, required_scene_ids, optional_scene_ids, mandatory_responsibility_id, input_fact_ids, produced_event_ids, choice_ids, payoff_ids, next_chapter_or_ending_ids, chapter_summary_id, owner_system`

   Production source manifest 必须覆盖序章、第一日至第七日、六个结局及适用尾声。所有 expected units 都必须非空、可达且不存在悬空引用。

### `rain_stops` Epilogue Extension Boundary

`epilogue_rain_stops_arcade` remains the sole existing true epilogue unit. Its
current first-guest and lights-out scenes remain in the same order, with their
existing completion events and completion boundary unchanged. The unit may
continue after lights-out into one short, non-interactive years-later tail.

The tail is limited to two structural viewpoints: an unnamed neighborhood
observer noticing the small arcade as an ordinary local business, and a clearly
marked written note by 绘梨衣. The observer may mention only unnamed old
friends and ordinary customers as background texture. The written note may
carry complex content, but it is written material, not complete spoken
dialogue; no `erii` speech line may carry that content. This boundary confirms
no named extra character return, family conversion, pregnancy, twins, or other
major world-state fact. It also adds no choice, reaction/payoff join, axis,
token, resource, qualification, ending predicate, persistent field,
achievement, Gallery record, canonical unit, or canonical completion event.

The input source for this amendment is an unconfirmed fan-adaptation reference.
Only high-level structure and theme may inform the implementation; the project
must not copy its wording or rely on its named-character/world-state claims.

### Formal Prose Expansion Boundary

To close the remaining authored-length gap, production proceeds through four
independent prose-only sprints in this order: Prologue/Day 1–2, Day 3–4, Day
5–6, and Day 7/six endings/`rain_stops` tail. Each sprint may enrich existing
scene description, physical action, observation, immediate reaction, and
already-frozen payoff recall. It must not add or alter choice IDs, menus,
labels, axes, tokens, resources, qualifications, route guards, ending
predicates, completion events, persistent fields, hidden numeric rules,
canonical units, active-character constraints, or assets. Each sprint refreshes
the affected source identities and runs the full automated QA chain before a
local close commit. Human playtest, SAPI/semantic, copyright, subjective
readability, and final narrative sign-off remain deferred.

### Journal Source Catalogs

SYS-NARRATIVE 独占并发布两个 player-safe immutable source catalogs：

- `journal_chapter_catalog:v1`：恰含 Day 1–7 七条 `(memory_id, day_index, list_title_id, list_summary_id, detail_title_id, detail_body_id, common_path_truth_approval_id)`；
- `journal_memory_catalog:v1`：恰含相同七个 `(memory_id, day_index)` 的 `(memory_id, day_index, object_title_id, list_summary_id, detail_title_id, detail_body_id, common_path_truth_approval_id)`。

两目录的 `(memory_id,day_index)` 必须一一相等，`day_index` 恰为无重复 `1–7`。首发 records 全部为实时渲染的纯文字内容，不声明 per-memory asset/alt 字段。SYS-JOURNAL 拥有顶层 bundle projection schema，但不得修改 source copy、ID 或 approval。

每个 `common_path_truth_approval_record` 字段恰为：

`approval_id, memory_id, day_index, completed_path_set_hash, allowed_common_fact_ids, forbidden_variant_fact_ids, reviewer_ids`

其中 `allowed_common_fact_ids` 必须是该日所有合法 chapter-completed paths 上玩家可感知事实的严格交集；`forbidden_variant_fact_ids` 至少覆盖互斥 choice、可变代价承担者、非共通 payoff、route qualification、axis/token/predicate 与逐 traversal cause。Chapter copy 只能把允许事实组织为日级共同经过和共同已实现结果；memory copy 只能聚焦其中一个共同物件、动作或情感近景。任一文案引用交集外事实、approval/path-set hash 陈旧或 reviewer 未通过时，使对应 category validation 失败；不得读取当前 `choice_history`、save slot 或 live flags生成替代文案。

任何未来 path-specific Journal 方案都必须新建 generation，并先由架构与 SYS-PERSIST amendment 冻结 player-safe projection/保存边界；不得在 v1 source records 中增加可选 traversal 字段。

3. **场景记录**

   每个 `narrative_scene_record` 必须声明：

   `scene_id, chapter_id, purpose, entry_condition_ids, active_character_ids, character_constraint_ids, input_fact_ids, choice_surface_ids, choice_ids, reaction_ids, payoff_ids, produced_event_ids, outcome_reference_ids, next_scene_ids, perceptible_summary_ids, owner_system`

   场景不得依靠未登记的章节 flag、背包状态、persistent 值或隐藏分数决定分支。所有语义条件必须来自 ordered `choice_history` 及其冻结投影。

4. **因果场景流程**

   每个含玩家决定的因果场景固定遵循：

   `场景建立 → 观察人物表达 → 必要时 request/answer → 玩家回应或行动 → 确认并提交 choice → 即时人物反应 → 进入 continuation → 严格较晚的 payoff`

   纯过场或桥接场景可以省略 choice，但不得产生未经 choice record 支持的语义增量、counterevidence、路线资格或结局变化。

5. **Agency transaction**

   涉及绘梨衣自主性的内容必须登记 `agency_transaction_record`：

   `transaction_id, request_event_id, answer_event_id, answer_subject_id, answer_state_id, allowed_answer_state_ids, answer_derivation_record_id, source_response_node_ids, response_choice_ids, accepting_choice_ids, overriding_choice_ids, response_outcome_bindings, resulting_outcome_ids, owner_system`

   - request 与 answer 只证明玩家询问过、绘梨衣表达过，不自动产生 `autonomy +1`。
   - 每个 answer 必须引用 `character_answer_derivation_record`，冻结输入事实、候选闭集、唯一 selected state、动作/物件证据、priority rule 与 source hash；不得由作者直接赋值，也不得读取 axis、token、qualification 或 ending prediction。
   - 只有接受、遵循或明确维护已登记 answer 的后续 choice，才可产生自主性正向证据。
   - 忽视、替代或推翻 answer 的 choice 必须明确投影零增量或对应 counterevidence。
   - 不得把沉默自动解释为同意；路明非可以复述自己的理解，但必须给绘梨衣以动作、视线、物件或单音节确认、否认或拒绝的机会。
   - 从 production scene CFG 反推的全部 response choices 必须与 `response_choice_ids` exact-equal；记录不得通过漏报分支使 partition 假通过。
   - `response_outcome_bindings` 必须为每个 response choice 提供非空、引用完整的 exact outcome tuple。接受类 response 不得同时 revoke 当前 answer domain。
   - answer 含混、未登记或为 `undetermined` 时不得出现 response surface；scene 与 transaction 保持 unfrozen。

6. **选择、反应与回收**

   - 每个玩家叙事选项恰分类为 `semantic_major` 或 `narrative_only`。
   - 选择确认后必须先通过 SYS-CHOICE 提交，再演出即时反应。
   - 即时反应必须在所有正常路径上发生一次，并在完成前禁止进入其他叙事节点。
   - 每个 choice 必须拥有至少一个严格较晚的 payoff；payoff 必须改变玩家可感知的人物、物件、信息、承诺、资源或结局损失。
   - 只更换文本、镜头、滤镜、音效或内部 ID 不构成有效回收。
   - 玩家应能自然认出回收来源，但内容不得公开 axis、token、qualification、predicate 或 terminal class。
   - 同一 route-critical token 被多次 revoke 时保持单一 set membership，但必须按 history 追加全部 contributor choice IDs；repair 只有在玩家可感知地逐项承认当前全部 contributors、撤回仍生效的冲突安排，且 `repaired_source_choice_ids` 与 contributors exact-equal 时才可移除 token。

7. **人物设定守恒**

   每个进入 production catalog 的人物必须拥有经批准的 `character_constraint_record`：

   `character_id, source_reference_ids, speech_constraints, knowledge_bounds, motivation_bounds, relationship_baseline, forbidden_behaviors, approval_record_id, owner_system`

   场景、选项、反应和结局不得为了连接分支而让人物：

   - 说出不符合既定表达能力或语言习惯的话；
   - 知道尚未获得的信息；
   - 无因改变核心动机、能力边界或关系立场；
   - 替作者解释隐藏评分、正确答案或结局条件；
   - 仅为推动剧情而接受此前明确拒绝的安排。

   绘梨衣继续遵守已批准约束：不能进行完整口语对白；复杂意图只能通过视线、身体动作、停顿、物件互动和上下文表达。简单单音节可以确认或否认，但不得承担完整解释。愿望纸等书面物件不得被用作连续口语对白的替代品。

   `narrative_content_baseline:v1.2` 的 active-character 闭集为路明非与绘梨衣；两人的 `character_constraint_record`、source references 与 approval IDs 已在配套内容基线及 entity registry 冻结。追踪者、家族与联系人目前只以登记信息、物件和 outcome 出现，不是 active characters；任何新增 active character 必须先增加独立 constraint record，并使全部引用场景重新进入人工审核。

8. **七日回收责任**

   | 单元 | 必须建立或回收的内容 |
   |---|---|
   | 序章 | 建立观察、催促与共同决定的初始差异；为第一日和第六日提供可回收输入 |
   | 第一日 | 绘梨衣如何表达自身愿望；便服、食物及名字相关的自主决定 |
   | 第二日 | 游戏昵称、两枚游戏币、普通生活愿望及后续盟友识别 |
   | 第三日 | 隐瞒、坦白或逃避产生的真相信任与服从关系 |
   | 第四日 | 根据既有回答准备车票、路线、联系人和备选方案 |
   | 第五日 | 交付家族真相，并让绘梨衣决定如何回应 |
   | 第六日 | 安全屋失效后兑现资源、承诺和代价；决定保护对象与代价承担者 |
   | 第七日 | 承认前六日形成的因果，不增加万能分数或最终覆盖选择 |
   | 结局与尾声 | 回收人物去向、代价承担者、未解决伤害和普通未来；不得新增反向决定结局的 source fact |

9. **分支图与结局路径**

   - 重大选择图必须是从新游戏入口到 ending entry 的有限 DAG。
   - 所有 scene、choice、reaction、payoff 与 ending entry 必须可达且无悬空跳转。
   - 分支重新汇合不得抹除 history 差异、未解决 token、资源状态或后续 payoff。
   - 六个结局各至少拥有一条首周目 canonical witness。
   - 每条终局路径必须唯一解析为一个 ending、一个 terminal-cause class、适用 payoff 和玩家可感知摘要。
   - SYS-NARRATIVE 负责提供四项 route qualification 的具体 source bindings，但不得修改 SYS-ENDING 已批准的资格语义、predicate 或优先级。
   - Day 6 route commitment 不是自由选择结局的菜单。内容基线必须冻结互斥且穷尽的 entry guards，使 independent/shared/solo/old-order/fallback 五个 choice 中恰有一个 active；前三项必须与绘梨衣已登记并被接受的 `answer_state_id` 一致。
   - 全图必须遵守 SYS-CHOICE 的 4096 条 terminal paths、65536 个展开 triples、1048576 个 continuation entries和 64 MiB compiled witness artifact 硬上限。

10. **明确禁止的内容**

    SYS-NARRATIVE 不得新增战斗、任务系统、可见属性、好感度、随机结局、独立叙事引擎或最终覆盖选择；不得让画面、声音、hover、限时输入或调试信息成为理解或推进剧情的唯一途径；不得通过违背人物设定、伪造 production ID 或压缩不同人物归宿来满足路径预算。

### States and Transitions

这些状态描述可验证的叙事控制位置，不新增 persisted lifecycle enum；实际恢复依据仍是 Ren’Py 控制位置与 rollback-owned `choice_history`。

| 状态 | 含义 | 合法下一状态 |
|---|---|---|
| `SceneEntered` | 场景 entry 条件已满足 | `ObservationPresented` |
| `ObservationPresented` | 人物、环境和可观察信息已建立 | `AnswerRegistered`、`ChoicePresented` 或无选择桥接 |
| `AnswerRegistered` | request/answer event 已完成，但尚未评价玩家回应 | `ChoicePresented` |
| `ChoicePresented` | 玩家可确认一个已登记 choice | `ChoiceCommitted` |
| `ChoiceCommitted` | SYS-CHOICE 已提交 stable ID | `ReactionEstablished` |
| `ReactionEstablished` | 反应事实、最终 pose/物件/文本已非交互建立；重复 activation 已禁用 | 恰一次 bounded reaction-presentation interaction |
| `ReactionCompleted` | bounded reaction interaction 返回；即时反应已可读，首次允许 checkpoint/control transfer | `Continuing` |
| `Continuing` | 后续场景按 history 与 registered facts 推进 | `PayoffRealized`、下一 `SceneEntered` 或 `ChapterClosed` |
| `PayoffRealized` | 一个严格较晚的因果回收已完成 | `Continuing` 或 `ChapterClosed` |
| `ChapterClosed` | 必需场景与章末输出完整 | 下一章节 `SceneEntered` 或 `EndingEntry` |
| `EndingEntry` | 第七日内容完成并调用唯一结局解析流程 | SYS-ENDING 映射的结局演出 |

`ChoiceCommitted → ReactionEstablished` 之间不得出现 interaction、存档、跳转或其他 choice；随后必须通过唯一批准的 wrapper call 进入恰一次 bounded reaction-presentation interaction。该 interaction 只呈现已建立的反应事实，期间 quick actions、game menu、save/load、rollback、skip、AFM/auto、history return 与重复 activation 均 disabled/unfocusable；返回后才进入 `ReactionCompleted` 和首个 `after_reaction` checkpoint。除下述唯一 wrapper call、其内部唯一 `call screen` 与 matching return 外，不得出现第二次 interaction、额外 choice、jump/call/return 或语义写入，也不得依赖 reaction/payoff ledger 修复叙事状态。

Ren’Py production scenes 必须使用唯一批准的 `narrative_choice_reaction:v1` authoring template：

1. `menu`/choice screen 只返回 canonical choice ID，并立即禁用重复 activation。
2. 同一语句序列调用一次 SYS-CHOICE commit；随后只建立非交互的 reaction facts、final pose/object/subtitle/summary IDs。
3. 使用 `call narrative_reaction_wrapper(...) from <stable_from_label>` 进入唯一 wrapper label；wrapper 内只执行一次 `call screen narrative_reaction_present(...)` 并返回。`from` 只属于 label call，不附着在 `call screen` 上。Screen 为 modal，暂停 skip 与 AFM/auto，不执行 semantic writes。
4. Wrapper 取得 screen 返回的 stable `roll_forward_id` 后立即 matching return；调用点记录唯一 hard checkpoint，进入 `ReactionCompleted`；只有此时恢复 quick actions。

SYS-CHOICE 独占 `choice_source_scanner:v1`、Ren’Py AST/lexer version、CFG normalizer 与 source-hash-bound canonical CFG artifact。SYS-NARRATIVE 不建立第二个 source scanner；`narrative_manifest_projection:v1` 只消费该 artifact，增加 chapter/unit/scene ownership 与 required-beat 投影。CFG 使用栈敏感的 `callsite → wrapper label → matching return site` normalizer，解析 label parameters、local labels、无返回出口与异常出口；缺失 `from`、动态 wrapper label、wrapper 内出现第二个 interaction/semantic write、无法匹配 return 或绕过 template 的自定义 interaction均使构建失败。Q9 在 SYS-SAVE 集成前进一步冻结每个 checkpoint 的 stable `control_location_id`、owner、rollback-owned storage、statement mapping、observation horizon 与 `after_load` validation；不得使用文件行号作为稳定 identity。

### Interactions with Other Systems

| 系统 | 数据流 | SYS-NARRATIVE 责任 |
|---|---|---|
| SYS-CHOICE | 双向：提交 production records，消费稳定 choice 合同 | 创作具体节点、反应、回收、事件、资源、outcome 与 witnesses；不修改 schema、join 或 graph validator |
| SYS-STATE | 经 SYS-CHOICE 间接写入，读取已批准 snapshot 语义 | 不直接写轴、history、sentinel 或派生缓存 |
| SYS-ENDING | 提交 qualification sources、terminal witnesses、outcome signatures 与 payoff；消费 selected ending；拥有 ending entry 与 completion boundary | 不复制 resolver，不修改 predicate 或优先级；只在 entry 与 terminal completion node 写入各自的 rollback-owned lifecycle/event |
| SYS-SAVE | 恢复叙事控制位置与 rollback-owned state | 不建立独立存档、去重 ledger 或 imported mutable state |
| SYS-PERSIST | 消费完成后的 ending、memory 与 narrative event；提供当前 `collection_epoch_id` detached value | 不允许跨周目 membership 反向参与本轮结局；ending 仅消费 `SYS-ENDING` terminal completion event；epoch 只用于拒绝 reset 前旧成就证据 |
| SYS-ACHIEVE | 输出 `achievement_event_catalog:v2` 的已完成事件、checkpoint 与 snapshot | 11项成就条件不得成为隐藏 axis/token 代理；ending/memory 不镜像为成就 |
| SYS-JOURNAL | 输出`journal_chapter_catalog:v1`、`journal_memory_catalog:v1`及7项`common_path_truth_approval_record` | Journal只读；摘要不得包含交集外逐traversal事实、未发现路径或内部判定 |
| SYS-ACCESS | 输出完整感知主体发现、semantic fact、perceptible/accessible summaries与可重访transcript合同；UX role 负责交付规格 | 无障碍等价输入必须解析到同一 canonical choice；summary不得越过人物知识/模糊边界 |
| SYS-AUDIO + Art Bible / asset pipeline | 提供场景、人物动作、物件与情境音需求 | 表现资产不得成为唯一因果信息来源 |
| SYS-TENSION | 可选提供限时表现层 | 始终保留非限时可达路径；timeout 也必须是已登记叙事结果 |
| SYS-TEST | 提供 manifest、完整图、catalog 与 witnesses | 支持静态 join、路径枚举、save/load/rollback 及无调试 playtest |

> Full review consulted `game-designer`, `narrative-director`, `systems-designer`, Ren’Py gameplay programmer, `qa-lead`, `ux-designer`, `ui-programmer`, `audio-director`, `performance-analyst` and `creative-director`; blocking findings are incorporated in this revision.

## Formulas

SYS-NARRATIVE 不计算玩家分数、概率或成长曲线。以下公式均为构建期 exact-boolean 验证；运行时语义继续由 SYS-CHOICE、SYS-STATE 与 SYS-ENDING 的批准公式负责。

### Chapter Manifest Validity

The `chapter_manifest_valid` formula is defined as:

`chapter_manifest_valid(M,U) = exact_manifest_type(M) ∧ canonical_cfg_artifact_version(M) = "choice_source_scanner:v1" ∧ manifest_projection_version(M) = "narrative_manifest_projection:v1" ∧ canonical_cfg_artifact_hash_matches(M) ∧ U = canonical_production_units_v1 ∧ |U| = 15 ∧ roots(M) ≠ ∅ ∧ duplicate_unit_count(M) = 0 ∧ expected_units(M) = U ∧ scanned_units(M) = U ∧ unresolved_reference_count(M) = 0 ∧ production_to_test_only_edge_count(M) = 0 ∧ source_hash_matches(M)`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| source manifest | `M` | exact record | one production manifest | 声明 source roots、expected units、canonical CFG artifact/projection versions 与 source hash |
| required units | `U` | exact finite set | exactly 15 canonical IDs | `narrative_content_baseline:v1.2` 中冻结的序章、第一日至第七日、六结局及真结局可玩尾声 |
| source roots | `roots(M)` | exact tuple | `1..N` paths | Production 章节脚本根目录 |
| expected units | `expected_units(M)` | finite set | `1..N` IDs | Manifest 声明必须存在的内容单元 |
| scanned units | `scanned_units(M)` | finite set | `0..N` IDs | 实际扫描到的内容单元 |
| unresolved references | — | exact int | `0..N` | 无法解析的 scene、choice、event、payoff 或 jump 引用 |
| production-to-test-only edges | — | exact int | `0..N` | Production 内容指向 fixture/test-only 内容的边 |
| duplicate units | — | exact int | `0..N` | raw manifest/scanner 中重复声明的 unit IDs；集合化前计数 |

**Output Range:** exact `False` 或 `True`；错误 record type、非 canonical SYS-CHOICE scanner artifact、非 v1 narrative projection、artifact/source hash 不匹配、`U` 为空或不是 canonical 15 项、空 roots、重复/缺失/多余单元、悬空引用或 production→test-only 边均为 `False`。`manifest_schema_valid` 不再被当作可以隐式吞掉唯一性与版本规则的黑盒。

**Example:** Production fixture 声明完整 15 个 canonical units，扫描结果与其 exact-equal，source roots 为 1，悬空引用与 production→test-only 边均为 0 且 hash 匹配，结果为 `True`；只声明 3 个单元、缺少任一 canonical unit 或加入第 16 个单元时均为 `False`。需要小型算法单测时必须调用另行命名的参数化 helper，不得把 3-unit fixture 传给 production predicate 并期待 `True`。

### Scene Graph Validity

The `scene_graph_valid` formula is defined as:

`scene_graph_valid(G,U,N) = exact_graph_type(G) ∧ graph_source_is_canonical_choice_cfg_artifact(G) ∧ exact_node_catalog_type(N) ∧ U = canonical_production_units_v1 ∧ N = canonical_choice_node_topology_v1 ∧ raw_control_node_id_duplicate_count(G)=0 ∧ raw_edge_record_duplicate_count(G)=0 ∧ raw_scene_id_duplicate_count(G)=0 ∧ registered_ending_entries(G) = canonical_six_ending_entries ∧ entry_nodes_resolve(G,U) ∧ references_resolve(G) ∧ raw_choice_node_membership_exact(G,N) ∧ every_choice_has_exactly_one_owner_node(G,N) ∧ sibling_sets_are_exclusive(G,N) ∧ opener_and_guard_edges_exact(G,N) ∧ replacement_nodes_are_mutually_exclusive(G,N) ∧ route_commitment_active_count_is_one(G,N) ∧ all_registered_control_nodes_reachable(G,U) ∧ reachable_control_graph_terminates(G) ∧ major_choice_subgraph_is_DAG(G) ∧ every_maximal_path_reaches_exactly_one_ending_entry(G) ∧ no_ending_entry_returns_to_chapter_graph(G)`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| scene graph | `G=(V,E)` | exact finite directed graph | `|V|≥1, |E|≥0` | Scene、choice、reaction、payoff 及 ending-entry 控制节点 |
| content units | `U` | exact finite set | canonical 15 IDs | Manifest 中的章节、结局与真结局尾声单元 |
| node topology | `N` | exact finite catalog | `canonical_choice_node_topology_v1` | sibling sets、openers、guards、replacement groups 与 Day 6 route partitions |
| nodes | `V` | finite set | `1..N` stable IDs | 全部注册控制节点 |
| edges | `E` | finite set | `0..N²` directed edges | 静态 jump、call、return 及 choice continuation |
| registered scenes | — | finite set | `1..|V|` | 全部 required 与 optional scene records |
| ending entries | — | finite set | exactly six registered IDs | SYS-ENDING 拥有的六个结局入口 |

**Output Range:** exact `False` 或 `True`；空/错误类型、choice 未归属或归属多个 nodes、同一 traversal 串联 sibling choices、缺 opener、guard 不匹配、普通/replacement node 同时可用、Day 6 active route choice count 不是 1、任一 reachable SCC 含控制循环、悬空边、任一 registered control node 不可达、六 ending entries 不 exact-equal、无结局终点、多个结局终点或从 ending entry 返回章节图均为 `False`。引擎 rollback 与 UI interaction 重入不属于 production narrative graph edge。完整图仍须另行通过 SYS-CHOICE 的四项硬预算 gate。

**Example:** Production fixture 使用完整 15 units、canonical node catalog 与六个 ending entries；所有节点可达、每个 choice 恰属一个 node、conditional/replacement guards exact-match、choice 子图无环且每条终局路径恰到达 1 个 ending entry时结果为 `True`。只保留 2 个 ending entries、移除 `prologue_ask_destination` 却直接到 `prologue_accept_destination`，或在同一路径串联两个 siblings 时均为 `False`。

### Agency Transaction Validity

The `agency_transaction_valid` formula is defined as:

`agency_transaction_valid(t,S) = exact_transaction_type(t) ∧ exact_response_source_type(S) ∧ request_answer_join_valid(t) ∧ character_answer_derivation_valid(answer_derivation(t)) ∧ answer_state_registered_and_determinate(t) ∧ selected_answer_state(answer_derivation(t)) = answer_state_id(t) ∧ raw_response_choice_duplicate_count(t)=0 ∧ raw_accepting_choice_duplicate_count(t)=0 ∧ raw_overriding_choice_duplicate_count(t)=0 ∧ raw_response_binding_key_duplicate_count(t)=0 ∧ source_response_choices(S,t) = R(t) ∧ |R(t)| ≥ 1 ∧ response_after_answer(t) ∧ A(t) ∩ O(t) = ∅ ∧ A(t) ∪ O(t) = R(t) ∧ keys(response_outcome_bindings(t)) = R(t) ∧ (∀c∈R(t): |response_outcome_ids(c,t)| ≥ 1 ∧ raw_response_outcome_id_duplicate_count(c,t)=0 ∧ response_projection_valid(c,t) ∧ response_outcome_references_resolve(c,t)) ∧ resulting_outcome_ids(t) = ordered_unique_union(response_outcome_bindings(t))`

其中：

`character_answer_derivation_valid(d) = exact_answer_derivation_type(d) ∧ references_resolve(input_fact_ids(d)) ∧ allowed_answer_state_ids(d)=approved_answer_state_closed_set(transaction_id(d)) ∧ selected_answer_state_id(d)=apply_frozen_priority_rule(priority_rule_id(d),input_fact_ids(d)) ∧ selected_answer_state_id(d)∈allowed_answer_state_ids(d) ∧ |observable_action_or_object_ids(d)|≥1 ∧ references_resolve(observable_action_or_object_ids(d)) ∧ forbidden_hidden_input_count(d)=0 ∧ source_hash_matches(d) ∧ unresolved_defect_ids(d)=()`

`response_projection_valid(c,t) = (autonomy_delta(c)=1 ⇒ c∈A(t)) ∧ (c∈A(t) ⇒ ¬counterevidence_revokes_answer_domain(c,t)) ∧ (c∈O(t) ⇒ autonomy_delta(c)=0 ∧ (counterevidence(c)=null ∨ counterevidence_targets_answer_domain(c,t))) ∧ (counterevidence(c)≠null ⇒ counterevidence_reference_valid(c,t))`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| agency transaction | `t` | exact record | one transaction | 一次 request/answer/response 序列 |
| response source | `S` | exact CFG-derived record | one source response horizon | 从 answer 后至 transaction terminal outcome 的实际 response choice universe |
| response choices | `R(t)` | exact finite set | `1..N` choice IDs | 对已登记 answer 作出回应的全部选项；空集固定失败 |
| accepting choices | `A(t)` | finite set | `0..|R|` | 接受、遵循或维护 answer 的选项 |
| overriding choices | `O(t)` | finite set | `0..|R|` | 忽视、替代或推翻 answer 的选项 |
| autonomy delta | `autonomy_delta(c)` | exact int | `0..1` | Choice 对自主轴的批准投影 |
| counterevidence | `counterevidence(c)` | nullable exact record | `null` 或一个 effect | Choice 的反证投影 |
| registered outcomes | — | exact tuple | `1..N` IDs | Response 实际建立的人物或剧情结果；空 tuple 固定失败 |
| answer derivation | — | exact record | one record | 输入事实、候选 answer 闭集、唯一 selected state、可感知动作/物件证据、priority rule 与 source hash |

**Output Range:** exact `False` 或 `True`；缺失/含混/无 derivation 的 answer、derivation 读取禁止状态或不能唯一导出 answer、response 先于 answer、source CFG 有漏报或多报 choice、raw response/partition/binding/outcome 重复、choice 未分类或双重分类、任一 response 缺 outcome、aggregate outcomes 不等于逐 response 有序并集、accepting response 同时 revoke 当前 answer、override 获得自主正向增量或引用悬空均为 `False`。接受 answer 可以保持零增量，并可合法 repair 其他已登记 domain，但只有接受类 choice 允许产生 `autonomy +1`。

**Example:** 某 transaction 有 3 个 response choices：1 个 accepting choice 投影 `autonomy +1`，1 个 overriding choice 投影零增量，另 1 个 overriding choice 产生已登记 revoke effect；三项在 answer 后发生且 outcome 引用完整，结果为 `True`。若第二个 overriding choice 改为 `autonomy +1`，结果为 `False`。

### Character Continuity Validity

The `character_continuity_valid` formula is defined as:

`character_continuity_valid(s,C,R) = exact_scene_type(s) ∧ exact_constraint_catalog_type(C) ∧ exact_review_catalog_type(R) ∧ active_characters(s) ≠ ∅ ∧ (∀c∈active_characters(s): raw_matching_constraint_count(s,c,C)=1 ∧ let k=only_matching_constraint(s,c,C): sources_resolve(k) ∧ approval_valid(k) ∧ constraint_version_matches_scene(k,s) ∧ structural_bounds_pass(s,k) ∧ raw_matching_review_count(s,k,R)=1 ∧ let r=only_matching_review(s,k,R): review_source_hash(r)=scene_source_hash(s) ∧ checklist_complete(r) ∧ unresolved_defect_ids(r)=())`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| narrative scene | `s` | exact record | one production scene | 被验证的场景 |
| constraint catalog | `C` | finite exact catalog | `1..N` records | 已批准人物设定约束 |
| review catalog | `R` | finite exact catalog | `1..N` records | source-hash-bound `character_scene_review_record` |
| active characters | — | finite set | `1..N` character IDs | 场景中实际行动、发言或作决定的人物 |
| matching constraints | — | finite set | `0..N` records | 当前人物及版本适用的 constraint records |
| structural check | — | exact bool | `False/True` | 检查来源、语言、知识、动机和禁止行为字段 |
| manual review | — | exact bool | `False/True` | 逐场景人物设定人工审核结果 |

**Output Range:** exact `False` 或 `True`；raw catalog 中人物缺少或重复约束、重复 review、所选 constraint 的来源/版本/approval 无效、scene hash 与审核记录不一致、checklist 缺项、存在 unresolved defect 或超出知识/语言边界均为 `False`。唯一性在 validity predicate 之前按 raw records 计数，失效的重复项不能被过滤后掩盖。裸 `manual_review=True` 不再构成证据。

**Example:** 某场景有路明非与绘梨衣 2 名 active characters，各恰匹配 1 项已批准 constraint；结构检查和人工审核均通过，结果为 `True`。若绘梨衣在该场景用完整口语解释玩家行为，即使其他引用有效，人工与语言约束检查仍为 `False`。

### Chapter Recovery Coverage

The `chapter_recovery_coverage_valid` formula is defined as:

`chapter_recovery_coverage_valid(D,A,P) = exact_source_chapter_type(D) ∧ exact_anchor_catalog_type(A) ∧ exact_payoff_catalog_type(P) ∧ D = canonical_source_chapters_v1 ∧ |D| = 7 ∧ duplicate_anchor_id_count(A)=0 ∧ duplicate_payoff_id_count(P)=0 ∧ orphan_anchor_or_payoff_count(A,P)=0 ∧ all_anchor_and_payoff_records_well_formed(A,P) ∧ (∀a∈A: |P(a)|≥1 ∧ raw_payoff_owner_count(a,P)=1 ∧ (∀p∈P(a): anchor_kind_valid(a) ∧ chapter_rank_defined_and_unique(source_chapter(a),p) ∧ chapter_rank(payoff_chapter(p)) > chapter_rank(source_chapter(a)) ∧ causal_proof_valid(a,p) ∧ perceptible_difference_valid(p))) ∧ (∀d∈D: |A(d)|≥1)`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| source chapters | `D` | exact ordered set | canonical 序章至第六日，恰 7 项 | 每个都必须建立至少一个跨章节回收锚点 |
| chapter anchors | `A(d)` | finite set | `0..N` records/chapter | 当章建立的具体元素 |
| payoff candidates | `P(a)` | finite set | `1..N` records | 声明回收该锚点的后续 payoffs；每个 anchor 必须非空 |
| anchor kind | — | enum | object/information/promise/character_decision/route_resource/relationship/consequence | 用户批准的七类回收元素 |
| chapter rank | — | exact int | 序章至 ending 的固定顺序 | 判断回收是否严格发生在后续章节 |
| causal proof | — | exact bool | `False/True` | History guard 或 counterfactual registered outcome 证明 |
| perceptible difference | — | exact bool | `False/True` | 剧情、人物状态、资源、路线或结局发生可感知差异 |

**Output Range:** exact `False` 或 `True`；`D` 为空或不是 canonical 7 项、anchor/payoff 重复或悬空、任一 anchor 没有 payoff、payoff 多 owner、chapter rank 未定义/重复、序章至第六日任一章节没有跨章节锚点、catalog 中任一 payoff 不严格较晚、只有重复提及或更换台词、缺少因果证明时均为 `False`。每 anchor 非空量词与全 catalog universal well-formedness 先于逐章覆盖存在量词，因此空 `P(a)` 或一个合法 pair 都不能掩盖坏 pair。

**Example:** 序章至第六日共 7 个 source chapters，每章至少登记 1 个锚点及 1 个严格较晚 payoff；其中第一日的人物决定在第四日改变车票准备，第六日的承诺在结局改变代价承担者，7 章全部覆盖时结果为 `True`。若第三日只在第五日重复提到同一信息但人物状态、资源、路线和结局均未变化，则第三日不计入覆盖，整体结果为 `False`。

上述五项通过后，仍须分别通过 SYS-CHOICE 的 surface、join、payoff coverage、dominance 和恢复验证，以及 SYS-ENDING 的 qualification、terminal class 与 witness 验证；本节不复制这些公式。

所有五个 public predicates 都采用 staged total validation：exact-type gate 失败立即返回 `False`，不得继续调用 record accessor；小型参数化 helpers 使用不同名称，不能改变 production predicates 的 canonical constants。`systems-designer` boundary review incorporated: empty-set truth, raw duplicates, bad-pair masking, source-response omissions, implicit variables, stale constraint review and nonterminating graph counterexamples now fail explicitly.

## Edge Cases

### Manifest 与记录完整性

- **If production manifest 的 roots 为空、expected units 缺失或 source hash/version 不匹配**：内容构建立即失败，不扫描场景且不生成任何可用 catalog。
- **If 实际扫描单元比 approved required units 少或多**：内容构建失败，并报告缺失或多余的 exact unit IDs；不得自动忽略多余章节。
- **If 任一 chapter、scene、choice、reaction、payoff、event、resource、outcome 或 witness ID 重复**：在引用连接前失败，不允许“最后声明覆盖前一声明”。
- **If 任一引用悬空、指向 test-only fixture 或跨越 manifest exclusions**：内容构建失败，且后续 graph、coverage 与 ending validators 不运行。
- **If `.rpy` 对白修订改变了控制流、人物决定、事件结果或资源结果，但对应 production record 未更新**：source hash失效，catalog freeze失败；不得把它作为纯文案修改放行。

### 场景图与路线

- **If 任一 registered scene 不可达、存在悬空 jump、重大选择图形成 cycle，或某条合法路径不能到达 ending entry**：`scene_graph_valid=False`，内容构建失败。
- **If 同一 terminal path 到达零个或多个 ending entries**：内容构建失败；固定结局优先级不得掩盖叙事图错误。
- **If ending entry 返回第一日至第七日的章节图**：内容构建失败；尾声只能消费已选结局，不得重新形成结局输入。
- **If 分支重新汇合时丢失应保留的 history、unresolved token、路线资源或适用 payoff**：汇合点无效，必须拆分 continuation 或保留可证明的分支差异。
- **If 一条看似合法的捷径绕过必需场景、代价或已登记人物决定**：该路径视为 unintended interaction，必须从图中移除或登记为完整合法分支；不得作为中性捷径保留。
- **If 全图超过4096 terminal paths、65536 triples、1048576 continuation entries或64 MiB artifact任一硬上限**：在最早可判定阶段失败；不得采样、截断或合并不同人物归宿。

### Choice、reaction 与 payoff

- **If 玩家确认 choice 后、reaction-state establishment 前出现 interaction、存档、jump、call、return 或另一 choice**：内容构建失败；必须恢复无交互的 commit→establishment 区域。
- **If reaction-state establishment 后不是恰一次 bounded presentation interaction，或该 interaction 允许 quick actions、game menu、save/load、rollback、skip、history return、重复 activation 或语义写入**：engine evidence 失败；异常退出还必须恢复所有临时输入 gate，避免永久禁用。
- **If 同一次正常 traversal 中choice未提交、提交多次或reaction未发生、发生多次**：执行证据失败；不得使用独立ledger补记或去重。
- **If 同一场景有多个合法payoff同时满足**：按 `narrative_scene_record.payoff_ids` 的冻结tuple顺序全部执行；每个payoff在该观察窗口最多一次，并在进入下一choice前完成。
- **If 多个适用payoff缺少稳定顺序或形成互相矛盾的outcome states**：内容构建失败；作者必须声明兼容顺序或拆分为互斥路径。
- **If payoff只重复提及旧元素、替换台词、镜头、滤镜或音效，而人物状态、剧情、资源、路线和结局均未发生可感知差异**：该payoff不计入因果或章节回收coverage。
- **If 多个choices共享一个payoff，但缺少逐choice history guard、counterfactual outcome或独立semantic evidence**：所有相关bindings失败，不允许用通用事件同时回收。
- **If skip、auto或快速点击会跳过唯一reaction/payoff事实**：该演出不合格；必须保留最终姿态、物件状态、文本或描述性摘要后才能继续。

### Agency transaction

- **If Day 4 票、路线或联系人准备没有先展示并登记 `preserve_executable_self_controlled_option` answer**：相关 response nodes 不得冻结；票或联系人不能仅因资源投影正确就被视为尊重绘梨衣自主。
- **If Day 5 route answer 不是由 `erii_route_answer_derivation:v1` 对已知资源事实唯一导出，或动作/物件证据与 selected state 不一致**：answer 为 `undetermined`，Day 5 response 与 Day 6 commitment 均不得出现。
- **If 玩家提出request但绘梨衣尚未产生可登记answer**：transaction保持未完成，不出现response choice，也不产生autonomy增量。
- **If 绘梨衣保持沉默且上下文不能区分接受、拒绝或未决定**：沉默不得登记为同意；场景必须增加可理解的动作、物件或确认机会，否则阻止冻结。
- **If 绘梨衣在玩家response前明确改变answer**：旧transaction以无语义增量的未完成状态关闭，并以新answer开启新的transaction；后续choice不得继续引用旧answer。
- **If response choice同时属于accepting与overriding，或两类均不属于**：`agency_transaction_valid=False`，内容构建失败。
- **If source CFG 反推的 response choice 与 transaction 自报集合不 exact-equal，或任一 response 没有非空 outcome binding**：内容构建失败，并报告 missing/extra response IDs；不得通过省略 replacement/reconsideration 分支使 partition 假通过。
- **If raw response、accepting/overriding tuple、binding key 或 per-response outcome tuple 含重复，或 `resulting_outcome_ids` 不等于逐 response outcome 的有序无重复并集**：在集合化前失败；不得用 set 语义吞掉重复或孤儿 outcome。
- **If overriding choice获得`autonomy +1`且没有被验证器拒绝**：视为合同破坏，阻止catalog freeze；不得通过改写玩家可见文案掩盖。
- **If 玩家早期接受answer、后来又推翻同一人物决定**：早期正向历史不被删除；后续行为必须按SYS-CHOICE登记零增量或counterevidence，并在结局与payoff中保留其后果。
- **If transaction outcome与绘梨衣实际动作或人物状态不一致**：以不一致失败处理，不允许以作者意图或旁白解释替代registered outcome。
- **If Day 6 初次把代价转嫁给绘梨衣**：先关闭 `agency_day6_cost` 并建立可感知 consequence；只有新的 request/answer 完成后才可进入 `agency_day6_cost_reconsideration`。不得把 `take_cost_back/leave_cost_shifted` 塞回旧 transaction，也不得在 consequence 前立即修复。

### 人物设定

- **If active character没有恰好一个适用且已批准的`character_constraint_record`**：场景不得进入production catalog。
- **If 两个来源对同一人物的语言、知识、动机或关系边界互相冲突**：不自动选择较新或较宽松来源；阻止场景冻结，直到人工批准明确的constraint版本。
- **If 人物说出尚未获得的信息、无因改变核心动机，或仅为连接分支而接受此前明确拒绝的安排**：人工人物审核失败，相关scene及其下游paths均不得冻结。
- **If 绘梨衣使用完整口语或连续书面文本解释复杂意图、隐藏评分或正确答案**：内容审核失败；必须改为符合既有约束的动作、视线、物件、停顿、上下文或简单单音节。
- **If character constraint 的批准被撤回或其来源失效**：所有引用该constraint的scene变为unfrozen，必须重新审核后才能恢复production状态。

### 跨章节回收

- **If 序章至第六日任一章节没有至少一个跨章节回收锚点**：`chapter_recovery_coverage_valid=False`，内容锁定失败；不要求每个场景单独建立锚点。
- **If 任一 anchor 的 payoff tuple 为空、payoff ID 重复或同一 payoff 被多个 anchor 非法拥有**：在全称量词前失败；空 `P(a)` 不得以 vacuous truth 通过。
- **If 第六日锚点只在同章重复出现**：不计入跨章节coverage；其合法回收必须发生在第七日或结局。
- **If 一个锚点被后续场景提及多次，但没有任何一次产生可感知差异**：所有提及均不计为payoff。
- **If 同一payoff同时声称回收互相矛盾的anchor states**：必须拆分为互斥outcomes；不得用模糊摘要合并。

### 第七日与结局

- **If 第七日新增万能正向分数、提供最终覆盖选择或直接修改qualification**：内容构建失败；第七日只能承认和回收既有因果。
- **If terminal path派生出两项以上route qualifications**：内容构建失败；不得依靠ending priority选择其一。
- **If Day 6 route commitment screen 的 active choice count 不是 1，或 active choice 与已 honored/overridden 的 Day 5 answer state及资源不一致**：内容构建失败；UI 不得把五项显示为结局预览菜单。
- **If reachable ending缺少canonical witness、terminal-cause class、具体payoff或玩家摘要**：该结局内容不完整，不能锁定production catalog。
- **If resolver返回错误或snapshot validation失败**：叙事流程保持`Active`，不进入任何ending label，也不触发persistent、achievement或journal更新。
- **If 结局演出引入新的source fact反向证明自身成立**：该fact无效并阻止内容冻结；结局只能消费ending entry之前形成的选择、事件与资源。

### Save、rollback 与替代输入

- **If load或rollback恢复到已登记checkpoint**：严格采用SYS-CHOICE批准的checkpoint-kind计数；不得重播已完成reaction/payoff或漏播其未来实例。
- **If load、rollback、skip或脚本修改使流程到达未登记control location**：进入既有阻断式安全流程；不得猜测scene、修补history或自动跳到邻近label。
- **If 鼠标、键盘、替代输入或无障碍路径解析到不同canonical choice IDs**：内容集成失败；所有等价输入必须进入同一choice record。
- **If 某条路线只能通过hover、动画、声音、限时输入或调试信息理解或继续**：该路线不合格；必须提供非限时、键盘可达且静音可理解的正式路径。

> `systems-designer` and `narrative-director` findings incorporated; production content still requires source-hash-bound automated and human evidence before freeze.

## Dependencies

系统索引中的主设计顺序保持：

`SYS-STATE → SYS-ENDING → SYS-CHOICE → SYS-NARRATIVE`

SYS-NARRATIVE 的索引级硬依赖继续记录为 `SYS-CHOICE + SYS-ENDING`；下表补充运行时、内容锁定与下游集成关系。

| Dependency | Strength | Direction | Required Interface | Owner / Current Status |
|---|---|---|---|---|
| Ren’Py 8.5.3 | Hard runtime | Engine → SYS-NARRATIVE | 静态 label、menu、jump/call/return、rollback-aware 控制位置与分章 `.rpy` | Engine pinned；章节内容不得使用未登记动态控制流 |
| Game Concept | Hard design authority | Concept → SYS-NARRATIVE | 四项创作支柱、七日结构、六结局、绘梨衣表达边界及 70–90k 字目标 | Approved |
| ADR-0003 | Hard architecture boundary | ADR → SYS-NARRATIVE | 分章文件、内容/表现分离、稳定 asset names、screen 不决定叙事结果 | Accepted |
| Seven-day content baseline | Hard narrative authority | Baseline → SYS-NARRATIVE | 15 units、required beats、54 choices、9 agency records、7 tokens、4 qualification bindings、6 complete ending histories、11 cause-family production variants | `narrative_content_baseline:v1.2` frozen；exact terminal classes require enumeration |
| Character constraint catalog | Hard content-lock input | Character sources → SYS-NARRATIVE | 每个 active character 恰有一个适用且已批准的 constraint record | v1 active-character 闭集为路明非+绘梨衣；新增人物必须先登记并重审 |
| SYS-CHOICE | Hard content-build | Bidirectional | choice declarations、canonical `choice_source_scanner:v1` CFG artifact、reaction/payoff bindings、semantic evidence、DAG 与恢复验证 | Approved with provisional downstream gates；SYS-NARRATIVE 只消费 canonical CFG artifact，不建立第二 scanner |
| SYS-STATE | Hard indirect runtime | SYS-NARRATIVE → SYS-CHOICE → SYS-STATE | 只通过批准的 choice commit 改变 ordered history 与 axes | Approved；SYS-NARRATIVE 不得直接写入 |
| SYS-ENDING | Hard content-build/runtime output | Bidirectional | qualification sources、counterevidence 内容、terminal witnesses、outcome signatures；返回 selected ending | Approved with provisional downstream gates；不得修改 resolver invariant |
| SYS-SAVE | Hard integration | Bidirectional | 同时恢复 semantic state 与正确叙事控制位置；共用 blocking safe flow | Not Started |
| SYS-ACCESS | Hard downstream gate | SYS-NARRATIVE → SYS-ACCESS | choice 等价输入、accessible causal summaries、键盘/静音/reduced-motion 可理解路径；UX 为交付角色而非 system ID | Designed（完整复审待完成）；不阻止 GDD 设计，实装证据仍阻止 production content lock |
| SYS-TEST | Hard validation gate | SYS-NARRATIVE → SYS-TEST | source manifest、catalog、完整 scene graph、canonical witnesses、negative fixtures 与无调试 playtest 内容 | Not Started；阻止跨系统集成封板 |
| SYS-PERSIST | Downstream read-only | SYS-NARRATIVE → SYS-PERSIST | 已完成 ending、memory 与批准的跨周目解锁事件 | Not Started；不得反向影响当前路线 |
| SYS-ACHIEVE | Downstream read-only | SYS-NARRATIVE → SYS-ACHIEVE | 已完成具体叙事事件与 witness IDs | Not Started；不得读取 axis/token/qualification |
| SYS-JOURNAL | Downstream read-only | SYS-NARRATIVE → SYS-JOURNAL | 两个v1 source catalogs、7×2 player-safe copy与逐日common-path truth approvals | In Revision；不得泄露交集外逐traversal事实或未发现路径 |
| SYS-AUDIO | Soft presentation | SYS-NARRATIVE → SYS-AUDIO | 情境音、单音节、声音动机与描述性字幕需求 | Not Started；静音仍须完整可玩 |
| Art Bible / asset pipeline | Soft presentation | SYS-NARRATIVE → Art | 人物动作、物件、环境、构图及稳定 semantic asset 需求 | Not Started；允许占位资产 |
| SYS-TENSION | Optional enhancement | SYS-TENSION → SYS-NARRATIVE | post-MVP 已登记 timeout 结果及非限时等价路径 | Deferred；默认关闭且不属于当前 P0 Production 硬要求 |
| SYS-BUILD | Downstream packaging | SYS-NARRATIVE → SYS-BUILD | 收录 source-hash-bound compiled catalogs 与章节脚本 | Not Started；发行包不得包含 test-only fixture 或运行时 source scanner |

### Interface Boundaries

- SYS-NARRATIVE 创作内容 records及 chapter/unit projection；SYS-CHOICE 独占 choice schema、提交顺序、source scanner、canonical CFG artifact、join 与 graph validators。`scene_graph_valid` 只对同一 artifact 增加 narrative ownership/termination 检查。
- SYS-NARRATIVE 提交终局前 sources 与结局演出；SYS-ENDING 独占 predicate、priority、resolver、selected ending 和 `Active → Ended`。
- SYS-NARRATIVE 不建立独立状态、存档、reaction/payoff ledger、qualification cache 或 persistent route flags。
- SYS-PERSIST、SYS-ACHIEVE 与 SYS-JOURNAL 只能在具体叙事结果完成后消费批准事件，不能反向改变选择或结局；Journal 只能消费两个owner-signed source catalogs，不得读取history生成path-specific摘要。
- SYS-AUDIO 与美术资产可以增强因果可读性，但不得成为唯一信息通道或内容可达性的前提。

#### SYS-NARRATIVE → SYS-ACHIEVE

`achievement_event_catalog:v2` 与逐项责任 scene 以 [七日内容基线](../narrative/seven-day-content-baseline.md) 为 normative source。每个稳定完成点只构造一个 exact `achievement_evidence_snapshot`：

`catalog_generation_id, collection_epoch_id, checkpoint_occurrence_id, checkpoint_id, completed_event_ids, newly_completed_event_ids, stable_completion_boundary`

- `collection_epoch_id` 在显式 New Game 时从 SYS-PERSIST detached root复制到 rollback-owned run envelope；load/rollback 恢复 save 中原值，不从当前 root 静默改写。
- `checkpoint_occurrence_id` 在当前 run envelope 中唯一并随 rollback 恢复；同一 occurrence 的跨 kind结果由唯一 persistence checkpoint coordinator 合批。
- `completed_event_ids` 是 canonical、唯一、有序累计 tuple；`newly_completed_event_ids` 必须是其 canonical tail，且每项都映射到当前 checkpoint。
- Ending completion additionally emits the exact `ending_completion_event_record` owned by SYS-ENDING: `ending_id, completed_event_id, checkpoint_id, checkpoint_occurrence_id, collection_epoch_id, catalog_generation_id, stable_completion_boundary, owner_system`. Its only callsite is the terminal completion node after final player-visible closure; `completed_event_id` is `ending_completed:{ending_id}`.
- Snapshot 不包含 axes、history、token、qualification、resource、ending predicate 或 resolver record。
- Snapshot epoch 与当前 root 不一致时，SYS-ACHIEVE 固定拒绝；叙事可继续，但必须显式 New Game 才重新启用成就求值。

### Required Ordering

1. 批准人物 constraint records 及 SYS-NARRATIVE 章节/场景合同。
2. 完成 production choice、reaction、payoff、event、resource、outcome 及 agency records。
3. 通过 SYS-CHOICE catalog/join/graph 验证。
4. 提交 SYS-ENDING qualification bindings、terminal witnesses 与 cause classes。
5. 完成 SYS-SAVE、SYS-ACCESS 及 SYS-TEST 集成证据。
6. 只执行一次既定的 `SYS-CHOICE/SYS-NARRATIVE → SYS-ENDING Cross-System Integration Validation`；locked resolver invariants 未变化时不重新运行完整 SYS-ENDING 审查。

## Tuning Knobs

SYS-NARRATIVE 的调节项只控制内容规模、节奏与分配，不得修改 choice schema、五轴范围、counterevidence 规则、qualification 语义、ending predicate 或验证预算。

| Tuning Knob | Target / Safe Range | Too Low | Too High | Validation / Source |
|---|---|---|---|---|
| `total_text_characters` | `70,000–90,000` 简体中文字符目标 | 七日关系发展和跨章回收缺少铺垫 | 制作、校对、分支验证与首轮时长膨胀 | Game Concept；超出触发内容范围复核，不单独使构建失败 |
| `chapter_word_allocation` | 各单元为正数，总和服务于总文本目标 | 必需章节无法完成其人物决定与回收责任 | 单章挤压其他章节或形成节奏失衡 | Narrative review；不冻结统一百分比 |
| `required_scene_count` | 每个 production unit 至少 1 个可达 required scene；上限由完整图预算约束 | 章节责任或结局回收不完整 | 必经内容过长，削弱选择差异并扩大全部路径 | `scene_graph_valid`、完整路径枚举 |
| `optional_scene_count` | `0..N`；允许为 0，无独立硬上限 | 路线差异和人物呼吸空间减少 | 路线组合、字数、资产和验证成本膨胀 | 4096/65536/1048576/64 MiB 预算 |
| `choice_class_mix` | 按内容需要组合 `semantic_major` 与 `narrative_only`；不设逐章数量配额 | 关键人物决定缺少正式语义记录 | 玩家持续面对“重大选择”，稀释日常观察与节奏 | SYS-CHOICE classification 与 coverage |
| `evidence_opportunities_per_axis` | 内容基线为每轴冻结 4 项独立 recovery opportunities；额外机会总安全范围 `4–6`；任一路径同轴同章 `0–1` | 错过早期机会后无法恢复，结局不可达 | 过早封顶并使选择趋同 | Recovery Opportunity Matrix、五条 earliest-miss witnesses、SYS-CHOICE |
| `zero_delta_major_choice_ratio` | 目标 `45–65%`，安全 `35–70%`；v1.2 baseline 为 `30/52 = 57.7%` | 玩家可能把所有选项理解为隐藏加分题 | 过多重大选择若又缺少 event/resource/token/outcome 差异，会变成空选择 | Entity Registry / SYS-CHOICE；零 axis 不等于零语义，仍须有正式 route fact、counterevidence、repair 或 outcome |
| `cross_chapter_anchor_count` | 序章至第六日每章 `1..N`；最低 1 项不可下调 | 章节成为孤立事件，连续回收合同失败 | 过多元素竞争注意力，payoff 与路径负担膨胀 | `chapter_recovery_coverage_valid` 与人工可读性审核 |
| `anchor_kind_mix` | object/information/promise/character_decision/route_resource/relationship/consequence 七类中按章选择 | 全部依赖同一媒介，回收单调或不适合人物 | 单章同时承担过多不同语义 | Chapter recovery catalog review |
| `payoff_distance` | 普通 choice 必须严格较晚；跨章锚点至少晚 1 章，最迟可在适用结局回收 | 反应与回收重叠，玩家感受不到时间重量 | 间隔过长导致玩家无法识别来源 | Payoff witness、semantic evidence 与无调试 playtest |
| `branch_width` | 无独立数值目标；保持满足六结局和人物差异所需的最小充分宽度 | 选择不改变 continuation、人物去向或代价 | 路径与 terminal classes 组合爆炸 | Dominance、reachability 与完整图预算 |
| `terminal_cause_classes_per_ending` | 目标 `1–6`，`7–12` 触发范围复核，`>12` 构建失败 | `0` 表示结局缺少 witness/payoff/causal coverage | 过多不同归宿和代价难以制作与解释 | SYS-ENDING 唯一 source of truth |
| `reaction_presentation_length` | 足够读懂一次人物反应；不设统一秒数 | 反应不可感知，choice 像被吞掉 | 打断阅读节奏并拖慢重复游玩 | 人工演出审核、skip/auto 与无调试 playtest |
| `character_constraint_granularity` | 每个 active character 每个场景恰解析到一个适用版本 | 约束过宽，无法判断人物是否失真 | 版本过碎导致大量无意义审核分支 | `character_continuity_valid` |

### Interaction Rules

- 增加 optional scenes、choice 数量或 anchor 数量，会同时增加文本量、payoff bindings、continuation witnesses 与路径预算消耗。
- 增加 semantic-major choices 时，必须同步提供 reaction、strictly-later payoff、semantic evidence 及适用 axis/counterevidence 投影。
- 延长 payoff 距离时，必须保持来源可识别；距离不能替代具体因果证明。
- 减少 branch width 不得通过合并不同人物归宿、代价承担者或悲剧闭环实现。
- 字数目标不优先于人物设定、章节责任、因果回收或首周目六结局可达性。

### Not Tunable Here

以下值由上游合同独占，不属于 SYS-NARRATIVE 调节项：

- 五轴名称、`0..3` 范围与单次 `+1` 投影；
- counterevidence 总量、domain cap 及 repair/irreversible 规则；
- route qualification 语义、ending predicate 与固定优先级；
- 四项完整图编译硬预算；
- commit→reaction 顺序、payoff 严格较晚及恢复点计数；
- 第七日不得新增万能分数或最终覆盖选择。

## Visual/Audio Requirements

### Visual Direction

SYS-NARRATIVE 采用克制、观察者式的因果演出。视觉反馈优先来自人物距离、视线方向、手部动作、停顿、呼吸、物件位置与环境变化，不使用突兀特写、道德化滤镜或胜负式特效替玩家解释选择。

- Reaction 必须让玩家在 choice 提交后看见人物或环境的即时变化。
- Payoff 必须让先前建立的具体元素再次出现并改变状态；仅重复构图或更换背景色不构成回收。
- 镜头优先使用中近景、手部和物件细节、人物间留白及普通生活动作。
- 收伞、递物、候车、整理衣物、放置车票、握住或松开物件等动作优先于宏大奇观。
- 悲剧结局必须清楚呈现代价承担者、人物去向或未完成之物，但不以血量式损伤、红色警告或失败评分呈现。
- 真结局的满足来自此前物件、承诺和普通生活愿望完成闭环，不使用“全收集”式视觉庆祝泄露内部条件。

### Chapter Visual Anchors

| 单元 | 主要视觉锚点 | 跨章用途 |
|---|---|---|
| 序章 | 雨、愿望纸、站台泥痕、伞与人物距离 | 第一日重新理解愿望；第六日回收最初路线与观察方式 |
| 第一日 | 便服、食物、名字或点单动作 | 第四、五日确认绘梨衣是否拥有真实决定权 |
| 第二日 | 两枚游戏币、屏幕昵称、普通网吧物件 | 盟友识别及真结局普通生活尾声 |
| 第三日 | 空教室、被隐藏或交出的信息物件 | 第五日信任与第六日服从/反抗关系 |
| 第四日 | 车票、路线图、联系人记录、车窗与海 | 第六日撤离能力及人物去向 |
| 第五日 | 家族真相的具体载体、被保留或交出的物件 | 第七日共同决策与结局原因 |
| 第六日 | 失效的安全屋、备用出口、已消耗资源、兑现的承诺 | 第七日或结局中的代价承担者与路线资格 |
| 第七日 | 红井前的空间关系、前六日留下的物件与人物站位 | 承认既有因果，不制造新的万能答案 |
| 结局与尾声 | 未完成物件、空位、列车、海、名字或普通网吧生活 | 回收具体 cause、loss、人物归宿与普通未来 |

锚点只规定语义身份和状态变化，不在本 GDD 冻结最终画风、镜头尺寸、资产分辨率或逐镜头清单。

### Character Performance

- 绘梨衣只通过视线、身体动作、停顿、物件互动和简单单音节表达即时回应。
- 路明非可以复述自己的理解，但画面必须给绘梨衣明确确认、否认、拒绝或暂不回答的空间。
- 其他人物的姿态、动作与距离必须遵守其 approved `character_constraint_record`。
- 人物 reaction 不得直接面向玩家解释“做对了”“分数增加”或结局条件。
- 同一人物决定在后续 payoff 中必须保留可识别动作或物件 lineage，同时产生新的可感知状态。

### Audio Direction

- 情境音优先于说明性配乐：雨、纸张、衣料、脚步、呼吸、门窗、硬币、列车、城市底噪及物件接触。
- 音乐可以支持章节情绪，但不得用固定和弦、主题或音效暗示 axis 增量、token 状态、qualification 或“正确选项”。
- 允许有意静默；沉默用于节奏与人物状态，不自动等同绘梨衣同意。
- 绘梨衣的简单单音节必须提供字幕。
- 承担因果信息的重要非语音声音必须拥有可关闭的描述性字幕或等价可见结果。
- 每个 production speech/audio cue 必须通过 `audio_accessibility_binding_record` 恰绑定一个 subtitle/alt identity；单音节字幕还必须声明 `answer_state_id`，并与确认、否认、拒绝或暂不回答的 registered outcome 一致。
- Audio 缺失、静音或设备不可用时，所有路线仍必须完整可玩并可理解。

### Accessibility and Reduced Presentation

- Reaction/payoff 的唯一事实不得只存在于颜色、声音、动画、镜头运动或 hover 状态。
- Reduced-motion 模式可以替换动画，但必须保留相同最终 pose、物件状态、文本或 summary identity。
- Immediate bounded reaction interaction 固定暂停 skip 与 AFM/auto，直到最终 pose、物件状态、字幕或 summary identity 建立；后续非关键演出与 payoff presentation 可以缩短，但不得跳过唯一可感知因果事实。
- Self-voicing 与描述字幕消费 SYS-ACCESS 批准的 `accessible_causal_summary_id`，不得朗读内部 IDs 或判定结构。Summary只可陈述 source semantic fact 已登记的可观察动作、物件、声音、已确认回答与当前后果，必须保留原场景的 epistemic certainty/ambiguity，不得替绘梨衣宣告未确认内心。
- 所有会影响下一步理解或决定的 request、answer/confirmation/refusal、reaction、payoff、ending cause及重要audio/environment facts都属于独立发现的 `U_ACCESS_SUBJECT`；reaction/payoff-only scanner 不构成完整覆盖。
- Decision-critical summary 必须在下一 choice/action 解锁前进入批准的 accessible transcript/backlog或保持可重访；该记录复用 canonical summary identity，只服务表现，不形成第二条因果 history。
- 所有因果场景必须在 1280×720 基线、键盘操作和静音状态下保持可推进。

### Asset Boundary

- 本 GDD 只冻结 scene、reaction、payoff 与 chapter anchor 的叙事语义需求和 stable content IDs，不宣称逐资产 identity 已冻结。
- Art Bible 冻结画面语言、人物造型、色彩、构图和动作词典。
- `/asset-spec system:seven-day-chapter-script` 负责生成逐资产描述、尺寸、变体、来源登记和制作提示。
- 每个新增图像必须登记来源，并提供计划中的 self-voicing 替代文本。
- Q11 与 Art Bible 批准后才冻结逐资产 stable semantic names、cue IDs、替代文本与 source registrations；Final assets 可以替换 placeholder，但不得改变这些已批准 identities、叙事控制流或 registered outcome。

> `audio-director` review incorporated. `art-director` review remains a downstream Art Bible gate and is not claimed complete here.

## UI Requirements

SYS-NARRATIVE 不新增独立 HUD、路线图、因果日志或叙事引擎界面。它向既有视觉小说 screen、SYS-CHOICE choice surface、SYS-ENDING cause-card flow 及下游 journal 提供批准的玩家可见内容；具体布局、焦点几何和响应式规则由 SYS-ACCESS 拥有，UX Designer 是交付角色而不是独立 system ID。

### Player-Facing Content

| Surface | SYS-NARRATIVE 提供 | 禁止内容 |
|---|---|---|
| Dialogue / narration | 对白、旁白、说话者身份及必要的非语音描述 | axis、token、qualification、predicate 或开发注释 |
| Chapter title | 当前日、章节名及玩家安全副标题 | 未到达章节、路线要求或结局提示 |
| Choice surface | 准确描述玩家即将采取的具体行为 | “正确”“最佳”“善良”“真结局”等评价或攻略标签 |
| Immediate reaction | 人物动作、视线、物件状态、简单单音节及等价字幕 | 分数变化、成功提示或内部 choice ID |
| Later payoff | 具体人物、物件、信息、资源、路线或结局差异 | 只有“系统记住了”之类抽象提示 |
| Ending cause cards | SYS-ENDING 批准的 matched cause 与有限附加原因文案 | 裸阈值、完整 exclusion matrix、token 目录或优先级 |
| Journal / memory | 已完成章节与回忆的玩家安全摘要 | 未发现路线、未触发 payoff 或隐藏结局条件 |
| Accessibility output | `accessible_causal_summary_id` 对应文本 | 内部 record 名称、测试术语或替玩家作道德判断 |

### Choice Presentation

- 每个 choice label 必须描述行为本身，使鼠标、键盘和替代输入使用者面对相同语义。
- Day 6 route commitment 的玩家文案只能描述当下执行动作，禁止出现结局名、路线评级、“没有更好选择”等结果性标签；route guard 已使 active choice count 恰为 1，UI 不得把不可用的四项显示成预览。
- 选项顺序来自 SYS-NARRATIVE 冻结记录；UI 不得按隐藏状态、预测结局或设计者偏好重新排序、推荐或高亮。
- Choice surface 只使用 SYS-CHOICE 批准的 `idle`、`focused`、`pressed`、`confirmed`、`disabled` 与 `timeout` presentation states；视觉状态不得改变 choice 语义，其中 `timeout` 仅在 SYS-TENSION 启用时使用。
- Self-voicing 可以朗读焦点文本，但不得自动确认 choice。
- 除可选 SYS-TENSION 模式外，所有正式路线必须存在非限时可达版本；timeout 结果也必须解析到已登记 choice。
- 不得要求 hover、精确指针移动、动画完成或声音提示才能理解或确认 choice。

### Reaction and Payoff Presentation

- Choice 确认后，choice surface 必须在 reaction-state establishment 前退场。
- `ChoiceCommitted → ReactionEstablished` 为无交互原子区；随后恰有一次 bounded reaction-presentation interaction。该 interaction 期间 game menu、quick save/load、rollback、skip、AFM/auto、history return、重复 activation 及所有可转移控制的快捷键均不可见或 disabled/unfocusable。
- Bounded interaction 返回并记录 `ReactionCompleted` 后，首个 `after_reaction` checkpoint 才允许恢复常规 quick actions；异常路径也必须执行同一 input-gate cleanup。
- Quick actions 不得覆盖人物手部、关键物件、描述字幕或因果摘要。
- 多个 payoff 在同一场景触发时，UI 按 `narrative_scene_record.payoff_ids` 冻结顺序呈现，完成全部适用 payoff 后才显示下一 choice。
- Bounded immediate reaction 完成前 skip/auto 不得推进；进入 `ReactionCompleted` 后，skip/auto 可以缩短非关键 continuation，但必须留下可识别的最终 pose、物件状态、文本或 summary。

### Chapter and Ending Flow

- 章节标题只确认当前单元，不展示完成率、分支比例或本章可获得轴机会。
- 章末摘要只包含已完成的玩家可见事件；不得作为隐藏数值报表。
- 第七日不得显示“最终选择”“修正路线”或类似覆盖前六日因果的 UI。
- 进入 ending label 后先以场景行为确认结果，再显示结局名称和批准的 cause cards；`commit_ending_entry` 只标记 lifecycle，不是 completion。
- Ending cause cards 最多展示 SYS-ENDING 允许的 1 项 matched cause 与至多 2 项固定顺序附加原因；fallback 首项必须是具体失败或未解决锚点。
- Persistent unlock、achievement 或 memory 通知只能在相应叙事结果完成后出现，且不得抢先泄露结局；ending unlock 只允许由 terminal completion node 产生。

### Accessibility and Layout Boundary

- 所有玩家可见内容必须支持键盘焦点、自述功能、字幕、静音与 reduced-motion 等价体验。
- 1280×720 及 SYS-ACCESS catalog 中最大批准字体缩放 ID 下，全部 choice/dialogue/reaction/payoff/cause-card pages 与 continue/next/previous affordances 不得截断、重叠或形成焦点陷阱。
- 因果信息不能只由颜色、声音、动画或人物位置表达；必须存在可读文本或可理解的等价摘要。
- SYS-NARRATIVE 拥有 content identity 和文案；SYS-ACCESS 拥有 screen flow、尺寸、焦点顺序、响应式规则与最终 wireframe。
- Screens 只读取状态并呈现批准内容，不得计算轴、派生 qualification、选择 ending 或修改叙事控制流。

> `ux-designer` and `ui-programmer` review incorporated; final wireframes remain owned by SYS-ACCESS after Q8 content samples freeze.

## Acceptance Oracle Records

验收不得用裸 `manual review=True`、`works correctly`、`可感知`、`可理解` 或 `presentation-safe` 作为通过条件。以下 exact evidence records 由 SYS-TEST 汇总，owner reviewer 只负责填写已冻结 checklist，不能改写 oracle：

- `narrative_content_review_record`：`review_id, review_kind, subject_id, contract_version, source_hash, checklist_result_ids, reviewer_id, unresolved_defect_ids, owner_system`。通过条件为 source hash 匹配、required checklist IDs exact-equal、所有结果为 `pass` 且 `unresolved_defect_ids=()`。
- `validation_diagnostic_record`：`validator_id, subject_id, valid, error_ids, offending_record_ids, catalog_emit_count, source_hash`。Boolean predicate 只返回 bool；需要 exact offending IDs 的 AC 必须读取同版本 diagnostic record，且 `valid=false` 时 `catalog_emit_count=0`。
- `merge_preservation_record`：`merge_node_id, prehistory_ids, history_diff_ids, unresolved_token_diff_ids, resource_diff_ids, pending_payoff_diff_ids, continuation_partition_ids`。每项差异必须被同一 state envelope 保留，或由互斥 continuation partition 覆盖。
- `character_answer_derivation_record`：`derivation_id, transaction_id, input_fact_ids, allowed_answer_state_ids, selected_answer_state_id, observable_action_or_object_ids, priority_rule_id, source_hash, forbidden_hidden_input_count, unresolved_defect_ids`。Selected state 必须由 priority rule 唯一导出，且禁止读取 axis/token/qualification/ending prediction。
- `character_scene_review_record`：`review_id, scene_id, character_id, constraint_id, constraint_version, scene_source_hash, speech_result, known_fact_result, motivation_result, relationship_baseline_result, forbidden_behavior_result, reviewer_id, unresolved_defect_ids`。
- `canonical_witness_replay_record`：`witness_id, entry_node_id, ordered_choice_ids, visited_required_scene_ids, per_step_enabled_results, chapter_axis_snapshots, token_fold_result, route_fact_fold_result, ending_entry_id, resolver_result_id, first_failure_id`。通过条件为从入口逐步 replay，全步 enabled、必经 scenes exact-covered、无 failure 且 ending exact-match。
- `agency_response_coverage_record`：`transaction_id, answer_state_id, source_response_choice_ids, declared_response_choice_ids, missing_ids, extra_ids, per_response_outcome_ids`。source 与 declared exact-equal，missing/extra 为空，每项 outcome tuple 非空。
- `action_gate_matrix_record`：`surface_id, path_kind, phase_id, action_id, visible, enabled, focusable, invocation_count, restored_state_id`。必须覆盖 normal/exception/load-abort × before/during/after reaction × quick-actions/game-menu/save/load/rollback/skip/AFM/history-return/repeated-activation/control-transfer shortcuts；during phase 全部 `false/false/false/0`，after/exception 按当前 phase 纯恢复。
- `accessible_semantic_fact_record`：`subject_kind, subject_id, observable_fact_ids, confirmed_interpretation_ids, epistemic_certainty_id, ambiguity_class_id, permitted_causal_scope_ids, forbidden_inference_ids, source_hash, semantic_review_approval_id`。每个 `U_ACCESS_SUBJECT` 恰有一项；summary claim只能是permitted facts子集且ambiguity class不变。
- `accessible_summary_binding_record`：`subject_kind, subject_id, variant_id, accessible_causal_summary_id, source_hash, localized_text_id, owner_system`。每个独立发现的request、answer/refusal、reaction、payoff、chapter summary、ending cause及重要audio/environment fact按SYS-ACCESS四variant恰绑定一组，共用一个summary identity，反向无 orphan。
- `audio_accessibility_binding_record`：`audio_or_speech_cue_id, subtitle_or_alt_id, answer_state_id, registered_outcome_id, silent_mode_equivalent_id, source_hash`。简单单音节必须有非空 answer/outcome；重要非语音 cue 必须有 subtitle 或可见 equivalent。
- `accessibility_matrix_record`：`scene_or_ending_id, surface_id, mode_set_id, activation_set_id, resolution_id, font_scale_id, page_id, canonical_choice_ids, outcome_ids, summary_ids, reachable_action_ids, spoken_or_visible_semantic_ids, forbidden_motion_event_count, audio_only_dependency_count, clipped_glyph_count`。`mode_set_id` 来自 `silent`、`reduced_motion`、`keyboard_only`、`self_voicing` 的批准组合闭集；必须覆盖全部 surfaces × required mode sets × `1280x720` × maximum approved font scale × cause-card pages。
- `layout_evidence_record`：`surface_id, page_id, resolution_id, font_scale_id, content_rect_ids, reserved_quick_action_rect_id, intersection_count, clipped_glyph_count, focus_order_ids, next_action_id, previous_action_id, continue_action_id`。Baseline resolution 为 `1280x720`；`font_scale_id` 必须来自 SYS-ACCESS 批准闭集并包含最大值。
- `terminal_class_enumeration_record`：`artifact_id, canonical_cfg_hash, terminal_path_count, terminal_class_ids, per_class_witness_ids, per_class_family_ids, per_class_payoff_ids, per_class_summary_ids, per_ending_class_counts, budget_verdict_ids, unresolved_defect_ids`。每条合法 terminal path 恰进入一个 SYS-ENDING exact class；11 个 family 只是 production coverage，不是 class count oracle。
- `integration_gate_record`：`gate_id, artifact_generation, input_contract_hashes, validator_ids, validator_result_ids, artifact_ids, frozen_output_hash, unresolved_defect_ids`。Required validator tuple 固定包含 `manifest_exact_v1, topology_exact_v1, canonical_witness_replay_v1, axis_earliest_miss_recovery_v1, repair_path_replay_v1, agency_source_response_coverage_v1, all_continuation_payoff_coverage_v1, qualification_source_removal_v1, qualification_mutual_exclusion_v1, old_order_autonomy_consistency_v1, terminal_class_enumeration_v1`；每个 validator 在该 artifact generation 中恰有一个 result。CI 可重复验证相同 deterministic artifact，不把测试执行次数写成设计语义。
- `benchmark_protocol_record`：`protocol_id, hardware_id, os_build_id, power_profile_id, build_id, renderer_id, fixture_id, input_scale_id, timer_id, gc_policy_id, process_temperature_id, file_cache_policy_id, warmup_count, run_count, sample_count, aggregation_method_id, reported_percentiles, peak_memory_metric_id, operation_count_kind_ids, threshold_ids`。没有完整 protocol 与已批准 threshold 时只能报告，不能宣称 performance PASS。
- `playtest_protocol_record`：`protocol_id, build_hash, approved_path_class_ids, per_class_minimum_counts, participant_exclusion_rules_id, fixed_question_ids, question_to_metric_map_id, coding_rubric_id, valid_participant_count, per_class_metric_eligible_counts, per_class_metric_success_counts, per_class_failure_sample_ids`。Metric IDs 固定为 `early_choice_cause_recognition, tragedy_loss_comprehension, erii_agency_impact`；每个 required class/metric 独立计算分母，总体结果只作汇总。

## Acceptance Criteria

### Manifest and Dual-Layer Content

| ID | Evidence | Criterion |
|---|---|---|
| `NARR-MANIFEST-001` | `STATIC` | **GIVEN** approved required units、nonempty source roots 及 source-hash-bound production manifest，**WHEN**运行 `chapter_manifest_valid`，**THEN**序章、第一日至第七日、六结局及适用尾声与扫描结果 exact-equal，unresolved 与 production→test-only edge counts 均为 0，结果为 `True`。 |
| `NARR-MANIFEST-002` | `STATIC` | **GIVEN**空 roots、缺失 unit、多余 unit、wrong artifact/source hash/version、悬空引用及 production→test-only edge 单缺陷 fixtures，**WHEN**分别运行 manifest 验证并读取同版本 `validation_diagnostic_record`，**THEN**每案 predicate 返回 `False`、diagnostic `error_ids/offending_record_ids` exact-match fixture oracle、`catalog_emit_count=0`。 |
| `NARR-CONTENT-001` | `STATIC` | **GIVEN** GDD records 与分章 `.rpy` 脚本，**WHEN**比较 stable IDs、控制流、人物决定、events、resources 与 outcomes，**THEN**双方引用双向一致；逐句对白不要求存入 GDD。 |
| `NARR-CONTENT-002` | `STATIC` | **GIVEN**只修改对白、旁白或镜头措辞的 revision，**WHEN**比较 `narrative_content_baseline:v1.2` 冻结的 stable IDs、choice class/projection、CFG edges、character answer/response、events、resources、outcomes、payoff semantic evidence 与 player-safe semantic IDs，**THEN**上述机器字段 deep-equal 且 source-hash-bound content review checklist 全部通过时允许 presentation revision；任一字段变化必须使旧 catalog hash 失效。 |
| `NARR-CONTENT-003` | `STATIC + CONTENT + GRAPH` | **GIVEN**Day 1–7全部合法chapter-completed paths、两个Journal v1 catalogs与7项truth approvals，**WHEN**逐日计算玩家可感知fact intersection并扫描14条copy，**THEN**catalog各7条、`(memory_id,day_index)`一一相等且day恰为1–7；每个copy fact均属于对应`allowed_common_fact_ids`，互斥choice/可变代价/非共通payoff/qualification/axis/token/predicate/traversal-cause命中数为0，approval/path-set/source hashes exact-match，history/save/live-flag read count为0。 |

### Scene Graph and Chapter Structure

| ID | Evidence | Criterion |
|---|---|---|
| `NARR-GRAPH-001` | `STATIC + BRANCH` | **GIVEN**完整 production scene graph 与 `canonical_choice_node_topology_v1`，**WHEN**运行 `scene_graph_valid`，**THEN**所有 entry 与 registered scenes 可达、每个 choice 恰属一个 node、siblings 互斥、opener/guard/replacement exact-match、Day 6 route active count 恰为 1、重大选择子图为有限 DAG，且每条 terminal path 恰到达一个 ending entry。 |
| `NARR-GRAPH-002` | `STATIC + BRANCH` | **GIVEN** cycle、dangling edge、unreachable scene、choice 多归属、missing opener、siblings 串联、ordinary/replacement 同时可达、route active count 0/2、zero-ending、two-of-six endings 及 ending-entry-return 单缺陷 fixtures，**WHEN**分别验证，**THEN**每案结果为 `False` 且不运行 terminal content freeze。 |
| `NARR-GRAPH-003` | `BRANCH` | **GIVEN**任一分支汇合点及其 `merge_preservation_record`，**WHEN**枚举全部到达 prehistories，**THEN**history、unresolved token、route resource 及 pending payoff 的 exact diff IDs 均存在于同一 rollback-owned envelope，或每项 diff 恰由 record 中互斥且穷尽的 continuation partitions 覆盖。 |
| `NARR-GRAPH-004` | `STATIC + BRANCH` | **GIVEN**最大合法 production graph，**WHEN**展开全部路径与 witness，**THEN** terminal paths≤4096、triples≤65536、continuation entries≤1048576 且 artifact bytes≤67108864；任一单项超限均失败且无截断或合并。 |
| `NARR-CHAPTER-001` | `STATIC` | **GIVEN**全部 production chapter records 与 `narrative_content_baseline:v1.2` scene beat catalog，**WHEN**比较 `required_scene_ids, mandatory_responsibility_id, next_chapter_or_ending_ids`，**THEN**每章与内容基线实际冻结字段 exact-equal、required scenes 非空、每个 responsibility ID 全局唯一；choice/event/payoff 完整性分别由 catalog/join/recovery validators 验证，不对 baseline 未声明 tuple 伪造 exact-equal oracle。 |
| `NARR-CHAPTER-002` | `STATIC` | **GIVEN**第七日及六结局 records，**WHEN**扫描新增 axis increment、qualification mutation、万能选择或 ending 自产 source fact，**THEN**匹配数量为 0。 |

### Scene Flow, Choice, Reaction and Payoff

| ID | Evidence | Criterion |
|---|---|---|
| `NARR-FLOW-001` | `STATIC + UT_ENGINE` | **GIVEN**任一含玩家决定的 production scene，**WHEN**从场景建立推进到 continuation，**THEN**流程依次包含观察、适用 request/answer、choice 确认、一次 commit、一次即时 reaction 及严格较晚 payoff。 |
| `NARR-FLOW-002` | `STATIC` | **GIVEN**纯过场或桥接场景，**WHEN**检查其输出，**THEN**它不产生未经 choice record 支持的 axis delta、counterevidence、qualification、route resource 或 ending 变化。 |
| `NARR-FLOW-003` | `UT_ENGINE + INSTR` | **GIVEN**使用 `narrative_choice_reaction:v1` template 的 choice，**WHEN**执行 `ChoiceCommitted → ReactionEstablished → ReactionCompleted`，**THEN**commit 与 reaction establishment 各恰一次；前段 interaction count 为 0；随后唯一 `call narrative_reaction_wrapper(...) from <stable_from_label>` 包含恰一次 `call screen` 与 matching return；bounded interaction count 恰为 1；完整 `action_gate_matrix_record` 在 during phase 对全部禁止 action 为 `false/false/false/0`；语义写入与 other-choice counts 为 0；异常出口按 phase 恢复全部 input gates。 |
| `NARR-PAYOFF-001` | `STATIC + BRANCH` | **GIVEN**全部 `(choice, reachable complete prehistory, legal terminal continuation)` triples，**WHEN**连接 reaction、payoff、semantic evidence 与 canonical SYS-CHOICE CFG artifact，**THEN**每个 choice 恰有一个即时 reaction，且每个 triple 在真实 continuation 上至少执行一个 strictly-later payoff；before/after registered outcome/resource/destination/cost-bearer exact diff 非空并绑定 player-safe summary ID。 |
| `NARR-PAYOFF-002` | `STATIC` | **GIVEN** text-only、camera-only、filter-only、sound-only、ID-only、unchanged-state 及 generic-ending payoff mutants，**WHEN**验证 semantic evidence，**THEN**每案失败且不计入 choice 或 chapter recovery coverage。 |
| `NARR-PAYOFF-003` | `UT_ENGINE + STATIC` | **GIVEN**同一 scene 内多个 payoffs 同时满足，**WHEN**进入 payoff 区段，**THEN**按 `narrative_scene_record.payoff_ids` 冻结 tuple 顺序全部执行、每项最多一次，并在下一 choice 出现前完成。 |

### Agency Transactions

| ID | Evidence | Criterion |
|---|---|---|
| `NARR-AGENCY-001` | `STATIC + UT_PURE` | **GIVEN**完整 request、`character_answer_derivation_record`、answer、canonical source CFG 与 response records，**WHEN**运行 `agency_transaction_valid`，**THEN**derivation 从批准输入唯一导出 selected answer、禁止 hidden inputs、`source_response_choice_ids=declared_response_choice_ids`、全部 choices 恰分类为 accepting 或 overriding、发生在 answer 之后、每项 outcome tuple 非空且引用完整、aggregate outcomes exact-equal 逐 response 有序并集，只有 accepting choices 允许 `autonomy +1`。 |
| `NARR-AGENCY-002` | `STATIC` | **GIVEN** missing request/answer/derivation、derivation 使用 axis/token/qualification/ending input、response-before-answer、source response 漏报/多报、raw response/partition/binding/outcome 重复、双重分类、未分类、empty per-response outcome、aggregate outcome missing/orphan、accepting revoke 当前 answer、override 获得 `autonomy +1` 及悬空 outcome 单缺陷 fixtures，**WHEN**分别验证，**THEN**每案为 `False` 且 transaction 不进入 production catalog。 |
| `NARR-AGENCY-003` | `STATIC + BRANCH` | **GIVEN** `answer_state_id=undetermined`、未登记 answer state 或 ambiguity checklist 未通过的 fixture，**WHEN**连接 source response surfaces、choice projections 与 outcomes，**THEN**`agency_transaction_valid=False`、transaction absent、response surface count=0、scene frozen=false、`unresolved_defect_ids` exact-contains `NARRATIVE_ANSWER_AMBIGUOUS`，且 autonomy delta sum=0。 |
| `NARR-AGENCY-004` | `BRANCH` | **GIVEN**玩家先接受 answer、后续又推翻同一人物决定，**WHEN**回放 ordered history，**THEN**早期 choice 仍存在，后续 choice 产生批准的零增量或 counterevidence，并在适用 payoff 与 ending cause 中保留后果。 |

### Character Continuity

| ID | Evidence | Criterion |
|---|---|---|
| `NARR-CHAR-001` | `STATIC + REVIEW` | **GIVEN**任一 production scene、approved constraint catalog 及 source-hash-matching `character_scene_review_record`，**WHEN**运行 `character_continuity_valid`，**THEN**每个 active character 恰匹配一个 constraint version，五项 review results 全为 `pass` 且 `unresolved_defect_ids=()`。 |
| `NARR-CHAR-002` | `STATIC + REVIEW` | **GIVEN**missing constraint、duplicate constraint、stale version/hash、conflicting sources、unknown `known_fact_id`、motivation violation、forbidden behavior 或 nonempty defect IDs 单缺陷 fixtures，**WHEN**分别验证，**THEN**每案为 `False`，并报告 exact scene/character/constraint IDs；相关 scene 与下游 paths 保持 unfrozen。 |
| `NARR-CHAR-003` | `STATIC + REVIEW` | **GIVEN**全部绘梨衣 content 及对应 review records，**WHEN**扫描 speech units 与书面物件连续片段，**THEN**完整口语 complex-intent count、连续书面解释 count、hidden-rule explanation count 均为 0；每个非语言 complex-intent scene 引用至少一个 approved action/object/context summary ID，且 review defects 为空。 |

### Cross-Chapter Recovery

| ID | Evidence | Criterion |
|---|---|---|
| `NARR-RECOVERY-001` | `STATIC + BRANCH` | **GIVEN**序章至第六日的完整 raw anchor/payoff catalogs，**WHEN**运行 `chapter_recovery_coverage_valid`，**THEN**全部 records 均 well-formed，七个 source chapters 各至少有一个合法 kind 锚点，且每个 declared pair 都在严格较晚章节产生有因果证明的 registered state diff；任一坏 pair 不得被同章另一合法 pair 掩盖。 |
| `NARR-RECOVERY-002` | `STATIC` | **GIVEN**某章无 anchor、anchor 的 `P(a)=()`、duplicate payoff、payoff 多 owner、same-chapter-only anchor、只重复提及、只换台词及无 causal proof 单缺陷 fixtures，**WHEN**分别验证，**THEN**每案为 `False`；空 payoff tuple 不得通过 vacuous truth。 |
| `NARR-RECOVERY-003` | `BRANCH + REVIEW` | **GIVEN** `witness_rain_stops_v1`、`witness_her_own_name_v1` 及对应反事实 sibling paths，**WHEN**推进到 Day 4 与 ending，**THEN**至少一项 ticket/contact resource ID、character-destination outcome ID 或 cost-bearer outcome ID deep-diff，且每项 diff 引用内容基线中的 exact choice/payoff binding 与 player-safe summary ID。 |
| `NARR-AXIS-RECOVERY-001` | `BRANCH + UT_PURE` | **GIVEN**五条命名 earliest-miss full-history witnesses，分别错过 U/A/T/P/S 的最早机会，**WHEN**从 New Game 逐 node replay，**THEN**对应后三项 opportunity 均仍可达、每次增量保持 `+1`、每路径每章每轴增量≤1、相关 token 按 contributor-aware repair 合法解决，最终五轴全 3 且命中 `rain_stops`。 |
| `NARR-AXIS-RECOVERY-002` | `BRANCH` | **GIVEN**同 token 一次、两次及最大合法次数 revoke histories，**WHEN**分别执行完整 contributor acknowledgement、漏一项 acknowledgement 与保留冲突方案的 repair，**THEN**仅第一案移除 token；后两案保持 unresolved，且原 contributor history 与 residual outcomes 不被删除。 |

### Endings and Cross-System Integration

| ID | Evidence | Criterion |
|---|---|---|
| `NARR-ENDING-001` | `BRANCH + UT_PURE` | **GIVEN**六条首周目 canonical histories，**WHEN**从 New Game 入口按 node topology 逐 choice replay，**THEN**每步 enabled、required beats 未绕过、chapter snapshots 与 axis/token/resource/event folds exact-match；到达 ending entry 后再调用 canonical resolver，六条路径各命中预期唯一 ending，并记录完整 matched causes 与全部高优先级 exclusions。 |
| `NARR-ENDING-002` | `BRANCH` | **GIVEN**全部合法 terminal paths，**WHEN**运行 SYS-ENDING exact class-key 枚举，**THEN**每条路径最多命中一项 route qualification并恰属于一个 ending 与一个 exact terminal-cause class；每个 class 有独立 witness、完整 matched/exclusion causes、unresolved-token tuple、outcome signature、适用 payoff、玩家摘要及恰一个 production family；per-ending class count 按 `1–6/7–12/>12` 产生 PASS/REVIEW/FAIL，绝不要求 class count 等于 11。 |
| `NARR-ENDING-003` | `STATIC + BRANCH` | **GIVEN**六个 reachable endings、全部 exact terminal classes 与 `narrative_content_baseline:v1.2` 的 11 个 cause families，**WHEN**检查 content records，**THEN**每个 ending 至少有一个 canonical witness与 core summary，每个 actual class 恰有一个 witness、destination、cost-bearer/tragedy-closure outcome、ending payoff、class summary及 family coverage；所有 references resolve且不同 class identity 不因共享 family/scene/text 被合并。 |
| `NARR-ENDING-004` | `UT_ENGINE` | **GIVEN** resolver 抛出 `TypeError` 或 `ValueError`，**WHEN**第七日 ending flow 执行，**THEN**流程保持 `Active`，不进入 ending label，也不触发 persistent、achievement 或 journal 写入。 |
| `NARR-INTEG-001` | `STATIC + BRANCH + UT_ENGINE` | **GIVEN** SYS-CHOICE 与 SYS-NARRATIVE contract hashes 均冻结且 locked resolver hashes 未改变，**WHEN**生成 `integration_gate_narrative_to_ending_v1` artifact generation 1，**THEN**validator IDs exact-equal `manifest_exact_v1, topology_exact_v1, canonical_witness_replay_v1, axis_earliest_miss_recovery_v1, repair_path_replay_v1, agency_source_response_coverage_v1, all_continuation_payoff_coverage_v1, qualification_source_removal_v1, qualification_mutual_exclusion_v1, old_order_autonomy_consistency_v1, terminal_class_enumeration_v1`，每项恰有一个实际 result/artifact 且 PASS，`unresolved_defect_ids=()`；CI 可重复校验同一 frozen artifact，但不存在完整 SYS-ENDING divergence-suite run ID。 |

### Save, Rollback and Accessibility

| ID | Evidence | Criterion |
|---|---|---|
| `NARR-RESTORE-001` | `UT_ENGINE + INSTR` | **GIVEN** before-choice、after-reaction、before-payoff 及 after-payoff checkpoint records，**WHEN**分别 load 或 rollback 并在恢复后清零 spy，**THEN** stable control location、schema sentinel、expected history/axes、observation horizon 与 commit/reaction/payoff counts 均逐字段 deep-equal SYS-CHOICE/SYS-SAVE 批准记录。 |
| `NARR-RESTORE-002` | `UT_ENGINE` | **GIVEN**unsupported state 或未登记 control location，**WHEN**尝试恢复，**THEN**进入 `screen_blocking_restore_error`；scene-guess count 与 history-write count 为 0；rollback、quick-save、quick-load、skip、history-return、game-menu-return actions 的 visible/enabled/focusable 均为 `false/false/false`，唯一 focusable exits 为 `action_main_menu` 与 `action_new_game`。 |
| `NARR-ACCESS-001` | `UT_ENGINE` | **GIVEN** activation set `mouse_primary, keyboard_enter, keyboard_space` 及 SYS-ACCESS catalog 中批准的替代 activation IDs，**WHEN**确认同一 choice surface，**THEN**全部返回同一 canonical choice ID；self-voicing 按 focus order 恰朗读绑定的 localized text/summary IDs、内部术语暴露 count=0、重复 read count 符合 catalog，且 confirmation count=0。 |
| `NARR-ACCESS-002` | `UT_ENGINE + LAYOUT + STATIC + REVIEW` | **GIVEN**独立发现的完整`U_ACCESS_SUBJECT`、semantic fact/binding catalogs及全部 causal surfaces 与 six ending flows × SYS-ACCESS 批准 mode-set × `1280x720` × maximum font scale × every cause-card page，**WHEN**执行矩阵，**THEN**discovered/catalog subject sets exact-equal；每格 canonical choices/outcomes/summaries、epistemic certainty/ambiguity 与 default exact-equal，文本/自述语义非空、decision-critical summary可重访、silent audio-only dependency=0、reduced-motion forbidden motion=0、actions可达、无焦点陷阱/禁止交叠/裁切；缺格、mind-reading或future spoiler固定失败。 |
| `NARR-UI-001` | `STATIC + REVIEW` | **GIVEN**全部玩家可见 choice、chapter、payoff、journal、cause-card 文案与 Day 6 route labels，**WHEN**扫描内部术语并执行 frozen anti-hidden-score/anti-ending-button checklist，**THEN** axis、token、qualification、predicate、terminal class、阈值/优先级代理、“差一步”攻略提示及结局预告暴露数量均为 0；Day 6 active route label 只描述当下动作。 |
| `NARR-UI-002` | `UT_ENGINE + LAYOUT` | **GIVEN** choice 确认后的即时 reaction及 normal/exception/load-abort paths，**WHEN**推进或恢复到 `after_reaction` checkpoint，**THEN** choice surface absent；`action_gate_matrix_record` 覆盖 quick/game-menu/save/load/rollback/skip/AFM/history-return/repeated activation/control-transfer shortcuts，并证明 bounded interaction 期间全部 invisible/disabled/unfocusable且 invocation count=0；返回或异常退出后 gate 由当前 phase 纯派生并恢复；布局无交叠且下一 choice activation count=0。 |

### Performance and Player Validation

| ID | Evidence | Criterion |
|---|---|---|
| `NARR-PERF-001` | `STATIC + UT_ENGINE + BENCH` | **GIVEN**production build 与完整 runtime observation horizon（process start → main menu → heaviest choice/reaction/payoff/cause-card scenes → one ending → save/load），**WHEN**对 approved route/accessibility matrix 执行 instrumentation，**THEN**全 horizon 的 runtime source-scan、path-enumeration、unexpected external-I/O 与 mutable-index counts 均为 0；只读取 immutable compiled catalogs；60fps/16.6ms、startup≤5s、normal save≤500ms、base memory<1GB 及 imminent-only asset loading 分别产生 threshold result，不得用 no-asset fixture 替代。 |
| `NARR-PERF-002` | `STATIC + BENCH` | **GIVEN**完整 benchmark protocol 与小/中/最大合法 compiler fixtures，**WHEN**按冻结 input scales、cold/warm process/cache、run aggregation、peak-memory metric 及 operation kinds 运行 offline compiler，**THEN**满足四项内容硬预算并输出 reproducible time/memory/operation results；Q10 关闭最终 compiler thresholds，`n/2n/4n` 只用于未超过最大硬上限的明确 input scales。 |
| `NARR-PLAYTEST-001` | `PLAYTEST` | **GIVEN**完整 `playtest_protocol_record`、至少 8 名有效且未接触调试信息的参与者，以及真/好/苦涩/悲剧每类的冻结最低有效样本配额，**WHEN**按 fixed question→metric map 与 coding rubric 编码，**THEN**每个 required class/metric 分别满足 `success_count(class,metric) / eligible_count(class,metric) ≥ 0.75` 并报告 Wilson interval；总体指标只作汇总，不能掩盖任一 class 失败；缺 path class、最低 n、题本、metric map、rubric 或 exclusion record固定失败。 |

> `qa-lead` review incorporated through exact oracle records, split accessibility/layout evidence, bounded reaction interaction counts and reproducible benchmark/playtest protocols.

## Open Questions

以下问题只追踪 implementation、UX、asset、benchmark、playtest 与 exact terminal-class enumeration 证据，不重新打开 SYS-CHOICE、SYS-ENDING 或 `narrative_content_baseline:v1.2` 已冻结的设计决定。

| ID | Open Question | Owner | Due | Closure Evidence |
|---|---|---|---|---|
| `NARR-Q8` | `U_ACCESS_SUBJECT`中每个request、answer/refusal、reaction、payoff、chapter summary、ending cause及重要声音/环境事实的semantic fact、最终简体中文摘要及 `accessible_causal_summary_id` 是什么？ | SYS-NARRATIVE + SYS-ACCESS + UX Designer / Andwey | 内容与 UX lock 前 | Independent discovery、semantic fact与localized summary catalogs；ambiguity/mind-reading/spoiler/anti-hidden-score双人review；可重访transcript、keyboard/self-voicing/silent/reduced-motion evidence；关闭相关 `CHOICE-Q5` 与 `ENDING-Q6` 门槛 |
| `NARR-Q9` | 分章脚本在 before-choice、after-reaction、before-payoff 与 after-payoff 恢复点的 stable control locations、ownership、statement mapping 及 observation horizons 是什么？ | SYS-NARRATIVE + SYS-SAVE + SYS-TEST / Andwey | Save/rollback 集成前 | `choice_restore_checkpoint_record` fixtures；stable `control_location_id` catalog（禁止文件行号 identity）；rollback-owned storage；`after_load` validation；四类 checkpoint engine tests；unsupported-location safe flow |
| `NARR-Q10` | 在冻结的四项内容硬上限内，offline compiler 在固定参考硬件上的耗时、峰值内存及 operation-count 门槛是什么？ | SYS-TEST / Andwey | 最终跨系统集成 gate 前 | 完整 benchmark protocol；small/medium/maximum fixtures；合法 input scales；cold/warm process/cache；maximum/p95 结果；关闭 `CHOICE-Q10` 与 `ENDING-Q7`，不得修改内容硬上限 |
| `NARR-Q11` | 每个 chapter anchor、reaction 与 payoff 需要哪些 stable visual/audio asset identities、cue/subtitle/alt IDs、动作、构图与声音动机？ | Art Bible + SYS-NARRATIVE / Andwey | Production asset 制作前 | Approved Art Bible；逐 content ID asset inventory；audio accessibility bindings；source registrations；`/asset-spec system:seven-day-chapter-script` 输出。关闭前仅叙事语义需求已冻结，不宣称 asset identity 已冻结 |
| `NARR-Q12` | 无调试信息的玩家能否识别早期 choice 与后果、理解悲剧损失并感到绘梨衣的自主决定真实影响后续？ | SYS-NARRATIVE + SYS-ACCESS + Playtest / Andwey | Closed vertical slice 内容锁定前 | 至少 8 名参与者；`early_choice_cause_recognition, tragedy_loss_comprehension, erii_agency_impact` 各≥75%；四类路径最低配额、固定 question→metric map、rubric、原始编码与失败样本 |
| `NARR-Q13` | 全部合法 terminal paths 按 SYS-ENDING exact class-key 实际形成多少 equivalence classes；每 class 的 witness、family coverage、payoff 与 summary 是什么？ | SYS-NARRATIVE + SYS-CHOICE + SYS-ENDING + SYS-TEST / Andwey | Production content lock 前 | `terminal_class_enumeration_record`；全路径 count；逐 class exact identity/witness/payoff/summary；11 cause-family coverage；per-ending `1–6/7–12/>12` verdict；不得把 family count 当 class count |

## Closed Design Decisions

| ID | Closed On | Decision | Evidence |
|---|---|---|---|
| `NARR-Q1` | 2026-07-29 | 冻结 15 个 canonical production units、required scene beats、responsibility IDs 与真结局必需可玩尾声；source hash 属实现证据。 | `narrative_content_baseline:v1.2` — Canonical Production Units / Chapter and Scene Beat Catalog |
| `NARR-Q2` | 2026-07-29 | 当前 active-character 闭集为路明非与绘梨衣；两项 constraints、authority references 与 approval IDs 冻结；新增人物触发全量 scene review。 | `narrative_content_baseline:v1.2` — Character Constraint Catalog |
| `NARR-Q3` | 2026-07-29 | 冻结 54 项 production choices、唯一 reaction identities、逐 continuation payoff 最低语义、五轴各四项独立 recovery opportunities 与五条完整 earliest-miss witnesses。 | `narrative_content_baseline:v1.2` — Choice, Reaction and Payoff Catalog / Recovery Matrix |
| `NARR-Q4` | 2026-07-29 | 冻结 9 项 request/answer/response transactions、answer derivation、canonical-CFG response universe、raw uniqueness、accepting/overriding partitions 与逐 response outcomes。 | `narrative_content_baseline:v1.2` — Agency Transaction Catalog |
| `NARR-Q5` | 2026-07-29 | 冻结四项 route qualifications 的 exact正向 choice/event/resource sources；solo contact absence 只作为 choice entry guard，并由正向 no-contact event 固结；Day 6 guards 恰启用一项 commitment/fallback。 | `narrative_content_baseline:v1.2` — Route Qualification Bindings / Choice Node Topology |
| `NARR-Q6` | 2026-07-29 | 冻结 7 项 repairable tokens、targeted repairs、完整 contributor acknowledgement、costs、residual outcomes 与 consequences；irreversible token count 为 0。 | `narrative_content_baseline:v1.2` — Counterevidence Catalog |
| `NARR-Q7` | 2026-07-29 | 冻结六条从 New Game 可重放的完整 canonical ending histories、11 个 cause-family production variants、人物归宿、代价承担与核心 ending summaries；actual class identity 转由 Q13 枚举。 | `narrative_content_baseline:v1.2` — Canonical Ending Witnesses / Terminal Cause-Family Forecast |

这些决定把 `CHOICE-Q1/Q3` 与 `ENDING-Q1/Q3` 从“内容未定义”推进为“exact design binding 已提供、validator evidence pending”。只有 reference-integrity、source-removal、repair path、qualification mutual-exclusivity 与全图 witness reports 全部 PASS 后，上游文档才能正式把相应 provisional downstream gates 标记为 closed；本 GDD 不越权伪造该状态。

### Closure Policy

- `NARR-Q1–Q7` 已关闭设计决定，但不等同 production implementation PASS；source hash、完整 records、negative fixtures、全图 enumeration、join reports 与 engine traces 仍必须按 Acceptance Criteria 生成。
- `NARR-Q8–Q12` 分别阻止 UX/content lock、save 集成、最终 benchmark、资产制作或 Player Fantasy 体验封板；`NARR-Q13` 阻止 production content lock 与最终跨系统 integration artifact。它们不阻止本 GDD 进入独立 re-review，也不倒灌为新的 SYS-CHOICE/ENDING schema 问题。
- Q8–Q13 与全部 implementation evidence 关闭后生成一次 artifact generation 1 的既定跨系统集成产物；CI 可重复验证同一产物。除非 locked resolver invariant 实际变化，否则不重新运行完整 SYS-ENDING 审查。
