# ADR-0010: End-to-End Player Flow Topology

## Status

Accepted

Accepted on 2026-08-16 after focused topology review: the decision matches
Story 024, the exact 15 `canonical_production_units_v1`, and the single
`day7_resolve_ending` → `resolve_ending_record` handoff. This acceptance is an
architecture decision only; it does not close GUI, human witness, SAPI,
semantic, performance, legal, archive, QA, or Production → Polish evidence.

## Date

2026-08-15

## Engine Compatibility

| Field | Value |
|---|---|
| **Engine** | Ren’Py 8.5.3; Python 3.12-compatible scripts |
| **Domain** | Core / Scripting / Narrative flow / Input and Build boundary |
| **Knowledge Risk** | HIGH — pinned 8.5.3 is newer than the May 2025 knowledge baseline |
| **References Consulted** | `docs/engine-reference/renpy/VERSION.md`; `docs/engine-reference/renpy/modules/scripting.md`; `docs/engine-reference/renpy/breaking-changes.md`; `docs/engine-reference/renpy/deprecated-apis.md`; `docs/engine-reference/renpy/BUILD.md`; `docs/engine-reference/renpy/capability-manifest-v1.json`; pinned SDK evidence under `docs/engine-reference/renpy/evidence/` |
| **Post-Cutoff APIs Used** | None introduced by this decision. Existing `renpy.is_in_test()` and the pinned Ren’Py label/call/jump/testcase/build workflow remain subject to current-SDK verification. |
| **Verification Required** | Source/CFG topology scan, full Ren’Py global testcase suite, pinned-SDK lint/compile, content-lock and production/test-edge scans, non-test GUI traversal, six ending witness replay, save/load/rollback evidence, and SYS-BUILD staging/archive identity checks. |

## ADR Dependencies

| Field | Value |
|---|---|
| **Depends On** | ADR-0001 Deterministic Ending Resolution; ADR-0002 Rollback and Persistence Boundary; ADR-0006 Ending Completion Boundary; ADR-0007 SYS-BUILD Contract Closure; ADR-0008 SYS-CHOICE / SYS-NARRATIVE Content Lock and Reachability Boundary; ADR-0009 Partial Day 1 Manifest and Handoff Boundary |
| **Enables** | Sprint 013 Production topology closure; complete seven-day player-flow evidence; six-ending witness replay; SYS-TEST RELEASE evidence; SYS-BUILD archive closure |
| **Blocks** | Production → Polish promotion until the topology, current-build traversal, terminal witness, and candidate/archive evidence are current and pass their owning gates |
| **Ordering Note** | The full `narrative_flow_manifest:v1` and terminal witnesses are required for Production; `narrative_partial_day1_manifest:v1` remains a non-production handoff artifact and must never satisfy this ADR. Any source/catalog/runner/environment identity change invalidates downstream flow evidence. |

## Context

### Problem Statement

The project now has a working Production entry and a fixed chapter sequence in `game/production_orchestrator.rpy`, but the end-to-end topology has not yet been recorded as an accepted architectural decision. Without that decision, the project can accidentally accumulate multiple traversal owners: chapter labels calling later chapters, tests using a different route than normal players, the resolver being invoked from more than one location, or build-time manifests being treated as runtime dispatch data.

Production needs one auditable player route:

```text
Normal New Game
  → Prologue
  → Day 1
  → Day 2
  → Day 3
  → Day 4
  → Day 5
  → Day 6
  → Day 7
  → one deterministic ending handoff
  → one of six ending labels
  → terminal completion
  → only the applicable `rain_stops` tail
```

The current implementation already expresses most of this shape:

- `game/script.rpy` resets a run and calls `production_end_to_end_orchestrator` for non-test start;
- `game/production_orchestrator.rpy` calls the fixed Prologue → Day 1–Day 7 sequence;
- `game/chapters/day7.rpy` jumps once to `day7_resolve_ending`;
- `game/10_state.rpy` owns the six-label map and the resolver handoff;
- `game/chapters/endings.rpy` owns player-visible ending closure and the one completion call per ending.

This ADR formalizes that topology and its boundaries. It does not redesign the already accepted choice, resolver, persistence, journal, achievement, accessibility or build contracts.

### Constraints

