# 无障碍设置

> **Status**: Approved with provisional downstream gates
> **Author**: Andwey + Codex
> **Last Updated**: 2026-08-04
> **Implements Pillar**: 看见未说出口的话；悲剧也是完整答案

## Overview

SYS-ACCESS 是贯穿所有玩家界面的输入与表现基础层，使玩家能够在设置界面调整字体缩放、高对比度、自发声、动态、闪烁、震动和限时效果，并使用键盘或鼠标完成所有核心交互。它直接保障玩家在本项目明确支持的视觉、听觉与输入配置内，都能独立看见未说出口的信息、按自己的节奏作出决定，并获得与默认呈现语义等价的选择、即时反应和延迟回收反馈。依据 [ADR-0003](../../docs/architecture/adr-0003-content-and-presentation-boundary.md)，无障碍表现只能呈现已批准内容，不得改变叙事结果或建立第二条因果路径；没有本系统，游戏将失去绘梨衣非语言表达与选择因果的等价可理解性，并违反项目不可削减的无障碍基线。

## Player Fantasy

玩家不应觉得自己开启的是内容缩水、节奏受限或需要他人代操作的“辅助版本”，而应感到自己始终是完整体验的主体：可以独立理解场景、控制阅读节奏、作出决定，并获得与默认呈现语义等价的反馈。核心幻想是：“在本项目明确支持的 Windows 10/11 输入与非视觉配置内，玩家都能独立看见未说出口的信息、按自己的节奏作出决定，并获得语义等价的反馈。”首发支持配置为键盘或鼠标输入，并具备可用简体中文 Windows SAPI 语音的 self-voicing；clipboard voicing 可与外部屏幕阅读器互操作，但不是项目单独保证的语音合成后备。触控、完整手柄以及缺少可用 SAPI 语音且没有外部屏幕阅读器的配置，不得被发行说明宣称为已通过独立非视觉验收。

这一感受锚定在具体时刻：玩家只使用键盘与自发声进入选择场景，仍能理解绘梨衣的视线、动作与物件变化，按自己的节奏确认选择，并在之后辨认该选择的即时反应与延迟回收。系统直接服务“看见未说出口的话”，同时确保成功与悲剧路线都能作为完整答案被理解，而不因颜色、声音、动画、精确指针或限时操作成为唯一信息通道。

该幻想不允许用“所有模式复用同一 ID”替代玩家理解证据。可访问描述必须忠实于玩家在该时点已经能够观察或确认的事实，保留绘梨衣表达中的不确定性，并由目标玩家测试验证早期选择、人物决定和悲剧代价仍可被理解。

## Detailed Design

### Core Rules

1. **语义等价优先**：无障碍设置只能改变输入方式、布局和反馈通道，不得改变 canonical choice ID、选择顺序、reaction/payoff、剧情控制流、隐藏状态或结局。
2. **核心交互全键盘可达**：主菜单、设置、叙事推进、选择、存读档、愿望手册、成就通知、结局与安全恢复流程都必须可通过键盘完成；鼠标调用相同 canonical action。首发不要求完整手柄支持，也不支持触控。
3. **输出不得激活操作**：Self-voicing、字幕、替代文本和因果摘要只能输出信息，不得自动确认、推进、滚动至新内容或改变焦点。
4. **设置入口受安全状态约束**：完整设置界面只可从主菜单或 `PlayableStable` 游戏菜单打开。`CriticalInteraction`、`LoadedUnvalidated` 和 `BlockingSafeFlow` 不得借设置界面绕过 action gate；不转移控制的 self-voicing 开关仍可使用。
5. **项目设置采用草稿事务**：打开设置时从合法 detached snapshot 建立草稿；修改即时预览，但只有 Apply 才经 SYS-PERSIST 持久化。Cancel 恢复最新合法值，assignment 与 flush 次数均为零。
6. **引擎偏好即时生效**：Self-voicing、文字速度、自动播放、跳过速度和音量继续由 Ren’Py preferences 拥有并即时生效，不进入 SYS-ACCESS 草稿或 SYS-PERSIST root。
7. **项目设置及默认值**：

| Setting | Default | Allowed values | Required effect |
|---|---:|---|---|
| `font_scale` | `1.0` | `1.0, 1.25, 1.5` | 全界面使用同一语义结构重新排版；不得裁切关键内容或操作 |
| `high_contrast` | `false` | exact bool | 提升文字、焦点和状态边界；降低或移除干扰纹理 |
| `reduced_motion` | `false` | exact bool | 非必要转场立即完成，停止循环及装饰性运动；保留最终语义状态 |
| `flash_effects_enabled` | `false` | exact bool | 关闭时以静态、非闪烁反馈替代全部闪光 |
| `screen_shake_enabled` | `false` | exact bool | 关闭时不产生视口或画面位移，并保留等价反馈 |

8. **独立控制**：减弱动效、闪烁与屏幕震动分别控制对应效果；关闭任一通道不得自动改写其他设置，也不得损失信息。
9. **限时选择边界**：限时规则与开关由 SYS-TENSION 拥有，默认关闭。SYS-ACCESS 只保证设置入口、剩余时间的多通道表达和非限时正式路径；不得自行生成 timeout choice。
10. **可访问因果摘要**：只靠视线、动作、人物距离、物件、声音或动画才能感知的 production reaction/payoff，必须绑定一个玩家安全的 `accessible_causal_summary_id`。视觉、字幕、self-voicing 与 reduced-motion 变体消费同一 identity，不得暴露轴、token、qualification 或结局规则。
11. **最大字体布局**：1280×720、字体 `1.5` 是硬基线。溢出内容必须进入键盘可操作 viewport；主操作不得被滚出唯一可达区域，焦点移动到视口外项目时必须自动滚入视野。
12. **焦点稳定**：动态设置预览和模式切换后，以 stable semantic focus ID 恢复当前控件；不得使用坐标或旧 displayable identity，不得因重排触发 action。
13. **安全恢复默认值**：persistent root 无效或处于 commit-unknown/reset recovery 时，恢复界面临时使用高对比度、字体 `1.5`、reduced-motion 开、闪烁关、屏幕震动关；这些值不写回 persistent。Engine-owned self-voicing 仍可使用。
14. **无隐藏旁路**：快捷键、替代 activation、自动播放、跳过、右键和手柄默认映射都必须服从当前 surface 的 action gate，不能访问隐藏、disabled 或 unfocusable 操作。
15. **持久化修订门槛**：`settings.reduced_motion`、`settings.flash_effects_enabled` 和 `settings.screen_shake_enabled` 属于 SYS-PERSIST canonical root 的三项新增规范叶字段。2026-08-04 已同步设计权威；正式代码、generated manifest、SYS-SAVE fixtures 与 evidence 全部达到同一合同时，settings 才进入 implementation-ready。
16. **现有实现不具权威性**：旧的平铺 `persistent.high_contrast/font_scale`、高对比占位按钮及原型布局必须由正式接口替换，不构成验收证据。
17. **支持配置与非视觉 preflight**：发行支持矩阵必须至少冻结一个 Windows 10/11 + 简体中文 SAPI 可用配置。首次启用 self-voicing 或执行无障碍验收时，preflight 必须区分 voice 缺失、初始化失败、运行中失败和 clipboard 不可用；失败时不得宣称该机器通过非视觉支持。界面保留视觉安全提示，并在 clipboard 可用时复制同一已本地化提示；不得联网下载语音或静默改用未知服务。
18. **Ren’Py 无障碍入口单一权威**：项目 `font_scale` 与 `high_contrast` 是唯一玩家可调字体倍率和高对比权威。发行构建固定 Ren’Py engine font-size multiplier 为 `1.0`、engine high-contrast text 为关闭，禁用 `Preference("accessibility menu")` 与默认 `Shift+A` 控制转移。`V` 与 `Shift+C` 仅作为受 action gate 约束的 output-only self-voicing/clipboard-voicing 快捷键保留；`Shift+Alt+V` 只允许开发构建。任何引擎入口不得形成第二套字体、对比度或设置持久化路径。
19. **可访问描述只陈述已知事实**：summary/caption 只能表达来源内容已建立的可观察动作、视线、停顿、位置、物件、声音、已确认回答或当前后果；不得推断未确认内心、把沉默写成同意、提前揭示 payoff/ending，或把模糊表达改写成确定结论。默认呈现要求玩家从动作与上下文推理时，可访问描述也必须保留同等级的不确定性。
20. **完整感知主体覆盖**：production coverage 不限于 reaction/payoff。所有会影响玩家下一步理解或决定的非语言 request、answer、confirmation/refusal、reaction、payoff、chapter summary、ending cause、重要环境/声音事实均属于 `U_ACCESS_SUBJECT`，并须由独立 source discovery 与批准 catalog exact 对齐。
21. **自定节奏与可重访**：decision-critical 可访问描述必须在下一选择可执行前进入批准的可访问 transcript/backlog，或保持在当前 surface 上直至玩家确认；skip/auto gate 只有在 canonical 语义事实及当前 active mode 的可访问交付义务完成后才可解除。视觉 pose、物件状态或 summary ID 的存在本身不能证明 self-voicing 已交付。

#### 12-Leaf Authority Amendment

SYS-ACCESS 明确选择 12-leaf / 5-setting 合同作为 schema-v2 唯一权威。2026-08-04 已原子修订 SYS-PERSIST GDD、ADR-0002、Architecture、Control Manifest、SYS-SAVE、SYS-ENDING 与 Entity Registry；旧设计值及平铺 prototype fields 不再是权威。Production code、generated manifests 与 fixtures 在同步完成前必须 fail build，不能从旧值继续运行。

冻结的目标设置为：

| Project setting | Default |
|---|---:|
| `settings.font_scale` | `1.0` |
| `settings.high_contrast` | `false` |
| `settings.reduced_motion` | `false` |
| `settings.flash_effects_enabled` | `false` |
| `settings.screen_shake_enabled` | `false` |

同步修订必须原子覆盖以下合同：

- `leaf_field_count: 9 → 12`；
- `setting_updates` 最大项数 `2 → 5`；
- `settings_base` 从二值快照扩展为按冻结顺序排列的五值快照；
- Reset 保留全部五项项目设置；Merge 对完整五值设置执行统一来源选择与冲突判定；
- Recovery 临时默认固定为高对比、字体 `1.5`、reduced-motion 开、闪烁关、屏幕震动关，且不写入 persistent；
- SYS-SAVE 的 persistent-invariance evidence 比较全部 12 个规范叶字段；
- 同步修订 SYS-PERSIST GDD、ADR-0002、root validator、ownership manifest、batch validator、merge/reset、recovery、SYS-SAVE fixtures、Entity Registry 与相关架构控制文档。

兼容性盘点已确认仓库仅有 `0.1.0-dev` 原型、旧平铺字段与本地测试/切片存档，没有 Git release tag、正式分发记录或公开存档兼容义务。制作人决定这些开发 fixtures/save 不兼容；schema v2 可原位修订为 12-leaf 合同。公开发行后若再次改变 schema、字段 ownership 或 exact type，必须提升 schema 版本并新增 migration ADR，不得重复使用本次开发期豁免。

### States and Transitions

