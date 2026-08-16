# QA Plan — Sprint 013 Non-Formal-Asset Automation Preflight

Date: 2026-08-16
Stage: Production
Scope: source identity, topology, automation contracts, regression, smoke, and evidence integrity
Out of scope: all formal visual/audio/voice assets and their integration

The original `production/qa/qa-plan-sprint-013-2026-08-15.md` is retained as historical evidence. This plan is the active preflight layer and does not rewrite or delete the original blocked-input records.

## Current preflight must-have

| ID | Deliverable | Verification |
|---|---|---|
| P13-01 | Refresh content-lock/source identity; record semantic diff | targeted source hash, UX/content constraint checks |
| P13-02 | Review and accept ADR-0010/topology | focused architecture review and topology tests |
| P13-03 | Bind candidate and complete narrative-flow manifests to the non-asset HEAD | manifest schema, 15-unit, resolver and source-hash checks |
| P13-04 | Validate automated seven-day, six-ending, save and accessibility contracts | ordinary Python and Ren'Py global suites |
| P13-05 | Verify regression, smoke and evidence classification | root unittest, compile/lint, content constraints, diff check |
| P13-06 | Provide explicit Production RC closeout runner | final gate reports `BLOCKED_INPUT`/`REPORT_ONLY` when external evidence is absent |

## Test layers

1. `python -m unittest discover` must be green for code contracts and fail-closed classification.
2. Ren'Py global tests, lint/compile, content constraints and `git diff --check` must pass for the preflight scope.
3. The explicit `tools/run-production-closeout-gate.py --final` is the only layer that evaluates external RC evidence as a non-PASS gate result.
4. Performance is protocol-only and `REPORT_ONLY`; no formal asset-affected sample is claimed.

## Deferred Production RC closeout inputs

After formal assets are merged, the next Sprint must provide: real GUI seven-day execution and six human ending witnesses; keyboard/mouse operation; SAPI transcript and listening review; semantic-equivalence review; new-player playtest; asset-affected performance samples; DOCX owner-boundary input if the referenced file becomes available; final archive; final QA/evidence bundle; and an explicit Production → Polish decision. These are not ordinary regression blockers, but they remain mandatory final-release requirements.

## Current definition of done

All automated preflight checks pass, the current candidate and narrative manifests are bound to the trusted non-asset HEAD, content-lock has zero Sprint 013 copy delta, ADR-0010 is Accepted, the explicit closeout gate preserves missing external inputs as non-PASS, and `production/stage.txt` remains `Production`.