- Exactly the 15 canonical production units from the current narrative baseline are in the full production graph.
- `narrative_flow_manifest:v1` remains the only content/reachability handoff between SYS-CHOICE/SYS-NARRATIVE and SYS-BUILD/SYS-TEST.
- The partial Day 1 manifest is never a production, terminal-witness, SYS-BUILD or release input.
- SYS-CHOICE owns canonical choice identity and commit order; SYS-NARRATIVE owns prose, chapter labels, reactions/payoffs and common-path truth.
- SYS-ENDING owns the pure resolver, fixed ending map, ending lifecycle and terminal completion boundary.
- SYS-STATE owns per-run semantic state; SYS-PERSIST is the only writer of product-persistent data; imported Python modules do not own mutable live rollback state.
- SYS-BUILD validates and packages owner outputs; it does not repair source, invent successors, rewrite IDs or become a runtime narrative dispatcher.
- The product is offline, non-commercial, UTF-8 and limited to keyboard/mouse input for this P0 topology; no new formal game assets are part of this decision.
- Ren’Py 8.5.3 behavior is high-risk and must be verified with the pinned SDK, not assumed from older Ren’Py versions.

### Requirements

- Provide exactly one normal-player Production traversal owner.
- Preserve independently callable chapter labels for unit tests, engine testcases, save/load fixtures and approved recovery flows without treating those entry points as alternate player routes.
- Keep runtime control flow static and auditable; do not enumerate or construct the narrative graph at runtime.
- Enter Day 7’s ending handoff exactly once per active run and call the canonical resolver exactly once.
- Map the resolver output through the existing one-to-one six-label map; do not duplicate ending predicates in chapter scripts.
- Keep ending entry, visible closure, completion event and persistent membership in the ADR-0006 order.
- Preserve save/load/rollback semantics across chapter calls, the Day 7 handoff and ending completion.
- Make the topology provable by source scan, manifest, witness replay, engine tests, current-build playtest and SYS-BUILD evidence.
- Avoid runtime startup work that would violate the current performance direction: no CFG enumeration, graph compilation or content scanning during normal player start.

## Decision

Adopt a **single static Production traversal owner** implemented by the Ren’Py label `production_end_to_end_orchestrator`. The orchestrator owns only the fixed end-to-end order; it does not own choice semantics, narrative text, ending predicates, persistence, UI presentation or asset admission.

### 1. Normal start has one Production route

`start` remains the only normal New Game entry. It initializes the rollback-owned run state, then uses the existing test boundary:

```renpy
label start:
    $ reset_run_state()
    if renpy.is_in_test():
        call prologue_start
        return
    call production_end_to_end_orchestrator
    return
```

The `renpy.is_in_test()` branch is a test-runner entry seam only. It is not a player-facing alternate route and must not be used as evidence of full Production coverage. SYS-BUILD/SYS-TEST continue to own test-only isolation and release exclusion.

### 2. The orchestrator owns fixed chapter order only

The Production owner calls the existing chapter labels in this exact order:

```text
prologue_start
→ chapter_day1_her_own_name
→ chapter_day2_two_game_tokens
→ chapter_day3_empty_school
→ chapter_day4_seaside_train
→ chapter_day5_family_lie
→ chapter_day6_no_safe_house
→ chapter_day7_before_red_well
```

Chapter labels remain independently callable by approved tests and fixtures. They must not call later chapter labels to form a second distributed Production topology. Chapter-local menus, choice commits, reaction/payoff joins and event writes remain governed by their owning systems and the `narrative_flow_manifest:v1` contract.

### 3. Day 7 owns the single terminal handoff

Day 7 completes its player-visible beats and performs one `jump day7_resolve_ending`. `day7_resolve_ending` is the only runtime handoff that:

1. validates the active ending lifecycle;
2. obtains the detached ending snapshot;
3. calls `resolve_ending_record(snapshot)` exactly once;
4. validates that the returned `ending_id` exists in the frozen one-to-one `ENDING_LABEL_MAP`;
5. stages the pending ending identity; and
6. jumps to the mapped ending label.

The runtime does not scan the narrative graph, derive a new route topology or read persistent data to choose an ending. All route facts and ending truth come from the accepted SYS-CHOICE/SYS-ENDING contracts and their frozen source/catalog inputs.

### 4. Ending labels preserve the completion boundary

Each of the six mapped ending labels follows the same boundary:

