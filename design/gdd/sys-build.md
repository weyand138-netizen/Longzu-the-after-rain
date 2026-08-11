# SYS-BUILD — 构建与发布

> **System ID**: SYS-BUILD
> **Status**: Approved with provisional downstream gates
> **Author**: Andwey + Codex
> **Last Updated**: 2026-08-09
> **Implements Pillar**: 看见未说出口的话；悲剧也是完整答案；用普通生活抵抗宏大命运
> **Review Mode**: Solo
> **Self-Check**: PASS — 2026-08-09

## Overview

SYS-BUILD 是《雨停之后》的离线构建与发布系统：它从各 owner 系统提交的已批准 source/catalog/asset manifests 和 SYS-JOURNAL 的 `journal_catalog_bundle:v1` assembler 合约出发，验证版本、来源、引用闭包、内容完整性、法律与 test-only 隔离，生成带有 candidate identity、SHA-256 provenance 和完整声明元数据的 Windows 10/11 离线发行包。玩家不直接操作它，但会通过“下载后无需联网即可运行、看到的是完整且未被构建过程改写的内容、问题能够被准确追溯到对应版本”间接感知其价值；没有 SYS-BUILD，游戏就无法把叙事、成就、愿望手册与无障碍约束可靠地封装成可验证、可发布、可复现的完整版本。

## Player Fantasy

SYS-BUILD 的玩家体验是间接的。玩家不应意识到构建流水线的存在，而应在打开发行包时获得一种安静的确定感：游戏无需联网即可启动，章节、愿望手册、成就、无障碍设置与保存行为都属于同一个被认真封存的作品；玩家看到的内容没有被构建过程擅自改写，也不会因为测试工具、调试入口或来源不明的资源混入而破坏信任。

它主要服务于“悲剧也是完整答案”与“用普通生活抵抗宏大命运”：即使玩家走向苦涩结局，交付给他的仍是完整、合法、可复查的故事，而不是一个只在开发环境里成立的半成品。核心情绪不是成就感，而是安心、信任和“这段经历被完整地交到了我手里”。锚定时刻是玩家首次在无网络条件下启动正式包，并能从主菜单进入完整旅途；之后若发现问题，candidate identity 与 SHA-256 provenance 让团队能够定位具体版本，而不要求玩家承担排查成本。

> `creative-director` 未咨询 — Solo mode。进入 production 前需人工复核。

## Detailed Design

### Core Rules

1. **构建范围与模式**
   - SYS-BUILD 只生成两类产物：内部验证用的 `staging candidate` 与可发布的 `release candidate`。只有后者可以进入发行归档。
   - 每次运行生成唯一 `build_run_id`；`candidate_identity` 只在 staging inventory、owner manifests、assembler 输出、环境 capability manifest 和 identity-affecting build config 全部锁定后生成。
   - 构建过程不联网、不发送遥测、不读取运行时外部服务；所有输入必须来自工作区、已批准 SDK、已登记资产和本地证据目录。

2. **Preflight**
   - 验证 Windows 10/11 x86-64、Ren’Py 8.5.3、Python 3.12-compatible runner、UTF-8、标准库约束、输出目录与 capability manifest。
   - 验证 source roots、asset roots、legal roots、test-only roots 和 evidence roots 均有明确分类；路径不可解析、环境版本不匹配或输出目标不安全时，构建进入 `BLOCKED_INPUT`/`FAILED`，不得继续。

3. **确定性 inventory**
   - 以规范化 UTF-8 相对路径排序建立 source、catalog、asset、generated 和 test-only inventory；记录文件类型、owner、来源、许可状态和 SHA-256。
   - 同一路径、stable ID、production unit、资源或 manifest 项重复时失败；无法解析的 alias、wrapper、closure、reflection、dynamic import 或依赖边不得被跳过。
   - `canonical_production_units_v1` 必须恰为注册表规定的 15 项；`chapter_manifest_valid` 必须为真。`total_text_characters` 只作内容范围报告，不替代 manifest 合法性。

4. **Owner manifest validation**
   - SYS-BUILD 读取各 owner 的已批准 manifest，验证 schema/generation/source hash/reference closure，并保留 owner 的文案、ID、rank、truth approval、结局条件和阈值。
   - SYS-BUILD 不得改写、排序重编号、补全、合并或“修复” source records；任何修订必须由 owner 更新 source 并使旧 candidate 失效。
   - SYS-SAVE 的 checkpoint/location exact join、`UNSUPPORTED_CONTROL_LOCATION`、`INTERNAL_LOAD_VALIDATION_FAILURE` 与保存性能阈值作为输入事实验证，不由 SYS-BUILD 重定义。

5. **SYS-JOURNAL bundle assembly**
   - 按 SYS-JOURNAL contract 执行 deterministic assembler，生成 exact immutable `journal_catalog_bundle:v1`。
   - bundle 必须包含且只包含：`bundle_schema_id="journal_catalog_bundle:v1"`、`persist_catalog_generation_id="persist_catalog:v2"`、`journal_chapter_catalog:v1`、`journal_memory_catalog:v1`、`achievement_catalog:v2`、`journal_ending_catalog:v1`、四类 source hashes 与 immutable cross-reference manifest。
   - 验证 chapter/memory 各 7 个 ID、achievement 恰 11 个、ending 恰 6 个、chapter/memory `(memory_id,day_index)` 一一对应、引用各解析恰 1 次；不允许 SYS-BUILD 改写文案、ID、rank 或 truth approval。

6. **Staging lock**
   - 将通过验证的 production source、生成的 bundle、批准资产、法律/许可声明、运行时配置和 provenance manifests 组成 staging tree。
   - staging tree 不得包含 test observers、spies、fault injectors、protocol bombs、synthetic saves/roots、benchmark harness、debug IDs、evidence forgers 或 runtime source scanners；production→test-only 传递依赖计数必须为 0。
   - staging lock 后重新计算 candidate identity；任何 source、catalog、asset、config 或环境 identity 变化都使现有 staging candidate 失效。

