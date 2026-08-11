# 存档、读档与回退

> **System ID**: SYS-SAVE
> **Status**: Approved with provisional downstream gates
> **Author**: Andwey + Codex
> **Last Updated**: 2026-08-04
> **Implements Pillar**: 温柔必须被挣来；悲剧也是完整答案
> **Review Mode**: Full
> **Journal Integration Amendment**: 2026-08-04 — freezes `journal_menu_gate:v1`, caller focus catalogs, blocking-load exclusion and four reverse-interface ACs

## Overview

SYS-SAVE 是贯穿全游戏的基础设施系统，负责玩家的手动存档、读档、快速存读档与自由回退，并保证每次恢复都把 Ren’Py 叙事控制位置、save-contract/catalog generation、完整 `semantic_state` 以及 `ending_flow` lifecycle 恢复到同一个一致时点。系统必须识别受支持、旧版、不受支持、损坏及内部恢复失败状态；只有受支持的存档可以继续。Detached preflight 已能确定的失败留在原 Load browser，不破坏当前安全上下文；只有安装状态后或 engine-control 恢复时发生的失败进入不可返回 loaded scene 的 root blocking safe flow。它不建立独立叙事状态、reaction/payoff 去重账本或外部存档格式，而是依据 ADR-0002、ADR-0004 与 ADR-0005 维护既有 rollback-owned 状态边界。该系统存在的目的，是让玩家能够自由重访选择而不破坏选择、即时反应、延迟回收和结局因果之间的可信关系。

## Player Fantasy

玩家不应感觉自己在管理一套脆弱的技术状态，而应确信：无论保存、读取还是回退，故事都会忠实回到自己选择的那个时刻。重新尝试可以改变之后真正重新作出的选择，却不能留下已撤销分支的隐藏痕迹，也不能凭借重复载入绕过即时反应、延迟回收或悲剧后果。

这种可靠性间接服务于“温柔必须被挣来”和“悲剧也是完整答案”两项支柱。玩家可以安心探索其他可能性，但每一次实际走过的 traversal 仍需承担完整因果；系统既不惩罚正常重访，也不让技术漏洞把关系与代价变成可随意冲销的账目。面对不兼容或损坏存档时，系统应清楚、克制地阻止不安全恢复，而不是伪装成功后让故事悄然失真。

“不留下已撤销分支的隐藏痕迹”专指本轮叙事因果、五轴、history、reaction、payoff 与 ending lifecycle。已经合法获得的跨周目解锁、成就和设置由 `persistent` 所有，可在 load/rollback 后保留；UI 必须把它们表达为跨周目收藏，而不是当前分支仍然发生过的证据。

> 2026-07-29 full review consulted `game-designer`、`systems-designer`、Ren’Py specialist、`performance-analyst`、`ux-designer`、`ui-programmer`、`qa-lead` 与 `creative-director`；本修订按 senior verdict 关闭核心合同阻断项。

## Detailed Design

### Core Rules

1. SYS-SAVE 统一管理手动存档、手动读档、快速存读档、引擎自动存档与回退；不同入口不得形成不同兼容性规则。
2. 存档只能产生于已登记的稳定控制位置。`Confirmed`、`Committed`、`ReactionEstablished` 及 bounded reaction interaction 均不允许保存、读取、回退或自动存档。
3. 一次恢复必须同时恢复 Ren’Py 控制位置、`save_contract_sentinel`、`save_catalog_generation_id`、`state_schema_sentinel`、完整 `semantic_state`、`ending_flow_sentinel/state`、`pending_ending_id` 及 frozen rollback-ownership manifest 中其他 rollback-owned per-run 状态。`save_contract_sentinel` 与 `save_catalog_generation_id` 均以 `default None` 声明，只能由批准的新游戏初始化入口写入；首发支持值分别为 exact string `"save_contract:v1"` 与当前发行 catalog 的 exact generation ID。
4. `persistent` 解锁、设置和跨周目数据不属于上述恢复单元；不兼容存档不得清除或从局内状态重建它们。
5. `semantic_state`、choice lifecycle、reaction、payoff、qualification 与 resolver 临时结果不得拥有第二套 serialization、dedupe ledger、screen-local cache 或 imported mutable state。
6. Production 恢复 catalog 与测试恢复证据严格分离：

   - SYS-SAVE 的 production catalog 只包含 `restore_control_location_record`，描述引擎位置、catalog generation、source artifact 与 action gate；它不冻结某个位置唯一的 `expected_history` 或 `expected_axes`。
   - SYS-CHOICE 的 exact `choice_restore_checkpoint_record` 是 test-only 恢复证据 fixture，包含 11 个字段：`checkpoint_id`、`checkpoint_kind`、`control_location_id`、`state_sentinel`、`expected_history`、`expected_axes`、`target_choice_id`、`target_reaction_id`、`target_payoff_id_or_none`、`observation_horizon_id`、`owner_system`。
   - 同一 production control location 可由多个合法 prehistory/axes fixtures 覆盖；不得把 fixture 与 production location 强制为一对一，也不得在运行时用单一 fixture snapshot 拒绝其他合法汇合状态。

   SYS-SAVE 另行拥有 `restore_control_location_record`，只描述引擎位置映射：

| 字段 | 约束 |
|---|---|
| `control_location_id` | 全局唯一稳定 ID；禁止文件行号 identity |
| `checkpoint_kind` | `before_choice`、`after_reaction`、`before_payoff`、`after_payoff` 之一 |
| `engine_statement_id` | 对应 source-hash-bound Ren’Py statement |
| `source_artifact_hash` | 对应 canonical CFG/catalog generation |
| `catalog_generation_id` | 与 rollback-owned `save_catalog_generation_id` exact-equal 的 generation ID |
| `action_gate_profile_id` | 该位置允许的 save/load/rollback/skip 行为 |
| `owner_system` | schema owner 为 `SYS-SAVE`；production mapping 内容由 `SYS-NARRATIVE` 提交 |

   Production records 必须按 `control_location_id + checkpoint_kind` 唯一，且 engine statement 必须恰好映射一条 record。Test fixtures 必须各自映射一条 production record；一条 production record 可拥有多个不同 prehistory fixture。fixture orphan、production record 无 canonical fixture、重复 fixture ID、重复 production key 或 kind mismatch 均阻止 evidence/catalog freeze。

7. engine statement 必须恰好映射到一条 `restore_control_location_record`。零项匹配属于 `UNSUPPORTED_CONTROL_LOCATION`；多项匹配、当前 production source 与当前 catalog hash 不一致或 catalog 自身结构非法属于构建错误，不得发布；若异常产物进入运行时，结果固定为 `INTERNAL_LOAD_VALIDATION_FAILURE`。
8. 已知位置与 `semantic_state.choice_history`、checkpoint kind 或 required lifecycle 不一致时，结果为 `CORRUPT_STATE`；不得猜测邻近场景、补写 history 或自动跳转。
9. 加载使用固定两阶段聚合顺序：

   1. 玩家选择非空本地 slot 后，custom load action 调用 detached preflight；它可使用引擎支持的 save-data inspection 读取 required sentinels 与 generation ID，但不改变当前游戏状态。该步骤不是不可信 pickle 的安全沙箱；产品只支持本机游戏生成且未经外部修改的存档。
   2. 容器不存在、无法读取或无法反序列化 → `UNREADABLE_SAVE`，留在当前 Load browser。
   3. preflight 能确定任一 required sentinel 为 `None` → `LEGACY_INCOMPATIBLE`；wrong exact type、未知版本或 catalog generation 不受支持 → `UNSUPPORTED_VERSION`。这些已知失败不安装 loaded state。
   4. 只有 preflight 未发现阻断问题且玩家确认“加载会放弃当前未保存进度”后，才调用原生 load。
   5. 引擎在恢复 statement/rollback log 时失败、未能进入 `after_load` → 由唯一 load-failure label 路由为 `UNSUPPORTED_CONTROL_LOCATION` 或 `INTERNAL_LOAD_VALIDATION_FAILURE`，进入 root blocking safe flow。
   6. `after_load` 依次 exact 校验 `save_contract_sentinel`、`save_catalog_generation_id`、semantic sentinel/state、ending sentinel/lifecycle、current control location 与 checkpoint-state coherence。
   7. 任一 required sentinel 为 `None` → `LEGACY_INCOMPATIBLE`；任一 wrong exact type、未知值或不受支持 generation → `UNSUPPORTED_VERSION`，且不访问对应 state。
   8. semantic 或 ending state 失败 → `CORRUPT_STATE`；零项 location match → `UNSUPPORTED_CONTROL_LOCATION`；多项 match、当前 source/catalog drift 或合同外异常 → `INTERNAL_LOAD_VALIDATION_FAILURE`；合法 location 但状态与 checkpoint kind/lifecycle 不相容 → `CORRUPT_STATE`。
   9. 全部通过才返回 `SUPPORTED` 并显示首个 loaded stable frame。

10. 空 UI slot 是 `EMPTY_SLOT_NOOP`，不调用任何 load API，也不进入兼容性结果。只有曾被识别为占用、但容器已丢失/损坏或引擎无法读取的 slot 才返回 `UNREADABLE_SAVE`；玩家留在当前 Load browser 并可选择其他槽位。
11. 所有 post-install 与 engine-control 失败结果共用 `screen_blocking_restore_error`，但显示对应的克制说明。精确字段、阶段和 offending IDs 只进入开发诊断，不向玩家暴露内部轴、token、路线或结局条件。
12. Post-install 或 engine-control 恢复失败必须先进入 root safe context：清空可返回 loaded scene 的 screen/call context，阻止底层 scene timers、callbacks、quick actions 与输入继续执行，再显示 `screen_blocking_restore_error`。rollback、quick save/load、普通 save/load、skip、auto、history return、screen dismissal 与 game-menu return 均不可见、不可用且不可聚焦。游戏内唯一恢复出口是主菜单与明确开始新游戏；OS 关闭窗口属于退出应用，不得被误定义为“留在阻断界面”，但退出过程不得恢复或短暂显示 loaded scene。
13. “开始新游戏”只通过批准的显式初始化入口同时写入 `save_contract_sentinel`、当前 `save_catalog_generation_id`、semantic 与 ending lifecycle；合法 persistent 数据保持不变。
14. 从 `before_choice` 恢复后重新确认会产生一次新 commit 与 reaction；从 `after_reaction` 恢复不重复二者；从 `before_payoff` 恢复会在当前 traversal 发生一次目标 payoff；从 `after_payoff` 恢复不重播已完成 payoff。
15. 从 `after_payoff` 回退到不同的 `before_payoff` 后再次前进属于新 observation window，目标 payoff 可以重新发生；不得用 persistent 或独立 ledger 阻止它。
16. 存档槽 metadata 可镜像 save-contract version、sentinels、build、`catalog_generation_id`、`chapter_summary_id` 及 `control_location_id`，用于槽位标记和加载前提示；缺失、过期或被修改的 metadata 永远不能替代 detached preflight 与 `after_load` 判定。玩家界面不直接渲染 raw metadata：`chapter_summary_id` 必须是 `[a-z0-9_]{1,64}` 并解析到内置简体中文 catalog；未知 ID、超长值、markup、双向控制字符或 wrong type 均使用中性 fallback，文本渲染关闭 substitution。
17. 首个公开版本不迁移旧开发存档。任何 schema 或 checkpoint catalog 兼容迁移必须先有独立接受的 ADR、明确支持矩阵与逐版本 fixtures。
18. 存档内容限于 primitives、Ren’Py-managed rollback collections 及已批准引擎状态；文件句柄、任务、socket、displayable ownership 或 imported mutable objects 均禁止进入 per-run store。
19. `save_contract_sentinel`、`save_catalog_generation_id` 与 rollback-ownership manifest 是新的架构同步点；进入 implementation-ready 前必须通过接受的 ADR 或对 ADR-0002/0005 的同步修订，并更新 Control Manifest。GDD 中冻结行为合同不等同于已完成该架构记录。

