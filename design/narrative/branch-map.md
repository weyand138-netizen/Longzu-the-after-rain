# 七日分支图 v0.1

## 分支原则

- 每个重大选择可以影响零至两条主轴，避免单选项成为万能答案。
- 预算按“单条可达路径、每章、每轴最多一次”统计，不按整章所有互斥分支合计。
- 即时对白不能直接说明“正确/错误”，但要让玩家理解自己的行为产生了什么感受。
- 延迟回收必须具体落到人、物、信息或承诺。
- 第七日不追加能覆盖前六日的“终极选择题”。

## 六结局路径证明规范

完整七日分支图必须为每个正式结局提供至少一条首周目标准见证路径：

| 结局 ID | 路径证明要求 | 当前状态 |
|---|---|---|
| `rain_stops` | 五轴最终全 3、未解决反证 token 集合为空；每轴四次机器可证独立得分机会，并有“错过最早一次、后三次补回”的见证 | `witness_rain_stops_v1` 完整 history、五轴 recovery opportunity matrix 与五条 earliest-miss histories 已在 baseline v1.2 冻结；compiler replay evidence pending |
| `her_own_name` | 首周目可达，命中本结局且不命中更高优先级结局 | `witness_her_own_name_v1` 已冻结 |
| `see_the_sea` | 首周目可达，命中本结局且不命中更高优先级结局 | `witness_see_the_sea_v1` 已冻结 |
| `one_person_train` | 首周目可达，命中本结局且不命中更高优先级结局 | `witness_one_person_train_v1` 已冻结 |
| `golden_cage` | 首周目可达，命中本结局且不命中更高优先级结局 | `witness_golden_cage_v1` 已冻结 |
| `unsent_postcard` | 首周目可达，命中本结局且不命中更高优先级结局 | `witness_unsent_postcard_v1` 已冻结 |

六条从 New Game 到 EndingEntry 的完整 ordered choice histories、五轴 recovery opportunity matrix、五条 earliest-miss histories、四项 qualification bindings、7 项 repairable tokens 与 11 个 cause-family production variants 的 normative source 是 [七日内容基线 v1.2](seven-day-content-baseline.md)。Cause families 不是 exact terminal equivalence classes；actual classes 必须由全图枚举生成。本文件只保留图原则和高层回收矩阵，避免建立第二份不同步的 exact catalog。

每条路径记录必须逐章列出全部有序 player-facing choice IDs（包括零轴、repair/keep 与 route commitment）、增量、章末五轴、每次产生或定向修复的 token、answer/outcome facts、route resources、结局时未解决集合和最终唯一结局。验证必须从 New Game 入口逐 node replay；只向 resolver 提交省略 opener/必经节点的 decisive-choice 摘要不构成可达性证明。不得使用开发标记、旧存档、跨周目解锁、随机结果、直接写值或互斥选择并存来证明可达性。

真结局恢复矩阵固定为：

- U：`prologue_read_note → day1_read_food_gesture → day2_accept_alias → day3_honor_pause`
- A：`prologue_accept_destination → day2_accept_alias → day3_honor_pause → day5_honor_erii_response`
- T：`prologue_notice_tracker → day3_share_school_evidence → day4_register_independent_contact → day5_share_full_archive`
- P：`prologue_notice_service_exit → day2_save_second_token → day4_buy_two_tickets_real_name → day5_include_self_in_truth`
- S：`day2_spend_both_tokens → day4_buy_two_tickets_real_name → day5_include_self_in_truth → day6_burn_old_identity`

五条 earliest-miss witnesses 必须分别错过对应第一项，并从其余三项恢复到 3；任一路径、任一章节、任一轴最多实际增量一次。

## 选择反馈与防严格劣势

Production scanner 必须枚举所有 menu、timed outcome 与 accessibility-equivalent 叙事选项；每项恰分类为 `semantic_major` 或 `narrative_only`，只有系统导航可进入 non-narrative allowlist。Semantic major 继续使用完整十字段 metadata；两类都必须有稳定 ID、CFG-postdominating reaction binding 与 payoff IDs。对每个 canonical prehistory 和完整合法 terminal continuation，必须有真实路径上的严格较晚 payoff，并以 history guard 或反事实 registered outcome 证明来自原 choice；通用无关结局事件不合格。

重大选择图必须是从新游戏到 ending entry 的有限 DAG。严格劣势检查对同 node 的每个可达 prehistory `h` 枚举完整 continuation language `L_A(h)` / `L_B(h)`；必须先证明 `L_A(h) ⊆ L_B(h)`，即 A 后每条合法 choice-ID suffix 在 B 后仍能按原顺序执行。相同可达 node 集或相同结局不等价于 language 包含。随后每个 suffix 的每个对齐前缀都必须满足 `U_B ⊆ U_A`；稀疏资源成本按 key 并集、缺键为 0，互不包含 token 集不可比较。只有所有维度均不差且至少一项严格改善时，A 才属于严格劣势。

