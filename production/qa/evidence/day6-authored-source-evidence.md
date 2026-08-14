# Day 6 Authored-Source Evidence

**Date**: 2026-08-13
**Unit**: `chapter_day6_no_safe_house`
**Source**: `game/chapters/day6.rpy`

**Source SHA-256**: `dbe1f47ce705bc73520c0aa3b6115cd2f803f292605dd2b79a2854adf0ff98be`

**Historical prior generation SHA-256**: `4571b38e0ad718d7ee0b2c581f4257c98e3f31fc948004408b204c6d3915f99e`

## Player-Safe Catalog Inputs

- Chapter: `chapter_day6_no_safe_house` / day 6 /
  `fact_day6_safehouse_failure`, `fact_day6_cost_consequence_expressed`, and
  `fact_day6_route_commitment_expressed`.
- Memory: `memory_day6_cost_and_route` / day 6 /
  `fact_day6_route_commitment_expressed`.

## Guarded Commitment Contract

`erii_day6_commitment_derivation:v1` accepts only the exact ordered Day 5
answer/outcome, route-response, resource, cost-acknowledgement, and unresolved
daily-override facts. It applies
`honored_contact_then_shared_then_solo_then_old_order_then_fallback_v1` and
records one allowed commitment state, its visible object/action, source hash,
and zero hidden inputs. Unknown, untyped, incompatible, or contradictory facts
are `undetermined` and expose no commitment choice.

## Scope Boundary

This record covers authored Day 6 source and its pure commitment derivation
only. It makes no Day 7, terminal-witness, resolver, qualification, ending,
epilogue, partial-manifest, asset-admission, route/accessibility-evidence, or
release claim.
