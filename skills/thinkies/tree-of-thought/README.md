# tree-of-thought

Systematic Tree of Thought reasoning for complex problem decomposition. Instead of committing to the first plausible approach, this skill generates and evaluates multiple solution paths before recommending one.

## When to use this

Use it when the right approach is not obvious and the cost of choosing wrong is high — architecture decisions, migration strategies, complex debugging with multiple hypotheses. It adds structure to decisions where a plain prompt would give you one answer with false confidence.

For straightforward questions with clear answers, this is overkill. Just ask directly.

## What comes back

The problem split into components with their dependencies, three approaches per component (direct, creative, systematic) scored on feasibility, effectiveness, and risk, the pick for each, and a synthesis that checks the picks work together. Where one pick undoes another, it goes back and chooses again. It ends with a recommendation, next steps, success checks, and a confidence level.

Excerpts from a run on seating twelve wedding guests at two tables of six, with a feuding aunt and uncle, twins who must sit together, a best man bound to the bride's grandmother, two ex-flatmates who need a chaperone, and a vegan quorum ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/tree-of-thought/wedding-seating.md)):

> That breaks the flatmate rule. What passes between the dependent components is C's table and the count of open seats at V. Approach A for component 1 leaves one seat, the feud split spends it, and the remainder land at W with A and B together and C absent. **Approach A for component 1 undoes component 3.** Back to Phase 3 for component 1.
>
> […]
>
> - **The natural first move fails.** Putting every vegan at V looks safest and is the only vegan placement with no solutions. It fills V so completely that the feud split and the flatmate rule collide on the last seat.

In the run's names, V is the vegan table, W the other, and C the flatmates' chaperone. The run found 24 valid seatings and confirmed the count with a script that tried every split.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/tree-of-thought/` into `~/.claude/skills/tree-of-thought/`.

## Usage

```
/tree-of-thought How should we architect the caching layer for our API?
/tree-of-thought Evaluate approaches for migrating from monolith to microservices
```

## Sources

- Yao et al. (2023). Tree of Thoughts. [arXiv:2305.10601](https://arxiv.org/abs/2305.10601).

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`tree-of-thought.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/tree-of-thought.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
