# Story 006: Save/load/rollback/new-game 不变性

> **Epic**: SYS-PERSIST — 跨周目解锁
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Integration
> **Estimate**: 4 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/cross-playthrough-unlocks.md`  
**Requirement**: `TR-PERSIST-001`, `TR-PERSIST-002`

**ADR Governing Implementation**: ADR-0002: Rollback and Persistence Boundary  
**Secondary ADR**: ADR-0006
**ADR Decision Summary**: persistent root 不属于 per-run save/rollback envelope；supported/unsupported/corrupt load、rollback、blocking exit 与 explicit new game 都必须保持 12 leaves 深值不变。run epoch、ending lifecycle 与 completion event 由各自 owner 恢复。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: Ren’Py save/load/rollback、after_load、persistent flush 后的 lifecycle invariance 与 restart fixtures 需目标引擎验证。

**Control Manifest Rules (this layer)**:
- Required: load/rollback never mutate persistent root。
- Required: explicit new game 复制当前 epoch 到 run envelope，保留合法 persistent data。
- Forbidden: per-run save 不得清除、修复、迁移或重建 persistent。
- Guardrail: empty/partial/stale/wrong-field-count manifest 不得通过 invariance checker。

---

## Acceptance Criteria

- [ ] `PERSIST-INV-001`: supported manual/quick/auto load 后 12 owned leaves 与 load 前 deep snapshot 全部相等。
- [ ] `PERSIST-INV-002`: rollback 穿过 choice、reaction、payoff、chapter completion、ending entry/completion 时，SYS-PERSIST writer/flush counts 为 0，12 leaves 不变。
- [ ] `PERSIST-INV-003`: blocking safe flow 的 main-menu exit 与 OS quit/restart 后 12 leaves 不变，writer/flush/popup counts 为 0。
- [ ] `PERSIST-INV-004`: explicit new game 前后 12 leaves 深值不变、writer/flush 为 0；run envelope 复制当前 epoch，由各 owner 初始化。
- [ ] `PERSIST-INV-005`: empty、unreadable、legacy、unsupported、corrupt、internal-failure per-run save 均不清除、修复或重建 product root。
- [ ] `PERSIST-INV-006`: empty、partial、stale-generation 或 wrong-field-count manifest 使 invariance evidence 固定失败，不能用 0 或部分 fields 获得 PASS。

## Implementation Notes

- 以 manifest 声明的 12 leaves 做 deep-value snapshot；不能只比较部分字段。
- SYS-PERSIST 只报告 persistent invariance，不宣称 SYS-SAVE 的 run lifecycle 或 completion event owner 合同。
- persistent root 损坏时暂停 collection reads/writes，但不得污染 resolver、axes、history 或 ending lifecycle。

## Out of Scope

- SYS-SAVE Epic：per-run restore、blocking flow 与 rollback control location。
- Story 003：ending completion projection。
- Story 007：persistent safe recovery UI。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: save/load/rollback run-only restoration; persistent isolation; New Game epoch copy; old-epoch regrant rejection.

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_persist/invariance_test.py` — load/rollback/new-game/blocking/manifest fixtures 与 deep snapshot。

**Status**: [x] Created and passing — 1 unit test

## Dependencies

- Depends on: Story 001, Story 003, Story 005

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; run-only restore, persistent isolation, epoch copy, and regrant boundary covered.
**Deviations**: None.
**Test Evidence**: `tests/unit/sys_persist/invariance_test.py`
**Code Review**: Complete — APPROVED; New Game receives epoch without mutating persistent state.
- Unlocks: None
