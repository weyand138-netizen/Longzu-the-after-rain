# 《雨停之后》Master Architecture

## Document Status

- Version: 2.0
- Last Updated: 2026-08-09
- Engine: Ren'Py 8.5.3
- GDDs Covered: `game-concept.md`, `systems-index.md`, all 11 current system GDDs in `design/gdd/`
- ADRs Referenced: ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0005, ADR-0006, ADR-0007
- Technical Director Sign-Off: 2026-08-09 - APPROVED WITH CONDITIONS
- Lead Programmer Feasibility: solo mode, external review skipped
- Conditions Accepted: C-01/C-02 closed by targeted P0 contract closure; C-03/C-04 deferred with SYS-TENSION to post-MVP; ENG-01 closed on 2026-08-10 by the pinned-SDK scripting, breaking-change, and deprecated-API reference set

## Technical Requirements Baseline

Extracted from the 11 current system GDDs plus the concept, systems index, and
technical preferences. Coverage is tracked at the architectural contract level;
content-lock and implementation gates remain downstream.

| ID | Source | Requirement | Domain |
|---|---|---|---|
| TR-STATE-001 | SYS-STATE | Schema 2, five axes, and ordered history share one rollback/save envelope | State |
| TR-STATE-002 | SYS-STATE | Validation is strict and commits one complete replacement | State |
| TR-END-001 | SYS-ENDING | Deterministic total six-ending resolution without randomness | Logic |
| TR-END-002 | SYS-ENDING | Counterevidence, cause lineage, and resolver purity are preserved | Logic |
| TR-CHOICE-001 | SYS-CHOICE | Every player-facing choice commits through SYS-STATE | Narrative |
| TR-CHOICE-002 | SYS-CHOICE | Reaction/payoff joins and terminal continuation coverage are exact | Narrative |
| TR-NAR-001 | SYS-NARRATIVE | Seven-day chapter paths and six endings are valid and content-locked | Content |
| TR-SAVE-001 | SYS-SAVE | Free save/load/rollback remain supported | Foundation |
| TR-SAVE-002 | SYS-SAVE | Legacy, unsupported, and corrupt loads enter blocking safe flow | Foundation |
| TR-PERSIST-001 | SYS-PERSIST | Schema-v2 root, epoch, settings, merge/reset, and flush are coherent | Persistence |
| TR-PERSIST-002 | SYS-PERSIST | Ending completion produces one durable completed-event boundary | Persistence |
| TR-ACH-001 | SYS-ACHIEVE | 11 event-based achievements are idempotent and persist independently | Feature |
| TR-JOURNAL-001 | SYS-JOURNAL | Journal bundle/read model exposes chapters, memories, endings, and achievements | UI |
| TR-ACCESS-001 | SYS-ACCESS | Keyboard, scale, contrast, self-voicing, and effect alternatives are equivalent | Accessibility |
| TR-TENSION-001 | SYS-TENSION | Timeout maps to a canonical choice and does not alter ending rules | Feature |
| TR-TENSION-002 | SYS-TENSION | Post-MVP tension preference survives restart but not per-run rollback | Deferred Feature |
| TR-TEST-001 | SYS-TEST | Lint, pure logic, engine testcase, and gate evidence control hand-off | QA |
| TR-BUILD-001 | SYS-BUILD | Offline Windows package includes legal and integrity provenance | Release |

## Engine Knowledge Gap Summary

Ren'Py 8.5.3 is post-May-2025 and therefore high-risk for newly introduced APIs.
The local reference library now contains the verified `BUILD.md` spike and
`capability-manifest-v1.json`, but the required breaking-change, deprecated-API,
current-best-practice, and module reference files are absent. Therefore the
following remain verification gates rather than settled implementation facts:

- HIGH: `testcase`/`testsuite` runner behavior, save/rollback and `after_load`,
  `persistent` flush/merge behavior, timed interaction and build CLI.
- MEDIUM: screen input/focus, self-voicing, accessibility actions, and audio APIs.
- LOW: detached pure Python ending resolution and ordinary label flow.

Any API claim marked HIGH or MEDIUM in this document must be checked against the
Ren'Py 8.5.3 reference set before implementation. CLI syntax is version-bound.

## System Layer Map

```text
PRESENTATION
  SYS-JOURNAL / SYS-ACCESS / SYS-GALLERY / SYS-AUDIO
                         |
FEATURE
  SYS-CHOICE / SYS-NARRATIVE / SYS-ACHIEVE / SYS-TENSION [POST-MVP DEFERRED]
                         |
CORE
  SYS-STATE ----------------------> SYS-ENDING
                         |
FOUNDATION
  SYS-SAVE / SYS-PERSIST / SYS-TEST
                         |
PLATFORM
  Ren'Py 8.5.3 / Python 3.12 / Windows 10-11 x86-64 / SYS-BUILD
```

