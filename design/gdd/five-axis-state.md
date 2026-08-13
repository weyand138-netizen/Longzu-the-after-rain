# 五轴局内状态系统

> **Status**: Approved
> **System ID**: SYS-STATE
> **Author**: Andwey + Codex
> **Last Updated**: 2026-08-04
> **Implements Pillar**: 看见未说出口的话；温柔必须被挣来；悲剧也是完整答案
> **Creative Director Review (CD-GDD-ALIGN)**: Skipped — Solo mode
> **Independent Design Review**: APPROVED — Twelfth Final Targeted Closure, 2026-07-27
> **SYS-ENDING Downstream Amendment**: Axis/history replay、presentation-safe fallback anchor 与 detectable ending lifecycle synchronized, 2026-07-27
> **Review Log**: [five-axis-state-2026-07-23.md](reviews/five-axis-state-2026-07-23.md)
> **Second Review Log**: [five-axis-state-second-review-2026-07-23.md](reviews/five-axis-state-second-review-2026-07-23.md)
> **Third Review Log**: [five-axis-state-third-review-2026-07-23.md](reviews/five-axis-state-third-review-2026-07-23.md)
> **Fourth Review Log**: [five-axis-state-fourth-review-2026-07-24.md](reviews/five-axis-state-fourth-review-2026-07-24.md)
> **Fifth Review Log**: [five-axis-state-fifth-review-2026-07-24.md](reviews/five-axis-state-fifth-review-2026-07-24.md)
> **Sixth Review Log**: [five-axis-state-sixth-review-2026-07-24.md](reviews/five-axis-state-sixth-review-2026-07-24.md)
> **Seventh Review Log**: [five-axis-state-seventh-review-2026-07-24.md](reviews/five-axis-state-seventh-review-2026-07-24.md)
> **Eighth Review Log**: [five-axis-state-eighth-review-2026-07-24.md](reviews/five-axis-state-eighth-review-2026-07-24.md)
> **Ninth Review Log**: [five-axis-state-ninth-review-2026-07-26.md](reviews/five-axis-state-ninth-review-2026-07-26.md)
> **Tenth Review Log**: [five-axis-state-tenth-review-2026-07-26.md](reviews/five-axis-state-tenth-review-2026-07-26.md)
> **Eleventh Review Log**: [five-axis-state-eleventh-review-2026-07-26.md](reviews/five-axis-state-eleventh-review-2026-07-26.md)
> **Twelfth Review Log**: [five-axis-state-twelfth-review-2026-07-27.md](reviews/five-axis-state-twelfth-review-2026-07-27.md)

## Overview

五轴局内状态系统将玩家在七天内表现出的理解、尊重自主、面对真相、完成准备与承担代价，分别记录为 `understanding`、`autonomy`、`truth`、`preparation`、`sacrifice` 五个隐藏语义轴；同时保留有序语义选择历史，使后续反向行为不会被早期封顶数值抹去。玩家不会直接操作或看见这些数据，而是通过叙事选择间接改变状态，并从人物动作、物件变化和延迟回收中感受影响。结局系统必须同时读取五轴与历史，才能让完整因果链而非最终五个整数决定结果。具体结局解析、回退边界、状态信封与反证生命周期分别遵循 ADR-0001、ADR-0002、ADR-0004、ADR-0005，本 GDD 只规定玩家可感知的行为规则和跨系统数据契约。

## Player Fantasy

玩家体验的不是管理五项属性，而是与一个会记住自己行为的故事共同生活。每次停下来观察、把选择权交还给绘梨衣、坦白风险、提前准备或愿意共同承担，都可能在当下只得到一个眼神、动作或物件变化；当这些细节在数小时后重新出现时，玩家应产生“原来那一刻一直有重量”的领悟。

系统刻意不提供即时正确答案或可优化的好感度条。玩家需要承受不确定感，并根据人物和情境作出自己愿意负责的选择。理想体验是：玩家在结局揭示后能够回想起完整因果链，理解结果来自连续行为，而非最后一道决定命运的选择题。

> `creative-director` 未参与本节——Solo 模式；生产前需独立复核。

## Detailed Design

### Core Rules

#### 五轴定义

| 轴 | 记录的行为证据 | 不代表 |
|---|---|---|
| `understanding` | 观察、复述、承认没有理解 | 猜中绘梨衣的想法 |
| `autonomy` | 询问、等待并接受她的选择 | 放任风险或不承担责任 |
| `truth` | 验证线索、分享风险与事实 | 无条件公开所有信息 |
| `preparation` | 建立路线、物资、联系人和备选方案 | 代替绘梨衣作决定 |
| `sacrifice` | 接受由自己承担的真实损失 | 口头承诺或英雄式自我感动 |

#### 状态规则

1. 新周目以五轴全 0、选择历史为空开始。
2. 每个 production player-facing narrative choice（包括 `semantic_major` 与 `narrative_only`）必须拥有稳定且唯一的语义 ID，并进入同一个有序选择历史。
3. 重大选择可以使零至两条轴分别增加 1；不使用负数，也不得一次增加 2。
4. 没有形成有效行为证据的选项可以不增加任何轴。
5. 每轴有效范围固定为 `0–3`；达到上限后不再增加。
6. schema、五轴和选择历史共同属于一个 rollback-owned `semantic_state` 状态信封；所有 player-facing narrative choices 都由 `SYS-STATE` 通过 `apply_choice` 写入，轴变化与选择 ID 必须通过一次替换提交，不能只完成其中一项。`narrative_only` 传入 empty `RunMap`，因此只追加历史且五轴不变。
7. 同一选择 ID 在同一状态历史中再次提交时不产生任何变化；测试必须把这种情况报告为内容错误。
8. 五轴和选择历史均属于单周目状态，必须随存档、读档和回退一起恢复；回退到任一 `narrative_only` 选择之前会移除其历史 ID，读档与重放不得产生重复提交。
9. 跨周目数据不得保存五轴数值；成就、回忆和结局解锁由其他系统负责。
10. 第七日只能读取脱离实时状态的完整结局快照；快照必须包含 schema、五轴和有序语义历史。结局解析从历史与冻结目录派生未解决反证 token、completed events、resource possession、路线资格、完整 clause trace 与路径级 cause records，并返回 immutable `ending_resolution_record`；不得读取或修改实时状态。
11. 玩家界面不得显示数值、进度、增减提示或隐藏轴名称。
12. 结局及愿望手册可以引用具体选择和回收事件解释因果，但不能公开内部分数。
13. 五轴只证明正向证据曾经发生，不单独证明路线关键反向行为已经得到修复。`SYS-ENDING` 必须结合有序历史派生未解决反证 token 集合。
14. 任何生成或修复反证 token 的行为都必须表现为普通重大选择并进入历史；不得在五轴系统内静默减分、隐藏改旗标或使用重复正向行为覆盖既存 token。
15. 本系统不建立第二套正向资格清单：不存在 `grant` 操作。正向结局需求只能由五轴，以及从 ordered `choice_history` 与冻结的 choice-to-event/resource 投影目录纯重建的正式路线资格表达；resolver 不得读取其他 live event/resource state。不得保存匿名 `qualified_*` 布尔值、独立正向 flag 集或与五轴一一对应的资格条目。路线资格只能表达路线成员关系、互斥承诺或具体资源持有，不能代替五轴为 `rain_stops` 提供正向证据。反证 ledger 只记录少量、严重、可指认的支柱违背。
16. `rain_stops` 的正向判定恰为五轴全部 exact int `3` 且 history fold 后 unresolved token 集合为空；它不得引用 route qualification、独立 event/resource 条件、persistent 解锁或外部 live state 作为附加正向门槛。

#### 公共写入契约

`SYS-STATE` 的唯一公共写入口接收 `choice_id` 与 `axis_deltas`，并返回明确状态；`SYS-CHOICE`/`SYS-NARRATIVE` 不得直接修改状态信封、五轴或选择历史。每个 player-facing narrative choice 在玩家确认该选项后、任何即时 reaction/payoff 逻辑之前调用一次 `apply_choice`；`narrative_only` 必须传入 empty `RunMap`，成功时返回 `APPLIED`、五轴不变并原子追加 ID。Canonical `prehistory_id` 使用本次提交前的 history，后续 history guard 使用提交后的 membership。首个公开版本使用 `STATE_SCHEMA_VERSION = 2`，并以独立 `STATE_SCHEMA_SENTINEL = "semantic_state:v2"` 区分显式初始化的新周目与被 `default` 补值的旧存档。

| 字段 | 合法形式 | 非法形式 |
|---|---|---|
| `choice_id` | 精确类型为 string；长度 `1–64`；匹配 `^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$`；在全部叙事内容中全局唯一 | bool、数字、空串、大写、空格、连字符、只有一个不含下划线的词、超过 64 字符 |
| `axis_deltas` | exact `RunMap`；稀疏键集只能来自五条合法轴；empty `RunMap` 合法；键为 exact string；出现的每个值为 exact int 且等于 `1` | 任意其他 mapping/list、null、未知轴、显式 `0`、bool、负数、小数、大于 1 的整数 |
| `semantic_state` | exact `RunMap`；恰好含 `schema_version`、`axes`、`choice_history` 三键 | 任意其他 mapping、缺键、多键、非 `RunMap` |
| `axes` | exact `RunMap`；恰好包含五个合法键；键为 exact string；每个值为 exact int，范围 `0–3` | 任意其他 mapping、缺键、多键、bool、非整数、越界值 |
| `choice_history` | exact `RunList`；每项均为 exact string 且符合合法 `choice_id`；内部不得重复 | built-in list、tuple、string、mapping、无序集合、非法 ID、重复 ID |
| schema version | exact int `STATE_SCHEMA_VERSION = 2` | bool、非整数、缺失或不受支持的版本 |
| lifecycle sentinel | 活动周目必须为 exact string `"semantic_state:v2"`；只由新游戏初始化写入 | `None`、其他字符串、bool、缺失或由加载流程猜测补写 |

`RunMap` 与 `RunList` 是本 GDD 的具体运行时类型别名：分别指 Ren’Py 8.5.3 在 `.rpy` Python 中由 `{}` 和 `[]` 产生的 rollback-transformed dict/list equivalent。实现以同一 `.rpy` 上下文中的 `type({})` 与 `type([])` 做 exact-type 判定，不直接依赖引擎内部类路径；任意 `collections.abc.Mapping`、Sequence 或 imported CPython built-in 容器都不属于 live-state 合法类型。此约束来自 Ren’Py 8.5.3 本地引擎文档 `save_load_rollback.html` 的 Revertable Objects 规则。

省略某条轴即表示该轴本次增量为 0；不得用显式 `0` 表达省略。empty `RunMap` 用于记录有叙事意义、但不形成正向五轴证据的重大选择，包括路线关键反向行为与后续修复行为。

#### Deterministic Validation Precedence

错误类型和首个失败阶段都是接口的一部分。除 `after_load` 的兼容性分类外，公共 validator 使用有限的 **schema-known 两遍式遍历**：先检查规范声明的容器、键和值槽位的 exact types，再检查 value/shape。Validator 不做通用递归、不跟随任意对象引用，也绝不通过 `__getitem__`、迭代、表示、比较、哈希、真值判断或其他协议访问/求值未知 key 对应的 value；未知 key 的存在统一在 value/shape sweep 以 `ValueError` 报告。因此，自引用或任意深对象只能出现在未知 value 中时不会被访问，验证必然终止。

`apply_choice` 的固定顺序如下，并在首个失败处停止：

1. **Global type sweep**：按 `state_schema_sentinel`、`semantic_state` root、全部 present root **key 本身**、present known `schema_version` value、present known `axes` container、全部 present axes key 本身、五轴固定顺序中的 present known value、present known `choice_history` container、history index 顺序中的 item、`choice_id`、`axis_deltas` container、全部 present delta key 本身、五轴固定顺序中的 present known delta value 扫描。缺失 known field 跳过；unknown key 的 value 永远不访问。遇到 expected container 自身类型错误时不向下遍历。此阶段覆盖 state 与整个 payload 的全部 schema-known type slots，任何 value/shape 检查都不得提前运行。
2. **State value/shape**：依次验证 sentinel 恰为 `"semantic_state:v2"`、root key set、schema value、axes key set与五轴固定顺序范围、history ID 格式与首次重复位置。
3. **Choice ID value**：验证 `choice_id` 长度、格式与全局稳定 ID 约束。若非法，在读取任何 delta known value 以外的 delta value/shape/count 规则之前抛出 `ValueError`。
4. **Delta value/shape/count**：执行与公共 `validate_axis_deltas(axis_deltas) -> int` 相同的纯 oracle，依次验证 delta key set、五轴固定顺序中的严格值，并返回原始 `affected_axis_count`；结果 `0–2` 合法，`3–5` 抛出 `ValueError`。
5. 检查提交 ID 是否已在合法 history 中：若存在，返回 `DUPLICATE_NOOP`，状态保持深值等价；静态内容验证器同时把重复定义报告为失败。
6. 只在局部变量中构造完整候选 `semantic_state`，包括复制后的 axes 与 replacement history。
7. 以一次 `semantic_state = candidate_state` 替换提交，随后返回稳定字符串常量 `APPLIED`。

Global type sweep 覆盖 state 与 payload 的全部 schema-known 槽位后，才开始任何 value/shape 检查；通过后固定采用 **state value/shape → choice ID value → delta value/shape/count**。这给出唯一复合错误 oracle：

- state 存在 type defect：按上述固定槽位顺序先报该 `TypeError`；
- state 只有 value/shape defect、payload 存在 type defect：先报 payload `TypeError`；
- state 与 payload 都只有 value/shape defect：按 state sentinel/root/schema/axes/history，再 `choice_id`，最后 deltas 的顺序报告首个 `ValueError`；因此非法 `choice_id` + delta value/shape/count defect 必须先返回 choice-ID `ValueError`。

`current_ending_snapshot` 必须执行同一 active sentinel + state 两遍式前缀，但没有 payload 阶段。`validate_axis_deltas` 是唯一不读取 lifecycle sentinel 的公共 helper，只遍历 deltas schema-known key/value 槽位。实现必须让 `apply_choice` 与该公共 helper 复用同一组无副作用 type/value/count primitives：公共 helper 依次执行它们；`apply_choice` 在 global type sweep 中执行 delta type primitive，直到 choice-ID value 通过后才执行 delta value/count primitives，不得通过完整调用公共 helper而破坏全局顺序。`after_load` 是唯一例外：它先按 sentinel 将存档分类为 legacy/unsupported，再在 v2 sentinel 下运行相同 state validator；玩家只看到兼容性结果，开发日志记录确定性的首个底层错误。

纯 resolver 对 detached snapshot 采用相同的有限 schema-known 原则：检查 root 与所有 key 本身，但只读取 `schema_version`、`axes`、`choice_history` 三个 known root value；axes 只读取五个 known axis value；history 只做一层 exact-string item 扫描。Unknown value 不访问。运行时固定顺序为 snapshot built-in type sweep → snapshot value/shape → history catalog coverage + axis semantic replay → token fold legality → route-fact fold legality → qualification derivation → priority predicate evaluation → cause extraction from frozen evaluation → immutable resolution-record construction。第三阶段必须按冻结 choice axis projections 从零重放五轴并与 snapshot axes exact-equal，同时冻结 threshold contributors；不一致抛 `ValueError`。目录 schema、token 定义、caps/domain/mode、repair reference、projection schema/reference 与 predicate clause graph 已在 import/build-time 冻结前验证，resolver 不重复验证，也不存在正常运行时的 catalog-schema failure 阶段。任一较早运行时阶段失败时，后续阶段不得运行。

无论错误发生在哪一步，都不得替换 `semantic_state`、追加历史、生成部分快照、返回 fallback 结局或静默修复输入。

未知值零访问使用受控测试 instrumentation，而非只能证明“不递归”的 watchdog。Validator 对 known-value 读取必须经过私有 `_read_known_slot(container, key, read_trace=None)`；测试构建可注入只记录 `(container_path, key)` 的 `read_trace`，发行构建固定传 `None`，该 seam 不改变容器 exact-type 判定、不允许替换 validator 或跳过错误。静态检查与 branch coverage 必须证明所有 validator value fetch 都经过该 accessor。fixture 使用两个 unknown key：`extra_cycle` 的 value 指回 root，`extra_bomb` 的 value 是 `ProtocolBomb`，其迭代、表示、比较、哈希、真值判断和属性访问一律计数并抛错。验收要求 read trace 恰为规范列出的 known paths，两个 unknown key 的访问数与 bomb protocol-call count 均为 0。

