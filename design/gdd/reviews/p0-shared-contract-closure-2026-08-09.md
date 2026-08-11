# P0 Shared-Contract Closure Matrix

Date: 2026-08-09  
Source: `design/gdd/gdd-cross-review-2026-08-09.md`  
Scope: C-01, C-02, C-05, and P1 SYS-TENSION deferral only  
Review mode: targeted closure; no new full review started

| Finding | Closure decision | Synchronized contract | Evidence / affected artifacts | Status |
|---|---|---|---|---|
| C-01 | SYS-PERSIST schema-v2 uses one authoritative 12-leaf manifest and five-setting tuple. Normative legacy leaf-count authority wording is removed; legacy development roots are incompatible fixtures only. | `leaf_field_count=12`; all twelve leaves and five settings are invariant across save/load/rollback/new game. | `design/gdd/cross-playthrough-unlocks.md`; `design/gdd/systems-index.md`; `design/gdd/sys-access.md`; `design/gdd/save-load-rollback.md`; `design/gdd/sys-test.md`; `design/registry/entities.yaml`; `docs/architecture/adr-0002-rollback-and-persistence-boundary.md`; `docs/architecture/architecture.md` | CLOSED |
| C-02 | SYS-ENDING solely owns `commit_ending_completion`. Each ending label has one terminal completion node after final narration/player-visible closure and before exit/return. The rollback-owned `ending_completion_event_record` is emitted once and consumed by the single persistence checkpoint coordinator. | `completed_event_id=ending_completed:{ending_id}`; pre-completion request/assignment/flush counts are `0`; `APPLIED_FLUSHED` adds canonical ending membership; rollback restores run lifecycle/event/control state without removing flushed membership; replay returns `DUPLICATE_NOOP`. | `docs/architecture/adr-0006-ending-completion-boundary.md`; ADR-0001/0002/0004/0005 amendments; `design/gdd/deterministic-ending-resolution.md`; `design/gdd/cross-playthrough-unlocks.md`; `design/gdd/seven-day-chapter-script.md`; `design/gdd/save-load-rollback.md`; `design/gdd/sys-test.md`; `design/registry/entities.yaml` | CLOSED |
| C-05 | Public persistence result contract uses `APPLIED_FLUSHED` only. No second public success name is accepted by consumers, fixtures, Registry or evidence. | `PersistDurableResult.status` public success value is `APPLIED_FLUSHED`; notification/projection eligibility uses that value. | `design/gdd/cross-playthrough-unlocks.md`; `design/gdd/local-achievements.md`; `design/gdd/sys-access.md`; `design/gdd/sys-journal.md`; `design/gdd/sys-test.md`; `design/registry/entities.yaml`; ADR-0002 | CLOSED |
| C-03 | Do not add a sixth persistent setting. SYS-TENSION preference ownership/path is deferred with the feature to post-MVP. | Current SYS-PERSIST contract remains exactly 12 leaves / five settings; no current Production gate depends on tension preference storage. | `design/gdd/sys-tension.md`; `design/gdd/systems-index.md`; `design/gdd/sys-test.md`; `design/registry/entities.yaml`; ADR-0002; `docs/architecture/architecture.md`; `production/session-state/active.md` | DEFERRED — NOT CURRENT BLOCKER |
| C-04 | Defer the timed active-phase save/load/rollback matrix with SYS-TENSION to post-MVP. | Current P0 Production gate excludes timed surfaces; future re-entry requires a SYS-SAVE amendment and post-MVP ADR/evidence. | `design/gdd/sys-tension.md`; `design/gdd/save-load-rollback.md`; `design/gdd/sys-test.md`; `design/gdd/systems-index.md`; `docs/architecture/architecture.md`; `production/session-state/active.md` | DEFERRED — NOT CURRENT BLOCKER |

## Boundary notes

- The historical cross-review report remains unchanged as the source finding record; its historical references are not normative contracts.
- No new gameplay feature, persistent leaf, timed-choice implementation, or new full review was started.
- Remaining engine-reference, content-lock, UX, build, and implementation evidence work remains outside this closure scope.
