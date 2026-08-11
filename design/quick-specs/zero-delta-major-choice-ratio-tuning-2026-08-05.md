# Quick Design Spec: Zero-Delta Major Choice Ratio Tuning

**Type**: Tuning  
**System**: SYS-STATE / SYS-NARRATIVE  
**GDD Reference**: `design/gdd/five-axis-state.md` — Tuning Knobs section  
**Date**: 2026-08-05

## Change

| Parameter | Old Value | New Value | Rationale |
|-----------|-----------|-----------|-----------|
| `zero_delta_major_choice_ratio` target | `10%–20%` | `45%–65%` | The frozen v1.2 content baseline contains 52 `semantic_major` choices, of which 30 (`57.7%`) intentionally use no axis delta while still producing registered event, resource, counterevidence, repair or outcome semantics. The higher target prevents the axis model from reading as a hidden score while retaining machine-verifiable consequences. |
| `zero_delta_major_choice_ratio` safe range | `0%–25%` | `35%–70%` | The old safe ceiling rejects the approved content structure. The new band contains the verified `57.7%` baseline while retaining lower and upper review pressure. |

## Tuning Knob Mapping

Maps to GDD tuning knob `zero_delta_major_choice_ratio` and registry entry of the same name.

The verified v1.2 value is `30/52 = 57.7%`, which is within the new target range. This is an authoring/content-build ratio, not a runtime parameter; no `assets/data/` file exists or is required for it.

Zero axis delta does not mean zero semantic effect. Every zero-axis `semantic_major` choice must retain at least one registered route fact, event, resource effect, counterevidence revoke/repair or outcome difference plus its reaction/payoff coverage.

## Acceptance Criteria

- [x] `design/gdd/five-axis-state.md` defines target `45%–65%` and safe range `35%–70%`.
- [x] `design/registry/entities.yaml` carries the same target and safe range.
- [x] `design/gdd/seven-day-chapter-script.md` remains consistent at target `45%–65%`, safe range `35%–70%` and baseline `30/52 = 57.7%`.
- [x] The v1.2 content catalog independently counts 52 `semantic_major` choices and 30 zero-axis choices.
- [x] Static catalog validation confirms every zero-axis major choice declares a non-axis semantic projection and nonempty reaction/payoff evidence.
- [ ] No regression: five-axis reachability, four-opportunity recovery minimum, token caps and ending qualification remain satisfied.

## GDD Update Required?

Yes. Update the `zero_delta_major_choice_ratio` row in `design/gdd/five-axis-state.md` and atomically update the registry entry. No chapter-GDD edit is required because the later content baseline already carries the approved replacement values.
