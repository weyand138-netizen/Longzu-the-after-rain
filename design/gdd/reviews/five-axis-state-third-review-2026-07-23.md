# 五轴局内状态系统：第三次独立复审

> **Date**: 2026-07-23  
> **Reviewed file**: `design/gdd/five-axis-state.md`  
> **Verdict**: MAJOR REVISION NEEDED  
> **Estimated remediation**: XL  
> **Review mode**: Independent review

## Review Scope

第三次复审检查第二次修订后的反向行为资格、结局快照、旧存档识别、严格劣势验证和验收可执行性。文档结构完整度为 8/8，但以下六项语义或可执行性问题阻止批准。

## Blocking Findings

### 1. 正向 grant 可以绕过 repair

原 `grant → revoke → grant` 折叠会重新得到有效资格，使后续普通正向行为替代对具体伤害的修复。该模型不能保证“后果必须被看见并承担”。

### 2. 多次违背被一次 repair 压平

原三态 domain 折叠无法区分同一 domain 内的多个具体伤害。`revoke_1 → revoke_2 → repair` 会恢复有效状态，未保留尚未修复的第二次违背。

### 3. qualification 可能成为第二套隐藏清单

原规范没有限制 qualification 的数量、粒度、支柱归属或修复方式。内容扩展可能形成五轴之外的另一套隐藏完成列表。

### 4. 严格劣势验证存在空洞通过

若每个选项独有的 reaction/payoff ID 都计为 `unique_value`，任意选项都能声称具有不可替代价值，严格劣势检查失去淘汰劣质选项的能力。

### 5. 旧存档检测不可实现

Ren'Py `default` 可能在 `after_load` 前为缺失变量补入 schema 2 的“有效”默认值。若没有独立 sentinel、显式新游戏初始化和阻断式安全流程，旧存档会被误判为兼容，或在失败后返回不安全的已加载场景。

### 6. 验收契约尚未闭合

以下边界未形成机器可判定契约：empty dict 与 `RunMap` 的区分、`affected_axis_count` 的公共可观察性、detached resolver 的精确容器类型和异常类别，以及“独立补救机会”的机器定义。

## Fourth Revision Decisions

### Event-level counterevidence ledger

- 删除正向 `grant`；普通正向选择和轴封顶都不能清除反证。
- 每个 route-critical 违背产生全局唯一 revoke token。
- repair 必须在具体后果可观察之后，携带已注册成本，并且一次恰好指向一个当前未解决 token。
- 反证 domain 固定为五轴；目录最多 10 个 token、每 domain 最多 2 个、每选择最多一个 effect。
- `revoke_a → revoke_b → repair_a` 的结果必须保留 `{revoke_b}`。

### Audited semantic value

- reaction/payoff ID 只承担追踪作用，不自动构成独特价值。
- 只有实体注册表中的 `kind: semantic_value` 条目及其具体内容证据可阻止严格劣势判定。
- repair 成本使用独立、有限类别的注册 schema，不得以空泛文本声明成本。

### Detectable initialization and blocking load flow

- `semantic_state` 与 `state_schema_sentinel` 的 Ren'Py `default` 均为 `None`。
- 只有显式新游戏初始化器能写入 `"semantic_state:v2"` 和合法 schema 2 状态。
- `after_load` 区分 `SUPPORTED`、`LEGACY_INCOMPATIBLE`、`UNSUPPORTED_VERSION`、`CORRUPT_STATE`。
- 失败分类只能进入阻断式安全流程；用户仅能返回主菜单或明确开始新游戏，不能返回已加载场景；持久化解锁保持不变。

### Closed acceptance boundaries

- empty exact `RunMap` 是合法的零轴写入；built-in dict 在运行时写入边界仍不合法。
- `validate_axis_deltas(axis_deltas) -> int` 是 `affected_axis_count` 的唯一公共实现。
- detached resolver 只接受由 exact CPython built-in dict/list/scalars 组成的图；精确类型错误抛 `TypeError`，shape/range/history/catalog/token 引用错误抛 `ValueError`。
- 独立机会要求不同 node/choice ID，且替换早期得分后，后续机会仍可达、delta 不变、不会自动改变 token；验证器必须输出原路径与替换路径。

## Files Revised

- `design/gdd/five-axis-state.md`
- `design/gdd/game-concept.md`
- `design/narrative/branch-map.md`
- `design/registry/entities.yaml`
- `docs/architecture/architecture.md`
- `docs/architecture/adr-0001-deterministic-ending-resolution.md`
- `docs/architecture/adr-0002-rollback-and-persistence-boundary.md`
- `docs/architecture/adr-0004-semantic-ending-snapshot-and-state-envelope.md`
- `docs/architecture/adr-0005-counterevidence-ledger-and-detectable-state-initialization.md`
- `docs/architecture/control-manifest.md`
- `design/gdd/systems-index.md`
- `production/session-state/active.md`

## Remediation Status

六项阻断问题已在第四次修订中形成同步规范。原 **MAJOR REVISION NEEDED** 结论仍然有效，直至新的独立复审检查修订后的整套文档并给出批准结论。不得把本修订记录视为自我批准。

## Remaining Maturity Gaps

- 生产 `state.rpy` 与 `ending_rules.py` 仍实现早期原型契约。
- 完整 token、semantic value、repair cost 目录以及一对一修复节点尚待 `SYS-ENDING` / `SYS-NARRATIVE` 设计。
- schema 2、sentinel 读档流程、静态内容验证器和完整存读档/回退证据尚未实现。
- 完整七日图和六结局 witness path 尚未制作。

这些是后续实现或依赖 GDD 的成熟度工作，不改变本次第四修订已完成六项规范修复的事实。

## Superseded by Fourth Review

第四次独立复审确认第三审的大部分问题已解决，但发现四组实施前契约仍需收口。见 [five-axis-state-fourth-review-2026-07-24.md](five-axis-state-fourth-review-2026-07-24.md)。本文件仅保留第三次复审的历史结论。
