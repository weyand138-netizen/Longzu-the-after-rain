# 七日内容基线

> **Status**: Normative design baseline v1.3 — independent re-review blockers revised; pending re-review
> **Owner**: SYS-NARRATIVE
> **Version**: `narrative_content_baseline:v1.3`
> **Date**: 2026-08-14
> **Governing GDD**: [七日章节脚本](../gdd/seven-day-chapter-script.md)

本文件冻结七日主线的内容身份、核心场景、正式玩家选择、agency transaction、路线资格、反证 token 与六结局见证。逐句对白、镜头和最终资产仍由 `game/chapters/`、Art Bible 与 `/asset-spec` 承担；这些下游交付不得改变本文件的稳定 ID、人物决定、因果方向或结局归宿。v1.3 只扩展既有 `rain_stops` 尾声的表现边界，不增加 canonical unit 或语义合同。

## Canonical Production Units

`canonical_production_units_v1` 恰为以下 15 项，顺序也是 source manifest、章节导航和测试报告的 canonical order：

1. `chapter_prologue_rain_platform`
2. `chapter_day1_her_own_name`
3. `chapter_day2_two_game_tokens`
4. `chapter_day3_empty_school`
5. `chapter_day4_seaside_train`
6. `chapter_day5_family_lie`
7. `chapter_day6_no_safe_house`
8. `chapter_day7_before_red_well`
9. `ending_rain_stops`
10. `ending_her_own_name`
11. `ending_see_the_sea`
12. `ending_one_person_train`
13. `ending_golden_cage`
14. `ending_unsent_postcard`
15. `epilogue_rain_stops_arcade`

Production manifest 的 `expected_units` 与 `scanned_units` 必须 exact-equal 该 tuple 对应的无重复集合；六个 ending units 与真结局可玩尾声均不可删除。“适用尾声”在本版本中只指 `rain_stops` 必须进入 `epilogue_rain_stops_arcade`，其他结局不得复用该尾声。v1.3 的多年以后短尾声仍属于该同一 unit，不能拆出第 16 个 unit。

## Character Constraint Catalog

本基线的 production scene 只允许 `character_lu_mingfei` 与 `character_erii` 成为 active characters。追踪者、家族、联系人和外部协助只通过已登记信息、物件与 outcome 出现；任何新增 active character 必须先增加独立 constraint record 并重新审核受影响场景。

| Character | Source references | Speech / knowledge / motivation bounds | Forbidden behaviors | Approval |
|---|---|---|---|---|
| `character_erii` | `source_game_concept_character_expression`、`source_project_nonnegotiable_rules` | 不进行完整口语对白；复杂意图只用视线、动作、停顿、物件、上下文和简单单音节；只知道已亲历或已向她交付的信息；核心动机是形成并维护自己的决定 | 沉默被写成同意；连续书面文本替代口语；解释隐藏分数、正确答案或结局条件；无因接受已拒绝安排 | `approval_character_erii_v1` |
| `character_lu_mingfei` | `source_game_concept_player_fantasy`、`source_project_nonnegotiable_rules` | 可以复述自己的理解，但必须允许绘梨衣确认、否认、拒绝或暂不回答；只知道已观察、验证或获得的事实；核心冲突是即时保护冲动与尊重自主之间的选择 | 替作者宣布正确选项；读取内部轴/token/qualification；无因获得家族全知信息；以旁白抹除自己的违背 | `approval_character_lu_mingfei_v1` |

两个 approval records 均使用 `character_constraint_review:v1` checklist，固定检查 `speech`、`known_facts`、`motivation`、`relationship_baseline`、`forbidden_behavior` 五项；只有 source hash 匹配、五项均 `pass` 且 `unresolved_defect_ids=()` 时有效。

尾声中的普通街坊观察者、非具名旧友与普通顾客是局外观察层的非 active-character 背景，不新增 character constraint record。绘梨衣复杂内容只能作为明确标记的书面手记出现，不能写成完整口语对白，也不能借书面手记解释隐藏规则、正确答案或结局条件。

## Chapter and Scene Beat Catalog

下表冻结 required scenes。`active` 未特别注明时均为 `character_lu_mingfei + character_erii`。

| Unit | Responsibility ID | Required scene IDs | Content purpose and mandatory outcome | Next |
|---|---|---|---|---|
| 序章 | `responsibility_prologue_observe_ask_prepare` | `scene_prologue_note`、`scene_prologue_destination`、`scene_prologue_ticket_gate`、`scene_prologue_train_close` | 发现或保住愿望纸；区分 request、answer 与 response；建立追踪、维修通道或共同承担承诺 | Day 1 |
| Day 1 | `responsibility_day1_daily_autonomy` | `scene_day1_clothing_answer`、`scene_day1_food_gesture`、`scene_day1_receipt_name` | 绘梨衣以衣物和点单动作表达偏好；玩家接受、误读或覆盖；收据上的名字成为 Day 4/5 回收锚点 | Day 2 |
| Day 2 | `responsibility_day2_alias_and_tokens` | `scene_day2_alias_answer`、`scene_day2_two_tokens`、`scene_day2_last_machine` | 绘梨衣选择屏幕昵称；两枚游戏币在“当下快乐”与“保留识别物”之间形成真实取舍 | Day 3 |
| Day 3 | `responsibility_day3_evidence_and_pause` | `scene_day3_classroom_trace`、`scene_day3_evidence_choice`、`scene_day3_truth_pace_answer` | 交叉验证空教室中的监视证据；决定分享、隐瞒及是否尊重暂停表达 | Day 4 |
| Day 4 | `responsibility_day4_self_controlled_options` | `scene_day4_ticket_counter`、`scene_day4_route_answer`、`scene_day4_contact_channel`、`scene_day4_sea_window` | 将此前回答变成双人票、单人票、独立联系人或无备选路线；真实姓名购票同时建立代价 | Day 5 |
| Day 5 | `responsibility_day5_truth_and_route_answer` | `scene_day5_family_archive`、`scene_day5_truth_delivery`、`scene_day5_response_answer`、`scene_day5_shared_liability` | 交付完整家族真相或安全化摘要；绘梨衣决定回应；路明非决定是否承认自己的责任 | Day 6 |
| Day 6 | `responsibility_day6_resources_cost_and_commitment` | `scene_day6_safehouse_failure`、`scene_day6_backup_exit`、`scene_day6_cost_inventory`、`scene_day6_route_commitment` | 回收维修通道、游戏币、车票、联系人和承诺；安全屋失效后只能提交一个可执行路线或承认没有路线 | Day 7 |
| Day 7 | `responsibility_day7_acknowledge_and_resolve` | `scene_day7_red_well_approach`、`scene_day7_causal_recall`、`scene_day7_ending_entry` | 只回放并承认前六日事实；不增加 axis、不 repair token、不产生 qualification；调用唯一 resolver | One ending |
| `rain_stops` | `responsibility_ending_rain_stops` | `scene_ending_rain_stops` | 路明非放弃力量与旧身份；绘梨衣保留自己的名字、决定和普通生活计划 | True epilogue |
| `her_own_name` | `responsibility_ending_her_own_name` | `scene_ending_her_own_name` | 绘梨衣依独立联系人离开；两人暂时分隔但保留持续联系 | End |
| `see_the_sea` | `responsibility_ending_see_the_sea` | `scene_ending_see_the_sea` | 两人共同逃离；身份或路线代价已经支付，未来危险由双方选择 | End |
| `one_person_train` | `responsibility_ending_one_person_train` | `scene_ending_one_person_train` | 绘梨衣拥有单人离开方案，但理解或准备不足使两人失散 | End |
| `golden_cage` | `responsibility_ending_golden_cage` | `scene_ending_golden_cage` | “安全”压过她已表达的决定；未解决 autonomy 违背将她送回旧秩序 | End |
| `unsent_postcard` | `responsibility_ending_unsent_postcard` | `scene_ending_unsent_postcard` | 没有可执行路线，或关键真相/准备/代价崩塌；愿望纸与明信片形成完整悲剧闭环 | End |
| True epilogue | `responsibility_epilogue_ordinary_future` | `scene_epilogue_first_guest`、`scene_epilogue_lights_out` | 可玩网吧日常；使用第二枚游戏币/昵称回声；完成“第一位客人”和“关灯回家”两个具体事件；之后可在同一 unit 内追加克制的多年以后观察与书面手记尾声 | End |

