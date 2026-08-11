# 五轴局内状态系统：第八次独立复审

> **Review date**: 2026-07-24  
> **Ninth revision date**: 2026-07-26  
> **Reviewed file**: `design/gdd/five-axis-state.md`  
> **Prior verdict**: NEEDS REVISION  
> **Verdict**: NEEDS REVISION  
> **Rough scope signal**: XL（剩余文档修订量 S–M）  
> **Review mode**: Full independent review

## Numbering Note

独立审查任务中的最终正文标题为“第八次设计复审”。用户在 2026-07-26 将后续周期称为“根据第九次审查结果进行第九次修订”。本记录保留原始审查编号，并把本轮写作明确标为第九次修订；不伪造第二份未落盘的审查结论。

## Review Panel

- Game Designer
- Systems Designer
- QA Lead
- Creative Director

## Regression Result

第七审的两个阻塞只部分关闭：

- Private builder 已有单一生产 callsite allowlist，但静态扫描闭包未覆盖 symbol escape、反射、生产到测试依赖与 CFG domination。
- Component AC 已有 24/24 evidence map，但 `STATE-COMP-003/007/017/022` 的证据宿主无法证明对应结论。

## Implementation-blocking Findings

### 1. Route qualification introduced an external input

Ending snapshot 只含 schema、axes 与 ordered history，但资格规则又读取 completed event/resource state。必须保持 snapshot 为唯一动态状态输入：用 frozen choice projection catalog 从 history 重建 event completion/resource possession，并证明不同外部 live state 不改变资格或结局。

### 2. Repair build-time/runtime errors were mixed

Frozen catalog 已禁止 unknown target、wrong domain/mode、irreversible target 与 invalid reference，正常 resolver 不应再拥有这些运行时分支。Runtime fold 只防御 target 尚未产生或已经解决。

### 3. Component evidence map used the wrong hosts

- `STATE-COMP-003` 的一次 replacement 需要 assignment instrumentation。
- `STATE-COMP-007` 测试 Ren’Py `RunMap` helper，必须使用 engine-hosted test。
- `STATE-COMP-017` 的 shared primitives 需要 static callgraph。
- `STATE-COMP-022` 的 private/non-export claim 必须关联 static evidence。
- Evidence taxonomy 声称“四类”但实际有五类，且连字符/下划线枚举不一致。

### 4. Private builder scan did not close all references

生产 manifest 必须覆盖完整 `game/**/*.py`，并处理 assignment、pass/return、closure/container storage、wrapper export、reflection/dynamic lookup、production-to-test dependency，以及 active validation 对唯一 callsite 的 CFG dominator 关系。无法解析的形式必须构建失败。

## Recommended Revisions

- 以固定 predicate-clause 目录做完整 cause extraction，禁止短路决定 cause 集。
- 统一 history-first cause ordering 与 stable-ID outcome ordering。
- 明确 `rain_stops` 恰由五轴全 3 且 unresolved token 为空成立。
- `display_cause_ids` 至少保留一个当前 ending 的 matched cause。
- 为 terminal-cause classes 设置内容预算，但不得合并不同人物归宿、代价承担者或悲剧闭合。

## Ninth Revision Decisions

### Closed route input boundary

每个正式 choice 都有 immutable `route_fact_projection_record`，映射 completed events 和 resource acquire/consume effects。Resolver 只从 snapshot history 与 frozen projection index 重建 facts/qualifications；外部 store、persistent、event manager、inventory 和 chapter flags 的读取次数必须为零。

### Separated repair lifecycle

Unknown target、wrong domain/mode、irreversible target 与 invalid reference 只属于 catalog build validation。Runtime fold 只处理 target 未产生或已解决；公式示例改为 revoke 后两个不同 repair choices 定向同一 token，第二个固定失败。

### Corrected component evidence

Canonical machine IDs 统一为 `UT_ENGINE`、`UT_PURE`、`INSTR`、`STATIC`、`BRANCH`。Atomic replacement、Ren’Py helper、shared primitives 与 private export status 分别绑定到能够实际观察结论的 evidence host。

### Closed builder reference graph

Source scan 覆盖 `game/**/*.rpy` 与 `game/**/*.py`，建立完整 reference/escape/callgraph/CFG 闭包。唯一生产调用仍是 `game/10_state.rpy::current_ending_snapshot`，且 active validation 必须支配全部到达路径。

### Deterministic causality and content budget

Ending predicate clauses 按固定 priority/order 全量求值；matched/exclusion/unresolved causes 使用 history-first ordering，outcome lists 使用 stable-ID ordering。`rain_stops` 无 qualification gate。每个 display 至少有一个 matched anchor。每 ending 的 terminal-cause class 目标为 1–6、7–12 预警、超过 12 构建失败，且禁止为满足预算合并不同 signature。

## Files Revised

- `design/gdd/five-axis-state.md`
- `design/gdd/game-concept.md`
- `design/gdd/systems-index.md`
- `design/gdd/reviews/five-axis-state-seventh-review-2026-07-24.md`
- `design/gdd/reviews/five-axis-state-eighth-review-2026-07-24.md`
- `design/narrative/branch-map.md`
- `design/registry/entities.yaml`
- `docs/architecture/architecture.md`
- `docs/architecture/adr-0001-deterministic-ending-resolution.md`
- `docs/architecture/adr-0004-semantic-ending-snapshot-and-state-envelope.md`
- `docs/architecture/adr-0005-counterevidence-ledger-and-detectable-state-initialization.md`
- `docs/architecture/control-manifest.md`
- `production/session-state/active.md`

## Remediation Status

四组 implementation blockers 与五项 recommendations 已纳入第九次同步修订。第八次独立审查的 **NEEDS REVISION** 仍是最新独立裁决；本修订记录不是自我批准。必须由新的独立任务执行下一次窄范围复审，之后才能开始 `SYS-ENDING`。

## Remaining Maturity Gaps

- Production state/resolver code 仍是旧 prototype contract。
- Projection catalog、complete cause extraction、static escape/CFG scanner 与 evidence collectors 只完成规格，尚未实现。
- 下游 records 仍等待 `SYS-ENDING`、`SYS-NARRATIVE` 与 `SYS-TEST` GDD。
- `docs/registry/architecture.yaml` 不存在；本轮未在缺少明确批准的情况下创建架构注册表。
