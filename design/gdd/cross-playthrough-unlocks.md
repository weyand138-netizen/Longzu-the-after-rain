# 跨周目解锁

> **System ID**: SYS-PERSIST
> **Status**: Approved with provisional downstream gates
> **Author**: Andwey + Codex
> **Last Updated**: 2026-08-04
> **Implements Pillar**: 温柔必须被挣来；悲剧也是完整答案；用普通生活抵抗宏大命运
> **Upstream Contracts**: Ren'Py 8.5.3；ADR-0002；SYS-ENDING/SYS-NARRATIVE approved output boundaries；SYS-SAVE persistent isolation contract
> **Review Mode**: Solo
> **Design Self-Check**: 2026-08-09 — P0 shared-contract closure in progress；11/11 required sections complete；11 achievement IDs + 6 ending IDs + 7 memory IDs；12 normative leaves；targeted closure only
> **Design Review**: 2026-07-30 — MAJOR REVISION NEEDED；merge、commit-unknown、ending-completion、exact batch、reset/UX 与 performance contracts revised in this pass；full re-review required before Production
> **SYS-ACCESS Amendment**: 2026-08-04 — schema v2 uses the single 12-leaf / 5-setting authority；legacy flat prototype fields and local development saves are explicitly incompatible

## Overview

SYS-PERSIST 是负责跨周目数据边界的 P0 Foundation 系统。它使用 Ren’Py 8.5.3 原生 `persistent` 机制，为已完成叙事结果产生的成就、结局与回忆解锁，以及项目自定义设置，提供版本化、可验证、幂等的存储、合并与显式落盘能力。各语义系统仍独占“何时解锁”的判定；SYS-PERSIST 只接受已批准 owner 提交的稳定 ID，并向 SYS-ACHIEVE、SYS-JOURNAL、SYS-GALLERY、SYS-ACCESS 和 SYS-SAVE 暴露只读状态或受控写入接口。

本系统不保存、恢复或推导五轴、选择历史、counterevidence token、路线资格、结局 predicate 或其他局内状态。合法跨周目数据不会被读档、回退、阻断式退出或明确开始新游戏撤销，也不得反向影响当前周目的选择与结局。首发只使用本地 Ren’Py persistent 文件，不提供云同步、玩家间导入或外部 JSON 主存储；schema、字段 ownership、flush 与未来迁移由 SYS-PERSIST 独占，并遵守 ADR-0002。

## Player Fantasy

当玩家开始第二个及后续周目时，愿望手册与收藏界面应像一份忠实的旅途记忆：真正经历过的章节、结局与重要时刻仍然存在，并随着探索自然丰富。每项解锁代表玩家确实走完的一段叙事，而不是对“正确选择”的评分；悲剧结局也以与好结局同等可靠、完整的方式被记录，使玩家愿意理解其他可能性，而不是把失败视为应被系统抹去的错误。

玩家不需要理解 persistent 文件、schema 或落盘时机，只需确信已经合法获得的记录不会因退出游戏、读档、回退或开始新游戏而丢失，尚未完成的事件也不会因预览分支或技术异常提前解锁。字体缩放、高对比度等项目设置同样应在下次启动时保持，使玩家回到熟悉、可用的体验；重置收藏进度不得顺带撤销这些无障碍设置。所有未解锁展示必须避免泄露剧情、隐藏轴和结局条件，让收藏表达“你经历过什么”，而不是暗示“你还缺哪个正确答案”。

## Detailed Design

### Core Rules

1. 产品拥有且直接访问的唯一持久化根字段是 `persistent.sys_persist_state`。除 Ren’Py 自有 preferences 与 achievement backend 外，不得新增平铺的 `persistent.*` 产品字段。
2. 首发根状态使用 schema v2，只包含本节冻结的 12 个规范叶字段。根及其全部后代只允许本 schema 明列的 exact CPython built-in types；不得把 Ren’Py rollback-aware 容器子类当作 exact built-in，也不得保存自定义类、displayable、文件句柄、任务、socket、generator 或 imported mutable object。Fresh default 必须由 `python_dict`/`python_list` 等明确的 built-in constructor 或 imported pure builder 构造，并通过 engine round-trip fixture。
3. 所有产品持久化更新必须先读取并验证当前根状态，在局部构造完整候选值，最后对 `persistent.sys_persist_state` 执行一次 replacement assignment；不得原地修改 collection 或嵌套 mapping。
4. SYS-PERSIST 是根字段、schema、validation、merge、replacement assignment、flush、reset 与 migration 的唯一实现 owner。其他系统只能通过获准的 request API 提交语义结果或读取 detached snapshot。
5. 成就、结局和回忆仅在对应叙事结果已经完成后解锁。Ending unlock 不得由 ending label entry 或 `commit_ending_entry` 触发；六个 ending label 必须在最后一段叙事与玩家可见收束完成后调用唯一 `commit_ending_completion`，再由 ending orchestrator 提交 completed-event request。SYS-PERSIST 验证专用 owner API、稳定 ID、catalog generation 与 completed-event catalog reference，但把“该 traversal 已完成”视为受信 orchestrator assertion，不读取 live state 重新证明成就条件、章节完成条件、ending predicate 或 ending priority。
6. Root 已存在的合法 ID 经专用 adapter 直接提交时返回 `DUPLICATE_NOOP`；semantic evaluator 应在调用前过滤 membership，因此正常 rollback 重走产生 0 request。Raw batch 内重复 `(unlock_kind,stable_id)` 固定为 `REJECTED_INVALID`。
7. 五轴、ordered choice history、counterevidence token、route qualification、resource possession、ending predicate、resolution record、ending lifecycle、reaction/payoff ledger、popup queue、UI focus 与当前 notification 均不得进入根状态。`seen_achievement_ids` 只表示愿望手册发现状态，不是 pending popup。
8. 合法 persistent 根状态不会因 per-run save/load、rollback、blocking safe-flow exit 或 explicit new game 被替换、清除或从局内状态重建。
9. 首发只使用 Ren’Py 本地 persistent 文件；不提供云同步、玩家间导入、MultiPersistent、外部 JSON 主存储、网络同步或平台账户恢复。
10. 任何 unknown schema、unknown catalog generation、wrong exact type、unknown key、missing key、非法 ID、batch 内重复 request、冲突 setting update、重复 collection item 或非 canonical ordering 均不得静默过滤、补写或规范化。

### Ending Completion Contract

`SYS-ENDING` 是 `commit_ending_completion` 的唯一 owner。六个 ending label 各自只有一个 stable completion node：完整 ending narration 与最后一个玩家可见 closure 已完成之后、离开 ending label 或返回章节控制流之前。该 node 只能调用一次 `commit_ending_completion(ending_id, completion_checkpoint)`；不得在 resolver、entry label 首句、`commit_ending_entry` 或 Journal/UI 回调中调用。

该调用构造一个 rollback-owned `ending_completion_event_record`，字段固定为 `ending_id, completed_event_id, checkpoint_id, checkpoint_occurrence_id, collection_epoch_id, catalog_generation_id, stable_completion_boundary, owner_system`。`completed_event_id` 固定为 `ending_completed:{ending_id}`，`owner_system` 固定为 `SYS-ENDING`，`stable_completion_boundary` 固定为 `True`。唯一 persistence checkpoint coordinator 以该记录提交 ending request；SYS-PERSIST 只验证 catalog、owner、epoch 与 checkpoint，不重新求值 ending predicate。

`commit_ending_entry` 只把 rollback-owned lifecycle 从 `Active` 变为 `Ended`；在 completion node 之前不得产生 ending membership 或 completed-event request。completion 成功后，ending membership 的 `APPLIED_FLUSHED` 结果进入 canonical persistent root；之后的 per-run save/load/rollback 只恢复 lifecycle、completion event 与控制位置，不撤销已落盘的 membership。回退到 completion node 之前时，completion event/request 计数恢复为 0；再次前进到同一 ending 时可重放同一 checkpoint，已存在 membership 返回 `DUPLICATE_NOOP`，不得产生第二次 popup 或 notification。

### Canonical State Schema

`persistent.sys_persist_state` 是 exact built-in `dict`，首发包含以下 12 个规范叶字段；`settings` 只是包含最后五项叶字段的固定容器。

| 规范路径 | Exact type | 首发约束 | 语义 |
|---|---|---|---|
| `schema_version` | exact `int`，不接受 `bool` | `2` | 根状态 schema |
| `catalog_generation_id` | exact `str` | `"persist_catalog:v2"` | ID catalog generation |
| `collection_epoch_id` | exact `int`，不接受 `bool` | `≥0`；fresh 为 `0`；每次成功 reset 恰加 `1` | 使 reset 前 run/save/evidence 失效的收藏时代 |
| `achievement_ids` | exact `tuple` of exact `str` | 已排序、唯一；为获批 11 项成就 ID 的子集 | 已获得的独立本地成就 |
| `seen_achievement_ids` | exact `tuple` of exact `str` | canonical subset of `achievement_ids` | 已在 modal 或愿望手册成功呈现的成就 |
| `ending_ids` | exact `tuple` of exact `str` | 已排序、唯一；为六个 canonical ending ID 的子集 | 已进入并正式提交的结局 |
| `memory_ids` | exact `tuple` of exact `str` | 已排序、唯一；为 `MEMORY_DAY_1`～`MEMORY_DAY_7` 的子集 | 已完成的章节回忆 |
| `settings.font_scale` | exact `float` | 必须属于获批离散档位；首发默认 `1.0` | 项目字体缩放 |
| `settings.high_contrast` | exact `bool` | 首发默认 `False` | 项目高对比度设置 |
| `settings.reduced_motion` | exact `bool` | 首发默认 `False` | 非必要转场与循环运动归零策略 |
| `settings.flash_effects_enabled` | exact `bool` | 首发默认 `False` | 是否允许已登记且有静态替代的闪烁效果 |
| `settings.screen_shake_enabled` | exact `bool` | 首发默认 `False` | 是否允许已登记且有静态替代的屏幕位移 |

Fresh install 通过 concrete `default persistent.sys_persist_state = build_fresh_persist_root()` 获得有效根状态；该 pure builder 必须返回 exact built-in `dict`，其中 nested `settings` 也是 exact built-in `dict`，collections 为 exact built-in `tuple`。不得直接用会被 Ren’Py 转换为 rollback-aware subclass 的 `.rpy` dict/list/set literal 充当规范根。初始化不得从 save slot、局内 state、achievement backend 或 UI cache 推导任何叶字段。

三类 collection namespace 与用途保持分离。Schema v2 不包含 ending/memory mirror achievements；SYS-PERSIST 不根据任一 collection 自动推导另一 collection。

### Ownership Manifest

Build-valid `persistent_ownership_manifest` 必须是非空、版本化、冻结的 exact immutable catalog record，字段集合必须恰为：

`manifest_generation_id, root_field_name, schema_version, catalog_generation_id, leaf_field_paths, leaf_field_count, exact_type_ids, semantic_owner_system_ids, allowed_requester_system_ids, merge_policy_ids, reset_policy_ids, migration_policy_id`

Manifest 表示为 exact built-in tuple，按上列顺序包含 12 项；文中 `M.<field>` 只是假名，严格对应该 positional tuple 的冻结 index，不要求或允许自定义 record class。所有并行 leaf arrays 都是长度恰为 12 的 exact tuple，并以 `leaf_field_paths` 的 canonical order 一一对齐。`manifest_generation_id`、`root_field_name`、`catalog_generation_id`、全部 type/owner/requester/policy IDs 与 `migration_policy_id` 均为 nonempty exact str；`schema_version`、`leaf_field_count` 为 exact int 且分别等于 `2`、`12`。不得有 extra/missing field、空 policy、重复 leaf、数组长度偏差或 unresolved ID。

首发 `root_field_name` 固定为 `"sys_persist_state"`。每个叶字段必须恰有一个 storage writer（SYS-PERSIST）和一个 semantic owner：

