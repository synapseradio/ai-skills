# ideate

Generate and filter ideas into vetted options. Six phases: seed, diverge, cluster, filter, refine, hand-off. Produces 2-5 comparable options for decision-making.

## It helps when

- You need options, not one idea, and want them in a form you can compare side by side.
- Brainstorms leave you with a long list and no idea which items survive contact with your constraints.
- The obvious answers are used up.

## What a run looks like

The problem restated with its hard constraints, soft preferences and a filter announced before any idea appears; a long unjudged list of ideas; the ideas grouped by how they work; each group passed, made conditional, or eliminated against the filter, with the reason; and a short set of options, each with its approach, strengths, key risk and what it needs.

Here it is on a cupboard full of left-over bubble wrap, cut down ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/ideate/bubble-wrap-cupboard.md)). The constraints were set by the run itself, since the question gave none, and the run says so:

> **Announced filter for step 4.** An idea survives only if it (a) uses no more than trivial money, (b) has a legal and safe end for the plastic, (c) consumes wrap in bulk, and (d) can start this week.
>
> […]
>
> 1. Assume popping is the point: sell bags of "pre-popped" and "pop-me" wrap.
>
> […]
>
> **Option 1: Pass it on**
>
> - Approach: Offer the whole cupboard free to neighbours, movers, small sellers and schools, with a fixed collection window.
> - Strengths: Empties the cupboard fastest with no cost, no making, no storage, and gives the plastic a second life as wrap.
> - Key risk: Takers do not turn up, so the cupboard stays full.
> - Requires: A neighbourhood channel or noticeboard, a collection slot, and bags sorted by size.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/ideate/` into `~/.claude/skills/ideate/`.

## Usage

```
/ideate <problem or opportunity to ideate on>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`ideate.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/ideate.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