### States and Transitions

以下为概念状态，不新增 persisted lifecycle enum。

| 当前状态 | 事件 | 下一状态 | 结果 |
|---|---|---|---|
| `PlayableStable` | 手动/快速/自动保存 | `Saving → PlayableStable` | 成功写入同一恢复单元；失败不改变当前游戏 |
| `PlayableStable` 或主菜单 | 选择非空存档 | `LoadPreflight` | metadata 仅提供提示；detached preflight 不改变当前状态 |
| `LoadPreflight` | 空 UI slot | 原安全界面 | `EMPTY_SLOT_NOOP`，load API 调用数为 0 |
| `LoadPreflight` | 容器丢失/损坏或引擎无法读取 | 原安全界面 | `UNREADABLE_SAVE`，不替换当前状态 |
| `LoadPreflight` | 已知 legacy/unsupported | 原安全界面 | 显示非破坏性失败说明；不安装 loaded state |
| `LoadPreflight` | preflight 未阻断且玩家确认 | `LoadedUnvalidated` | 原生 load；立即进入 engine failure route 或 `after_load`，不显示 loaded scene |
| `LoadedUnvalidated` | 返回 `SUPPORTED` | `ResumeReady → PlayableStable` | 从原稳定位置继续 |
| `LoadedUnvalidated` | 任一 post-install 或 engine-control 失败 | `BlockingSafeFlow` | 进入 root safe context，不得返回 loaded scene |
| `PlayableStable` | rollback | `RollbackRestored` | Ren’Py 恢复 rollback-owned 状态与控制位置 |
| `RollbackRestored` | checkpoint 合法 | `PlayableStable` | 按 checkpoint kind 开启新的 observation window |
| `RollbackRestored` | 位置或状态不合法 | `BlockingSafeFlow` | 不猜测或修复 |
| `CriticalInteraction` | save/load/rollback 请求 | `CriticalInteraction` | 请求不可达；调用数为 0 |
| `BlockingSafeFlow` | 主菜单 | 主菜单 | 放弃当前不安全 per-run state |
| `BlockingSafeFlow` | 明确开始新游戏 | `PlayableStable` | 显式初始化 save/semantic/ending lifecycle；persistent 保持 |
| `BlockingSafeFlow` | 其他返回或恢复动作 | `BlockingSafeFlow` | 全部拒绝 |
| `BlockingSafeFlow` | OS 关闭窗口 | 应用退出 | 不恢复或暴露 loaded scene |

### Interactions with Other Systems

| 系统 | 接口 | SYS-SAVE 所有权边界 |
|---|---|---|
| Ren’Py 8.5.3 | serialization、detached save-data inspection、load-failure label、current statement、return stack、screens、rollback checkpoints | 使用引擎原生存档；不建立外部 JSON 主存档；preflight 不宣称任意 pickle 安全 |
| SYS-STATE | semantic sentinel、schema 2 envelope、加载分类与 exact validation | 不修改或规范化 semantic state |
| SYS-ENDING | `ending_flow:v1`、`Active/Ended`、pending ID | 完整恢复并校验；不保存 resolver 临时状态 |
| SYS-CHOICE | test-only 11-field checkpoint fixtures、canonical CFG artifact、commit/reaction/payoff 计数合同 | 不把 fixture 变成 runtime snapshot catalog，不增加 reaction/payoff ledger |
| SYS-NARRATIVE | stable control locations、statement mapping、observation horizons | SYS-SAVE 拥有 record schema/恢复验证；SYS-NARRATIVE 拥有 production records |
| SYS-PERSIST | 跨周目解锁和设置 | 保留但不从 per-run save 推导或回滚 |
| SYS-JOURNAL | `journal_menu_gate:v1`、main/game-menu caller focus catalogs、blocking recovery preemption | SYS-SAVE只拥有入口许可与caller恢复边界；不向Journal提供slot/persistent membership，也不保存Journal controller |
| SYS-ACCESS | 键盘、文本、焦点及错误界面可达性 | 阻断界面的两个出口必须在全部支持模式下可用 |
| SYS-TEST | engine fixtures、instrumentation、负例、benchmark | 测试观察器不得进入 production save |
| SYS-BUILD | build/version、compiled checkpoint catalog 与 source hashes | 发行包必须携带与脚本匹配的冻结 catalog |

> Full specialist review incorporated engine hooks、catalog/fixture ownership、performance、UI gates、blocking flow 与 QA observability；production records 与 engine evidence 仍受 Open Questions 的 implementation gates 约束。

## Formulas

### Load Compatibility Result

The `load_compatibility_result` formula is defined as:

```text
load_compatibility_result(I) =
    INTERNAL_LOAD_VALIDATION_FAILURE
        if input_shape_exact(I)=False
    LEGACY_INCOMPATIBLE
        if any required sentinel is None
    UNSUPPORTED_VERSION
        if any non-None sentinel/generation has wrong exact type
        or unknown/unsupported value
    INTERNAL_LOAD_VALIDATION_FAILURE
        if current_catalog_structure_valid=False
        or current_source_artifact_match=False
    CORRUPT_STATE
        if semantic_state_valid=False or ending_lifecycle_valid=False
    UNSUPPORTED_CONTROL_LOCATION
        if control_location_match_count = 0
    INTERNAL_LOAD_VALIDATION_FAILURE
        if control_location_match_count > 1
    CORRUPT_STATE
        if checkpoint_state_coherent=False
    SUPPORTED
        otherwise
```

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| load validation input | `I` | exact record | frozen field set | 聚合全部下述值；缺字段、多字段或 wrong exact type 首先失败 |
| save-contract sentinel | `S꜀` | object | `None` or exact supported string | `"save_contract:v1"` compatibility marker |
| catalog generation | `G` | object | `None` or exact supported string | 存档创建时的 production catalog generation |
| semantic sentinel | `Sₛ` | object | `None` or exact supported string | SYS-STATE compatibility marker |
| ending sentinel | `Sₑ` | object | `None` or exact supported string | SYS-ENDING lifecycle marker |
| semantic validity | `Vₛ` | exact bool | `False/True` | schema 2 exact validator result |
| ending validity | `Vₑ` | exact bool | `False/True` | lifecycle/state/pending combination |
| location matches | `M` | exact int | `0..N` | matching control-location records |
| current catalog validity | `V꜀` | exact bool | `False/True` | 当前 catalog exact schema、唯一性与 generation 自洽 |
| source artifact match | `Vₕ` | exact bool | `False/True` | 当前 catalog hashes 与当前 canonical CFG artifact exact-match |
| checkpoint coherence | `C` | exact bool | `False/True` | restored history/axes/lifecycle 符合 checkpoint kind |

所有 bool 必须是 exact bool，`M` 必须是非 bool exact int 且 `M≥0`。聚合器先执行顶层 exact-shape/type sweep，再按上述顺序访问 schema-known fields；禁止对 unknown/custom object 求真、迭代、表示、比较或哈希。

**Output Range:** `SUPPORTED`、`LEGACY_INCOMPATIBLE`、`UNSUPPORTED_VERSION`、`CORRUPT_STATE`、`UNSUPPORTED_CONTROL_LOCATION`、`INTERNAL_LOAD_VALIDATION_FAILURE` 中恰好一项。`EMPTY_SLOT_NOOP` 与 `UNREADABLE_SAVE` 属原生 load 前结果，不进入本公式。

**Example:** 三个 sentinels 与 generation 均受支持、两个 state validators 均通过，但当前 statement 没有 location mapping，则结果为 `UNSUPPORTED_CONTROL_LOCATION`。若 ending sentinel 类型错误，即使 semantic/ending state 内含 protocol bomb，也直接返回 `UNSUPPORTED_VERSION`，两个 state validator 调用数均为 0。若 `M=2`，结果固定为 `INTERNAL_LOAD_VALIDATION_FAILURE`，不得归因于玩家存档。

### Production Location Catalog Validity

The `restore_control_location_catalog_valid` formula is defined as:

```text
restore_control_location_catalog_valid(L,A,G) =
    exact_top_level_types(L,A,G)
    ∧ |L| > 0
    ∧ staged_exact_record_validation(L)
    ∧ duplicate_control_key_count(L) = 0
    ∧ duplicate_engine_statement_id_count(L) = 0
    ∧ ∀l∈L: l.catalog_generation_id = G
    ∧ ∀l∈L: artifact_contains_exact_statement(A,l.engine_statement_id)
    ∧ ∀l∈L: artifact_hash(A,l.engine_statement_id) = l.source_artifact_hash
    ∧ all_action_gate_profiles_resolve(L)
```

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| location mapping catalog | `L` | exact tuple | `1..N` records | SYS-SAVE production mapping records |
| canonical source artifact | `A` | exact immutable artifact | one frozen generation | SYS-CHOICE canonical CFG/source identity input |
| catalog generation | `G` | exact string | one supported generation | 当前发行 catalog generation |

验证采用 staged total evaluation：顶层类型失败后不访问 records；record exact-shape/type sweep 失败后不读取 value fields；随后依次验证闭集值、重复项、generation、statement、hash 与 gate references。任何 custom object/protocol bomb 均不得被迭代或调用。

**Output Range:** exact `False` 或 `True`。空 catalog、missing/extra/wrong-type fields、duplicate production key、一个 statement 对应多条 records、generation mismatch、无效 statement、source-hash mismatch 或 unresolved gate profile 均为 `False`，并阻止 catalog freeze。

### Restore Evidence Coverage and Integrity

Test-only `save_restore_fixture_record` contains, in order:

`fixture_id, choice_checkpoint_record, expected_save_contract_sentinel, expected_catalog_generation_id, expected_ending_sentinel, expected_ending_state, expected_pending_ending_id, owner_system`

Nested `choice_checkpoint_record` 必须保持 SYS-CHOICE 的 11-field exact schema。The formulas are:

```text
restore_fixture_coverage_valid(F,L) =
    exact_nonempty_fixture_and_location_tuples(F,L)
    ∧ duplicate_fixture_id_count(F) = 0
    ∧ ∀f∈F: ∃!l∈L:
        f.choice_checkpoint_record.control_location_id = l.control_location_id
        ∧ f.choice_checkpoint_record.checkpoint_kind = l.checkpoint_kind
    ∧ ∀l∈L: ∃f∈F:
        f.choice_checkpoint_record.control_location_id = l.control_location_id
        ∧ f.choice_checkpoint_record.checkpoint_kind = l.checkpoint_kind
    ∧ all_four_checkpoint_kinds_have_nonempty_fixtures(F)

save_restore_integrity_valid(Fx,R,T,L,A,G) =
    exact_save_restore_fixture_record(Fx)
    ∧ restore_control_location_catalog_valid(L,A,G)
    ∧ restored_control_location(R) =
        Fx.choice_checkpoint_record.control_location_id
    ∧ restored_save_contract_sentinel(R) =
        Fx.expected_save_contract_sentinel
    ∧ restored_catalog_generation_id(R) =
        Fx.expected_catalog_generation_id
    ∧ restored_state_sentinel(R) =
        Fx.choice_checkpoint_record.state_sentinel
    ∧ deep_equal(restored_history(R),
        Fx.choice_checkpoint_record.expected_history)
    ∧ deep_equal(restored_axes(R),
        Fx.choice_checkpoint_record.expected_axes)
    ∧ restored_ending_sentinel(R) = Fx.expected_ending_sentinel
    ∧ restored_ending_state(R) = Fx.expected_ending_state
    ∧ restored_pending_ending_id(R) = Fx.expected_pending_ending_id
    ∧ trace_target_reaction_id(T) =
        Fx.choice_checkpoint_record.target_reaction_id
    ∧ trace_target_payoff_id_or_none(T) =
        Fx.choice_checkpoint_record.target_payoff_id_or_none
    ∧ trace_observation_horizon_id(T) =
        Fx.choice_checkpoint_record.observation_horizon_id
    ∧ restored_traversal_occurrence_valid(
        Fx.choice_checkpoint_record.target_choice_id,
        T,
        Fx.choice_checkpoint_record.checkpoint_kind
      )
```

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| restore fixtures | `F` | exact tuple | nonempty | test-only evidence records；允许多个 fixtures 映射同一 production location |
| expected fixture | `Fx` | exact record | one frozen record | nested choice evidence + save/ending lifecycle expected values |
| restored snapshot | `R` | exact evidence record | one restored state | 实际位置、sentinels、history、axes 与 ending lifecycle |
| post-restore trace | `T` | exact trace record | one observation window | 恢复后清零 spy 至冻结 horizon 的调用 |