**Machine example:** state root 含合法 known fields，另有 `extra_cycle` 指向 state 自身、`extra_bomb` 保存 `ProtocolBomb`，同时 payload 的 `choice_id` 为 bool。Global type sweep 不访问两个 unknown value，但会检查 payload known slot，因此结果固定为 `TypeError`。把 payload 修正后再次提交，type sweep 通过，state key set 在 value/shape sweep 以 `ValueError` 拒绝 extra keys。两次调用都必须在有限步内终止，trace 中不得出现 `extra_cycle` 或 `extra_bomb`。

```text
validation_fixture_id: example_unknown_cycle_payload_type
unknown_key: extra_cycle
unknown_value_reference: $state_root
protocol_bomb_key: extra_bomb
history_items: []
payload_choice_id_type: bool
payload_axis_deltas: {}
expected_error: TypeError
expected_unknown_getitem_reads: 0
expected_unknown_protocol_calls: 0
expected_trace_paths:
  - state.schema_version
  - state.axes
  - state.choice_history
  - state.axes.understanding
  - state.axes.autonomy
  - state.axes.truth
  - state.axes.preparation
  - state.axes.sacrifice
expected_termination: finite
```

`validate_axis_deltas` 是可直接测试的公共验证 helper，也是 `apply_choice` 计算轴数的唯一实现。它不读取或修改 live state；合法 payload 返回 exact int `0–2`，非法 payload 使用与写入入口相同的 `TypeError`/`ValueError` 分类。内容验证器必须在报告中输出该返回值，因此 `affected_axis_count` 不是不可观察的中间概念。

`default semantic_state = None` 且 `default state_schema_sentinel = None`。只有显式的新游戏初始化入口可以同时创建 schema 2 状态信封并写入 sentinel；普通 `default` 绝不构造合法活动状态。`after_load` 必须先分类 sentinel，再决定是否校验信封：

1. sentinel 为 `None`：返回 `LEGACY_INCOMPATIBLE`，不得初始化或补键。
2. sentinel 为任意非 `None` 且非 exact string `"semantic_state:v2"` 的值，包括未知 exact string 与 bool/int/custom object：返回 `UNSUPPORTED_VERSION`，不得先进入 state validator。
3. sentinel 为 `"semantic_state:v2"` 但状态类型或内容非法：返回 `CORRUPT_STATE`。
4. sentinel 与状态均合法：返回 `SUPPORTED`，游戏才可继续。

前三种结果必须跳转到阻断式 `incompatible_semantic_save` 流程，禁止返回原场景。该流程只允许“返回主菜单”或“开始新游戏”；开始新游戏必须通过显式初始化创建新状态，不修改合法 persistent 解锁。首个公开版本发布后，任何 schema 变化都必须先由独立迁移 ADR 定义逐版本迁移，不得在加载时猜测、钳制、静默补键或把失败存档当新周目。

#### 结局快照契约

`current_ending_snapshot()` 必须先以与写入入口相同的规则验证 active sentinel 与活动状态，再返回 detached plain dict：

```text
{
  "schema_version": 2,
  "axes": {五个轴的独立 dict 副本},
  "choice_history": [有序 ID 的独立 list 副本]
}
```

复制边界固定在 `.rpy` 与 imported pure Python 之间：

1. `.rpy` 侧完成 active sentinel 与 live `RunMap`/`RunList` 的全部验证。
2. `.rpy` 侧只提取 exact scalar：schema int、按五轴固定顺序的五个 int，以及由 history exact strings 构成的 detached built-in tuple。
3. imported private `_build_detached_ending_snapshot(schema_version, five_axis_values, history_ids)` 只接收这些 immutable built-ins，并在 imported module 内创建 exact CPython built-in dict/list graph。它不属于公共 API，只能由已完成 active validation 的 `.rpy` adapter 调用。它仍有统一的防误用契约：root/scalar/tuple/item exact type 错误抛 `TypeError`；type-clean 但 schema 非 2、轴 tuple 非恰好五项、轴越界、history ID 非法或重复抛 `ValueError`；失败时不返回部分快照。测试不得把直调成功当作绕过 adapter 的公共支持。
4. live `RunMap`、live `RunList` 或其可变嵌套对象绝不跨越 import boundary。

生产调用边界还必须由静态门槛强制，而不是只靠命名约定。生产 source manifest 覆盖完整 `game/**/*.rpy` 与 `game/**/*.py`，并把 `game/testcases.rpy`、`tests/**` 等显式标记为 `test_only` 后分开扫描；production source 对 test-only source 的直接或传递 import 同样属于失败。扫描器必须建立 builder symbol 的闭包，解析 direct name、import alias、module-attribute alias，以及 symbol 的赋值、传参、返回、closure 捕获、容器存储和 wrapper 导出；`getattr`、动态 import、字符串查找、反射、计算属性或任何无法静态解析的引用形式一律使构建失败。生产 allowlist 恰为 `game/10_state.rpy::current_ending_snapshot` 中 active validation success block 的一处直接调用，且 CFG 必须证明 active sentinel/state validation 在所有到达该 callsite 的路径上支配该调用。chapter、screen/UI、achievement、ending orchestrator、其他 adapter、符号逃逸或 test-only 依赖泄漏均使构建失败。测试 fixture 可以直调私有 builder，但不进入生产 allowlist，也不能向生产模块导出或间接传递 builder/wrapper。

不得先规范化再验证；非法活动状态必须按同一 `TypeError` / `ValueError` 分类失败。消费方可修改返回副本，但不得影响活动状态或后续快照。

> Specialist agents not consulted — Solo mode. Review manually before production.

### States and Transitions

| 当前状态 | 触发 | 下一状态 | 精确结果 |
|---|---|---|---|
| 无活动周目 | 开始新游戏 | Active | 显式创建 schema 2 `semantic_state` 并写入 sentinel；五轴全 0，选择历史为空 |
| Active | 首次提交合法选择 ID | Active | 原子记录 ID，并按规则增加最多两条轴；返回 `APPLIED` |
| Active | 再次提交已存在的 ID | Active | 返回 `DUPLICATE_NOOP`；状态保持深值等价，并由静态验证报告内容错误 |
| Active | 合法增量使轴超过 3 | Active | 该轴保持 3 |
| Active | 玩家回退 | Active | 引擎以同一时间点的五轴和完整历史恢复活动状态 |
| 任意 | 玩家读取存档 | Active/Blocked | `after_load` 先分类 sentinel；只有 `SUPPORTED` 进入 Active，其余结果跳转阻断式失败流程 |
| Active | 第七日请求结局 | Active | 校验活动状态并生成包含 schema、axes、history 的 detached plain dict；快照是数据产物，不是运行状态 |
| Active | 第七日编排器收到唯一合法 `ending_id` 并进入对应 ending entry label | Ended | `SYS-ENDING` 独占触发和拥有该叙事流程转换；不回写 `semantic_state`，不得由选择、成就或章节脚本直接标记 Ended |
| Ended | 开始新周目 | Active | 创建全新局内状态，不继承旧轴值 |

### Interactions with Other Systems

| 系统 | 方向 | 接口与所有权 |
|---|---|---|
| `SYS-CHOICE` | 输入 | 提供符合公共写入契约的 `choice_id` 与稀疏 `axis_deltas`；五轴系统负责验证、原子应用并返回 `APPLIED` 或 `DUPLICATE_NOOP` |
| `SYS-ENDING` | 输出 | 接收 schema、五轴和有序历史组成的独立结局快照；从 frozen catalogs 重放 axes 并验证一致性，再派生未解决 token、event/resource facts、路线资格、完整 clause trace 与实际路径 causes；返回 immutable resolution record，独占 detectable `ending_flow:v1` 的 `Active → Ended` ending-entry 触发，不得访问或修改任何实时状态 |
| `SYS-NARRATIVE` | 双向 | 章节定义选择语义，并读取选择历史生成即时反应和延迟回收 |
| `SYS-SAVE` | 双向 | Ren’Py 保存与恢复 sentinel 及局内状态；`after_load` 必须执行支持性分类和安全失败流程 |
| `SYS-PERSIST` | 边界 | 不接收五轴值；只保存已完成叙事产生的跨周目解锁 |
| `SYS-ACHIEVE` | 下游可见性边界，Provisional | `SYS-ACHIEVE` 独占成就条件与目录 owner；不得覆盖五个 domain、映射轴名/阈值或形成“正确选择”代理清单 |
| `SYS-JOURNAL` | 只读输出 | 可读取具体事件摘要，不得读取或显示轴值 |
| `SYS-ACCESS` | 呈现/输入边界，Designed（完整复审待完成） | accessibility-equivalent input 必须映射到同一 choice record/ID，不能生成未被 choice coverage scanner 发现的替代叙事分支；不读取隐藏轴 |
| `SYS-TENSION` | 输入，暂定 | 超时若产生叙事结果，必须转换为稳定选择 ID；不得直接修改轴值 |
| `SYS-TEST` | 观察 | 验证范围、原子性、重复 ID、回退、存读档与快照纯度 |

`SYS-CHOICE`、`SYS-NARRATIVE` 与 `SYS-TENSION` 已有各自设计合同；`SYS-ACCESS` 已达 Designed（完整复审待完成）。SYS-TENSION 按 systems-index 延期至 post-MVP，各接口按表内状态与下游证据门槛执行。

### Path-Level Reachability Contract

全局机会总数只能用于发现内容分布异常，不能作为结局可达性的证明。`SYS-NARRATIVE` 与 `SYS-ENDING` 获批前，必须共同提供以下路径级证据：

1. 六个正式结局各有至少一条首周目标准见证路径：`rain_stops`、`her_own_name`、`see_the_sea`、`one_person_train`、`golden_cage`、`unsent_postcard`。
2. 每条见证路径必须从全新周目的合法初始状态开始，只使用玩家可见的正式选择，不依赖开发标记、控制台写值、旧存档、跨周目解锁、随机结果或同时选择互斥分支。
3. 路径记录必须按章节列出有序 `choice_id`、每次合法 `axis_deltas`、章末累计五轴、每次产生或定向修复的反证 token、最终未解决 token 集合，以及唯一结局。
4. `rain_stops` 的标准见证路径必须以五轴全部为 3 且未解决反证 token 集合为空结束。每条轴在真结局补救路径上必须至少有四次两两独立的得分机会；对五条轴分别提供一条补救见证，跳过该轴最早一次得分后仍能用后三次达到 3，并保持真结局可达。
5. 其余五条标准见证路径必须命中各自结局且不命中任何更高优先级结局；具体阈值与优先级判定由 `SYS-ENDING` 独占定义。
6. 自动枚举必须拒绝不可达节点、悬空跳转、互斥选择并存、单章同路径同轴多次得分，以及任何无法产生唯一结局的合法终态。
7. 六条标准见证都必须登记一个 `ending_causality_record`：`causality_record_id`、`ending_id`、`witness_path_id`、非空 `matched_cause_ids`、`higher_priority_exclusions`、`terminal_outcome_signature`、`payoff_scene_id`、`payoff_id` 和 `player_facing_summary_id`。这些 ID 必须逐项对应 `resolve_ending_record` 生成的路径级 cause records，不能由作者从 clause template 中手填。Predicate graph、完整求值、实际来源选择、无 history cause 桶与 total-order key 遵循下述“Executable Ending Predicate and Cause Contract”。
8. `higher_priority_exclusions` 必须对该 ending 之前的每个更高优先级 ending ID 恰有一项非空 cause-ID list，证明为何本见证没有命中它；`rain_stops` 的该 mapping 合法为空。`payoff_scene_id` 必须在场景中实际回收 `matched_cause_ids` 和每项关键 exclusion，而不是数值化解释规则。
9. 六个 ending 的因果回收都属于硬门槛：好结局必须解释它为何不是更完整的上位结局，苦涩/悲剧结局必须回收决定性损失或未解决伤害，真结局必须回收完整成立的正向证据与承担。泛化成功/失败旁白不合格。
10. 六条 canonical record 只证明最低可达性，不代表同 ending 的其他因果链已覆盖。`SYS-ENDING` 与 `SYS-NARRATIVE` 必须把全部合法 terminal paths 按 `terminal_cause_equivalence_class` 分区；class identity 恰由 `ending_id`、完整规范化 `matched_cause_ids`、逐个高优先级 ending 的规范化 exclusion cause IDs、最终 unresolved token IDs 与 `terminal_outcome_signature` 组成。`terminal_outcome_signature` 恰含 `ending_selection_id`、排序后的 `character_fate_outcome_ids`、`cost_bearer_outcome_ids`、`tragedy_closure_outcome_ids`。任一字段不同即为新 class，不得因 ending ID 相同而合并；每个 class 必须关联至少一个 witness path、一个适用 payoff scene 与玩家可感知摘要。
11. 玩家演出使用单独的确定性 `display_cause_ids`，不反向影响 class identity 或 resolver。只允许 summary catalog 标为 presentation-safe 的 causes。五个非 fallback ending 先取首个 safe matched cause；`unsent_postcard` 的 constant match 保留为 audit-only，首卡按专用顺序从 concrete failure/unresolved causes 选择。再把其余 safe causes 稳定去重并按同一 total-order key 排序，取前两项补足，最终为 1–3 项。完整 matched/exclusion/outcome signature 只留在审计与测试层。
12. `terminal_cause_equivalence_class` 的内容预算按每个 ending 计算：目标 `1–6` 个 class；`7–12` 个触发 Producer/Creative Director 范围预警；超过 `12` 个使内容构建失败，必须削减上游分支组合或增加可参数化的 payoff 产能后再审。预算压力绝不能通过合并不同人物归宿、代价承担者、悲剧闭合、matched/exclusion 或 unresolved-token signature 来消除。

“标准见证路径”是最低可达性证据，不意味着游戏只有六条路线；实际所有可达路径仍必须由内容验证器覆盖。等价类枚举属于 `SYS-ENDING`/`SYS-NARRATIVE` 获批后的联合门槛，不倒灌为当前 `SYS-STATE` 独立批准证据。

#### Executable Ending Predicate and Cause Contract

每个 ending 恰有一个 root clause。冻结的 exact immutable `ending_predicate_clause_record` 恰含：`ending_id`、全局唯一 `clause_id`、exact `clause_order`、`clause_kind`、`operand_clause_ids`、`source_kind`、`source_reference_ids`、`comparator`、`expected_int`、`required_truth_value`、`match_cause_template_id`、`failure_cause_template_id`。

`required_truth_value` 对 group 与 atomic 一律固定为 exact bool `true`；反向要求只能通过 `absent` comparator 表达，禁止 `present + false`、`absent + false`、`always_true + false` 等双重否定。`clause_order` 为 exact int，单个 ending 内恰为连续且无重复的 `0..N-1`，root 固定为 0；operand 必须属于同一 ending，并按 child `clause_order` 严格递增。跨 ending operand、cycle、shared child、dangling operand、不可达 clause、重复/缺号 order 均在 predicate catalog freeze 前失败。

合法域是下表的穷尽集合；表外组合一律构建失败：

| Clause kind | Source kind | Comparator | Expected | Source refs | Match cause | Failure cause |
|---|---|---|---|---|---|---|
| `group_all` | `None` | `None` | `None` | `None` | 不直接生成 | 不直接生成 |
| `group_any` | `None` | `None` | `None` | `None` | 不直接生成 | 不直接生成 |
| `atomic` | `axis_value` | `at_least` | exact int `1–3` | 恰一个 axis ID | 实际增量 choices | `evidence_shortfall` |
| `atomic` | `history_choice` | `present` | `None` | 恰一个 choice ID | 该 choice | no-history `evidence_shortfall` |
| `atomic` | `history_choice` | `absent` | `None` | 恰一个 choice ID | no-history absence | 该 choice 的 `exclusion_evidence` |
| `atomic` | `unresolved_token` | `present` | `None` | 恰一个 token ID | 当前有效 revoke | repair/no-history shortfall |
| `atomic` | `unresolved_token` | `absent` | `None` | 恰一个 token ID | 最终 repair 或 no-history absence | 当前有效 revoke |
| `atomic` | `completed_event` | `present`/`absent` | `None` | 恰一个 event ID | 首个完成 choice / no-history absence | no-history shortfall / 首个完成 choice |
| `atomic` | `resource_possession` | `present`/`absent` | `None` | 恰一个 resource ID | 最后有效 acquire / 最后 consume 或 no-history absence | 最后 consume/no-history shortfall / 最后有效 acquire |
| `atomic` | `route_qualification` | `present`/`absent` | `None` | 恰一个 qualification ID | qualification trace 的满足/失败 contributors | 相反 contributor 集 |
| `atomic` | `constant` | `always_true` | `None` | empty tuple | 仅 fallback | 不存在 |