7. **Evidence binding**
   - release candidate 只能消费同一 candidate identity 世代下的 SYS-TEST current PASS evidence、source/catalog hashes、完整 RELEASE manifest 和 exclusion report。
   - SYS-BUILD 不修改 artifact、source hash、fixture、evidence 或归档来制造 PASS；缺失、stale、跨世代拼接、空 manifest、required case 不完整或 `BLOCKED_INPUT` 均阻止 release。
   - SYS-TEST 对 staging 与最终 archive 各执行一次 test-only exclusion scan；SYS-BUILD 保存其结果并将其绑定到 candidate manifest。

8. **Archive and final closure**
   - 使用 Ren’Py 8.5.3 capability manifest 认可的 Windows 构建入口生成离线包；CLI 参数、退出码和失败传播必须由版本固定 runner 记录。
   - 归档完成后扫描最终 archive、store、正式 save/persistent payload 与运行时依赖闭包；不得发现 test-only 类型/ID、网络依赖、遥测入口、allowlist 外资产或未登记声明。
   - 对最终 archive、bundle、source/catalog/asset manifests、法律声明和 candidate manifest 生成完整 lowercase SHA-256；hash 不足 64 个十六进制字符或同世代 hash 不一致时失败。

9. **Release output**
   - READY 只允许输出：离线 Windows package、candidate manifest、source/catalog/asset hash manifest、archive hash、法律/资产声明索引、SYS-TEST evidence index、test-only exclusion report 和稳定失败/发现 ID。
   - 输出必须能从 candidate identity 追溯到 build run、owner manifest、环境 capability、原始 evidence 与最终 archive；不输出内部五轴、token、resolver predicate、隐藏进度或玩家不可见测试数据。

10. **冻结的 runner、manifest 与目录合同（ADR-0007）**
    - 唯一 runner authority 是 `engine-capability-manifest:v1`，当前实例为 `docs/engine-reference/renpy/capability-manifest-v1.json`；runner path/hash、CLI、退出码、原始输出、runtime markers、timeout 与进程树清理必须 exact-match。
    - 唯一候选清单是 `candidate_manifest:v1`。release 目录固定为 `production/releases/<candidate_identity>/`，其下 manifest/index 与 `archive/<package-name>.zip` 同级；临时 staging/runner/diagnostics 只能位于独立的 `production/build-runs/<build_run_id>/`。
   - candidate manifest 的 `candidate_identity` 只来自 identity core；不包含 `build_run_id`、时间戳、工作区路径、输出位置、日志级别、超时、`diagnostic_retention_runs`、最终 archive bytes、archive/manifest/provenance hash 或任何派生封板记录。上述 run-only 字段只进入 `run_record`。
    - 所有 manifest/hash 输入使用 `canonical_encoding:v1`；UTF-8 无 BOM、LF、canonical JSON、稳定 key/path 排序、精确整数，禁止隐式默认、浮点、locale 或平台枚举顺序。

11. **Provenance、legal closure 与 archive hash**
    - 每个 source/catalog/generated/asset/legal/runner/evidence/archive record 必须记录 owner、stable ID、relative path、generation、输入 hash 与 canonical record hash。
    - `legal_closure:v1` 必须为每个资产 exact-join Legal Asset Register 的 source、permission/license、modification、attribution、allowlist 与非商业/同人声明；缺失或模糊声明阻止 READY。
    - `archive_hash` 是最终 ZIP exact bytes 的 SHA-256 lowercase 64-hex；manifest/index 不进入 ZIP，因此 archive hash 不会自引用。`release_identity` 只在 archive 与所有最终 hash 产生后计算。

12. **SYS-TEST 双向 evidence 阶段**
    - `STAGING_EVIDENCE_BOUND`：SYS-BUILD 提供 candidate manifest、staging inventory、candidate identity、RELEASE manifest、runner/environment identity；SYS-TEST 返回同世代 current evidence bundle 与 staging exclusion report。
    - package runner 只能在 staging evidence 通过后运行；SYS-BUILD 保留 stdout/stderr/log/distribute output、exit code、产物 cardinality 与 archive hash。
    - `ARCHIVE_EVIDENCE_BOUND`：SYS-BUILD 提供 archive inventory/hash；SYS-TEST 返回 final RELEASE binding 与 archive exclusion report。
    - 只有两阶段 evidence、legal closure、archive closure、runner 与所有 hash 均通过时才允许 `READY`；SYS-BUILD 不修改 SYS-TEST artifact，SYS-TEST 不修改 production source/catalog。

### States and Transitions

