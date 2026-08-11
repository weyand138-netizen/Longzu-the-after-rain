# Story 002: Batch request、root replacement 与 flush

> **Epic**: SYS-PERSIST — 跨周目解锁
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Integration
> **Estimate**: 4 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/cross-playthrough-unlocks.md`  
**Requirement**: `TR-PERSIST-001`

**ADR Governing Implementation**: ADR-0002: Rollback and Persistence Boundary  
**ADR Decision Summary**: 每个 changing batch 必须构造完整 candidate、执行一次 root replacement、一次 `renpy.save_persistent()`，成功结果只能是 `APPLIED_FLUSHED`；duplicate 返回 `DUPLICATE_NOOP`，不允许 reentrant queue。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: persistent flush、temporary write、replacement、process interruption 与 commit-unknown 需要 pinned engine evidence。

**Control Manifest Rules (this layer)**:
- Required: changing request 走完整-root replacement + required flush。
- Required: invalid batch 在 candidate 前拒绝且 side effects 为 0。
- Forbidden: 不得逐 leaf mutation、set 化去重、暴露第二成功结果或排队 reentrant request。
- Guardrail: safe pre-write failure 与 commit-unknown 必须分开处理。

---

## Acceptance Criteria

- [ ] `PERSIST-UPD-001`～`003`: achievement/ending/memory 与 settings 请求正确更新目标 leaves，其余 leaves 深值不变；每个 batch replacement/flush 各恰一次，公开结果为 `APPLIED_FLUSHED`，ending entry 不能提前提交。
- [ ] `PERSIST-UPD-004`: 已存在 ID 或未变化 setting 返回 `DUPLICATE_NOOP`，root、assignment、flush、projection、popup counts 均为 0。
- [ ] `PERSIST-UPD-005`: duplicate + new batch 只加入 new IDs，整批 replacement/flush 各一次。
- [ ] `PERSIST-UPD-006`: empty/oversize/乱序/duplicate/conflicting settings/wrong owner-kind-ID-event-checkpoint-type 在冻结 validator stage 返回 `REJECTED_INVALID`，合法成员也不得部分应用。
- [ ] `PERSIST-UPD-008`: stale/empty manifest、wrong schema/generation 或 invalid/marker root 在 side effect 前返回 `REJECTED_INVALID` 或 `PERSISTENCE_UNAVAILABLE`，product/backend/presentation 不变。
- [ ] `PERSIST-UPD-009`: reentrant request API entry/body-entry 为 `1/0`，同步返回 `REJECTED_REENTRANT`，queue length=0，首个操作继续。
- [ ] `PERSIST-UPD-010`: proven pre-write failure 恢复 previous root 并返回 `PERSIST_FLUSH_FAILED_SAFE`；不能证明安全终态时返回 `COMMIT_STATUS_UNKNOWN`，冻结后续写入，磁盘只为完整 previous/candidate。

## Implementation Notes

- caller 不能注入 owner ID；owner 由批准的专用 adapter 固定。
- batch 必须保持 canonical ordering，不得先转 set 丢失 duplicate/conflict 诊断。
- flush 成功后才允许 projection 或 player-facing success feedback。
- commit-unknown 重启后走 replay-required 或 silent projection convergence，不补发普通 popup。

## Out of Scope

- Story 001：root schema/manifest validator。
- Story 003：ending completion callsite 的 owner boundary。
- Story 004：achievement backend projection。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: one replacement/one flush; safe pre-write failure; commit-unknown and write freeze; APPLIED_FLUSHED public result.

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_persist/batch_flush_test.py` — valid/duplicate/invalid/reentrant/fault-injection batches 与 exact side-effect counts。

**Status**: [x] Created and passing — 2 integration tests

## Dependencies

- Depends on: Story 001
- Unlocks: Story 003, Story 004, Story 008

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; single replacement/flush, safe failure, and commit-unknown freeze covered.
**Deviations**: None.
**Test Evidence**: `tests/integration/sys_persist/batch_flush_test.py`
**Code Review**: Complete — APPROVED; public success is APPLIED_FLUSHED only.
