---
name: tree-of-thought
description: Use for a multi-part problem where each part has several workable solutions. Weighs alternative approaches for every part and joins the best of them into one coherent solution path.
---

# Tree of Thought Analysis

Work the query through four phases, and return what each phase produced: the components, the approaches with their scores, the selections, and the solution path.

## Query

`$ARGUMENTS`

A run handed no query text takes the problem from the request that loaded this skill, and failing that from the conversation. Where neither names a problem, ask for one before Phase 1 and stop.

## Phase 1: Decomposition

Break the query into core components with dependencies.

1. Identify a small set of fundamental components.
2. For each: describe what it involves, why it has its position in the sequence, and what it depends on.
3. Map dependencies between components (which must resolve before others can start).
4. Check that the components together cover the query: every one must be resolved for the query to be, and no two cover the same ground.

## Phase 2: Solution Generation

For each component, generate these distinct approaches:

- **A — Direct/Conventional**: straightforward, proven, minimal complexity.
- **B — Creative/Unconventional**: novel angle, handles edge cases, more flexible.
- **C — Systematic/Comprehensive**: thorough coverage, well-documented, maintainable.

The three kinds exist to force variety, so that the first plausible approach has rivals. The approaches for a component are alternatives: any one of them resolves it, and Phase 3 keeps one. Give each a first-pass viability score from 0.0 to 1.0 with a one-line reason. One shared scale lets approaches be compared at a glance across components before the full scoring.

## Phase 3: Evaluation & Selection

Score each approach against weighted criteria. Use these weights when the problem states no priorities of its own:

| Criterion       | Weight |
|-----------------|--------|
| Feasibility     | 40%    |
| Effectiveness   | 35%    |
| Risk (lower=better) | 25% |

Feasibility leads the default because an approach that cannot be carried out resolves nothing, however effective it would be. Reset the weights where the problem says what matters most, as when a safety-critical problem puts risk first, and state the weights you used.

Present scores in a comparison table per component. Select the best approach for each with a one-line rationale.

When no approach for a component scores well enough to act on, go back: generate new approaches for it in Phase 2, or cut it differently in Phase 1. Go back twice at most for any one component, so the run is not spent on one part of the problem. After that, carry the best available approach forward and name the gap under the areas of uncertainty in Phase 4.

## Phase 4: Synthesis

1. Integrate selected approaches into a coherent solution path with specific implementation steps per component.
2. Check that the selected approaches work together: name what passes between dependent components, and where one approach undoes another, return to Phase 3 for that component.
3. Surface key insights: patterns recognized, trade-offs made, unexpected findings.
4. Assess overall confidence (High/Medium/Low with percentage) noting strongest elements and areas of uncertainty.
5. Note a couple of alternative paths worth considering if the primary path encounters issues.

## Summary

Conclude with:

- **Recommended Solution**: one-paragraph synthesis.
- **Next Steps**: a few immediate actions.
- **Success Metrics**: how to validate the solution works.

The run is done when the summary is written and every component has a selected approach or a named gap.
