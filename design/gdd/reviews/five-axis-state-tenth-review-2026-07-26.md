# 五轴局内状态系统：第十次独立复审

> **Review date**: 2026-07-26  
> **Reviewed revision**: Tenth  
> **Reviewed file**: `design/gdd/five-axis-state.md`  
> **Prior verdict**: NEEDS REVISION — Ninth Re-review  
> **Verdict**: NEEDS REVISION  
> **Rough scope signal**: XL（聚焦文档修订量约 S–M）  
> **Review mode**: Full independent review, read-only

## Review Panel

- Game Designer / Narrative Director
- Systems Designer / Ren’Py Implementation Reviewer
- QA Lead
- Creative Director

## Completeness

8/8 必备章节齐全：

- Overview
- Player Fantasy
- Detailed Rules
- Formulas
- Edge Cases
- Dependencies
- Tuning Knobs
- Acceptance Criteria

活动 AC 共 82 项：COMP 24、ENGINE 11、DOWNSTREAM 10、CONTENT 28、ACHIEVE 4、UX 5。`STATE-CONTENT-020` 已永久标为 reserved/deprecated，不属于活动定义。

## Ninth-review Regression

| 第九审项目 | 第十审结果 |
|---|---|
| Executable predicate/cause contract | **部分关闭，仍阻断**：已有 typed tree、完整求值框架、path-specific contributor、anchor 与 total order，但合法域、cause identity 和 schema 尚未闭合 |
| Structured resolution interface | **部分关闭，仍阻断**：已有 canonical record 与 string wrapper，但嵌套 schema、display 输入和阶段关系尚未闭合 |
| Duplicate resource acquire runtime oracle | **已关闭**：与 absent consume 同为 route-fact-fold `ValueError`，后续阶段零调用 |
| Static resolver purity closure | **部分关闭，仍阻断**：四类证据与传递 closure 已加入，但 dependency classifier 仍缺机器唯一的 trusted-leaf/native boundary |
| Reserved CONTENT-020 | **已关闭** |
| Architecture ending flow synchronization | **已关闭** |
| Resolver complexity statement | **已纳入文档；表达精度仍建议复核** |
| History-first anchor narrative salience | **未关闭，保留建议** |

## Dependency Graph

| 依赖 | GDD 状态 | 本次判断 |
|---|---|---|
| Ren’Py store/rollback | 引擎依赖；版本与本地文档已固定 | 存在 |
| `SYS-CHOICE` | 独立 GDD 未创建 | Provisional，不单独阻断 `SYS-STATE` |
| `SYS-SAVE` | 独立 GDD 未创建 | Provisional，不单独阻断 `SYS-STATE` |
| `SYS-ENDING` | 独立 GDD 未创建 | 不得在本次批准前开始 |
| `SYS-NARRATIVE` | 独立 GDD 未创建 | Provisional，不单独阻断 `SYS-STATE` |
| `SYS-JOURNAL` | 独立 GDD 未创建 | Provisional |
| `SYS-TENSION` | 独立 GDD 未创建 | Optional / Provisional |
| `SYS-TEST` | 独立 GDD 未创建 | 当前 AC 已声明联合验证边界 |
| `SYS-PERSIST` | 独立 GDD 未创建 | ADR-0002 已确认边界，GDD 仍待创建 |
| Imported Python modules | 架构与 ADR 已定义 | 存在 |

这些缺失依赖已经在被审 GDD 中明确标记为 Provisional；它们阻止下游 stories 把接口当作最终验收依据，但不是本次拒绝 `SYS-STATE` 的原因。

## Required Before Implementation

### 1. Predicate/clause/cause 合法域必须成为穷尽、可执行的契约

`source_kind`、comparator 与 `required_truth_value` 的合法组合尚未逐项映射到唯一 contributor、anchor、template 与 `cause_kind`。当前合法域允许但没有唯一结果的边界包括：

- `present`/`absent` 与 `required_truth_value: false` 的反转；
- `history_choice` 或 `completed_event` 缺席；
- `constant/always_true` 与 false requirement；
- `axis_value at_least 0`，其成立时没有“首次达到 0”的 history contributor。

