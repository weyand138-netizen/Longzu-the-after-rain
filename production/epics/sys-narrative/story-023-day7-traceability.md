# Story 023: Day 7 Story and Evidence Traceability

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Blocked
> **Layer**: Feature
> **Type**: Config/Data
> **Estimate**: 1 day
> **Last Updated**: 2026-08-13

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Requirement**: `TR-NAR-023` — Day 7 stories, source, assets, terminal-
handoff tests, evidence, review, smoke, and QA identify one verified generation.

**Governing ADRs**: ADR-0003, ADR-0006, ADR-0008
**Engine**: Ren'Py 8.5.3 | **Risk**: Medium

## Acceptance Criteria

- [ ] Create a link matrix for Stories 020-022, Day 7 source hash, asset/legal
  records, terminal handoff tests, captures, code review, smoke, and QA sign-
  off.
- [ ] Verify Epic, story, and sprint status agree without claiming six ending,
  epilogue, full-manifest, release, or stage delivery.
- [ ] Explicitly state the Ren'Py implementation root is `game/`; no empty
  `src/` directory is created to manufacture gate compliance.

## Blocking Dependency

Stories 020-022 must be Complete. The traceability record cannot make a
blocked terminal handoff appear verified.
