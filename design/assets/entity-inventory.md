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
| `runtime_ui_day1_choice_surface` | Code-defined UI primitives | Dialogue window and two-option critical-choice surface | Ren'Py `say` and `choice` screens in `game/screens.rpy`; `Solid()` backgrounds, no image file | **Present; admitted as project code** | `RUNTIME-UI-DAY1-CHOICE-SURFACE`; source-file SHA-256 `72d963e5c0df442dec889d1024f82a8951af573575ad5ebd84a8c0e5a7e5a291` | `a11y.day1.choice-surface`: stable IDs `day1_choice_0`/`day1_choice_1`, first keyboard focus, captions as accessible text, distinct high-contrast focus treatment, and no quick-menu focus during critical choices. Verified at 1280x720, silent, reduced motion, and 1.5x/high-contrast baselines. |

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

**Date**: 2026-08-11<br>
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
| `runtime_ui_day1_choice_surface` | Day 3 evidence and truth-pace choices | Ren'Py `say` and `choice` screens in `game/screens.rpy`; `Solid()`/textbutton primitives, no image file | `RUNTIME-UI-DAY1-CHOICE-SURFACE`; source-file SHA-256 `72d963e5c0df442dec889d1024f82a8951af573575ad5ebd84a8c0e5a7e5a291` | `a11y.day3.choice-surface`: captions carry the choice meaning; keyboard focus and high-contrast treatment must be verified by Story 007, with no quick-menu focus during critical input. | **Present; admitted reuse pending Story 007 presentation verification.** |

No Day 3 image, audio, video, character art, CG, prop, generated, or planned
file is present or admitted. The papers, red-clay trace, and archive in Day 3
are narrative text/semantic facts, not asset-file claims.

## Day 4 audit result

**Date**: 2026-08-11<br>
**Scope**: Sprint 3 / S3-03 actual runtime references in
`game/chapters/day4.rpy`, `game/00_resources.rpy`, `game/screens.rpy`, and
`game/assets/`.

Day 4 introduces no binary, external, generated, image, audio, video,
character-art, CG, or prop asset. Its direct scene reference is `bg warm_room`;
dialogue and the two possible critical choice surfaces reuse the admitted font
and code-defined screens. Tickets, route map, contact card, game coin, and sea
window are narrative text and semantic facts, not asset-file claims.

| Existing asset ID | Day 4 production role | Verified runtime path | Source / SHA-256 | Day 4 accessibility semantic binding | Admission status |
|---|---|---|---|---|---|
| `font_source_han_sans_lite` | All Day 4 dialogue and ticket/route/contact choice captions | `game/assets/fonts/SourceHanSansLite.ttf`, loaded by `game/screens.rpy` as `assets/fonts/SourceHanSansLite.ttf` | `FONT-SOURCEHAN-LITE-P0`; `b2aaf73b7acc23d746b110f1caeaecc93d4292824979af44e96000200591b2a7` | `a11y.day4.text-and-choice-copy`: ticket, route, independent-contact, and consequence facts are visible/localizable text; no decision depends on a visual asset. | **Present; admitted reuse.** |
| `runtime_solid_day1_warm_room` | Decorative backing for `chapter_day4_seaside_train` | Ren'Py image `bg warm_room` from `game/00_resources.rpy` (`Solid("#4a3840")`); no file path | `RUNTIME-SOLID-DAY1-WARM-ROOM`; source-file SHA-256 `4333d936fbe481f61c4cb828e43e17057133ae5af99b79cdf76e76545ee49801` | `a11y.day4.warm-room-decorative`: the background supplies no ticket, identity-cost, route, contact, or progress fact; all such facts remain text and keyboard accessible. | **Present; admitted reuse.** |
| `runtime_ui_day1_choice_surface` | Day 4 route-preparation and conditional independent-contact choices | Ren'Py `say` and `choice` screens in `game/screens.rpy`; `Solid()`/textbutton primitives, no image file | `RUNTIME-UI-DAY1-CHOICE-SURFACE`; source-file SHA-256 `72d963e5c0df442dec889d1024f82a8951af573575ad5ebd84a8c0e5a7e5a291` | `a11y.day4.choice-surface`: captions are semantic and keyboard-operable; high-contrast focus must remain distinct and critical input must expose no quick-menu target. | **Present; admitted reuse.** Story 010 presentation verification passed on 2026-08-11. |

No Day 4 image, audio, video, character art, CG, prop, generated, or planned
file is present or admitted. Intended background and prop files listed below
remain not admitted and must not be treated as Day 4 runtime references.

## Day 5 audit result

