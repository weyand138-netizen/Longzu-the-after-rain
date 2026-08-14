# Day 3 Asset Admission Consistency Check

**Story**: S2-02 — Day 3 asset admission records  
**Recorded**: 2026-08-11  
**Verdict**: **PASS — source/data admission scope**

## Scope

Audited actual runtime references in `game/chapters/day3.rpy`,
`game/00_resources.rpy`, `game/screens.rpy`, and `game/assets/`; cross-checked
them against `design/assets/entity-inventory.md` and
`docs/legal/asset-register.md`.

## Results

| Check | Result |
|---|---|
| Actual Day 3 scene reference | `bg warm_room` only; it is the already-admitted code-defined `Solid("#4a3840")` primitive in `game/00_resources.rpy`. |
| Actual file assets | `game/assets/fonts/SourceHanSansLite.ttf` only; SHA-256 `b2aaf73b7acc23d746b110f1caeaecc93d4292824979af44e96000200591b2a7`. |
| Code-defined hashes | `game/00_resources.rpy`: `4333d936fbe481f61c4cb828e43e17057133ae5af99b79cdf76e76545ee49801`; `game/screens.rpy`: `019041a6ae96cb28e88a45547e385b014217e3c612a1bb2215ec0dc77835757c`. Both match the inventory and legal register. |
| Day 3 source binding | `game/chapters/day3.rpy` SHA-256 `6bd6d5ed98983bf28027d96d5e61905a67053b2511ff9ca0a2d68cdedfddfb16`; it contains no binary asset path, image/audio/video command, or external media reference. |
| Legal/admission join | The inventory and legal register agree on `FONT-SOURCEHAN-LITE-P0`, `RUNTIME-SOLID-DAY1-WARM-ROOM`, and `RUNTIME-UI-DAY1-CHOICE-SURFACE` for Day 3 reuse, including provenance, licence, SHA-256, stable path, and `a11y.day3.text-and-choice-copy`, `a11y.day3.warm-room-decorative`, and `a11y.day3.choice-surface` semantic bindings. |
| Non-admission | No Day 3 image, audio, video, character art, CG, prop, generated, planned, or unregistered runtime asset is present or admitted. |

## Accessibility conclusion

The background is decorative. The empty-school trace, evidence-sharing choice,
and pause response are all visible/localizable text and keyboard-operable
choices. Story 007 remains responsible for the engine route and visual
baseline confirmation of focus, clipping, quick-menu exclusion, high contrast,
silent output, and reduced motion.
