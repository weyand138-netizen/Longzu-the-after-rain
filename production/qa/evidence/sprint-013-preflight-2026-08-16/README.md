# Sprint 013 Preflight Evidence Bundle

This small bundle contains only evidence produced by the 2026-08-16 automation preflight. It is not a replacement for, and does not absorb, the historical Sprint 013 evidence directories.

## Recorded commands

- `python -m unittest discover` — 350/350 PASS.
- `python -m unittest discover -s tests -p '*_test.py'` — 350/350 PASS.
- `python -m compileall -q game/modules tests tools` — exit 0.
- `tools/run-renpy-tests.ps1 -Suite global -TimeoutSeconds 120` — 56/56 cases and 474/474 assertions PASS.
- Ren'Py 8.5.3 `lint --compile` with project-local APPDATA — exit 0.
- `tools/test-content-constraints.ps1` — Erii dialogue constraint PASS.
- `git diff --check` — no whitespace errors.
- `tools/run-production-closeout-gate.py --final` — exit 1, expected `BLOCKED_INPUT` for deferred RC evidence and `REPORT_ONLY` for performance.

The full classifications are in the adjacent smoke, evidence-review, and gate-check reports. No external evidence is represented as PASS.