Optional scenes 只能补充节奏、人物呼吸或已登记 payoff，不得新增 axis、token、qualification、ending source 或 active character。

## `rain_stops` Epilogue Extension Boundary

本版本只允许在现有 `scene_epilogue_lights_out` 完成后追加一段短尾声，且
仍由 `responsibility_epilogue_ordinary_future` 负责。尾声保留两个结构元素：

- 普通街坊对小网吧多年后仍作为普通生意存在的局外观察；只可使用少量非具名旧友和普通顾客作为背景，不确认任何新增重大世界状态。
- 绘梨衣明确标注为“书面手记”的短段落；复杂内容只能属于纸面记录，不能以完整口语对白演出，也不能由 `erii` 对白承载。

该扩展不新增 choice、reaction、payoff、event、axis、token、resource、
qualification、ending predicate、resolver 输入、persistent 字段、成就、
Gallery、stable label、canonical unit 或 completion boundary。现有
`event_epilogue_first_guest_completed` 与 `event_epilogue_lights_out_completed`
仍是唯一尾声 completion events，新增文字发生在 lights-out completion 之后。

扩展只借鉴未确认同人改编参考的高层结构和主题，不逐句复制；夏弥、源氏兄弟、
路鸣泽家庭化、怀孕、龙凤胎及其他额外正典事实均保持未确认。

## Choice, Reaction and Payoff Catalog

以下 54 项是 `narrative_content_baseline:v1.2` 的完整 production player-facing choice universe。新增、删除或重分类任何一项都使 catalog hash 失效并要求重新运行完整 join、payoff、qualification 与 witness 验证。

记号：`U/A/T/P/S` 分别为 understanding/autonomy/truth/preparation/sacrifice 的 `+1`；`R:<token>` 为 revoke；`F:<token>` 为 repair。每个 choice 的即时反应 ID 固定为 `reaction_<choice_id>`，表中 payoff ID 均严格晚于 choice 所在节点。

