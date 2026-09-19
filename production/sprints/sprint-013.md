# Sprint 013 — 2026-08-17 to 2026-08-28

> **Sprint-plan update — 2026-08-16**
>
> The active scope below supersedes the original closeout task tables further
> down. Those tables remain intact as a historical record; their `N13-*` and
> `S13-*` external-evidence blockers are not part of the ordinary regression
> baseline. They are re-registered under the future **Production RC Closeout**
> section below.

## Active Sprint 013 — Non-formal-asset automation preflight

### Sprint Goal

在不生成、接入或修改任何正式资产的前提下，完成可信的非资产自动化预检：修复 content-lock/source identity，接受与 Story 024、15 个 canonical units 和唯一 resolver handoff 一致的 ADR-0010，生成绑定当前非资产 HEAD 的 candidate/narrative-flow manifest，恢复普通 Python 回归全绿，并把人工/性能/归档证据严格留在显式 Production RC closeout gate。

### Baseline and boundary

- Trusted code baseline: `HEAD ff00c7a` and the pre-change ordinary suite `346 tests / 19 fail-closed external-input failures`; those 19 failures are not described as 19 code regressions.
- Active stage remains `Production`; this update never writes `production/stage.txt`.
- Formal assets are out of scope: character art, backgrounds, CGs, UI bitmaps, VFX, music, sound effects and voice acting. `E:\Longzu-assets` is out of scope and is not read or modified.
- `content_lock:player_visible:v6` remains the lock generation because the semantic diff against the trusted HEAD is zero; only stale source identity rows are refreshed.
- The ordinary `python -m unittest discover` command is wired to the normal `*_test.py` suite. Missing external evidence is classified, not promoted.

### Current Must Have — automated preflight only

| ID | Task / Owner | Est. h | Dependencies | Acceptance criteria |
|---|---|---:|---|---|
| P13-01 | Content-lock/source identity repair / Andwey | 4 | `HEAD ff00c7a` | `game/screens.rpy` and `game/11_achievements.rpy` have current line/hash rows; semantic diff record says zero copy delta; content constraints and source-manifest checks pass. |
| P13-02 | ADR-0010 and end-to-end topology review / Andwey | 4 | Story 024, ADR-0001/2/6/7/8/9 | ADR-0010 is Accepted only after the fixed route, 15 units, six ending map and one resolver handoff are source-verified; focused architecture review is recorded. |
| P13-03 | Candidate and complete narrative-flow manifest preflight / Andwey | 6 | P13-01, P13-02 | `candidate_manifest:v1`, full `narrative_flow_manifest:v1`, canonical source hashes and explicit `release_candidate:false` bind to the current non-asset HEAD; partial Day 1 manifest is rejected as a production input. |
| P13-04 | Automated seven-day, six-ending, save/load and accessibility contracts / Andwey | 12 | P13-01 to P13-03 | Static and pure/engine contracts pass for the fixed path, six endings, persistence and accessibility semantics; no GUI, SAPI, semantic or player understanding is claimed. |
| P13-05 | Regression, smoke and evidence-integrity layer / Andwey | 8 | P13-01 to P13-04 | Ordinary discovery is green; regression manifest is current; smoke report distinguishes PASS/NOT RUN/WARNINGS; evidence review distinguishes ADEQUATE/INCOMPLETE/MISSING; external missing inputs classify as `BLOCKED_INPUT`/`REPORT_ONLY`. |
| P13-06 | Explicit Production-closeout gate runner and preflight record / Andwey | 6 | P13-01 to P13-05 | `tools/run-production-closeout-gate.py --final` is the only runner that emits non-PASS for missing external evidence; it never updates stage or creates formal assets; preflight stops at Production. |

### Deferred: Production RC Closeout Sprint

The following original records are retained as future RC inputs and do not
block the current automation preflight's ordinary regression baseline:

