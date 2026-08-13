# Scope Check: Sprint 5 Day 6 Narrative Unit

**Generated**: 2026-08-13
**Baseline**: `design/narrative/seven-day-content-baseline.md`
**Prior committed sprint**: Sprint 4 / `c40f616`

## Original Scope

One canonical Day 6 unit: `chapter_day6_no_safe_house`; four required scenes;
the fifteen frozen Day 6 choices; conditional backup and late-truth repair
nodes; the two cost transactions; and exactly one guarded route-commitment or
fallback action. Asset admission, route/accessibility validation, and
traceability must bind one Day 6 source generation.

## Planned Scope

The same Day 6 unit, four scenes, fifteen canonical choice records, existing
resource/event/token inputs, direct production events, player-safe catalog
inputs, asset records, unit/integration/engine tests, evidence, and
traceability. The route commitment will record Day 6 facts only; it will not
call the resolver, enter an ending, create a terminal witness, or write
persistent state.

## Scope Additions

None.

## Scope Removals

None.

## Bloat Score

- Original items: 8
- Planned items: 8
- Items added: 0 (+0%)
- Items removed: 0
- Net scope change: 0 (0%)

## Risk Assessment

- **Schedule Risk**: Medium — fifteen choices include conditional sibling nodes
  and a five-way mutually exclusive commitment/fallback partition.
- **Quality Risk**: High — resource guards, contributor-aware token repair,
  delayed cost reconsideration, and direct event ordering must remain exact.
- **Integration Risk**: High — Day 6 produces sources later consumed by
  SYS-ENDING, but it may not take ownership of resolver, qualification, ending,
  completion, or persistence behavior.

## Recommendation

Keep the Day 6 boundary. Defer Day 7, terminal witnesses, ending labels and
resolver changes, all six endings, true-ending epilogue, partial-manifest work,
new asset sourcing, release work, and stage advancement.

**Scope Verdict: PASS**
Net change: 0% - On Track.