**Output Range:** exact `False` 或 `True`；任一状态字段、位置、catalog、target identity、horizon 或调用次数不一致即为 `False`。Persistent 数据不参与该 deep equality，但必须通过独立、非空 ownership-manifest 不变性断言保持。

**Example:** 两个合法 prehistories 可各自拥有 `before_payoff` fixture 并映射同一 production location；二者不要求 expected history 相等。每个 fixture 恢复后 save/semantic/ending sentinels、history、axes、pending ending、target payoff 与 horizon 均匹配时分别为 `True`。

### Request Permission and UI Affordance

Engine permission and player-facing UI state are separate contracts:

```text
save_request_allowed(P,A,Q) =
    exact_inputs(P,A,Q)
    ∧ registered_control_location_required(A) is satisfied
    ∧ Q[A].request_enabled = True
    ∧ phase_action_allowed(P,A)

ui_action_affordance(P,A,G) =
    exact_player_facing_action(P,A)
    ∧ save_request_allowed(P,A,G.request_profile) = True
    ∧ G[A].visible = True
    ∧ G[A].enabled = True
    ∧ G[A].focusable = True
```

`phase_action_allowed` is a closed matrix:

```text
PlayableStable:
  manual_save, quick_save, auto_save, load_slot, quick_load, rollback = True
MainMenu:
  load_slot, quick_load = True
CriticalInteraction, LoadPreflight, LoadedUnvalidated,
BlockingSafeFlow, Saving:
  all save/load/rollback actions = False
unknown phase/action or any unlisted pair = False
```

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| phase | `P` | enum | approved conceptual states | 当前恢复阶段 |
| action | `A` | enum | six request actions | `auto_save` 是非 UI policy action |
| request profile | `Q` | exact record | one profile | request-enabled、stable-location requirement 与来源 policy |
| UI gate profile | `G` | exact record | one profile | 只为玩家动作定义 visible/enabled/focusable |

**Output Range:** 两式均为 exact `False` 或 `True`。缺 key、多 key、wrong exact type、unknown phase/action 均 fail closed 为 `False`，不得抛出、排队或延迟补执行。`auto_save` 只调用 `save_request_allowed`，不要求 visible/focusable。

**Example:** `PlayableStable + quick_save` 且 request/UI gates 均为 true 时 UI affordance 为 `True`；合法 checkpoint 的 `auto_save` request 可为 `True` 而不存在 UI affordance；bounded reaction interaction 中即使 UI profile 错误地报告 enabled，最终仍为 `False`。

### Save/Load Performance

The `save_load_performance_pass` formula is defined as:

```text
save_load_performance_pass(S,L,Hs,Hl) =
    ∀X∈{S,L,Hs,Hl}: exact_key_set(X) = {manual,quick,auto}
    ∧ all_sequences_have_exact_finite_nonnegative_numbers(S,L,Hs,Hl)
    ∧ ∀o∈{manual,quick,auto}:
        |S[o]| ≥ 30 ∧ |L[o]| ≥ 30
        ∧ |Hs[o]| = |S[o]| ∧ |Hl[o]| = |L[o]|
        ∧ nearest_rank_p95(S[o]) ≤ 500 ms
        ∧ max(S[o]) ≤ 1000 ms
        ∧ nearest_rank_p95(L[o]) ≤ 1000 ms
        ∧ nearest_rank_p95(Hs[o]) ≤ 16.6 ms
        ∧ nearest_rank_p95(Hl[o]) ≤ 16.6 ms
        ∧ max(Hs[o]) ≤ 33.2 ms
        ∧ max(Hl[o]) ≤ 33.2 ms
```

其中：

`nearest_rank_p95(X) = sort(X)[ceil(0.95 × |X|) - 1]`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| save latency samples | `S[o]` | exact numeric sequence | at least 30 measured runs/origin | 从操作确认至引擎报告存档成功 |
| load latency samples | `L[o]` | exact numeric sequence | at least 30 measured runs/slot class | 从载入确认至首个可交互稳定帧 |
| save longest-frame samples | `Hs[o]` | exact numeric sequence | one per save run | 同一 save run 的最长 rendered frame/main-thread block |
| load longest-frame samples | `Hl[o]` | exact numeric sequence | one per load run | 同一 load run 的最长 rendered frame/main-thread block |
| origin/slot class | `o` | enum | manual/quick/auto | 三类存档来源 |
| latency | — | milliseconds | `≥0` | 单调计时器结果 |

所有数值必须是非 bool exact int/float、finite 且 `≥0`；NaN、±∞、wrong type、空/不足样本、missing/extra origin、样本长度不一致均直接返回 `False`，且不得调用 sort/max 处理非法序列。

**Output Range:** exact `False` 或 `True`。每类分别判定，整体平均值不得掩盖单一来源失败。

**Example:** 即使三类 end-to-end p95 合格，只要 auto save 最大单次为 1100 ms、某类只有 29 个样本，或 load 的 longest-frame p95 为 20 ms，整体均为 `False`。

Benchmark 的 save end-to-end 区间为 accepted request 至 durable slot 与 success callback 完成，包含 screenshot capture、rotation 与 metadata callback；load 区间为玩家确认至 `after_load` validation 完成且首个 rendered/input-accepting stable frame。使用固定最低硬件、production build、正式表现资产、最大合法内容 fixture、固定电源/后台进程/文件缓存/GC 政策；cold/warm cache 分层报告，每类至少 5 次 warm-up 后采集 30 次正式样本。不得用无资产、空 history 或缺少最大 rollback log 的 fixture 代替。

> Full specialist review incorporated systems boundary values、protocol-safe staged validation、frame-hitch evidence 与 non-vacuous sample requirements。

## Edge Cases

### Save Creation and Slot Integrity

- **If 保存目标槽位已有合法存档，而新写入因磁盘空间、权限、I/O 或序列化错误失败**：不得报告成功；当前游戏保持不变，原槽位必须仍可读取。
- **If 新空槽位写入失败**：该槽位保持为空或不可加载状态，不得显示成功时间、截图或章节摘要。
- **If 进程终止或设备断电发生在既有槽位覆盖期间**：下一次启动时终态只能是完整旧存档或完整新存档；既有槽位不得消失。若引擎无法保证此原子性，实现必须采用经 ADR 批准的临时写入/替换策略。
- **If 进程终止或设备断电发生在空槽位首次写入期间**：下一次启动时终态只能是空槽位或完整新存档。
- **If 存档成功但截图捕获失败**：可使用已登记的中性占位缩略图；状态存档仍可成功，缩略图失败不得改变恢复数据。
- **If 保存成功回调尚未完成时再次触发 save、load 或 rollback**：第一个请求独占执行，其余请求调用数为 0，不排队。
- **If 自动存档请求发生于 `CriticalInteraction`、`LoadedUnvalidated` 或 `BlockingSafeFlow`**：本次请求直接跳过；只允许下一个正常 autosave 周期重新判断，不在离开窗口后突然补存。
- **If 任一保存来源试图把 imported mutable object、任务、文件句柄、socket 或 displayable ownership 纳入 per-run state**：保存验证失败；不得删掉该字段后继续生成部分存档。

### Slot Metadata and Preflight

- **If 玩家选择空槽位读取**：返回 UI-only `EMPTY_SLOT_NOOP`；不调用 detached inspection 或原生 load，不改变当前游戏，并保持 Load browser 可操作。
- **If metadata 缺失、过期、类型错误或被修改**：只影响槽位提示；不得直接宣告存档受支持或损坏。
- **If metadata 显示兼容但 detached preflight 或 `after_load` 验证失败**：以 validator 结果为准；pre-install 失败留在 Load browser，post-install 失败进入 root blocking safe flow。
- **If metadata 显示可能不兼容但 detached preflight 证明 required sentinels/generation 受支持**：仍需玩家确认加载；最终由 `after_load` 决定完整支持性。
- **If 曾占用槽位的容器丢失、损坏或无法反序列化**：返回 `UNREADABLE_SAVE`，不安装 loaded state，玩家留在原安全界面并可选择其他槽位。
- **If raw metadata 包含未知 chapter ID、超长字符串、markup、双向控制字符或 wrong type**：不直接显示 raw value；使用中性 fallback 与 `substitute False`，self-voicing 读取同一安全 fallback。
- **If 存档来自外部复制或来源不明位置**：不提供导入工作流；产品说明明确只支持本机游戏生成且未经外部修改的存档。Detached inspection 与 `after_load` 都不是不可信 pickle 的安全边界，不承诺安全打开任意第三方文件。

### Compatibility Classification

- **If `save_contract_sentinel`、`state_schema_sentinel`、`ending_flow_sentinel` 或 `save_catalog_generation_id` 任一为 `None`，而其他项同时未知或错误类型**：按固定优先级返回 `LEGACY_INCOMPATIBLE`，不读取任何对应 state。
- **If required sentinels/generation 均非 `None`，且任一个为未知 exact string、unsupported generation 或错误类型**：返回 `UNSUPPORTED_VERSION`；semantic 与 ending state validator 调用数均为 0。
- **If sentinel 错误且对应 state 是 protocol bomb、自引用或任意深对象**：不得访问、迭代、表示、比较、哈希或求真该 state；结果仍为 `UNSUPPORTED_VERSION`。
- **If 全部 required sentinels/generation 均受支持，但 semantic 与 ending state 同时损坏**：聚合结果为 `CORRUPT_STATE`；内部诊断按 semantic validator 再 ending validator 的固定顺序停止于首个失败。
- **If semantic state 合法但 ending lifecycle 缺字段、类型错误、pending 组合非法或版本不受支持**：根据 sentinel 阶段返回 `UNSUPPORTED_VERSION` 或 `CORRUPT_STATE`，不得只恢复 semantic state 后继续。
- **If validator 抛出合同声明的 `TypeError` 或 `ValueError`**：转换为当前阶段规定的兼容性结果；不得向玩家显示异常文本。
- **If validator、catalog adapter 或路由代码抛出合同外异常**：记录 `INTERNAL_LOAD_VALIDATION_FAILURE`，进入同一阻断界面并显示通用安全说明；不得错误归因于玩家存档。
- **If 未来 schema 或 sentinel 首次出现且没有接受的迁移 ADR**：返回 `UNSUPPORTED_VERSION`；不得猜测、钳制、补键或降级读取。
- **If 旧存档缺失变量并由 `default` 补为 `None`**：返回 `LEGACY_INCOMPATIBLE`；不得把默认值解释为新游戏初始化。

