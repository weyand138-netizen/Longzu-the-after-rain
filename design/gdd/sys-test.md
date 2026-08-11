# SYS-TEST — 自动化验证

> **Status**: Approved with downstream implementation gates
> **Author**: Andwey + Codex
> **Last Updated**: 2026-08-09
> **Implements Pillar**: 间接保障全部四项创作支柱，重点保障“温柔必须被挣来”与“悲剧也是完整答案”的因果可验证性
> **Review Mode**: Solo
> **Creative Director Review (CD-GDD-ALIGN)**: Skipped — Solo mode; manual review required before production
> **Self-Check**: PASS — 2026-08-09
> **Targeted Closure Re-review**: 2026-08-09 — verdict `APPROVED`; producer accepted the constrained review disposition; evidence-schema and registry-traceability alignment remain downstream implementation gates

## Overview

SYS-TEST 是面向制作与发布流程、玩家不直接操作的自动化验证基础设施。它为 Ren’Py 8.5.3 项目建立统一的证据分类和阻断门槛，通过 lint、Python 纯逻辑测试、Ren’Py testcase、静态分析、受控 instrumentation、完整路线枚举、故障注入、无障碍与布局验证、性能基准及证据包审计，证明六结局判定、选择—反应—回收链、存读档与回退、跨周目持久化、成就与愿望手册在合法与失败路径上均符合各 owning GDD 的冻结合同；SYS-TENSION 的 timed-choice 套件已明确延期至 post-MVP，不属于当前 P0 Production gate。玩家只会间接感受到它带来的稳定因果、安全恢复和输入语义等价；若缺少该系统，游戏将失去对“玩家选择确实产生一致后果”的可信保证。具体的纯度、快照、生命周期与 completion-event 技术边界遵循 ADR-0001、ADR-0002、ADR-0004、ADR-0005 与 ADR-0006，不在本 GDD 中重新定义。

## Player Fantasy

玩家不应意识到自己正在依赖一套测试系统；他们应自然地相信游戏记得自己做过什么。无论经历普通选择、限时迟疑、无障碍等价输入、存档读档或回退，后来出现的反应、代价与结局都应与真实选择一致，不发生重复回收、遗漏回收、路线串线或“读档后因果变了”。这一间接幻想服务于“温柔必须被挣来”——系统必须证明善意、询问、替代决定与承担代价之间存在准确区别；也服务于“悲剧也是完整答案”——失败结局必须由可追溯的选择链产生，而不是随机性、隐藏故障或恢复状态污染。玩家最终获得的感受不是“系统通过了测试”，而是“这个故事诚实地记住了我”。

*Creative Director 未参与——Solo 模式；进入制作前需人工复核本节的情感表达。*

## Detailed Design

### Core Rules

1. **领域合同归属原系统**：每个 owning GDD 和实体注册表拥有自己的 schema、公式、常量、阈值及验收条件。SYS-TEST 只能引用、编排和验证这些合同，不得复制后修改，也不得通过 fixture 建立第二套权威。
2. **联合所有权、集中门禁**：各系统提供版本化生产 manifest、领域 fixtures、预期 oracle 和验收条件；SYS-TEST 统一提供 runner 编排、证据 schema、新鲜度验证、跨系统 fixtures、结果聚合及构建门禁。
3. **每项测试必须绑定稳定验收 ID**：每个自动化 case 必须映射到一个或多个已登记 criterion IDs；每个阻断性 criterion 必须映射到至少一个非空 case。未映射测试、重复 criterion、零 case 的 PASS、仅有总结而无原始结果均不得关闭门禁。
4. **证据类型保持精确**：SYS-TEST 接受现有合同使用的 `UT_PURE`、`UT_ENGINE`、`STATIC`、`INSTR`、`BRANCH`、`A11Y`、`VISUAL`、`BENCH`、`SPIKE`、`HUMAN`、`PLAYTEST` 与 `REVIEW`。不得把一种证据冒充另一种；例如 Python 单元测试不能替代 Ren'Py-hosted 恢复测试，自动化截图检查不能替代人工可理解性结论。
5. **三层执行门禁**：`FAST` 执行 lint、纯逻辑测试、schema/catalog 校验和静态扫描；`INTEGRATION` 执行 Ren'Py testcase、instrumentation、分支/恢复测试、故障注入、跨系统 joins 与无障碍交互遍历；`RELEASE` 执行完整合法路径和 terminal class 枚举、最大 fixtures、性能基准、视觉/无障碍矩阵、人工证据完整性、发行归档和测试资产排除。
6. **影响分析不能降低权威门槛**：`FAST` 与 `INTEGRATION` 可以按 source/catalog dependency graph 选择受影响套件；`RELEASE` 必须执行完整冻结 manifest。无法解析的动态引用、反射、字符串查找或依赖边必须扩大执行范围或直接失败，不能据此跳过测试。
7. **证据必须与输入精确绑定**：每份 artifact 必须记录 criterion、证据类型、scope、source/catalog/config hashes、fixture manifest、runner identity/version/hash、环境 identity、case/assertion IDs、期望与实际 case count、原始输出引用及 hash、exit code、状态和失败 IDs。任一权威输入或 runner 变化后，旧 PASS 立即成为 `STALE`。
8. **PASS 必须非空且可重放**：PASS 要求所有 required cases 实际执行、case count 与冻结 manifest 完全一致、exit code 为零、原始产物存在且 hash 匹配。空 manifest、过滤后零测试、异常被吞掉、仅保存摘要、缺失负例或 stale artifact 均固定失败。
9. **fixture 分区**：`Production-derived fixtures` 由批准的 production catalogs、CFG、schema 和稳定 IDs 生成；`Synthetic boundary fixtures` 用于极值、非法类型、容量上限、竞争顺序及故障注入。两者使用不同 namespace 并分别计数；synthetic 最大值不得冒充真实 production 可达最大值。
10. **测试与发行严格隔离**：Test observers、spies、fault injectors、protocol bombs、synthetic saves/roots、benchmark harness、测试目录替换器和 evidence forgers 只能存在于 test-only manifest。Production source 不得直接或传递依赖 test-only source；发行归档、store、persistent root 和正式 save payload 中相关对象计数必须为零。
11. **不得为测试修改生产语义**：禁止向 resolver、state、choice、save、persistent、achievement、Journal 或 tension 公共 API 添加 catalog 注入、可变全局替换、跳过验证、强制成功或任意状态写入 seam。需要隔离非法 catalog 时，只能调用已批准的纯 validator、隔离模块初始化或 test-only engine adapter。
12. **确定性与离线执行**：自动化门禁不得依赖网络、遥测、墙钟日期、随机结果或执行顺序。需要时间行为时使用批准的单调时钟 fixture 和显式 event sequence；benchmark 使用冻结真实计时协议，但性能结果不得改变游戏语义。
13. **失败即停止错误声明，不隐藏后续诊断**：单个 validator 必须遵守所属合同的固定错误优先级；suite runner 可继续执行独立 cases 以收集诊断，但最终 gate 只要存在 required failure、runner error、missing input 或 stale evidence 就必须失败。
14. **组件通过不等于集成通过**：上游内容尚未冻结时，可以使用 isolated fixtures 证明 schema、纯函数或状态机组件正确，但 artifact 必须标记为 component scope。它不能关闭 production catalog、跨系统 integration、performance 或 release gate。
15. **人工证据只做完整性校验**：SYS-TEST 可以验证 `HUMAN`、`PLAYTEST`、`VISUAL` 与 `REVIEW` artifact 是否具备批准的 rubric、参与者或 reviewer 元数据、原始回答/captures、分组结果和裁定；不得自动生成审美、叙事理解或玩家感受的 PASS 结论。
16. **证据协议先于执行门禁**：所有 FAST、INTEGRATION 与 RELEASE suite 必须引用已冻结的 `test_evidence_bundle:v1`、scope、criterion-to-case 映射和 artifact 状态词汇；协议缺失时只能产生 `BLOCKED_INPUT`，不得运行后凭摘要补齐协议。
17. **禁止自动接受当前输出为 golden**：Golden vectors、截图基线、目录 hashes 和路径 oracle 的变更必须显示差异并经 owning system 批准。Runner 不得以“更新快照”方式把当前失败输出自动改为期望值。

### States and Transitions

| State | 含义 | 合法转换 |
|---|---|---|
| `UNBOUND` | criterion 尚无有效 manifest 或没有非空 case 映射 | manifest 完成且重新预检通过 → `READY`；仍缺外部输入 → `BLOCKED_INPUT` |
| `BLOCKED_INPUT` | 缺少批准 catalog、engine capability、人工 artifact 或其他必需输入 | 输入补齐并重新预检通过 → `READY`；输入仍缺失则保持阻断 |
| `READY` | manifest、fixtures、runner 和环境预检均有效 | → `RUNNING` |
| `RUNNING` | cases 正在执行，尚无最终门禁结论 | assertion/runner/cleanup失败 → `FAILED`；输入 identity 改变 → `STALE`；全部 required cases 成功 → `PASSED_CURRENT` |
| `FAILED` | assertion、runner、case-count、hash、exit-code 或完整性检查失败 | → `READY` |
| `PASSED_CURRENT` | 全部 required evidence 对当前输入有效 | → `STALE` |
| `STALE` | source、catalog、config、fixture、runner 或环境 identity 已改变 | → `READY` |