- **N13-02/N13-03**: real GUI seven-day run and six-ending human witnesses.
- **N13-05/N13-06/N13-07**: human keyboard/mouse, SAPI transcript/listening and semantic-equivalence review.
- **N13-08**: new-player playtest and comprehension dossier.
- **N13-09**: formal-asset-influenced target-hardware performance measurement; current preflight keeps protocol as `REPORT_ONLY`.
- **N13-10**: DOCX/source provenance and owner boundary decision; only metadata/SHA-256 may be read when the input is supplied, and the owner rule is not third-party legal authorization.
- **N13-11/N13-12**: final archive, final QA and Production → Polish promotion gate.

Every preserved `BLOCKED_INPUT`/`REPORT_ONLY` record remains fail-closed in
`production/sprint-status.yaml` under `deferred_rc_closeout`; none is changed to
PASS by this update. The explicit closeout runner must be invoked later to
turn those missing external inputs into a non-PASS final-gate result.

## Sprint Goal

在不制作任何正式游戏资产的前提下，完成当前版本的非正式资产 Production 收尾：把端到端玩家流程、六结局、存档/日志/成就、Production 级键鼠与无障碍、人工语义/版权/性能检查，以及 SYS-BUILD 归档证据绑定到同一候选版本，并完成最终 Production → Polish 门禁复核。

**Review mode:** `solo`。PR-SPRINT 与其他 director/lead gate 按参数跳过；本文件不把自动化 PASS 扩大为人工或发布 PASS。

## Current Baseline and Carryover

- 当前阶段：`Production`（`production/stage.txt` 未更新）。
- `production/milestones/` 与 `production/risk-register/` 当前没有可读文件；本冲刺以 `production/gate-checks/production-to-polish-2026-08-14-final.md` 的最终失败报告作为里程碑约束与风险基线。
- Sprint 012 已完成 Day 7、六结局与 `rain_stops` 文案扩展及自动化链；其余 GUI/试玩、SAPI/语义、版权、主观人工审阅、性能和发布归档证据继续作为本冲刺收尾输入。
- `docs/architecture/adr-0010-end-to-end-player-flow-topology.md` 已创建并纳入本冲刺的 N13-01 架构基线；其状态仍为 `Proposed`，实现闭合、实际玩家流程和证据闭合仍由 N13-01 至 N13-12 负责，注册表同步不在本次更新内。
- 本冲刺不重开已完成的章节文案、resolver、结局条件或正式资产制作；只有发现 Production 收尾证据所需的窄范围实现缺口时，才允许建立可追溯的最小修复。

## Scope and Explicit Exclusions

### Included

- 端到端玩家流程拓扑的决策冻结、现有 Production 编排器的实现闭合与实际运行证明。
- Day 1–Day 7 的真实玩家流程、六个固定结局及 `rain_stops` 既有尾声的可达性与终端证据。
- 存档/读档、愿望手册/日志、成就和持久化状态的同一玩家流程贯通。
- 当前版本的键盘、鼠标、字体倍率、对比度、动效/闪烁/震动、静音、焦点、viewport、SAPI/transcript 与语义等价人工证据。
- 当前版本试玩、无调试玩家理解度验证、性能实测、DOCX/同人版权边界确认。
- SYS-BUILD staging/archive、candidate identity、hash、法律闭合、test-only exclusion 和发布证据。
- 最终 Production → Polish 门禁复核；门禁失败时只记录阻塞，不擅自修改 `production/stage.txt`。

### Explicitly excluded

角色立绘、背景图、CG、UI 位图、音乐、音效、配音，以及其他正式游戏资产的设计、生成、采购、接入、替换或扩产。现有代码定义的纯色背景、文字/choice surface 和已登记字体只允许作为当前版本验证对象，不得在本冲刺新增正式资产。

## Capacity

- 工作日：10 天（2026-08-17 至 2026-08-28）。
- Solo capacity：80 小时（10 × 8h）。
- Buffer：16 小时（20%，保留给重跑、人工证据修复和 identity 漂移）。
- Must Have available：64 小时；Must Have 合计正好 64 小时。
- Should Have：17 小时，仅在所有 Must Have 完成且仍有 buffer 时执行；不为 Should Have 延长冲刺或牺牲门禁证据。

## Dependency Order — Confirmed

