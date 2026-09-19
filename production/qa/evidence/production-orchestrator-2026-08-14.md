# Production End-to-End Orchestrator Evidence

**Date**: 2026-08-14
**Scope**: Story 024 — Production End-to-End Orchestrator
**Runtime root**: `game/`
**Engine**: Ren'Py 8.5.3.26051504

## Fixed Production traversal

`game/script.rpy::start` resets the run once and, outside the Ren'Py test
harness, calls the only Production traversal label:
`game/production_orchestrator.rpy::production_end_to_end_orchestrator`.

The orchestrator's exact call order is:

```text
prologue_start
chapter_day1_her_own_name
chapter_day2_two_game_tokens
chapter_day3_empty_school
chapter_day4_seaside_train
chapter_day5_family_lie
chapter_day6_no_safe_house
chapter_day7_before_red_well
day7_resolve_ending (owned by the Day 7 chapter handoff)
corresponding ending label (owned by SYS-ENDING's fixed map)
```

The test-harness branch exists only so the existing independent chapter tests
can enter `start` without the outer test runner advancing into the next
chapter. It does not write state or exist in the non-test Production path.

## Evidence matrix

| Check | Result | Evidence |
| --- | --- | --- |
| Orchestrator focused integration test | PASS — 3/3 | `tests/integration/sys_narrative/production_orchestrator_test.py` |
| Full Python suite | PASS — 281/281 | `uv run python -m unittest discover -s tests -p '*_test.py'` |
| Ren'Py global suite | PASS — 56/56 testcases, 474/474 assertions | `tools/run-renpy-tests.ps1 -Suite global -TimeoutSeconds 120` |
| Ren'Py lint/compile | PASS | Ren'Py 8.5.3 `lint --compile` |
| Content constraints | PASS | `tools/test-content-constraints.ps1` |
| Diff whitespace | PASS | `git diff --check` |

## Semantic boundary

No choice, axis, token, resource, qualification, ending condition,
player-facing copy, persistence field, or persistence write was added or
modified. Existing chapter labels remain present and independently callable;
the Day 7 chapter retains the single `jump day7_resolve_ending` handoff and
SYS-ENDING retains ownership of resolver selection, ending labels, lifecycle,
completion, and persistence.

## Source hashes

The hashes below bind this evidence to the reviewed source generation.

- `game/script.rpy`: `e8c0b143f937aff62f8cce2f3b43160ea4721f4c6edba0f5b0524bc89cf66f12`
- `game/production_orchestrator.rpy`: `3ab95a165db8de6fb2d447bfcf3571198184d7b293a1595ffc37fe60ed57cc8f`
- `tests/integration/sys_narrative/production_orchestrator_test.py`: `d2aaf129fad280b9b615a07b95724fcb62c489af8c67adcaf49a32028eafef89`
