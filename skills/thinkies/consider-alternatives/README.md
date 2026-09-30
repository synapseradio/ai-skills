# consider-alternatives

Generate competing explanations for the same observations by varying mechanism, scope, timing, and causation, then identify the tests that distinguish them.

## Reach for it when

- One explanation arrived first and nobody has looked for a second.
- The favourite explanation fits most of the facts and strains on one or two.
- You need to decide what to check, and want the check that rules out the most.

## A run, trimmed

The current explanation and its evidence, a set of alternatives that vary the mechanism, the scope, the timing, or the direction of cause (combined causes and coincidence included), what each would predict if true, and the tests that separate one from another.

Excerpts from a run on every sock in the house losing its partner in the same week ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/consider-alternatives/the-great-sock-loss.md)):

> Two observations strain it. The loss hit every sock in the house, where a machine fault would usually take some. And it landed in one week, where a machine has been doing the same thing for months. Whatever is true must explain "all" and "one week", or it is at best a piece of the answer.
>
> […]
>
> 1. **Direction of cause reversed: the socks were not lost, the count was.** Someone began checking pairs that week, after a first missing sock made the topic salient. Socks that had always been odd were noticed for the first time. Nothing changed in the socks. Attention changed.
>
> […]
>
> 1. **Count.** Count the singles and count the pairs a month ago, using a photo or the shopping record if one exists.
>    - Total unchanged, singles now visible: alternatives 3 and 8.
>    - Total lower by half the pairs: alternatives 1, 4, 5, 6 (something left the drawer).
>    - Total lower by a few: alternative 9.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/consider-alternatives/` into `~/.claude/skills/consider-alternatives/`.

## Usage

```
/consider-alternatives <observation or current explanation>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`consider-alternatives.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/consider-alternatives.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
