# 五轴局内状态系统：第十二次独立复审

> **Review date**: 2026-07-27  
> **Reviewed revision**: Twelfth  
> **Reviewed file**: `design/gdd/five-axis-state.md`  
> **Prior verdict**: NEEDS REVISION — Eleventh Re-review  
> **Verdict**: NEEDS REVISION  
> **Rough scope signal**: XL（聚焦文档修订量约 M）  
> **Review mode**: Full independent review, read-only

## Review Panel

- Game Designer / Narrative Director
- Systems Designer / Ren’Py Implementation Reviewer
- QA Lead
- Senior Creative Director

## Completeness

8/8 必备章节齐全。活动 AC 共 87 项：COMP 24、ENGINE 11、DOWNSTREAM 10、CONTENT 33、ACHIEVE 4、UX 5。`STATE-CONTENT-020` 保持 reserved/deprecated，未发现活动定义或引用。

注册表含 69 个唯一 SYS-STATE contract facts；39 份 Markdown 的本地链接检查为 0 个断链。两个 canonical cause golden vector 已独立复算通过：

- `fallback_v1` → `f57b3ae4a102befa05f8e5a51b1be688338ad1daf3708963d676cb12c7ecac8b`
- `axis_match_v1` → `640f8e05affdf6805530156ad232d2849830f9197c872ad010421db05439f9be`

现有纯逻辑测试 6/6 通过，但只验证当前旧式 resolver 行为，不构成新增 frozen-cause、全 choice 因果或复杂度 AC 的通过证据。

## Eleventh-review Regression

| 第十一审 blocker | 第十二次复审结果 |
|---|---|
| Cause lineage、payload population 与 collision proof | **关闭**：clause/audit lineage key 已分离，payload matrix、axis earliest-contributor 与隔离 digest-bijection checker 已闭合 |
| Exact records、frozen trace 与 wrapper observability | **部分关闭**：concrete record identity、唯一 field order、wrapper scope 与 AST observation 已闭合；frozen artifact 仍缺 cause identity/source fields |
| Purity implicit operations 与 constructors | **关闭**：policy v2 覆盖 opcode/operand、六个 record constructors、exception construction 与 protocol/native mutants |
| All-choice reaction/payoff proof | **部分关闭**：coverage universe、全 continuation 量词、即时执行与因果 proof kind 已定义；history ownership 与 exact joins/cardinality 仍开放 |
| Complete resolver complexity | **部分关闭**：B/R/F/K 排序项已进入公式；用于吸收字符串比较成本的全局 stable-ID byte cap 尚未成为契约 |

`SYS-ACCESS` ownership 已同步到交互、Dependencies、注册表与架构文件。

## Dependency Graph

| 依赖 | GDD 状态 | 本次判断 |
|---|---|---|
| Ren’Py store/rollback | 引擎依赖已固定 | 存在 |
| `SYS-CHOICE` | 独立 GDD 未创建 | Provisional |
| `SYS-SAVE` | 独立 GDD 未创建 | Provisional |
| `SYS-ENDING` | 独立 GDD 未创建 | 当前不得开始 |
| `SYS-NARRATIVE` | 独立 GDD 未创建 | Provisional |
| `SYS-JOURNAL` | 独立 GDD 未创建 | Provisional |
| `SYS-ACCESS` | 独立 GDD 未创建 | Provisional，所有权已声明 |
| `SYS-TENSION` | 独立 GDD 未创建 | Optional / Provisional |
| `SYS-TEST` | 独立 GDD 未创建 | 联合验证边界已声明 |
| `SYS-PERSIST` | 独立 GDD 未创建 | ADR-0002 已确认边界 |
| Imported Python modules | 架构与 ADR 已定义 | 存在 |

缺失的 provisional GDD 不单独构成本次拒绝理由，但不得据此创建最终下游 stories。

## Required Before Implementation

### 1. `FrozenResolutionEvaluation` 必须成为真正的 cause-ready artifact

`EndingCauseRecord` 需要 `cause_template_id`、`source_kind`、`polarity` 与 `cause_kind`，但 `ClauseEvaluationTraceEntry` 只冻结 clause identity/results、contributors、source references、values 与 anchors。Cause extraction 同时被规定只能读取 `FrozenResolutionEvaluation`，不得读取 predicate/template catalog。

因此 cause stage 无法唯一选择 match/failure template，也无法区分 `absent` 失败产生的 `exclusion_evidence` 与普通 `evidence_shortfall`。`UnresolvedAuditFact` 同样没有冻结 `source_kind`。

必须把完整 cause identity/source fields 冻结进 atomic artifact，或新增唯一 exact `FrozenClauseCauseFact`；随后同步 GDD、registry、ADR、`STATE-DOWNSTREAM-008` 与 `STATE-CONTENT-032`。

证据：`design/gdd/five-axis-state.md:250`、`:303–310`、`:804`、`:846`；`design/registry/entities.yaml:791–866`。

### 2. `narrative_only` 的 rollback/save/history 权威模型必须唯一

全部 player-facing choices 包含 `narrative_only`，但正文只说它“不写五轴/token”，注册表则声明 `narrative_only_state_effect: forbidden`。与此同时 canonical prehistory、`history_guard`、route projection 与 payoff causality 依赖 ordered history。