| Choice ID | Class / projection | Immediate reaction identity | Strictly-later payoff ID and perceptible change |
|---|---|---|---|
| `prologue_read_note` | `semantic_major; U` | 绘梨衣按住未写完的愿望 | `payoff_prologue_read_note_day1`：Day 1 主动展开愿望纸并指向衣物 |
| `prologue_hurry_to_train` | `narrative_only; event_headstart` | 她自己捡起愿望纸 | `payoff_prologue_hurry_day6`：Day 6 多出短暂撤离时间，但她不主动交出纸 |
| `prologue_ask_destination` | `semantic_major; event_destination_requested; 0 axis` | 她在地图上明确指向小站 | `payoff_prologue_ask_day4`：Day 4 她主动把路线图推回玩家面前 |
| `prologue_accept_destination` | `semantic_major; A; completion event_achievement_ask_first_answer_honored after detour consequence` | 她收起试探姿态并保留所指路线 | `payoff_prologue_accept_day4`：她愿意共同选择海边路线 |
| `prologue_override_destination` | `semantic_major; R:token_override_first_destination` | 她松开地图，转而服从 | `payoff_prologue_override_day1`：衣物选择前先等待命令 |
| `prologue_choose_route` | `semantic_major; R:token_override_first_destination; event_fast_departure` | 她立刻点头但不再看地图 | `payoff_prologue_direct_route_day6`：保留撤离时间，同时触发 autonomy cause 候选 |
| `prologue_notice_service_exit` | `semantic_major; P; acquire resource_service_exit` | 她记住门与封条的位置 | `payoff_prologue_exit_day6`：安全屋失效时出现正式备用出口 |
| `prologue_notice_tracker` | `semantic_major; T; event_tracker_direction_shared` | 她确认并提出反方向 | `payoff_prologue_tracker_day3`：识别空教室的同源红泥 |
| `prologue_promise_cost` | `semantic_major; event_shared_cost_promised; 0 axis` | 她以手掌确认承诺 | `payoff_prologue_promise_day6`：Day 6 成本盘点先回放双方手掌确认与承诺物；承担成本时建立 `outcome_prior_cost_promise_honored`，转嫁成本时建立 `outcome_prior_cost_promise_broken`；未作承诺的路径不出现该回放或两项 outcome |
| `day1_accept_clothing` | `semantic_major; A` | 她保留自己挑出的便服 | `payoff_day1_clothing_day4`：她主动把该便服装入行李 |
| `day1_choose_safe_clothing` | `semantic_major; R:token_override_daily_choice` | 她换上安全外套但收起原选择 | `payoff_day1_safe_clothing_day5`：她先看玩家而不是档案，等待安排 |
| `day1_repair_first_destination` | `semantic_major; F:token_override_first_destination; 0 axis` | 玩家先承认序章覆盖过她的路线，再执行她此刻挑出的便服方案 | `payoff_repair_first_destination`：Day 4 她重新主动提出路线 |
| `day1_keep_first_override` | `semantic_major; R:token_override_daily_choice; event_first_override_unrepaired` | 玩家回避序章的覆盖行为，并再次以安全方案覆盖她当前挑出的衣物 | `payoff_keep_first_override`：首次路线 token 保持 unresolved；Day 5 她停止主动提供日常偏好 |
| `day1_read_food_gesture` | `semantic_major; U` | 玩家复述后，她以单音节确认 | `payoff_day1_food_day5`：玩家正确识别她拒绝继续服用不明药物 |
| `day1_assume_food_consent` | `semantic_major; R:token_silence_as_consent` | 她停止动作，没有确认 | `payoff_day1_assume_day5`：药物场景出现含混与延迟 |
| `day2_accept_alias` | `semantic_major; U+A` | 玩家正确读出并接受她自己输入的昵称 | `payoff_day2_alias_day4`：Day 4 联系渠道以她选择的昵称识别本人；真结局尾声继续回收该昵称 |
| `day2_assign_alias` | `semantic_major; R:token_override_daily_choice` | 她使用玩家输入的名字但移开手 | `payoff_day2_assigned_alias_day6`：联系人无法以她自己的标记确认身份 |
| `day2_admit_alias_unknown` | `semantic_major; U; F:token_silence_as_consent; accepting response` | 她重新演示并确认保留自己输入的昵称 | `payoff_day2_admit_day5`：含混回答时玩家会再次请求确认 |
| `day2_save_second_token` | `semantic_major; P; acquire resource_arcade_token` | 她把第二枚币交给玩家保管 | `payoff_day2_token_day6`：可用作独立联系人识别物 |
| `day2_spend_both_tokens` | `semantic_major; S; event_both_tokens_spent` | 玩家放弃把第二枚币留作路线资源，让她完成当下想玩的整局游戏 | `payoff_day2_spend_day4`：Day 4 缺少实体识别物，独立联系人节点不可用；所有结局仍保留当晚共享记忆 |
| `day3_share_school_evidence` | `semantic_major; T` | 她看完全部证据后决定暂停 | `payoff_day3_share_day5`：她愿意接过完整家族档案 |
| `day3_hide_school_evidence` | `semantic_major; R:token_hide_school_evidence` | 她只收到结论，没有获得证据 | `payoff_day3_hide_day5`：真相交付时先拒绝接触档案 |
| `day3_honor_pause` | `semantic_major; U+A` | 玩家读懂暂停动作并执行；她之后主动重新打开档案 | `payoff_day3_pause_day5`：她自己决定继续阅读 |
| `day3_force_explanation` | `semantic_major; R:token_override_daily_choice` | 她后退并停止回应 | `payoff_day3_force_day6`：危机中不再主动提供路线偏好 |
| `day4_buy_two_tickets_real_name` | `semantic_major; P+S; acquire resource_two_tickets; event_identity_exposed; completion event_two_window_tickets_acquired` | 两张靠窗票进入她手中 | `payoff_day4_two_tickets_day6`：共同逃离路线可执行，路明非身份暴露 |
| `day4_buy_single_ticket_cash` | `semantic_major; P; acquire resource_single_ticket` | 她确认只有一张票 | `payoff_day4_single_ticket_ending`：单人列车路线可执行 |
| `day4_register_independent_contact` | `semantic_major; T; consume resource_arcade_token; acquire resource_contact_card; event_contact_risk_handover_complete` | 她用自己选择的昵称和保留的游戏币完成验证，并看完联系人风险说明 | `payoff_day4_contact_ending`：独立联系路线可执行，但实体游戏币已交付且身份暴露风险上升 |
| `day4_decline_independent_contact` | `semantic_major; R:token_abandon_backup_plan; event_contact_channel_declined` | 她收回用于验证的游戏币和昵称纸条，保留隐私但放弃独立联系备选 | `payoff_day4_decline_contact_ending`：游戏币仍在，结局中不存在持续联系渠道 |
| `day4_follow_one_route_no_backup` | `semantic_major; R:token_abandon_backup_plan` | 路线图只剩一条线 | `payoff_day4_no_backup_day6`：安全屋失效后缺少第二出口 |
| `day5_share_full_archive` | `semantic_major; T; event_full_archive_shared` | 她获得原始证据与不确定项 | `payoff_day5_full_archive_day7`：能共同识别结局前风险 |
| `day5_give_safe_summary` | `semantic_major; R:token_withhold_family_truth` | 她获得安全结论但无法核对来源 | `payoff_day5_summary_day7`：关键家族事实缺失成为 ending cause |
| `day5_include_self_in_truth` | `semantic_major; P+S; event_self_liability_disclosed` | 路明非承认自己的选择也造成风险，并把自己承担的后续步骤写入路线计划 | `payoff_day5_self_liability_ending`：结局由他承担身份或分隔代价，且 Day 6 拥有可执行的责任分配 |
| `day5_blame_family_only` | `narrative_only; event_external_blame_only` | 她听见敌人，却没有听见他的责任 | `payoff_day5_blame_day6`：代价协商缺少共同承担基础 |
| `day5_honor_erii_response` | `semantic_major; A; event_route_preference_honored` | 她的独立联系、共同逃离、单独离开或继续寻找路线的具体决定被执行 | `payoff_day5_honor_day6`：Day 6 只启用与 registered answer state及现有资源一致的 commitment/fallback |
| `day5_replace_erii_response` | `semantic_major; R:token_override_daily_choice; event_route_preference_overridden_to_old_order` | 她的具体回答被旧秩序安全方案覆盖 | `payoff_day5_replace_ending`：old-order guard 与 cause 获得具体来源 |
| `day5_repair_daily_choice` | `semantic_major; F:token_override_daily_choice; 0 axis` | 玩家承认此前持续覆盖她的日常决定，并撤回自己的替代方案 | `payoff_repair_daily_choice`：她重新提供 route preference |
| `day5_keep_daily_override` | `semantic_major; event_daily_override_unrepaired; 0 axis` | 玩家维持自己的替代方案 | `payoff_keep_daily_override`：该 autonomy token 保持 unresolved |
| `day5_repair_school_evidence` | `semantic_major; F:token_hide_school_evidence; 0 axis` | 家族档案前先补交第三日被隐藏的原始证据 | `payoff_repair_school_truth`：她能把两组证据联系起来 |
| `day5_keep_school_evidence_hidden` | `semantic_major; event_school_evidence_stays_hidden; 0 axis` | 玩家继续只给结论 | `payoff_keep_school_truth_hidden`：该 truth token 保持 unresolved |
| `day6_reopen_service_exit` | `semantic_major; P; F:token_abandon_backup_plan; requires resource_service_exit` | 此前已发现的维修通道重新成为可用路线 | `payoff_day6_exit_ending`：保留车票或联系人资源；从未取得 `resource_service_exit` 的路径不得出现该 choice |
| `day6_abandon_backup` | `semantic_major; R:token_abandon_backup_plan` | 已知出口被留在封锁区 | `payoff_day6_abandon_ending`：准备不足决定人物去向 |
| `day6_use_service_exit` | `semantic_major; event_service_exit_used; 0 axis` | 已准备的维修通道按计划启用 | `payoff_day6_use_exit_ending`：保留车票或联系人资源且不产生 repair |
| `day6_keep_backup_abandoned` | `semantic_major; event_backup_stays_abandoned; 0 axis` | 已出现的路线损失仍未修复 | `payoff_day6_keep_backup_ending`：该 preparation token 保持 unresolved |
| `day6_disclose_withheld_archive` | `semantic_major; T; F:token_withhold_family_truth` | 危机后果已经出现，路明非交出此前省略的原始页 | `payoff_day6_late_truth_ending`：真相得到修复但失去提前准备时间 |
| `day6_keep_archive_withheld` | `semantic_major; event_family_truth_stays_withheld; 0 axis` | 他保留原始页，绘梨衣只能依据安全化结论行动 | `payoff_day6_keep_truth_ending`：`token_withhold_family_truth` 保持 unresolved |
| `day6_burn_old_identity` | `semantic_major; S; event_shared_cost_acknowledged; conditional completion event_prior_cost_promise_honored_without_shift` | 路明非销毁旧身份凭据，并让绘梨衣确认代价由他承担 | `payoff_day6_identity_cost_ending`：他承担身份代价；共同逃离的代价承诺成立 |
| `day6_shift_cost_to_erii` | `semantic_major; R:token_shift_promised_cost` | 必要代价被写到她的路线与身份上 | `payoff_day6_shift_cost_ending`：悲剧/苦涩结局由她承担额外损失 |
| `day6_take_cost_back` | `semantic_major; S; F:token_shift_promised_cost; event_shared_cost_acknowledged; completion event_achievement_refusal_honored` | 在转嫁后果已经可见且绘梨衣再次拒绝后，已登记成本重新由路明非承担 | `payoff_day6_take_back_ending`：移除 unresolved sacrifice token，但保留曾经转嫁代价的 residual outcome |
| `day6_leave_cost_shifted` | `semantic_major; event_shifted_cost_confirmed; 0 axis` | 后果已经可见，玩家仍维持由她承担的安排 | `payoff_day6_leave_cost_ending`：`token_shift_promised_cost` 保持 unresolved |
| `day6_commit_independent_contact` | `semantic_major; event_independent_route_committed` | 她独立保管联系人与风险说明 | `payoff_route_independent_ending`：进入 `her_own_name` 候选 |
| `day6_commit_shared_escape` | `semantic_major; event_shared_route_committed` | 她确认两张票和共同路线 | `payoff_route_shared_ending`：进入 `see_the_sea` 或更高优先级候选 |
| `day6_commit_solo_departure` | `semantic_major; event_solo_route_committed; event_no_continuing_contact_commitment` | 在不存在 contact card 时，她独自持有单人票并明确不建立持续联系承诺 | `payoff_route_solo_ending`：进入 `one_person_train` 候选，且不会同时保留独立联系承诺 |
| `day6_commit_old_order_return` | `semantic_major; event_old_order_route_committed` | 她的既有决定被旧秩序方案取代 | `payoff_route_old_order_ending`：进入 `golden_cage` 候选 |
| `day6_no_executable_route` | `semantic_major; event_route_collapse` | 两人承认没有可执行方案 | `payoff_route_collapse_ending`：fallback `unsent_postcard` 的具体原因 |