| 状态 | 进入条件 | 允许行为 | 离开条件 |
|---|---|---|---|
| `UNBOUND` | 尚无有效 build input set | 仅加载并验证输入声明 | 输入完整且非空 → `PREFLIGHT`；缺输入 → `BLOCKED_INPUT` |
| `PREFLIGHT` | build mode、engine、platform、runner、roots 和配置正在验证 | 不生成可发布产物 | 通过 → `INVENTORY_LOCKED`；版本/路径/配置不符 → `FAILED` |
| `INVENTORY_LOCKED` | source/catalog/asset/legal/test-only inventory 已规范化并 hash | 只读锁定 inventory | 全部 owner manifest 合法 → `SOURCE_VALIDATED`；缺失/重复/未解析边 → `FAILED` |
| `SOURCE_VALIDATED` | owner contracts、15 个 canonical units 与 cross-system facts 通过 | 允许执行 Journal assembler | assembler 输入完整 → `BUNDLE_ASSEMBLED`；generation/schema/hash 不符 → `FAILED` |
| `BUNDLE_ASSEMBLED` | `journal_catalog_bundle:v1` 与 cross-reference manifest 已冻结 | 允许生成 staging tree | staging inventory 与 candidate identity 生成 → `STAGING_LOCKED` |
| `STAGING_LOCKED` | production staging tree 已锁定 | 允许请求同世代 SYS-TEST staging evidence | staging evidence 完整且 current → `STAGING_EVIDENCE_BOUND`；缺失/stale/leakage → `BLOCKED_INPUT` 或 `FAILED` |
| `STAGING_EVIDENCE_BOUND` | candidate identity 与 staging RELEASE evidence/exclusion exact-match | 允许调用批准的 Ren’Py package runner | package 成功 → `ARCHIVED`；runner 失败 → `FAILED` |
| `ARCHIVED` | Windows archive 已生成且 archive hash 已记录 | 只允许读取并请求最终 SYS-TEST evidence | archive evidence 完整且 current → `ARCHIVE_EVIDENCE_BOUND`；缺失/stale/leakage → `BLOCKED_INPUT` 或 `FAILED` |
| `ARCHIVE_EVIDENCE_BOUND` | archive identity、最终 exclusion 与 RELEASE evidence exact-match | 允许执行 legal/provenance/hash closure | closure、法律、asset、hash 扫描全通过 → `CLOSURE_VERIFIED`；任一失败 → `FAILED` |
| `CLOSURE_VERIFIED` | archive 与 provenance 已完整验证 | 生成最终报告，不再修改输入 | manifest 写入成功 → `READY`；写入/哈希失败 → `FAILED` |
| `READY` | 所有 release gates 通过 | 只读、复制或发布已锁定产物 | 新输入变化时新建 run；禁止原地修补 |
| `BLOCKED_INPUT` | 外部 owner/engine/evidence 输入不足 | 只生成阻断报告；不得伪装为失败包或空内容包 | 输入变更后新建 run → `UNBOUND` |
| `FAILED` | 合同、完整性、隔离、runner 或 archive 检查失败 | 保留原始诊断；不得继续后续阶段 | 修复后新建 run → `UNBOUND` |

### Interactions with Other Systems

| 系统 | 方向与接口 | SYS-BUILD 权限边界 |
|---|---|---|
| Ren’Py 8.5.3 / Engine | Engine capability manifest、package runner、退出码与 archive 输出 → SYS-BUILD | 调用批准 runner；不假设未验证的 CLI 行为 |
| SYS-NARRATIVE | source units、chapter/memory catalogs、truth approvals、canonical CFG/source hashes → SYS-BUILD | 只验证与封存，不改写叙事内容 |
| SYS-CHOICE | choice declarations、joins、projection/coverage manifests → SYS-BUILD | 只验证构建输入，不重算 choice 语义 |
| SYS-ENDING | ending catalog、cause/display contracts、terminal coverage → SYS-BUILD | 只保留 owner 输出，不执行 resolver |
| SYS-ACHIEVE | `achievement_catalog:v2` display records → SYS-BUILD | 只验证恰 11 项与引用，不读取条件 |
| SYS-ACCESS | settings/accessibility/source and evidence manifests → SYS-BUILD | 只验证已批准配置与资源声明，不重定义 setting authority |
| SYS-SAVE / SYS-PERSIST | schema/generation/checkpoint/persistent/save manifests 与性能 evidence → SYS-BUILD | 只验证 exact contract，不拥有存档或 persistent 数据 |
| SYS-JOURNAL | assembler contract → SYS-BUILD；`journal_catalog_bundle:v1` 与 source-hash manifest ← SYS-BUILD | SYS-JOURNAL 拥有 schema、assembler 与 error taxonomy；SYS-BUILD 拥有执行、封存和 archive closure |
| SYS-TEST | SYS-BUILD 输出 candidate/staging/archive identity 与扫描结果 → SYS-TEST；current RELEASE evidence → SYS-BUILD | SYS-TEST 拥有 evidence；SYS-BUILD 不修改或替代 evidence |
| Legal Asset Register | 资产来源、许可、修改状态与 attribution → SYS-BUILD | 未登记或禁止资产直接阻止 release |
| Architecture / Control Manifest | 架构与禁止项 → SYS-BUILD | 构建实现不得创建第二权威或绕过 production isolation |

各 owner manifest 的语义字段仍由 owning GDD 拥有；candidate manifest、证据 binding、目录布局、hash 与证据阶段由 ADR-0007 冻结。SYS-BUILD 只消费 owner 结果，不创建第二套内容权威。

## Formulas

> `systems-designer` 未咨询 — Solo mode。公式与阈值在进入 production 前需人工复核；SYS-BUILD 不重定义上游 owner 的公式，只消费其结果。

The `candidate_identity` formula is defined as:

`candidate_identity = SHA256(canonical_bytes_v1(source_identity, bundle_identity, engine_capability, identity_affecting_build_config, legal_asset_inventory))`

**Variables:**
| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Source identity records | `I_s` | exact tuple | `1–N` unique records | 已排序的 source/catalog/asset/generated records；每项含 kind、relative path、owner、generation、content hash |
| Bundle identity | `B` | exact record | 1 valid record | `journal_catalog_bundle:v1` 的 schema、generation、source hashes 与 cross-reference identity |
| Engine capability | `E` | exact record | 1 valid record | Ren’Py、Python、Windows、runner 和 capability manifest identity |
| Identity-affecting build config | `C_i` | exact record | 1 valid record | 目标平台、包格式/选择、archive/include policy 及改变交付字节或语义的选项 |
| Run-only config | `C_r` | exact record | 1 valid record | 工作区路径、输出位置、日志级别、timeout、`diagnostic_retention_runs`、时间与 `build_run_id`；仅进入 `run_record` |
| Legal/asset inventory | `L` | exact tuple | `0–N` records | 资产来源、许可、修改状态、attribution 与声明 identity |
| Canonical bytes | `K` | bytes | `>0` bytes | 对所有输入按 UTF-8、长度前缀、稳定 key/path 顺序编码后的字节序列 |
| Candidate identity | `Y` | lowercase hex string | exactly 64 chars | candidate identity core 的内容身份；不含 archive/manifest/provenance/finalization hash |

