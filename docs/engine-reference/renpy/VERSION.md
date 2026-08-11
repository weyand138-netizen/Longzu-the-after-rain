# Ren'Py Version Reference

| Field | Value |
|---|---|
| Engine | Ren'Py |
| Pinned version | 8.5.3 |
| Release date | 2026-05-15 |
| Project pinned | 2026-07-23 |
| Python compatibility | Python 3.12-compatible scripts |
| Knowledge risk | High: version is newer than the May 2025 baseline |

## Verified official references

- Release: https://www.renpy.org/release/8.5.3
- CLI: https://www.renpy.org/doc/html/cli.html
- Automated tests: https://www.renpy.org/doc/html/testcases.html
- Persistent data: https://www.renpy.org/doc/html/persistent.html
- Achievements: https://www.renpy.org/doc/html/achievement.html
- Build distributions: https://www.renpy.org/doc/html/build.html
- Incompatible changes: https://www.renpy.org/doc/html/incompatible.html

## Project-relevant 8.5 facts

- Ren'Py 8.5 introduced the `testcase` and `testsuite` automated testing framework.
- Ren'Py 8.4+ uses Python 3.12; project Python must remain forward-compatible.
- Persistent fields should be initialized with `default persistent.<field>`.
- Imported `.py` modules are not transformed for rollback. They may compute and return values but must not own mutable live game state.
- CLI syntax is not a stable public interface, so CI commands must be revalidated when upgrading.

## Upgrade policy

Do not move away from 8.5.3 during production without:

1. reviewing the official incompatible-changes page;
2. running lint and all testcases;
3. verifying save, load, rollback, persistent achievements, and Windows builds;
4. recording the change in an ADR.