Dependencies point downward. The pure ending resolver has no upward or engine dependency.
SYS-BUILD consumes frozen owner manifests and current SYS-TEST evidence; it does not
own narrative, persistence, or test semantics. SYS-TENSION is explicitly deferred to
post-MVP; its preference owner and timed save/recovery contract are not current
Production inputs.

## Module Ownership

### Approved System Ownership Map (provisional where marked)

| Layer | Module | Owns | Exposes | Consumes | Engine/API risk |
|---|---|---|---|---|---|
| Platform | SYS-BUILD | Build run, staging/archive, source/catalog/asset hashes, release closure | Candidate validation and release build entry points | Owner manifests, SYS-TEST evidence, Ren'Py build CLI | HIGH; local API reference missing |
| Foundation | SYS-SAVE | Save/load/rollback contract, schema sentinel, legacy/corrupt safe flow, control locations | `after_load()`, safe-flow routing, save contract | Ren'Py save/rollback/`after_load` | HIGH; local API reference missing |
| Foundation | SYS-PERSIST | Persistent schema, epoch, merge/reset, complete-root replacement, flush, backend projection | Persistent batch, snapshot, mark-seen, reset adapters | Ren'Py `persistent`, `renpy.save_persistent()` | HIGH; 12-leaf authority synchronized |
| Foundation | SYS-TEST | Test manifests, runner separation, evidence artifacts, gate aggregation | FAST/INTEGRATION/RELEASE runners | `testcase`/`testsuite`, lint, Python tests | HIGH; 8.5.3 behavior unverified |
| Core | SYS-STATE | Schema 2, five axes, ordered history, active sentinel, validation | `apply_choice()`, snapshot, validation | Rollback-owned Ren'Py store | MEDIUM/HIGH |
| Core | SYS-ENDING | Pure resolver, predicates, cause records, ending lifecycle and completion boundary | `resolve_ending_record()`, `commit_ending_entry`, `commit_ending_completion` | Detached snapshot and frozen catalogs | Pure logic LOW; completion contract synchronized |
| Feature | SYS-CHOICE | Choice schema, canonical IDs, reaction/payoff joins, coverage validators | Canonical activation and graph validation | SYS-STATE, SYS-NARRATIVE, SYS-ACCESS, SYS-TENSION | Medium; content contract provisional |
| Feature | SYS-NARRATIVE | Chapter labels, prose, events, reactions/payoffs, ending closure content | Chapter flow, content catalogs, completion event | SYS-CHOICE, SYS-STATE, SYS-ENDING | Low engine risk; content lock pending |
| Feature | SYS-ACHIEVE | 11 event-condition records, candidate scan, session queue | Candidate and mark-seen adapters | Completed-event snapshots, SYS-PERSIST | Medium; backend behavior unverified |
| Feature | SYS-TENSION | Optional timer, arbitration, timeout-to-canonical-choice mapping | Timed surfaces and mode preference | SYS-ACCESS, SYS-CHOICE, SYS-SAVE | Post-MVP deferred; excluded from current Production gate |
| Presentation | SYS-JOURNAL | Journal read model, chapter/memory/ending/achievement presentation | Bundle assembler, refresh, mark-seen request | SYS-PERSIST, SYS-ACCESS, approved catalogs | Medium; bundle contract in revision |
| Presentation | SYS-ACCESS | Settings semantics, focus/navigation, self-voicing, effect alternatives | Input normalization, settings UI, transcript | Ren'Py screens/input/self-voicing, SYS-PERSIST | MEDIUM/HIGH; local API reference missing |
| Presentation | SYS-GALLERY | Locked/unlocked CG read model and gallery presentation | Gallery screen | SYS-PERSIST and asset catalog | Not designed |
| Presentation | SYS-AUDIO | Audio channels, mute/volume, asset provenance | Audio playback adapter | Ren'Py audio and asset register | Not designed |

Ownership constraints:

- SYS-STATE is the only writer of per-run semantic state.
- SYS-PERSIST is the only writer of product-persistent data; SYS-ACCESS owns setting semantics but not storage.
- SYS-ENDING owns selection, cause construction, `commit_ending_entry` and `commit_ending_completion`; the latter has one terminal completion node per ending label and emits the rollback-owned completion event consumed by SYS-PERSIST.
- SYS-CHOICE owns canonical choice identity and execution order; SYS-NARRATIVE owns concrete content and event records.
- Presentation modules consume read models and cannot decide endings, mutate axes, or inspect hidden tokens.
- SYS-BUILD validates and packages owner outputs; it cannot repair or rewrite them.

The code-location table below is a subordinate implementation snapshot. The system
ownership map above is authoritative; any code-location mismatch is an
implementation task, not a second ownership authority.

