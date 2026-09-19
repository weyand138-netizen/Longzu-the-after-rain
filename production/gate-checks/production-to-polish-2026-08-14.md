# Gate Check: Production → Polish

**Date**: 2026-08-14
**Checked by**: gate-check skill
**Review mode**: solo (`production/review-mode.txt`)
**Current authoritative stage**: Production (`production/stage.txt`)

## Scope and convention

This is a formal recheck after Sprint 6 Day 7 QA close-out (`2e066b3`).
The Ren'Py runtime implementation root is `game/`, not `src/`; this project
convention is established by `CLAUDE.md` and all current runtime/test evidence.
No empty `src/` directory was created to simulate compliance.

The Solo review mode skips the Director Panel. The verdict is based on artifact
and quality evidence only, and this report does not change `production/stage.txt`.

## Required Artifacts: 6/9 satisfied

| Status | Gate artifact | Evidence |
| --- | --- | --- |
| PASS | Active implementation organized into subsystems | `game/chapters/`, `game/modules/`, and `game/screens.rpy` are active; `game/` is the approved runtime root. |
| FAIL | All core mechanics implemented and main gameplay path playable end-to-end | `game/script.rpy` enters `prologue_start`, but `game/chapters/prologue.rpy` ends in `chapter_complete` then `return`; Day 1 through Day 6 labels also end in `return`. Outside `game/testcases.rpy`, no production Day 1→Day 7 handoff exists. Day 7 can enter the resolver only when separately invoked. |
| PASS | Unit and integration test suites exist | `tests/unit/` and `tests/integration/` contain substantive SYS-NARRATIVE, SYS-ENDING, save, persist, accessibility, and test-framework coverage. |
| PASS | Logic-story unit coverage exists | Core logic stories have corresponding unit modules under `tests/unit/`; the full suite passed on this revision. |
| PASS | Current smoke evidence | `production/qa/smoke-sprint-006-2026-08-14.md` is PASS; the previous Sprint 7 terminal smoke is also PASS. |
| PASS | QA plan | `production/qa/qa-plan-sprint-006-2026-08-13.md` and `qa-plan-sprint-007-2026-08-13.md` exist. |
| PASS | QA sign-off | Sprint 6 and Sprint 7 sign-offs are APPROVED, each scoped to its delivered work. |
| FAIL | Three production playtest sessions | No `production/playtests/` directory or current-production session records exist. The historic vertical-slice report is not evidence for the completed seven-day build. |
| FAIL | Fun-hypothesis validation on the current build | No production-like no-debug protocol, raw responses, coding rubric, participant records, or adjudication exists. `NARR-PLAYTEST-001` requires this external evidence. |

## Quality Checks: 4/9 passing

| Status | Check | Evidence |
| --- | --- | --- |
| PASS | Automated regression | Python `unittest` full suite: **278/278 PASS** on 2026-08-14. Pinned Ren'Py global: **56/56 testcases, 474/474 assertions PASS**. |
| PASS | Static runtime quality | Ren'Py 8.5.3 `lint --compile`, Erii content constraint scan, and `git diff --check` pass. |
| PASS | No known automated S1/S2 defect | No project bug tracker records were found; the latest Sprint 6/7 QA sign-offs record no open automated S1/S2 defect. |
| PASS | Key UX specifications and interaction patterns exist | The approved UX cross-reference covers the seven key P0 surfaces and links the shared interaction-pattern contract. |
| FAIL | Core loop plays as designed | The current player entry path returns after the prologue and cannot reach Day 1–7 or an ending in production runtime. Existing individual chapter/terminal testcases do not create a player-visible end-to-end path. |
| BLOCKED_INPUT | Performance is within committed budgets | Static profiling found one active `timer 0.05 repeat True` focus initialization check and no large runtime bitmap assets (only the 2.9 MB approved font); however there is no current-build measurement of 16.6 ms frames, startup ≤5 s, memory <1 GB, or save latency. Existing performance tests validate threshold calculations, not collected measurements. |
| BLOCKED_INPUT | Playtest findings, confusion-loop rate, and difficulty validation | These require real participants. There is no current production playtest data, and no `design/difficulty-curve.md` validation artifact. |
| BLOCKED_INPUT | P0 accessibility production evidence | `design/accessibility-requirements.md` explicitly leaves production evidence open: current-screen layout matrix, semantic-equivalence human review, SAPI transcript/listening evidence, and related adjudication are not closed. Existing spike/capture evidence must not be promoted to that claim. |
| CONCERNS | Every implemented screen has current implementation evidence | `design/ux/cross-reference.md` approves key-screen specifications, but it explicitly retains per-screen production captures and some runtime evidence as downstream work. |

