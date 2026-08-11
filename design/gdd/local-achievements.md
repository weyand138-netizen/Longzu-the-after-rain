# 11 项本地成就

> **System ID**: SYS-ACHIEVE
> **Status**: Approved
> **Author**: Andwey + Codex
> **Last Updated**: 2026-08-04
> **Implements Pillar**: 看见未说出口的话；温柔必须被挣来；悲剧也是完整答案
> **Producer Decisions**: 2026-07-30 — 采用 11 项独立成就；6 个结局与 7 个章节由各自 ending/memory 收藏记录，不再镜像为成就；通知保持 session-only，跨会话发现由 `seen_achievement_ids` 提供
> **Review Disposition**: 2026-07-30 — 初审为 MAJOR REVISION NEEDED；完成 v2 修订后，制作人选择接受修订、豁免独立复审并批准本设计。批准不关闭 backend、content callsite、UI/audio 或 performance implementation gates
> **Catalog Generation**: `achievement_catalog:v2`
> **Journal Contract Amendment**: 2026-08-03 — split modal/Journal mark-seen callers；player-visible third group renamed；completion copy removed；IDs、conditions与internal group keys unchanged

## Overview

SYS-ACHIEVE 负责 11 项独立本地成就。它只消费 SYS-NARRATIVE 在已批准稳定完成点输出的具体 completed events，不读取五轴、choice history、counterevidence token、route qualification、资源、ending predicate 或 resolver record。六个结局和七个章节已由 SYS-PERSIST 的 `ending_ids`、`memory_ids` 记录，不再重复进入成就目录；成就只保留需要具体观察、回应、回收或路线发现才能发生的独立经历。

成就记录的是玩家**曾完整走到过的可能性**，不是 rollback 后当前时间线仍然成立的事实。合法解锁跨周目保留；modal 只在当前 session 的安全边界出现，若因 load、rollback、退出或 recovery 丢弃，愿望手册仍通过持久化的“新记录”状态让玩家在以后发现它。

## Player Fantasy

玩家应在场景重新安静之后，感到某个具体经历被游戏轻轻记住，而不是看到一张正确行为清单。成就名称因此使用物件、代价或场景结果，不使用“先问她”“正确选择”“最佳路线”一类品格判断。未获得项目完全不渲染，也不显示总数、槽位或缺失步骤；只有玩家真正获得记录后，它才进入愿望手册。

悲剧、苦涩、好结局和真结局由 ending 收藏等价记录，不通过成就的可见性、音效、边框或数量制造等级。Rollback 后保留的条目在愿望手册中解释为“曾经走过”，不声称它属于当前恢复后的故事时间线。

## Detailed Design

### Core Rules

