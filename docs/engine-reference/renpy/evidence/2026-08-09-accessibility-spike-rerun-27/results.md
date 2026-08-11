# Ren'Py Accessibility Spike — P0 rerun

> **Run:** `2026-08-09-accessibility-spike-rerun-27`
> **Engine:** Ren'Py 8.5.3.26051504
> **Host:** Windows 11 build 22631
> **Viewport:** 1280×720

## Result

**PASS — 4/4 testcases and 18/18 assertions.**

The focus graph establishes the first semantic action without mouse input,
routes Tab/Shift+Tab through the project keymap, scrolls the offscreen target
before focusing it, and never activates the target while moving focus.

The run records `viewport_y` changing from `0.0` to `221.0`; the target is fully
visible and `deep_action_count` remains `0`. The 1.5 font layout, reading order,
safe Escape exit, and debug self-voicing transcript also passed.

## Evidence

Raw artifacts are under `run/`: `stdout.txt`, `stderr.txt`, `result.json`,
`focus-log.json`, `viewport-log.json`, screenshots, `transcript-log.txt`, and
`sapi-preflight.json`. The preflight enumerated three Windows voices, including
Simplified Chinese; this is capability evidence only and does not claim human
listening comprehension.
