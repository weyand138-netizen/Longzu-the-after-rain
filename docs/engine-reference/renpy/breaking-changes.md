# Ren'Py 8.5.3 Project-Relevant Breaking-Change Review

**Reviewed**: 2026-08-10 against the pinned SDK documentation and `VERSION.md`.

- Ren'Py 8.5 uses Python 3.12-compatible scripts; production Python must remain compatible with that runtime.
- The testcase framework and CLI runner behaviour are treated as 8.5-specific and exercised through `tools/run-renpy-tests.ps1`.
- No project code may rely on a previous engine version's persistence, rollback, screen-action, or build behaviour without a pinned-SDK test.
- Any SDK upgrade requires a new ADR/review, lint, full testcase run, save/load/rollback verification, and Windows build evidence.