1. SYS-ACHIEVE 拥有且只拥有 11 项 `achievement_condition_record`。字段固定为：`achievement_id`、非空 `condition_event_ids`、`condition_operator`、`zero_delta_witness_path_ids`、`non_best_ending_witness_path_ids`、`reveal_policy`、`display_order_group`、`owner_system`。
2. `condition_operator` 首发固定为 `all`；`reveal_policy` 固定为 `ON_UNLOCK`；`owner_system` 固定为 `SYS-ACHIEVE`。不支持未使用且语义含混的 `any`。
3. `condition_event_ids` 按因果顺序排列，最后一项是唯一 canonical completion event。每项 completion event 必须映射到恰一个稳定 checkpoint。
4. 六个 ending IDs 与七个 memory IDs 不属于成就 ID 集；SYS-PERSIST 不从 ending/memory membership 推导成就。
5. 条件输入只能来自 versioned `achievement_evidence_snapshot`。Snapshot 字段固定为：`catalog_generation_id`、`collection_epoch_id`、`checkpoint_occurrence_id`、`checkpoint_id`、`completed_event_ids`、`newly_completed_event_ids`、`stable_completion_boundary`。
6. `collection_epoch_id` 来自 canonical SYS-PERSIST root。显式 New Game 把当前 epoch 复制到 rollback-owned run envelope；旧 save 保留旧 epoch。Snapshot epoch 与 root 不一致时，成就求值固定拒绝，直到玩家开始使用当前 epoch 的新 traversal。
7. `checkpoint_occurrence_id` 在同一 run envelope 中唯一并随 rollback 恢复。同一 occurrence 只能由 persistence checkpoint coordinator 接受一次；并发或重入请求不得静默丢失同 checkpoint 的其他 kind。
8. Snapshot 必须先整体验证一次，再把累计事件派生为一次只读 set view，随后固定扫描 11 条记录。不得为每条成就重复验证 snapshot 或重复构造 set。
9. 只有条件完整为真、最后事件属于本 checkpoint 的新增事件、membership 尚未包含 ID 时，才向 SYS-PERSIST 的专用 achievement adapter 提交 candidate。SYS-ACHIEVE 不构造或填写 requester identity。
10. SYS-PERSIST adapter 返回 exact durable-result record：`status`、`checkpoint_occurrence_id`、`collection_epoch_id`、`added_achievement_ids`、`existing_achievement_ids`、`notification_group_id`。只有 `status=APPLIED_FLUSHED` 且 `added_achievement_ids` 非空时可产生展示资格。
11. Existing-membership duplicate 在 evaluator 层产生 0 个 candidate；直接对 SYS-PERSIST adapter 提交一个已存在 ID 才测试 `DUPLICATE_NOOP`。Raw batch 内重复 `(unlock_kind,stable_id)` 则是 `REJECTED_INVALID`。
12. 成就 modal 不持久化、不跨 session 重播。Load、rollback、blocking exit、commit-unknown、reset recovery 或进程退出会清除全部待展示 group、timer 与音频 token，但不会把新 ID 加入 `seen_achievement_ids`。
13. `seen_achievement_ids` 是 `achievement_ids` 的 canonical subset。自动成就 modal 关闭后由 SYS-ACHIEVE caller 调用 SYS-PERSIST 专用 mark-seen adapter；愿望手册的实际呈现凭据由 SYS-JOURNAL caller在玩家离开旅途记录分区时调用同一专用 adapter。两类 caller 都不能自由填写 requester/checkpoint，SYS-PERSIST 以 canonical root 幂等收敛；失败时条目仍保持“新记录”，不会丢 membership。
14. Collection reset 递增 `collection_epoch_id`，清空 achievement/ending/memory memberships、`seen_achievement_ids` 与 backend progress，保留 settings，并要求显式 New Game 后才重新启用成就求值。
15. 玩家不能手动领取、撤销、刷新或输入成就 ID。成就、seen 状态与 backend membership 都不能成为剧情、选择、路线或结局的输入。

### Approved 11-Item Catalog

所有 locked 项均不渲染；表中顺序是通知与愿望手册的批准顺序。

| Achievement ID | 批准名称 | `condition_event_ids` | Required witness | Group |
|---|---|---|---|---|
| `CHOICE_READ_THE_NOTE` | 被雨打湿的愿望 | (`event_achievement_read_note_recovered`) | `witness_achievement_read_note_zero_delta` | `01_scene_echoes` |
| `CHOICE_ASK_FIRST` | 多绕一小时 | (`event_achievement_ask_first_answer_honored`) | `witness_achievement_ask_first_accept_cost` | `01_scene_echoes` |
| `CHOICE_ACCEPT_NO` | 换一条安全的路 | (`event_achievement_refusal_honored`) | `witness_achievement_accept_no_nonbest` | `01_scene_echoes` |
| `CHOICE_SHARE_TRUTH` | 摊开的家族档案 | (`event_full_archive_shared`, `event_erii_selects_route_response`) | `witness_achievement_share_truth_answer_expressed` | `01_scene_echoes` |
| `CHOICE_KEEP_PROMISE` | 烧掉的旧身份 | (`event_shared_cost_promised`, `event_prior_cost_promise_honored_without_shift`) | `witness_achievement_direct_cost_honored` | `01_scene_echoes` |
| `ROUTE_ARCADE_ALIAS` | 屏幕上的另一个名字 | (`event_erii_enters_alias`) | `witness_route_arcade_alias_expressed` | `02_route_discoveries` |
| `ROUTE_EMPTY_SCHOOL` | 没有学生的教室 | (`event_empty_school_trace_confirmed`) | `witness_route_empty_school_trace` | `02_route_discoveries` |
| `ROUTE_SEASIDE_TICKET` | 两张靠窗的票 | (`event_two_window_tickets_acquired`) | `witness_route_two_window_tickets` | `02_route_discoveries` |
| `ROUTE_BACKUP_EXIT` | 封条后的出口 | (`event_service_exit_used`) | `witness_route_service_exit_used` | `02_route_discoveries` |
| `EPILOGUE_FIRST_GUEST` | 今天的第一位客人 | (`event_epilogue_first_guest_completed`) | `witness_epilogue_first_guest` | `03_true_epilogue` |
| `EPILOGUE_LIGHTS_OUT` | 关灯，回家 | (`event_epilogue_lights_out_completed`) | `witness_epilogue_lights_out` | `03_true_epilogue` |

