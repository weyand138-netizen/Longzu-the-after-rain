# 五轴局内状态系统：第四次独立复审

> **Date**: 2026-07-24  
> **Reviewed file**: `design/gdd/five-axis-state.md`  
> **Prior verdict**: MAJOR REVISION NEEDED  
> **Verdict**: NEEDS REVISION  
> **Rough scope signal**: XL（剩余文档修订约 M）  
> **Review mode**: Full independent review

## Review Panel

- Game Designer
- Systems Designer
- QA Lead
- Creative Director

## Completeness

8/8 required sections were present: Overview, Player Fantasy, Detailed Rules, Formulas, Edge Cases, Dependencies, Tuning Knobs, and Acceptance Criteria.

第四版已经实质解决 `grant` 绕过、一次 repair 清除多次违背、无限 qualification、reaction/payoff ID 空洞价值、旧存档 sentinel，以及 RunMap/helper/resolver/独立机会等第三审问题。架构不再需要推翻，剩余工作为四组实施前契约收口。

## Implementation-blocking Findings

### 1. Snapshot copy boundary conflict

ADR-0004 允许 imported helper 直接接收 live `RunMap`/`RunList`，而 ADR-0005 规定 imported Python 只能接收 detached built-ins。必须统一为一个不会把 rollback-owned mutable object 传出 `.rpy` 的可实现边界。

### 2. Field-level validation order is incomplete

live validator、snapshot validator 与 resolver 遇到复合非法输入时，尚不能保证唯一首个 `TypeError`/`ValueError`。`apply_choice` 与 `current_ending_snapshot` 是否校验 active sentinel 也未闭合。

### 3. Strict-dominance partial order is ambiguous

必须明确：

- 稀疏资源成本按 A/B key 并集比较，缺键视为 0；
- 每个对齐可达前缀均满足 `U_B ⊆ U_A`；
- 互不包含 token 集默认不可比较；
- repair/revoke 和 token 数量不能替代集合关系；
- strict dominance 至少包含一个严格改善分量。

### 4. Repair and irreversible token contract is incomplete

repair domain 必须与目标 token domain 一致，并在每条到达路径证明目标在 repair 前仍 unresolved。每个 token 必须显式分类为 `repairable` 或经审核的 `irreversible`；不可逆 token 需要严重性、时序与结局回收证据，不能成为第七日最后一道判题。

## Recommended Revisions

- 审查成就目录，避免正向行为成就成为玩家可见的五轴代理清单。
- 悲剧结局回收决定性的 unresolved token 或具体缺失因果。
- 将 ADR-0001 的 resolver 复杂度从 constant-time 改为 `O(history length)`。
- Overview 补列 ADR-0005。
- 明确 `Active → Ended` 的所有权与精确触发点。
- 阻断式读档流程覆盖 rollback、快捷存读档、skip、history/screen return 等旁路。

## Fifth Revision Decisions

### Immutable import transfer

`.rpy` 侧验证 active sentinel 与 live state，只提取 schema/axis exact ints 和 history exact-string tuple。Imported `build_detached_ending_snapshot` 只接收这些 immutable built-ins，并在 imported module 内创建 exact dict/list snapshot。Live `RunMap`/`RunList` 不跨边界。

### Two-pass validation

Active APIs 先完成整个可达对象图的 exact-type sweep，再执行 value/shape sweep；type defect 总是先产生 `TypeError`。Resolver 固定阶段为 type → value/shape → catalog → token schema/reference → fold → ending priority。`apply_choice` 与 `current_ending_snapshot` 都校验 active sentinel；`after_load` 保留兼容性分类例外。

### Unique dominance order

稀疏成本按 key 并集、缺键为 0。对 A 的每条 continuation，以 B 替换该节点选项后，每个对齐前缀必须满足 `U_B(k) ⊆ U_A(k)`。互不包含集合不可比较，数量不参与排序，并要求至少一个严格改善。

### Explicit token lifecycle

每个 token 显式声明 `repairable` 或 `irreversible`。Repair 必须同 domain、目标仍 unresolved 且后果已可观察。Irreversible token 需要独立审核、严重性证据、至少两个后续重大选择节点、每个可达结局的 token-specific payoff，并禁止出现在 ending commit。

### Player-facing safeguards

成就目录改为复合场景回声条件，禁止形成五轴代理清单，并要求零增量与非最佳结局路径成就。悲剧 witness path 必须登记 decisive token/cause 与具体回收。`SYS-ENDING` 独占 entering ending label 时的 `Active → Ended` 转换。

## Files Revised

- `design/gdd/five-axis-state.md`
- `design/gdd/game-concept.md`
- `design/gdd/systems-index.md`
- `design/narrative/branch-map.md`
- `design/narrative/achievement-catalog.md`
- `design/registry/entities.yaml`
- `docs/architecture/architecture.md`
- `docs/architecture/adr-0001-deterministic-ending-resolution.md`
- `docs/architecture/adr-0002-rollback-and-persistence-boundary.md`
- `docs/architecture/adr-0004-semantic-ending-snapshot-and-state-envelope.md`
- `docs/architecture/adr-0005-counterevidence-ledger-and-detectable-state-initialization.md`
- `docs/architecture/control-manifest.md`
- `production/session-state/active.md`

## Remediation Status

四项实施前阻断与六项建议已经进入第五次同步修订。原 **NEEDS REVISION** 结论继续有效，直至新的独立复审验证修改后的完整文档。本记录不是自我批准。

## Remaining Maturity Gaps

- Production `state.rpy`、`ending_rules.py`、achievement catalog 仍实现早期原型契约。
- 完整 token、repair、irreversible、semantic value 与 ending payoff 目录尚待 `SYS-ENDING` / `SYS-NARRATIVE` GDD。
- 新 validation pipeline、snapshot builder、blocking load flow 和 static dominance validator 尚未实现。
- 完整七日图、六结局 witness path 与悲剧 decisive-cause evidence 尚未制作。

## Superseded by Fifth Review

第五次独立复审确认第四审技术主线已稳定，但发现五组最终确定性与内容契约缺口。见 [five-axis-state-fifth-review-2026-07-24.md](five-axis-state-fifth-review-2026-07-24.md)。本文件仅保留第四次复审的历史结论。
