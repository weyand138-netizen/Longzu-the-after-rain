# Control Manifest

> **Engine**: Ren'Py 8.5.3  
> **Last Updated**: 2026-08-04  
> **Manifest Version**: 2026-08-04.1  
> **ADRs Covered**: ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0005  
> **Status**: Active

## Foundation Layer Rules

### Required

- Default `semantic_state` and `state_schema_sentinel` to `None`; only explicit new-game initialization may create schema 2 state. — ADR-0002/0005
- Use exactly one product field, `default persistent.sys_persist_state`, built as an exact schema-v2 root with 12 normative leaves, including the canonical five-setting tuple `font_scale, high_contrast, reduced_motion, flash_effects_enabled, screen_shake_enabled`. — ADR-0002 / SYS-ACCESS
- Treat flat prototype fields and local `0.1.0-dev` saves as incompatible development artifacts；after public release, any persistent schema change requires a version bump and migration ADR. — ADR-0002
- Keep Ren’Py engine font multiplier at `1.0`, engine high-contrast text off, and built-in accessibility menu/`Shift+A` absent from production. `V` and `Shift+C` may only switch output channels and must never bypass the current action gate. — SYS-ACCESS
- Claim independent nonvisual support only for declared Windows 10/11 configurations with a verified usable Simplified Chinese SAPI voice. Do not treat visual error copy or optional clipboard output alone as a nonvisual PASS. — SYS-ACCESS
- Route every changing unlock/settings/mark-seen batch through SYS-PERSIST: one complete-root replacement, one required flush, then projection/presentation. — ADR-0002
- Increment `collection_epoch_id` on collection reset; only max-epoch roots participate in collection merge, and explicit New Game copies the current epoch into the run envelope. — ADR-0002
- Keep save state limited to primitives and Ren'Py-managed collections. — ADR-0002
- Run lint, pure logic tests, and route testcases before hand-off. — ADR-0001

### Forbidden

- Never put file handles, sockets, generators, tasks, or displayables in save state. — ADR-0002
- Never use external JSON as the primary save system. — ADR-0002
- Never introduce network or telemetry dependencies. — technical preferences
- Never resume a legacy, unsupported, or corrupt loaded state; disable rollback/quick save-load/skip/history return and route it only to main menu or explicit new game. — ADR-0002/0005

## Core Layer Rules

### Required

