# tutor

Interactive tutoring that adapts to your pace. Elicits learner preferences, plans 3-5 progressive layers, then teaches one concept at a time with comprehension checks and pacing controls.

## Try it when

- You want to learn something by working through it, not by reading about it.
- You learn best from comparisons with a field you already know.
- You want to set the pace: faster, slower, another example, or a detour.

## How a lesson runs

It asks how you like to learn: short or detailed, comparisons or definitions, a wander or a goal. Then it teaches one layer at a time, each one true on its own, and ends each with a question. Your answer decides whether it backs up, tries another angle, or moves on. You can say "faster", "slower", "example please", or "what if…" at any point.

Trimmed from a staged conversation on learning what a derivative is. A second agent played the learner, who knows only cooking and wants to explain it to their sister over tea ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/tutor/derivative-for-a-cook.md)):

> **User (played):** A short window gets you closer because the oven has less time to change its pace. Over a whole minute it might speed up partway through, so the average mixes slow and fast. Over a few seconds it's basically going one speed, so the average is nearly the true speed at that moment. It's like tasting a sauce with a tiny spoon instead of a ladle from the whole pot.
>
> […]
>
> **Skill:** Zero is the answer, and your second question is the sharp part of it. Zero means "not changing", not "nothing happening". The oven is still on and working hard to hold 180. The derivative only reports how fast the temperature is moving, never how hot it is.
>
> […]
>
> A cook who watches for the moment the rise stops is watching for the derivative to hit zero.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/tutor/` into `~/.claude/skills/tutor/`.

## Usage

```
/tutor <topic to learn about>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`tutor.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/tutor.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