`clause_order` 也缺 exact type、范围、唯一/连续规则及跨 ending operand 禁止规则。必须补充 exhaustive truth table、predicate catalog build-time validator、freeze 规则，以及 cycle、shared child、dangling operand、重复 order、非法 source/comparator/template 组合等负例 AC。

证据：`design/gdd/five-axis-state.md:223–239`、`STATE-CONTENT-019`。

### 2. Cause identity 与 template identity 必须只有一种规范解释

当前 `cause_id` 只声明“UTF-8 长度前缀 SHA-256”，没有冻结：

- type tags；
- UTF-8 长度单位与长度字段语法；
- `None`、bool、int、string、tuple 的编码；
- tuple framing、元素数量与 source-reference 规范形式；
- predicate lineage（至少 ending、clause 与 polarity）。

因此不同实现可对同一 cause 产生不同 digest，或把不同语义 clause 合并成同一 payload。还存在直接 ID 冲突：`cause_unsent_postcard_fallback` 在主契约与 registry 中是 template ID，但 `STATE-CONTENT-019` 又把它当作 matched runtime cause；这与 runtime `cause_<64 hex>` 格式不能同时成立。

必须定义 type-tagged canonical byte grammar、template record schema、golden byte/hash vectors、collision/duplicate fixtures，并明确 template ID 与 hashed runtime cause ID 的不同字段。

证据：`design/gdd/five-axis-state.md:229`、`:231–243`、`:698`，`design/registry/entities.yaml:516–557`。

### 3. `EndingResolutionRecord` 的完整嵌套 schema 与 display 输入必须冻结

当前只列出顶层字段，没有规定：

- `clause_evaluation_trace` 的 entry schema 与顺序；
- matched causes、higher-priority exclusions 的 exact container、key order 与深层不可变性；
- folded event/resource/qualification/token IDs 的规范顺序；
- display dedupe 和 ID resolution；
- unresolved-token cause records 的生成、排序与返回位置。

这最后一点构成内部断裂：display 算法要求把 unresolved-token cause records 纳入候选，但 resolution record 只保证 `unresolved_token_ids`，且未保证每个 unresolved token 都会成为 selected/higher-priority predicate contributor。

证据：`design/gdd/five-axis-state.md:216`、`:231–245`，`design/registry/entities.yaml:563–579`。

### 4. Resolver 阶段顺序与 wrapper oracle 必须自洽

固定运行时阶段写为 `ending priority → complete clause/cause extraction`，但 ending priority 必须先求每个候选 ending 的 root clause；`STATE-CONTENT-019` 同时要求每个 reachable clause 只求值一次。现文档没有说明：

- clause evaluation 是 priority 的组成部分还是独立阶段；
- 哪些 ending trees 被求值；
- priority 阶段保存何种 immutable trace；
- cause extraction 是否只能消费该 trace；
- 失败计数器在哪一阶段停止。

必须给出单次求值流程与 stage counters。另需用 call spy 证明 `resolve_ending` 恰调用 `resolve_ending_record` 一次、只读取 `.ending_id`，不自行调用 fold、priority 或 cause helper；两个公共入口都要覆盖相同 invalid-snapshot 与 purity oracle。

证据：`design/gdd/five-axis-state.md:105`、`:245`、`:662`、`:668–670`、`:698`。

### 5. Static purity closure 必须冻结机器可判定的 trusted leaves

`UT_PURE + INSTR + STATIC + BRANCH` 方向正确，但“pure standard-library value operations”仍需人工判断。必须提供 fully-qualified builtin/stdlib allowlist 和 C/native leaf policy，并固定到可审计的 Python/构建身份；其余 builtin、stdlib、native、descriptor、decorator 或 unresolved dependency 均 fail closed，并报告精确位置。

证据：`design/gdd/five-axis-state.md:337–341`、`:670`，`design/registry/entities.yaml:586–619`。

### 6. 每个重大选择都必须有可达的较晚因果回收证据

项目硬规则要求每个选择同时具有即时反应和 later causal payoff。当前非空 `payoff_ids` 只证明引用存在；只有零增量选择的 AC 明确要求到达回收点，不能证明所有重大选择都在某条合法 continuation 上被较晚、具体地消费。

必须为每个正式 choice 提供 choice → payoff 的可达路径 witness，区分即时 reaction 与严格较晚 payoff，并定义 chapter-terminal payoff 的合法时序与 continuation coverage。

