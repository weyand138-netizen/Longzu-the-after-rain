# ADR-0003: Content and Presentation Boundary

- Status: Accepted
- Date: 2026-07-23
- Engine: Ren'Py 8.5.3
- GDD requirements: SYS-NARRATIVE, SYS-JOURNAL, SYS-ACCESS, SYS-AUDIO, SYS-BUILD

## Context

The seven-day narrative will grow to tens of thousands of Chinese characters while presentation assets will change repeatedly. Story logic must remain readable and asset replacement must not rewrite branches.

## Decision

- Put each chapter in its own `.rpy` file under `game/chapters/`.
- Centralize character, color, transition, and placeholder declarations.
- Screens read state but do not decide narrative outcomes.
- Narrative labels call small helpers for state and achievement changes.
- Use stable semantic asset names; final files replace placeholders behind those names.

## Implementation Guidelines

- A chapter label owns prose and local branching, not global ending rules.
- Screens must support keyboard focus and readable text at 1280x720.
- No scene may require animation, sound, hover, or timed input to continue.
- Every image introduced must include source registration and planned self-voicing alternative text.

## Alternatives Considered

- One monolithic script: rejected due to merge, lint, and navigation cost.
- UI-owned route branching: rejected because screens can be shown from many contexts.
- Asset paths embedded throughout prose: rejected because placeholder replacement would be unsafe.

## Performance Implications

Chapter separation has no material runtime cost. Predict only imminent images and audio.

## Engine Compatibility

Uses standard Ren'Py labels, screens, styles, and image declarations available in 8.5.3.

