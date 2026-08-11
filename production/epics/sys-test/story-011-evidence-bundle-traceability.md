# Story 011: Evidence bundle 与 registry traceability

> **Epic**: SYS-TEST — 自动化验证
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Logic
> **Estimate**: 4 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/sys-test.md`  
**Requirement**: `TR-TEST-001` — Partial ADR coverage; evidence-lifecycle ADR remains a required architecture gate

**ADR Governing Implementation**: ADR-0007: SYS-BUILD Contract Closure and Release Identity  
**Secondary ADRs**: ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0005, ADR-0006
**ADR Decision Summary**: evidence bundle 必须是同世代、content-addressed、可从 manifest 追踪到 owner contract/source/catalog/fixture/runner/environment/raw output 的集合。当前架构审查要求额外的 SYS-TEST evidence-lifecycle ADR；该 ADR 尚不存在，因此完整 hand-off 仍为 `BLOCKED_INPUT`。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: bundle 只消费已验证 runner/artifacts；任何 source/catalog/runner/environment/archive hash 改变都需要新 run。

**Control Manifest Rules (this layer)**:
- Required: current artifact、完整 SHA-256、同一 identity generation 与 raw output index。
- Required: 每个 `referenced_by: SYS-TEST` registry fact 解析到 criterion 或 owner-approved external mapping。
- Forbidden: 不得跨世代拼接 current/stale PASS，不得只输出 summary 无原始产物。
- Guardrail: unresolved blocker、missing/stale artifact、错误 owner 或值漂移不得关闭 gate。

---

## Acceptance Criteria

- [ ] `TEST-EVID-001`: manifest-derived unique ID 集合与 GDD criteria exact-match，无缺失、重复、额外 ID。
- [ ] `TEST-EVID-002`: 每个 criterion artifact 的 source/catalog/config/fixture/runner/environment/raw output 引用存在、SHA-256 匹配且可从 bundle index 定位。
- [ ] `TEST-EVID-003`: 多证据 criterion 的全部 artifacts 属于同一冻结 identity generation，跨世代拼接固定失败。
- [ ] `TEST-EVID-004`: bundle 同时存在 current/stale PASS 时只读取 current，stale count>0 使 required gate 失败。
- [ ] `TEST-EVID-005`: failure/blocking summary 含稳定 finding ID、case/assertion、raw artifact path 与 owner contract，不接受空泛“测试失败”。
- [ ] `TEST-EVID-006`: Entity Registry 所有 `referenced_by: SYS-TEST` 条目均映射到 criterion 或 approved external mapping，未映射/错误 owner/value drift 为 0。
- [ ] `TR-TEST-001` hand-off：在 evidence-lifecycle ADR、test setup 与完整 current bundle 缺失时，implementation/release 结果保持 `BLOCKED_INPUT`，不得宣称 unconditional PASS。

## Implementation Notes

- bundle 由 manifest 派生 criterion 集合，不使用手填总数；当前 SYS-PERSIST 的 60 criterion bundle 与其他 domain bundle 均需同世代。
- current/stale、failure/blocker、owner、raw output 路径写入可读 Markdown 摘要与 machine-readable index。
- 先补 evidence-lifecycle ADR、`tests/unit/`、`tests/integration/` 与 CI workflow，再将本 Story 作为 hand-off gate。

## Out of Scope

- Story 001：criterion manifest 基础结构。
- Story 004：gate verdict aggregation。
- `/test-setup`：测试目录与 CI scaffold。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: manifest-derived IDs; source/catalog/fixture/runner/environment/raw-output hashes; generation/stale blocking; failure IDs/index.

## Test Evidence

**Story Type**: Logic  
**Required evidence**:
- `tests/unit/sys_test/evidence_bundle_traceability_test.py` — manifest-derived IDs、hash/index、generation、stale、failure summary、registry mapping 与 blocked input。

**Status**: [x] Created and passing — 2 unit tests

## Dependencies

- Depends on: Story 001, Story 002, Story 004, Story 008, Story 009, Story 010

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 6/6 passing; manifest-derived IDs, content-addressed traceability, generation/stale blocking, and failure summary covered.
**Deviations**: No complete current production evidence bundle exists locally; the bundle API correctly remains BLOCKED_INPUT until supplied.
**Test Evidence**: `tests/unit/sys_test/evidence_bundle_traceability_test.py`
**Code Review**: Complete — APPROVED; cross-generation and stale evidence cannot be composed.
- Unlocks: None
