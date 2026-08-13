# Sprint 4 — 2026-09-21 to 2026-10-04

## Sprint Goal

Deliver the playable, source-locked, asset-admitted, route- and
accessibility-validated Day 5 unit `chapter_day5_family_lie`, including its
resource-fact-only route-answer derivation, without beginning Day 6, Day 7,
terminal, ending, epilogue, partial-manifest, or release work.

## Capacity

- Total days: 14
- Buffer (20%): 3 days
- Available: 11 days
- Planned critical-path effort: 6 days
- Planned supporting effort: 1 day
- Review mode: Solo

## Tasks

### Must Have (Critical Path)

| ID | Task | Agent/Owner | Est. Days | Dependencies | Acceptance Criteria |
|---|---|---:|---:|---|---|
| S4-01 | Day 5 authored source and derived route answer | Andwey | 3 | Sprint 3 complete; frozen Day 5 baseline | Add only `chapter_day5_family_lie`, its four required scenes, the ten approved Day 5 choice/reaction/payoff bindings, and `erii_route_answer_derivation:v1` using only permitted Day 4 resource facts. |
| S4-02 | Day 5 asset admission records | Andwey | 1 | S4-01 | Audit every actual Day 5 runtime asset; record provenance, licence, SHA-256, stable path, and semantic binding; leave planned/missing assets unadmitted. |
| S4-03 | Day 5 route, accessibility, and evidence validation | Andwey | 2 | S4-01, S4-02 | Exercise truth, liability, derived shared/contact/solo/fallback answers, response, and eligible repair branches by keyboard at both approved accessibility baselines; bind evidence to the source hash. |

### Should Have

| ID | Task | Agent/Owner | Est. Days | Dependencies | Acceptance Criteria |
|---|---|---:|---:|---|---|
| S4-04 | Day 5 story and evidence traceability | Andwey | 1 | S4-01–S4-03 | Bind stories, source, asset records, tests, and evidence to one Day 5 generation without implying Day 6+, terminal, ending, or release delivery. |

### Nice to Have

None. Remaining capacity is delivery buffer and must not start Day 6, Day 7,
ending, epilogue, full-manifest, terminal-witness, or release scope.

## Carryover from Previous Sprint

| Task | Reason | New Estimate |
|---|---|---:|
| None | Sprint 3 Day 4 work is QA-approved and locally committed as `f694337`. | — |

## Scope Check

**Verdict: PASS.** The baseline contains one Day 5 unit with four scenes and
ten approved choices. This sprint implements those required contracts only;
there are no scope additions or removals. The sprint does not create a new
partial manifest, a terminal continuation witness, a Day 6 commitment, ending
entry, resolution, epilogue, or external asset.

## Day 5 Source Contract

- **Unit and responsibility:** `chapter_day5_family_lie` /
  `responsibility_day5_truth_and_route_answer`.
- **Required scenes:** `scene_day5_family_archive`, `scene_day5_truth_delivery`,
  `scene_day5_response_answer`, and `scene_day5_shared_liability`.
- **Exact choice set:** `day5_share_full_archive`, `day5_give_safe_summary`,
  `day5_include_self_in_truth`, `day5_blame_family_only`,
  `day5_honor_erii_response`, `day5_replace_erii_response`,
  `day5_repair_daily_choice`, `day5_keep_daily_override`,
  `day5_repair_school_evidence`, and `day5_keep_school_evidence_hidden`.
- **Agency boundary:** `agency_day5_response` may be recorded only after
  `erii_route_answer_derivation:v1` uniquely derives an allowed answer from
  known Day 4 resource facts. It must freeze input facts, selected state,
  action/object evidence, priority rule, and source hash. It must never read
  axes, counterevidence tokens, qualifications, ending predicates/predictions,
  or developer flags.
- **Derivation order:** valid two-ticket facts select `shared_escape`; otherwise
  valid contact-card plus completed-risk-handover facts select
  `independent_contact`; otherwise a valid single-ticket/no-contact-card fact
  selects `solo_departure`; otherwise the valid empty-resource state selects
  `continue_without_executable_route`. Contradictory, incomplete, or untyped
  facts derive `undetermined`; that route has no Day 5 response surface.
- **Repair boundary:** Day 3 school-evidence repair is shown only for a
  pre-existing unresolved token. Daily-choice repair is shown only when the
  token was unresolved before entering the route-answer scene; a new
  `day5_replace_erii_response` token cannot be repaired in that same scene.
- **Source boundary:** prose and local branches belong in `game/chapters/day5.rpy`;
  pure derivation belongs in a pure module; screens present state but never
  select an outcome. Player-facing text never exposes internal IDs, hidden
  scores/tokens, qualifications, ending hints, persistent state, or test data.

## Explicitly Out of Scope

- Day 6 and Day 7 source, any route commitment, terminal witness, ending label,
  resolver or qualification change, true-ending epilogue, release QA, packaging,
  performance profiling, and formal production playtests.
- Any change to `game/modules/narrative_partial_manifest.py`,
  `narrative_partial_day1_manifest:v1`, or a new partial-manifest schema.
- New character art, CG, external image, audio, video, final UI redesign,
  gallery work, or third-party asset sourcing.

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Day 5 route answer reads hidden state or is assigned by author intent | Medium | High | Pure derivation tests reject unknown/contradictory facts and forbidden inputs; source tests bind its visible action to selected state. |
| More than one response route or an early repair appears | Medium | High | Engine and source tests prove exact response partition and pre-existing-token boundaries. |
| Truth, liability, or route facts become sensory-only | Medium | High | Keyboard-only silent/reduced-motion and high-contrast captures assert textual facts and focus. |
| Scope drifts into Day 6 commitment or ending behavior | Medium | High | Content-boundary tests reject Day 6+, terminal, ending, and partial-manifest references. |

## Dependencies on External Factors

- None. The pinned Ren'Py 8.5.3 runner and Day 1–Day 4 test harnesses are the
  verification baseline. No network or external asset is required.

## Definition of Done for this Sprint

- [ ] All Must Have tasks are complete.
- [ ] Day 5 has exactly the approved unit, four scenes, ten choice/reaction/payoff
  records, and no later-day or content-lock expansion.
- [ ] The route answer is uniquely derived from permitted, visible resource facts;
  invalid facts fail closed without a response surface.
- [ ] Truth, liability, response, and permitted repair consequences are
  perceptible before their corresponding event/checkpoint/outcome records.
- [ ] Source hash, derivation record, asset admission, route/accessibility evidence,
  and traceability identify the same content generation.
- [ ] All actual runtime assets are admitted; planned/missing assets are explicitly
  unadmitted.
- [ ] Unit, integration, global Ren'Py, lint/compile, and content-constraint checks pass.
- [ ] No S1 or S2 defect remains open in delivered Day 5 work.
- [ ] No Day 5 data enters the Day 1-only partial manifest and no Day 6+, terminal,
  ending, epilogue, or release claim is made.
- [ ] A Sprint 4 QA plan exists before implementation begins.

> **Scope check:** Run `/scope-check sys-narrative` before implementation if a
> Day 6+, terminal, ending, epilogue, partial-manifest, or release story is proposed.
