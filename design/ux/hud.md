# In-Game HUD Specification

> **Status**: Approved for P0 production handoff  
> **Date**: 2026-08-10  
> **Owner**: UX / SYS-ACCESS and SYS-NARRATIVE  
> **Scope**: Minimal visual-novel HUD; this document intentionally prohibits a persistent score/status HUD.

## Purpose

Narrative play must keep attention on observable character action, dialogue, and choice. The HUD exposes only reversible navigation and accessibility entry points; it never renders five-axis values, affinity, morality, route progress, hidden tokens, ending likelihood, or a “correct choice” signal.

## Surfaces and Entry Rules

| Surface | Visible controls | Entry / exit | Focus rule |
|---|---|---|---|
| Normal narration | Dialogue window plus quick menu: Back, Quick Save, Quick Load, Journal, Settings | Quick menu is available outside critical interactions; opening a menu returns focus to the invoking control | Logical left-to-right order; text labels always present |
| Choice | Dialogue/choice surface only | On choice entry, quick-menu controls are hidden and removed from focus; exit follows the committed choice | First choice receives focus immediately; choices are one vertical column |
| Critical/recovery flow | Approved safe-flow controls only | Recovery preempts Journal and quick actions | Initial focus is the first safe action; unavailable controls are neither visible nor focusable |
| Ending | Ending narration and approved 1–3 cause cards | Game-menu entry only after narration/cause-card flow completes | Cause cards preserve source order and expose no score or rank |

## Visual and Accessibility Contract

- Deep-blue, low-presence screen-space controls follow the Art Bible; the Journal alone may use its paper treatment.
- Every control exposes a text label and visible focus treatment using outline, fill, position, and text-state change. Colour never carries exclusive meaning.
- At 1280×720 with 1.5x text, the quick menu may wrap or use a viewport but may not obscure choice text or clip a focusable control.
- High contrast replaces decorative rain/paper texture with the approved token set. Reduced motion uses direct state changes. Silent and self-voicing paths present equivalent labels and status text.
- Hover-only, timed-only, icon-only, score, route, and hidden-state affordances are forbidden.

## Acceptance Evidence

- Engine testcase covers focus suppression during choices and recovery.
- Visual captures cover normal narration, choice, recovery, and 1.5x/high-contrast layouts.
- Content review confirms no HUD string exposes internal IDs, axes, tokens, predicates, or future outcomes.
