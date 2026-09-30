# skill-design

Design a new Agent Skill, refactor an existing one, or audit one with
the user. Each mode works the same way: pose a principle as a question
about the skill at hand, gather evidence from its files, and decide
from the evidence. One question underlies all ten principles: can the
executor close every decision delegated to it, using only what the
skill provides?

Design ends at a brief for skill-creator to build from, never at a
SKILL.md. Refactor ends at a change set backed by evidence, applied
once approved. Audit changes nothing: it runs as a conversation —
align on intent, walk the principles as lenses, converge — and ends at
priorities the user confirms.

## Reach for it when

- You have an idea for a skill and want to decide what it does, for whom, and where its edges are before anyone writes a SKILL.md.
- A skill fires on requests it shouldn't, misses ones it should, or loads more context than the task needs.
- You want a skill judged against stated principles before you ship it.

## A design session, trimmed

In design mode the skill states the intent as it reads it, and stops wherever two readings would build different skills. When you ask, it researches the facts the skill will rest on and keeps what it couldn't verify on a separate list. It ends at a design brief.

From a staged conversation on "Design an Agent Skill that helps someone pick a houseplant they will not kill." ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/skill-design/unkillable-houseplant.md)). A second agent played the user, a cat owner:

> 1. **Match the plant to the home and habits.** The skill asks a few questions (window direction, hours of light, how long the person is away, whether they tend to overwater or forget, pets or small children) and recommends plants whose needs sit inside what that person supplies.
>
> […]
>
> 1. **Name the most forgiving plants, with no intake.** The skill hands over a ranked short list of tolerant plants (the kind that survive low light and missed waterings) with one line on each.
>
> […]
>
> **Floor (move 4).** The weakest executor the skill must work on can ask the user questions one at a time, read a reference table, and apply a stated exclusion before ranking. It cannot be assumed to browse the web. That choice shapes the design: toxicity has to sit in the reference, with its source link per row, because a floor with no web access cannot look it up at run time.

## Pairs with skill-creator

Deciding what a skill should be belongs here; building, testing, and
packaging belong with skill-creator. The two overlap nowhere:
drafting, evals, trigger optimization, and packaging all sit with
skill-creator, and whoever runs skill-creator next can answer its
intake questions from the design brief alone.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/skill-design/` into `~/.claude/skills/skill-design/`.

## Usage

> Design a skill that turns a captured team workflow into a reusable
> Agent Skill.

> Audit skills/my-skill against the ten principles.

> This skill over-triggers on unrelated requests. Refactor it so the
> description narrows correctly.

> Review my SKILL.md before I ship it.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`skill-design.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/skill-design.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