`axis_value at_least 0` 非法；`constant` 只允许作为 `unsent_postcard` 唯一 root。Group 的 `operand_clause_ids` 是非空 exact tuple；`group_all` 对全部 child satisfaction 求 `all`，`group_any` 对全部 child satisfaction 求 `any`，均先求值所有 child，禁止语言短路。对 true `group_all` 取全部 true children、true `group_any` 取全部 true children；对 false `group_all` 取全部 false children、false `group_any` 取全部 children，再递归得到唯一 contributing atomic set。

每个非 constant atomic 恰有两个已冻结 `ending_cause_template_record`；constant fallback 恰有一个 match template。Template 的 concrete identity 为 `ending_rules.EndingCauseTemplateRecord`，字段顺序恰为 `cause_template_id`、`ending_id_or_none`、`clause_id_or_none`、`token_id_or_none`、`polarity`、`cause_kind`、`source_kind`、`player_summary_id`。Clause template 要求 ending/clause 为 exact string、token 为 `None`，唯一键为 `(ending_id, clause_id, polarity)`；audit template 要求 ending/clause 为 `None`、token 为 exact string、polarity 为 `audit`，唯一键为 `(token_id, audit)`。每个 revoke token 恰有一个 `unresolved_counterevidence` audit template。运行时对每个最终 unresolved token 与实际 selected ending 生成一项 cause：runtime `ending_id` 固定为 selected ending、`clause_id` 为 `None`、`source_reference_ids[0]` 固定为该 template 的 token ID。因此一个 token template 可在六个 selected ending 中生成六个不同 lineage，多个 token 也不会共享 template identity。

Runtime `ending_rules.EndingCauseRecord` 的字段顺序恰为：`cause_id`、`cause_kind`、`cause_template_id`、`ending_id`、`clause_id`、`polarity`、`source_kind`、`source_reference_ids`、`observed_value`、`required_value`、`anchor_bucket`、`history_anchor_start`、`history_anchor_end`。字符串字段为 exact string，只有 audit 的 `clause_id` 为 exact `None`；references 为 exact tuple of exact strings；value 只允许 exact `None`/bool/int/str 或其 exact tuple；anchor 只允许 nonnegative exact int。设 `h(x)` 为 choice 在 ordered history 中的唯一零基 index，`n = len(history)`。所有 payload 字段按下表唯一填充，表外行为构建失败：

| Source / comparator / actual result | `source_reference_ids` | `observed_value` / `required_value` | Anchor |
|---|---|---|---|
| `axis_value at_least r`, `A >= r` | `E_r`；按 history 顺序最早的、实际使该轴从 `<r` 增到 `<=r` 的恰 `r` 个 choice IDs；轴已封顶后的证据不进入 | `A` / `r` | bucket 0；`min/max h(E_r)` |
| `axis_value at_least r`, `A < r` | `E_A`；使用全部且仅实际产生现有 `A` 次增量的 choices | `A` / `r` | `A>0` 为 bucket 0 与 `min/max h(E_A)`；`A=0` 为 empty tuple、bucket 1、`n/n` |
| 任意 `present`/`absent` atom | 下述 source-specific identity 加决定当前事实的 choice contributors | 当前 exact bool / `present→True`、`absent→False` | 有 contributor 为 bucket 0 与最小/最大 history index；无 contributor为 bucket 1、`n/n` |
| `history_choice` | `(choice_id,)`；present 时该 ID 自身也是唯一 contributor | bool / comparator target bool | present 为 bucket 0、`h(choice)/h(choice)`；absent 为 bucket 1、`n/n` |
| `unresolved_token` | 从 `(token_id, revoke_choice_id)` 开始；若已 repair，再追加 `repair_choice_id`；从未产生则仅 `(token_id,)` | bool / comparator target bool | unresolved 以 revoke 定位；repaired 取 revoke/repair min/max；从未产生为 bucket 1 |
| `completed_event` | `(event_id, completing_choice_id)`；未完成则仅 `(event_id,)` | bool / comparator target bool | 完成为 completing choice；未完成为 bucket 1 |
| `resource_possession` | `(resource_id, last_effect_choice_id)`；从未 acquire/consume 则仅 `(resource_id,)` | bool / comparator target bool | 有 effect 为最后有效 acquire/consume 的同一 index；无 effect 为 bucket 1 |
| `route_qualification` | `(qualification_id, *encoded_source_facts)`；每个 fact 编码 `source_kind/source_id/truth/contributor_choice_ids`。`all` true 取全部 facts，`all` false 取全部 false facts，`any` true 取全部 true facts，`any` false 取全部 facts；按 `(source_kind_rank, source_id, contributor history order)` 规范排序 | bool / comparator target bool | 有 contributor 为 bucket 0 与 min/max；无 contributor为 bucket 1 |
| `constant always_true` | empty tuple | `True` / `True` | bucket 2、`n/n` |
| unresolved audit | `(token_id, revoke_choice_id)` | `True` / `True` | bucket 0、revoke index/revoke index |

Atomic 的 comparator truth 决定 `polarity`：满足为 `match`，不满足为 `failure`；audit 固定 `audit`。Match 固定生成 `matched_evidence`，constant match 生成 `fallback`；failure 在 `absent` 但对象 present 时生成 `exclusion_evidence`，其余为 `evidence_shortfall`。Axis source identity 由 `clause_id` 与 template 固定，故 golden vector 继续只保存 contributor choices；其余非轴 source 按矩阵显式保存 semantic source ID。Postcard constant match 保留其既有 payload/golden vector，但 `player_summary_id` 标为 audit-only，不得成为 `display_cause_ids[0]`。

#### Canonical Cause Identity Encoding

Template ID 与 runtime cause ID 是不同字段：`cause_unsent_postcard_fallback` 只允许是 `cause_template_id`；其 runtime `cause_id` 必须匹配 `^cause_[0-9a-f]{64}$`。Hash payload 是下列 exact tuple，字段顺序不可改变：

`("cause_payload_v1", ending_id, clause_id_or_none, polarity, cause_kind, cause_template_id, source_kind, source_reference_ids, observed_value, required_value)`

Canonical encoder 只接受 exact `None`、bool、int、str、tuple，使用以下 byte grammar；长度均是 UTF-8 **byte count**，不是 Unicode code points：

```text
None       = ASCII "n;"
False      = ASCII "b:0;"
True       = ASCII "b:1;"
int        = ASCII "i:" + canonical_base10 + ";"
str        = ASCII "s:" + utf8_byte_count + ":" + utf8_bytes + ";"
tuple      = ASCII "t:" + element_count + ":[" + encode(each element in order) + "];"
```

Exact bool 必须在 int 之前分类；canonical int 的 0 只写 `0`，负数只允许单一前导 `-`，禁止 `+` 和前导零。`source_reference_ids` 必须先按该 cause 的规范 source order 形成 exact tuple。对整个 encoded tuple 求 `_hashlib.openssl_sha256`，使用 `_hashlib.HASH.hexdigest()` 的完整 lowercase 64 hex，并加 `cause_` 前缀。不同 payload 得到相同 digest、同一 digest 对应不同 payload、非规范 bytes 或截断 hash 均构建失败。

Collision proof 不依赖构造真实 SHA-256 collision，也不允许替换 production hash leaf。构建工具在 production digest 计算后调用纯 `tools.validate_cause_digest_bijection(pairs)`；`pairs` 是 exact tuple of exact `(payload_bytes, digest_hex)` tuples。该函数只验证双射：同 payload 必须只有同 digest，同 digest 必须只有同 payload。`tests/**` 提供 synthetic unequal payloads + equal 64-hex digest 的负例，必须失败；该 checker 与 test fixture 不被 `ending_rules.py` import，不属于 resolver production manifest，也不向 resolver 暴露 digest seam。

Golden vectors：

| Vector | Canonical bytes (hex) | SHA-256 |
|---|---|---|
| `fallback_v1` | `743a31303a5b733a31363a63617573655f7061796c6f61645f76313b733a31353a756e73656e745f706f7374636172643b733a32303a756e73656e745f706f7374636172645f726f6f743b733a353a6d617463683b733a383a66616c6c6261636b3b733a33303a63617573655f756e73656e745f706f7374636172645f66616c6c6261636b3b733a383a636f6e7374616e743b743a303a5b5d3b623a313b623a313b5d3b` | `f57b3ae4a102befa05f8e5a51b1be688338ad1daf3708963d676cb12c7ecac8b` |
| `axis_match_v1` | `743a31303a5b733a31363a63617573655f7061796c6f61645f76313b733a31303a7261696e5f73746f70733b733a34303a7261696e5f73746f70735f617869735f756e6465727374616e64696e675f61745f6c656173745f333b733a353a6d617463683b733a31363a6d6174636865645f65766964656e63653b733a35323a63617573655f7261696e5f73746f70735f617869735f756e6465727374616e64696e675f61745f6c656173745f335f6d617463683b733a31303a617869735f76616c75653b743a333a5b733a31383a70726f6c6f6775655f726561645f6e6f74653b733a32323a646179315f726561645f666f6f645f676573747572653b733a31373a646179325f6163636570745f616c6961733b5d3b693a333b693a333b5d3b` | `8d6112f9e5f8292f03db2560738b124cbe429e2d1ea40095e979bfd29ebaee0c` |

所有 matched/exclusion/unresolved/display cause records 使用 total-order key `(anchor_bucket, history_anchor_start, history_anchor_end, cause_kind_rank, source_kind_rank, cause_id)`；`cause_kind_rank` 为 matched `0`、unresolved `1`、exclusion `2`、shortfall `3`、fallback `4`，`source_kind_rank` 按 truth table 顺序为 `0–6`。

#### Structured Resolution Schema and Single-pass Flow

Runtime record identity 与字段顺序只有下表一种；module、qualname、field order 任一不同都不是兼容 record。全部 class 在 `ending_rules.py` module import 时创建一次并冻结，禁止同名替代 class：

| Module + qualname | Exact field order |
|---|---|
| `ending_rules.EndingCauseRecord` | `cause_id`, `cause_kind`, `cause_template_id`, `ending_id`, `clause_id`, `polarity`, `source_kind`, `source_reference_ids`, `observed_value`, `required_value`, `anchor_bucket`, `history_anchor_start`, `history_anchor_end` |
| `ending_rules.ClauseEvaluationTraceEntry` | `ending_id`, `clause_id`, `clause_order`, `clause_kind`, `comparator_result`, `satisfaction_result`, `contributing_clause_ids`, `source_reference_ids`, `observed_value`, `required_value`, `anchor_bucket`, `history_anchor_start`, `history_anchor_end`, `cause_template_id_or_none`, `polarity_or_none`, `cause_kind_or_none`, `source_kind_or_none` |
| `ending_rules.HigherPriorityExclusionEntry` | `ending_id`, `causes` |
| `ending_rules.EndingResolutionRecord` | `ending_id`, `unresolved_token_ids`, `unresolved_token_causes`, `completed_event_ids`, `resource_possession_ids`, `qualification_ids`, `clause_evaluation_trace`, `matched_causes`, `higher_priority_exclusions`, `display_cause_ids` |

`ClauseEvaluationTraceEntry` 的前七项沿用原义。对 atomic，`source_reference_ids` 至 `history_anchor_end` 六项必须逐字段复制上文 payload-population matrix，末四项必须在 evaluation 时从该 atomic 的 match/failure template 与 cause semantics 冻结 exact `cause_template_id`、`polarity`、`cause_kind`、`source_kind`；对 group，六项固定为 empty tuple、`None`、`None`、`None`、`None`、`None`，末四项也全部为 exact `None`。Trace 按 ending priority 后 clause order 排序，只包含从最高优先级到 selected ending（含）的全部 clause，每项一次。Qualification derivation 先冻结每个 qualification outcome 的 contributor choices 与 anchors；atomic evaluator 只能复制该 frozen fact，不能重新遍历目录。

Token fold 同时冻结 exact tuple of `ending_rules.UnresolvedAuditFact`，其 module/qualname/field order 恰为 `cause_template_id`, `token_id`, `polarity`, `cause_kind`, `source_kind`, `source_reference_ids`, `observed_value`, `required_value`, `anchor_bucket`, `history_anchor_start`, `history_anchor_end`；其中三项 exact 固定值分别为 `audit`、`unresolved_counterevidence`、`unresolved_token`。Priority stage 最终输出一个 exact `ending_rules.FrozenResolutionEvaluation`，字段恰为 `selected_ending_id`, `clause_evaluation_trace`, `unresolved_audit_facts`。Cause extraction 的唯一输入是该 frozen artifact；它不得读取 snapshot、history、catalog、qualification index 或再次调用 fold/evaluator。这样 clause causes 与 audit causes 已冻结 template/polarity/kind/source identity，可独立构造全部 causes 并保持单遍。

`HigherPriorityExclusionEntry` 的 `ending_id` 为 exact string，`causes` 为 nonempty exact tuple of `EndingCauseRecord` 并按 total-order；entries 按 ending priority。`EndingResolutionRecord` 完全采用上表唯一顺序：`ending_id` 为 exact string；ID fields 为 exact tuple of exact strings；cause fields、trace、exclusions 分别为对应 exact record tuples。嵌套只允许 exact tuple 与上表 exact immutable records，不允许 list/dict/set/custom subclass。Unresolved IDs/causes 按 revoke history index 后 stable ID；event/resource/qualification IDs 按 UTF-8 bytes；causes 按 total-order。每个 unresolved ID 恰有一个 audit cause。

`display_cause_ids` 是 1–3 个 exact string 的 tuple。非 postcard 先取首个 presentation-safe matched cause；postcard 按 `understanding → truth → preparation → unresolved consequence → latest failed commitment` 从 presentation-safe concrete failure/unresolved causes 取首项。再合并其余 safe matched、unresolved 和 exclusions，按 `cause_id` 稳定去重并按 total-order 取前两项。每个 display ID 必须在 resolution record 的三个 cause collections 并集中恰解析一次。

单次运行阶段固定为：snapshot type sweep → snapshot value/shape → catalog coverage + axis semantic replay → token fold → route-fact fold → qualification derivation → **priority predicate evaluation** → cause extraction from frozen evaluation → record construction。Priority stage 按 ending priority 完整求值一棵 tree、冻结 artifact、检查 root；首个 true 后停止。Cause stage 只消费 artifact。任一失败后的 stage counts 为 0，每个已评估 clause count 恰为 1。

`resolve_ending_record(snapshot) -> EndingResolutionRecord` 是唯一 canonical pass。`resolve_ending(snapshot) -> str` 除唯一一次 canonical call 与随后一次 `.ending_id` descriptor read 外，不得**自行**直接或间接调用 validator、fold、qualification、predicate、cause 或 record helper；canonical call 内部的合法传递调用不受此禁令。两个入口共享同一 invalid/purity oracle。

可观测性由 production manifest 外的 test-only AST instrumentation build 提供，不在 production API 添加 counter/seam。工具验证 production source SHA-256 后，从同一 AST 生成只插入 observation callbacks 的隔离副本；production 不 import `tests/**`，隔离副本也不得打包。它返回 exact `tests.resolver_observation.ResolverObservationRecord`，字段顺序恰为 `entrypoint_id`, `result_or_exception_signature`, `stage_entry_counts`, `clause_evaluation_counts`, `canonical_call_count`, `wrapper_field_read_names`, `production_source_sha256`。`stage_entry_counts` 是按九阶段固定顺序的 `(stage_id, exact_int_count)` tuple；clause counts 按 ending priority/clause order；wrapper reads 必须恰为 `("ending_id",)`。正常 wrapper 的 canonical count 为 1；任何失败后阶段 count 为 0。静态报告另外证明 instrumented 与 production CFG/expressions 相同，唯一差异是 callback nodes。

所有 `outcome_reference_id` 必须解析到一个 exact `outcome_reference_record`：`outcome_reference_id`、`outcome_kind`、`subject_entity_id`、`outcome_state_id`、非空 `source_event_ids` 与 `owner_system: SYS-NARRATIVE`。`outcome_kind` 只能为 `ending_selection`、`character_fate`、`cost_bearer`、`tragedy_closure`。ID 全局唯一；`subject_entity_id`、`outcome_state_id` 与全部 source event 必须存在。agency witness、terminal outcome signature 与 payoff 引用未知或错误 kind 的 outcome 均使内容构建失败。

