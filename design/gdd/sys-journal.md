# 愿望手册 UI

> **System ID**: SYS-JOURNAL
> **Status**: Approved with provisional downstream gates
> **Author**: Andwey + Codex
> **Last Updated**: 2026-08-04
> **Implements Pillar**: 看见未说出口的话；悲剧也是完整答案；用普通生活抵抗宏大命运
> **Review Mode**: Full
> **Design Review**: 2026-08-04 — NEEDS REVISION；static-day truthfulness、bundle ownership、formula error domains、bounded presentation evidence、reentrant handling、all-category fault routing 与 SYS-SAVE reverse contract revised；independent re-review required before implementation-ready

## Overview

SYS-JOURNAL 是《雨停之后》的 P0 玩家表现系统：它以“愿望手册”的形式，把玩家已经合法完成的章节回忆、成就与结局整理为可主动进入、返回和浏览的旅途记录。系统只消费 SYS-PERSIST 提供的 detached collection snapshot，以及 SYS-NARRATIVE、SYS-ACHIEVE、SYS-ENDING 批准的玩家安全文案；遵循 ADR-0003 的内容与表现边界，界面只读取并呈现结果，不重新判定叙事事件、成就条件或结局原因。未解锁内容不占据可见位置，也不通过数量、空槽或提示泄露未来路径，使每段被记录的经历——包括苦涩与悲剧——都成为完整而非带评分意味的答案。

## Player Fantasy

玩家主动翻开愿望手册时，应感到这不是一份等待清空的任务列表，而是游戏在认真保存自己与绘梨衣共同经历过的片段：一件被留住的物件、一段已经走完的章节、一次被兑现的承诺，或一个无法挽回但依然完整的结局。章节与回忆只确认“这一天与这个片段确实被留下”，不冒充逐选项的个人行程复述；旅途记录中新出现的成就则带来“这个具体回声被温柔而准确地发现了”的确认。再次浏览时，手册应像一本随旅途自然变厚的私人记录，而不是攻略完成率。

这一体验直接服务于“看见未说出口的话”与“悲剧也是完整答案”：记录强调人物、物件、行动和后果，不评价玩家是否选择正确，也不把好结局置于悲剧之上。玩家可以从已经经历的内容中重新理解因果与绘梨衣的自主决定，但无法借愿望手册窥探隐藏数值、未发现路线或未来条件。

*2026-08-04 re-review revision 已收窄静态 Day 摘要的真实性承诺：Journal 不保存或推导逐 traversal 选择，不把共通摘要伪装为“玩家本次具体做了什么”。*

## Detailed Design

### Core Rules

1. **唯一数据权威**：进入愿望手册时，系统从 SYS-PERSIST 获取并完整验证一份 detached collection snapshot。页面不得直接读取或修改 `persistent.sys_persist_state`，也不得从存档、achievement backend、当前五轴或叙事控制位置补全数据。

2. **双入口**：玩家可从主菜单或正常游戏菜单进入愿望手册。若当前处于 achievement modal、阻断式恢复流程或其他禁止游戏菜单的交互阶段，则不得绕过上游输入 gate 打开愿望手册。

3. **四区目录**：愿望手册首页固定提供“章节”“回忆”“旅途记录”“结局”四个等权入口：

   - **章节**：按 Day 1→Day 7 顺序列出已完成章节的标题与玩家安全摘要。
   - **回忆**：使用同一组已解锁 `memory_ids`，呈现对应章节中批准的物件、行动或情感片段；不是全文回放或历史记录。
   - **旅途记录**：展示已解锁的 11 项成就，按“场景回声→路线发现→后来留下的回声”的批准组序排列；最后一组不得被称为真结局、终极或完成组。
   - **结局**：展示已合法完成的结局标题、批准摘要及 SYS-ENDING 专供 Journal 的 `journal_cause_ids` 对应原因摘要。

4. **章节与回忆共享 membership，但内容职责不同**：首发不建立独立 `chapter_ids`。一个 `MEMORY_DAY_N` 解锁后，对应章节摘要和回忆详情同时可用，但它们是不同内容视图，不形成两次解锁或两个进度项。章节视图只回答“这一天有哪些对全部合法 completed paths 都成立的共同事件、地点与已实现结果”，按时间线提供宏观概览；不得声称玩家选择了某一互斥行动、承担了某一可变代价或触发了某一非共通后果。回忆视图只回答“哪个同样对全部合法 completed paths 成立的物件、动作或情感近景值得被重新看见”，不得复述整日时间线、结局资格或章节概览。首页副标题必须明确二者是“同一天的共同经过”与“其中一个被留下的片段”。首发目录明确只覆盖 Day 1–7：序章是旅途框架，真结局尾声归入对应结局详情，不建立隐藏的序章/尾声槽位。若冻结盲测不能证明玩家理解这一区分，制作门槛固定为合并成单一章节记录区，而不是以更多说明掩盖重复。任何未来 path-specific 日记必须先由 SYS-NARRATIVE 定义 player-safe projection、由新的 persistence/architecture amendment 明确保存边界；Journal 不得读取 choice history 自行补全。

5. **未解锁内容完全缺席**：未解锁章节、回忆、成就和结局均不渲染、不占槽、不进入计数、焦点顺序或自发声输出。页面不得显示总分母、百分比、空白剪影、问号标题或“还差几项”。只有旅途记录分区使用上游批准的“曾经走过 X 项”；章节、回忆与结局默认不显示可见数量。

6. **只呈现批准文案，并按故障域 fail-closed**：

   - 章节和回忆只读取 SYS-NARRATIVE 的玩家安全摘要。
   - 成就只读取 SYS-ACHIEVE 的批准名称、描述、组别和展示顺序，不读取条件。
   - 结局只读取 SYS-ENDING 批准的标题、摘要与 Journal 专用原因卡文案。SYS-PERSIST 首发只保存 `ending_ids`，不保存逐 traversal resolution/cause，因此 `journal_cause_ids` 是 `journal_ending_catalog:v1` 中按 ending ID 冻结的 1–3 个静态安全摘要：每项必须由 build validator 证明对该 ending 的全部 terminal equivalence classes 都成立，只能描述共同发生的结果、代价或未解决伤害，不得伪装成玩家本次 path-specific 原因，也不得包含 higher-priority exclusion、阈值或“另一条更高路线为何没有发生”；原因顺序与数量不得改变。
   - 顶层 `journal_catalog_bundle:v1` 的 schema、generation matrix 或 source-hash manifest 无法验证时，普通 Journal 整体进入非破坏性的 `ContentHandoff`；不得导向收藏 reset。
   - 顶层 bundle 已验证而单一分区在加载或引用解析时失败时，仅该分区进入 `CategoryUnavailable`，其他完整验证的分区继续可用；损坏分区不显示部分列表、项目数或未来内容提示。

7. **价值中立排序**：章节与回忆按日序排列；成就按批准 catalog rank 排列；结局按 SYS-ENDING 提供、经创意审查的 `journal_display_rank` 排列。`journal_display_rank` 只用于稳定策展，不得等同 resolver priority、结局优劣或获得顺序。界面绝不显示内部 ID/rank，也不通过尺寸、颜色、音效或位置暗示结局等级。

8. **“新记录”只表示已呈现发现状态**：只有 `achievement_ids − seen_achievement_ids` 显示低强调度的“新记录”。`seen` 不表示玩家已经阅读、理解或完成条目，只表示该 ID 已在真实、非 prediction 的 Journal achievement list 版本中成功呈现且可被键盘与 self-voicing 发现。Screen 构造、prediction、`on show`、不可交互帧、未建立 viewport/focus graph 的帧均不得生成呈现凭据。Journal 是玩家从手册触发 mark-seen 的唯一 semantic caller，并通过 SYS-PERSIST 的 `achievement-mark-seen` 专用 adapter 提交；SYS-ACHIEVE 只拥有自动成就 modal 关闭后的 mark-seen caller。

9. **有界呈现证据与标签稳定性**：一次 `journal open cycle` 从 Journal 成功打开起，到关闭、`ContentHandoff` 或 persistence recovery 接管止。真实可交互的 achievement list 版本只能由 `renpy_interaction_probe:v1` 生成一份绑定 mounted version、visible IDs、viewport、focus graph 与 self-voicing tree hash 的 immutable evidence；controller 立即把该 evidence 折叠进一个仅含 `collection_epoch_id` 与 `0–11` 个 unique achievement IDs 的 `journal_seen_accumulator`，随后丢弃原始 evidence，不保存 raw-evidence sequence 或 version-key ledger。重复 version、restart、滚动与详情往返只做幂等集合并集，不增加状态大小。玩家离开旅途记录分区或关闭 Journal 时才把 accumulator 与最新权威 unseen 相交并提交一次 acknowledgement。mark-seen 成功后，当前 cycle 的“新记录”标签仍保留；下一次打开才显示“曾经走过”。安全落盘失败或 reentrant rejection 时清空本次 accumulator、保留“新记录”并执行原 intent；下一次真实呈现可重新累计。commit 状态未知时立即移交阻断式恢复流程。

10. **目录导航可预测**：每次打开先进入首页目录。每个分区的滚动位置只在当前 `process session` 中保留；返回首页再进入时可恢复，退出进程后不持久化。关闭愿望手册后，焦点返回调用入口对应的 stable semantic focus ID；目标不存在时使用调用界面批准的安全 fallback。

11. **稳定焦点、主线程控制器与原子刷新**：外部 persistent merge 或合法 membership 更新只由 callback 记录已验证 generation/fingerprint，不得在 callback 或 screen 求值中调用 UI。Non-save/non-rollback 的 process-session Journal controller 在下一合法 interaction boundary 合并通知、完整验证并构建新的 detached read model，再一次替换当前列表并恰请求一次必要的 interaction restart；deep-equal payload 不重建、不 restart。若原焦点 ID 仍存在则保留；否则回退到分区返回操作。不得出现半更新列表或 stale displayable。Controller 在进程退出、full restart、reset/epoch change 与 recovery 接管时清空，且不得进入 save、rollback、persistent 或 imported mutable cache。

12. **分离 persistence 与内容不可用状态**：invalid persistent root、persistence unavailable、commit-unknown、reset recovery 原子移交 SYS-PERSIST 的统一阻断恢复界面；catalog bundle/schema/generation/hash 缺陷进入非破坏性的 `ContentHandoff`，只允许返回安全菜单、重试重新载入已安装内容或退出，不显示 reset 收藏；已验证 bundle 内的单分区加载/引用故障进入 `CategoryUnavailable`。三类状态均不得伪装成“0 项”，也不得暴露内部技术字段。

13. **首发不提供管理操作**：愿望手册不提供搜索、筛选、自定义排序、手动领取、撤销、单项删除、收藏重置、章节重播或完整对话回放。收藏重置只存在于 SYS-PERSIST 批准的独立流程。

### States and Transitions

| 状态 | 进入条件 | 允许行为 | 离开条件 |
|---|---|---|---|
| `Closed` | 愿望手册未打开 | 从合规入口请求打开 | 合法请求 → `Validating` |
| `Validating` | 获取 detached snapshot 与已编译 bundle | 无内容交互；不得显示旧模型 | root 不可信 → `PersistenceRecoveryHandoff`；bundle 不可信 → `ContentHandoff`；顶层有效且至少可建立首页 → `Contents` |
| `Contents` | 首页及四区 availability 已原子生成 | 进入可用分区、进入不可用说明、关闭 | 可用分区 → `CategoryList`；不可用分区 → `CategoryUnavailable`；关闭 → `Closing`；合法更新 → `Refreshing` |
| `CategoryList` | 某分区列表已原子生成 | 滚动、选择已解锁条目、返回或关闭 | 选条目 → `Detail`；返回/关闭且 accumulator 为空 → `Contents/Closing`；achievement 返回/关闭且 accumulator 非空 → `SeenAckPending`；合法更新 → `Refreshing` |
| `Detail` | 已解锁条目的批准详情可用 | 阅读、滚动、返回或关闭 | 返回 → 原 `CategoryList`；关闭且 accumulator 为空 → `Closing`；achievement 关闭且 accumulator 非空 → `SeenAckPending`；合法更新 → `Refreshing` |
| `SeenAckPending` | 玩家已请求离开 achievement 分区/关闭，且 `journal_seen_accumulator.ids` 非空 | 已渲染 blocking-safe pending frame；所有输入 gated；只保留触发本状态的 `pending_user_intent`，后台更新只设置独立 `refresh_required` bool | `APPLIED_FLUSHED/DUPLICATE_NOOP/PERSIST_FLUSH_FAILED_SAFE` → 清 accumulator，若需先 `Refreshing`，再重验证并执行原 intent；`PERSISTENCE_UNAVAILABLE/COMMIT_STATUS_UNKNOWN` → `PersistenceRecoveryHandoff`；`REJECTED_INVALID` → `ContentHandoff`；`REJECTED_REENTRANT` → 清 accumulator、保持 unseen、不等待未定义事件、不自动重提并立即执行原 intent；任何随后到达的全局 recovery 仍可从任意普通状态抢占 |
| `Refreshing` | 主线程 controller 在合法 interaction boundary 消费一个或多个 coalesced update | 输入 gated；验证并构造完整新模型，不呈现中间值 | persistence 故障 → `PersistenceRecoveryHandoff`；bundle 故障 → `ContentHandoff`；分区故障 → `CategoryUnavailable/Contents`；完整替换 → 原语义页面或批准 fallback；若存在已验证 pending intent 再执行该 intent |
| `CategoryUnavailable` | 顶层 bundle 有效，但所选分区加载或引用解析失败 | `category_retry`、`section_back`、`journal_close`；初始焦点为 `category_retry` | retry 成功 → 对应 `CategoryList`；retry 仍为单区故障 → 本状态；返回 → `Contents`；关闭 → `Closing`；顶层 bundle 失效 → `ContentHandoff` |
| `ContentHandoff` | bundle schema/generation/hash 无法验证，或 acknowledgement 请求本身违反冻结合同 | 只允许重新载入已安装内容、返回安全菜单或退出；不得显示/建议收藏 reset | 重新载入且验证成功 → `Validating`；否则安全菜单/退出 → `Closed` |
| `PersistenceRecoveryHandoff` | invalid root、persistence unavailable、commit-unknown 或 reset recovery | 只执行 SYS-PERSIST 恢复界面批准的安全操作 | 恢复流程决定返回主菜单、退出或重新初始化 |
| `Closing` | 玩家关闭或调用界面要求退出 | 恢复稳定焦点或安全 fallback | 完成 → `Closed` |