五轴封顶不抹去后续行为。少量路线关键反向选择产生全局唯一 revoke token，并显式分类为 `repairable` 或经独立审核的 `irreversible`。repair domain 必须匹配目标 token，发生在具体后果可观察之后，并且每条到达路径在 repair 前都证明目标仍 unresolved；一次只能指向一个既存 repairable token。不可逆 token 的每条 continuation 都必须证明最短后续重大选择数至少为 2，并至少包含一个会改变结局选择、人物归宿、代价承担者或悲剧闭环的实质 agency witness；witness 必须登记 agency node 的全部 `branch_choice_id → outcome_reference_ids`，至少两个分支映射到不同注册 outcome。每个 outcome ID 必须解析到含 kind、subject、state 与 source events 的正式记录。无关填充节点不计。其 approval 的 `author_id`/`reviewer_id` 必须解析到项目身份注册表，并按 `canonical_person_id` 证明不是同一人，同时提供严重性证据和每个可达结局的 token-specific payoff。不存在 `grant`，普通正向选择不能清除 token。

不同 `immediate_reaction_id`、`payoff_id`、文本、镜头或动画不自动构成独有价值；严格劣势检查只读取实体注册表中 `kind: semantic_value` 的审核标签。每轴独立得分机会也必须满足 GDD 的图枚举定义：跳过较早机会后，后三个稳定节点仍可达、增量不变且不会自动改变 token。

六个结局的每条标准见证都必须登记 `ending_causality_record`：matched cause IDs、对每个更高优先级结局的具体 exclusion cause IDs、payoff scene 与玩家可感知摘要。Cause 只能引用具体选择证据、unresolved token、登记的证据缺失或路线资源/承诺；不能引用裸阈值。好结局必须解释为何不是更完整的上位结局，苦涩/悲剧必须回收决定性损失，真结局必须回收完整成立的证据与承担。

Canonical witness 之外，全部 terminal paths 按完整 cause/outcome signature 分区。Clause templates 与 per-token audit templates 使用不同 lineage key；payload matrix 冻结 contributors/value/anchors。Priority stage 生成 cause-ready `FrozenResolutionEvaluation`，cause extraction 不再读取 history/catalog。四种输出 record 的 module/qualname/field order唯一，runtime ID 使用规范 bytes 完整 SHA-256。Class 预算与 display 规则不变。

正式路线资格只从 ordered `choice_history` 纯派生：冻结 projection catalog 为每个 choice 映射 completed events 以及 resource acquire/consume effects，resolver 左到右重建 event/resource facts，不读取 store、persistent、event manager 或 inventory live state。重复 acquire 与 absent consume 在 route-fact fold 固定失败，不能静默 set no-op。资格只用于路线成员关系、互斥承诺或具体资源持有。不得保存 `qualified_*` 布尔值，不得按五轴创建五条正向资格；`rain_stops` 恰由五轴全 3 且 unresolved-token 为空成立，不能读取资格。

## 章节回收矩阵

| 章节 | 关键输入 | 当章输出 | 后续主要回收 |
|---|---|---|---|
| 序章 | 先看愿望纸 / 先催促 / 自己定路线 | 理解、自主、准备的初始差异 | 第一日愿望讨论、第六日撤离 |
| 第一日 | 谁选择便服与食物 | 自主、理解 | 第五日是否愿意分享真相 |
| 第二日 | 游戏昵称与两枚游戏币 | 理解、准备 | 真结局网吧、盟友识别 |
| 第三日 | 隐瞒 / 坦白 / 逃避 | 真相、自主 | 第五日信任与第六日服从 |
| 第四日 | 车票、路线、联系人 | 准备、代价 | 第六日安全屋失败后的备选 |
| 第五日 | 如何交付真相 | 真相、自主、理解 | 第七日是否共同决策 |
| 第六日 | 保护谁、使用何物、兑现何诺 | 准备、代价 | 结局资源与身份代价 |
| 第七日 | 对既有因果的承认 | 不新增万能分数 | 唯一结局 |

## 序章当前实现

```text
雨夜站台
  ├─ 先读被雨打湿的纸 -> understanding +1
  │    ├─ 问她想去哪 -> 0（request/answer）
  │    │    ├─ 接受她指的小站 -> autonomy +1
  │    │    └─ 改走更快东线 -> 0 + autonomy counterevidence
  │    └─ 替她决定 -> 0 + autonomy counterevidence（保留速度优势）
  └─ 先催她上车 -> 0（保留即时安全收益）
       ├─ 回头问她 -> 0（request/answer）
       │    ├─ 接受她指的小站 -> autonomy +1
       │    └─ 改走更快东线 -> 0 + autonomy counterevidence
       └─ 坚持计划 -> 0 + autonomy counterevidence（保留速度优势）

检票口
  ├─ 记住维修通道 -> preparation +1
  ├─ 对照鞋底红泥与站台泥痕，并把追踪方向指给她看 -> truth +1
  └─ 约定共同决定 -> 0（记录约定；实际支付代价后才增加 sacrifice）

临时收束：写入章节回忆，跳回主菜单。
```

序章不直接产生正式六结局；调试入口可调用纯结局解析器验证当前状态。
