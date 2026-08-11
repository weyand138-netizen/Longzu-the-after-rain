# 系统索引

| ID | 系统 | 层级 | MVP | 依赖 | 状态 | 设计文档 | 验收摘要 |
|---|---|---|---|---|---|---|---|
| SYS-STATE | 五轴局内状态 | Core | P0 | Ren'Py rollback | Approved | [GDD](five-axis-state.md) | 第十二次最终定点验证 4/4 PASS；cause-ready artifact 与 narrative-only history 已闭合，choice/reaction/payoff exact joins 转为 SYS-CHOICE/SYS-NARRATIVE provisional 下游门槛 |
| SYS-CHOICE | 选择与因果记录 | Feature | P0 | SYS-STATE + SYS-ENDING contract | Approved with provisional downstream gates | [GDD](choice-and-causality-record.md) | 2026-07-28 固定 Required 1–7 定点封板 7/7 PASS；Agency、accessible presentation与Player Fantasy分别由SYS-NARRATIVE、SYS-ACCESS + UX Designer及无调试playtest下游关闭 |
| SYS-ENDING | 确定性结局判定 | Core | P0 | SYS-STATE | Approved with provisional downstream gates | [GDD](deterministic-ending-resolution.md) | 五项核心合同定点封板 5/5 PASS；2026-08-09 targeted closure 冻结 `commit_ending_completion` owner、六个 terminal completion nodes、completion event 与 rollback/persistent 语义；Q1/Q2/Q3/Q5/Q6/Q7 仍为下游门槛 |
| SYS-NARRATIVE | 七日章节脚本 | Feature | P0 | SYS-CHOICE + SYS-ENDING | Approved with provisional downstream gates | [GDD](seven-day-chapter-script.md) | 2026-07-29独立design-review的历史修订项已在当前文档闭合；Q8–Q13保留为下游content-lock/integration gates |
| SYS-SAVE | 存档/读档/回退 | Foundation | P0 | Engine + SYS-STATE + SYS-ENDING + SYS-CHOICE + SYS-NARRATIVE contracts | Approved with provisional downstream gates | [GDD](save-load-rollback.md) | 2026-07-29 full design-review的历史修订项已同步至当前合同；Q1/Q2/Q7 保留为 implementation-ready 下游门槛 |
| SYS-PERSIST | 跨周目解锁 | Foundation | P0 | Engine + SYS-ENDING/SYS-NARRATIVE completed-event contracts | Approved with provisional downstream gates | [GDD](cross-playthrough-unlocks.md) | 2026-08-09 P0 targeted closure：单一 schema-v2 root、12-leaf ownership manifest、五项设置、collection epoch、achievement seen subset、ending completion event、epoch-aware merge/reset、batch/flush、单向 projection与safe recovery；旧权威引用清零；实现证据仍为下游门槛 |
| SYS-ACHIEVE | 11 项本地成就 | Feature | P0 | SYS-PERSIST schema v2 + SYS-NARRATIVE `achievement_event_catalog:v2` + SYS-SAVE epoch contract + SYS-JOURNAL/SYS-ACCESS | Approved | [GDD](local-achievements.md) | 2026-07-30初审为MAJOR REVISION NEEDED；制作人批准11项独立成就、`seen_achievement_ids`与v2完整修订，并选择豁免独立复审。Design Approved；backend、真实content callsites、UI/audio与performance仍是下游implementation gates |
| SYS-JOURNAL | 愿望手册 UI | Presentation | P0 | SYS-PERSIST snapshot/mark-seen + SYS-NARRATIVE/SYS-ACHIEVE/SYS-ENDING player-safe catalogs + SYS-ACCESS/SYS-SAVE UI contracts + SYS-BUILD bundle packaging | Approved with provisional downstream gates | [GDD](sys-journal.md) | 2026-08-04 NEEDS REVISION blockers已修订：common-path Day truth、bundle ownership/error domains、bounded evidence accumulator、reentrant终态、4/4 category fault路由与SYS-SAVE反向接口；实现、UX与性能仍为下游门槛 |
| SYS-ACCESS | 无障碍设置 | Presentation | P0 | Ren'Py 8.5.3 + SYS-PERSIST + downstream surface contracts | Approved with provisional downstream gates | [GDD](sys-access.md) | 冻结12-leaf/5-setting目标合同、键盘/鼠标语义等价、self-voicing、720p×1.5字体与效果替代；legacy pre-v2 事实只作不兼容 fixture，不构成并行权威；engine/UX证据仍为下游门槛 |
| SYS-TENSION | 可选紧张模式 | Feature | P1 | Ren'Py 8.5.3 + SYS-CHOICE + SYS-NARRATIVE + SYS-ACCESS + SYS-SAVE/SYS-TEST integration contracts | Deferred to post-MVP | [GDD](sys-tension.md) | 按最快进入 Production 的 scope decision 延期至 post-MVP；不进入当前 P0 Production gate，不改动 SYS-PERSIST 12-leaf/5-setting 合同；原 42 AC、偏好 owner、active-timer recovery 与 Q1–Q11 保留为 post-MVP implementation gates |
| SYS-GALLERY | CG/回忆画廊 | Presentation | P1 | SYS-PERSIST | Not Started | — | 锁定状态不泄露剧情 |
| SYS-AUDIO | 音乐与环境音 | Presentation | P1 | Assets | Not Started | — | 独立音量、授权可追踪 |
| SYS-BUILD | 构建与发布 | Platform | P0 | Engine + approved source manifests + SYS-JOURNAL bundle assembler contract + SYS-TEST bidirectional release evidence | Approved with provisional downstream gates | [GDD](sys-build.md) | 2026-08-09 ADR-0007 contract closure：runner capability、`candidate_manifest:v1`、固定产物目录、canonical encoding、provenance/legal closure、archive hashing、test-only isolation与staging/archive双向 evidence 已冻结；identity-affecting config 与 run-only config 已分离；BUILD-Q1–Q5 closed，Q6–Q9 为后续 implementation/release gates，不阻止 GDD 封板 |
| SYS-TEST | 自动化验证 | Foundation | P0 | Engine/Python + SYS-STATE + SYS-ENDING + SYS-CHOICE + SYS-NARRATIVE + SYS-SAVE + SYS-PERSIST + SYS-ACHIEVE + SYS-JOURNAL + SYS-ACCESS + SYS-BUILD candidate/evidence contract | Approved | [GDD](sys-test.md) | 2026-08-09 ADR-0007 targeted closure：`candidate_manifest:v1` 驱动的 `STAGING_EVIDENCE_BOUND` 与 `ARCHIVE_EVIDENCE_BOUND` 双阶段、同世代 hash binding、两次 test-only exclusion scan 与 release evidence 回传已冻结；SYS-TENSION timing suite 仍为 post-MVP |

## 依赖顺序

`SYS-STATE -> SYS-ENDING -> SYS-CHOICE -> SYS-NARRATIVE -> SYS-PERSIST -> SYS-ACHIEVE -> SYS-JOURNAL`

`SYS-SAVE`、`SYS-ACCESS`、`SYS-TEST` 从第一段可玩内容开始贯穿所有系统。

## 设计进度

- 全部系统：当前状态统计沿用生命周期标签；SYS-TENSION 已标记 `Deferred to post-MVP`，不计入当前 P0 Production gate；其余系统的 downstream implementation gates 保持原 owner 约束。
- P0 系统：当前 Production scope 包含 SYS-STATE、SYS-CHOICE、SYS-ENDING、SYS-NARRATIVE、SYS-SAVE、SYS-PERSIST、SYS-ACHIEVE、SYS-JOURNAL、SYS-ACCESS、SYS-BUILD 与 SYS-TEST；C-03/C-04 不在此 scope。
- P1 系统：SYS-TENSION 的 timed-choice、preference storage 与 active-timer recovery 均延期至 post-MVP；SYS-GALLERY 与 SYS-AUDIO 仍按各自设计状态推进。