每个表项在 production catalog 中展开为一项 `player_facing_choice_record`、一项 projection、一项 reaction binding、至少一项 payoff binding、semantic evidence 与每条合法 continuation witness。表中的玩家可感知变化是 semantic-evidence 的最低内容；逐句文本不能把它降级为只换措辞或镜头。

### Choice Node Topology

以下 sibling sets 在同一 node 内互斥；箭头表示前一 node 的某个 choice 才会开启后续条件 node。所有未列为条件 node 的 chapter beat 使用确定性桥接，不产生玩家选择。

- `node_prologue_note = {prologue_read_note, prologue_hurry_to_train}`。
- `node_prologue_destination_start = {prologue_ask_destination, prologue_choose_route}`；只有 `prologue_ask_destination` 才开启 `node_prologue_destination_response = {prologue_accept_destination, prologue_override_destination}`。
- `node_prologue_gate = {prologue_notice_service_exit, prologue_notice_tracker, prologue_promise_cost}`。
- 若 `token_override_first_destination` 不存在：`node_day1_clothing_response = {day1_accept_clothing, day1_choose_safe_clothing}`；若该 token unresolved，则由互斥的 `node_day1_first_override_repair = {day1_repair_first_destination, day1_keep_first_override}` 取代普通 clothing response。两个 replacement choices 同时是当前 clothing answer 的 response：前者接受当前回答并修复旧覆盖，后者再次覆盖当前回答。
- `node_day1_food_interpretation = {day1_read_food_gesture, day1_assume_food_consent}`。
- `node_day2_alias_response = {day2_accept_alias, day2_assign_alias}`；若 `token_silence_as_consent` unresolved，第三个 sibling `day2_admit_alias_unknown` 才可出现。三项互斥且任一 choice 都结束本次 response。
- `node_day2_tokens = {day2_save_second_token, day2_spend_both_tokens}`。
- `node_day3_school_evidence = {day3_share_school_evidence, day3_hide_school_evidence}`。
- `node_day3_truth_pace = {day3_honor_pause, day3_force_explanation}`。
- `scene_day4_route_answer` 先登记绘梨衣的 `answer_state_id=preserve_executable_self_controlled_option`：她把票、路线图与联系人纸片并排放置，并把至少一项可由自己持有或执行的方案推回玩家面前。该 answer 不选择最终结局路线，只要求 Day 4 的准备保留她可控制的可执行选项。
- `node_day4_ticket_plan = {day4_buy_two_tickets_real_name, day4_buy_single_ticket_cash, day4_follow_one_route_no_backup}` 是 `agency_day4_route_preparation` 的唯一 response node；前两项接受 answer，最后一项覆盖 answer。
- 只有 approved alias outcome 与 `resource_arcade_token` 同时存在时，才开启独立的 `agency_day4_independent_contact`：绘梨衣以昵称纸与游戏币登记 `answer_state_id=keep_independent_contact_option`，随后 `node_day4_contact = {day4_register_independent_contact, day4_decline_independent_contact}`；注册接受 answer，拒绝覆盖 answer。未开启该 transaction 时不得制造 missing response。
- `node_day5_truth_delivery = {day5_share_full_archive, day5_give_safe_summary}`。
- `node_day5_liability = {day5_include_self_in_truth, day5_blame_family_only}`。
- `scene_day5_response_answer` 必须通过 `erii_route_answer_derivation:v1` 登记绘梨衣以动作/物件表达的 exact `answer_state_id`。候选与选择顺序只读取她已知且可见的 Day 4 资源事实，不读取五轴、token、qualification 或预测 ending：
  1. `resource_two_tickets` 存在 → `shared_escape`（她把两张票并排压在路线图上）；
  2. 否则 `resource_contact_card` 与 `event_contact_risk_handover_complete` 同时存在 → `independent_contact`（她独自收起联系人卡）；
  3. 否则 `resource_single_ticket` 存在且 contact card absent → `solo_departure`（她把单人票放入自己的证件夹）；
  4. 否则 → `continue_without_executable_route`（她把空路线图推回并保留未决定姿态）。
  Candidate fact set、selected state、动作证据与 scene source hash 必须冻结在 `character_answer_derivation_record`；若两个高优先级 guard 同时异常成立、资源事实不完整或动作证据缺失，answer 为 `undetermined` 且 response surface 不出现。随后 `node_day5_response = {day5_honor_erii_response, day5_replace_erii_response}`；前者产生 state-matching honored outcome，后者明确产生 `outcome_route_preference_overridden_to_old_order`。
- 若 `token_hide_school_evidence` unresolved：`node_day5_school_evidence_repair = {day5_repair_school_evidence, day5_keep_school_evidence_hidden}`。
- 只有 `token_override_daily_choice` 在进入 `scene_day5_response_answer` 前已经 unresolved 且其 consequence 已可感知时，才开启 `node_day5_daily_choice_repair = {day5_repair_daily_choice, day5_keep_daily_override}`；`day5_replace_erii_response` 当场新产生的 token 不得在同场修复。
- 若 `token_abandon_backup_plan` unresolved 且 `resource_service_exit` 存在：`node_day6_backup_repair = {day6_reopen_service_exit, day6_keep_backup_abandoned}`。若 token unresolved 但该 resource 从未取得，只开启 singleton acknowledgement `node_day6_backup_loss_acknowledgement = {day6_keep_backup_abandoned}`，不得呈现“重新开启”选项。若 token 不存在但 `resource_service_exit` 存在：`node_day6_prepared_exit = {day6_use_service_exit, day6_abandon_backup}`。
- 若 `token_withhold_family_truth` unresolved：`node_day6_late_truth = {day6_disclose_withheld_archive, day6_keep_archive_withheld}`。
- `node_day6_cost = {day6_burn_old_identity, day6_shift_cost_to_erii}`。若选择后者，必须先经过不可跳过的 `scene_day6_shifted_cost_consequence`，建立 `consequence_erii_bears_promised_cost` 与再次拒绝的 answer，之后才开启独立 transaction 的 `node_day6_cost_reconsideration = {day6_take_cost_back, day6_leave_cost_shifted}`。
- `node_day6_route_commitment` 不是自由选择结局的五项菜单。根据 Day 5 answer/outcome 与当前 resources，以下 guards 必须互斥且穷尽，并使 active choice count 恰为 1：
  - honored `independent_contact` + `resource_contact_card` + `event_contact_risk_handover_complete` → `day6_commit_independent_contact`；
  - honored `shared_escape` + `resource_two_tickets` + `event_shared_cost_acknowledged` → `day6_commit_shared_escape`；
  - honored `solo_departure` + `resource_single_ticket` + contact card absent → `day6_commit_solo_departure`；
  - `outcome_route_preference_overridden_to_old_order` + unresolved autonomy token → `day6_commit_old_order_return`；
  - 上述四项均不成立 → `day6_no_executable_route`。

### True-Ending Recovery Opportunity Matrix

以下是 `rain_stops` 的五组机器可证独立机会。每组恰冻结四个不同章节/node 的 choice IDs；“错过最早一次”见证必须选择该 sibling 的非增量/反向分支，并证明其余三项仍可达、增量不变、相关 token 可合法修复或不阻止真结局。

