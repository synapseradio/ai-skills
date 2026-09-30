# prompt

Craft or refactor LLM instructions grounded in Anthropic's functional-emotions
research. The skill detects whether the input is a seed task or an existing `CLAUDE.md` to refactor, and emits structured output that applies the seven Emotional Intelligence
Prompting (EIP) principles while preserving every instruction in the input.

## What it does

Two modes, one pipeline:

- **Seed:** rough task description → a prompt in six sections
  (Perspective, Task, Context, Tooling, Constraints, Invitations)
- **Refactor:** existing CLAUDE.md / system prompt → refactored file, with
  every instruction numbered and mapped to a section so none is dropped;
  past 15 instructions it shows the coverage report and asks before
  writing

When the input could be either, it treats it as a seed and says so on the
artifact's first line.

Every output passes a 9-item anti-pattern lint derived from the
[emotion-concepts paper](https://transformer-circuits.pub/2026/emotions/index.html):
no threat framing, no demanded certainty, no authoritarian stacks, no
forced enthusiasm, no perfect-prompt fallacy.

## Call on it when

- You have a task for a model and only a rough sentence describing it.
- An existing `CLAUDE.md` or system prompt has grown by accretion, and you want it restructured without losing a single instruction.
- A prompt keeps getting brittle or anxious output, and you suspect the wording is the cause.

## A seed, in and out

From a run on the seed "Write a prompt that makes a model write limericks about tax law without a single wrong fact." ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/prompt/tax-law-limericks.md)). The seed named no jurisdiction or count, so the run picked five limericks in one named jurisdiction and said so. Trimmed from the prompt it wrote:

> So the craft is in choosing what to rhyme. Pick rules you can state exactly, and let the joke sit in the situation, the wording, or the irony. Leave the numbers out of the verse unless you are certain of the number and its year.
>
> […]
>
> - A figure appears in a verse only if its claim line gives the same figure and its year.
>
> […]
>
> If you cannot find five rules you are sure of, write fewer limericks and say so. Four sound limericks are worth more than five with a soft spot.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/prompt/` into `~/.claude/skills/prompt/`.

## Usage

```
/prompt <seed task, or a CLAUDE.md or system prompt to refactor>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`prompt.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/prompt.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
