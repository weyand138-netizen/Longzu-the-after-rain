# Story 001: Day 1 Authored Source and Causal Beats

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production  
> **Status**: Complete  
> **Last Updated**: 2026-08-10  
> **Layer**: Feature  
> **Type**: Config/Data  
> **Estimate**: 2 days  
> **Manifest Version**: 2026-08-04.1

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`  
**Requirement**: `TR-NAR-001` — Seven-day chapter paths and six endings are valid and content-locked. Day 1 must preserve the exact 15-unit baseline, declare only canonical choice/reaction/payoff identities, bind its owner source hash, and expose no player-facing hidden-state or score information.  
**Governing ADRs**: ADR-0008 (primary), ADR-0003  
**Engine**: Ren'Py 8.5.3 | **Risk**: High

**Traceability status**: `TR-NAR-001` is `partial` in `docs/architecture/tr-registry.yaml`. In this registry, `partial` records incomplete downstream implementation evidence, not a deprecated or blocked lifecycle state; Sprint 1 is the approved work that closes the Day 1 portion. ADR-0008 is Accepted and authorizes this work.

## Implementation Notes

- Create the Day 1 source only in `game/chapters/` using a stable `chapter_day1_*` label. Keep player-visible prose and local beats in the chapter; do not duplicate global ending conditions or let UI decide narrative outcomes.
- Build-time source scanning and manifest generation may validate the source, but runtime must consume immutable compiled catalogs and perform no source scan or CFG/path enumeration.
- Follow Feature-layer rules: each player-facing choice has one canonical ID, immediate reaction, and causally bound strictly later or approved terminal payoff; Erii's complex intent is expressed only through approved action/object/context evidence.
- Keep the source UTF-8, offline, and free of persistent-state, hidden-axis/token, resolver-internal, test-fixture, network, telemetry, score, prediction, qualification, route-label, or ending-hint reads/writes.

## Out of Scope

- Day 2–7 prose, global ending logic, SYS-CHOICE ownership, runtime CFG/path enumeration, Journal rendering, asset creation/admission, audio production, and UI/layout changes.
- Any new player-visible prose outside the canonical Day 1 unit or any change to the 15-unit `narrative_content_baseline:v1.2` contract.

## Performance Notes

No material runtime performance impact is expected: this story adds source data only. Scanning, hash generation, and validation run at build/test time; runtime consumes immutable compiled catalogs and must perform zero source scans or CFG/path enumerations.

## Acceptance Criteria

- [ ] Add the canonical `chapter_day1_her_own_name` source unit under `game/chapters/` without changing the baseline's 15-unit set.
- [ ] Implement the required Day 1 beats: clothing answer, food gesture, and receipt-name anchor, preserving Erii's action/object-led expression boundary.
- [ ] Use only canonical Day 1 choice IDs, immediate reactions, and delayed-payoff identities from `narrative_content_baseline:v1.2`.
- [ ] Do not render axes, tokens, route labels, internal IDs, or prediction/score language.
- [ ] Produce the owner source-hash record and player-safe Day 1 chapter/memory catalog inputs for Story 002.

## QA Test Cases

- **AC-1**: Given the Day 1 unit, when the content scanner enumerates labels and choices, then it finds `chapter_day1_her_own_name`, preserves the exact 15-unit baseline set, and rejects a missing, duplicate, or extra unit.
- **AC-2/3**: Given the source scanner and dialogue-constraint scan, when they inspect Day 1 beats and IDs, then clothing, food, and receipt-name anchors are present; only approved Day 1 choice/reaction/payoff identities resolve; and Erii has no complete spoken dialogue or hidden-state-derived expression.
- **AC-4**: Given all player-visible Day 1 strings, when the content constraint scan runs, then axis, token, route, internal-ID, prediction, score, qualification, and ending-hint disclosure counts are zero.
- **AC-5**: Given an edited Day 1 source, when the source hash is recomputed, then stale catalog/manifest input is rejected with no catalog emission; matching player-safe chapter/memory catalog inputs are produced only from approved common facts.

**Required test path**: `tests/unit/sys_narrative/day1_authored_source_test.py`

## Test Evidence

- Source/data validation: `tests/unit/sys_narrative/day1_authored_source_test.py`
- Content-constraint scan: `tools/test-content-constraints.ps1`
- Sprint smoke evidence: `production/qa/smoke-sprint-001-2026-08-10.md`
- Owner source-hash and player-safe catalog inputs: `production/qa/evidence/day1-authored-source-evidence.md`

## Dependencies

- Depends on: ADR-0008 accepted.
- Unlocks: Story 002.

## Completion Notes

**Completed**: 2026-08-10  
**Criteria**: 5/5 passing  
**Deviations**: None. A dedicated Sprint 1 Day 1 smoke report remains a cross-story hand-off item after Story 002/003 implement the manifest, route, and accessibility evidence.  
**Test Evidence**: Source/data test at `tests/unit/sys_narrative/day1_authored_source_test.py` (9/9 passing); content-constraint scan, Ren'Py global tests, and lint/compile passed; owner hash record at `production/qa/evidence/day1-authored-source-evidence.md`.  
**Code Review**: Skipped — Solo review mode.
