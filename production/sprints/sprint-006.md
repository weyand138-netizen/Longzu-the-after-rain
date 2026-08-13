# Sprint 6 — 2026-10-19 to 2026-11-01

## Sprint Goal

Deliver the source-locked, asset-admitted, accessible, and failure-closed Day 7
unit `chapter_day7_before_red_well`, which acknowledges only Days 1-6 and
hands off through the unique owned SYS-ENDING resolver, without entering six-
ending prose/completion, the true-ending epilogue, full-manifest, release, or
stage-promotion scope.

## Capacity

- Total days: 14
- Buffer (20%): 3 days
- Available: 11 days
- Planned critical-path effort: 5 days
- Planned supporting effort: 1 day
- Review mode: Solo

## Tasks

### Must Have (Critical Path)

| ID | Task | Owner | Est. Days | Dependencies | Acceptance Criteria |
|---|---|---:|---:|---|---|
| S6-01 | Day 7 authored source and resolver handoff | Andwey | 2 | complete SYS-ENDING terminal adapter | Three frozen scenes, no new state facts, one owned handoff. |
| S6-02 | Day 7 asset admission records | Andwey | 1 | S6-01 | Every actual reference is admitted; no new external/final identity. |
| S6-03 | Day 7 handoff and accessibility validation | Andwey | 2 | S6-01, S6-02 | Six histories, exact preservation, failure closure, both accessibility baselines. |

### Should Have

| ID | Task | Owner | Est. Days | Dependencies | Acceptance Criteria |
|---|---|---:|---:|---|---|
| S6-04 | Day 7 story and evidence traceability | Andwey | 1 | S6-01–S6-03 | One verified Day 7 generation with no later-scope claim. |

### Nice to Have

None. Retained capacity must not begin ending prose/completion, true epilogue,
full-manifest, release, or stage work.

## Scope Check

**Verdict: CONCERNS — scope delta is 0%, but all Day 7 stories are blocked by
the missing owned SYS-ENDING terminal adapter and real label targets.** See
`production/qa/evidence/scope-check-sprint-006-day7-2026-08-13.md`.

## Day 7 Source Contract

- **Unit and responsibility:** `chapter_day7_before_red_well` /
  `responsibility_day7_acknowledge_and_resolve`.
- **Required scenes:** `scene_day7_red_well_approach`,
  `scene_day7_causal_recall`, and `scene_day7_ending_entry`.
- **State boundary:** Day 7 replays and acknowledges prior visible facts only.
  It creates no choice, axis change, repair/revoke, qualification, route
  resource, ending predicate input, persistence result, achievement, journal
  result, or ending completion event.
- **Handoff boundary:** the only terminal action is one call to the owned
  `day7_resolve_ending` interface. It must fail closed on adapter/resolver
  validation errors. Narrative code never imports/copies predicates, chooses a
  stable label, writes lifecycle, or calls `commit_ending_entry`/
  `commit_ending_completion`.
- **Source boundary:** prose/local flow belongs under `game/chapters/`; screens
  present state only. Player-facing text may not expose hidden axes, tokens,
  qualifications, predicates, internal IDs, ending forecasts, or test data.

## Explicitly Out of Scope

- Six ending labels/prose, `commit_ending_completion`, the true-ending arcade
  epilogue, resolver predicates/priorities, qualification implementation,
  terminal-witness/full-manifest expansion, release validation, packaging, and
  stage changes.
- New character art, CG, external image/audio/video, official/source-unknown
  material, logos, fonts, final UI redesign, gallery work, or sourcing.

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Narrative code could duplicate or bypass SYS-ENDING ownership. | Medium | High | Static scans require only the owned handoff and reject lifecycle/resolver/persistent writes. |
| Missing target labels could tempt an empty placeholder. | High | High | Keep the stories blocked; deliver real SYS-ENDING targets first. |
| Causal recall could misrepresent variable history or disclose hidden state. | Medium | High | Test exact common-path facts and player-safe text at both accessibility baselines. |

## Definition of Done

- [ ] All Must Have tasks are complete after their blocking terminal dependency is delivered.
- [ ] Day 7 has exactly one unit and three required scenes with zero new choice/state source facts.
- [ ] It uses the one owned terminal handoff exactly once and fails closed.
- [ ] Source identity, asset records, tests, evidence, review, smoke, and QA bind one generation.
- [ ] All Python, global Ren'Py, lint/compile, and content-constraint checks pass.
- [ ] No S1/S2 defect remains and no ending/epilogue/full-manifest/release claim is made.
- [ ] A Sprint 6 QA plan exists before implementation begins.