| State | Meaning | Allowed transitions |
|---|---|---|
| `Closed` | 设置界面未挂载 | 安全入口且 snapshot 合法 → `OpenClean`；root 不可用 → `RecoveryHandoff` |
| `OpenClean` | 草稿与最新合法项目设置一致 | 项目设置变化 → `PreviewDirty`；引擎 preference 操作 → 保持本状态；关闭 → `Closed` |
| `PreviewDirty` | 存在未持久化的项目设置预览 | Apply → `Applying`；Cancel → `OpenClean`；请求关闭 → `ExitConfirm`；外部设置冲突 → `StaleConflict` |
| `ExitConfirm` | 防止静默丢弃或提交草稿 | 返回编辑 → `PreviewDirty`；放弃更改 → `Closed`；Apply → `Applying` |
| `Applying` | 输入已 gate，等待唯一 SYS-PERSIST batch 结果；保留 `exit_intent` 与 retry draft | durable success/no-op 且 `exit_intent=false` → `OpenClean`；durable success/no-op 且 `exit_intent=true` → `Closed`；safe failure → `SaveFailed`；stale → `StaleConflict`；reentrant → `PreviewDirty`；invalid → `SettingsUnavailable`；unknown/unavailable → `RecoveryHandoff` |
| `SaveFailed` | 已证明未发生磁盘变更 | Retry → `Applying`；Cancel → 恢复最新合法值并进入 `OpenClean` |
| `StaleConflict` | 外部提交已改变项目设置 | Reload latest → `OpenClean`；Cancel → 恢复最新合法值并关闭；Apply 保持禁用且不可聚焦 |
| `SettingsUnavailable` | UI 生成了违反合同的 batch；草稿已清除，内部诊断已记录 | Close → `Closed`；不得 retry 同一无效 payload |
| `RecoveryHandoff` | 持久化结果未知或 root 不可用 | 清除草稿与普通设置 UI；只进入 SYS-PERSIST 批准的安全恢复流程 |

补充转换规则：

- 外部更新只改变 memberships、seen 或 epoch 且项目设置仍等于草稿 base 时，`PreviewDirty` 原地 rebase，不进入冲突。
- Apply 期间重复 activation、关闭、快捷键和第二个 batch dispatch 次数必须为零。
- `REJECTED_INVALID` 属合同/构建错误，清除 preview 与 draft，进入 `SettingsUnavailable` 并记录开发诊断；不得把内部字段或 ID 显示给玩家。
- `REJECTED_REENTRANT` 不排队；保留 retry draft 与 `exit_intent`，恢复 canonical presentation 后返回 `PreviewDirty` 并显示可重试状态。
- Recovery 抢占时清除预览、焦点恢复意图和 pending action，不返回旧调用界面。

### Interactions with Other Systems

| System | Data or behavior supplied to SYS-ACCESS | SYS-ACCESS output / boundary |
|---|---|---|
| Ren’Py 8.5.3 | Screen focus、viewport、self-voicing、`alt/group_alt`、即时 engine preferences | 只封装玩家可见行为；不得创建第二套 engine preference 存储 |
| SYS-PERSIST | Detached snapshot、project-setting batch、完整 result enum、recovery | SYS-ACCESS 拥有五项项目设置语义；SYS-PERSIST 仍是唯一 writer |
| SYS-CHOICE | Canonical choices、presentation states、commit/reaction 顺序 | 等价输入必须 exact-match choice ID；无障碍输出不得确认选择 |
| SYS-NARRATIVE | 玩家可见文本、动作、声音与因果内容 identity | 为需要冗余表达的内容绑定 `accessible_causal_summary_id`，不改写叙事 |
| SYS-SAVE | Action gates、slot/failure surfaces、blocking recovery | 提供键盘、最大字体、高对比和朗读合同，不新增加载旁路 |
| SYS-ENDING | 已批准 ending 与 cause-card 内容 | 六结局使用相同可达性和信息层级，不重排或推导原因 |
| SYS-ACHIEVE | 成就 modal、状态文案和通知 timing | Self-voicing 时 suppress 通知音；reduced-motion 只改变演出 |
| SYS-JOURNAL | Stable semantic IDs、focus fallback、fault surfaces | 提供字体、对比、朗读和 focus graph 验收，不改变 read model |
| SYS-TENSION | Timed-choice ownership、timeout choice 与暂停规则 | 提供可访问剩余时间和非限时入口；默认关闭 |
| SYS-AUDIO | Engine volume、语音、非语音 cue 与字幕 IDs | 声音不得成为唯一信息通道；self-voicing suppress 规则保持一致 |
| SYS-TEST | Versioned mode/layout/interaction fixtures | 输出 keyboard walk、transcript、1280×720×字体矩阵及无单通道依赖证据 |
| UX / Art Bible | Screen geometry、视觉 token、字体和动效规范 | 必须满足本 GDD 的语义、焦点、对比、动效替代和安全默认值 |

Ren’Py 的 `Preference("font size")`、`Preference("high contrast text")`、`Preference("accessibility menu")`、`V`、`Shift+A`、`Shift+C` 与 `Shift+Alt+V` 均纳入 engine spike 和 production keymap scan；不得只验证自定义 Settings screen。

## Formulas

本系统没有早期/中期/后期数值成长。所有公式输出均为 exact bool、有限枚举或确定性时长。固定顺序为：

`K_ACCESS = (font_scale, high_contrast, reduced_motion, flash_effects_enabled, screen_shake_enabled)`

`settings_tuple(S) = (S.font_scale, S.high_contrast, S.reduced_motion, S.flash_effects_enabled, S.screen_shake_enabled)`

`settings_record(B) = {font_scale:B[0], high_contrast:B[1], reduced_motion:B[2], flash_effects_enabled:B[3], screen_shake_enabled:B[4]}` for an exact five-value tuple `B`.

### Project Settings Validity

The `project_settings_valid` formula is defined as a staged predicate; no membership、sorting or equality operation runs before exact container/scalar types are proven:

`project_settings_valid(S) = exact_dict(S) ∧ key_set(S) = set(K_ACCESS) ∧ exact_float(S.font_scale) ∧ finite(S.font_scale) ∧ S.font_scale ∈ {1.0, 1.25, 1.5} ∧ exact_bool(S.high_contrast) ∧ exact_bool(S.reduced_motion) ∧ exact_bool(S.flash_effects_enabled) ∧ exact_bool(S.screen_shake_enabled)`

`exact_float(x)` means `type(x) is float`; `exact_bool(x)` means `type(x) is bool`. `key_set(S)` is constructed only after `exact_dict(S)` and every key is proven exact `str`; dict insertion order does not affect validity.

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Project settings | `S` | exact built-in dict | exactly 5 fields | Detached project-setting value |
| Allowed fields | `K_ACCESS` | exact tuple | exactly 5 unique paths | Frozen field order |

**Output Range:** exact `true` or `false`; invalid values are rejected without normalization.  
**Example:** `{font_scale:1.5, high_contrast:true, reduced_motion:true, flash_effects_enabled:false, screen_shake_enabled:false}` returns `true`; font scale `1.3`、integer `1`、boolean `true` or any float subclass returns `false`.

### Project Settings Batch Validity

Each update record is an exact built-in two-tuple `(path,value)`; `path` is exact `str` and must use the canonical persistent path (`settings.font_scale` etc.). Validation stages are outer tuple → member exact shape/type → count → canonical path order/uniqueness → exact base → candidate construction → full candidate validation. Any failure returns exact `false` without unpacking、hashing、sorting or invoking custom protocols on an unvalidated value.

`exact_five_settings_tuple(B)` means `type(B) is tuple`、`len(B) = 5` and `project_settings_valid(settings_record(B)) = true`; positional access occurs only after the exact tuple and length checks pass.

`K_ACCESS_PATH = ("settings.font_scale", "settings.high_contrast", "settings.reduced_motion", "settings.flash_effects_enabled", "settings.screen_shake_enabled")`

`project_settings_batch_valid(U,B) = exact_five_settings_tuple(B) ∧ exact_tuple(U) ∧ 1 ≤ |U| ≤ 5 ∧ every_exact_update_pair(U) ∧ paths(U) is a unique canonical-order subsequence of K_ACCESS_PATH ∧ at_least_one_changed_pair(U,B) ∧ project_settings_valid(apply_exact(U,settings_record(B)))`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Setting updates | `U` | exact tuple of exact `(path,value)` tuples | 1–5 entries | Canonically ordered changed fields；unchanged pairs are invalid |
| Settings base | `B` | exact tuple | exactly 5 values | Valid snapshot captured when opened/rebased; current canonical comparison is handled separately by stale detection |

**Output Range:** exact `true` or `false`; one invalid member rejects the complete batch.  
**Example:** updates `(("settings.font_scale",1.5),("settings.reduced_motion",true))` against base `(1.0,false,false,false,false)` return `true`; duplicate、unchanged、unqualified、wrong-shape or wrong-type entries return `false`.

### Settings Rebase Result

`B`、`D` and `C` must each pass `exact_five_settings_tuple` before equality comparison; invalid input returns `REBASE_INPUT_INVALID`. The four valid branches are the truth combinations of `(D = B, C = B)` rather than all mathematical equality partitions of three values.

The `settings_rebase_result` formula is defined as:

```text
settings_rebase_result(B,D,C) =
    REBASE_INPUT_INVALID   if any input is not an exact valid five-setting tuple
    CLEAN_UNCHANGED       if D = B and C = B
    CLEAN_REFRESH         if D = B and C ≠ B
    DIRTY_REBASE_ALLOWED  if D ≠ B and C = B
    STALE_DRAFT_CONFLICT  if D ≠ B and C ≠ B
```

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Base settings | `B` | exact five-value tuple | valid settings | Draft creation/rebase point |
| Draft settings | `D` | exact five-value tuple | valid settings | Current preview |
| Canonical settings | `C` | exact five-value tuple | valid settings | Latest detached root value |

**Output Range:** exactly one of five listed enum values. `C = D ≠ B` remains `STALE_DRAFT_CONFLICT`; a matching external commit must still be explicitly reloaded.  
**Example:** `B=(1.0,F,F,F,F)`, `D=(1.5,F,T,F,F)`, `C=(1.0,F,F,F,F)` returns `DIRTY_REBASE_ALLOWED`; changing `C.high_contrast` to `true` returns `STALE_DRAFT_CONFLICT`.

### Accessibility Semantic Equivalence

Both records must first pass the same frozen surface/state/mode manifest and contain exact ordered ID tuples. Empty semantic tuples are legal only when that manifest registers a gated transient with zero required output and actions.

The `accessibility_semantic_equivalence` formula is defined as:

`accessibility_semantic_equivalence(M0,Mx,F) = matrix_record_valid(M0) ∧ matrix_record_valid(Mx) ∧ same_manifest_identity(M0,Mx) ∧ canonical_choice_ids(M0) = canonical_choice_ids(Mx) ∧ enabled_action_ids(M0) = enabled_action_ids(Mx) ∧ outcome_ids(M0) = outcome_ids(Mx) ∧ normalized_semantic_output_ids(M0) = normalized_semantic_output_ids(Mx) ∧ semantic_fidelity_valid(F,M0) ∧ semantic_fidelity_valid(F,Mx)`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Baseline presentation | `M0` | accessibility matrix record | one valid surface state | Default settings |
| Accessible presentation | `Mx` | accessibility matrix record | one valid mode combination | Alternate input/output settings |
| Source semantic facts | `F` | exact tuple of approved semantic fact records | complete subjects for the surface | Observable/confirmed facts、knowledge boundary、ambiguity and permitted causal scope |

**Output Range:** exact `true` or `false`; layout, color, animation and spoken/rendered channels may differ, normalized meaning may not.  
**Example:** a choice with IDs `(ask, decide, wait)` and outcomes `(r1,r2,r3)` remains valid when self-voicing and reduced-motion are active; reordering choices or omitting `r2` returns `false`.

### Accessible Causal Binding Validity

`U_ACCESS_SUBJECT` is generated by independent production-source discovery and contains every decision-relevant sensory subject: request、answer/confirmation/refusal、reaction、payoff、chapter summary、ending cause and important audio/environment fact. A binding record is the exact tuple `(subject_kind, subject_id, variant_id, accessible_causal_summary_id, source_hash, localized_text_id, owner_system)`; required variants are the exact tuple `("visual_text","descriptive_subtitle","self_voicing","reduced_motion")`. A semantic fact record is the exact tuple `(subject_kind, subject_id, observable_fact_ids, confirmed_interpretation_ids, epistemic_certainty_id, ambiguity_class_id, permitted_causal_scope_ids, forbidden_inference_ids, source_hash, semantic_review_approval_id)`. `semantic_fidelity_valid` requires summary claims to be a subset of those permitted facts, preserve ambiguity class, pass spoiler/anti-proxy lint, and carry an independent human semantic-review approval.