`GATE_ACCEPTED` 不作为可手工写入的生命周期状态；它只能由当前 scope 的全部 required criteria 均为 `PASSED_CURRENT`、required artifact 非空且 unresolved blocking findings 为空时派生。进程中止留下的 `RUNNING` 不得恢复为 PASS，下次读取时按 `FAILED` 处理并重新运行。`BLOCKED_INPUT` 是 criterion/gate 的阻断结果，不是成功结果；`REPORT_ONLY` 是 artifact result，只能保存诊断数据，永远不能关闭 required criterion。

### Interactions with Other Systems

| 系统 | 输入到 SYS-TEST | SYS-TEST 输出 | 所有权边界 |
|---|---|---|---|
| Ren'Py 8.5.3 / Python 3.12 | testcase、lint、存档/persistent、focus、自发声、interaction restart 与计时能力 | version-pinned capability traces、runner结果、spike与benchmark artifacts | SYS-TEST 不重新定义 engine API；未验证能力保持阻断 |
| SYS-STATE | schema、choice projections、原子替换、快照与纯度合同 | component、engine、static、branch及内容覆盖证据 | 五轴、token和验证优先级仍归 SYS-STATE |
| SYS-ENDING | 六个 canonical vectors、boundary fixtures、resolver records、terminal class合同、`ending_completion_event_record` | 唯一性、互斥性、purity、完整路径枚举、completion callsite、save/rollback 与性能证据 | predicate、priority、cause identity、completion ownership归 SYS-ENDING |
| SYS-CHOICE | source manifest、compiled catalogs、joins、CFG/DAG、恢复点与内容预算 | join negatives、continuation coverage、恢复 traces及compiler benchmark | SYS-TEST 不注册 production choice或替换 catalog |
| SYS-NARRATIVE | production records、canonical CFG、witnesses、oracle records与内容 hashes | 全图枚举、路线/回收覆盖、恢复与内容集成 artifacts | 文案、选择及因果内容归 SYS-NARRATIVE |
| SYS-SAVE | load classifier、checkpoint catalog、action gates、save contracts | 四恢复点、重复载入、损坏/不兼容、I/O failure、hitch及production-isolation证据 | SYS-TEST instrumentation 不进入正式存档 |
| SYS-PERSIST | schema-v2 root、12-leaf manifest、batch/merge/reset/flush与epoch合同 | merge permutation、failure injection、invariance、projection及性能证据 | Persistent 写入和恢复策略归 SYS-PERSIST |
| SYS-ACHIEVE | 11项 catalog、snapshot、condition、backend与presentation合同 | golden/negative vectors、epoch/reset/merge、queue、backend和UI证据 | SYS-TEST 不授予、撤销或伪造成就 |
| SYS-JOURNAL | bundle、detached snapshot、read model、focus、seen receipt及failure surfaces | 0/max列表、read-model、focus、refresh、recovery、layout和performance证据 | SYS-TEST 不构造 production 玩家摘要 |
| SYS-ACCESS | mode sets、字体/对比/动效设置、semantic focus、transcript与替代表达合同 | keyboard walk、TTS transcript、布局矩阵、单通道移除和恢复证据 | SYS-TEST 不创建第二套无障碍语义 |
| SYS-TENSION | post-MVP scene manifest、状态机、计时公式、暂停区间、竞争优先级与timeout choice | post-MVP 时钟、暂停、同刻竞争、唯一dispatch、恢复及negative fixtures | 不属于当前 P0 Production gate；SYS-TEST 不修改时间或提交 choice |
| SYS-BUILD | `candidate_manifest:v1`、staging/archive inventory、candidate identity、archive hash 与两阶段请求 | 同世代 `test_evidence_bundle:v1`、`STAGING_EVIDENCE_BOUND`/`ARCHIVE_EVIDENCE_BOUND`、staging/archive exclusion reports | SYS-BUILD拥有 candidate/archive manifest 与 package bytes；SYS-TEST拥有 evidence/result/scan artifact；双方不得修改对方产物 |

系统索引已把 SYS-STATE、SYS-NARRATIVE 与 SYS-ACCESS 加入 SYS-TEST 的显式当前依赖；SYS-TENSION 的 timed-choice suite 标为 post-MVP，不属于当前 P0 Production 依赖；SYS-BUILD 与 SYS-TEST 通过 `candidate_manifest:v1`、两阶段 evidence 与双向 exclusion report 形成当前 P0 release-hard 双向依赖。

*Systems Designer、Gameplay Programmer 与 Engine Programmer 未参与——Solo 模式。Ren'Py testcase CLI、原子写入故障注入、persistent callback、计时、焦点、自发声及 interaction restart 的具体机制必须由版本固定的 spike/ADR 和人工技术复核关闭。*

## Formulas

The `test_artifact_current` formula is defined as:

`test_artifact_current = exact_identity_keys ∧ identity_generation_match ∧ all_identity_hashes_match ∧ raw_output_present ∧ raw_output_hash_matches`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---:|---|---|---|
| Required identity keys | `K_r` | exact tuple[str] | `1–N` | 当前 manifest 要求的 schema generation、criterion、evidence type、scope/gate tier、case/fixture/oracle、source、catalog、config、runner、environment、protocol、threshold及capture字段 |
| Artifact identity keys | `K_a` | exact tuple[str] | `0–N` | artifact 实际保存的字段 |
| Recorded identity hash | `h_a(k)` | SHA-256 string | 64 lowercase hex chars | artifact 对字段 `k` 保存的完整 hash |
| Current identity hash | `h_c(k)` | SHA-256 string | 64 lowercase hex chars | 对当前权威输入重新计算的完整 hash |
| Recorded raw-output hash | `h_a(raw)` | SHA-256 string | 64 lowercase hex chars | artifact 声明的原始输出 hash |
| Current raw-output hash | `h_c(raw)` | SHA-256 string | 64 lowercase hex chars | 对现存原始输出重新计算的 hash |
| Recorded identity generation | `g_a` | exact string | non-empty | artifact 所属的冻结输入世代 |
| Current identity generation | `g_c` | exact string | non-empty | 当前 manifest 的冻结输入世代 |
| Raw output presence | `raw_output_present` | exact bool | `False/True` | 原始输出文件/记录存在且可读取 |

`exact_identity_keys = (K_a = K_r)`；`identity_generation_match = (g_a = g_c)`；`all_identity_hashes_match = ∀k∈K_r, h_a(k)=h_c(k)`。Identity records 按 UTF-8 key bytes 排序并使用长度前缀编码；文件输入使用 exact file bytes，结构化输入使用其 owning schema 的 canonical encoding。时间戳不参与身份计算。`raw_output_present=False` 或原始输出为空时不得计算为 current。

**Output Range:** exact `False` 或 `True`；任一缺失、额外或不匹配字段均为 `False`。
**Example:** 所有 required identity、generation 和 raw output 全部 exact-match 时输出 `True`；runner hash 改变一个字符后输出 `False`，旧 artifact 转为 `STALE`。

---

The `test_criterion_pass` formula is defined as:

`test_criterion_pass = nonempty ∧ exact_case_set ∧ evidence_coverage ∧ all_artifacts_current ∧ all_artifacts_passed ∧ no_blocking_findings`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---:|---|---|---|
| Required artifact set | `A_c` | exact tuple[artifact] | `0–N` | criterion `c` 的全部 required artifacts |
| Expected case count | `n_e` | exact int | `1–N` | 冻结 manifest 声明的 case 数 |
| Executed case count | `n_x` | exact int | `0–N` | 实际执行且产生原始结果的 case 数 |
| Required case IDs | `I_e` | exact set[case_id] | `1–N` | 冻结 manifest 要求执行的 case 集合 |
| Executed case IDs | `I_x` | exact set[case_id] | `0–N` | 实际产生原始结果的 case 集合 |
| Required evidence types | `E_r` | exact set[enum] | `1–12` | owning criterion 要求的证据类型 |
| Present evidence types | `E_a` | exact set[enum] | `0–12` | 当前 artifacts 实际提供的证据类型 |
| Artifact current result | `C(a)` | exact bool | `False/True` | `test_artifact_current(a)` |
| Artifact result | `P(a)` | enum | `PASS/FAIL/ERROR/REPORT_ONLY` | runner 记录的结果；PASS 同时要求 exit code `0`，`REPORT_ONLY` 不可关闭 required criterion |
| Blocking finding count | `b` | exact int | `0–N` | 未解决的阻断 finding 数 |

`nonempty = |A_c|≥1`，`exact_case_set = (I_x=I_e) ∧ (|I_x|=n_x=n_e>0)`，`evidence_coverage = (E_a=E_r)`。额外 evidence type 也必须先被 criterion manifest 明确批准，否则不能参与聚合。

**Output Range:** exact `False` 或 `True`；缺少 required 外部输入时另记录 `criterion_status=BLOCKED_INPUT`，但该公式仍输出 `False`；不使用通过率或人工覆盖。
**Example:** 某 criterion 要求 `UT_ENGINE + INSTR`，两个 artifact 均 current/PASS、12个预期 case 全部执行且 `b=0`，输出 `True`；缺少 `INSTR` 时输出 `False`。

