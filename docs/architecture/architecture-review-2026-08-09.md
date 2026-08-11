# Architecture Review Report

Date: 2026-08-09  
Mode: `full`  
Engine: Ren'Py 8.5.3 / Python 3.12  
System GDDs reviewed: 12  
ADRs reviewed: 7

## Scope and Inputs

Reviewed the 12 system GDDs linked by `design/gdd/systems-index.md`, the game
concept, systems index, master architecture, ADR-0001 through ADR-0007, the
Ren'Py engine reference, technical preferences, and the consistency-failure log.

The stable TR registry did not exist before this review. The 18 TR-IDs recorded
below are therefore the initial stable registry entries created by this run.

## Traceability Summary

| Status | Count |
|---|---:|
| Covered | 10 |
| Partial | 5 |
| Current gap | 1 |
| Deferred to post-MVP | 2 |
| **Total** | **18** |

The row-level statuses above correct the stale aggregate count in
`docs/architecture/architecture.md`, which currently reports three gaps even
though two SYS-TENSION rows are explicitly deferred.

## Traceability Matrix

| TR-ID | GDD / System | Requirement | ADR Coverage | Status |
|---|---|---|---|---|
| TR-STATE-001 | five-axis-state.md / SYS-STATE | Schema 2, five axes, and ordered history share one rollback/save envelope | ADR-0002, ADR-0004, ADR-0005 | Covered |
| TR-STATE-002 | five-axis-state.md / SYS-STATE | Strict validation and one complete replacement assignment | ADR-0004 | Covered |
| TR-END-001 | deterministic-ending-resolution.md / SYS-ENDING | Deterministic total six-ending resolution without randomness | ADR-0001 | Covered |
| TR-END-002 | deterministic-ending-resolution.md / SYS-ENDING | Counterevidence, cause lineage, terminal compatibility, and resolver purity | ADR-0001, ADR-0005 | Covered |
| TR-CHOICE-001 | choice-and-causality-record.md / SYS-CHOICE | Every player-facing choice commits through SYS-STATE | ADR-0002, ADR-0005 | Covered |
| TR-CHOICE-002 | choice-and-causality-record.md / SYS-CHOICE | Exact reaction/payoff joins and terminal continuation witness coverage | None | Gap |
| TR-NAR-001 | seven-day-chapter-script.md / SYS-NARRATIVE | Seven-day chapter paths and six endings are valid and content-locked | ADR-0003 | Partial |
| TR-SAVE-001 | save-load-rollback.md / SYS-SAVE | Free save, load, and rollback remain supported | ADR-0002, ADR-0004 | Covered |
| TR-SAVE-002 | save-load-rollback.md / SYS-SAVE | Legacy, unsupported, and corrupt loads enter a blocking safe flow | ADR-0002, ADR-0005 | Covered |
| TR-PERSIST-001 | cross-playthrough-unlocks.md / SYS-PERSIST | Schema-v2 root, 12-leaf authority, epoch, settings, merge/reset, and flush | ADR-0002 | Covered |
| TR-PERSIST-002 | cross-playthrough-unlocks.md / SYS-PERSIST | Ending completion emits one durable completed-event boundary | ADR-0002, ADR-0006 | Covered |
| TR-ACH-001 | local-achievements.md / SYS-ACHIEVE | Eleven event-based achievements evaluate and persist independently and idempotently | ADR-0002 | Partial |
| TR-JOURNAL-001 | sys-journal.md / SYS-JOURNAL | Journal bundle/read model exposes chapters, memories, endings, and achievements | ADR-0003 | Partial |
| TR-ACCESS-001 | sys-access.md / SYS-ACCESS | Keyboard, scale, contrast, self-voicing, captions, and effect alternatives remain semantically equivalent | ADR-0002, ADR-0003 | Partial |
| TR-TENSION-001 | sys-tension.md / SYS-TENSION | Timeout maps to a canonical choice and does not alter ending rules | None; feature deferred | Deferred |
| TR-TENSION-002 | sys-tension.md / SYS-TENSION | Tension preference survives restart but not per-run rollback | Future ADR; feature deferred | Deferred |
| TR-TEST-001 | sys-test.md / SYS-TEST | Lint, pure logic, engine testcase, and gate evidence control hand-off | ADR-0007 partially covers release evidence | Partial |
| TR-BUILD-001 | sys-build.md / SYS-BUILD | Offline Windows package includes legal and integrity provenance | ADR-0007, with ADR-0003 asset boundary | Covered |

## Coverage Gaps

### Current P0 gap

- `TR-CHOICE-002`: no ADR owns the SYS-CHOICE/SYS-NARRATIVE exact join,
  cardinality, CFG, and terminal continuation witness contract.

Suggested action: create an ADR for SYS-CHOICE/SYS-NARRATIVE content lock,
compiled catalogs, CFG validation, exact reaction/payoff joins, and witness
coverage.

### Partial coverage requiring downstream ADRs or implementation evidence

- `TR-NAR-001`: ADR-0003 defines the content/presentation boundary but not the
  production content-lock and full path enumeration contract.