“两两独立得分机会”具有机器定义。对同一轴的机会 `O1...On`，必须同时满足：

- 每个机会来自不同稳定 node ID 和不同 `choice_id`；
- 选择 `Oi` 的零增量替代项后，所有较晚 `Oj` 仍可达；
- 替换 `Oi` 不改变较晚机会的 `axis_deltas`，不要求同时选择互斥节点，也不自动产生或修复反证 token；
- 图验证器能输出原路径与替换路径，并证明两者除 `Oi` 的局部选择及声明的叙事回收外保持同一后续机会集合。

仅仅位于不同章节、使用不同文本或拥有不同 reaction/payoff ID，不足以证明独立。

### Anti-Hidden-Score Content Contract

#### Player-facing Choice Coverage Universe

反馈硬规则覆盖发行构建中**全部 player-facing narrative choices**，不能靠把选项改名为“非重大”绕过。Production source scanner 枚举所有 `menu` options、screen `Button`/`hotspot` 导向叙事 label 的 actions、timed choice outcomes，以及由 accessibility-equivalent input 触发的同一叙事分支。每一项必须恰归属：

1. exact `player_facing_choice_record`：`choice_id`、`choice_node_id`、`choice_class`（`semantic_major`/`narrative_only`）、`immediate_reaction_id`、nonempty `payoff_ids`、`owner_system: SYS-NARRATIVE`；或
2. exact `non_narrative_interaction_allowlist_record`：`interaction_id`、`source_path`、`source_line`、`interaction_kind`、`rationale`、`owner_system`。`interaction_kind` 只允许主菜单/设置/存读档/accessibility/退出/开发工具导航，禁止章节内对话、行动、沉默、超时或路线选择。

每个 `semantic_major` 必须且只能链接下述 major-choice metadata；`narrative_only` 不写五轴/token，但仍必须有稳定 choice ID、即时 reaction 与后续 payoff，并在玩家确认后、reaction 前通过 `SYS-STATE.apply_choice(choice_id, empty RunMap)` 提交到同一 `semantic_state.choice_history`。这一次提交与重大选择共享 save/load/rollback envelope：回退至选择前移除 ID，读档恢复保存点 membership，重放只提交一次。Scanner 报告 source manifest、全部发现项、分类与 allowlist；未分类、重复分类、章节叙事误列 allowlist、动态字符串 option、无法解析 action 或 production→test-only choice 均构建失败。

每个重大选择节点必须使用机器可读内容记录。缺少任何 required 字段都属于静态验证失败：

| 字段 | 类型与规则 | 用途 |
|---|---|---|
| `choice_id` | 合法且全局唯一的 exact string | 运行时历史与跨文档追踪 |
| `axis_deltas` | 机器可读 mapping；内容编译后必须产生符合公共写入契约的 exact `RunMap` | 正向证据 |
| `next_node_ids` | 非空 exact list；每项为存在的稳定节点 ID | 枚举该选项保留的后续路线 |
| `risk_vector` | exact dict，恰含 `physical`、`exposure`、`time`；值为 exact int `0–3` | 分量比较即时风险 |
| `resource_costs` | exact dict；稳定资源 ID 映射到非负 exact int | 分量比较可消耗资源 |
| `character_costs` | exact dict，恰含 `erii_burden`、`player_burden`、`ally_burden`、`autonomy_restriction`；值为 exact int `0–3` | 分量比较人物代价 |
| `unique_value_tags` | exact list；只引用注册表中 `kind: semantic_value` 的稳定 ID，不得临时从 reaction/payoff ID 生成 | 证明零增量或较高成本选项的已审核语义价值 |
| `counterevidence_effect` | `null`，或一个 exact record；`kind` 只能为 `revoke`/`repair`，且遵守下述 token schema | 让 `SYS-ENDING` 从历史派生未解决反证 token |
| `immediate_reaction_id` | 已登记且唯一的 exact string | 即时反馈追踪 |
| `payoff_ids` | 非空 exact list；若回收即为章节终止，登记唯一 `chapter_terminal_*` ID | 延迟或终止回收追踪 |

即时反应可以是绘梨衣的视线、动作、停顿、物件操作或环境变化；遵守角色设定，不要求她通过完整口语表达。内容构建会把每个 `choice_id`（包括 `counterevidence_effect: null`）编译进 `SYS-ENDING` 可读取的不可变语义目录；运行时历史仍只保存稳定 ID。

#### Later Payoff Witness Contract

非空 IDs 只是声明。对 player-facing choice `c`，令 `h` 为到达 choice node 前的完整 ordered choice history，`s` 为选择 `c` 后到 ending entry 的一个完整合法 choice-ID suffix。Canonical IDs 使用上文 byte encoder：

- `prehistory_id = "prehistory_" + SHA256(encode(("prehistory_v1", choice_node_id, h)))`
- `continuation_id = "continuation_" + SHA256(encode(("continuation_v1", choice_id, prehistory_id, s)))`

因此相同节点但不同历史、相同历史但不同 terminal suffix 不会合并。图验证器必须完整枚举每个 reachable `(c, h, s)`；**每一个**组合都必须至少有一项适用 payoff witness，不是“每个 h 存在一条好 continuation”。每个声明 `payoff_id` 还必须至少在一个合法组合上被使用，但不要求每个 payoff 适用于所有 suffix。

Exact `choice_payoff_witness_record` 字段顺序为：`witness_id`、`choice_id`、`prehistory_id`、`continuation_id`、`continuation_choice_ids`、`payoff_id`、`payoff_node_id`、`payoff_event_id`、`causal_binding_id`、`timing_kind`、`owner_system`。`continuation_choice_ids` 保存从 choice 后到 ending 的完整 `s`；payoff node 必须在 `s` 对应 CFG 上严格晚于 choice 且不晚于 ending entry。`chapter_terminal` 必须在选择后、离章前实际发生。

每个 choice 另有 exact `choice_reaction_binding_record`：`reaction_binding_id`、`choice_id`、`choice_node_id`、`reaction_id`、`reaction_event_id`、`reaction_node_id`、`owner_system`。CFG 必须证明 reaction event 在 choice commit 后执行，并在任何下一 menu、jump/call、return、chapter exit 或 ending entry 前 postdominate 该 choice edge；`reaction_event_id` 的 metadata 必须反向引用同一 `choice_id`。这同时证明 reaction 已登记且在真实玩家路径即时执行。

每个 witness 的 `causal_binding_id` 必须解析到 exact `choice_payoff_binding_record`：`causal_binding_id`、`choice_id`、`payoff_id`、`payoff_event_id`、`proof_kind`、`guard_reference_id_or_none`、`counterfactual_witness_id_or_none`、`outcome_reference_ids`、`owner_system`。`proof_kind` 只能为：

- `history_guard`：payoff event 的 production CFG/AST 显式读取该 exact `choice_id` 的 history membership；false 分支不能发出同一 payoff event；
- `counterfactual_outcome`：登记成对合法路径，只替换该 choice 而保持对齐 continuation，可证明 payoff event 不发生或 registered `outcome_reference_ids` 深值不同。

Payoff event metadata 必须反向列出同一 `choice_id` 与 binding ID；一个通用 later event 若不读取/不受该 choice 控制则不合格。共享 event 可以绑定多个 choices，但必须有逐 choice guard 或逐 choice 不同的 registered outcome，不能让所有 choices 指向同一无关事件。任一 `(c,h,s)` 缺 witness、prehistory/continuation hash 不匹配、reaction 未 postdominate、payoff 不在真实路径、因果绑定单向/悬空、counterfactual 不改变结果、同节点/即时伪回收或错误 owner 均使构建失败。

#### Provisional Downstream Join Gate

Choice declaration、reaction binding、payoff binding、witness 与双向 event metadata 之间的 exact joins、cardinality 和 proof-kind nullability 由 `SYS-CHOICE` 与 `SYS-NARRATIVE` 共同拥有，当前保持 **provisional downstream gate**，不计入 `SYS-STATE` 批准。两系统在各自 GDD/stories/实现获批前必须冻结并验证：跨记录 ID 等值连接、每个 choice 的 reaction-binding 基数、witness/binding/event 的双向引用，以及 `history_guard`/`counterfactual_outcome` 两种 proof kind 的互斥可空字段；本 GDD 不预先替它们选择具体下游 schema。

#### Route Qualification Derivation

正式路线资格使用 exact `route_qualification_record`：`qualification_id`、`qualification_kind`、`source_choice_ids`、`source_event_ids`、`source_resource_ids`、`derivation_operator` 与 `owner_system: SYS-ENDING`。`qualification_kind` 只能为 `route_membership`、`exclusive_commitment`、`resource_possession`；`derivation_operator` 只能为 `all`/`any`，三组 source IDs 的并集必须非空且全部解析到正式稳定记录。

Axes、event completion 与 resource possession 都不是额外运行时输入。构建期为语义目录中的每个正式 `choice_id` 编译一个 exact immutable `choice_semantic_projection_record`：`choice_id`、`axis_deltas`、`completed_event_ids`、`resource_effects`。`axis_deltas` 是按五轴 canonical order 排序的 exact tuple of `(axis_id, 1)`，可为空且最多两项，必须与提交给 `apply_choice` 的 declaration 深值一致；`resource_effects` 是 exact tuple，每项 exact `route_resource_effect_record` 恰含 `resource_id` 与 `operation`，其中 operation 只能为 `acquire`/`consume`。同一 projection 内不得重复 axis/resource；所有 event/resource ID 必须已登记。目录先由纯 validator 验证 choice coverage、schema、引用、operation 与路径顺序，再冻结为 private `MappingProxyType`。Resolver 第三阶段先重放 `axis_deltas` 并与 snapshot axes 比较，再进入 token/route folds。

Resolver 只从 ordered `choice_history` 左到右重建：completed-event set 对 `completed_event_ids` 做 union；resource-possession set 对 `acquire` 加入、对 `consume` 移除。任一路径对已持有资源重复 acquire、对未持有资源 consume，或 history choice 缺少 projection，均由内容路径验证失败；即使 snapshot exact-type、ID 唯一、catalog-covered，运行时遇到重复 acquire 或 absent consume 也必须在 route-fact fold stage 防御性抛出 `ValueError`，且 qualification、ending-priority、cause extraction 与 record construction 调用数全部为 0。随后 `source_choice_ids` 只检查 history membership，`source_event_ids`/`source_resource_ids` 只检查上述两个派生集合。除 detached snapshot 与冻结目录外，resolver 不得读取 Ren’Py store、persistent、章节 flag、事件管理器、背包或其他 live state；同一 snapshot 在任意不同外部状态 fixture 下必须产生深值等价的 facts、qualification set 与完整 `ending_resolution_record`。

资格不保存、授予或修复独立布尔状态。资格记录不得使用五轴名、反证 domain、阈值或抽象“善意/理解/正确选择”类别作为 source；不得恰好形成五条与 semantic axes 一一对应的条目，也不得被 `rain_stops` predicate 引用。静态验证必须证明同一 snapshot 总是派生同一资格，且删除资格目录不会改变 `semantic_state` 的保存形状。

#### Counterevidence Token Contract

反证 domain 固定且恰好对应五轴：`understanding`、`autonomy`、`truth`、`preparation`、`sacrifice`。它们不是新分数，也没有正向 `grant`。

- `revoke` record 必须包含：`kind: revoke`、`domain`、全局唯一 `token_id`、所违反的创作支柱 ID、具体反向行为摘要、token-specific `consequence_id` 和 `resolution_mode`。`resolution_mode` 只能为 `repairable` 或 `irreversible`。
- `repair` record 必须包含：`kind: repair`、`domain`、exactly one `target_token_id`、token-specific `repair_payoff_id` 和一个已注册 `repair_cost_tag`。
- 单个选择最多携带一个 effect；一个 repair 只能解决一个 token，不能通配 domain、前缀或集合。
- `repair_cost_tag` 必须指向实体注册表中 `kind: repair_cost` 的条目；类别只能是可观察的资源损失、人物承担、路线机会损失或已发生后果后的具体补偿，并附具体内容证据。单纯再次选择正向答案、口头道歉或不同 reaction 文本不构成 repair。
- repair 的 `domain` 必须与目标 token 的 domain 完全一致；目标 token 必须为 `repairable`。repair 必须发生在其 `consequence_id` 已经可观察之后，并且在每条到达该 repair 的路径上，目标都必须在 repair 前一前缀仍属于 unresolved set。图验证器必须拒绝同节点立即撤销、domain 不匹配、目标不可达、目标已被其他 repair 清除或任一路径前缀中目标未处于 unresolved 的 repair。
- 每个 `repairable` token 必须登记至少一个 token-specific repair choice，并提供“产生 → 后果可观察 → repair 前仍 unresolved → repair 后移除”的完整路径见证。
- `irreversible` token 不得拥有 repair，并必须引用一个 `irreversible_approval` record：`approval_id`、`token_id`、`owner_system: SYS-NARRATIVE`、`author_id`、`reviewer_role: Creative Director`、`reviewer_id`、`review_date`、`severity_class: route_critical`、`severity_evidence_id`、`criterion_results`、`rationale` 与 `status: accepted`。`author_id`/`reviewer_id` 不是自由字符串，必须各自解析到 exact `review_identity_record`：`identity_id`、`canonical_person_id`、非空 `display_name`、非空 `role_ids`、`aliases`、`status: active` 与 `registry_owner: PROJECT`；所有 alias 全局唯一且只能归属一个 `canonical_person_id`。机器验证比较规范身份，要求 `canonical_person_id(reviewer_id) != canonical_person_id(author_id)`，因此同一人使用两个 identity/alias 仍不能绕过审核。`criterion_results` 必须恰含 `pillar_violation`、`remaining_time_unrepairable`、`scene_demonstrates_permanence`、`not_content_cost_shortcut` 四键且值全部为 `pass`。
- 对产生 irreversible token 的每个 reachable prehistory `h` 和每个 `s ∈ L_revoke(h)`，路径验证器都必须登记 `irreversible_path_witness`：`witness_id`、`token_id`、`prehistory_id`、`continuation_ids`、`later_major_choice_node_ids`、`shortest_later_choice_count`、`agency_witness_node_id`、`agency_effect_kind`、`agency_branch_outcomes` 和 `ending_payoff_id`。每条 continuation 的 `shortest_later_choice_count >= 2`，而不是全图合计两个节点。
- `agency_witness_node_id` 必须位于该 continuation 的 revoke 之后、ending entry 之前。`agency_branch_outcomes` 是非空 exact tuple，每项为 exact record `branch_choice_id → outcome_reference_ids`；它必须恰好覆盖该 node 的所有直接玩家分支、至少包含两个不同 branch choice ID，且至少两项映射到不同的 registered outcome reference 集合。差异必须在 token 保持 unresolved 时改变 `ending_selection`、`character_fate`、`cost_bearer` 或 `tragedy_closure` 之一；只有文本、reaction ID、镜头或无关资源差异不算后续能动性。
- 不可逆 revoke 不得发生在第七日 ending commit 节点，也不得成为紧邻结局的最后一道选择。每条可达结局 continuation 都必须拥有 token-specific ending payoff。
- 全部正式内容最多定义 10 个 revoke token，每个 domain 最多 2 个。新增或改变上限必须重新进行本 GDD 的独立设计审查。

**Machine example:** `token_hide_terminal_truth` 在 Day 5 产生。若一条可达 continuation 为 `("day6_choose_carrier", "day7_accept_cost")`，witness 必须记录最短后续节点数 2，并证明 `day6_choose_carrier` 的不同分支改变 `cost_bearer` 或人物归宿。若另一条到结局的 continuation 只有 `("day7_cosmetic_pause",)`，即使全图其他路线存在更多节点，该 token 仍因该路径计数 1 且没有实质 agency witness 而构建失败。

```text
witness_id: example_irreversible_path_01
token_id: token_hide_terminal_truth
prehistory_id: example_day5_history
continuation_ids: [day6_choose_carrier, day7_accept_cost]
later_major_choice_node_ids: [node_day6_carrier, node_day7_cost]
shortest_later_choice_count: 2
agency_witness_node_id: node_day6_carrier
agency_effect_kind: cost_bearer
agency_branch_outcomes:
  - branch_choice_id: day6_player_bears_cost
    outcome_reference_ids: [outcome_player_bears_cost]
  - branch_choice_id: day6_ally_bears_cost
    outcome_reference_ids: [outcome_ally_bears_cost]
ending_payoff_id: payoff_hidden_truth_cost
```