- **N13-01** is the sole topology prerequisite. It consumes ADR-0010, Story 024, the SYS-NARRATIVE baseline and the SYS-BUILD canonical-unit contract.
- **N13-02** starts after N13-01 and produces the real Day 1–Day 7 player-flow/checkpoint evidence.
- **N13-03** starts after N13-01 and N13-02; it consumes the approved flow/checkpoint baseline to produce six ending witnesses and terminal proof.
- **N13-04** starts after N13-02 and N13-03; it validates save/load, journal, achievements and persistence across the actual flow and ending witnesses.
- **N13-05** starts after N13-02 and N13-04; it uses the same current build and state contracts for keyboard/mouse and accessibility evidence.
- **N13-06** starts after N13-05 and `content-lock:v6`; it records SAPI/transcript evidence for the already-validated surfaces.
- **N13-07** starts after N13-03, N13-05 and N13-06; it adjudicates semantic equivalence against the same ending and accessibility evidence generation.
- **N13-08** starts after N13-02, N13-03, N13-04 and N13-05; it aggregates the complete gate-ready playtest record and adds the no-debug comprehension session.
- **N13-09** starts after N13-02 and N13-04, with a stable current candidate identity; it cannot promote `REPORT_ONLY` data to PASS.
- **N13-10** starts after N13-02, N13-03, `content-lock:v6` and the existing legal register; missing DOCX input remains `BLOCKED_INPUT`.
- **N13-11** starts only when N13-05 through N13-10 are current and classified; any stale, blocked or report-only required input blocks archive/release evidence.
- **N13-12** is the final action and consumes N13-01 through N13-11; it may record FAIL/CONCERNS/blocked, but never promotes `production/stage.txt` automatically.

N13-02 begins only after N13-01 has recorded ADR-0010 and its implementation baseline. N13-03 begins only after N13-02's flow/checkpoint evidence is current; fixture preparation may overlap, but acceptance does not. N13-06 and N13-07 must consume the same accessibility/content-lock generation. N13-11 and N13-12 remain strictly downstream gates.

## Tasks

### Historical Must Have — preserved original Sprint 013 scope (superseded)