| Module | Owns | Exposes | Consumes |
|---|---|---|---|
| `game/10_state.rpy` | Uninitialized defaults, lifecycle sentinel, schema 2 envelope and validation | `initialize_new_semantic_state`, `classify_loaded_semantic_state`, `validate_axis_deltas`, `apply_choice`, `current_ending_snapshot` | Ren'Py store |
| `ending_rules.py` | Private snapshot builder; frozen catalogs; cause-ready evaluation artifact; exact concrete record classes; canonical cause bytes/hash; policy-v2 pure resolver | `_build_detached_ending_snapshot` (private), `resolve_ending_record`, compatibility `resolve_ending` | Immutable transfer; detached exact built-in graph |
| `game/11_persistence.rpy` | Single schema-v2 root、12-leaf manifest、five-setting base/batch、epoch/seen、flush、merge/reset、backend projection | owner adapters、detached snapshot、exact durable-result record | Ren’Py persistent/achievement APIs |
| `game/12_achievements.rpy` | 11-item condition catalog、snapshot evaluator、session-only presentation | achievement candidate、mark-seen、Journal/presenter adapters | SYS-NARRATIVE snapshot、SYS-PERSIST detached result |
| chapter scripts | Prose, local menus, immediate feedback | Chapter labels | State/achievement helpers |
| `screens.rpy` | Interaction layout and journal views | Screens | Read-only store/persistent state |
| `options.rpy` | Build and product configuration | Ren'Py config | Platform/build system |
| test files | Canonical vectors and smoke paths | Test reports | Public module/label contracts |

## Data Flow

### Approved Runtime Data Flows

#### 1. Ordinary choice and presentation refresh

```text
Mouse/keyboard/accessibility-equivalent input
  -> SYS-ACCESS canonical choice_id
  -> SYS-CHOICE confirmation
  -> SYS-STATE.apply_choice()
  -> atomic semantic_state replacement
  -> SYS-NARRATIVE immediate reaction
  -> later label/menu control flow
  -> SYS-JOURNAL/SYS-ACCESS/screens read-only refresh
```

This is synchronous and single-threaded. Reaction follows commit without an
interactive boundary. Presentation never reads axes, tokens, or resolver internals.

#### 2. Event and delayed payoff flow

```text
SYS-NARRATIVE event
  -> SYS-CHOICE reaction/payoff bidirectional join validation
  -> SYS-STATE ordered history
  -> later history guard or route fact
  -> payoff event
  -> SYS-ENDING/SYS-ACHIEVE consume completed event
```

Stable IDs identify choices, reactions, and payoffs. Payoff timing is strictly
later than the originating choice. Achievements consume completed events only and
cannot change narrative state.

#### 3. Save, load, and rollback

```text
Ren'Py save/rollback
  -> semantic_state + state_schema_sentinel + control location
  -> SYS-SAVE.after_load()
  -> sentinel classification
       SUPPORTED -> SYS-STATE validation -> resume narrative
       LEGACY/UNSUPPORTED/CORRUPT -> blocking safe flow
                               -> main menu or explicit New Game
```

Per-run state is rollback-owned by Ren'Py. SYS-PERSIST is not part of ordinary
rollback. Unsupported or corrupt state is never repaired in place.

#### 4. Initialization and ending completion [PROVISIONAL]

```text
Engine/config/catalogs
  -> SYS-PERSIST product-root initialization
  -> SYS-STATE defaults remain None
  -> explicit New Game creates schema 2 semantic_state
  -> chapter labels/screens become available
  -> Day 7 SYS-ENDING resolution
  -> ending entry
  -> complete ending narration and visible closure
  -> SYS-ENDING terminal completion node
  -> commit_ending_completion -> ending_completion_event_record
  -> SYS-PERSIST unlock/achievement/Journal refresh
```

`commit_ending_completion` ownership, six terminal callsites, completion event
shape and persistent/rollback semantics are frozen by ADR-0006. This closure is
targeted and does not start a new full review.

#### 5. Optional tension mode [POST-MVP DEFERRED]

```text
PlayableStable (post-MVP only)
  -> SYS-TENSION reads future approved preference
  -> timed surface / pause / arbitration
  -> canonical choice_id or timeout choice_id
  -> SYS-CHOICE -> SYS-STATE -> reaction -> payoff
```

The durable owner of `tension_mode_enabled` and the save/load/rollback action
matrix for Presenting, Running, Paused, and Resolving phases remain unresolved.

No flow crosses a thread boundary. Engine callbacks, persistence I/O, and timed
interaction behavior require Ren'Py 8.5.3 reference verification before implementation.

### Choice and rollback

```text
Player -> Ren'Py menu -> chapter branch -> apply_choice(choice_id, axis_deltas)
       -> validate current envelope and payload
       -> one replacement assignment to `default semantic_state`
       -> immediate dialogue -> later chapter queries semantic state
```

Every production player-facing narrative choice uses this path. `narrative_only` passes an empty `RunMap`, commits its stable ID after player confirmation and before reaction logic, leaves axes unchanged, and shares the same save/load/rollback history envelope.

Ren'Py owns rollback snapshots. Imported Python never holds live mutable state.

### Ending resolution