### Control Locations and Catalogs

- **If 当前 engine statement 没有对应 `restore_control_location_record`**：返回 `UNSUPPORTED_CONTROL_LOCATION`，scene-guess 与 history-write count 均为 0。
- **If 当前 statement 同时映射多条 location records，或 production catalog 存在 duplicate key、generation/hash drift、unresolved gate profile**：production catalog 构建失败；若异常产物仍进入运行时，则作为 `INTERNAL_LOAD_VALIDATION_FAILURE` fail closed。
- **If test fixture 没有 production mapping、production mapping 没有任何 canonical fixture、fixture ID 重复或 kind mismatch**：evidence freeze 失败；多个不同 prehistory fixtures 映射同一 production record 是合法的。
- **If 已知 control location 的 restored state 与 schema invariants、checkpoint kind 或 ending lifecycle 不相容**：返回 `CORRUPT_STATE`；不得用单一 canonical fixture 的 expected history/axes 否定其他可验证的合法汇合状态。
- **If loaded `save_catalog_generation_id` 与当前支持矩阵不匹配**：返回 `UNSUPPORTED_VERSION`。若当前 catalog 自身与当前 source artifact hash 不匹配，则为 `INTERNAL_LOAD_VALIDATION_FAILURE`，不得归因于玩家存档。
- **If engine 在进入 `after_load` 前无法恢复 statement/rollback log**：唯一 load-failure label 进入 root blocking safe flow；已知零映射归为 `UNSUPPORTED_CONTROL_LOCATION`，无法安全区分的引擎内部失败归为 `INTERNAL_LOAD_VALIDATION_FAILURE`。
- **If production `call` 缺少稳定 `from` identity，动态生成目标或无法静态解析 return site**：production location catalog 构建失败，不得发布该脚本。
- **If checkpoint record 使用文件行号作为稳定 identity**：构建失败；移动空行或改写文案不得改变 `control_location_id`。

### Restore and Rollback Semantics

- **If load 或 rollback 恢复到 `before_choice`**：该 choice 及其后续影响不存在；重新确认后当前 observation window 恰有一次 commit 与一次 reaction。
- **If load 恢复到 `after_reaction`**：history/axes 保持，commit 与 reaction 调用数均为 0。
- **If load 恢复到 `before_payoff`**：commit/reaction 为 0，目标 payoff 在冻结 horizon 前恰发生一次。
- **If load 恢复到 `after_payoff`**：已完成目标 payoff 在下一控制边界前调用数为 0。
- **If 从 `after_payoff` rollback 到 distinct `before_payoff` 后再次前进**：开始新的 observation window，目标 payoff 恰发生一次。
- **If 反复加载同一个 `before_payoff` 存档**：每次恢复 traversal 都可发生一次目标 payoff；不得以 persistent 或独立 ledger 导致丢失。
- **If 支持的存档在 ending entry 后保存且 lifecycle 为 `Ended`**：恢复 exact `Ended` 与 pending ending ID，从该控制位置继续；canonical resolver 不重新运行。
- **If rollback 跨过 ending entry**：恢复 `Active`、对应 pending 值与 semantic snapshot；相同 snapshot 重新求值时产生深值相同结果。
- **If 玩家成功加载后继续 rollback**：只能在 loaded save 自身恢复的 rollback history 内回退；不承诺恢复执行 load 前的另一局运行时状态。`after_load` 临时诊断与 action gates 不得进入 rollback-owned store 或残留。
- **If rollback history 已耗尽**：rollback action 必须 disabled、hidden from keyboard focus 且 invocation count 为 0；当前状态深值不变，不得跳到新游戏或主菜单。
- **If save/load/rollback 在 commit→reaction 或 bounded reaction interaction 内被脚本、快捷键或替代输入调用**：所有调用数为 0，当前交互继续；不得排队到 interaction 结束后执行。

### Blocking Safe Flow

- **If 任一 post-install 或 engine-control 恢复失败**：先清除可返回 caller 的 screen/call contexts、阻止底层 callbacks/timers/shortcuts，再进入 `screen_blocking_restore_error`；loaded scene、choice surface、reaction、payoff、cause UI 与普通 game menu 均不得显示、更新或接收焦点。
- **If 玩家尝试 rollback、普通/快速存读档、skip、auto、history return、screen return 或关闭错误 screen 返回 caller**：全部留在阻断流程；唯一可聚焦出口仍为主菜单与明确开始新游戏。
- **If 玩家选择主菜单**：清除不安全的当前上下文并进入主菜单；不得通过 screen stack 返回 loaded scene。
- **If 玩家选择明确开始新游戏**：同时显式初始化 save contract/catalog generation、semantic 与 ending lifecycle；合法 persistent 解锁、设置和跨周目数据保持不变。
- **If 阻断界面的本地化文案、字体或辅助模式缺失**：使用内置简体中文安全文本和键盘可达的两个出口；不得因表现资源缺失恢复 loaded scene。
- **If 阻断流程自身发生重复 activation**：第一个退出动作独占执行，其余调用数为 0。
- **If 玩家通过 OS window close 请求退出应用**：允许正常退出；退出过程不得 dismiss blocking screen 后恢复、显示或执行 loaded scene。

> Full specialist review incorporated atomic terminal-state separation、engine pre-`after_load` failure routing、trusted-local threat model、merge-safe fixture semantics 与 exact blocking/OS-exit boundaries。

## Dependencies

SYS-SAVE 的系统索引依赖更新为：

`Engine + SYS-STATE + SYS-ENDING + SYS-CHOICE + SYS-NARRATIVE contracts`

这表示设计与集成合同依赖，不改变 SYS-SAVE 从第一段可玩内容开始贯穿项目的 cross-cutting 地位。SYS-NARRATIVE 当前未批准不会阻止本 GDD 完成，但会阻止 production checkpoint catalog freeze、四恢复点 engine evidence 与最终集成封板。

| Dependency | Strength | Direction | Required Interface | Owner / Current Status |
|---|---|---|---|---|
| Ren’Py 8.5.3 | Hard runtime | Engine → SYS-SAVE | 原生 serialization、detached save-data inspection、load-failure label、current statement/return stack、rollback-transformed store、screen actions、`after_load`、slot metadata | Pinned；engine control-recovery 与 atomic replacement 需 tests/ADR 关闭 |
| Game Concept | Hard design authority | Concept → SYS-SAVE | 自由重访选择但保持完整因果；悲剧与代价不得被技术状态冲销 | Approved |
| ADR-0002 | Hard architecture | ADR → SYS-SAVE | rollback/persistent 边界、原生存档、无外部 JSON 主存档 | Accepted；新增 save-contract/catalog sentinel 需同步修订 |
| ADR-0004 | Hard architecture | ADR → SYS-SAVE | schema 2 envelope、exact validation、detached import boundary | Accepted |
| ADR-0005 | Hard architecture | ADR → SYS-SAVE | detectable initialization、blocking safe flow、ending lifecycle | Accepted；新增 detectable save lifecycle 需同步修订 |
| Control Manifest | Hard implementation boundary | Manifest → SYS-SAVE | required/forbidden state ownership、失败流程与测试边界 | Active |
| SYS-STATE | Hard runtime | Bidirectional | `state_schema_sentinel`、schema 2 `semantic_state`、exact validator、四项基础加载分类 | Approved |
| SYS-ENDING | Hard runtime | Bidirectional | `ending_flow:v1`、`Active/Ended`、pending ID、唯一 `commit_ending_completion` terminal node、completion event 与 rollback contract | Approved with provisional downstream gates；completion boundary 已冻结 |
| SYS-CHOICE | Hard build/integration | Bidirectional | test-only exact 11-field `choice_restore_checkpoint_record`、canonical CFG artifact、四类恢复计数、`restored_traversal_occurrence_valid` | Approved with provisional downstream gates |
| SYS-NARRATIVE | Hard content/integration | Bidirectional | production control locations、statement mapping、observation horizons、action-gate profiles | In Revision；不阻止 GDD，阻止 production catalog lock |
| SYS-PERSIST | Explicit hard boundary | SYS-PERSIST ↔ SYS-SAVE | 消费 schema v2 的12-leaf ownership manifest；跨周目 schema、epoch、flush、merge/reset与迁移由SYS-PERSIST独占；SYS-SAVE只验证局内恢复不改变persistent，并管理rollback-owned run epoch 与 ending completion event | In Revision |
| SYS-JOURNAL | Hard menu/recovery integration | SYS-SAVE ↔ SYS-JOURNAL | `journal_menu_gate:v1`、`journal_caller_focus_catalog:v1`、unsupported/corrupt/loaded-unvalidated exclusion与blocking recovery preemption；不提供收藏数据 | In Revision；本amendment关闭设计接口，UX captures仍为下游gate |
| SYS-ACCESS | Hard presentation | SYS-ACCESS → SYS-SAVE | load/save/error surfaces 的键盘、自发声、五项project settings、字体缩放、高对比、0 ms reduced-motion与焦点合同 | Designed；full re-review pending |
| SYS-TEST | Hard verification | SYS-SAVE → SYS-TEST | load-classification fixtures、四 checkpoint traces、I/O failures、performance protocol、production observer isolation | Not Started |
| SYS-BUILD | Downstream packaging | SYS-SAVE → SYS-BUILD | 匹配脚本的 checkpoint catalog、source hashes、build/version metadata；排除 test-only observers | Not Started |
| Migration ADR | Conditional hard gate | Future ADR → SYS-SAVE | 每个受支持旧版本的迁移矩阵、fixtures、rollback policy | 当前不存在；首发不迁移旧开发存档 |

### Interface Boundaries

- SYS-SAVE 只编排和验证恢复，不重新定义 SYS-STATE、SYS-ENDING 或 SYS-CHOICE 的内部 schema。
- SYS-CHOICE 拥有 test-only checkpoint evidence schema 与 canonical CFG artifact；SYS-SAVE 拥有 production `restore_control_location_record` schema、save-contract/generation sentinels 和恢复编排；SYS-NARRATIVE 提交 production mapping 内容。Fixtures 与 production mappings 是多对一覆盖，不是一对一状态快照合同。
- SYS-PERSIST 独占 persistent schema、写入、flush、merge/reset与迁移。SYS-SAVE 不调用成就/结局/回忆解锁逻辑，也不从 per-run save 重建 persistent。显式 New Game 只把当前 `collection_epoch_id` 复制到 rollback-owned run envelope；存档/load/rollback恢复保存时的run epoch，不覆盖canonical persistent epoch。
- SYS-SAVE 为 Journal 冻结入口与caller边界，不拥有其内容或controller。`journal_menu_gate:v1` 只在安全主菜单与`PlayableStable`游戏菜单返回true；`CriticalInteraction`、`LoadedUnvalidated`、`BlockingSafeFlow`及任一动态blocking recovery均返回false，快捷键/direct action同样不可绕过。`journal_caller_focus_catalog:v1` 恰含：主菜单`(entry=main_menu_journal,fallback=main_menu_start)`、游戏菜单`(entry=game_menu_journal,fallback=game_menu_return)`。Journal关闭后只能在对应caller已mounted时按该顺序恢复；blocking recovery抢占会销毁caller restore intent，直到进入新的安全主菜单interaction前不得恢复旧focus。
- SYS-ACCESS 只改变可达性和表现，不得创建绕过 `save_request_allowed` 的替代加载路径；UI affordance 不得反向改变 engine permission。
- SYS-TEST 的 instrumentation、protocol bomb、spy、benchmark harness 与 synthetic saves 均为 test-only，不得进入 production save 或发行 catalog。
- SYS-BUILD 不得通过替换 source hash、忽略 orphan mapping 或包含旧 catalog 来“修复”兼容性失败。

