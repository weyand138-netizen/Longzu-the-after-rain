# 五轴局内状态系统：第十一次独立复审

> **Review date**: 2026-07-26  
> **Reviewed revision**: Eleventh  
> **Reviewed file**: `design/gdd/five-axis-state.md`  
> **Prior verdict**: NEEDS REVISION — Tenth Re-review  
> **Verdict**: NEEDS REVISION  
> **Rough scope signal**: XL（聚焦文档修订量约 S–M）  
> **Review mode**: Full independent review, read-only

## Review Panel

- Game Designer / Narrative Director
- Systems Designer / Ren’Py Implementation Reviewer
- QA Lead
- Creative Director

## Completeness

8/8 必备章节齐全。活动 AC 共 82 项：COMP 24、ENGINE 11、DOWNSTREAM 10、CONTENT 28、ACHIEVE 4、UX 5。`STATE-CONTENT-020` 继续保持 reserved/deprecated。

两个 canonical cause golden vector 已由独立实现复算并通过：

- `fallback_v1` → `f57b3ae4a102befa05f8e5a51b1be688338ad1daf3708963d676cb12c7ecac8b`
- `axis_match_v1` → `640f8e05affdf6805530156ad232d2849830f9197c872ad010421db05439f9be`

Pinned SDK interpreter 的 CPython 3.12.7、`cpython-312` cache tag 与 SHA-256 也已复核一致。Golden vector 和 runtime pin 不是本次拒绝原因。

## Tenth-review Regression

| 第十审 blocker | 第十一次复审结果 |
|---|---|
| Predicate/cause legal domain | **部分关闭**：predicate truth table、order 与 graph closure 已闭合；audit lineage 与每个合法分支的 payload population 未闭合 |
| Canonical cause identity | **部分关闭**：template/runtime 分离、byte grammar、两条 golden vector 已通过；audit identity、具体字段赋值与 collision oracle 仍开放 |
| Structured resolution schema | **部分关闭**：新增 nested schema 与 unresolved causes，但 GDD/registry exact order 冲突，record identity 与 trace 信息不足 |
| Single-pass stage and wrapper | **部分关闭**：阶段文字顺序已自洽；冻结 trace、wrapper 禁令与可观测 instrumentation 尚未闭合 |
| Trusted-leaf purity closure | **部分关闭**：显式 target 与 runtime pin 已加入；implicit operations 和 runtime record constructors 未纳入唯一分类 |
| Later causal payoff | **未关闭**：严格较晚与 per-prehistory 方向已加入，但覆盖全集、量词、因果绑定与即时执行证据仍不足 |

Duplicate acquire / absent consume 的 route-fact-fold oracle 继续保持关闭。

## Dependency Graph

| 依赖 | GDD 状态 | 本次判断 |
|---|---|---|
| Ren’Py store/rollback | 引擎依赖已固定 | 存在 |
| `SYS-CHOICE` | 独立 GDD 未创建 | Provisional |
| `SYS-SAVE` | 独立 GDD 未创建 | Provisional |
| `SYS-ENDING` | 独立 GDD 未创建 | 当前不得开始 |
| `SYS-NARRATIVE` | 独立 GDD 未创建 | Provisional |
| `SYS-JOURNAL` | 独立 GDD 未创建 | Provisional |
| `SYS-TENSION` | 独立 GDD 未创建 | Optional / Provisional |
| `SYS-TEST` | 独立 GDD 未创建 | 联合验证边界已声明 |
| `SYS-PERSIST` | 独立 GDD 未创建 | ADR-0002 已确认边界 |
| `SYS-ACHIEVE` | 独立 GDD 未创建 | Provisional downstream |
| `SYS-ACCESS` | 独立 GDD 未创建，且未列入 Dependencies 表 | 应补齐接口所有权 |
| Imported Python modules | 架构与 ADR 已定义 | 存在 |

缺失的 provisional GDD 不单独构成本次拒绝理由，但不得据此创建最终下游 stories。

## Required Before Implementation

### 1. Cause lineage、payload population 与 collision proof 必须完整闭合

`ending_cause_template_record` 规定每个 revoke token 一个 audit template，但 record 没有 `token_id` 或其他 token-binding 字段；其唯一键是 `ending_id + clause_id + polarity`，而 audit 的 `clause_id` 固定为 `None`、polarity 固定为 `audit`。结果是同一 ending 最多只能容纳一个 audit template，且单一 token template 不能自然产生六个可能 selected ending 的 runtime lineage。

此外，truth table 只冻结了字段允许类型，没有为每个 source/comparator/result/polarity 组合冻结：

- `source_reference_ids`
- `observed_value`
- `required_value`
- anchor bucket/index