- Update schema, all five axes, and ordered choice history only through strict `apply_choice`. — ADR-0001/0004
- Reject invalid types, schema, keys, formats, duplicates, and ranges; commit a complete candidate through one replacement assignment. — ADR-0004
- Resolve endings only through the pure resolver using the detached axes-plus-history snapshot. — ADR-0001/0004
- Derive bounded event-level counterevidence tokens from history; each repair targets exactly one token. — ADR-0005
- Validate active sentinel before writes/snapshots; traverse schema-known slots only; permit no `__getitem__` or protocol access on unknown values; and order `apply_choice` as global state+payload type sweep, state value/shape, choice-ID value, then delta value/shape/count. — ADR-0004/0005
- Build detached snapshots across the import boundary using only exact ints and detached tuples; never pass live `RunMap`/`RunList` to imported Python. — ADR-0004/0005
- Scan all `game/**/*.rpy` and `game/**/*.py`; close every private builder alias/assignment/pass/return/closure/container/wrapper/reflection reference; allow exactly `game/10_state.rpy::current_ending_snapshot`, prove active validation dominates it, and reject unresolved forms or production-to-test leakage. — ADR-0004/0005
- Prove `L_A(h) ⊆ L_B(h)` for every prehistory before dominance prefix-set comparison; sparse resources use key union/missing zero. — ADR-0005
- Require every token to be repairable with a still-unresolved same-domain witness or an irreversible approval whose author/reviewer identities resolve to different canonical people, plus per-continuation timing, complete registered agency branch-to-outcome mapping, and payoff witnesses. — ADR-0005
- Validate catalog schema/references only at import/build-time, build the index once from immutable tuple records, expose it only through private `MappingProxyType` storage, and keep catalog injection out of the runtime resolver. — ADR-0005
- Validate the exhaustive predicate source/comparator table before freeze and evaluate each reached clause once; cause extraction reads `FrozenResolutionEvaluation` only. — ADR-0001/0005
- Use disjoint clause-template and token-audit lineage keys; populate every payload field from the exhaustive matrix, including earliest-required axis contributors and selected-ending audit lineage. Prove digest bijection in a non-production build checker without replacing `_hashlib`. — ADR-0001/0005
- Freeze exact `ending_rules` module/qualname/field order. Cause extraction accepts only cause-ready `FrozenResolutionEvaluation`; observe stage/clause/wrapper behavior through a source-hash-verified test-only AST copy, never a production seam. — ADR-0001/0004/0005
- Rebuild completed events/resource possession only from ordered history plus the frozen choice projection catalog; derive qualifications from those facts, read no external live state, never persist qualification booleans or create a five-axis proxy checklist, and never gate `rain_stops` with qualifications. — ADR-0001/0005
- Replay frozen per-choice axis projections during catalog coverage and require exact equality with snapshot axes before token fold; freeze threshold contributors from that replay. — ADR-0001/0004/0005
- Restrict qualification sources to pre-terminal commitments/resources/constraints and encode decisive source kind, ID, truth and contributor lineage in cause identity. — ADR-0001/0005
- Validate selected-ending versus terminal-outcome compatibility at content-build time; priority must not hide a fate/ending contradiction. — SYS-ENDING GDD
- Admit only presentation-safe summaries to `display_cause_ids`; keep the postcard constant match audit-only and use a concrete failure/unresolved presentation anchor. — SYS-ENDING GDD/ADR-0001/0005
- Use detectable `ending_flow:v1` lifecycle state, the fixed six-label map, one Day 7 resolver callsite, one ending-entry commit helper and one terminal completion helper per ending label; completion emits the rollback-owned event defined by ADR-0006. — SYS-ENDING GDD/ADR-0001/0005/0006
- Treat both duplicate resource acquire and absent consume as route-fact-fold `ValueError`; prove qualification, priority predicate evaluation, cause extraction and record construction do not run afterward. — ADR-0001/0005
- Close resolver purity against policy v2: explicit leaves, CPython 3.12 implicit opcode/operand pairs, exact record constructors and fixed-code exceptions; every unlisted/custom/native dispatch fails closed. — ADR-0001/0004/0005
- Close the complete transitive resolver callgraph with `UT_PURE + INSTR + STATIC + BRANCH`; allow only detached inputs, locals, frozen immutable catalogs and exact trusted leaves, and reject mutable globals/caches, external state, reflection or unresolved edges. — ADR-0001/0004/0005
- Use only `UT_ENGINE`, `UT_PURE`, `INSTR`, `STATIC`, and `BRANCH` evidence IDs; prove atomic replacement, shared primitives, private export status, reference escape closure, and CFG domination with the evidence host that can observe each claim. — ADR-0004/0005
- Give all six canonical endings matched causes, exact higher-priority exclusions, and concrete payoff scenes. — ADR-0001/0005
- Keep canonical and boundary test vectors with threshold changes. — ADR-0001

### Forbidden

- Never use random values or final-choice overrides in ending resolution. — ADR-0001
- Never clamp or silently repair invalid semantic state. — ADR-0004
- Never use five capped axis integers as the complete ending input. — ADR-0004
- Never add positive `grant` qualifications or let ordinary positive choices clear counterevidence tokens. — ADR-0005
- Never send unknown-target, wrong-domain/mode, irreversible-target, or invalid-reference repair records to runtime; reject them before catalog freeze. Runtime repair failures are limited to target-not-yet-produced/already-resolved history order. — ADR-0005
- Never treat distinct reaction/payoff IDs as semantic value without an approved `semantic_value` registry entry. — ADR-0005
- Never compare counterevidence by token count/effect count or treat incomparable token sets as ordered. — ADR-0005
- Never display axis numbers or convert them into visible affection meters. — ADR-0001
- Never let imported Python modules own live mutable rollback state. — ADR-0002
- Never implement a second ending-decision path in the string compatibility wrapper. — ADR-0001/0005
- Never treat SYS-ENDING core approval as production content lock: exact CHOICE/NARRATIVE bindings, full terminal enumeration, localized summaries and benchmark evidence remain explicit downstream gates. — SYS-ENDING GDD

## Feature Layer Rules

### Required

