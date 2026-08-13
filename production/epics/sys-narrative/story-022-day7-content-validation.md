# Story 022: Day 7 Handoff, Accessibility, and Evidence Validation

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Blocked
> **Layer**: Feature
> **Type**: Integration
> **Estimate**: 2 days
> **Last Updated**: 2026-08-13

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Requirement**: `TR-NAR-022` — Day 7 route and accessibility evidence proves
zero Day 7 state creation, one owned ending handoff, and failure-closed flow.

**Governing ADRs**: ADR-0003, ADR-0006, ADR-0008
**Engine**: Ren'Py 8.5.3 | **Risk**: High

## Acceptance Criteria

- [ ] Exercise all six canonical Day 1-6 histories through Day 7; each reaches
  its required scenes, preserves the exact prior snapshot/history, and calls
  the owned terminal handoff once.
- [ ] Prove Day 7 has zero axis, token, qualification, route-resource,
  persistence, achievement, and journal mutations before terminal ownership
  accepts the handoff.
- [ ] Inject resolver `TypeError` and `ValueError`; the flow remains Active,
  enters no label, and writes no persistent/achievement/journal result.
- [ ] Capture the causal-recall surface at 1280x720 keyboard-only
  silent/reduced-motion and 1.5x high-contrast/reduced-motion; require
  readable, focused, keyboard-operable text without quick-menu focus.

## Blocking Dependency

Stories 020 and 021 plus the owned executable SYS-ENDING adapter/labels are
required. This story must not supply a test-only terminal substitute.

## Out of Scope

Six ending content validation, epilogue validation, resolver semantics,
qualification enumeration, full-manifest work, external assets, release, and
stage changes.
