# Design Change Impact: rain_stops epilogue extension

**Date**: 2026-08-14
**Changed design**: `design/gdd/seven-day-chapter-script.md`
**Normative baseline**: `design/narrative/seven-day-content-baseline.md`
**Reference input**: `C:\Users\Andwey\Downloads\好结局剧本标注版.docx`
**Change owner**: SYS-NARRATIVE
**Decision status**: Design-authorized for implementation; source-license/official-canon status remains unconfirmed.

## Source and usage boundary

The DOCX is treated as an unconfirmed fan-adaptation reference. This project
uses only its high-level structure and thematic direction. No sentence,
character roster, named-world-state assertion, or scene wording is copied into
the project. If implementation would require line-by-line reuse or a major new
canon fact, the work must pause for human adjudication.

## Proposed change

Extend the already existing `epilogue_rain_stops_arcade` inside the existing
`rain_stops` path, after the current lights-out scene, with a restrained
“years later” tail:

1. An unnamed neighborhood observer notices the small arcade continuing as an
   ordinary local business, using a few unnamed old friends and ordinary
   customers as background texture rather than a named-character reunion.
2. A clearly marked written note by 绘梨衣 provides the inward-facing close.
   Complex content belongs to the written note only; it is not rendered as
   complete spoken dialogue and does not become an `erii` speech line.
3. The tail remains quiet and short. It does not confirm 夏弥's return, the
  源氏兄弟's return, 路鸣泽 as family, pregnancy, twins, or any other major
   world-state claim.

## Frozen invariants

- Six ending IDs, resolver, priority order, canonical witnesses, five axes,
  token definitions, route qualifications, ending predicates, and completion
  boundary remain byte-for-byte semantic contracts.
- `rain_stops` remains the only path that enters the existing arcade epilogue.
- No choice, route, ending, achievement, Gallery entry, persistent field,
  canonical unit, new canonical event, or hidden-score rule is added.
- Existing `event_epilogue_first_guest_completed` and
  `event_epilogue_lights_out_completed` remain the only epilogue completion
  events. The new tail occurs after the existing lights-out completion and
  does not move or duplicate the completion boundary.
- No asset directory, image, UI bitmap, audio, music, or voice file is
  created or modified. Existing code-defined text presentation remains the
  only implementation surface.

## Impact assessment

| Area | Impact | Required action |
|---|---|---|
| GDD | The ending/epilogue boundary must state that the existing rain-stops unit may contain this post-lights-out tail under the same responsibility. | Update the epilogue rules and character/content constraints. |
| Content baseline | The 15-unit tuple, six ending records, witnesses, choice universe, token set, qualification bindings, and completion events remain unchanged; the existing epilogue purpose gains the two retained structural elements and explicit exclusions. | Update baseline version and epilogue boundary text; do not add a unit or stable ID. |
| Content lock | This is a player-visible narrative addition, so the lock needs a new lock ID and source-manifest identity after final implementation. | Register the affected ending source and updated baseline hash; rerun source/content constraints. |
| Traceability | `TR-NAR-001` remains Partial because full content-lock/enumeration evidence is still downstream. The change is a controlled implementation expansion under its existing requirement; no new TR-ID is needed. | Record this impact and preserve the Partial status. |
| ADR-0003 | Still valid: chapter/epilogue prose remains in a chapter file; the orchestrator and screens do not own narrative outcomes; text-only presentation does not require assets. | Keep as-is. |
| ADR-0006 | Still valid: the new text follows the existing terminal completion node; no new completion call or persistence input is introduced. | Keep as-is and test callsite/order invariants. |
| ADR-0008 | Still valid: no canonical unit, choice, reaction/payoff join, terminal witness, resolver input, or production graph edge is added. | Keep as-is and add static source-boundary tests. |
| Assets/legal | No production asset admission or licence decision is required. The DOCX remains a reference only. | Do not touch asset/legal production files. |

## Risk and acceptance strategy

The main risk is accidental canon expansion or accidentally presenting written
material as spoken dialogue. The story and tests must therefore assert:

- only `rain_stops` contains the tail;
- the tail appears after lights-out and after the existing completion events;
- no new choice/axis/token/qualification/resolver/persistence/achievement
  identifiers occur;
- no named extra character or forbidden world-state phrase is required;
- complex 绘梨衣 content is explicitly labeled as written and is not an
  `erii` dialogue statement;
- the source remains within the existing 15-unit manifest.

Automated checks may establish source topology, IDs, ordering, and copy-boundary
constraints. Human narrative/readability, copyright, official-canon, SAPI, and
subjective experience review remain deferred and must not be marked PASS by
automation.
