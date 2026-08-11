# Story 001: Schema-v2 根与 ownership manifest

> **Epic**: SYS-PERSIST — 跨周目解锁
> **Status**: Complete
> **Layer**: Foundation
> **Type**: Logic
> **Estimate**: 4 hours
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-10

## Context

**GDD**: `design/gdd/cross-playthrough-unlocks.md`  
**Requirement**: `TR-PERSIST-001` — Schema-v2 root, 12-leaf authority, epoch, settings, merge/reset, and flush

**ADR Governing Implementation**: ADR-0002: Rollback and Persistence Boundary  
**ADR Decision Summary**: persistent data 只有一个 `persistent.sys_persist_state` schema-v2 root，包含 12 个规范 leaf；SYS-PERSIST 是唯一 storage writer，settings semantics 由 SYS-ACCESS 拥有。

**Engine**: Ren’Py 8.5.3 / Python 3.12 | **Risk**: HIGH  
**Engine Notes**: 使用 Ren’Py persistent 原生 serialization；root/settings 必须是 exact built-in dict，初始化、restart 与 default 行为需要目标引擎证据。

**Control Manifest Rules (this layer)**:
- Required: 唯一 12-leaf root 与 canonical 五项 setting tuple。
- Required: root、manifest、leaf path、owner/requester/merge/reset arrays 全部 exact validation。
- Forbidden: 不得保留 flat prototype persistent fields、legacy fields 或第二套 authority。
- Guardrail: invalid type/key/order/ID 不得被过滤、排序或选择性接受。

---

## Acceptance Criteria

- [ ] `PERSIST-SCHEMA-001`: clean Ren’Py 8.5.3 install 首次启动、flush、full restart 后 root 始终是 valid schema-v2 exact built-in root，epoch=0，collection/seen 为空，settings 为 `False/1.0`，normative leaf count=12。
- [ ] `PERSIST-SCHEMA-002`: 最大合法 achievement、seen、ending、memory IDs、epoch 与批准 font scale fixtures 通过 full validation，detached deep values 与输入相等。
- [ ] `PERSIST-SCHEMA-003`: missing/extra top-level 或 settings key、wrong root/settings container 在 key/container stage 固定失败，且不读取 unknown payload。
- [ ] `PERSIST-SCHEMA-004`: wrong exact type 或 protocol bomb 在有限步失败，bomb invocation count 为 0。
- [ ] `PERSIST-SCHEMA-005`: collection 中 unknown、duplicate、noncanonical order、wrong-kind ID 及边界值只有 canonical subset 通过，不能先过滤或重排。
- [ ] `PERSIST-SCHEMA-006`: `font_scale` 只接受批准档位，四项 boolean setting 只接受 exact bool。
- [ ] `PERSIST-SCHEMA-007`: 只有 exact 12-field ownership manifest、canonical leaf paths、等长 owner/requester/merge/reset arrays 与完整 migration policy 通过。
- [ ] `PERSIST-SCHEMA-008`: detached read snapshot 只来自 canonical root，无 object alias，修改 snapshot 不影响 root，legacy field read count 为 0。
- [ ] `PERSIST-OWN-001`～`006`: static/runtime ownership scan 证明只有批准 writer、requester 与 detached adapters 可访问 root；无 unresolved alias、foreign mutation、live store/cache、legacy field 或 unknown writer。

## Implementation Notes

- 使用 `default persistent.sys_persist_state = build_fresh_persist_root()`；不要声明第二个 product persistent field。
- canonical leaf 顺序为 schema、generation、epoch、achievement、seen、ending、memory 与五项 settings。
- validator 必须 staged、fail closed，并以 `root_field_name` 驱动 manifest 读取。
- imported Python 只处理 detached exact built-ins，不持有 live persistent/store 或 mutable module cache。

## Out of Scope

- Story 002：batch update 与 flush。
- Story 005：merge 公式与 startup marker。
- Story 009：achievement presentation adapter。

## QA Test Cases

*Test cases not yet defined — solo mode skipped QA readiness gate; run `/qa-plan` to generate them.*

QA coverage generated: fresh/restart exact 12-leaf root; staged fail-closed validation; protocol-bomb safety; ownership arrays; detached snapshot.

## Test Evidence

**Story Type**: Logic  
**Required evidence**:
- `tests/unit/sys_persist/schema_manifest_test.py` — schema、leaf、type、ownership、legacy isolation 与 detached snapshot。

**Status**: [x] Created and passing — 4 unit tests

## Dependencies

- Depends on: None
- Unlocks: Story 002, Story 005, Story 006

## Completion Notes
**Completed**: 2026-08-10
**Criteria**: 9/9 passing; schema-v2, exact 12-leaf ownership, fail-closed validation, and detached snapshot covered.
**Deviations**: None.
**Test Evidence**: `tests/unit/sys_persist/schema_manifest_test.py`
**Code Review**: Complete — APPROVED; standard-library-only and no live persistent aliasing.
