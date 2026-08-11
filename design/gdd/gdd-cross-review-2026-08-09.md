# Cross-GDD Review Report

Date: 2026-08-09  
Mode: `full`  
Engine: Ren'Py 8.5.3 / Python 3.12  
Registry: `design/registry/entities.yaml` (version 2; present)  
Summary scan: no current system GDD exposes a standardized `## Summary` section; review used document headers plus Overview, Dependencies, Formulas, Tuning Knobs and Acceptance Criteria sections.

## Scope

GDDs reviewed: 11 system GDDs.

- `choice-and-causality-record.md`
- `cross-playthrough-unlocks.md`
- `deterministic-ending-resolution.md`
- `five-axis-state.md`
- `local-achievements.md`
- `save-load-rollback.md`
- `seven-day-chapter-script.md`
- `sys-access.md`
- `sys-journal.md`
- `sys-tension.md`
- `sys-test.md`

Also reviewed: `game-concept.md`, `systems-index.md`, `design/registry/entities.yaml`, `.claude/docs/technical-preferences.md`, and `docs/engine-reference/renpy/VERSION.md`.

The four design pillars were taken from `game-concept.md`. No separate `game-pillars.md` or explicit anti-pillar document exists.

Registry baseline: the registry-name consistency scan reported no authoritative value conflicts. This full review additionally checks document relationships, ownership, lifecycle boundaries, design theory and cross-system scenarios.

---

## Consistency Issues

### Blocking

#### C-01 — SYS-PERSIST has a live 9-leaf / 12-leaf authority split

`cross-playthrough-unlocks.md` defines schema v2 as 12 normative leaves and `sys-access.md`, ADR-0002, Architecture and the registry agree with that authority. However, the systems index still describes a 9-leaf manifest, and SYS-PERSIST acceptance criteria still assert 9 leaves and “other 8 leaves”.

Evidence:

- 12-leaf core contract: `design/gdd/cross-playthrough-unlocks.md:31`, `:43`, `:68-70`
- stale index summary: `design/gdd/systems-index.md:10`
- stale acceptance criterion: `design/gdd/cross-playthrough-unlocks.md:725`
- stale invariance criteria: `design/gdd/cross-playthrough-unlocks.md:785-788`
- stale “other 8 leaves” wording: `design/gdd/cross-playthrough-unlocks.md:749`
- current 12-leaf authority: `design/gdd/sys-access.md:47`, `:57`

This can produce incompatible validators, incomplete persistence invariance evidence and false-positive acceptance. Before architecture or implementation gates proceed, replace all stale 9-leaf references with the approved 12-leaf contract, update the affected fixtures and rerun SYS-PERSIST/SYS-SAVE/SYS-ACCESS/SYS-TEST traceability.

#### C-02 — Ending completion boundary is referenced but not owned or defined

SYS-PERSIST requires a unique `commit_ending_completion` after the complete ending narration and player-visible closure. SYS-ENDING currently defines only `commit_ending_entry`; its lifecycle and integration criteria make that entry the only commit path. No owning GDD currently freezes the completion callsite, exact control boundary, rollback behavior or completion event record.

Evidence:

- completion requirement: `design/gdd/cross-playthrough-unlocks.md:34`, `:178`, `:455-456`
- SYS-ENDING entry-only lifecycle: `design/gdd/deterministic-ending-resolution.md:124`, `:130`, `:150`
- entry-only callsite assertion: `design/gdd/deterministic-ending-resolution.md:666-667`
- unresolved completion callsite question: `design/gdd/cross-playthrough-unlocks.md:835`

The result is undefined behavior across ending entry, the remaining ending narration/epilogue, persistent unlock, save/load and rollback. Assign the completion owner and exact post-closure callsite, then synchronize SYS-ENDING, SYS-NARRATIVE, SYS-PERSIST, SYS-SAVE and SYS-TEST.

#### C-03 — SYS-TENSION preference storage has no approved owner/path

SYS-TENSION requires `tension_mode_enabled` to survive New Game and application restart while remaining outside per-run save/load/rollback. The same GDD states that SYS-PERSIST’s 12-leaf/5-setting root does not contain the preference and that the storage mechanism is deferred to a later architecture decision. No approved alternative owner or durable path is defined.

Evidence:

- persistence requirement: `design/gdd/sys-tension.md:26`
- explicit SYS-PERSIST exclusion: `design/gdd/sys-tension.md:344`
- provisional storage ownership: `design/gdd/sys-tension.md:377`
- unique setting identity outside ACCESS draft: `design/gdd/sys-tension.md:467`
- unresolved implementation gate: `design/gdd/sys-tension.md:636`

Either approve a dedicated preference contract/ADR with a unique owner and path, or defer the P1 feature until that contract exists. Do not add a sixth product persistent setting without a formal amendment to the 12-leaf authority.

#### C-04 — SYS-TENSION and SYS-SAVE have an asymmetric active-timer recovery contract

SYS-TENSION requires timed surfaces to disable save/load/rollback, preserve a choice-before checkpoint and never serialize an active timer. Its dependency table says SYS-SAVE has not yet been explicitly amended. SYS-SAVE’s dependency table has no SYS-TENSION row or phase-by-action matrix.

Evidence:

- Tension-side requirement: `design/gdd/sys-tension.md:29`, `:125`, `:339`
- Tension-side identified gap: `design/gdd/sys-tension.md:373`, `:638`
- SYS-SAVE dependency table: `design/gdd/save-load-rollback.md:436-450`

If timed mode is enabled, save/load/rollback during `Presenting`, `Running`, `Paused` and `Resolving*` has undefined cross-system behavior. Add the reciprocal dependency and freeze the phase × action × source matrix, or explicitly remove timed mode from the current architecture/content scope.

### Warnings

#### C-05 — Persistent result enum has an unclosed internal/public naming boundary

SYS-PERSIST uses `DURABLE_SUCCESS` in its mutation/state-flow description, while its public result formula, registry and consumers use `APPLIED_FLUSHED`.

Evidence:

- internal name: `design/gdd/cross-playthrough-unlocks.md:122`, `:166`
- public name: `design/gdd/cross-playthrough-unlocks.md:328`
- registry enum: `design/registry/entities.yaml:3127-3134`
- consumer usage: `design/gdd/local-achievements.md:38`, `design/gdd/sys-access.md:296-301`

This may be an intended internal-to-public mapping, but the mapping is not explicit. Freeze one public enum and document any private adapter classification, or remove the duplicate name.

#### C-06 — Several dependency status notes are stale after later GDD approvals

SYS-ACCESS still describes SYS-TENSION as lacking an approved GDD, while SYS-TENSION is now indexed and documented as Approved. Similar historical “Not Started” status text remains in dependency tables. These are tracking inconsistencies rather than new runtime rules, but they can misroute implementation work.

Evidence:

- current index status: `design/gdd/systems-index.md:14`
- stale SYS-ACCESS note: `design/gdd/sys-access.md:423`

Synchronize status text against the systems index after the blocking contract revisions are complete.

---

## Game Design Issues

### Blocking

No additional game-theory blocker was found beyond the contract blockers above.

### Warnings

#### D-01 — Dominant-strategy proof is not yet complete

The content baseline contains 52 `semantic_major` choices, 30 of them with zero axis delta (`57.7%`). The design intentionally gives those choices route facts, resources, counterevidence, repairs or outcome differences, which is a sound anti-hidden-score direction. However, exact terminal-class enumeration and full path evidence remain open under NARR-Q13, so the review cannot yet prove that one low-risk path is not superior across all meaningful dimensions.

Evidence:

- zero-delta tuning rationale: `design/quick-specs/zero-delta-major-choice-ratio-tuning-2026-08-05.md:12-19`
- choice trade-off tuning: `design/gdd/seven-day-chapter-script.md:473-478`
- unresolved exact class enumeration: `design/gdd/seven-day-chapter-script.md:748`, `:767`

Close NARR-Q13 and include path-level comparison/playtest evidence for route resources, character costs, token consequences, repair opportunities and ending outcomes.

## Holism Checks with No Finding

- Progression loops: one dominant narrative/causal loop; persistent collections, achievements and Journal are support loops.
- Player attention: approximately three active systems in the core choice loop; optional tension mode raises this to approximately four.
- Economy: route resources are bounded acquire/consume facts; axes, tokens and persistent collections are capped. No infinite source or runaway positive feedback was found.
- Difficulty curves: no incompatible combat or power-scaling curves exist; tension duration is an optional pacing system rather than a player-power curve.
- Pillar alignment: all reviewed systems support at least one of the four concept pillars. No explicit anti-pillar violation was found.
- Player fantasy: systems consistently reinforce observation, respect for autonomy, causal memory and shared cost.