`SYS-ENDING` 从 `U0 = ∅` 开始按 history 左到右折叠未解决集合：

- 遇到 `revoke(token_id)`：`U_next = U_current ∪ {token_id}`。
- 遇到 `repair(target_token_id)` 且目标存在于 `U_current`：`U_next = U_current - {target_token_id}`。
- 遇到 repair 时，若其已通过构建期验证的目标在当前 history 前缀中尚未产生或已经解决，即目标不在 `U_current`：resolver 在 fold-legality stage 抛出 `ValueError`，不得继续判定结局；静态路径验证同时报告内容失败。
- 普通正向选择或重复轴证据：集合不变。

因此 `revoke_a → revoke_b → repair_a` 后仍保留 `revoke_b`；任意数量的普通正向选择都不能清除 token。Unknown target、wrong domain/mode、irreversible target、重复 token 定义或其他 invalid repair reference 在冻结目录创建前固定构建失败，正常 resolver 不存在这些 catalog-schema/reference 分支。运行时只防御 history catalog coverage，以及 repair target 在当前前缀尚未产生或已被另一 repair 解决的 fold-legality 错误。

#### Frozen Catalog Construction

Counterevidence catalog 的 authoring source 在 import/build-time 编译为 exact tuple；每项是 immutable `NamedTuple` record，字段只含 exact scalar 或 tuple，不含 list/dict/set。Imported module 初始化时先调用私有 `_validate_counterevidence_records(records)`，按固定顺序验证 choice ID 唯一性、effect `kind`、字段 schema、token 上限/domain、repair 引用与 resolution mode；通过后才创建私有 `_COUNTEREVIDENCE_INDEX = MappingProxyType({...})`。任一失败都阻止模块初始化、测试收集与构建，不产生半成品 index。

目录没有运行时注册、替换或删除 API。对 mapping 的 item assignment 必须抛出 `TypeError`，对 record 字段赋值必须抛出 `AttributeError`，且嵌套 tuple 无可变对象。Snapshot history 的 catalog coverage、逐项 fold 合法性与 ending priority 仍在每次 resolver 调用中验证；目录 schema、token definition、caps/domain/mode 与 repair reference 不在运行时重复验证。测试 catalog failure 时只允许显式调用纯 `_validate_counterevidence_records(fixture_records)` 或在隔离模块初始化中替换编译期 records；不得向 `resolve_ending` 增加 catalog 注入参数、可变全局替换 seam 或运行时 failure hook。

#### Resolver Purity Closure

`STATE-DOWNSTREAM-010` 的零外部状态读取不能只由已执行 fixture 的 spy 证明。`SYS-TEST` 必须保存 `resolve_ending_record` 与兼容 wrapper `resolve_ending` 的 production source manifest、解析后的完整传递 callgraph、每个 global/import/call target 的分类、branch coverage、动态 dependency trace 和违规位置报告。Callgraph 必须覆盖直接调用、import/module aliases、赋值、参数/返回、closure、容器、wrapper、property、decorator、`getattr`、`globals`/`locals`、动态 import、字符串查找与反射；任何无法静态解析的边使构建失败。

Resolver closure 只允许 detached exact built-ins、局部值、冻结 catalogs 与下列 **v2 exact dependency policy**。Static analyzer 同时扫描显式 call target、constructor expansion 和 CPython 3.12 bytecode implicit dispatch；只扫 callgraph 不合格。

**Explicit leaves:** `builtins.len/range/enumerate/zip/all/any/min/max/sorted/tuple/list/dict/set/frozenset/type/isinstance`，`builtins.str.encode`、`builtins.bytes.join`，`builtins.list.append`，`builtins.set.add/remove/discard`，`builtins.dict.get/items/__setitem__`，`types.MappingProxyType.__getitem__/get/items`，以及 `_hashlib.openssl_sha256`、`_hashlib.HASH.hexdigest`。Local mutable list/dict/set 只能在当前 call 内创建、修改和丢弃，不得存入 module/catalog/return record。

**Implicit opcode policy (CPython 3.12 only):**

| Opcode family | Exact allowed operands / condition |
|---|---|
| `COMPARE_OP`, `IS_OP` | exact bool/int/str/bytes/tuple/`None`；只允许 `== != < <= > >= is is-not` |
| `CONTAINS_OP` | needle 为 exact scalar；haystack 为 exact tuple/list/set/frozenset/dict/MappingProxyType；禁止 custom `__contains__` |
| `BINARY_SUBSCR` | exact tuple/list/bytes/str + exact int，或 exact dict/MappingProxyType + exact str；禁止 `__index__` coercion |
| `BINARY_OP` | exact int 的 `+ -`；exact str/bytes/tuple 的同类型 `+`；其他 arithmetic/dispatch 禁止 |
| `GET_ITER`, `FOR_ITER` | exact tuple/list/range；exact set/frozenset/dict/MappingProxyType 只允许作为 `builtins.sorted` 的直接输入并使用固定 key，不得直接影响输出顺序 |
| `BUILD_TUPLE/LIST/SET/MAP`, `STORE_SUBSCR` | 仅构造/修改当前 call 的 exact local built-ins；key/value 已通过 exact-type policy |
| truth branch / `UNARY_NOT` | 只接受 exact bool；不得隐式调用任意对象 `__bool__`/`__len__` |
| bytes/string/tuple construction | 只允许上表同类型 concatenation 与显式 allowlisted encoder leaves |

**Record constructors:** 只允许 `ending_rules.EndingCauseRecord`、`ClauseEvaluationTraceEntry`、`HigherPriorityExclusionEntry`、`EndingResolutionRecord`、`UnresolvedAuditFact`、`FrozenResolutionEvaluation` 的 concrete class call。Analyzer 将每次 call 展开为该 exact class generated `__new__` 与 `builtins.tuple.__new__`；后者只可从这些六个 callsites 到达。上述 class 的 `(module, qualname, field order)` 必须与 schema 表逐项相同。Descriptor reads 也按 concrete `(module, qualname, field)` 完全展开，禁止 wildcard。

**Exceptions:** 只允许 concrete `builtins.TypeError` 与 `builtins.ValueError` constructor，参数恰为一个冻结 error-code exact string；禁止把输入对象格式化、`repr` 或连接进错误文本。`raise` 不允许 custom exception、cause/context traversal 或外部日志。

任何未列 explicit leaf、opcode/operand pair、record/exception constructor、native target 或无法解析 edge 一律 fail closed。对抗 fixtures 为每个 implicit family 注入 exact-type 不合格的 subclass/protocol bomb，并覆盖 `__contains__`、`__getitem__`、`__index__`、`__iter__`、`__bool__`、arithmetic reflected methods、descriptor 与 constructor metaclass；resolver 必须在 dispatch 前按类型失败，所有 bomb call count 为 0。另有 native-dispatch mutant 把非白名单 C descriptor 放到未执行 branch；STATIC/BRANCH 必须定位并使构建失败。

Native boundary 仍固定到 Ren’Py `8.5.3.26051504` 自带 CPython `3.12.7`、`cpython-312` 与 interpreter SHA-256 `7c220ddbc41821a2c15199449fed09c0717e928f1d31abf0af7011c211d153a0`。Static report 保存 policy version/hash、opcode table hash、constructor expansion、每个 dependency exact module/qualname/source/native 分类与 runtime manifest。任一 runtime 或 opcode 变化都要求重新生成并独立复审；`UT_PURE + INSTR + STATIC + BRANCH` 缺一不可。

严格劣势使用唯一、不可按实现自行解释的偏序。正式重大选择图从新游戏到 ending entry 必须是有限 DAG；出现 choice-node cycle、悬空边或无法到达 ending entry 的 continuation 时，内容构建先失败，不进入 dominance。

对同一 node、任一可达合法前置 history `h` 和选项 `X`，定义 continuation language `L_X(h)`：选择 X 后到 ending entry 之前所有合法、有限、按顺序排列的 stable `choice_id` suffix 集合，包括没有后续重大选择时的空 suffix。B “接受” suffix `s`，仅当 `h → B → s` 中每个 ID 都能按原顺序合法执行并到达 ending entry；仅仅到达相同 node 集合或相同结局不算接受。

只有对该 node 的**每个**可达 `h`，B 同时满足以下全部条件，并且至少一个条件严格改善时，A 才是严格劣势：

- **Continuation-language preservation**：`L_A(h) ⊆ L_B(h)`。若 A 的任一合法 suffix 在替换成 B 后有任一 ID 不可执行，立即判为不可支配，不再用节点集合弥补。
- **Prefix token relation**：对每个 `s ∈ L_A(h)`，比较 `h → A → s` 与 `h → B → s`；从选择后前缀开始到 ending entry 的每个对齐前缀 `k`，都必须满足 `U_B(h,s,k) ⊆ U_A(h,s,k)`。任一前缀出现互不包含的 token 集，A/B 在 token 维度默认不可比较，不能仅按集合大小、token 数量或 repair/revoke 标签声称 B 更优。
- **Costs**：B 的 `risk_vector`、`resource_costs` 与 `character_costs` 均逐分量不高于 A。固定向量按固定 key 比较；稀疏 `resource_costs` 按 A/B key 并集比较，缺键严格视为 exact int `0`，未知资源 ID 先使内容验证失败。
- **Positive evidence**：B 的轴增量 key set 包含 A 的全部轴增量 key set。
- **Audited value**：A 的已注册 `unique_value_tags` 是 B 对应集合的子集。

“至少一个严格改善”只能来自：某个 `h` 上 continuation language proper superset、任一对齐前缀 token proper subset、任一成本分量更低、轴增量 proper superset，或审核后价值 proper superset。若所有维度完全相等，属于重复/等价选项预警，不构成 strict dominance；若任一维度不可比较，则不得判定支配。

`immediate_reaction_id`、`payoff_ids`、文本措辞、镜头或动画 ID 只用于追踪呈现，永远不能单独作为严格劣势比较中的独有价值。不同 ID 只有在它们交付了注册表中不同的 `semantic_value` 且有具体证据引用时，才会影响比较结果。验证失败必须列出支配选项、每个前置 `h` 的 `L_A/L_B`、每个 suffix/前缀的 `U_A/U_B`、按并集展开的三组成本向量、轴增量和审核后价值标签，并指出至少一个严格改善分量。

**Machine example:** 若 `L_A(h) = {("day5_share", "day6_exit"), ("day5_hide", "day6_wait")}`，而 B 虽能到达与 A 相同的 node 集合，却只能执行第一条 suffix，则 `L_A(h) ⊄ L_B(h)`，B 不支配 A。只有 B 接受两条完整 suffix，且所有对应 token 前缀、成本、轴与价值条件均成立，才继续判定。

```text
comparison_id: example_dominance_language_01
node_id: example_day4_route
prehistory_id: example_h
option_a: example_a
option_b: example_b
L_A:
  - [day5_share, day6_exit]
  - [day5_hide, day6_wait]
L_B:
  - [day5_share, day6_exit]
language_inclusion: false
dominance_result: incomparable
```

零增量选项必须保留至少一种可验证的独有价值或代价，不能只是“没有得分的错误答案”。得分选项也不得自动获得最温暖的即时反应；反应强度由情境和人物边界决定，不由累计轴值统一驱动。

愿望手册与结局回顾可以显示具体事件和因果回收，但不得呈现待填满槽位、完成百分比、缺失条目暗示、轴标签、阈值或“正确选择”提示。首次通关前必须保持结果不确定；通关后的解释可以指出具体行为造成的结果，但仍不显示原始数值或判定公式。

## Formulas

本系统不使用章节权重、负数、随机数或组合倍率。序章至第七日均使用同一组固定规则。

### Choice Novelty

The `choice_novelty` formula is defined as:

`N(c, H) = 1 if c not in H else 0`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Choice ID | `c` | exact string | 合法且全局唯一 | 当前提交的语义选择 |
| Choice history | `H` | validated ordered collection | 0 至全部已选 ID | 当前回退点下已经发生的选择 |
| Novelty | `N` | int | 0–1 | 该选择是否尚未应用 |

**Output Range:** `0–1`；新 ID 输出 1，重复 ID 输出 0。  
**Example:** `c = "prologue_read_note"` 且 `c not in H` 时，`N = 1`；同一状态再次提交时，`N = 0`。

### Axis Update

The `axis_update` formula is defined as:

`axis_next(a) = min(AXIS_MAX, axis_current(a) + N(c, H) × delta(a))`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Current axis value | `axis_current(a)` | int | 0–3 | 选择发生前该轴的值 |
| Axis maximum | `AXIS_MAX` | int | 固定为 3 | 任意轴允许达到的最高值 |
| Choice novelty | `N(c, H)` | int | 0–1 | `choice_novelty` 的输出 |
| Axis delta | `delta(a)` | derived int | 0–1 | `a` 出现在合法稀疏 mapping 中时为 1，否则为 0 |
| Next axis value | `axis_next(a)` | int | 0–3 | 原子提交后的轴值 |

**Output Range:** `0–3`；任何合法输入都不能产生范围外结果。  
**Example:** `understanding = 2`，新选择提供 `delta = 1` 时，下一值为 3；若当前值已经为 3，结果仍为 3；若 ID 已存在于历史中，`N = 0`，结果保持不变。

### Affected Axis Count

The `affected_axis_count` formula is defined as:

`affected_axis_count = Σ delta(a), for a in AXES`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Axis set | `AXES` | fixed set | 5 个轴 | 五条合法语义轴 |
| Axis delta | `delta(a)` | int | 0–1 | 该选择对每条轴的增量 |
| Affected axis count | `affected_axis_count` | int | 原始值 0–5；合法值 0–2 | 当前选择影响的轴数 |

**Output Range:** 原始数学输出为 `0–5`；只有 `0–2` 是合法提交，结果大于 2 时拒绝整个内容定义，不应用任何轴变化。  
**Example:** `{"understanding": 1, "autonomy": 1}` 的结果为 2，可以提交；再加入 `truth: 1` 后结果为 3，属于无效选择配置。

### Unresolved Counterevidence Fold

The `unresolved_counterevidence` fold is defined as:

`U_i = (U_(i-1) ∪ {t_i})` for `revoke(t_i)`  
`U_i = (U_(i-1) - {t_i})` for `repair(t_i)` when `t_i ∈ U_(i-1)`  
`U_i = U_(i-1)` for ordinary choices; an invalid repair has no mathematical output and raises `ValueError`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Ordered history | `H` | exact built-in list | 0 至全部重大选择 | detached snapshot 中的稳定 choice IDs |
| Semantic catalog | `C` | private read-only `types.MappingProxyType` over exact built-in dict | 每个正式 choice ID 恰好一项；import/build-time 已验证并冻结 | ID 对应 null/revoke/repair immutable record |
| Token | `t_i` | exact string | 全局唯一 revoke token | 一次具体路线关键违背 |
| Unresolved set | `U_i` | built-in set during pure calculation | 0–10 tokens | 处理第 i 个历史项后的未解决 token |

**Output Range:** 空集合至最多 10 个全局已登记 token；结果由有序 history 唯一决定。  
**Example:** `revoke(token_a) → revoke(token_b) → repair(token_a) → 普通正向选择` 的最终集合为 `{token_b}`；`revoke(token_a) → repair_via_cost_a(token_a) → repair_via_cost_b(token_a)` 在第二个不同 repair choice 处因目标已解决而抛出 `ValueError`。Unknown target、wrong domain/mode 与 irreversible target fixture 在 catalog validator 阶段失败，不能进入该运行时公式；不存在 `grant` 或“最后选择覆盖”分支。

> `systems-designer` 未参与本节——Solo 模式；生产前需独立复核。

## Edge Cases

