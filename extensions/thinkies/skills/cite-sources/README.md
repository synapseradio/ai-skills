# cite-sources

Track, validate, and cite external sources with working URLs. Distinguishes retrieved information from training data and separates source material from synthesis.

## Try it when

- A claim needs a source a reader can open, and a link that might be dead will not do.
- You want to see which statements come from sources and which are the writer's own conclusions.
- A popular "fact" needs checking before you repeat it.

## What you walk away with

Each source consulted, with the URL actually visited, whether it resolved, what came from it, and which claims depend on it. Then what the sources state kept apart from what the writer concludes, and citations in the format the context calls for: structured for formal work, plain references for a technical discussion, inline links for a quick answer.

Here it is on the claim "goldfish have a three-second memory", cut down ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/cite-sources/goldfish-memory.md)):

> **What the sources state.**
>
> - According to Live Science, the three-second figure is a myth, and goldfish memory runs to weeks, months and years.
> - According to the Plymouth abstract, goldfish fed for one hour a day over 4 weeks anticipated the feeding time, and kept doing so for several days after the food stopped.
> - According to the Times, the Plymouth researchers reported a memory span of up to three months.
>
> […]
>
> **What I conclude.**
>
> […]
>
> - The three-month figure rests on source 3, a press report, and it is not in the Plymouth abstract I read. I would repeat "up to three months" only with that attribution.
>
> […]
>
> - I found no source that traces where the three-second number began. Source 1 says only that the number varies by region. This run therefore cannot say who first claimed three seconds.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/cite-sources/` into `~/.claude/skills/cite-sources/`.

## Usage

```
/cite-sources <claims or content requiring citation>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`cite-sources.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/cite-sources.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