**Output Range:** 64 位 lowercase hexadecimal SHA-256；任一输入缺失、重复、类型非法或 canonical encoding 不确定时不产生输出。

**Example:** 同一组 15 个 canonical production units、同一 bundle、同一 Ren’Py capability、同一资产与法律 inventory，在不同工作区路径、输出位置、日志级别、timeout 或 diagnostic retention 下运行，仍产生相同的 `Y`；任一 source hash 或 identity-affecting config 改变 1 位时产生不同的 `Y`。最终 `archive_hash` 只哈希 ZIP bytes，`release_identity` 才吸收 archive、manifest、provenance、legal 与 evidence hashes。

The `archive_closure_valid` formula is defined as:

`archive_closure_valid = (test_only_count = 0) ∧ (network_dependency_count = 0) ∧ (telemetry_entry_count = 0) ∧ (unallowlisted_asset_count = 0) ∧ (undeclared_asset_count = 0) ∧ (production_to_test_only_edge_count = 0) ∧ legal_asset_valid ∧ archive_hash_valid`

**Variables:**
| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Test-only count | `T` | int | `0–N` | archive、store、save、persistent 与 dependency closure 中 test-only 类型/ID 数量 |
| Network dependency count | `N` | int | `0–N` | 网络客户端、外部服务或运行时网络调用数量 |
| Telemetry count | `M` | int | `0–N` | telemetry、analytics、crash upload 或类似入口数量 |
| Unallowlisted asset count | `U` | int | `0–N` | 未在批准 asset allowlist 中的资源数量 |
| Undeclared asset count | `D` | int | `0–N` | 缺少来源/许可/attribution 声明的资源数量 |
| Production→test edge count | `P` | int | `0–N` | 生产依赖闭包到 test-only 的边数量 |
| Legal/asset validity | `A` | exact bool | `false/true` | Legal Asset Register 与声明索引均通过 |
| Archive hash validity | `H` | exact bool | `false/true` | archive 与 candidate manifest 的 SHA-256 完全匹配 |
| Closure validity | `Q` | exact bool | `false/true` | 归档闭包是否满足所有隔离和完整性条件 |

**Output Range:** `true` 或 `false`；任何计数大于 0、`A=false` 或 `H=false` 时必须为 `false`。

**Example:** `T=N=M=U=D=P=0` 且 `A=true、H=true` 时 `Q=true`；即使其他条件全真，只要 `T=1`，`Q=false`。

The `release_gate_pass` formula is defined as:

`release_gate_pass = source_manifest_valid ∧ journal_bundle_valid ∧ staging_evidence_bound ∧ archive_evidence_bound ∧ candidate_identity_match ∧ environment_match ∧ package_runner_success ∧ archive_closure_valid ∧ legal_asset_valid ∧ archive_hash_valid`

**Variables:**
| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Source manifest validity | `S` | exact bool | `false/true` | owner manifests、15 个 production units、reference closure 和上游公式结果均通过 |
| Journal bundle validity | `J` | exact bool | `false/true` | `journal_catalog_bundle:v1` schema、generation、hash、ID 闭集和引用均通过 |
| Staging evidence | `E_s` | exact bool | `false/true` | SYS-TEST staging RELEASE evidence 与 exclusion report 非空、current、同世代且 required cases 完整 |
| Archive evidence | `E_a` | exact bool | `false/true` | SYS-TEST final archive evidence 与 exclusion report 非空、current、同世代且 archive hash exact-match |
| Candidate identity match | `Y` | exact bool | `false/true` | staging、evidence、archive 与最终 manifest 指向同一 candidate identity |
| Environment match | `V` | exact bool | `false/true` | Windows/Ren’Py/Python/runner capability 与批准 environment manifest 相等 |
| Package runner success | `R` | exact bool | `false/true` | 版本固定 package runner 正常退出且 archive 已生成 |
| Archive closure validity | `Q` | exact bool | `false/true` | 上述 `archive_closure_valid` |
| Legal/asset validity | `A` | exact bool | `false/true` | 资产、许可、声明与 attribution 通过 |
| Archive hash validity | `H` | exact bool | `false/true` | archive exact bytes hash matches; downstream bundle/manifest/provenance references are exact |
| Release gate result | `G` | exact bool | `false/true` | 是否允许进入 READY |

**Output Range:** `true` 仅当 10 个输入全部为 `true`；任一输入为 `false`、缺失或 stale 时为 `false`。不存在 partial pass 或自动修复。

**Example:** 10 个 gate 全为 `true` 时 `G=true`；若 staging 或 archive evidence 任一 stale，即使 package 已成功生成，`G=false`。

已注册的 `chapter_manifest_valid`、`restore_checkpoint_join_valid`、`save_load_performance_pass` 与 `persist_catalog_generation_id` 作为上游输入或 identity 成员使用，SYS-BUILD 不复制其表达式或改写其阈值。

## Edge Cases

> `systems-designer` 未咨询 — Solo mode。进入 production 前需人工复核边界与故障注入覆盖。

