# Vertical Slice Test Evidence

> VERTICAL SLICE — NOT FOR PRODUCTION
>
> Validation Question: Can a new player feel that care means observing, asking, and accepting shared cost within five minutes without guidance, and can one such loop be produced in one build day at representative quality?
>
> Date: 2026-07-23

## Automated result

- Engine: Ren'Py 8.5.3.26051504
- Python: 3.12.7
- Test suites: 1/1 passed
- Test cases: 3/3 passed
- Assertions: 16/16 passed
- Repeatability: the complete suite passed twice after the final visual baseline was created
- Character dialogue constraint: passed; Erii has no complete spoken line
- Lint: clean
- Compile: clean

## Covered paths

1. Observe → ask → identify the tracker; verifies all three delayed payoffs.
2. Prioritize safety → decide the route → retain an exit; verifies the alternate payoff text.
3. Complete the full loop using keyboard navigation, then open and close the wish journal.

## Visual evidence

- The game requests a 1280 × 720 default physical window while retaining a 1920 × 1080 virtual layout.
- The automated Windows test surface reported 1739 × 978 and produced 1738 × 977 captures under desktop scaling.
- Choice, revised completion, and revised journal baselines were visually inspected for legibility, contrast, clipping, and focus state.
- Evidence is stored in `tests/screenshots/visual/`.

## Remaining gate

Automated evidence does not answer whether a first-time player understands the intended meaning or completes the loop within five minutes. A real unguided playthrough is required before recording a PROCEED, PIVOT, or KILL verdict.