- **If an update contains an unknown axis name**: reject the entire update; do not change any axis or append the choice ID.
- **If any supplied axis delta is not exact integer `1`**: reject the entire update; explicit zero, negative values, booleans, fractions and values above 1 are invalid. An omitted key means zero.
- **If one choice affects more than two axes**: reject the entire update; do not truncate the extra axes.
- **If the choice ID is empty or violates the stable-ID convention**: only after the global state+payload type sweep succeeds, reject the update before any delta value/shape/count evaluation.
- **If the choice ID already exists in the restored history**: return `DUPLICATE_NOOP` and preserve deep value equivalence; static content validation reports the duplicate as a failing content defect.
- **If a new legal choice uses an empty `RunMap` for axis deltas**: append its ID to history and leave all axes unchanged, preserving it for narrative reactions, delayed payoff, or a declared counterevidence effect.
- **If a legal new choice adds evidence to an axis already at 3**: keep that axis at 3 and still append the new choice ID.
- **If a route-critical reverse behavior occurs after its related axis has reached 3**: keep the axis at 3, append the choice ID, and add its unique revoke token to the derived unresolved set.
- **If two different revoke tokens remain unresolved**: one targeted repair removes at most its named token; the other remains and `rain_stops` cannot match.
- **If ordinary positive evidence or the same axis reaches 3 after a revoke**: leave the unresolved token unchanged; no `grant` operation exists.
- **If a build-valid frozen repair targets a token not unresolved at the current history prefix**: resolver 在 fold-legality stage 抛出 `ValueError`，不产生结局，并使静态路径验证失败；不得把 repair 转成正向路线 credit。
- **If route-fact fold sees acquire for a resource already possessed, or consume for a resource not possessed**: raise `ValueError` at route-fact fold; qualification, ending priority, cause extraction and record construction must not run.
- **If an authoring repair references an unknown target, wrong domain/mode, irreversible target, or otherwise invalid record**: pure catalog validator/import initialization fails before `_COUNTEREVIDENCE_INDEX` exists；该错误没有正常 resolver runtime 分支。
- **If a predicate catalog uses a missing/non-contiguous `clause_order`, cross-ending operand, forbidden comparator/value pair, `required_truth_value: false`, non-fallback constant, cycle, dangling operand or unreachable clause**: fail the build before the frozen predicate index exists; resolver has no recovery or normalization path.
- **If clause/audit templates violate their disjoint lineage key, an audit source does not start with its token ID, canonical bytes differ from golden vectors, or the build-layer digest bijection checker receives equal digest for unequal payloads**: fail catalog construction; production hash is never replaceable.
- **If any player-facing narrative option is unclassified, allowlisted as navigation, lacks an immediate postdominating reaction, or any legal `(choice, prehistory, continuation)` lacks a causally bound later payoff**: fail content validation even when IDs are nonempty.
- **If `resolve_ending` invokes the canonical resolver zero or more than one time, reads any field besides `.ending_id`, or performs validation/fold/evaluation itself**: fail wrapper conformance; it is not an alternative resolution entrypoint.
- **If an irreversible token is offered at ending commit, or any one continuation has shortest later-choice count below 2, lacks a substantive agency witness, accepted non-author approval, or ending payoff**: fail content validation; it cannot be admitted to the catalog.
- **If any validation step fails during submission**: commit neither the axis changes nor the history entry; partial state is forbidden.
- **If the player rolls back before a choice and selects the same branch again**: use the restored pre-choice history, then apply the choice normally once.
- **If the player rolls back and selects another branch**: remove the original branch’s ID and axis effects through rollback, then apply only the new branch.
- **If one interaction attempts to submit multiple choice IDs**: treat it as a content defect; do not merge the submissions or infer their order.
- **If active state has an exact-type error when an ending snapshot is requested**: raise `TypeError`; never clamp, normalize, or create a partial snapshot.
- **If active state has a schema value, key-set, ID-format, duplicate-history or range error when an ending snapshot is requested**: raise `ValueError`; never repair it silently.
- **If a consumer mutates a returned ending snapshot**: allow mutation of that detached local dict/list graph; the live `semantic_state` and later snapshots remain unchanged.
- **If a loaded save has `state_schema_sentinel is None`**: classify it as `LEGACY_INCOMPATIBLE`, jump to the blocking safe flow, and never let `default` initialize a valid state.
- **If a loaded save has an unknown exact-string or wrong-type sentinel, or a corrupt schema 2 envelope**: classify the first two as `UNSUPPORTED_VERSION` without invoking the state validator, and the v2-plus-corrupt case as `CORRUPT_STATE`; offer only main menu or explicit new game.
- **If the player starts a new game from the incompatibility flow**: initialize sentinel and state through the sole new-game initializer; preserve valid persistent unlocks and discard only the incompatible per-run state.
- **If a persistent achievement remains unlocked after rollback restores an earlier run state**: preserve the persistent unlock, restore the five axes normally, and never derive axis values from that unlock.

> `systems-designer` 未参与本节——Solo 模式；生产前需独立复核。

## Dependencies

| 依赖 | 类型 | 数据方向 | 接口与所有权 | 状态 |
|---|---|---|---|---|
| Ren’Py store/rollback | Hard runtime | Engine → SYS-STATE | 引擎拥有局内变量生命周期、存档快照和回退恢复；SYS-STATE 只定义必须共同恢复的数据 | Confirmed by ADR-0002 |
| `SYS-CHOICE` | Hard runtime | SYS-CHOICE → SYS-STATE | 提供稳定 `choice_id` 与合法增量；SYS-STATE 验证并原子提交 | Provisional |
| `SYS-SAVE` | Hard runtime | Bidirectional | 保存并恢复 sentinel 与 `semantic_state`，并在 `after_load` 分类支持性后进入继续或阻断式安全流程 | Provisional |
| `SYS-ENDING` | Hard runtime | SYS-STATE → SYS-ENDING | 接收 exact built-in schema/axes/history 快照；从冻结目录派生未解决 token、event/resource facts、资格、完整 clause trace 与实际路径 causes，返回 immutable resolution record 且不读取/回写实时状态 | Confirmed by ADR-0001/0004/0005 |
| `SYS-NARRATIVE` | Hard content | Bidirectional | 章节定义行为证据；读取选择历史进行即时反应和延迟回收 | Provisional |
| `SYS-JOURNAL` | Soft presentation | SYS-STATE → SYS-JOURNAL | 只提供事件摘要或选择回收，不提供轴值 | Provisional |
| `SYS-ACCESS` | Hard presentation/input | Bidirectional | 等价输入复用同一 player-facing choice record/ID；UI/自发声不读取隐藏轴，也不绕过 reaction/payoff coverage | Designed；full re-review pending |
| `SYS-TENSION` | Optional extension | SYS-TENSION → SYS-CHOICE | post-MVP 超时结果先转为普通语义选择，再由统一入口提交 | Deferred to post-MVP |
| `SYS-TEST` | Verification | Observe all public behavior | 验证范围、原子性、重复 ID、回退、存读档和快照纯度 | Required for acceptance |
| `SYS-PERSIST` | Explicit boundary | No axis-value flow | 仅管理跨周目解锁；不得保存、恢复或推导五轴 | Confirmed by ADR-0002 |
| Imported Python modules | Explicit boundary | Immutable transfer in / detached snapshot out | snapshot builder 只接收 exact scalar 与 detached tuple，resolver 只接收 exact built-in snapshot；二者不得接收或持有 live `RunMap`/`RunList` | Confirmed by ADR-0001/0002/0004/0005 |

### Bidirectional Consistency Requirements

- `SYS-CHOICE` GDD 必须把 `SYS-STATE` 列为唯一语义状态写入目标。
- `SYS-ENDING` GDD 必须把完整结局快照（schema、五轴、有序历史）列为唯一动态结局状态输入，并定义 frozen choice-to-counterevidence、choice-to-event/resource projection、typed predicate-clause graph、未解决 token/route-fact fold、实际路径 cause generation、total ordering 与 immutable resolution record；不得读取其他 live state。
- `SYS-NARRATIVE` GDD 必须遵守每个选择最多影响两轴、每轴最多 `+1`。
- `SYS-SAVE` GDD 必须把 sentinel 与状态信封视为同一存读档兼容性单元，并实现三类失败结果的阻断式安全流程。
- `SYS-JOURNAL` GDD 必须禁止读取或显示内部轴值。
- `SYS-ACCESS` GDD 必须让键盘、鼠标与已批准等价输入复用相同 choice ID/coverage record，不得创建 scanner 外的叙事分支；首发不宣称完整手柄支持。
- `SYS-PERSIST` GDD 必须明确五轴不跨周目保存。
- `SYS-ACHIEVE` GDD 必须采用下述 `achievement_condition_record` schema，并证明玩家不能从未解锁槽位、名称、描述或一组正向行为成就反推出五轴、token、阈值或真结局清单。

在相关 GDD 获批前，所有标记为 Provisional 的接口不得作为 stories 的最终验收依据。

## Tuning Knobs

### Locked Invariants

以下值不是日常调参项。任何修改都必须同步修订本 GDD、ADR-0001、ADR-0002、ADR-0004、ADR-0005、`SYS-ENDING` 规则及测试：

| Invariant | Locked Value |
|---|---|
| Axis count | 5 |
| Axis domain | `0–3` |
| Per-choice delta | `0` or `+1` |
| Maximum affected axes per choice | 2 |
| Player visibility | Hidden |
| Rollback state shape | One schema 2 `semantic_state` envelope |
| Load-detection marker | Separate sentinel, explicitly initialized; defaults to `None` |
| Ending state input | Detached schema + axes + ordered choice history |
| Axis interpretation | Positive evidence only; unresolved counterevidence remains separate |
| Counterevidence domains | Exactly 5, one per semantic axis |
| Revoke token definitions | Maximum 10 total; maximum 2 per domain |
| Effects per choice | 0 or 1 revoke/repair record |
| Repair target count | Exactly 1 existing token |
| Token resolution modes | Exactly `repairable` or independently reviewed `irreversible` |
| Irreversible timing witness | On every continuation: shortest later-major-choice count ≥ 2 plus ≥ 1 substantive agency witness; never at ending commit |
| Positive counterevidence-clearing operation | Forbidden; no `grant` |
| Axis/route-qualification dynamic input | Ordered `choice_history` only；axes、event/resource facts rebuild from frozen projection catalog，replayed axes must equal snapshot |
| `rain_stops` positive predicate | Exactly five axes at 3 and unresolved-token set empty; no qualification gate |
| Resolver canonical output | Exact deep-immutable `ending_resolution_record`; string wrapper calls canonical pass once and reads only `.ending_id` |
| Runtime duplicate resource acquire | Route-fact fold `ValueError`; later stages do not run |
| Predicate/cause execution | Exhaustive legal table; per-ending contiguous clause order; one evaluation per reached clause; cause extraction consumes `FrozenResolutionEvaluation` only |
| Cause identity | `cause_payload_v1` exact typed bytes + full SHA-256 runtime ID; template ID remains separate |
| Resolver dependency closure | Detached snapshot + frozen immutable catalogs + explicit/implicit/constructor trusted policy v2 pinned to the engine interpreter |
| Choice feedback/payoff coverage | Every production player-facing narrative choice; every reachable prehistory and every legal terminal continuation has immediate reaction proof plus at least one causal strictly-later payoff |

### Content-Level Knobs

| Knob | Target | Safe Range | Too Low | Too High | Interaction |
|---|---:|---:|---|---|---|
| `evidence_opportunities_per_axis` | 4–5 offered per true-ending recovery route | 4–6 | Fewer than four cannot prove “miss one, still reach 3” recovery | More than six causes early caps and makes later evidence numerically redundant | Four is a hard true-ending witness minimum; range statistics remain advisory elsewhere |
| `same_axis_opportunities_per_chapter` | 0–1 per reachable path | 0–1 per reachable path | Zero across too many chapters makes an axis disappear from the story | More than one allows concentrated progression and weakens seven-day accumulation | Constrained by the chapter branch map |
| `zero_delta_major_choice_ratio` | 45%–65% | 35%–70% | Below 35%, axis-bearing choices risk reading as hidden score optimization | Above 70%, too many major choices may rely on non-axis semantics without enough positive-evidence progression | Zero-delta choices still require registered event/resource/counterevidence/repair/outcome semantics and narrative payoff through `SYS-CHOICE`; v1.2 baseline is `30/52 = 57.7%` |
| `axis_opportunity_spread` | 0–1 per canonical route | 0–1 | A perfectly equal distribution is acceptable but may feel mechanically patterned | A spread above one makes some ending requirements structurally harder | Advisory warning; hard gate is path-level reachability |
| `irreversible_token_definition_count` | 0–2 | 0–2 | Zero is valid; all harms may remain repairable | 3+ risks making routes feel pre-judged and triggers design warning | Advisory target only; absolute token cap remains 10 total/2 per domain |
| `terminal_cause_classes_per_ending` | 1–6 | 1–12 | Zero means a reachable ending lacks causal/payoff coverage | 7–12 triggers scope review; above 12 fails content build until branch scope or payoff capacity changes | Distinct fate/cost/tragedy/cause signatures may never be merged to meet budget |

### Ownership Boundaries

- Ending thresholds and priority belong exclusively to `SYS-ENDING`.
- Counterevidence domains, token caps and fold semantics belong to `SYS-STATE`; token assignment and repair cost evidence are jointly owned by `SYS-NARRATIVE`, `SYS-ENDING` and `SYS-TEST`.
- Immediate-response and delayed-payoff timing belong to `SYS-CHOICE` and `SYS-NARRATIVE`.
- Timeout duration and hesitation behavior belong to `SYS-TENSION`.
- These systems may consume the five-axis rules but may not redefine their locked invariants.

## Visual/Audio Requirements

- 五轴变化本身不触发加分音效、升级提示、闪光、粒子或数值动画。
- 即时反馈必须由 `SYS-NARRATIVE` 通过人物动作、视线、停顿、物件操作或环境变化表达。
- 延迟反馈必须由具体的人、物、信息或承诺完成，不使用抽象的“关系提升”提示。
- 某轴已经封顶时，相关选择仍播放完整叙事反馈；玩家不能从反馈缺失推断内部数值。
- 任何关键信息不得只依靠颜色、声音或动画传达，必须存在可阅读文本或可理解动作语境。
- 本系统不直接申请美术或音频资产；具体资产需求由产生反馈的叙事、UI 或音频系统拥有。

## UI Requirements

- 主菜单、对话 HUD、快捷菜单、存读档、设置、愿望手册、章节完成页和结局页均不得显示五轴名称、数值、趋势或进度条。
- 愿望手册可以显示“被记住的事”和具体因果摘要，但不得将事件映射为轴标签。
- 结局回顾可以列出产生结果的具体选择、物件和承诺，但首屏演出只呈现按固定 cause ordering 生成的 1–3 个 presentation-safe `display_cause_ids`。五个非 fallback ending 的首项必须 matched；postcard 首项必须是 concrete failure/unresolved anchor，constant match 只作审计。不得由作者临时挑选、逐项朗读完整 exclusion matrix，也不得公开内部阈值或评分公式。完整 matched/exclusion/outcome signature 只存在于开发审计与自动化测试。
- 成就页不得用五个正向行为类别、可见未解锁槽位或描述措辞构成五轴/token 的代理清单；零增量选择和非最佳结局路径必须同样拥有可获得成就。
- 玩家不能通过设置界面开启五轴显示。
- 开发构建可以提供状态检查器，显示五轴快照和有序选择历史；该工具必须明确标记为开发专用，并从发行构建中移除。
- 轴状态不得只通过颜色或音效表达；自发声和键盘操作无需识别隐藏轴也能完成游戏。
- UI 自动化应扫描玩家屏幕，确认不存在五轴内部标识符。

> **UX Flag — SYS-STATE**：在创建 UI stories 前，相关约束必须进入主菜单、对话 HUD、愿望手册和结局回顾的 UX 规格。

## Acceptance Criteria

每条验收条件使用稳定 ID，并明确责任系统和证据类型。`STATE-COMP-*` 是 `SYS-STATE` 自身的实现门槛；其余分组只有在对应下游系统进入实现后才成为联合门槛，不得用下游尚未完成为由伪造 `SYS-STATE` 组件通过证据。

### Component Contract — Owner: `SYS-STATE`

组件门槛允许五类 canonical machine evidence，且以下映射是 exhaustive：`UT_ENGINE`（Ren’Py-hosted 自动化组件单元测试）、`UT_PURE`（imported Python 纯逻辑单元测试）、`INSTR`（受控 read/call/dependency/assignment instrumentation）、`STATIC`（生产/测试 source manifest 的静态访问、callgraph、escape 与 CFG 扫描）、`BRANCH`（目标 validator 的 branch coverage）。每个动态测试使用全新 fixture，失败前后比较深值等价；静态结果必须保存被扫描文件清单、排除理由、解析后的 symbol/escape、CFG dominator 证明与违规位置。连字符形式 `UT-ENGINE`/`UT-PURE` 不是有效机器枚举。

