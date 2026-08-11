# Epic: SYS-SAVE — 存档、读档与回退

> **Layer**: Foundation
> **GDD**: design/gdd/save-load-rollback.md
> **Architecture Module**: SYS-SAVE
> **Status**: Complete
> **Stories**: Not yet created — run `/create-stories sys-save`

## Overview

实现 Ren’Py 原生存档、读档、快速存读档、自动存档与自由回退合同。Epic 负责把控制位置、save-contract/catalog generation、schema 2 semantic state、ending lifecycle 及 rollback-owned per-run 状态恢复到同一一致时点；对旧版、不支持、损坏及内部恢复失败执行严格分类，并将不安全恢复导向只能返回主菜单或明确开始新游戏的阻断安全流程。SYS-SAVE 不拥有 persistent 数据、结局/成就逻辑或第二套 reaction/payoff 去重状态。

## Governing ADRs

| ADR | Decision Summary | Engine Risk |
|-----|------------------|-------------|
| ADR-0002: Rollback and Persistence Boundary | Ren’Py 原生存档是 per-run 主存档；rollback-owned 状态与 persistent 数据严格分界；不兼容加载进入阻断安全流程。 | HIGH |
| ADR-0004: Semantic Ending Snapshot and Rollback State Envelope | schema 2 状态 envelope、严格验证、detached snapshot 与 imported Python 边界保持一致。 | HIGH |
| ADR-0005: Counterevidence Ledger and Detectable State Initialization | 使用可检测的 `None` 默认值、显式新游戏初始化和不可返回 loaded scene 的安全恢复流程。 | HIGH |
| ADR-0006: Ending Completion Boundary | ending completion event 属于 rollback-owned 状态；完成前后存档、读档与回退必须保持边界语义。 | HIGH |

## GDD Requirements

| TR-ID | Requirement | ADR Coverage |
|-------|-------------|--------------|
| TR-SAVE-001 | Free save, load, and rollback remain supported | ADR-0002, ADR-0004 ✓ |
| TR-SAVE-002 | Legacy, unsupported, and corrupt loads enter a blocking safe flow | ADR-0002, ADR-0005 ✓ |

## Definition of Done

This epic is complete when:

- All stories are implemented, reviewed, and closed via `/story-done`
- All acceptance criteria from `design/gdd/save-load-rollback.md` are verified
- All Logic and Integration stories have passing test files in `tests/`
- All Visual/Feel and UI stories have evidence docs with sign-off in `production/qa/evidence/`

## Known Gates

- SYS-NARRATIVE production control-location catalog and source-hash mappings must be frozen before the production compatibility catalog is locked.
- SYS-CHOICE checkpoint fixtures must map many-to-one onto SYS-SAVE production locations without becoming runtime state.
- Ren’Py 8.5.3 save/load/rollback and engine-control recovery behavior remain HIGH-risk implementation verification gates.
- The active Control Manifest is version `2026-08-04.1`; its ADR coverage must be synchronized with ADR-0006/0007 before implementation hand-off.

## Stories

| # | Story | Type | Status | ADR |
|---|-------|------|--------|-----|
| 001 | [Save 写入、轮换与原子完整性](story-001-save-write-atomicity.md) | Integration | Complete | ADR-0002 |
| 002 | [读档预检与兼容性分类](story-002-load-classification.md) | Integration | Complete | ADR-0005 |
| 003 | [Checkpoint 与控制位置目录](story-003-control-location-catalog.md) | Integration | Complete | ADR-0004 |
| 004 | [四类恢复点语义与回退](story-004-restore-semantics.md) | Integration | Complete | ADR-0002 |
| 005 | [Ending completion 存档边界](story-005-ending-completion-restore.md) | Integration | Complete | ADR-0006 |
| 006 | [Action gates 与操作互斥](story-006-action-gates-mutex.md) | Logic | Complete | ADR-0002 |
| 007 | [Root blocking safe flow 与新游戏出口](story-007-blocking-safe-flow.md) | Integration | Complete | ADR-0005 |
| 008 | [Journal 安全入口与 recovery 抢占](story-008-journal-recovery-gate.md) | Integration | Complete | ADR-0002 |
| 009 | [Persistent ownership 与恢复不变性](story-009-persistent-boundary.md) | Integration | Complete | ADR-0002 |
| 010 | [Slot UI、metadata 与无障碍路径](story-010-save-load-ui-accessibility.md) | UI | Complete | ADR-0002 |
| 011 | [Save/load 性能协议与预算](story-011-save-load-performance.md) | Integration | Complete | ADR-0002 |
| 012 | [Production catalog freeze 与 release evidence](story-012-build-evidence-boundary.md) | Integration | Complete | ADR-0007 |

## Next Step

Run `/story-readiness production/epics/sys-save/story-001-save-write-atomicity.md` before implementation.
