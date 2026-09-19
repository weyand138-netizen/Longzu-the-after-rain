# Story 025 QA Evidence — `rain_stops` Years-Later Tail

**Date**: 2026-08-14
**Story**: `production/epics/sys-narrative/story-025-rain-stops-years-later-tail.md`
**Sprint**: Sprint 008
**Review mode**: solo
**Result**: Automated evidence PASS; human review deferred

## Scope and source boundary

The input `C:\Users\Andwey\Downloads\好结局剧本标注版.docx` was treated as an
unconfirmed fan-adaptation reference. Only high-level structure and theme were
used. The implementation does not copy lines, confirm named extra world states,
or introduce the source document as an approved canon authority.

Only the existing `epilogue_rain_stops_arcade` body was extended, after the
existing lights-out completion event. The six ending IDs, resolver, priority,
canonical witnesses, five axes, token definitions, qualifications, ending
predicates, and completion boundary remain covered by the focused invariant
test.

## Automated results

| Check | Result | Evidence |
|---|---|---|
| Story 025 focused integration tests | **PASS — 7/7** | `tests/integration/sys_narrative/rain_stops_tail_test.py` |
| Full Python suite | **PASS — 288/288** | `uv run python -m unittest discover -s tests -p '*_test.py'` |
| Python compileall | **PASS** | `uv run python -m compileall -q game/modules tests` |
| Ren'Py global suite | **PASS — 56/56 testcases, 474/474 assertions** | `tools/run-renpy-tests.ps1 -Suite global -TimeoutSeconds 120` |
| Ren'Py 8.5.3 lint/compile | **PASS** | pinned SDK `renpy.py ... lint --compile` |
| Erii content constraints | **PASS** | `tools/test-content-constraints.ps1` |
| Source/content-lock identity | **PASS** | Story 025 focused test; lock v2 |
| Whitespace validation | **PASS** | `git diff --check` (line-ending notices only) |

## Current source identities

| Source | SHA-256 |
|---|---|
| `game/chapters/endings.rpy` | `6f8ddcdde2fbd02e921d6b3d1564d63ca6a69bd2e15e8d4073327c95e0d0944a` |
| `tests/integration/sys_narrative/rain_stops_tail_test.py` | `6e198484ba1f4f74e6fa4cca2727bcc2b22bf13d501a678ac51666b09b414e16` |
| `design/narrative/seven-day-content-baseline.md` | `1c20fe09a018c2c7d0016549040f9b84a9ee7bbd2c5125a39da487da2ff30750` |
| `docs/architecture/change-impact-2026-08-14-rain-stops-epilogue.md` | `8e4f9b0b15c9888ec1c12e3d41c6bc010913a7f3296e0f3c6e658c78af320a4b` |
| `production/epics/sys-narrative/story-025-rain-stops-years-later-tail.md` | `a802f8b7bb9c7cbb4fff990cca27481a1338d78de4d80bbf647cd2309d336c90` |

`design/content-lock.md` records `endings.rpy` at 105 lines with the current
hash above, and the baseline at 375 lines with its current hash above.

## Manual and human-only items

The following are intentionally **NOT RUN / NOT PASS** under the task scope:

- non-test GUI Production start and end-to-end visual traversal;
- narrative readability, restraint, and subjective experience review;
- SAPI listening and semantic-equivalence review;
- copyright/source review and final narrative/正典 sign-off;
- performance observation or manual playtest.

No playtest session, listening review, or subjective approval is fabricated by
this evidence.

## QA hand-off boundary

The automated implementation boundary is ready for story close-out once the
read-only code review records its verdict. This evidence does not promote the
project to Polish and does not alter `production/stage.txt`.
