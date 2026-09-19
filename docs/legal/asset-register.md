# Asset and License Register

**Last audited**: 2026-08-14
**Audit scope**: Day 1, Day 3, Day 4, Day 5, Day 6, and Day 7 actual runtime references only.

This register records provenance and the exact hash used for admission. It
does not claim a final legal authorization beyond the stated source and licence
terms. `Present` applies only to an artifact verified in the current runtime
tree. Code-defined Ren'Py primitives have no standalone binary; their SHA-256
therefore identifies the source file that defines the admitted primitive.

| Asset ID | Verified runtime path | File / source and SHA-256 | Creator / source | Licence / permission | AI assisted | Accessibility semantic binding | Review status |
|---|---|---|---|---|---|---|---|
| `FONT-SOURCEHAN-LITE-P0` | `game/assets/fonts/SourceHanSansLite.ttf` (referenced at runtime as `assets/fonts/SourceHanSansLite.ttf`) | Runtime file `game/assets/fonts/SourceHanSansLite.ttf`; SHA-256 `b2aaf73b7acc23d746b110f1caeaecc93d4292824979af44e96000200591b2a7`. Licence text: `docs/legal/fonts/SourceHanSansLite-OFL-1.1.txt`. | Ren'Py 8.5.3 SDK `sdk-fonts/SourceHanSansLite.ttf`; upstream family Adobe Source Han Sans | SIL Open Font License 1.1; reserved font name `Source`; bundled licence text retained | No | `a11y.day1.text-and-choice-copy`: readable dialogue/choice text is the decision-bearing, localizable semantic channel at all approved font scales. | **Present; admitted.** Source path, local hash, and bundled OFL text verified; release archive must retain this hash. |
| `RUNTIME-SOLID-DAY1-WARM-ROOM` | Ren'Py image `bg warm_room` defined in `game/00_resources.rpy`; no standalone asset file | Project-authored source `game/00_resources.rpy`, `image bg warm_room = Solid("#4a3840")`; source SHA-256 `4333d936fbe481f61c4cb828e43e17057133ae5af99b79cdf76e76545ee49801` | Project code | Project-owned code; no third-party media incorporated | No | `a11y.day1.warm-room-decorative`: no causal or choice meaning is conveyed by the colour/background alone; the equivalent facts are visible/localizable text and keyboard-operable controls. | **Present; admitted as code-defined primitive.** |
| `RUNTIME-UI-DAY1-CHOICE-SURFACE` | Ren'Py `say` and `choice` screens in `game/screens.rpy`; `Solid()`/textbutton primitives, no standalone asset file | Project-authored source `game/screens.rpy`; source SHA-256 `72d963e5c0df442dec889d1024f82a8951af573575ad5ebd84a8c0e5a7e5a291` | Project code | Project-owned code; no third-party media incorporated | No | `a11y.day1.choice-surface`: `day1_choice_0`/`day1_choice_1` provide stable focus and caption semantics; high contrast adds a white/black focus state; quick-menu controls are absent during critical choices. | **Present; admitted as code-defined primitive.** Day 6 extends the same focus treatment to its choice surfaces; all global baselines are rerun before Sprint 5 hand-off. |

## Day 3 runtime reuse admission

Day 3 adds no new asset identity. The following existing records are admitted
for the actual references in `game/chapters/day3.rpy`; their source, licence,
hash, and stable path remain exactly the records above.

| Asset ID | Day 3 runtime use | Day 3 accessibility binding | Review status |
|---|---|---|---|
| `FONT-SOURCEHAN-LITE-P0` | Day 3 dialogue and evidence/pause choice captions | `a11y.day3.text-and-choice-copy`: text is the localizable decision-bearing channel. | **Present; admitted reuse.** |
| `RUNTIME-SOLID-DAY1-WARM-ROOM` | `scene bg warm_room` at `chapter_day3_empty_school` entry | `a11y.day3.warm-room-decorative`: no trace, choice, reaction, or progress fact is carried by background colour alone. | **Present; admitted reuse.** |
| `RUNTIME-UI-DAY1-CHOICE-SURFACE` | Day 3 `say` and two `choice` surfaces | `a11y.day3.choice-surface`: captions are semantic, keyboard-operable text; Story 007 verifies focus and high-contrast presentation. | **Present; admitted reuse pending Story 007 presentation verification.** |

