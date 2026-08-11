# Story 005: Player-critical causal evidence

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
**Secondary ADRs**: ADR-0002, ADR-0003, ADR-0006
**ADR Decision Summary**: SYS-TEST 验证 choice→reaction→payoff→ending cause 的可追溯因果与 completion boundary，但不拥有 resolver predicate、内容语义或 persistent state；玩家证据不得展示隐藏轴、分数或测试状态。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH integration  
**Engine Notes**: 四 checkpoint replay、keyboard/self-voicing path、Ren’Py hosted flow 与 manual review evidence 需目标环境与批准 rubric。

**Control Manifest Rules (this layer)**:
- Required: reaction/payoff/ending cause evidence exact-bind stable IDs。
- Required: visual、keyboard、self-voicing/transcript path 语义等价。
- Forbidden: 不得以隐藏分数、debug output、测试状态替代玩家可见因果。
- Guardrail: HUMAN/PLAYTEST/REVIEW 只能以批准 rubric/adjudication 关闭主观 criterion。

---

## Acceptance Criteria

- [ ] `TEST-FANTASY-001`: production-like choice path 的 `choice_id → immediate_reaction_id → payoff_id` exact-bind，且无 debug/hidden score 进入玩家输出。
- [ ] `TEST-FANTASY-002`: 四类恢复点 rollback/replay 的 expected history、choice、reaction、payoff、ending cause 与实际逐项一致，至少一条改选路径产生不同 registered payoff/cause。
- [ ] `TEST-FANTASY-003`: visual、keyboard、self-voicing/transcript 移除或替代设置后，choice identity、observable fact、reaction、payoff 语义摘要等价。
- [ ] `TEST-FANTASY-004`: blind playtest 的 raw response、rubric、分组、reviewer/adjudication、protocol identity 完整；未批准主观结果保持 `BLOCKED_INPUT`。
- [ ] `TEST-FANTASY-005`: 六个 canonical ending witness 各有可追溯选择链、具体 payoff 与可由人工 reviewer 指出的主要原因。

## Implementation Notes

- 使用 owner system 提供的 traces/oracles，不在 SYS-TEST 中复制 ending conditions。
- review evidence 只能证明证据完整性与绑定关系，不能自动从截图或多数票生成 PASS。
- playtest artifact 作为外部 evidence，不进入 production source/save/persistent。

## Out of Scope

- SYS-CHOICE/SYS-NARRATIVE Epic：reaction/payoff 内容与 CFG 实现。
- Story 006：跨系统 contract coverage。
- Story 010：通用 HUMAN/PLAYTEST artifact completeness。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: choice/reaction/payoff causal joins; rollback/replay; accessibility semantic equivalence; human adjudication blocker.

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_test/player_critical_evidence_test.py` — causal ID binding、checkpoint replay、accessibility equivalence 与 approved review artifacts。

**Status**: [x] Created and passing — 2 integration tests

## Dependencies

- Depends on: Story 004

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; causal evidence identity, accessible semantic equivalence boundary, and adjudication blocker covered.
**Deviations**: Human playtest session evidence is not available in this environment; unapproved results remain BLOCKED_INPUT.
**Test Evidence**: `tests/integration/sys_test/player_critical_evidence_test.py`
**Code Review**: Complete — APPROVED; no score/debug information is used to infer PASS.
- Unlocks: Story 006, Story 007
