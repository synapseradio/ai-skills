# flip-assumptions

Test claims by forming the contrapositive. Reveals hidden assumptions by negating and reversing the original conditional.

## Use it when

- A rule of thumb sounds right and you can't think how you would ever check it.
- A claim leans on a word nobody can measure ("fun", "good", "healthy").
- You want the counterexample that settles an argument in one sentence.

## What comes back

The claim as an explicit if-then, its contrapositive (kept apart from the converse, which says something else), which of the two is easier to test and how, the assumptions the flip exposes, evidence for and against both forms, and the weaker claim that survives.

A run on "If the party is fun, people stay past midnight", trimmed ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/flip-assumptions/party-past-midnight.md)):

> One of the common proxies for fun is guests staying late, which is Q. Testing the original with that proxy means testing Q against Q, so the test cannot fail.
>
> […]
>
> The contrapositive is plainly false for the child's birthday party. The skill's rule applies: since the contrapositive fails, the original fails, and here it failed faster. "That party was over by six and nobody remembers it as anything but a great day" settles the matter in one sentence, where refuting the original directly meant hunting for a fun party that ended early.
>
> What survives is a weaker claim. "Among parties where guests are free to stay and midnight lies inside the party's hours, fun raises the chance that some guests stay past midnight."

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/flip-assumptions/` into `~/.claude/skills/flip-assumptions/`.

## Usage

```
/flip-assumptions <claim or conditional to flip>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`flip-assumptions.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/flip-assumptions.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
