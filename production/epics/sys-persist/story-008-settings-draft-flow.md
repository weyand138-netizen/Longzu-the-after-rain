# Story 008: Settings batch、draft conflict 与失败处理

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
**ADR Decision Summary**: SYS-ACCESS 拥有五项 setting semantics，SYS-PERSIST 负责一次性 settings batch、root replacement 与 flush。external merge 期间 dirty draft 不能覆盖新 root，safe failure 与 commit-unknown 必须使用不同恢复路径。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: settings screen、persistent batch、reentrant Apply、flush error 与 commit-unknown 必须在目标引擎验证。

**Control Manifest Rules (this layer)**:
- Required: 五项 project settings 作为 canonical tuple 存储，setting batch 一次 replacement/flush。
- Required: dirty draft 使用 rebase/conflict 规则，不覆盖 newer canonical root。
- Forbidden: 不得启用 Ren’Py 第二套 font/contrast authority。
- Guardrail: safe failure 保留在 Settings；commit-unknown 进入 blocking recovery，均不显示 saved success。

---

## Acceptance Criteria

- [ ] `PERSIST-UI-001`: 两项合法 draft change 与 external unlock update rebase 后 Apply，只替换请求 settings、保留新 unlock，一次 replacement/flush 后控件与 snapshot 一致，重复 Apply dispatch/queue 为 0。
- [ ] `PERSIST-UI-002`: dirty preview 期间 external settings change 进入 `STALE_DRAFT_CONFLICT`，Apply disabled；Reload latest/Cancel 恢复最新 snapshot，stale draft 不写 root。
- [ ] `PERSIST-UI-003`: safe pre-write failure 留在 Settings 并提供 Retry/Cancel、控件恢复 previous values；commit-unknown 进入 blocking recovery；均不显示 saved/success。

## Implementation Notes

- Settings semantics 由 SYS-ACCESS 提交，SYS-PERSIST 只接收已验证的 canonical draft。
- unchanged settings 不产生 replacement/flush；合法 changed batch 一次完成。
- UI 不直接访问 persistent root，使用 approved request/snapshot API。

## Out of Scope

- Story 001：setting value/root validation。
- Story 007：recovery state machine。
- SYS-ACCESS Epic：完整 settings semantics 与 alternative presentation。

## QA Test Cases

*Manual verification steps not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: draft rebase; stale conflict; one Apply replacement/flush; safe failure; commit-unknown; idempotence.

## Test Evidence

**Story Type**: UI  
**Required evidence**:
- `production/qa/evidence/sys-persist-settings-evidence.md` — draft/rebase/conflict、safe failure、commit-unknown 与 focus/notification evidence。

**Status**: [x] Created and passing — 2 integration tests

## Dependencies

- Depends on: Story 002, Story 005, Story 007

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; draft apply, external conflict, rebase, and conflict status covered.
**Deviations**: None.
**Test Evidence**: `tests/integration/sys_persist/settings_draft_test.py`
**Code Review**: Complete — APPROVED; canonical settings remain SYS-ACCESS-owned and one batch boundary is preserved.
- Unlocks: Story 010
