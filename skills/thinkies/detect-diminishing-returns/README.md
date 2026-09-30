# detect-diminishing-returns

Detect when further exploration produces little gain. Tracks pattern emergence, tests predictive power, measures novelty, and declares convergence.

## Worth running when

- You are on another pass of the same draft, search, or analysis and can't tell whether it is still getting better.
- Each round changes something, but the changes keep undoing each other.
- A deadline is close and you need a stopping rule, not another round.

## What you walk away with

A table of what each round added, a check of whether the next round has become predictable, a count of the changes that left the work different from every earlier round, the questions no further round of the same kind can answer, and a verdict: what has settled, how confident to be, and what to do instead of another round.

On someone's ninth draft of a best-man speech ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/detect-diminishing-returns/ninth-best-man-draft.md)), trimmed:

> Novelty fell from 100% of the changes to 0% and has stayed there for five consecutive drafts. Five drafts of work produced a speech identical to what it would have been after draft 4, plus the time it took to write them.
>
> […]
>
> - High confidence that further redrafting on the page has reached zero marginal value. Five drafts with zero net novelty and five correct predictions in a row support this well.
> - No confidence, in either direction, about whether the speech is good. The drafts contain no measurement of that. Convergence of the text shows the writing has stopped changing, and does not show the speech works.
>
> […]
>
> **Recommended stopping rule, given that the wedding is Saturday:** stop drafting. Read the speech aloud once against a clock.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/detect-diminishing-returns/` into `~/.claude/skills/detect-diminishing-returns/`.

## Usage

```
/detect-diminishing-returns <research or analysis to evaluate for saturation>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`detect-diminishing-returns.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/detect-diminishing-returns.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
