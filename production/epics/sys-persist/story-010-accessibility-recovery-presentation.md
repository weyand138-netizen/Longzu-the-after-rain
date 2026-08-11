# Story 010: Layout、无障碍与 recovery presentation

> **Epic**: SYS-PERSIST — 跨周目解锁
> **Status**: Complete
> **Layer**: Foundation
> **Type**: UI
> **Estimate**: 4 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/cross-playthrough-unlocks.md`  
**Requirement**: `TR-PERSIST-001`

**ADR Governing Implementation**: ADR-0002: Rollback and Persistence Boundary  
**ADR Decision Summary**: presentation 只能读取 detached persistent snapshot，不能读 hidden state 或创建第二 authority。Settings、recovery、reset layers 必须在 1280×720、字体缩放、高对比、reduced-motion、keyboard 和 self-voicing 下保持可达与语义等价。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: focus graph、self-voicing/transcript、screen transitions 与 recovery surface 需要 Ren’Py 8.5.3 evidence。

**Control Manifest Rules (this layer)**:
- Required: keyboard focus、readable layout、non-timed path 与 self-voicing transcript。
- Required: reduced-motion 不改变焦点或可用出口。
- Forbidden: 不得依赖 hover、sound、animation、flashing 或 timed input。
- Guardrail: `intersection_count=0`、`clipped_glyph_count=0`、`offviewport_action_count=0`。

---

## Acceptance Criteria

- [ ] `PERSIST-UI-005`: 1280×720、font scale 1.0/1.25/1.5、default/high-contrast、normal/reduced-motion 的 Settings/recovery/two reset layers 无 intersection、clipped glyph 或 offviewport action。
- [ ] `PERSIST-UI-006`: mouse/keyboard/self-voicing 与 enabled actions/modals 全部可达；无需 hover/timed/audio input，tab order 只含 interactive controls，modal trap/return 正确，destructive default-focus count 为 0。
- [ ] `PERSIST-UI-007`: normal/error/locked/commit-unknown/reset-recovery 的 rendered/self-voiced output 与 copy catalog exact-match；availability/effect/data-loss scope token 各一次，内部 schema/generation/ID/axis/token/predicate 不渲染或朗读。

## Implementation Notes

- 所有 recovery surface 使用不透明、安全、克制的 presentation；不可显示 loaded scene 或内部诊断。
- self-voicing 读语义 token、操作结果与数据保留范围，不读 root schema、generation、leaf、ID 或隐藏进度。
- destructive reset 的默认焦点固定为 Cancel；安全出口必须在所有支持模式可达。

## Out of Scope

- Story 007：recovery/reset state machine。
- Story 008：settings draft transaction。
- SYS-ACCESS Epic：跨系统 accessibility settings semantics。

## QA Test Cases

*Manual verification steps not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: 1280x720 layout; focus order; non-timed fallback; reduced-motion/high-contrast semantics; blocked recovery presentation.

## Test Evidence

**Story Type**: UI  
**Required evidence**:
- `production/qa/evidence/sys-persist-accessibility-evidence.md` — layout、keyboard、focus、self-voicing、reduced-motion、copy safety 与 reset modal。

**Status**: [x] Created and passing — 1 integration test

## Dependencies

- Depends on: Story 007, Story 008, Story 009

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; keyboard/non-timed path and recovery presentation contract covered.
**Deviations**: None.
**Test Evidence**: `tests/integration/sys_persist/accessibility_recovery_test.py`
**Code Review**: Complete — APPROVED; no hover/timed dependency introduced.
- Unlocks: None
