# Story 002: Terminal Lifecycle and Completion Boundary

> **Epic**: SYS-ENDING — Terminal Narrative Closure
> **Status**: Complete
> **Layer**: Core
> **Type**: Integration
> **Estimate**: 3 days
> **Last Updated**: 2026-08-13

## Context

**GDD**: `design/gdd/deterministic-ending-resolution.md`
**Requirements**: `TR-END-002`, `TR-END-004`
**Governing ADRs**: ADR-0002, ADR-0004, ADR-0006, ADR-0008
**Engine**: Ren'Py 8.5.3 | **Risk**: High

SYS-ENDING owns the only Day 7 terminal handoff. Existing defaults do not
initialize or validate the required lifecycle and no adapter, entry commit, or
completion coordinator is wired. This story adds those frozen boundaries
without copying resolver logic into narrative code or bypassing SYS-PERSIST.

## Acceptance Criteria

- [x] The new-game/schema-2 entry initializes the exact sentinel, `Active`
  lifecycle, and pending state atomically; malformed lifecycle combinations
  fail through the approved safe boundary rather than silently defaulting.
- [x] `day7_resolve_ending` validates active state, builds one detached
  snapshot, calls the canonical resolver once, validates the exact six-entry
  map, records the pending ending ID, and jumps only to its mapped stable label.
- [x] Resolver/type/value/map/preflight errors remain `Active` and cause zero
  label, persistence, achievement, journal, or completion actions; a second
  request after entry raises the frozen already-committed error before resolve.
- [x] Each entry uses only `commit_ending_entry(expected_id)` as its first
  lifecycle operation. Each terminal node uses only
  `commit_ending_completion(ending_id, checkpoint)` after visible closure,
  creates the exact ADR-0006 event, applies the persistent membership through
  the existing coordinator once, and preserves duplicate replay idempotency.
- [x] Engine and integration tests prove rollback-owned lifecycle restoration,
  fixed one-to-one mapping, one entry transition, and one completion boundary
  per ending.

## Out of Scope

Resolver predicate changes, ending prose, new content facts, Day 7 prose,
terminal manifest enumeration, external assets, release, and stage promotion.

## QA Test Cases

- **AC-1/2:** Engine tests exercise fresh initialization, invalid state, each
  mapped pending ID, and resolver failure closure.
- **AC-3/4:** Integration tests assert call counts, persistent root membership,
  event fields, duplicate no-op, and rollback before/after completion.
- **AC-5:** Static scan rejects lifecycle/persistent writes outside owned
  helpers and verifies the six mapped target labels are real.

## Dependencies

- Depends on: Story 001 canonical resolver and existing SYS-PERSIST/SYS-SAVE
  coordinator contracts.
- Unlocks: Story 003 and Sprint 6 Day 7 authored handoff.

## Completion Notes

**Completed**: 2026-08-13
**Criteria**: Schema-2 initialization, one-snapshot/one-resolver handoff,
strict six-ID map, entry transition, ADR-0006 completion coordination, replay
idempotency, and safe-load validation are implemented. The valid active staged
pending-ID state is preserved; a completion event cannot exist before entry.

**Test evidence**: Focused terminal suite 6/6; Python 252/252; pinned Ren'Py
global suite 46/46 testcases and 405/405 assertions; `lint --compile`; and
`git diff --check` pass. Code review:
`production/qa/evidence/sprint-007-s7-02-code-review-2026-08-13.md`.