---

## Cross-System Scenario Issues

Scenarios walked: 3.

### Blockers

#### S-01 — Timed choice with accessibility and save/load interaction

Systems: SYS-TENSION, SYS-ACCESS, SYS-CHOICE, SYS-STATE, SYS-SAVE.

Trigger: player enters an approved timed surface and activates a choice through mouse, keyboard or self-voicing-compatible input.

Expected order: stable accessible presentation → timer/arbitration → canonical choice activation → SYS-CHOICE → SYS-STATE history commit → reaction → later control flow.

Failure: the preference’s durable owner is undefined, and SYS-SAVE has no reciprocal timed-phase action matrix. Save/load/rollback during the active surface can therefore lack a defined safe checkpoint and timer non-serialization result.

Required action: close C-03 and C-04 before timed content enters production.

#### S-02 — Ending entry, full closure, persistent unlock and rollback

Systems: SYS-ENDING, SYS-NARRATIVE, SYS-PERSIST, SYS-SAVE, SYS-JOURNAL.

Trigger: Day 7 resolver selects an ending.

Expected order: detached resolution → ending entry/lifecycle transition → complete ending narration and player-visible closure → `commit_ending_completion` → persistent ending membership → later Journal presentation.

Failure: SYS-ENDING freezes only `commit_ending_entry`, while SYS-PERSIST requires a later completion callsite. The owner, exact boundary and rollback/save behavior for the gap are undefined.

Required action: close C-02 and add end-to-end completion/rollback evidence.

### Warnings

#### S-03 — Persistent unlock followed by Journal mark-seen

Systems: SYS-PERSIST, SYS-ACHIEVE, SYS-JOURNAL, SYS-ACCESS.

The intended flow is coherent: detached persistent snapshot → Journal read model → bounded presentation receipt → mark-seen request → persistent result → Journal state transition. The 9/12-leaf mismatch and `DURABLE_SUCCESS`/`APPLIED_FLUSHED` naming split can cause the evidence to validate a different state shape or result branch than the consumers expect.

Required action: close C-01 and C-05, then rerun the Journal/persistence integration matrix.

### Info

The normal non-timed choice path is structurally coherent: canonical activation commits once through SYS-STATE before reaction, and later payoff witnesses are required by SYS-CHOICE/SYS-NARRATIVE. Production proof remains gated by the unresolved content-lock artifacts.

---

## GDDs Flagged for Revision

| GDD | Reason | Type | Priority |
|---|---|---|---|
| `cross-playthrough-unlocks.md` | 9/12-leaf conflicts; missing completion boundary; result enum naming | Consistency | Blocking |
| `deterministic-ending-resolution.md` | Entry-only lifecycle conflicts with required completion unlock boundary | Consistency | Blocking |
| `sys-tension.md` | Preference owner/path and timed recovery contract incomplete | Consistency | Blocking |
| `save-load-rollback.md` | Missing reciprocal SYS-TENSION integration matrix | Consistency | Blocking |
| `systems-index.md` | Stale 9-leaf authority and dependency metadata | Tracking/Consistency | Blocking |
| `sys-access.md` | Stale dependency status notes | Consistency | Warning |
| `seven-day-chapter-script.md` | Exact terminal-class/dominant-strategy proof still pending | Design Theory | Warning |

---

## Required Actions Before Re-running

1. Make 12 leaves the only SYS-PERSIST authority; remove stale 9-leaf and “other 8 leaves” references from the index, GDD criteria and fixtures.
2. Define `commit_ending_completion`, its owner, callsite, post-closure boundary, completion event and rollback/save semantics across SYS-ENDING/SYS-NARRATIVE/SYS-PERSIST/SYS-SAVE/SYS-TEST.
3. Approve the SYS-TENSION preference storage contract or defer timed mode from the current architecture/content scope.
4. Add SYS-TENSION to SYS-SAVE’s dependency and freeze the timed phase × action × source matrix.
5. Normalize `DURABLE_SUCCESS` versus `APPLIED_FLUSHED` and update the registry and consumer contracts.
6. Complete NARR-Q13 and perform path-level dominant-strategy/playtest validation.

## Verdict

**FAIL** — four cross-system contract blockers must be resolved before architecture/implementation gates can safely proceed.

