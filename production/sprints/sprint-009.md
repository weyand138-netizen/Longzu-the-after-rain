# Sprint 009 — 2026-08-14 to 2026-08-16

## Sprint Goal

Expand the Prologue and Day 1–2 prose toward the authored-length target while
preserving every stable choice, state, route and ending contract.

## Capacity

- Total days: 3
- Review mode: solo
- Asset scope: none

## Tasks

| ID | Task | Owner | Est. Days | Dependency | Acceptance |
|---|---|---|---:|---|---|
| S9-01 | Story 026 — Prologue and Day 1–2 prose expansion | Andwey | 3 | Story 025 complete | prose-only additions; focused/full QA pass |

## Scope Check

**Verdict**: PASS — only existing Prologue/Day 1–2 labels and direct evidence
are in scope. No choice, route, ending, hidden rule, canonical unit or asset
scope may be added.

## QA Plan

`production/qa/qa-plan-sprint-009-2026-08-14.md`

## Risks

- Copy additions accidentally disclose internal state: scan all player-facing
  lines and review against ADR-0003/0008.
- Prose edit disturbs a control boundary: exact choice/control signature test.
- Historical source evidence becomes stale: content-lock v3 and focused hash
  assertion.

## Definition of Done

- [x] Story readiness, dev, review, story-done, smoke and team QA complete.
- [x] Full automated chain passes; manual playtest and narrative sign-off stay
  NOT RUN.
- [x] Local close commit created; no `production/stage.txt` or asset directory
  changed.
