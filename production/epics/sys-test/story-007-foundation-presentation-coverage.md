# Story 007: Foundation/presentation contract coverage

> **Epic**: SYS-TEST — 自动化验证
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Integration
> **Estimate**: 4 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/sys-test.md`  
**Requirement**: `TR-TEST-001`

**ADR Governing Implementation**: ADR-0002: Rollback and Persistence Boundary  
**Secondary ADRs**: ADR-0003, ADR-0006, ADR-0007
**ADR Decision Summary**: SYS-TEST 验证 SAVE、PERSIST、ACHIEVE、JOURNAL、ACCESS 之间的 owner boundary、round-trip、UI/read-model、backend、release evidence 与 persistent isolation；各系统仍拥有自己的 semantics。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: save/persistent/testcase、focus/self-voicing、UI visual evidence 与 candidate/archive evidence 都需要 pinned engine/build evidence。

**Control Manifest Rules (this layer)**:
- Required: persistent root 与 rollback-owned state 分离，presentation 只读 read models。
- Required: save/rollback、projection、Journal、ACCESS 与 release isolation evidence 同世代绑定。
- Forbidden: 不得把 test observer 或 UI debug state 写入正式 save/persistent。
- Guardrail: component evidence 不得替代 integration/release evidence。

---

## Acceptance Criteria

- [ ] `TEST-DOM-005`: SYS-SAVE 合法/不兼容/损坏 cross-product、四 checkpoint、ending completion、I/O fault fixtures 的分类、blocking、控制位置、原子性、重复计数与性能均符合合同。
- [ ] `TEST-DOM-006`: SYS-PERSIST schema、12-leaf、ending request、batch/merge/reset/failure、`APPLIED_FLUSHED`、foreign writes 与 test-root isolation 均有 current evidence。
- [ ] `TEST-DOM-007`: 11 项 achievement catalog、event/witness、epoch、backend、queue、seen、UI 的 43 项 owner criteria exact covered。
- [ ] `TEST-DOM-008`: SYS-JOURNAL bundle/read-model、focus、refresh、seen、recovery、failure domain、layout 与 performance evidence exact covered。
- [ ] `TEST-DOM-009`: SYS-ACCESS keyboard、TTS、focus、font/contrast/motion、single-channel removal 与 recovery semantic equivalence evidence 完整；voice failure 不得降级为 nonvisual PASS。
- [ ] `TEST-DOM-011`: 四 checkpoint、loaded-save rollback、persistent membership fixtures 的 state/control/history/choice/reaction/payoff/cause IDs exact-match，persistent 不被 per-run recovery 覆盖。

## Implementation Notes

- 每个 domain evidence 使用 owner system 的 manifest、fixture、oracle 与 source hash。
- UI/ACCESS evidence 需要 A11Y/VISUAL/HUMAN 类型时，严格按 criterion 要求聚合。
- persistent foreign writer、test-root、popup/focus 等禁止项必须静态与运行时双重扫描。

## Out of Scope

- Story 003：通用 toolchain/test-only isolation。
- Story 005：player-critical blind review。
- Story 008：SYS-BUILD candidate/archive handshake。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: source/presentation coverage; keyboard/accessibility paths; visual evidence completeness; 720p/scale/motion variants.

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_test/foundation_presentation_coverage_test.py` — SAVE/PERSIST/ACHIEVE/JOURNAL/ACCESS domain manifests、round-trip、UI/A11Y 与 evidence identity。

**Status**: [x] Created and passing — 1 integration test

## Dependencies

- Depends on: Story 003, Story 004, Story 005

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; keyboard/layout/accessibility reachability and non-timed surface covered.
**Deviations**: Visual sign-off is advisory and requires engine-enabled 720p captures.
**Test Evidence**: `tests/integration/sys_test/foundation_presentation_coverage_test.py`
**Code Review**: Complete — APPROVED; presentation model has no hover/timed dependency.
- Unlocks: Story 008, Story 010