任何状态都不得转入叙事判定、成就求值或结局 resolver。`CategoryList` 与 `Detail` 只能由已验证 read model 建立。顶层 bundle 有效时，即使四个 category 全部 unavailable，仍进入 `Contents` 并保留四个等权、可聚焦入口；每个入口进入自己的 `CategoryUnavailable`，不得升级成 `ContentHandoff`。Journal 打开期间拥有 collection-browser input gate：非阻断 achievement modal 与 quick/game-menu 请求延后到 `Closed` 后；blocking persistence recovery 立即抢占并清除 accumulator、scroll、focus 与 queued intent。事件优先级固定为 `PersistenceRecoveryHandoff → ContentHandoff → epoch/reset invalidation → acknowledgement 已知终态 → coalesced refresh → 已冻结 pending_user_intent → 普通导航`。

### Interactions with Other Systems

| 系统 | 输入到 SYS-JOURNAL | SYS-JOURNAL 输出 | 所有权边界 |
|---|---|---|---|
| SYS-PERSIST | detached snapshot、generation、availability、merge/reset/recovery 状态 | Journal caller 的 exact achievement mark-seen 请求与 bounded presentation evidence | SYS-PERSIST 独占 root、验证、写入、flush 与恢复；Journal 不自由填写 requester |
| SYS-NARRATIVE | `journal_chapter_catalog:v1` 与 `journal_memory_catalog:v1`：Day 1–7 标题、全路径共通章节摘要和回忆详情 | 无叙事写入 | SYS-NARRATIVE 独占 source copy 与 all-completed-path truth review；Journal 不读取 live chapter flag/history，也不解锁内容 |
| SYS-ACHIEVE | 11 项展示目录、组序、名称、描述及 membership/seen 语义 | Journal 产生的 bounded presentation accumulator 与 mark-seen evidence | Journal 不运行条件 evaluator、不访问 backend；自动 modal 与 Journal 各自调用专用 adapter，不互相代理 |
| SYS-ENDING | 已解锁 ending membership、批准标题/摘要、`journal_display_rank` 及 `journal_cause_ids` 文案 | 无 resolver 输入 | Journal 不重排原因、不显示 higher-priority exclusion、阈值或未到达条件 |
| SYS-ACCESS | 字体倍率、高对比度、reduced-motion、自发声及键盘合同 | screen/row/detail 的语义结构需求 | 最终焦点几何、朗读 transcript 与响应式布局仍为 provisional gate |
| SYS-AUDIO | 批准的页面与通知声音策略 | 可选的语义 UI 音频事件 | 声音不得成为唯一反馈；self-voicing 时遵守 suppress 规则 |
| SYS-SAVE | `journal_menu_gate:v1`、`journal_caller_focus_catalog:v1` 与 blocking-load exclusion | 无存档数据；只返回调用界面批准的 focus result | Journal 不从 save slot 构建收藏，也不改变 rollback 状态；unsupported/corrupt/loaded-unvalidated flow 中入口调用数为 0 |
| SYS-BUILD | 执行 Journal bundle assembler、计算 source hashes、验证 archive closure并排除 test-only evidence forger | `journal_catalog_bundle:v1` release artifact；保留production `renpy_interaction_probe:v1` | SYS-JOURNAL 拥有 bundle schema/assembler contract；各 source system 拥有内容，SYS-BUILD 不改写文案或 ID |
| ADR-0003 / UI 层 | screen 只读、稳定资源名、键盘与 720p 约束 | 玩家表现需求 | 具体 screen 结构与实现方式留给 ADR 和 `/ux-design` |
| SYS-TEST | snapshot、catalog、focus、merge、recovery 与布局 fixtures | 可验证状态和语义 ID | 测试接口不得进入发行 read model |

*2026-08-03 full design-review 已完成跨职能正式评审；最终 Art Bible、UX spec、SYS-ACCESS 合同与 Ren’Py engine spike 仍须在进入制作前关闭。*

## Formulas

所有公式只派生显示模型，不成为解锁或叙事权威。

### Journal Read-Model Validity

首发冻结 `journal_catalog_bundle:v1`。它是 exact immutable built-in record，字段恰为：

```text
bundle_schema_id = "journal_catalog_bundle:v1"
persist_catalog_generation_id = "persist_catalog:v2"
chapter_catalog_generation_id = "journal_chapter_catalog:v1"
memory_catalog_generation_id = "journal_memory_catalog:v1"
achievement_catalog_generation_id = "achievement_catalog:v2"
ending_catalog_generation_id = "journal_ending_catalog:v1"
source_hashes = exact mapping(category -> lowercase full SHA-256)
cross_reference_manifest = exact immutable ID/reference table
```

Chapter record 字段恰为 `(memory_id, day_index, list_title_id, list_summary_id, detail_title_id, detail_body_id, common_path_truth_approval_id)`；memory record 为 `(memory_id, day_index, object_title_id, list_summary_id, detail_title_id, detail_body_id, common_path_truth_approval_id)`；首发两者都是纯文字记录，不引用 per-memory image，因此不声明孤立的 `alt_text_id`。`day_index` 恰为 `1–7` 且七项唯一，chapter/memory 的 `(memory_id,day_index)` 必须一一相等。`common_path_truth_approval_id` 必须解析到 SYS-NARRATIVE 的逐日 all-completed-path review，不允许逐 traversal 可变事实。Achievement display record 为 `(achievement_id, group_rank, item_rank, name_id, description_id)`，`(group_rank,item_rank)` 全局唯一；ending record 为 `(ending_id, journal_display_rank, title_id, summary_id, journal_cause_ids)`，`journal_display_rank` 六项唯一，每个 `journal_cause_ids` 是长度 `1–3` 的 exact unique tuple。每个 Journal cause record 为 `(cause_id, summary_id, cause_scope)`，且 `cause_scope` 只允许 `CURRENT_ENDING_FACT` 或 `CURRENT_ENDING_UNRESOLVED_CONSEQUENCE`。

Ownership 冻结如下：SYS-NARRATIVE 独占 chapter/memory source records 与 truth approvals；SYS-ACHIEVE 独占 achievement display source；SYS-ENDING 独占 ending source；SYS-JOURNAL 独占 `journal_catalog_bundle:v1` schema、deterministic assembler 与 error taxonomy；SYS-BUILD 只执行 assembler、计算 source hashes、验证 archive closure并打包 release artifact。任一 source owner 改 generation 或 schema 时必须使旧 bundle validation 失败，不允许 SYS-BUILD 或 Journal 重写内容来维持旧 hash。

`journal_ending_catalog:v1` 的中立策展 rank 冻结为：`one_person_train=10`、`her_own_name=20`、`rain_stops=30`、`unsent_postcard=40`、`see_the_sea=50`、`golden_cage=60`。该“移动→名字→天气→书信→远方→空间”母题序列刻意不等于 resolver priority、stable-ID UTF-8 或结局类型分组；只渲染已解锁条目，因此不显示空位或完整序列。

Source hash 在构建/导入 archive 时验证一次；打开、refresh、滚动、self-voicing 与 screen prediction 只比较已验证的 immutable bundle identity，不读取 filesystem，也不重新计算全文 hash。

The `journal_model_result` formula is defined as:

```text
bundle_valid(R, B) =
    exact_bundle_schema(B, "journal_catalog_bundle:v1")
    ∧ R.catalog_generation_id = B.persist_catalog_generation_id
    ∧ exact_generation_matrix(B)
    ∧ exact_sha256_manifest(B.source_hashes)
    ∧ manifest_ids(B, chapter) = approved_memory_ids
    ∧ manifest_ids(B, memory) = approved_memory_ids
    ∧ manifest_ids(B, achievement) = approved_achievement_ids_v2
    ∧ manifest_ids(B, ending) = canonical_ending_ids

category_valid(B, C, k) =
    exact_category_schema(C.k)
    ∧ ids(C.k) = manifest_ids(B, k)
    ∧ source_identity(C.k) = B.source_hashes[k]
    ∧ all_references_resolve_once(C.k, B.cross_reference_manifest)
    ∧ (k not in {chapter,memory} or exact_day_catalog(C.k,1..7))
    ∧ (k != achievement or exact_unique_display_ranks(C.achievement))
    ∧ (k != ending or (
          exact_unique_display_ranks(C.ending)
          ∧ every(1 <= len(record.journal_cause_ids) <= 3
                  for record in C.ending)
          ∧ every(record.journal_cause_ids is an exact unique tuple
                  for record in C.ending)
          ∧ every(cause_scope(id) in
                  {CURRENT_ENDING_FACT,
                   CURRENT_ENDING_UNRESOLVED_CONSEQUENCE}
                  for record in C.ending
                  for id in record.journal_cause_ids)))

chapter_memory_pair_valid(C) =
    tuple((record.memory_id,record.day_index) for record in C.chapter)
    = tuple((record.memory_id,record.day_index) for record in C.memory)

journal_model_result(R, B, C) =
    CONTRACT_ERROR(INPUT_EXACT_TYPE)
        when input containers or scalar exact types are invalid
    CONTRACT_ERROR(PERSIST_SNAPSHOT_INVALID)
        when R.status = READY and not persist_snapshot_valid(R)
    PERSISTENCE_UNAVAILABLE
        when R.status != READY
    CONTENT_BUNDLE_UNAVAILABLE
        when not bundle_valid(R, B)
    READY(tuple(
        READY(k) if (category_valid(B,C,k)
                     and (k not in {chapter,memory}
                          or chapter_memory_pair_valid(C)))
        else CATEGORY_UNAVAILABLE(k)
        for k in (chapter,memory,achievement,ending)
    ))
        otherwise
```

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Detached snapshot | `R` | exact immutable snapshot | 1 | SYS-PERSIST 验证后的候选输入 |
| Bundle manifest | `B` | exact immutable record | 1 | generation、hash 与 cross-reference 权威 |
| Content catalogs | `C` | exact immutable catalog tuple | 4 个分区目录 | 章节、回忆、成就与结局的批准文案 |
| Category | `k` | exact enum | 4 项 | `chapter/memory/achievement/ending` |
| Snapshot validity | `persist_snapshot_valid` | upstream exact bool | `true/false` | READY snapshot 的 exact schema/canonical/closed-set validation；失败是 contract error，非运行时 unavailable |
| Reference count | `resolve_count` | exact int | `0–N` | 每个目录引用的解析次数 |

**Output Range:** `CONTRACT_ERROR(INPUT_EXACT_TYPE/PERSIST_SNAPSHOT_INVALID)`、`PERSISTENCE_UNAVAILABLE`、`CONTENT_BUNDLE_UNAVAILABLE`，或含四个 exact category status 的 `READY(...)`。任何 error/unavailable 状态都没有“0 项”或部分损坏列表输出。前两类 snapshot contract error 与 unavailable 都移交 `PersistenceRecoveryHandoff`，但测试和诊断不得把二者合成同一公式返回值。