Group keys 是内部兼容 identity，不进入 render/self-voicing。玩家可见映射固定为 `01_scene_echoes → 场景回声`、`02_route_discoveries → 路线发现`、`03_true_epilogue → 后来留下的回声`；最后一项不得渲染为“真结局尾声”、终极组或完成组。

### Completion Event and Checkpoint Contract

| Completion event | Exact semantic boundary | Checkpoint |
|---|---|---|
| `event_achievement_read_note_recovered` | 零轴路径中由绘梨衣保住愿望纸，且 Day 6 的正式回收 `payoff_prologue_hurry_day6` 已完整演出 | `cp_day6_note_recovery_complete` |
| `event_achievement_ask_first_answer_honored` | `prologue_ask_destination` 后接受小站回答，并让一小时绕行的可感知后果完整结束 | `cp_prologue_small_station_detour_complete` |
| `event_achievement_refusal_honored` | `event_erii_rejects_shifted_cost_again` 后选择 `day6_take_cost_back`，`outcome_cost_returned_to_lu` 已可感知；不得由 override 或无安全替代路径产生 | `cp_day6_cost_reconsideration_complete` |
| `event_erii_selects_route_response` | 完整档案已交付，绘梨衣的 registered answer 已通过动作/物件完整表达；该成就不声明玩家随后尊重了回答 | `cp_day5_route_answer_expressed` |
| `event_prior_cost_promise_honored_without_shift` | 先前存在 `event_shared_cost_promised`，Day 6 直接选择 `day6_burn_old_identity`；路径中未发生 `day6_shift_cost_to_erii` | `cp_day6_direct_cost_complete` |
| `event_erii_enters_alias` | 绘梨衣完成输入自己的 alias，动作与屏幕结果均已呈现；不评价玩家随后的 accepting/overriding response | `cp_day2_alias_answer_expressed` |
| `event_empty_school_trace_confirmed` | 空教室 trace 经过交叉验证并向玩家呈现确认结果 | `cp_day3_empty_school_trace_complete` |
| `event_two_window_tickets_acquired` | 两张实名靠窗票已交到绘梨衣手中，身份暴露代价已呈现 | `cp_day4_two_tickets_complete` |
| `event_service_exit_used` | 已准备的维修通道实际启用并离开封锁区 | `cp_day6_service_exit_complete` |
| `event_epilogue_first_guest_completed` | 真结局尾声“第一位客人”的可玩事件完整结束 | `cp_epilogue_first_guest_complete` |
| `event_epilogue_lights_out_completed` | 真结局尾声“关灯回家”的可玩事件完整结束 | `cp_epilogue_lights_out_complete` |

`event_full_archive_shared` 是 `CHOICE_SHARE_TRUTH` 的前置事实，不是 completion event；它在完整原始档案交付完成后产生。所有 11 个 completion events 与 checkpoints 属于 `achievement_event_catalog:v2`，缺失、重复或 source callsite 不受对应责任 scene 支配时构建失败。

### States and Transitions

| State | Trigger | Result |
|---|---|---|
| `Observing` | 无稳定 completed-event snapshot | 不判定、不写入、不展示 |
| `SnapshotValidation` | 收到 snapshot | 一次验证 schema、generation、epoch、occurrence、事件顺序和 checkpoint |
| `ConditionEvaluation` | Snapshot 合法 | 一次 set 派生后扫描 11 条冻结记录 |
| `NoChange` | 无首次满足项 | 不调用 SYS-PERSIST，返回 `Observing` |
| `BatchSubmitted` | 存在 candidate | 交给唯一 persistence checkpoint coordinator |
| `PresentationDeferred` | durable result 有新增，但当前 boundary 不安全 | 按 arrival sequence 追加 session-only group |
| `PresentationReady` | 达到 authored safe boundary | 合并全部 pending groups，按批准 display rank 去重并显示一个 modal |
| `Presented` | 玩家关闭 | 清 modal/queue/timer/audio token；异步提交 exact mark-seen IDs |
| `PersistenceBlocked` | unavailable、commit-unknown 或 recovery | 原子清 queue/timer/modal；转交 SYS-PERSIST blocking flow |

多个 deferred groups 的合并规则固定为 append by arrival sequence、achievement ID 去重、最终按批准 catalog rank展示。容量上限为 11 个 ID；同一 stable scene 最多一个 modal和一次通知音。Merge、projection repair、load、rollback、reset 与 duplicate 不创建 group。

## Formulas

### Catalog Validity

`achievement_catalog_valid(C) = exact_schema(C) ∧ len(C)=11 ∧ ids(C)=approved_ids_v2 ∧ ids_unique(C) ∧ all_nonempty(C) ∧ all_operators_all(C) ∧ all_reveal_on_unlock(C) ∧ references_resolve_once(C) ∧ completion_events_unique(C) ∧ display_order_exact(C)`

