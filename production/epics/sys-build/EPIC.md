# Epic: SYS-BUILD — Content Manifest and Provenance

> **Layer**: Platform (P0 core-production portfolio)  
> **GDD**: `design/gdd/sys-build.md`  
> **Architecture Module**: SYS-BUILD  
> **Status**: Ready  
> **Stories**: Deferred until the Day 1 flow manifest exists.

## Overview

Validate the canonical 15-unit source closure, owner hashes, catalog bundle, legal admission, and test-only isolation before packaging. SYS-BUILD validates inputs and never rewrites content IDs, rank, truth approvals, or copy.

## Governing ADRs

| ADR | Decision Summary | Engine Risk |
|---|---|---|
| ADR-0007 | Candidate/release identity and evidence binding | High |
| ADR-0008 | Narrative flow manifest ownership and validation | High |
