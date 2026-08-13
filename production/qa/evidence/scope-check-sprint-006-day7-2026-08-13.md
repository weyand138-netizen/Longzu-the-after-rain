# Scope Check: Sprint 6 Day 7 Narrative Unit

**Generated**: 2026-08-13
**Baseline**: `design/narrative/seven-day-content-baseline.md`
**Prior committed sprint**: Sprint 5 / `9f0bd12`

## Original Scope

One canonical Day 7 unit, `chapter_day7_before_red_well`, with exactly
`scene_day7_red_well_approach`, `scene_day7_causal_recall`, and
`scene_day7_ending_entry`. It acknowledges only facts already established by
Days 1-6, creates no choice, axis increment, token repair, route qualification,
or ending source fact, and hands the terminal state to the one SYS-ENDING
resolver/orchestrator.

## Planned Scope

The same three-scene Day 7 unit; source identity and player-safe catalog input;
asset admission using only existing approved runtime identities; route,
accessibility, failure-closure, and traceability evidence. The chapter may call
the established SYS-ENDING `day7_resolve_ending` handoff only. It may not
import or duplicate resolver predicates, write lifecycle/persistent state,
choose an ending, or create an ending label.

## Scope Additions

None. The six ending labels, their terminal completion nodes, the true-ending
epilogue, full-manifest expansion, terminal-witness enumeration, qualification
implementation, and release work remain separate future scope.

## Scope Removals

None.

## Bloat Score

- Original items: 6
- Planned items: 6
- Items added: 0 (+0%)
- Items removed: 0
- Net scope change: 0 (0%)

## Readiness Dependency

The frozen baseline requires Day 7 to reach one ending through the unique
SYS-ENDING handoff. The checked-in runtime currently has only the early pure
`resolve_ending(snapshot)` helper; it does not yet contain the required
`day7_resolve_ending` lifecycle adapter, six stable target labels, or the
ADR-0006 terminal-completion callsites. A Day 7 source that jumps to absent
labels, stores a locally selected ending, or supplies placeholder endings would
be a false gate pass.

Therefore Stories 020-023 are correctly **Blocked**, not Ready, until the
already-authorized SYS-ENDING terminal implementation provides that established
interface. This is an implementation dependency, not a request to alter the
frozen GDD, ADRs, ending meanings, or content identity.

## Risk Assessment

- **Schedule Risk**: Low for the Day 7 prose surface; it has no new choice
  graph or repair transaction.
- **Quality Risk**: High if terminal lifecycle ownership leaks into narrative
  code or a resolver failure enters a label.
- **Integration Risk**: High because a terminal handoff without the owned
  SYS-ENDING adapter and labels is not runnable or lint-valid.

## Recommendation

Preserve the Day 7 boundary and do not create a stub. Deliver the required
SYS-ENDING terminal interface and the six real ending labels as the next
authorized dependency batch, then return to Day 7 story-readiness and complete
its normal source, review, smoke, and QA flow. No stage promotion is proposed.

**Scope Verdict: CONCERNS**
**Scope delta: 0%; implementation readiness: blocked by an explicit existing
terminal dependency.**