### Required Ordering

1. 批准 SYS-SAVE production record、test-fixture boundary、classification、request/UI gates 与性能合同。
2. 接受 save-contract/catalog-generation detectable state 与 atomic replacement 的新 ADR 或既有 ADR 同步修订，并更新 Control Manifest。
3. SYS-NARRATIVE 冻结 production control locations 和 source-hash-bound mappings。
4. SYS-CHOICE 与 SYS-SAVE 完成 fixture→production mapping coverage；允许多个 prehistory fixtures 映射同一 location。
5. SYS-STATE、SYS-ENDING 与 SYS-SAVE 完成合法/旧版/未知版/损坏组合验证。
6. SYS-ACCESS 完成 load/save/blocking surfaces 的输入与布局证据。
7. SYS-TEST 完成四恢复点、失败写入、重复载入、loaded-save rollback 与 benchmark fixtures。
8. SYS-BUILD 收录匹配脚本且 generation exact-match 的冻结 catalog 后，才允许 production save compatibility gate 通过。

### Bidirectional Consistency Requirements

- 系统索引中的 SYS-SAVE 依赖应更新为上述显式合同。
- SYS-TEST 的依赖应加入 SYS-SAVE，并把 load/rollback evidence 作为硬验收输入。
- SYS-PERSIST GDD 必须声明跨周目数据不随 per-run load/rollback 恢复。
- SYS-ACCESS GDD 必须复用 SYS-SAVE action-gate profile，不建立可从阻断界面返回 loaded scene 的路径。
- SYS-BUILD GDD 必须验证 checkpoint catalog、source artifact 与 production scripts 的 hash 一致。
- SYS-NARRATIVE 获批前，本 GDD 可进入 Designed/Review，但 production checkpoint catalog 与最终集成状态保持 provisional。

## Tuning Knobs

### Designer-Adjustable Save Policy

| Tuning Knob | Default / Target | Safe Range | Too Low | Too High | Required Validation |
|---|---|---|---|---|---|
| `manual_slot_page_count` | 3 pages × 6 slots = 18 slots | `1–5` pages；每页固定 6 个 | 单页容易迫使玩家覆盖关键分支存档 | 页面过多增加导航和无障碍遍历负担 | 1280×720 布局、最大字体缩放、键盘分页、空/满槽位测试 |
| `quicksave_slot_count` | 3 | `1–10` | 仅 1 个时误操作恢复空间很小 | 数量过多会让“快存”历史难以理解并增加磁盘占用 | rotation order、newest identity、重复快存与快读 |
| `autosave_slot_count` | 6 | `3–10` | 无法覆盖多个近期稳定恢复点 | 额外安全收益递减，并增加启动扫描与磁盘占用 | rotation order、三类存档性能、槽位 metadata |
| `autosave_checkpoint_policy` | 每个 `after_reaction`；以及承担章末回收的 `after_payoff` | 只能选择已登记且 `save_request_allowed=True` 的稳定点 | 过稀会让崩溃后丢失较长进度 | 每个 statement 保存会打断节奏并放大 I/O | production location catalog、跳过关键窗口、p95/max/hitch benchmark |
| `slot_summary_fields` | 章节标题、游戏时长、时间戳、兼容性提示 | 仅玩家安全且不影响恢复判定的 metadata | 玩家难以辨认存档 | 路线、choice 或 ending 信息会泄露因果和正确答案 | spoiler/anti-hidden-score scan、metadata tamper fixtures |

每页 6 个槽位属于当前 UI 布局合同；若要改变每页数量，必须同步修改 UX spec 和布局证据，不能仅调整配置值。

### Interaction Rules

- `manual_slot_page_count` 增加时，全部页面都必须通过键盘、鼠标和 self-voicing 导航；不能只验证第一页。
- `autosave_checkpoint_policy` 与 `autosave_slot_count` 共同决定实际恢复覆盖。增加频率但不增加轮换深度，会更快覆盖相邻的有效恢复点。
- 自动存档频率不得绕过 `save_request_allowed`；关键窗口触发的请求只能跳过，不能延迟补写。Autosave 没有 player-facing `ui_action_affordance`。
- 降低 quick/auto 槽位数不得改变 compatibility result、checkpoint semantics 或 persistent 状态。
- 槽位 metadata 只影响显示；任何字段组合都不能让不兼容状态通过 `after_load`。
- 每次调整槽位数量或 autosave policy 后，必须重跑 manual/quick/auto 分项 p95、最大延迟、rotation 与磁盘失败测试。

### Locked Invariants

以下不是调参项：

- Ren’Py 原生存档为唯一 per-run 主存档；
- `save_contract_sentinel="save_contract:v1"` 与受支持的 exact `save_catalog_generation_id`；
- `state_schema_sentinel="semantic_state:v2"` 与 schema version `2`；
- `ending_flow_sentinel="ending_flow:v1"` 及 `Active/Ended`/pending 合法组合；
- `SUPPORTED`、`LEGACY_INCOMPATIBLE`、`UNSUPPORTED_VERSION`、`CORRUPT_STATE`、`UNSUPPORTED_CONTROL_LOCATION` 的固定优先级；
- `UNREADABLE_SAVE` 属引擎载入前失败；
- 四类 checkpoint kind 与 SYS-CHOICE exact record schema；
- production location key/engine statement 唯一；test fixture 到 production location 为多对一覆盖；
- critical interaction 中所有 save/load/rollback 调用数为 0；
- blocking safe flow 只有主菜单和明确新游戏两个出口；
- 无 migration ADR 时不迁移旧开发存档；
- 不存在 reaction/payoff/persistent/imported mutable dedupe ledger；
- 正常存档各来源 p95 ≤500 ms、最大≤1000 ms，正常读档各槽位类 p95≤1000 ms，save/load longest-frame p95≤16.6 ms、max≤33.2 ms；
- metadata 永远不是 `after_load` 的替代权威。

改变 locked invariant 必须同步修订本 GDD、相关 ADR、Control Manifest、Entity Registry、canonical fixtures 与跨系统集成证据。

## Visual/Audio Requirements

本节定义 SYS-SAVE 的反馈语法，不批准具体图标、字体、音频文件或最终画面资产。最终样式必须在 Art Bible 与对应 UX specs 批准后冻结。

### Visual Language

- 保存、读取和阻断界面延续项目现有的深蓝底、暖米色正文与低饱和强调色方向；它们应像叙事工具而非独立“系统仪表盘”，不得压过场景与人物。
- manual、quick、auto 的类别，以及空槽、已占用、聚焦、不可用与兼容性提示，必须同时具有可读文字和非颜色单一编码的形状、边框或图标差异。红/绿、明/暗或动画不能单独承担含义。
- 槽位不得显示场景截图、人物立绘缩略图、CG、路线徽章、选择图标或结局色彩。现有原型中的 `FileScreenshot` 不属于 production SYS-SAVE 合同。
- 槽位视觉只能承载章节标题、游戏时长、时间戳和兼容性提示；不得从构图、颜色、图标或装饰泄露隐藏轴、choice、reaction、payoff、路线或 ending。
- compatibility hint 必须呈现为“提示”而非可信认证标章；即使 metadata 标记为可用，视觉也不得暗示已经通过 detached preflight 或 authoritative `after_load` validation。Raw metadata 永不直接渲染。

### Blocking Safe Flow Presentation

- `screen_blocking_restore_error` 必须运行于清除可返回 caller 的 root safe context，并以不透明背景完全遮蔽 loaded scene；底层 timers/callbacks/shortcuts 调用数为 0，不得让人物、选择、reaction、payoff、历史或普通 game menu 从透明层下可见。
- 阻断画面保持克制、稳定和可阅读：不使用故障闪烁、画面撕裂、红色频闪、突发放大、震屏、惊吓音或把“存档损坏”奇观化的演出。
- 不同失败类别可使用不同文字标题和中性图标，但不得展示 sentinel、schema、内部 ID、文件路径、异常栈、隐藏状态或结局条件。
- reduced-motion 模式下不播放位移、缩放、闪烁、短淡入或 dissolve；effective transition固定为 `0 ms`，直接建立阻断内容最终状态。关闭动画不得改变焦点或可用出口。

### Audio and Silent-Safe Operation

- 保存成功、读取请求、覆盖确认与界面导航可使用统一的中性 UI 声；manual、quick、auto 不得因“更安全”或“更正确”而拥有奖励性差异。
- `UNREADABLE_SAVE` 与 post-load 阻断可使用低强度警示声，但不得使用恐怖化失真、失败蜂鸣连发或按内部失败类别编码的音高密码。
- 静音、关闭音乐或缺失音频资产时，全部槽位状态、兼容提示、确认步骤与失败原因仍须完整可理解并可操作。
- 自发声必须读取界面标题、存档类别、槽位序号、空/占用状态、四项安全摘要、兼容提示和阻断出口；图标和声音只作补充。

### Asset Boundary

- 本系统在 GDD 阶段只提出通用存档类别图标、兼容性提示图标与阻断状态图标的需求；不申请场景缩略图或专用角色、CG、VFX 资产。
- 所有最终图标、字体与音频必须原创或来源可追踪，并拥有简体中文可读标签及替代文本。
- Art Bible 尚未建立；上述颜色仅延续已验证的方向，不构成最终色板。最终资产规格必须在 Art Bible 批准后生成。

> Full review 已覆盖信息安全、阻断语义与 silent-safe 边界；具体资产仍须在 Art Bible 批准后人工复核。

## UI Requirements

本节定义玩家可观察的行为、信息边界、焦点与安全出口。具体组件尺寸、响应式几何和视觉 token 由后续 UX specs 冻结。

### Surface Inventory

| Surface | Purpose | Required Entry | Allowed Exit |
|---|---|---|---|
| Save browser | 浏览三类槽位并向 manual slot 保存 | 仅 `PlayableStable` game menu | 返回安全 caller；成功保存后留在 browser 或明确返回 |
| Load browser | 浏览并请求加载任一来源的槽位 | 主菜单或 `PlayableStable` game menu | 返回安全 caller；成功加载进入 validation，不先显示 loaded scene |
| Overwrite confirmation | 确认覆盖已占用 manual slot | Save browser | 取消返回原 browser；确认只执行一次覆盖 |
| Load confirmation | 确认放弃当前未保存进度并安装所选存档 | Load browser 且 detached preflight 未阻断 | 取消返回原 browser；确认只执行一次原生 load |
| `screen_blocking_restore_error` | 阻止 post-load 不安全状态继续 | `LoadedUnvalidated` validation failure | 仅“返回主菜单”或“明确开始新游戏” |

普通 save/load game menu 不得在 `CriticalInteraction`、`LoadedUnvalidated` 或 `BlockingSafeFlow` 成为绕过 action gate 的替代入口。

### Journal Entry and Return Contract

