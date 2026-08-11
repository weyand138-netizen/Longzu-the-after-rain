# Story 006: Day 3 Authored Source and Causal Bindings

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production  
> **Status**: Complete  
> **Layer**: Feature  
> **Type**: Config/Data  
> **Estimate**: 2 days  
> **Manifest Version**: 2026-08-04.1  
> **Last Updated**: 2026-08-11

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`  
**Requirement**: `TR-NAR-006` — the canonical Day 3 authored source declares
the empty-school scenes, exact bindings, perceptible trace completion, and
player-safe provenance without partial-manifest or terminal-scope expansion.

**Governing ADRs**: ADR-0008 (primary), ADR-0003, ADR-0006 (boundary only)  
**Engine**: Ren'Py 8.5.3 | **Risk**: High

**Engine Notes**: No post-cutoff runtime API is introduced. Standard Ren'Py
labels and choice surfaces are verified by lint/compile, the global testcase
suite, source-hash validation, and the content-constraint scan.

**Control Manifest Rules (Feature layer)**:

- Required: keep the chapter in its own stable-label file; classify each
  player-facing choice; commit through SYS-CHOICE before an immediate reaction;
  give each choice a causally bound, strictly later payoff.
- Required: express Erii through body language, gaze, objects, context, or a
  simple monosyllable; register narrative-complete events only after their
  perceptible completion.
- Forbidden: duplicate global ending conditions, expose internal
  axis/token/qualification state, or turn Erii's response into full spoken or
  narrated internal-monologue text.
- Performance: no runtime source scan, CFG construction, or path enumeration;
  these remain build/test work only.

**Normative source**: `design/narrative/seven-day-content-baseline.md`,
`narrative_content_baseline:v1.2`: unit `chapter_day3_empty_school`,
responsibility `responsibility_day3_evidence_and_pause`, and required scenes
`scene_day3_classroom_trace`, `scene_day3_evidence_choice`, and
`scene_day3_truth_pace_answer`.

## Acceptance Criteria

- [ ] Add `game/chapters/day3.rpy::chapter_day3_empty_school` without changing
  the baseline's exact 15-unit set.
- [ ] Implement the three required Day 3 scenes. The empty-school trace is
  cross-validated and perceptibly presented before
  `event_empty_school_trace_confirmed` and
  `cp_day3_empty_school_trace_complete` are recorded.
- [ ] Expose exactly these Day 3 choice IDs in their two baseline-defined
  sibling nodes: `day3_share_school_evidence`,
  `day3_hide_school_evidence`, `day3_honor_pause`, and
  `day3_force_explanation`.
- [ ] Bind every choice to its exact immediate reaction and strictly-later
  payoff identity: `payoff_day3_share_day5`, `payoff_day3_hide_day5`,
  `payoff_day3_pause_day5`, and `payoff_day3_force_day6`, respectively.
- [ ] Model `agency_day3_truth_pace` as the existing request/answer contract:
  `day3_honor_pause` accepts the registered pause answer and
  `day3_force_explanation` overrides it. Do not expose this internal contract
  to players.
- [ ] Record a Day 3 source SHA-256 and player-safe chapter/memory catalog
  inputs referring to the exact same source generation.
- [ ] Keep player-visible copy free of axes, tokens, resources,
  qualifications, route predictions, internal IDs, ending hints, persistent
  state, and test-fixture language. Erii's complex intent must remain
  action-, object-, gaze-, and context-led.

## Implementation Notes

- ADR-0003 requires a separate stable-label chapter file. Screens render
  state only; they never decide an evidence or pace outcome.
- Commit the canonical choice through SYS-CHOICE before presenting the
  immediate reaction. Each reaction completes before continuation and each
  payoff is strictly later and perceptible.
- Runtime consumes authored content only. Source scanning, hash calculation,
  CFG inspection, and path enumeration remain build/test responsibilities.
- ADR-0006 reserves ending completion to SYS-ENDING. This Day 3 chapter must
  not call ending entry or completion APIs.

## Out of Scope

- Day 3 runtime asset admission, route validation, screenshots, and evidence
  packaging; Stories 007 and 008 own those deliverables.
- `narrative_partial_day1_manifest:v1`, any Day 3 partial-manifest schema,
  full 15-unit manifest construction, terminal witnesses, ending entry,
  resolver, qualification, or release work.
- Day 4 through Day 7, endings, epilogue, final art/audio, or UI redesign.

## QA Test Cases

- **AC-1: Unit, scene, and binding coverage**
  - Given: the frozen baseline and Day 3 source scanner.
  - When: it enumerates production units, scene markers, choices, reactions,
    and payoff bindings.
  - Then: it finds only `chapter_day3_empty_school`, the three required scenes,
    and the four approved bindings with their exact later payoff IDs.
  - Edge cases: missing/duplicate IDs, unresolved references, a generic or
    same-scene payoff, or an extra production unit fails closed.
- **AC-2: Perceptible trace completion and source provenance**
  - Given: the completed Day 3 source and its source-hash/catalog record.
  - When: source-order and provenance checks run.
  - Then: perceptible trace confirmation precedes the event/checkpoint and the
    hash/catalog inputs identify the same generation.
  - Edge cases: stale hash, source revision, early event, or mismatched catalog
    record fails validation.
- **AC-3: Content and boundary constraints**
  - Given: all Day 3 player-visible strings and production references.
  - When: the content-constraint and manifest-boundary scans run.
  - Then: forbidden internal wording and full explanatory Erii dialogue have
    zero matches; no Day 3 partial-manifest, terminal witness, ending entry,
    or production-to-test-only reference exists.
  - Edge cases: any prohibited reference or text fragment fails validation.

## Test Evidence

- `tests/unit/sys_narrative/day3_authored_source_test.py`
- `tools/test-content-constraints.ps1`
- `production/qa/evidence/day3-authored-source-evidence.md`

## Dependencies

- Depends on: Story 005's Day 2 source and route evidence remain current.
- Unlocks: Story 007 and Story 008.

## Completion Notes

**Completed**: 2026-08-11  
**Criteria**: 7/7 passing.  
**Classification**: Corrected from Integration to Config/Data: this story owns
authored source, source provenance, and pure canonical-history projection;
Story 007 exclusively owns engine-route and accessibility integration evidence.
**Deviations**: The required pure Day 3 token projection was added so the
baseline-defined hide-evidence and force-explanation consequences are not inert.
It adds no partial manifest, terminal witness, ending, asset, or route evidence.
**Test Evidence**: `tests/unit/sys_narrative/day3_authored_source_test.py`
(19 focused Day 2/Day 3 source tests passing),
`tools/test-content-constraints.ps1`, Ren'Py `lint --compile`, and
`production/qa/evidence/day3-authored-source-evidence.md`.  
**Code Review**: Approved after corrective review.