| 叶字段 | Semantic owner | Allowed requester | Storage writer |
|---|---|---|---|
| `schema_version` | SYS-PERSIST | SYS-PERSIST | SYS-PERSIST |
| `catalog_generation_id` | SYS-PERSIST | SYS-PERSIST | SYS-PERSIST |
| `collection_epoch_id` | SYS-PERSIST | SYS-PERSIST reset adapter | SYS-PERSIST |
| `achievement_ids` | SYS-ACHIEVE | SYS-ACHIEVE | SYS-PERSIST |
| `seen_achievement_ids` | SYS-ACHIEVE | SYS-ACHIEVE / SYS-JOURNAL 经专用 mark-seen adapter | SYS-PERSIST |
| `ending_ids` | SYS-ENDING | ending orchestrator，在 `commit_ending_completion` 成功后 | SYS-PERSIST |
| `memory_ids` | SYS-NARRATIVE | chapter orchestrator，在章节完成事件后 | SYS-PERSIST |
| `settings.font_scale` | SYS-ACCESS | SYS-ACCESS | SYS-PERSIST |
| `settings.high_contrast` | SYS-ACCESS | SYS-ACCESS | SYS-PERSIST |
| `settings.reduced_motion` | SYS-ACCESS | SYS-ACCESS | SYS-PERSIST |
| `settings.flash_effects_enabled` | SYS-ACCESS | SYS-ACCESS | SYS-PERSIST |
| `settings.screen_shake_enabled` | SYS-ACCESS | SYS-ACCESS | SYS-PERSIST |

SYS-SAVE、SYS-JOURNAL 与 SYS-GALLERY 对 root 只读取 detached snapshot 或 manifest，不得成为 writer；SYS-JOURNAL 仅可通过专用 caller 请求 mark-seen，由 SYS-PERSIST 验证并写入。Static ownership scan 必须拒绝 manifest 外字段、直接 `persistent.sys_persist_state` assignment、嵌套原地修改及未获准 requester。

Requester identity 不由调用方自由填写。SYS-PERSIST 暴露五个专用入口：achievement、achievement-mark-seen、ending-completion、memory-completion 与 project-setting；adapter 在入口内注入冻结 requester ID。Static callgraph 与 CFG dominance 必须证明每个 production unlock callsite 位于对应 owner 的完成边界之后。Request 中的 `completed_event_id` 只是 catalog-covered assertion 与诊断引用，不是密码或运行时权限证明。

### Update Requests and Batches

一次 unlock request 是 transient exact built-in dict，key set 必须恰为：

`unlock_kind, stable_id, completed_event_id, requesting_owner_system_id, checkpoint_id, checkpoint_occurrence_id, collection_epoch_id, catalog_generation_id`

除 `collection_epoch_id` 为 exact nonnegative int 外，其余七个值均为 nonempty exact str。`unlock_kind` 只允许 `achievement/ending/memory`；kind、stable ID、event、requester、checkpoint 与 generation 必须在同一 catalog record 中 exact-match；epoch 必须等于当前 root。该 dict 只能由对应专用 requester adapter 构造；公共调用方不能传入或覆盖 `requesting_owner_system_id`。

它只作为当前调用的输入，不进入 canonical persistent root、achievement queue 或独立产品 ledger。调用方可在 rollback-owned completion checkpoint 中保留可重放的 transient batch，直到结果确定；该 checkpoint 必须存在 pre-completion save/replay path。`completed_event_id` 必须解析到冻结 catalog 中由该 requester 拥有且位于真正 completion boundary 后的事件；SYS-PERSIST 不读取 axes、history、token 或其他 live state 来重新证明条件。

一次 persistence batch 是 exact built-in dict，key set 恰为：

`checkpoint_id, checkpoint_occurrence_id, collection_epoch_id, catalog_generation_id, unlock_requests, seen_achievement_ids_to_add, setting_updates, settings_base`

- `checkpoint_id`、`checkpoint_occurrence_id` 与 `catalog_generation_id` 为 nonempty exact str；`collection_epoch_id` 为 exact nonnegative int并等于当前root；
- `unlock_requests` 为长度 0～24 的 exact tuple of exact unlock-request dicts，canonical order 固定为 `(unlock_kind UTF8, stable_id UTF8)`，同一 `(kind,id)` 重复固定非法；
- `seen_achievement_ids_to_add` 为长度 0～11 的 exact tuple，只能包含当前 root 已有但尚未 seen 的批准成就 ID，并按 stable ID UTF-8排序；
- `setting_updates` 为长度 0～5 的 exact tuple of exact `(field_path, value)` pairs，按 `settings.font_scale → settings.high_contrast → settings.reduced_motion → settings.flash_effects_enabled → settings.screen_shake_enabled` canonical order，field 唯一且只允许五项设置；每个 pair 必须实际改变 base 值；
- unlock-only batch 的 `settings_base` 必须为 exact `None`；含 setting update 时，它必须是打开/最后一次 rebase Settings 时的 exact `(font_scale, high_contrast, reduced_motion, flash_effects_enabled, screen_shake_enabled)` tuple；
- 三类 payload 不得同时为空；同一 checkpoint 需要多个系统结果时，由唯一 persistence checkpoint coordinator 预先合成一个 batch。Mark-seen 使用独立 `journal_seen_ack` checkpoint，不和 narrative unlock 合批。

Batch validation 必须按固定 stage 在任何 assignment 前完成：container/exact keys → scalar exact types → length/order/duplicates → manifest/generation → requester/event/catalog references → settings-base conflict → candidate。任一成员非法时整批拒绝，不允许部分应用或 set 化去重。合法 batch 按以下顺序处理：

1. 验证当前 root、ownership manifest、catalog generation、request schema、owner 与全部引用。
2. 若含 setting update，比较当前 settings 与 `settings_base`：相等则可提交；若只发生 membership/seen 变化则以当前 root rebase 后提交；若 settings 自身已变化则返回 `STALE_DRAFT_CONFLICT`，不应用任何成员。
3. 将 root 中已存在的 unlock IDs 分类为 existing duplicate；若 batch 不产生任何深值变化，返回 `DUPLICATE_NOOP`。
4. 在局部 exact built-in 值中构造完整 candidate；三类 membership 与 seen 集合按 canonical UTF-8 stable-ID 顺序冻结为 tuple，并再次验证 `seen_achievement_ids ⊆ achievement_ids`。
5. 对 `persistent.sys_persist_state` 执行一次 replacement assignment。
6. 在同一 stable checkpoint 调用一次 `renpy.save_persistent()`。
7. 只有 engine adapter 明确分类为公开结果 `APPLIED_FLUSHED` 后才返回 exact durable-result record：`status, checkpoint_occurrence_id, collection_epoch_id, added_achievement_ids, existing_achievement_ids, added_ending_ids, added_memory_ids, newly_seen_achievement_ids, notification_group_id`。`APPLIED_FLUSHED` 是唯一公开的成功结果名；不得向 consumer、fixture、registry 或 evidence 暴露另一成功别名。只有新增 memberships 交给 projection/presentation；seen-only update 的 `notification_group_id` 固定为空字符串且不产生玩家提示。
8. 只有 failure-injection 已证明该失败发生在任何磁盘变更前，才能恢复 previous root 并返回 `PERSIST_FLUSH_FAILED_SAFE`。
9. 其他异常、未文档化返回、serialization/temporary-write/replacement/process-interruption 均进入 `COMMIT_STATUS_UNKNOWN`：保留 previous/candidate 的 session-local detached copies，冻结全部后续 persistent writes、projection 与成功反馈，进入独立 blocking recovery，要求 restart 后重新读取并验证磁盘 root。若磁盘为 candidate，则静默收敛 projection且不补 popup；若为 previous，则从 rollback-owned pre-completion checkpoint 重放同一 batch。不得在未知状态下接受不同 batch。

Invalid owner、ID、schema、generation、type、field count 或 completion reference 必须在 step 4 前固定失败，并记录开发诊断；玩家界面不得显示隐藏条件、内部 ID、轴或结局规则。

### Achievement Backend Projection

产品根状态是 SYS-ACHIEVE、SYS-JOURNAL、SYS-GALLERY 和产品 UI 的唯一产品权威。Ren’Py achievement backend 只是针对 `achievement_ids` 的幂等投影：

1. 仅对一次 `ABSENT → PRESENT` 且 canonical root 已成功 flush 的 achievement ID 调用 `achievement.grant()`。
2. Projection 成功或 `achievement.has(id)` 已为真都视为已收敛；不得产生第二次产品解锁或第二个 popup。
3. Projection 失败不得撤销 canonical root。系统在下次启动或下一个稳定 persistence checkpoint 从 root 单向重试。
4. Repair scan 只遍历当前批准的 11 项 achievement IDs；它不读取 achievement backend 来反向添加 canonical root membership。
5. Projection repair 不产生 player-facing popup；popup 只对应当前 session 中首次成功完成的 canonical root transition。
6. 不得建立持久化 pending list、backend-to-product reconciliation、第二套 dedupe ledger 或把 `achievement.has()` 作为 Journal/Gallery 的显示权威。

### Merge, Startup Validation, and Migration

SYS-PERSIST 为 `"sys_persist_state"` 注册唯一 `renpy.register_persistent()` merge function。Callback contract 固定为 Ren’Py 的 `merge_sys_persist_state(old, new, current)`；项目接受引擎已给出的 `old/new` 旧新顺序，不读取或声称获得 raw age、equal-age flag 或 source identity。只有 schema、generation、exact keys/types 与 catalog membership 均合法，且 `current.settings` 深值等于 `old.settings` 或 `new.settings` 时，来源才可参与正常合并：

- 先计算 `e=max(old.collection_epoch_id,new.collection_epoch_id,current.collection_epoch_id)`；只有 epoch 等于 `e` 的 roots 参与 collection merge，低 epoch roots 的 memberships 与 seen 全部忽略；
- 在最大 epoch roots 中，`achievement_ids`、`ending_ids`、`memory_ids` 与 `seen_achievement_ids` 分别取 canonical union；合并后再次验证 `seen_achievement_ids ⊆ achievement_ids`；
- 输出 `collection_epoch_id=e`；
- 五项 project settings 固定作为一个 exact tuple 采用 callback 的 `new` 值；不得逐字段混合来源。Settings preview 从不进入 canonical root，operation mutex 保证 callback 期间没有第三个未 flush setting commit；
- 三个来源的 `schema_version` 与 `catalog_generation_id` 必须完全相等；
- 合并结果必须再次通过 full root validator 后才能成为 active root。

Wrong type、unknown/missing key、非法集合成员、重复/乱序 tuple、unknown schema、incompatible generation，或 `current.settings` 同时不同于 old/new，均不得被 union、截断、过滤或由 backend 补足。Callback 不抛异常或依赖未文档化 abort，而是返回 exact built-in recovery marker：

`("PERSISTENCE_SAFE_RECOVERY", "merge_invalid_or_incompatible", "persist_catalog:v2")`

该 marker 与获批 reset adapter 的 exact reset marker 是 `persistent.sys_persist_state` 仅有的非-root合法分类值；merge marker 只允许 merge callback 产生。Startup classifier 必须在 default/root validation 前通过 `_hasattr` 与 exact tuple comparison 识别它们；marker 不参与 normal root validator、collection read、write、projection 或再次正常 merge。Merge marker 进入 persistence-safe recovery；该分类不得阻止玩家返回主菜单或开始不依赖跨周目状态的新游戏，但在安全恢复或玩家明确重置前，不得展示、写入或声称已保存受影响的收藏数据。项目不宣称从非法 merge source 保留或选择性抢救 old IDs。

首发不承诺迁移当前开发构建中的平铺字段 `achievements_unlocked`、`endings_unlocked`、`memories_unlocked`、`high_contrast` 与 `font_scale`。公开发行后的任何 schema、catalog generation 或字段 ownership 变化必须先获得独立 migration ADR，冻结 source→target 支持矩阵、golden persistent fixtures、失败策略、回退方案与删除窗口。

### Runtime States and Transitions

以下仅为概念运行状态，不新增 persisted lifecycle enum：

| 状态 | 触发 | 允许结果 |
|---|---|---|
| `Validated` | fresh/default、startup validation 或合法 merge 完成 | 可读取；可接受 request |
| `CandidatePrepared` | 合法非空 batch 验证完成 | 尚未修改 root |
| `Flushing` | replacement assignment 后调用 `save_persistent()` | `APPLIED_FLUSHED` 进入 `Validated`；proven pre-write failure 恢复 previous；其他结果进入 `CommitUnknown` |
| `CommitUnknown` | flush/进程中断无法证明磁盘是 previous 或 candidate | 冻结写入、projection 与成功反馈；只允许 blocking recovery、restart 与 startup reconciliation |
| `ProjectionRepair` | canonical root 已含 achievement、backend 尚未收敛 | 单向 grant；不弹窗 |
| `PersistenceSafeRecovery` | root 非法、不兼容或为 exact merge recovery marker | 禁止收藏写入与成功声明；允许安全主菜单、新游戏、明确恢复或重置 |
| `ResetRecovery` | root 为 exact reset marker 或 startup 发现 reset terminal 不一致 | 只允许 retry same reset、返回安全主菜单或退出；不得进入 normal collection UI |