- 安全主菜单的 `main_menu_journal` 与 `PlayableStable` 游戏菜单的 `game_menu_journal` 是唯一 Journal entry semantic IDs；两者调用同一 Journal open request，但携带不同 caller context。
- 主菜单入口不依赖 per-run save state；若 persistence recovery 等全局阻断状态已激活，则由对应上游 gate 拒绝，Journal不得短暂出现。
- 游戏菜单入口仅在 `journal_menu_gate:v1(PlayableStable)=true` 时 visible/enabled/focusable。`CriticalInteraction`、`LoadedUnvalidated`、`BlockingSafeFlow`、unsupported/corrupt load flow 及动态 gate revocation 时均为 `false/false/false`，direct action、快捷键、screen return和替代activation调用数为0且不排队。
- 正常关闭时，主菜单依次尝试`main_menu_journal→main_menu_start`，游戏菜单依次尝试`game_menu_journal→game_menu_return`；只在caller已经mounted后恢复，不按坐标或旧displayable猜测。
- Journal打开期间若进入blocking recovery，SYS-SAVE/root recovery先销毁可返回caller context，再抢占Journal；旧caller focus restore、Journal close callback、save/load/rollback与底层action调用数均为0。恢复流程进入新的安全主菜单后，那是新interaction，不恢复旧Journal caller。

### Slot Browser Structure

1. 顶层以明确标记的 `手动存档`、`快速存档`、`自动存档` 三个分区呈现；切换分区不改变任何 slot 数据。
2. manual 默认 3 页、每页固定 6 个 slots。提供“上一页”“下一页”和 `当前页 / 总页数`；分页不循环，第一页的上一页与最后一页的下一页不可用且不可误触。
3. quick 分区显示 3 个按 newest identity 排序的 slots；auto 分区显示 6 个按 newest identity 排序的 slots。二者无需分页。
4. Save browser 中只有 manual slots 可由玩家选择写入；quick 与 auto 分区只读，并解释它们分别由 quicksave action 与 autosave policy 管理。Load browser 中三类已占用 slots 均可请求加载。
5. 空 slot 返回 `EMPTY_SLOT_NOOP` 且不能加载；已有 manual slot 被选择保存时必须先进入 overwrite confirmation。quick/auto rotation 不弹出逐槽覆盖确认。
6. Engine request permission 由 `save_request_allowed` 控制；player-facing visible/enabled/focusable 由 `ui_action_affordance` 控制。不可执行的隐藏入口、快捷键或替代 activation 不得保留焦点，也不得把请求排队到稍后执行。

### Slot Card Contract

每个 slot card 只显示：

- 玩家可读的章节标题；
- 累计游戏时长；
- 本地时间戳；
- 明确标为非权威提示的兼容性状态。

slot card 不得显示截图、路线、choice 文本或 ID、五轴、token、reaction、payoff、pending ending、结局名称、隐藏进度、排名或“最佳路线”提示。章节标题只由合法 `chapter_summary_id` 查内置 catalog 取得；raw metadata、未知 ID、markup 或双向控制字符不得直接渲染。缺失或被篡改的 metadata 使用中性未知提示，不得阻止真实 load validation，也不得把不安全存档标成 authoritative `SUPPORTED`。

兼容性提示至少拥有 `未知/需验证`、`旧版`、`版本不受支持`、`状态异常`、`位置不受支持` 五种玩家可读表现；`UNREADABLE_SAVE` 只在引擎读取失败后于当前 Load browser 显示，`INTERNAL_LOAD_VALIDATION_FAILURE` 只在 blocking surface 显示为内部恢复失败。最终简体中文文案在 `SAVE-Q3` 关闭前保持 provisional。

### Load and Failure Flow

1. 玩家选择已占用 slot 后，Load browser 可基于 metadata 给出提示，并执行不改变当前游戏状态的 detached preflight。
2. `UNREADABLE_SAVE` 或 detached preflight 已确定的 compatibility failure 不替换当前安全上下文；Load browser 保持打开、焦点回到失败 slot，并允许选择其他槽位或返回。
3. Preflight 未阻断时显示加载确认，明确说明“加载会放弃当前未保存进度”；默认焦点为“取消”。主菜单加载不显示“当前进度”警告，但仍显示 slot 身份。
4. 玩家确认后调用原生 load；引擎成功安装存档后立即进入非玩家可见的 `LoadedUnvalidated`。只有 `SUPPORTED` 才显示首个可交互稳定帧。
5. Engine-control failure、post-install `LEGACY_INCOMPATIBLE`、`UNSUPPORTED_VERSION`、`CORRUPT_STATE`、`UNSUPPORTED_CONTROL_LOCATION` 与 `INTERNAL_LOAD_VALIDATION_FAILURE` 均先进入 root safe context，再显示共享 blocking surface。
6. blocking surface 包含类别安全标题、简短说明以及两个游戏内出口。默认焦点固定在“返回主菜单”；“明确开始新游戏”必须使用不会与普通确认混淆的完整标签。
7. blocking surface 屏蔽 Escape、Return-to-caller、rollback、save/load、quick actions、skip、auto 和 history return；重复输入只能让首个退出动作执行一次。OS close 退出应用，不恢复 caller。

### Input, Focus, Layout and Accessibility

- 在 1280×720、默认与 `1.5×` 最大字体缩放下，标题、分区标签、6 个 manual slot cards、分页、加载/覆盖确认动作和 blocking exits 均不得重叠或裁切。字体放大可触发 card 内换行或纵向重排，不得隐藏字段。
- Save/Load browser 的键盘顺序固定为：界面标题 → 分区切换 → 当前分区 slots（阅读顺序）→ manual 分页 → 返回。切换 manual 页面后，焦点落在新页第一个可用 slot；切换分区后落在该分区首个 slot。
- Overwrite confirmation 的顺序固定为目标 slot 摘要 → “取消” → “确认覆盖”，默认焦点为“取消”。
- Load confirmation 的顺序固定为目标 slot 安全摘要 → “取消” → “确认加载”，默认焦点为“取消”；从 `PlayableStable` 进入时必须朗读“当前未保存进度将被放弃”。
- blocking surface 的顺序固定为标题 → 类别安全说明 → “返回主菜单” → “明确开始新游戏”，默认焦点为“返回主菜单”。
- 鼠标、键盘与已登记替代 activation 必须调用同一 canonical action；不要求 hover、限时输入、声音、动画或精确指针操作。
- focus 必须使用高对比边框、形状或位置变化，不能只改变颜色。高对比模式和 self-voicing 不得改变 slot 顺序、分类结果、默认安全焦点或 action gate。
- 右上角 quick actions 必须从属于叙事内容，且在 critical interaction 与 blocking flow 中隐藏并移出焦点。切片中“快捷按钮过大”与“正文字重过重”是待修问题，不是 production 基线。

### Existing Implementation Boundary

当前 `game/screens.rpy` 与垂直切片只证明基础 save/load screen、六槽布局和键盘入口可行；其中单页六槽、`FileScreenshot`、缺少 manual/quick/auto 分区、缺少分页与 blocking surface 的实现均不得直接视为本合同已完成。正式 production 实现必须依据后续 UX specs 从头验证。

> **UX Flag — SYS-SAVE**：在创建 UI stories 前，必须分别为 Save/Load browser、Overwrite Confirmation 与 Blocking Restore Error 创建 UX specs。Stories 应引用 `design/ux/` 中获批规格，并复用本 GDD 的 slot、action-gate、信息安全与焦点合同。

## Acceptance Criteria

以下标准均须由不依赖玩家肉眼判断的测试证据验证；涉及计数时，测试观察器只存在于测试构建，不得写入正式存档或 production catalog。

### Save Creation and Slot Integrity

- **SAVE-WRITE-001 — Manual save**：**GIVEN** 玩家位于任一已登记且 `save_request_allowed=True` 的稳定控制点，**WHEN** 玩家向空 manual slot 保存，**THEN** 该 slot 生成可读取存档，保存的 save-contract/catalog generation、semantic、ending 与 frozen rollback-ownership manifest 声明的全部 per-run fields 均等于触发瞬间的深值快照。
- **SAVE-WRITE-002 — Quicksave rotation**：**GIVEN** 3 个 quicksave slots 已满且当前位于可保存稳定点，**WHEN** 再次 quicksave，**THEN** 仅最旧 quicksave 被替换，新存档成为 newest，其他两个 slot 的内容与顺序保持有效。
- **SAVE-WRITE-003 — Autosave rotation**：**GIVEN** 6 个 autosave slots 已满，**WHEN** 合法 `after_reaction` 或章末 `after_payoff` 触发 autosave，**THEN** 仅最旧 autosave 被替换，新存档成为 newest，且未登记或 action gate 关闭的控制点不生成补写 autosave。
- **SAVE-WRITE-004 — Overwrite confirmation**：**GIVEN** 目标 manual slot 已有存档，**WHEN** 玩家取消覆盖确认，**THEN** 原 slot 字节、时间戳和 metadata 均不变；**WHEN** 玩家确认覆盖且写入成功，**THEN** slot 只包含新快照。
- **SAVE-WRITE-005A — Interrupted overwrite**：**GIVEN** 任一来源正在覆盖既有合法 slot，**WHEN** 在序列化、临时写入或替换边界分别注入 I/O 失败，**THEN** slot 最终状态只能是完整旧存档或完整新存档；`不存在` 与任何被识别为 `SUPPORTED` 的部分写入均失败。
- **SAVE-WRITE-005B — Interrupted first write**：**GIVEN** 任一来源正在写入空 slot，**WHEN** 在三个相同边界分别注入 I/O 失败，**THEN** slot 最终状态只能是不存在或完整新存档。
- **SAVE-WRITE-006 — Metadata is non-authoritative**：**GIVEN** 存档主体不变而章节标题、游玩时长、时间戳或兼容提示 metadata 被删除、伪造或交换，**WHEN** 扫描 slot 并执行真实加载验证，**THEN** authoritative compatibility result 与恢复状态不因 metadata 改变。

### Compatibility Classification

