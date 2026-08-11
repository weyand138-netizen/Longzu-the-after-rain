# Sprint 1 — 2026-08-10 to 2026-08-23

**Sprint Status**: Complete (2026-08-11)

## Sprint Goal

Begin formal content production by delivering the playable, manifest-validated Day 1 narrative unit without expanding P1 scope or admitting unregistered assets.

## Capacity

- Total days: 14
- Buffer: 3 days
- Available: 11 days
- Review mode: Solo

## Must Have

| ID | Task | Owner | Est. days | Dependencies | Acceptance criteria |
|---|---|---:|---:|---|---|
| S1-01 | [Day 1 authored source and causal beats](../epics/sys-narrative/story-001-day1-authored-source.md) | Andwey | 2 | ADR-0008 | Day 1 source, approved IDs, source hash, no hidden-state copy |
| S1-02 | [Day 1 flow manifest and reachability witness](../epics/sys-narrative/story-002-day1-flow-manifest.md) | Andwey | 1 | S1-01 | Exact joins, one valid continuation, no test-only edge |
| S1-03 | [Day 1 content validation and accessibility evidence](../epics/sys-narrative/story-003-day1-content-validation.md) | Andwey | 1 | S1-02 | Engine route test, accessibility captures, validated evidence bundle |

## Should Have

| ID | Task | Owner | Est. days | Dependencies | Acceptance criteria |
|---|---|---:|---:|---|---|
| S1-04 | Day 1 asset admission records | Andwey | 1 | S1-01 | **Complete 2026-08-10.** Every actual Day 1 runtime asset is inventoried with source, licence, SHA-256, runtime path, and accessibility binding; planned/missing files are explicitly not admitted. |

## Explicitly Out of Scope

- SYS-TENSION, timed choices, sixth setting, timer recovery, audio production, gallery, and release packaging.
- Unregistered external/generated art, final character art, CGs, or new player-visible prose outside Day 1.

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Day 1 prose changes a locked causal identity | Medium | High | Validate against ADR-0008 and baseline before implementation |
| Accessibility layout regresses at 1.5x | Medium | High | Capture all required baselines before closure |
| Scope spreads into later days or P1 | Medium | Medium | Keep all non-Day-1 work in backlog |

## Definition of Done

- [x] All Must Have stories are Complete.
- [x] Sprint QA plan exists before any `dev-story` work begins.
- [x] Ren'Py global tests, lint/compile, content constraints, and new Day 1 checks pass. (2026-08-11: 13/13 testcases and 64/64 assertions passed after the visual baseline harness pinned the physical 1280x720 surface and disabled persisted clipboard voicing.)
- [x] No S1/S2 defect is open in the Day 1 route.
- [x] Source hash, manifest, witness, visual evidence, and review records identify the same content generation.

## S1-04 Completion Record

- **Completed**: 2026-08-10
- **Scope**: actual Day 1 runtime references in `game/chapters/day1.rpy`,
  `game/screens.rpy`, `game/00_resources.rpy`, and `game/assets/`.
- **Result**: one admitted font file and two admitted code-defined Ren'Py
  primitives; no external image, audio, video, character-art, CG, or prop file
  is referenced by Day 1.
- **Records**: `design/assets/entity-inventory.md` and
  `docs/legal/asset-register.md` now carry the provenance/licence,
  SHA-256, verified runtime path, and accessibility semantic binding for each
  admitted asset. Intended PNG/prop/UI files that do not exist are recorded as
  not present and not admitted.
- **Consistency result**: PASS — inventory and legal-register IDs, hashes,
  paths, admission states, and semantic bindings exactly agree.
- **Initial verification**: 30 targeted Python tests and the content-constraint
  scan passed. The initial Ren'Py re-run exposed a physical-surface/clipboard
  preference leak in `day1_accessibility_visual_baselines`; the corrected final
  Sprint run is recorded in the completion record below.

## Sprint Completion Record

- **Completed**: 2026-08-11
- **Gate result**: PASS. All four Sprint 1 stories are done and every
  Definition-of-Done item is checked.
- **Final verification**: Ren'Py global test suite 13/13 testcases and 64/64
  assertions; 30 targeted Day 1 Python tests; content-constraint scan; and
  Ren'Py lint/compile all passed.
- **Evidence**: `production/qa/smoke-sprint-001-2026-08-11.md`.
