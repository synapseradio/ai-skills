# probe-boundaries

Test a claim or framing at its edges and extremes — maximize, minimize, remove, and transform its load-bearing variables — to find where it breaks and revise the scope.

## Worth running when

- A definition or rule works for every case you've tried, and you haven't tried the odd ones.
- A claim has to decide borderline cases ahead of time: a policy, a price list, a contract.
- Two people keep arguing over one example, and you suspect the definition itself is the problem.

## A run, trimmed

The words that carry the claim, each pushed to its extremes and removed in turn, each changed in kind and not just in degree, the framing's key words swapped for alternatives, the failures sorted into "too broad" and "too narrow" and traced to one cause, and a revised claim with its limits and a table of verdicts under both versions.

Excerpts from a run on "A sandwich is anything between two pieces of bread." ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/probe-boundaries/what-is-a-sandwich.md)):

> **"two", maximized.** A stack of forty slices, filling between each pair. Every adjacent pair satisfies the claim, so the stack holds thirty-nine sandwiches, or one. The claim counts pieces of bread and gives no way to count sandwiches.
>
> […]
>
> **The single cause.** The claim fixes three things (filling, position, bread) that are, in use, held together by a fourth thing that it never states: a middle enclosed by a carrier, eaten as one unit.
>
> […]
>
> **Revised claim.** A sandwich is an edible filling held between two pieces of a carrier, eaten as one handheld unit. Bread is the prototype carrier and not a requirement.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/probe-boundaries/` into `~/.claude/skills/probe-boundaries/`.

## Usage

```
/probe-boundaries <claim or framing>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`probe-boundaries.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/probe-boundaries.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