### Snapshot Validity

`achievement_snapshot_valid(S,R,I) = exact_snapshot_schema(S) ∧ S.catalog_generation_id=current_catalog_generation ∧ S.collection_epoch_id=R.collection_epoch_id ∧ S.stable_completion_boundary=True ∧ occurrence_id_valid_and_unclaimed(S.checkpoint_occurrence_id) ∧ canonical_unique_event_tuple(S.completed_event_ids) ∧ canonical_unique_event_tuple(S.newly_completed_event_ids) ∧ S.newly_completed_event_ids=tail(S.completed_event_ids,len(S.newly_completed_event_ids)) ∧ every_new_event_maps_to(S.checkpoint_id,I)`

空 `newly_completed_event_ids` 可以形成合法 NoChange snapshot，但不会进入条件扫描。

### Condition Satisfaction

`achievement_condition_satisfied(r,E_set) = all(e in E_set for e in r.condition_event_ids)`

### Grant Eligibility

`achievement_grant_eligible_now(r,S,E_set,P) = achievement_condition_satisfied(r,E_set) ∧ last(r.condition_event_ids) in S.newly_completed_event_ids ∧ r.achievement_id not in P`

Snapshot validity 不在该函数中重复调用；调用方只在一次验证通过后调用它。

### New Achievement IDs

`new_achievement_ids(C,S,P) = UTF8Sort(tuple(r.achievement_id for r in C if achievement_grant_eligible_now(r,S,E_set,P)))`

Production 最大值由冻结 event→checkpoint 图计算为 `max_reachable_eligible_per_checkpoint`；纯排序 helper 可使用 synthetic 11-item fixture，但不得伪装成合法 production snapshot。

### Candidate Construction

`achievement_candidates = tuple((id,completion_event(id),checkpoint_of(completion_event(id))) for id in new_achievement_ids)`

Tuple 保持 `new_achievement_ids` 的 UTF-8 stable-ID 顺序。SYS-PERSIST 专用 adapter 注入 `unlock_kind` 与 requester identity，并在跨 kind batch 中按 `(unlock_kind UTF8,stable_id UTF8)` 排序。

### Unseen Achievement IDs

`unseen_achievement_ids(R) = DisplayOrder(tuple(id for id in R.achievement_ids if id not in R.seen_achievement_ids))`

`seen_achievement_ids ⊆ achievement_ids` 是 root invariant。Popup 关闭或 Journal 成功呈现后只增加 seen IDs，不删除 membership。

### Presentation Decision

`achievement_presentation_decision(D,s) = PRESENT(DisplayOrder(D.added_achievement_ids))` 当 `D.status=APPLIED_FLUSHED`、新增非空且 boundary safe；boundary unsafe 时为 `DEFER(...)`；其他情况为 `NO_PRESENTATION`。

## Edge Cases

### Catalog and Snapshot Integrity

- **If catalog 不是恰好 11 项、含 ending/memory mirror、未知 event/witness/checkpoint 或非 `all` operator**：整体拒绝。
- **If snapshot epoch 与 root 不同**：不求值、不提交；旧 save 可以继续剧情，但成就功能保持不可用，直到显式 New Game。
- **If completed/new tuples 含 wrong type、未知、重复、乱序，或 new tuple 不是 cumulative tuple 的 canonical tail**：整体拒绝。
- **If occurrence 已被 coordinator 接受或正处于 in-flight**：相同 payload 返回已知处理状态；不同 payload 固定阻断并进入开发诊断，不丢弃其他 kind。
- **If snapshot 合法但 new tuple 为空**：返回 NoChange，validation count 为 1、condition scan count 为 0。

### Condition Semantics

- **If `CHOICE_SHARE_TRUTH` 后玩家覆盖绘梨衣回答**：成就仍可成立，因为它只见证完整真相交付和回答被表达；copy 不得宣称回答被尊重。
- **If 玩家先转嫁代价再 `day6_take_cost_back`**：可获得“换一条安全的路”，但不能获得“烧掉的旧身份”。
- **If 玩家直接 `day6_burn_old_identity` 但没有早期 promise**：不能获得“烧掉的旧身份”。
- **If composite condition 的最后 event 新完成但前置 event 缺失**：不授予，也不缓存部分成就进度。

### Persistence, Rollback, Reset, and Merge

