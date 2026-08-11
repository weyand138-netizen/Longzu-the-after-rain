# Epic: SYS-ENDING — Terminal Narrative Closure

> **Layer**: Core  
> **GDD**: `design/gdd/deterministic-ending-resolution.md`  
> **Architecture Module**: SYS-ENDING  
> **Status**: Ready  
> **Stories**: Deferred until the first terminal narrative unit is scheduled.

## Overview

Preserve deterministic six-ending resolution and the sole terminal completion callsite. Endings receive locked narrative closure before ADR-0006 completion emission; they never infer results from presentation or persistent state.

## Governing ADRs

| ADR | Decision Summary | Engine Risk |
|---|---|---|
| ADR-0001 | Deterministic resolver | Low |
| ADR-0006 | Single completion-event boundary | High |
| ADR-0008 | Terminal continuation witnesses | High |
