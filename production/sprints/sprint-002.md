# Sprint 2 — 2026-08-24 to 2026-09-06

## Sprint Goal

Deliver the playable, asset-admitted, route- and accessibility-validated Day 3
unit `chapter_day3_empty_school`, without expanding the Day 1-only partial
flow manifest or terminal-witness scope.

## Capacity

- Total days: 14
- Buffer (20%): 3 days
- Available: 11 days
- Planned critical-path effort: 4 days
- Review mode: Solo

## Must Have

| ID | Task | Owner | Est. days | Dependencies | Acceptance criteria |
|---|---|---:|---:|---|---|
| S2-01 | Day 3 authored source and causal bindings | Andwey | 2 | Sprint 1 complete; Day 2 source remains current | Add `game/chapters/day3.rpy::chapter_day3_empty_school`; implement only the three baseline scenes and four approved Day 3 choice/reaction/payoff bindings; record source hash and player-safe catalog inputs. |
| S2-02 | Day 3 asset admission records | Andwey | 1 | S2-01 | Inventory every actual Day 3 runtime asset with provenance, licence, SHA-256, stable runtime path, and self-voicing/semantic binding; explicitly mark planned or missing assets as not admitted. |
| S2-03 | Day 3 route, accessibility, and evidence validation | Andwey | 1 | S2-01, S2-02 | Engine routes cover both Day 3 choice nodes and reach the Day 3 handoff; keyboard, 1280x720, silent/reduced-motion, and 1.5x/high-contrast evidence pass and is bound to the current source hash. |

## Should Have

None. Remaining capacity is retained as delivery buffer; it must not be used to
add later-day content, partial-manifest entries, or terminal witnesses.

## Nice to Have

None.

## Carryover from Previous Sprint

| Task | Reason | New Estimate |
|---|---|---:|
| None | Sprint 1 completed on 2026-08-11. | — |

## Day 3 Source Contract

- **Unit and responsibility:** `chapter_day3_empty_school` / `responsibility_day3_evidence_and_pause`.
- **Required scenes:** `scene_day3_classroom_trace`, `scene_day3_evidence_choice`, and `scene_day3_truth_pace_answer`.
- **Exact choice set:** `day3_share_school_evidence`, `day3_hide_school_evidence`, `day3_honor_pause`, and `day3_force_explanation`, with their baseline-defined immediate reactions and strictly later payoff IDs.
- **Required local completion:** cross-validation of the empty-school trace is perceptibly presented before `event_empty_school_trace_confirmed` / `cp_day3_empty_school_trace_complete` is recorded.
- **Source boundary:** chapter prose and local branches belong in `game/chapters/day3.rpy`; screens render state but never choose an outcome. Record the source SHA-256 and player-safe chapter/memory catalog inputs in a Day 3 authored-source evidence record.
- **Narrative boundary:** no player-visible axes, tokens, resources, qualifications, route predictions, internal IDs, ending hints, persistent state, or test-fixture language. Erii's complex intent remains action-, object-, gaze-, and context-led rather than full explanatory dialogue.

## Route and Accessibility Validation Contract

- Add source/data checks at `tests/unit/sys_narrative/day3_authored_source_test.py` and engine/integration coverage at `tests/integration/sys_narrative/day3_content_validation_test.py` plus `game/testcases.rpy`.
- From a Day 2-compatible setup, exercise share/withhold evidence and honor/force pace combinations through keyboard activation, asserting exact canonical histories, availability, immediate reactions, the Day 3 handoff, and no traceback.
- Capture every critical Day 3 choice surface at the physical 1280x720 keyboard-only, silent, reduced-motion baseline and at 1.5x font, high contrast, reduced motion. Captions must be visible and readable, focus must be distinct and keyboard-operable, and critical input must not expose a quick-menu focus target.
- No decision-relevant fact may depend solely on colour, hover, audio, motion, or a presentation effect. Silent and reduced-motion configurations may change presentation only, never canonical IDs, availability, reactions, or continuation.
- Preserve runner output, result record, capture metadata, screenshots, content review, and source hash under `production/qa/evidence/day3-content-validation-<date>/`.

## Asset Admission Contract

- Reuse ADR-0003 stable semantic asset names; do not embed mutable asset paths throughout prose.
- For every actual runtime asset referenced by Day 3, record source/provenance, licence, SHA-256, verified runtime path, asset ID, and planned self-voicing alternative-text or semantic binding in both the asset inventory and legal register.
- Do not admit an intended, missing, generated, unregistered, or unused asset. Do not add final character art, CGs, external images, audio, or video merely to fill the chapter.

## Explicitly Out of Scope

- Any change to `game/modules/narrative_partial_manifest.py`, `narrative_partial_day1_manifest:v1`, or a new Day 3 partial-manifest schema.
- Full 15-unit manifest construction, terminal continuation witnesses, ending-entry validation, resolver changes, qualification coverage, or release/terminal evidence.
- Day 4–Day 7 prose, ending or epilogue production, UI information-architecture redesign, final art/audio production, gallery work, and release packaging.

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Day 3 prose changes a locked choice/reaction/payoff identity or source hash | Medium | High | Exact source-data tests, hash-bound evidence, and baseline review before route validation. |
| Classroom-trace or pause meaning becomes dependent on presentation | Medium | High | Assert text/keyboard paths in silent, reduced-motion, and high-contrast captures. |
| Unregistered placeholder or generated asset enters the runtime path | Medium | Medium | Admission record checks actual references only; absent assets remain explicitly unadmitted. |
| Scope drifts into manifest or terminal-witness work | Medium | High | Fail tests if Day 3 is added to the Day 1-only partial manifest; review evidence only to the Day 3 handoff. |

## Dependencies on External Factors

- None. The existing Ren'Py 8.5.3 test runner and Day 1/Day 2 route harness remain the verification baseline.

## Definition of Done for this Sprint

- [ ] All Must Have tasks are complete.
- [ ] Day 3 contains exactly one approved unit, three required scenes, and four approved choice/reaction/payoff bindings, with no baseline expansion.
- [ ] Source hash, player-safe catalog record, asset admission records, and route/accessibility evidence identify the same content generation.
- [ ] All actual runtime assets are admitted; missing or planned assets are explicitly not admitted.
- [ ] Unit, integration, global Ren'Py, lint/compile, and content-constraint checks pass.
- [ ] All critical Day 3 choices are visible, readable, focused, and keyboard-operable at both required accessibility baselines; no critical quick-menu focus target is present.
- [ ] No S1 or S2 defect remains open in the delivered Day 3 route.
- [ ] No Day 3 data is added to the Day 1-only partial manifest, and no terminal-witness or ending-validation claim is made.
- [ ] A Sprint 2 QA plan exists before implementation begins.

> ⚠️ **No QA Plan**: This sprint was created without a QA plan. Run `/qa-plan sprint` before implementing the first story. QA sign-off cannot proceed without it.

> **Scope check:** This sprint deliberately excludes work beyond the Day 3 production unit. Run `/scope-check sys-narrative` before implementation if any later-day, partial-manifest, or terminal-witness story is proposed.
