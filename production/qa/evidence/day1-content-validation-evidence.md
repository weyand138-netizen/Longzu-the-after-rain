# Day 1 Content Validation Evidence

**Story**: `production/epics/sys-narrative/story-003-day1-content-validation.md`  
**Requirement**: `TR-NAR-001`  
**Recorded**: 2026-08-10  
**Source SHA-256**: `8172d12c3676e5b55487ffe76dbb1eb2cbec7e7fd74994e0f9ffe61c1afb01ba`

## Preserved Engine Run

- Evidence root: `production/qa/evidence/day1-content-validation-2026-08-10-r9/run/`
- Engine: Ren'Py 8.5.3.26051504 on Windows 11 10.0.22631.
- Test command: `renpy.py E:\Longzu test global --report-detailed --overwrite-screenshots` with an isolated save directory.
- Result: **PASSED** — 13/13 testcases and 63/63 assertions.
- Raw output: `run/stdout.txt` — SHA-256 `70a7703dce7e0538d062f4d277adc4ee2b1dff345a72ffe70c2eb1893cb9997c`.
- Raw stderr: `run/stderr.txt` — SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Machine-readable runner record: `run/result.json`.

## Visual and Accessibility Results

| Baseline | Capture | Result |
| --- | --- | --- |
| 1280×720, keyboard focus, silent, reduced motion | `run/screenshots/visual/day1_choice_1280x720_keyboard_silent_reduced_motion.png` | 1280×720 PNG; 25,912 bytes; SHA-256 `28053a6304e71815a6d68faade80a401128bfb0b8f6d196599cd39482a94fe63`. First choice focus is visible; both required choices are readable and the quick menu is absent. |
| 1280×720, 1.5× font, high contrast, reduced motion | `run/screenshots/visual/day1_choice_1280x720_font_1_5_high_contrast.png` | 1280×720 PNG; 36,012 bytes; SHA-256 `22fd7078b9e72c394e7b234e1f82bab034972d1c0fde76b31e76f0b5cf62e05c`. Both choice captions are fully visible and the focused first choice has a distinct white/black contrast treatment. |

The route testcase sets a stable first choice focus and submits both Day 1
choices with `K_RETURN`; it verifies the two canonical choice history IDs and
that `quick_menu_root` is absent at each critical choice. Reduced motion
suppresses the Day 1 opening dissolve. Day 1 source has no decision-relevant
audio cue, and `run/sapi-preflight.json` records three available SAPI voices
without inferring a human-listening result.

## Content Review

**PASS.** Day 1 stays within the partial-Day-1 boundary: the implemented route
contains the two formal Day 1 choices, their immediate reactions, and the
receipt-name handoff only. It contains no future placeholder, ending entry,
direct ending edge, test-only production edge, hidden score wording, or
decision-relevant audio/motion-only fact. ADR-0009 remains the controlling
boundary for the deferred full manifest and terminal ending witness.