Per-run load、rollback、blocking exit 与 explicit new game 不构成上述状态转换，也不得改变 canonical root 的深值。

### Interactions with Other Systems

| 系统 | 合法接口 | 禁止行为 |
|---|---|---|
| SYS-ENDING | ending label 完整收束并执行 `commit_ending_completion` 后提交 stable ending ID | `commit_ending_entry` 只拥有 lifecycle entry，不得触发 unlock；persistent 不得参与 resolver、priority 或 predicate |
| SYS-NARRATIVE | 章节完成后提交 memory ID；提供 completed event references | 不得直接写 root 或用未完成场景提前解锁 |
| SYS-ACHIEVE | 条件完成后提交11项独立 achievement candidate；自动achievement modal关闭后以SYS-ACHIEVE caller提交mark-seen IDs；消费epoch与exact durable-result record | SYS-PERSIST 不复制成就条件；ending/memory不镜像为achievement；seen不是pending popup |
| SYS-ACCESS | 提交五项项目设置更新 | 不得绕过 validator；Ren’Py self-voicing/text/auto/skip/volume preferences 不移入产品 root；engine font/high-contrast入口按SYS-ACCESS合同禁用而不形成第二套权威 |
| SYS-SAVE | 消费 ownership manifest 与不变性 snapshot | load/rollback/new game 不写 persistent；不从 per-run save 重建 |
| SYS-JOURNAL | 读取detached product snapshot；玩家离开achievement list时，以immutable presentation receipts支持的exact IDs调用Journal专用mark-seen caller | 不以backend、slot metadata或隐藏条件推导解锁；不提交未实际呈现ID；不自由填写requester/checkpoint |
| SYS-GALLERY | 读取 detached product snapshot | 不以 backend、slot metadata 或隐藏条件自行推导解锁 |
| SYS-TEST | 消费 fixtures、fault injection、merge 与 ownership evidence | test observer、spy、synthetic root 不进入 production persistent |

## Formulas

### Definitions and Canonical Ordering

设批准目录分别为：

- \(C_A\)：11 个 achievement IDs；
- \(C_E\)：6 个 ending IDs；
- \(C_M\)：7 个 memory IDs；
- \(F\)：批准的字体缩放档位。

Stable ID catalog 只接受 nonempty exact ASCII str，字符集冻结为 `[A-Za-z0-9_:-]`，因此不存在 Unicode normalization 或 UTF-8 encoding failure 分支。规范排序只按 UTF-8 bytes：

\[
Canonical(X)=tuple(sorted(X,\ key=UTF8Bytes))
\]

集合字段合法当且仅当：

\[
ValidIDs(T,C)=ExactTuple(T)
\land ExactStringItems(T)
\land T=Canonical(T)
\land |T|=|set(T)|
\land set(T)\subseteq C
\]

`ExactTuple` 与 `ExactStringItems` 均拒绝 subclass、custom sequence、lazy iterator 和隐式 coercion。

字体档位目录必须先满足：

\[
ValidFontCatalog(F)=ExactTuple(F)
\land |F|\ge1
\land Unique(F)
\land 1.0\in F
\land \forall f\in F:\ type(f)=float\land isfinite(f)\land f>0
\]

首发 \(F=(1.0,1.25,1.5)\)。Root validator 只能引用已通过该 catalog gate 的 \(F\)。

### Root and Manifest Validation

令 \(K_{root}\) 为冻结的八个 top-level keys：`schema_version`、`catalog_generation_id`、`collection_epoch_id`、`achievement_ids`、`seen_achievement_ids`、`ending_ids`、`memory_ids`、`settings`；`settings` 的 key set 必须恰为 `font_scale`、`high_contrast`、`reduced_motion`、`flash_effects_enabled` 与 `screen_shake_enabled`。

\[
\begin{aligned}
ValidRoot(S)=&\ ExactDict(S)
\land Keys(S)=K_{root}\\
&\land type(S.schema\_version)=int
\land S.schema\_version=2\\
&\land type(S.catalog\_generation\_id)=str\\
&\land S.catalog\_generation\_id=\text{"persist\_catalog:v2"}\\
&\land type(S.collection\_epoch\_id)=int
\land S.collection\_epoch\_id\ge0\\
&\land ValidIDs(S.achievement\_ids,C_A)\\
&\land ValidIDs(S.seen\_achievement\_ids,C_A)\\
&\land set(S.seen\_achievement\_ids)\subseteq set(S.achievement\_ids)\\
&\land ValidIDs(S.ending\_ids,C_E)\\
&\land ValidIDs(S.memory\_ids,C_M)\\
&\land ExactDict(S.settings)\\
&\land Keys(S.settings)=\{font\_scale,high\_contrast,reduced\_motion,flash\_effects\_enabled,screen\_shake\_enabled\}\\
&\land type(S.settings.font\_scale)=float\\
&\land isfinite(S.settings.font\_scale)\\
&\land S.settings.font\_scale\in F\\
&\land type(S.settings.high\_contrast)=bool\\
&\land type(S.settings.reduced\_motion)=bool\\
&\land type(S.settings.flash\_effects\_enabled)=bool\\
&\land type(S.settings.screen\_shake\_enabled)=bool
\end{aligned}
\]

因为 `bool` 是 `int` 的 subclass，`schema_version` 与 `collection_epoch_id` 必须使用 `type(value) is int` 验证；`True` 与 `False` 均不得通过。Unknown/missing keys、extra nested keys、wrong type、NaN 与 ±∞ 均固定失败。

上式不是可任意重排的短路表达式。Runtime validator stage 固定为：root exact type → top-level exact key set → scalar exact types → settings exact type/key set → collection exact container/item types → catalog generation/membership → canonical order/uniqueness → scalar value/range。任一 stage 失败立即返回冻结 error code，不访问后续或 unknown payload；protocol bomb invocation 与 validator-thrown exception counts 均为 0。

Ownership manifest 有效条件：

\[
\begin{aligned}
ValidManifest(M)=&\ ExactTuple(M)
\land |M|=12\\
&\land M.root\_field\_name=\text{"sys\_persist\_state"}\\
&\land ExactNonemptyString(M.manifest\_generation\_id)\\
&\land M.schema\_version=2\\
&\land M.catalog\_generation\_id=\text{"persist\_catalog:v2"}\\
&\land M.leaf\_field\_count=12\\
&\land M.leaf\_field\_paths=CanonicalLeafPaths\\
&\land |M.exact\_type\_ids|
=|M.semantic\_owner\_system\_ids|\\
&=|M.allowed\_requester\_system\_ids|
=|M.merge\_policy\_ids|\\
&=|M.reset\_policy\_ids|
=M.leaf\_field\_count=12\\
&\land AllParallelItemsExactNonemptyStrings(M)\\
&\land UniqueStorageWriter(M)=SYS\text{-}PERSIST\\
&\land AllOwnersAndPoliciesResolve(M)
\end{aligned}
\]

### Batch Update

以下集合公式只在 batch 已通过 exact order/length/duplicate preflight 后使用；不得通过把 raw requests 转成 set 来接受重复输入。

对 unlock kind \(k\in\{achievement,ending,memory\}\)：

\[
Added_k=Requested_k\setminus Existing_k
\]

\[
Candidate_k=Canonical(Existing_k\cup Added_k)
\]

Setting update 只替换 batch 明确包含且已验证的规范叶字段；未请求字段保持深值不变。完整 candidate：

\[
CandidateSeen=Canonical(ExistingSeen\cup SeenToAdd)
\quad\land\quad CandidateSeen\subseteq Candidate_{achievement}
\]

\[
Changed=(Candidate\ne Current)
\]

结果函数：

\[
Result=
\begin{cases}
PERSISTENCE\_UNAVAILABLE, & root\ invalid/marker/commit\ unknown\\
REJECTED\_INVALID, & request/manifest\ invalid\\
REJECTED\_REENTRANT, & operation\ mutex\ already\ held\\
STALE\_DRAFT\_CONFLICT, & settings\ne settings\_base\\
DUPLICATE\_NOOP, & \neg Changed\\
APPLIED\_FLUSHED, & Changed\land DurableSuccess\\
PERSIST\_FLUSH\_FAILED\_SAFE, & Changed\land ProvenNoDiskWrite\\
COMMIT\_STATUS\_UNKNOWN, & Changed\land \neg DurableSuccess\land \neg ProvenNoDiskWrite
\end{cases}
\]

结果优先级按上表从上到下冻结；例如 recovery/commit-unknown root 总是 `PERSISTENCE_UNAVAILABLE`，不被 request defect 覆盖。只有 `APPLIED_FLUSHED` 可以生成 presentation notification 或 achievement projection。一个 batch 中 root 已存在的 duplicate 与 new requests 可共存；candidate 只加入 new IDs。任一 raw batch 内 duplicate 或其他非法 request 使整批 `REJECTED_INVALID`，不应用其余成员。

### Merge

三个相同 schema/generation 的合法 callback 根状态先选择最大收藏时代：

\[
e=\max(old.epoch,new.epoch,current.epoch)
\]

\[
Sources_e=\{r\in(old,new,current)\mid r.epoch=e\}
\]

\[
MergeUnlocks_k=Canonical(\bigcup_{r\in Sources_e} r_k)
\]

\[
MergeSeen=Canonical(\bigcup_{r\in Sources_e} r.seen\_achievement\_ids)
\]

并要求 `MergeSeen ⊆ MergeUnlocks_achievement`。项目设置采用 Ren’Py 已放入 `new` 参数的较新合法来源；项目不读取 raw age：

\[
MergeSetting(old,new,current)=new
\quad\text{iff}\quad
current.settings\in\{old.settings,new.settings\}
\]

任一输入非法、schema/generation 不同，或 current settings 同时不同于 old/new：

\[
Merge(old,new,current)=MERGE\_RECOVERY\_MARKER
\]

对 unlock collections，三源 merge 必须满足 permutation、grouping 与 idempotency：

\[
A\cup B=B\cup A
\]

\[
(A\cup B)\cup C=A\cup(B\cup C)
\]

\[
A\cup A=A
\]

设置合并不要求值交换律；确定性定义为相同 ordered callback triple 必须得出相同结果。Equal-age 情况由 Ren’Py 决定 old/new 参数位置，项目不另行识别或覆盖。

### Achievement Projection

\[
BackendGranted=\{id\in C_A\mid achievement.has(id)\}
\]

\[
ProjectionMissing=RootAchievementIDs\setminus BackendGranted
\]

系统只对 `ProjectionMissing` 按 canonical 顺序调用 `achievement.grant()`，且：

\[
RootAchievementIDs'=RootAchievementIDs
\]

投影永远不能改变 canonical root。产品弹窗条件：

\[
Popup(id)=1
\iff id\notin Root_{before}
\land id\in Root_{after}
\land Result=APPLIED\_FLUSHED
\]

启动 repair、projection retry、load、rollback、new game 与 duplicate request 的 `Popup(id)=0`。

### Persistence Invariance

对操作集合：

\[
O=\{load,rollback,blocking\_exit,explicit\_new\_game\}
\]

每次操作都必须满足：

\[
\forall o\in O,\ DeepValue(P_{after(o)})=DeepValue(P_{before(o)})
\]

其中 \(P\) 是由 generation 匹配、`leaf_field_count=12` 的 nonempty ownership manifest 枚举并复制的全部规范叶字段。只比较选定字段、空 manifest 或 stale generation 不构成不变性证据。

### Bounds and Complexity

\[
|achievement\_ids|\le11,\quad
|seen\_achievement\_ids|\le|achievement\_ids|,\quad
|ending\_ids|\le6,\quad
|memory\_ids|\le7
\]

\[
N=|achievement\_ids|+|ending\_ids|+|memory\_ids|\le24
\]

令 \(S=|seen\_achievement\_ids|\le11\)，\(R=|unlock\_requests|\le24\)。Batch validator 必须先以 \(O(R)\) exact length/order/duplicate preflight 拒绝超限输入，再执行 candidate canonicalization。Full root validation 上界为 \(O((N+S)\log\max(2,N+S))\)，batch update 为 \(O((N+S+R)\log\max(2,N+S+R))\)，三源 merge 为 \(O((N+S)\log\max(2,N+S))\)，额外内存为 \(O(N+S+R)\)。Achievement projection 最多检查11个批准ID。磁盘flush与backend I/O延迟不包含在该纯计算上界内，必须由独立engine benchmark与failure-injection protocol计量。