**Example:** bundle 的 achievement generation 不是 `achievement_catalog:v2` 时输出 `CONTENT_BUNDLE_UNAVAILABLE`；bundle 已验证但 achievement category 在 archive load 后发生单一引用解析失败时，只输出 `CATEGORY_UNAVAILABLE(achievement)`，其他通过验证的分区保持 READY。

### Visible Ordered IDs

The `visible_ordered_ids` formula is defined as:

```text
membership(R, category) =
    R.memory_ids       when category ∈ {chapter, memory}
    R.achievement_ids  when category = achievement
    R.ending_ids       when category = ending

visible_ordered_ids(R, B, C, category) =
    CONTRACT_ERROR(INVALID_CATEGORY)
        when category not in {chapter,memory,achievement,ending}
    CONTRACT_ERROR(MODEL_INPUT_INVALID)
        when journal_model_result(R,B,C) is CONTRACT_ERROR
    NO_MODEL when journal_model_result(R,B,C) does not contain READY(category)
    otherwise
    DisplayOrder_category(
        membership(R, category)
    )
```

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Category | `k` | enum | 4 项 | `chapter/memory/achievement/ending` |
| Membership | `M_k` | exact tuple of IDs | `0–7/7/11/6` | 对应分区的合法已解锁集合 |
| Catalog IDs | `I_k` | exact tuple of IDs | `7/7/11/6` | 分区批准目录 |
| Display order | `D_k` | deterministic ordering function | 1 项/分区 | 日序、achievement catalog rank 或 ending `journal_display_rank` |

**Output Range:** `CONTRACT_ERROR(INVALID_CATEGORY/MODEL_INPUT_INVALID)`、`NO_MODEL`，或 chapter `0–7`、memory `0–7`、achievement `0–11`、ending `0–6` 个 exact unique ID。Unknown/duplicate membership 由 `journal_model_result` 精确归类为 `MODEL_INPUT_INVALID`，公式不得通过过滤静默丢弃非法输入。

**Example:** `R.memory_ids=(MEMORY_DAY_2,MEMORY_DAY_5)` 时，章节和回忆分区均输出 `(MEMORY_DAY_2,MEMORY_DAY_5)`，但分别解析到章节摘要与回忆详情。

### Journal Session New IDs

The `journal_session_new_ids` formula is defined as:

```text
upstream_unseen(R) =
    DisplayOrder_achievement(
        tuple(id for id in R.achievement_ids
              if id not in R.seen_achievement_ids)
    )

N_0 = upstream_unseen(R_open)

N_(t+1) =
    DisplayOrder_achievement(
        (N_t ∪ upstream_unseen(R_refresh))
        ∩ visible_ordered_ids(R_refresh, B, C, achievement)
    )
```

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Opening new IDs | `N_0` | exact tuple | `0–11` | `journal open cycle` 开始时的 unseen 成就 |
| Session new IDs | `N_t` | cycle-only exact tuple | `0–11` | 本次 `journal open cycle` 保持“新记录”的项目 |
| Refreshed snapshot | `R_refresh` | valid detached snapshot | 1 | 原子 refresh 后的新权威读取结果 |
| Visible achievement IDs | `V_a` | exact tuple | `0–11` | 当前合法可见成就 |

**Output Range:** `0–11` 个按 achievement display rank 排序的 ID；关闭愿望手册时清空。mark-seen 成功不会在本次 `journal open cycle` 删除这些 ID。

**Example:** 打开时 `N_0=(A)`；A 的 mark-seen 已落盘后页面仍显示 A 为“新记录”。随后 external update 加入 unseen B，则结果为批准顺序下的 `(A,B)`；下次重新打开时 A 不再进入集合。

### Journal Seen-Acknowledgement IDs

The bounded presentation evidence and `journal_seen_ack_ids` formulas are defined as:

```text
list_version_key(R,B,V) = (
    R.collection_epoch_id,
    R.snapshot_fingerprint,
    B.bundle_schema_id,
    B.source_hashes[achievement],
    V
)

presentation_ready(E,K,V) =
    exact_evidence_schema(E, "renpy_interaction_probe:v1")
    ∧ E.producer_id = "renpy_interaction_probe:v1"
    ∧ E.mounted_list_version_key = K
    ∧ E.mounted_visible_ids = V
    ∧ E.render_tree_hash = hash_of_committed_mounted_tree(K,V)
    ∧ E.actual_interaction = true
    ∧ E.prediction = false
    ∧ E.first_interactive_frame_committed = true
    ∧ E.viewport_ready = true
    ∧ E.focus_graph_ready = true
    ∧ E.all_visible_ids_reachable = true
    ∧ E.self_voicing_names_ready = true

make_presentation_evidence(R,B,V,E) =
    CONTRACT_ERROR
        when any exact input type/provenance/hash/version binding is invalid
    NO_EVIDENCE
        when exact evidence is valid but readiness bools are not all true
    PresentationEvidence(
        collection_epoch_id = R.collection_epoch_id,
        list_version_key = list_version_key(R,B,V),
        presented_unseen_ids = tuple(id for id in V
                                     if id in upstream_unseen(R))
    )
        when presentation_ready(E,list_version_key(R,B,V),V)

A_0 = SeenAccumulator(
    collection_epoch_id = R_open.collection_epoch_id,
    presented_unseen_ids = ()
)

accumulate_seen(A,Evidence) =
    CONTRACT_ERROR when exact types or epoch binding are invalid
    SeenAccumulator(
        collection_epoch_id = A.collection_epoch_id,
        presented_unseen_ids = CanonicalUTF8(
            set(A.presented_unseen_ids)
            union set(Evidence.presented_unseen_ids)
        )
    ) otherwise

journal_seen_ack_ids(R_submit, A) =
    CONTRACT_ERROR
        when exact types or epoch binding are invalid
    CanonicalUTF8(
        set(A.presented_unseen_ids)
        ∩ set(upstream_unseen(R_submit))
    )
        when persist_snapshot_valid(R_submit)
             and A.collection_epoch_id = R_submit.collection_epoch_id
    PERSISTENCE_UNAVAILABLE otherwise
```

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Visible IDs | `V` | exact tuple | `0–11` | 该列表版本实际渲染的成就 IDs |
| Presentation evidence | `E` | exact immutable record | fixed provenance/version/tree fields + 7 exact bools | 只能由 engine instrumentation 对 committed mounted tree 生成；普通 screen/controller 不能自由填写 |
| Seen accumulator | `A` | exact immutable record | one epoch + `0–11` unique IDs | 本 cycle 唯一有界累计状态；raw evidence fold 后立即丢弃，不保存 version ledger |
| Submit snapshot | `R_submit` | valid detached snapshot | 1 | 离开分区时重新取得的权威 snapshot；只用于相交，不扩张凭据 |
| Canonical request order | `CanonicalUTF8` | deterministic ordering | 1 | SYS-PERSIST batch 要求的 UTF-8 ID 顺序 |

**Output Range:** `CONTRACT_ERROR`、`NO_EVIDENCE`、`PERSISTENCE_UNAVAILABLE`，或 `0–11` 个 unique ID。空 tuple 不产生 mark-seen request。重复 version/evidence 只对同一 bounded set 做幂等 union；refresh 只能通过新的成功 evidence 增加可提交 ID，绝不能从 `R_submit` 自行加入未呈现项目。Accumulator retained size 的合同上限是 11 IDs，与 refresh/version 数量无关。

**Example:** v1 evidence 实际呈现 unseen `(A)`，accumulator 为 `(A)`；refresh snapshot 新增 B，但新 mounted tree 尚无合法 evidence 时关闭，提交只含 `(A)`。若 v2 evidence 已绑定并通过，accumulator 幂等变为 `(A,B)`；外部 merge 已把 A 标为 seen 时，提交只含 `(B)`。

### Visible Counts

The `journal_visible_count` formula is defined as:

```text
journal_visible_count(R, B, C, category) =
    CONTRACT_ERROR(code)
        when visible_ordered_ids(R,B,C,category) = CONTRACT_ERROR(code)
    NO_MODEL when visible_ordered_ids(R,B,C,category) = NO_MODEL
    len(visible_ordered_ids(R,B,C,category)) otherwise
```

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Visible ordered IDs | `V_k` | exact tuple | `0–7/7/11/6` | 当前分区实际渲染的项目 |
| Category | `k` | enum | 4 项 | 当前分区 |

**Output Range:** named `CONTRACT_ERROR`、`NO_MODEL`，或 chapter `0–7`、memory `0–7`、achievement `0–11`、ending `0–6`。只有 achievement count 用于玩家文案“曾经走过 X 项”；其余 count 只用于内部验证与测试。所有分区均不显示分母或百分比；invalid/unavailable 状态没有数值计数输出。

**Example:** 四区可见项目分别为 `2、2、3、1` 时，内部验证结果保持该四项计数；玩家界面只在旅途记录显示“曾经走过 3 项”，不得显示 `2/7`、`3/11` 或完成率。

### Focus Restoration

Refresh 与关闭使用不同 target catalog：

```text
restore_after_refresh(T_journal, previous, section_back, contents_entry) =
    FOCUS_TARGET(first(id for id in
        (previous, section_back, contents_entry)
        if id in T_journal))
    if any candidate exists
    FOCUS_CONTRACT_ERROR otherwise

restore_to_caller(T_caller, caller_entry, caller_fallback) =
    FOCUS_TARGET(first(id for id in
        (caller_entry, caller_fallback)
        if id in T_caller))
    if any candidate exists
    CALLER_FOCUS_UNAVAILABLE otherwise
```

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Journal focus targets | `T_journal` | exact set of semantic IDs | `≥1` | 当前 mounted Journal 模型的合法目标 |
| Caller focus targets | `T_caller` | exact set of semantic IDs | `≥1` | Journal 关闭后 mounted caller 的合法目标 |
| Previous target | `p` | semantic ID | 0–1 | 刷新前焦点 |
| Section return | `b` | semantic ID | 0–1 | 当前分区返回操作 |
| Contents entry | `h` | semantic ID | 0–1 | 首页对应分区入口 |
| Caller entry/fallback | `caller_entry/caller_fallback` | semantic IDs | 各 0–1/恰1 | 调用界面批准的目标 |

**Output Range:** exact `FOCUS_TARGET(id)` 或命名失败 enum；不调用 `first(empty)`，不把尚未 mounted 的 caller target 混入 Journal target set。

**Example:** 外部刷新移除了当前条目，`previous∉T` 但分区返回仍存在，则结果为 `section_back`。

*本公式合同已按 2026-08-03 full design-review 的 systems-designer、QA、UI 与 Ren’Py 专项意见修订；具体 8.5.3 API 调用仍需 ADR 与 engine spike。*

## Edge Cases

### Empty and Boundary Collections

- **If persistent root 合法且四类 membership 全为空**：首页先显示一段中性首开说明，四个入口仍可进入；各分区显示中性空页文案、“返回目录”和“关闭”，不显示可见数量 `0`、unavailable、分母、空槽或未来内容提示。
- **If 某一分区为空而其他分区非空**：只对该分区显示空页；其他分区正常呈现，不隐藏或禁用首页入口。
- **If membership 达到章节/回忆 7 项、成就 11 项或结局 6 项上限**：完整呈现全部已解锁项目；使用滚动，不截断、不抽样、不分页。
- **If 章节与回忆同时引用同一个 `MEMORY_DAY_N`**：分别呈现章节摘要和回忆详情，但收藏计数、解锁和持久化 membership 仍只有一项。
- **If 序章、尾声或一日多回忆没有批准的独立 ID**：不得由标题、章节位置或当前剧情推导解锁，也不得创建临时条目。

### Snapshot and Catalog Integrity

- **If snapshot schema、generation、exact type、canonical ordering 或 membership 任一非法**：不构建任何普通 read model，原子转入 `PersistenceRecoveryHandoff`。
- **If 顶层 bundle schema、generation matrix、source-hash manifest 或 closed ID sets 非法**：四个分区整体进入 `ContentHandoff`；不得显示 reset 收藏，也不得选择性信任其中一个目录。
- **If 顶层 bundle 已验证，但单一分区在 archive load、record schema 或引用解析时失败**：只将该分区标为 `CategoryUnavailable`；不得隐藏坏条目后显示部分分区列表，其他分区按各自完整验证结果继续可用。
- **If achievement backend 含有 canonical root 中不存在的 ID**：Journal 显示项目数不增加，backend 读取次数为 0。
- **If save slot、当前章节 flag 或 rollback 状态与 persistent membership 不同**：只使用 detached persistent snapshot；不得把当前时间线覆盖到跨周目记录。
- **If 玩家已回退到获得记录之前**：合法跨周目 membership 仍显示为“曾经走过”，但 Journal 不声称该内容属于当前恢复后的时间线。
- **If 结局条目缺少任一批准 `journal_cause_id` 摘要，或含 higher-priority exclusion/未到达路线**：不得用 cause ID、泛化失败文案或内部字段补位；ending 分区进入 `CategoryUnavailable`。
- **If 结局只有一条批准原因摘要**：只显示一条；不得复制或增加空白卡。
- **If 结局有三条批准摘要**：按 SYS-ENDING 给定顺序全部显示，不按长度、类型或语气重排。