The `accessible_causal_binding_valid` formula is defined as:

`accessible_causal_binding_valid(C,F,U) = exact_binding_tuple(C) ∧ exact_fact_tuple(F) ∧ exact_nonempty_discovery_record(U) ∧ discovered_subject_ids(U) = catalog_subject_ids(C) = fact_subject_ids(F) ∧ for_each_subject_exact_variants(C,("visual_text","descriptive_subtitle","self_voicing","reduced_motion")) ∧ for_each_subject_one_summary_identity(C) ∧ every_binding_source_hash_matches(C,F) ∧ every_summary_semantic_fidelity_valid(C,F) ∧ forbidden_internal_or_future_fact_count(C,F) = 0`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Binding set | `C` | exact tuple of exact binding records | all discovered subjects × four required variants | Visual、subtitle、self-voicing and reduced-motion bindings |
| Semantic facts | `F` | exact tuple of exact semantic fact records | one per discovered subject | Permitted claims and ambiguity boundary |
| Discovered universe | `U` | exact source-discovery record | nonempty complete production set | Independent coverage oracle |

**Output Range:** exact `true` or `false`.  
**Example:** answer beat `event_erii_points_small_station` and reaction `station_note_ask` each use one approved summary identity across all four variants and only describe registered observable gestures/facts; a self-voicing-only replacement、missing pre-choice answer、mind-reading interpretation or exposed axis ID returns `false`.

### Effective Transition Duration

The formula is evaluated in this order: prove `type(t) is int`、`type(r) is bool` and `type(t_max) is int`; then prove `t_max ≥ 0` and `0 ≤ t ≤ t_max`. Invalid input returns `TRANSITION_INPUT_INVALID` and renders no effect.

`effective_transition_ms(t,r,t_max) = TRANSITION_INPUT_INVALID if inputs invalid; otherwise 0 if r else t`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Authored duration | `t` | exact nonnegative int | `0–t_max` ms | Duration owned by the presenting system |
| Reduced motion | `r` | exact bool | `false/true` | SYS-ACCESS project setting |
| Registered maximum | `t_max` | exact nonnegative int | owning manifest maximum | Upper bound owned by the presenting system |

**Output Range:** `TRANSITION_INPUT_INVALID` or exact int `0–t_max` ms; reduced-motion always produces exact int `0`.  
**Example:** an authored `200 ms` notification transition returns `200 ms` when `r=false` and `0 ms` when `r=true`.

### Accessible Surface Validity

`A`、`L` and `R` must be exact versioned records and exact ordered tuples. Their `surface_id/state_id/mode_set_id/manifest_generation` must exact-match the owning surface manifest before counts are read. Counts are exact nonnegative ints and never accept bool; `R` must exact-match the manifest-declared required action tuple rather than caller-selected data. `intersection_count` counts only prohibited overlap between independently actionable/content regions, not parent-child containment.

The `accessible_surface_valid` formula is defined as:

`accessible_surface_valid(A,L,R,M) = exact_surface_evidence_valid(A,L,R,M) ∧ R = required_action_ids(M) ∧ reachable_keyboard_action_ids(A) = R ∧ ((|R| = 0 ∧ gated_transient(M) ∧ initial_focus_count(A) = 0) ∨ (|R| ≥ 1 ∧ ¬gated_transient(M) ∧ initial_focus_count(A) = 1 ∧ focus_graph_total_from_initial(A,R))) ∧ L.clipped_glyph_count = 0 ∧ L.prohibited_intersection_count = 0 ∧ viewport_unreachable_content_count(L) = 0 ∧ forbidden_single_channel_dependency_count(A) = 0`

**Variables:**

| Variable | Symbol | Type | Range | Description |
|---|---|---|---|---|
| Accessibility evidence | `A` | accessibility matrix record | one surface×mode case | Actions, focus, reading and semantic evidence |
| Layout evidence | `L` | layout evidence record | 1280×720 or approved larger resolution | Rects, clipping, viewport and focus evidence |
| Required actions | `R` | exact tuple of semantic IDs | 0–surface maximum | Actions required by the owning GDD; empty only for a registered gated transient |
| Surface manifest | `M` | exact immutable record | one registered surface/state/mode | Authoritative required actions、initial focus policy and gated-transient classification |

**Output Range:** exact `true` or `false`.  
**Example:** a project-settings fixture with 7 required and 7 keyboard-reachable actions, one initial focus, zero clipped glyphs, zero intersections and zero unreachable content returns `true`; registered `Applying` with zero required/reachable actions and zero focus also returns `true`; any missing Apply action, focus on a gated transient, or clipped label returns `false`.

All formula accessors above are pure and total over their declared external input universe: malformed values return the frozen invalid result before unsafe projection、sorting、hashing or equality.

## Edge Cases

### Settings Data and Validation

- **If project settings contain a missing/extra key, wrong exact type, non-finite value or unapproved font scale**: `project_settings_valid=false`; do not normalize or partially salvage the value, and enter SYS-PERSIST recovery.
- **If `font_scale` is integer `1`、boolean `true`、numeric subclass or custom equality/hash object**: reject it before enum membership；only `type(value) is float` may proceed.
- **If the installed root still contains a legacy pre-v2 layout after the 12-leaf revision**: classify it as an incompatible development fixture/save; do not invent missing values at load time.
- **If `setting_updates` is empty**: Apply is disabled and unfocusable; direct or repeated activation dispatches no batch.
- **If `setting_updates` contains more than five entries, duplicate paths, unknown paths or non-canonical ordering**: reject the complete batch as `REJECTED_INVALID`; assignment and flush counts remain zero.
- **If any update member is not an exact two-tuple of exact string path plus value, or contains an unchanged value**: reject before unpack/sort/apply；custom protocol invocation count remains zero.
- **If `settings_base` is not the exact ordered five-value tuple**: reject the complete batch before candidate construction.
- **If one update is invalid while the other updates are valid**: reject the complete batch; no partial setting change is allowed.
- **If preview code produces an impossible value**: restore the last valid preview immediately, record a development diagnostic and keep Apply disabled.
- **If the target schema has been implemented but the ownership manifest still declares 9 leaves or two setting updates**: fail build/integration validation; do not select whichever contract happens to load first.
- **If existing implementation or public saves are discovered before the v2 amendment is complete**: stop the in-place revision and require a schema version upgrade plus migration ADR and versioned fixtures.

### Draft, Apply and Concurrency

- **If an external update changes only membership, seen state or epoch while the draft is dirty**: rebase the fingerprint/root context, preserve the five-value draft and remain `PreviewDirty`.
- **If external project settings change while the draft is clean**: atomically refresh to the latest settings and restore the same semantic focus.
- **If external project settings change while the draft is dirty**: enter `StaleConflict`; disable and remove Apply from focus until Reload latest or Cancel.
- **If the external settings now equal the dirty draft**: still classify using the frozen rebase formula as `StaleConflict`; Reload latest converts the matching canonical value into a clean draft without a new write.
- **If Apply is activated twice or by mouse and keyboard in the same interaction**: dispatch exactly one batch; subsequent activations, queues and delayed retries are zero.
- **If SYS-PERSIST returns `APPLIED_FLUSHED`**: replace the detached snapshot once, mark the draft clean and show no reward/success animation.
- **If SYS-PERSIST returns `DUPLICATE_NOOP`**: refresh from the canonical snapshot, mark the draft clean and do not flush or show success feedback.
- **If SYS-PERSIST returns `REJECTED_REENTRANT`**: retain the retry draft and `exit_intent`, restore canonical presentation, return to `PreviewDirty`, show a non-technical retry state and do not queue or automatically redispatch.
- **If SYS-PERSIST returns `STALE_DRAFT_CONFLICT`**: enter `StaleConflict` and require Reload latest or Cancel.
- **If SYS-PERSIST returns `PERSIST_FLUSH_FAILED_SAFE`**: restore the previous canonical presentation and enter `SaveFailed` with Retry and Cancel.
- **If SYS-PERSIST returns `COMMIT_STATUS_UNKNOWN` or `PERSISTENCE_UNAVAILABLE`**: clear preview/pending intent, destroy caller-focus restoration and hand off to blocking persistence recovery.
- **If SYS-PERSIST returns `REJECTED_INVALID` for a UI-produced batch**: treat it as a contract defect, clear the invalid draft/preview, enter `SettingsUnavailable`, display only a player-safe close action and record internal diagnostics.
- **If the player requests close with a dirty project draft**: enter `ExitConfirm`; do not silently Apply or discard.
- **If the process exits or crashes while only a preview is dirty**: persist nothing; the next launch uses the last durable canonical settings.

### Engine-Owned Preferences

- **If an engine preference changes while the project draft is dirty**: apply the engine preference immediately without changing `settings_base`, dirty fields or SYS-PERSIST batch contents.
- **If the player Cancels a project-setting draft after changing an engine preference**: restore only the five project-setting previews; do not revert the engine-owned preference.
- **If self-voicing is enabled on an already mounted surface**: announce the current surface title and focused control once, preserve focus and trigger no action.
- **If self-voicing is disabled while speech is queued**: stop pending TTS output, preserve the current surface/focus and do not advance dialogue.
- **If engine preference persistence fails independently of a project draft**: report the engine-owned preference as not saved without rolling back or rewriting SYS-PERSIST values.
- **If `Shift+A`、engine font-size/high-contrast action or an unapproved accessibility-menu entry is invoked in production**: action count is zero and no control-transfer screen opens；font multiplier remains `1.0` and engine high-contrast remains off.
- **If `V` or `Shift+C` is invoked**: toggle only the approved output channel, preserve semantic focus/action gate and dispatch no gameplay/UI action. `Shift+Alt+V` is absent from release keymaps.

### Input, Focus and Layout

- **If keyboard and mouse activation target the same semantic action simultaneously**: the UI activation latch accepts the first event and suppresses all duplicates until the surface transition completes.
- **If self-voicing, alt text or a status announcement emits input-like characters**: treat them only as output; canonical action count remains zero.
- **If font-scale preview causes reflow**: replace the layout atomically and restore the same stable semantic focus ID.
- **If a previously focused semantic ID no longer exists after an upstream content refresh**: use the owning surface’s frozen fallback order; do not guess from coordinates or displayable similarity.
- **If 1280×720 at font `1.5` cannot show all content**: place content in a keyboard-operable viewport while keeping required actions visible in the owning surface’s fixed action area.
- **If long Simplified Chinese text exceeds a row or card**: wrap or vertically reflow it; never truncate the only action label, consequence or compatibility explanation.
- **If focus moves to an item outside a viewport**: scroll that item fully into view before accepting activation.
- **If a required surface has no valid initial focus or a required action is absent from the keyboard graph**: `accessible_surface_valid=false`; fail the surface contract instead of opening a focus trap.
- **If Escape/right-click is pressed during `ExitConfirm`, `Applying` or recovery**: follow that state’s frozen safe action exactly once; never propagate to an underlying menu or scene.
- **If high-contrast preview removes a decorative asset that previously carried focus indication**: retain focus through text plus a high-contrast outline/shape; decoration is never the focus authority.

### Motion, Flash and Screen Shake

- **If reduced-motion is enabled during an active transition**: cancel remaining transition time, render the authored final semantic state in the same interaction and preserve focus.
- **If flashing is disabled during an active flash**: stop all remaining flash frames and render the approved static replacement immediately.
- **If screen shake is disabled during active displacement**: stop the effect, recenter the presentation immediately and retain the same content/focus state.
- **If an authored motion, flash or shake has no semantically equivalent static result**: fail content/build validation; do not silently omit the only feedback.
- **If multiple effect settings change together**: evaluate each channel independently from the same draft; one setting must not rewrite another.
- **If reduced-motion is active while flash or shake remains enabled**: suppress only general transition/looping motion; flash and shake follow their independent switches.
- **If a notification owns an authored `200 ms` transition under reduced-motion**: use `0 ms`; do not delay input or focus until the former duration expires.