- **If membership 已含 ID**：evaluator 产生 0 candidate、SYS-PERSIST call count 为 0、popup/audio 为 0。
- **If direct adapter fixture 提交已存在 ID**：返回 `DUPLICATE_NOOP`；这不等于 raw batch duplicate。
- **If raw batch 内 `(kind,id)` 重复**：整批 `REJECTED_INVALID`。
- **If rollback 到 completion 前再前进**：membership 保留；当前时间线证据回退；再次抵达时 evaluator 因 membership 产生 0 candidate。
- **If collection reset 完成**：epoch 递增，所有旧 run/save snapshot epoch 失配；只有显式 New Game 的新 run envelope可重新获得。
- **If external merge 含不同 epoch roots**：只保留最大 epoch 的 roots参与 membership/seen union；低 epoch 数据不得复活。最大 epoch 相同的 sources 对 memberships 与 seen 分别取 canonical union。
- **If mark-seen flush 失败**：membership 不变；条目继续显示“新记录”，不得撤销已显示内容。

### Presentation and Accessibility

- **If 多个 checkpoint 在 unsafe 区间完成**：全部 group 合并为下一安全边界的一个 modal，不连续弹多个窗口。
- **If modal 前发生 load、rollback、exit 或 recovery**：session queue 丢弃；unseen 状态保留，Journal 下次标记新记录。
- **If modal 已打开时发生 blocking recovery**：原子停止通知音、取消 timer、关闭 modal并把焦点移交 recovery safe action。
- **If self-voicing active**：通知音固定 suppress；标题、列表和“继续”按顺序朗读。
- **If内容超过一屏**：固定使用 viewport 滚动，不使用分页。方向键、PageUp/PageDown、鼠标滚轮可滚动；“继续”常驻 viewport 外固定操作区。

## Dependencies

| Dependency | Required contract | Status / Gate |
|---|---|---|
| Ren’Py 8.5.3 | achievement backend、screen/keymap、persistent 与 reset engine fixtures | Pinned；backend/durability/reset 行为仍需 engine evidence |
| ADR-0002 + Architecture + Control Manifest | 单一 SYS-PERSIST root、强制 flush-before-projection、epoch/seen leaves、session presentation boundary | 本版要求同步 amendment |
| Approved achievement catalog | 11 IDs、名称、三组顺序、全部 ON_UNLOCK | v2 catalog 与本 GDD同步 |
| SYS-PERSIST | epoch、seen subset、candidate/mark-seen adapters、durable-result record、merge/reset/recovery | GDD需同步并 re-review |
| SYS-NARRATIVE | `achievement_event_catalog:v2`、snapshot与11个 checkpoint callsites | baseline/GDD需同步并 re-review |
| SYS-STATE / SYS-SAVE | New Game 复制当前 epoch；旧 save 保留旧 epoch；load/rollback action gates | 联合 contract需同步 |
| SYS-JOURNAL | detached achievement/seen snapshot、版本化呈现receipt、入口/返回/focus/scroll | GDD In Revision；2026-08-03 full-review修订合同阻止完整UI acceptance，待re-review |
| SYS-ACCESS | keyboard、self-voicing、high contrast、font scale、reduced motion | GDD Designed（完整复审待完成）；五项项目设置、语义摘要与可访问记录合同已冻结，实装证据仍阻止完整 UI acceptance |
| SYS-AUDIO | 唯一 notification-group SFX owner；self-voicing 时 suppress | GDD Not Started；阻止 audio acceptance |
| SYS-TEST | catalog golden vectors、epoch/reset/merge、queue、backend与UI evidence | GDD Not Started；阻止 implementation acceptance |

### Interface Boundaries

- SYS-NARRATIVE 构造 snapshot；SYS-ACHIEVE 只验证并消费。
- SYS-ACHIEVE 输出 candidate 参数；SYS-PERSIST adapter 构造 request、注入 requester并返回 durable-result record。
- SYS-PERSIST 是 membership、epoch 与 seen 的唯一 writer；SYS-ACHIEVE 与 SYS-JOURNAL 消费 detached snapshot，并分别只能经冻结 caller 的专用 mark-seen adapter 请求增加 seen IDs。
- SYS-PERSIST notification coordinator 生成唯一 group；SYS-ACHIEVE presenter只呈现其中 achievement entries，SYS-AUDIO只对完整 group调用一次。
- SYS-JOURNAL 打开时使用 stable item ID 保持焦点；unavailable/recovery 原子替换正常列表，不返回 stale screen。

## Tuning Knobs

| Knob | Type | Target | Safe Range | Rule |
|---|---|---:|---:|---|
| `presentation_settle_delay_ms` | exact int | `500` | `0–1000` | 只在 authored safe boundary 后开始；interaction restart 不得重置 |
| `notification_transition_ms` | exact int | `200` | `0–300` | reduced-motion 时 effective value 为 `0` |

