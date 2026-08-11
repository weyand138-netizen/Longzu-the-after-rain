# 五轴局内状态系统：第九次独立复审

> **Review date**: 2026-07-26  
> **Tenth revision date**: 2026-07-26  
> **Reviewed file**: `design/gdd/five-axis-state.md`  
> **Prior verdict**: NEEDS REVISION  
> **Verdict**: NEEDS REVISION  
> **Rough scope signal**: XL（本轮文档修订量 S–M）  
> **Review mode**: Full independent review, read-only

## Review Panel

- Game Designer
- Systems Designer
- QA Lead
- Creative Director

## Regression Result

第八审四组阻断均已关闭：

- Private builder 的 production manifest、symbol escape、callgraph 与 CFG domination 已闭合。
- `STATE-COMP-000`–`023` 的证据映射为 24/24，关键 evidence host 已修正。
- Repair catalog build-time 错误与 runtime history-order 错误已分离。
- Route qualification 已改为只从 snapshot history 与冻结 projection catalog 派生。

文档完整度为 8/8。复审确认 82 个唯一活动 AC：COMP 24、ENGINE 11、DOWNSTREAM 10、CONTENT 28、ACHIEVE 4、UX 5。

## Implementation-blocking Findings

### 1. Ending cause-resolution 仍不能导出唯一实现

现有 clause 目录未封闭 `clause_kind`、operand、source kind、AND/OR/group 求值、实际路径 cause source、多来源 anchor、无 history cause 排序桶与 total-order key。`unsent_postcard` 无条件 fallback 也没有合法 matched cause 生成规则。运行流程要求 complete cause extraction，但 `resolve_ending(snapshot) -> str` 只暴露 ending ID。

### 2. Duplicate resource acquire 没有唯一 runtime 结果

正式路径构建期会拒绝 duplicate acquire，但 exact-type、ID 唯一、catalog-covered 的结构合法非法 history 在 runtime 仍可能被实现为 set no-op 或错误。必须固定 route-fact-fold `ValueError`，并证明后续阶段零调用。

### 3. `STATE-DOWNSTREAM-010` 缺少 static purity closure

动态 instrumentation 只能证明已执行 fixture，不能排除未执行分支、cache、传递 helper、alias 或 reflection 读取外部状态。必须增加 production manifest、完整传递 callgraph、禁止依赖分类、branch coverage 与精确违规位置证据。

## Non-blocking Recommendations

- 在正式内容进入 `SYS-ENDING` 前预测每个 ending 的 terminal class 数量。
- 为保留的 CONTENT 编号 `020` 增加 reserved/deprecated 注记。
- 更新旧 ending architecture flow，加入 route-fact、qualification 与 cause extraction。
- 将 resolver 复杂度明确为 `O(history + projected effects + evaluated clauses)`。
- 试玩验证 history-first matched anchor 的叙事显著性。

## Tenth Revision Decisions

### Closed executable predicate and cause contract

Predicate catalog 改为封闭的 `group_all`/`group_any`/`atomic` 无环树，冻结 source/comparator 合法组合与完整、无短路 contributor 规则。实际路径 choice/token/event/resource/qualification/shortfall/fallback causes 使用规范 source selection、SHA-256 cause identity、三档 anchor bucket 和固定 total-order key。`unsent_postcard` 只有一个 `constant/always_true` root，并固定生成 `cause_unsent_postcard_fallback`。

### Added structured resolution interface

`resolve_ending_record(snapshot) -> EndingResolutionRecord` 成为唯一 canonical pass，返回 ending ID、folded facts、qualifications、完整 clause trace、matched causes、逐高优先级 exclusions 与 display causes。`resolve_ending` 只返回该 record 的 `.ending_id`，不得复制或再次求值。

### Closed duplicate acquire runtime behavior

Duplicate acquire 与 absent consume 均固定在 route-fact fold 抛 `ValueError`。`STATE-DOWNSTREAM-006/008` 要求 qualification、ending priority、cause extraction 和 record construction 后续计数为零。

### Closed resolver purity proof

`STATE-DOWNSTREAM-010` 固定使用 `UT_PURE + INSTR + STATIC + BRANCH`，扫描 canonical resolver 与兼容 wrapper 的完整传递 production closure，只允许 detached snapshot、局部值、纯标准库值运算与冻结 immutable catalogs；mutable globals、cache、Ren’Py/store/persistent、event/inventory、I/O、time/random/environment、反射与未解析边均构建失败。

### Incorporated recommendations

保留 terminal-class 1–6/7–12/>12 预算；内容编号 `020` 永久 reserved/deprecated；同步 architecture flow；复杂度固定为 `O(history + projected effects + evaluated clauses)`；history-first anchor 的叙事显著性保留为下游试玩门槛。

## Architecture Impact

- ADR-0001: minor in-place amendment，补充 structured resolver、typed predicate tree、path-specific causes、total ordering 与精确复杂度。
- ADR-0004: minor in-place amendment，补充 structured interface 和 purity closure；snapshot/lifecycle 决策不变。
- ADR-0005: minor in-place amendment，补充 cause-generation、duplicate acquire 和 static purity proof。
- ADR-0002: still valid，存档与 rollback 生命周期合同不变。

无 ADR 被 supersede。仓库没有已提交 GDD 基线；本影响判断以第九版文档、会话状态与本次只读复审结论为基准。

## Remediation Status

三项 implementation blocker 与五项建议已经纳入第十次同步修订。第九次独立复审的 **NEEDS REVISION** 仍是最新独立裁决；本记录不是自我批准。必须在新的独立任务中执行第十次复审，批准后才能开始 `SYS-ENDING`。