### Concurrent Updates and Refresh

- **If persistence recovery、content fault、reset/epoch change、external merge、导航和 seen acknowledgement 同时待处理**：固定优先级为 persistence recovery → content handoff → epoch/reset invalidation → acknowledgement 已知终态 → coalesced refresh → 冻结的 `pending_user_intent` → 普通导航。Refresh 使用独立 `refresh_required` bool，不覆盖玩家 intent。
- **If external merge 在首页、分区列表或详情打开时到达**：冻结当前内容操作，完整验证并一次替换 read model；不得呈现半更新帧。
- **If external merge 在 `SeenAckPending` 期间到达**：只把 `refresh_required` 设为 true；先等待 acknowledgement 已知终态，再使用最新 snapshot 完整重建并重验证原 intent，不从旧 evidence 二次扩张 accumulator。
- **If refresh 后当前详情 ID 仍存在**：保留详情和稳定焦点；新条目不得自动抢焦点或打开。
- **If refresh 后当前详情 ID 不再存在**：返回对应分区并聚焦返回操作；不得恢复 stale displayable。
- **If refresh 新增 unseen achievement**：在批准位置加入条目并显示“新记录”，但不改变当前滚动位置或自动打开该条目。
- **If refresh 在列表 action 已按下但尚未派发时开始**：取消该旧 action；refresh 完成后要求玩家从新 read model 重新操作。
- **If reset 开始或 collection epoch 改变**：立即停止普通 Journal 交互并移交 reset/recovery 流程；不得把旧 epoch 条目保留到新模型。
- **If 相同合法 refresh payload 重复到达**：read model 深值不变，build/replacement/interaction restart 数均为 0，焦点与滚动位置不跳动；changed payload 合并后 build/replacement/restart 各恰 1 次。

### Seen Acknowledgement

- **If achievement 分区没有 unseen 项**：`journal_seen_ack_ids=()`，mark-seen adapter 调用数为 0。
- **If 列表只在 prediction/screen construction 中出现，或 engine probe 无法把 committed mounted version 与 viewport、focus graph、全部 item reachability、self-voicing tree exact 绑定**：返回 `NO_EVIDENCE`，不扩张 accumulator、不提交 mark-seen；所有 unseen 项保持“新记录”。
- **If 玩家留在旅途记录中浏览**：只把合法 evidence 幂等折叠进单一 `0–11` ID accumulator，不启动 persistence；请求返回目录或关闭时才进入一次 `SeenAckPending`。
- **If 同一列表版本重复产生等价 evidence**：accumulator 深值不变；interaction restart、滚动或详情往返不增加 retained state，也不重复提交。
- **If mark-seen 返回 durable success**：本次 `journal open cycle` 继续显示“新记录”；下一次打开从新 snapshot 显示“曾经走过”。
- **If mark-seen 返回 `PERSIST_FLUSH_FAILED_SAFE`**：保持 membership 与“新记录”，不显示成功提示；消费本次 pending intent，下一次真实呈现并离开时允许重试。
- **If mark-seen 返回 duplicate/no-op**：不产生提示或音频；本次 `journal open cycle` 的标签保持稳定，下一次打开按权威 snapshot 重算。
- **If mark-seen 返回 `PERSISTENCE_UNAVAILABLE` 或 `COMMIT_STATUS_UNKNOWN`**：停止普通 Journal 操作并进入 persistence 阻断恢复；不得声称记录已呈现确认或继续接受其他 persistent request。
- **If mark-seen 返回 `REJECTED_INVALID`**：视为实现/catalog contract fault并进入非破坏性 `ContentHandoff`；不得建议 reset。`REJECTED_REENTRANT` 证明本请求未进入 operation body；controller 清空 accumulator、保持 unseen、不建立队列、不等待上游事件、不自动重提并立即执行原 intent。若首个 persistence operation 随后进入全局 recovery，该 recovery 仍从任意普通状态立即抢占。
- **If acknowledgement 尚无已知终态**：全部输入已 gated，不能产生第二个导航/关闭请求；后台 refresh 只设置 `refresh_required`。页面显示并恰朗读一次“正在整理手册……”。
- **If external merge 已把某 unseen ID 标记为 seen，但本次 `journal open cycle` 已将其加入 session-new 集合**：当前仍显示“新记录”，下一次打开才移除标签。

### Navigation, Focus, and Presentation

- **If 玩家从主菜单进入**：关闭后恢复主菜单的愿望手册入口；若入口不存在，则使用主菜单批准的安全 fallback。
- **If 玩家从游戏菜单进入**：关闭后恢复游戏菜单入口，不改变叙事控制位置或 rollback state。
- **If achievement modal、阻断恢复或其他全局 input gate 禁止游戏菜单**：Journal 请求不可达，不得通过快捷键或 screen action 绕过。Journal 已打开时，非阻断 modal 延后到关闭后；阻断恢复立即抢占并清除 Journal controller。
- **If 前一焦点条目在刷新后消失**：在 mounted Journal target set 中依次尝试分区返回、首页对应入口；关闭后才在 mounted caller target set 中尝试 caller entry/fallback。不得跨 screen 混用 target 或按坐标猜测。
- **If 分区列表为空**：静态空页文案不进入 Tab 顺序；初始交互焦点为返回操作。
- **If 文案在 1280×720 或最大字体倍率下超过可见区域**：文本与条目使用可键盘操作的滚动区域；返回操作保持可达，不裁切字形。
- **If 玩家只使用键盘、自发声、静音或 reduced-motion**：四区进入、阅读、返回和关闭仍全部可完成；hover、声音、颜色、动画或定时输入均不是必要信息通道。
- **If 标题或摘要包含 internal ID、axis、token、qualification、predicate、threshold、backend、schema 或 epoch 文案**：catalog validation 失败；不得在运行时删除敏感片段后继续显示。
- **If 页面没有任何收藏内容**：不显示可见数量 `0`、`/7`、`/11`、`/6`、百分比或“尚缺”提示；只显示批准的中性空页文案和 exact action tuple `(section_back, journal_close)`。
- **If 玩家尝试搜索、筛选、排序、领取、撤销、删除、重置或重播章节**：首发界面不存在对应 action；不得以 disabled 控件预告这些功能。

*本边界矩阵已按 2026-08-04 re-review revision 修订；engine-specific failure injection 仍须由 ADR、SYS-PERSIST 与 SYS-TEST 固定。*

## Dependencies

| Dependency | Strength | Direction | Required Interface | Current Status / Gate |
|---|---|---|---|---|
| Ren’Py 8.5.3 | Hard runtime | Engine → SYS-JOURNAL | Screen、viewport、keyboard focus、self-voicing、interaction restart 与主/游戏菜单入口 | Engine pinned；8.5.3 高知识风险，具体 API 在 ADR/实现前复核 |
| Game Concept | Hard design authority | Concept → SYS-JOURNAL | 四项创作支柱、价值中立、六结局、七日结构及绘梨衣表达边界 | Approved |
| ADR-0002 | Hard state boundary | ADR → SYS-JOURNAL | 单一 persistent root、detached reads、`seen_achievement_ids`、mark-seen、epoch/reset/recovery | Accepted |
| ADR-0003 | Hard presentation boundary | ADR → SYS-JOURNAL | Screen 只读、不决定叙事结果、稳定资源名、键盘与 1280×720 可读性 | Accepted |
| SYS-PERSIST | Hard runtime/data | SYS-PERSIST ↔ SYS-JOURNAL | Snapshot、fingerprint、availability、merge/reset/recovery；Journal 输出 bounded evidence 支持的 exact mark-seen IDs，并消费完整 result enum | GDD 与系统索引均为 In Revision；核心 contract 继续作为上游权威，完成 re-review 前阻止 Journal implementation-ready |
| SYS-NARRATIVE | Hard content | SYS-NARRATIVE → SYS-JOURNAL | `journal_chapter_catalog:v1`、`journal_memory_catalog:v1`、逐日 common-path truth approvals 与稳定 `memory_ids` 映射 | In Revision；7×2 source records 与 truth review 冻结前阻止 Journal content lock |
| SYS-ACHIEVE | Hard catalog / bidirectional acceptance | SYS-ACHIEVE → SYS-JOURNAL；SYS-JOURNAL → achievement UI gate | 11 项目录、“场景回声→路线发现→后来留下的回声”组序、seen 语义；Journal 自己调用 mark-seen adapter | Approved；同步 caller/copy amendment 后，backend/UI/audio/performance acceptance 仍有下游 gates |
| SYS-ENDING | Hard content | SYS-ENDING → SYS-JOURNAL | 六结局 membership、批准标题/摘要、`journal_display_rank` 及原序 `journal_cause_ids` 文案 | Approved with provisional downstream gates；Journal projection catalog 完整性阻止 content lock |
| SYS-ACCESS | Hard cross-cutting production gate | SYS-ACCESS → SYS-JOURNAL | 五项project settings、唯一font/contrast authority、0 ms reduced-motion、keyboard、自发声与 transcript 合同 | Designed；full re-review pending，不阻止本 GDD，阻止 UI story Ready 和 implementation acceptance |
| SYS-SAVE | Hard integration gate | SYS-SAVE ↔ menu/Journal | 游戏菜单可用性、阻断流程、调用位置与返回焦点；不得提供收藏数据 | In Revision；入口和恢复集成在其 gate 关闭前 provisional |
| SYS-TEST | Hard acceptance gate | SYS-JOURNAL → SYS-TEST | Catalog、read model、0/max items、focus、merge、mark-seen、recovery、layout 与 accessibility fixtures | Not Started；阻止 implementation accepted |
| SYS-AUDIO | Soft presentation | SYS-JOURNAL → SYS-AUDIO | 中性页面/通知音事件、静音与 self-voicing suppress 规则 | Not Started；声音不得阻止完整操作 |
| SYS-BUILD | Hard packaging/validation | SYS-JOURNAL → SYS-BUILD | 执行 `journal_catalog_bundle:v1` assembler、source hashes、generation matrix、archive closure 与 test-only evidence-forger exclusion；保留production probe | Not Started；阻止 release artifact lock，不允许改写 source catalogs |
| Art Bible / asset pipeline | Soft presentation, required before asset production | Art → SYS-JOURNAL | 纸页、票据、印记、雨后余光的视觉语言及合法素材来源 | Not Started；允许明确标记的占位资源 |
| UX specifications | Hard pre-epic delivery gate | GDD → `/ux-design` → stories | 首页、四分区、详情、空页、恢复、720p/字体倍率 wireframes 与 focus graph | Not Started；创建 UI epics 前必须完成 |

### Interface Boundaries

- SYS-PERSIST 独占 persistent root、schema、validation、merge、flush、reset 与 recovery；SYS-JOURNAL 只可作为冻结的 Journal caller 调用专用 `achievement-mark-seen` adapter，不自由填写 requester/checkpoint。
- SYS-NARRATIVE 独占章节与回忆 source records、`common_path_truth_approval_id` 及完成条件；Journal 拥有 bundle projection schema，但不读取章节 flag/history、不创建独立 `chapter_ids`，也不把共通摘要扩写为本次 traversal 事实。
- SYS-ACHIEVE 独占成就条件、catalog 与 seen 语义；自动 modal 关闭由 SYS-ACHIEVE caller 提交 mark-seen，Journal 成功呈现由 SYS-JOURNAL caller提交，二者由 SYS-PERSIST adapter 幂等收敛。
- SYS-ENDING 独占 resolver、结局 priority、cause identity 与安全摘要筛选，并构建 Journal 专用 projection；Journal 不重排、重新过滤或从 `display_cause_ids` 推导 `journal_cause_ids`。
- SYS-ACCESS 独占最终无障碍设置和交互合同；本 GDD 只规定必须达到的行为结果。
- SYS-SAVE 只决定 `journal_menu_gate:v1`、调用方 focus catalog 与恢复边界，不向 Journal 提供收藏 membership；SYS-SAVE GDD 的 2026-08-04 amendment 是该反向接口的权威。
- SYS-BUILD 只执行 SYS-JOURNAL 拥有的 bundle assembler contract、hash 与 archive closure；不拥有或改写任何玩家文案、ID、rank 或 truth approval。
- SYS-AUDIO 与美术只能增强手册体验，不能成为内容理解、状态区分或导航的唯一通道。
- SYS-GALLERY 与 Journal 可复用同类 detached-snapshot原则，但二者没有运行时依赖，也不得共享可变 UI 状态。

### Bidirectional Consistency Findings