```text
Day 7 label -> validate active sentinel + live state
            -> extract exact ints + detached tuple[str, ...]
            -> imported private _build_detached_ending_snapshot(...)
            -> exact built-in snapshot -> resolve_ending_record(snapshot)
            -> fold history into unresolved counterevidence token set
            -> rebuild completed events/resource possession from frozen choice projections
            -> derive route qualifications without external live state
            -> priority predicate evaluation; freeze cause-ready clause trace + audit facts
            -> extract path-specific causes only from FrozenResolutionEvaluation
            -> canonical cause_payload_v1 bytes + full SHA-256 IDs + fixed total order
            -> deep-immutable resolution record, including unresolved-token causes
            -> record.ending_id -> Day 7 orchestrator enters matching ending label
            -> Active -> Ended (flow ownership: SYS-ENDING) -> persistent unlock + achievement
```

### Persistence

```text
Approved completed-event snapshot
  -> SYS-ACHIEVE validates generation + collection epoch + checkpoint occurrence once
  -> 11-record condition scan
  -> SYS-PERSIST owner adapter injects requester and joins cross-kind batch
  -> one complete schema-v2 root replacement
  -> required save_persistent checkpoint
  -> exact durable-result record
  -> backend projection + session-only notification group
  -> modal close or Journal render -> mark-seen batch
```

### Load compatibility

```text
default semantic_state = None
default state_schema_sentinel = None

new game -> explicit initializer -> sentinel "semantic_state:v2" + schema 2 RunMap

after_load
  -> sentinel None ----------------> LEGACY_INCOMPATIBLE ----\
  -> sentinel unknown/wrong type --> UNSUPPORTED_VERSION ----> blocking safe flow
  -> sentinel v2 + invalid state --> CORRUPT_STATE ----------/
  -> sentinel v2 + valid state ----> SUPPORTED -> resume
```

The blocking safe flow cannot return to the loaded scene. It disables rollback, quick save/load, skip, history return, and screen return; it offers main menu or explicit new game only. Persistent unlocks are not cleared.

### Initialization order

1. Engine/common scripts.
2. Config, characters, stable semantic resources.
3. Pure module import and catalogs.
4. Store defaults/persistent defaults; `semantic_state` and its sentinel default to `None`.
5. New game explicitly initializes sentinel and schema 2 state.
6. On load only: `after_load` classifies the sentinel before validating state and either resumes or enters the blocking safe flow.
7. Screens and chapter labels.
8. Testcases in test mode.

## API Boundaries

### Approved Public Contracts

```python
apply_choice(choice_id: str, axis_deltas: RunMap) -> Literal["APPLIED", "DUPLICATE_NOOP"]
current_ending_snapshot() -> dict[str, object]
```

SYS-STATE is the sole writer of `semantic_state`. It validates the sentinel,
schema, choice ID, and delta, then commits one complete replacement. A duplicate
must not trigger reaction.

```python
resolve_ending_record(snapshot: dict[str, object]) -> EndingResolutionRecord
```

SYS-ENDING is pure: no Ren'Py state, files, time, randomness, persistence, or
mutable cache. It accepts only a detached exact built-in graph and returns exactly
one ending for every valid snapshot. Its separate `commit_ending_completion`
boundary is owned by the ending orchestrator and is governed by ADR-0006.

```python
normalize_choice_input(surface_id: str, raw_input: object) -> CanonicalChoiceAction
validate_choice_manifest(manifest: ChoiceManifest) -> ChoiceCoverageReport
```

SYS-CHOICE owns canonical identity, input equivalence, execution order, and
reaction/payoff coverage. Every successful `apply_choice` precedes reaction; no
caller may write history or axes directly.

```python
run_chapter(label: str) -> None
emit_completed_event(event_id: str) -> None
```

SYS-NARRATIVE owns chapter text, labels, events, reactions, and payoffs. It does
not own global ending predicates or persistent writes. Completion events are
emitted only after the corresponding content is complete.

```python
classify_loaded_semantic_state(sentinel: object, state: object) -> Literal[
    "SUPPORTED", "LEGACY_INCOMPATIBLE", "UNSUPPORTED_VERSION", "CORRUPT_STATE"
]
route_invalid_load(classification: LoadClassification) -> None
```

SYS-SAVE resumes only supported state. All other classifications enter the
blocking safe flow and never repair state in place or clear persistent data.

```python
submit_persistent_batch(request: PersistentBatchRequest) -> PersistDurableResult
get_persistent_snapshot() -> PersistentSnapshot
```

SYS-PERSIST owns the single product root and the sequence complete-root
replacement -> flush -> projection. It must distinguish safe failure from
commit-unknown. The 12-leaf authority is the sole current persistence contract.

```python
submit_achievement_candidate(
    stable_id: str, completed_event_id: str, checkpoint_id: str
) -> PersistDurableResult
```

SYS-ACHIEVE consumes completed events only, does not read hidden semantic state,
and relies on SYS-PERSIST for durable writes.

```python
normalize_input(surface_id: str, input_event: object) -> CanonicalAction
get_access_settings() -> AccessSettings
```