| ID | Task / Owner | Est. h (days) | Dependencies | Acceptance criteria | Blocking conditions | Required QA evidence |
|---|---|---:|---|---|---|---|
| N13-01 | 端到端玩家流程拓扑决策与实现闭合 / Andwey | 4h (0.5d) | ADR-0010（Proposed）、现有 Story 024、SYS-NARRATIVE baseline、SYS-BUILD canonical units | 以 ADR-0010 为拓扑基线，冻结 `New Game → Prologue → Day 1–7 → 唯一 resolver handoff → 六结局 entry → 适用的 rain_stops tail → 正常返回`；生产入口只有一个，非测试启动不经过 debug/test branch；15 个 canonical production units、六结局与尾声均有唯一责任路径；当前 source hash 与运行拓扑一致。 | 拓扑存在未决分叉/重复 caller；缺 canonical unit；非测试入口无法启动；source/hash drift；发现需要新增 choice、route、ending 或 asset。 | ADR-0010 状态/引用、topology decision record/manifest、CFG/source scan、当前 hash、非测试启动 raw stdout/stderr、一次完整运行 trace、production→test-only edge=0 报告。 |
| N13-02 | Day 1–Day 7 实际玩家流程 / Andwey | 8h (1d) | N13-01 | 从主菜单的当前版本开始，以真实键鼠输入完成一条合法七日流程；不使用 debug 入口、直接写状态、旧存档、传送或测试 observer；每一天的场景、选择、即时反应、延迟 payoff、章节完成和下一日衔接均可观察且不丢失。 | 任一日崩溃、卡死、缺 scene/choice、无法正常推进或只能依赖测试入口；玩家可见文本/选项顺序在 content lock 外变化。 | 当前 build identity、逐日 session log、原始截图/视频或等价 capture、输入/存档 checkpoint 记录、日间 completion 矩阵、无 debug 复核清单、重跑后的 automated regression。 |
| N13-03 | 六结局实际玩家流程与终端证明 / Andwey | 6h (0.75d) | N13-01、N13-02 | 为 `rain_stops`、`her_own_name`、`see_the_sea`、`one_person_train`、`golden_cage`、`unsent_postcard` 各完成一条从 New Game 或批准 checkpoint 开始的真实 witness；只用玩家选择与正式存取档到达结局；六个 ending entry、completion、原因回收及 `rain_stops` 尾声均符合 owner contract，其他结局不错误复用尾声。 | witness 不能重放；通过直接注值/调试标记到达；resolver 与可见结局不一致；结局完成事件、日志或成就漏写；终端路径数量/hash 不一致。 | 六结局 witness manifest、每条输入/choice history、checkpoint 与 load trace、ending/epilogue captures、结局原因 transcript、completion/persistent 结果、六结局 automated replay 与 negative fixture 结果。 |
| N13-04 | 存档/读档/日志/成就贯通 / Andwey | 7h (0.875d) | N13-02、N13-03 | 在真实七日流程和至少两个结局 witness 中，于批准 checkpoint 保存、读档、重复读档、跨日恢复、结局完成后恢复；愿望手册/日志、ending/memory/achievement projection 和 persistent root 同步；重复加载不重复授予、不回滚、不污染下一次 New Game；UI 错误/恢复路径可理解且可重访。 | checkpoint/location join 失败；load 未分类或写回不可信 draft；日志焦点/空态/恢复态缺失；成就队列或 persistent epoch 不一致；需要改动冻结 schema。 | 原始 save slot/payload 及 hash、save/load 前后 state diff、load classifier/restore trace、日志/愿望手册 captures、成就 unlock/重复授予记录、persistent merge/reset evidence、相关 unit/integration suite PASS。 |
| N13-05 | Production 级键鼠与无障碍证据 | 8h (1d) | N13-02、N13-04 | 在批准的 Windows 10/11 + Ren’Py 8.5.3 环境完成一条只键盘流程与一条只鼠标流程；P0 screens 覆盖 stable focus、Tab/Shift+Tab、viewport auto-scroll、鼠标/canonical action parity、1280×720 的 1.0/1.25/1.5 字体、高对比、reduced-motion、flash/shake suppression、静音，以及 loading/empty/error/disabled/recovery（不适用需 owner rationale）；无裁切、焦点丢失、trap、隐藏旁路或仅靠颜色/动效传达的关键事实。 | 任一 required matrix cell 缺失；1.5 倍裁切/重叠/不可达；焦点不可见或鼠标绕过 disabled gate；静音/高对比/恢复态丢语义；只得到旧世代截图。 | environment preflight、keyboard walk trace、mouse parity trace、每屏/每状态 raw screenshots、1280×720×1.0/1.25/1.5 layout matrix、focus/viewport log、setting tuple、当前 source/config/environment hash、人工逐屏 checklist。 |
| N13-06 | SAPI 与 transcript | 5h (0.625d) | N13-05、content-lock v6 | 在实际可用的简体中文 Windows SAPI 配置完成 capability preflight、self-voicing 开关、焦点/状态/choice/反应/payoff/recovery 读序验证；记录 raw transcript、announcement count、focus/action sequence、是否自动执行 action；语音不可用时显示静态安全提示且不伪造 PASS；人工听测只接受当前 identity 的 transcript。 | 只有 capability enumeration 没有真实 transcript/听测；SAPI voice 不可用且没有批准替代环境；读序与键盘/可见阅读顺序不一致；self-voicing 自动执行 action；raw transcript 或 hash 缺失。 | `sapi-preflight.json`、raw transcript 与 SHA-256、逐 surface transcript record、语音环境 identity、no-auto-action trace、中文听测 rubric/adjudication、失败时的视觉安全提示 capture。 |
| N13-07 | 语义等价人工复核 | 5h (0.625d) | N13-05、N13-06、N13-03 | 对同一玩家路径执行带声音/无声音、彩色/非颜色、高动效/减弱动效及相关 reduced-mode 对照；不接触隐藏状态的 reviewer 能复述具体行动、即时反应、payoff、恢复动作和结局原因；各变体绑定同一 `accessible_causal_summary_id`，而不是只比较截图相似度。 | 没有 paired capture/transcript；reviewer 不能独立裁定；变体需要内部 axis/token/threshold 才能理解；source/catalog/config 世代不一致；人工结果被自动截图替代。 | paired raw captures、对应 transcript、semantic tuple comparison、reviewer 原始回答、rubric、adjudication record、人工签名/日期、所有输入及输出 hash。 |
| N13-08 | 当前版本完整试玩记录与无调试玩家理解度验证 | 5h (0.625d) | N13-02、N13-03、N13-04、N13-05 | 形成满足当前 Production → Polish 门禁的完整试玩档案：从当前候选版本正常非测试入口开始，覆盖核心 Day 1–Day 7 玩家流程与六个 canonical ending witness（可链接 N13-02/N13-03 的原始记录，但不得只引用摘要）；试玩者不可见 debug ID、测试入口、内部状态或开发说明；至少一位新/未 briefing 玩家能说明选择回收、保存/读取、日志/愿望手册、成就、六结局差异及结局原因；所有步骤、阻塞、误解与复现信息均绑定同一 candidate identity；不把“自动化通过”当作理解度通过。 | 没有当前候选包或正常非测试 GUI start；核心流程或任一六结局 witness 缺少 current raw evidence；试玩者接触到 debug 辅助；只有摘要/截图而无原始回答、输入/choice history、capture 或观察者记录；理解度回答只复述内部术语；问题无法绑定版本/步骤。 | `playtest-sprint-013-n13-08.md` 完整 gate-ready dossier；链接并校验 `playtest-sprint-013-n13-02.md` 与六份 `playtest-sprint-013-n13-03-ending-<ending-id>.md` 原始记录；candidate/build/environment identity；逐日与逐结局输入/存档/checkpoint trace；raw screenshot/video 或等价 capture；理解度问卷/口述原始回答；observer log、无 debug checklist、severity/reproduction 与 owner adjudication。 |
| N13-09 | 当前版本性能实测 | 3h (0.375d) | N13-02、N13-04、稳定 candidate identity | 按批准 protocol 在当前 build 实测启动、章节切换、输入响应、保存/读取和内存/资源使用等 owner 指标；记录硬件、Windows build、renderer、timer、warm-up、cache/GC、样本数、percentile 与阈值；仅在阈值存在且 protocol valid 时宣称 PASS，缺阈值只能是 `REPORT_ONLY` 并阻塞门禁。 | 无 approved threshold；不是当前 candidate；样本不足/原始样本缺失；计时、warm-up、cache 或硬件信息缺失；将纯性能单测冒充 engine 实测。 | `benchmark_protocol:v1`、raw samples、环境/构建 identity、启动/切换/save/load trace、p95/max 计算、阈值 manifest、原始 stdout/stderr、performance report。 |
| N13-10 | DOCX 与同人版权边界确认 | 3h (0.375d) | N13-02、N13-03、content-lock v6、现有 legal register | 找到并登记实际 DOCX 参考的来源、版本、hash、取得方式和许可状态；当前工作区缺少 DOCX 时明确保留 `BLOCKED_INPUT`，不得用摘要、自动扫描或默认同人声明代替；确认当前文本只采用高层结构/主题，不逐句复制未确认来源，不使用官方插画、Logo、音乐、音效或游戏素材；更新或确认 `fan-work-notice.md`、asset register 与 owner decision。 | DOCX 缺失且无外部 owner 提供（维持 `BLOCKED_INPUT`）；来源/许可不明；发现逐句复制或官方素材；法律边界需要商业化/发行授权；不能由 solo 自动审查伪造法律意见。 | DOCX 元数据与 SHA-256（若输入存在）；否则 `BLOCKED_INPUT` 原始记录；source/provenance note、差异/逐句复制审计、法律清单、owner decision/sign-off、`docs/legal/asset-register.md` 与 fan-work notice 复核记录。 |
| N13-11 | SYS-BUILD 构建归档与发布证据 | 7h (0.875d) | N13-05 至 N13-10 全部 current；SYS-BUILD runner/capability manifest | 以同一 candidate identity 完成 staging 与 final archive 两阶段证据；生成离线 Windows package、candidate/release manifest、source/catalog/asset/legal/evidence hash、archive hash、staging/archive exclusion report；最终 archive 不含 test observer/spy、fault injector、synthetic save、benchmark harness、debug ID、evidence forger、网络/遥测入口或未登记资产；输出只归档不发布。 | 任一上游证据 stale/BLOCKED_INPUT；candidate identity 漂移；runner/environment 不匹配；test-only 泄漏；法律闭合、字体 hash、asset allowlist 或 archive hash 缺失；package runner 失败。 | build run record、candidate manifest、staging/final inventory、runner stdout/stderr/exit code、source/catalog/asset/legal/evidence hash manifests、两次 exclusion report、archive tree listing、archive SHA-256、release evidence index。 |
| N13-12 | 最终 Production → Polish 门禁复核 | 3h (0.375d) | N13-01 至 N13-11 | 用同一 candidate identity 重跑最终 gate，逐项核对 Must Have、人工裁定、版权、性能、SYS-BUILD archive 和 test-only exclusion；输出 current PASS/CONCERNS/FAIL 与 blocker list；不得因复核自动推进 stage，`production/stage.txt` 仅在独立批准后变更；本冲刺明确不包含主观叙事/正典 sign-off，若门禁仍要求则记录为外部 blocker。 | 任一 required artifact 缺失/stale/`BLOCKED_INPUT`；DOCX/人工 reviewer/clean player/目标 SAPI 输入未到位；门禁报告与 candidate/archive identity 不一致；有人要求未经批准的 stage promotion。 | `production/gate-checks/production-to-polish-2026-08-xx-final.md`、完整 traceability matrix、evidence index、阻塞项 adjudication、stage unchanged/promotion decision record、最终 QA sign-off。 |