当前没有规定 narrative-only choice 是否进入 `semantic_state.choice_history`、由谁提交、何时 commit，以及如何随 rollback/save/load 恢复。合法实现可以选择记录或不记录，从而产生不同的 prehistory hash、guard 结果与 resolver facts。

必须冻结唯一 owner、exact history schema、commit 时点、rollback/save/load 语义与 history-commit AC；可以由 SYS-STATE 或下游系统拥有，但不得留到 SYS-ENDING 后再反向改变已封板状态模型。

证据：`design/gdd/five-axis-state.md:55–64`、`:69–83`、`:337–379`、`:381–389`、`:593`；`design/registry/entities.yaml:64–83`。

### 3. Choice → reaction/payoff 证明链必须具有 exact join、cardinality 与 nullability

当前 choice record、reaction binding、payoff witness、payoff binding 与 event metadata 重复保存 choice/reaction/payoff/event IDs，但没有冻结所有外键的逐字段相等、唯一基数和反向 metadata concrete schema。

文档仍允许：

- choice 声明 reaction A，实际 binding 执行 reaction B；
- declared payoff 与 witness 使用不同 payoff；
- witness 与 causal binding 的 `choice_id`、`payoff_id` 或 `payoff_event_id` 不一致；
- 同一 choice 存在零个或多个 reaction binding；
- `history_guard` 与 `counterfactual_outcome` 的 optional references 同时为空或同时非空。

必须加入 exact join table、唯一键/外键基数、event 反向 metadata schema，以及 proof-kind 的互斥 nullability truth table，并让 AC 使用错配 fixture 固定失败。

证据：`design/gdd/five-axis-state.md:337–379`、`:823`、`:847–848`；`design/registry/entities.yaml:64–174`。

### 4. 复杂度公式的 stable-ID 比较成本前提必须成为契约

性能段声称所有 stable IDs 最长 64 ASCII bytes，因此可把字符串比较成本吸收为常数；但目前只有 `choice_id` 明确具有 `1–64` 限制。参与 source/fact 排序的 token、event、resource、qualification、clause、template 与 outcome IDs 没有同等 byte cap。

因此 `R log R` 与 `F log F` 仍没有完整的字符比较成本边界。必须选择其一：

- 建立覆盖全部参与比较 ID 的全局 UTF-8 byte grammar/cap，并增加 build validator 与 boundary mutants；或
- 把最大比较长度或总 comparison bytes 显式加入时间复杂度。

同时明确 `R` 是否包含全部 qualification contributor references，避免遗漏额外排序项。

证据：`design/gdd/five-axis-state.md:73`、`:261`、`:876`；`design/registry/entities.yaml:1065–1085`。

## Recommended Revisions

1. 在 `SYS-ENDING` 内容锁定前完成逐 ending terminal-cause-class forecast。
2. 为 history-first `display_cause_ids` 增加叙事显著性试玩门槛，避免低显著原因挤掉决定性牺牲、人物损失或 unresolved harm。
3. 为 `STATE-COMP-016`、`STATE-DOWNSTREAM-001` 等 “only / no hidden dependency” AC 补充 `STATIC + BRANCH` 证据。

## Specialist Disagreements

三位专业审查者对最终 verdict 无实质分歧。唯一需要高级裁决的是 `narrative_only` history ownership 是否可降级为下游事项；Senior Creative Director 判定它是 SYS-STATE 封板阻断，因为它可能反向改变 rollback/save schema 与跨系统 ownership。

## Senior Verdict

第十二次修订已关闭 audit lineage、payload population、collision checker、purity v2 和 SYS-ACCESS ownership，并修正了全 continuation 的 payoff 量词。核心幻想、角色表达、rollback 边界和非商业同人规则保持一致。

但 frozen cause stage 仍缺构造完整 cause 的信息，全 choice proof 尚无唯一 history authority 与 exact relational joins，复杂度又依赖未建立的全局 ID byte cap。多个实现者仍可产生不同的 resolution record、prehistory identity、binding verdict 或复杂度结论。

### Verdict: NEEDS REVISION

不得封板 `SYS-STATE`，不得开始 `SYS-ENDING`。关闭上述四项聚焦阻断后，形成第十三次修订并运行新的独立复审。

## Final Targeted Closure

> **Closure date**: 2026-07-27  
> **Authority**: User-directed constrained closure  
> **Validation**: One targeted four-item validation, **4/4 PASS**  
> **Final project disposition**: **SYS-STATE Approved**

1. `FrozenResolutionEvaluation` 已通过 atomic trace 的 template/polarity/kind/source fields 与 audit fact 的 `audit`/`unresolved_counterevidence`/`unresolved_token` fields 成为真正 cause-ready artifact。
2. 所有 player-facing narrative choices 均在确认后、reaction 前由 `SYS-STATE.apply_choice` 提交；`narrative_only` 使用 empty `RunMap`，只追加 history，并与五轴共用 rollback/save/load envelope。
3. Choice→reaction/payoff exact joins、cardinality、proof-kind nullability 与 reverse event metadata 已转交 `SYS-CHOICE`/`SYS-NARRATIVE`，保留为不计入 `SYS-STATE` 批准的 provisional 下游门槛。
4. 复杂度合同已修正为包含最大 UTF-8 stable-ID 比较长度 `L`，且 `R` 明确包含 qualification contributor references。

本 closure 不执行第十三次完整发散审查，也不接受新的 blocker 类别。上文只读审查 verdict 保留为历史记录；本节是其四项定点处置后的最终项目状态。
