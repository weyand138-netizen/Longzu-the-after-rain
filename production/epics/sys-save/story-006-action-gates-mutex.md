# Story 006: Action gates 与操作互斥

> **Epic**: SYS-SAVE — 存档、读档与回退
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Logic
> **Estimate**: 3 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/save-load-rollback.md`  
**Requirement**: `TR-SAVE-001` — Free save, load, and rollback remain supported

**ADR Governing Implementation**: ADR-0002: Rollback and Persistence Boundary  
**Secondary ADR**: ADR-0005
**ADR Decision Summary**: save/load/rollback 只能在稳定控制点执行；critical interaction 期间请求必须拒绝且不排队。engine request permission 与 player-facing affordance 是分离合同，不能由 UI 创建替代加载路径。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: action gate 与 Ren’Py screen action、quick action、keyboard shortcut 的实际调用数需在目标引擎验证。
**Performance**: No measurable performance impact expected — gate checks operate on fixed-size closed matrices without I/O or per-frame scanning；必须保持 Control Manifest 的 60 fps / 16.6 ms interactive-frame budget。

**Control Manifest Rules (this layer)**:
- Required: `V` 与 `Shift+C` 只切换输出通道，不得绕过当前 action gate。
- Global budget: target 60 fps / 16.6 ms interactive frame。

**GDD / Story Contract Rules**:
- Required: critical interaction 中 save/load/rollback invocation count 为 0。
- Required: request permission 与 visible/enabled/focusable affordance 分别使用各自的闭集矩阵。
- Forbidden: 不得隐藏入口后仍保留可聚焦 shortcut，也不得将拒绝请求排队。
- Guardrail: 任一 save/load/rollback operation 未完成时，后续同类请求 invocation count 与 queue length 均为 0。

---

## Acceptance Criteria

- [x] `SAVE-GATE-001`: 已登记稳定点、无 critical interaction 且来源受支持时，manual/quick/auto request allowed 为 `True`；auto save 不创建 UI affordance。
- [x] `SAVE-GATE-001A`: 完整 nonempty phase×action manifest 下，engine permission 与 request 闭集矩阵 exact-equal；仅 player-facing action 拥有 UI affordance，其 visible/enabled/focusable 与 UI 闭集矩阵 exact-equal；`auto_save` 不创建 UI affordance，unknown/missing/extra/wrong-type 输入均返回 `False`。
- [x] `SAVE-GATE-002`: commit→reaction 或 bounded reaction interaction 期间，玩家、快捷键、脚本及替代输入的 save/load/rollback 调用数均为 0，且请求不排队。
- [x] `SAVE-GATE-003`: 任一五类操作进行中，后续操作请求 invocation count 与 queue length 均为 0；不得在首个操作完成后回放拒绝请求。

## Implementation Notes

- 将 `save_request_allowed` 与 `ui_action_affordance` 建模为不同输出，不能用一个输出替代另一个。
- 对 unknown phase/action 失败关闭；不要依赖 truthiness 或未登记默认行为。
- mutex 必须覆盖 manual save、quick save、autosave、load、rollback 五类操作。

## Out of Scope

- Story 007：blocking screen 的 root safe context 与出口。
- Story 010：screen 的视觉布局与 keyboard/self-voicing evidence。

## QA Test Cases

**Automated test file**: `tests/unit/sys_save/action_gates_test.py`  
**Framework**: Python `unittest`; use parameterized `subTest` matrices for phase/action, source/action, and active/follow-up operation coverage.

1. `test_request_matrix_exact_for_all_registered_phases_and_actions` — exhaustively match all registered phases and six actions to the GDD closed request matrix.
2. `test_playable_stable_supported_save_requests_are_allowed` — registered stable manual/quick/auto requests return exact `True`.
3. `test_autosave_has_permission_without_ui_affordance` — autosave permission is independent from visible/enabled/focusable UI state.
4. `test_player_facing_affordance_requires_all_ui_flags` — each player-facing action requires request permission plus exact `True` visible/enabled/focusable fields.
5. `test_each_false_ui_flag_disables_affordance` — independently false visible, enabled, or focusable fields produce exact `False`.
6. `test_missing_extra_and_wrong_type_manifest_inputs_fail_closed` — malformed request/UI manifests return exact `False`.
7. `test_wrong_type_values_are_not_coerced_by_truthiness` — truthy non-bools and protocol-bomb values receive no truthiness or custom protocol dispatch.
8. `test_unknown_phase_or_action_fails_closed` — unknown/unlisted pairs return exact `False` without exception, queue entry, or delayed request.
9. `test_location_and_request_profile_preconditions_fail_closed` — missing registered location, unsupported source, or disabled profile invokes no engine action.
10. `test_critical_interaction_denies_every_source_without_queue` — player/shortcut/script/alternative-input × save/load/rollback yields invocation count `0`, queue length `0`, and continued interaction.
11. `test_disallowed_phases_skip_autosave_without_deferred_replay` — autosave in critical/loaded-unvalidated/blocking phases is skipped and never replayed.
12. `test_mutex_rejects_all_five_by_five_followup_combinations` — the five active operations reject every follow-up operation while the first continues.
13. `test_mutex_does_not_replay_rejected_requests_after_completion` — completion leaves rejected invocation history and queue empty.
14. `test_new_request_is_allowed_after_operation_completion` — a genuinely new explicit or normal-cycle request is evaluated after completion.

**Ren’Py 8.5.3 engine evidence**:
- Verify screen action、quick action、keyboard shortcut、script 与 alternative activation 的 actual invocation/queue counts。
- Verify `V`/`Shift+C` only switch approved output channels and cannot bypass the action gate。
- Verify unavailable player-facing actions are invisible、disabled、unfocusable，且 rejected requests never replay。
- Record results and the 16.6 ms interactive-frame check at `production/qa/evidence/story-006-action-gates-mutex-engine.md`。

## Test Evidence

**Story Type**: Logic  
**Required evidence**:
- `tests/unit/sys_save/action_gates_test.py` — phase×action truth table、critical denial、mutex 与 no-queue assertions。

**Status**: [x] Complete — Python 14/14；Ren’Py global 11/11 testcases、57/57 assertions；lint/compile passed。

## Dependencies

- Depends on: Story 001, Story 003
- Unlocks: Story 007, Story 010

## Completion Notes

**Completed**: 2026-08-10  
**Criteria**: 4/4 passing  
**Deviations**: None  
**Test Evidence**: Logic unit test at `tests/unit/sys_save/action_gates_test.py`；target-engine evidence at `production/qa/evidence/story-006-action-gates-mutex-engine.md`  
**Code Review**: Complete — APPROVED / TESTABLE-CLEAN  
**Smoke Check**: PASS WITH WARNINGS — core、Story 006/regression 与实际 save/load 已确认；16.6 ms manual frame profiling 未在本次 session 执行，保留为 release-level performance sign-off 项。