---

The `test_gate_pass` formula is defined as:

`test_gate_pass = nonempty_required_criteria ∧ all_required_criteria_pass ∧ no_blocked_inputs ∧ no_stale_artifacts ∧ no_unresolved_blocking_findings`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---:|---|---|---|
| Required criteria | `R_g` | exact tuple[criterion_id] | `1–N` | 当前 `FAST`、`INTEGRATION` 或 `RELEASE` scope 的冻结验收 ID |
| Criterion result | `P(c)` | exact bool | `False/True` | `test_criterion_pass(c)` |
| Blocked input count | `i_b` | exact int | `0–N` | 缺失 engine capability、catalog或外部证据输入 |
| Stale artifact count | `a_s` | exact int | `0–N` | 当前 scope 中过期 artifact 数 |
| Global blocking finding count | `b_g` | exact int | `0–N` | 当前 scope 中未绑定或未解决的 blocking finding 数 |

`test_gate_pass = (|R_g|>0) ∧ (∀c∈R_g, P(c)) ∧ (i_b=0) ∧ (a_s=0) ∧ (b_g=0)`。任何未绑定 criterion 的 blocking finding 也计入 `b_g`，不得因没有所属 criterion 而从 gate 中消失。

**Output Range:** exact `False` 或 `True`；只有 `True` 可派生 `GATE_ACCEPTED`。
**Example:** 一个包含43项成就 criteria 的 integration scope 中，43项全为 current PASS、无阻断输入、无 stale artifact 且无全局 unresolved blocker 时输出 `True`；其中一项缺少原始 artifact 或存在未绑定 blocker 时输出 `False`。

---

The `test_impacted_suites` formula is defined as:

`test_impacted_suites = all_tier_suites if unresolved_edge_count > 0 else suites_reached_by_impact_closure`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---:|---|---|---|
| Dependency graph | `D=(V,E)` | directed graph | finite | source、catalog、system、suite及gate之间的版本化依赖图 |
| Changed nodes | `Δ` | exact set[node_id] | `0–|V|` | 当前变更的权威输入；空集表示无受影响套件 |
| Tier suites | `S_t` | exact set[suite_id] | `1–N` | 当前 FAST 或 INTEGRATION 层的全部套件 |
| Transitive reachable nodes | `Reach⁺(Δ)` | exact set[node_id] | `0–|V|` | 从变更节点沿依赖方向得到的传递闭包，不含节点自身 |
| Impact closure | `Reach*(Δ)` | exact set[node_id] | `0–|V|` | `Δ ∪ Reach⁺(Δ)`，包含直接变更节点 |
| Suite inputs | `Inputs(s)` | exact set[node_id] | `1–N` | 套件 `s` 声明的全部直接输入 |
| Unresolved edge count | `u` | exact int | `0–N` | 动态、反射或无法静态归属的依赖边数 |

当 `Δ=∅` 且 `u=0` 时输出空集；当 `u=0` 且 `Δ≠∅` 时，输出 `{s∈S_t | Inputs(s) ∩ Reach*(Δ) ≠ ∅}`；当 `u>0` 时输出完整 `S_t`。依赖边方向固定为“权威输入 → 消费者”。`RELEASE` 不调用影响裁剪，始终运行完整 release manifest。

**Output Range:** `0–|S_t|` 个稳定 suite IDs；输出按 UTF-8 ID bytes 排序。
**Example:** 一个变更节点经已登记依赖到达三个 integration suites 时输出这三个 ID；出现一条未解析动态依赖后输出该层全部 suites。

---

The `test_nearest_rank_percentile` formula is defined as:

`Q_p(X) = sort(X)[ceil(p × |X|) - 1]`，其中 `p` 使用规范化有理数并以整数运算完成 `ceil`。

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---:|---|---|---|
| Raw samples | `X` | exact tuple[finite number] | `1–N` | 未过滤的合法原始样本 |
| Percentile | `p` | canonical rational pair | `(0,1]` | owning GDD 或批准 protocol 要求的 percentile；禁止依赖语言相关浮点序列化 |
| Sample count | `n` | exact int | `1–N` | `|X|` |
| Rank | `r` | exact int | `1–n` | `ceil(p×n)` |

NaN、正负无穷、错误类型、缺失样本、样本不足或未经批准的过滤都会使 protocol validation 失败，不产生 PASS percentile。

**Output Range:** `min(X)–max(X)`。
**Example:** `n=30`、`p=0.95` 时读取升序样本的第29项。

---

The `test_performance_pass` formula is defined as:

`test_performance_pass = protocol_valid ∧ nonempty_approved_thresholds ∧ all_metric_comparisons_pass`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---:|---|---|---|
| Protocol validity | `V_p` | exact bool | `False/True` | hardware、build、timer、GC、cache、warm-up、样本数及统计方法完整有效 |
| Approved comparisons | `T` | exact tuple[comparison] | `0–N` | owning GDD 批准的 metric/operator/threshold 记录 |
| Measured metric | `m_i` | finite number | owning metric range | 原始样本按批准方法得到的结果 |
| Comparison operator | `op_i` | enum | `<, ≤, =, ≥, >` | owning GDD 批准的比较符 |
| Approved threshold | `τ_i` | finite number | owning GDD range | SYS-TEST 不得修改的阈值 |

`test_performance_pass = V_p ∧ (|T|>0) ∧ ∀i, op_i(m_i,τ_i)`。没有批准阈值时可以生成带原始样本的 `REPORT_ONLY` artifact，但输出不得为 PASS。

**Output Range:** exact `False` 或 `True`。
**Example:** owning GDD 要求 p95≤2 ms、max≤5 ms，测得1.7 ms和4.2 ms且 protocol valid时输出 `True`；阈值缺失时不能宣称 PASS。

*Systems Designer 未参与——Solo 模式；公式在进入制作前需人工验证，尤其是 canonical identity encoding、依赖图闭包和 benchmark protocol。*

### Evidence Bundle v1 Baseline

`test_evidence_bundle:v1` 在实现前必须由 Architect、SYS-TEST 与 owning system 共同冻结。每个 gate manifest 必须包含：`bundle_schema_version`、`run_id`、`scope`（`component`/`FAST`/`INTEGRATION`/`RELEASE`）、`criterion_id`、`owner_system`、`suite_id`、`expected_case_ids`、`executed_case_ids`、`fixture_manifest_id`、`oracle_id`、`matrix_cell_ids`、`expected_case_count`、`required_evidence_types`、`identity_generation`、`source/catalog/config/fixture/runner/environment` identity、`source_inventory_id/hash`、`protocol_manifest_id/hash`、`threshold_manifest_id/hash`、runner version/hash、capture protocol、provider approval、canonical relative artifact path、原始输出引用及 hash、exit code、artifact result、failure/finding IDs 和生成时间。

每个 criterion 必须有一个且仅一个冻结 mapping record；该 record 将 criterion 映射到非空 case IDs、fixture IDs、oracle/expected-output IDs 和 scope。`expected_case_ids` 与 `executed_case_ids` 必须集合完全相等，`expected_case_count` 必须等于两者数量且大于零，case、fixture、oracle、matrix cell 与 artifact ID 在 bundle 内唯一。跨 identity generation 的 artifact 不得拼接。

### SYS-BUILD 双向 Evidence 阶段

SYS-TEST 与 SYS-BUILD 的 RELEASE evidence 只允许按以下两个阶段封板：

1. `STAGING_EVIDENCE_BOUND`：SYS-BUILD 提供 `candidate_manifest:v1`、staging inventory、`candidate_identity`、RELEASE manifest、runner/environment identity 与 source/catalog/config hashes；SYS-TEST 返回非空 current `test_evidence_bundle:v1`、完整 case mapping 与 `staging_exclusion_report:v1`。
2. `ARCHIVE_EVIDENCE_BOUND`：SYS-BUILD 提供最终 archive inventory 与 `archive_hash`；SYS-TEST 返回绑定该 hash 的 final RELEASE evidence 与 `archive_exclusion_report:v1`。

两阶段均要求 `candidate_identity`、`identity_generation`、fixture、runner、environment 和原始输出 hash exact-match；第二阶段额外要求 `archive_hash` exact-match。SYS-BUILD 只能在第一阶段通过后运行 package runner，只有两阶段都通过才可宣称 `READY`。SYS-TEST 拥有 evidence/result/exclusion artifact，SYS-BUILD 拥有 candidate/archive manifest；不得互相改写，也不得用 component PASS 替代任一 RELEASE 阶段。

Artifact 只能使用以下状态：`PASS`、`FAIL`、`ERROR`、`REPORT_ONLY`。Criterion/gate 另有 `UNBOUND`、`BLOCKED_INPUT`、`READY`、`RUNNING`、`FAILED`、`PASSED_CURRENT`、`STALE` 生命周期状态；二者不得混用。并发运行必须先以唯一 `run_id` 隔离写入，再通过原子封板锁验证同一 identity 下是否已有完整 artifact；若出现两个完整候选，不得任意选择，必须报告 duplicate-finalization 并使 criterion 失败。