1. 系统索引已为 SYS-JOURNAL 列出 SYS-PERSIST、SYS-NARRATIVE、SYS-ACHIEVE、SYS-ENDING、SYS-ACCESS 与 SYS-SAVE；本版另显式补充 acceptance 已实际依赖的 SYS-TEST、SYS-AUDIO 与 SYS-BUILD gates。
2. SYS-ACHIEVE 将 SYS-JOURNAL/SYS-ACCESS 列为 UI acceptance dependency，而 SYS-JOURNAL 从 SYS-ACHIEVE 获取 catalog。这是“数据输入 + 验收输出”的双向集成，不授予 Journal 成就 ownership。
3. SYS-NARRATIVE、SYS-ENDING 和 SYS-PERSIST 已把 Journal 声明为只读下游，方向与本设计一致。
4. SYS-PERSIST 的 GDD header 与系统索引已统一为 `In Revision`；其 re-review 仍是 Journal implementation-ready 的上游 gate。
5. SYS-SAVE 已通过 2026-08-04 amendment 声明 Journal game-menu gate、caller focus 与 blocking-load exclusion；Q12 的设计合同关闭，具体 UX captures 仍为下游证据。
6. SYS-ACCESS 已达 Designed（完整复审待完成）；SYS-TEST、SYS-AUDIO 与 SYS-BUILD 尚无批准 GDD。其最终接口分别是 UI story、implementation acceptance、audio acceptance 与 release artifact lock 的下游 gate，不改变本 GDD 已冻结的 ownership。

## Tuning Knobs

SYS-JOURNAL 首发不新增专属数值参数。它只消费既有系统拥有的设置与演出参数，避免同一行为出现多个配置权威。

| Knob | Owner | Target / Options | Safe Range | Journal Rule |
|---|---|---|---|---|
| `font_scale_options` | SYS-PERSIST / SYS-ACCESS | `1.0, 1.25, 1.5` | 仅这三档 | 四区首页、列表、详情、空页与恢复界面全部响应；Journal 不缓存或覆盖 |
| `settings.high_contrast` | SYS-ACCESS | `false/true` | exact bool | 所有状态必须保持等价语义；颜色不是唯一标识 |
| `presentation_settle_delay_ms` | SYS-ACHIEVE | `500 ms` | `0–1000 ms` | 只作用于成就通知，不延迟 Journal 主动打开或 mark-seen |
| `notification_transition_ms` | SYS-ACHIEVE | `200 ms` | `0–300 ms` | 只作用于成就通知；reduced-motion 时 effective value 为 `0 ms` |
| `reduced_motion` | SYS-ACCESS | `false/true` | exact bool | Journal 页面不得依赖转场完成才能交互；具体视觉替代由 UX spec 定义 |

以下内容不是 tuning knobs，不得通过数据配置改变：

- 四个首页分区及其顺序；
- 章节/回忆 7 项、成就 11 项、结局 6 项上限；
- 未解锁内容完全缺席；
- 成就三组顺序和低强调度“新记录”的呈现语义；
- 结局原因数量、identity 与顺序；
- mark-seen 的成功边界、UTF-8 request order 和一次提交规则；
- refresh 优先级、原子替换与焦点 fallback 顺序；
- 无分母、百分比、空槽、攻略提示；
- 不提供搜索、筛选、自定义排序、领取、撤销、重置或重播。

页面转场、行距、卡片间距、滚动步长、viewport 尺寸与详情留白属于响应式 UX 参数，应在 `/ux-design` 中结合 1280×720、三档字体和键盘焦点证据确定；不得在 GDD 中提前冻结未经版式验证的数值。

## Visual/Audio Requirements

### Visual Direction

- 愿望手册采用“私人旅途手册”视觉语言：无涂层纸、轻微雨痕、铅笔批注、票据、压印、折页与雨后微光。基础色为纸张暖灰、墨色和低饱和雨蓝；纹理必须退居文字之后。
- 首页四区始终使用等权重入口，仅以纸质线索区分内容类型：
  - 章节：装订页签；
  - 回忆：纯文字物件剪贴页与中性类别装饰；首发不要求逐回忆专属插图；
  - 旅途记录：文字印记；
  - 结局：归档页。
- 这些差异不得表达稀有度、价值或完成等级。禁止奖杯、星级、五色轴、进度环、稀有度边框、空槽、收藏册厚度和“最佳结局”视觉语言。
- 章节与回忆共享 membership 时，视觉上表达为“同一经历的两种阅读方式”，不得出现双份解锁、双份计数或两次奖励反馈。
- 列表只渲染已解锁项目；成就空组不显示标题或留白。未解锁内容不得通过剪影、问号、页码缺口或预留空间暗示。
- “新记录”必须同时使用明确文字和非颜色性的纸签或新压印轮廓；“曾经走过”使用稳定文字状态。两者不能只靠色彩、亮度或动画区分。
- “新记录”标签在当前 `journal open cycle` 保持稳定，不闪烁、不脉冲，也不在 mark-seen 成功后立即消失。
- 详情页延续相同纸面体系。结局原因使用等尺寸、等层级的小记页，严格保持上游 1–3 条顺序；不得补空卡、突出真结局或弱化悲剧。
- 合法空状态使用已有分区标题的干净页面和中性、无剧透文案。不可用状态不得复用空页：persistent 故障使用 SYS-PERSIST 恢复表现，bundle 故障使用非破坏性内容不可用表现，单分区故障使用该分区的不可用页；三者不得共用 reset 暗示。
- Achievement 11 项全部获得时仍只显示现有已解锁记录，不增加“完整”“全收集”或庆祝终态；“悲剧也是完整答案”只作为内部创作支柱，不转译成收藏完成率文案。
- 所有文字实时渲染，不把简体中文烘焙进图片，以支持三档字体、自发声、本地化和高对比度模式。铅笔批注、票据标签与压印是中性编辑层，不伪装成绘梨衣写下的完整语言；任何绘梨衣真实书写物必须由 SYS-NARRATIVE source record 明确登记。
- 高对比度模式必须降低或移除纸纹、雨痕与装饰干扰，同时保留所有标题、状态和焦点语义。

### Motion

- 仅允许一次性、克制的淡入、轻微纸页位移或层叠切换。
- 禁止拟真翻页、弹跳、粒子、循环发光、闪烁、屏幕震动与庆祝式演出。
- “新记录”可以使用一次轻微压印出现，但文字标签必须从首个可交互帧起清晰存在。
- 原子 refresh 完成前不播放转场；完成后不得自动滚动、抢焦点或打开新条目。
- reduced-motion 下所有转场立即完成；信息、层级、焦点、阅读顺序与操作必须完全等价。
- 玩家不需要等待任何动画结束才能滚动、返回或关闭。

### Audio

- Journal 的可选声音只使用克制的干燥纸张、轻翻页、铅笔或印章触感；不得使用奖杯解锁声、胜利和弦或稀有度音色。
- 主动浏览不为每个条目或“新记录”状态播放声音。Journal 只能触发普通、不依赖 unseen 的页面导航纸页声；跨系统新解锁声音只由 SYS-PERSIST notification group 的唯一 coordinator/SYS-AUDIO owner触发。Mark-seen、duplicate、safe failure、merge、refresh 与 seen-only 更新的音频事件数均为 0。
- 六个结局使用相同音色、音高、响度与包络，不建立声学等级。
- 静音时全部流程保持完整。Self-voicing 激活时，全部 Journal UI 声音 dispatch/play count 为 0；若切换 self-voicing 或 recovery 接管时已有实例播放，stop count 恰为 1。
- 异常、不可用和恢复状态不能依赖警报声传达；必须通过文本、焦点与可操作项说明。
- 最终声音文件、响度、格式和替换 ID 由 SYS-AUDIO 批准；在其 GDD 完成前，本节只冻结语义和最大触发次数。

### Asset and Licensing Boundary

需要的资产类别包括：

- 纸张与雨痕纹理；
- 装订、分隔和折页元素；
- 四区中性图形；
- 条目、详情和结局原因框；
- 默认、高对比度、焦点与选中状态；
- 空页装饰；
- persistence recovery、content handoff 与 category unavailable 三类不可用状态所需的可区分兼容表现；
- 可选纸页与印章声音。

每项资产必须登记来源、作者、许可、hash、格式和稳定替换 ID。只允许原创、明确委托授权、CC0/公版，或具有修改与再分发权的素材。字体必须具备可嵌入发行包的书面许可和完整简体中文覆盖。

禁止使用官方《龙族》美术、Logo、截图、小说扫描、音乐、字体、游戏资产或任何来源不明素材；整体表现不得暗示官方授权。占位资源必须明确命名，并可在不修改叙事或状态代码的情况下替换。

### Production Gates

- 当前尚无 Art Bible；色板、纹理密度、字体、图形母题、焦点状态和高对比度变体均为 provisional，阻止正式资产制作。
- SYS-ACCESS 已形成 Designed 合同并完成首轮 full review 修订；最终 wireframe、目标 TTS 配置、读序、对比度、字体与焦点 evidence 仍是硬 gate，待独立 re-review 后方可关闭。
- SYS-AUDIO 未设计，任何 Journal 音效仍为 provisional。
- 正式资产制作前必须完成 Art Bible、`/asset-spec system:sys-journal`、字体许可审查和最大字体视觉 captures。

*Art Director 专项建议已纳入；未声称完成 Art Bible 或正式资产审批。*

## UI Requirements

### Screen Hierarchy and Entry

```text
Main Menu / Game Menu
        ↓
     Validating
        ↓
Journal Contents
        ↓
Category List
        ↓
Item Detail
```

- 主菜单与游戏菜单共用同一内部层级，但分别使用 SYS-SAVE `journal_caller_focus_catalog:v1`：主菜单`(entry=main_menu_journal,fallback=main_menu_start)`，游戏菜单`(entry=game_menu_journal,fallback=game_menu_return)`。
- 每次新的 `journal open cycle` 都从 Journal Contents 开始，不直接恢复上次分区。
- SYS-SAVE `journal_menu_gate:v1` 仅允许安全主菜单与`PlayableStable`游戏菜单；`CriticalInteraction`、`LoadedUnvalidated`、`BlockingSafeFlow`、unsupported/corrupt load及动态recovery时入口visible/enabled/focusable均为false，direct action/快捷键调用数为0，不得短暂打开 Journal 后再关闭。
- Validating 完成前不显示普通目录或旧 snapshot 内容。
- 关闭 Journal 时恢复调用方入口；入口不存在时使用该调用界面批准的 fallback。

### Journal Contents

Self-voicing 阅读顺序固定为：

1. 页面标题“愿望手册”；
2. 玩家安全的简短说明；
3. “章节”；
4. “回忆”；
5. “旅途记录”；
6. “结局”；
7. “关闭”。

标题与说明不进入 Tab 顺序。顶层 bundle 有效时，首页初始交互焦点固定为第一个目录入口 `chapter`；四个入口始终可聚焦，单区或四区全部 unavailable 时激活对应入口进入该区 `CategoryUnavailable`，不跳到 `ContentHandoff`。只有顶层 bundle 本身无效才显示 ContentHandoff 的首个安全操作。四个入口具有相同尺寸、层级、对比、装饰预算与进入反馈，不显示完成率、推荐顺序或新内容数量。方向键、Tab/Shift+Tab、鼠标和 Ren’Py 默认可用的部分手柄导航都必须可达。

Escape 或右键在首页执行一次关闭，不传播到底层主菜单或游戏菜单。

### Category Lists

所有分区使用相同语义结构：

1. 分区标题；
2. 可选的玩家安全说明；
3. 可见条目列表或合法空页；
4. 返回目录；
5. 关闭 Journal。

具体内容：

| 分区 | 列表内容 | 详情内容 |
|---|---|---|
| 章节 | 已完成 Day 1–7 的章节标题与短摘要 | 较完整的玩家安全章节概览 |
| 回忆 | 同一 memory membership 对应的纯文字物件、行动或情感片段 | 批准的纯文字回忆正文；首发无 per-memory image/alt 字段 |
| 旅途记录 | 成就名称、“新记录”或“曾经走过” | 批准描述；不显示条件或缺失步骤 |
| 结局 | 已完成结局标题与批准短摘要 | 结局摘要及原序 1–3 条原因内容 |

- “章节概览”与“回忆片段”必须使用不同标题、说明和内容目录，避免被理解为重复收藏。
- 成就只显示非空组，按“场景回声→路线发现→后来留下的回声”排列。
- 仅旅途记录显示“曾经走过 X 项”；11 项全部获得时也不显示“完整”、`11/11`、百分比或庆祝终态。
- 章节、回忆和结局默认不显示可见数量。
- 所有分区均不显示分母、百分比、空槽或 locked hints。
- 非空列表初始交互焦点为首个可见 row；合法空列表的初始交互焦点为“返回目录”；不可用分区按冻结 fault-surface manifest 聚焦 `category_retry`。标题、说明、组标题与静态空页文案不进入 Tab 顺序。
- Escape/右键从列表返回目录且只执行一次。

