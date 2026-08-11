# Ren'Py 8.5.3 Deprecated / Disallowed API Review

**Reviewed**: 2026-08-10.

No deprecated engine API is admitted by the current P0 architecture. The project additionally disallows the following patterns regardless of engine support:

- storing live mutable game state in imported Python modules;
- direct screen-local mutation of `persistent.sys_persist_state`;
- a second save/persistence authority or production-to-test-only import;
- unpinned engine invocation or network/telemetry calls.

New engine APIs must be added to the relevant local module reference and verified against the pinned SDK before adoption.