以下不是调节项：11 项总数、ID、名称、条件、ON_UNLOCK、三组顺序、epoch/seen 语义、一次 snapshot validation、session-only modal、跨会话新记录、合成通知和不自动关闭。

## Visual/Audio Requirements

- 视觉语言采用纸页、票据、印记与雨后余光，不使用奖杯、星级、稀有度、五色轴图标或进度环。
- 所有未解锁项完全不存在；已解锁条目使用“曾经走过”，未 seen 条目追加非颜色的“新记录”状态。
- 达到 authored safe boundary 后等待 500 ms；modal 使用 200 ms 轻微淡入/上移，reduced-motion 为 0 ms。
- Modal 不自动关闭，不使用闪烁、循环发光、粒子爆发、屏幕震动或胜利式演出。
- 每个合成 notification group 至多一次中性纸页音；全部结局语境使用同一文件、音高、响度与包络。Self-voicing active 时不播放通知音。
- 音效来源、许可证、hash、格式、采样率、声道、响度、`loop=false` 与替换 ID 必须登记；不得使用官方或来源不明素材。

## UI Requirements

### Surface and Flow

1. 愿望手册主页面提供“旅途记录”入口；入口在 persistence ready 时启用，在 unavailable/recovery 时打开统一恢复界面。
2. 非空列表打开后默认焦点位于首个已解锁 row；空列表默认焦点为返回操作。保留本 process session 的 semantic scroll anchor；关闭后恢复到愿望手册入口。
3. 成就页只渲染已解锁 rows，按“场景回声→路线发现→后来留下的回声”分组；空组不显示标题或空白。
4. 页面顶部显示“曾经走过 X 项”；不显示 `/11`、百分比、剩余数、“完整”或全收集终态。
5. 未 seen row 显示“新记录”；seen row 显示“曾经走过”。状态不只依赖颜色。
6. Persistence unavailable 时不显示正常列表或“0项”，原子转入统一恢复界面。

### Combined Notification Modal

- 标题：“新的旅途记录”；操作：“继续”。
- Modal 打开时主动朗读标题→记录名称→“继续”；self-voicing active 时 suppress SFX。
- 固定使用可滚动 viewport；静态 rows 不进入 Tab order，“继续”始终可见并获得初始交互焦点。
- `modal True` 不是完整输入证明；必须显式 gate rollback、save/load、skip、AFM、history、game menu、quick menu、Journal、Settings 与底层 choice actions。
- Escape 与右键只触发一次“继续”，不得传播到 game menu。
- 自动出现的 modal 在显示前捕获 stable semantic focus ID；关闭后若目标仍存在则恢复，否则落到 scene continuation fallback。Scene jump/recovery 时不得恢复 stale displayable。

### Copy Boundary

批准文案：

- “新的旅途记录”
- “曾经走过”
- “新记录”
- “曾经走过 X 项”
- “继续”
- “收藏记录暂时不可用”

不得显示或朗读 internal IDs、条件、缺失步骤、axis、token、qualification、threshold、resolver、backend、schema、epoch 或 repair 细节。

## Acceptance Criteria

证据类型：`STATIC`、`UT_PURE`、`UT_ENGINE`、`INSTR`、`BRANCH`、`A11Y`、`VISUAL`、`BENCH`。

### Catalog and Semantic Integrity — 8

| ID | Evidence | Criterion |
|---|---|---|
| `ACH-CAT-001` | STATIC + UT_PURE | 批准目录恰为11项，ID唯一并与 v2 exact-match；ending/memory mirror count 为0。 |
| `ACH-CAT-002` | STATIC + UT_PURE | 8字段 schema exact-match；owner固定、operator全为`all`、reveal全为`ON_UNLOCK`。 |
| `ACH-CAT-003` | STATIC | 11个 completion events、checkpoints与 witnesses各解析一次，真实 source callsite由对应 responsibility scene支配。 |
| `ACH-CAT-004` | STATIC + UT_PURE | 三组与组内 rank exact-match，所有 locked surface count 为0。 |
| `ACH-CAT-005` | UT_PURE | 每项至少1个 positive golden、逐 required-event missing negatives、wrong-checkpoint negative；复合条件含顺序负例。 |
| `ACH-CAT-006` | STATIC + REVIEW | 技术 forbidden reference count 为0；semantic anti-checklist rubric证明名称/条件/分组不能一对一恢复五轴或结局等级。 |
| `ACH-CAT-007` | BRANCH + UT_PURE | 零轴 witness 完整重放后只解锁 `CHOICE_READ_THE_NOTE`。 |
| `ACH-CAT-008` | BRANCH + UT_PURE | Day6拒绝→`day6_take_cost_back`→安全替代 exact witness解锁 `CHOICE_ACCEPT_NO`；override、无替代与不匹配 checkpoint 均失败，并存在一条 non-`rain_stops` positive path。 |

