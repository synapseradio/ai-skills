# excavate-assumptions

Surface unstated assumptions at the semantic, pragmatic, logical, and framework levels, rank them by importance and certainty, and test the ones that are both critical and shaky.

## Worth running when

- A plan sounds obviously good and nobody has asked what it takes for granted.
- You want to know which of a plan's premises would sink it if wrong, and which can wait.
- An argument moves in one smooth step from what is true now to what will be true later.

## You get back

Every assumption in the framing, numbered; what each level of reading (meaning, purpose, logic, worldview) requires to be true; a table rating each assumption for importance and certainty; the critical, shaky ones grouped by what they are about; and for each of those, the evidence that would disprove it and what follows if it is false.

A run on a plan to train the office parrot as receptionist, trimmed ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/excavate-assumptions/parrot-receptionist.md)):

> - "Hello" and "one moment please" are both cue-free courtesies. They work at nearly any moment: a greeting fits any arrival, and a wait phrase fits nearly any pause. A question fits only its own cue, and the answer to it varies. The step from courtesy to question crosses a boundary the argument treats as flat.
>
> […]
>
> - If the opposite were true: the parrot is a recording with a beak. It can be entertaining and cannot be a receptionist, and the plan becomes a question about mascots.
>
> […]
>
> The cheapest first step is the duty log and the visitor-question tally, because if they show reception is more than three recited questions, the parrot is not a candidate whatever it can learn.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/excavate-assumptions/` into `~/.claude/skills/excavate-assumptions/`.

## Usage

```
/excavate-assumptions <claim or framing>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`excavate-assumptions.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/excavate-assumptions.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