### Self-Voicing, Captions and Causal Summaries

- **If Windows TTS is unavailable or initialization/runtime speech fails**: display a player-safe self-voicing-unavailable message, copy the same localized message when clipboard is available, retain the complete keyboard/visual path and expose clipboard voicing；the machine is outside the independently verified nonvisual support configuration unless a compatible external screen reader is present.
- **If no usable Simplified Chinese system voice exists on a release reference fixture**: fail the release support gate and record the tested OS/voice configuration；do not claim nonvisual or pronunciation acceptance for that configuration.
- **If a focusable control lacks readable text or approved `alt/group_alt` content**: fail accessibility validation before release.
- **If a production reaction/payoff lacks `accessible_causal_summary_id`**: fail content lock; do not generate a summary from hidden runtime state.
- **If visual, subtitle, self-voicing and reduced-motion variants bind different summary identities**: `accessible_causal_binding_valid=false`; fail integration.
- **If a summary contains axis, token, qualification, predicate, threshold or internal record IDs**: reject it as presentation-unsafe.
- **If self-voicing is active when a notification or Journal sound would play**: suppress the UI sound while retaining visible text, transcript content and navigation actions.
- **If decorative text would be repeated for every row**: use approved grouping semantics so it is announced once per group; item identity and state remain individually spoken.
- **If mode changes during a reaction/payoff**: switch only the remaining presentation channel, establish the same final summary identity and never replay the semantic event.
- **If a summary would state intent, consent, certainty, future consequence or moral value not present in its semantic fact record**: reject content lock even when all modes reuse the same summary ID.
- **If independent source discovery finds a decision-relevant request/answer/refusal/audio/environment subject absent from the binding catalog**: fail coverage；reaction/payoff-only coverage is insufficient.
- **If a decision-critical summary has not entered the accessible transcript/backlog or remained available on the active surface**: keep the next decision and skip/auto gated；a pose/object state alone cannot release the gate.

### Save, Load, Recovery and Timed Choices

- **If the player saves, loads or rolls back**: all five project settings and engine-owned preferences remain outside per-run restoration; the complete 12-leaf persistent snapshot is unchanged.
- **If explicit New Game starts**: preserve all five project settings and copy only the current collection epoch into run state.
- **If collection reset succeeds**: clear only collection memberships/seen data, increment epoch and preserve all five project settings exactly.
- **If merge processes valid roots**: select and validate the complete five-setting tuple as one settings source; never merge individual fields from different roots.
- **If persistence recovery is active**: use temporary high contrast, font `1.5`, reduced-motion on, flashing off and screen shake off without writing those values.
- **If recovery later obtains a valid canonical root**: mount a new safe interaction using its five settings; do not restore the old Settings caller or pending draft.
- **If a blocking save/load failure surface is shown**: self-voicing and temporary recovery defaults remain available, while Settings, rollback and return-to-loaded-scene paths remain blocked.
- **If timed choices are disabled**: render no countdown, timeout state or timeout dispatch.
- **If timed choices are enabled but the current choice lacks a registered non-timed formal path or accessible remaining-time channel**: fail SYS-TENSION/SYS-ACCESS integration before content lock.
- **If self-voicing is reading the active timed-choice prompt or an allowed accessibility shortcut is being used**: pause countdown consumption until speech/accessibility handling completes and stable choice focus is restored.
- **If the player attempts to open the full Settings screen during a timed critical interaction**: deny the control-transfer action without consuming time; output-only accessibility shortcuts remain available.
- **If timeout occurs after accessible presentation resumes**: SYS-TENSION resolves the registered canonical timeout choice and then uses the normal SYS-CHOICE commit/reaction sequence; SYS-ACCESS performs no semantic write.

Malformed formula、engine-shortcut、semantic-boundary and nonvisual-capability cases above are mandatory negative fixtures, not advisory examples.

## Dependencies

| Dependency | Strength / Direction | Required contract | Current status / gate |
|---|---|---|---|
| Game Concept | Hard design → SYS-ACCESS | 不可削减的无障碍基线、非语言因果、完整六结局与离线要求 | Approved |
| Ren’Py 8.5.3 | Hard runtime → SYS-ACCESS | Focus、viewport、keyboard activation、self-voicing、`alt/group_alt` 与 engine preferences | Pinned；组合行为仍需 engine spike |
| ADR-0002 | Hard architecture ↔ SYS-ACCESS | Accessibility settings 跨周目、单一 persistent root、flush/recovery 边界 | Accepted；2026-08-04 已加入12-leaf amendment |
| ADR-0003 | Hard architecture → SYS-ACCESS | 内容/表现分离、1280×720、键盘焦点、替代文本及无单通道依赖 | Accepted |
| SYS-PERSIST | Hard data / bidirectional | Detached snapshot、五项 project-setting batch、merge/reset/recovery 与完整 result enum | In Revision；12-leaf设计已同步，production code/fixtures/evidence阻止 settings implementation-ready |
| SYS-CHOICE | Hard semantic / bidirectional | Canonical choice、presentation states、等价输入与 commit/reaction 顺序 | Approved with provisional gates；ACCESS/UX evidence 待关闭 |
| SYS-NARRATIVE | Hard content / bidirectional | 玩家可见文本、reaction/payoff identities、accessible summaries、字幕与非语言事实 | In Revision；summary catalog 和完整路线 evidence 待冻结 |
| SYS-SAVE | Hard integration / bidirectional | Action gates、menu entry、slot/failure surfaces、persistent-invariance fixtures | In Revision；12-leaf fixtures 与 ACCESS surface evidence 待同步 |
| SYS-ENDING | Hard presentation / bidirectional | 六结局、cause-card 顺序及玩家安全摘要 | Approved with provisional gates；可访问 cause-card evidence 待完成 |
| SYS-ACHIEVE | Hard presentation / bidirectional | Modal、Journal 状态、notification timing 与 self-voicing suppression | Approved；完整 UI/audio/performance acceptance 仍为下游 gate |
| SYS-JOURNAL | Hard presentation / bidirectional | Stable semantic focus、fault surfaces、三档字体、高对比与 transcript 合同 | In Revision；SYS-ACCESS 阻止其 UI stories Ready |
| SYS-TEST | Hard verification ← SYS-ACCESS | Mode/layout matrices、keyboard walk、TTS、focus、effect suppression 与恢复 fixtures | Not Started；阻止 implementation acceptance |
| SYS-TENSION | Post-MVP conditional / bidirectional | Timed-choice ownership、暂停、倒计时表达与 canonical timeout choice | Deferred；默认关闭，不阻止当前非限时 P0 内容 |
| SYS-AUDIO | Conditional presentation | 字幕/alt、静音、自发声 suppress 与非语音因果冗余 | Not Started；声音不得阻止完整操作 |
| SYS-BUILD | Hard release downstream | Versioned manifests、source hashes、12-leaf schema一致性及 test-only exclusion | Not Started；阻止 release artifact lock |
| SYS-GALLERY | Downstream presentation | Detached unlock state、spoiler-safe keyboard/focus/layout contracts | Not Started；无运行时反向依赖 |
| UX specifications | Hard pre-story gate | Settings、choice、save/load、Journal、notification、ending 与 recovery 的 wireframes/focus graphs | Not Started；UI stories 前必须批准 |
| Art Bible | Soft presentation gate | 字体、焦点样式、高对比变体、动效和静态替代视觉规范 | Not Started；阻止正式资产制作 |

### Interface Boundaries

- SYS-ACCESS 拥有五项项目设置的玩家语义、默认值、预览行为和可访问性验收；SYS-PERSIST 独占 schema、assignment、flush、merge、reset、recovery 与 migration。
- Ren’Py 独占 self-voicing、文字/自动播放/跳过速度和音量 preferences；SYS-ACCESS 不复制这些值到产品 root。
- Ren’Py 的 engine font-size、高对比文字与内建 accessibility menu 在发行构建中不是玩家权威：其值/入口按 Core Rule 18 固定或禁用；只有 `V`/`Shift+C` output-only shortcuts 保留。
- SYS-CHOICE 独占 canonical action 和提交顺序；SYS-ACCESS 只规范化输入与输出通道。
- SYS-NARRATIVE 拥有 reaction/payoff 内容、玩家安全摘要文案和 subject identity；SYS-ACCESS 拥有 required-variant coverage、exact join 与 presentation-safety validation。
- SYS-SAVE 和各 owning GDD 决定 surface 的合法 actions 与安全出口；SYS-ACCESS 证明这些 actions 可达，不增加旁路。
- SYS-TENSION 独占倒计时、暂停与 timeout 语义；SYS-ACCESS 不生成或改写 timeout choice。
- SYS-AUDIO 只增强反馈；字幕、文字、最终状态和可操作项必须在静音或声音不可用时完整保留。
- UX 与 Art Bible 可以决定几何和视觉 token，但不能降低 GDD 的语义等价、焦点、最大字体或静态替代要求。
- SYS-TEST 只观察并验证；不得伪造 production alt/summary records 或向发行包注入测试旁路。

### Required Ordering

1. 批准 SYS-ACCESS GDD。
2. 原子同步 SYS-PERSIST、ADR-0002、Architecture、Control Manifest、SYS-SAVE/SYS-ENDING fixtures 与 Entity Registry 的 12-leaf/5-setting、0 ms reduced-motion 和 engine-accessibility authority 合同。
3. 冻结 project-setting manifest、five-value base/batch、merge/reset/recovery 与旧开发存档不兼容策略。
4. 使用 Ren’Py 8.5.3 小型 spike 验证 focus、viewport、self-voicing、TTS 切换、即时 preference 和 interaction restart。
5. 完成 Settings 及下游 surfaces 的 UX specs、完整 `U_ACCESS_SUBJECT` summary/caption catalogs、可访问 transcript/backlog 与 Art Bible 可访问视觉规范。
6. 实现并运行 keyboard、layout、transcript、effect suppression、save/load/recovery 和 timed-choice integration evidence。
7. SYS-BUILD 验证冻结 schema/manifests/source hashes 后，才允许 release acceptance。

### Bidirectional Consistency Findings

1. 系统索引的 `Engine/UI` 过度简化，应在收尾时扩展为显式的 SYS-PERSIST、SYS-CHOICE、SYS-NARRATIVE、SYS-SAVE、SYS-ENDING、SYS-ACHIEVE、SYS-JOURNAL 和 SYS-TEST 合同。
2. SYS-PERSIST、ADR-0002、Architecture、Control Manifest、SYS-SAVE 与 Entity Registry 已在 2026-08-04 同步12-leaf设计权威；production code/generated manifest/fixtures 仍须按该权威替换，legacy pre-v2 values 必须构建失败。
3. SYS-CHOICE、SYS-NARRATIVE、SYS-SAVE、SYS-ACHIEVE 与 SYS-JOURNAL 均已把 SYS-ACCESS 设为下游 gate，方向与本节一致。
4. SYS-TEST 的系统索引依赖尚未显式包含 SYS-ACCESS，应补充 accessibility matrices、TTS/focus 与 effect suppression evidence。
5. SYS-GALLERY、SYS-AUDIO 尚无批准 GDD；SYS-TENSION 已有 GDD 但按 scope decision 延期至 post-MVP，不授予其当前 persistence setting ownership；SYS-BUILD 仍为 downstream gate。
6. SYS-ENDING 与 SYS-SAVE 的 reduced-motion 规则已于 2026-08-04 同步为即时 `0 ms` 状态切换并禁止 dissolve/fade 例外；production evidence 仍须证明实现一致。

## Tuning Knobs

### SYS-ACCESS-Owned Project Settings