外部证据的 `BLOCKED_INPUT` 必须带 reason code：`UNVERIFIED_NONVISUAL`（只有 transcript/trace，未完成 capability preflight 或真实听测）或 `ADJUDICATION_REQUIRED`（原始回答/capture 存在但没有批准 reviewer 裁定）。这两种 reason code 都不能由多数票、分数或自动截图结果升级为 PASS。

### Benchmark, Matrix, and Resource Baselines

`benchmark_protocol:v1` 必须包含参考硬件、Windows build、renderer、Python/Ren'Py 版本、timer、GC/cache/warm-up、sample count、canonical percentile encoding、metric/operator/threshold records 和 raw-sample policy；protocol 与 threshold manifest 的 hash 必须参与 artifact identity。`p` 使用规范化有理数 `(numerator, denominator)` 表示，`ceil(p×n)` 以整数运算完成；必须覆盖 `n=1`、`p=1/n`、`1/n±ε` 和 `p=1` 边界。

FAST 的 `fast_gate_feedback_target_seconds` 是工作流目标，不是无限等待许可。每个 suite 必须有批准的 hard timeout、最大内存、最大磁盘和最大 raw-output 配额；超限必须终止该 suite，产生 `TIMEOUT`/`ERROR` artifact 并使 scope 失败。不得把超限仅记为 warning。

RELEASE 的完整性由 versioned source inventory、graph inventory、terminal-path count、terminal-class count、maximum fixture manifest 和 replay-closure hash 证明；实际 inventory 与 manifest 必须 exact-match。A11Y/VISUAL 必须由显式矩阵生成 case，至少覆盖 1280×720 与 1920×1080、批准字体档位、对比度、reduced-motion/flash/shake、self-voicing/muted、production surface/state 和 0/max/longest-copy cells。TTS 证据必须区分 expected transcript、observed speech trace、capability preflight 与 human listening adjudication；无可用 SAPI 或语音能力时不得宣称非视觉 PASS。

### Criterion Traceability Baseline

`TEST-EVID-006` 的 traceability index 必须从 `design/registry/entities.yaml` 的实际解析结果生成，不使用手填数量。每个 `referenced_by: SYS-TEST` 条目必须解析到至少一个 criterion 或 owner-approved external-evidence mapping；未解析条目、owner 漂移和 value drift 都是 STATIC failure。当前工作树的原始文本扫描为 204 处 `SYS-TEST` 引用，但该数字不是规范值，正式结果必须由 YAML parser 输出唯一 entity count。

## Edge Cases

- **If required manifest 不存在、为空或解析后没有 criterion**：对应 scope 进入 `UNBOUND`，`test_gate_pass=False`；不得生成 PASS artifact。只有 manifest 有效但缺少批准 catalog、engine capability、人工 artifact 或其他外部输入时，才进入 `BLOCKED_INPUT`。
- **If test filter、tag、平台条件或错误 discovery 使 required case count 变为0**：该 criterion 固定 `FAILED`；“没有测试需要运行”不能视为成功。
- **If 实际发现的 case 多于或少于冻结 manifest**：按 exact case-count mismatch 失败；额外 case 也不得静默执行后忽略。
- **If criterion ID、case ID、artifact ID 或 suite ID 重复**：预检失败，在任何 case 执行前停止该 scope，列出全部冲突位置。
- **If required case 被 skip、xfail、disabled 或 quarantine**：该 case 不计为执行成功，criterion 固定失败；只有 owning GDD 正式移除 requirement 后才能解除。
- **If runner、Ren'Py 进程或宿主进程在执行中崩溃/被终止**：保留 partial raw output 仅作诊断，将 artifact result 记为 `ERROR`、生命周期记为 `FAILED`；残留 `RUNNING` 状态不得恢复为 PASS。
- **If source、catalog、config、fixture、runner 或 environment identity 在执行期间变化**：本次全部结果标记 `STALE`，重新预检并完整运行受影响 scope；不得只重跑失败项。
- **If 两个运行并发写入同一 criterion**：各自使用唯一 run ID和隔离输出目录；只有输入 identity 完全相同且单个运行原子封板的 artifact 可参与门禁，不执行 last-writer-wins。
- **If 不同 source/catalog hashes 的 artifacts 分别覆盖同一 criterion 的不同证据类型**：禁止拼接；criterion 失败并要求在同一冻结 identity 下重跑全部 required evidence。
- **If 相同 identity、fixture 和 runner 出现 PASS/FAIL、不同输出或不同 case order结果**：标记为 non-deterministic/flaky，当前门禁失败。诊断性重复运行不覆盖首次失败，直到原因修复并生成新的 runner或source identity。
- **If artifact 声称 PASS 但 exit code 非0、runner exception非空或 raw output包含未处理错误**：artifact 状态强制为 `ERROR`，声明的 PASS 被拒绝。
- **If raw output、capture、trace、sample或其 hash 缺失/不匹配**：artifact 无效并进入 `FAILED`；摘要和日志摘录不能替代原始产物。
- **If required HUMAN、PLAYTEST、VISUAL、REVIEW 或 engine capability证据尚未提交**：仅相关 criterion与依赖它的 gate进入 `BLOCKED_INPUT`；不依赖它的独立 FAST/INTEGRATION scope可以继续，但不能据此宣称更高层 gate通过。
- **If 人工 reviewers 或 playtest编码结果相互冲突**：SYS-TEST 保存全部原始结果与 adjudication缺口，将对应 finding保持阻断；不得自动选择多数结果或生成主观PASS。
- **If performance protocol有效但 owning GDD 尚无批准阈值**：生成 `REPORT_ONLY` artifact并保存原始样本；`test_performance_pass=False`，不得使用临时阈值。
- **If benchmark samples含NaN、正负无穷、负时长、错误类型、缺失值、样本不足或未经批准的过滤**：整个 metric失败，不计算替代 percentile，也不丢弃异常值后重算。
- **If benchmark、视觉或无障碍矩阵缺少任一冻结环境组合**：对应 criterion失败；高分辨率通过不能替代1280×720、最大字体或目标Windows环境。
- **If production-derived 与 synthetic fixtures 使用相同ID、namespace或报告分组**：fixture manifest validation失败；必须拆分后重跑，不能用synthetic上限声称production最大路径已覆盖。
- **If production catalog 超出 owning GDD 的容量或terminal-class预算**：构建门禁失败；SYS-TEST不得缩减catalog、合并class或只测试可接受子集。
- **If golden vector、截图基线、路径oracle或catalog hash与当前输出不同**：产生显式差异并失败；只有owning system批准新权威后才生成新identity，禁止自动更新expected。
- **If dependency graph出现动态导入、反射、字符串查找或未解析边**：FAST/INTEGRATION扩大到该层完整套件；若仍无法证明production/test隔离或影响边界，则门禁失败。
- **If RELEASE运行尝试应用影响裁剪**：预检拒绝配置并运行完整release manifest；无法运行完整manifest时release gate失败。
- **If production source直接或传递依赖test-only source**：静态门禁失败并报告完整依赖路径；删除归档文件不能掩盖production source违规。
- **If release archive、store、正式save或persistent root发现observer、spy、fault injector、protocol bomb、synthetic root/save、benchmark harness或evidence forger**：release gate立即失败，相关计数必须恢复为0后完整重跑。
- **If engine版本、Python版本、renderer、Windows build或批准环境不匹配**：依赖该环境的artifact进入 `STALE` 或 `BLOCKED_INPUT`；其他版本的成功结果不能复用。
- **If test-only save/persistent故障注入污染后续case的磁盘、root、backend或rollback状态**：当前case失败并执行批准的隔离清理；清理验证不通过时停止整个suite，后续case不得运行。
- **If cleanup本身失败或无法证明fixture恢复到基线**：artifact result 为 `ERROR`、运行生命周期为 `FAILED`，所有后续结果无效；不得把测试断言通过与清理失败拆开计算。
- **If waiver、人工备注或“已知问题”试图覆盖required failure**：`test_gate_pass`结果不变。要解除阻断，必须由owning GDD正式修改criterion或scope并产生新的权威hash。
- **If 测试系统收到超出 schema 的类型、范围、字段或状态值**：按该输入所属 validator 的固定错误优先级失败；不得规范化、截断或补默认值后继续。
- **If 系统时区、locale、文件枚举顺序或路径分隔符变化导致结果不同**：标记为non-deterministic并失败；canonical UTF-8排序、稳定IDs及规范化路径必须使语义结果一致。

*Systems Designer 未参与——Solo 模式；进入制作前需对 flaky、并发封板、进程中止和故障注入清理策略进行人工对抗复核。*

## Dependencies

