# Consistency Check Report

Date: 2026-08-09  
Mode: `full`  
Registry: `design/registry/entities.yaml` (version 2)

## Scope

Registry entries checked: 207 total

- Entities: 0
- Items: 0
- Formulas: 58
- Constants: 25
- Other registered schemas, catalogs, contracts, predicates, settings, enums and tuning knobs: 124

GDDs scanned: 11

- `choice-and-causality-record.md`
- `cross-playthrough-unlocks.md`
- `deterministic-ending-resolution.md`
- `five-axis-state.md`
- `local-achievements.md`
- `save-load-rollback.md`
- `seven-day-chapter-script.md`
- `sys-access.md`
- `sys-journal.md`
- `sys-tension.md`
- `sys-test.md`

Excluded as required: `game-concept.md`, `systems-index.md`, `game-pillars.md`, and files under `design/gdd/reviews/`.

## Scan Summary

The scan used literal, case-insensitive registry-name searches against the current system GDDs, followed by targeted context extraction. Cross-document occurrences were compared against the authoritative registry source entry.

- 86 registry names had at least one literal occurrence in the in-scope GDDs.
- 10 names occurred in more than one current GDD and were compared across documents.
- 76 names occurred in exactly one current GDD.
- 121 registry names had no literal occurrence in the in-scope GDDs.
- 3 additional names occurred only in a consumer GDD rather than their declared source GDD; these remain coverage notes, not inferred conflicts.
- The 9 registry entries introduced for `sys-test.md` that were directly locatable in that GDD match their registered formulas, targets and safe ranges.

## Conflicts Found

None.

## Stale Registry Entries

None confirmed. The authoritative source values for the directly locatable entries agree with the registry. No Git history is available in this repository, so source-age comparison was not possible.

## Unverifiable References

The grep-first contract cannot directly compare 124 entries against authoritative source text:

- 121 registry names do not occur literally in any current in-scope GDD. Most are normalized registry labels whose source facts are expressed under different prose or record names.
- `resolver_complexity_contract` appears in `deterministic-ending-resolution.md`, not its declared source `five-axis-state.md`.
- `persist_catalog_generation_id` appears in `sys-journal.md`, not its declared source `cross-playthrough-unlocks.md`.
- `canonical_production_units_v1` appears in `seven-day-chapter-script.md`, while its declared source `design/narrative/seven-day-content-baseline.md` is outside this skill's GDD scan scope.

No contradiction was inferred from an absent literal name. These are coverage notes only.

## Clean Entries

83 registry entries were directly locatable in their declared source GDD and had no conflicting comparable value in any other in-scope GDD. All 10 cross-GDD entries are consistent, including:

- `ending_selection`
- `evidence_opportunities_per_axis`
- `font_scale_options`
- `notification_transition_ms`
- `presentation_settle_delay_ms`
- `restored_traversal_occurrence_valid`
- `state_schema_sentinel`
- `terminal_cause_classes_per_ending`
- `unresolved_counterevidence`
- `zero_delta_major_choice_ratio`

## Verdict

**PASS**

No cross-GDD conflicts remain in the checked registry-name surface. Coverage notes remain informational.

Skill completion state: **COMPLETE**