| Axis | Four independent opportunities in chapter order | Earliest-miss recovery |
|---|---|---|
| understanding | `prologue_read_note` → `day1_read_food_gesture` → `day2_accept_alias` → `day3_honor_pause` | 选择 `prologue_hurry_to_train` 后，后三项仍分别提供一次 U |
| autonomy | `prologue_accept_destination` → `day2_accept_alias` → `day3_honor_pause` → `day5_honor_erii_response` | 选择 `prologue_override_destination`，Day 1 用 `day1_repair_first_destination` 合法修复；后三项仍分别提供一次 A |
| truth | `prologue_notice_tracker` → `day3_share_school_evidence` → `day4_register_independent_contact` → `day5_share_full_archive` | 序章选择非 truth sibling 后，后三项仍分别提供一次 T |
| preparation | `prologue_notice_service_exit` → `day2_save_second_token` → `day4_buy_two_tickets_real_name` → `day5_include_self_in_truth` | 序章选择非 preparation sibling 后，后三项仍分别提供一次 P |
| sacrifice | `day2_spend_both_tokens` → `day4_buy_two_tickets_real_name` → `day5_include_self_in_truth` → `day6_burn_old_identity` | Day 2 选择保留游戏币后，后三项仍分别提供一次 S |

以下五条 earliest-miss witnesses 冻结为完整 ordered history；`witness_recovery_p_miss_v1` 与 `witness_recovery_s_miss_v1` 虽与 canonical true-ending history 的 choice tuple 相同，仍以不同 witness ID 记录不同被证明的 axis obligation：

| Witness | Missed earliest opportunity | Complete ordered choice history |
|---|---|---|
| `witness_recovery_u_miss_v1` | `prologue_read_note` → `prologue_hurry_to_train` | `prologue_hurry_to_train → prologue_ask_destination → prologue_accept_destination → prologue_notice_tracker → day1_accept_clothing → day1_read_food_gesture → day2_accept_alias → day2_save_second_token → day3_share_school_evidence → day3_honor_pause → day4_buy_two_tickets_real_name → day4_register_independent_contact → day5_share_full_archive → day5_include_self_in_truth → day5_honor_erii_response → day6_burn_old_identity → day6_commit_shared_escape` |
| `witness_recovery_a_miss_v1` | `prologue_accept_destination` → `prologue_override_destination` | `prologue_read_note → prologue_ask_destination → prologue_override_destination → prologue_notice_tracker → day1_repair_first_destination → day1_read_food_gesture → day2_accept_alias → day2_save_second_token → day3_share_school_evidence → day3_honor_pause → day4_buy_two_tickets_real_name → day4_register_independent_contact → day5_share_full_archive → day5_include_self_in_truth → day5_honor_erii_response → day6_burn_old_identity → day6_commit_shared_escape` |
| `witness_recovery_t_miss_v1` | `prologue_notice_tracker` → `prologue_notice_service_exit` | `prologue_read_note → prologue_ask_destination → prologue_accept_destination → prologue_notice_service_exit → day1_accept_clothing → day1_read_food_gesture → day2_accept_alias → day2_save_second_token → day3_share_school_evidence → day3_honor_pause → day4_buy_two_tickets_real_name → day4_register_independent_contact → day5_share_full_archive → day5_include_self_in_truth → day5_honor_erii_response → day6_burn_old_identity → day6_commit_shared_escape` |
| `witness_recovery_p_miss_v1` | `prologue_notice_service_exit` → `prologue_notice_tracker` | `prologue_read_note → prologue_ask_destination → prologue_accept_destination → prologue_notice_tracker → day1_accept_clothing → day1_read_food_gesture → day2_accept_alias → day2_save_second_token → day3_share_school_evidence → day3_honor_pause → day4_buy_two_tickets_real_name → day4_register_independent_contact → day5_share_full_archive → day5_include_self_in_truth → day5_honor_erii_response → day6_burn_old_identity → day6_commit_shared_escape` |
| `witness_recovery_s_miss_v1` | `day2_spend_both_tokens` → `day2_save_second_token` | `prologue_read_note → prologue_ask_destination → prologue_accept_destination → prologue_notice_tracker → day1_accept_clothing → day1_read_food_gesture → day2_accept_alias → day2_save_second_token → day3_share_school_evidence → day3_honor_pause → day4_buy_two_tickets_real_name → day4_register_independent_contact → day5_share_full_archive → day5_include_self_in_truth → day5_honor_erii_response → day6_burn_old_identity → day6_commit_shared_escape` |

每条 replay 必须证明对应后三项机会仍分别贡献 `+1`、每路径每章每轴最多一次、所有 token 依 contributor-aware repair 合法处理、最终五轴全 3 且命中 `rain_stops`；不得只直接写最终轴值。

## Agency Transaction Catalog

每个 transaction 引用一项 `character_answer_derivation_record`：

`derivation_id, transaction_id, input_fact_ids, allowed_answer_state_ids, selected_answer_state_id, observable_action_or_object_ids, priority_rule_id, source_hash, unresolved_defect_ids`

通过条件为输入事实引用完整、候选闭集 exact-match、选中状态由冻结 priority rule 唯一导出、至少一个动作/物件证据可被玩家感知、source hash 匹配且 defects 为空。Derivation 不得读取五轴、token、qualification、ending predicate 或开发标记。固定 request/answer 的简单 transaction 仍必须用单候选 derivation record，不能靠作者直接赋值绕过证据。

| Transaction | Request / answer | Accepting responses | Overriding responses | Exact per-response outcomes |
|---|---|---|---|---|
| `agency_prologue_destination` | `event_destination_requested` / `event_erii_points_small_station` | `prologue_accept_destination` | `prologue_override_destination` | accept → `outcome_destination_honored`；override → `outcome_destination_overridden` |
| `agency_day1_clothing` | `event_clothing_preference_requested` / `event_erii_selects_casual_clothes` | `day1_accept_clothing`、`day1_repair_first_destination` | `day1_choose_safe_clothing`、`day1_keep_first_override` | accept → `outcome_clothing_honored`；repair → `outcome_clothing_honored_after_route_repair`；safe/keep → `outcome_clothing_overridden` |
| `agency_day2_alias` | `event_alias_requested` / `event_erii_enters_alias` | `day2_accept_alias`、`day2_admit_alias_unknown` | `day2_assign_alias` | accept → `outcome_alias_honored`；admit → `outcome_alias_replayed_and_honored`；assign → `outcome_alias_overridden` |
| `agency_day3_truth_pace` | `event_truth_pace_requested` / `event_erii_closes_archive` | `day3_honor_pause` | `day3_force_explanation` | honor → `outcome_pause_honored`；force → `outcome_pause_overridden` |
| `agency_day4_route_preparation` | `event_route_preparation_requested` / `event_erii_requests_self_controlled_option(answer_state=preserve_executable_self_controlled_option)` | `day4_buy_two_tickets_real_name`、`day4_buy_single_ticket_cash` | `day4_follow_one_route_no_backup` | two tickets → `outcome_shared_option_prepared`；single ticket → `outcome_solo_option_prepared`；no backup → `outcome_self_controlled_option_not_prepared` |
| `agency_day4_independent_contact` | `event_independent_contact_option_requested` / `event_erii_keeps_alias_token_ready(answer_state=keep_independent_contact_option)` | `day4_register_independent_contact` | `day4_decline_independent_contact` | register → `outcome_independent_option_prepared`；decline → `outcome_independent_option_declined` |
| `agency_day5_response` | `event_family_response_requested` / `event_erii_selects_route_response(answer_state_id)` | `day5_honor_erii_response` | `day5_replace_erii_response` | honor → `event_route_preference_honored` + exactly one `outcome_route_preference_honored_{answer_state_id}`；replace → `event_route_preference_overridden_to_old_order` + `outcome_route_preference_overridden_to_old_order` |
| `agency_day6_cost` | `event_cost_bearer_requested` / `event_erii_rejects_shifted_cost` | `day6_burn_old_identity` | `day6_shift_cost_to_erii` | burn → `outcome_cost_borne_by_lu`；shift → `outcome_cost_shifted_to_erii` + `consequence_erii_bears_promised_cost` |
| `agency_day6_cost_reconsideration` | `event_cost_reconsideration_requested` / `event_erii_rejects_shifted_cost_again` | `day6_take_cost_back` | `day6_leave_cost_shifted` | take-back → `outcome_cost_returned_to_lu` + `outcome_shift_attempt_residual`；leave → `outcome_cost_shift_confirmed` |