- `TR-ACH-001`: ADR-0002 defines persistence and grant timing, but not the full
  eleven-item catalog/evaluator/backend architecture.
- `TR-JOURNAL-001`: ADR-0003 defines read-only presentation, but not the Journal
  bundle, read-model, refresh, and error taxonomy.
- `TR-ACCESS-001`: ADR-0002/0003 define storage and presentation boundaries, but
  not the complete input-equivalence and self-voicing architecture.
- `TR-TEST-001`: ADR-0007 defines the SYS-BUILD/SYS-TEST release handshake and
  isolation, but not the complete test-evidence lifecycle.

## Cross-ADR Conflict Detection

No current data-ownership, integration-contract, performance-budget,
architecture-pattern, state-authority, or dependency-cycle conflict was found.

Known conflict-prone areas from `docs/consistency-failures.md` are SYS-STATE /
SYS-NARRATIVE tuning ownership and the previously resolved ending/persistence
completion boundary. The current ADR set is synchronized on those boundaries.

### ADR dependency order

1. Foundation: ADR-0001, ADR-0002, ADR-0003.
2. Core state/ending envelope: ADR-0004, depending on ADR-0001 and ADR-0002.
3. Counterevidence and detectable initialization: ADR-0005, depending on
   ADR-0001, ADR-0002, and ADR-0004.
4. Ending completion boundary: ADR-0006, synchronized with ADR-0001, ADR-0002,
   ADR-0004, and ADR-0005.
5. Build and release identity: ADR-0007, depending on ADR-0001 through ADR-0006.

All seven ADRs are Accepted. No unresolved dependency or cycle was found.
ADR-0001, ADR-0002, ADR-0003, and ADR-0006 should expose formal dependency
sections before implementation stories are generated.

## Engine Audit Results

- Engine/version consistency: PASS. All ADRs target Ren'Py 8.5.3.
- ADRs with an Engine Compatibility section: 6 / 7. ADR-0006 has an engine
  version field but no standalone compatibility section.
- Post-cutoff APIs: ADR-0007 uses `launcher distribute` and `testcase`/`testsuite`
  only through the verified capability boundary in `BUILD.md` and
  `capability-manifest-v1.json`.
- Deprecated API check: inconclusive. `breaking-changes.md`,
  `deprecated-apis.md`, and the module reference directory are absent.
- Stale version references: none found.
- Engine specialist consultation: skipped because
  `.claude/docs/technical-preferences.md` does not define an Engine Specialists
  section.

### GDD Revision Flags

No GDD revision flags. No verified engine finding contradicts a current GDD
assumption. The missing engine references remain verification gates, not proven
design contradictions.

## Architecture Document Coverage

- All 14 systems listed in `systems-index.md` appear in the master architecture
  layer map and ownership map.
- No orphaned architecture system was found. SYS-GALLERY and SYS-AUDIO are
  represented as P1 systems that are not yet designed.
- Runtime data flows cover choice, delayed payoff, save/load/rollback,
  initialization/ending completion, and deferred tension mode.
- Documentation mismatch: `architecture.md` says it covers 11 current system
  GDDs, while the systems index links 12.
- Documentation mismatch: SYS-PERSIST, SYS-JOURNAL, and SYS-NARRATIVE retain
  `In Revision` / `Needs Revision` text inside their GDDs while the systems index
  presents them as approved with provisional downstream gates.

## Required ADRs

1. SYS-TEST test-evidence and gate lifecycle.
2. SYS-CHOICE/SYS-NARRATIVE content-lock and CFG/witness validation.
3. SYS-JOURNAL bundle/read-model/error taxonomy.
4. SYS-ACCESS input equivalence, self-voicing, settings semantics, and authority
   split.
5. SYS-TENSION preference and active-timer recovery, only when the feature
   returns from post-MVP scope.

No additional SYS-BUILD ADR is required after ADR-0007; implementation and
release evidence are still required.

## Pre-gate Checklist

| Check | Status | Action |
|---|---|---|
| `tests/unit/` | FAIL | Run `/test-setup` |
| `tests/integration/` | FAIL | Run `/test-setup` |
| `.github/workflows/tests.yml` | FAIL | Run `/test-setup` |
| `design/accessibility-requirements.md` | PASS | None |
| `design/ux/interaction-patterns.md` | PASS | None |

## Verdict

### CONCERNS

The P0 state, ending, save, persistence, and build contracts are architecturally
covered. The architecture is not yet ready for an unconditional PASS because
the choice/narrative content-lock contract is uncovered, several presentation
and test requirements are only partially covered, engine references are
incomplete, and the test infrastructure pre-gate is missing.

## Immediate Actions

1. Create the SYS-CHOICE/SYS-NARRATIVE content-lock ADR.
2. Create the SYS-TEST evidence-lifecycle ADR and run `/test-setup`.
3. Create the SYS-JOURNAL bundle/read-model ADR.

Re-run `/architecture-review` after each new ADR changes coverage.
