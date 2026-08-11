# Consistency Check Report

Date: 2026-08-05  
Mode: `full`, followed by targeted recheck `entity:zero_delta_major_choice_ratio`  
Registry: `design/registry/entities.yaml` (version 2)

## Scope

Registry entries checked: 193 total

- Entities: 0
- Items: 0
- Formulas: 52
- Constants: 24
- Other registered schemas, catalogs, contracts, predicates, settings and tuning knobs: 117

GDDs scanned: 10

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

Excluded as required: `game-concept.md`, `systems-index.md`, `game-pillars.md`, and files under `design/gdd/reviews/`.

## Scan Summary

The scan used literal, case-insensitive registry-name searches against current system GDDs, followed by `-C 3` context extraction. Only the initially confirmed conflict received a wider section read. After the fix, the changed entry was rescanned against every current GDD occurrence.

- 77 registry names had at least one literal GDD occurrence.
- 10 names occurred in more than one current GDD and were compared across documents.
- All 10 cross-GDD entries are now consistent.
- 1 cross-GDD conflict was initially confirmed and resolved during this run.
- 116 registry names had no literal occurrence in the in-scope GDDs.
- 3 additional names occurred only in a consumer document, not in their declared source document.

## Conflicts Found (remaining)

None.

## Resolved Conflict

### ✅ `zero_delta_major_choice_ratio`

- Initial source/registry value: target `10%–20%`; safe range `0%–25%`
- Downstream content value: target `45%–65%`; safe range `35%–70%`; v1.2 baseline `30/52 = 57.7%`
- Resolution: approved the later content-informed tuning as an intentional source-level design change.
- Source GDD now says: target `45%–65%`; safe range `35%–70%`.
- Registry now says: `target_range_percent: [45, 65]`; `safe_range_percent: [35, 70]`.
- Chapter GDD remains unchanged and now agrees with the source and registry.
- Static content check: 52 `semantic_major` choices, 30 zero-axis choices (`57.7%`), zero missing non-axis semantic declarations, zero missing reactions and zero missing payoffs.
- Design rationale and acceptance criteria: `design/quick-specs/zero-delta-major-choice-ratio-tuning-2026-08-05.md`.

## Stale Registry Entries

None confirmed.

## Unverifiable References

The grep-first contract could not directly compare 119 entries against their authoritative source text:

- 116 registry names do not occur literally in any in-scope current GDD. Most are normalized registry labels whose source facts appear under different prose or record names.
- `resolver_complexity_contract` appears only in `deterministic-ending-resolution.md`, not its declared source `five-axis-state.md`.
- `persist_catalog_generation_id` appears only in `sys-access.md`, not its declared source `cross-playthrough-unlocks.md`.
- `canonical_production_units_v1` appears in `seven-day-chapter-script.md`, while its declared source `design/narrative/seven-day-content-baseline.md` is outside this skill's GDD scan scope.

No contradiction was inferred from an absent literal name. These are coverage notes, not conflicts.

## Clean Entries

74 registry entries were directly locatable in their declared source GDD and had no conflicting comparable value in any other in-scope GDD. This includes all 10 cross-GDD entries:

- `notification_transition_ms`
- `terminal_cause_classes_per_ending`
- `ending_selection`
- `evidence_opportunities_per_axis`
- `font_scale_options`
- `presentation_settle_delay_ms`
- `restored_traversal_occurrence_valid`
- `state_schema_sentinel`
- `unresolved_counterevidence`
- `zero_delta_major_choice_ratio`

## Verdict

**PASS**

No cross-GDD conflicts remain in the checked registry-name surface. The grep-first coverage notes remain informational.

Skill completion state: **COMPLETE — consistency conflict resolved and targeted recheck passed.**
