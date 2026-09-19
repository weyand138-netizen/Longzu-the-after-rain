# Sprint 5 — 2026-10-05 to 2026-10-18

## Sprint Goal

Deliver the playable, source-locked, asset-admitted, route- and
accessibility-validated Day 6 unit `chapter_day6_no_safe_house`, including its
frozen resource recovery, cost responsibility, and exactly-one guarded route
commitment/fallback, without entering Day 7, terminal, ending, epilogue,
partial-manifest, or release scope.

## Capacity

- Total days: 14
- Buffer (20%): 3 days
- Available: 11 days
- Planned critical-path effort: 7 days
- Planned supporting effort: 1 day
- Review mode: Solo

## Tasks

### Must Have (Critical Path)

| ID | Task | Agent/Owner | Est. Days | Dependencies | Acceptance Criteria |
|---|---|---:|---:|---|---|
| S5-01 | Day 6 authored source and guarded route commitment | Andwey | 4 | Sprint 4 approved; frozen Day 6 baseline and ADR-0003/0006/0008 | Add only `chapter_day6_no_safe_house`, its four scenes, the fifteen frozen Day 6 choices, conditional repair/keep nodes, cost/reconsideration transactions, and exact-one resource/event-guarded commitment or fallback. |
| S5-02 | Day 6 asset admission records | Andwey | 1 | S5-01 | Audit every actual Day 6 runtime asset with provenance, licence, SHA-256, stable runtime path, and semantic/accessibility binding; admit no new external or planned asset. |
| S5-03 | Day 6 route, accessibility, and evidence validation | Andwey | 2 | S5-01, S5-02 | Exercise each legal conditional repair, cost/reconsideration branch, all five commitment/fallback partitions, and both approved accessibility baselines; bind evidence to the current source hash. |

### Should Have

| ID | Task | Agent/Owner | Est. Days | Dependencies | Acceptance Criteria |
|---|---|---:|---:|---|---|
| S5-04 | Day 6 story and evidence traceability | Andwey | 1 | S5-01–S5-03 | Bind stories, source, asset records, tests, verified evidence, code review, smoke, and QA sign-off to one Day 6 generation without claiming Day 7, terminal, ending, epilogue, or release delivery. |

### Nice to Have

None. Remaining capacity is delivery buffer and must not be used to begin Day 7,
terminal witnesses, ending implementation, epilogue, manifest expansion, or
release work.

## Carryover from Previous Sprint

| Task | Reason | New Estimate |
|---|---|---:|
| None | Sprint 4 Day 5 is QA-approved and locally committed as `c40f616`. | — |

## Day 6 Source Contract

- **Unit and responsibility:** `chapter_day6_no_safe_house` /
  `responsibility_day6_resources_cost_and_commitment`.
- **Required scenes:** `scene_day6_safehouse_failure`, `scene_day6_backup_exit`,
  `scene_day6_cost_inventory`, `scene_day6_route_commitment`.
- **Exact choice set:** `day6_reopen_service_exit`, `day6_abandon_backup`,
  `day6_use_service_exit`, `day6_keep_backup_abandoned`,
  `day6_disclose_withheld_archive`, `day6_keep_archive_withheld`,
  `day6_burn_old_identity`, `day6_shift_cost_to_erii`, `day6_take_cost_back`,
  `day6_leave_cost_shifted`, `day6_commit_independent_contact`,
  `day6_commit_shared_escape`, `day6_commit_solo_departure`,
  `day6_commit_old_order_return`, and `day6_no_executable_route`.
- **Repair/cost boundary:** reopen exists only for a pre-existing abandoned
  backup with a discovered service exit; late truth exists only after the
  withheld-truth consequence; reconsideration exists only after a visible cost
  shift, a second refusal, and the specified consequence. Repairs acknowledge
  every applicable frozen contributor and preserve residual outcomes.
- **Commitment boundary:** calculate the active action only from the frozen Day
  5 answer/outcome and approved resource/event facts. The guarded commitment
  choices and fallback are mutually exclusive and exhaustive (active count one).
  They record their Day 6 event/outcome and return through the existing seam;
  they do not invoke an ending resolver, entry/completion, qualification writer,
  persistent grant, Day 7 branch, or terminal witness.
- **Source boundary:** prose/local branches belong in `game/chapters/day6.rpy`;
  screens present state but never select outcomes. Player-visible copy never
  exposes axes, tokens, qualifications, predicates, internal IDs, persistent
  state, ending predictions, or test data.

## Explicitly Out of Scope

- Day 7, terminal witness, ending label, resolver or qualification ownership
  changes, ending completion, six endings, true-ending epilogue, full manifest,
  release validation, packaging, or stage promotion.
- Any change to `game/modules/narrative_partial_manifest.py`,
  `narrative_partial_day1_manifest:v1`, or a new partial-manifest schema.
- New character art, CG, external image, audio, video, official asset, logo,
  final UI redesign, gallery work, or third-party asset sourcing.

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| A route commitment can become a free ending selector or expose more than one active action. | Medium | High | Source and pure tests assert exact guard order, source fact closure, and active count one. |
| Cost reconsideration can repair an unseen or incomplete shift. | Medium | High | Engine tests require shift reaction, visible consequence, renewed refusal, then the independent response node. |
| Day 6 can accidentally consume SYS-ENDING ownership. | Medium | High | Static tests reject resolver, ending entry/completion, qualification writer, terminal, and persistent references. |
| Resource repair can silently infer a service exit that was never discovered. | Medium | High | Tests distinguish discovered exit, absent exit acknowledgement, prepared exit, and abandoned backup paths. |

## Definition of Done

- [x] All Must Have tasks are complete.
- [x] Day 6 has exactly the approved unit, four scenes, fifteen choice/reaction/payoff records, and no extra Day 6 production labels.
- [x] Conditional repairs, the cost reconsideration transaction, and the commitment/fallback partition have exact visible preconditions and outputs.
- [x] Exactly one Day 6 commitment/fallback action is available for every legal resource/answer partition, and none invokes SYS-ENDING.
- [x] Source hash, player-safe catalog input, asset-admission records, route/accessibility evidence, and traceability identify the same Day 6 generation.
- [x] All actual runtime assets are admitted; planned/missing assets remain unadmitted.
- [x] Unit, integration, global Ren'Py, lint/compile, content-constraint, and accessibility checks pass.
- [x] No S1 or S2 defect remains open in delivered Day 6 work.
- [x] No Day 6 data enters the Day 1-only partial manifest, and no Day 7, terminal, ending, epilogue, or release claim is made.
- [x] A Sprint 5 QA plan exists before implementation begins.
