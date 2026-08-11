# Story 009: Achievement collection 状态展示

> **Epic**: SYS-PERSIST — 跨周目解锁
> **Status**: Complete
> **Layer**: Foundation
> **Type**: UI
> **Estimate**: 3 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/cross-playthrough-unlocks.md`  
**Requirement**: `TR-PERSIST-001`

**ADR Governing Implementation**: ADR-0002: Rollback and Persistence Boundary  
**ADR Decision Summary**: canonical achievement membership 由 root 提供；`seen_achievement_ids` 只表示跨 session 新记录。locked achievement 不渲染、不计数、不聚焦、不 self-voice；backend 不得补写 root membership。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: read snapshot、focus/self-voicing 与 achievement backend projection 的 UI adapter 需目标引擎验证。

**Control Manifest Rules (this layer)**:
- Required: SYS-ACHIEVE 拥有 11 个 stable event-condition records；SYS-PERSIST 只提供 membership projection。
- Required: locked absent、unseen、unlocked 等状态使用 approved copy/icon/focus policy。
- Forbidden: 不得把 achievement names/order/triggers 变成 ending 或 five-axis proxy checklist。
- Guardrail: unavailable 不得伪装成 zero progress，backend 不得反向增加 membership。

---

## Acceptance Criteria

- [ ] `PERSIST-UI-004`: `achievement_catalog:v2` 的 `UNLOCKED`、`UNLOCKED_UNSEEN`、`LOCKED_ABSENT`、`PERSISTENCE_UNAVAILABLE` 状态精确匹配 copy/icon/count/focus/self-voicing policy；locked 不渲染、不占槽、不计数、不聚焦、不朗读。
- [ ] `PERSIST-PROJ-004`: backend 额外 achievement 不增加 canonical root 或 product UI。
- [ ] `PERSIST-PROJ-005`: load、rollback、blocking exit、new game、duplicate、merge、repair 不产生额外 popup/audio。

## Implementation Notes

- `seen_achievement_ids` 必须是 `achievement_ids` 子集，只表示“新记录”发现。
- 不调用 `achievement.has()` 作为 product membership authority；使用 detached snapshot。
- locked/unavailable 状态必须不泄露内部 schema、generation、field、axis、token 或 predicate。

## Out of Scope

- SYS-ACHIEVE Epic：achievement event catalog 与 condition evaluation。
- Story 004：backend grant/repair implementation。
- SYS-JOURNAL Epic：完整 Journal bundle/read model。

## QA Test Cases

*Manual verification steps not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: locked-surface exclusion; stable new/seen ordering; truthful counts; unsafe durable-result deferral.

## Test Evidence

**Story Type**: UI  
**Required evidence**:
- `production/qa/evidence/sys-persist-achievement-ui-evidence.md` — four collection states、count/focus/self-voicing 与 unavailable behavior。

**Status**: [x] Created and passing — 2 integration tests

## Dependencies

- Depends on: Story 001, Story 004

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; locked-surface exclusion, new/seen ordering, and unsafe-boundary deferral covered.
**Deviations**: None.
**Test Evidence**: `tests/integration/sys_persist/achievement_state_ui_test.py`
**Code Review**: Complete — APPROVED; internal state is excluded from presentation rows.
- Unlocks: Story 010
