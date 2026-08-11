# Story 004: Day 2 Authored Source and Causal Beats

> **Epic**: SYS-NARRATIVE — Seven-Day Content Production  
> **Status**: Complete  
> **Layer**: Feature  
> **Type**: Config/Data  
> **Estimate**: 2 days  
> **Manifest Version**: 2026-08-04.1  
> **Last Updated**: 2026-08-11

## Context

**GDD**: `design/gdd/seven-day-chapter-script.md`  
**Requirement**: `TR-NAR-004` — The canonical Day 2 source unit declares its
three required scenes, exact choice/reaction/payoff bindings, and player-safe
source-hash/catalog inputs. `TR-NAR-001` remains the partial parent requirement
for the full seven-day content lock; this story does not claim full-manifest or
terminal-witness coverage.

**Governing ADRs**: ADR-0008 (primary), ADR-0003  
**Engine**: Ren'Py 8.5.3 | **Risk**: High

**Normative source**: `design/narrative/seven-day-content-baseline.md`,
`narrative_content_baseline:v1.2`: unit `chapter_day2_two_game_tokens`,
responsibility `responsibility_day2_alias_and_tokens`, and required scenes
`scene_day2_alias_answer`, `scene_day2_two_tokens`, and
`scene_day2_last_machine`.

## Acceptance Criteria

- [ ] Add the canonical `chapter_day2_two_game_tokens` unit under
  `game/chapters/` without changing the baseline's 15-unit set.
- [ ] Implement all three required Day 2 beats: `scene_day2_alias_answer`
  shows Erii entering her chosen screen alias; `scene_day2_two_tokens` presents
  the exact save-versus-spend effects stated in the Canonical Day 2 Binding
  Table; and `scene_day2_last_machine` completes the ordinary arcade handoff
  without score, route, or ending language.
- [ ] Use only the five canonical Day 2 choice IDs and implement their exact
  immediate reactions and strictly-later payoff IDs/results in the Canonical
  Day 2 Binding Table: `day2_accept_alias`, `day2_assign_alias`, conditional
  `day2_admit_alias_unknown`, `day2_save_second_token`, and
  `day2_spend_both_tokens`.
- [ ] Gate `day2_admit_alias_unknown` exactly on unresolved
  `token_silence_as_consent`; it is mutually exclusive with the two ordinary
  alias responses and ends the alias response node when present.
- [ ] Preserve Erii's action/object-led expression boundary and expose no
  axis, token, resource, route, qualification, internal-ID, prediction, score,
  or ending-hint language to players.
- [ ] Record the Day 2 source SHA-256 and player-safe Day 2 chapter/memory
  catalog inputs without runtime source scanning or live-history-derived copy.

## Implementation Notes

- Put Day 2 prose and local branching in its own `.rpy` chapter file with
  stable `snake_case` labels. Screens may render state but must not decide an
  alias, a token outcome, or continuation.
- Erii selects the alias through typing/gesture/object context; she may use a
  simple confirming monosyllable but no full spoken explanation or substitute
  written monologue.
- `day2_accept_alias` honors her entered alias (`U+A`), while
  `day2_assign_alias` overrides it and revokes `token_override_daily_choice`.
  When the prior silence token is unresolved,
  `day2_admit_alias_unknown` acknowledges uncertainty, re-asks, repairs that
  token, and honors her replayed alias (`U`).
- `day2_save_second_token` acquires `resource_arcade_token`; `day2_spend_both_tokens`
  establishes `event_both_tokens_spent`. Neither path may be framed as a
  correct/incorrect choice.
- Produce only source/data and source-hash evidence. ADR-0009 restricts the
  existing partial manifest to Day 1, so this story must not extend it, create
  a Day 2 partial-manifest alias, or claim terminal coverage.
- Apply the Feature-layer rules in `docs/architecture/control-manifest.md`:
  keep Day 2 in its own stable-label chapter file; let screens render state but
  never decide outcomes; retain keyboard/non-timed progression; and express
  Erii's complex intent through action, gaze, object interaction, or a simple
  monosyllable rather than a complete spoken sentence.

### Canonical Day 2 Binding Table

The source and source-data test must implement these exact observable bindings:

