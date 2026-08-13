# Day 4 Traceability Record

**Date**: 2026-08-11
**Sprint item**: S3-05 — Day 4 story and evidence traceability
**Generation anchor**: `game/chapters/day4.rpy` SHA-256 `dc62786bf08623b243dca77a5e24e37c17084d39e37e3041985e3a9350fccaac`

## Link Matrix

| Concern | Current artifact | Generation binding / result |
| --- | --- | --- |
| Authored source | `game/chapters/day4.rpy` | SHA-256 `dc62786bf08623b243dca77a5e24e37c17084d39e37e3041985e3a9350fccaac` |
| Source story | `production/epics/sys-narrative/story-009-day4-authored-source.md` | Complete; `TR-NAR-009`; source evidence points to the generation anchor. |
| Route and accessibility story | `production/epics/sys-narrative/story-010-day4-content-validation.md` | Complete; `TR-NAR-010`; evidence record uses the generation anchor. |
| Asset-admission story | `production/epics/sys-narrative/story-011-day4-asset-admission.md` | Complete; `TR-NAR-011`; admitted Day 4 runtime assets are recorded below. |
| Authored-source evidence | `production/qa/evidence/day4-authored-source-evidence.md` | Declares the generation-anchor SHA-256. |
| Route/accessibility evidence | `production/qa/evidence/day4-content-validation-2026-08-11/record.md`; `production/qa/evidence/day4-qa-revalidation-2026-08-12.md` | Both declare the generation-anchor SHA-256. The preserved visual run passed 30/30 testcases and 255/255 assertions; the current-test-definition revalidation passed 30/30 and 256/256. |
| Asset inventory and legal register | `design/assets/entity-inventory.md`; `docs/legal/asset-register.md` | Day 4 declares only the admitted font, `bg warm_room`, and shared choice surface. The shared `game/screens.rpy` source SHA-256 is `45f8315a4ee8af5191c523d1d29594147383759b50c5b773d89e0c73f96284ed` in both records. |
| Automated source test | `tests/unit/sys_narrative/day4_authored_source_test.py` | Reads the authored-source evidence and rejects a stale Day 4 source hash. |
| Automated asset test | `tests/unit/sys_narrative/day4_asset_admission_test.py` | Recomputes all admitted runtime-source hashes and requires both admission records. |
| Automated integration test | `tests/integration/sys_narrative/day4_content_validation_test.py` | Validates the source guard, focus treatment, scope boundary, and passing evidence bundle. |
| Engine tests | `game/testcases.rpy` and `tools/run-renpy-tests.ps1` | Pinned Ren'Py 8.5.3 global suite recorded above; wrapper status is authoritative. |

## Scope and Verdict

The matrix covers Day 4 only. It introduces no Day 5+ source, terminal/ending
work, or partial-manifest expansion. S3-05 traceability is **complete**: every
completed Day 4 story has a current test and evidence path, while source,
asset, test, and evidence records identify the same verified content generation.