## Blockers

1. **No production end-to-end route.** The seven authored units and endings are
   individually implemented and tested, but the actual player flow stops after
   the prologue. Connecting the labels would alter the frozen runtime narrative
   topology, which this gate does not authorize and the current owner direction
   forbids without an explicit decision.
2. **Required human playtesting is absent.** At least three current-production
   sessions must cover new-player experience, mid-game systems, and the
   difficulty/causality curve. The frozen narrative contract additionally
   requires a no-debug protocol, raw participant responses, rubric, and human
   adjudication; automation cannot manufacture this evidence.
3. **Accessibility Production evidence is incomplete.** The frozen P0 tier
   itself marks the pending SAPI/transcript, human semantic-equivalence, and
   current-surface evidence as blocking inputs rather than PASS.
4. **No measured performance benchmark.** Current automated checks prove the
   reporting protocol only, not the committed runtime budgets on target
   hardware.

## Static Performance Profile

| Metric | Committed budget | Current evidence | Result |
| --- | --- | --- | --- |
| Interactive frame time | 16.6 ms / 60 fps | No target-hardware frame-time samples. `focus_graph_bindings` polls initial focus every 50 ms and should be included in measurement. | BLOCKED_INPUT |
| Startup | main menu ≤5 s | No timing samples. | BLOCKED_INPUT |
| Normal save | ≤500 ms | Only threshold-calculation tests; no engine I/O samples. | BLOCKED_INPUT |
| Base memory | <1 GB | No process memory samples. Runtime asset directory currently contains only the 2,901,056-byte font, but this is not a memory measurement. | BLOCKED_INPUT |

No optimization is proposed or applied: runtime profiling must precede any
performance change.

## Chain-of-Verification

Five challenge questions were checked. The verdict is **revised from the
2026-08-11 FAIL evidence**, because the former missing Day 4–Day 7/ending
implementation and Python-test failure are now resolved; it remains FAIL for
the independent blockers below.

1. **[TOOL ACTION] Do the automated suites actually pass on the close-out
   revision?** Re-ran Python full: 278/278 PASS; re-ran pinned Ren'Py global:
   56/56 testcases and 474/474 assertions PASS.
2. **[TOOL ACTION] Is there a true player-facing sequence rather than only
   independently invokable labels?** Re-read `game/script.rpy` and each chapter
   ending, then scanned non-test `jump/call` statements. The prologue and Days
   1–6 return without a next-day handoff.
3. **[TOOL ACTION] Were the required current-build playtests perhaps recorded
   elsewhere?** Re-scanned `production/` for playtest/protocol/rubric artifacts.
   Only story specifications were found; no production sessions exist.
4. **[TOOL ACTION] Did the accessibility contract itself claim this evidence
   is closed?** Re-read the P0 Production Gate and current-open-items sections
   of `design/accessibility-requirements.md`; they explicitly retain the cited
   human/current-build evidence as unclosed.
5. **Could static performance tests be treated as benchmark evidence?** No.
   The current tests pass synthetic input tuples to pure threshold functions;
   none captures frame, startup, memory, or engine save measurements.

## Verdict: FAIL

Production may not advance to Polish. `production/stage.txt` remains
**Production**. The next required input is an owner-approved change decision
for the frozen end-to-end topology, followed by real playtesting and the
remaining human accessibility evidence; performance must be measured rather
than inferred.