- **If `build_run_id` 缺失、重复或无法绑定唯一输入集**：进入 `BLOCKED_INPUT`，不生成 `candidate_identity`，不得复用其他 run 的身份。
- **If Windows、Ren’Py、Python、runner 或 capability manifest 与批准环境不匹配**：进入 `FAILED`，记录实际与期望 identity；不得使用其他环境的 PASS evidence。
- **If source/catalog/asset/legal/test-only manifest 缺失、为空、重复或存在未解析依赖边**：进入 `FAILED`；保留所有对应 failure IDs，禁止进入 assembler。
- **If canonical production units 不等于注册表规定的 15 项，或 chapter manifest 不合法**：进入 `FAILED`；`total_text_characters` 超出目标范围只产生内容范围 finding，不单独替代该失败。
- **If 多个错误在同一阶段同时出现**：保留按稳定 ID 排序的完整 finding 集合，并按固定 primary 优先级选择首个错误：environment/input contract → owner manifest/schema → inventory/reference closure → Journal bundle → evidence freshness → package runner → archive closure/hash → report write。
- **If SYS-JOURNAL generation、schema、source hash、ID 闭集、chapter/memory pair 或引用基数不匹配**：进入 `FAILED`；不选择性信任其他 category，也不由 SYS-BUILD 改写 source record。
- **If SYS-TEST evidence 缺失、stale、跨 candidate 世代、required case 不完整或只提供摘要**：进入 `BLOCKED_INPUT`；已生成的 package 仍不得被标记为 release，必须等待同一 candidate identity 的 current evidence。
- **If staging 或 final archive 中发现 test-only observer/spy/fault injector/protocol bomb/synthetic save/root/benchmark/evidence forger、production→test-only edge、网络/遥测入口**：进入 `FAILED`；不得通过删除单个发现项后继续当前 run，必须重新 inventory 并创建新 run。
- **If 资产缺少 Legal Asset Register 来源、许可、修改状态或 attribution，或出现 allowlist 外资源**：进入 `FAILED`；不得以占位声明或 archive 内隐藏文件满足法律门禁。
- **If archive 生成中断、部分输出存在、目标目录已有文件或 final hash 写入失败**：当前 run 保持 `FAILED`；未发布输出不得被当作 READY，发布器只能从新 `UNBOUND` run 重新生成并原子写入新的输出位置。
- **If archive、bundle、manifest 或 provenance 的 hash 不为 64 位 lowercase hex，或同一 identity 世代出现 hash 不一致**：进入 `FAILED`；不允许截断、重算后覆盖或静默接受。
- **If 可选诊断清单为空但核心 15 个 production units、Journal 四类 catalog 或 required RELEASE evidence 均完整**：保持可继续；空诊断不渲染为玩家内容，也不阻止合法构建。
- **If 构建完成后任何 source、catalog、asset、config、runner、environment 或 owner generation 改变**：旧 candidate 立即视为 stale；不得增量修补，必须生成新的 candidate identity 并重新执行受影响阶段及完整 RELEASE gate。
- **If 构建进程收到重试、取消或重复提交请求**：当前阶段只接受一个 active run；重复请求返回现有 run 状态，不重复发布；取消只保留诊断并将 run 置为 `FAILED`，不产生可发布部分包。

## Dependencies

| 依赖系统/来源 | 方向与性质 | 接口数据 | 所有权与 SYS-BUILD 责任 |
|---|---|---|---|
| Ren’Py 8.5.3 / Windows 10/11 x86-64 | 上游，Hard | capability manifest、runner identity、package output、exit code、环境 identity | Engine 拥有运行时；SYS-BUILD 只调用已验证 runner 并记录结果 |
| SYS-NARRATIVE | 上游，Hard | 15 个 canonical production units、chapter/memory source catalogs、truth approvals、CFG/source hashes | SYS-NARRATIVE 拥有内容；SYS-BUILD 验证完整性与 provenance，不改文案 |
| SYS-CHOICE | 上游，Hard | choice declarations、join/coverage/projection manifests | SYS-CHOICE 拥有选择语义；SYS-BUILD 只验证输入，不重算语义 |
| SYS-ENDING | 上游，Hard | ending/display/cause contracts、terminal coverage 与 source hashes | SYS-ENDING 拥有 resolver 与结局语义；SYS-BUILD 不执行 resolver |
| SYS-ACHIEVE | 上游，Hard | `achievement_catalog:v2` display records | SYS-ACHIEVE 拥有成就条件与展示源；SYS-BUILD 只验证显示目录 |
| SYS-ACCESS | 上游，Hard | settings、accessibility source/evidence manifests、资源声明 | SYS-ACCESS 拥有无障碍权威；SYS-BUILD 不重定义设置或阈值 |
| SYS-SAVE | 上游，Hard | schema/generation、checkpoint/location catalogs、failure constants、performance evidence | SYS-SAVE 拥有存档合同；SYS-BUILD 验证 `restore_checkpoint_join_valid` 与 `save_load_performance_pass` 输入 |
| SYS-PERSIST | 上游，Hard | `persist_catalog:v2`、persistent schema/epoch/merge manifests | SYS-PERSIST 拥有 persistent 数据；SYS-BUILD 只封存 generation identity |
| SYS-JOURNAL | 上游合同 + 下游消费者，Hard | `journal_catalog_bundle:v1` schema、assembler、generation matrix、error taxonomy | SYS-JOURNAL 拥有 bundle schema/assembler；SYS-BUILD 执行 assembler、计算 hash、验证 archive closure 并封存 bundle |
| SYS-TEST | 双向，Hard release gate | SYS-BUILD 输出 `candidate_manifest:v1`、staging/archive inventory 与 archive hash；SYS-TEST 返回同世代 staging/archive RELEASE evidence 与两份 exclusion reports | SYS-TEST 拥有 evidence schema/runner/result；双方均不得改写对方产物 |
| Legal Asset Register | 上游，Hard | source、permission/license、modification、attribution、allowlist | 注册表拥有资产 admission；未登记或禁止资产阻止发布 |
| Architecture / Control Manifest / ADRs | 策略上游，Hard policy | ownership、purity、offline、test isolation、save/accessibility/build constraints | 架构文档拥有约束；SYS-BUILD 必须通过静态和闭包验证落实 |

### Bidirectional contract