| Dependency | Strength / Direction | Required Interface | Current Status / Gate |
|---|---|---|---|
| Ren'Py 8.5.3 / Python 3.12 | Hard toolchain / Engine → SYS-TEST | `engine-capability-manifest:v1`、`testcase`、lint、Python `unittest`、进程退出码、save/persistent、focus、自发声、interaction restart与计时能力 | runner capability manifest 已冻结；CLI/故障注入/部分运行时能力仍需实现前复跑与对应 evidence |
| Entity Registry | Hard authority / Registry → SYS-TEST | SYS-TEST引用的schema、公式、常量、调节项、source owner和`referenced_by`关系 | 数量由 YAML parser 和 registry generation 生成；当前工作树原始文本扫描为204处引用，非规范常量；任何冲突先修订owner，不在测试中覆盖 |
| ADR-0001 / 0004 / 0005 / 0006 | Hard architecture / ADR → SYS-TEST | resolver纯度、detached snapshot、九阶段观测、ending completion event、test-only AST/instrumentation与生命周期验证边界 | Accepted；SYS-TEST不得增加production seam |
| ADR-0002 | Hard architecture / ADR → SYS-TEST | rollback-owned状态与persistent边界、12-leaf authority、public `APPLIED_FLUSHED`、unsupported/corrupt load安全流程 | Accepted；engine evidence仍有下游门槛 |
| ADR-0003 | Hard source boundary / ADR → SYS-TEST | chapter/content/presentation分离、稳定资源名与test-only source隔离 | Accepted |
| SYS-STATE | Hard direct verification / SYS-STATE → SYS-TEST | state schema、choice projections、counterevidence、snapshot、purity policy、component/engine/content criteria | Approved；生产内容joins仍由下游集成关闭 |
| SYS-ENDING | Hard direct verification / SYS-ENDING → SYS-TEST | 六个canonical vectors、boundary fixtures、resolver records、terminal classes、唯一 completion callsites/event、purity与性能合同 | Approved with provisional downstream gates；完整production路径和benchmark待SYS-TEST关闭 |
| SYS-CHOICE | Hard direct verification / SYS-CHOICE → SYS-TEST | source manifest、compiled catalogs、join reports、CFG/DAG、continuation、恢复点和内容预算 | Approved with provisional downstream gates；生产catalog与最大图证据尚未冻结 |
| SYS-NARRATIVE | Hard direct content validation / SYS-NARRATIVE → SYS-TEST | production records、canonical CFG、witnesses、acceptance oracle、terminal classes、恢复位置和内容hashes | In Revision；不阻止isolated组件测试，阻止production integration/content-lock |
| SYS-SAVE | Hard direct engine integration / SYS-SAVE → SYS-TEST | load分类、save/catalog sentinels、四恢复点、action gates、I/O failure与performance protocol | In Revision；Q1/Q2/Q4/Q5/Q7分别阻止相关engine、catalog、performance和architecture证据 |
| SYS-PERSIST | Hard direct engine integration / SYS-PERSIST → SYS-TEST | schema-v2 root、12-leaf manifest、batch、flush、merge/reset、epoch、ending completion projection和safe recovery | In Revision；P0 shared-contract blockers closed，Q1/Q2/Q5仍为implementation evidence gates |
| SYS-ACHIEVE | Hard direct validation / SYS-ACHIEVE → SYS-TEST | 11项catalog、event/witness catalogs、snapshot、condition、backend、queue、seen与UI合同 | Approved；backend、UI/audio与performance仍是implementation gates |
| SYS-JOURNAL | Hard direct UI/data integration / SYS-JOURNAL → SYS-TEST | catalog bundle、detached snapshot、read model、focus、mark-seen receipt、failure surfaces和evidence accumulator | In Revision；engine spike、layout与performance证据未完成 |
| SYS-ACCESS | Hard direct cross-cutting validation / SYS-ACCESS → SYS-TEST | mode-set、五项project settings、键盘、TTS、semantic focus、字体/对比/动效矩阵及恢复合同 | Designed；完整复审、engine spike与production evidence待完成 |
| SYS-TENSION | Post-MVP optional-feature validation / SYS-TENSION → SYS-TEST | scene/eligibility manifests、状态机、绝对时间、暂停区间、竞争顺序、唯一dispatch和恢复合同 | Deferred；不属于当前 P0 Production gate |
| QA / UX / Art / Playtest evidence providers | Conditional hard input / External evidence → SYS-TEST | 批准rubric、captures、transcripts、参与者/评审元数据、原始结果与adjudication | 不参与自动判定；仅在criterion明确要求时阻止对应gate |
| SYS-BUILD | Hard bidirectional release consumer / SYS-TEST ⇄ SYS-BUILD | SYS-BUILD 提供 `candidate_manifest:v1`、staging/archive inventory、candidate identity 与 archive hash；SYS-TEST 返回同世代 `test_evidence_bundle:v1`、`STAGING_EVIDENCE_BOUND`/`ARCHIVE_EVIDENCE_BOUND` 和两份 exclusion report | ADR-0007 已冻结接口；实现前只能生成 component/integration evidence，必须完成 staging 与 archive 两阶段后才能关闭 RELEASE |

### Interface Boundary

所有跨系统输入均为 immutable、versioned、source-hash-bound manifest、fixture、catalog、trace或raw artifact。SYS-TEST 不通过运行时callback查询内部状态，不持有live Ren'Py store对象，不替换production catalog，也不向生产API加入注入入口。需要观测运行时行为时，使用test-only adapter、engine testcase或已批准instrumentation，并由 staging 与 final archive 两次扫描证明它们未进入production dependency closure。SYS-BUILD 先提供 candidate/staging identity，SYS-TEST 返回 staging evidence；SYS-BUILD 生成 archive 后再提供 archive hash，SYS-TEST 返回 final evidence。任何一方不得修改另一方 artifact。

### Required Ordering

1. Owning GDD、ADR和注册表冻结行为合同。
2. Owning system提交非空criterion/fixture/source manifest。
3. SYS-TEST运行FAST组件与静态门禁。
4. Engine capability spike和production catalogs可用后运行INTEGRATION。
5. 人工、视觉、无障碍与benchmark协议提交后运行其对应门禁。
6. Production内容、环境和release candidate冻结后运行完整RELEASE。
7. SYS-BUILD先从冻结 staging tree 生成唯一 candidate identity；SYS-TEST 返回 `STAGING_EVIDENCE_BOUND` 后 SYS-BUILD 才能运行 package runner；archive 生成后 SYS-TEST 返回 `ARCHIVE_EVIDENCE_BOUND`。任一 source/catalog/config/fixture/runner/environment/archive hash变化都要求新 run 与重新验证。

### Bidirectional Consistency Requirements

- 系统索引已列出`SYS-STATE + SYS-NARRATIVE + SYS-ACCESS`为SYS-TEST依赖；后续只维护双向关系，不得重复添加第二套依赖权威。
- SYS-BUILD 已把 `candidate_manifest:v1`、两阶段 release evidence 与 staging/archive exclusion 列为硬输入；SYS-TEST 只接受同世代 candidate/archive identity。
- SYS-STATE、SYS-NARRATIVE和SYS-ACCESS已经把SYS-TEST列为验证方；补充索引后关系才双向一致。
- 上游GDD处于In Revision不阻止SYS-TEST设计或isolated component evidence，但对应production integration、content-lock和release criterion保持`BLOCKED_INPUT`。
- 任一依赖要求改变owning formula、schema、threshold、lifecycle或error precedence时，必须先修订owning GDD/ADR/registry，再生成新的test identity；不得由测试fixture反向定义产品行为。`candidate_identity` 不吸收 archive/manifest/provenance final hashes，`archive_hash` 只覆盖 ZIP exact bytes，避免自引用。

## Tuning Knobs

| Knob | Type | Target | Safe Range | Too Low | Too High |
|---|---|---:|---:|---|---|
| `diagnostic_repeat_count` | exact int | `3` | `2–10` | 难以收集足够的重复轨迹来定位非确定性 | 延长诊断时间并扩大原始artifact数量；仍不得把偶然通过转为PASS |
| `current_artifact_retention_generations` | exact int | `10` | `3–50` | 缺少跨输入世代的回归和flaky对比证据 | 增加本地存储与审计成本；正式release bundle不受该值影响 |
| `fast_gate_feedback_target_seconds` | exact int，工作流目标 | `120` | `30–300` | 持续产生无意义警告，诱发过度拆分suite | 反馈过慢，开发者更晚发现schema、lint和纯逻辑问题 |

### Knob Interactions

- 提高`diagnostic_repeat_count`会增加FAST/INTEGRATION耗时及每个世代的artifact数量。
- `diagnostic_repeat_count × current_artifact_retention_generations`共同决定诊断证据的主要存储规模。
- `fast_gate_feedback_target_seconds`只能触发suite拆分或调度优化建议；不得自动降低repeat count、retention、case count或证据类型。
- Release evidence、批准的human/playtest记录及用于公开版本追溯的原始样本不由generation retention自动删除。

### Locked Invariants — Not Tuning Knobs

以下行为不可配置：strict-AND门禁、完整SHA-256 exact-match、required criterion与case非空、required skip失败、证据类型不可替代、production/test隔离、golden变更需批准、RELEASE完整运行、owning GDD阈值权威，以及flaky诊断通过不得覆盖失败。

## Visual/Audio Requirements

- SYS-TEST 不新增玩家可见资产、角色演出或专属音乐。
- 视觉证据仅包括测试截图、视频帧、布局捕获、焦点轨迹和对比度/字体矩阵；所有文件使用稳定 ID、source hash 和 test-only 路径。
- 音频证据仅包括 self-voicing transcript、音频可用性/静音状态记录和可选的非语音提示验证；声音不得成为唯一 PASS/FAIL 通道。
- 截图和 transcript 必须支持 1280×720、最大批准字体、键盘、自发声、高对比和 reduced-motion 场景；证据缺失时对应 criterion 阻断。
- 测试媒体不得进入发行资源、存档、persistent root 或玩家可见日志。无需运行 `/asset-spec`。

