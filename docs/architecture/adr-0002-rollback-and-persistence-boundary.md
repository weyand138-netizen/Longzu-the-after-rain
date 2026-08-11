# ADR-0002: Rollback and Persistence Boundary

- Status: Accepted
- Date: 2026-07-23
- Amended: 2026-07-27 by the twelfth-final targeted closure for narrative-only history authority
- Amended: 2026-07-30 for SYS-PERSIST schema v2, collection epoch, achievement discovery state, and flush-before-projection
- Amended: 2026-08-04 for SYS-ACCESS 12-leaf / five-setting authority and disposable pre-release development saves
- Amended: 2026-08-09 for P0 shared-contract closure: 12-leaf-only authority, public `APPLIED_FLUSHED`, ending completion boundary, and post-MVP SYS-TENSION deferral
- Engine: Ren'Py 8.5.3
- GDD requirements: SYS-STATE, SYS-CHOICE, SYS-SAVE, SYS-PERSIST, SYS-ACHIEVE

## Context

Players may freely save, load, and roll back. Per-run choices must roll back; achievements, unlocked endings, memories, and accessibility preferences must survive between playthroughs.

## Decision

- `default semantic_state = None` and `default state_schema_sentinel = None`; defaults never create a valid active run.
- Explicit new-game initialization writes sentinel `"semantic_state:v2"` and one rollback-transformed `RunMap` containing `schema_version`, an axes `RunMap`, and ordered `RunList` history. These aliases mean the concrete types produced by `{}` and `[]` in `.rpy`.
- Cross-playthrough product data uses one field only: `default persistent.sys_persist_state = build_fresh_persist_root()`. Schema v2 contains 12 normative leaves: `schema_version`、`catalog_generation_id`、`collection_epoch_id`、`achievement_ids`、`seen_achievement_ids`、`ending_ids`、`memory_ids` plus `settings.font_scale`、`settings.high_contrast`、`settings.reduced_motion`、`settings.flash_effects_enabled` and `settings.screen_shake_enabled` in that canonical settings order.
- The five project settings are validated、captured as one base tuple、merged from one approved source、preserved by collection reset and covered by save/load/rollback/new-game invariance. SYS-PERSIST remains the only storage writer；SYS-ACCESS owns their player semantics.
- Ren’Py self-voicing、clipboard voicing、text/auto/skip speed and volume remain engine preferences. Ren’Py engine font-size/high-contrast controls and the built-in accessibility menu are disabled in the production keymap so they cannot create a second font/contrast authority.
- State updates run in `.rpy` Python blocks, construct a complete candidate locally, and replace `semantic_state` once instead of mutating imported module objects or committing fields separately.
- Every production player-facing narrative choice, including `narrative_only`, commits through `SYS-STATE.apply_choice` after player confirmation and before immediate reaction. `narrative_only` passes an empty `RunMap`, appends only its stable history ID, and therefore saves, loads, rolls back, and replays under the same envelope as semantic-major choices.
- Achievement grants occur only after their approved completed-event/checkpoint condition is complete. Ending and memory memberships are separate namespaces and are not mirrored as achievements.
- Every changing SYS-PERSIST batch performs one complete-root replacement followed by one required `renpy.save_persistent()` before achievement backend projection or player-facing success feedback. The only public success result is `APPLIED_FLUSHED`; internal adapter classifications must not expose a second success name. Engine behavior that cannot prove a safe terminal result enters commit-unknown recovery.
- Collection reset increments `collection_epoch_id`; reset-time merge ignores lower-epoch collection data. Explicit New Game copies the current epoch into the rollback-owned run envelope, so reset前旧 saves/evidence cannot regrant achievements.
- `seen_achievement_ids` is a subset of `achievement_ids` used only for cross-session “新记录” discovery. It is not a pending-popup ledger and never affects narrative logic.
- Load resumes only when `after_load` classifies the sentinel as supported and then validates the state. Legacy, unsupported, and corrupt results enter a blocking safe flow that cannot return to the loaded scene; rollback, quick save/load, skip, history return, and screen return remain disabled until main menu or explicit new game.

## Implementation Guidelines

- The single persistent root and `semantic_state` must have concrete defaults/builders; no product subsystem may add a second flat persistent field.
- Save data must contain primitives and Ren'Py-managed collections only.
- Never place file handles, generators, tasks, sockets, or live engine displayables in save state.
- A rollback before a choice must restore the complete schema, five axes, and choice history to one coherent point.
- Rollback to before a narrative-only choice removes its history ID; load restores saved membership exactly, and replay performs one normal commit without duplication.
- The lifecycle sentinel must be saved with the run but never inferred from state contents or repaired by `default`.
- Flat prototype persistent fields and local `0.1.0-dev` saves/fixtures are explicitly incompatible and may be discarded；the pre-release schema v2 authority is amended in place to 12 leaves. After public release, any schema、field ownership or exact-type change requires a new schema version, a separate accepted migration ADR and version-by-version fixtures.
- Replaying an already granted achievement is filtered before request; direct adapter duplicates remain idempotent `DUPLICATE_NOOP`.
- Load and rollback never mutate the persistent root. A reset-era mismatch disables achievement evaluation for that loaded run without preventing the narrative from continuing.
- `SYS-ENDING` owns `commit_ending_completion`. Each ending label has one terminal completion node after final player-visible closure and before label exit/return. It emits `ending_completion_event_record` with `completed_event_id=ending_completed:{ending_id}` through the single persistence checkpoint coordinator. `commit_ending_entry` only owns `Active → Ended` and cannot emit a persistent ending request.
- Before completion, ending request/assignment/flush counts are zero. After `APPLIED_FLUSHED`, ending membership is canonical in `persistent.sys_persist_state`; later per-run load/rollback restores only lifecycle, completion event and control location. Rolling back before completion never removes the canonical membership; replay of an existing membership returns `DUPLICATE_NOOP` without a second notification.
- `SYS-TENSION` is post-MVP. The current 12-leaf/5-setting root is closed and receives no sixth setting; tension preference storage and active-timer save/load/rollback semantics require a future ADR and do not block the current Production gate.

## Alternatives Considered

- Store all state in `persistent`: rejected because rollback and new-game isolation would break.
- External JSON save files: rejected because Ren'Py already provides save and persistent semantics.
- Imported Python state container: rejected because it is not rollback-transformed.

## Performance Implications

Persistent writes are limited to changing unlock/settings/mark-seen batches at coarse checkpoints, not every dialogue line or rendered frame.

## Engine Compatibility

Verified against Ren'Py 8.5.3 persistent and Python documentation. Persistent data uses Ren'Py's own serialization and is not designed for untrusted sharing.