### Valid Empty State

合法空分区仍可进入，包含：

1. 分区标题；
2. 尚待批准的中性、无剧透空页文案；
3. 返回目录；
4. 关闭 Journal。

空页装饰与说明不进入 Tab 顺序；初始交互焦点位于“返回目录”。空状态不得使用“错误”“不可用”“恢复”或任何未来内容提示。

### Item Detail

- 进入详情前保存来源条目的 semantic item ID 和列表滚动位置。
- 阅读顺序为：标题 → 状态标签（如适用）→ 正文 → 结局原因（如适用）→ 返回。
- 详情初始交互焦点为“返回列表”；正文使用独立可键盘滚动 viewport，静态内容不进入 Tab 顺序但必须进入 self-voicing reading tree。
- 返回详情时恢复来源条目与滚动位置，而不是列表顶部。
- 若 refresh 后来源条目不存在，则返回分区并聚焦“返回目录”，同时显示并通过 self-voicing 恰宣布一次 `journal_content_changed_notice`：“手册内容已更新，原记录暂时无法继续显示。”同一原子 replacement 只允许一次该通知；普通新增、排序不变或仍存在的条目不触发。
- 结局原因使用相同语义层级，严格保持上游顺序；没有独立“最佳原因”焦点或视觉状态。
- Escape/右键从详情返回列表且只执行一次。

### Focus and Scrolling

- 所有 interactive rows 使用稳定 semantic ID，不用屏幕坐标或 displayable identity 恢复焦点。
- 键盘将焦点移动到 viewport 外条目时，该条目自动滚入可视范围。
- External refresh 新增条目时不得自动滚动、聚焦或打开。
- 1280×720 是硬布局基线；1920×1080 只增加留白或同时可见行数，不改变内容顺序和导航结构。
- 字体 `1.0/1.25/1.5` 使用同一语义结构。内容溢出时，列表和详情分别使用键盘可操作的 viewport。
- 最大集合 7/7/11/6 项连续可达，不截断、不分页。
- “返回目录”与“关闭”使用 viewport 外的固定 action rail，在 1280×720、字体 1.5 下始终可见、可聚焦且不遮挡正文；列表/详情内容单独滚动。
- `process session` 内分别保存四区 scroll position；退出进程后清空，不写入 persistent、save 或 imported cache。

### New Record and Seen Acknowledgement

一次 achievement list version 的 presentation evidence 生成必须同时满足：

1. Snapshot、bundle 与 achievement category 已完整验证；
2. 当前不是 prediction，真实 interaction 的首个可交互帧已经 commit；
3. viewport、exact focus graph、reading order、返回与关闭操作已经建立；
4. 每个已解锁条目都可通过键盘滚动到达；
5. self-voicing 可访问名称包含条目名称与“新记录/曾经走过”状态；
6. Engine probe 的 producer ID、mounted `list_version_key`、visible-ID tuple 与 committed render-tree hash exact-match。

满足后只生成 immutable evidence，controller 立即把其中 IDs 幂等折叠进单一 bounded accumulator并丢弃 evidence，不立即写 persistent。玩家请求离开旅途记录或关闭 Journal 时，controller 重新取得 `R_submit`，把 accumulator IDs 与当前 upstream unseen 相交，再提交 exact payload。Evidence 不声称玩家已逐项阅读。

`SeenAckPending` 是短暂的写入子状态：

- 进入前先显示静态 blocking-safe pending frame，再 gate 全部输入；同步 `save_persistent()` 期间不承诺滚动或 self-voicing 可以并发运行；
- 只保留触发写入的一个 immutable `pending_user_intent`；后台更新只设置 `refresh_required=true`，两者互不覆盖；
- 页面显示非技术化 live status：“正在整理手册……”；
- status 必须通过文本与 self-voicing 恰宣布一次，不依赖 spinner、声音或动画；
- `APPLIED_FLUSHED`、`DUPLICATE_NOOP` 或 `PERSIST_FLUSH_FAILED_SAFE` 后移除 status；若有 refresh，先刷新，再对新模型重验证并执行原 intent；
- durable success 不显示成功 toast，不改变当前 `journal open cycle` 的“新记录”标签；
- safe failure 不显示失败技术细节，标签保持“新记录”；
- `PERSISTENCE_UNAVAILABLE/COMMIT_STATUS_UNKNOWN` 取消 intent、清除普通 UI并进入 persistence recovery；`REJECTED_INVALID` 进入 content handoff；`REJECTED_REENTRANT` 清 accumulator、保持 unseen、不二次提交、不等待未定义事件并立即执行 intent，后续全局 recovery 仍可抢占。

### Refresh and Recovery

- Persistent callback 只记录已验证 generation/fingerprint；主线程 controller 的 refresh 顺序固定为：冻结旧模型 action → 完整验证新 snapshot/bundle/category → 构造完整 read model → 单次替换 → 恢复 mounted Journal semantic focus → 必要时恰一次 restart。
- 刷新期间不显示半更新内容，不派发旧列表 action。
- 若 refresh 在 `SeenAckPending` 到达，只设置 `refresh_required`；先等待 acknowledgement 已知终态，再验证最新 snapshot；不从旧 evidence 扩张 accumulator或提交第二次 acknowledgement。
- 新 unseen 成就加入当前 `journal open cycle` 的 session-new 集合，但不抢焦点。
- Invalid root、persistence unavailable、commit-unknown 或 reset recovery 移交 persistence recovery；顶层 bundle generation/hash corruption 移交 content handoff；已验证 bundle 内的单分区 load/reference failure 只禁用该分区。
- Persistence/content handoff 接管后，普通列表、返回旁路、scroll cache、session-new IDs、bounded accumulator、未消费 evidence 和旧焦点缓存均不可达。
- 分区 fail-closed 只允许继续使用其余各自完整验证的分区；不得从损坏目录选择性抢救条目。

### Fault-Surface Interaction Contract

| Surface | Exact actions | Initial focus | Escape / right-click | Retry / next state |
|---|---|---|---|---|
| `CategoryUnavailable(k)` | `(category_retry, section_back, journal_close)` | `category_retry` | `section_back` / `section_back`，各只执行一次 | retry 成功→`CategoryList(k)`；单区仍坏→原状态；顶层失效→`ContentHandoff` |
| `ContentHandoff` | `(reload_installed_content, return_safe_menu, quit_application)` | `reload_installed_content` | `return_safe_menu` / `return_safe_menu`，各只执行一次 | reload 全量验证成功→`Validating`；失败→原状态；不得出现 collection reset |
| `PersistenceRecoveryHandoff` | SYS-PERSIST `persistence_recovery_surface:v1` 的 exact actions | 上游批准首个 safe action | 上游阻断规则；不得返回 Journal caller | 只由 SYS-PERSIST 决定主菜单、退出或重新初始化；Journal action count=0 |

Self-voicing 顺序均固定为标题→玩家安全说明→上述 exact actions。若四区同时 unavailable，首页仍是 `Contents`，首焦点 `chapter`；依次激活四入口分别进入对应 `CategoryUnavailable(k)`，ContentHandoff render count 为 0。

### Accessibility

- Self-voicing 朗读标题、说明、状态、条目正文和操作；不朗读装饰、隐藏条目、分母或内部 ID。
- “新记录/曾经走过”必须成为条目的可访问名称组成部分。
- Self-voicing 不自动激活任何入口、条目、返回或关闭操作。
- 高对比度模式降低或移除纸纹、雨痕及低对比装饰；焦点和状态同时使用文字与清晰轮廓。
- Reduced-motion 在首个可交互帧完成全部状态替换；不等待淡入、压印或纸页位移。
- 静音、keyboard-only、self-voicing 和最大字体下均能完成进入、四区浏览、详情、返回与关闭。
- 任何功能都不依赖 hover、定时输入、声音或动画完成。

### Copy Boundary

当前已批准或本节提出的 UI 文案：

- “愿望手册”
- “章节”
- “回忆”
- “旅途记录”
- “结局”
- “新记录”
- “曾经走过”
- “曾经走过 X 项”
- “正在整理手册……”
- “手册内容已更新，原记录暂时无法继续显示。”
- “这一部分暂时无法打开”
- “手册内容暂时无法载入”
- “返回目录”
- “关闭”

四个分区的说明、合法空页文案、category unavailable、content handoff 与 persistence recovery 文案仍需在 `/ux-design` 中完成 spoiler、self-voicing 与最大字体审查；content 类文案不得出现“重置收藏”。

### UX Handoff

创建 UI epics 前，必须由 `/ux-design` 交付：

- 主菜单与游戏菜单入口/返回 flow；
- 首页、四区列表、四类详情、空页、pending 与 recovery wireframes；
- 1280×720、1920×1080及三档字体响应式矩阵；
- exact keyboard focus graph、reading order 和 Escape/右键行为；
- viewport 高度、滚动步长、长标题换行及返回操作布局；
- 结局原因 1/2/3 项响应式排列；
- high-contrast 与 reduced-motion variants；
- exact self-voicing transcripts；
- mark-seen readiness、pending status 与 queued-request interaction tests；
- 章节概览与回忆片段的内容差异验证。

章节/回忆无调试盲测使用预注册问卷和评分 rubric：至少 8 名未接触设计材料的参与者中，至少 7/8 能复述“同一天的共同经过与其中一个片段”，至少 7/8 能分别找到指定的日级共同事实和近景片段，把两区误认为两份独立收藏或完成率槽位者不得超过 1/8。未达到任一阈值即执行 Core Rule 4 的合并 fallback，不以追加说明文字代替。

*UX Designer 专项建议已纳入；未声称完成正式 UX spec 或 SYS-ACCESS 审批。*

## Acceptance Criteria

### Authority and Catalog Integrity

| ID | Evidence | Criterion |
|---|---|---|
| `JOURNAL-AUTH-001` | `STATIC + INSTR` | **GIVEN**versioned Journal production source/callgraph manifest，**WHEN**分别执行首次open、changed refresh、category retry与ContentHandoff reload，**THEN**每个 transaction 的 membership snapshot read恰1，renderer/screen-eval read为0；direct persistent、achievement backend、save slot、axis、history、token、qualification、predicate 与 live chapter flag 读取数均为 0。 |
| `JOURNAL-AUTH-002` | `UT_PURE` | **GIVEN**合法 schema-v2 snapshot、`journal_catalog_bundle:v1` 与四个 exact catalogs，**WHEN**执行 `journal_model_result`，**THEN**输出 exact `READY((READY(chapter),READY(memory),READY(achievement),READY(ending)))`。 |
| `JOURNAL-AUTH-003` | `UT_PURE + MUTATION` | **GIVEN**bundle wrong schema/generation/hash/closed-set单缺陷、单category wrong record/ref及chapter-memory pair mismatch fixtures，**WHEN**执行`journal_model_result`，**THEN**bundle缺陷exact `CONTENT_BUNDLE_UNAVAILABLE`，普通单区缺陷只对目标分区返回`CATEGORY_UNAVAILABLE(k)`，pair mismatch只使chapter与memory两区unavailable，achievement/ending保持READY；选择性坏条目renderer count为0。 |
| `JOURNAL-AUTH-004` | `STATIC + UT_PURE` | **GIVEN**`journal_catalog_bundle:v1` golden manifest及四个 owner-signed source catalogs，**WHEN**由 SYS-BUILD 执行 SYS-JOURNAL assembler并验证 generation/hash/ID闭集，**THEN**generation matrix exact-match冻结常量、chapter/memory各7 IDs、achievement恰11、ending恰6、每个引用解析恰1次、SHA-256均为64位lowercase hex；build-side copy/ID/rank rewrite count为0。 |
| `JOURNAL-AUTH-005` | `UT_PURE + CONTENT + PLAYTEST` | **GIVEN**7×2 copy fixtures、逐日 `common_path_truth_approval_id`、完整 completed-path facts及预注册8人盲测rubric，**WHEN**构建两区并审查，**THEN**每条chapter只含对应日全部合法completed paths共同成立的`DAY_OVERVIEW + REALIZED_COMMON_RESULT`，每条memory恰含一个共同成立的`OBJECT/ACTION/EMOTIONAL_CLOSEUP`且不声称互斥选择；truth approval逐项通过、history read=0、membership/unlock/count各一项；盲测理解两项均≥7/8且双收藏/完成率误解≤1/8，否则输出`MERGE_SECTIONS_REQUIRED`。 |
| `JOURNAL-AUTH-006` | `STATIC` | **GIVEN**versioned renderable/speakable copy manifest，**WHEN**扫描 internal ID、axis、token、qualification、predicate、threshold、backend、schema、epoch、条件进度、“完整/全收集/真结局”与攻略语句，**THEN**命中数均为 0。 |
| `JOURNAL-AUTH-007` | `UT_PURE + STATIC` | **GIVEN**0/1/2/3/4 个 cause IDs、重复ID、错误scope与批准fixtures，**WHEN**执行category validation并构建结局详情，**THEN**只有1–3个exact unique且scope合法的tuple通过，数量、identity、顺序exact-match上游；0/4/duplicate/wrong-scope均为`CATEGORY_UNAVAILABLE(ending)`，higher-priority exclusion、补卡、删卡、重排与 runtime filtering 数均为0。 |
| `JOURNAL-AUTH-008` | `UT_ENGINE + INSTR` | **GIVEN**backend-only achievement、save/current-run 差异及 rollback-before-unlock fixtures，**WHEN**打开 Journal，**THEN**显示只匹配 canonical root；backend→UI membership、save→persistent 与 rollback→persistent 写入数均为 0。 |