## UI Requirements

- 不创建 Ren'Py 内置 debug dashboard，不允许玩家在发行构建中查看隐藏轴、resolver trace、测试状态或内部评分。
- 开发者报告由三部分组成：版本化 JSON evidence manifest、按 run/criterion 隔离的原始产物目录、可读 Markdown 摘要。
- 终端只显示简短状态：scope、PASS/FAIL/BLOCKED、失败数量、首个 failure ID 和 manifest/hash 引用；完整诊断通过产物索引访问。
- 每条失败必须显示 criterion ID、case/assertion ID、owner contract、输入 hashes、环境 identity、exit code 和原始输出位置；不得只显示“测试失败”。
- 报告字段必须可通过键盘和纯文本阅读；不得依赖颜色、hover、声音或动画来表达状态。
- 报告和 test-only 资源在 release archive、正式 save、persistent root 和玩家日志中的计数必须为零。

## Acceptance Criteria

证据类型沿用：`UT_PURE`、`UT_ENGINE`、`STATIC`、`INSTR`、`BRANCH`、`A11Y`、`VISUAL`、`BENCH`、`SPIKE`、`HUMAN`、`PLAYTEST`、`REVIEW`。

### Framework Integrity — 12

| ID | Evidence | Criterion |
|---|---|---|
| `TEST-FRAME-001` | `STATIC` | **GIVEN** owning GDD、ADR、注册表和test manifests，**WHEN**扫描所有schema、公式、常量及阈值声明，**THEN**每项只有一个产品权威owner，SYS-TEST中的重复或不同值声明计数为0。 |
| `TEST-FRAME-002` | `STATIC + UT_PURE` | **GIVEN**所有直接依赖系统，**WHEN**解析领域manifest和集中runner manifest，**THEN**每个系统提供自己的criteria/fixtures/oracles，SYS-TEST只拥有编排、证据和跨系统门禁。 |
| `TEST-FRAME-003` | `STATIC + UT_PURE` | **GIVEN**任一gate manifest，**WHEN**验证criterion、suite、case和artifact映射，**THEN**required集合全部非空、ID唯一、expected 与 executed case ID 集合 exact-match、expected case count 大于0且无孤立required criterion。 |
| `TEST-FRAME-004` | `UT_PURE` | **GIVEN**各证据类型的正例及互相冒充的负例，**WHEN**验证artifact，**THEN**只接受criterion声明的exact evidence types；错误类型不能关闭criterion。 |
| `TEST-FRAME-005` | `UT_PURE` | **GIVEN**required case分别为executed、skip、xfail、disabled和quarantined，**WHEN**聚合criterion，**THEN**只有实际执行并通过的case计入PASS，其余状态均使criterion失败。 |
| `TEST-FRAME-006` | `STATIC + UT_PURE` | **GIVEN**production-derived与synthetic fixtures，**WHEN**验证namespace、ID和报告分组，**THEN**两类完全分离、分别计数，synthetic最大值不会被标为production-reachable最大值。 |
| `TEST-FRAME-007` | `UT_PURE` | **GIVEN**完整artifact及逐字段删除、增加、错类型和wrong-hash mutants，**WHEN**验证artifact schema，**THEN**只有exact字段、类型和hash全部匹配的artifact有效。 |
| `TEST-FRAME-008` | `UT_PURE` | **GIVEN**声明PASS但exit code非0、exception非空或raw output含未处理错误的artifact，**WHEN**聚合结果，**THEN**状态固定为`ERROR`且gate失败。 |
| `TEST-FRAME-009` | `STATIC + UT_PURE` | **GIVEN**golden vector、截图基线、路径oracle或catalog发生差异，**WHEN**runner执行，**THEN**输出显式diff并失败；没有owning-system approval不能更新expected identity。 |
| `TEST-FRAME-010` | `UT_PURE + INSTR` | **GIVEN**相同identity/fixture/runner产生不一致结果，**WHEN**按`diagnostic_repeat_count`重复，**THEN**标记flaky并保持gate失败；后续偶然PASS不覆盖该失败。 |
| `TEST-FRAME-011` | `UT_PURE + INSTR` | **GIVEN**两个并发运行尝试写入同一criterion，**WHEN**封板artifact，**THEN**每个run使用唯一目录和run ID；原子封板锁只允许一个完整artifact成为 gate candidate，任何第二个完整候选都产生 duplicate-finalization 并使 criterion 失败，不发生last-writer-wins或跨run拼接。 |
| `TEST-FRAME-012` | `UT_PURE + STATIC` | **GIVEN**versioned dependency graph和变更节点，**WHEN**计算受影响套件，**THEN**按“权威输入→消费者”的边方向、包含直接变更节点的 `Reach*` 和 `Δ=∅` 规则返回准确传递闭包；存在未解析边时返回该层全部suites，RELEASE始终返回完整release manifest。 |

### Lifecycle and Aggregation — 8

| ID | Evidence | Criterion |
|---|---|---|
| `TEST-LIFE-001` | `UT_PURE` | **GIVEN**缺失manifest或必需外部输入，**WHEN**预检gate，**THEN**分别进入`UNBOUND`或`BLOCKED_INPUT`，不能直接进入`RUNNING`或`PASSED_CURRENT`。 |
| `TEST-LIFE-002` | `UT_PURE + INSTR` | **GIVEN**有效manifest、runner、fixtures和环境，**WHEN**全部cases成功执行并原子封板，**THEN**生命周期严格为`READY → RUNNING → PASSED_CURRENT`。 |
| `TEST-LIFE-003` | `UT_PURE + INSTR` | **GIVEN**assertion、runner、case-count、hash或cleanup失败，**WHEN**结束运行，**THEN**状态进入`FAILED`；修复后只能转回`READY`并重新执行。 |
| `TEST-LIFE-004` | `UT_PURE` | **GIVEN**一个`PASSED_CURRENT` artifact，**WHEN**任一source/catalog/config/fixture/runner/environment identity改变，**THEN**状态立即转为`STALE`且不能参与gate。 |
| `TEST-LIFE-005` | `UT_ENGINE + INSTR` | **GIVEN**运行中的宿主或Ren'Py进程被终止，**WHEN**下次读取运行目录，**THEN**partial output仅保留诊断用途，artifact result 为 `ERROR`、生命周期为 `FAILED` 并要求重跑。 |
| `TEST-LIFE-006` | `UT_PURE` | **GIVEN**`test_artifact_current`的全匹配正例及每个identity/generation/raw-output-presence/raw-hash单缺陷负例，**WHEN**计算，**THEN**仅全匹配正例输出`True`。 |
| `TEST-LIFE-007` | `UT_PURE` | **GIVEN**`test_criterion_pass`的nonempty、case count、evidence coverage、current、PASS和blocking-finding truth-table，**WHEN**计算全部组合，**THEN**只有六项条件同时成立时输出`True`。 |
| `TEST-LIFE-008` | `UT_PURE` | **GIVEN**`test_gate_pass`的required criteria、blocked input、stale artifact和global unresolved blocking finding truth-table，**WHEN**计算全部组合，**THEN**只有非空criteria全部通过且三个阻断条件均为0时输出`True`。 |

### Toolchain and Production Isolation — 8

| ID | Evidence | Criterion |
|---|---|---|
| `TEST-ISO-001` | `SPIKE + STATIC` | **GIVEN**目标Windows环境，**WHEN**记录Ren'Py、Python、renderer及runner版本，**THEN**精确匹配批准environment manifest；不匹配时相关artifact为`STALE/BLOCKED_INPUT`。 |
| `TEST-ISO-002` | `STATIC + UT_ENGINE + UT_PURE` | **GIVEN**lint、纯逻辑和Ren'Py-hosted cases，**WHEN**执行FAST/INTEGRATION，**THEN**三类分别由批准runner执行并保存独立exit code/raw output，不能互相冒充。 |
| `TEST-ISO-003` | `UT_PURE + UT_ENGINE + INSTR` | **GIVEN**相同输入在不同执行顺序、时区、locale和文件枚举顺序下运行，**WHEN**比较语义artifacts，**THEN**除非批准环境identity不同，否则canonical结果和hash完全一致，网络/遥测/随机调用计数为0。 |
| `TEST-ISO-004` | `STATIC` | **GIVEN**完整production/test source manifest，**WHEN**解析直接与传递依赖、aliases、wrappers、closures、reflection和dynamic imports，**THEN**production→test-only路径计数为0，未解析边阻止release。 |
| `TEST-ISO-005` | `STATIC + UT_ENGINE` | **GIVEN**冻结 staging tree、最终 release archive、store、正式save和persistent root，**WHEN**扫描test-only类型与IDs，**THEN**observer、spy、fault injector、protocol bomb、synthetic save/root、benchmark harness和evidence forger计数均为0；staging 与 archive 两次 inventory 必须分别 exact-match 其批准排除规则。 |
| `TEST-ISO-006` | `STATIC` | **GIVEN**所有production APIs和call graph，**WHEN**扫描catalog注入、mutable-global替换、skip-validation、force-success及任意状态写入入口，**THEN**未获ADR批准的test seam计数为0。 |
| `TEST-ISO-007` | `UT_ENGINE + INSTR` | **GIVEN**每类save/persistent/timer故障注入fixture，**WHEN**case结束，**THEN**磁盘、root、backend、rollback状态和test clock恢复到批准基线；cleanup失败立即停止suite并使后续结果无效。 |
| `TEST-ISO-008` | `UT_PURE + UT_ENGINE` | **GIVEN**artifact来自错误Windows build、renderer、Python或Ren'Py版本，**WHEN**验证environment identity，**THEN**该artifact不能关闭当前环境criterion，其他版本的PASS不被复用。 |