| AC | Required evidence |
|---|---|
| `STATE-COMP-000`–`002` | `UT_ENGINE` |
| `STATE-COMP-003` | `UT_ENGINE + INSTR`（state-slot replacement-count spy） |
| `STATE-COMP-004`–`006` | `UT_ENGINE` |
| `STATE-COMP-007` | `UT_ENGINE` |
| `STATE-COMP-008`–`015` | `UT_ENGINE` |
| `STATE-COMP-016` | `UT_ENGINE + INSTR`（dependency-call spy） |
| `STATE-COMP-017` | `UT_ENGINE + STATIC`（shared-primitive callgraph） |
| `STATE-COMP-018`–`019` | `UT_ENGINE` |
| `STATE-COMP-020` | `UT_ENGINE + INSTR + STATIC`（import-boundary trace） |
| `STATE-COMP-021` | `UT_ENGINE + INSTR + STATIC + BRANCH` |
| `STATE-COMP-022` | `UT_PURE + STATIC`（private export/access linkage；与 `STATE-COMP-023` 同一报告） |
| `STATE-COMP-023` | `STATIC`（production callsite allowlist） |

| ID | Given | When | Then |
|---|---|---|---|
| `STATE-COMP-000` | 引擎应用所有 `default`，但尚未显式开始新游戏 | 检查 store | `semantic_state is None` 且 `state_schema_sentinel is None`；不存在自动合法状态 |
| `STATE-COMP-001` | 无活动周目 | 调用唯一新游戏初始化入口 | 写入 exact sentinel，并创建 exact `RunMap` `semantic_state`，恰含 schema 2、五个 exact int 0 的 axes `RunMap`、empty `RunList` history |
| `STATE-COMP-002` | 合法新 ID 与一个 `+1` | 提交 | 返回 `APPLIED`；目标轴加 1；ID 追加一次 |
| `STATE-COMP-003` | 合法新 ID 与两个 `+1`，并对 `semantic_state` slot 启用只记录 replacement 次数的测试 instrumentation | 提交 | 返回 `APPLIED`；replacement count 恰为 1，且该一次替换同时提交两轴与一个历史项 |
| `STATE-COMP-004` | 合法新 ID 与 empty `RunMap` | 提交 | 返回 `APPLIED`；轴不变；ID 追加一次 |
| `STATE-COMP-005` | 目标轴已为 3 | 提交合法新证据 | 轴保持 3，ID 仍追加一次 |
| `STATE-COMP-006` | ID 已在历史中 | 再次提交 | 返回 `DUPLICATE_NOOP`；完整状态保持深值等价 |
| `STATE-COMP-007` | 分别影响 0、1、2、3、4、5 条轴的 payload | 直接调用 `validate_axis_deltas` | 前三项分别返回 exact int 0、1、2；后三项分别抛出 `ValueError`；helper 无状态副作用 |
| `STATE-COMP-008` | `semantic_state`、axes、history 或 deltas 不是规定的 exact `RunMap`/`RunList`，或任一 scalar 不是规定的 exact type | 提交 | 抛出 `TypeError`；完整状态保持深值等价 |
| `STATE-COMP-009` | exact types 合法但 schema 值、ID 格式、键集、历史唯一性或数值范围非法 | 提交 | 抛出 `ValueError`；完整状态保持深值等价 |
| `STATE-COMP-010` | 四组复合错误：state type + payload 任意错误；state value + payload type；state value + payload value；非法 `choice_id` + delta value/shape/count defect | 分别提交 | 依次得到：固定 state-slot `TypeError`；payload `TypeError`；固定 state value-stage `ValueError`；choice-ID `ValueError`。固定顺序为 global known-slot type sweep → state value/shape → choice ID value → delta value/shape/count |
| `STATE-COMP-011` | 逐一构造 `STATE-COMP-007` 至 `010` 的每条失败输入 | 提交前后比较对象图 | `semantic_state` 未被替换，axes 与 history 深值均不变；不存在候选计算注入钩子或不可构造 oracle |
| `STATE-COMP-012` | 合法活动状态 | 请求结局快照 | 返回 detached exact dict，恰含 schema version 2、五轴 exact dict 和有序 history exact list |
| `STATE-COMP-013` | 已返回的快照 | 消费方修改其中 axes 与 history | 活动状态和下一份快照均不受影响 |
| `STATE-COMP-014` | 活动状态存在任一 exact-type 错误 | 请求快照 | 抛出 `TypeError`；不钳制、不修复、不生成部分快照 |
| `STATE-COMP-015` | 活动状态 exact types 合法，但 schema、键集、ID、重复历史或范围非法 | 请求快照 | 抛出 `ValueError`；不钳制、不修复、不生成部分快照 |
| `STATE-COMP-016` | 任意合法或非法状态提交或快照请求 | 跟踪依赖调用 | 组件不执行文件、网络、存档或资产 I/O |
| `STATE-COMP-017` | 当前 state 与 sentinel 均合法，并拥有完整 payload helper callgraph | 调用 `validate_axis_deltas` 后再调用 `apply_choice`，并静态解析二者调用的 private primitives | 两者使用同一组 delta exact-type/value/count primitives；不存在复制实现或一个接受而另一个拒绝的合法/非法 payload |
| `STATE-COMP-018` | sentinel 非法但 state/payload 合法，以及 sentinel 合法但 state/payload 非法 | 分别调用 `apply_choice` 与 `current_ending_snapshot` | 两个 active API 都先验证 sentinel；wrong exact type 抛 `TypeError`，wrong exact value 抛 `ValueError`，不提交也不生成快照 |
| `STATE-COMP-019` | schema-known 槽位同时含 type defect 和 value/shape defect | 分别调用 state validator、`apply_choice` 与 snapshot validator | 每个 `SYS-STATE` 接口均先抛固定槽位 `TypeError`；移除全部 known-slot type defect 后才在固定 value stage 抛 `ValueError`；resolver 复合缺陷由 `STATE-DOWNSTREAM-009` 独立拥有 |
| `STATE-COMP-020` | 合法 live `RunMap`/`RunList` | 请求结局快照并跟踪 import boundary 参数 | private imported builder 只收到 exact int、exact string 组成的 detached tuple；未收到任何 live `RunMap`/`RunList`，返回 exact built-in dict/list graph |
| `STATE-COMP-021` | state/snapshot 有 `extra_cycle`（value 指回 root）与 `extra_bomb`（value 为 protocol bomb）两个 unknown key；payload 分别为 bool 与合法值 | 通过受控 `_read_known_slot` read-trace instrumentation 调用 public APIs，并以静态/branch coverage 证明所有 value fetch 都经过 accessor | trace 恰含规范 known paths，两个 unknown key 的 `__getitem__` 读取与 protocol-call count 均为 0；bool payload 案先抛 `TypeError`，合法 payload 案在 key-set stage 抛 `ValueError`；均有限步终止 |
| `STATE-COMP-022` | 以 wrong root/scalar/item exact type，或 type-clean 但 wrong schema、非五元轴 tuple、越界轴、非法/重复 history 直调 private builder；并读取 `STATE-COMP-023` 的 private-export/access 报告 | 调用 `_build_detached_ending_snapshot` | type defect 固定抛 `TypeError`；其余固定抛 `ValueError`；不返回部分快照，不接受 live `RunMap`/`RunList`；静态报告证明 builder 未作为 public export、wrapper 或 escaped value 暴露 |
| `STATE-COMP-023` | 完整 production/test source manifest，含 `game/**/*.rpy`、`game/**/*.py`、direct/import/module aliases、symbol escape/reflection fixtures、production→test transitive dependency fixtures 与多条 CFG 路径 | 建立 `_build_detached_ending_snapshot` 的 reference/callgraph/CFG 闭包 | 生产调用恰有一处且 symbol 为 `game/10_state.rpy::current_ending_snapshot` 的 active-validation success block，validation 支配所有到达路径；赋值、传参、返回、closure/容器存储、wrapper export、`getattr`/动态 import/字符串反射、未解析引用、production→test-only 泄漏，以及 chapter/UI/achievement/ending/其他 adapter 调用全部构建失败；test-only 直调被报告但不计入生产 allowlist |

### Engine Integration — Joint Owners: `SYS-STATE`, `SYS-SAVE`, `SYS-PERSIST`

证据类型：Ren’Py 自动化集成测试。以下十一项必须是相互独立的测试用例，分别重置 fixture；不得只用一条复合手工流程代替。

| ID | Given | When | Then |
|---|---|---|---|
| `STATE-ENGINE-001` | defaults 为两个 `None`，前一周目 persistent 解锁存在 | 开始新游戏 | 显式写入 `"semantic_state:v2"` 和 schema 2 信封；合法 persistent 解锁不变 |
| `STATE-ENGINE-002` | 合法 sentinel 与状态下创建存档，再改变状态 | 读取该存档 | sentinel 与 `semantic_state` 深值等价于保存点，`after_load` 分类一次并返回 `SUPPORTED` |
| `STATE-ENGINE-003` | 一个选择已应用 | 回退到选择前并再次选同分支 | 从恢复点正常应用一次，不产生重复累计 |
| `STATE-ENGINE-004` | 一个选择已应用 | 回退到选择前并选择另一分支 | 原分支 ID/增量均不存在，只保留替代分支 |
| `STATE-ENGINE-005` | persistent 解锁与局内轴同时存在 | 回退局内状态 | 解锁保持，五轴按回退点恢复，二者互不推导 |
| `STATE-ENGINE-006` | 旧存档缺少两个变量，加载时 defaults 补为 `None` | 进入 `after_load` | 返回 `LEGACY_INCOMPATIBLE` 并跳转阻断式安全流程；不得创建 schema 2 state |
| `STATE-ENGINE-007` | sentinel 为未知 exact string | 进入 `after_load` | 返回 `UNSUPPORTED_VERSION` 并跳转阻断式安全流程 |
| `STATE-ENGINE-008` | sentinel 为 `"semantic_state:v2"`，但 state 非法 | 进入 `after_load` | 返回 `CORRUPT_STATE` 并跳转阻断式安全流程；错误原因进入开发日志而非玩家评分 UI |
| `STATE-ENGINE-009` | 任一阻断结果 | 查看并操作失败界面 | 只能返回主菜单或显式开始新游戏；不能返回旧场景；新游戏只重建 per-run state，合法 persistent 解锁保持 |
| `STATE-ENGINE-010` | 已进入阻断式失败流程 | 尝试 rollback、快捷读档、快捷存档、跳过、history return 与 screen return | 全部被禁用或留在阻断流程；唯一离开路径仍是主菜单或显式新游戏 |
| `STATE-ENGINE-011` | sentinel 分别为 bool、int 与 custom object，state 同时放置会在访问时抛错的 fixture | 进入 `after_load` | 三案均直接返回 `UNSUPPORTED_VERSION` 并进入阻断式安全流程；state validator 调用数为 0，错误 fixture 未被访问 |

### Downstream Contract — Joint Owners

证据类型：接口契约测试；在相应系统获批并实现后执行。

| ID | Joint Owner | Given | When | Then |
|---|---|---|---|---|
| `STATE-DOWNSTREAM-001` | `SYS-CHOICE`, `SYS-NARRATIVE` | 任一 player-facing narrative choice，包括 `narrative_only` | 玩家确认后、reaction 前写入语义状态 | 只调用 `SYS-STATE.apply_choice`，不直接修改轴或历史；`narrative_only` 传 empty `RunMap`，提交 ID 且五轴不变，并随 save/load/rollback 恢复 |
| `STATE-DOWNSTREAM-002` | `SYS-ENDING` | 合法快照与 source-hash-verified test-only AST observation build | 分别调用两个入口 | canonical 返回唯一 exact `ending_rules.EndingResolutionRecord`；wrapper canonical count=1、field reads=`("ending_id",)`，除 canonical call 外无 helper edge；production/instrumented 结果深值相等且 production 不依赖 test source |
| `STATE-DOWNSTREAM-003` | `SYS-PERSIST` | 周目结束或回退 | 保存跨周目数据 | 不保存、恢复或推导五轴数值 |
| `STATE-DOWNSTREAM-004` | `SYS-SAVE` | schema version 不受支持 | 读取存档 | 开发期明确失败；公开发布后仅执行已接受 ADR 覆盖且具有逐版本 fixture 的迁移 |
| `STATE-DOWNSTREAM-005` | `SYS-ENDING` | snapshot、axes、history 或 scalar 不是规定的 exact CPython built-in type | 分别调用两个公共入口 | 均在相同首个阶段抛出同一 `TypeError`；wrapper spy 证明只经一次 canonical pass；不规范化自定义 Mapping/Sequence，不返回 fallback 结局 |
| `STATE-DOWNSTREAM-006` | `SYS-ENDING` | exact types 合法但 snapshot schema、键集、范围、ID 格式、历史唯一性、history catalog coverage 或 replayed-axis equality 非法；token fold 对尚未产生/已经解决的 repair target 执行 repair；或 route-fact fold 对已持有资源重复 acquire / 对未持有资源 consume | 分别调用两个公共入口 | 均在相同首个 snapshot value/shape、coverage+semantic-replay、token-fold 或 route-fact-fold 阶段抛出同一 `ValueError`；不返回 fallback record。失败阶段后的 qualification、priority predicate evaluation、cause extraction 与 record construction counters 为 0。Unknown target、wrong domain/mode、irreversible target 与其他非法 catalog reference 只由构建期 `STATE-CONTENT-025` 验证 |
| `STATE-DOWNSTREAM-007` | `SYS-ENDING` | resolver 返回唯一合法 `ending_id` | `day7_resolve_ending` 进入固定 mapping 对应 label 并调用 `commit_ending_entry` | 只有 `SYS-ENDING` 以 detectable `ending_flow:v1` state 触发 `"Active" → "Ended"`；选择、成就和章节脚本均无直接终止入口，且 transition 不修改 `semantic_state` |
| `STATE-DOWNSTREAM-008` | `SYS-ENDING` | 合法目录、复合缺陷、resource 与 short-circuit mutants、exact observation schema | 调用 instrumented canonical copy | 九阶段按固定顺序；首个失败后 counters 为 0；每个 clause count=1；atomic trace entries 冻结 template/polarity/kind/source 与 value/anchor，audit facts 冻结 `audit`/`unresolved_counterevidence`/`unresolved_token`，cause stage 只读 `FrozenResolutionEvaluation` 即可构造 causes；production CFG 仅多 callback nodes |
| `STATE-DOWNSTREAM-009` | `SYS-ENDING` | detached snapshot 的 schema-known slot 同时含 type defect 与 value/shape/catalog-coverage defect | 分别调用两个公共入口 | 先抛相同固定 built-in slot `TypeError`；移除全部 known-slot type defect 后才在相同固定运行时阶段抛 `ValueError`，且不运行 priority predicate evaluation；wrapper 仍只有一次 canonical 调用 |
| `STATE-DOWNSTREAM-010` | `SYS-ENDING` | 深值等价快照、不同外部状态，以及 explicit/implicit/constructor/custom-protocol/native-dispatch mutants | 以 `UT_PURE + INSTR + STATIC + BRANCH` 扫描/调用两个入口 | record 深值相等、外部读取与 protocol-bomb calls 为 0；policy v2 报告覆盖 explicit targets、CPython 3.12 opcode+operand pairs、六个 record constructors、TypeError/ValueError policy、descriptor expansion 和 runtime pin；任何未列 dispatch 精确定位并失败 |

### Content Contract — Joint Owners: `SYS-NARRATIVE`, `SYS-CHOICE`, `SYS-ENDING`, `SYS-TEST`

证据类型：静态内容验证与确定性路径枚举。`STATE-CONTENT-008/033/034` 中 reaction/payoff exact joins、cardinality、proof-kind nullability 与反向 event metadata 的部分属于 `SYS-CHOICE`/`SYS-NARRATIVE` provisional downstream gate，不计入 `SYS-STATE` 批准。

内容编号 `020` 为 **reserved/deprecated**：对应已撤销的旧资格 AC，永久保留且不得复用；扫描器要求不存在该编号的活动定义或引用。

