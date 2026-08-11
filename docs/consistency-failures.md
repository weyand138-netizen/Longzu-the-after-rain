# Consistency Failure Log

<!-- Auto-maintained by /consistency-check. Do not edit manually. -->
<!-- One entry per detected conflict, in chronological order. -->

| Date | GDD A | GDD B | Conflict Type | Status |
|------|-------|-------|---------------|--------|
| 2026-08-05 | `five-axis-state.md` | `seven-day-chapter-script.md` | Tuning range and production baseline | Resolved |

### 2026-08-05 — /consistency-check — 🔴 CONFLICT

**Domain**: SYS-STATE / SYS-NARRATIVE / SYS-CHOICE  
**Documents involved**: `design/gdd/five-axis-state.md` vs `design/gdd/seven-day-chapter-script.md`  
**What happened**: `zero_delta_major_choice_ratio` is target `10%–20%`, safe `0%–25%` in the authoritative source and registry, but target `45%–65%`, safe `35%–70%`, baseline `30/52 = 57.7%` in the chapter GDD.  
**Resolution**: Resolved — approved the content-informed target `45%–65%` and safe range `35%–70%` as a source-level tuning change; updated `five-axis-state.md` and `entities.yaml`, retained the verified `30/52 = 57.7%` narrative baseline, and passed the targeted consistency recheck.  
**Pattern**: A downstream production-content metric was frozen under the same registry name with a range that does not match the owning system GDD; check owner values before accepting content baselines.