### Snapshot and Evaluation — 8

| ID | Evidence | Criterion |
|---|---|---|
| `ACH-EVAL-001` | UT_PURE | generation/epoch匹配、occurrence未占用、canonical cumulative/new tail与checkpoint mapping合法时输出True。 |
| `ACH-EVAL-002` | UT_PURE | wrong type/generation/epoch、unknown/duplicate/out-of-order、non-tail delta、wrong checkpoint与claimed occurrence逐案及组合均False，scan/request counts为0。 |
| `ACH-EVAL-003` | UT_PURE | snapshot validation和set derivation各恰一次，11条record各访问一次。 |
| `ACH-EVAL-004` | UT_PURE | 完整条件+last event本次新增+membership absent才eligible；任一缺失固定False。 |
| `ACH-EVAL-005` | UT_PURE + UT_ENGINE | startup/load/rollback的空delta与旧epoch snapshot均产生0 candidate。 |
| `ACH-EVAL-006` | INSTR + UT_PURE | 合法checkpoint固定扫描11条，不提前结束、不重复snapshot validation。 |
| `ACH-EVAL-007` | UT_PURE + BRANCH | production图生成 exact `max_reachable_eligible_per_checkpoint` fixture；另用synthetic 11-record helper验证排序/去重，二者不得混称。 |
| `ACH-EVAL-008` | UT_PURE | N=`0,1,max-reachable,synthetic11`时candidate长度exact N，与new IDs逐项对应、无extra/missing并保持UTF-8 stable-ID顺序。 |

### Persistence and Backend — 9

| ID | Evidence | Criterion |
|---|---|---|
| `ACH-PERSIST-001` | UT_ENGINE + INSTR | 新candidate由专用adapter构造request，result record含exact added/existing/epoch/occurrence/group；成功只新增目标。 |
| `ACH-PERSIST-002` | UT_ENGINE + INSTR | 直接提交existing-membership request返回`DUPLICATE_NOOP`且所有write/projection/popup/audio counts为0。 |
| `ACH-PERSIST-003` | UT_ENGINE + INSTR | Batch含一次existing ID与new ID时只新增new；existing不展示。 |
| `ACH-PERSIST-004` | UT_ENGINE + INSTR | Raw batch内重复`(kind,id)`或wrong owner/ID/event/checkpoint/epoch/generation/type时整批拒绝。 |
| `ACH-PERSIST-005` | UT_ENGINE + INSTR | 同checkpoint跨kind candidates由唯一coordinator形成一个batch、一次flush和一个notification group；无mirror achievement。 |
| `ACH-PERSIST-006` | UT_ENGINE + INSTR | Safe failure无成功反馈；相同occurrence只允许相同payload按SYS-PERSIST批准策略重试。 |
| `ACH-PERSIST-007` | UT_ENGINE + INSTR | Commit-unknown冻结后续writes/projection/feedback；restart reconciliation不靠历史snapshot补发。 |
| `ACH-PERSIST-008` | UT_ENGINE + INSTR | Root成功后backend partial failure不撤销membership；repair只补missing且不通知。 |
| `ACH-PERSIST-009` | UT_ENGINE + INSTR | Backend额外IDs不能反向增加root/UI；backend→root write count为0。 |

### Rollback, Epoch, Seen, and Recovery — 6

| ID | Evidence | Criterion |
|---|---|---|
| `ACH-INV-001` | UT_ENGINE + INSTR | Durable unlock后rollback再前进，membership保留，evaluator candidate与SYS-PERSIST call均为0，popup/audio为0。 |
| `ACH-INV-002` | UT_ENGINE | Completion前save但root已含ID时load不清membership、不伪造event、不补modal；Journal仍可显示曾经走过。 |
| `ACH-INV-003` | UT_ENGINE + INSTR | Deferred/ready/modal在load、rollback、exit、recovery时清除；membership保留、seen不增加、恢复后popup/audio为0。 |
| `ACH-INV-004` | UT_ENGINE + BRANCH | Reset递增epoch；old-save-before-event、between-composite-events与same-run fixtures均拒绝；explicit New Game复制新epoch后可合法重获。 |
| `ACH-INV-005` | UT_PURE + UT_ENGINE | Merge只使用max epoch roots；旧epoch membership不能复活，same-max memberships/seen canonical union。 |
| `ACH-INV-006` | UT_ENGINE + A11Y | unavailable/commit-unknown/reset recovery不进入正常目录；mark-seen失败只保留“新记录”，不丢membership。 |