- SYS-JOURNAL 必须声明其 bundle schema、assembler、generation matrix 与错误域；SYS-BUILD 不得自行创造第二套 bundle contract。
- SYS-TEST 必须声明 `test_evidence_bundle:v1`、`STAGING_EVIDENCE_BOUND`/`ARCHIVE_EVIDENCE_BOUND`、identity binding 与 exclusion-report schema；SYS-BUILD 必须提供其扫描所需的 candidate/staging/archive manifests 与 archive hash。
- 每个 source owner 必须提供版本化、非空、source-hash-bound manifest；owner 未完成冻结时，SYS-BUILD 返回 `BLOCKED_INPUT`。
- 所有上述依赖均为 release-hard；可选诊断、非发布 benchmark 或未来 P1 资产不属于当前 release-hard 输入，也不能关闭 RELEASE gate。
- 当前 `SYS-NARRATIVE`、`SYS-SAVE`、`SYS-PERSIST`、`SYS-JOURNAL` 的 GDD 仍带 revision/downstream gates；因此本节把它们作为已定义但尚未 implementation-ready 的 provisional contracts，直到各自 owner 完成独立复核与 content/integration lock。

## Tuning Knobs

> `systems-designer` 未咨询 — Solo mode。正确性与安全边界需要在实现前人工复核。

### 可调运行参数

| Knob | Owner | Default | Safe range / allowed values | 过低/过高行为 |
|---|---|---:|---|---|
| `build_runner_timeout_ms` | SYS-BUILD | 600,000（provisional，待 engine spike） | 60,000–3,600,000 ms | 过低会把合法慢构建判为 timeout；过高只会延迟失败报告；不改变内容或 gate 逻辑 |
| `diagnostic_retention_runs` | SYS-BUILD | 5 | 1–20 次非发布诊断 run | 过低会损失回溯样本；过高增加本地磁盘使用；不得删除 release provenance、human/playtest 记录或公开版本证据 |
| `staging_workspace_root` | SYS-BUILD | 项目批准 staging 根目录 | 必须位于批准工作区，且每个 run 使用独立子目录 | 路径不可解析、越界或与 release output 重叠时 `FAILED`；合法路径变化不得改变 candidate identity |
| `release_output_root` | SYS-BUILD | 项目批准 release 输出根目录 | 必须是显式、可写、与 staging 隔离的输出根目录 | 已存在且未绑定当前 candidate 的目录不得覆盖；写入失败保持 `FAILED` |

### 锁定、不属于 tuning 的值

- `hash_algorithm = SHA-256`
- canonical encoding、UTF-8、稳定排序与完整 lowercase hex
- `release_gate_pass` 的 strict-AND 语义
- `archive_closure_valid` 中所有 test-only/network/telemetry/undeclared/unallowlisted 计数必须为 0
- `build_mode ∈ {STAGING, RELEASE}`；只有 `RELEASE` 可生成发布归档
- findings 不截断、不静默覆盖；primary failure priority 固定
- 15 个 canonical production units、Journal generation/ID 闭集与 `persist_catalog:v2`
- 上游 owner 的 `total_text_characters` 目标范围、`save_load_performance_pass` 阈值和其他 schema/formula；SYS-BUILD 只消费其结果

### Knob interactions

- 降低 `build_runner_timeout_ms` 不得降低任何 manifest、evidence 或 closure 门禁；timeout 只能产生 `FAILED/TIMEOUT`。
- `diagnostic_retention_runs` 不能影响 candidate identity、release archive 或 current/stale 判定。
- staging 与 release root 必须分离；同一路径或路径别名导致 archive 覆盖时立即失败。
- 只有会改变交付内容、字节或语义的 `identity-affecting build config` 变更才进入 candidate identity；工作区路径、输出位置、日志级别、timeout 与 `diagnostic_retention_runs` 只进入 `build_run_id/run_record`，不改变 candidate identity。

## Visual/Audio Requirements

不适用。SYS-BUILD 没有玩家运行时视觉或音频表现；构建日志、failure report、provenance 与 exclusion report 以结构化文本/JSON/Markdown 产出，不进入游戏内表现层。任何用于诊断的声音、动画、调试覆盖层或玩家可见测试素材均不得进入 release archive。

## UI Requirements

不适用。SYS-BUILD 不提供玩家运行时 UI。开发者侧只需要稳定的命令行终端摘要与可读取产物索引；终端摘要显示 scope、状态、失败数量、首个 failure ID 与 manifest/hash 引用，完整诊断通过 versioned artifact 访问，且这些工具不进入 production dependency closure。

## Acceptance Criteria

> `qa-lead` 未咨询 — Solo mode。进入 production 前需人工复核；以下 criteria 需由 SYS-TEST 映射到非空 fixture、runner、oracle 与原始 artifact。

#### Preflight、Inventory 与 Ownership

- **BUILD-CORE-001** — **GIVEN** Windows 10/11 x86-64、Ren’Py 8.5.3、Python/runner capability manifest 与完整 build input set，**WHEN**执行 `PREFLIGHT`，**THEN**环境 identity exact-match 且状态进入 `INVENTORY_LOCKED`；任一版本、路径或输入缺失则不进入该状态。
- **BUILD-CORE-002** — **GIVEN**相同 source/catalog/asset/legal/test-only roots，**WHEN**执行 inventory 两次，**THEN**规范化相对路径、分类、owner、generation 与 SHA-256 tuple 完全相同，且不依赖文件枚举顺序。
- **BUILD-CORE-003** — **GIVEN** canonical production manifest，**WHEN**执行 source validation，**THEN**生产单元集合恰等于注册表中的 15 项；重复、缺失或未解析 dependency edge 使状态为 `FAILED`。
- **BUILD-CORE-004** — **GIVEN** owner manifest 含 source copy、stable ID、rank 与 truth approval，**WHEN** SYS-BUILD 通过 validation 并生成 staging，**THEN**source copy/ID/rank/truth approval rewrite count 均为 0。
- **BUILD-CORE-005** — **GIVEN** `total_text_characters` 超出 70,000–90,000 目标范围但所有 owner manifest 合法，**WHEN**执行 validation，**THEN**产生 content-scope finding 但不得替代或伪造 `chapter_manifest_valid` 结果。