## Edge Cases

### Root and Catalog Integrity

- **If fresh install has no product root**：创建完整 schema-v2 concrete default；不读取或迁移旧平铺字段。
- **If root 为 `None`、wrong exact type 或含 missing/extra top-level/nested key**：进入 `PersistenceSafeRecovery`；不得补字段后继续。
- **If `schema_version` 为 `True`、`False`、字符串 `"2"`、float、subclass 或其他非 exact int**：root validation 固定失败。
- **If collection 含 unknown ID、重复项、非 canonical ordering、wrong item type、custom tuple/string subclass**：整根失败；不得过滤坏成员后保留其余数据。
- **If `font_scale` 为 NaN、±∞、非 exact float、越界或不属于批准档位**：整根失败；recovery surface 使用不写入 persistent 的安全显示默认值。
- **If catalog generation 不同**：不猜测 ID rename、delete、split 或 kind change；等待独立 migration ADR。
- **If catalog 删除、改名或改变任一 ID 的 kind/owner**：必须提升 generation；不得让旧 membership 静默消失或跨集合移动。

### Requests and Completion Boundaries

- **If request 在 catalog 声明的 completed-event boundary 之前提交**：整批 `REJECTED_INVALID`；root assignment、flush、projection 与 popup 调用数均为 0。
- **If batch 同时包含 duplicate 与 new requests**：只加入 new IDs，但整批仍只执行一次 root replacement 与一次 canonical flush。
- **If batch 任一成员的 owner、ID、kind、event reference、checkpoint 或 generation 非法**：整批拒绝，不部分应用合法成员。
- **If ending 只执行 `commit_ending_entry`，但尚未抵达 `commit_ending_completion`**：request count 为 0；退出、rollback 或 load 均不得产生 ending membership。
- **If ending 在 `commit_ending_completion` 成功后解锁，随后 rollback 到 ending completion 之前**：跨周目解锁保持；当前局 ending lifecycle/完成事件按 rollback 恢复，两者不得互相推导。
- **If 玩家加载 ending entry 或 chapter completion 之前的 per-run save**：既有合法 persistent unlock 保持，但不重放 popup，也不把当前局标为已完成。
- **If 同一 completed event 经 rollback 后再次抵达并提交同一 ID**：返回 `DUPLICATE_NOOP`。
- **If 多个系统在同一 stable checkpoint 产生解锁**：orchestrator 必须合成一个 batch；不得依赖多个写入的偶然顺序。
- **If canonical persistence operation 正在 validation、replacement 或 flush，另一个 request 重入**：后者 API entry count 为 1、operation-body entry count 为 0，同步返回 `REJECTED_REENTRANT`；首个操作继续，queue length 为 0且结束后不回放。需要共同提交的内容必须由 caller 预先 batch。

### Flush and Process Failure

- **If validation 或 candidate construction 失败**：root 深值、backend 与 presentation queue 均不变。
- **If engine adapter 证明 `renpy.save_persistent()` 在任何磁盘写入前失败**：恢复当前进程的 previous root，返回 `PERSIST_FLUSH_FAILED_SAFE`，不执行 projection，不显示成功或解锁 popup。
- **If `renpy.save_persistent()` 抛出、返回未文档化结果或在 durability boundary 中断，且不能证明 pre-write failure**：返回 `COMMIT_STATUS_UNKNOWN`，进入 blocking recovery；不得恢复后继续接受其他写入。
- **If canonical root flush 成功后、achievement projection 前应用退出**：root 已是权威；下次启动单向修复 backend，不补发 popup。
- **If projection 只成功一部分**：已成功 backend grants 保持，缺失项在下次 repair 重试；root 深值不变。
- **If backend 已有某 achievement 但 root 没有**：不得反向导入产品状态，也不得因此显示 Journal/Gallery unlock。
- **If backend 被清除而 root 仍含 achievement**：下次 startup/checkpoint repair 可重新 grant，但不得显示新解锁通知。
- **If 进程在 persistent serialization、temporary write 或 replacement boundary 中断**：磁盘最终状态只能是完整 previous root 或完整 candidate root；任何 partial root、supported-but-mixed leaf state 或丢失旧根均失败。重启后 previous 进入 replay-required completion path，candidate 进入 silent projection convergence；两者均不补发普通 unlock popup。Ren’Py 8.5.3 engine evidence 未证明该终态前，implementation readiness 保持 provisional。

### Merge

- **If old/new/current 均为合法同 schema/generation root，且 current settings 等于 old 或 new**：三类 unlock collections 取三源并集，项目设置取 `new`；外部 merge 不产生 popup。
- **If 任一来源非法**：不得从该来源选择性提取“看起来合法”的 unlocks 或 settings。
- **If 任意来源 generation 不同**：callback 返回 exact merge recovery marker，不合并、不迁移、不宣称保留任一来源的 old IDs。
- **If engine 将 equal-age sources 传入 callback**：项目只消费既定 old/new 参数位置；相同 ordered triple 的输出必须一致，不读取不存在的 equal-age flag。
- **If current settings 同时不同于 old/new**：视为 operation-mutex/adapter contract violation，返回 merge recovery marker。
- **If merge 在 Journal、Gallery 或 achievement list 打开期间发生**：先完整验证并原子替换 detached read model，再刷新 interaction；不得显示半合并列表或让旧焦点指向已不存在的行。

### Save, Load, Rollback, and New Game

- **If 执行 supported/unsupported/corrupt per-run load、rollback、blocking exit 或 explicit new game**：ownership manifest 的 12 个叶字段全部保持深值不变；只有明确 collection reset 可以递增 epoch并清收藏。
- **If per-run save 损坏或不兼容**：不得清除、修复、迁移或从 save payload 重建 persistent。
- **If persistent root 损坏**：不得影响 resolver、axes、history、ending lifecycle 或 per-run state；collection reads、writes 与成功声明暂停。
- **If popup queue、当前 focus、notification animation 或 projection repair 正在运行**：这些 transient 状态不进入 canonical root，也不随 persistent merge、save slot 或 rollback 恢复。

### Reset and Safe Recovery

- 首发普通 Settings、Journal 与 Gallery 不提供按类别删除 unlocks，也不提供单项 revoke。
- 合法 root 的“重置收藏进度”将 `collection_epoch_id` 恰加 `1`，清除 `achievement_ids`、`seen_achievement_ids`、`ending_ids`、`memory_ids` 及 Ren’Py achievement progress；必须原样保留五项 project settings。首发 Settings 不提供独立“恢复显示设置默认值”入口；未来若增加，必须是与 collection reset 分离的明确 project-setting batch。
- `PersistenceSafeRecovery` 不允许从 invalid root 选择性抢救字段。由于 invalid root 的 settings 也不可信，recovery 使用不写 persistent 的 exact temporary profile `(font_scale=1.5, high_contrast=true, reduced_motion=true, flash_effects_enabled=false, screen_shake_enabled=false)`；reset 成功重启后先进入可键盘/self-voicing完成的 accessibility setup，再进入普通 collection UI。
- Collection reset 是可跨重启识别的 operation state machine：`Idle → Confirmed → ClearingProduct → ClearingBackend → RestartPending → Verified`；任一 exception 或 hard kill 进入 `ResetRecovery`。若 engine surface 无法提供 durable phase marker 与双侧可恢复终态，则 player-facing reset 保持隐藏。
- 获批 adapter 如需 durable phase，只能把同一 `persistent.sys_persist_state` 暂时替换为 exact built-in reset marker `("RESET_RECOVERY", phase_id, next_collection_epoch_id, preserved_font_scale, preserved_high_contrast, preserved_reduced_motion, preserved_flash_effects_enabled, preserved_screen_shake_enabled, "persist_catalog:v2")`；不得新增第二个 product persistent field。Startup classifier 在 defaults/root validation 前识别 marker。若 engine clear surface 会在 backend 尚未确定清除时删除该 marker，且无法原子完成或可靠重建 phase，则该 adapter 不获批。
- Reset 成功必须清除三类 membership、seen 与 backend progress，写入递增后的 epoch、保留合法 settings、重新启动并验证 fresh collections + preserved settings；不得把只清 product 或 backend 一侧视为 supported success。Reset 后旧 save/run epoch 固定失配，成就求值保持禁用，直到玩家显式 New Game 把当前 epoch 复制进新 run envelope。
- 使用 `persistent._clear(progress=True)`、`achievement.clear_all()` 或等价 engine surface 前，必须通过 Ren’Py 8.5.3 fixture 验证它们对 product root、achievement progress、engine preferences、双 persistent storage locations、失败注入及 defaults reapplication 的 exact 行为。若 `_clear` 会清 settings，adapter 必须只在已验证的 session-local detached settings copy 可安全重建时执行，否则不得使用该 surface。
- Reset surface 必须明确说明只清除收藏进度并保留显示/无障碍设置，提供取消与退出；不得显示内部 schema、generation、字段名、稳定 ID、隐藏条件或结局 predicate。

## Dependencies

### Dependency Matrix

| Dependency | Strength / Direction | Required Contract | Owner / Current Effect |
|---|---|---|---|
| Ren’Py 8.5.3 | Hard runtime / Engine → SYS-PERSIST | exact built-in default construction、`renpy.register_persistent(old,new,current)`、`renpy.save_persistent()`、achievement API、persistent reset | Pinned；atomic disk terminal、callback marker round-trip、grant durability 与 reset exact behavior 仍需 engine evidence |
| Game Concept | Hard design / Concept → SYS-PERSIST | 多周目收藏、悲剧同等完整、完全离线、无隐藏数值提示 | Approved |
| ADR-0002 | Hard architecture / ADR → SYS-PERSIST | rollback/persistent boundary、completed-event grant、idempotency、coarse flush、无外部 JSON 主存储 | Accepted |
| Master Architecture / Control Manifest | Hard bidirectional | 单一根状态、ownership manifest、safe recovery、achievement projection 与 module ownership | Active；implementation 前需同步 |
| SYS-STATE | Explicit boundary / No data flow | 五轴与 ordered history 不跨周目 | Approved；不得接收 persistent input |
| SYS-ENDING | Hard upstream output / SYS-ENDING → SYS-PERSIST | 唯一 terminal completion node 在完整 ending narration 后通过 `commit_ending_completion` 产生的 `ending_completion_event_record` 与 stable ending ID | Approved core；ADR-0006 已冻结 completion boundary |
| SYS-NARRATIVE | Hard upstream content / SYS-NARRATIVE → SYS-PERSIST | chapter completion、memory IDs、completed event IDs 与 stable checkpoints | In Revision；ending completion event 由 SYS-ENDING owner node 产生 |
| SYS-SAVE | Hard bidirectional boundary | 消费 12-leaf manifest；证明 load/rollback/exit/new-game invariance；New Game 将当前 epoch 复制到 rollback-owned run envelope；为每个 persistence completion boundary 提供可重放的 pre-completion checkpoint | In Revision；本 GDD 是关闭 `SAVE-Q5` 与 commit-unknown replay 的 normative input |
| SYS-ACHIEVE | Hard downstream semantic owner / SYS-ACHIEVE → SYS-PERSIST | 11项独立成就 candidate、epoch校验、seen mark与session-only presentation | In Revision；阻止 achievement integration |
| SYS-ACCESS | Hard downstream/bidirectional | 拥有五项项目设置语义、engine font/contrast authority以及 recovery/reset accessibility | Designed；full re-review pending，阻止 settings 与 recovery UI lock |
| SYS-JOURNAL | Downstream read-mostly / SYS-PERSIST ↔ SYS-JOURNAL | Detached product snapshot、namespaced IDs、safe empty/recovery state；Journal receipt-supported mark-seen caller | In Revision；2026-08-03 full-review amendment待re-review |
| SYS-GALLERY | Downstream read-only / SYS-PERSIST → SYS-GALLERY | Spoiler-safe ending/memory/gallery unlock state | Not Started |
| SYS-TEST | Hard verification / SYS-PERSIST → SYS-TEST | Schema、merge、failure injection、projection、invariance、performance evidence | Not Started；阻止 implementation acceptance |
| SYS-BUILD | Hard release / SYS-PERSIST → SYS-BUILD | Manifest/catalog generation 与 source hash 匹配；排除 test fixtures | Not Started；阻止 release |
| Migration ADR | Conditional hard gate | 每个公开 source→target 版本的 migration、failure、rollback 与 support window | 当前不存在；首发不迁移旧开发 persistent |

