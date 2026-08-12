# Day 4 Content Validation Evidence

**Story**: `production/epics/sys-narrative/story-010-day4-content-validation.md`
**Requirement**: `TR-NAR-010`
**Recorded**: 2026-08-11
**Day 4 source SHA-256**: `dc62786bf08623b243dca77a5e24e37c17084d39e37e3041985e3a9350fccaac`

## Preserved Engine Run

- Evidence root: `production/qa/evidence/day4-content-validation-2026-08-11/run/`
- Engine: Ren'Py 8.5.3.26051504 on Windows 11 10.0.22631.
- Test command: `renpy.py E:\Longzu test global --savedir <isolated evidence save directory> --report-detailed --overwrite-screenshots`.
- Result: **PASSED** (30/30 testcases and 255/255 assertions).
- Raw output: `run/stdout.txt` (SHA-256 `f95724edad23e47a2c24cd95f5a7da4e676ef808801aaa3d30dce9de173c3d64`).
- Raw stderr: `run/stderr.txt` (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).
- Machine-readable runner record: `run/result.json`; `status_line` is `[rpytest] Status: PASSED` and the isolated save directory is `run/saves/`.

The established wrapper terminated the post-report Ren'Py display loop, so the
recorded process `exit_code: -1` is expected. The terminal status and exact
testcase/assertion totals remain authoritative. This bundle is not a release,
terminal, ending, or full-manifest claim.

The three canonical Day 4 keyboard routes pass: two-ticket/contact-register,
single-ticket/contact-decline, and no-backup/contact-register. The guarded
no-backup route also passes: contact remains unavailable when a retained token
is paired with `day2_assign_alias`, and is available only after either approved
alias outcome plus the retained token. The routes assert exact ordered Day
2/Day 3/Day 4 histories, reactions, resources, events, outcomes, and the
existing test-harness continuation to a fresh prologue choice surface. No Day 5
source or label was added; Day 5 is outside this story's scope.

## Visual and Accessibility Results

| Baseline | Capture | Result |
| --- | --- | --- |
| 1280x720, keyboard focus, silent, reduced motion | `run/screenshots/visual/day4_route_1280x720_keyboard_silent_reduced_motion.png` | 1280x720 PNG; SHA-256 `95df99098cb299c84ea72ec3dd6bc727a6ca729c101eae4cb1028c19e5c23bb5`. |
| 1280x720, keyboard focus, silent, reduced motion | `run/screenshots/visual/day4_contact_1280x720_keyboard_silent_reduced_motion.png` | 1280x720 PNG; SHA-256 `818d765a98875f618b6f1b3fac037f71176373f9ca7745cbe148a2c7a50f9b20`. |
| 1280x720, 1.5x font, high contrast, reduced motion | `run/screenshots/visual/day4_route_1280x720_font_1_5_high_contrast.png` | 1280x720 PNG; SHA-256 `698bb5e24b91037d0e1370199550767c7de1bc36ffaec15b34749d603bc928a9`. |
| 1280x720, 1.5x font, high contrast, reduced motion | `run/screenshots/visual/day4_contact_1280x720_font_1_5_high_contrast.png` | 1280x720 PNG; SHA-256 `67d89c903d800376e6c6cb072eda527e4895e82b299744e8a17ce69e4151e8d3`. |

The testcases set the physical surface, disable self-voicing, use reduced
motion in both variants, observe native default focus, traverse by arrow keys,
and keep the quick menu absent during critical input. The focused Day 4 control
has the existing underline in addition to colour, so focus is not colour-only.

## Content Review and Scope Boundary

`game/modules/narrative_partial_manifest.py` remains Day 1-only
`narrative_partial_day1_manifest:v1`; it contains no Day 4 data. There is no Day
4 partial manifest expansion. This evidence does not claim full-manifest,
terminal-witness, ending, or release validation.
