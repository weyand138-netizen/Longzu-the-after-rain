# Project Instructions

## Project

- **Title**: 雨停之后
- **Creator Credit**: Andwey
- **Type**: Free, non-commercial, unofficial Dragon Raja fan visual novel
- **Language**: Simplified Chinese
- **Target**: Windows 10/11 x86-64

## Technology Stack

- **Engine**: Ren'Py 8.5.3
- **Language**: Ren'Py Script + Python 3.12-compatible pure modules
- **Build System**: Ren'Py distribution builder
- **Asset Pipeline**: Source assets -> reviewed game assets -> Ren'Py archives
- **Design Resolution**: 1920x1080, scalable to 1280x720

## Non-Negotiable Product Rules

1. No commercial release, donations, official branding, or implied authorization.
2. Do not quote or closely reproduce prose from the original novels.
3. Do not add official or source-unknown art, music, logos, fonts, or game assets.
4. Endings are deterministic and must never depend on randomness, external guides, or secret passwords.
5. Player-facing UI must not expose numeric affection or morality scores.
6. Choices must have an immediate reaction and a later causal payoff.
7. Save/load/rollback compatibility takes priority over implementation convenience.
8. Network access and telemetry are forbidden in the shipped game.
9. Accessibility-critical features and the six endings may not be cut for schedule.

## Implementation Rules

- Use `default` for per-playthrough mutable state.
- Use `persistent` only for cross-playthrough unlocks and settings.
- Keep ending resolution in `game/modules/ending_rules.py`; narrative labels consume its result.
- Imported pure Python modules must not mutate Ren'Py store state.
- Use replacement assignment for choice history (`history = history + [...]`) so rollback remains reliable.
- Every new route requires both a pure logic test and a Ren'Py flow testcase.
- Placeholder assets must be clearly named and replaceable without changing story code.