例如 `axis_value at_least 2`、实际轴值为 3 时，正文未决定使用前三次、最早两次或其他 contributor，合法实现会产生不同 runtime cause ID。

`unequal-payload SHA collision` AC 也没有可执行 fixture：真实 full SHA-256 collision 不可构造，而 production hash leaf 又不可替换。应定义纯 build-layer collision checker，或明确隔离于 production manifest 的 test-only digest seam。

必须补充 audit token/ending identity、完整 payload-population matrix、超额 axis contributor rule，以及不污染 resolver 的 collision fixture。

证据：`design/gdd/five-axis-state.md:224–276`、`:765`；`design/registry/entities.yaml:570–647`。

### 2. Exact record、frozen trace 与 wrapper observability 必须成为单一 schema

GDD 的 exact `EndingResolutionRecord` 顺序是：

`ending_id → 四组 ID tuples → unresolved/matched causes → trace → exclusions → display`

Registry 则把 `unresolved_token_causes` 插在其余 fact IDs 之前，并把 trace 放在 matched causes 之前。两个 canonical field order 不能同时成立。

四类 NamedTuple 也没有冻结 concrete `(module, qualname, field order)`，因此 exact-type 检查和 trusted descriptor expansion 无法唯一生成。

单遍流程仍有两处不可执行：

- `ClauseEvaluationTraceEntry` 只保存 bool 结果和 contributing clause IDs，不含 actual observed/required values、source references、history anchors 或 qualification contributor trace；但 cause stage 被要求“只消费 frozen trace”，信息不足以构造 cause。
- Wrapper 必须调用 canonical resolver 一次，却又被禁止“直接或间接”调用 validator/fold/predicate/cause helpers；canonical call 必然间接调用它们，字面合同自相矛盾。

Stage counters、clause counters、wrapper field-read spy 也缺 exact test-only schema/harness。应同步唯一 record order；冻结 record identity；让 frozen artifact 包含 cause-ready facts，或明确 cause extraction 可读取哪些已冻结输入；把 wrapper 禁令改为“除唯一 canonical call 外不自行调用”；并定义 production manifest 外的 observation harness。

证据：`design/gdd/five-axis-state.md:280–290`、`:729–737`；`design/registry/entities.yaml:665–735`。

### 3. Purity allowlist 必须覆盖 implicit operations 与 runtime constructors

Trusted-leaf v1 已列出显式 built-in/native targets，但没有说明 membership、subscript、comparison、arithmetic、bytes/tuple concatenation 与其他 bytecode-triggered special methods是否属于 dependency closure。两个 static analyzer 可据此得出相反结论。

同时，allowlist 只允许 NamedTuple field descriptor reads，没有允许 runtime record construction 所需的 concrete class constructor、generated `__new__`、`tuple.__new__` / `type.__call__` 或等价边界；按当前 fail-closed 规则，resolver 构造自己的返回 record 也可能失败。

必须冻结 implicit-op 审计规则或 opcode + exact operand-type/descriptor allowlist，加入 exact record constructors 与 exception construction policy，并提供 custom-protocol/native-dispatch mutants。

证据：`design/gdd/five-axis-state.md:388–401`、`:737`；`design/registry/entities.yaml:742–779`。

### 4. Choice feedback/payoff proof 必须覆盖真实玩家路径和真实因果

项目硬规则覆盖所有 player-facing narrative choices，但当前正文与 AC 只覆盖未定义的“重大选择”。没有 taxonomy 或跨脚本扫描证明其他玩家选项不存在，内容方仍可通过改称“非重大”绕过。

当前量词为：

- 每个 reachable prehistory 至少存在一条 payoff continuation；
- 每个 declared payoff 至少被某个 witness 覆盖。

这允许玩家实际进入另一条从不回收的 legal continuation。Registry / ADR 又使用“每个 prehistory 与每个 payoff”的更强措辞，跨文档不一致。

Reachability 也不等于 causality：witness 只证明 later event 发生，没有证明 event 读取、引用或因原 `choice_id` 发生实质变化；所有 choices 可共同指向一个无关结局事件。`prehistory_id` 没有 canonical identity，`immediate_reaction_id` 也只有登记而没有 choice-node 实际执行证据。

必须冻结：

- player-facing choice coverage universe 与允许排除项；
- canonical prehistory identity；
- payoff applicability 量词；
- 对所有 applicable legal continuations 的覆盖；
- choice ↔ reaction/payoff event 双向绑定或等价反事实证据；
- immediate reaction 在选择后、任何后续分支或离开前实际执行的 oracle。

证据：`CLAUDE.md` 产品规则 6；`design/gdd/five-axis-state.md:305–326`、`:754`；`design/registry/entities.yaml:64–81`。

