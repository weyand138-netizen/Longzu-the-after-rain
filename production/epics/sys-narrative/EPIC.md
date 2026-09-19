# Epic: SYS-NARRATIVE — Seven-Day Content Production

> **Layer**: Feature (P0 core-production portfolio)  
> **GDD**: `design/gdd/seven-day-chapter-script.md`  
> **Architecture Module**: SYS-NARRATIVE  
> **Status**: Ready  
> **Stories**: 27 stories

## Overview

Produce the 15 canonical narrative units as player-safe Ren'Py content, beginning with Day 1. SYS-NARRATIVE owns prose, beat placement, source hashes, common-path truth approvals, and catalog inputs; it consumes canonical choices and never bypasses state, ending, persistence, or content-lock boundaries.

## Governing ADRs

| ADR | Decision Summary | Engine Risk |
|---|---|---|
| ADR-0003 | Content/presentation separation | Medium |
| ADR-0006 | Ending completion after player-visible closure | High |
| ADR-0008 | Content lock, CFG, joins, and witnesses | High |

## GDD Requirements

| TR-ID | Requirement | ADR Coverage |
|---|---|---|
| TR-NAR-001 | Seven-day chapter paths and endings are valid and content-locked | ADR-0003, ADR-0008 |
| TR-NAR-006 | Day 3 authored source, exact bindings, and player-safe source provenance | ADR-0003, ADR-0008 |
| TR-NAR-007 | Day 3 routes, accessibility evidence, and content-boundary validation | ADR-0003, ADR-0008 |
| TR-NAR-008 | Day 3 asset admission and semantic accessibility bindings | ADR-0003, ADR-0008 |
| TR-NAR-009 | Day 4 authored source, exact bindings, and player-safe source provenance | ADR-0003, ADR-0008, ADR-0006 |
| TR-NAR-010 | Day 4 routes, accessibility evidence, and content-boundary validation | ADR-0003, ADR-0008 |
| TR-NAR-011 | Day 4 asset admission and semantic accessibility bindings | ADR-0003, ADR-0008 |
| TR-NAR-012 | Day 5 authored source, derived route answer, and player-safe provenance | ADR-0003, ADR-0008, ADR-0006 |
| TR-NAR-013 | Day 5 asset admission and semantic accessibility bindings | ADR-0003, ADR-0008 |
| TR-NAR-014 | Day 5 routes, accessibility evidence, and content-boundary validation | ADR-0003, ADR-0008 |
| TR-NAR-015 | Day 5 story and evidence traceability | ADR-0003, ADR-0008 |
| TR-NAR-016 | Day 6 authored source, exact resource/cost/commitment bindings, and player-safe provenance | ADR-0003, ADR-0008, ADR-0006 |
| TR-NAR-017 | Day 6 asset admission and semantic accessibility bindings | ADR-0003, ADR-0008 |
| TR-NAR-018 | Day 6 routes, accessibility evidence, and content-boundary validation | ADR-0003, ADR-0008 |
| TR-NAR-019 | Day 6 story and evidence traceability | ADR-0003, ADR-0008 |
| TR-NAR-020 | Day 7 authored source and owned terminal handoff | ADR-0003, ADR-0006, ADR-0008 |
| TR-NAR-021 | Day 7 asset admission and semantic accessibility bindings | ADR-0003, ADR-0008 |
| TR-NAR-022 | Day 7 preservation, handoff, and accessibility validation | ADR-0003, ADR-0006, ADR-0008 |
| TR-NAR-023 | Day 7 story and evidence traceability | ADR-0003, ADR-0006, ADR-0008 |

## Stories

