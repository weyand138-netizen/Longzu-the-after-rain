# P0 Entity and Asset Inventory

**Date**: 2026-08-10  
**Scope**: Sprint 1 / S1-04 Day 1 runtime-asset admission audit for *Rain After*  
**Authority**: Art Bible, accessibility requirements, Day 1 source, and [asset register](../../docs/legal/asset-register.md).

## Day 1 audit result

The audit searched `game/chapters/day1.rpy`, `game/screens.rpy`,
`game/00_resources.rpy`, and the shipped `game/assets/` tree. Day 1 has **one
binary runtime asset** and **two code-defined Ren'Py presentation assets**. It
does not reference external images, audio, video, character art, CGs, or prop
files. The three background PNG paths formerly described as existing are not
present under `game/assets/` and are not Day 1 runtime references; they remain
planned only.

`Present` below means the identified runtime artifact exists and is admitted;
it never means that an intended path is merely named in a design document.
`N/A — no standalone file` is valid only for a code-defined Ren'Py primitive;
the hash then identifies its owning source file in the legal register.

| ID | Kind | Day 1 production role | Verified runtime path | Admission status | Source / SHA-256 | Accessibility semantic binding |
|---|---|---|---|---|---|---|
| `font_source_han_sans_lite` | Font | Simplified-Chinese body, dialogue, and choice text | `game/assets/fonts/SourceHanSansLite.ttf`, loaded as `assets/fonts/SourceHanSansLite.ttf` | **Present; admitted** | `FONT-SOURCEHAN-LITE-P0`; `b2aaf73b7acc23d746b110f1caeaecc93d4292824979af44e96000200591b2a7` | `a11y.day1.text-and-choice-copy`: all Day 1 dialogue and choice captions remain readable at 1.0/1.25/1.5 scale; text is the decision-bearing channel. |
| `runtime_solid_day1_warm_room` | Code-defined background | Non-decision decorative scene backing for the Day 1 room | Ren'Py image `bg warm_room` from `game/00_resources.rpy` (`Solid("#4a3840")`); no file path | **Present; admitted as project code** | `RUNTIME-SOLID-DAY1-WARM-ROOM`; source-file SHA-256 `4333d936fbe481f61c4cb828e43e17057133ae5af99b79cdf76e76545ee49801` | `a11y.day1.warm-room-decorative`: decorative only. Clothing, food, receipt-name, choices, reactions, and progress are supplied by visible/localizable text and keyboard-operable controls, never by this colour field. |
| `runtime_ui_day1_choice_surface` | Code-defined UI primitives | Dialogue window and two-option critical-choice surface | Ren'Py `say` and `choice` screens in `game/screens.rpy`; `Solid()` backgrounds, no image file | **Present; admitted as project code** | `RUNTIME-UI-DAY1-CHOICE-SURFACE`; source-file SHA-256 `019041a6ae96cb28e88a45547e385b014217e3c612a1bb2215ec0dc77835757c` | `a11y.day1.choice-surface`: stable IDs `day1_choice_0`/`day1_choice_1`, first keyboard focus, captions as accessible text, distinct high-contrast focus treatment, and no quick-menu focus during critical choices. Verified at 1280x720, silent, reduced motion, and 1.5x/high-contrast baselines. |

## Planned or not-admitted inventory

| ID | Kind | Intended runtime path | Status (not an existence claim) | Admission requirement / semantic binding |
|---|---|---|---|---|
| `char_erii_p0` | Character direction | `game/assets/characters/erii/` | Direction approved; **no artwork file present or admitted** | Before use: source, permission, binary SHA-256, and `a11y` action/object description that does not substitute an unapproved inner monologue. |
| `char_lu_mingfei_p0` | Character direction | `game/assets/characters/lu_mingfei/` | Direction approved; **no artwork file present or admitted** | Before use: source, permission, binary SHA-256, and text/voicing-equivalent player-facing semantics. |
| `bg_station_platform_rain` | Background | `game/assets/backgrounds/bg_station_platform_rain.png` | **Not present in `game/assets/`; not admitted; not a Day 1 reference** | Source, licence, binary SHA-256, and decorative/non-decision semantic record before admission. |
| `bg_ticket_gate` | Background | `game/assets/backgrounds/bg_ticket_gate.png` | **Not present in `game/assets/`; not admitted; not a Day 1 reference** | Source, licence, binary SHA-256, and decorative/non-decision semantic record before admission. |
| `bg_train_window` | Background | `game/assets/backgrounds/bg_train_window.png` | **Not present in `game/assets/`; not admitted; not a Day 1 reference** | Source, licence, binary SHA-256, and decorative/non-decision semantic record before admission. |
| `prop_wish_paper` | Prop | `game/assets/props/prop_wish_paper.png` | Needed later; **no file present or admitted** | Source, licence, binary SHA-256, and an approved descriptive/causal summary binding before use. |
| `prop_receipt_name` | Prop | `game/assets/props/prop_receipt_name.png` | Planned Day 1 prop; **no file present or admitted** | Source, licence, binary SHA-256, player-safe copy review, and receipt-name semantic summary before a visible prop replaces the current textual anchor. |
| `ui_focus_frame` | UI primitive | Ren'Py primitive or `game/assets/ui/ui_focus_frame.png` | No separate file exists or is admitted; current Day 1 focus is the code-defined choice surface above | A separate file requires source, licence, binary SHA-256, and a non-colour-only focus binding; it must not imply a correct answer. |