SYS-ACCESS owns input equivalence and setting semantics while SYS-PERSIST owns
storage. Self-voicing cannot implicitly confirm a choice.

```python
resolve_timed_surface(
    surface_id: str, elapsed: object, input_event: object | None
) -> CanonicalChoiceAction
```

SYS-TENSION maps timeout only to a registered canonical choice, defaults off, and
keeps a non-timed path when re-entered post-MVP. Preference ownership and active-
timer recovery are deferred and do not block the current Production gate.

```python
build_journal_bundle() -> JournalCatalogBundle
build_candidate_manifest_v1(inputs: BuildInputs) -> CandidateManifestV1
bind_staging_evidence(candidate: CandidateManifestV1, evidence: TestEvidenceBundleV1) -> StagingEvidenceBound
build_release(candidate: CandidateManifestV1) -> ArchiveArtifact
bind_archive_evidence(candidate: CandidateManifestV1, archive_hash: str, evidence: TestEvidenceBundleV1) -> ArchiveEvidenceBound
run_gate(manifest: TestManifest) -> GateArtifact
```

SYS-JOURNAL consumes read models, SYS-BUILD validates and packages owner outputs,
and SYS-TEST consumes production contracts without catalog or resolver injection.
SYS-BUILD owns `candidate_manifest:v1` and archive bytes; SYS-TEST owns
`test_evidence_bundle:v1`, `staging_exclusion_report:v1`, and
`archive_exclusion_report:v1`. The package runner is blocked until staging
evidence is bound, and READY is blocked until archive evidence is bound. The
archive hash covers ZIP bytes only; manifests are siblings outside the archive.
All engine-specific types and runners require Ren'Py 8.5.3 reference verification.

```text
source_identity -> candidate_identity -> scoped_evidence_identity
                                   \-> archive_hash -> release_identity
```

`candidate_identity` includes only source/catalog/asset/legal/engine inputs and
identity-affecting build configuration that can change delivered bytes or
semantics. Workspace path, output location, log level, timeout, and diagnostic
retention are run-only fields in `run_record` and do not change the candidate.
All final archive/manifest/provenance hashes remain excluded from
`candidate_identity`; `archive_hash` is SHA-256 over exact package bytes and
therefore cannot hash a file that contains itself.

```python
apply_choice(choice_id: str, axis_deltas: RunMap) -> Literal["APPLIED", "DUPLICATE_NOOP"]
```

- Requires exact `RunMap` payload type, known axes, exact integer `+1` values, and a globally unique stable ID. `RunMap`/`RunList` mean the concrete rollback-transformed types produced by `{}`/`[]` in `.rpy`, not abstract protocols or imported CPython containers.
- Validates the active sentinel and existing schema 2 state envelope before validating the payload.
- Builds a complete candidate locally and commits through one replacement assignment; never clamps or partially repairs.
- Returns `DUPLICATE_NOOP` without replacing state when the ID already exists.

```python
validate_axis_deltas(axis_deltas: RunMap) -> int
```

- Owns the only affected-axis count primitives used by `apply_choice`; the public helper runs type then value/shape/count, while `apply_choice` schedules the same primitives around its global precedence.
- Returns exact int 0–2 for legal payloads; preserves the shared `TypeError`/`ValueError` oracle.

```python
validate_active_semantic_state(
    sentinel: object,
    state: object,
) -> None
```

- Is the shared active-state validation implementation used by writes and snapshots; `after_load` reuses the state portion only after sentinel classification.
- Uses a finite schema-known exact-type sweep before a value/shape sweep. It checks known containers/slots and all key objects but never performs `__getitem__` or protocol access on unknown-key values and never follows arbitrary references.
- Across `apply_choice`, the fixed order is global state+payload known-slot type sweep → state value/shape → choice-ID value → delta value/shape/count. Therefore state-value + payload-type yields payload `TypeError`, while illegal choice ID + delta value defect yields choice-ID `ValueError`.
- Known-value reads use private `_read_known_slot`; test builds may inject a read-only trace sink to prove that only the allowlisted known paths were accessed. Production passes no trace, and the seam cannot substitute containers or validation results.

```python
current_ending_snapshot() -> dict[str, object]
```

- After active sentinel/live-state validation, extracts only exact ints and a detached built-in tuple of exact history strings.
- Calls private `_build_detached_ending_snapshot` with those immutable built-ins; the imported helper creates and returns the exact CPython built-in dict/list graph. No chapter, UI, achievement, or ending caller may invoke it directly.
- Never passes live `RunMap`/`RunList` or another mutable store collection across the import boundary.
- A static production-source scan covers all `game/**/*.rpy` and `game/**/*.py`, resolves direct/import/module aliases, and closes over assignment, argument/return flow, closures, containers, wrappers and reflection/dynamic lookup. Exactly one production callsite is allowed: `game/10_state.rpy::current_ending_snapshot`; CFG proof requires active validation to dominate it on every path. Unresolved references, symbol escape, production-to-test-only dependency, and test wrapper leakage fail the build.