- **SAVE-LOAD-000 — Empty slot no-op**：**GIVEN** UI slot 为空，**WHEN** 玩家尝试激活，**THEN** 返回 `EMPTY_SLOT_NOOP`，detached inspection、原生 load 与 compatibility classifier 调用数均为 0，焦点保持该 slot。
- **SAVE-LOAD-001 — Unreadable occupied container**：**GIVEN** 曾占用 slot 的容器丢失、损坏或引擎无法反序列化，**WHEN** 玩家请求加载，**THEN** 在 state installation 前返回 `UNREADABLE_SAVE`，且不进入 loaded scene。
- **SAVE-LOAD-002 — Legacy sentinel**：**GIVEN** `save_contract_sentinel`、`save_catalog_generation_id`、`state_schema_sentinel` 或 `ending_flow_sentinel` 任一为 `None`，**WHEN** detached preflight 或 `after_load` 分类，**THEN** 返回 `LEGACY_INCOMPATIBLE`，不继续 semantic、ending 或 location 验证。
- **SAVE-LOAD-003 — Unknown semantic version**：**GIVEN** semantic sentinel 存在但不是受支持的精确值，**WHEN** `after_load` 分类，**THEN** 返回 `UNSUPPORTED_VERSION`，且不运行 semantic-state validator。
- **SAVE-LOAD-004 — Unknown ending version or wrong exact type**：**GIVEN** ending sentinel 未知，或任一 sentinel 的 exact type 不合法，**WHEN** `after_load` 分类，**THEN** 返回 `UNSUPPORTED_VERSION`，且不运行 state validator。
- **SAVE-LOAD-004A — Unknown save contract or catalog generation**：**GIVEN** save-contract sentinel 未知、catalog generation 不在支持矩阵，或任一项 wrong exact type，**WHEN** preflight/`after_load` 分类，**THEN** 返回 `UNSUPPORTED_VERSION`，且 semantic、ending 与 location validators 调用数均为 0。
- **SAVE-LOAD-005 — Invalid semantic state**：**GIVEN** 全部 required sentinels/generation 均受支持但 semantic envelope 的 schema、字段、exact type、范围或不变量非法，**WHEN** 验证，**THEN** 返回 `CORRUPT_STATE`。
- **SAVE-LOAD-006 — Invalid ending state**：**GIVEN** semantic state 合法但 `ending_flow:v1` 的 lifecycle、pending ID 或组合非法，**WHEN** 验证，**THEN** 返回 `CORRUPT_STATE`。
- **SAVE-LOAD-007 — Unsupported control location**：**GIVEN** sentinels/generation、semantic 与 ending state 合法，但 current statement 对应 production location match count 为 0，**WHEN** 验证，**THEN** 返回 `UNSUPPORTED_CONTROL_LOCATION`。
- **SAVE-LOAD-007A — Internal catalog/source failure**：**GIVEN** match count>1、当前 catalog structure 非法或当前 catalog hash 与当前 source artifact 不匹配，**WHEN** 验证，**THEN** 返回 `INTERNAL_LOAD_VALIDATION_FAILURE`，不得归因于玩家存档。
- **SAVE-LOAD-008 — Checkpoint coherence failure**：**GIVEN** control location 可映射但 restored semantic/ending lifecycle 与该 location 的 checkpoint kind 不相容，**WHEN** 验证，**THEN** 返回 `CORRUPT_STATE`；validator 不读取 test fixture 的单一 expected history/axes。
- **SAVE-LOAD-009 — Supported save**：**GIVEN** 容器可读、required sentinels/generation 受支持、semantic/ending 合法、location 唯一可映射且 checkpoint-state coherent，**WHEN** 完成验证，**THEN** 唯一结果为 `SUPPORTED`，随后才允许显示 loaded scene。
- **SAVE-LOAD-010 — Classification precedence**：**GIVEN** nonempty manifest 列出的 required defect dimensions 与 exact cross-product count，**WHEN** 参数化运行每格，**THEN** 结果严格遵循 `EMPTY_SLOT_NOOP/UNREADABLE_SAVE`（pre-load，互斥）→ malformed aggregate `INTERNAL_LOAD_VALIDATION_FAILURE` → `LEGACY_INCOMPATIBLE` → `UNSUPPORTED_VERSION` → `INTERNAL_LOAD_VALIDATION_FAILURE`（current catalog/artifact）→ `CORRUPT_STATE`（semantic/ending）→ `UNSUPPORTED_CONTROL_LOCATION` → `INTERNAL_LOAD_VALIDATION_FAILURE`（duplicate mapping）→ `CORRUPT_STATE`（checkpoint coherence）→ `SUPPORTED`；缺失 manifest、空 dimension 或实际 case count 不等于声明 cross-product 均固定失败。

### Checkpoint and Control-Location Catalog

- **SAVE-CATALOG-001 — Four checkpoint kinds**：**GIVEN** nonempty production location catalog 与 nonempty test fixture manifest，**WHEN** 构建验证，**THEN** kind 只允许 `before_choice`、`after_reaction`、`before_payoff`、`after_payoff`，且每个 kind 至少有一条 production record 与一条 canonical fixture。
- **SAVE-CATALOG-002 — Exact schemas**：**GIVEN** catalog 与 fixture records，**WHEN** schema validator 执行，**THEN** `choice_restore_checkpoint_record` 保持 SYS-CHOICE 的 11-field exact contract，`restore_control_location_record` 保持本 GDD 的 7-field exact contract，`save_restore_fixture_record` 保持本 GDD 的 8-field exact contract；缺字段、多字段或 wrong exact type 均失败。
- **SAVE-CATALOG-003 — Fixture coverage mapping**：**GIVEN** production locations 与 test fixtures，**WHEN** 按 `control_location_id + checkpoint_kind` join，**THEN** 每个 fixture 恰好匹配一条 production record，每条 production record 至少有一条 fixture；多个不同 prehistory fixtures 映射同一 production record 合法且不得要求 expected history/axes 相等。
- **SAVE-CATALOG-004 — Orphan or production duplicate rejection**：**GIVEN** fixture orphan、production record 无 fixture、duplicate fixture ID、duplicate production key 或同一 engine statement 多映射，**WHEN** build validator 运行，**THEN** 构建失败并报告冲突 key；合法的多 fixture 覆盖不得误报。
- **SAVE-CATALOG-005 — Source identity drift**：**GIVEN** 已登记脚本 statement、稳定 `from` identity 或 source artifact hash 被修改，**WHEN** 构建 catalog，**THEN** 未同步迁移证据的 mapping 失败，不得静默把旧存档映射到相邻 label。
- **SAVE-CATALOG-006 — Unstable control site rejection**：**GIVEN** production `call` 缺少稳定 `from` return identity、目标动态生成、clean build 无法延续声明的 statement identity 或以文件行号作为持久 identity，**WHEN** catalog validator 运行，**THEN** 构建失败并指出不稳定控制位置。
- **SAVE-CATALOG-007 — Authoritative generation**：**GIVEN** release catalog、current canonical CFG artifact 与 save initialization constants，**WHEN** build gate 运行，**THEN**全部 production records、rollback-owned `save_catalog_generation_id` 与 artifact generation exact-equal；任一不一致固定失败。

### Restore Semantics

- **SAVE-RESTORE-001 — Before choice**：**GIVEN** 支持的 `before_choice` 存档，**WHEN** 加载并重新确认该 choice，**THEN** 加载瞬间该 choice 及其后果尚未发生；当前 observation window 内 commit 和 reaction 各恰好发生一次。
- **SAVE-RESTORE-002 — After reaction**：**GIVEN** 支持的 `after_reaction` 存档，**WHEN** 加载并前进到下一稳定点，**THEN** expected history/axes 与存档快照相等，目标 commit 和 reaction 调用数均为 0。
- **SAVE-RESTORE-003 — Before payoff**：**GIVEN** 支持的 `before_payoff` 存档，**WHEN** 加载并前进穿过目标 payoff，**THEN** commit/reaction 调用数均为 0，目标 payoff 在当前 observation horizon 内恰好发生一次。
- **SAVE-RESTORE-004 — After payoff**：**GIVEN** 支持的 `after_payoff` 存档，**WHEN** 加载并前进到下一控制边界，**THEN**已完成的目标 payoff 调用数为 0，history/axes 不被重复修改。
- **SAVE-RESTORE-005 — Origin/checkpoint matrix**：**GIVEN** manual、quick、auto 三种来源分别在四类 checkpoint 生成的 12 个 canonical saves，**WHEN** 每个 fixture 独立加载，**THEN** 均满足对应 SAVE-RESTORE-001～004，且来源不改变恢复语义。
- **SAVE-RESTORE-006 — Repeatable pre-payoff load**：**GIVEN** 同一个 `before_payoff` 存档，**WHEN** 在独立运行中反复加载并穿过 payoff，**THEN** 每次恢复 traversal 都产生一次目标 payoff，不因 persistent 或独立 mutable ledger 丢失。
- **SAVE-RESTORE-007 — Ending-entry save**：**GIVEN** 支持的存档保存于 ending entry 后且 lifecycle 为 `Ended`，**WHEN** 加载，**THEN** 精确恢复 `Ended` 与 pending ending ID，从保存控制位置继续，canonical resolver 调用数为 0。
- **SAVE-RESTORE-008 — Rollback across ending entry**：**GIVEN** 当前处于 ending entry 后，**WHEN** rollback 到其前方并以相同 semantic snapshot 再次求值，**THEN** lifecycle、pending 值和 semantic state 回到对应 `Active` 快照，并再次得到相同结局。
- **SAVE-RESTORE-011 — Ending completion save/load**：**GIVEN** ending label terminal completion node 之前与之后的合法存档，**WHEN** 分别加载，**THEN** 之前的存档恢复 `ending_completion_event_record` 缺失且 ending request count 为 0；之后的存档恢复该 record、`completed_event_id=ending_completed:{ending_id}` 与控制位置，canonical persistent membership 保持不变，resolver 调用数为 0。
- **SAVE-RESTORE-012 — Rollback across ending completion**：**GIVEN** completion 已成功落盘后，**WHEN** rollback 到 terminal completion node 之前，**THEN** rollback-owned completion event/control state 恢复为未完成，12-leaf persistent snapshot、ending membership、epoch 与 writer/flush counts 深值不变；再次前进到同一 node 返回 `DUPLICATE_NOOP` 且 notification count 为 0。
- **SAVE-RESTORE-009 — Loaded-save rollback boundary**：**GIVEN** 玩家成功加载后继续游玩，**WHEN** rollback 到 loaded save 自身 rollback history 的最早可达点，**THEN**只恢复该 save 所含 rollback-owned 状态，不恢复执行 load 前的另一局状态；`after_load` 临时诊断与 action gates 不存在于 store/rollback log。
- **SAVE-RESTORE-010 — Exhausted rollback**：**GIVEN** rollback history 已耗尽，**WHEN** 玩家请求 rollback，**THEN** action 的 visible/enabled/focusable 为 `false/false/false`、invocation count 为 0、当前深值状态不变，且不跳转主菜单或新游戏。

### Action Gates and Blocking Flow

- **SAVE-GATE-001 — Stable-point request allowance**：**GIVEN** 当前 control location 已登记、没有 critical interaction 且请求来源受支持，**WHEN**计算 `save_request_allowed`，**THEN** 对应 manual/quick/auto request 返回 `True`；auto save 不创建 UI affordance。
- **SAVE-GATE-001A — UI/request separation**：**GIVEN** 完整 nonempty phase×action manifest，**WHEN**逐格计算 request permission 与 player-facing affordance，**THEN** engine result 与闭集矩阵 exact-equal；仅 player-facing 动作拥有 visible/enabled/focusable，unknown/missing/extra/wrong-type 输入均返回 `False`。
- **SAVE-GATE-002 — Critical-interaction denial**：**GIVEN** commit→reaction 或 bounded reaction interaction 正在进行，**WHEN** 玩家、快捷键、脚本或替代输入请求 save、load 或 rollback，**THEN** 三类调用数均为 0、当前交互继续，且请求不排队到交互结束后补执行。
- **SAVE-GATE-003 — Canonical operation mutex**：**GIVEN** manual save、quick save、background autosave、load 或 rollback 任一请求已被接受且尚未完成，**WHEN**任一来源再次请求这五类操作，**THEN**首个操作继续且后续 invocation count 为 0、queue length 为 0；操作结束后只接受新的显式/正常周期请求，不回放被拒绝请求。
- **SAVE-BLOCK-001 — Enter root blocking context**：**GIVEN** 任一 post-install/engine-control 分类失败或 `INTERNAL_LOAD_VALIDATION_FAILURE`，**WHEN**进入 `screen_blocking_restore_error`，**THEN**可返回 caller 的 screen/call context count 为 0；loaded scene、choice、reaction、payoff、pause UI 与普通 game menu 不可见、不更新且不接收焦点，底层 timer/callback/shortcut invocation count 为 0。
- **SAVE-BLOCK-002 — No screen escape to caller**：**GIVEN** blocking screen 激活，**WHEN** 玩家请求 rollback、普通/快速存读档、skip、auto、history return、screen return、Escape/right-click dismissal，**THEN**仍留在阻断流程，不返回 loaded scene。
- **SAVE-BLOCK-002A — OS quit**：**GIVEN** blocking screen 激活，**WHEN** OS window close 请求退出，**THEN**应用退出，且 loaded scene visible frame、callback invocation 与 caller return count 均为 0。
- **SAVE-BLOCK-003 — Main-menu exit**：**GIVEN** blocking screen 激活，**WHEN** 玩家选择“返回主菜单”，**THEN**不安全的当前上下文被清除并进入主菜单，screen stack 不可返回 loaded scene。
- **SAVE-BLOCK-004 — Explicit new game**：**GIVEN** blocking screen 激活，**WHEN** 玩家明确选择“开始新游戏”，**THEN** `save_contract_sentinel`、当前 `save_catalog_generation_id`、semantic、ending lifecycle与rollback-owned `collection_epoch_id` 被同一入口显式初始化；canonical 12-leaf persistent root深值不变，重复激活只允许第一个退出动作执行。

