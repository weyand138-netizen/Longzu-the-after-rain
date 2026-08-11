# Story 009: Persistent ownership 与恢复不变性

> **Epic**: SYS-SAVE — 存档、读档与回退
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Integration
> **Estimate**: 3 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/save-load-rollback.md`  
**Requirement**: `TR-SAVE-001` — Free save, load, and rollback remain supported

**ADR Governing Implementation**: ADR-0002: Rollback and Persistence Boundary  
**Secondary ADR**: ADR-0006
**ADR Decision Summary**: SYS-PERSIST 是 persistent root 的唯一 writer；SYS-SAVE 只能恢复 rollback-owned run state。load/rollback 不得重建、覆盖或删除跨周目数据，ending completion 已 flush membership 也必须保持不变。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: persistent root、Ren’Py rollback 与 load installation 的隔离，以及 completion flush 后的 rollback invariance 必须在目标引擎中验证。

**Control Manifest Rules (this layer)**:
- Required: 所有 persistent 变更通过 SYS-PERSIST complete-root replacement + flush。
- Required: explicit New Game 复制当前 collection epoch 到 run envelope，不写回 canonical root。
- Forbidden: SYS-SAVE 不得写入 achievement、ending/memory unlock、migration 或 dedupe ledger。
- Guardrail: ownership manifest 必须 nonempty、12-leaf、generation exact-match。

---

## Acceptance Criteria

- [ ] `SAVE-BOUNDARY-001`: 支持存档加载完成后，schema-v2 ownership manifest、generation、12 owned leaves 与加载前深值快照相等；run epoch 可恢复但不得写回 canonical root。
- [ ] `SAVE-BOUNDARY-002`: rollback 穿过 choice、reaction、payoff、ending entry 或 loaded-save history 时，12 owned leaves 与快照相等，run epoch 按历史恢复。
- [ ] `SAVE-BOUNDARY-003`: 静态及运行时 ownership scan 证明 SYS-SAVE 不创建或写入 achievement、ending/wish unlock、migration、reaction/payoff dedupe ledger。
- [ ] `SAVE-BOUNDARY-004`: trusted-local detached preflight 不改变当前 run/persistent 深值；产品不宣称任意第三方 pickle 安全沙箱。

## Implementation Notes

- 使用 SYS-PERSIST 的 frozen 12-leaf ownership manifest 作为验证输入，不在 SYS-SAVE 复制第二份 persistent schema。
- load/rollback 只处理 rollback-owned state；任何 persistent mutation 必须由 SYS-PERSIST coordinator 发生。
- completion event 是 run-owned 输入，已成功 flush 的 ending membership 是 canonical persistent 数据。

## Out of Scope

- SYS-PERSIST Epic：persistent root、batch、merge/reset 与 flush 实现。
- Story 005：completion event 恢复细节。
- Story 012：release archive 的最终 test-only scan。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: complete-root replacement/flush; run save-load-rollback invariance; persistent membership/settings isolation; foreign-writer scan.

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_save/persistent_boundary_test.py` — load/rollback deep snapshot、ownership scan、epoch 与 trusted preflight containment。

**Status**: [x] Created and passing — 1 integration test

## Dependencies

- Depends on: Story 004, Story 005

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; complete-root boundary, run save/load/rollback invariance, and persistent isolation covered.
**Deviations**: None.
**Test Evidence**: `tests/integration/sys_save/persistent_boundary_test.py`
**Code Review**: Complete — APPROVED; per-run restore has no persistent-root write path.
- Unlocks: None