No Day 3 image, audio, video, character art, CG, prop, generated, or planned
asset file has a runtime reference. Those asset categories remain not admitted.

## Day 4 runtime reuse admission

Day 4 adds no new asset identity. The following existing records are admitted
for the actual references in `game/chapters/day4.rpy`; their source, licence,
hash, and stable path remain exactly the records above.

| Asset ID | Day 4 runtime use | Day 4 accessibility binding | Review status |
|---|---|---|---|
| `FONT-SOURCEHAN-LITE-P0` | Day 4 dialogue and route/contact choice captions | `a11y.day4.text-and-choice-copy`: ticket, contact, and consequence facts are localizable decision-bearing text. | **Present; admitted reuse.** |
| `RUNTIME-SOLID-DAY1-WARM-ROOM` | `scene bg warm_room` at `chapter_day4_seaside_train` entry | `a11y.day4.warm-room-decorative`: colour/background alone establishes no route, ticket, identity-cost, or contact fact. | **Present; admitted reuse.** |
| `RUNTIME-UI-DAY1-CHOICE-SURFACE` | Day 4 route-preparation and conditional independent-contact `say`/`choice` surfaces | `a11y.day4.choice-surface`: captions remain semantic and keyboard-operable; Story 010 verifies focus, high contrast, and absence of a quick-menu focus target. | **Present; admitted reuse.** Story 010 presentation verification passed on 2026-08-11. |

No Day 4 image, audio, video, character art, CG, prop, generated, or planned
asset file has a runtime reference. Those asset categories remain not admitted.

## Day 5 runtime reuse admission

Day 5 adds no new asset identity. The following existing records are admitted
for actual references in `game/chapters/day5.rpy`; their source, licence, hash,
and stable path remain exactly the records above. The family archive, route map,
tickets, contact card, document case, and source pages are narrative text and
semantic facts, not asset-file claims.

| Asset ID | Day 5 runtime use | Day 5 accessibility binding | Review status |
|---|---|---|---|
| `FONT-SOURCEHAN-LITE-P0` | Day 5 archive, liability, response, and repair dialogue/choice captions | `a11y.day5.text-and-choice-copy`: text carries archive, route-answer, response, and consequence facts. | **Present; admitted reuse.** |
| `RUNTIME-SOLID-DAY1-WARM-ROOM` | `scene bg warm_room` at `chapter_day5_family_lie` entry | `a11y.day5.warm-room-decorative`: colour/background alone establishes no Day 5 fact. | **Present; admitted reuse.** |
| `RUNTIME-UI-DAY1-CHOICE-SURFACE` | Day 5 `say` and truth/response/liability/repair `choice` surfaces | `a11y.day5.choice-surface`: captions remain semantic and keyboard-operable; Story 014 verifies focus, high contrast, and absence of a quick-menu focus target. | **Present; admitted reuse pending Story 014 presentation verification.** |

No Day 5 image, audio, video, character art, CG, prop, generated, or planned
asset file has a runtime reference. Those asset categories remain not admitted.

## Day 6 runtime reuse admission

Day 6 adds no asset identity. The safehouse, service exit, route map, tickets,
contact card, archive, and identity documents are visible narrative facts in
text, not asset-file claims. Only the existing font, code-defined warm-room
background, and code-defined choice surface are admitted for actual references
in `game/chapters/day6.rpy`.

