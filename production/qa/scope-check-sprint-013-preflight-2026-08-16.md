# Scope Check — Sprint 013 Automation Preflight

Date: 2026-08-16
Baseline: `HEAD ff00c7a`
Decision: **in scope and contained**

## Quantified re-scope

| Original Sprint 013 grouping | Current treatment | Count / boundary |
|---|---|---|
| Automation/source contracts | Active current Sprint 013 | 6 P13 must-have tasks |
| GUI seven-day and six human witnesses | Future Production RC Closeout Sprint | 2 preserved N13 records |
| Keyboard/mouse, SAPI and semantic review | Future Production RC Closeout Sprint | 3 preserved N13 records |
| New-player playtest | Future Production RC Closeout Sprint | 1 preserved N13 record |
| Asset-affected performance | Future Production RC Closeout Sprint; current protocol `REPORT_ONLY` | 1 preserved N13 record |
| DOCX provenance/owner boundary | Future Production RC Closeout Sprint | 1 preserved N13 record; source path absent |
| Archive, final QA and Production → Polish | Future Production RC Closeout Sprint | 2 preserved N13 records |
| Historical Should Have follow-ups | Future Production RC Closeout Sprint | 3 preserved S13 records |

The old task tables and old QA/evidence directories remain in the worktree as historical records. The active plan and `sprint-status.yaml` explicitly place those records under `deferred_rc_closeout`; their `BLOCKED_INPUT`/`REPORT_ONLY` states are not used to fail ordinary automation regression.

## Exclusions verified

- No character art, backgrounds, CG, UI bitmap, VFX, music, sound-effect, or voice asset was generated, admitted, connected, or modified.
- `E:\Longzu-assets` was not read or modified.
- `production/stage.txt` was not modified; current stage remains `Production`.
- No push, PR, or production-stage promotion was performed.

## Scope conclusion

The current Sprint 013 delivers only source identity, architecture/topology, non-asset candidate/flow manifests, automated contracts, regression/smoke/evidence classification, and the explicit final gate boundary. The deferred RC list remains mandatory and is not weakened by this re-scope.