- Put each chapter in its own file and use stable labels. — ADR-0003
- Classify every production player-facing narrative choice, including timed and accessibility-equivalent choices. For every canonical prehistory and legal terminal continuation, prove immediate reaction execution and a causally bound strictly-later payoff; generic later events are forbidden. — GDD
- Discover every decision-relevant sensory subject—request、answer/refusal、reaction、payoff、ending cause and important audio/environment fact—and exact-join it to one approved accessible summary identity across required variants. Accessible copy may state only registered observable/confirmed facts, must preserve ambiguity and must enter a replayable transcript/backlog before the next decision unlocks. — SYS-ACCESS / SYS-NARRATIVE
- Express Erii's responses through body language, gaze, object interaction, or simple monosyllables only. — GDD
- Grant achievements only after their condition is narratively complete. — ADR-0002
- Keep achievement grants idempotent. — ADR-0002
- Let `SYS-ACHIEVE` own the 11 stable event-condition records; ending/memory memberships are not mirrored as achievements. — GDD
- Keep all locked achievements absent from render/count/focus/self-voicing; use `seen_achievement_ids` only for cross-session “新记录” discovery. — GDD
- Keep names、order、groups and triggers from forming a five-axis/token or good/bad-ending proxy checklist. — GDD

### Forbidden

- Never duplicate global ending conditions in a chapter. — ADR-0001
- Never make an achievement a prerequisite for a story ending. — GDD
- Never let axis、history、token、qualification、resource、ending predicate、backend membership、seen state or popup state become an achievement condition or narrative input. — GDD
- Never give Erii complete spoken sentences or use narration to transcribe a full internal monologue for her. — GDD

## Presentation Layer Rules

### Required

- Support keyboard focus and readable layout at 1280x720. — ADR-0003
- Provide a non-timed path through every scene. — ADR-0003
- Use semantic asset names so placeholders can be replaced safely. — ADR-0003
- Register asset source and planned alternative text before admission. — ADR-0003

### Forbidden

- Never require hover, sound, animation, flashing, vibration, or timed input to progress. — ADR-0003
- Never add official or source-unknown *Dragon Raja* assets. — project policy

## Global Rules

| Element | Convention | Example |
|---|---|---|
| Labels | `snake_case` with chapter prefix | `prologue_station` |
| Variables | `snake_case` | `choice_history` |
| Functions | `snake_case` | `resolve_ending` |
| Constants | `UPPER_SNAKE_CASE` | `ENDING_PRIORITY` |
| Screens | `snake_case` | `wish_journal` |
| Assets | lowercase `snake_case` | `bg_station_rain.webp` |

- Target 60 fps / 16.6 ms interactive frame.
- Standard-library-only Python; no speculative packages.
- UTF-8 throughout.
- Any engine upgrade requires incompatible-change review and full regression.

## Build / Test Boundary Rules

### Required

- Use the verified `engine-capability-manifest:v1` as the only package-runner authority; bind engine version, runner path/hash, command, exit codes, raw output, output markers, timeout, and process-tree cleanup before invoking Ren'Py. — ADR-0007 / SYS-BUILD
- Emit exactly one `candidate_manifest:v1` for each candidate identity and use the frozen sibling layout under `production/releases/<candidate_identity>/`; keep the package in `archive/` and manifests outside the package. — ADR-0007 / SYS-BUILD
- Encode identity and manifest inputs with `canonical_encoding:v1`: UTF-8 without BOM, LF, canonical JSON, stable key/path ordering, exact integers only, and no timestamps or implicit defaults in identity inputs. — ADR-0007
- Keep the identity hierarchy separate: source identity → candidate identity → scoped evidence/archive hashes → release identity. Compute `archive_hash` over exact package bytes only. — ADR-0007 / Registry
- Complete the two release evidence stages: SYS-TEST must bind current RELEASE evidence and a staging exclusion report before package execution, then bind the archive exclusion report and final evidence after package execution. — ADR-0007 / SYS-BUILD / SYS-TEST
- Require legal closure for every shipped asset, including source, permission/license, modification status, attribution, allowlist status, and the exact asset hash. — ADR-0007 / SYS-BUILD
- Require zero test-only, production-to-test-only, network, telemetry, undeclared, and unallowlisted findings in both staging and final archive scans. — ADR-0007 / SYS-BUILD / SYS-TEST

### Forbidden

- Never hash the release directory, a manifest containing `archive_hash`, or any archive member that records the hash of that same archive. — ADR-0007
- Never let production source, staging, archive, formal saves, or persistent payloads import, reference, discover, or receive a runtime seam from test-only code or data. — ADR-0007
- Never combine component, staging, and archive evidence across candidate identities or identity generations, or promote component PASS to RELEASE PASS. — ADR-0007 / SYS-TEST
- Never use native object serialization, locale/platform ordering, floating-point values, timestamps, or auto-filled defaults in identity hashes. — ADR-0007
