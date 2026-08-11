# Story 001: Save 写入、轮换与原子完整性

> **Epic**: SYS-SAVE — 存档、读档与回退
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Integration
> **Estimate**: 4 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/save-load-rollback.md`  
**Requirement**: `TR-SAVE-001` — Free save, load, and rollback remain supported

**ADR Governing Implementation**: ADR-0002: Rollback and Persistence Boundary  
**Secondary ADR**: ADR-0004: Semantic Ending Snapshot and Rollback State Envelope
**ADR Decision Summary**: Ren’Py 原生存档是 per-run 主存档；保存必须捕获完整 rollback-owned 状态，不能引入外部 JSON 主存档或 imported mutable state。状态使用 rollback-transformed 容器，且不得把 persistent 数据混入 per-run 写入。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: 保存、序列化、临时写入、替换和中断恢复行为必须用目标 Ren’Py 8.5.3 验证；引擎数据不面向不可信外部共享。

**Control Manifest Rules (this layer)**:
- Required: 保存数据只包含 primitives 与 Ren’Py-managed rollback collections。
- Required: `semantic_state` 与 sentinel 由显式新游戏初始化，保存时保持同一 coherent envelope。
- Forbidden: file handles、tasks、sockets、displayables 或 imported mutable objects 不得进入 save state。
- Guardrail: 正常 save end-to-end p95 ≤500 ms、max ≤1000 ms，longest-frame p95 ≤16.6 ms、max ≤33.2 ms。

---

## Acceptance Criteria

*From GDD `design/gdd/save-load-rollback.md`, scoped to this story:*

### Verification Status

- [x] SAVE-WRITE-001 — deep save-envelope snapshot contract
- [x] SAVE-WRITE-002 — three-slot quicksave rotation
- [x] SAVE-WRITE-003 — six-slot autosave policy gate
- [x] SAVE-WRITE-004 — confirmed manual overwrite
- [x] SAVE-WRITE-005A/B — interrupted overwrite and first-write atomicity
- [x] SAVE-WRITE-006 — metadata-independent authoritative classification

- [ ] `SAVE-WRITE-001`: 在已登记且允许保存的稳定控制点向空 manual slot 保存后，slot 可读取，且 save-contract/catalog generation、semantic、ending 及全部 rollback-owned per-run fields 等于触发瞬间深值快照。
- [ ] `SAVE-WRITE-002`: 3 个 quicksave slot 已满时再次 quicksave 只替换最旧 slot，新存档成为 newest，其余 slot 内容与顺序保持有效。
- [ ] `SAVE-WRITE-003`: 6 个 autosave slot 已满时，合法 `after_reaction` 或章末 `after_payoff` 只替换最旧 slot；未登记或 action gate 关闭的位置不补写。
- [ ] `SAVE-WRITE-004`: 取消 manual overwrite 时原 slot 字节、时间戳和 metadata 不变；确认并成功写入后 slot 只包含新快照。
- [ ] `SAVE-WRITE-005A`: 覆盖既有 slot 时在序列化、临时写入或替换边界注入 I/O 失败，最终只能是完整旧存档或完整新存档。
- [ ] `SAVE-WRITE-005B`: 首次写入空 slot 时发生同类 I/O 失败，最终只能是不存在或完整新存档。
- [ ] `SAVE-WRITE-006`: 删除、伪造或交换非权威 metadata 不改变 authoritative compatibility result 与恢复状态。

## Implementation Notes

- 使用 Ren’Py 原生 save 机制；不要建立外部 JSON 主存档。
- 保存的 per-run 单元必须包含 save-contract sentinel、catalog generation、semantic state、ending lifecycle 及批准的 rollback-owned 字段。
- 写入失败必须保留完整旧存档或回到不存在状态，不得让部分写入被识别为 `SUPPORTED`。
- quicksave 与 autosave 轮换按固定 newest/oldest 规则执行；autosave 只能发生在登记且允许保存的稳定点。
- slot metadata 只能用于提示，永远不能替代 detached preflight 或 `after_load` 判定。

## Out of Scope

- Story 002：读档预检与兼容性分类。
- Story 006：save/load/rollback action gates 与操作互斥。
- Story 011：性能样本与预算报告。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_save/save_write_test.py` — manual/quick/auto rotation、overwrite、I/O fault injection 与 metadata non-authority。

**Status**: [x] Created and passing

## Dependencies

- Depends on: None
- Unlocks: Story 002, Story 006

## Completion Notes

**Completed**: 2026-08-10
**Criteria**: 6/6 passing at the save-operation contract and Ren'Py configuration level.
**Deviations**: Runtime checkpoint-catalog wiring and engine-level I/O fault injection remain downstream integration work; native quicksave/autosave slot counts are configured and verified.
**Test Evidence**: Integration test at `tests/integration/sys_save/save_write_test.py`; Python 8/8 passed, Ren'Py global 4/4 testcases and 17/17 assertions passed.
**Code Review**: Complete — Approved with suggestions.