### Formula Coverage

| ID | Evidence | Criterion |
|---|---|---|
| `JOURNAL-FORM-001` | `UT_PURE` | **GIVEN**每类 membership 的 0、1 与最大 golden tuples，**WHEN**执行 `visible_ordered_ids`，**THEN**输出逐项 exact-match各自预期 ordered tuple；unknown/duplicate/category-invalid fixture返回命名 contract error，category unavailable返回 `NO_MODEL`。 |
| `JOURNAL-FORM-002` | `UT_PURE` | **GIVEN**乱序合法 memberships，**WHEN**构建四区可见 IDs，**THEN**chapter/memory按日序、achievement按批准rank、ending按 `journal_display_rank` 排序，重复运行深值相等且 resolver priority/acquisition order 读取数为0。 |
| `JOURNAL-FORM-003` | `UT_PURE` | **GIVEN**opening unseen 集合、mark-seen 后 refresh 及新增 unseen merge，**WHEN**连续执行 `journal_session_new_ids`，**THEN**本次 `journal open cycle` 保留原 new IDs、合入新 IDs并按 achievement rank 排序；关闭后清空。 |
| `JOURNAL-FORM-004` | `UT_PURE + MUTATION` | **GIVEN**0–11 unseen、probe schema/provenance/version/tree-hash/readiness字段逐项mutation、v1/v2 evidence、bounded accumulator及submit时新增/已seen IDs，**WHEN**生成evidence、累计并执行`journal_seen_ack_ids`，**THEN**只有exact绑定且全部readiness为真生成evidence；accumulator始终为0–11 unique IDs，payload exact等于“accumulator IDs∩当前unseen”的UTF-8 tuple，未呈现新增ID永不进入；invalid exact type/provenance/hash/epoch返回`CONTRACT_ERROR`。 |
| `JOURNAL-FORM-005` | `UT_ENGINE + INSTR` | **GIVEN**同一/不同`list_version_key`的prediction、restart、scroll、detail round-trip、refresh及1000次重复合法evidence，**WHEN**累计并离开分区，**THEN**raw evidence在fold后retained count=0、accumulator ID count≤11且重复输入深值不变；`ack_ids!=()`时adapter submission恰1，`ack_ids=()`时为0，prediction submission=0。 |
| `JOURNAL-FORM-006` | `UT_PURE` | **GIVEN**四区合法 visible tuples、category unavailable与contract-invalid fixtures，**WHEN**执行 `journal_visible_count`，**THEN**合法输出exact tuple长度、unavailable输出 `NO_MODEL`、invalid输出命名error；renderer不得把后两者转换为0。 |
| `JOURNAL-FORM-007` | `UT_PURE` | **GIVEN**versioned Journal/caller target catalogs及候选存在矩阵，**WHEN**分别执行 `restore_after_refresh`/`restore_to_caller`，**THEN**返回各自mounted set首个合法ID；无候选分别返回 `FOCUS_CONTRACT_ERROR`/`CALLER_FOCUS_UNAVAILABLE`，跨set target返回数为0。 |
| `JOURNAL-FORM-008` | `UT_PURE + INSTR` | **GIVEN**相同 snapshot/bundle/catalog/evidence/accumulator/focus inputs 与不同 external time、random、backend、filesystem 或 live-store fixtures，**WHEN**执行全部公式，**THEN**输出深值相等且 external read/write/hash count 为 0。 |

### Content and Presentation

| ID | Evidence | Criterion |
|---|---|---|
| `JOURNAL-UI-001` | `UT_ENGINE + A11Y` | **GIVEN**READY顶层bundle与0–4个category unavailable的完整矩阵，**WHEN**分别从主菜单与正常游戏菜单打开，**THEN**四入口exact tuple恒为`(chapter,memory,achievement,ending)`、首焦点恒为`chapter`、入口面积/层级/对比/装饰token exact-match`journal_equal_weight_template:v1`；激活坏区只进入对应CategoryUnavailable，4/4坏时ContentHandoff render count=0。 |
| `JOURNAL-UI-002` | `UT_ENGINE + VISUAL + A11Y` | **GIVEN**合法全空 root与批准empty-copy IDs，**WHEN**遍历四区，**THEN**每区interactive action exact tuple为`(section_back,journal_close)`、initial focus=`section_back`、row/locked/future/count/denominator surfaces均为0。 |
| `JOURNAL-UI-003` | `UT_ENGINE + VISUAL` | **GIVEN**7 memory、11 achievement 与6 ending 的最大合法 root，**WHEN**遍历四区，**THEN**章节7、回忆7、成就11、结局6项全部可达，无截断、抽样或分页。 |
| `JOURNAL-UI-004` | `STATIC + UT_ENGINE + A11Y` | **GIVEN**每类部分解锁 golden fixtures，**WHEN**capture render tree、interactive focus IDs、internal counts与self-voicing transcript，**THEN**visible rows/groups/headings exact-match已解锁catalog projection；locked row/slot/count/focus/spoken surface均为0。 |
| `JOURNAL-UI-005` | `UT_ENGINE + A11Y` | **GIVEN**0/1/11项成就及三组混合 fixtures，**WHEN**打开旅途记录，**THEN**只显示非空组，玩家组名exact为“场景回声/路线发现/后来留下的回声”，item rank exact-match catalog，unseen为低强调度“新记录”、seen为“曾经走过”，全量时“完整/全收集/真结局”命中数为0。 |
| `JOURNAL-UI-006` | `STATIC + VISUAL + A11Y` | **GIVEN**versioned screen-state/copy/fault-surface manifest，**WHEN**检查每个普通、空页、category unavailable、content handoff与recovery视觉/朗读输出，**THEN**actual `(actions,initial_focus,escape,right_click,reading_order,next_state)` exact-match冻结表；`0项`、`/7`、`/11`、`/6`、百分比、remaining、空槽、问号与“还差”命中数为0，content状态reset action/copy count为0。 |
| `JOURNAL-UI-007` | `UT_ENGINE` | **GIVEN**任一已解锁记录与ending journal-cause fixtures，**WHEN**打开详情，**THEN**rendered content IDs exact-match对应catalog；章节全文、backlog replay、成就条件、resolver matrix、higher-priority exclusion 与未到达内容调用数为0。 |
| `JOURNAL-UI-008` | `STATIC + UT_ENGINE` | **GIVEN**首发 Journal screens，**WHEN**枚举 actions，**THEN**search、filter、custom sort、claim、revoke、delete、reset、chapter replay 与 transcript replay action 数均为 0。 |
| `JOURNAL-UI-009` | `UT_ENGINE` | **GIVEN**结局 membership 按不同获得顺序产生但最终集合相同，**WHEN**打开结局分区，**THEN**显示顺序深值相等，不暴露获得顺序、resolver priority 或 ending ID。 |
| `JOURNAL-UI-010` | `VISUAL + A11Y + INSTR` | **GIVEN**六结局各自1/2/3 cause-card fixtures与同长度控制copy，**WHEN**capture列表/详情/achievement交叉入口，**THEN**row/card尺寸、色彩token、焦点样式、motion、audio-event count与文本层级exact-match同一等权模板；真/好/苦涩/悲剧专属庆祝、损坏、稀有度或完成态token命中数为0。 |

### Navigation and Lifecycle

| ID | Evidence | Criterion |
|---|---|---|
| `JOURNAL-NAV-001` | `UT_ENGINE + BRANCH` | **GIVEN**冻结的state×event transition manifest，**WHEN**对每条合法边各执行1案并对每条禁止边做negative案，**THEN**actual `(from,event,to,side_effect_trace)` exact-match manifest，所有状态均有入/出或明确终态，evaluator/resolver边数为0。 |
| `JOURNAL-NAV-002` | `UT_ENGINE + A11Y` | **GIVEN**主菜单caller target catalog的entry present/absent矩阵，**WHEN**经`Closing`关闭并mount caller，**THEN**`restore_to_caller`返回exact entry/fallback；关闭前caller focus调用数0、stale displayable count0。 |
| `JOURNAL-NAV-003` | `UT_ENGINE + INSTR` | **GIVEN**游戏菜单caller catalog与versioned navigation path manifest，**WHEN**逐路径关闭，**THEN**焦点exact恢复caller entry/fallback，叙事label、rollback state、save payload与persistent membership深值不变，Escape/right-click底层传播数0。 |
| `JOURNAL-NAV-004` | `UT_ENGINE + INSTR` | **GIVEN**四区不同`(top_visible_semantic_id,intra_row_offset)` anchors，**WHEN**同进程重入、load、rollback、menu-context重建与full restart，**THEN**仅同process-session controller重入恢复exact anchors；persistent/save/rollback/imported-cache字段与读取数均为0，full restart后为初始anchor。 |
| `JOURNAL-NAV-005` | `UT_ENGINE + A11Y` | **GIVEN**versioned focus/action manifest与mouse/keyboard-only模式，**WHEN**逐screen遍历每个interactive ID，**THEN**actual focus/activation tuple exact-match，focused ID在viewport内、fixed action rail可见，hover/timed/precision-pointer前置数为0。 |
| `JOURNAL-NAV-006` | `UT_ENGINE + A11Y` | **GIVEN**versioned `alt/group_alt` tree与expected transcript/action tuples，**WHEN**self-voicing遍历全部冻结screen states，**THEN**debug transcript exact-match，pending live status announcement count恰1，装饰/隐藏/internal字段/自动activation count均为0。 |
| `JOURNAL-NAV-007` | `UT_ENGINE + INSTR` | **GIVEN**冻结global-gate enum在Closed与每个open state激活，**WHEN**触发菜单/快捷键/direct action或动态revocation，**THEN**Closed时open count0；open时非阻断modal deferred至Closed，blocking recovery抢占一次并清controller，底层action与旁路count均为0。 |
| `JOURNAL-NAV-008` | `UT_ENGINE + A11Y` | **GIVEN**refresh前exact semantic page/focus/scroll anchor与新增/删除fixtures及copy ID `journal_content_changed_notice`，**WHEN**原子替换，**THEN**仍合法的page/focus/anchor深值相等；失效详情返回section_back并使该notice可见/朗读各恰1，同一replacement重复announcement=0；auto-open/auto-focus-to-new/auto-scroll-to-new count均为0。 |
| `JOURNAL-NAV-009` | `UT_ENGINE + INSTR` | **GIVEN**SYS-SAVE `journal_menu_gate:v1` 与主/游戏菜单 caller focus catalogs，**WHEN**覆盖PlayableStable、CriticalInteraction、LoadedUnvalidated、BlockingSafeFlow及动态recovery抢占，**THEN**仅主菜单和PlayableStable游戏菜单可打开；关闭分别恢复exact caller entry/fallback，后三类open count=0，recovery抢占后caller restore=0，save/rollback/persistent深值不变。 |

### Mark-Seen, Merge, and Recovery