### Journal Integration

- **SAVE-JOURNAL-001 — Safe dual entry**：**GIVEN**安全主菜单与`PlayableStable`游戏菜单，**WHEN**分别激活`main_menu_journal`/`game_menu_journal`，**THEN**`journal_menu_gate:v1`返回true、Journal open request各恰1，caller context exact记录；save payload、rollback state与12-leaf persistent root深值不变。
- **SAVE-JOURNAL-002 — Normal caller restore**：**GIVEN**从两种caller打开后正常关闭及entry present/absent矩阵，**WHEN**caller mounted，**THEN**主菜单exact选择`main_menu_journal→main_menu_start`首个存在ID，游戏菜单exact选择`game_menu_journal→game_menu_return`首个存在ID；mount前focus call=0、跨catalog target=0、stale displayable=0。
- **SAVE-JOURNAL-003 — Four blocked phases**：**GIVEN**`CriticalInteraction`、`LoadedUnvalidated`、`BlockingSafeFlow`与unsupported/corrupt-load blocking path，**WHEN**枚举菜单、快捷键、direct screen action与替代activation，**THEN**Journal visible/enabled/focusable=`false/false/false`、open request=0、queue length=0，普通game menu或loaded scene不可被Journal绕过。
- **SAVE-JOURNAL-004 — Recovery preemption**：**GIVEN**Journal从`PlayableStable`已打开且随后动态进入blocking recovery，**WHEN**root safe context接管，**THEN**Journal controller、caller context与restore intent各清除恰1，old caller focus/close callback/save/load/rollback/bottom action counts均0；只显示blocking surface，新安全主菜单interaction不恢复旧caller。

### Persistence and Ownership Boundaries

- **SAVE-BOUNDARY-001 — Persistent unchanged by load**：**GIVEN** nonempty frozen schema-v2 SYS-PERSIST ownership manifest、`leaf_field_count=12`与逐字段深值快照，**WHEN** 任一支持存档加载完成，**THEN**manifest generation/field count exact-match且12个owned leaves与快照相等；save中的run epoch照常恢复，但不得写回canonical root；missing/empty/stale manifest固定失败。
- **SAVE-BOUNDARY-002 — Persistent unchanged by rollback**：**GIVEN**同一12-leaf manifest与深值快照，**WHEN** rollback 穿过 choice、reaction、payoff、ending entry 或 loaded-save history，**THEN**12个owned leaves与快照相等，rollback-owned run epoch恢复到历史值；不声明恢复执行load前的另一局persistent状态。
- **SAVE-BOUNDARY-003 — No foreign ownership**：**GIVEN** production build 与 save payload，**WHEN**执行静态及运行时 ownership scan，**THEN** SYS-SAVE 不创建或写入 achievement、ending/wish unlock、persistent migration、reaction dedupe 或 payoff dedupe ledger。
- **SAVE-BOUNDARY-004 — Trusted-local preflight containment**：**GIVEN** 本机游戏生成且未经外部修改的 slot，**WHEN** detached preflight 执行，**THEN**当前 run/persistent 深值不变；产品不提供外部导入，且本标准不把 save-data inspection/`after_load` 宣称为任意第三方 pickle 的安全沙箱。

### Slot UI and Accessibility

- **SAVE-UI-001 — Slot layout**：**GIVEN** 1280×720 viewport 与默认/`1.5×` 字体，**WHEN**打开 save/load screen，**THEN**每页恰有 6 个 manual slots、可到达 3 个 quick slots 与 6 个 autosave slots，空、已占用、当前焦点和不可兼容状态可区分，`intersection_count=0`、`clipped_glyph_count=0`。
- **SAVE-UI-002 — Spoiler-safe summary**：**GIVEN** 任一 slot 及合法/未知/超长/markup/bidi/wrong-type metadata fixtures，**WHEN**显示摘要，**THEN**只允许由合法 `chapter_summary_id` 解析的章节标题、游戏时长、时间戳和兼容性提示；raw metadata render count=0，不显示路线、choice、隐藏轴、reaction、payoff 或 ending 信息。
- **SAVE-UI-003 — Category-safe error copy**：**GIVEN** 每种 load failure category，**WHEN**显示错误，**THEN**玩家文案仅说明安全类别与可执行出口，不泄露内部 sentinel、schema、文件路径或异常栈；精确诊断只进入开发日志。
- **SAVE-ACCESS-001 — Complete keyboard path**：**GIVEN** 鼠标不可用，**WHEN**玩家仅用键盘操作 save/load、分页、slot 选择、load/overwrite confirmation 和 blocking exits，**THEN**所有动作均可完成，焦点始终可见且顺序确定。
- **SAVE-ACCESS-002 — Self-voicing and scaled text**：**GIVEN** nonempty mode manifest 中 self-voicing、`1.5×` 字体缩放、高对比及其 required combined modes，**WHEN**在 1280×720 遍历全部 save/load、load-confirmation 与 blocking surfaces，**THEN**实际 case count 与 manifest 声明 exact-equal；每个 slot 的类型、位置、状态、摘要与动作均有可理解标签，raw metadata 不朗读，`intersection_count=0`、`clipped_glyph_count=0`，两个 blocking exits 始终可达。

### Performance and Build Integration

- **SAVE-PERF-001 — Save budget and hitch**：**GIVEN** reference hardware、最大合法 production fixture、cold/warm cohorts 与每种来源 5 次 warmup 后至少 30 次正式样本，**WHEN**验证 exact keys/types/counts 并以 nearest-rank 计算 manual、quick、auto 延迟，**THEN**每种来源 end-to-end p95≤500 ms、max≤1000 ms、longest-frame p95≤16.6 ms、max≤33.2 ms；报告保留全部原始样本与硬件/环境标识。
- **SAVE-PERF-002 — Load budget and hitch**：**GIVEN**同一 protocol 与 manual/quick/auto slot classes，**WHEN**从确认加载测至 `after_load` 完成后的首个 rendered/input-accepting stable frame，**THEN**每类 end-to-end p95≤1000 ms、longest-frame p95≤16.6 ms、max≤33.2 ms；NaN、±∞、negative、wrong type、<30、missing/extra keys 或长度不一致均固定失败。
- **SAVE-BUILD-001 — Production catalog freeze**：**GIVEN** SYS-NARRATIVE production mappings 尚未批准、任一 source/generation hash 不匹配、production catalog validator 或 fixture coverage validator 失败，**WHEN**执行 release build gate，**THEN** production checkpoint catalog 不得冻结且构建不得宣称 save compatibility ready。
- **SAVE-BUILD-002 — Test observer exclusion**：**GIVEN** release candidate，**WHEN**扫描归档、store 和 save payload，**THEN** protocol bombs、spies、benchmark harness、synthetic saves 与 traversal counters 均不存在于 production runtime 和正式存档。
- **SAVE-BUILD-003 — Canonical evidence bundle**：**GIVEN** release candidate，**WHEN**执行 SYS-SAVE gate，**THEN**证据包包含 nonempty 分类 cross-product、12 项 origin/checkpoint matrix、fixture→production coverage、I/O fault injection、loaded-save rollback、ending rollback、persistent isolation、accessibility traversal、catalog generation/source hash 校验及 end-to-end/hitch 原始样本；任一 manifest 为空、case count 不符或证据缺失即 gate 失败。

> Full `qa-lead` review incorporated exact field counts、split write outcomes、nonempty manifests/cross-products、machine-observable blocking semantics 与 invalid benchmark inputs。

## Open Questions

以下问题不重开已经批准的行为合同；它们只关闭实现机制、生产内容或验证证据。

| ID | Open Question | Owner | Target Date | Closure Evidence |
|---|---|---|---|---|
| `SAVE-Q1` | Ren’Py 8.5.3 下，如何实现 manual/quick/auto slot 的 atomic replacement，并在序列化、临时写入和替换阶段稳定注入 I/O failure？ | Engine Programmer + SYS-TEST / Andwey | Foundation/Core stories 进入 Ready 前 | 接受的 ADR 或 story-level technical contract、三阶段 fault-injection harness；既有槽位仅旧/新，空槽位仅不存在/新，partial-write negative fixtures |
| `SAVE-Q2` | 四类 checkpoint 的 production `control_location_id`、`engine_statement_id`、`source_artifact_hash`、`catalog_generation_id`、`action_gate_profile_id` 与 observation horizon 如何完整冻结？ | SYS-NARRATIVE + SYS-CHOICE / Andwey | Production checkpoint catalog freeze 前 | 7-field production catalog、11-field choice fixtures、8-field save fixtures、四 kind 全覆盖、fixture→production coverage report、orphan/duplicate/hash/generation/clean-build drift negative fixtures |
| `SAVE-Q3` | `UNREADABLE_SAVE`、`LEGACY_INCOMPATIBLE`、`UNSUPPORTED_VERSION`、`CORRUPT_STATE`、`UNSUPPORTED_CONTROL_LOCATION` 与 `INTERNAL_LOAD_VALIDATION_FAILURE` 的最终简体中文标题、说明、自发声标签和非颜色兼容图标分别是什么？ | UX + SYS-ACCESS / Andwey | SYS-SAVE UX specs 批准前 | Localized copy catalog、self-voicing transcript、1280×720 与 1.5× 字体 captures、spoiler/internal-ID/raw-metadata scan |
| `SAVE-Q4` | 性能门槛使用哪台最低 reference hardware，以及 timer、OS/build、电源、后台进程、cold/warm 文件缓存、GC、磁盘空间和最大合法内容 fixture 如何冻结？ | SYS-TEST + Engine Programmer / Andwey | 首次 SYS-SAVE performance gate 前 | Benchmark manifest、硬件标识、固定环境说明、每类 5 次 warm-up + ≥30 个 end-to-end/longest-frame 原始样本及 nearest-rank 报告 |
| `SAVE-Q5` | 已冻结的schema-v2 12-leaf persistent边界与rollback-owned run epoch如何通过联合engine evidence关闭？ | SYS-PERSIST + SYS-TEST / Andwey | SYS-PERSIST GDD批准前 | Nonempty versioned 12-leaf ownership manifest、合法字段深值snapshot fixtures、old-save/new-game epoch fixtures、foreign-write scan与四类operation preservation tests |
| `SAVE-Q6` | 若未来提出 semantic schema、ending lifecycle 或 checkpoint catalog 新版本，公开支持哪些来源版本、采用何种逐版本迁移路径与 rollback policy？ | Producer + Engine Programmer / Andwey | 首次公开 schema/catalog 变更提案时 | 独立 Accepted migration ADR、支持矩阵、逐版本 golden saves、failure fixtures 与回退/撤销方案 |
| `SAVE-Q7` | `save_contract_sentinel`、`save_catalog_generation_id`、detached preflight、engine load-failure label 与 root safe context 如何同步进入架构控制面？ | Architect + Engine Programmer / Andwey | 任一 SYS-SAVE implementation story 进入 Ready 前 | Accepted ADR 或 ADR-0002/0005 amendments、updated Control Manifest、new-game initialization fixture、legacy/unknown generation fixtures、pre/post-install failure routing tests |

当前首发仍执行“不迁移旧开发存档”的已批准策略；`SAVE-Q6` 未触发前不得实现猜测性迁移。