#### Journal Bundle 与 Cross-System Contracts

- **BUILD-JOURNAL-001** — **GIVEN**四个 owner-signed Journal source catalogs、assembler contract 与 golden manifest，**WHEN**执行 assembler，**THEN**输出 `journal_catalog_bundle:v1`，generation matrix exact-match，chapter/memory 各 7 个 ID、achievement 恰 11 个、ending 恰 6 个。
- **BUILD-JOURNAL-002** — **GIVEN** chapter/memory records 与 cross-reference manifest，**WHEN**验证 bundle，**THEN**每个引用恰解析 1 次，chapter/memory `(memory_id,day_index)` 一一对应；pair mismatch 或 duplicate reference 使 bundle validation 失败。
- **BUILD-JOURNAL-003** — **GIVEN**同一 generation 的 source catalog 与不同 source hash，**WHEN**执行 bundle validation，**THEN**输出 `FAILED/CONTENT_BUNDLE_UNAVAILABLE`，不选择性信任其他 category。
- **BUILD-CONTRACT-001** — **GIVEN** SYS-SAVE 的 checkpoint/location catalogs、`restore_checkpoint_join_valid` 与 `save_load_performance_pass` evidence，**WHEN**执行 release input validation，**THEN**只验证并记录 owner result，不重定义 schema、join 或性能阈值。

#### Staging、Isolation 与 Evidence

- **BUILD-ISO-001** — **GIVEN**完整 production/test source graph，**WHEN**扫描 direct/transitive imports、aliases、wrappers、closures、reflection 与 dynamic imports，**THEN**production→test-only edge count 为 0；未解析边阻止 release。
- **BUILD-ISO-002** — **GIVEN** staging tree 与 test-only exclusion policy，**WHEN**扫描 observer、spy、fault injector、protocol bomb、synthetic save/root、benchmark harness、debug ID、evidence forger 与 runtime scanner，**THEN**每类计数均为 0。
- **BUILD-EVID-001** — **GIVEN** staging candidate 与 SYS-TEST evidence，**WHEN**比较 candidate identity、source/catalog hashes、RELEASE manifest、fixture、runner 与 environment identity，**THEN**所有 required evidence 均为 current 且同一 identity 世代；缺失/stale/跨世代 evidence 使 release gate 为 `BLOCKED_INPUT`。
- **BUILD-EVID-002** — **GIVEN** SYS-TEST 提供 component PASS 但缺少 current RELEASE evidence，**WHEN**执行 `release_gate_pass`，**THEN**结果为 `false`，不得把 component PASS 提升为 release PASS。
- **BUILD-EVID-003** — **GIVEN** build 已生成 archive，**WHEN** SYS-BUILD 消费 SYS-TEST scan result，**THEN**不修改 artifact、source hash、fixture 或 archive；任一修改计数大于 0 时 build gate 失败。
- **BUILD-EVID-004** — **GIVEN** staging lock 已完成，**WHEN** SYS-TEST 执行 `STAGING_EVIDENCE_BOUND`，**THEN** candidate manifest、RELEASE case mapping、runner/environment identity 与 staging exclusion report exact-match；缺失、stale、跨世代或 component-only evidence 不能绑定。
- **BUILD-EVID-005** — **GIVEN** archive hash 已生成，**WHEN** SYS-TEST 执行 `ARCHIVE_EVIDENCE_BOUND`，**THEN** final evidence 与 archive exclusion report exact-bind 同一 archive hash；任一 test-only、network、telemetry、undeclared 或 unallowlisted finding 使 gate 失败。

#### Formula and Identity

- **BUILD-FORM-001** — **GIVEN**两次运行使用完全相同的 identity records、bundle、engine capability、identity-affecting build config 与 legal/asset inventory，且 run-only 配置可不同，**WHEN**计算 `candidate_identity`，**THEN**两次结果完全相等且为 64 位 lowercase SHA-256。
- **BUILD-FORM-002** — **GIVEN** candidate identity 输入中的任一 source/catalog/asset/identity-affecting-config/environment identity 改变，**WHEN**重新计算 `candidate_identity`，**THEN**新 identity 与旧 identity 不相等，旧 candidate 标记为 stale；workspace path、output location、log level、timeout 或 diagnostic retention 变化不得触发 stale。
- **BUILD-FORM-003** — **GIVEN**最终 archive 中 test-only/network/telemetry/unallowlisted/undeclared 计数均为 0、production→test-only edge 为 0、legal/hash 均有效，**WHEN**计算 `archive_closure_valid`，**THEN**结果为 `true`；任一计数变为 1 或 legal/hash 为 false 时结果为 `false`。
- **BUILD-FORM-004** — **GIVEN** 10 个 `release_gate_pass` 输入全部为 `true`，**WHEN**聚合 release gate，**THEN**结果为 `true` 并允许进入 `READY`；任一输入为 false、缺失或 stale 时结果为 `false`，不得 partial pass。
- **BUILD-FORM-005** — **GIVEN**相同错误集合以不同发现顺序出现，**WHEN**生成失败报告，**THEN**完整 finding 集合按稳定 ID 排序且 primary failure 遵循固定优先级，报告内容可复现。
- **BUILD-FORM-006** — **GIVEN**相同 identity core 但不同 build run/time，**WHEN**计算 candidate identity，**THEN**结果相同；当 source、runner、legal、config、fixture 或 environment identity 任一变化时旧 candidate 为 `STALE`。
- **BUILD-FORM-007** — **GIVEN** final ZIP、candidate manifest 与 provenance index，**WHEN**计算 archive hash，**THEN** hash 输入只包含 ZIP exact bytes；manifest 或 release directory hash 不得形成 archive-hash self-reference。

#### Archive、Offline Package 与 Provenance