```text
mapped ending label entry
  → commit_ending_entry(expected_ending_id)
  → complete ending narration and player-visible closure
  → commit_ending_completion(ending_id, completion_checkpoint)
  → return / applicable tail
```

`commit_ending_entry` owns only rollback-owned `Active → Ended`. It does not write persistent membership. `commit_ending_completion` is called exactly once at the terminal completion node after the final player-visible closure; it emits the event consumed by SYS-PERSIST. Only `rain_stops` jumps to `epilogue_rain_stops_arcade`. The orchestrator does not call either ending boundary directly.

### 5. Topology truth remains derived from existing owner artifacts

This ADR does **not** create a second runtime graph schema or a second narrative catalog. Topology evidence is derived from:

- the fixed Runtime label/call source;
- the complete `narrative_flow_manifest:v1`;
- SYS-CHOICE canonical choice/reaction/payoff records;
- six ending witness records and terminal-path enumeration;
- SYS-ENDING’s fixed label map and completion callsite scan;
- SYS-BUILD/SYS-TEST candidate and evidence manifests.

A topology report may be generated for QA/release traceability, but it is a derived artifact. It cannot override the owner manifest, add a successor, change a choice, merge terminal classes or turn a partial manifest into a full production input.

### Architecture Diagram

```mermaid
flowchart TD
    A["Normal New Game: start"] --> B["reset_run_state"]
    B --> C{ "renpy.is_in_test()" }
    C -- "test runner only" --> T["prologue_start test entry"]
    C -- "normal player" --> O["production_end_to_end_orchestrator"]
    O --> P["Prologue"]
    P --> D1["Day 1"]
    D1 --> D2["Day 2"]
    D2 --> D3["Day 3"]
    D3 --> D4["Day 4"]
    D4 --> D5["Day 5"]
    D5 --> D6["Day 6"]
    D6 --> D7["Day 7"]
    D7 --> H["day7_resolve_ending: one resolver call"]
    H --> M["ENDING_LABEL_MAP: one-to-one six labels"]
    M --> E["Ending entry and visible closure"]
    E --> K["commit_ending_completion"]
    K --> R{ "ending_id == rain_stops?" }
    R -- "yes" --> W["rain_stops arcade tail"]
    R -- "no" --> X["return from ending"]
    W --> X
```

### Key Interfaces

| Interface | Owner | Contract |
|---|---|---|
| `start` | Runtime / SYS-NARRATIVE entry | Reset run state once; route normal player to the single Production orchestrator; keep test entry behind `renpy.is_in_test()`. |
| `production_end_to_end_orchestrator` | SYS-NARRATIVE runtime flow | Static `call` sequence for Prologue → Day 1–Day 7 only; no resolver, persistent write, UI decision or asset admission. |
| Chapter labels | SYS-NARRATIVE | Independently callable implementation/test units; choices use SYS-CHOICE/SYS-STATE; no distributed chapter-to-chapter Production chain. |
| `narrative_flow_manifest:v1` | SYS-NARRATIVE | Complete build-time source/reachability handoff with 15 units, choices, reaction/payoff joins, successor nodes, terminal entries and witnesses. |
| `day7_resolve_ending` | SYS-ENDING | One active-run handoff; one detached snapshot; one canonical resolver call; one validated fixed-label jump. |
| `resolve_ending_record(snapshot)` | SYS-ENDING | Pure immutable resolver; no Ren’Py store, persistent, UI, file, network, time, randomness or mutable cache access. |
| `ENDING_LABEL_MAP` | SYS-ENDING | Exact frozen priority order and one-to-one ending ID → label map for six endings. |
| `commit_ending_entry` | SYS-ENDING | Only mapped ending label entry; rollback-owned `Active → Ended`; no persistent membership. |
| `commit_ending_completion` | SYS-ENDING | Exactly one terminal completion call after final player-visible closure; produces the completion event consumed by SYS-PERSIST. |
| `candidate_manifest:v1` / `test_evidence_bundle:v1` | SYS-BUILD / SYS-TEST | Bind topology/source/evidence to one candidate identity; staging and archive evidence must be current and exact-match. |

## Alternatives Considered

### Alternative 1: Single static Production orchestrator — **Chosen**