### Interface Boundaries

- 只有 SYS-PERSIST 可以 validation 后 assignment、flush、merge、reset 或 migrate canonical root。
- SYS-ENDING、SYS-NARRATIVE、SYS-ACHIEVE 与 SYS-ACCESS 只能提交 catalog-authorized request，不得直接读写 `persistent.sys_persist_state`。
- SYS-SAVE 只能用 nonempty generation-matched manifest 枚举 snapshot 并验证不变性；不得从 per-run save 恢复、修复或重建 persistent。
- SYS-JOURNAL 与 SYS-GALLERY 只消费 detached read-only snapshot，不访问 achievement backend、slot metadata、axes、history、token、qualification 或 resolver；Journal mark-seen request 只携带receipt支持的stable IDs，不扩大读取权。
- Ren’Py engine preferences 保持在 engine-owned namespace；只有 `font_scale`、`high_contrast`、`reduced_motion`、`flash_effects_enabled` 与 `screen_shake_enabled` 五个项目自定义设置进入 product root。
- Imported Python 可验证 detached exact built-ins 或返回 detached candidate，不得持有 live persistent root、Ren’Py store reference 或 mutable module cache。
- Achievement backend 不得成为 product UI、叙事、ending logic、unlock condition 或 root migration 的反向依赖。

### Required Ordering

1. 批准 SYS-PERSIST GDD。
2. 同步 ADR-0002、Master Architecture、Control Manifest 与 Entity Registry。
3. 实现 root schema、validator、ownership manifest、batch API、merge 与 projection。
4. SYS-ACHIEVE 和 SYS-ACCESS 分别冻结 condition request 与 project-setting interfaces。
5. SYS-NARRATIVE 接入 chapter completion checkpoints；SYS-ENDING 接入已冻结的 terminal completion node 与 `commit_ending_completion`，不得复用 entry commit。
6. SYS-JOURNAL、SYS-GALLERY 接入 detached read-only snapshot。
7. SYS-SAVE、SYS-TEST 完成 invariance、failure injection、merge、reset 与 performance evidence。
8. SYS-BUILD 验证 generation、manifest/source hashes 与 test-asset exclusion。

### Bidirectional Consistency Requirements

- Systems index 中 SYS-TEST 的依赖必须加入 SYS-PERSIST，并将 persistent integration evidence 设为硬验收输入。
- SYS-SAVE 的 `SAVE-Q5` 只有在 ownership manifest 非空、generation 与 `leaf_field_count=12` 匹配、foreign-write scan 及四类 operation invariance tests 全部通过后才能关闭。
- Architecture module map 应新增 `game/11_persistence.rpy`；现有 `game/11_achievements.rpy` 不再拥有平铺 persistent 字段或 direct flush。
- ADR-0002、Master Architecture 与 Control Manifest 必须把旧的 “achievement.grant → flat persistent set → optional flush” 改为 “owner completion assertion → SYS-PERSIST batch → durable flush → backend projection/presentation”，并登记 merge recovery marker 与 commit-unknown blocking flow。
- 当前 implementation 的 `PROLOGUE` memory ID、过早 `CHOICE_ASK_FIRST` grant 及 hidden metadata 偏差属于后续实现/内容修正；它们不得进入首发 persistent catalog。
- SYS-NARRATIVE 未批准前，可完成 schema、validator、merge 与 synthetic engine fixtures，但 production completed-event catalog 及 checkpoint integration 保持 provisional。
- SYS-ACHIEVE 未批准前，可完成 achievement storage 与 projection framework，但不得宣称11项 condition/seen integration完成。
- 改变12个 leaf fields、canonical ID membership、owner、merge/epoch policy 或 root authority，必须同步修订本 GDD、ADR/Architecture、Control Manifest、Entity Registry、SYS-SAVE manifest fixtures 与 migration policy。

## Tuning Knobs

### Adjustable Parameters

| Parameter | Launch Value | Owner | Adjustment Boundary |
|---|---|---|---|
| `font_scale_options` | `(1.0, 1.25, 1.5)` | SYS-ACCESS | 只能增加通过 1280×720 全 UI 验证的新档位；删除已发行档位需要 migration |
| `font_scale_default` | `1.0` | SYS-ACCESS | 只影响 fresh install 与 invalid-root rebuild；collection reset 不得覆盖已有合法值 |
| `high_contrast_default` | `False` | SYS-ACCESS | 只影响 fresh install 与 invalid-root rebuild；collection reset 不得覆盖已有合法值 |
| `reduced_motion_default` | `False` | SYS-ACCESS | 只影响 fresh install 与 invalid-root rebuild；recovery temporary profile 固定为 `True` |
| `flash_effects_enabled_default` | `False` | SYS-ACCESS | 只影响 fresh install 与 invalid-root rebuild；recovery 同样固定为 `False` |
| `screen_shake_enabled_default` | `False` | SYS-ACCESS | 只影响 fresh install 与 invalid-root rebuild；recovery 同样固定为 `False` |
| `unlock_flush_policy` | 每个 stable completion checkpoint 一次 | SYS-PERSIST | 不得延迟到应用退出；同 checkpoint 多项解锁必须 batch |
| `settings_flush_policy` | 每次明确 setting commit 一次 | SYS-PERSIST + SYS-ACCESS | 允许 transient preview；离开设置界面前必须 commit 或 cancel |
| `projection_repair_points` | startup validation 后、含新增 achievement 或已知 projection 缺口的 successful flush 后 | SYS-PERSIST | ending/memory/seen-only batch 不扫描11项；不得在 dialogue frame 或 screen render 中每帧扫描 |
| `projection_attempt_cap` | 每个 achievement 每个 interaction 最多一次 | SYS-PERSIST | 防止失败循环；下一个 stable checkpoint 可重试 |
| `recovery_display_defaults` | high contrast on、font scale `1.5`、reduced-motion on、flash off、shake off | SYS-ACCESS | 只用于 invalid-root/commit-unknown/reset-recovery surface，不写入 persistent |
| `reset_confirmation_steps` | `2` | SYS-ACCESS | 不得降为单次 activation 立即删除 |

### Interaction Rules

- 增加 font scale 档位必须重跑全部 persistent setting、Journal、Gallery、safe recovery 与 blocking UI 的 1280×720 layout/accessibility tests。
- 已发行 font scale 值必须继续被 validator 接受，直到 migration 明确转换并具有逐版本 fixtures。
- Setting preview 不改变 canonical root；Apply 才产生一个 settings batch。Cancel 恢复 preview 前表现且 assignment/flush count 为 0。
- Unlock flush 不受 popup delay policy 影响：SYS-ACHIEVE 可以延迟表现，SYS-PERSIST 不得延迟 canonical durability。
- Synchronous flush 只能在 stable completion transition 已渲染静态 blocking-safe frame、玩家输入已 gated、下一段叙事尚未开始时执行；不得在 dialogue render、choice activation 或 animation frame 中调用。I/O blocking interval 与普通 rendered-frame time 是两个独立指标，不得用 16.6 ms frame budget 伪装或否决已声明的 bounded persistence wait。
- Projection repair frequency 只能影响 backend convergence time，不能改变 root membership、产品 UI 或 popup eligibility。
- 增加 achievement、ending 或 memory ID 必须提升 catalog generation；不得只扩大 validator allowlist。
- Batch member 上限由批准目录总量24固定，不是内容调参项。
- `reset_confirmation_steps` 只控制防误触交互；不得改变 collection reset 的三类 membership 全量清除、backend 双侧收敛、settings preservation、restart 和 post-reset validation 合同。

### Locked Invariants

以下不可作为调参修改：

- 单一 `persistent.sys_persist_state` authority；normal `READY` 状态只能是 canonical root，非-root值只允许本 GDD 冻结的 merge/reset recovery markers；
- schema v2 的12个规范叶字段及 exact types；
- SYS-PERSIST 是唯一 storage writer；
- 三类 unlock collections 已排序、唯一且只含批准 IDs；
- 产品 root 为权威，achievement backend 只作单向 projection；
- completed-event-only grant 与 duplicate request no-op；
- 合法 unlock 在 successful completion 后不受 load、rollback、blocking exit 或 new game 撤销；
- 五轴、history、token、qualification 与 ending predicate 不进入 persistent；
- 合法同 generation unlock merge 使用并集；
- Collection reset 清三类 membership并保留合法 accessibility settings；
- merge、repair、load、rollback 与 new game 不产生 popup；
- 不使用 network、cloud sync、player import、external JSON 主存储或 MultiPersistent；
- schema、catalog、ownership、merge 或 reset policy 变化必须经过 migration ADR。

## Visual/Audio Requirements

### Unlock Feedback

- SYS-PERSIST 本身不显示“保存成功”、flush、merge 或 projection 技术状态；正常持久化对玩家不可见。
- 新解锁 notification 只能来自一次成功的 `ABSENT → PRESENT → APPLIED_FLUSHED` canonical root transition。
- 唯一 persistence notification coordinator 根据 exact durable-result record 构造 `notification_group_id` 与逐 kind added IDs，再分别交给 SYS-ACHIEVE、SYS-ENDING、SYS-JOURNAL presenter；presenter 不允许自行 diff detached snapshot推导新解锁。
- Schema v2 不存在 ending/memory mirror achievements。同一 batch 有多个 kind 时仍只形成一个 notification group；多个 unsafe checkpoint groups由 session presenter在下一 authored safe boundary合并为一个summary。SYS-AUDIO只由完整group的唯一owner调用一次。
- Ending、memory 与 achievement 使用同等级别的视觉完成度，不得用颜色、光效、稀有度边框或音调暗示“最佳路线”。
- 悲剧结局的收藏卡不得使用损坏、失败、叉号、低清或未完成态视觉语言。
- 未解锁隐藏内容只显示获批中性 placeholder，不显示名称长度、图像轮廓、condition、五轴类别、token domain、路线门槛或 progress percentage。
- Merge、startup repair、projection retry、load、rollback、blocking exit 与 new game 均不显示新解锁 feedback。
- 任何 notification 动画必须支持 reduced-motion；关闭动画后仍可通过文本与非颜色 status icon 理解结果。

### Recovery Presentation

- `PersistenceSafeRecovery` 使用独立、克制的 local-progress error surface，不复用 per-run save corruption screen，也不显示当前剧情画面。
- 标题和说明只表达“本地收藏数据无法安全读取”，不得显示 schema、generation、field path、stable ID、achievement condition 或 ending 信息。
- 状态、主操作和 destructive operation 必须同时具有文本与非颜色 icon，不得只依赖红/绿区分。
- Recovery surface 使用 built-in Simplified Chinese safe copy、high-contrast-safe palette 与不依赖 persistent root 的字体尺寸。
- 缺少字体、图标、主题或本地化资产时使用 engine-safe fallback；不得因此自动 reset、尝试 partial recovery 或进入正常 collection UI。
- Collection reset 的第二次确认必须视觉上区分“取消”和“清除收藏进度（保留显示设置）”，默认 focus 位于取消。

### Audio and Silent-Safe Operation

- Unlock sound 是可选增强，不得成为唯一 feedback。
- 所有通知必须在 muted、music off、sound off 与 self-voicing 模式下保持可理解。
- 不同 endings 不得用 victory/failure cue 进行价值排序。
- Recovery 与 reset 不使用 alarm loop、突然高音量、持续声音压力或要求玩家依声定位的操作。
- Sound playback 遵循 engine-owned volume preferences，不进入 product root。
- Projection repair、merge、duplicate no-op、load、rollback 与 new game 的 notification audio call count 必须为 0。

### Asset Boundary

- SYS-PERSIST 不要求专属 CG、character animation、scene background 或 voice asset。
- 如使用 collection、locked、recovery 或 reset icons，必须采用 stable semantic asset names，并登记 source、license 与 self-voicing alternative text。
- 不得使用 official、source-unknown 或未经批准的《龙族》art、logo、font、music 或 sound asset。
- Journal/Gallery 的具体 card composition、animation duration 与 audio motif 分别交由后续 UX、UI 与 SYS-AUDIO 规格定义，但不得改变本节的状态、spoiler safety 与 value-neutral contracts。

