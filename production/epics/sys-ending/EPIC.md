# Epic: SYS-ENDING — Terminal Narrative Closure

> **Layer**: Core  
> **GDD**: `design/gdd/deterministic-ending-resolution.md`  
> **Architecture Module**: SYS-ENDING  
> **Status**: Complete
> **Stories**: 4

## Overview

Preserve deterministic six-ending resolution and the sole terminal completion callsite. Endings receive locked narrative closure before ADR-0006 completion emission; they never infer results from presentation or persistent state.

## Sprint 7 Delivery Scope

Sprint 7 closes the already-approved terminal contracts that block the Day 7
handoff. It implements the schema-2, ordered-history resolver record; the sole
Day 7 lifecycle and completion boundaries; the six fixed ending labels; and the
approved `rain_stops` arcade epilogue. It does not alter GDD predicates,
priority, route qualifications, ending meanings, terminal manifest scope,
release work, or project stage.

| Story | Requirement | Status |
|---|---|---|
| [Story 001](story-001-canonical-ending-resolution.md) | `TR-END-001`, `TR-END-003` — deterministic schema-2 history replay, folds, qualification predicates, and immutable record | Complete |
| [Story 002](story-002-terminal-lifecycle-and-completion.md) | `TR-END-002`, `TR-END-004` — owned Day 7 resolver adapter, entry mapping, and ADR-0006 completion boundary | Complete |
| [Story 003](story-003-six-endings-and-rain-epilogue.md) | `TR-END-005` — six fixed closures and the true-ending arcade epilogue | Complete |
| [Story 004](story-004-terminal-validation-and-traceability.md) | `TR-END-006` — terminal contract, accessibility, evidence, and traceability validation | Complete |

## Governing ADRs

| ADR | Decision Summary | Engine Risk |
|---|---|---|
| ADR-0001 | Deterministic resolver | Low |
| ADR-0006 | Single completion-event boundary | High |
| ADR-0008 | Terminal continuation witnesses | High |