### Historical Should Have — preserved original Sprint 013 scope (superseded)

| ID | Task / Owner | Est. h (days) | Dependencies | Acceptance criteria | Blocking conditions | Required QA evidence |
|---|---|---:|---|---|---|---|
| S13-01 | 第二位独立无调试玩家理解度复测 / Andwey | 6h (0.75d) | N13-08、N13-12 无 blocker | 第二位未接触内部设计/调试信息的玩家独立完成指定流程，并能解释选择回收、存取档/日志/成就和结局原因；与第一轮结果分离记录，不能用平均分掩盖关键误解。 | 没有第二位玩家；候选版本已变更；回答缺少原始记录或观察者诱导。 | 第二份 clean-player raw record、问卷/口述转录、observer log、版本 hash、差异与复现报告。 |
| S13-02 | 第二环境/第二输入方式的 Release 证据复跑 | 6h (0.75d) | N13-05、N13-11、同一 runner/candidate identity | 在另一台批准的 Windows 10/11 环境或批准的第二输入组合复跑最小 critical path 与 RELEASE exclusion；结果与第一环境不矛盾，所有 artifact identity 明确区分。 | 第二环境不可用；runner/candidate identity 不同且无法重新封板；只复制截图没有 raw run。 | 第二环境 preflight、关键路径 raw trace、截图/transcript、exclusion report、identity comparison、差异 adjudication。 |
| S13-03 | 性能重复性/短时 soak 复测 | 5h (0.625d) | N13-09 PASS、N13-11 candidate archived | 依同一 protocol 做批准次数的冷/热启动或短时连续流程复测，报告波动、p95/max 与资源趋势；不得以无阈值数据制造 PASS。 | N13-09 为 REPORT_ONLY/FAIL；阈值或样本协议不完整；测试过程引入 benchmark harness 到正式 archive。 | 第二轮 raw samples、protocol/hash 对照、波动分析、资源/崩溃日志、更新后的 performance adjudication。 |