## Day 3 audit result

**Date**: 2026-08-11  
**Scope**: Sprint 2 / S2-02 actual runtime references in
`game/chapters/day3.rpy`, `game/00_resources.rpy`, `game/screens.rpy`, and
`game/assets/`.

Day 3 introduces no new binary or external asset. Its only direct scene
reference is `bg warm_room`; dialogue and the two choice surfaces reuse the
existing font and code-defined screens. The three records below are the same
already-admitted runtime artifacts, now explicitly admitted for their Day 3
reuse; they are not duplicate assets.

| Existing asset ID | Day 3 production role | Verified runtime path | Source / SHA-256 | Day 3 accessibility semantic binding | Admission status |
|---|---|---|---|---|---|
| `font_source_han_sans_lite` | All Day 3 dialogue and evidence/pause choice captions | `game/assets/fonts/SourceHanSansLite.ttf`, loaded by `game/screens.rpy` as `assets/fonts/SourceHanSansLite.ttf` | `FONT-SOURCEHAN-LITE-P0`; `b2aaf73b7acc23d746b110f1caeaecc93d4292824979af44e96000200591b2a7` | `a11y.day3.text-and-choice-copy`: the trace, evidence choice, and pause answer are visible/localizable text; no decision meaning depends on a visual asset. | **Present; admitted reuse.** |
| `runtime_solid_day1_warm_room` | Decorative backing for `chapter_day3_empty_school` | Ren'Py image `bg warm_room` from `game/00_resources.rpy` (`Solid("#4a3840")`); no file path | `RUNTIME-SOLID-DAY1-WARM-ROOM`; source-file SHA-256 `4333d936fbe481f61c4cb828e43e17057133ae5af99b79cdf76e76545ee49801` | `a11y.day3.warm-room-decorative`: the background does not establish the classroom trace, choices, reactions, or progress; those facts remain text and keyboard accessible. | **Present; admitted reuse.** |
| `runtime_ui_day1_choice_surface` | Day 3 evidence and truth-pace choices | Ren'Py `say` and `choice` screens in `game/screens.rpy`; `Solid()`/textbutton primitives, no image file | `RUNTIME-UI-DAY1-CHOICE-SURFACE`; source-file SHA-256 `019041a6ae96cb28e88a45547e385b014217e3c612a1bb2215ec0dc77835757c` | `a11y.day3.choice-surface`: captions carry the choice meaning; keyboard focus and high-contrast treatment must be verified by Story 007, with no quick-menu focus during critical input. | **Present; admitted reuse pending Story 007 presentation verification.** |

No Day 3 image, audio, video, character art, CG, prop, generated, or planned
file is present or admitted. The papers, red-clay trace, and archive in Day 3
are narrative text/semantic facts, not asset-file claims.

## Admission checklist

1. Confirm the asset strengthens an observable fact or a concrete everyday-life contrast.
2. Record source, licence/non-commercial basis, original filename or code origin, SHA-256, owner, and verified runtime path in the legal register.
3. Bind any player-relevant asset to an approved semantic/alt-text record; colour, hover, sound, motion, or art alone must never be its only meaning.
4. Verify 1920x1080 and the 1280x720, 1.5x-font, high-contrast, silent, reduced-motion baseline before lock.

## Evidence

- Runtime-reference source: `game/chapters/day1.rpy` uses only `bg warm_room`; `game/screens.rpy` supplies the Day 1 dialogue/choice surface and font reference.
- Filesystem audit: the only file in `game/assets/` is `fonts/SourceHanSansLite.ttf`; no image, audio, video, character, or prop file exists there.
- Accessibility evidence: `production/qa/evidence/day1-content-validation-evidence.md` records passing Day 1 keyboard, silent, reduced-motion, 1.5x-font, and high-contrast captures.