| Asset ID | Day 6 runtime use | Day 6 accessibility binding | Review status |
|---|---|---|---|
| `FONT-SOURCEHAN-LITE-P0` | Day 6 safehouse, repair, cost, and commitment dialogue/choice captions | `a11y.day6.text-and-choice-copy`: all service-exit, truth, cost, and route facts remain visible/localizable text. | **Present; admitted reuse.** |
| `RUNTIME-SOLID-DAY1-WARM-ROOM` | `scene bg warm_room` at `chapter_day6_no_safe_house` entry | `a11y.day6.warm-room-decorative`: background colour establishes no Day 6 resource, cost, consequence, or route fact. | **Present; admitted reuse.** |
| `RUNTIME-UI-DAY1-CHOICE-SURFACE` | Day 6 backup/truth/cost/reconsideration/commitment choice surfaces | `a11y.day6.choice-surface`: captions remain semantic and keyboard-operable; Story 018 verifies focus, high contrast, and absence of a quick-menu focus target. | **Present; admitted reuse pending Story 018 presentation verification.** |

No Day 6 image, audio, video, character art, CG, prop, generated, or planned
asset file has a runtime reference. Those asset categories remain not admitted.

## Day 7 runtime reuse admission

Day 7 adds no asset identity. The red well, wind, water, paper, routes, and
names are visible narrative facts in text, not asset-file claims. Only the
existing font, code-defined warm-room background, and code-defined `say`
dialogue surface are admitted for actual references in `game/chapters/day7.rpy`.
Day 7 invokes no `choice` surface.

| Asset ID | Day 7 runtime use | Day 7 accessibility binding | Review status |
|---|---|---|---|
| `FONT-SOURCEHAN-LITE-P0` | Day 7 acknowledgement and resolver-handoff dialogue | `a11y.day7.text-copy`: all acknowledgement and handoff meaning remains visible/localizable text. | **Present; admitted reuse.** |
| `RUNTIME-SOLID-DAY1-WARM-ROOM` | `scene bg warm_room` at `chapter_day7_before_red_well` entry | `a11y.day7.warm-room-decorative`: background colour conveys no Day 1-6 fact, terminal input, or ending result. | **Present; admitted reuse.** |
| `RUNTIME-UI-DAY1-CHOICE-SURFACE` | Existing `say` dialogue screen only; no Day 7 `choice` surface | `a11y.day7.say-surface`: text remains readable and keyboard-advanceable; no quick-menu or visual-only interaction decides the handoff. | **Present; admitted reuse.** |

No Day 7 image, audio, video, character art, CG, prop, generated, planned, or
choice-only asset file has a runtime reference. Those asset categories remain
not admitted.

## Not admitted / not present

The following intended files have no matching file under `game/assets/`, no
recorded source or permission, and no binary SHA-256. They are deliberately
**not admitted** and must not be described as existing or be included in a
runtime build:

| Intended asset ID | Intended runtime path | State |
|---|---|---|
| `bg_station_platform_rain` | `game/assets/backgrounds/bg_station_platform_rain.png` | Not present; not admitted; not a Day 1 runtime reference. |
| `bg_ticket_gate` | `game/assets/backgrounds/bg_ticket_gate.png` | Not present; not admitted; not a Day 1 runtime reference. |
| `bg_train_window` | `game/assets/backgrounds/bg_train_window.png` | Not present; not admitted; not a Day 1 runtime reference. |
| `prop_wish_paper` | `game/assets/props/prop_wish_paper.png` | Not present; not admitted. |
| `prop_receipt_name` | `game/assets/props/prop_receipt_name.png` | Not present; not admitted. |
| `ui_focus_frame` | `game/assets/ui/ui_focus_frame.png` | Not present; not admitted; current focus treatment is code-defined. |

## Admission rule

An asset may enter `game/` only after its source, permission, modification
status, attribution requirements, SHA-256, runtime path, and accessibility
semantic binding are recorded here. Official *Dragon Raja* art, logos,
screenshots, audio, and extracted game assets are not admissible.