| ID | Evidence | Criterion |
|---|---|---|
| `JOURNAL-PERSIST-001` | `UT_ENGINE + INSTR` | **GIVEN**v1 evidence累计A、refresh新增但未产生evidence的B及离开分区，**WHEN**Journal caller提交 acknowledgement，**THEN**adapter call恰1、payload exact `(A)`、checkpoint exact `journal_seen_ack`、requester由adapter注入、unlock/settings为空；`APPLIED_FLUSHED`时replacement=1/flush=1，`DUPLICATE_NOOP`时二者=0。 |
| `JOURNAL-PERSIST-002` | `UT_ENGINE + A11Y` | **GIVEN**mark-seen durable success，**WHEN**保持当前 Journal 打开并随后重新打开，**THEN**本次 `journal open cycle` 仍显示“新记录”，下一次显示“曾经走过”，membership 深值不变。 |
| `JOURNAL-PERSIST-003` | `UT_ENGINE + INSTR` | **GIVEN**SYS-PERSIST冻结的每个safe-prewrite injection phase，**WHEN**mark-seen返回`PERSIST_FLUSH_FAILED_SAFE`，**THEN**root-on-disk与pre-request snapshot深值相等、当前/下次仍为“新记录”、success/audio count0、原pending intent执行恰1、下一次真实呈现并离开允许重试。 |
| `JOURNAL-PERSIST-004` | `UT_ENGINE + INSTR` | **GIVEN**duplicate/no-op acknowledgement，**WHEN**返回结果，**THEN**不显示提示、不播放声音、不重复写入；下次打开只按权威 snapshot 分类。 |
| `JOURNAL-PERSIST-005` | `UT_ENGINE + BRANCH` | **GIVEN**mark-seen commit status unknown，**WHEN**结果到达，**THEN**普通 Journal 原子关闭并进入 blocking recovery；后续导航、refresh、write 与 success feedback count 均为 0。 |
| `JOURNAL-PERSIST-006` | `UT_ENGINE + INSTR` | **GIVEN**Journal任一页面期间收到deep-equal、single-changed与N个coalesced合法merge，**WHEN**controller refresh，**THEN**deep-equal的build/replacement/restart均0；changed/coalesced各build=1、replacement=1、restart=1；callback内UI call0、半更新frame0。 |
| `JOURNAL-PERSIST-007` | `UT_ENGINE + A11Y` | **GIVEN**refresh 前焦点 item 分别继续存在或消失，**WHEN**替换模型，**THEN**前者保持相同 semantic ID，后者聚焦分区返回；stale/offscreen focus count为0。 |
| `JOURNAL-PERSIST-008` | `UT_ENGINE + BRANCH` | **GIVEN**冻结finite event-bitmask matrix，分别覆盖accumulator empty/nonempty、ack每个终态（含REJECTED_REENTRANT）、refresh flag、user intent、content fault、reset与recovery，**WHEN**调度，**THEN**每案actual `(handled,cancelled,accumulator_ids,refresh_required,pending_intent,to_state)` exact-match expected tuple；reentrant清accumulator并执行intent、不等待事件，低优先级越界count0。 |
| `JOURNAL-PERSIST-009` | `UT_ENGINE + INSTR` | **GIVEN**collection reset或epoch change在每个open/pending state开始，**WHEN**状态到达，**THEN**旧read model、session-new IDs、bounded accumulator、未消费evidence、scroll/focus caches与pending intent清除各恰1，普通collection UI与旧async callback可达数0。 |
| `JOURNAL-PERSIST-010` | `UT_ENGINE + VISUAL + A11Y` | **GIVEN**invalid root/persistence unavailable/commit-unknown/reset、bundle invalid、1–4 category invalid fixtures，**WHEN**处理，**THEN**前组exact进入`PersistenceRecoveryHandoff`、bundle进入`ContentHandoff`、任意1–4坏区仍进入`Contents`且坏区分别为`CategoryUnavailable(k)`；4/4坏时首焦点chapter、ContentHandoff count0，content状态reset action/copy count0，所有不可用状态“0项”与旁路count0。 |

### Visual, Accessibility, Performance, and Build

| ID | Evidence | Criterion |
|---|---|---|
| `JOURNAL-A11Y-001` | `VISUAL + A11Y` | **GIVEN**冻结的screen×1280×720/1920×1080×font1.0/1.25/1.5×contrast×motion×0/max/longest-copy manifest，**WHEN**capture每个case，**THEN**glyph intersection/clipping均0，required action IDs全部位于viewport外fixed rail且可见，focus outline与背景对比达到SYS-ACCESS批准阈值。 |
| `JOURNAL-A11Y-002` | `STATIC + A11Y` | **GIVEN**每个状态的semantic-token manifest及静音/self-voicing/high-contrast/reduced-motion variants，**WHEN**删除颜色、声音、动画、位置或hover任一单通道，**THEN**visible+spoken semantic token tuple与enabled action tuple保持exact相等。 |
| `JOURNAL-A11Y-003` | `UT_ENGINE + A11Y` | **GIVEN**批准的最长UTF-8/grapheme copy fixture与font1.5，**WHEN**keyboard/self-voicing遍历，**THEN**每个copy ID在render/transcript各出现恰1、每个row与正文末端可达、fixed return/close始终可达，truncation/timed-dismiss count0。 |
| `JOURNAL-PERF-001` | `BENCH + UT_ENGINE` | **GIVEN**SYS-TEST冻结的最低硬件/build/timer/GC/quantile manifest、5 warm-up与≥30 samples，**WHEN**测量普通交互帧和同步mark-seen wait，**THEN**普通帧p95≤16.6ms/max≤33.2ms；pending frame与result→interactive frame max≤33.2ms；flush wait p95≤250ms/max≤500ms；保留全部raw samples。 |
| `JOURNAL-PERF-002` | `BENCH + INSTR` | **GIVEN**SYS-TEST冻结的process/build、allocator、GC enabled mode、pre-open baseline、measurement boundaries与raw-sample protocol，以及31 records、18 cause cards、11 unseen、1000次重复/changed evidence-refresh churn、最长copy和720p/font1.5/self-voicing manifest，**WHEN**分别从controller transaction start计pure build、从open action dispatch到首个interactive frame计first-present、从refresh consume到restored interactive frame计refresh+focus并以post-close GC后baseline计算retained/peak，**THEN**build p95≤2ms/max≤5ms；first-present p95≤33.2ms/max≤50ms；refresh+focus p95≤16.6ms/max≤33.2ms；accumulator IDs≤11、raw evidence retained=0、retained≤4MiB、peak allocation≤8MiB；runtime filesystem/network/hash count0。 |
| `JOURNAL-PERF-003` | `BENCH + INSTR` | **GIVEN**一个READY模型，**WHEN**执行1000次idle/redraw、全列表键盘滚动与一次self-voicing traversal，**THEN**snapshot read、catalog validation/hash、read-model build及external I/O count均0，并报告allocated bytes、GC count与pause samples。 |
| `JOURNAL-BUILD-001` | `STATIC` | **GIVEN**versioned release source/callgraph/asset allowlist，**WHEN**扫描全部manifest entries，**THEN**direct persistent/backend write、live-state inference、resolver/evaluator call、chapter replay、hidden-score copy、network、telemetry及allowlist外asset reference count均为0。 |
| `JOURNAL-BUILD-002` | `STATIC + UT_ENGINE` | **GIVEN**四个owner-signed source catalogs、SYS-JOURNAL assembler contract、release candidate与`journal_catalog_bundle:v1` golden manifest，**WHEN**由SYS-BUILD执行assembler并验证generation/source hashes/archive closure，**THEN**五项generation常量与四项full SHA-256 exact-match；source copy/ID/rank rewrite=0；production `renpy_interaction_probe:v1` source hash/allowlist exact-match，而test evidence forger、spy、fault injector、debug ID与runtime source scanner均未入包；same-generation/different-hash fixture固定失败。 |
| `JOURNAL-BUILD-003` | `STATIC` | **GIVEN**SYS-JOURNAL evidence bundle，**WHEN**汇总 acceptance IDs，**THEN**每个 ID 唯一且映射到含fixture/assertion、source/catalog hash、runner/environment、raw output与exit code 0的PASS artifact；空壳PASS、stale hash或缺失证据失败。 |

### Audio Ownership and Suppression

| ID | Evidence | Criterion |
|---|---|---|
| `JOURNAL-AUDIO-001` | `UT_ENGINE + INSTR` | **GIVEN**0/1/N unseen、achievement modal→Journal、同notification group跨kind与重复打开fixtures，**WHEN**呈现/mark-seen，**THEN**Journal unseen/new-record/seen-only audio event count0；完整notification group的SFX只由SYS-AUDIO owner触发且每group≤1；普通导航声不携带group/unseen dedupe key。 |
| `JOURNAL-AUDIO-002` | `UT_ENGINE + A11Y` | **GIVEN**mute、self-voicing在打开前/播放中切换、merge/refresh/reset/commit-unknown与recovery接管，**WHEN**执行全部路径，**THEN**mute或self-voicing时Journal dispatch/play count0；已有实例在切换/recovery时stop count恰1；success/alert-only audio count0。 |
| `JOURNAL-AUDIO-003` | `STATIC + INSTR` | **GIVEN**六结局row/detail与1–3 cause cards，**WHEN**逐一浏览，**THEN**outcome/rarity/victory SFX event count均0，普通navigation event ID/parameters/count在六结局间exact相等。 |

*本验收矩阵已按 2026-08-04 re-review revision 重写；所有 manifest、fixture 与阈值必须随实现证据冻结版本和 source hash。*

## Open Questions

| ID | Open Question | Owner | Target Resolution | Closure Evidence |
|---|---|---|---|---|
| `JOURNAL-Q1` | 六个 ending 各自 1–3 个 `journal_cause_ids` 的最终摘要是什么，如何证明它们对该 ending 全部 terminal equivalence classes 都成立而不伪装成逐 traversal 原因？ | SYS-ENDING + SYS-NARRATIVE + Localization / Andwey | Ending/Journal content lock 前 | `journal_ending_catalog:v1` records、全class intersection report、spoiler/等级暗示审查、六结局parity captures |
| `JOURNAL-Q2` | Day 1–7 的章节概览与回忆片段具体文案如何在共享同一 `memory_id` 时保持不同，并逐条证明只含全部合法 completed paths 的共同事实？ | SYS-NARRATIVE + UX + Localization / Andwey | Narrative content lock 前；日期由内容 sprint 固定 | 7×2 玩家安全文案、逐日all-path intersection report、`common_path_truth_approval_id`、逐ID差异/spoiler审查、冻结盲测rubric |
| `JOURNAL-Q3` | 首页说明、四区说明、合法空页、“正在整理手册……”及三类不可用 surface 的最终简体中文文案是什么？ | UX + SYS-ACCESS + Localization / Andwey | `/ux-design` 批准前 | Copy catalog、最大字体 captures、self-voicing transcripts、spoiler/technical-language scan、content surface reset-language count=0 |
| `JOURNAL-Q4` | 在本 GDD 已冻结三故障域的 exact action/focus/escape/transition manifest 后，各 surface 的最终布局、非技术化文案与高对比表现是什么？ | SYS-PERSIST + SYS-ACCESS + UX | UI stories Ready 前 | Three-surface wireframes/copy catalog、branch manifest exact-match、no-reset-from-content tests、focus/reading-order evidence |
| `JOURNAL-Q6` | 首页、四区、详情、空页、pending 和 recovery 的 exact focus graph、viewport、长文换行与响应式布局是什么？ | SYS-ACCESS + UX / Andwey | UI epics 前 | 720p/1080p wireframes、三档字体矩阵、keyboard walk、self-voicing transcript、0/max content captures |
| `JOURNAL-Q7` | 纸张、雨痕、票据、字体、焦点样式和高对比度变体的最终 Art Bible 规范是什么？ | Art Director / Andwey | 正式资产制作前 | Approved Art Bible、色板/纹理/字体规范、high-contrast variants、asset source policy |
| `JOURNAL-Q8` | 是否制作普通 Journal 纸页/印章导航声；若制作，其 event owner/dedupe/cancel policy、文件、许可、hash、响度、格式和 self-voicing suppress matrix 是什么？ | SYS-AUDIO + Audio Director | Audio acceptance 前 | Versioned audio-event catalog、license records、asset manifest、muted/self-voicing/recovery captures |
| `JOURNAL-Q9` | Ren’Py 8.5.3 的 focus、viewport、self-voicing、persistent callback 与 interaction restart API 是否满足本状态机？ | Engine Programmer + UI Programmer + SYS-TEST | Architecture implementation-ready 前 | 官方 API verification、small engine spike、failure matrix、version-pinned ADR |
| `JOURNAL-Q10` | 最低参考硬件上最大 read model、first present、atomic refresh 和 focus restore 的实际时间与内存是多少？ | SYS-TEST + Performance Analyst | Performance acceptance 前 | Frozen hardware/build/timer/GC manifest、5 warm-up + ≥30 raw samples、p95/max report |
| `JOURNAL-Q11` | 真实7×2文案能否通过已冻结的章节/回忆理解门槛，并且不把 Journal 视为评分或攻略清单？ | UX + Playtest + Producer / Andwey | Closed vertical slice content lock 前 | 预注册≥8人盲测；两项理解各≥7/8、双收藏/完成率误解≤1/8；原始回答、失败样本及修订/合并决定 |

所有具体日历日期均由对应 sprint plan 固定；本 GDD 先冻结每项必须在哪个 production gate 前关闭，避免臆造尚未批准的排期。

**Resolved in 2026-08-04 revision:** `JOURNAL-Q12` 的设计接口已由 SYS-SAVE amendment 冻结为 `journal_menu_gate:v1`、`journal_caller_focus_catalog:v1`、blocking-load exclusion 与四项 integration AC；具体 wireframe capture 仍属于 Main/game-menu UX evidence，不再是开放设计问题。