**Date**: 2026-08-13
**Scope**: Sprint 4 / S4-02 actual runtime references in
`game/chapters/day5.rpy`, `game/00_resources.rpy`, `game/screens.rpy`, and
`game/assets/`.

Day 5 introduces no binary, external, generated, image, audio, video,
character-art, CG, or prop asset. Its direct scene reference is `bg warm_room`;
the family archive, source pages, route map, tickets, contact card, and document
case are narrative text and semantic facts, not asset-file claims. Dialogue and
all Day 5 choice surfaces reuse the admitted font and code-defined screens.

| Existing asset ID | Day 5 production role | Verified runtime path | Source / SHA-256 | Day 5 accessibility semantic binding | Admission status |
|---|---|---|---|---|---|
| `font_source_han_sans_lite` | All Day 5 archive, liability, response, and repair captions | `game/assets/fonts/SourceHanSansLite.ttf`, loaded by `game/screens.rpy` as `assets/fonts/SourceHanSansLite.ttf` | `FONT-SOURCEHAN-LITE-P0`; `b2aaf73b7acc23d746b110f1caeaecc93d4292824979af44e96000200591b2a7` | `a11y.day5.text-and-choice-copy`: archive facts, route-answer actions, response, liability, and repair meanings are visible/localizable text; no decision depends on a visual asset. | **Present; admitted reuse.** |
| `runtime_solid_day1_warm_room` | Decorative backing for `chapter_day5_family_lie` | Ren'Py image `bg warm_room` from `game/00_resources.rpy` (`Solid("#4a3840")`); no file path | `RUNTIME-SOLID-DAY1-WARM-ROOM`; source-file SHA-256 `4333d936fbe481f61c4cb828e43e17057133ae5af99b79cdf76e76545ee49801` | `a11y.day5.warm-room-decorative`: background colour carries no archive, route, answer, resource, or consequence fact; those remain text and keyboard accessible. | **Present; admitted reuse.** |
| `runtime_ui_day1_choice_surface` | Day 5 truth, response, liability, and conditional repair choices | Ren'Py `say` and `choice` screens in `game/screens.rpy`; `Solid()`/textbutton primitives, no image file | `RUNTIME-UI-DAY1-CHOICE-SURFACE`; source-file SHA-256 `72d963e5c0df442dec889d1024f82a8951af573575ad5ebd84a8c0e5a7e5a291` | `a11y.day5.choice-surface`: captions are semantic and keyboard-operable; high-contrast focus must remain distinct and critical input must expose no quick-menu target. | **Present; admitted reuse pending Story 014 presentation verification.** |

No Day 5 image, audio, video, character art, CG, prop, generated, or planned
file is present or admitted. Intended background and prop files listed below
remain not admitted and must not be treated as Day 5 runtime references.

## Day 6 audit result

**Date**: 2026-08-13
**Scope**: Sprint 5 / S5-02 actual runtime references in
`game/chapters/day6.rpy`, `game/00_resources.rpy`, `game/screens.rpy`, and
`game/assets/`.

Day 6 introduces no binary, external, generated, image, audio, video,
character-art, CG, or prop asset. Its direct scene reference is `bg warm_room`;
the safehouse, service exit, route map, tickets, contact card, archive, and old
identity documents are narrative text and semantic facts, not asset-file claims.
Dialogue and all Day 6 choice surfaces reuse the admitted font and code-defined
screens.

| Existing asset ID | Day 6 production role | Verified runtime path | Source / SHA-256 | Day 6 accessibility semantic binding | Admission status |
|---|---|---|---|---|---|
| `font_source_han_sans_lite` | All Day 6 safehouse, repair, cost, and commitment captions | `game/assets/fonts/SourceHanSansLite.ttf`, loaded by `game/screens.rpy` as `assets/fonts/SourceHanSansLite.ttf` | `FONT-SOURCEHAN-LITE-P0`; `b2aaf73b7acc23d746b110f1caeaecc93d4292824979af44e96000200591b2a7` | `a11y.day6.text-and-choice-copy`: service-exit, truth, cost, consequence, and commitment facts are visible/localizable text; no decision depends on a visual asset. | **Present; admitted reuse.** |
| `runtime_solid_day1_warm_room` | Decorative backing for `chapter_day6_no_safe_house` | Ren'Py image `bg warm_room` from `game/00_resources.rpy` (`Solid("#4a3840")`); no file path | `RUNTIME-SOLID-DAY1-WARM-ROOM`; source-file SHA-256 `4333d936fbe481f61c4cb828e43e17057133ae5af99b79cdf76e76545ee49801` | `a11y.day6.warm-room-decorative`: background supplies no safehouse, resource, consequence, or route fact; all such facts remain text and keyboard accessible. | **Present; admitted reuse.** |
| `runtime_ui_day1_choice_surface` | Day 6 backup, truth, cost, reconsideration, and commitment choices | Ren'Py `say` and `choice` screens in `game/screens.rpy`; `Solid()`/textbutton primitives, no image file | `RUNTIME-UI-DAY1-CHOICE-SURFACE`; source-file SHA-256 `72d963e5c0df442dec889d1024f82a8951af573575ad5ebd84a8c0e5a7e5a291` | `a11y.day6.choice-surface`: captions are semantic and keyboard-operable; high-contrast focus must remain distinct and critical input must expose no quick-menu target. | **Present; admitted reuse pending Story 018 presentation verification.** |

