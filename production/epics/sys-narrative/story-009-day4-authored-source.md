# Story 009: Day 4 Authored Source and Causal Bindings

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production
> **Status**: Complete
> **Layer**: Feature
> **Type**: Config/Data
> **Estimate**: 2 days
> **Manifest Version**: 2026-08-04.1
> **Last Updated**: 2026-08-11

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`
**Requirement**: `TR-NAR-009` — Canonical Day 4 authored source declares the
seaside-train scenes, exact choice/reaction/payoff and self-controlled-option
bindings, and player-safe source-hash/catalog inputs without partial-manifest
or terminal-scope expansion.

**Governing ADRs**: ADR-0008 (primary), ADR-0003, ADR-0006 (boundary only)
**Engine**: Ren'Py 8.5.3 | **Risk**: High

**Engine Notes**: Standard labels and choice surfaces are verified through
lint/compile, source-hash validation, the content-constraint scan, and the
pinned Ren'Py testcase wrapper. No post-cutoff runtime API is introduced.

**Control Manifest Rules (Feature layer)**:

- Required: keep the chapter in its own stable-label file; classify every
  player-facing choice; commit through SYS-CHOICE before its immediate reaction;
  bind every choice to a strictly later perceptible payoff.
- Required: express Erii through body language, gaze, objects, context, or a
  simple monosyllable; register events only after their perceptible completion.
- Forbidden: duplicate global ending conditions, expose internal state, or add
  full spoken or narrated internal-monologue text for Erii.
- Performance: source scans, CFG construction, and path enumeration remain
  build/test work and add no runtime polling.

**Normative source**: `design/narrative/seven-day-content-baseline.md`,
`narrative_content_baseline:v1.2`: unit `chapter_day4_seaside_train`,
responsibility `responsibility_day4_self_controlled_options`, and its four
required scenes.

## Acceptance Criteria

- [x] `game/chapters/day4.rpy` owns exactly `chapter_day4_seaside_train` with
  `scene_day4_ticket_counter`, `scene_day4_route_answer`,
  `scene_day4_contact_channel`, and `scene_day4_sea_window`.
- [x] It exposes only the five approved Day 4 choice IDs and their exact
  immediate reactions and later payoff identities.
- [x] The route-answer scene perceptibly presents and registers
  `preserve_executable_self_controlled_option` before its related response
  surface; tickets, route map, and contact options remain executable choices.
- [x] Independent contact is guarded by the approved alias outcome and retained
  arcade token; ticket acquisition makes both tickets and identity exposure
  perceptible before its event/checkpoint record.
- [x] Source SHA-256 and player-safe chapter/memory catalog inputs identify the
  same source generation, with no hidden-state wording, Day 1 partial-manifest
  expansion, terminal witness, ending, or later-day scope.

## Implementation Notes

- ADR-0003 requires a separate stable-label chapter file; screens render state
  only and never select an outcome.
- ADR-0008 requires the canonical choice commit before one bounded immediate
  reaction, with every payoff strictly later and perceptible.
- ADR-0006 reserves ending entry and completion to SYS-ENDING; this chapter
  must not call either API.

## Out of Scope

- Day 4 asset admission (Story 011) and route/accessibility evidence (Story
  010).
- Day 5–Day 7 prose, terminal witnesses, endings, resolver changes, or any
  Day 4 partial-manifest schema.

## QA Test Cases

- **AC-1: Unit, scene, and binding coverage**
  - Given: the frozen baseline and Day 4 source scanner.
  - When: it enumerates production units, scenes, choices, reactions, and
    payoff bindings.
  - Then: it finds only the approved unit, four scenes, five choices, and exact
    strictly-later payoffs.
  - Edge cases: missing, duplicate, unapproved, unresolved, or same-scene
    payoff IDs fail closed.
- **AC-2: Self-controlled option and ticket consequence**
  - Given: the Day 4 source and its source-order record.
  - When: answer registration and ticket order are checked.
  - Then: the registered answer precedes every dependent response and identity
    exposure precedes `event_two_window_tickets_acquired`.
  - Edge cases: absent/ambiguous/late answer, resource-only inference, or an
    early event/checkpoint fails validation.
- **AC-3: Provenance and content boundary**
  - Given: source, source hash, catalog inputs, and visible strings.
  - When: provenance and content-boundary checks run.
  - Then: all records identify one source generation and forbidden scope/text
    has zero matches.
  - Edge cases: stale hash, catalog mismatch, hidden state, full Erii dialogue,
    partial manifest, terminal witness, or Day 5+ source fails validation.

## Test Evidence

- `tests/unit/sys_narrative/day4_authored_source_test.py`
- `tools/test-content-constraints.ps1`
- `production/qa/evidence/day4-authored-source-evidence.md`

## Dependencies

- Depends on: Story 007's Day 3 source and route evidence remain current.
- Unlocks: Story 010 and Story 011.

## Completion Notes

**Completed**: 2026-08-11.
**Evidence**: `tests/unit/sys_narrative/day4_authored_source_test.py` reports
7/7 passing; the source-hash evidence record is present.
