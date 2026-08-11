# Day 3 Content Validation Evidence

**Story**: `production/epics/sys-narrative/story-007-day3-content-validation.md`  
**Requirement**: `TR-NAR-007`  
**Recorded**: 2026-08-11  
**Day 3 source SHA-256**: `dc3626da59e5036c1c202f4f79f260bd6d0f1dd56cc35fd291efa0157cb3d6d5`

## Preserved Engine Run

- Evidence root: `production/qa/evidence/day3-content-validation-2026-08-11/run/`
- Engine: Ren'Py 8.5.3.26051504 on Windows 11 10.0.22631.
- Test command: `renpy.py E:\Longzu test global --savedir <isolated evidence save directory> --report-detailed --overwrite-screenshots`.
- Result: **PASSED** (24/24 testcases and 172/172 assertions).
- Raw output: `run/stdout.txt` (SHA-256 `f68558e5efffc3793123dcae3924b42a7e507527b76cb548f39418df67c9cef3`).
- Raw stderr: `run/stderr.txt` (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).
- Machine-readable runner record: `run/result.json`; `status_line` is `[rpytest] Status: PASSED` and the isolated save directory is `run/saves/`.

The established wrapper treats the terminal PASSED record, complete 24/24 and
172/172 summaries, and matching raw-output hashes as the authoritative success
criterion. It then kills Ren'Py's still-open display loop, so `result.json`
deliberately records subprocess `exit_code: -1`; that code alone is never
interpreted as a product pass. The integration verifier fails closed unless this
known wrapper outcome, terminal PASSED marker, exact summaries, and all hashes
agree.

The engine submits all four Day 3 combinations by keyboard from a Day 2-compatible
canonical-history setup: share/honor, share/force, withhold/honor, and
withhold/force. Each route asserts both sibling controls are available before
activation, exact immediate-reaction text, exact ordered Day 2-to-Day 3 history,
and then advances through the Day 3 return to a fresh prologue choice surface
without traceback. The quick menu is absent during critical input.

## Visual and Accessibility Results

| Baseline | Capture | Result |
| --- | --- | --- |
| 1280x720, keyboard focus, silent, reduced motion | `run/screenshots/visual/day3_evidence_1280x720_keyboard_silent_reduced_motion.png` | 1280x720 PNG; 29,911 bytes; SHA-256 `6aa757eb34ce0adf7a80c9cdc5057ca9f097c59fd635d2bb770a57e56053ba23`. Evidence choices and the natively focused underlined control are visible; quick menu is absent. |
| 1280x720, keyboard focus, silent, reduced motion | `run/screenshots/visual/day3_truth_pace_1280x720_keyboard_silent_reduced_motion.png` | 1280x720 PNG; 27,265 bytes; SHA-256 `0a2848d133da160190076896dd90cdd5b293feabe1d40cb45ce451ee9d961d59`. Truth-pace choices and the natively focused underlined control are visible; quick menu is absent. |
| 1280x720, 1.5x font, high contrast, reduced motion | `run/screenshots/visual/day3_evidence_1280x720_font_1_5_high_contrast.png` | 1280x720 PNG; 41,768 bytes; SHA-256 `0597043403e60c433f975f4b0963890c5264417dd39398208c4ec5bb33955c14`. Evidence captions remain readable, focusable, and unclipped. |
| 1280x720, 1.5x font, high contrast, reduced motion | `run/screenshots/visual/day3_truth_pace_1280x720_font_1_5_high_contrast.png` | 1280x720 PNG; 37,108 bytes; SHA-256 `d976e15e0a4df0537f08eb80a018c82528b8f6787f7c57baa6ffdd3a7b3a4ecf`. Truth-pace captions remain readable, focusable, and unclipped. |

The visual testcase pins the physical surface, disables self-voicing, uses
reduced motion in both variants, and observes native default focus before each
capture. The Day 3 focused choice has an underline in addition to colour, so
keyboard focus is not colour-only. Decision facts are Chinese text available
through keyboard menus; availability, canonical IDs, reaction, and continuation
do not depend on colour, hover, sound, motion, or timed input.

## Content Review and Scope Boundary

**PASS.** The source generation matches Story 006's owner record.
`game/modules/narrative_partial_manifest.py` remains Day 1-only
`narrative_partial_day1_manifest:v1`; it contains no Day 3 data. There is no
Day 3 partial manifest expansion, and this record does not claim full-manifest,
terminal-witness, ending, or release validation.