### Gate Execution — 6

| ID | Evidence | Criterion |
|---|---|---|
| `TEST-GATE-001` | `STATIC + UT_PURE` | **GIVEN**FAST manifest，**WHEN**执行gate，**THEN**lint、pure logic、schema/catalog validation及static scans全部非空执行；FAST 不运行 Ren'Py-hosted testcase；超出 hard timeout 时产生 `TIMEOUT/ERROR` 并使 scope 失败。 |
| `TEST-GATE-002` | `UT_ENGINE + INSTR + BRANCH` | **GIVEN**INTEGRATION manifest和可用production contracts，**WHEN**执行gate，**THEN**Ren'Py flows、恢复、fault injection、joins、branch及accessibility interaction suites按影响闭包全部运行并严格AND聚合。 |
| `TEST-GATE-003` | `STATIC + UT_ENGINE + BENCH + A11Y + VISUAL` | **GIVEN**release candidate，**WHEN**执行RELEASE，**THEN**完整路径、最大fixtures、benchmark、layout/accessibility、外部证据完整性和production-isolation全部运行；任何影响裁剪配置均失败。 |
| `TEST-GATE-004` | `UT_PURE` | **GIVEN**isolated component fixtures通过但production catalog或engine input缺失，**WHEN**聚合gate，**THEN**component scope可为PASS，integration/release保持`BLOCKED_INPUT`且不会继承component verdict。 |
| `TEST-GATE-005` | `UT_PURE` | **GIVEN**某required HUMAN、VISUAL、PLAYTEST或engine artifact缺失，**WHEN**计算依赖图，**THEN**仅其criterion和下游gates阻断，独立FAST scope仍可运行且不会被提升为更高层PASS。 |
| `TEST-GATE-006` | `STATIC` | **GIVEN**SYS-BUILD生成的冻结 staging/archive candidate identity，**WHEN**消费SYS-TEST release evidence，**THEN**只读取current artifacts、source/catalog hashes和staging/archive exclusion报告；任何修改artifact、source hash或候选包以制造PASS的行为使build gate失败；缺少SYS-BUILD owner contract时保持 `BLOCKED_INPUT`。 |

### Player-Critical Causality — 5

这些 criterion 验证玩家可感知的因果，而不是仅验证测试系统自身的 provenance。它们必须使用无调试信息、无隐藏分数展示的 production-like flow；`HUMAN`/`PLAYTEST`/`REVIEW` 只能由批准 rubric 和人工 adjudication 提供主观结论，SYS-TEST 只验证证据完整性与绑定关系。

| ID | Evidence | Criterion |
|---|---|---|
| `TEST-FANTASY-001` | `UT_ENGINE + BRANCH + REVIEW` | **GIVEN**一条合法 production-like choice path，**WHEN**执行选择、即时 reaction 与严格较晚的 payoff，**THEN** evidence exact 绑定 `choice_id → immediate_reaction_id → payoff_id`，且无调试信息或隐藏分数进入玩家可见输出。 |
| `TEST-FANTASY-002` | `UT_ENGINE + BRANCH + INSTR` | **GIVEN**before-choice、after-reaction、before-payoff 与 after-payoff 四个恢复点，**WHEN**回滚后改选并重放，**THEN** `expected_history → expected_choice_id → expected_reaction_id → expected_payoff_id → expected_ending_cause` 与实际记录逐项一致；改选产生不同 registered payoff 或 ending cause 的路径必须被覆盖。 |
| `TEST-FANTASY-003` | `UT_ENGINE + A11Y + REVIEW` | **GIVEN**同一 choice/reaction/payoff flow 的视觉、键盘与 self-voicing/transcript 路径，**WHEN**移除视觉通道或启用替代设置，**THEN** choice identity、observable fact、reaction 与 payoff 的语义摘要保持等价，不读出隐藏轴、分数或测试状态。 |
| `TEST-FANTASY-004` | `HUMAN + PLAYTEST + REVIEW` | **GIVEN**无隐藏分数、无调试信息的盲测 protocol，**WHEN**参与者复述此前选择造成的一条即时反应与后续 payoff，**THEN**原始回答、编码 rubric、分组结果、reviewer/adjudication 与 protocol identity 全部存在；主观结果未获批准时 criterion 保持 `BLOCKED_INPUT`。 |
| `TEST-FANTASY-005` | `BRANCH + HUMAN + REVIEW` | **GIVEN**六个 canonical ending witness，**WHEN**审阅每个结局的 cause/payoff/summary，**THEN**每个 ending 均有可追溯选择链和具体 payoff，人工 reviewer 能在不查看隐藏分数的情况下指出其主要原因；仅有 hash/路径结构不能替代该结论。 |

### Cross-System Contract Coverage — 12

| ID | Evidence | Criterion |
|---|---|---|
| `TEST-DOM-001` | `UT_PURE + UT_ENGINE + STATIC + INSTR + BRANCH` | **GIVEN**SYS-STATE当前criterion manifest，**WHEN**执行组件、恢复、快照、纯度及内容cases，**THEN**所有登记criteria均有current evidence，轴/token/validation precedence不由SYS-TEST重定义。 |
| `TEST-DOM-002` | `UT_PURE + STATIC + BRANCH + INSTR` | **GIVEN**六个canonical ending vectors、boundary mutants 与 ending completion event fixtures，**WHEN**执行resolver/ending-flow correctness cases，**THEN**每个合法输入恰有一个ending、六结局互斥、purity/trace合同通过，且唯一 terminal completion node/event 关系可追踪；完整 production terminal-path enumeration 由 `TEST-DOM-012` 单独负责。 |
| `TEST-DOM-003` | `STATIC + UT_PURE + UT_ENGINE + BRANCH` | **GIVEN**SYS-CHOICE production manifests，**WHEN**验证catalog、CFG/DAG、reaction/payoff及qualification joins，**THEN**完整正例通过，missing/duplicate/orphan/wrong-nullability和continuation缺口逐案失败；每条新增 production route 都有对应 `UT_PURE` 与 Ren'Py-hosted `UT_ENGINE` case，不能只用一个类型替代另一个。 |
| `TEST-DOM-004` | `STATIC + BRANCH + UT_ENGINE` | **GIVEN**SYS-NARRATIVE source manifest、canonical CFG、witnesses和oracle records，**WHEN**验证完整production图，**THEN**所有scene/control edges、agency、reaction/payoff、恢复位置和terminal witnesses均exact覆盖，无调试playtest artifact保持外部证据类型。 |
| `TEST-DOM-005` | `UT_ENGINE + INSTR + BENCH` | **GIVEN**SYS-SAVE合法/旧版/未知/损坏cross-product、四恢复点、ending completion save/rollback fixtures 和I/O failure fixtures，**WHEN**执行load/save/rollback，**THEN**分类、阻断流程、控制位置、原子结果、重复/丢失计数、completion event 恢复和owning performance thresholds全部符合合同。 |
| `TEST-DOM-006` | `UT_PURE + UT_ENGINE + INSTR + BENCH` | **GIVEN**SYS-PERSIST schema-v2、12-leaf manifest、ending completion request 及batch/merge/reset/failure fixtures，**WHEN**执行validation、flush、merge、epoch、projection和operation invariance，**THEN**公开成功结果只为`APPLIED_FLUSHED`，结果与owner公式一致，foreign writes和test-root泄漏计数为0。 |
| `TEST-DOM-007` | `STATIC + UT_PURE + UT_ENGINE + A11Y` | **GIVEN**11项成就catalog、events、witnesses及0/max/synthetic fixtures，**WHEN**执行snapshot、condition、epoch、backend、queue、seen和UI验证，**THEN**43项owning criteria均有exact current evidence，无mirror或隐藏分数代理。 |
| `TEST-DOM-008` | `UT_PURE + UT_ENGINE + INSTR + A11Y + VISUAL` | **GIVEN**SYS-JOURNAL bundle、snapshot及0/max/long-copy/failure fixtures，**WHEN**执行read-model、focus、refresh、seen、recovery和layout验证，**THEN**可见顺序、计数、焦点、bounded evidence及四故障域均符合owning合同。 |
| `TEST-DOM-009` | `UT_ENGINE + A11Y + VISUAL + HUMAN` | **GIVEN**SYS-ACCESS冻结mode/layout/interaction matrix，**WHEN**执行keyboard walk、TTS transcript、字体/对比/动效及单通道移除验证，**THEN**semantic action/output tuples保持等价，choice/reaction/payoff 的 causal replay 在视觉、键盘和非视觉通道一致；skip/auto 等待 accessible transcript/backlog 交付，flash/shake 替代语义存在，voice failure 不得降级为非视觉 PASS，人工TTS结果只按批准rubric导入。 |
| `TEST-DOM-010` | `UT_PURE + UT_ENGINE + INSTR + BENCH` | **POST-MVP DEFERRED — GIVEN**SYS-TENSION timed/non-timed pair、pause intervals、竞争序列和恢复fixtures，**WHEN**运行时钟与resolution，**THEN**剩余时间、阶段、同刻优先级、唯一dispatch、timeout canonical choice及timer non-serialization全部符合owner合同；本 criterion 不阻断当前 P0 Production gate。 |
| `TEST-DOM-011` | `UT_ENGINE + INSTR + BRANCH` | **GIVEN**before-choice、after-reaction、before-payoff、after-payoff、loaded-save rollback及persistent membership fixtures，**WHEN**save/load/rollback/replay，**THEN**每个 checkpoint 的 semantic state、控制位置、ordered history、choice/reaction/payoff/ending-cause IDs 与 expected snapshot 逐项 exact-match，不存在重复或丢失；至少一条回滚后改选路径必须产生不同 registered payoff 或 ending cause，persistent不被per-run恢复覆盖。 |
| `TEST-DOM-012` | `STATIC + BRANCH` | **GIVEN**冻结production source/graph inventory、choice/narrative/ending catalogs 和 maximum fixture，**WHEN**枚举全部合法terminal paths，**THEN**实际 source roots、nodes、edges、terminal entries、path count 与 inventory exact-match；每条path恰映射一个ending、一个terminal class、有效witness、payoff和summary；per-ending class budget按SYS-ENDING权威判定。 |

