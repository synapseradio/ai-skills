# derive-first-principles

Strip convention to irreducible truths — question every component, keep only what survives, reason up from the fundamentals — and find which constraints are real versus inherited.

## Try it when

- Something costs, takes, or weighs far more than it seems it should, and "that's just how it's done" is the only answer on offer.
- You are about to copy a standard approach and want to know which parts of it you actually need.
- A constraint feels fixed and you suspect it was only inherited.

## What it hands back

Every component of the conventional approach sorted into fundamental or inherited, with where each belief came from (law, need, habit, authority); the short list of truths that survive; a version rebuilt from those alone; the real constraints set apart from the inherited ones; and the options that open once the inherited ones are gone. Claims it cannot back are held as hypotheses with a stated test.

Trimmed from a run on why weddings cost so much ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/derive-first-principles/wedding-from-scratch.md)):

> The number follows from asking, for each name, "would the couple want this person present if nobody expected them to invite them?" That question separates presence the couple wants from presence obligation adds.
>
> […]
>
> **A tension in the reasoning.** The step from "the guest list is inherited from obligation" to "reduce it" ignores that for many couples, community presence is the point. […] The reasoning shows what is inherited and what is required. It does not show whether the couple should want the larger event. That is a values question for the couple, and the run leaves it there.
>
> […]
>
> - **Test the label.** Request quotes for the identical event under two names. If the quotes differ, the premium is a fact and can be avoided by not using the label with the vendor. If they do not differ, drop the hypothesis.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/derive-first-principles/` into `~/.claude/skills/derive-first-principles/`.

## Usage

```
/derive-first-principles <belief or approach>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`derive-first-principles.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/derive-first-principles.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
