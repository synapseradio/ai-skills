# evaluate-evidence

Assess how well evidence supports claims. Evaluates source quality, methodology, and counter-evidence, then rates support as strong, moderate, weak, or unsupported.

## Call on it when

- Someone offers a few stories and a half-remembered study as proof, and you want to know what they actually show.
- A claim bundles a cause, a mechanism, and advice, and you suspect only one of them was tested.
- You need to say how sure to be, not just whether something is true.

## What you walk away with

The claim split into the parts that can be tested separately, an inventory of each piece of evidence (direct or indirect, primary or secondhand), the other explanations that fit the same facts, outside sources each placed on a rung from artifact down to hearsay, a support rating per part, and what would strengthen or weaken it, down to the cheapest test you could run yourself.

Trimmed from a run on whether houseplants thrive when you talk to them, the evidence being an aunt's lush ferns, a TV show, and a silent cactus that died ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/evaluate-evidence/talking-to-plants.md)):

> The offered evidence alone rates **Unsupported to Weak**: it adds nothing that a fern in a lively household and a cactus in a quiet one would not show under every other explanation.
>
> […]
>
> - A control that separates sound from attention: a third group that receives the same human attention (watering, inspection) with recorded speech or with no speech, so the effect of noticing problems can be told apart from the effect of sound.
>
> […]
>
> **Cheapest test the reporter can run now:** two cuttings of one fern, same window, same watering, one talked to daily, one not, kept for two months. It will not settle the question at n = 2, and it will show whether a difference large enough to notice appears.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/evaluate-evidence/` into `~/.claude/skills/evaluate-evidence/`.

## Usage

```
/evaluate-evidence <claim requiring evidence evaluation>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`evaluate-evidence.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/evaluate-evidence.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
