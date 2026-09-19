# Sprint 009 QA Evidence — Prologue and Day 1–2 Prose Expansion

**Date**: 2026-08-14
**Story**: `production/epics/sys-narrative/story-026-prologue-day1-day2-prose-expansion.md`
**Result**: Automated evidence PASS; human review deferred

## Scope

The implementation adds only scene texture, physical action, observation,
immediate reaction, and frozen-payoff recall inside existing Prologue, Day 1,
and Day 2 labels. Existing choice/menu/control signatures, state writes,
resource/token effects, and chapter boundaries remain unchanged. No asset,
audio, voice, UI bitmap, new character, or new canonical unit was added.

## Automated results

| Check | Result | Command/evidence |
|---|---|---|
| Story 026 focused structural tests | **PASS — 3/3** | `tests/integration/sys_narrative/prose_expansion_sprint009_test.py` |
| Full Python suite | **PASS — 291/291** | `uv run python -m unittest discover -s tests -p '*_test.py'` |
| Python compileall | **PASS** | `uv run python -m compileall -q game/modules tests` |
| Ren'Py global suite | **PASS — 56/56 testcases, 474/474 assertions** | `tools/run-renpy-tests.ps1 -Suite global -TimeoutSeconds 120` |
| Ren'Py 8.5.3 lint/compile | **PASS** | pinned SDK `renpy.py ... lint --compile` |
| Erii content constraints | **PASS** | `tools/test-content-constraints.ps1` |
| Source/content-lock identity | **PASS** | focused test; lock v3 |
| Diff whitespace | **PASS** | `git diff --check` (line-ending notices only) |

## Source identities

| Source | Lines | SHA-256 |
|---|---:|---|
| `game/chapters/prologue.rpy` | 138 | `d5135e3c124c0cd6ee3455d78210fb45eba5e0e082402ade1961ee1a7b480895` |
| `game/chapters/day1.rpy` | 128 | `8172d12c3676e5b55487ffe76dbb1eb2cbec7e7fd74994e0f9ffe61c1afb01ba` |
| `game/chapters/day2.rpy` | 135 | `fafd4643d207450842c6bbfc0a2c57432a4cd006540c0672b035a0578ff02ec1` |
| `tests/integration/sys_narrative/prose_expansion_sprint009_test.py` | 123 | `0422970c7a3c7eff525d4e87d38b8de673d2533a3f6e3b777e7f18ddf2ca7d9f` |
| `design/narrative/seven-day-content-baseline.md` | 393 | `87e54f616076ef91883ebb687b05468978a7956ecc66bafad512c2797398a85f` |
| `docs/architecture/change-impact-2026-08-14-prose-expansion.md` | 53 | `1073b759472346d2c9888611cb3ad197b8bb86b07a6797e57179906a070cf0d6` |

## Human boundary

Non-test GUI start, manual playtest, SAPI listening, semantic-equivalence
review, copyright/source review, subjective readability/experience review,
performance observation, and final narrative/正典 sign-off are **NOT RUN**.
No human PASS is fabricated, and Sprint 009 does not promote Polish or modify
`production/stage.txt`.