每项 request 和 answer 均为零 axis。九个 transaction 的 source response universe 必须从 canonical CFG artifact 反推并与各 transaction 的唯一实际 response node exact-equal；每个 response 恰属于 accepting/overriding 一侧，并恰关联表中非空 outcomes。Raw response、partition 与 outcome tuples 均禁止重复；`resulting_outcome_ids` 必须与逐 response outcome tuple 的无重复有序并集 exact-equal。`answer_state_id` 只能来自批准闭集并通过 answer derivation；answer 含混、未登记或为 `undetermined` 时不得出现 response surface，transaction 与 scene 均不能冻结。

## Counterevidence Catalog

本版本冻结 7 个、全部 `repairable` 的 route-critical revoke tokens；不存在 irreversible token，也不需要 irreversible approval。每个 repair 只能移除表中指定的一个 token。

Token 是“仍未解决的领域违背”集合成员，不是计数器。对同一 token 的第二次及后续 revoke 不创建重复 token，但必须把 source choice 追加到该 token 的有序 `contributor_choice_ids`，不得静默丢弃。Repair 只有在 `repaired_source_choice_ids` exact-equal 当前全部 unresolved contributors、玩家可感知地逐项承认这些行为，并撤回仍生效的冲突安排时才能移除 token；少报任一 contributor、只作笼统道歉或仍保留冲突方案均使 repair 失败。这样一次 repair 可以处理一个持续领域模式，但不能“一键洗掉”未被承认的多次侵犯。

| Token | Domain / violated pillar | Revoke choices | Consequence | Repair choices / cost / payoff |
|---|---|---|---|---|
| `token_override_first_destination` | autonomy / 温柔必须被挣来 | `prologue_override_destination`、`prologue_choose_route` | `consequence_erii_waits_for_orders` | `day1_repair_first_destination` / 承认覆盖并执行她当前选择 / `payoff_repair_first_destination` |
| `token_override_daily_choice` | autonomy / 看见未说出口的话 | `day1_choose_safe_clothing`、`day1_keep_first_override`、`day2_assign_alias`、`day3_force_explanation`、`day5_replace_erii_response` | `consequence_erii_stops_offering_preferences`；保留全部 contributor choice IDs | `day5_repair_daily_choice` / 逐项承认当前全部 contributors、撤回所有仍生效替代方案并接受已表达决定 / `payoff_repair_daily_choice` |
| `token_silence_as_consent` | understanding / 看见未说出口的话 | `day1_assume_food_consent` | `consequence_ambiguous_refusal_missed` | `day2_admit_alias_unknown` / 承认没懂并重问 / `payoff_day2_admit_day5` |
| `token_hide_school_evidence` | truth / 温柔必须被挣来 | `day3_hide_school_evidence` | `consequence_archive_initially_rejected` | `day5_repair_school_evidence` / 先补交被隐藏证据再继续家族档案 / `payoff_repair_school_truth` |
| `token_withhold_family_truth` | truth / 悲剧也是完整答案 | `day5_give_safe_summary` | `consequence_terminal_fact_missing` | `day6_disclose_withheld_archive` / 安全屋后果已发生且失去提前准备时间 / `payoff_day6_late_truth_ending` |
| `token_abandon_backup_plan` | preparation / 用普通生活抵抗宏大命运 | `day4_follow_one_route_no_backup`、`day4_decline_independent_contact`、`day6_abandon_backup` | `consequence_route_resource_lost` | `day6_reopen_service_exit` / 暴露时间与位置 / `payoff_day6_exit_ending` |
| `token_shift_promised_cost` | sacrifice / 温柔必须被挣来 | `day6_shift_cost_to_erii` | `consequence_erii_bears_promised_cost` | `day6_take_cost_back` / 路明非失去旧身份；保留 `outcome_shift_attempt_residual` / `payoff_day6_take_back_ending` |

每个 repair 都发生在 token-specific consequence 首次可感知之后；若 entry condition 不满足，对应 repair choice 不得出现。没有任何普通正向 choice 可以清除非目标 token。Build validator 必须覆盖同 token 一次、两次和最大合法次数 revoke，再分别证明完整 contributor acknowledgement 可修复、遗漏任一 contributor 固定失败。

## Route Qualification Bindings

四项 records 的 `qualification_kind` 均为 `route_membership`，`owner_system` 均为 `SYS-ENDING`，operator 均固定为 `all`。

| Qualification | Source choice IDs | Source event IDs | Source resource IDs |
|---|---|---|---|
| `qualification_independent_contact_route` | `day6_commit_independent_contact` | `event_independent_route_committed`、`event_contact_risk_handover_complete`、`event_route_preference_honored` | `resource_contact_card` |
| `qualification_shared_escape_route` | `day6_commit_shared_escape` | `event_shared_route_committed`、`event_shared_cost_acknowledged`、`event_route_preference_honored` | `resource_two_tickets` |
| `qualification_solo_departure_route` | `day6_commit_solo_departure` | `event_solo_route_committed`、`event_no_continuing_contact_commitment`、`event_route_preference_honored` | `resource_single_ticket` |
| `qualification_old_order_return_route` | `day6_commit_old_order_return` | `event_old_order_route_committed` | — |

前三项的所有 qualification fields 都只使用上游冻结 schema 能表达的正向 choice/event/resource sources。Solo 的 contact-card absence 不是 `route_qualification_record` 字段：它只属于 `day6_commit_solo_departure` 的 entry guard，并由该 choice 成功后产生的正向 `event_no_continuing_contact_commitment` 固结为 qualification source。Canonical CFG 必须证明 contact card present 时该 choice 不可达，因此不需要也不得添加 `absent_resource_ids`、negated source 或其他未声明字段。Day 6 route guards 使四个 commitment choices 与 `day6_no_executable_route` 的 active count 恰为 1，因此每条 terminal path 最多命中一个 qualification；`day6_no_executable_route` 命中零项；`rain_stops` 仍完全不读取 qualification。

## Canonical Ending Witnesses

下表列出每个 ending 的首周目 canonical witness。每条 `ordered_choice_history` 都是从 New Game 到 `EndingEntry` 的完整 player-facing choice history：包含零轴 semantic choices、条件 repair/keep choices 和 route commitment，不允许省略 opener、必经 choice node 或 replacement node。非交互 scene beats 与 answer/outcome facts 单列，由 scene records 确定性产生。

