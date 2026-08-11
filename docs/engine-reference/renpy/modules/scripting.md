# Ren'Py 8.5.3 Scripting, State, and Test Reference

**Pinned SDK**: `.tools/renpy-8.5.3-sdk` (Ren'Py 8.5.3.26051504)  
**Verified**: 2026-08-10  
**Knowledge risk**: High — all implementation choices below require pinned-SDK verification.

## Verified Local Sources

| Area | SDK source / documentation | Project consequence |
|---|---|---|
| Persistent state | `doc/persistent.html`; `renpy/config.py`; `renpy/common/00db_ren.py` | Initialize project persistent fields with `default persistent.<field>` and keep them outside rollback-owned run state. |
| Rollback | `doc/rollback.html`; `renpy/config.py`; `renpy/game.py`; `renpy/loadsave.py` | Use Ren'Py-managed script/default state for mutable run data; imported Python modules may validate/transform snapshots but must not own live mutable state. |
| Screens and actions | `doc/screen_actions.html`; `doc/screens.html`; `renpy/display/behavior.py` | Screen actions must preserve focusability/visibility semantics and must not bypass action gates. |
| Testcases | `doc/testcases.html`; `renpy/ast.py`; `renpy/test/` | Run the project wrapper because it isolates APPDATA and terminates the post-report display loop. |
| CLI/lint | `doc/cli.html`; pinned `renpy.py` | CLI behaviour is revalidated by the project wrapper on this SDK version; do not treat shell exit behavior as an undocumented invariant. |

## Approved Project Patterns

- `default` owns per-playthrough mutable state; replacement assignment protects rollback semantics.
- `persistent.sys_persist_state` is the only product persistent root; validate the detached candidate before one root replacement and `renpy.save_persistent()`.
- Narrative content is authored as `.rpy` labels and may call only approved pure adapters. It must not inspect persistent data, hidden scores, test fixtures, or network state.
- Engine verification for each new content unit includes the global testcase suite, lint/compile, and source-manifest scan.

## Explicitly Rejected Patterns

- Mutable game state in imported `.py` modules.
- Separate JSON/save authority, direct persistent writes from screens, or a production dependency on test-only sources.
- Unpinned SDK execution or undocumented CLI parsing as a release decision.