| Knob | Type | Default | Safe values | Disabled / minimum behavior | Enabled / maximum behavior |
|---|---|---:|---|---|---|
| `font_scale` | exact float enum | `1.0` | `1.0, 1.25, 1.5` | `1.0` 使用批准的基础字号 | `1.5` 触发最大字体重排；不得裁切、重叠或隐藏操作 |
| `high_contrast` | exact bool | `false` | `false/true` | 使用默认批准主题，仍须满足非颜色单通道要求 | 使用高对比主题并降低装饰干扰；语义和焦点顺序不变 |
| `reduced_motion` | exact bool | `false` | `false/true` | 使用 owning system 批准的非必要转场和装饰运动 | 非必要转场归零、循环运动停止，直接建立最终语义状态 |
| `flash_effects_enabled` | exact bool | `false` | `false/true` | 全部闪光使用批准的静态替代 | 只允许已通过安全审查且具有静态替代的 authored flash |
| `screen_shake_enabled` | exact bool | `false` | `false/true` | 视口保持稳定，以其他通道表达冲击或变化 | 只允许已登记且具有等价替代的 authored displacement |

这些值必须作为一个五值设置域进行 validation、base capture、merge、reset-preservation 和 recovery。增加、删除、改名或改变 exact type 都会修改 persistent schema，必须同步 SYS-PERSIST、ADR、注册表和迁移策略。

### Externally Owned Parameters

| Parameter | Owner | Current target/range | SYS-ACCESS rule |
|---|---|---|---|
| `notification_transition_ms` | SYS-ACHIEVE | target `200 ms`; safe `0–300 ms` | `reduced_motion=true` 时 effective value 固定为 `0 ms` |
| Timed-choice enable/duration | SYS-TENSION | 默认关闭；数值待其 GDD 冻结 | 必须有非限时正式路径、可访问剩余时间和暂停规则 |
| Self-voicing mode | Ren’Py | Engine preference | 即时生效，不复制到 product root |
| Text/auto/skip speed | Ren’Py | Engine preferences | 即时生效；不得跳过唯一因果事实 |
| Music/sound/voice volume | Ren’Py / SYS-AUDIO | Engine mixer preferences | 静音时全部语义和操作保持完整 |

### Knob Interactions

- `font_scale` 的任何档位变化都必须重跑 1280×720 全 surface 布局、viewport、focus 和 transcript evidence。
- `high_contrast` 可以替换颜色、纹理和装饰，但不能改变 semantic IDs、action availability 或阅读顺序。
- `reduced_motion` 只控制一般转场和循环运动；闪烁与屏幕震动继续服从各自独立开关。
- Flash 或 shake 即使启用，也不能成为信息、状态或因果的唯一通道。
- Engine-owned preference 的即时变化不得污染 project-setting draft、`settings_base` 或 batch。
- Recovery 临时 profile 不是玩家调节项：固定为 high contrast on、font `1.5`、reduced-motion on、flash off、shake off，且不写入 persistent。

### Locked Invariants — Not Tuning Knobs

以下内容不得通过配置改变：

- 12 个规范 persistent leaves 和五项设置的 frozen order；
- 五项设置的 exact types 与默认值；
- Keyboard 可完成全部核心交互；
- 等价输入使用同一 canonical action/choice；
- Self-voicing、字幕或 alt 输出不得激活操作；
- 1280×720、字体 `1.5` 的硬布局基线；
- 无颜色、声音、动画、hover、精确指针或限时输入的单通道依赖；
- Accessible summary 与视觉/字幕/self-voicing/reduced-motion 变体的 exact join；
- Save/load/rollback/new game 不改变五项 project settings；
- Collection reset 保留五项设置；
- Timed choices 默认关闭并保留非限时正式路径。

## Visual/Audio Requirements

### Visual Feedback Language

- Every setting and system state MUST be understandable through a visible label, its current value, and a non-color state cue. Color, texture, hover, animation, sound, vibration, flash, or screen shake MUST NOT be the sole carrier of meaning.
- Dirty draft, applying, apply success, apply failure, stale conflict, and recovery mode MUST use stable text plus shape, outline, or icon-state changes. Success MUST NOT depend on particles; failure MUST NOT depend on alarm flashes, shake, or technical error codes.
- High-contrast mode MUST remove nonessential texture noise while preserving information hierarchy, grouping, focus, selection, disabled state, warning severity, and action priority.
- All visual feedback MUST remain legible at 1280×720 with `font_scale = 1.5`; clipping, ellipsis that removes meaning, and horizontal scrolling of setting labels or values are prohibited.

### High Contrast, Focus and Typography

- `font_scale` values `1.0`, `1.25`, and `1.5` MUST preview with live interface text, not a sample image. Layout reflow MUST preserve control order, labels, values, descriptions, and Apply/Cancel actions.
- Keyboard focus MUST use a persistent outline or shape change plus an explicit focused state; it MUST remain distinguishable from hover, selection, enabled/disabled, dirty, and error states without relying on color or animation.
- `high_contrast = true` MUST switch every accessible surface to the approved high-contrast token set, including overlays, modal dialogs, choice controls, journal entries, save/load slots, achievement notifications, captions, and recovery UI.
- Exact palettes, typefaces, outline widths, contrast ratios, spacing tokens, and focus geometry remain gated by the Art Bible and later UX specification. Until those authorities exist, all directions in this section are provisional production constraints rather than final art tokens.

### Motion, Flash, Shake and Static Replacements

- When `reduced_motion = true`, nonessential UI and narrative transition duration MUST resolve to `0 ms` through `effective_transition_ms`; state changes display directly and MUST NOT use a substitute short fade.
- When `flash_effects_enabled = false`, flashes, strobes, rapid luminance changes, and flash-only emphasis MUST be replaced by a stable composition, persistent state change, or readable caption that communicates the same event.
- When `screen_shake_enabled = false`, shake-only emphasis MUST be replaced by a stable pose, object or environment state change, and—where required for causal understanding—a semantic caption.
- Replacement treatments MUST preserve narrative identity and causal meaning without increasing input urgency. They MUST NOT add a new timing requirement or a new sensory dependency.
- Essential motion, if any is later proposed, requires an explicit documented exception, a semantic alternative, and approval through the Art Bible and architecture controls; no such exception is currently approved.

### Audio, Self-Voicing and Silent-Safe Operation

- Every core flow MUST remain complete and understandable with audio muted or unavailable. Audio MUST NOT be the only indicator of focus, state change, success, failure, urgency, reaction, consequence, or ending resolution.
- Ren’Py self-voicing MUST announce the screen title, focused control, label, current value, availability, contextual description where necessary, and Apply/Cancel/confirmation actions in reading order. Spoken feedback MUST never activate a control or advance a choice.
- Nonessential UI sound effects SHOULD be suppressed when they would create repetitive self-voicing clutter. Any retained audio cue MUST have a visible semantic equivalent.
- Ordinary audio cues MUST bind to an `audio_accessibility_binding_record`. Choice reaction, delayed payoff, journal causal evidence, achievement evidence, and ending explanation MUST use the canonical `accessible_causal_summary_id` rather than a separate paraphrase that can drift from the source event.
- Accessible summaries MUST be authored from the approved semantic fact record: observable action/object/position/sound、confirmed answer and current consequence only. They MUST preserve the source ambiguity/knowledge boundary and MUST NOT infer Erii’s unconfirmed intention、consent、moral value or future route result.
- Decision-critical summaries MUST remain visible or enter the accessible transcript/backlog before the next decision becomes actionable. Transcript entries reuse the canonical summary identity and follow save/load/rollback control position；they are presentation records, not a second causal history.
- Player-facing failures and recovery notices MUST use plain-language localized copy. Technical identifiers may be logged, but MUST NOT be required for player action.

### Asset and Art Bible Gates

- No final palette, font family, focus token, high-contrast token, state icon, transition treatment, static flash replacement, static shake replacement, or audio cue is approved until the Art Bible defines it.
- The Art Bible MUST freeze: standard and high-contrast palettes; typography and fallback coverage; focus/selection/error/disabled tokens; motion and static-replacement language; value-neutral pose/object/environment cues; asset provenance, license, and content hash requirements.
- Asset production MUST include equivalent-state variants needed for reduced motion, disabled flash, and disabled shake. Variants MUST share the same semantic asset identity and localization binding as the default presentation.
- All presentation assets remain subject to ADR-0003: authored content owns semantic meaning; presentation code and assets render that meaning but MUST NOT invent or reinterpret persistent state, choice identity, or causal outcome.

### Cross-System Consistency Findings

- `save-load-rollback.md` and `deterministic-ending-resolution.md` were synchronized on 2026-08-04: reduced-motion presentation uses direct display at `0 ms`, with no short-fade or dissolve alternative.
- `sys-journal.md` was synchronized on 2026-08-04 to mark SYS-ACCESS as Designed with full re-review pending；its implementation evidence remains a downstream gate.
- Existing SYS-SAVE and SYS-JOURNAL color and presentation directions remain provisional until the Art Bible supplies shared tokens; they MUST NOT create system-local accessibility palettes.

*Art Director recommendations are integrated; the Art Bible has not yet been established.*

## UI Requirements

### Settings Screen Structure

设置界面采用单页纵向 viewport，结构顺序固定为：

1. 页面标题；
2. “显示设置需应用，阅读与音频设置立即生效”的简短说明；
3. “显示与效果”项目设置组；
4. “阅读与音频”Ren’Py 引擎偏好组；
5. 非技术状态说明；
6. viewport 外固定操作区。

“显示与效果”按 canonical 顺序提供：

| Semantic control ID | 玩家控件 | Values |
|---|---|---|
| `settings_font_scale` | 字体大小单选组 | `100% / 125% / 150%` |
| `settings_high_contrast` | 高对比度开关 | 开 / 关 |
| `settings_reduced_motion` | 减弱动态效果开关 | 开 / 关 |
| `settings_flash_effects_enabled` | 允许闪烁效果开关 | 开 / 关 |
| `settings_screen_shake_enabled` | 允许屏幕震动开关 | 开 / 关 |

“阅读与音频”提供 Ren’Py engine-owned 即时偏好：

- Self-voicing 开关；
- 文字速度、自动播放速度与跳过速度；
- 音乐、音效与语音音量。

这些引擎偏好不得进入项目设置草稿、五值 `settings_base` 或 SYS-PERSIST batch。Ren’Py font size 固定 `1.0`、high contrast text 固定关闭，内建 accessibility menu/`Shift+A` 不进入发行 surface；项目控件是字体与高对比的唯一权威。首发验收覆盖键盘与鼠标；触控和完整手柄支持不在范围内，但现有引擎映射不得绕过 action gate。设置页不提供独立的项目设置重置功能；collection reset 同样只保留五项设置，不负责恢复其默认值。

### Preview, Apply and Cancel

- 修改任一项目设置后立即预览并进入 `PreviewDirty`，但不写入 persistent。
- 字体与高对比度立即重排当前设置界面；动态、闪烁和震动设置只改变后续表现策略，不自动播放演示。
- 固定操作区顺序为“取消显示更改”→“应用”→“返回”。
- `OpenClean` 时“取消显示更改”和“应用”均 disabled 且 unfocusable；“返回”直接关闭。
- `PreviewDirty` 时“应用”最多发送一个 canonical batch；“取消显示更改”恢复最新合法项目设置，但不撤销已即时改变的引擎偏好。
- dirty 状态下选择“返回”、Escape 或右键时进入 `ExitConfirm`，不得静默应用或丢弃更改。
- Apply 成功或 no-op 后只更新 canonical 值与状态文字，不显示奖励动画、粒子或成功 toast。
- 从 `ExitConfirm` 发起 Apply 时保留退出意图；durable success/no-op 后关闭设置界面，失败时继续留在安全错误流程。

### Focus and Input