- **BUILD-ARCHIVE-001** — **GIVEN**通过 `EVIDENCE_BOUND` 的 release candidate，**WHEN**使用批准的 Ren’Py 8.5.3 package runner，**THEN**生成 Windows 10/11 x86-64 离线包，并记录 runner version、arguments、exit code 与 archive identity。
- **BUILD-ARCHIVE-002** — **GIVEN**已生成 archive，**WHEN**扫描 archive、store、正式 save/persistent payload 与 runtime dependency closure，**THEN**test-only、网络、遥测、allowlist 外资产与未登记声明计数均为 0。
- **BUILD-ARCHIVE-003** — **GIVEN**archive、bundle、source/catalog/asset manifests、legal declarations 与 candidate manifest，**WHEN**计算并比较 SHA-256，**THEN**所有 hash 均为 64 位 lowercase hex 且 exact-match；任何 mismatch 使 build `FAILED`。
- **BUILD-ARCHIVE-004** — **GIVEN**断开网络的目标 Windows 环境与 READY archive，**WHEN**启动并进入主菜单，**THEN**无需网络服务即可成功启动；启动时间不超过项目 5 秒目标，且未产生网络/遥测调用。
- **BUILD-ARCHIVE-005** — **GIVEN**READY candidate，**WHEN**从 candidate manifest 追溯 build run、owner manifests、environment capability、SYS-TEST evidence、legal/asset declarations 与 archive，**THEN**每条引用存在且 hash 完全匹配；manifest 不包含五轴、token、resolver predicate 或隐藏进度数据。
- **BUILD-ARCHIVE-006** — **GIVEN**任一 shipped asset，**WHEN**验证 `legal_closure:v1`，**THEN**source、permission/license、modification、attribution、allowlist 与 exact asset hash 均可追溯；缺失或模糊记录阻止 READY。

#### Failure、Retry 与 Output Safety

- **BUILD-FAIL-001** — **GIVEN**任一 required input 缺失，**WHEN**执行 build，**THEN**状态为 `BLOCKED_INPUT`，不生成可发布 archive，不伪装为空内容包。
- **BUILD-FAIL-002** — **GIVEN**archive 生成中断、目标目录已有未绑定文件或 final manifest 写入失败，**WHEN**run 结束，**THEN**当前 run 为 `FAILED`，未发布产物不可标记 `READY`，且新 run 使用新的独立 output identity。
- **BUILD-FAIL-003** — **GIVEN**同一 active run 收到重复提交或重试，**WHEN**处理请求，**THEN**只保留一个 active run；重复请求返回现有状态，不重复发布或生成第二个 candidate。
- **BUILD-FAIL-004** — **GIVEN**`build_runner_timeout_ms` 到期，**WHEN**package runner 未完成，**THEN**产生 `FAILED/TIMEOUT` 与原始 runner evidence，不降低其他 gate，也不把 partial archive 标为 READY。
- **BUILD-FAIL-005** — **GIVEN**diagnostic retention 清理运行，**WHEN**超过 `diagnostic_retention_runs` 的非发布诊断被清理，**THEN**只删除允许删除的旧诊断；release provenance、human/playtest 记录与公开版本追溯 evidence 保留。

## Open Questions

| ID | 问题 | Owner | 目标解决时间 |
|---|---|---|---|
| `BUILD-Q1` | Ren’Py 8.5.3 Windows build 的实际 CLI、退出码、失败传播、输出目录与 capability manifest 如何冻结？ | Engine Programmer + Build Owner | 已由 ADR-0007 冻结；实现前重跑 capability probe |
| `BUILD-Q2` | `candidate_manifest:v1`、canonical identity record、source/catalog/asset hash manifest 与 provenance index 的 exact schema 是否需要新增 ADR？ | Architect + Build Owner | 已由 ADR-0007 冻结；实现 validator |
| `BUILD-Q3` | staging tree、final archive、legal declarations、evidence index 与 exclusion report 的最终目录布局和版本化 artifact path 是什么？ | Build Owner + SYS-TEST | 已由 ADR-0007 冻结；实现目录锁与原子封板 |
| `BUILD-Q4` | SYS-JOURNAL re-review、source owner generation lock 与 `journal_catalog_bundle:v1` golden manifest 何时完成 content/integration lock？ | SYS-JOURNAL Owner + Producer | ADR-0007 已冻结 Build 侧消费接口；Journal owner 仍需完成其 content/integration lock |
| `BUILD-Q5` | SYS-TEST `test_evidence_bundle:v1`、current RELEASE evidence、registry traceability 与 SYS-BUILD candidate identity 的最终双向接口是什么？ | SYS-TEST + Build Owner + QA | 已由 ADR-0007 冻结为 staging/archive 两阶段 evidence handshake；实现并生成新 evidence |
| `BUILD-Q6` | Windows 最低参考硬件、renderer、断网启动验证、build runner timeout 默认值与 benchmark protocol 如何冻结？ | Engine Programmer + Performance Analyst | 设计阶段只冻结 `benchmark_protocol:v1` 的字段、采样和判定方法；最终硬件/renderer/离线启动/timeout 实测属于实现与发布门禁，不阻止 GDD 封板 |
| `BUILD-Q7` | 中文字体、最终资产、授权、非商业声明与公开离线包中的 attribution 文案是否全部满足 Legal Asset Register？ | Producer + Legal/Asset Owner | 后续资产/法律/发布门禁；不阻止本 GDD 封板 |
| `BUILD-Q8` | `diagnostic_retention_runs` 的本地清理位置、备份边界与 release/human/playtest evidence 保留策略是什么？ | Build Owner + Producer | 后续生产工具/发布门禁；该 run-only 参数不进入 candidate identity，不阻止本 GDD 封板 |
| `BUILD-Q9` | 最终 Windows 包是自包含目录、压缩 archive 还是其他离线交付格式；是否需要额外 installer/signing 流程？ | Producer + Build Owner | 后续发布门禁；不阻止本 GDD 封板 |