```python
_build_detached_ending_snapshot(
    schema_version: int,
    axis_values: tuple[int, int, int, int, int],
    history_ids: tuple[str, ...],
) -> dict[str, object]
```

- Private, non-exported helper; only `current_ending_snapshot` may call it in production.
- Direct tests must pass exact int, exact five-int tuple, and exact-string tuple. Wrong exact types raise `TypeError`; type-clean wrong schema, arity, ranges, ID format, or uniqueness raise `ValueError`; failures return no partial graph and never normalize.

```python
classify_loaded_semantic_state(
    sentinel: object,
    state: object,
) -> Literal["SUPPORTED", "LEGACY_INCOMPATIBLE", "UNSUPPORTED_VERSION", "CORRUPT_STATE"]
```

- Never initializes or repairs state.
- Is called only by `after_load`; non-supported results enter the blocking safe flow.

```python
resolve_ending_record(snapshot: dict[str, object]) -> EndingResolutionRecord

resolve_ending(snapshot: dict[str, object]) -> str
```

- Requires exact CPython built-in dict/list/scalar types and validates the complete schema 2 snapshot before fallback evaluation.
- Uses fixed runtime stages through priority predicate evaluation → cause extraction from `FrozenResolutionEvaluation` → record construction. Atomic trace entries freeze template/polarity/kind/source identity plus exact source/value/anchor fields; token fold freezes audit template identity and exact `audit`/`unresolved_counterevidence`/`unresolved_token` values. Cause extraction reads neither snapshot/catalog nor evaluator.
- Raises `TypeError` for known-slot exact-type violations and `ValueError` for unknown keys, schema, shape, range, history, missing catalog coverage, or invalid fold operations.
- Folds ordered choice IDs through private `_COUNTEREVIDENCE_INDEX`, a `MappingProxyType` built once from an exact tuple of immutable `NamedTuple` records after private import/build-time validation. Choice/effect schema, token caps/domains/modes, and repair references are not revalidated per call. No runtime mutation, replacement, registration, or resolver-injection API exists.
- A revoke adds one unique repairable or audited irreversible token. Catalog validation rejects unknown target, wrong domain/mode, irreversible target, and other invalid repair references before freeze. At runtime a validated repair removes its named token only when currently unresolved; an as-yet-unproduced or already-resolved target is a fold-legality `ValueError`.
- Frozen route projections map every history choice to completed events and resource acquire/consume operations. The resolver reconstructs route facts and qualifications solely from history and immutable catalogs. Duplicate acquire and absent consume both raise `ValueError` at route-fact fold, before qualification or later stages.
- `rain_stops` requires exactly all five axes at 3 and an empty unresolved-token set; route qualifications are not an additional predicate input.
- Clause templates and per-token audit templates have disjoint lineage keys. The payload matrix uniquely fixes source references, observed/required values and anchors; axis matches use the earliest required actual increments. Production SHA remains fixed, while a separate build-layer bijection checker accepts synthetic collision pairs outside the resolver manifest.
- `ending_rules.EndingCauseRecord`, `ClauseEvaluationTraceEntry`, `HigherPriorityExclusionEntry` and `EndingResolutionRecord` have one module/qualname/field order. A source-hash-verified test-only AST copy observes stages, clauses, wrapper call count and field reads without adding a production seam.
- Purity policy v2 classifies explicit leaves, CPython 3.12 implicit opcode/operand pairs, six exact record constructors and TypeError/ValueError construction. Custom-protocol/native-dispatch mutants must fail before dispatch. Runtime/interpreter pin remains unchanged.
- Complexity is `O(H + P + Q + C + B + L·R log R + L·F log F + K log K)` with `O(H + P + Q + C + B + R + F + K)` extra space; `L` is the maximum UTF-8 byte length among sorted source/fact stable IDs, and `R` includes qualification contributor references.
- Performs no side effects.

### Deterministic validation stages

All active APIs except `validate_axis_deltas` validate the lifecycle sentinel. `apply_choice` and `current_ending_snapshot` share the active type/value prefix. Traversal is limited to schema-known slots: root/axes/delta keys are type-checked, but unknown values receive no `__getitem__` or protocol access; history is inspected one level only. Missing/extra fields are caught after the type sweep. `after_load` is the compatibility exception: it classifies `None`, unknown exact strings, and wrong-type sentinels before invoking state validation only under the exact v2 sentinel.

Strict-dominance tooling requires a finite choice DAG. For every reachable prehistory `h`, it proves `L_A(h) ⊆ L_B(h)` over complete stable choice-ID suffixes before comparing token prefixes. Every A suffix must remain executable in the same order after B; matching node sets are insufficient. Sparse resource costs use key union/missing zero, and each aligned prefix must satisfy `U_B(h,s,k) ⊆ U_A(h,s,k)`.