- 初始焦点为 `settings_font_scale`。
- Tab 顺序为五项项目设置、引擎偏好、当前可用的固定操作；Shift+Tab 反向。
- 正常模式下 Left/Right 在字体单选组和滑杆内部调整值，Up/Down 可在同组条目间移动；self-voicing 模式下 Up/Down 保留给 Ren’Py 的逐 focusable 朗读遍历，Left/Right 仍只调整当前值。Space/Enter 激活当前控件。
- PageUp/PageDown 只在批准的 viewport 内滚动且不得触发 rollback/rollforward；Tab、Shift+Tab 和 self-voicing Up/Down 导致焦点越出 viewport 时，必须同步将目标完整滚入视野后才允许激活。
- 鼠标与键盘必须调用同一 semantic action；双击或同一 interaction 内的多通道输入由 activation latch 合并为一次操作。
- Hover 仅为视觉补充。隐藏、disabled、底层或当前 action gate 禁止的控件不得进入 focus graph。
- 字体、对比度或布局变化后，通过 stable semantic focus ID 恢复同一控件；必要时先将控件完整滚入视野。
- Modal 必须 trap focus。关闭后恢复 opener；recovery 抢占时销毁旧 caller focus、preview focus 和 pending activation。
- `Applying` 是无交互的 gated transient status，不适用“恰有一个初始交互焦点”的 interactive-surface 断言。

### State Surfaces

| State | 玩家可见行为 | Actions and initial focus |
|---|---|---|
| `ExitConfirm` | “存在尚未应用的显示更改。” | “返回设置”〔初始〕、“应用”、“放弃显示更改”；Escape/右键等同“返回设置” |
| `Applying` | 静态显示“正在保存显示设置……”并 gate 全部输入 | 无可执行操作；只保留成功后的 semantic focus/exit intent |
| `SaveFailed` | “显示设置未能保存，已恢复到上次保存的状态。” | “重试”〔初始〕、“取消” |
| `StaleConflict` | “设置已在其他位置改变，请重新载入后继续。” | “重新载入最新设置”〔初始〕、“取消并关闭”；Apply disabled 且 unfocusable |
| `SettingsUnavailable` | “显示设置暂时不可用，请关闭后重试。” | “关闭”〔初始〕；不得显示字段名、schema 或 result enum |
| `RecoveryHandoff` | 清除普通设置界面、草稿、预览和 caller focus，启用临时安全 profile | 只呈现 SYS-PERSIST recovery surface 批准的操作 |
| Engine preference persistence failure | 说明该即时偏好可能无法在下次启动保留 | 不回滚或重写五项项目设置 |

`REJECTED_INVALID` 只显示“显示设置暂时不可用”等玩家安全信息。Schema、字段名、result enum 和内部 ID 只能进入诊断日志。

### 1280×720 and Font 1.5 Layout

- 1280×720、`font_scale = 1.5` 使用单列堆叠布局，不依赖双栏。
- 标题与固定操作区保持可见；两个设置组位于独立的键盘可操作 viewport。
- 每个控件允许按“标签→当前值→简短效果说明”纵向重排。
- 简体中文长文本必须换行；标签、当前值和必要说明不得通过省略号丢失语义。
- Modal 正文允许滚动，但全部决策操作保持固定可见。
- 1920×1080 只能增加留白或可见行数，不得改变语义顺序、焦点图或操作位置。

### Self-Voicing and Semantic Feedback

阅读顺序固定为：

1. 页面标题；
2. 持久化模式说明；
3. 分组标题；
4. 控件标签、当前值、效果，以及“应用后保存”或“立即生效”；
5. 当前状态；
6. 可用操作。

控件改变时只朗读新值和必要效果，不重新朗读整页。开启 self-voicing 时，当前页面标题与当前焦点各宣布一次；`Applying`、失败、冲突和 recovery handoff 状态各宣布一次。

任何朗读不得激活控件、确认操作、移动焦点、滚动页面或关闭界面。Dirty、applying、失败和冲突必须同时使用稳定文字与非颜色状态标记，不显示面向开发者的 dirty、schema 或 persistence 术语。

Self-voicing 支持声明仅适用于通过 capability preflight 的发行支持配置。Preflight 与运行时故障提示使用同一本地化 message identity；clipboard 可用时同步复制。支持矩阵和发行说明必须列出已验证的 Windows build、SAPI voice、语言、速度与失败分类，不得把“可显示错误文字”等同非视觉 PASS。

### Pending UX Locks

后续 `/ux-design` 必须冻结：

- 引擎滑杆范围、步长与最终玩家文案；
- 所有控件、状态和 modal 的精确几何与 focus graph；
- engine-preference persistence failure 文案；
- 是否需要安全、非自动播放的效果预览；
- self-voicing 在 Windows 简体中文 TTS 下的实际读序与可理解性证据。
- normal/self-voicing/viewport 三种键盘语义以及 `V`、`Shift+C`、disabled `Shift+A` 的逐状态 keymap。

## Acceptance Criteria

### Schema and Formula Coverage

| ID | Evidence | Criterion |
|---|---|---|
| `ACCESS-SCHEMA-001` | `UT_PURE + UT_ENGINE` | **GIVEN** fresh install，**WHEN**构造并 round-trip canonical persistent root，**THEN**root 恰含 12 个规范 leaves，五项设置依次为 `1.0,false,false,false,false`，且全部通过 exact-type validation。 |
| `ACCESS-SCHEMA-002` | `UT_PURE` | **GIVEN** missing/extra key、wrong type、font `1.3`、NaN/±∞、integer `1`、boolean `true`、numeric/custom subclasses 及 wrong bool fixtures，**WHEN**按 staged `project_settings_valid` 验证，**THEN**每项返回 exact false，custom equality/hash、normalize 和 salvage invocation count 为 0。 |
| `ACCESS-SCHEMA-003` | `UT_PURE` | **GIVEN**1–5 项 exact pair、exact canonical persistent path、至少一项真实变化的 updates 与 exact five-value base，**WHEN**运行 `project_settings_batch_valid`，**THEN**返回 true 且 candidate 通过完整五设置验证。 |
| `ACCESS-SCHEMA-004` | `UT_PURE + INSTR` | **GIVEN**empty、6项、duplicate、unknown/unqualified path、out-of-order、unchanged-only、bad base、non-pair/1项/3项 pair、wrong exact path/value type 或单项非法 batch，**WHEN**验证，**THEN**完整 batch 返回 false/`REJECTED_INVALID`，unsafe unpack/hash/sort、assignment、flush 和 partial-apply count 均为 0。 |
| `ACCESS-SCHEMA-005` | `UT_PURE` | **GIVEN**valid `B/D/C` 的 `(D==B,C==B)` 四个 truth combinations、额外 `C==D!=B` fixture 及 malformed tuple/type mutants，**WHEN**运行 `settings_rebase_result`，**THEN**valid exact 输出覆盖四个业务 enum，malformed 均为 `REBASE_INPUT_INVALID`，Python numeric equality 不绕过 exact validation。 |
| `ACCESS-SCHEMA-006` | `UT_PURE` | **GIVEN**同一 frozen surface/state/mode manifest 的 baseline 与批准 mode records及 source semantic facts，**WHEN**运行 `accessibility_semantic_equivalence`，**THEN**合法布局/通道差异返回 true；choice、action、outcome、ordered normalized semantic output、ambiguity或 permitted-fact 的删除、增加、重排/扩张 mutant 返回 false；interactive 空记录不得通过。 |
| `ACCESS-SCHEMA-007` | `UT_PURE + STATIC + REVIEW` | **GIVEN**独立 source discovery、semantic fact records 与全部 required variants bindings，**WHEN**运行 `accessible_causal_binding_valid`，**THEN**discovered/catalog/fact subject sets exact-equal、逐 subject 恰四 variant且共享一个 summary identity、source hash一致、human semantic review批准；missing/divergent/mixed-subject/mind-reading/spoiler/internal-ID mutant 返回 false。 |
| `ACCESS-SCHEMA-008` | `UT_PURE` | **GIVEN**author duration `0`、`200`、owning-system max、`-1`、`max+1`、bool/wrong-type/subclass `t` 与 non-bool `r` fixtures，**WHEN**运行 `effective_transition_ms`，**THEN**valid reduced-motion false/true 返回原 exact int/`0`，invalid 全部返回 `TRANSITION_INPUT_INVALID` 且不 render。 |
| `ACCESS-SCHEMA-009` | `UT_PURE + A11Y` | **GIVEN**exact versioned surface manifest 与 valid/mutated accessibility/layout evidence records，**WHEN**运行 `accessible_surface_valid`，**THEN**caller `R` 必须 exact-match manifest；interactive surface 仅在 required actions exact reachable、唯一 exact-int 初始焦点和从该焦点 total graph 时通过；registered gated transient 仅在 manifest-required/reachable actions 与初始焦点均为零时通过；bool counts、caller-selected empty `R`、裁切、禁止交叠、不可达内容或单通道依赖均失败。 |

### Settings Lifecycle

| ID | Evidence | Criterion |
|---|---|---|
| `ACCESS-SET-001` | `UT_ENGINE` | **GIVEN**安全主菜单或 `PlayableStable` 游戏菜单与合法 snapshot，**WHEN**打开 Settings，**THEN**进入 `OpenClean`、草稿 exact-match 五项 canonical settings，并聚焦批准的首个 semantic control。 |
| `ACCESS-SET-002` | `UT_ENGINE + INSTR` | **GIVEN**`OpenClean`，**WHEN**修改任一项目设置，**THEN**即时预览并进入 `PreviewDirty`，persistent assignment/flush count 为 0。 |
| `ACCESS-SET-003` | `UT_ENGINE + INSTR` | **GIVEN**合法 dirty draft，**WHEN**Apply 返回 `APPLIED_FLUSHED`，**THEN**只提交一个 canonical batch、替换 snapshot 一次、进入 `OpenClean`，且 reward/success animation count 为 0。 |
| `ACCESS-SET-004` | `UT_ENGINE + INSTR` | **GIVEN**dirty draft，**WHEN**Cancel，**THEN**恢复最新合法五设置、进入 `OpenClean`，assignment、flush 和 engine-preference rollback count 均为 0。 |
| `ACCESS-SET-005` | `UT_ENGINE` | **GIVEN**dirty draft，**WHEN**请求关闭，**THEN**进入 `ExitConfirm`；silent apply/discard count 为 0。 |
| `ACCESS-SET-006` | `UT_ENGINE` | **GIVEN**dirty draft与仅 membership/seen/epoch 变化的外部 root，**WHEN**refresh，**THEN**rebase fingerprint/context、保留五值 draft 和 semantic focus，并保持 `PreviewDirty`。 |
| `ACCESS-SET-007` | `UT_ENGINE` | **GIVEN**dirty draft与外部 project-setting 变化，**WHEN**refresh，**THEN**进入 `StaleConflict`，Apply hidden/disabled/unfocusable，Reload latest 或 Cancel 是唯一解决路径。 |
| `ACCESS-SET-008` | `UT_ENGINE + INSTR` | **GIVEN**Applying，**WHEN**同时或重复触发鼠标、键盘、快捷键 Apply，**THEN**batch dispatch count 恰为 1，queue、delayed retry 和第二次 flush count 均为 0。 |
| `ACCESS-SET-009` | `UT_ENGINE + INSTR` | **GIVEN**SYS-PERSIST 完整 result enum及 `exit_intent` true/false，**WHEN**逐项注入结果，**THEN**success/no-op→`OpenClean`或`Closed`、safe failure→`SaveFailed`、stale→`StaleConflict`、unknown/unavailable→`RecoveryHandoff`、reentrant→保留 retry draft并回`PreviewDirty`、invalid→清 draft并进`SettingsUnavailable`；每项恰有一个命名终态。 |
| `ACCESS-SET-010` | `UT_ENGINE` | **GIVEN**dirty project draft，**WHEN**修改 self-voicing、text/auto/skip speed 或 volume，**THEN**engine preference 即时生效而 `settings_base`、dirty field set 与 SYS-PERSIST payload 深值不变。 |
| `ACCESS-SET-011` | `UT_ENGINE` | **GIVEN**项目草稿和 engine preference 都已变化，**WHEN**Cancel 项目草稿，**THEN**只恢复五项项目设置；engine preference 保持新值。 |
| `ACCESS-SET-012` | `UT_ENGINE + PROCESS` | **GIVEN**只有未 Apply 的 preview，**WHEN**强制结束并重启进程，**THEN**加载最后 durable canonical settings，preview 值不存在于 root 或 engine preferences。 |

