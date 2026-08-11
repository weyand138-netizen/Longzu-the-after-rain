# Epic: SYS-ACHIEVE — Achievement Projection

> **Layer**: Feature (P0 core-production portfolio)  
> **GDD**: `design/gdd/local-achievements.md`  
> **Architecture Module**: SYS-ACHIEVE  
> **Status**: Ready  
> **Stories**: Deferred until Day 1 emits its first production completion event.

## Overview

Project independently evaluated, idempotent local achievements from approved completion events without exposing hidden metrics, deriving narrative truth, or becoming a second persistence owner.

## Governing ADRs

| ADR | Decision Summary | Engine Risk |
|---|---|---|
| ADR-0002 | Persistent boundary | High |
| ADR-0008 | Owner-approved narrative event bindings | High |
