# Day 7 Handoff and Accessibility Evidence

**Date**: 2026-08-14
**Scope**: Sprint 6 / Story 022 objective Day 7 handoff and accessibility
validation. The Ren'Py runtime implementation root for this project is
`game/`; no empty `src/` directory is used or implied.

## Generation Binding

- **Day 7 source SHA-256**:
  `017e1582d1dfcb0b78d4c8f2545b41090f4b6bf24763fdcb59e0f58984f8f214`
- **Testcases SHA-256**:
  `3824e0756da12701a0ff7cb018c0ff9a80953bd82892bdbc21d0cce5147982d6`
- **Runner stdout SHA-256**:
  `0190453127efb34fe3a68db1aceac25632f0889594451a0db690e5dc0078ed4e`
- **Runner stderr SHA-256**:
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Automated Result

`tools/run-renpy-day7-evidence.ps1` ran the pinned Ren'Py
8.5.3.26051504 global suite in a fresh evidence-local save directory. The
machine-readable result at `run-passed/result.json` records the terminal
runner status `[rpytest] Status: PASSED`, process exit `-1`, 56/56 testcases,
and 474/474 assertions.

The tracked stdout copy has only terminal line-end whitespace normalized so the
repository passes `git diff --check`; its SHA-256 above binds the normalized
copy. The runner's pre-normalization byte digest was
`bb8ab5c87fec9a6bcff091e465066fd026ba932cb3c222644b1e3c3b81e79055`.

The suite drives exactly one Day 7 handoff for each frozen canonical history:
`rain_stops`, `her_own_name`, `see_the_sea`, `one_person_train`,
`golden_cage`, and `unsent_postcard`. It asserts that each prior choice
history and five-axis snapshot are unchanged before the resolver-owned label
is entered. Golden Cage is explicitly the frozen
`day5_replace_erii_response` path, never `day5_honor_erii_response`, with
the unchanged `3/2/3/2/1` axis vector. The fail-closed checks leave lifecycle,
pending ending, persistence, achievements, seen endings, and memory empty or
unchanged as applicable.

## Accessibility Captures

| Capture | SHA-256 | Baseline |
|---|---|---|
| `day7_causal_recall_1280x720_keyboard_silent_reduced_motion.png` | `4a6d8c0726f2da70b4b52c1b1f59f8c7a70378d3c6c0e03bd4d8f23511830182` | 1280x720, keyboard, silent, reduced motion |
| `day7_causal_recall_1280x720_font_1_5_high_contrast.png` | `4a6d8c0726f2da70b4b52c1b1f59f8c7a70378d3c6c0e03bd4d8f23511830182` | 1280x720, 1.5x font, high contrast, reduced motion |

Both captures are valid 1280x720 PNGs. The deterministic scene pixels are
identical; the engine testcase separately asserts the applied font-size,
high-contrast, self-voicing, reduced-motion, and no-quick-menu-focus runtime
settings. Human visual/readability review remains required.

## Scope Boundary

This bundle verifies only the Day 7 authored handoff and its objective
contracts. It does not claim six-ending prose, completion, epilogue, resolver
semantics, route qualification, release, or human narrative/readability
approval.