| ID | Given | When | Then |
|---|---|---|---|
| `STATE-CONTENT-001` | 完整分支图 | 枚举每条可达章节路径 | 任一章节、任一路径、任一轴最多得分一次 |
| `STATE-CONTENT-002` | 六个正式结局 | 枚举首周目见证路径 | 每个结局至少一条合法路径，并记录有序 ID、增量、章末轴、token 产生/定向修复、最终未解决集合和唯一结果 |
| `STATE-CONTENT-003` | `rain_stops` 标准路径，以及分别改变任一 route qualification 的对照 fixture | 解析完整结局快照 | 五轴全 3 且未解决 token 集合为空时命中；route qualification 变化不改变该 predicate，且不使用直接写值、开发标记、persistent 条件或互斥选择并存 |
| `STATE-CONTENT-004` | 五条轴分别对应的一条真结局补救见证 | 依机器定义替换该轴最早一次机会并枚举后续 | 每个机会使用不同 node/choice ID，替换后其余三次仍可达且增量不变、不自动改变 token，最终轴恢复到 3 且结果为 `rain_stops` |
| `STATE-CONTENT-005` | 任一重大选项记录 | 按机器可读 schema 静态验证 | 十个 required 字段齐全、exact 类型正确、所有引用存在；effect 只能为 null、单一 revoke 或单一定向 repair |
| `STATE-CONTENT-006` | 全部正式内容中的 `choice_id` | 跨文件全量扫描 | 每个 ID 只定义一次；引用未定义或重复定义均失败 |
| `STATE-CONTENT-007` | 有限 DAG 中任一重大选择节点的每个可达 prehistory | 枚举 `L_A(h)`/`L_B(h)` 并按唯一偏序比较 | 必须先满足 `L_A(h) ⊆ L_B(h)`；A 的任一 suffix 在 B 后非法即不可支配；随后每个对齐前缀满足 token 子集、成本/轴/价值条件及至少一项严格改善 |
| `STATE-CONTENT-008` | 全部 production player-facing narrative choices、每个 canonical prehistory 与每个 legal terminal continuation | 扫描 source、枚举 DAG 与验证 bindings | 每项恰分类；reaction 在下一控制转移前 postdominate choice commit 并双向绑定；每个 `(c,h,s)` 至少一项严格较晚且在该真实路径上的 payoff，每个 declared payoff 至少被使用；payoff 以 history guard 或 counterfactual outcome 双向证明因果 |
| `STATE-CONTENT-009` | 任一零增量重大选项 | 到达其回收点 | 产生已登记的反应、信息、物件、时间优势、自主性结果或代价，不作为纯错误答案 |
| `STATE-CONTENT-010` | 历史为 `revoke_a → revoke_b → repair_a → 普通正向选择` | fold 并解析结局 | 最终未解决集合恰为 `{revoke_b}`；`rain_stops` 不匹配；正向选择不能清除 token |
| `STATE-CONTENT-011` | 机会数量与分布统计 | 超出非真结局路线的 tuning safe range | 报告设计预警；最终通过/失败仍由路径级可达性、token fold 与唯一结局证据决定 |
| `STATE-CONTENT-012` | 序章“追踪者鞋底”分支 | 检查 `truth +1` 轴证据 | 场景必须同时包含交叉验证线索与向绘梨衣分享风险；仅“记住红泥”不得获得 `truth` |
| `STATE-CONTENT-013` | 绘梨衣的任一即时反馈 | 内容约束扫描与人工复核 | 只使用视线、动作、停顿、物件操作或简单单音节，不以完整口语解释评分 |
| `STATE-CONTENT-014` | 完整语义目录 | 统计 revoke token | domain 恰来自五轴；总定义数不超过 10、每 domain 不超过 2、每选择最多一个 effect；不存在 `grant` |
| `STATE-CONTENT-015` | 任一 `unique_value_tag` | 查询实体注册表与证据引用 | 存在 `kind: semantic_value` 条目和具体内容证据；仅 ID 前缀、reaction/payoff 差异或文本改写均失败 |
| `STATE-CONTENT-016` | 任一 repair authoring record 与全部可达该 repair 的路径 | 先运行 catalog schema/reference validation，再枚举路径并查询实体注册表 | catalog 阶段拒绝 unknown/wrong-domain/wrong-mode/irreversible/wildcard/multi-target/unregistered-cost；路径阶段要求 target 已先产生、consequence 可观察且每条 repair 前缀仍 unresolved，已解决或尚未产生均失败 |
| `STATE-CONTENT-017` | 任意 revoke token 后出现同 domain 正向选择 | fold 历史 | token 保持未解决；目录中若出现 `grant` 操作则构建立即失败 |
| `STATE-CONTENT-018` | 完整 token 目录、approval records、identity registry 与全部 irreversible continuation witnesses | 按 `resolution_mode` 逐路径验证 | repairable 有完整修复 witness；irreversible 的每条 continuation 最短 later count ≥2；author/reviewer IDs 均解析且其 `canonical_person_id` 不同；agency node 的全部 branch choice IDs 恰有 `branch_choice_id → outcome_reference_ids` 映射且至少两项改变注册 outcome；含 ending payoff，且不发生在 ending commit |
| `STATE-CONTENT-019` | 完整 predicate catalog 与逐类非法 mutant | 运行 build validator | exhaustive truth table、exact/连续 order、same-ending graph closure、完整求值与 contributor rules 成立；表外组合逐类失败 |
| `STATE-CONTENT-021` | 两选项的 token 集大小相等但互不包含，以及 repair/revoke 数量相同但 token 不同 | 运行 strict-dominance validator | 两对都报告 token 维度不可比较，不得以数量或 effect kind 判定支配 |
| `STATE-CONTENT-022` | 编译后的 counterevidence records 与 private index | 初始化并尝试修改 mapping、record 与 nested field | records exact tuple 且只含 immutable scalars/tuples；index 是 `MappingProxyType`；修改分别抛 `TypeError`/`AttributeError`，resolver 前后目录深值等价 |
| `STATE-CONTENT-023` | choice graph 含 cycle、悬空边或不能到达 ending entry 的路径 | 构建 continuation languages | 构建失败且不运行 dominance；合法图的所有 `L_X(h)` 均有限并可完整枚举 |
| `STATE-CONTENT-024` | 全部合法 terminal paths | 按 ending ID、total-order causes、history-ordered unresolved IDs/causes、UTF-8 sorted facts 与 terminal outcome signature 生成因果签名 | 每条路径恰归属一个 class；任一签名字段不同不得合并；每 class 有 witness、payoff scene、玩家摘要及 1–3 display IDs。每个 display ID 在 matched/unresolved/exclusion cause union 中恰解析一次且含 matched anchor。每 ending 1–6 正常、7–12 预警、超过 12 构建失败；归下游联合门槛 |
| `STATE-CONTENT-025` | 分别含重复 choice ID、wrong effect kind/schema、超 cap、unknown target、wrong domain/mode、irreversible target 与其他 invalid repair reference 的 authoring-record fixtures | 显式调用纯 catalog validator，并在隔离模块执行初始化 | 每案在 import/build-time 固定失败且不创建 `_COUNTEREVIDENCE_INDEX`；正常 `resolve_ending` 没有 catalog 注入参数、wrong-domain/irreversible-reference 分支或 runtime catalog-schema failure hook |
| `STATE-CONTENT-026` | 完整 outcome registry，以及 agency、terminal signature、payoff 中全部 `outcome_reference_id` | 按 `outcome_reference_record` schema 和 kind 上下文静态验证 | 每个 ID 全局唯一并恰解析一次；subject/state/source events 存在；引用位置允许该 kind；未知、重复、wrong-kind 或悬空引用均使构建失败 |
| `STATE-CONTENT-027` | approval records 与完整 review identity registry | 解析 author/reviewer identity 与 aliases | 每个 identity/alias 恰归属一个 canonical person；不存在 alias 冲突；每个 accepted approval 的 author/reviewer canonical person 不同；自由字符串或同人双 ID 均失败 |
| `STATE-CONTENT-028` | 完整 route qualification 目录、route-fact projection 目录与所有正式路径 | 只依据 ordered history 重建 completed events/resource possession 后重算资格，并扫描保存 schema 与 `rain_stops` predicate | 每项资格 source 并集非空、引用存在、kind/operator 合法且结果确定；不存在 persisted/anonymous qualification bool、外部 live-state read、五轴一一对应清单或 `rain_stops` qualification gate |
| `STATE-CONTENT-029` | 每个正式 choice 的 `choice_semantic_projection_record`、axis/event/resource registry 与全部路径 | 验证 exact schema/coverage/reference/operation，重放 axes并依 history 顺序 fold acquire/consume | 每个 choice 恰有一项 projection（axis/event/resource tuples 均可空）；axis deltas 与 apply-choice declaration 相等且每项为 1、最多两轴；event/resource 引用存在；operation 只能 acquire/consume；任一路径 replayed axes 等于 snapshot，重复 acquire、absent consume 或缺失 projection 构建失败，且冻结 index 不可变 |
| `STATE-CONTENT-030` | Clause/audit templates、每个 source/comparator/result 组合、axis 超额证据路径与 audit 跨六 ending fixtures | 填充 runtime payload | template lineage keys 不冲突；audit 绑定 token 与 selected ending；每格 source/value/anchor 唯一；axis match 只取最早 `r` 个实际增量 choice；同 snapshot 产生唯一 bytes/ID |
| `STATE-CONTENT-031` | Golden vectors、production digest pairs 与 test-only synthetic collision pairs | 运行 encoder 与 build-layer bijection checker | golden hashes不变；production `_hashlib` 不可替换；equal digest + unequal payload 在非 production checker 中失败且 resolver manifest 无 seam/import |
| `STATE-CONTENT-032` | 六个 concrete record classes、frozen artifact、field-order/type/subclass/mutation fixtures | 构造 resolution | module/qualname/field order 唯一；GDD/registry 顺序相同；atomic trace 明确冻结 template/polarity/kind/source，audit fact 明确冻结 `audit`/`unresolved_counterevidence`/`unresolved_token`，cause extraction 仅凭 frozen artifact 独立构造 causes；nested records deep immutable；替代 class/subclass 失败 |
| `STATE-CONTENT-033` | 完整 choice-surface manifest、non-narrative allowlist、history commit 与 provisional reaction/payoff bindings | 扫描 production CFG/AST 并执行 rollback/save/load fixtures | 所有叙事 options/timed/accessibility equivalents 均为 player-facing choice；仅系统导航可排除；每项选择均在确认后、reaction 前经 `apply_choice` 提交，`narrative_only` 使用 empty `RunMap`，其 history ID 随 rollback/save/load 正确恢复且重放一次；reaction exact join/cardinality 仍为 `SYS-CHOICE`/`SYS-NARRATIVE` provisional 门槛 |
| `STATE-CONTENT-034` | 每个 `(choice, canonical prehistory, legal terminal continuation)` 与因果/反事实 fixtures | 验证 payoff coverage | 每组合至少一项真实路径 later payoff；每 declared payoff 被使用；history guard false 时 event 不发出，或 counterfactual registered outcome 不同；通用无关 later event、hash mismatch、单向 binding 均失败 |

### Achievement Anti-Proxy Downstream Gate — Owner: `SYS-ACHIEVE`; Joint: `SYS-NARRATIVE`, `SYS-TEST`

本分组在 `SYS-ACHIEVE` GDD 独立复审通过前是 provisional 下游门槛，不计入 `SYS-STATE` 独立批准。每项成就必须使用 exact 8-field `achievement_condition_record`：`achievement_id`、非空 `condition_event_ids`、`condition_operator=all`、`zero_delta_witness_path_ids`、`non_best_ending_witness_path_ids`、`reveal_policy=ON_UNLOCK`、`display_order_group` 和 `owner_system: SYS-ACHIEVE`。条件只能引用稳定、已完成的叙事 event ID；schema 不允许 axis、token、阈值、resource、qualification、ending membership 或 resolver predicate 字段。

| ID | Given | When | Then |
|---|---|---|---|
| `STATE-ACHIEVE-001` | 11 项独立成就目录，ending/memory mirror count为0 | 按 record schema 静态验证 | 每项字段与 exact 类型正确，event 引用存在且completion mapping唯一，不出现 axis/token/threshold/resource/qualification/ending/resolver 直接读取 |
| `STATE-ACHIEVE-002` | 至少一个非空 `zero_delta_witness_path_ids` | 枚举对应路径 | 成就在已登记 event 完成后解锁，触发选择 `axis_deltas` 为空，witness ID 与路径记录稳定 |
| `STATE-ACHIEVE-003` | 至少一个非空 `non_best_ending_witness_path_ids` | 枚举对应路径 | 成就正常解锁且最终 ending 不是 `rain_stops`；witness ID、event IDs 与结局记录一致 |
| `STATE-ACHIEVE-004` | 成就名称、三组顺序、`ON_UNLOCK`与未解锁零surface | 运行 catalog/UI anti-proxy 检查 | 不形成五 domain 一对一清单，不泄露正确行为或真结局步骤；locked row/slot/count/focus/self-voicing counts均为0 |

### UX/Presentation Contract — Joint Owners: `SYS-JOURNAL`, `SYS-ENDING`, `SYS-ACCESS`; downstream `SYS-ACHIEVE`

证据类型：发行构建 UI 自动扫描加人工视觉检查。

| ID | Surface | Required Result |
|---|---|---|
| `STATE-UX-001` | 主菜单、对话 HUD、快捷菜单、存档、读档、设置、章节完成页 | 不显示轴名、数值、趋势、增减提示或进度条 |
| `STATE-UX-002` | 愿望手册 | 不显示完成槽、缺失条目暗示、百分比、轴标签、阈值或正确答案标记 |
| `STATE-UX-003` | 结局页与结局回顾 | 首屏演出呈现按固定 cause ordering 得到的 1–3 个 presentation-safe `display_cause_ids`；非 postcard 首项 matched，postcard 首项 concrete failure/unresolved，constant fallback audit-only；不由作者临时挑选，不逐项展示完整 exclusion matrix，也不显示原始数值、阈值或判定公式 |
| `STATE-UX-004` | 发行构建全部可达界面 | 不包含开发状态检查器或五轴内部标识符 |
| `STATE-UX-005` | 成就目录与解锁提示（`SYS-ACHIEVE` 下游门槛） | 不按五轴/domain 排列，不显示正向行为缺口，不以五个成就构成真结局步骤清单；未解锁的行为成就不暴露名称或触发提示 |

### Performance Ownership Boundary

- `STATE-COMP-016` 的“无 I/O”是 `SYS-STATE` 唯一独立性能硬门槛。
- Ending canonical pass 的最坏渐进复杂度为 `O(B_in + P + Q + C + B + L·R log R + L·F log F + K log K)`，额外空间为 `O(B_in + P + Q + C + B + R + F + K)`；`B_in` 是被检查输入/catalog IDs 的总字节量，`L=max(1,max sorted source/fact ID bytes)`，`R` 包含全部 cause-ready source references 与 qualification source facts，其余变量沿用本节定义。Cause extraction 的二次 clause 求值仍被禁止。
- 单次更新耗时只有在架构文档定义最低硬件、构建类型、采样数量、计时边界与测试工具后才能设置数值阈值；此前不得使用无法复现的 `16.6 ms` 声明。
- 完整存档耗时属于 `SYS-SAVE`，不由本 GDD 规定或验收；原 `500 ms` 目标必须在 `SYS-SAVE` GDD 中结合实际存档体积和测试硬件重新评估。

> `qa-lead` 未参与本节——Solo 模式；独立复审必须验证分层所有权、稳定 ID 与证据可执行性。

## Open Questions

| ID | 问题 | Owner | 目标期限 |
|---|---|---|---|
| STATE-Q1 | 完整七日分支为每轴安排的四个独立真结局补救节点分别是什么？ | Game Designer / Andwey | `SYS-NARRATIVE` GDD 批准前 |
| STATE-Q2 | 开发状态检查器采用何种构建隔离方式，才能保证不会进入发行包？ | Programmer / Andwey | Foundation/Core epics 创建前 |
| STATE-Q3 | 若未来提出 schema 3，迁移范围与最低兼容公开版本是什么？当前不得提前实现猜测性迁移。 | Programmer + Producer / Andwey | 首次 schema 变更提案时 |
| STATE-Q4 | 最多 10 个 route-critical revoke token 的具体 ID、支柱证据、后果、`resolution_mode`，以及 repairable 的一对一 repair 或 irreversible 的非作者审核、逐 continuation 时序/agency/结局回收见证分别是什么？ | Game Designer + Systems Designer / Andwey | `SYS-ENDING` 与 `SYS-NARRATIVE` GDD 批准前 |