| Witness | Complete `ordered_choice_history` | Required answer / route facts | Final axes `U/A/T/P/S` | Unresolved tokens | Qualification / ending |
|---|---|---|---|---|---|
| `witness_rain_stops_v1` | `prologue_read_note → prologue_ask_destination → prologue_accept_destination → prologue_notice_tracker → day1_accept_clothing → day1_read_food_gesture → day2_accept_alias → day2_save_second_token → day3_share_school_evidence → day3_honor_pause → day4_buy_two_tickets_real_name → day4_register_independent_contact → day5_share_full_archive → day5_include_self_in_truth → day5_honor_erii_response → day6_burn_old_identity → day6_commit_shared_escape` | Day 5 `answer_state=shared_escape` honored；contact risk handover complete；shared cost acknowledged | `3/3/3/3/3` | `()` | shared route present but ignored / `rain_stops` |
| `witness_her_own_name_v1` | `prologue_read_note → prologue_ask_destination → prologue_accept_destination → prologue_notice_tracker → day1_accept_clothing → day1_read_food_gesture → day2_accept_alias → day2_save_second_token → day3_share_school_evidence → day3_honor_pause → day4_follow_one_route_no_backup → day4_register_independent_contact → day5_share_full_archive → day5_blame_family_only → day5_honor_erii_response → day6_keep_backup_abandoned → day6_burn_old_identity → day6_commit_independent_contact` | Day 5 `answer_state=independent_contact` honored；contact risk handover complete | `3/3/3/1/1` | `(token_abandon_backup_plan)` | independent contact / `her_own_name` |
| `witness_see_the_sea_v1` | `prologue_hurry_to_train → prologue_ask_destination → prologue_accept_destination → prologue_promise_cost → day1_accept_clothing → day1_assume_food_consent → day2_accept_alias → day2_save_second_token → day3_share_school_evidence → day3_honor_pause → day4_buy_two_tickets_real_name → day4_register_independent_contact → day5_share_full_archive → day5_include_self_in_truth → day5_honor_erii_response → day6_burn_old_identity → day6_commit_shared_escape` | Day 5 `answer_state=shared_escape` honored；shared cost acknowledged | `2/3/3/3/3` | `(token_silence_as_consent)` | shared escape / `see_the_sea` |
| `witness_one_person_train_v1` | `prologue_read_note → prologue_ask_destination → prologue_accept_destination → prologue_promise_cost → day1_accept_clothing → day1_assume_food_consent → day2_accept_alias → day2_spend_both_tokens → day3_share_school_evidence → day3_honor_pause → day4_buy_single_ticket_cash → day5_give_safe_summary → day5_blame_family_only → day5_honor_erii_response → day6_keep_archive_withheld → day6_burn_old_identity → day6_commit_solo_departure` | Day 5 `answer_state=solo_departure` honored；contact card absent；no continuing-contact commitment | `3/3/1/1/2` | `(token_silence_as_consent, token_withhold_family_truth)` | solo departure / `one_person_train` |
| `witness_golden_cage_v1` | `prologue_hurry_to_train → prologue_choose_route → prologue_promise_cost → day1_keep_first_override → day1_read_food_gesture → day2_accept_alias → day2_save_second_token → day3_share_school_evidence → day3_honor_pause → day4_buy_single_ticket_cash → day4_register_independent_contact → day5_share_full_archive → day5_blame_family_only → day5_replace_erii_response → day5_keep_daily_override → day6_burn_old_identity → day6_commit_old_order_return` | Day 5 non-old-order answer explicitly overridden to old order | `3/2/3/2/1` | `(token_override_first_destination, token_override_daily_choice)` | old order / `golden_cage` |
| `witness_unsent_postcard_v1` | `prologue_hurry_to_train → prologue_choose_route → prologue_promise_cost → day1_keep_first_override → day1_assume_food_consent → day2_assign_alias → day2_spend_both_tokens → day3_hide_school_evidence → day3_force_explanation → day4_follow_one_route_no_backup → day5_give_safe_summary → day5_blame_family_only → day5_honor_erii_response → day5_keep_school_evidence_hidden → day5_keep_daily_override → day6_keep_backup_abandoned → day6_keep_archive_withheld → day6_shift_cost_to_erii → day6_leave_cost_shifted → day6_no_executable_route` | Day 5 `answer_state=continue_without_executable_route` honored；no ticket/contact route survives | `0/1/0/0/1` | `(token_override_first_destination, token_override_daily_choice, token_silence_as_consent, token_hide_school_evidence, token_withhold_family_truth, token_abandon_backup_plan, token_shift_promised_cost)` | none / `unsent_postcard` |

每条 witness 必须由拓扑 replay validator 从入口逐 choice 验证 enabled guard、必经 beat、response join、chapter boundary、axis/token/resource/event fold 与 ending entry。只把表中 history 直接交给 resolver、但不证明图上可重放，不构成 witness PASS。

### Terminal Cause-Family Forecast

下列 11 项是内容制作与摘要覆盖的 **cause-family forecast**，不是 SYS-ENDING `terminal_cause_equivalence_class` 的 exact identity，也不授权合并不同 causes、exclusions、unresolved-token tuples、人物归宿、代价承担者或悲剧闭环。每个 family 冻结最低叙事差异、payoff semantic ID 与 summary semantic ID：

| Cause-family ID | Ending | Required terminal difference | Payoff semantic ID | Summary semantic ID |
|---|---|---|---|---|
| `family_rain_stops_ordinary_future` | `rain_stops` | 绘梨衣保留名字与决定；路明非放弃力量及旧身份；普通未来成立 | `payoff_family_rain_stops_ordinary_future` | `summary_family_rain_stops_ordinary_future` |
| `family_her_own_name_independent_contact` | `her_own_name` | 绘梨衣使用独立联系人离开，分隔但保留持续联系 | `payoff_family_her_own_name_contact` | `summary_family_her_own_name_contact` |
| `family_see_the_sea_identity_cost` | `see_the_sea` | 共同逃离且主要代价为路明非旧身份/力量 | `payoff_family_see_the_sea_identity` | `summary_family_see_the_sea_identity` |
| `family_see_the_sea_route_cost` | `see_the_sea` | 共同逃离且主要可感知代价为路线、位置或资源暴露，同时已满足共同承担合同 | `payoff_family_see_the_sea_route` | `summary_family_see_the_sea_route` |
| `family_one_person_train_understanding_loss` | `one_person_train` | 绘梨衣能离开，但理解或持续联系承诺不足导致失散 | `payoff_family_one_person_train_understanding` | `summary_family_one_person_train_understanding` |
| `family_one_person_train_preparation_truth_loss` | `one_person_train` | 单人路线存在，但准备或真相反证使同行承诺失效 | `payoff_family_one_person_train_preparation_truth` | `summary_family_one_person_train_preparation_truth` |
| `family_golden_cage_first_route_override` | `golden_cage` | 最初路线决定被覆盖并一直未被完整承认 | `payoff_family_golden_cage_first_route` | `summary_family_golden_cage_first_route` |
| `family_golden_cage_daily_override` | `golden_cage` | 多次日常决定的 contributor pattern 未解决，旧秩序重新成立 | `payoff_family_golden_cage_daily` | `summary_family_golden_cage_daily` |
| `family_unsent_postcard_no_route` | `unsent_postcard` | 没有可执行路线 | `payoff_family_unsent_postcard_no_route` | `summary_family_unsent_postcard_no_route` |
| `family_unsent_postcard_truth_loss` | `unsent_postcard` | 关键真相缺失或交付过晚成为决定性损失 | `payoff_family_unsent_postcard_truth` | `summary_family_unsent_postcard_truth` |
| `family_unsent_postcard_shifted_cost` | `unsent_postcard` | 必要代价仍由绘梨衣承担 | `payoff_family_unsent_postcard_shifted_cost` | `summary_family_unsent_postcard_shifted_cost` |

Offline compiler 必须枚举全部合法 terminal paths，并按 SYS-ENDING 的 exact class-key 生成实际 `terminal_cause_equivalence_class` records。每个实际 class 必须：

- 引用上述恰一个最接近的内容 family 作为制作责任，但 class identity 不包含或依赖 family ID；
- 拥有独立 `terminal_class_witness_id`、完整 ordered history、exact matched/exclusion causes、unresolved-token tuple、terminal outcome signature、适用 payoff 与玩家摘要；
- 接受每 ending `1–6`、`7–12` 触发范围复核、`>12` 构建失败的上游预算；
- 在任何 identity 字段不同的情况下保持分离，即使它们共享 family、ending scene 或基础文案。

因此 `11` 只表示最低内容变体覆盖，不再宣称完整图恰有 11 个 equivalence classes。实际 class count 与逐 class witnesses 由 `NARR-Q13` 在 production content lock 前关闭。

## Core Player-Safe Ending Summaries

这些 summary IDs 冻结语义，不冻结最终润色：

