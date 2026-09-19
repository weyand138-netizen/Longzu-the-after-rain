# Day 7 Asset Admission Evidence

**Date**: 2026-08-14
**Story**: S6-02 / Story 021
**Source audited**: `game/chapters/day7.rpy`

## Actual-reference audit

| Runtime reference | Admitted identity | Provenance and SHA-256 | Semantic/accessibility binding |
|---|---|---|---|
| Day 7 dialogue through `say` | `FONT-SOURCEHAN-LITE-P0` | Local `game/assets/fonts/SourceHanSansLite.ttf`; OFL 1.1 record and SHA-256 `b2aaf73b7acc23d746b110f1caeaecc93d4292824979af44e96000200591b2a7` | `a11y.day7.text-copy`: all acknowledgement and handoff meaning is readable/localizable text. |
| `scene bg warm_room` | `RUNTIME-SOLID-DAY1-WARM-ROOM` | Project-authored `game/00_resources.rpy`; SHA-256 `4333d936fbe481f61c4cb828e43e17057133ae5af99b79cdf76e76545ee49801` | `a11y.day7.warm-room-decorative`: colour conveys no history, terminal input, or ending result. |
| Existing `say` dialogue screen | `RUNTIME-UI-DAY1-CHOICE-SURFACE` | Project-authored `game/screens.rpy`; SHA-256 `72d963e5c0df442dec889d1024f82a8951af573575ad5ebd84a8c0e5a7e5a291` | `a11y.day7.say-surface`: text is keyboard-advanceable and semantically complete; no visual-only interaction decides the handoff. |

The source has exactly one direct presentation statement, `scene bg warm_room`.
No Day 7 image, audio, video, character art, CG, prop, generated, planned, or
external identity is present or admitted; it also has no Day 7 `choice` surface,
music, logo, or planned/absent identity.
The red well and all described objects are narrative text, not a claim that an
asset exists. Inventory and legal register records were updated together.

## Verdict: ADMITTED REUSE ONLY

No new asset was created, copied, downloaded, or introduced. This evidence does
not claim S6-03 accessibility capture review, ending presentation admission,
release licensing, or a stage change. The Ren'Py runtime root remains `game/`;
no empty `src/` directory is used for gate compliance.