| Choice ID | Immediate player-visible reaction | Strictly later payoff ID and required result |
|---|---|---|
| `day2_accept_alias` | The player accepts the alias Erii entered. | `payoff_day2_alias_day4`: the Day 4 contact channel recognizes her chosen alias. |
| `day2_assign_alias` | Erii uses the player-entered name and moves her hand away. | `payoff_day2_assigned_alias_day6`: the contact cannot confirm her identity by her own marker. |
| `day2_admit_alias_unknown` | Erii demonstrates the alias again and confirms her entered alias. | `payoff_day2_admit_day5`: an ambiguous answer prompts a renewed request for confirmation. |
| `day2_save_second_token` | Erii gives the second token to the player for safekeeping. | `payoff_day2_token_day6`: it is available as an independent-contact identifier. |
| `day2_spend_both_tokens` | The second token is spent so Erii completes the game she wants to play. | `payoff_day2_spend_day4`: no physical identifier is available for the independent-contact node, while the shared arcade memory remains. |

At `scene_day2_two_tokens`, the visible copy must make the above practical
choice legible: saving keeps the second token for later identification, while
spending it completes the present game. Neither option may be presented as
correct, optimal, or ending-predictive.

## Performance Notes

No material runtime performance impact is expected: this story adds authored
source and immutable source-data inputs only. SHA-256 generation, source
scanning, and binding validation run only at build/test time; runtime performs
no source scan, CFG construction, or path enumeration.

## Out of Scope

- Any `narrative_partial_day2_manifest`, change to
  `narrative_partial_day1_manifest:v1`, full 15-unit manifest, terminal
  witness, ending, route qualification, or SYS-BUILD admission work.
- Day 3 prose, new player-visible prose outside Day 2, final art/audio,
  asset admission, and UI/layout redesign.

## QA Test Cases

- **AC-1 — canonical unit and beat coverage**
  - Given: the Day 2 source scanner and frozen baseline.
  - When: it enumerates production chapter labels and Day 2 scene markers.
  - Then: it finds exactly `chapter_day2_two_game_tokens` and the three
    required Day 2 scenes without changing the 15-unit baseline.
  - Edge cases: missing/duplicate unit or scene, or an extra production unit,
    fails with no catalog emission.
- **AC-2 — choice and conditional-node contract**
  - Given: source fixtures with and without `token_silence_as_consent`.
  - When: canonical Day 2 choice/reaction/payoff bindings are scanned.
  - Then: the two ordinary alias choices are always available, the admission
    choice appears only for the unresolved-token fixture, and all choices map
    to their approved Day 2 identities.
  - Edge cases: unknown ID, duplicate response, unavailable conditional choice,
    or a generic/same-scene payoff fails validation.
- **AC-3 — player-safe expression and provenance**
  - Given: all Day 2 player-visible strings and the completed source file.
  - When: the content-constraint and source-hash checks run.
  - Then: Erii has no full spoken dialogue, forbidden hidden-state language has
    zero matches, and the Day 2 catalog inputs match the recorded SHA-256.
  - Edge cases: stale hash, full Erii sentence, hidden-score wording, or
    live-history read rejects the source/catalog handoff.

**Required test path**: `tests/unit/sys_narrative/day2_authored_source_test.py`

## Test Evidence

- Automated source/data validation:
  `tests/unit/sys_narrative/day2_authored_source_test.py`
- Content-constraint scan: `tools/test-content-constraints.ps1`
- Owner source hash and player-safe catalog inputs:
  `production/qa/evidence/day2-authored-source-evidence.md`

## Dependencies

- Depends on: Sprint 1 complete; Story 001's Day 1 source remains the prior
  formal unit.
- Unlocks: Story 005.

## Completion Notes

**Completed**: 2026-08-11  
**Criteria**: 6/6 passing  
**Deviations**: User-authorized scope extension: a pure, history-derived token
projection was added for the Day 2 repair gate. It adds no persistent state,
manifest, terminal logic, or runtime source scanning.  
**Test Evidence**: `tests/unit/sys_narrative/day2_authored_source_test.py`
(8/8 passing); SYS-NARRATIVE authored-source suite (17/17 passing);
`tools/test-content-constraints.ps1` passed; Ren'Py 8.5.3 lint/compile passed;
source-hash record at `production/qa/evidence/day2-authored-source-evidence.md`.  
**Code Review**: Approved with suggestions. Story 005 retains the engine-route
and accessibility evidence responsibility.