No Day 6 image, audio, video, character art, CG, prop, generated, or planned
file is present or admitted. Intended background and prop files listed below
remain not admitted and must not be treated as Day 6 runtime references.

## Day 7 audit result

**Date**: 2026-08-14
**Scope**: Sprint 6 / S6-02 actual runtime references in
`game/chapters/day7.rpy`, `game/00_resources.rpy`, `game/screens.rpy`, and
`game/assets/`.

Day 7 introduces no binary, external, generated, image, audio, video,
character-art, CG, or prop asset. Its only direct scene reference is
`bg warm_room`; the red well, wind, water, paper, visible routes, and names are
narrative text and semantic facts, not asset-file claims. The dialogue is
rendered through the existing `say` screen and admitted font; Day 7 has no
choice surface at all.

| Existing asset ID | Day 7 production role | Verified runtime path | Source / SHA-256 | Day 7 accessibility semantic binding | Admission status |
|---|---|---|---|---|---|
| `font_source_han_sans_lite` | All Day 7 acknowledgement and handoff dialogue text | `game/assets/fonts/SourceHanSansLite.ttf`, loaded by `game/screens.rpy` as `assets/fonts/SourceHanSansLite.ttf` | `FONT-SOURCEHAN-LITE-P0`; `b2aaf73b7acc23d746b110f1caeaecc93d4292824979af44e96000200591b2a7` | `a11y.day7.text-copy`: Day 1-6 acknowledgement and the resolver handoff are visible/localizable text; no semantic outcome depends on a visual asset. | **Present; admitted reuse.** |
| `runtime_solid_day1_warm_room` | Decorative backing for `chapter_day7_before_red_well` | Ren'Py image `bg warm_room` from `game/00_resources.rpy` (`Solid("#4a3840")`); no file path | `RUNTIME-SOLID-DAY1-WARM-ROOM`; source-file SHA-256 `4333d936fbe481f61c4cb828e43e17057133ae5af99b79cdf76e76545ee49801` | `a11y.day7.warm-room-decorative`: background colour establishes no Day 1-6 fact, terminal input, or ending result; those remain text and the owned resolver boundary. | **Present; admitted reuse.** |
| `runtime_ui_day1_choice_surface` | Existing `say` dialogue screen used by the Day 7 text-only unit; no Day 7 `choice` surface is invoked | Ren'Py `say` screen in `game/screens.rpy`; `Solid()`/text primitives, no image file | `RUNTIME-UI-DAY1-CHOICE-SURFACE`; source-file SHA-256 `72d963e5c0df442dec889d1024f82a8951af573575ad5ebd84a8c0e5a7e5a291` | `a11y.day7.say-surface`: text remains readable, keyboard-advanceable, and semantically complete at the approved accessibility baselines; no quick-menu target or visual-only input decides the handoff. | **Present; admitted reuse.** |

No Day 7 image, audio, video, character art, CG, prop, generated, planned, or
choice-only identity is present or admitted. Intended files listed below remain
not admitted and must not be treated as Day 7 runtime references.

## Admission checklist

1. Confirm the asset strengthens an observable fact or a concrete everyday-life contrast.
2. Record source, licence/non-commercial basis, original filename or code origin, SHA-256, owner, and verified runtime path in the legal register.
3. Bind any player-relevant asset to an approved semantic/alt-text record; colour, hover, sound, motion, or art alone must never be its only meaning.
4. Verify 1920x1080 and the 1280x720, 1.5x-font, high-contrast, silent, reduced-motion baseline before lock.

## Evidence

- Runtime-reference source: `game/chapters/day1.rpy` uses only `bg warm_room`; `game/screens.rpy` supplies the Day 1 dialogue/choice surface and font reference.
- Filesystem audit: the only file in `game/assets/` is `fonts/SourceHanSansLite.ttf`; no image, audio, video, character, or prop file exists there.
- Accessibility evidence: `production/qa/evidence/day1-content-validation-evidence.md` records passing Day 1 keyboard, silent, reduced-motion, 1.5x-font, and high-contrast captures.