### 5. Resolver complexity 必须包含全部规范排序成本

文档锁定为 `O(H + P + Q + C + K log K)`，并声称 `K log K` 只来自 cause 排序；但同一合同还要求：

- multi-source references 排序；
- event/resource/qualification IDs 按 UTF-8 bytes 排序；
- matched/unresolved/exclusion/display causes 排序。

若这些集合不是按总序线性生成，fact/source 排序会产生额外的 `P log P`、`Q log Q` 或相应输出规模项。额外空间表达也漏掉 qualification contributor trace 的 `O(Q)`。

必须定义线性有序生成算法，或把所有实际排序和输出规模纳入时间/空间公式，并同步 GDD、architecture 与 ADR。

证据：`design/gdd/five-axis-state.md:248`、`:267`、`:276`、`:284`、`:802`。

## Recommended Revisions

1. 在 `SYS-ENDING` / `SYS-NARRATIVE` 正式 story 或内容锁定前完成逐 ending terminal-class forecast。当前 baseline + 五轴补救见证就可能占满 `rain_stops` 的 1–6 目标预算。
2. 为 history-first display cause 增加叙事显著性试玩门槛，避免早期低显著原因挤掉决定性牺牲、人物损失或 unresolved harm。
3. 将过度聚合的 `STATE-CONTENT-019` 拆分为 predicate、canonical identity、record immutability 与 single-pass instrumentation AC。
4. 补齐 `SYS-ACCESS` 到 Dependencies 与接口所有权表。

## Specialist Disagreements

- **Payoff witness**：Systems Reviewer 认为 per-choice/per-prehistory 严格较晚 witness 已关闭第十审 blocker；Game/Narrative 与 QA 认为存在量词、coverage universe 和 causal binding 漏洞。Creative Director 同意后者，列入 blocker 4。
- **Single-pass / purity**：Game/Narrative 从玩家体验角度认为主方向已关闭；Systems/QA 认为 frozen trace、wrapper 文义与 implicit-op/constructor closure 仍无法执行。Creative Director 同意 Systems/QA。
- **Predicate/cause legal domain**：Game/Narrative 认为 truth table 已关闭；Systems/QA 认为 audit cause 与 payload population 仍属于该合法域的未闭部分。Creative Director 将其与 canonical identity 合并为 blocker 1。

## Nice-to-Have

- 为 schema 冻结后的完整 resolution record 增加人类可读 worked example。
- 将语义性 AC 的人工复核证据类型显式登记，而不是混入“静态验证与路径枚举”。

## Senior Verdict

第十一次修订在 predicate table、canonical bytes、golden vectors、阶段主线和 runtime pin 上取得了实质进展；核心幻想、rollback/save 边界、反证修复伦理与 duplicate-resource oracle 保持稳定。

但剩余缺口仍位于 identity、exact schema、single-pass information flow、purity classifier、玩家实际因果回收与渐进复杂度边界。多个实现者仍可能写出互不兼容、却都声称符合文档的 resolver；内容验证也仍能让未被原 choice 触发的通用 later event 伪装成 payoff。

### Verdict: NEEDS REVISION

不得开始 `SYS-ENDING`。完成上述五个聚焦修订包后，运行新的独立复审。本记录不是第十二次修订，也不构成自我批准。

## Twelfth Revision Remediation Record

> Authoring appendix only. The historical `NEEDS REVISION` verdict remains unchanged until a fresh independent review.

| Eleventh-review blocker | Twelfth-revision action | Status |
|---|---|---|
| Cause lineage / payload / collision | Disjoint clause/audit keys, token+selected-ending audit lineage, exhaustive population matrix, earliest-axis rule, isolated digest-bijection checker | Remediated; awaiting verification |
| Exact records / frozen trace / wrapper | Unique concrete identities and field order, cause-ready frozen artifact, corrected wrapper scope, exact test-only AST observation record | Remediated; awaiting verification |
| Purity implicit operations / constructors | Policy v2 opcode+operand table, record/exception constructors, protocol/native mutants | Remediated; awaiting verification |
| All-choice real reaction/payoff | Complete choice-surface taxonomy, canonical prehistory/continuation IDs, all-continuation coverage, bidirectional reaction/payoff causality | Remediated; awaiting verification |
| Complete complexity | Added canonical-byte, source/fact/cause sorting and qualification contributor time/space terms | Remediated; awaiting verification |

Normative synchronization covered the GDD, registry, Master Architecture, ADR-0001/0004/0005, control manifest, game concept, branch map, systems index and change-impact report. No ADR was superseded. A fresh independent twelfth review is still required before `SYS-ENDING`.
