# Story 004: Achievement backend projection 与 repair

> **Epic**: SYS-PERSIST — 跨周目解锁
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Integration
> **Estimate**: 3 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/cross-playthrough-unlocks.md`  
**Requirement**: `TR-PERSIST-001`

**ADR Governing Implementation**: ADR-0002: Rollback and Persistence Boundary  
**ADR Decision Summary**: canonical root 是 product authority；backend 只接受 root-to-backend projection。backend 缺失 membership 可在 startup/checkpoint repair，backend 额外 membership 永远不能反向导入 root 或 UI。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: `achievement.grant()` 的调用、startup repair 与 backend failure 行为必须使用目标 Ren’Py 8.5.3 evidence。

**Control Manifest Rules (this layer)**:
- Required: achievement grant 仅在 canonical root transition 成功后发生。
- Required: projection 每 interaction 至多一次，repair 按 canonical order 且不显示 popup/audio。
- Forbidden: backend 不能成为 root authority，不得写回未知或额外 achievement。
- Guardrail: failed projection 保留 missing，后续只重试仍缺失 IDs。

---

## Acceptance Criteria

- [ ] `PERSIST-PROJ-001`: canonical flush 成功后，每个目标 achievement 每 interaction 至多 grant 一次；popup eligibility 只来自成功 root transition 且恰为 1。
- [ ] `PERSIST-PROJ-002`: startup repair 只按 canonical order grant `ProjectionMissing`，root 不变，popup/audio counts 为 0。
- [ ] `PERSIST-PROJ-003`: projection 中途失败后下一 stable repair point 只调用仍缺失 IDs，最终 backend 收敛，已成功项不重复。
- [ ] `PERSIST-PROJ-004`: backend 中 root 未包含的 approved/unknown achievement 不增加 root/product UI，backend-to-root write count 为 0。
- [ ] `PERSIST-PROJ-005`: duplicate、merge、repair、load、rollback、blocking exit 与 new game 不产生 achievement popup 或 unlock audio。

## Implementation Notes

- 使用 `seen_achievement_ids` 只做跨 session discovery，不把它当 pending popup ledger。
- projection 不改变 root；root transition 与 backend result 必须分开记录。
- backend error 不得撤销 canonical root membership，也不得制造成功反馈。

## Out of Scope

- SYS-ACHIEVE Epic：11 项 achievement condition/event catalog。
- Story 002：canonical root batch/flush。
- Story 009：locked/unseen achievement UI 状态。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: eleven condition records; event-tail eligibility; idempotent grant; backend repair; no ending/memory mirror.

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_persist/achievement_projection_test.py` — grant count、missing repair、backend extras、failure retry 与 no-popup invariants。

**Status**: [x] Created and passing — 2 integration tests

## Dependencies

- Depends on: Story 001, Story 002

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; eleven-record catalog, event-tail eligibility, idempotence, and seen-subset invariant covered.
**Deviations**: None.
**Test Evidence**: `tests/integration/sys_persist/achievement_projection_test.py`
**Code Review**: Complete — APPROVED; no ending/memory mirror and no hidden state inputs.
- Unlocks: Story 009, Story 012
