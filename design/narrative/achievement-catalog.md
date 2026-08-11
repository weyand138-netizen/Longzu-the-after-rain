# 成就目录（11 项）

> **Version**: `achievement_catalog:v2`
> **Status**: Approved normative catalog
> **Date**: 2026-07-30
> **Amended**: 2026-08-03 — player-visible group/copy only；IDs、conditions与internal group identity unchanged
> **Producer Decision**: 6 个结局与 7 个章节继续由 `ending_ids` / `memory_ids` 收藏记录，不再镜像为成就

## 场景回声（5）

| ID | 名称 | 触发意图 |
|---|---|---|
| `CHOICE_READ_THE_NOTE` | 被雨打湿的愿望 | 零轴路径中由绘梨衣保住愿望纸，并在 Day 6 完成正式回收 |
| `CHOICE_ASK_FIRST` | 多绕一小时 | 询问目的地、接受她的回答，并完整承担一小时绕行的可感知不便 |
| `CHOICE_ACCEPT_NO` | 换一条安全的路 | 在 Day 6 明确拒绝后接受回答、收回转嫁的代价并采用不剥夺自主的安全替代 |
| `CHOICE_SHARE_TRUTH` | 摊开的家族档案 | 交付完整原始档案，并让绘梨衣形成和表达 registered answer；不声明玩家随后尊重了该回答 |
| `CHOICE_KEEP_PROMISE` | 烧掉的旧身份 | 早期承诺共同承担成本，Day 6 未先转嫁代价而直接由路明非承担 |

## 路线发现（4）

| ID | 名称 | 触发意图 |
|---|---|---|
| `ROUTE_ARCADE_ALIAS` | 屏幕上的另一个名字 | 绘梨衣完成输入自己选择的 alias |
| `ROUTE_EMPTY_SCHOOL` | 没有学生的教室 | 空教室 trace 经交叉验证并完成可感知确认 |
| `ROUTE_SEASIDE_TICKET` | 两张靠窗的票 | 两张实名靠窗票交到绘梨衣手中，身份代价已呈现 |
| `ROUTE_BACKUP_EXIT` | 封条后的出口 | 已准备的维修通道被实际启用 |

## 后来留下的回声（2）

| ID | 名称 | 触发意图 |
|---|---|---|
| `EPILOGUE_FIRST_GUEST` | 今天的第一位客人 | 真结局尾声“第一位客人”的可玩事件完整结束 |
| `EPILOGUE_LIGHTS_OUT` | 关灯，回家 | 真结局尾声“关灯回家”的可玩事件完整结束 |

## Display Contract

- 11 项均使用 `reveal_policy=ON_UNLOCK`。
- 未解锁项目不渲染、不占槽、不计数、不生成组标题、不聚焦、不朗读，也不显示“？？？”。
- 页面不显示 `/11`、百分比、剩余数、条件进度、“完整”或全收集终态；11 项全部获得时也只显示现有记录。
- 解锁后使用物件、场景或代价式名称，不使用五轴/domain、正确行为、好坏结局、稀有度或等级语言。
- 玩家可见目录顺序固定为场景回声 → 路线发现 → 后来留下的回声；内部稳定 group identity 可保持兼容，但不得向玩家显示“真结局”“终极”或完成组语言，也不得按五轴、结局优劣或最近解锁重排。
- “新记录”只来自 canonical `achievement_ids - seen_achievement_ids`，不是持久化 pending popup。

## Condition Ownership

`SYS-ACHIEVE` 是 `achievement_condition_record` 的唯一 owner。可执行条件、completion event、checkpoint、witness 与 display rank 以 [本地成就 GDD](../gdd/local-achievements.md) 和 `achievement_event_catalog:v2` 为准。

条件不得读取 axis、token、qualification、resource、ending predicate、resolver record 或 live store。技术引用为零之外，还必须通过 semantic anti-checklist review，证明名称、分组与条件不能一对一恢复五轴或结局等级。

## Required Witnesses

- `witness_achievement_read_note_zero_delta`
- `witness_achievement_ask_first_accept_cost`
- `witness_achievement_accept_no_nonbest`
- `witness_achievement_share_truth_answer_expressed`
- `witness_achievement_direct_cost_honored`
- `witness_route_arcade_alias_expressed`
- `witness_route_empty_school_trace`
- `witness_route_two_window_tickets`
- `witness_route_service_exit_used`
- `witness_epilogue_first_guest`
- `witness_epilogue_lights_out`

每项必须拥有至少一个 positive golden vector、逐 required-event missing negatives 与 wrong-checkpoint negative。复合条件另需顺序负例；`CHOICE_ACCEPT_NO` 另需 override、无安全替代与错误 checkpoint 负例。
