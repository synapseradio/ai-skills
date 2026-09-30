# what-if

Play out possible futures from a sparse question. Finds the unknowns that would change a decision, tiles one coherent future per combination, traces consequences and watchpoints between them, and walks its reasoning out loud before ending on a reasoned recommendation plus the conditions that would flip it.

## Reach for it when

- A decision hangs on things nobody can know yet: a rival's move, a customer's habit, a date that hasn't come.
- You keep picturing one future, usually the one you fear.
- You want a move you can commit to now, plus the signs that would tell you to change it.

## What comes back

The walk, question by question, sized to the problem. A question with no real unknowns gets a direct answer. A question with real unknowns gets the futures, named and told as a short story, followed by a table of how each candidate move fares in each. After that come what holds in every future, the early signs of which future is arriving, and a recommendation, with where it runs weakest. Facts only you hold, it asks for.

Trimmed from a staged conversation on a corner bakery, two staff and famous for its cinnamon knots, that learns a supermarket with an in-store bakery opens across the street in four months ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/what-if/corner-bakery.md)). A second agent played the owner, and supplied the numbers the run asked for: knots at about 40% of takings, an oven cap of 180 a morning, five months of savings.

> Your bakery's next year splits on two things nobody can look up today: whether the people who come for your knots keep coming once a supermarket sits across the street, and whether that supermarket sells a cinnamon roll of its own.
>
> […]
>
> | Tile | Landings | Hold course | Expand the oven | Knot club, trimmed counter |
> | --- | --- | --- | --- | --- |
> | Steady queue | regulars stay, no rival roll | survives | thrives | survives |
> | Two knots | regulars stay, rival roll | survives | survives | thrives |
> | Bread drain | regulars drift, no rival roll | dies | dies | survives |
> | Cold morning | regulars drift, rival roll | dies | dies | survives |
>
> […]
>
> Recommendation: start a knot club before opening day, trim the bread lines the supermarket will undercut, and buy nothing large until week three has spoken.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/what-if/` into `~/.claude/skills/what-if/`.

## Usage

```
/what-if <a decision, hypothetical, or idea whose future is uncertain>
```

## Sources

- Yao et al., "Tree of Thoughts" (arXiv:2305.10601) — propose candidates together to avoid duplication; triage states as sure/likely/impossible via lookahead; breadth limits; backtracking.
- Besta et al., "Graph of Thoughts" (arXiv:2308.09687) — aggregation merges convergent reasoning paths into one node; refinement loops a thought once through improvement.
- Weimer-Jehle's cross-impact balance analysis (properties in arXiv:0912.5352) — promote/restrict judgments between outcomes; a scenario stays consistent only when each of its outcomes holds against the combined impacts of the others.
- Peter Schwartz, "The Art of the Long View" — scenario planning, predetermined elements, critical uncertainties.
- Fritz Zwicky — morphological analysis and cross-consistency assessment.
- Jerome Glenn, early 1970s — the futures wheel.
- Winston, Chaffin & Herrmann (1987), "A Taxonomy of Part-Whole Relations," Cognitive Science 11(4), 417-444 — the relation types behind Q1, Q2, and the link-typing discipline.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`what-if.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/what-if.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
