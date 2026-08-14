# Design Change and Impact Analysis — Formal Prose Expansion

**Date**: 2026-08-14
**Scope**: non-asset authored prose in the existing seven-day production units
**Mode**: solo; manual playtest and final narrative sign-off deferred

## Decision

The remaining length gap toward the game-concept target is handled as four
independent prose-only sprints:

1. Prologue and Day 1–2;
2. Day 3–4;
3. Day 5–6;
4. Day 7, the six endings, and the existing `rain_stops` epilogue tail.

Each sprint may add scene texture, physical action, observation, immediate
reaction, and already-frozen payoff recall inside existing labels. It may not
add or alter a choice, menu, label, jump/call topology, axis delta, token
effect, resource, qualification, ending predicate, completion event, hidden
numeric rule, canonical unit, asset reference, or player-facing system rule.

## Invariant contract

- The canonical production unit set remains exactly 15.
- Existing choice IDs, reaction IDs, payoff IDs, route qualifications, token
  IDs/effects, five axes, witness histories, resolver priority, six ending IDs,
  and completion boundaries remain byte-level test targets where applicable.
- Prose additions must remain observable and local to the scene; they cannot
  disclose hidden state or predict a route/ending.
- No new active character, asset, image, UI bitmap, music, sound effect, or
  voice work is admitted.
- Every sprint refreshes the relevant content-lock source identities and runs
  the full automated regression suite before local close-out.

## Impact matrix

| Artifact | Impact | Required action |
|---|---|---|
| Seven-day GDD | Adds prose-only expansion boundary and sprint order | Update boundary text; no mechanics change |
| Content baseline | Adds length-delivery schedule and restates frozen IDs | Update version/history; keep 15-unit catalog exact |
| Content lock | Player-visible source bytes change per sprint | Increment lock ID and refresh only affected hashes |
| ADR-0003 | Existing narrative/presentation boundary remains applicable | Recheck; keep Accepted |
| ADR-0006 | Ending completion boundary remains unchanged | Recheck; keep Accepted |
| ADR-0008 | Copy freeze and source identity rules remain applicable | Recheck; keep Accepted |
| Tests/QA | Add sprint-local structural tests and evidence | Require focused, full, Ren'Py, lint, constraints, diff check |
| Assets | No impact | Do not modify formal asset directories |

## Human boundary

Manual playtest, visual readability review, SAPI/semantic review, copyright or
source-licence review, and final narrative/正典 sign-off remain deferred. They
must be listed as NOT RUN and cannot be converted into automated PASS claims.
