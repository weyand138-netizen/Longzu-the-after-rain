# Day 2 Content Validation Evidence

**Story**: `production/epics/sys-narrative/story-005-day2-content-validation.md`  
**Requirement**: `TR-NAR-005`  
**Recorded**: 2026-08-11  
**Day 2 source SHA-256**: `fafd4643d207450842c6bbfc0a2c57432a4cd006540c0672b035a0578ff02ec1`

## Preserved Engine Run

- Evidence root: `production/qa/evidence/day2-content-validation-2026-08-11/run/`
- Engine: Ren'Py 8.5.3.26051504 on Windows 11 10.0.22631.
- Test command: `renpy.py E:\Longzu test global --savedir <isolated evidence save directory> --report-detailed --overwrite-screenshots`.
- Result: **PASSED** — 18/18 testcases and 102/102 assertions.
- Raw output: `run/stdout.txt` — SHA-256 `2c120a8874736b9a08c206d4a955828c0b5862eca8e26864adae59a3a5c8a3c8`.
- Raw stderr: `run/stderr.txt` — SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Machine-readable runner record: `run/result.json`.

The Day 2 routes submit choices by keyboard and reach the last-machine handoff
without a traceback: accept-alias plus save-token, assign-alias plus
spend-both-tokens, and the prior `token_silence_as_consent` repair route plus
save-token. Each route asserts its exact ordered history, so an unavailable,
unknown, or duplicate choice activation fails the testcase.

The added `day2_keyboard_default_focus_and_traversal_contract` never assigns
focus programmatically. It directly observes automatic `day1_choice_0` focus
on both Day 2 choice surfaces, uses the player keyboard's down-arrow traversal
to reach and activate the second option, and reaches the conditional repair
option with two down-arrow steps before activation. Its resulting histories
and immediate reactions are asserted in-engine.

## Visual and Accessibility Results

| Baseline | Capture | Result |
| --- | --- | --- |
| 1280×720, keyboard focus, silent, reduced motion | `run/screenshots/visual/day2_alias_1280x720_keyboard_silent_reduced_motion.png` | 1280×720 PNG; 26,415 bytes; SHA-256 `47de8ee60c02666d4834f517bebba7c183a7580cc9988f4fcbb7932057a9b8b3`. Alias choices are visible with first-choice keyboard focus and no quick menu. |
| 1280×720, keyboard focus, silent, reduced motion | `run/screenshots/visual/day2_tokens_1280x720_keyboard_silent_reduced_motion.png` | 1280×720 PNG; 37,368 bytes; SHA-256 `b4b8f058d2507ea0c2fb11146def3bf5e9d87bc36fa6eb53ef266310ca8617cf`. Both token trade-off captions are visible with first-choice focus and no quick menu. |
| 1280×720, 1.5× font, high contrast, reduced motion | `run/screenshots/visual/day2_alias_1280x720_font_1_5_high_contrast.png` | 1280×720 PNG; 37,045 bytes; SHA-256 `ccdbc09d6848d46939bf6e3d3f8aa42e815bb4c589ae5537ef6a570943d2fb30`. Alias captions remain readable and the focus treatment is black/white. |
| 1280×720, 1.5× font, high contrast, reduced motion | `run/screenshots/visual/day2_tokens_1280x720_font_1_5_high_contrast.png` | 1280×720 PNG; 49,440 bytes; SHA-256 `7228a209df1b8c20fddd8fc19e729e639d3d0813b1eacc2e8eecca1a146f726f`. The longer two-token captions remain readable and keyboard-operable. |

The testcase pins the physical surface, disables self-voicing before capture,
sets stable first focus, and asserts that `quick_menu_root` is absent on every
critical Day 2 choice surface. Day 2’s alias and token trade-offs are visible
Chinese text; no response availability, immediate reaction, final handoff, or
canonical ID depends on colour, hover, audio, motion, arcade presentation, or
timed input.

## Content Review

**PASS.** The authored unit retains exactly the five approved Day 2
choice/reaction/payoff joins and the history-derived
`day2_admit_alias_unknown` repair gate. `game/modules/narrative_partial_manifest.py`
remains the ADR-0009 Day 1-only `narrative_partial_day1_manifest:v1`: it has no
Day 2 partial manifest, Day 2 alias, future source, terminal field, or terminal
witness. This evidence does not claim a full manifest, ending validation, or
terminal continuation witness; those remain deferred until their approved
scope exists.
