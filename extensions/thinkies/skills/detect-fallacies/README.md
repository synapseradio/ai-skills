# detect-fallacies

Spot logical errors in reasoning. Scans for ten common fallacy patterns, locates the specific flaw, and suggests corrections.

## Call on it when

- An argument feels persuasive and wrong at once, and you can't say where it slips.
- You are about to make a case yourself and want the weak links found first.
- You want to tell a fallacy apart from an ordinary exaggeration before calling one out.

## What you'll get

The argument laid out as claim and premises, the fallacies found with where each one sits, the single step where the reasoning breaks, a steelman that tests each flag against the most charitable reading, and a corrected version that makes only claims someone could check.

Here it is on a cereal advert ("Nine out of ten astronauts' kids eat Crunchos…"), cut down ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/detect-fallacies/crunchos-advert.md)):

> The break is between P1 and the conclusion. The advert never says why an astronaut's child's breakfast should be evidence of quality for anyone else. That gap is filled with status.
>
> […]
>
> After steelmanning, the stronger version of the advert is: "Children in a small, notable group eat this cereal, and we think you might like it." That version commits no fallacy, and it also fails to persuade, which suggests the fallacies are the persuasion.
>
> […]
>
> A counter-example makes the transfer visible: nine out of ten test pilots' kids may also drink a particular brand of orange juice, and nobody would conclude the juice makes a pilot.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/detect-fallacies/` into `~/.claude/skills/detect-fallacies/`.

## Usage

```
/detect-fallacies <argument or reasoning to check for fallacies>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`detect-fallacies.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/detect-fallacies.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
