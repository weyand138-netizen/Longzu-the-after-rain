# Sprint 3 — 2026-09-07 to 2026-09-20

## Sprint Goal

Deliver the playable, asset-admitted, route- and accessibility-validated Day 4
unit `chapter_day4_seaside_train`, while restoring the full Python test suite
to a passing baseline; do not expand the Day 1-only partial manifest or enter
Day 5, ending, or release scope.

## Capacity

- Total days: 14
- Buffer (20%): 3 days
- Available: 11 days
- Planned critical-path effort: 5 days
- Planned supporting effort: 1 day
- Review mode: Solo

## Tasks

### Must Have (Critical Path)

| ID | Task | Agent/Owner | Est. Days | Dependencies | Acceptance Criteria |
|---|---|---:|---:|---|---|
| S3-01 | Repair Day 2 keyboard-route regression | Andwey | 0.5 | Current test failure reproduced | Correct the stale Day 2 `K_RETURN` assertion boundary without weakening route coverage; the affected test and the full Python suite pass. |
| S3-02 | Day 4 authored source and causal bindings | Andwey | 2 | S3-01; frozen content baseline and ADR-0003/0008 | Add `chapter_day4_seaside_train` with exactly `scene_day4_ticket_counter`, `scene_day4_route_answer`, `scene_day4_contact_channel`, and `scene_day4_sea_window`; bind only the five approved Day 4 choices, reactions, and later payoffs; record source hash and player-safe catalog inputs. |
| S3-03 | Day 4 asset admission records | Andwey | 1 | S3-02 | Inventory every actual Day 4 runtime asset with provenance, licence, SHA-256, stable runtime path, and self-voicing/semantic binding; explicitly leave planned or missing assets unadmitted. |
| S3-04 | Day 4 route, accessibility, and evidence validation | Andwey | 1.5 | S3-02, S3-03 | Exercise all approved Day 4 choice paths through the Day 5 handoff; preserve current-source-hash evidence for keyboard-only 1280x720 silent/reduced-motion and 1.5x high-contrast/reduced-motion baselines; no traceback, hidden-state disclosure, or quick-menu focus target. |

### Should Have

| ID | Task | Agent/Owner | Est. Days | Dependencies | Acceptance Criteria |
|---|---|---:|---:|---|---|
| S3-05 | Day 4 story and evidence traceability | Andwey | 1 | S3-02–S3-04 | Create linked Day 4 story records and bind source, asset, test, and evidence references to the same content generation; update the epic index without changing later-day scope. |

### Nice to Have

None. Remaining capacity is delivery buffer and must not be used to begin Day 5,
terminal witnesses, ending implementation, or release packaging.

## Carryover from Previous Sprint

| Task | Reason | New Estimate |
|---|---|---:|
| None | Sprint 2 Day 3 source, asset admission, and validation are complete and QA-approved. | — |

## Day 4 Source Contract

- **Unit and responsibility:** `chapter_day4_seaside_train` /
  `responsibility_day4_self_controlled_options`.
- **Required scenes:** `scene_day4_ticket_counter`, `scene_day4_route_answer`,
  `scene_day4_contact_channel`, and `scene_day4_sea_window`.
- **Exact choice set:** `day4_buy_two_tickets_real_name`,
  `day4_buy_single_ticket_cash`, `day4_register_independent_contact`,
  `day4_decline_independent_contact`, and `day4_follow_one_route_no_backup`.
- **Agency boundary:** before any response surface is frozen, register
  `preserve_executable_self_controlled_option`; show tickets, route map, and
  contact option as choices she can hold or execute. Resource projection alone
  never proves her autonomy has been honoured.
- **Source boundary:** Day 4 prose and local branches belong in
  `game/chapters/day4.rpy`; screens present state but never select an outcome.
  Do not expose axes, tokens, qualifications, route predictions, internal IDs,
  persistent state, or ending hints.
- **Asset boundary:** do not add final character art, CGs, external images,
  audio, or video merely to fill the chapter. Actual runtime references require
  admission records; missing intended assets remain unadmitted.

## Explicitly Out of Scope

- Day 5–Day 7 prose, ending or epilogue production, terminal-witness
  validation, resolver changes, qualification coverage, and release evidence.
- Any change to `game/modules/narrative_partial_manifest.py`,
  `narrative_partial_day1_manifest:v1`, or a new incremental partial-manifest
  schema.
- UI information-architecture redesign, final art/audio production, gallery
  work, package/release work, or formal full-production playtests.

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Day 4 ticket/contact preparation is treated as a resource check rather than a registered player-visible answer | Medium | High | Validate the required answer state, action/object evidence, response partition, and outcome bindings before route tests. |
| Identity-exposure and contact-risk consequences are omitted or inferred from presentation | Medium | High | Assert exact events, resources, reactions, and player-safe summaries in source and engine routes. |
| The existing Day 2 keyboard-route assertion remains stale or coverage is weakened during repair | Medium | High | Reproduce the failure first, make the narrowest correction, and rerun the entire Python suite. |
| Scope drifts into Day 5, terminal witnesses, or a partial-manifest expansion | Medium | High | Limit routes to the Day 5 handoff and fail source/data checks on forbidden scope changes. |

## Dependencies on External Factors

- None. The existing Ren'Py 8.5.3 runner, Day 1–Day 3 route harnesses, and
  approved narrative baseline are the verification baseline.

## Definition of Done for this Sprint

- [ ] All Must Have tasks are complete.
- [ ] The Day 2 regression is repaired and the complete Python suite passes.
- [ ] Day 4 has exactly the approved unit, four required scenes, five approved
  choice bindings, and no unapproved content-lock expansion.
- [ ] The self-controlled-option answer is perceptibly presented and registered
  before related response choices are available.
- [ ] Source hash, player-safe catalog input, asset-admission records, and
  route/accessibility evidence identify the same content generation.
- [ ] All actual runtime assets are admitted; planned or missing assets are
  explicitly not admitted.
- [ ] Unit, integration, global Ren'Py, lint/compile, content-constraint, and
  accessibility checks pass.
- [ ] No S1 or S2 defect remains open in delivered Day 4 work.
- [ ] No Day 4 data enters the Day 1-only partial manifest, and no terminal or
  ending-validation claim is made.
- [ ] A Sprint 3 QA plan exists before implementation begins.

> **Scope check:** Run `/scope-check sys-narrative` before implementation if a
> Day 5+, partial-manifest, terminal-witness, or ending story is proposed.
