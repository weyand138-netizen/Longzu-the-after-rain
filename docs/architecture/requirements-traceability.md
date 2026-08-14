# Architecture Traceability Index

Last Updated: 2026-08-14
Engine: Ren'Py 8.5.3 / Python 3.12  
Mode: `/architecture-review full`

## Coverage Summary

- Total requirements: 18
- Covered: 11 (61.1%)
- Partial: 5 (27.8%)
- Current gaps: 0 (0%)
- Deferred to post-MVP: 2 (11.1%)

## Full Matrix

| TR-ID | GDD / System | Requirement | ADR Coverage | Status |
|---|---|---|---|---|
| TR-STATE-001 | five-axis-state.md / SYS-STATE | Schema 2, five axes, and ordered history share one rollback/save envelope | ADR-0002, ADR-0004, ADR-0005 | Covered |
| TR-STATE-002 | five-axis-state.md / SYS-STATE | Strict validation and one complete replacement assignment | ADR-0004 | Covered |
| TR-END-001 | deterministic-ending-resolution.md / SYS-ENDING | Deterministic total six-ending resolution without randomness | ADR-0001 | Covered |
| TR-END-002 | deterministic-ending-resolution.md / SYS-ENDING | Counterevidence, cause lineage, terminal compatibility, and resolver purity | ADR-0001, ADR-0005 | Covered |
| TR-CHOICE-001 | choice-and-causality-record.md / SYS-CHOICE | Every player-facing choice commits through SYS-STATE | ADR-0002, ADR-0005 | Covered |
| TR-CHOICE-002 | choice-and-causality-record.md / SYS-CHOICE | Exact reaction/payoff joins and terminal continuation witness coverage | ADR-0008 | Covered |
| TR-NAR-001 | seven-day-chapter-script.md / SYS-NARRATIVE | Seven-day chapter paths and six endings are valid and content-locked | ADR-0003 | Partial |
| TR-SAVE-001 | save-load-rollback.md / SYS-SAVE | Free save, load, and rollback remain supported | ADR-0002, ADR-0004 | Covered |
| TR-SAVE-002 | save-load-rollback.md / SYS-SAVE | Legacy, unsupported, and corrupt loads enter a blocking safe flow | ADR-0002, ADR-0005 | Covered |
| TR-PERSIST-001 | cross-playthrough-unlocks.md / SYS-PERSIST | Schema-v2 root, 12-leaf authority, epoch, settings, merge/reset, and flush | ADR-0002 | Covered |
| TR-PERSIST-002 | cross-playthrough-unlocks.md / SYS-PERSIST | Ending completion emits one durable completed-event boundary | ADR-0002, ADR-0006 | Covered |
| TR-ACH-001 | local-achievements.md / SYS-ACHIEVE | Eleven event-based achievements evaluate and persist independently and idempotently | ADR-0002 | Partial |
| TR-JOURNAL-001 | sys-journal.md / SYS-JOURNAL | Journal bundle/read model exposes chapters, memories, endings, and achievements | ADR-0003 | Partial |
| TR-ACCESS-001 | sys-access.md / SYS-ACCESS | Keyboard, scale, contrast, self-voicing, captions, and effect alternatives remain semantically equivalent | ADR-0002, ADR-0003 | Partial |
| TR-TENSION-001 | sys-tension.md / SYS-TENSION | Timeout maps to a canonical choice and does not alter ending rules | None; feature deferred | Deferred |
| TR-TENSION-002 | sys-tension.md / SYS-TENSION | Tension preference survives restart but not per-run rollback | Future ADR; feature deferred | Deferred |
| TR-TEST-001 | sys-test.md / SYS-TEST | Lint, pure logic, engine testcase, and gate evidence control hand-off | ADR-0007 partially covers release evidence | Partial |
| TR-BUILD-001 | sys-build.md / SYS-BUILD | Offline Windows package includes legal and integrity provenance | ADR-0007, with ADR-0003 asset boundary | Covered |

## Known Gaps

### Current P0 gaps

None. ADR-0008 closes the SYS-CHOICE/SYS-NARRATIVE content-lock, CFG, terminal-continuation, and witness boundary.

### Partial coverage

- `TR-NAR-001`: ADR-0008 supplies content-lock and path-enumeration architecture coverage; Day 1 must now supply the first production source/manifest/witness evidence.
- `TR-ACH-001`: define the complete achievement catalog/evaluator/backend boundary.
- `TR-JOURNAL-001`: define Journal bundle, read model, refresh, and error taxonomy.
- `TR-ACCESS-001`: define input equivalence, self-voicing, captions, and settings authority.
- `TR-TEST-001`: define evidence lifecycle, gate aggregation, and artifact ownership.

## Active Design Change Impacts

| Date | Change | TR-ID | ADR review | Status |
|---|---|---|---|---|
| 2026-08-14 | Extend the existing `rain_stops` epilogue after lights-out with a short years-later observer/note tail; preserve the 15-unit set and all ending/state contracts | `TR-NAR-001` | ADR-0003, ADR-0006, ADR-0008 — still valid | Design authorized for implementation; content-lock and human review remain downstream |

### Deferred

- `TR-TENSION-001` and `TR-TENSION-002` remain outside the current P0 Production gate.

## Superseded Requirements

None identified. Existing requirements retain their IDs and wording in the
initial registry.

## History

| Date | Coverage | Notes |
|---|---:|---|
| 2026-08-09 | 55.6% Covered; 27.8% Partial | Initial stable TR registry and full architecture review |
| 2026-08-10 | 61.1% Covered; 27.8% Partial | ADR-0008 accepted; no current P0 traceability gap |
| 2026-08-14 | 61.1% Covered; 27.8% Partial | Rain-stops epilogue design amendment recorded; no new TR-ID or canonical unit |