### Presentation and Accessibility — 8

| ID | Evidence | Criterion |
|---|---|---|
| `ACH-UI-001` | UT_ENGINE + INSTR | Unsafe boundary返回DEFER，视觉/音频/self-voicing notification counts为0。 |
| `ACH-UI-002` | UT_ENGINE + VISUAL | 1个及多个deferred groups在下一safe boundary合并为一个modal，ID去重并按catalog rank排序。 |
| `ACH-UI-003` | UT_ENGINE + INSTR | 关闭modal消费exact pending IDs、清queue/timer/audio token并提交mark-seen；membership不变。 |
| `ACH-UI-004` | STATIC + VISUAL + A11Y | 11项locked时row/slot/group/count/focus/self-voicing surface全为0；解锁后各出现一次。 |
| `ACH-UI-005` | UT_ENGINE + A11Y + INSTR | Missed modal后跨会话Journal显示unseen“新记录”；prediction/screen construction的mark-seen call count为0；真实可交互list version生成receipt且玩家离开分区后，SYS-JOURNAL caller提交的payload只含实际呈现IDs，seen subset更新且下次为“曾经走过”。 |
| `ACH-UI-006` | STATIC + VISUAL | 全部surface的internal ID/condition/axis/token/predicate/backend/schema/epoch render count为0。 |
| `ACH-UI-007` | UT_ENGINE + A11Y | Journal入口/返回、modal viewport滚动、reading order、keymap gate、focus capture/fallback在mouse/keyboard/self-voicing/静音下全部可达。 |
| `ACH-UI-008` | VISUAL + A11Y | Journal 0/1/11项与modal 1/max-reachable/11 synthetic在720p、三档字体、两种对比度与motion模式下无裁切/重叠/offviewport action。 |

### Performance and Build — 4

| ID | Evidence | Criterion |
|---|---|---|
| `ACH-PERF-001` | BENCH | Manifest冻结`E_max`、`ΔE_max`、`Σ|R_e|`、最长ID、max-reachable与synthetic11 fixtures；5次warm-up+≥30原始样本，validation+set build+11 scan的p95≤2ms、max≤5ms。 |
| `ACH-PERF-002` | BENCH + VISUAL | 分别记录durable result、modal build、first present、transition frames与focus restore；普通帧p95≤16.6ms、max≤33.2ms，I/O/timer不混入。 |
| `ACH-BUILD-001` | STATIC | 除SYS-PERSIST adapters外无direct root/backend write、manual claim/revoke、persistent pending-popup ledger、forbidden condition read或test seam。 |
| `ACH-BUILD-002` | STATIC | 43个criterion IDs唯一，每项artifact含criterion-specific fixture/assertion IDs、source/catalog hashes、runner/environment/raw samples与exit code 0；空壳PASS失败。 |

## Resolved Decisions and Remaining Gates

### Resolved in this revision

- `ACH-Q1`：取消 visible/hidden split；11项全部 `ON_UNLOCK`，locked surface为0。
- `ACH-Q2`：`achievement_event_catalog:v2` 冻结11个 completion event与checkpoint。
- `ACH-Q3`：snapshot增加epoch与occurrence，冻结canonical tail与一次验证规则。
- `ACH-Q6`：取消13个mirror achievements；唯一coordinator与durable-result/group payload已定义。
- `ACH-Q7`：reset递增epoch，merge只接纳max epoch，显式New Game复制新epoch。
- Producer：采用11项独立成就；采用`seen_achievement_ids`跨会话发现，modal不跨session重播。

### Remaining external gates

| ID | Gate | Required evidence |
|---|---|---|
| `ACH-Q4` | Ren’Py backend integration | 11-item grant/has/exception/restart matrix、call order、partial failure与zero-duplicate-popup evidence |
| `ACH-Q5` | Architecture implementation-ready | Accepted ADR-0002 amendment、Architecture/Control Manifest/root manifest更新、foreign-write scan |
| `ACH-Q8` | UI/audio story Ready | SYS-JOURNAL/SYS-ACCESS UX specs、Art Bible、asset spec、三档字体与self-voicing captures、audio license |
| `ACH-Q9` | Performance acceptance | Lowest reference hardware、timer/GC/cache/process manifest、exact maxima与raw samples |

关闭以上外部 gate 前可以实现纯 catalog/snapshot/evaluator 模块，但不得宣称 backend、reset、player-facing UI 或完整 implementation accepted。