**Nice to Have：无。** 本冲刺明确不增加超出上述 Production 收尾边界的工作；Should Have 已是唯一可选扩展。

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| DOCX 参考未在工作区提供或许可边界不可证 | High | High | N13-10 先做 provenance lookup；缺源即 `BLOCKED_INPUT`，不以摘要、默认同人声明或自动扫描替代权利确认。 |
| SAPI 能力可枚举但实际语音/听测不可用 | Medium | High | 固定 preflight、raw transcript 和人工 adjudication；只能记录 `UNVERIFIED_NONVISUAL`，不宣称非视觉 PASS。 |
| 手工流程或证据期间 source/content hash 漂移 | Medium | High | N13-01 冻结 topology/content-lock 世代；N13-11 前重新计算 identity，旧 artifact 标记 `STALE` 并完整重跑。 |
| 长流程人工试玩出现不可复现问题 | Medium | High | 用六结局 witness manifest、批准 checkpoint 和原始输入/存档记录；禁止使用 debug 直接修复证据。 |
| test-only 工具进入 staging/archive | Medium | High | SYS-BUILD staging 与 archive 各做一次 exclusion scan；泄漏即阻断，不靠手工删除后声称同一 candidate。 |
| 当前没有正式 milestone/risk-register 文件 | High | Medium | 以最终 Production gate 报告为本冲刺约束；本计划中所有外部输入和 blocker 必须落入最终 gate report。 |