## UI Requirements

### Surface Inventory

SYS-PERSIST 不拥有常规 collection browser，只提供状态、接口与以下基础 surfaces：

- `screen_persistence_safe_recovery`；
- `screen_confirm_collection_progress_reset`；
- Settings 中的 project-setting preview/commit/error state；
- 提供给 SYS-ACHIEVE、SYS-JOURNAL 与 SYS-GALLERY 的 detached read model。

正常运行不显示 persistence icon、dirty indicator、schema/generation 或“保存成功”提示。

### Detached Read Model

UI 只能读取一次 full validation 后生成的 detached exact-built-in snapshot，至少包含：

`status, snapshot_fingerprint, schema_version, catalog_generation_id, collection_epoch_id, achievement_ids, seen_achievement_ids, ending_ids, memory_ids, font_scale, high_contrast, reduced_motion, flash_effects_enabled, screen_shake_enabled`

`snapshot_fingerprint` 由完整 deep value 计算，只用于检测 UI draft stale，不进入 persistent、catalog 或玩家显示。`status` 只允许 `READY`、`COMMIT_STATUS_UNKNOWN`、`PERSISTENCE_SAFE_RECOVERY` 或 `RESET_RECOVERY`。Root update 或 merge 后，deep-equal snapshot 不替换、不请求 refresh；changed snapshot 在完整验证后替换恰一次并向主线程 UI bridge 请求 refresh 恰一次。UI 不得直接读取/写入 `persistent.sys_persist_state`，不得访问 backend 补充 membership，也不得在 screen-local cache 中推导、加入或去重 unlock。

### Settings Flow

1. 打开 Settings 时，从合法 `READY` snapshot 建立 transient draft，并保存 `settings_base=(font_scale,high_contrast,reduced_motion,flash_effects_enabled,screen_shake_enabled)` 与 base fingerprint。
2. 五项 project settings 允许即时 preview，但 preview 不改变 canonical root；字体与对比立即重排，三个效果开关只改变后续表现策略。
3. Apply 将全部变化作为一个 settings batch 提交；不得逐控件 partial commit。
4. External root update/merge 到达 clean draft 时直接刷新；到达 dirty draft 时，若 settings 仍等于 `settings_base`，只 rebase membership/fingerprint 并保留 preview；若 settings 已变化，进入 `STALE_DRAFT_CONFLICT`，禁用 Apply，要求玩家 Reload latest 或 Cancel。
5. `APPLIED_FLUSHED` 后才替换 read snapshot 并把 draft 标为 clean。
6. Cancel 恢复最新合法 snapshot 的表现，而不是过期 base；root assignment 与 flush count 均为 0。
7. `PERSIST_FLUSH_FAILED_SAFE` 时留在 Settings，恢复 previous root/read snapshot，显示中性本地设置保存错误，并提供 Retry 与 Cancel；`COMMIT_STATUS_UNKNOWN` 进入独立 blocking recovery，不允许在 Settings 内继续重试不同 draft。
8. Operation 进行时 Apply disabled 且不可聚焦；重复 activation 的 action-dispatch count 为 0，queue length 为 0。
9. 离开 Settings 前必须明确 Apply、Reload latest 或 Cancel，不允许 silent partial commit。

### Collection States

SYS-PERSIST 只提供 membership/seen/epoch，不决定卡片 copy、layout、order 或 spoiler treatment。成就下游 surface 必须区分：

- `UNLOCKED`；
- `UNLOCKED_UNSEEN`；
- `LOCKED_ABSENT`；
- `PERSISTENCE_UNAVAILABLE`。

状态映射由 nonpersistent、versioned `collection_visibility_catalog` 冻结；每项必须包含 `stable_id, kind, reveal_policy, unlocked_copy_key, count_policy, focus_policy, self_voicing_policy`。`achievement_catalog:v2` 的 11 项全部为 `ON_UNLOCK`：locked 不渲染、不占槽、不计总数、不可聚焦且不进入 self-voicing；membership 存在但 seen 不存在时显示“新记录”，seen 后显示“曾经走过”。Ending 与 memory collection 可以拥有各自不泄露剧情的 catalog，但不得重新镜像为 achievement IDs。

`PERSISTENCE_UNAVAILABLE` 不得伪装成“全部未解锁”，以免玩家误以为进度被清空。任何状态都不得显示 internal condition、axis、token、qualification、ending predicate、backend difference 或 catalog generation。

### Recovery and Reset Flow

- Invalid root 激活独立 `screen_persistence_safe_recovery`，normal Journal、Gallery 与 achievement list 不可进入。
- Recovery surface 的稳定出口至少包括返回主菜单与退出应用；玩家可从主菜单明确开始不依赖 collection state 的新游戏。
- Recovery 状态下全部 unlock/setting requests 返回 `PERSISTENCE_UNAVAILABLE`，不 assignment、不 flush、不 projection、不提示成功，也不建立 pending/backfill queue。
- Player-facing collection reset 入口只有在 Ren’Py 8.5.3 reset fixtures 与 crash-recovery matrix 全部通过后才显示、启用并进入 focus order；否则 surface 只提供安全非破坏性出口。
- Reset 第一次 activation 显示“清除收藏进度、保留显示与无障碍设置”的影响摘要；第二次 confirmation 才执行清除。两个层级默认 focus 均为 Cancel。
- Escape/right-click 在确认层只返回上一层，不执行 reset；在基础 recovery surface 不得返回 invalid collection screen。
- Reset operation 显示不可重复触发的 busy state；各 phase failure 或 hard-kill 后进入 `ResetRecovery`，只允许 Retry same reset、返回安全主菜单或退出。Reset success 后执行 full restart，验证 empty collections、preserved valid settings 与 cleared backend progress；reset failure 不进入 normal collection UI。
- 开始 persistence-unavailable 新游戏前必须明确提示本次完成结果不会加入收藏；确认与取消均可键盘到达。

### Input, Focus, Layout, and Accessibility

- 全部操作支持 mouse 与完整 keyboard navigation，不要求 hover、audio、animation、gamepad-only action 或 timed input。
- 1280×720 下，font scale `1.0`、`1.25`、`1.5` 的 Settings、recovery 与两个 reset confirmation layers 均不得重叠、裁切或把操作推出 viewport。
- Default/high-contrast、normal/reduced-motion、muted/self-voicing 组合均须覆盖。
- Screen-reader reading order 固定为说明 → 当前 availability/effect → safe operation → destructive operation；keyboard tab order 只包含 interactive controls，按 safe operation → destructive operation 排列。Modal 必须 trap focus，关闭后恢复到 opener；destructive action 不得成为 default focus。
- Focused、disabled、selected、error 与 destructive states 均须有非颜色差异。
- Self-voicing 读取 operation effect、当前 persistence availability 与 data-loss scope；不朗读 internal ID、schema、field path、condition 或 predicate。

### Existing Implementation Boundary

- `game/screens.rpy` 当前直接读取 `persistent.memories_unlocked` 与 `persistent.achievements_unlocked`；implementation 必须改为消费 detached snapshot。
- `game/11_achievements.rpy` 当前五个 flat persistent fields、direct collection assignments 与 direct flush 必须迁移到 SYS-PERSIST API。
- `achievement_popup_queue` 保持 rollback-owned/per-run presentation state，不进入 canonical root、manifest 或 merge。
- 在上述重构、source scan 与 integration tests 完成前，现有 screen/helper 只视为 prototype evidence，不构成 SYS-PERSIST acceptance。

## Acceptance Criteria

以下 60 条标准必须由 `UT_ENGINE`、`UT_PURE`、`INSTR`、`STATIC` 或 `BRANCH` 证据验证。计数、深值、source ownership、layout 与 timing 不得由玩家肉眼判断代替。

每个 evidence artifact 必须遵守 `persist_evidence_contract:v1`：记录 runner/tool 与版本、Ren’Py/Python/build IDs、fixture manifest generation、输入 fixture IDs、source/catalog hashes、assertion/case/raw-sample counts、完整原始日志、exit code、PASS/FAIL，以及生成时间。组合 evidence 必须逐类列出各自能证明的断言；`STATIC` 不得单独宣称证明 runtime writer、I/O durability、screen reachability 或 timing。Release gate 只接受 generation/hash 与当前 source 完全匹配且 exit code 为 0 的 PASS artifact；缺失、stale、空 manifest、仅有总结或人工勾选均固定失败。

### Schema and Manifest — 8

| ID | Evidence | Criterion |
|---|---|---|
| `PERSIST-SCHEMA-001` | `UT_ENGINE` | **GIVEN** clean Ren’Py 8.5.3 persistent storage，**WHEN**以 pure builder default 首次启动、flush、full restart，**THEN**每一阶段的 `persistent.sys_persist_state` 都是 valid schema-v2 exact built-in root（root/settings 均 `type is dict`），epoch为0、四个collection/seen tuples为空、settings为`False/1.0`，且 normative leaf count 恰为12。 |
| `PERSIST-SCHEMA-002` | `UT_PURE` | **GIVEN**含全部11 achievement IDs、其 seen 子集、6 ending IDs、7 memory IDs、最大合法 epoch和每个批准 font scale 的 fixtures，**WHEN**full validation，**THEN**全部通过且 detached deep values 与输入相等。 |
| `PERSIST-SCHEMA-003` | `UT_PURE` | **GIVEN**逐一 missing/extra top-level key、missing/extra settings key、wrong root/settings container fixtures，**WHEN**validation，**THEN**每案在 key/container stage 固定失败且不读取未知 value payload。 |
| `PERSIST-SCHEMA-004` | `UT_PURE + INSTR` | **GIVEN**`schema_version` 为 bool/float/string/subclass，generation 为 wrong type，collection/container/item 为 wrong exact type或protocol bomb，**WHEN**validation，**THEN**每案抛出规定 type error、有限步终止且 bomb invocation count 为 0。 |
| `PERSIST-SCHEMA-005` | `UT_PURE` | **GIVEN**三类 collection 分别含 unknown ID、duplicate、noncanonical order、wrong kind ID、empty/nonempty合法边界，**WHEN**validation，**THEN**只有 canonical approved subsets 通过；其余不被过滤、排序后接受或跨集合移动。 |
| `PERSIST-SCHEMA-006` | `UT_PURE` | **GIVEN**`font_scale` 为每个批准档位及 NaN、±∞、negative、wrong type、未批准 finite float，且四项布尔设置分别为 exact bool/wrong type，**WHEN**validation，**THEN**只接受批准 exact values。 |
| `PERSIST-SCHEMA-007` | `UT_PURE + STATIC` | **GIVEN**production ownership manifest 及逐字段 missing/extra/wrong-type/length-mismatch/duplicate/unresolved fixtures，**WHEN**按 staged manifest validator 验证，**THEN**仅 exact 12-field manifest tuple、12个 canonical leaf paths及其等长 type/owner/requester/merge/reset arrays、nonempty migration policy 全部解析的 manifest 通过；公式与实现都读取 `root_field_name`。 |
| `PERSIST-SCHEMA-008` | `UT_ENGINE + INSTR` | **GIVEN**valid canonical root 与同时填充的五个 legacy flat fields，**WHEN**生成 detached read snapshot，**THEN**snapshot 只来自 canonical root、无对象 alias，修改 snapshot 不改变 root，legacy field read count 为 0。 |

### Ownership and Isolation — 6

| ID | Evidence | Criterion |
|---|---|---|
| `PERSIST-OWN-001` | `STATIC` | **GIVEN**完整 production source manifest，**WHEN**扫描 root assignment、nested mutation、flush、merge registration、reset 与 migration calls，**THEN**仅批准的 SYS-PERSIST module/functions 命中；未解析 alias、reflection、wrapper 或 dynamic access 使构建失败。 |
| `PERSIST-OWN-002` | `UT_PURE + STATIC` | **GIVEN**manifest 中每个 leaf 与 requester fixtures，**WHEN**验证 owner matrix，**THEN**achievement/ending/memory/settings 只接受各自批准 requester，schema/generation 只接受 SYS-PERSIST。 |
| `PERSIST-OWN-003` | `STATIC` | **GIVEN**canonical root、manifest、save payload 与 runtime reads，**WHEN**扫描 axes、history、token、qualification、resource、ending predicate/record/lifecycle、reaction/payoff、popup/focus/notification，**THEN**这些字段、引用与反向依赖计数均为 0。 |
| `PERSIST-OWN-004` | `STATIC + UT_PURE` | **GIVEN**imported Python validators/builders，**WHEN**执行 callgraph、escape 与 mutation scan，**THEN**它们只接收/返回 detached exact built-ins，不持有 live persistent/store、Ren’Py object 或 mutable module cache。 |
| `PERSIST-OWN-005` | `STATIC` | **GIVEN**SYS-ACHIEVE、JOURNAL、GALLERY、ACCESS、SAVE 与 UI source，**WHEN**扫描 direct root/backend access，**THEN**消费者只经批准 request/snapshot/manifest API；product membership 不读取 `achievement.has()`、slot metadata 或 legacy fields。 |
| `PERSIST-OWN-006` | `STATIC + UT_ENGINE` | **GIVEN**release candidate 与 runtime writer instrumentation，**WHEN**比较 manifest、source scan 与 observed writes，**THEN**root/leaf field count、generation、writer/flush callsites 完全一致，flat product persistent field declaration count 为 0。 |

