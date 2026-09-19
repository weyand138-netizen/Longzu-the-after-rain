# Day 2 Authored Source Evidence

**Story**: `production/epics/sys-narrative/story-004-day2-authored-source.md`  
**Source unit**: `game/chapters/day2.rpy::chapter_day2_two_game_tokens`  
**Content baseline**: `narrative_content_baseline:v1.2`  
**Recorded**: 2026-08-11

## Owner Source Record

**Source SHA-256**: `fafd4643d207450842c6bbfc0a2c57432a4cd006540c0672b035a0578ff02ec1`

The record binds the Day 2 authored source to its three required scenes, the
five canonical choice/reaction/payoff identities, and the history-derived
`token_silence_as_consent` repair gate. A changed source requires a new hash
before a later full narrative-manifest or source-local validation handoff.

## Player-safe Catalog Inputs

- `chapter_day2_two_game_tokens`: Erii enters an alias and the final arcade
  handoff is observed.
- `memory_day2_arcade_alias`: Erii entering the alias only.

Neither input reads choice history, persistent state, live flags, axes, tokens,
qualifications, route labels, or ending state. The runtime-only repair gate is
derived by the separate pure canonical-choice projection.