## External Dependencies

- 可运行的 Windows 10/11 + Ren’Py 8.5.3 当前候选环境，以及批准的 package runner/capability manifest。
- 至少一套可用的简体中文 Windows SAPI 配置和可完成听测的 reviewer。
- 一位不接触 debug/test 入口的试玩者；Should Have 的第二位玩家另计。
- 实际 DOCX 参考文件或明确的 owner provenance/版权决定；工作区当前未发现 `.docx` 文件。
- SYS-BUILD 与 SYS-TEST 能在同一 candidate identity 下完成 staging/archive 双阶段证据绑定。

## Definition of Done

- [ ] N13-01 至 N13-12 全部完成；不得以 `REPORT_ONLY`、`BLOCKED_INPUT`、`STALE` 或人工未裁定关闭 Must Have。
- [ ] 六结局、Day 1–Day 7、`rain_stops` 尾声的实际玩家流程和无 debug 证据齐全。
- [ ] 存档/读档、日志/愿望手册、成就、persistent 状态在同一 candidate identity 下通过。
- [ ] 键鼠、字体倍率、焦点/viewport、五项无障碍设置、SAPI/transcript、语义等价人工复核均有 current raw evidence。
- [ ] DOCX/同人版权边界有 owner decision；当前缺少实际 DOCX 时 N13-10 必须保留 `BLOCKED_INPUT`，不得宣称完成或用摘要替代，最终报告必须保留 blocker。
- [ ] SYS-BUILD staging/archive、legal closure、hash、两次 test-only exclusion 与 release evidence index 齐全。
- [ ] Final Production → Polish gate report 已生成；本冲刺不自动更新 `production/stage.txt`，也不把 Polish promotion 当作本冲刺默认结果。
- [ ] 不新增角色立绘、背景、CG、UI 位图、音乐、音效、配音或其他正式游戏资产。
- [ ] 所有 Must 任务的 automated/engine/manual evidence 均可重放、非空、hash/current；无 S1/S2 bug。
- [x] `production/qa/qa-plan-sprint-013-2026-08-15.md` 已存在；实现完成后仍须生成最终 QA sign-off report。

> **QA Plan**：`production/qa/qa-plan-sprint-013-2026-08-15.md` 已生成。该计划把本冲刺的自动化、人工、试玩、SAPI/transcript、性能、版权和 SYS-BUILD RELEASE 证据要求冻结为可追踪的 case/criterion；最终 Production → Polish 门禁仍要求 current QA sign-off。

## Next Steps

1. 使用已存在并已同步 N13-08 门禁要求的 `production/qa/qa-plan-sprint-013-2026-08-15.md`。
2. 逐项执行 `/story-readiness`（本冲刺任务以本文件的 N13/S13 work package 为范围）并从 N13-01 开始。
3. 在所有 Must 证据 current 后执行 `/smoke-check sprint`，再完成 N13-12 的最终 gate report。
4. 只有最终 gate 明确 PASS 且获得独立 stage 决策批准时，才考虑 Production → Polish 的阶段变更。