### Input, Focus and Layout

| ID | Evidence | Criterion |
|---|---|---|
| `ACCESS-NAV-001` | `STATIC + UT_ENGINE + A11Y` | **GIVEN**versioned production surface/action manifest，**WHEN**只用键盘遍历，**THEN**每个核心 action exact reachable，隐藏/disabled action 不进入 focus graph。 |
| `ACCESS-NAV-002` | `UT_ENGINE + INSTR` | **GIVEN**每个 interactive semantic action，**WHEN**分别由鼠标、键盘及批准替代 activation 触发，**THEN**canonical action ID、参数和结果 exact-match。 |
| `ACCESS-NAV-003` | `UT_ENGINE + A11Y` | **GIVEN**逐 state exact manifest `{required_ids,reachable_ids,initial_focus_id\|null,gated_transient}`，**WHEN**首次挂载，**THEN**runtime evidence 与 manifest 逐字段 exact-equal；interactive state 恰一个批准初始 focus，gated transient 三项动作/focus tuples 均为空且 `initial_focus_id=null`。 |
| `ACCESS-NAV-004` | `VISUAL + A11Y` | **GIVEN**全部 production surfaces × `1280×720/1920×1080` × font `1.0/1.25/1.5` × contrast modes，**WHEN**capture longest-copy/0/max-content fixtures，**THEN**clipped glyph、required-action overlap、off-viewport fixed action 和 focus-trap count 均为 0。 |
| `ACCESS-NAV-005` | `UT_ENGINE + A11Y` | **GIVEN**内容超出 viewport，**WHEN**键盘移动至 viewport 外项目，**THEN**目标完全滚入视野后才可 activation，所有正文末端和固定返回/关闭操作可达。 |
| `ACCESS-NAV-006` | `UT_ENGINE` | **GIVEN**mounted surface 与 stable semantic focus，**WHEN**font/high-contrast preview 原子重排，**THEN**同一 ID 恢复并可见，action dispatch count 为 0。 |
| `ACCESS-NAV-007` | `UT_ENGINE` | **GIVEN**focused ID 在上游 atomic refresh 后消失，**WHEN**恢复焦点，**THEN**exact 使用 owning GDD 的冻结 fallback 顺序，coordinate/displayable guessing count 为 0。 |
| `ACCESS-NAV-008` | `UT_ENGINE + INSTR` | **GIVEN**self-voicing、alt、status announcement 与 input-like 文本，**WHEN**输出，**THEN**action/confirmation/scroll/advance count 均为 0。 |
| `ACCESS-NAV-009` | `UT_ENGINE + INSTR` | **GIVEN**`CriticalInteraction`、`LoadedUnvalidated` 或 `BlockingSafeFlow`，**WHEN**尝试菜单、快捷键或 direct action 打开完整 Settings，**THEN**open count 为 0，底层 gate 与计时状态不变。 |
| `ACCESS-NAV-010` | `UT_ENGINE` | **GIVEN**`ExitConfirm`、`Applying`、`SaveFailed`、`StaleConflict`、`SettingsUnavailable` 和 recovery 的 exact key→action/`NOOP` manifest，**WHEN**按 Escape/右键/Enter，**THEN**要求 action 的键恰执行一次批准 action、显式 inert 键执行零次，`Applying` invocation count 为 0，底层传播和重复执行 count 为 0。 |
| `ACCESS-NAV-011` | `STATIC + UT_ENGINE + A11Y` | **GIVEN**production keymap 与 normal/self-voicing/viewport modes，**WHEN**遍历 `Shift+A`、`V`、`Shift+C`、`Shift+Alt+V`、Tab/Shift+Tab、arrows及PageUp/PageDown，**THEN**`Shift+A`与debug voicing无发行 binding，engine font multiplier=`1.0`、engine high contrast=false；`V`/`Shift+C`只切 output channel；self-voicing Up/Down遍历 focus、Left/Right调值、viewport滚动不触发 rollback且焦点目标先完全可见。 |

### Semantic Equivalence, Self-Voicing and Captions

| ID | Evidence | Criterion |
|---|---|---|
| `ACCESS-SEM-001` | `STATIC` | **GIVEN**独立 production source discovery 与批准 binding catalog，**WHEN**枚举 request、answer/confirmation/refusal、reaction、payoff、chapter summary、ending cause及重要 audio/environment facts，**THEN**raw discovered `U_ACCESS_SUBJECT` 非空并与 catalog subject IDs exact-equal；逐 subject 恰绑定一个 presentation-safe `accessible_causal_summary_id`，missing/duplicate/orphan count均0。 |
| `ACCESS-SEM-002` | `STATIC + UT_ENGINE + REVIEW` | **GIVEN**每个 summary subject 的 semantic fact record，**WHEN**比较 default、subtitle、self-voicing、muted 与 reduced-motion variants，**THEN**summary identity、canonical outcome、normalized final semantic tuple、epistemic certainty与ambiguity class exact-match；summary claim IDs均为 permitted-fact subset。 |
| `ACCESS-SEM-003` | `STATIC + REVIEW` | **GIVEN**全部 player-facing accessibility copy 与 frozen spoiler/ambiguity/anti-proxy rubric，**WHEN**执行 lint及双人语义复核，**THEN**axis、token、qualification、predicate、threshold、internal record ID、hidden/future ending rule、未确认内心、沉默即同意、正确答案/重要性代理命中数均为 0；普通叙事词汇的 lint 命中须人工裁决。 |
| `ACCESS-SEM-004` | `UT_ENGINE + INSTR` | **GIVEN**每个 production choice 的鼠标、键盘和 accessibility-equivalent inputs，**WHEN**逐一确认，**THEN**canonical choice ID、commit count、immediate reaction ID 和 payoff obligations exact-match。 |
| `ACCESS-SEM-005` | `UT_ENGINE + INSTR` | **GIVEN**reaction/payoff 正在呈现，**WHEN**切换 self-voicing、contrast 或 motion settings，**THEN**只切换剩余表现通道，semantic event/reaction/payoff replay count 为 0。 |
| `ACCESS-SEM-006` | `UT_ENGINE + INSTR` | **GIVEN**decision-critical canonical fact 尚未进入当前 mode 的可访问输出与 transcript/backlog，**WHEN**skip/auto 或下一 decision 尝试推进，**THEN**gate保持；只有 canonical fact建立且visible/subtitle可重访、self-voicing active时批准的queued/completed策略满足后才解除，visual pose/object alone 永不满足。 |
| `ACCESS-SEM-007` | `HUMAN + A11Y` | **GIVEN**无调试信息的默认、keyboard+self-voicing、muted/captioned、reduced-motion 分层样本，**WHEN**至少8名参与者按冻结 question→metric rubric体验代表性早期choice与六类ending结果，**THEN**各模式分别报告 early-cause recognition、Erii ambiguity/agency comprehension、tragedy decisive-loss/cost-bearer comprehension；任一支持模式三项低于75%即不通过，不得用跨模式平均值掩盖失败。 |
| `ACCESS-TTS-001` | `A11Y + UT_ENGINE` | **GIVEN**所有冻结 surface states，**WHEN**用 self-voicing 遍历，**THEN**transcript exact-match批准的标题、说明、状态、内容和 action 顺序，隐藏/装饰/internal 文本 count 为 0。 |
| `ACCESS-TTS-002` | `UT_ENGINE + A11Y` | **GIVEN**已挂载 surface，**WHEN**开启 self-voicing，**THEN**当前标题与 focus 各宣布一次且不 activation；关闭时停止 pending TTS、保留 focus 且不推进。 |
| `ACCESS-TTS-003` | `SPIKE + UT_ENGINE + A11Y` | **GIVEN**批准 Windows/SAPI 支持配置、voice missing、初始化失败、运行中失败及 clipboard available/unavailable fixtures，**WHEN**执行 capability preflight或启用 self-voicing，**THEN**支持配置完成可听读序；失败分支显示并在可用时复制同一 localized message、保留键盘/视觉路径，并将当前配置标为 nonvisual-unverified；不得联网获取 voice或宣称 PASS。 |
| `ACCESS-TTS-004` | `UT_ENGINE + INSTR` | **GIVEN**self-voicing active，**WHEN**achievement、Journal 或其他可选 UI sound 将播放，**THEN**dispatch/play count 为 0，visible copy、transcript 和 actions 不变。 |
| `ACCESS-TTS-005` | `A11Y` | **GIVEN**重复 rows/groups及 focus leave→other group→return trace，**WHEN**self-voicing 遍历，**THEN**`group_alt`按 engine-native contiguous group entry 朗读一次、离组后返回可再次朗读，每个 item identity/state 每次 focus各朗读一次。 |

### Motion, Flash, Shake and Timed Choices

| ID | Evidence | Criterion |
|---|---|---|
| `ACCESS-FX-001` | `UT_PURE + UT_ENGINE` | **GIVEN**每个 registered transition duration，**WHEN**reduced-motion 分别为 false/true，**THEN**effective duration 分别为 authored value/`0`，final state 与 actions exact-match。 |
| `ACCESS-FX-002` | `UT_ENGINE + VISUAL + FAULT` | **GIVEN**活动转场及批准的 external/recovery setting refresh或 fault injection，**WHEN**中途启用 reduced-motion，**THEN**同一 interaction 立即建立 authored final state、保留 focus，remaining animation frames 为 0；不虚构玩家在 critical interaction 内打开完整 Settings 的路径。 |
| `ACCESS-FX-003` | `UT_ENGINE + VISUAL + FAULT` | **GIVEN**每个 authored flash及批准 refresh/fault trigger，**WHEN**flash disabled 或中途关闭，**THEN**flash frame count 为 0/停止增长，并显示批准 static replacement。 |
| `ACCESS-FX-004` | `UT_ENGINE + VISUAL + FAULT` | **GIVEN**每个 authored screen shake及批准 refresh/fault trigger，**WHEN**shake disabled 或中途关闭，**THEN**displacement 为 0/立即归零，content、focus 与 outcome 不变。 |
| `ACCESS-FX-005` | `UT_PURE + UT_ENGINE` | **GIVEN**reduced-motion、flash 和 shake 的全部 8 种布尔组合，**WHEN**计算/呈现，**THEN**三个 channel 仅服从各自设置，不互写且 semantic outputs exact-match。 |
| `ACCESS-FX-006` | `STATIC` | **GIVEN**production effect manifest且每项分类为`semantic`或`decorative`，**WHEN**扫描，**THEN**semantic event恰有 static semantic binding；decorative event恰有 inert final rest state且信息增减为0；缺失/双重分类即构建失败。 |
| `ACCESS-TIME-001` | `UT_ENGINE + STATIC` | **GIVEN**SYS-TENSION 默认关闭，**WHEN**遍历全部正式路线，**THEN**countdown、timeout presentation 和 timeout dispatch count 均为 0。 |
| `ACCESS-TIME-002` | `STATIC + UT_ENGINE + A11Y` | **GIVEN**任一 timed choice fixture，**WHEN**启用 SYS-TENSION，**THEN**存在 registered non-timed formal path、非单通道剩余时间和 canonical timeout choice；缺一项则 integration fail。 |
| `ACCESS-TIME-003` | `UT_ENGINE + INSTR` | **GIVEN**self-voicing 正在朗读 timed prompt 或允许的 accessibility shortcut 正在处理，**WHEN**采样计时器，**THEN**elapsed countdown delta 为 0，稳定 choice focus 恢复后才继续。 |
| `ACCESS-TIME-004` | `UT_ENGINE + INSTR` | **GIVEN**timed critical interaction，**WHEN**尝试打开完整 Settings，**THEN**Settings open count 和 countdown consumption 均为 0；合法 timeout 仍由 SYS-TENSION 提交同一 canonical choice。 |

