# Ren'Py Accessibility Capability Spike

> **Status**: Raw engine evidence; not a UX approval
> **Date**: 2026-08-09
> **Engine**: Ren'Py 8.5.3.26051504
> **Host target**: Windows 10/11 x86-64
> **Scope**: focus, viewport, reading order, self-voicing transcript path, SAPI preflight, 1280×720 and 1.5 font layout

This fixture is isolated from production game semantics. It uses the selected
production font candidate `SourceHanSansLite.ttf`, copied from the Ren'Py
8.5.3 SDK and registered at `docs/legal/asset-register.md`; SHA-256
`B2AAF73B7ACC23D746B110F1CAEAECC93D4292824979AF44E96000200591B2A7`.
The license text is at `docs/legal/fonts/SourceHanSansLite-OFL-1.1.txt`.

The test distinguishes:

- **Engine behavior**: keyboard focus, focus coordinates, viewport adjustment, screen reading order and 1.5-scale rendering are exercised by Ren'Py testcase assertions and captures.
- **Transcript behavior**: Ren'Py `debug` self-voicing exposes the exact text selected for voicing. This is a transcript capture path, not a claim that a human heard SAPI output.
- **SAPI capability**: Windows SAPI voice enumeration and the Ren'Py Windows TTS launch path are recorded separately. A transcript is not evidence of voice availability or listening comprehension.

Run with:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\run-renpy-accessibility-spike.ps1
```

The runner must preserve raw stdout/stderr, result JSON, screenshots, focus log, transcript log, SAPI preflight output and environment identity. Any missing artifact is `BLOCKED_INPUT`, not PASS.