### Update and Flush — 10

| ID | Evidence | Criterion |
|---|---|---|
| `PERSIST-UPD-001` | `UT_ENGINE + INSTR` | **GIVEN**分别由专用 owner adapter 在真实完成边界后构造的一个新 achievement、ending、memory request，**WHEN**逐案提交，**THEN**对应 collection 仅增加目标 ID、其余11 leaves深值不变，每案replacement/flush各恰为1并返回公开结果`APPLIED_FLUSHED`；ending entry commit路径request count为0，只有唯一 completion node 的`commit_ending_completion`后为1。 |
| `PERSIST-UPD-002` | `UT_ENGINE + INSTR` | **GIVEN**任意 1–5 项合法 project-setting draft changes，**WHEN**Apply，**THEN**一次 settings batch 同时替换全部请求字段、unlock collections 不变、replacement/flush 各恰为 1。 |
| `PERSIST-UPD-003` | `UT_ENGINE + INSTR` | **GIVEN**同一 stable checkpoint 的多个合法跨 kind 新 unlock requests，**WHEN**唯一 coordinator 提交一个 exact batch，**THEN**所有目标同时出现、canonical ordering 正确、replacement/flush 各恰为1并只生成一个notification group；achievement mirror count为0。 |
| `PERSIST-UPD-004` | `UT_ENGINE + INSTR` | **GIVEN**目标 ID 已存在或 setting value 未变化，**WHEN**提交合法 request，**THEN**返回 `DUPLICATE_NOOP`，root、assignment、flush、projection、popup counts 分别为 unchanged/0/0/0/0。 |
| `PERSIST-UPD-005` | `UT_ENGINE + INSTR` | **GIVEN**一个 batch 同时含 duplicate 与 new IDs，**WHEN**提交，**THEN**只加入 new IDs，duplicate 不重复，整批 replacement/flush 各恰为 1。 |
| `PERSIST-UPD-006` | `UT_ENGINE + INSTR` | **GIVEN**empty/oversize/乱序 batch、batch 内 duplicate `(kind,id)`、conflicting setting pair，或任一成员含 wrong owner/kind/ID/event/checkpoint/type，**WHEN**提交，**THEN**在冻结 validator stage 返回 `REJECTED_INVALID`，包括合法成员在内均不应用，所有 side-effect counts 为 0；不得先 set 化去重。 |
| `PERSIST-UPD-007` | `STATIC + BRANCH + INSTR` | **GIVEN**每类专用 requester adapter、完整 production callgraph 及 before/after-completion source paths，**WHEN**执行，**THEN**caller 不能注入 owner ID，before paths 与 ending-entry paths 的 request/assignment/flush/popup counts 为 0，after paths 恰调用批准 request 一次，且 CFG 证明 completion dominates callsite。 |
| `PERSIST-UPD-008` | `UT_ENGINE + INSTR` | **GIVEN**stale/empty manifest、wrong request schema/generation 或 invalid/marker current root，**WHEN**提交 otherwise-valid batch，**THEN**manifest/request defects 在 candidate 前返回 `REJECTED_INVALID`；invalid/marker root 返回 `PERSISTENCE_UNAVAILABLE`；product/backend/presentation state 均不变。 |
| `PERSIST-UPD-009` | `UT_ENGINE + INSTR` | **GIVEN**canonical operation 正在 validation、replacement 或 flush，**WHEN**另一 request 重入，**THEN**首个 operation 继续，后者 API entry/body-entry counts 为 `1/0`、同步返回 `REJECTED_REENTRANT`、queue length 为 0且不在结束后回放。 |
| `PERSIST-UPD-010` | `UT_ENGINE + INSTR + BRANCH` | **GIVEN**valid changing batch，**WHEN**分别注入 proven pre-write failure、未分类异常及 serialization/temp-write/replace/process kill，**THEN**pre-write 案返回 `PERSIST_FLUSH_FAILED_SAFE` 且内存/磁盘均为 previous；其余返回/重启分类为 `COMMIT_STATUS_UNKNOWN`，冻结后续写入，磁盘只为完整 previous 或 candidate。重启后 previous 要求 replay same completion batch，candidate 静默 projection convergence；所有普通 popup counts 为 0。 |

### Achievement Projection — 5

| ID | Evidence | Criterion |
|---|---|---|
| `PERSIST-PROJ-001` | `UT_ENGINE + INSTR` | **GIVEN**新 achievement canonical flush 成功、backend 未授予及 success/false/exception grant fixtures，**WHEN**projection 执行，**THEN**目标 `achievement.grant()` 每 interaction 至多一次，root 深值不变；产品 popup eligibility 只来自已成功的 root transition 且恰为1，不随 backend result 重复或撤销，失败项保持 missing 供后续 silent repair。 |
| `PERSIST-PROJ-002` | `UT_ENGINE + INSTR` | **GIVEN**startup 时 root 含 backend 缺失 IDs，**WHEN**repair scan，**THEN**只对 `ProjectionMissing` 按 canonical order grant，root 不变且 popup/audio counts 为 0。 |
| `PERSIST-PROJ-003` | `UT_ENGINE + INSTR` | **GIVEN**projection 在若干 IDs 后失败，且后续 fixture 明确让剩余 grant 成功，**WHEN**下一 stable repair point 重试，**THEN**只调用仍缺失 IDs、每项每 interaction 至多一次；已成功项不重复，最终 backend 收敛到 root且 popup/audio counts 为0。 |
| `PERSIST-PROJ-004` | `UT_ENGINE + INSTR` | **GIVEN**backend 含 root 未包含的 approved/unknown achievements，**WHEN**startup、merge 与 read snapshot generation，**THEN**canonical root/product UI 不增加 membership，backend-to-root write count 为 0。 |
| `PERSIST-PROJ-005` | `UT_ENGINE + INSTR` | **GIVEN**duplicate request、merge、repair、load、rollback、blocking exit 与 new game，**WHEN**逐案执行，**THEN**achievement product popup 与 unlock audio counts 均为 0。 |

### Merge and Migration — 6

| ID | Evidence | Criterion |
|---|---|---|
| `PERSIST-MERGE-001` | `UT_PURE + UT_ENGINE` | **GIVEN**合法同 schema/generation 的 ordered `old/new/current` roots，current settings 等于 old 或 new，三源包含相同或不同 epoch 与相交/不相交 IDs，**WHEN**engine callback，**THEN**结果 epoch 为三源最大值，只有最大 epoch roots 的 memberships/seen 分别 canonical union，低 epoch 数据不复活，settings exact-equal `new`，结果通过 full validation，且项目不读取 raw age/equal-age/source identity。 |
| `PERSIST-MERGE-002` | `UT_PURE` | **GIVEN**seed/version 固定的三源合法 root generator，**WHEN**对 unlock portions验证 permutation、grouping、幂等并报告 case/shrink counts，**THEN**所有结果深值相等；settings 只对相同 ordered triple 要求确定。 |
| `PERSIST-MERGE-003` | `UT_ENGINE + INSTR` | **GIVEN**old/new/current 任一含 wrong type/key/ID/order/value，或 current settings 同时不同于 old/new，**WHEN**engine merge callback，**THEN**不抛异常、不选择性提取 leaf，返回 exact recovery marker；startup 在 default/root validation 前识别 marker，popup/projection/write counts 为 0。 |
| `PERSIST-MERGE-004` | `UT_ENGINE` | **GIVEN**三源任一 schema 或 catalog generation 不同，**WHEN**merge，**THEN**不 union、不 migrate、不宣称保存 old IDs，返回 exact marker并进入 `PERSISTENCE_SAFE_RECOVERY`。 |
| `PERSIST-MERGE-005` | `UT_ENGINE + UT_PURE` | **GIVEN**Ren’Py 为任意时间关系提供的 ordered `old/new/current` triples，**WHEN**重复运行 callback，**THEN**相同 ordered triple 每次得出同一合法 root或同一 marker；无项目 raw-age/equal-age API 调用。 |
| `PERSIST-MERGE-006` | `UT_ENGINE + INSTR` | **GIVEN**Journal/Gallery或clean/dirty Settings interaction打开期间收到deep-equal与changed合法external merge，**WHEN**merge完成，**THEN**deep-equal的snapshot replacement/UI bridge refresh counts均0；changed只在full validation后replacement=1、主线程refresh request=1；clean draft刷新，dirty draft在settings未变时rebase、已变时进入`STALE_DRAFT_CONFLICT`；callback内UI call、半合并frame、stale focus target、popup与audio counts均0。 |

### Save, Load, Rollback, and New-Game Invariance — 6

| ID | Evidence | Criterion |
|---|---|---|
| `PERSIST-INV-001` | `UT_ENGINE` | **GIVEN**nonempty generation-matched manifest、非空合法 root 与 supported manual/quick/auto saves，**WHEN**逐类 load，**THEN**12 owned leaves 与 load 前 deep snapshot 全部相等。 |
| `PERSIST-INV-002` | `UT_ENGINE + INSTR` | **GIVEN**unlock 后在 choice、reaction、payoff、chapter completion、ending entry 与 ending completion 两侧的 rollback fixtures，**WHEN**逐案 rollback/forward，**THEN**SYS-PERSIST 只断言12 owned leaves 始终等于操作前 snapshot且 writer/flush counts为0；per-run epoch、lifecycle 与 completion event 恢复由对应owner联合artifact证明。 |
| `PERSIST-INV-003` | `UT_ENGINE + INSTR` | **GIVEN**SYS-SAVE blocking safe flow 中的 main-menu exit 与外部 process harness 驱动的 OS quit，**WHEN**逐案执行并重启读取，**THEN**12 owned leaves 不变、root writer/flush/popup counts为0。 |
| `PERSIST-INV-004` | `UT_ENGINE + INSTR` | **GIVEN**合法非空 root，**WHEN**从主菜单或 blocking flow 明确开始新游戏，**THEN**12 persistent leaves深值不变且writer/flush counts为0；rollback-owned run envelope复制当前`collection_epoch_id`，save/semantic/ending lifecycle/completion event初始化只引用各owner联合artifact，不由SYS-PERSIST单独宣称。 |
| `PERSIST-INV-005` | `UT_ENGINE + INSTR` | **GIVEN**empty、unreadable、legacy、unsupported、corrupt 与 internal-failure per-run save fixtures，**WHEN**load/preflight/after-load failure route 执行，**THEN**无 fixture 清除、修复或重建 product root，assignment/flush/reset/rebuild counts 均为0。 |
| `PERSIST-INV-006` | `UT_ENGINE + INSTR` | **GIVEN**empty、partial、stale-generation 或 wrong-field-count manifest fixtures，**WHEN**运行 invariance checker，**THEN**证据固定失败；不得以比较 0 个或部分 fields 得到 PASS。 |

### Recovery and Reset — 7