### Performance, Operations, and External Evidence — 9

| ID | Evidence | Criterion |
|---|---|---|
| `TEST-PERF-001` | `UT_PURE` | **GIVEN**已知排序样本以及奇偶样本数和边界percentiles，**WHEN**计算`test_nearest_rank_percentile`，**THEN**结果恰为`sort(X)[ceil(p×n)-1]`，不执行插值。 |
| `TEST-PERF-002` | `BENCH + UT_PURE` | **GIVEN**有效protocol、批准阈值和raw samples，**WHEN**计算`test_performance_pass`，**THEN**只有全部metric/operator/threshold比较通过时输出`True`。 |
| `TEST-PERF-003` | `BENCH` | **GIVEN**有效raw samples但没有owning-system批准阈值，**WHEN**完成benchmark，**THEN**生成`REPORT_ONLY` artifact并保存样本，performance PASS为`False`。 |
| `TEST-PERF-004` | `BENCH + UT_PURE` | **GIVEN**NaN、无穷、负时长、错类型、缺失、样本不足及过滤后样本fixtures，**WHEN**验证protocol，**THEN**每类固定失败且不产生替代percentile。 |
| `TEST-PERF-005` | `BENCH` | **GIVEN**FAST suite 分别低于和超过批准 hard timeout，**WHEN**聚合结果，**THEN**超时产生 `TIMEOUT/ERROR`、scope 失败且保留 raw output；`fast_gate_feedback_target_seconds` 只能产生 workflow warning，不能覆盖 hard timeout 或减少 required case。 |
| `TEST-PERF-006` | `UT_PURE + INSTR` | **GIVEN**`diagnostic_repeat_count`为2、3、10及越界值，**WHEN**运行flaky诊断，**THEN**安全范围内执行exact次数、越界预检失败，任何重复PASS均不覆盖原失败。 |
| `TEST-PERF-007` | `UT_PURE + STATIC` | **GIVEN**artifact世代超过retention目标，**WHEN**执行清理，**THEN**只删除超出保留世代的非release诊断产物；release、human/playtest及公开版本追溯证据保留。 |
| `TEST-EXT-001` | `STATIC + REVIEW` | **GIVEN**HUMAN、PLAYTEST、VISUAL或REVIEW artifact，**WHEN**验证完整性，**THEN**rubric、参与者/reviewer、环境、raw responses/captures、分组结果与adjudication字段全部存在且hash匹配。 |
| `TEST-EXT-002` | `UT_PURE + REVIEW` | **GIVEN**完整人工artifact但没有批准的人工PASS裁定，**WHEN**SYS-TEST聚合，**THEN**系统不得从分数、多数票或截图自动生成主观PASS，criterion保持阻断。 |

### Evidence Bundle and Traceability — 6

| ID | Evidence | Criterion |
|---|---|---|
| `TEST-EVID-001` | `STATIC` | **GIVEN**SYS-TEST acceptance bundle，**WHEN**从 manifest 汇总 criterion IDs，**THEN**manifest-derived unique ID 集合与本节逐项 exact-match，无缺失、重复或额外ID；数量不得依赖手填常量。 |
| `TEST-EVID-002` | `STATIC + UT_PURE` | **GIVEN**每个criterion artifact，**WHEN**追踪source/catalog/config/fixture/runner/environment及raw output，**THEN**所有引用存在、完整SHA-256匹配且可从bundle索引定位。 |
| `TEST-EVID-003` | `UT_PURE` | **GIVEN**一个criterion需要多个证据类型，**WHEN**组合artifacts，**THEN**所有artifact必须属于同一冻结identity世代；跨世代拼接固定失败。 |
| `TEST-EVID-004` | `UT_PURE` | **GIVEN**bundle同时包含current与stale PASS artifacts，**WHEN**聚合gate，**THEN**只读取current artifacts，stale count大于0使required gate失败。 |
| `TEST-EVID-005` | `STATIC + UT_PURE` | **GIVEN**任一失败或阻断criterion，**WHEN**生成summary，**THEN**包含稳定failure/finding IDs、对应case/assertion、原始产物位置和owning contract引用；空泛“测试失败”不合格。 |
| `TEST-EVID-006` | `STATIC` | **GIVEN**Entity Registry中全部`referenced_by: SYS-TEST`条目，**WHEN**建立traceability index，**THEN**每项解析到至少一个criterion或明确的owner-approved external-evidence mapping；未映射、错误owner或值漂移计数为0。 |

*QA Lead 未参与——Solo 模式；以上66项criteria在进入实现前必须由独立QA人工复核其可执行性、fixture非空性、证据类型和人工 adjudication 合同正确性。*

## Open Questions

| ID | 问题 | Owner | 目标门槛 | 关闭证据 |
|---|---|---|---|---|
| `SYS-TEST-Q1` | Ren'Py 8.5.3 `testcase/testsuite` 的调用方式、exit code、失败传播和 lint 编排是否稳定？ | Engine Programmer + SYS-TEST | Implementation stories Ready 前 | 版本固定 capability manifest、最小 testcase、失败/中止矩阵 |
| `SYS-TEST-Q2` | Save/Persistent 原子写入、temporary file、replacement、process interruption 的故障注入如何实现？ | Engine Programmer + SYS-SAVE + SYS-PERSIST | Save/Persist stories Ready 前 | 四阶段 fault-injection harness、safe-failure/commit-unknown report、restart fixtures |
| `SYS-TEST-Q3` | post-MVP timed-choice 的单调时钟、暂停、self-voicing、focus、interaction restart 和 input receipt 如何在目标环境可观测？ | Engine Programmer + SYS-TENSION + SYS-ACCESS | post-MVP Tension/Access implementation 前 | crisis-scene spike、raw arbitration traces、keyboard/TTS/focus evidence |
| `SYS-TEST-Q4` | 已定义的 `test_evidence_bundle:v1` baseline 如何落实为 accepted schema/ADR、content-addressed artifact storage 和本地/CI入口？ | Architect + SYS-BUILD + SYS-TEST | Architecture/Build stories Ready 前 | Accepted schema/ADR、sample bundle、读写和 stale fixtures |
| `SYS-TEST-Q5` | 已定义的 `benchmark_protocol:v1` 如何绑定最低参考硬件、Windows build、renderer、timer、GC、cache、warm-up、sample count 和 percentile policy？ | SYS-TEST + Engine Programmer | 首次 performance gate 前 | Benchmark/threshold manifest、raw samples、nearest-rank report |
| `SYS-TEST-Q6` | 已定义的 source inventory 如何覆盖 alias、closure、reflection、dynamic import、generated files、resource roots 与 test-only leakage？ | Architect + SYS-TEST | Release build gate 前 | 完整 source manifest、实际 inventory hash、解析图、negative fixtures、unresolved-edge report |
| `SYS-TEST-Q7` | 66项 SYS-TEST criteria 与全部 `referenced_by: SYS-TEST` Registry facts 如何完成 manifest-derived traceability？ | Producer + QA + SYS-TEST | Epic/Story 创建前 | manifest-derived ID bundle、registry traceability index、未映射计数为0 |
| `SYS-TEST-Q8` | 66项 criteria 的 fixture、matrix cell、证据类型、人工 adjudication 与负例是否独立可执行？ | QA Lead | Implementation handoff 前 | 独立 QA review、fixture/matrix inventory、criterion-to-evidence audit |
| `SYS-TEST-Q9` | SYS-BUILD 如何消费 current evidence、排除 test-only 资源并保留 release provenance？ | Build Owner + SYS-TEST | Release artifact lock 前 | archive scan、source/catalog hash report、evidence index与排除报告 |

Solo 模式下未调用 Art Director、Audio Director、UX Designer 或 QA Lead；上述章节和问题必须在制作前由相应责任人独立复核。