Every irreversible token is admitted only with an accepted approval whose author/reviewer IDs resolve through the project identity registry to different `canonical_person_id` values. Every continuation has a shortest-later-choice count of at least two plus an agency node whose complete `branch_choice_id → outcome_reference_ids` mapping proves that at least two branches change ending selection, character fate, cost bearer, or tragedy closure. Outcome references have exact kind/subject/state/source-event records.

Production source scanning classifies every player-facing narrative choice or an explicitly non-narrative navigation interaction. Every choice commits through `SYS-STATE.apply_choice` after confirmation and before reaction; `narrative_only` uses an empty `RunMap`, so its history membership rolls back and saves/loads with the same envelope. For every choice, canonical prehistory and legal terminal continuation, reaction CFG proof and a later payoff witness are mandatory. Their exact joins, cardinality, proof-kind nullability and reverse event metadata remain a provisional downstream gate owned by `SYS-CHOICE`/`SYS-NARRATIVE` and are excluded from `SYS-STATE` approval. Canonical ending witnesses and terminal-cause classes retain their existing causal/exclusion/display budget.

Route qualifications are pure predicates over ordered stable choices and event/resource facts rebuilt from the frozen choice-projection catalog. They represent route membership, exclusive commitments, or concrete resource possession only; no external live-state read, persisted `qualified_*` flag, five-axis proxy checklist, or true-ending gate is allowed.

Component verification uses five canonical machine evidence types: `UT_ENGINE`, `UT_PURE`, `INSTR`, `STATIC`, and `BRANCH`. Atomic replacement, shared helper primitives, private export status, full symbol escape closure, and CFG domination each have matching evidence rather than unit-test labels that cannot prove them.

```python
submit_achievement_candidate(
    stable_id: str,
    completed_event_id: str,
    checkpoint_id: str,
    checkpoint_occurrence_id: str,
    collection_epoch_id: int,
) -> PersistDurableResult
```

- Public callers cannot pass requester identity; the SYS-PERSIST adapter injects it.
- Existing membership is normally filtered by SYS-ACHIEVE and yields no call; a direct duplicate adapter fixture returns `DUPLICATE_NOOP`.
- `SYS-ACHIEVE` owns 11 exact event-condition records and receives only `achievement_event_catalog:v2` snapshots.
- Achievement code may not read axis values, token emptiness, ending thresholds, resources or resolver predicates.
- SYS-PERSIST owns root replacement, required flush, backend projection, collection epoch and `seen_achievement_ids`.

## ADR Audit

| ADR | Engine compatibility | Version | GDD linkage | Conflicts / risks | Validity |
|---|---|---|---|---|---|
| ADR-0001 | Present | Present | Present | None direct | Valid |
| ADR-0002 | Present | Present | Present | 12-leaf authority, public `APPLIED_FLUSHED`, ending completion and post-MVP tension scope synchronized | Valid with downstream implementation gates |
| ADR-0003 | Present | Present | Present | None direct | Valid |
| ADR-0004 | Present | Present | Present | Completion event remains rollback-owned and outside semantic snapshot | Valid with ADR-0006 |
| ADR-0005 | Present | Present | Present | Ending entry/completion lifecycle synchronized | Valid with ADR-0006 |
| ADR-0006 | Present | Present | Present | None; targeted completion boundary closure | Valid |
| ADR-0007 | Present | Present | Present | Runner capability, candidate manifest, canonical encoding, evidence handshake, legal/archive closure, and identity self-reference prevention | Valid; targeted SYS-BUILD closure |

The engine reference is high risk because Ren'Py 8.5.3 post-dates the training
baseline. The local reference library contains `VERSION.md`, the verified
`BUILD.md` spike, and `capability-manifest-v1.json`; dedicated module,
breaking-change, and deprecated-API references remain absent. All engine-specific
API claims outside the verified build boundary remain subject to reference
refresh.

## Technical Requirements Traceability