### Persistence and Cross-System Integration

| ID | Evidence | Criterion |
|---|---|---|
| `ACCESS-PERSIST-001` | `UT_ENGINE + INSTR` | **GIVEN**合法 12-leaf root，**WHEN**执行 save、load、rollback 和 blocking exit，**THEN**全部 12 leaves 深值不变。 |
| `ACCESS-PERSIST-002` | `UT_ENGINE` | **GIVEN**任意合法五设置组合，**WHEN**explicit New Game，**THEN**五设置 exact preserved，只有当前 collection epoch 被复制到 run state。 |
| `ACCESS-PERSIST-003` | `UT_ENGINE + INSTR` | **GIVEN**非空 collections 与任意五设置，**WHEN**collection reset 成功，**THEN**collections/seen 清空、epoch 恰加一、五设置 exact preserved。 |
| `ACCESS-PERSIST-004` | `UT_PURE + UT_ENGINE` | **GIVEN**valid merge roots，**WHEN**merge，**THEN**完整 five-setting tuple 来自一个批准 source，per-field mixed-source count 为 0，结果通过 12-leaf validator。 |
| `ACCESS-PERSIST-005` | `UT_ENGINE + A11Y` | **GIVEN**invalid root、commit-unknown 或 reset recovery，**WHEN**显示 recovery surface，**THEN**effective profile exact 为 `high_contrast=true`、`font_scale=1.5`、`reduced_motion=true`、`flash_effects_enabled=false`、`screen_shake_enabled=false`，persistent write count 为 0。 |
| `ACCESS-PERSIST-006` | `UT_ENGINE` | **GIVEN**legacy pre-v2 development root，**WHEN**startup validation，**THEN**分类 incompatible 并进入安全恢复；silent missing-field insertion 和 normal Settings open count 为 0。 |
| `ACCESS-INT-001` | `UT_ENGINE + A11Y` | **GIVEN**SYS-SAVE 的 browser、confirmation、failure 和 blocking surfaces，**WHEN**遍历 accessibility matrix，**THEN**required actions/focus/reading order exact-match SYS-SAVE，且无 load gate bypass。 |
| `ACCESS-INT-002` | `UT_ENGINE + A11Y` | **GIVEN**SYS-JOURNAL 0/max/fault/pending/recovery states，**WHEN**以最大字体、键盘和 self-voicing 遍历，**THEN**其 frozen semantic focus、fixed actions、transcript 和 no-hidden-content contracts全部成立。 |
| `ACCESS-INT-003` | `UT_ENGINE + A11Y` | **GIVEN**SYS-ACHIEVE 1/max modal与Journal seen states，**WHEN**遍历，**THEN**viewport、continue focus、state text、audio suppression 和 reduced-motion transition exact-match上游合同。 |
| `ACCESS-INT-004` | `UT_ENGINE + A11Y + BRANCH` | **GIVEN**全部 reachable terminal classes、六结局及各自 1–3 cause cards，**WHEN**逐一浏览，**THEN**heading-level、card identity/count/order、focus sequence、actions与summary bindings exact-match批准 manifest；逐 class decisive loss、cost bearer、Erii outcome及unresolved consequence保持可理解，不因结局类型改变可达性或价值层级。 |
| `ACCESS-INT-005` | `STATIC + UT_ENGINE` | **GIVEN**SYS-CHOICE/NARRATIVE production catalogs，**WHEN**验证 choice/reaction/payoff/accessibility joins，**THEN**每个玩家输入和 summary binding exact-covered，无第二语义写入路径。 |

### Performance, Engine Verification and Build

| ID | Evidence | Criterion |
|---|---|---|
| `ACCESS-PERF-001` | `BENCH` | **GIVEN**冻结的最低硬件、Windows build、renderer、window/DPI/vsync、timer、GC、cold/warm policy、surface/mode/longest-copy manifest、5次 warm-up 与Q9批准的样本/percentile方法，**WHEN**测量普通 dispatch→first stable frame，**THEN**p95≤16.6 ms、max≤33.2 ms，并保留原始样本与置信规则。 |
| `ACCESS-PERF-002` | `BENCH + INSTR` | **GIVEN**font reflow、contrast swap、motion snap 与 focus restore fixtures，**WHEN**测量 restart→stable layout/focus restored，**THEN**遵守Q9批准的独立 reflow latency预算，action replay/duplicate activation count 为 0；普通帧预算与 SYS-PERSIST flush wait 分别报告。 |
| `ACCESS-SPIKE-001` | `SPIKE + A11Y` | **GIVEN**Ren’Py 8.5.3 与目标 Windows 10/11 fixtures，**WHEN**验证 focus、viewport、normal/self-voicing keymap、`V/Shift+A/Shift+C/Shift+Alt+V`、engine font/high-contrast authority、`alt/group_alt`、debug transcript、clipboard mode、preference persistence 和 interaction restart，**THEN**每项 mandatory capability 必须 PASS；FAIL/UNVERIFIED 均阻止 implementation-ready，只有先批准替代合同并重测PASS才能关闭。 |
| `ACCESS-SPIKE-002` | `SPIKE + HUMAN` | **GIVEN**版本化关键字符串 corpus、listener qualification、重试与评分 rubric及目标系统可用 Simplified Chinese TTS voices，**WHEN**朗读最长 UI copy、角色名、单音节、错误/恢复提示和因果摘要，**THEN**记录 OS/voice/速度、完整 transcript，所有关键 action/error/cause strings达到批准阈值；无通过配置时不得宣称 self-voicing accepted。 |
| `ACCESS-BUILD-001` | `STATIC` | **GIVEN**SYS-PERSIST GDD、ADR-0002、Architecture、Control Manifest、SYS-SAVE fixtures、Entity Registry 与 production code，**WHEN**同步检查，**THEN**全部只声明同一 12-leaf/5-setting 权威；并行 legacy authority count 为 0。 |
| `ACCESS-BUILD-002` | `STATIC` | **GIVEN**production source，**WHEN**扫描，**THEN**flat project `persistent.*` settings、direct root writes、第二套 engine preference storage、runtime hidden-state summary generation、test-only accessibility forgery 和 network/telemetry count 均为 0。 |
| `ACCESS-BUILD-003` | `STATIC` | **GIVEN**SYS-ACCESS acceptance bundle，**WHEN**汇总 criterion IDs，**THEN**每个 ID 唯一并映射到 typed evidence artifact：自动化证据含 source/catalog hashes、fixture/assertion IDs、runner/environment、raw output与exit code 0；VISUAL/HUMAN/REVIEW证据含 reviewer、rubric、captures/raw responses、adjudication与PASS status；空壳、类型错配或 stale evidence 失败。 |

该验收矩阵已纳入 full design-review 的 QA/UX/engine adversarial findings；具体 fixture generation 与人工协议仍须由独立 QA 在实施前复核。

## Closed Review Decisions

| ID | Decision | Consequence |
|---|---|---|
| `ACCESS-R1` | Nonvisual support is guaranteed only for declared Windows 10/11 configurations with a verified usable Simplified Chinese SAPI voice；clipboard voicing is supported interoperability, not a bundled speech synthesizer guarantee. | Add capability preflight、release support matrix and failure classification；narrow absolute Player Fantasy language without cutting self-voicing. |
| `ACCESS-R2` | SYS-ACCESS project settings are the sole font-scale/high-contrast authority. Ren’Py engine multiplier stays `1.0`、engine high contrast stays off、built-in accessibility menu/`Shift+A` is disabled；`V`/`Shift+C` remain output-only. | No multiplied layout modes or second preference storage；add production keymap/static scan and 8.5.3 spike. |
| `ACCESS-R3` | Existing flat prototype fields and local development saves are disposable development artifacts with no public compatibility duty. | Keep schema v2 at the single 12-leaf authority；all future post-release schema changes require version bump and migration ADR. |

## Open Questions

| ID | Open Question | Owner | Due | Closure Evidence |
|---|---|---|---|---|
| `ACCESS-Q2` | 已同步的12-leaf / 5-setting设计合同何时在production code、generated manifest与fixtures中完成原子落地？ | SYS-PERSIST + Architecture / Andwey | SYS-ACCESS implementation-ready gate 前 | 代码root validator、ownership manifest、batch、merge/reset/recovery与SYS-SAVE fixtures exact匹配2026-08-04设计权威；foreign/stale legacy scan为0，不存在并行权威 |
| `ACCESS-Q3` | 设置页的精确几何、focus graph、控件文案、滑杆范围与步长、状态 modal 和效果预览策略是什么？ | UX Designer + SYS-ACCESS / Andwey | UI stories Ready 前 | 批准的 `/ux-design` 规范；覆盖 1280×720、三档字体、两种对比度、键盘、鼠标和 self-voicing |
| `ACCESS-Q4` | 默认与高对比视觉 token、简体中文字体、焦点轮廓及 reduced-motion/flash-off/shake-off 静态替代语言是什么？ | Art Director + UX Designer / Andwey | Asset production 前 | 批准的 Art Bible、资产来源与许可规则，以及后续 `/asset-spec system:sys-access` 输出 |
| `ACCESS-Q5` | Ren’Py 8.5.3 的 viewport、stable semantic focus 恢复、interaction restart、模式切换和 engine-preference 保存行为是否满足本合同？ | UI Programmer + SYS-TEST / Andwey | 实现 stories Ready 前 | 最小 engine spike；keyboard walk、focus trace、mode-switch、Apply/Cancel 与 preference persistence evidence |
| `ACCESS-Q6` | 哪些具体 Windows build、Simplified Chinese SAPI voice、速度与 corpus 满足已冻结的 release support contract？失败提示最终文案是什么？ | SYS-ACCESS + UX + QA / Andwey | Self-voicing story Ready 前 | 按 `ACCESS-R1` 执行人工听测、读序、capability preflight与 missing/init/runtime-failure fixtures；所有关键字符串达到批准阈值 |
| `ACCESS-Q7` | `U_ACCESS_SUBJECT` 中每个 request、answer/refusal、reaction、payoff、chapter summary、结局原因与重要声音/环境事实的最终可访问摘要、字幕、semantic fact及 binding identity 是什么？ | SYS-NARRATIVE + SYS-AUDIO + SYS-ACCESS / Andwey | Content lock 前 | source discovery exact coverage、`accessible_causal_summary_id`/semantic fact/`audio_accessibility_binding_record` catalogs；ambiguity、mind-reading、spoiler、anti-proxy与内部术语双人复核 |
| `ACCESS-Q8` | 限时选择启用后，self-voicing、焦点移动、替代输入和 modal 期间的倒计时暂停与播报规则是什么？ | SYS-TENSION + SYS-ACCESS + UX / Andwey | Timed-choice implementation 前 | SYS-TENSION 批准合同；默认关闭、剩余时间多通道表达、非限时正式路径及无输入惩罚测试 |
| `ACCESS-Q9` | 如何冻结完整 accessibility mode-set、布局矩阵、性能环境和证据格式？ | SYS-TEST + SYS-ACCESS / Andwey | QA plan / implementation gate 前 | 版本化 fixture manifest；12-leaf invariance、720p×字体×对比度×效果×self-voicing/静音矩阵、原始 captures/traces 与性能样本 |
| `ACCESS-Q10` | 已同步的跨系统设计 authority 是否全部取得消费者实现与验证证据？ | SYS-SAVE + SYS-ENDING + SYS-JOURNAL + SYS-PERSIST / Andwey | 跨 GDD consistency gate 前 | 设计侧保持 reduced-motion `0 ms`、12-leaf/五设置、单一设置入口与正式 SYS-ACCESS 状态；消费者实现、自动化与构建证据全部通过 |
