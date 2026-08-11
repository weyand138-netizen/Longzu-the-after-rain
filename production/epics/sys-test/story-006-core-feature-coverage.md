# Story 006: Core/feature contract coverage

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

**ADR Governing Implementation**: ADR-0001: Deterministic Ending Resolution  
**Secondary ADRs**: ADR-0003, ADR-0004, ADR-0005, ADR-0006
**ADR Decision Summary**: SYS-TEST 验证 STATE、ENDING、CHOICE、NARRATIVE 的 owner manifests、pure resolver、CFG/DAG、reaction/payoff joins、terminal witnesses 与 completion event；产品语义仍由各 owner GDD/ADR 决定。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH integration  
**Engine Notes**: pure/static cases 与 Ren’Py-hosted cases 必须分别执行；production content-lock 与最大图输入缺失时保持 blocked。

**Control Manifest Rules (this layer)**:
- Required: resolver 只接受 detached inputs；production/test evidence 分离。
- Required: 每条 production route 同时有 pure 与 engine case，完整 CFG/terminal coverage exact-match。
- Forbidden: SYS-TEST 不得重定义 axis/token/priority/ending predicate。
- Guardrail: content-lock 缺口保持 `BLOCKED_INPUT`，不能被 isolated component PASS 掩盖。

---

## Acceptance Criteria

- [ ] `TEST-DOM-001`: SYS-STATE criteria 均有 current evidence，SYS-TEST 不重新定义轴/token/validation precedence。
- [ ] `TEST-DOM-002`: 六 canonical ending vectors、boundary mutants、completion event fixtures 验证唯一性、互斥性、purity/trace 与唯一 terminal completion node/event。
- [ ] `TEST-DOM-003`: SYS-CHOICE catalog、CFG/DAG、reaction/payoff/qualification joins 的 missing/duplicate/orphan/wrong-nullability/continuation negatives 逐案失败。
- [ ] `TEST-DOM-004`: SYS-NARRATIVE source graph、witness、oracle、control location、terminal witness 与 content hash exact 覆盖。
- [ ] `TEST-DOM-012`: 冻结 source/graph/catalog/maximum fixture 枚举全部合法 terminal paths；每条 path 恰映射 ending、terminal class、witness、payoff、summary。

## Implementation Notes

- 使用 owning manifests 与 current identity；测试不得注册 production choice 或替换 catalog。
- `TEST-DOM-010` SYS-TENSION timing suite 明确 post-MVP，不纳入当前 Story/P0 gate。
- source graph unresolved edge 或 production content-lock 缺失时只阻断受影响 integration/release scope。

## Out of Scope

- SYS-STATE/SYS-ENDING/SYS-CHOICE/SYS-NARRATIVE Epic：被测产品合同实现。
- Story 005：玩家盲测与主观 causal review。
- Story 007：foundation/presentation cross-system coverage。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: owner criteria; resolver vectors; CFG/DAG joins; terminal inventory; content-lock BLOCKED_INPUT.

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_test/core_feature_coverage_test.py` — owner criteria、resolver vectors、CFG/DAG、joins、terminal path enumeration 与 blocked input。

**Status**: [x] Created and passing — 2 integration tests

## Dependencies

- Depends on: Story 003, Story 004

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; contract vector, missing content-lock blocker, and integration gate behavior covered.
**Deviations**: Full production content-lock and Ren’Py-hosted terminal enumeration remain release-environment evidence.
**Test Evidence**: `tests/integration/sys_test/core_feature_coverage_test.py`
**Code Review**: Complete — APPROVED; blocked input cannot be masked by component PASS.
- Unlocks: Story 007, Story 008
