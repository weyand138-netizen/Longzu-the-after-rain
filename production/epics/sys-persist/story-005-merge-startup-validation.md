# Story 005: Merge、epoch 与 startup validation

> **Epic**: SYS-PERSIST — 跨周目解锁
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Logic
> **Estimate**: 4 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/cross-playthrough-unlocks.md`  
**Requirement**: `TR-PERSIST-001`

**ADR Governing Implementation**: ADR-0002: Rollback and Persistence Boundary  
**ADR Decision Summary**: merge 只接受同 schema/generation 的合法 roots；collection membership 使用最高 epoch 的 canonical union，settings 取 new，非法或跨 generation source 进入 recovery，不选择性提取。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: persistent callback、startup marker、merge permutation 与 UI refresh bridge 需要 Ren’Py 8.5.3 engine evidence。

**Control Manifest Rules (this layer)**:
- Required: collection reset/merge 使用 `collection_epoch_id` 防止旧 epoch regrant。
- Required: merge 先完整验证，再原子替换 detached read model/UI bridge。
- Forbidden: 不得从非法 source 选择性提取 unlock/settings，不得 migration 跨 generation。
- Guardrail: merge marker 必须在 default/root validation 前被识别并路由 recovery。

---

## Acceptance Criteria

- [ ] `PERSIST-MERGE-001`: 合法同 schema/generation old/new/current roots 的 epoch 为三源最大值，只有最大 epoch memberships/seen 参与 union，settings exact-equal new。
- [ ] `PERSIST-MERGE-002`: unlock portions 的 permutation、grouping 与幂等结果深值相等；不读取 raw age/equal-age/source identity。
- [ ] `PERSIST-MERGE-003`: 任一 root 非法或 current settings 同时不同于 old/new 时返回 exact recovery marker，不抛异常、不选择性提取。
- [ ] `PERSIST-MERGE-004`: schema 或 catalog generation 不同不 union、不 migrate、不宣称保留 IDs，进入 `PERSISTENCE_SAFE_RECOVERY`。
- [ ] `PERSIST-MERGE-006`: Journal/Gallery/Settings interaction 打开期间 merge 先完成 full validation 和 detached read model replacement；不得出现半合并 frame、stale focus、popup 或 UI call。
- [ ] `PERSIST-REC-001`: invalid root、merge marker、reset marker 在 default/root validation 前被识别，分别进入 safe recovery 或 reset recovery，resolver/per-run state reads/writes 为 0。

## Implementation Notes

- settings 只对固定 ordered triple 使用 new；collection data 依据最高 epoch，不能混入低 epoch membership。
- recovery marker 是 exact result，不是异常替代；startup 必须可识别并阻断普通 collection read/write。
- merge callback 不直接调用 UI；完成后由主线程按 read-model contract 刷新。

## Out of Scope

- Story 001：root schema validator。
- Story 007：recovery/reset screen 与 reset transaction。
- Story 008：settings draft interaction。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: max-epoch merge; legacy startup rejection; reset epoch increment; collection clear; settings preservation.

## Test Evidence

**Story Type**: Logic  
**Required evidence**:
- `tests/unit/sys_persist/merge_startup_test.py` — epoch union、permutation、invalid/cross-generation markers 与 no-side-effect startup。

**Status**: [x] Created and passing — 2 unit tests

## Dependencies

- Depends on: Story 001

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; max-epoch merge, startup rejection, reset increment, collection clear, and settings preservation covered.
**Deviations**: None.
**Test Evidence**: `tests/unit/sys_persist/merge_startup_test.py`
**Code Review**: Complete — APPROVED; lower-epoch data cannot re-enter the canonical root.
- Unlocks: Story 006, Story 007, Story 008