| Req ID | Requirement | ADR coverage | Status |
|---|---|---|---|
| TR-STATE-001 | Schema 2, five axes, ordered history share rollback/save envelope | ADR-0002/0004/0005 | Covered |
| TR-STATE-002 | Strict validation and one replacement assignment | ADR-0004 | Covered |
| TR-END-001 | Deterministic total six-ending resolution | ADR-0001 | Covered |
| TR-END-002 | Counterevidence, cause lineage, and resolver purity | ADR-0001/0005 | Covered |
| TR-CHOICE-001 | Every player-facing choice commits through SYS-STATE | ADR-0002 | Covered |
| TR-CHOICE-002 | Exact reaction/payoff joins and terminal continuation coverage | ADR-0008 | Covered |
| TR-NAR-001 | Seven-day chapter paths and six endings | ADR-0003 | Conditional on content lock |
| TR-SAVE-001 | Free save/load/rollback | ADR-0002/0004 | Covered |
| TR-SAVE-002 | Blocking legacy/unsupported/corrupt load flow | ADR-0002/0005 | Covered |
| TR-PERSIST-001 | Schema-v2 root, epoch, settings, merge/reset and flush | ADR-0002 | Covered; 12-leaf authority |
| TR-PERSIST-002 | Completed-ending event and durable unlock boundary | ADR-0002/0006 | Covered; targeted closure |
| TR-ACH-001 | 11 event-based local achievements with idempotent persistence | ADR-0002 | Conditional |
| TR-JOURNAL-001 | Journal bundle and read-model presentation | ADR-0003 | Conditional |
| TR-ACCESS-001 | Keyboard, scale, contrast, self-voicing, and effect alternatives | ADR-0002/0003 | Conditional |
| TR-TENSION-001 | Timeout maps to canonical choice and never changes ending rules | None | GAP |
| TR-TENSION-002 | Tension preference survives restart but not run rollback | Future post-MVP ADR | Deferred; excluded from current Production gate |
| TR-TEST-001 | Lint, pure logic, engine testcase, and gate evidence | ADR-0001/0007 | Covered at contract level; implementation evidence pending |
| TR-BUILD-001 | Offline Windows package with legal and integrity provenance | ADR-0003/0007 | Covered at contract level; implementation evidence pending |

Coverage count: 10 covered, 5 conditional, 3 gaps; SYS-BUILD/SYS-TEST contract gaps are closed by ADR-0007, while implementation evidence remains downstream.

## Required ADRs

### Must complete before coding starts

1. ADR-0002 and ADR-0006 now freeze the 12-leaf authority, public durable-result enum, ending completion boundary, completion event and rollback semantics.
2. Future post-MVP ADR: SYS-TENSION preference ownership and active-timer save/load/rollback matrix; excluded from current Production.
3. ADR-0007 now freezes the Ren'Py 8.5.3 runner capability, candidate manifest,
   canonical encoding, provenance/legal/archive closure, SYS-TEST bidirectional
   evidence stages, test-only isolation, and identity hierarchy.

### Complete before the relevant system is built

5. New ADR: SYS-CHOICE/SYS-NARRATIVE content-lock, CFG, reaction/payoff coverage, and witness validation.
6. New ADR: SYS-JOURNAL bundle schema, read model, refresh, and error taxonomy.
7. New ADR: SYS-ACCESS input equivalence, self-voicing, settings semantics, and authority split.
8. Implement ADR-0007's SYS-BUILD/SYS-TEST contract before the relevant release
   system is built; no additional ADR is required for these five blockers.

### Can defer to implementation

9. SYS-GALLERY CG unlock/read strategy.
10. SYS-AUDIO channel, authorization, and silent-safe fallback strategy.

## Architecture Principles

1. Semantic state, not affection totals.
2. Pure outcome logic, one rollback-owned live state envelope.
3. Positive axis evidence and ordered semantic history are both required ending inputs; history derives bounded event-level counterevidence, not a second positive checklist.
4. Narrative files author meaning; screens only present it.
5. Offline and accessibility constraints are architectural, not release polish.
6. All persistent achievement/ending unlocks happen after completed narrative events.
7. SYS-ACCESS owns the only player-facing font-scale/high-contrast authority；Ren’Py engine font/high-contrast and its built-in accessibility menu are disabled in production, while `V`/`Shift+C` remain gated output-only shortcuts.
8. Nonvisual support claims apply only to declared Windows 10/11 configurations with a verified usable Simplified Chinese SAPI voice；clipboard voicing is external assistive-technology interoperability, not a bundled TTS guarantee.

## Open Questions

| ID | Summary | Priority | Resolution |
|---|---|---|---|
| QQ-01 | Final Chinese font and redistribution rights | High before public build | Asset review |
| QQ-02 | Exact high-contrast palette and scale steps | Medium before vertical slice | UX spec/playtest |
| QQ-03 | Whether optional tension mode belongs in first release | Resolved for current scope | Deferred to post-MVP; no current persistent setting or timed gate |
| QQ-04 | Separation boundary for future MIT framework repository | Medium before publication | Licensing ADR |
| C-01 | SYS-PERSIST authority split | Closed 2026-08-09 | Single 12-leaf authority; legacy references removed from normative contracts; targeted closure matrix |
| C-02 | `commit_ending_completion` owner, callsite, event, and rollback semantics | Closed 2026-08-09 | ADR-0006 and synchronized GDD/Registry/SYS-TEST contracts |
| C-03 | SYS-TENSION preference storage owner/path | Deferred, not current blocker | SYS-TENSION post-MVP; no sixth setting or current Production gate |
| C-04 | Timed active-phase save/load/rollback matrix | Deferred, not current blocker | SYS-TENSION post-MVP; future SYS-SAVE amendment required before re-entry |
| ENG-01 | Required Ren'Py 8.5.3 reference modules were missing locally | Closed | `docs/engine-reference/renpy/modules/scripting.md`, `breaking-changes.md`, and `deprecated-apis.md` verified against the pinned SDK on 2026-08-10 |
