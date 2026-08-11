# ADR-0006: Ending Completion Boundary

- Status: Accepted
- Date: 2026-08-09
- Scope: P0 shared-contract closure
- Engine: Ren'Py 8.5.3
- GDD requirements: SYS-ENDING, SYS-NARRATIVE, SYS-PERSIST, SYS-SAVE, SYS-TEST

## Context

`commit_ending_entry` marks entry into an ending, but ending membership must not be granted until the complete ending narration and player-visible closure are finished. The boundary must be unique, observable, replayable and independent from the pure resolver. It must also distinguish rollback-owned per-run completion state from cross-playthrough persistent membership.

## Decision

1. `SYS-ENDING` is the sole owner of `commit_ending_completion`.
2. Each of the six stable ending labels has exactly one terminal completion node. The call occurs after the final player-visible closure and before leaving the label or returning to chapter control flow. No resolver, entry statement, UI/Journal callback or SYS-PERSIST adapter may call it.
3. The call emits one rollback-owned `ending_completion_event_record`:

   `ending_id, completed_event_id, checkpoint_id, checkpoint_occurrence_id, collection_epoch_id, catalog_generation_id, stable_completion_boundary, owner_system`

   `completed_event_id` is `ending_completed:{ending_id}`; `stable_completion_boundary=True`; `owner_system=SYS-ENDING`.
4. The single persistence checkpoint coordinator converts that record into the ending request. SYS-PERSIST validates owner, catalog generation, epoch, checkpoint and completion reference; it does not re-run resolver logic or inspect live ending state.
5. `commit_ending_entry` owns only rollback-owned `Active → Ended`. Before the terminal completion node, ending request, root replacement and flush counts are zero.
6. A successful public result is `APPLIED_FLUSHED`. It adds the ending ID to the canonical 12-leaf root. `DUPLICATE_NOOP` is returned when the same ending membership already exists.
7. Per-run save/load/rollback restores lifecycle, completion event and control location. It never removes a successfully flushed persistent membership. Rolling back before completion restores an absent completion event; replaying the same completion is idempotent and produces no second notification.

## Consequences

- Ending entry and ending completion are testable as two separate boundaries.
- The ending completion event is a transient/run-owned input, not a thirteenth or sixth persistent leaf.
- SYS-SAVE can prove both pre-completion non-write behavior and post-completion persistent invariance.
- SYS-TEST can close the callsite count, event shape, replay and rollback matrix without adding a second ending decision path.

## Rejected Alternatives

- Granting at `commit_ending_entry`: rejected because entry is not narrative completion.
- Letting SYS-NARRATIVE or SYS-PERSIST own the call: rejected because SYS-ENDING owns ending lifecycle and stable ending identity, while SYS-PERSIST must remain semantic-agnostic.
- Recording completion in the persistent root: rejected because completion is per-run rollback state and the root already has the canonical `ending_ids` membership leaf.

## Traceability

| Contract | Updated artifact |
|---|---|
| Owner/callsite/event | `design/gdd/deterministic-ending-resolution.md`, `design/registry/entities.yaml` |
| Persistent result and root invariance | `design/gdd/cross-playthrough-unlocks.md`, `docs/architecture/adr-0002-rollback-and-persistence-boundary.md` |
| Save/load/rollback behavior | `design/gdd/save-load-rollback.md` |
| Content completion event | `design/gdd/seven-day-chapter-script.md` |
| Verification and traceability | `design/gdd/sys-test.md` |