- **Description**: One `production_end_to_end_orchestrator` owns the fixed chapter order. Chapter labels remain reusable units; Day 7 owns the single resolver handoff; ending labels own completion.
- **Pros**: One obvious player path; simple Ren’Py `call`/`return` control flow; easy source/CFG audit; preserves independent testcase entry points; keeps ownership boundaries aligned with existing ADRs; no runtime graph construction.
- **Cons**: A chapter-order change requires editing one central label and rerunning full topology evidence; chapter labels must remain disciplined not to create a second chain.
- **Rejection Reason**: This is the selected approach; the costs are accepted because explicit central ownership is the lowest-risk Production topology for the pinned engine and current content contract.

### Alternative 2: Distributed chapter-to-chapter calls

- **Description**: Each chapter label calls the next chapter and the final chapter calls the resolver.
- **Pros**: Local chapter files appear self-contained; adding a chapter can look like a local edit.
- **Cons**: Creates multiple implicit topology owners; chapter test entry and Production entry become hard to distinguish; call/return stack and rollback evidence become less obvious; accidental alternate paths and skipped units are easier to introduce.
- **Rejection Reason**: Contradicts the single Production traversal owner and makes the full 15-unit reachability contract harder to prove. Chapter labels must remain independently testable without being the distributed Production dispatcher.

### Alternative 3: Runtime graph dispatcher / manifest interpreter

- **Description**: Load `narrative_flow_manifest:v1` at runtime and dynamically enumerate nodes/successors to drive the player.
- **Pros**: Centralized data-driven traversal; topology changes could be represented as data.
- **Cons**: Turns a build-time content contract into runtime execution authority; adds startup parsing/graph construction; complicates Ren’Py rollback/control-location semantics; risks exposing test/content metadata; blurs SYS-NARRATIVE/SYS-CHOICE/SYS-ENDING ownership; requires dynamic/reflection edge analysis in SYS-BUILD.
- **Rejection Reason**: The manifest is explicitly a build-time integration handoff. Existing GDD/ADR rules require runtime labels and owner systems to execute approved content, while SYS-BUILD validates rather than dispatches it.

### Alternative 4: Direct `start` branching to every chapter or ending

- **Description**: `start` chooses a chapter/ending path directly, with no single intermediate orchestrator.
- **Pros**: Fewer visible labels in the initial call chain.
- **Cons**: Duplicates route ownership in the entry point; encourages debug/test shortcuts; makes seven-day progression and terminal witness closure non-central; can bypass chapter boundary and completion rules.
- **Rejection Reason**: Violates the required fixed chapter order and makes the Production path less auditable.

## Consequences

### Positive

- The normal player path has one static, source-auditable owner.
- Existing chapter labels stay reusable for focused engine tests and approved recovery fixtures without becoming alternate player routes.
- Day 7 resolver, six ending labels and completion boundaries remain aligned with ADR-0001 and ADR-0006.
- Save/load/rollback evidence can name stable control locations and one known traversal sequence.
- SYS-BUILD and SYS-TEST can verify topology from current source/manifests without executing a runtime graph interpreter.
- The topology does not require new formal art, audio, voice or other game assets.

### Negative

- The central orchestrator is a deliberate change point; chapter-order edits require full topology and player-flow evidence.
- Test entry labels and the normal Production entry must be kept visibly and statically separate.
- The topology decision does not by itself prove actual player comprehension, accessibility, SAPI behavior, copyright boundary, performance or release readiness; those remain downstream evidence gates.
- A source-level fixed order cannot replace complete witness/path enumeration; both are required.

### Risks and Mitigations