| # | Story | Type | Status | ADR |
|---|---|---|---|---|
| 001 | [Day 1 authored source and causal beats](story-001-day1-authored-source.md) | Config/Data | Complete | ADR-0008 |
| 002 | [Day 1 flow manifest and reachability witness](story-002-day1-flow-manifest.md) | Integration | Complete | ADR-0008, ADR-0009 |
| 003 | [Day 1 content validation and accessibility evidence](story-003-day1-content-validation.md) | Integration | Complete | ADR-0003, ADR-0008 |
| 004 | [Day 2 authored source and causal beats](story-004-day2-authored-source.md) | Config/Data | Complete | ADR-0008, ADR-0003 |
| 005 | [Day 2 content validation and accessibility evidence](story-005-day2-content-validation.md) | Integration | Complete | ADR-0003, ADR-0008 |
| 006 | [Day 3 authored source and causal bindings](story-006-day3-authored-source.md) | Integration | Complete | ADR-0008, ADR-0003, ADR-0006 |
| 007 | [Day 3 route, accessibility, and evidence validation](story-007-day3-content-validation.md) | Integration | Complete | ADR-0003, ADR-0008 |
| 008 | [Day 3 asset admission records](story-008-day3-asset-admission.md) | Config/Data | Complete | ADR-0003, ADR-0008 |
| 009 | [Day 4 authored source and causal bindings](story-009-day4-authored-source.md) | Config/Data | Complete | ADR-0008, ADR-0003, ADR-0006 |
| 010 | [Day 4 route, accessibility, and evidence validation](story-010-day4-content-validation.md) | Integration | Complete | ADR-0003, ADR-0008 |
| 011 | [Day 4 asset admission records](story-011-day4-asset-admission.md) | Config/Data | Complete | ADR-0003, ADR-0008 |
| 012 | [Day 5 authored source and derived route answer](story-012-day5-authored-source.md) | Config/Data | Complete | ADR-0008, ADR-0003, ADR-0006 |
| 013 | [Day 5 asset admission records](story-013-day5-asset-admission.md) | Config/Data | Complete | ADR-0003, ADR-0008 |
| 014 | [Day 5 route, accessibility, and evidence validation](story-014-day5-content-validation.md) | Integration | Complete | ADR-0003, ADR-0008 |
| 015 | [Day 5 story and evidence traceability](story-015-day5-traceability.md) | Config/Data | Complete | ADR-0003, ADR-0008 |
| 016 | [Day 6 authored source and guarded route commitment](story-016-day6-authored-source.md) | Config/Data | Complete | ADR-0008, ADR-0003, ADR-0006 |
| 017 | [Day 6 asset admission records](story-017-day6-asset-admission.md) | Config/Data | Complete | ADR-0003, ADR-0008 |
| 018 | [Day 6 route, accessibility, and evidence validation](story-018-day6-content-validation.md) | Integration | Complete | ADR-0003, ADR-0008 |
| 019 | [Day 6 story and evidence traceability](story-019-day6-traceability.md) | Config/Data | Complete | ADR-0003, ADR-0008 |
| 020 | [Day 7 authored source and resolver handoff](story-020-day7-authored-source.md) | Config/Data | Complete | ADR-0003, ADR-0006, ADR-0008 |
| 021 | [Day 7 asset admission records](story-021-day7-asset-admission.md) | Config/Data | Complete | ADR-0003, ADR-0008 |
| 022 | [Day 7 handoff, accessibility, and evidence validation](story-022-day7-content-validation.md) | Integration | Complete | ADR-0003, ADR-0006, ADR-0008 |
| 023 | [Day 7 story and evidence traceability](story-023-day7-traceability.md) | Config/Data | Complete | ADR-0003, ADR-0006, ADR-0008 |
| 024 | [Production end-to-end orchestrator](story-024-production-end-to-end-orchestrator.md) | Integration | Complete | ADR-0003, ADR-0006, ADR-0008 |
| 025 | [rain_stops years-later tail](story-025-rain-stops-years-later-tail.md) | Integration | Complete | ADR-0003, ADR-0006, ADR-0008 |
| 026 | [Prologue and Day 1–2 prose expansion](story-026-prologue-day1-day2-prose-expansion.md) | Content | Complete | ADR-0003, ADR-0008 |
| 027 | [Day 3–4 prose expansion](story-027-day3-day4-prose-expansion.md) | Content | Complete | ADR-0003, ADR-0008 |
| 028 | [Day 5–6 prose expansion](story-028-day5-day6-prose-expansion.md) | Content | Complete | ADR-0003, ADR-0008 |
| 029 | [Day 7, endings, and rain_stops prose expansion](story-029-day7-endings-prose-expansion.md) | Content | Complete | ADR-0003, ADR-0006, ADR-0008 |

Day 2 flow-manifest expansion is intentionally not a story in this batch:
ADR-0009 permits exactly the Day 1 partial artifact and blocks a partial Day 2
alias. A new accepted ADR is required before creating an incremental manifest
or terminal-witness story.