| ID | Evidence | Criterion |
|---|---|---|
| `PERSIST-REC-001` | `UT_ENGINE + INSTR` | **GIVEN**root 的 key/type/schema/generation/ID/order/settings invalid cross-product、exact merge marker 或 exact reset marker，**WHEN**startup classifier/validation，**THEN**markers 在 default/root validation 前被识别，reset marker 进入 `RESET_RECOVERY`，其余进入 `PERSISTENCE_SAFE_RECOVERY`；resolver/per-run state reads/writes 为 0。 |
| `PERSIST-REC-002` | `UT_ENGINE + INSTR` | **GIVEN**safe recovery active，**WHEN**提交 unlock 或 setting request，**THEN**返回 `PERSISTENCE_UNAVAILABLE`，assignment/flush/projection/popup/pending/backfill counts 均为 0。 |
| `PERSIST-REC-003` | `UT_ENGINE + BRANCH` | **GIVEN**safe recovery active，**WHEN**选择 main menu、quit 或明确开始 persistence-unavailable new game，**THEN**各路径可达且不进入 collection screens；新游戏前展示无收藏写入警告并可取消。 |
| `PERSIST-REC-004` | `STATIC + UT_ENGINE` | **GIVEN**reset engine fixtures 或跨 phase exception/hard-kill recovery matrix 未全部 PASS，**WHEN**render recovery，**THEN**collection reset action visible/enabled/focusable 均为 false；两者 PASS 后才三者均为 true。 |
| `PERSIST-REC-005` | `UT_ENGINE + INSTR` | **GIVEN**reset action 可用，**WHEN**分别在第一/第二 confirmation 取消、Escape、right-click或确认，**THEN**只有第二层明确确认调用 reset 一次；其他路径 reset count 为 0，default focus 均为 Cancel。 |
| `PERSIST-REC-006` | `UT_ENGINE` | **GIVEN**非空 valid root/backend progress 与合法 nondefault accessibility settings，**WHEN**collection reset 成功，**THEN**`collection_epoch_id`恰加1，三类product memberships、`seen_achievement_ids`与backend progress清除，settings深值保留，应用full restart，root通过schema validation且旧epoch membership无法由旧save复活。 |
| `PERSIST-REC-007` | `UT_ENGINE + INSTR + BRANCH` | **GIVEN**`Idle→Confirmed→ClearingProduct→ClearingBackend→RestartPending→Verified` 各 boundary 的 exception/hard-kill，**WHEN**重启或 retry，**THEN**进入可识别 `ResetRecovery`，只允许 retry same reset/main menu/quit，不进入 normal collection UI、不声称成功；最终收敛为双侧已清+settings preserved，任何单侧状态都不是 supported success。 |

### UI and Accessibility — 7

| ID | Evidence | Criterion |
|---|---|---|
| `PERSIST-UI-001` | `UT_ENGINE + INSTR` | **GIVEN**Settings 中两项合法 draft changes 及期间仅 unlock membership 改变的 external update，**WHEN**rebase 后 Apply，**THEN**一个 settings batch 只替换请求 settings并保留新 unlock，一次 replacement/flush 后 snapshot 与控件一致，operation 中重复 Apply action-dispatch/queue counts 为 0。 |
| `PERSIST-UI-002` | `UT_ENGINE + INSTR` | **GIVEN**dirty preview 期间 external settings 改变，**WHEN**merge/update 到达，**THEN**进入 `STALE_DRAFT_CONFLICT`、Apply disabled；Reload latest 或 Cancel 恢复最新合法 snapshot，canonical root 不被 stale draft 覆盖，assignment/flush counts 为 0。 |
| `PERSIST-UI-003` | `UT_ENGINE + INSTR` | **GIVEN**setting Apply 分别得到 safe pre-write failure 与 commit-unknown，**WHEN**错误处理，**THEN**safe failure 留在 Settings并显示 Retry/Cancel、控件恢复 previous values；commit-unknown 进入 blocking recovery；两者均不显示 saved/success state。 |
| `PERSIST-UI-004` | `UT_ENGINE + INSTR` | **GIVEN**`achievement_catalog:v2` 与 `UNLOCKED/UNLOCKED_UNSEEN/LOCKED_ABSENT/PERSISTENCE_UNAVAILABLE` fixtures，**WHEN**render adapter执行，**THEN**每态精确匹配copy/icon/count/focus/self-voicing policy；locked不渲染/占槽/计数/聚焦/朗读，unseen显示“新记录”，unavailable不被计为zero progress，backend不补membership。 |
| `PERSIST-UI-005` | `UT_ENGINE + INSTR` | **GIVEN**1280×720、font scale `1.0/1.25/1.5`、default/high-contrast、normal/reduced-motion 的 Settings/recovery/two reset layers，**WHEN**layout，**THEN**`intersection_count=0`、`clipped_glyph_count=0`、`offviewport_action_count=0`。 |
| `PERSIST-UI-006` | `UT_ENGINE + BRANCH` | **GIVEN**mouse/keyboard、self-voicing 与全部 enabled actions/modals，**WHEN**分别遍历 reading order 与 interactive focus/activation graph，**THEN**每项可达、无需 hover/timed/audio input；tab order 只含 interactive controls并按 safe→destructive，modal trap/return 正确，destructive default-focus count 为 0。 |
| `PERSIST-UI-007` | `UT_ENGINE + INSTR` | **GIVEN**批准 copy catalog、muted/self-voicing 和全部 normal/error/locked/commit-unknown/reset-recovery states，**WHEN**capture rendered/self-voiced output，**THEN**snapshot/transcript exact-match，availability、operation effect、data-loss/preservation scope semantic tokens 各出现一次；internal schema/generation/field/ID、axis、token、qualification、predicate render/speech counts 均为 0。 |

### Performance and Build — 5

| ID | Evidence | Criterion |
|---|---|---|
| `PERSIST-PERF-001` | `UT_PURE` | **GIVEN**版本化 benchmark manifest、最大双侧/三源24-member roots、24-request batch、11-item seen set、最大epoch与最长合法 UTF-8 IDs、validation/update/merge 各5次warm-up与至少30次正式样本，**WHEN**nearest-rank统计，**THEN**artifact 保留全部 raw samples，每类 p95≤2 ms、max≤5 ms，allocation 不超过冻结预算；NaN、±∞、negative、missing/extra或不足样本固定失败。 |
| `PERSIST-PERF-002` | `UT_ENGINE + INSTR` | **GIVEN**静态 blocking-safe frame 已渲染、输入 gated、同一 protocol 与最大合法 changing batch，**WHEN**分别测量 request entry→durable result、同步 I/O unresponsive interval 与 I/O 前后普通 rendered frames，**THEN**artifact 保留全部 raw samples，end-to-end/I/O-wait p95≤250 ms、max≤500 ms；不含同步 I/O wait 的 rendered-frame p95≤16.6 ms、max≤33.2 ms。不得把 I/O wait 计入普通帧后同时声称两套阈值 PASS。 |
| `PERSIST-PERF-003` | `UT_ENGINE + INSTR` | **GIVEN**最大 root、cold/warm backend 与 absent/partial/full 11项 membership fixtures，**WHEN**startup validation + projection scan，**THEN**artifact 保留全部 raw samples，记录 `has_count=11`、grant count=missing count，已收敛时grant count=0；各场景p95≤冻结startup budget、max≤冻结max budget，且ending/memory/seen-only successful batch的repair scan count为0。 |
| `PERSIST-BUILD-001` | `STATIC + UT_ENGINE` | **GIVEN**release candidate，**WHEN**验证 root schema、manifest、catalog generation、source hashes、writer allowlist 与 archives，**THEN**全部匹配，legacy flat fields、test roots、spies、fault injectors、benchmark harness、pending ledger 与 unknown writer count 均为0。 |
| `PERSIST-BUILD-002` | `STATIC` | **GIVEN**SYS-PERSIST release gate，**WHEN**按 `persist_evidence_contract:v1` 汇总 evidence，**THEN**bundle 含恰60个 unique criterion IDs，每项映射到 source/catalog hash 匹配、runner/environment/fixture/assertion/raw-sample metadata 完整且 exit code 为0的 PASS artifact；任一分组缺失、stale hash、case count错误、manifest为空、仅总结无原始产物或 unresolved blocker 均不得宣称 implementation accepted。 |

## Open Questions

| ID | Question | Owner | Deadline / Blocker | Required Closure Evidence |
|---|---|---|---|---|
| `PERSIST-Q1` | Ren’Py 8.5.3 的 `save_persistent()` 在 serialization、temporary write、replacement 与 process interruption 时，能否保证磁盘仅为完整 previous root 或完整 candidate root，并把哪些失败证明为 pre-write safe failure？ | Engine Programmer + SYS-TEST / Andwey | 任一 persistence write story 进入 Ready 前 | 四阶段 failure-injection harness、safe-failure vs commit-unknown classification、previous/candidate restart reconciliation、partial-root negative fixtures |
| `PERSIST-Q2` | Ren’Py 实际 `old/new/current` callback、exact recovery marker round-trip、classifier-before-default/root-validation ordering 与 callback exception containment 是否符合本 GDD 已冻结的三源合同？ | Engine Programmer / Andwey | Merge implementation 前 | Engine contract fixture、三源 permutation、invalid/incompatible marker、startup classifier ordering、重复运行 deterministic report |
| `PERSIST-Q3` | `_clear(progress=True)`、`achievement.clear_all()` 或替代 adapter 对三类 membership、achievement progress、preserved accessibility settings、双 persistent storage locations 与 defaults reapplication 的 exact behavior是什么？如何在各 phase hard kill 后识别并继续同一 collection reset？ | Engine Programmer + SYS-ACCESS / Andwey | Player-facing collection reset 入口开放前 | Clean/nonempty/corrupt fixtures、durable reset phase/recovery matrix、settings-preservation proof、restart 后完整 state report |
| `PERSIST-Q4` | `achievement.grant/has` 的 local backend write、error reporting 与 `save_persistent()` ordering 如何冻结，才能稳定执行 root→backend 单向 repair？ | Engine Programmer + SYS-ACHIEVE / Andwey | Achievement integration 前 | 11-item backend matrix、partial failure/restart fixtures、zero-duplicate-popup evidence |
| `PERSIST-Q5` | 单一根状态、12-leaf manifest、epoch-aware merge/reset、merge recovery marker、commit-unknown blocking flow、flush-before-projection 与 module ownership如何落实 ADR-0002 amendment、Architecture 与 Control Manifest？ | Architect / Andwey | 任一 core implementation story 进入 Ready 前 | Accepted ADR amendment、updated module/dataflow/control rules、Entity Registry entries、foreign-write scan |
| `PERSIST-Q6` | 11 achievement IDs、6 ending IDs、7 memory IDs 的 exact completed-event/checkpoint 与专用 owner adapter如何通过真实CFG关闭；六 ending 的唯一 completion node 是否 exact 覆盖？ | SYS-ACHIEVE + SYS-NARRATIVE + SYS-ENDING / Andwey | Production request catalog freeze 前 | `achievement_event_catalog:v2`、`ending_completion_event_record` catalog、owner callgraph/CFG coverage、before-entry/after-completion branch evidence、single notification-group matrix；achievement mirror count=0 |
| `PERSIST-Q7` | 已冻结行为状态机下，Settings conflict、commit-unknown、safe recovery、persistence-unavailable new game、collection reset/recovery 的最终简体中文 copy、self-voicing transcript 与版式 captures 是什么？ | SYS-ACCESS + UX / Andwey | SYS-PERSIST UI specs 批准前 | Copy catalog、exact self-voicing transcript、三档字体/high-contrast/reduced-motion captures、reading/focus traversal |
| `PERSIST-Q8` | Performance thresholds 使用哪台最低 reference hardware，以及 timer、同步 I/O wait、rendered frame、disk/cache/GC/background processes、cold/warm backend 与最大 N/R/ID fixtures 如何冻结？ | SYS-TEST + Engine Programmer / Andwey | 首次 SYS-PERSIST performance gate 前 | Benchmark manifest、hardware/environment IDs、5 warm-up + ≥30 unfiltered raw samples、nearest-rank report |
| `PERSIST-Q9` | 公开发行后首次 schema/catalog/ownership 变化支持哪些 source versions、采用何种 migration 与 rollback policy？ | Producer + Architect / Andwey | 首次公开变更提案时 | 独立 Accepted migration ADR、support matrix、逐版本 golden roots、failure/rollback fixtures |

当前首发仍执行“不迁移旧开发 persistent”的批准策略；`PERSIST-Q9` 在首次公开变更前不阻止首发。`PERSIST-Q1`、`PERSIST-Q2` 与 `PERSIST-Q5` 阻止 core implementation-ready；`PERSIST-Q3` 只阻止 player-facing collection reset；`PERSIST-Q4`、`PERSIST-Q6`、`PERSIST-Q7` 与 `PERSIST-Q8` 分别阻止对应 achievement integration、production catalog、UI approval 与 performance acceptance。Schema/validator/manifest 纯框架可在 Q3/Q4/Q6/Q7/Q8 未关闭时实现，但不得越过各自功能 gate。