- **Ren’Py call/jump/return semantics differ across SDK versions.** Mitigation: use the pinned 8.5.3 SDK, global testcase suite, lint/compile and a non-test GUI traversal; do not infer behavior from older versions.
- **A chapter adds a hidden second handoff.** Mitigation: static scan for chapter-to-chapter calls, exactly one Day 7 handoff and exactly one normal orchestrator caller.
- **Test entry is mistaken for Production coverage.** Mitigation: tag test-only entry evidence separately, require current non-test GUI evidence and run SYS-BUILD/SYS-TEST exclusion scans.
- **The manifest becomes a second runtime truth.** Mitigation: keep `narrative_flow_manifest:v1` build-time only; runtime source labels and owner APIs remain authoritative for execution, while source/manifest mismatch fails closed.
- **Completion is granted too early.** Mitigation: preserve ADR-0006’s six terminal callsite checks and verify pre-completion request/flush counts are zero.
- **A content/hash change invalidates previous flow evidence.** Mitigation: bind all artifacts to source/catalog/config/runner/environment identity and mark old artifacts `STALE`.
- **Runtime graph enumeration or hidden metadata increases startup cost or leaks internal state.** Mitigation: no runtime scan/interpreter; use precomputed/compiled owner outputs and build-time validation only.

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|---|---|---|
| `seven-day-chapter-script.md` | Seven-day chapter order, complete valid paths, exact 15-unit production baseline and six ending reachability | Assigns one static Production owner for Prologue → Day 1–Day 7 and requires the complete `narrative_flow_manifest:v1`/witness set. |
| `choice-and-causality-record.md` | Every player-facing choice commits through SYS-STATE with exact reaction/payoff and continuation coverage | Keeps chapter labels as content units and requires choices to use existing SYS-CHOICE/SYS-STATE interfaces; the orchestrator never invents joins. |
| `deterministic-ending-resolution.md` | One Day 7 resolver, one-to-one six-label map, pure resolver and unique terminal completion nodes | Makes `day7_resolve_ending` the only ending handoff and preserves `ENDING_LABEL_MAP`, `commit_ending_entry` and `commit_ending_completion` ownership. |
| `save-load-rollback.md` | Stable control locations, rollback-owned run state, safe loads and completion restore | Uses static label locations, no runtime graph dispatcher and the existing rollback/persistence boundary across the full flow. |
| `cross-playthrough-unlocks.md` | Ending/memory/achievement unlock only after completed player-visible events | Keeps the orchestrator out of persistence and requires completion to occur at each ending’s terminal node before SYS-PERSIST projection. |
| `sys-journal.md` | Journal consumes approved catalogs/read models and cannot rewrite narrative truth | Journal remains a downstream consumer of completed events and manifests, never a topology owner. |
| `local-achievements.md` | 11 event-based achievements with exact completion checkpoints and idempotent persistence | The topology exposes completed events in the approved order while leaving achievement conditions and persistence to SYS-ACHIEVE/SYS-PERSIST. |
| `sys-access.md` / `accessibility-requirements.md` | Keyboard/mouse flows, focus, viewport, silent-safe and semantic-equivalent presentation | The fixed flow must be executable through the approved input/screen contracts; it adds no hidden visual-only or hover-only control path. |
| `sys-build.md` | Owner-manifest validation, test-only isolation, candidate/archive identity and offline packaging | Topology is a validated source/manifest input; SYS-BUILD packages it without rewriting or interpreting runtime graph data. |
| `sys-test.md` | Exact evidence types, complete terminal path coverage, current identity and human/engine gate separation | Defines source/engine/witness/playtest/archive checks and prevents test-entry or component PASS from masquerading as Production/RELEASE PASS. |

## Performance Implications

- **CPU**: Normal runtime uses a bounded sequence of Ren’Py label calls and one Day 7 resolver call. It performs no runtime CFG enumeration, manifest scan or graph compilation. Resolver cost remains governed by ADR-0001’s pure-function complexity and its own downstream benchmark; the 16.6 ms frame budget is not automatically assigned to the resolver.
- **Memory**: No runtime topology graph is allocated. Chapter/runtime state remains in Ren’Py rollback-owned state; imported Python modules remain stateless with respect to live mutable game state. The current base-memory target remains below 1 GB excluding platform overhead.
- **Load Time**: No topology work is added to normal startup beyond the existing static script loading; the current main-menu target remains visible within 5 seconds on minimum target hardware. Any candidate build must verify this on the approved environment.
- **Network**: None. The flow is offline and has no network, telemetry, analytics or crash-upload dependency.

## Migration Plan

The current implementation is already close to this decision, so migration is primarily a closure and evidence task rather than a runtime rewrite:

