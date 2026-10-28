# writing-agent-instructions

Write, shorten, or review an instruction a model reads and acts on: a
rule, a system prompt, a CLAUDE.md, an agent file, a skill body. Every
mode treats the instruction as a generator, a short line the reader
expands in its own thinking into the act for every case in a named set,
and proves it by expanding it on cases before it lands.

Write starts from a need or an incident, collects the cases the
instruction must decide, and generates from them. Compress starts from
a list that has grown by accretion and replaces it with a generator
that gives back every listed act. Review traces a draft, or an original
against a rewrite, and reports what the reader must decide on its own
and what the rewrite lost. Each mode ends at the same output: the
generator, the lines kept beside it, an accounting table with one row
per case, and a list of acts the generator adds that nobody wrote, for
approval.

## Reach for it when

- An agent keeps doing something and you want a rule that stops it in every form, not only the one you saw.
- An instruction file has a block of bullets or bans that grows every time someone gets burned.
- Someone rewrote a rule set shorter and you want to know what it dropped before merging.
- A rule reads fine but two sessions act on it differently.

## Pairs with prompt

Writing a whole prompt for an agent or task call, with its scaffold of
role, task, and context, belongs with `prompt`. Deciding what one
instruction inside it covers, and proving it covers that, belongs here.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/writing-agent-instructions/` into `~/.claude/skills/writing-agent-instructions/`.

## Usage

> The agent keeps committing straight to main when I say "save the
> work". Write something for CLAUDE.md that stops it, and not as a
> one-off ban.

> Collapse the git rules block in our CLAUDE.md into one or two rules
> and prove nothing got dropped.

> Someone rewrote our comment rules from eleven bullets to a paragraph.
> Check what it lost before I merge.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`writing-agent-instructions.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/writing-agent-instructions.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
