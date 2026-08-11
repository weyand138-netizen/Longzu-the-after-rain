# Epic: SYS-PERSIST — 跨周目解锁

> **Layer**: Foundation
> **GDD**: design/gdd/cross-playthrough-unlocks.md
> **Architecture Module**: SYS-PERSIST
> **Status**: Complete
> **Stories**: Not yet created — run `/create-stories sys-persist`

## Overview

实现跨周目产品数据的唯一 persistent authority：schema-v2 根对象、12 个规范叶、collection epoch、五项设置、成就与结局成员关系、批量更新、flush、merge/reset、启动校验及安全恢复。SYS-PERSIST 是 persistent 数据的唯一写入者，所有改变通过完整 root replacement 后执行一次必要 flush，再向成就后端和展示层投影；ending completion event 由 SYS-ENDING 产生并由单一 persistence coordinator 转换为持久化请求。SYS-PERSIST 不拥有 per-run rollback 状态，不重新运行结局 resolver，也不从 live ending state 推导结果。

## Governing ADRs

| ADR | Decision Summary | Engine Risk |
|-----|------------------|-------------|
| ADR-0002: Rollback and Persistence Boundary | 使用唯一 schema-v2 persistent root，严格区分跨周目数据与 rollback-owned per-run 状态，并规定 flush、epoch、reset 与安全加载边界。 | HIGH |
| ADR-0006: Ending Completion Boundary | 只有完成完整结局叙事后才产生 ending completion event；SYS-PERSIST 只校验并投影该 event，不拥有 completion callsite。 | HIGH |

## GDD Requirements

| TR-ID | Requirement | ADR Coverage |
|-------|-------------|--------------|
| TR-PERSIST-001 | Schema-v2 root, 12-leaf authority, epoch, settings, merge/reset, and flush | ADR-0002 ✓ |
| TR-PERSIST-002 | Ending completion emits one durable completed-event boundary | ADR-0002, ADR-0006 ✓ |

## Definition of Done

This epic is complete when:

- All stories are implemented, reviewed, and closed via `/story-done`
- All acceptance criteria from `design/gdd/cross-playthrough-unlocks.md` are verified
- All Logic and Integration stories have passing test files in `tests/`
- All Visual/Feel and UI stories have evidence docs with sign-off in `production/qa/evidence/`

## Known Gates

- Ren’Py 8.5.3 persistent initialization, flush/merge behavior and process-failure recovery remain HIGH-risk implementation verification gates.
- SYS-ENDING must remain the sole owner of `commit_ending_completion`; SYS-PERSIST must not infer completion from entry or resolver output.
- SYS-ACCESS owns setting semantics, while SYS-PERSIST owns storage and persistence of the canonical five-setting tuple.
- SYS-ACHIEVE, SYS-JOURNAL and SYS-BUILD consume approved projections/manifests; they must not introduce a second persistent authority.
- The active Control Manifest is version `2026-08-04.1`; its ADR coverage must be synchronized with ADR-0006/0007 before implementation hand-off.

## Stories

| # | Story | Type | Status | ADR |
|---|-------|------|--------|-----|
| 001 | [Schema-v2 根与 ownership manifest](story-001-schema-ownership-manifest.md) | Logic | Complete | ADR-0002 |
| 002 | [Batch request、root replacement 与 flush](story-002-batch-flush.md) | Integration | Complete | ADR-0002 |
| 003 | [Ending completion projection 边界](story-003-ending-completion-projection.md) | Integration | Complete | ADR-0006 |
| 004 | [Achievement backend projection 与 repair](story-004-achievement-projection.md) | Integration | Complete | ADR-0002 |
| 005 | [Merge、epoch 与 startup validation](story-005-merge-startup-validation.md) | Logic | Complete | ADR-0002 |
| 006 | [Save/load/rollback/new-game 不变性](story-006-per-run-invariance.md) | Integration | Complete | ADR-0002 |
| 007 | [Safe recovery 与 collection reset](story-007-safe-recovery-reset.md) | Integration | Complete | ADR-0002 |
| 008 | [Settings batch、draft conflict 与失败处理](story-008-settings-draft-flow.md) | UI | Complete | ADR-0002 |
| 009 | [Achievement collection 状态展示](story-009-achievement-state-ui.md) | UI | Complete | ADR-0002 |
| 010 | [Layout、无障碍与 recovery presentation](story-010-accessibility-recovery-presentation.md) | UI | Complete | ADR-0002 |
| 011 | [Pure persistence 性能协议](story-011-pure-performance.md) | Logic | Complete | ADR-0002 |
| 012 | [Engine startup 与 projection 性能证据](story-012-engine-performance.md) | Integration | Complete | ADR-0002 |
| 013 | [Release build evidence 与 isolation](story-013-build-evidence.md) | Integration | Complete | ADR-0002 |

## Next Step

Run `/story-readiness production/epics/sys-persist/story-001-schema-ownership-manifest.md` before implementation.