1. Treat `game/production_orchestrator.rpy` and `game/script.rpy` as the implementation baseline; do not introduce a second orchestrator.
2. Add/update source and integration tests that assert one normal Production caller, exact chapter order, one Day 7 handoff, six-label mapping and no distributed chapter chain.
3. Generate a derived topology evidence report from current source, complete `narrative_flow_manifest:v1`, witnesses and ending callsite scans. Do not introduce a runtime topology schema.
4. Re-run all 15-unit/content-lock/source-hash checks and reject `narrative_partial_day1_manifest:v1` wherever a full Production input is required.
5. Run current-build non-test GUI traversal, Day 1–Day 7 flow, six ending witnesses, save/load/rollback, accessibility and performance evidence under one candidate identity.
6. Bind staging and archive evidence through the existing SYS-BUILD/SYS-TEST two-stage contract.
7. After this ADR is Accepted and the evidence is current, update the master architecture ADR reference list and any registry `referenced_by` fields through a separately reviewed architecture-sync change. This ADR does not modify the registry automatically.

## Validation Criteria

### Static and source validation

- `start` has exactly one non-test call to `production_end_to_end_orchestrator`.
- `production_end_to_end_orchestrator` has exactly the fixed Prologue → Day 1–Day 7 call order and no resolver/persistent/UI/asset side effect.
- Chapter labels have no distributed Production calls to later chapters.
- Day 7 has exactly one `jump day7_resolve_ending` and no alternate terminal handoff.
- `ENDING_LABEL_MAP` contains exactly the six frozen IDs in priority order, maps one-to-one to existing labels, and has no runtime guessing fallback.
- Each ending label has exactly one entry call and exactly one terminal completion call after visible closure; only `rain_stops` jumps to its existing tail.
- The complete 15-unit `narrative_flow_manifest:v1`, terminal witnesses and source hashes exact-match the current baseline; partial Day 1 artifacts are rejected by full-production/build/release validators.
- Production-to-test-only dependency count, network dependency count and telemetry entry count are zero.

### Engine and automated validation

- Pinned Ren’Py 8.5.3 global testcase suite passes through `tools/run-renpy-tests.ps1`.
- Ren’Py 8.5.3 `lint --compile` passes; Python tests, content constraints and `git diff --check` pass.
- Existing and planned coverage includes `tests/integration/sys_narrative/production_orchestrator_test.py`, `tests/integration/sys_ending/terminal_lifecycle_source_test.py`, `ending_closure_source_test.py` and `terminal_traceability_test.py`.
- Six canonical ending vectors and exclusivity checks pass; resolver is called once and does not read persistent/UI/environment/random state.
- Save/load/rollback restores control location, lifecycle and completion event correctly without removing flushed persistent membership.

### Human and release validation

- A clean non-test current build traverses Day 1–Day 7 without debug/test assistance.
- Six canonical ending witnesses are replayed from New Game or approved production checkpoints and produce the intended visible closure.
- Keyboard-only and mouse-only critical paths, accessibility matrix, SAPI/transcript, semantic-equivalence review and player comprehension are current and separately adjudicated.
- Performance uses the approved current-build protocol and thresholds; missing thresholds remain `REPORT_ONLY` and block the relevant gate.
- DOCX/source/rights provenance is present or explicitly remains `BLOCKED_INPUT`; no legal PASS is fabricated.
- SYS-BUILD staging/archive candidate identity, source/catalog/asset/legal/evidence hashes, archive hash and both exclusion reports are exact-match.
- Final Production → Polish gate reports PASS/CONCERNS/FAIL without automatically changing `production/stage.txt`.

## Related Decisions

- [ADR-0001: Deterministic Ending Resolution](adr-0001-deterministic-ending-resolution.md)
- [ADR-0002: Rollback and Persistence Boundary](adr-0002-rollback-and-persistence-boundary.md)
- [ADR-0003: Content and Presentation Boundary](adr-0003-content-and-presentation-boundary.md)
- [ADR-0006: Ending Completion Boundary](adr-0006-ending-completion-boundary.md)
- [ADR-0007: SYS-BUILD Contract Closure and Release Identity](adr-0007-sys-build-contract-closure.md)
- [ADR-0008: SYS-CHOICE / SYS-NARRATIVE Content Lock and Reachability Boundary](adr-0008-choice-narrative-content-lock.md)
- [ADR-0009: Partial Day 1 Manifest and Handoff Boundary](adr-0009-partial-day1-manifest-and-handoff-boundary.md)
- `docs/architecture/architecture.md`
- `docs/registry/architecture.yaml`
- `game/script.rpy`
- `game/production_orchestrator.rpy`
- `game/10_state.rpy`
- `game/chapters/day7.rpy`
- `game/chapters/endings.rpy`
