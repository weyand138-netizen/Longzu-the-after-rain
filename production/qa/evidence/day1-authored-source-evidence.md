# Day 1 Authored Source Evidence

**Story**: `production/epics/sys-narrative/story-001-day1-authored-source.md`  
**Source unit**: `game/chapters/day1.rpy::chapter_day1_her_own_name`  
**Content baseline**: `narrative_content_baseline:v1.2`  
**Recorded**: 2026-08-10

## Owner Source Record

**Source SHA-256**: `7bcf51ae66b558703b453125bd7f804346895ce7d24757be3fd0b643dfdf8aa9`

The record binds the Day 1 authored source to its required scene IDs, canonical
Day 1 choice/reaction/payoff identities, and player-safe chapter/memory catalog
inputs. A changed source requires recomputing this hash before Story 002 may
generate a flow manifest.

## Player-safe Catalog Inputs

- `chapter_day1_her_own_name`: clothing selected, food gesture observed, and
  receipt-name anchor observed.
- `memory_day1_receipt_name`: the receipt-name anchor only.

Neither input reads choice history, persistent state, live flags, axes, tokens,
qualifications, route labels, or ending state.