证据：`CLAUDE.md` 产品规则 6，`design/gdd/five-axis-state.md:49`、`:260–275`、`:687–688`。

## Recommended Revisions

1. 在 `SYS-ENDING` / `SYS-NARRATIVE` story 或正式内容锁定前，按计划分支与 terminal signature 预估每个 ending 的 class 数；保留现有 1–6 / 7–12 / >12 政策。本项是下游 preflight，不是当前 `SYS-STATE` 独立批准 blocker。
2. 为 history-first `display_cause_ids` 增加叙事显著性试玩门槛，确认最早 matched anchor 能帮助玩家回忆因果链，而不会把决定性牺牲或损失挤出三项展示。
3. 复核复杂度表达是否需要包含 qualification source、cause payload 与排序成本；若实现不能按总序生成，明确 `C log C` 排序项。
4. Schema 冻结后增加一个人类可读的完整 structured-resolution worked example；若 golden vectors 已完整覆盖，本项可省略。

## Specialist Disagreements

- **Purity closure**：Game/Narrative 认为现有四类证据已关闭；Systems/QA 认为缺 trusted-leaf/native boundary 仍允许不同 classifier。Creative Director 同意 Systems/QA，列为 blocker 5。
- **Terminal-class budget**：Game/Narrative 认为缺少内容制作前 forecast；QA 认为 1–6 / 7–12 / >12 硬门槛已经闭合。Creative Director 判定当前 `SYS-STATE` 合同已闭合，forecast 作为下游建议。
- **Later payoff**：Game/Narrative 要求补齐所有选择的可达回收；QA 认为至少应成为建议或下游门槛。Creative Director 因项目 non-negotiable rule 6 将其提升为 blocker 6。

## Nice-to-Have

- 把 UX `Surface / Required Result` 表改写为完整 Given / When / Then。
- 把“启用/禁用语言短路优化的两个 build”改成正常 evaluator 与故意短路 mutant 的明确 mutation test。

## Senior Verdict

第十次修订已经保住了隐藏分数体验、确定性结局、rollback/save 边界、反证修复伦理与 duplicate-resource runtime oracle，概念方向和架构主线无需推翻。

剩余问题集中在 identity、schema、execution order 与 audit proof 的接缝。它们会允许两个实现者写出互不兼容、却都声称符合文档的 resolver，或让合法 predicate 在边界上没有 cause。当前不得批准，也不得开始 `SYS-ENDING`；完成上述聚焦修订后应运行新的独立复审。

### Verdict: NEEDS REVISION

本记录是只读独立审查结论，不是第十一次修订，也不构成自我批准。

## Eleventh Revision Remediation Record

> This appendix records authoring actions only. It does not alter the historical `NEEDS REVISION` verdict and is not an independent re-review.

| Tenth-review blocker | Eleventh-revision action | Status |
|---|---|---|
| Exhaustive predicate/cause legal domain | Added exact clause order/domain rules, complete source/comparator table, same-ending operands, build validator failures and mutation fixtures | Remediated; awaiting independent verification |
| Canonical cause identity | Added template schema, type-tagged `cause_payload_v1`, full SHA-256 runtime IDs, two golden byte/hash vectors and collision failure | Remediated; awaiting independent verification |
| Structured resolution schema | Added exact trace/exclusion/record schemas, deep immutability, deterministic ordering, unresolved causes and display-ID resolution | Remediated; awaiting independent verification |
| Single-pass stage order and wrapper | Split priority evaluation from trace-only cause extraction; added clause/stage counters and exact-one wrapper spy oracle | Remediated; awaiting independent verification |
| Trusted leaves/native boundary | Added exact allowlist v1 and pinned Ren'Py/CPython/interpreter identity; all unlisted targets fail closed | Remediated; awaiting independent verification |
| Later causal payoff | Added per-choice/per-prehistory reachable strictly-later payoff witness schema and declared-payoff coverage | Remediated; awaiting independent verification |

Normative files synchronized in place: `five-axis-state.md`, registry, Master Architecture, ADR-0001/0004/0005, control manifest, game concept, branch map, systems index and change-impact report. ADR-0002/0003 remain valid; no ADR was superseded. Solo mode skipped the Technical Director gate. A fresh independent eleventh review remains required before `SYS-ENDING`.
