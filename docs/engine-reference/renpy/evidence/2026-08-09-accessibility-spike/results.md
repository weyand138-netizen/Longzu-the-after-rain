# Ren'Py Accessibility Spike — focus-aware viewport rerun

> **Run:** `2026-08-09-accessibility-spike-rerun-26`
> **Engine:** Ren'Py 8.5.3.26051504
> **Host:** Windows 11 build 22631
> **Viewport:** 1280x720

## Result

**PASS — 4/4 testcases and 18/18 assertions.**

The fixture now establishes `first_action` without mouse input. Keyboard navigation is routed through the project `FocusAwareGraph`; `focus_graph_next` and `focus_graph_previous` own Tab and Shift+Tab, while the Ren'Py skip binding remains disabled. The helper scrolls the target before focusing it and never invokes the target action.

The offscreen `deep_action` target is reached by keyboard-only navigation. The final evidence records `viewport_y` changing from `0.0` to `221.0`; the target is then fully visible and `deep_action_count` remains `0`.

## Testcases

| Testcase | Result |
|---|---|
| Focus order, initial focus, and safe exit | PASS |
| Font scale 1.5 layout | PASS |
| Offscreen focus auto-scroll and non-activation | PASS |
| Debug self-voicing transcript | PASS |

## Evidence

All final artifacts are under `../2026-08-09-accessibility-spike-rerun-26/run/`:

- `stdout.txt` and `stderr.txt` — original Ren'Py process output.
- `result.json` — command, environment, exit status, and output hashes.
- `focus-log.json` — semantic focus, focus rectangles, focus list, and viewport state.
- `viewport-log.json` — viewport position/range and full-visibility checks.
- `screenshots/visual/focus_initial_1280x720.png`
- `screenshots/visual/focus_second_visible_1280x720.png`
- `screenshots/visual/focus_deep_visible_1280x720.png`
- `screenshots/visual/layout_1280x720_font_1_5.png`
- `transcript-log.txt` and `sapi-preflight.json` — transcript and capability evidence; no human listening PASS is inferred.

The production implementation is `game/modules/accessibility_focus.py`; the Spike fixture carries the same helper under `fixture/game/modules/accessibility_focus.py` and exercises it through the same focus graph contract.
