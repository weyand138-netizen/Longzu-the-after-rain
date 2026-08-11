# Story 010: External evidence 完整性与人工 adjudication

> **Epic**: SYS-TEST — 自动化验证
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Integration
> **Estimate**: 3 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/sys-test.md`  
**Requirement**: `TR-TEST-001`

**ADR Governing Implementation**: ADR-0003: Content and Presentation Boundary  
**Secondary ADRs**: ADR-0007, ADR-0002
**ADR Decision Summary**: HUMAN、PLAYTEST、VISUAL、REVIEW evidence 是外部输入，必须有 rubric、参与者/reviewer、环境、raw response/capture、分组与 adjudication 的完整 provenance；SYS-TEST 只验证完整性，不从分数/多数票自动生成主观 PASS。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: MEDIUM/HIGH integration  
**Engine Notes**: visual/TTS/playtest captures 必须绑定目标 build/environment；人工 adjudication 由批准 reviewer 提供。

**Control Manifest Rules (this layer)**:
- Required: 外部 evidence 使用稳定 ID、source hash、environment 与 raw artifacts。
- Required: 主观结论必须由 approved rubric/reviewer adjudication 提供。
- Forbidden: 测试媒体不得进入 release resources、save、persistent 或 player logs。
- Guardrail: 缺批准 PASS 裁定时 criterion 保持 `BLOCKED_INPUT`。

---

## Acceptance Criteria

- [ ] `TEST-EXT-001`: HUMAN、PLAYTEST、VISUAL、REVIEW artifact 具备 rubric、参与者/reviewer、环境、raw responses/captures、分组结果、adjudication 与 hash。
- [ ] `TEST-EXT-002`: artifact 完整但没有 approved human PASS adjudication 时，系统不得从 score、majority 或 screenshot 自动生成 PASS，criterion 保持 blocked。
- [ ] `TEST-FANTASY-004`～`005`: blind playtest 与六 ending witness review 的主观输入、reviewer/adjudication 与 protocol identity 可追踪。

## Implementation Notes

- 只验证 evidence completeness、identity 与 adjudication provenance，不执行内容价值判断。
- capture/transcript 必须使用 test-only path，不能被 production dependency closure 发现。
-人工证据的缺失只阻断依赖该证据的 criterion，不阻断可独立运行的 FAST scope。

## Out of Scope

- Story 005：player-critical flow 的 engine trace。
- Story 009：benchmark protocol。
- Story 011：bundle-level traceability。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: external artifact completeness/hashes/rubric/reviewer/environment; approved PASS requirement; test-only media isolation.

## Test Evidence

**Story Type**: Integration  
**Required evidence**:
- `tests/integration/sys_test/external_evidence_test.py` — artifact completeness、hash、rubric、adjudication、blocked input 与 test-only media isolation。

**Status**: [x] Created and passing — 2 integration tests

## Dependencies

- Depends on: Story 003, Story 005

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 3/3 passing; external artifact completeness, approved adjudication, and test-only media rejection covered.
**Deviations**: No real human/visual evidence bundle exists locally; missing adjudication remains BLOCKED_INPUT by design.
**Test Evidence**: `tests/integration/sys_test/external_evidence_test.py`
**Code Review**: Complete — APPROVED; scores/screenshots cannot infer human PASS.
- Unlocks: Story 004, Story 011
