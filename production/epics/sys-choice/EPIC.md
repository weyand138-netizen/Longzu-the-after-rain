# Epic: SYS-CHOICE — Canonical Choice Flow

> **Layer**: Feature (P0 core-production portfolio)  
> **GDD**: `design/gdd/choice-and-causality-record.md`  
> **Architecture Module**: SYS-CHOICE  
> **Status**: Ready  
> **Stories**: Deferred until a narrative unit requires a new canonical choice seam.

## Overview

Own canonical player-choice records, commit order, exact reaction/payoff bindings, and the scanner output consumed by the narrative flow manifest. It never authors prose, persistent state, ending selection, or player-facing score feedback.

## Governing ADRs

| ADR | Decision Summary | Engine Risk |
|---|---|---|
| ADR-0002 | Rollback-owned state boundary | High |
| ADR-0005 | Detectable initialization and counterevidence | High |
| ADR-0008 | Exact joins, CFG, and terminal witnesses | High |

## GDD Requirements

| TR-ID | Requirement | ADR Coverage |
|---|---|---|
| TR-CHOICE-001 | Choices commit through SYS-STATE | ADR-0002, ADR-0005 |
| TR-CHOICE-002 | Exact reaction/payoff and terminal witnesses | ADR-0008 |
