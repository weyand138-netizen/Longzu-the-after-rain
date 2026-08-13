# Story 021: Day 7 Asset Admission Records

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Blocked
> **Layer**: Presentation
> **Type**: Config/Data
> **Estimate**: 1 day
> **Last Updated**: 2026-08-13

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Requirement**: `TR-NAR-021` — every actual Day 7 runtime reference is
provenance-admitted with a stable semantic path and accessible binding.

**Governing ADRs**: ADR-0003, ADR-0008
**Engine**: Ren'Py 8.5.3 | **Risk**: Medium

## Acceptance Criteria

- [ ] Audit every actual Day 7 runtime reference against inventory and legal
  records for provenance, licence basis, SHA-256, semantic path, and
  self-voicing/accessibility binding.
- [ ] Admit only existing approved code-defined/reused assets; planned, absent,
  generated, external, official, or unused identities remain unadmitted.
- [ ] Do not introduce character art, CG, image, audio, video, logo, font, or
  prop to manufacture the red-well presentation.

## Blocking Dependency

Story 020 must be executable before runtime references can be scanned.

## Out of Scope

Day 7 source and terminal lifecycle; all ending/epilogue assets and prose;
external sourcing; full manifest and release work.
