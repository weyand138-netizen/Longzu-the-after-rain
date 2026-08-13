# Code Review: Sprint 7 Story 001 Canonical Ending Resolver

**Date**: 2026-08-13
**Review mode**: solo
**Story**: S7-01 / `TR-END-001`, `TR-END-003`

## Reviewed Surface

- `game/modules/ending_rules.py`
- `tests/test_ending_rules.py`
- `tests/integration/sys_save/restore_semantics_test.py`
- `design/gdd/five-axis-state.md` and `design/registry/entities.yaml`

## Findings and Resolution

| Severity | Finding | Resolution |
| --- | --- | --- |
| P1 (resolved) | The historical `axis_match_v1` vector encoded retired choice IDs, so it could not represent the current authoritative 54-choice witness. | With explicit owner approval, the active GDD vector and registry digest now use the canonical current witness contributors `prologue_read_note`, `day1_read_food_gesture`, and `day2_accept_alias`; fallback vector remains unchanged. |
| P1 (resolved) | Qualification failure causes initially omitted false source-fact identity, making distinct missing bindings collapse to one boolean-only explanation. | Frozen source-fact encoding now includes kind, stable source ID, truth, and contributor lineage; targeted tests prove distinct missing facts produce distinct cause IDs. |
| P2 (resolved) | Restore semantic coverage still called the retired axes-only resolver shape. | The test now constructs the exact detached schema-2 snapshot and exercises the same resolver contract as runtime integration. |

## Review Result

The resolver accepts only an exact detached schema-2 snapshot and replays every
supported choice through one immutable catalog before token, route-fact,
qualification, predicate, cause, and record construction stages. It imports no
Ren'Py store and owns no mutable game state. The compatibility wrapper makes
one canonical call and reads only `ending_id`.

The catalog retains the approved Day 5 sibling semantics: Golden Cage's
authoritative witness contains `day5_replace_erii_response` only, replace has
zero axis projection, and its `3/2/3/2/1` result is unchanged. No predicate,
priority, topology, or ending meaning was changed.

Automated review evidence: focused resolver suite 9/9; Python 246/246;
Ren'Py 8.5.3.26051504 global suite 45/45 testcases and 386/386 assertions;
isolated `lint --compile`; pinned-Python module compile; and `git diff --check`
all passed. The runtime implementation root is `game/`; no empty `src/`
directory was created.

## Verdict: APPROVED FOR S7-02
