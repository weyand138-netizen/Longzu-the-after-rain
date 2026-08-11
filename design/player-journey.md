# 玩家旅程图：从观察到回收

> **Status**：Approved for UX review
> **Owner**：UX / SYS-NARRATIVE
> **Platform**：Windows 10/11 x86-64；鼠标 + 完整键盘；无 hover 依赖
> **Accessibility tier**：`P0-ACCESS-KEYBOARD-MOUSE-SAPI-EQUIVALENCE`
> **Last Updated**：2026-08-09

## Journey overview

```text
启动/重返
  → 主菜单：开始、读取、愿望手册、设置、退出
  → 稳定叙事帧：标题/场景/对话
  → 观察：读懂人物、物件与环境
  → 询问/决定：Choice Surface，首焦点为第一项
  → canonical choice commit：只提交一次
  → reaction / payoff：静态文字与可访问因果摘要
  → after-reaction checkpoint：恢复安全控制
  → 结局与 1–3 张因果卡：理解已发生事实
  → 愿望手册：回顾已验证内容并返回 caller
```

## Context and player need by phase

| Phase | Player arrives with | Player wants | Required accessible result | Safe exit |
|---|---|---|---|---|
| Main menu | 首次好奇或带着上一轮记忆重返 | 开始、读取、回顾或调整环境 | 标题→说明→稳定初始焦点；完整键盘可到达所有入口 | 退出确认→取消/退出 |
| Stable narrative | 刚读完一段对白或旁白 | 继续阅读或打开安全菜单 | 文字可见且可 self-voicing；菜单不旁路 critical interaction | 继续、Esc/右键返回 |
| Observe | 看到场景、人物动作、物件 | 理解上下文而非猜隐藏数值 | 阅读顺序固定；声音、颜色、动画都不是唯一信息 | 进入下一段/稳定菜单 |
| Ask/decide | 已读懂 prompt 与候选行动 | 选择自己的行动 | 第一项初始焦点；Tab/方向键/鼠标同一 canonical action；不显示轴/成本/预测 | 仅在 choice 可用时离开 |
| Reaction/payoff | choice 已提交 | 看懂即时反应和延迟后果 | action latch 一次；静态文本与 `accessible_causal_summary_id` 等价；禁止 save/load/rollback/skip | after-reaction checkpoint |
| Journal | 想回顾已发生内容 | 找到章节、回忆、旅途记录或结局摘要 | validating/loading、合法空页、不可用与 recovery 均有可朗读状态；关闭恢复 caller semantic ID | 关闭/返回目录 |
| Settings | 想提高可读性或关闭效果 | 调整字体、对比度、动效、闪烁、震动与 self-voicing | 预览与应用边界清楚；失败不丢意图；设置值有文字状态 | 取消/应用/恢复 |
| Save/load/recovery | 想保存、读取或处理失败 | 安全恢复，不进入半加载场景 | loading/empty/error/disabled/recovery fail closed；只保留批准动作 | 返回主菜单或开始新游戏 |
| Ending | 已完成 terminal narration 与 closure | 理解发生了什么 | 标题→具体事实→1–3 因果卡→尾声；无评分、路线条件或隐藏数值 | 继续尾声/打开手册 |

## Cross-channel invariants

- 鼠标、键盘和 self-voicing 输出共享同一个 canonical action；self-voicing 只输出，不自动确认、推进、滚动或抢焦点。
- 所有状态使用文字并配合轮廓、填充、位置或形状；颜色、声音、闪烁和震动不承载唯一语义。
- 字体 `1.0 / 1.25 / 1.5` 和 `1280×720 / 1920×1080` 不改变阅读顺序、focus graph 或安全出口。
- viewport 外目标在聚焦前完整滚入视野；滚动不提交叙事 action，也不改变 history、rollback 或 persistent。
- loading、empty、error、disabled、recovery 均可键盘到达、可重访，并声明 transcript 内容范围。

## Recovery boundary

任何内容、存档、持久化或设置验证失败都会销毁不可信的草稿/旧 caller，进入 owning system 的 blocking safe flow。默认只保留批准的安全出口；不得通过快捷菜单、回退、跳过或隐藏坐标返回旧叙事帧。
