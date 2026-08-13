# Day 5 Content Validation Evidence

**Story**: `production/epics/sys-narrative/story-014-day5-content-validation.md`
**Requirement**: `TR-NAR-014`
**Recorded**: 2026-08-13
**Day 5 source SHA-256**: `9ec6fd98498902c8bfe1bc0a72c9f497d0be8a584ce5d289853e532f4168e432`
**Testcase source SHA-256**: `6ec6b92d5df8b91f852db4831783698b14a0b27d0f6aa8cbb7c4c5ed52e503ad`

## Preserved Engine Run

- Evidence root: `production/qa/evidence/day5-content-validation-2026-08-13-reviewed-verified/run-passed/`.
- Engine: Ren'Py 8.5.3.26051504 on Windows 11 10.0.22631.
- Test command: `renpy.py E:\Longzu test global --savedir <isolated evidence save directory> --report-detailed --overwrite-screenshots`.
- Result: **PASSED** (37/37 testcases and 345/345 assertions).
- Raw output: `run-passed/stdout.txt` (SHA-256 `4fa0f6fba89f72a69d6662e28b7f0e5b403c1d95b96628cb994ee330865e4175`).
- Raw stderr: `run-passed/stderr.txt` (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).
- Machine-readable runner record: `run-passed/result.json`; `status_line` is `[rpytest] Status: PASSED` and the isolated save directory is `run-passed/saves/`.

The evidence wrapper closes Ren'Py's post-report display loop. Consequently
the recorded process `exit_code: -1` is expected; terminal status and exact
testcase/assertion totals are authoritative. Earlier Day 5 attempts remain
preserved in their own roots and are not used as passing evidence.

The engine routes exercise keyboard traversal of full archive and safe summary,
self-liability and external-only liability, valid shared/contact/solo/empty
resource facts, honor/replace response, eligible school/daily repairs, and the
invalid-fact fail-closed response omission. The derivation records only the
closed Day 4 resource facts and their visible action/object evidence. Exact
history, axes, unresolved-token effects, events, outcomes, focus, and the
existing continuation seam are asserted by the testcase suite.

## Visual and Accessibility Results

| Baseline | Capture | Result |
| --- | --- | --- |
| 1280x720, keyboard focus, silent, reduced motion | `run-passed/screenshots/visual/day5_truth_1280x720_keyboard_silent_reduced_motion.png` | 1280x720 PNG; SHA-256 `b10511edcf42c70f21506d0c3c1e05668b5d845f1f04c6312125758a3d5ba077`. |
| 1280x720, keyboard focus, silent, reduced motion | `run-passed/screenshots/visual/day5_response_1280x720_keyboard_silent_reduced_motion.png` | 1280x720 PNG; SHA-256 `3d66b92ed645d071dbf4a9130a7a1936c15c4346ce14d6e3f79e6c7276566b62`. |
| 1280x720, 1.5x font, high contrast, reduced motion | `run-passed/screenshots/visual/day5_truth_1280x720_font_1_5_high_contrast.png` | 1280x720 PNG; SHA-256 `0b1447ca7e69505cbba46f0ca704641084cdb93f52461245cd7f76daea1c5a91`. |
| 1280x720, 1.5x font, high contrast, reduced motion | `run-passed/screenshots/visual/day5_response_1280x720_font_1_5_high_contrast.png` | 1280x720 PNG; SHA-256 `aab19a6be0bf22160bd8233583a7a1ae44ef017aa3a1fe61c4a96f1d7a089161`. |

The testcases set physical 1280x720, disable self-voicing, use reduced motion
in both variants, observe native default focus without assigning it, traverse
by keyboard, and keep quick-menu controls absent during critical input. The
focused control has the existing underline as well as contrast treatment, so
focus is not colour-only.

## Content Review and Scope Boundary

`game/modules/narrative_partial_manifest.py` remains the Day 1-only
`narrative_partial_day1_manifest:v1`; it contains no Day 5 data. There is no
Day 5 partial manifest expansion. This evidence does not claim full-manifest,
terminal-witness, ending, epilogue, or release validation.