| Ending | Summary ID | Required meaning |
|---|---|---|
| `rain_stops` | `summary_ending_rain_stops_core` | 她的决定、完整真相、准备与由路明非承担的代价共同保住普通未来 |
| `her_own_name` | `summary_ending_her_own_name_core` | 她以自己的名字和联系人离开，分隔不是失去决定权 |
| `see_the_sea` | `summary_ending_see_the_sea_core` | 两人选择同一条危险路线，并已支付身份或资源代价 |
| `one_person_train` | `summary_ending_one_person_train_core` | 她有能力独自离开，但关系或准备不足使同行承诺失效 |
| `golden_cage` | `summary_ending_golden_cage_core` | 安全方案覆盖了她已表达的决定，旧秩序因此重新成立 |
| `unsent_postcard` | `summary_ending_unsent_postcard_core` | 行动太晚或没有可执行方案，未交付的真相与未承担的代价留下完整后果 |

最终简体中文文案、字幕长度和 cause-card 分页继续由 `NARR-Q8`、SYS-ACCESS 与 UX Designer 关闭，但不得改变以上 meaning。

## Achievement Witness Bindings

成就只消费 `achievement_event_catalog:v2` 中已完成的叙事事件，不读取 axes、tokens、qualification、resources、ending predicate 或 resolver record。六个 ending 与七个 chapter memory 使用各自收藏 namespace，不再镜像为成就。

### Achievement Completion Event Catalog v2

| Event | Exact production source | Completion checkpoint |
|---|---|---|
| `event_achievement_read_note_recovered` | `prologue_hurry_to_train` 零轴路径中绘梨衣保住愿望纸，Day 6 `payoff_prologue_hurry_day6` 完整结束 | `cp_day6_note_recovery_complete` |
| `event_achievement_ask_first_answer_honored` | `prologue_ask_destination → event_erii_points_small_station → prologue_accept_destination`，且一小时绕行后果已完整呈现 | `cp_prologue_small_station_detour_complete` |
| `event_achievement_refusal_honored` | `event_erii_rejects_shifted_cost_again → day6_take_cost_back → outcome_cost_returned_to_lu`；override 或无安全替代路径不得产生 | `cp_day6_cost_reconsideration_complete` |
| `event_erii_selects_route_response` | `character_answer_derivation_record` 已确定 registered answer，动作/物件表达完整结束；不声明玩家随后 honor | `cp_day5_route_answer_expressed` |
| `event_prior_cost_promise_honored_without_shift` | 存在 `event_shared_cost_promised`，并直接执行 `day6_burn_old_identity`；本 path 未发生 `day6_shift_cost_to_erii` | `cp_day6_direct_cost_complete` |
| `event_erii_enters_alias` | 绘梨衣完成输入自己的 alias，屏幕结果与动作均已呈现 | `cp_day2_alias_answer_expressed` |
| `event_empty_school_trace_confirmed` | `scene_day3_classroom_trace` 的交叉验证结果完成可感知呈现 | `cp_day3_empty_school_trace_complete` |
| `event_two_window_tickets_acquired` | `day4_buy_two_tickets_real_name` 后，两张靠窗票交到绘梨衣手中且身份暴露代价已呈现 | `cp_day4_two_tickets_complete` |
| `event_service_exit_used` | `day6_use_service_exit` 实际启用维修通道并离开封锁区 | `cp_day6_service_exit_complete` |
| `event_epilogue_first_guest_completed` | `scene_epilogue_first_guest` 的可玩事件完整结束 | `cp_epilogue_first_guest_complete` |
| `event_epilogue_lights_out_completed` | `scene_epilogue_lights_out` 的可玩事件完整结束 | `cp_epilogue_lights_out_complete` |

上表恰含11个 canonical completion events，每项成就各占一个且checkpoint mapping唯一。`event_full_archive_shared`与`event_shared_cost_promised`是复合条件的前置事实，不计入completion-event数量；前者在`cp_day5_full_archive_shared`产生，后者在`prologue_promise_cost`完整结束后产生。

### Achievement Witness Catalog v2

| Witness | Required ordered facts | Achievement |
|---|---|---|
| `witness_achievement_read_note_zero_delta` | `prologue_hurry_to_train → event_note_preserved_by_erii → payoff_prologue_hurry_day6 → event_achievement_read_note_recovered` | `CHOICE_READ_THE_NOTE` |
| `witness_achievement_ask_first_accept_cost` | `prologue_ask_destination → event_erii_points_small_station → prologue_accept_destination →` 一小时绕行完整后果 | `CHOICE_ASK_FIRST` |
| `witness_achievement_accept_no_nonbest` | `day6_shift_cost_to_erii → event_erii_rejects_shifted_cost_again → day6_take_cost_back → outcome_cost_returned_to_lu`，随后进入任一批准的 non-`rain_stops` witness | `CHOICE_ACCEPT_NO` |
| `witness_achievement_share_truth_answer_expressed` | `day5_share_full_archive → event_full_archive_shared → event_erii_selects_route_response`；honor/replace 后续 response 均可达 | `CHOICE_SHARE_TRUTH` |
| `witness_achievement_direct_cost_honored` | `event_shared_cost_promised → day6_burn_old_identity → event_prior_cost_promise_honored_without_shift`，path 中无 shift choice | `CHOICE_KEEP_PROMISE` |
| `witness_route_arcade_alias_expressed` | `event_alias_requested → event_erii_enters_alias` | `ROUTE_ARCADE_ALIAS` |
| `witness_route_empty_school_trace` | 空教室 trace 的输入 facts → 交叉验证 → `event_empty_school_trace_confirmed` | `ROUTE_EMPTY_SCHOOL` |
| `witness_route_two_window_tickets` | `day4_buy_two_tickets_real_name → event_two_window_tickets_acquired` | `ROUTE_SEASIDE_TICKET` |
| `witness_route_service_exit_used` | `resource_service_exit → day6_use_service_exit → event_service_exit_used` | `ROUTE_BACKUP_EXIT` |
| `witness_epilogue_first_guest` | `rain_stops → scene_epilogue_first_guest → event_epilogue_first_guest_completed` | `EPILOGUE_FIRST_GUEST` |
| `witness_epilogue_lights_out` | `rain_stops → scene_epilogue_first_guest → scene_epilogue_lights_out → event_epilogue_lights_out_completed` | `EPILOGUE_LIGHTS_OUT` |

每个 event/checkpoint 必须由 production CFG 证明唯一 source callsite、责任 scene 支配、发生在可感知结果结束之后，并提供 missing-event、wrong-order 与 wrong-checkpoint negative fixtures。

## Closure Evidence for Prior Design Questions

| Prior question | Resolution in this baseline |
|---|---|
| `NARR-Q1` | 15 个 canonical units 与 required scene IDs 已冻结；source hash、scanner output 属于 production implementation evidence |
| `NARR-Q2` | 当前 active character 闭集与两项 constraint records 已冻结；新增人物触发重新审核 |
| `NARR-Q3` | 54 项 production choice universe、唯一 reaction identity、修订后的 U/T/P/S recovery projections 与最低 payoff semantic evidence 已冻结 |
| `NARR-Q4` | 9 项 agency transactions、answer derivation records、CFG-derived response universes、per-response outcomes 与 Day 6 reconsideration transaction 已冻结 |
| `NARR-Q5` | 四项 exact qualification source bindings 与 operator 已冻结 |
| `NARR-Q6` | 7 项 repairable token definitions、repair targets 和 consequences 已冻结；irreversible count 为 0 |
| `NARR-Q7` | 六条 canonical ending witnesses、11 个 cause-family production variants、人物归宿、代价与 payoff direction 已冻结；不再把 family 数量误称为 exact equivalence-class count |
| `NARR-Q13` | 尚待 offline compiler 对全部合法 terminal paths 生成 exact class-key、逐 class witness、payoff/summary binding 与 per-ending budget verdict；这是 production content-lock gate，不是可由本基线伪造的静态数量 |

本文件关闭的是设计决定，不伪造实现证据。Production freeze 仍必须生成 source hash、完整 records、negative fixtures、全图 enumeration、join report 与 engine traces；任一结果与本基线不一致都必须回到设计修订，而不是静默改 catalog。
