# writing-agent-instructions

Write or refine any agent instruction in any agent executable context.
Every route treats the instruction as a generator, a short line the
reader expands in its own thinking into the act for every case in a
named set, and proves it by expanding it on cases before it lands.

Write starts from a need or an incident, collects the cases the
instruction must decide, generates from them, and hands the draft to
Refine. Refine takes an instruction that exists or was just drafted,
prunes what no longer earns its place, replaces a list with a generator
that gives back every listed act, and traces the result; where the ask
is a judgment it reports findings and changes nothing. Both routes end
at the same output: the generator, the lines kept beside it, an
accounting table with one row per case, every pruned line with its
meaning, and a list of acts the generator adds that nobody wrote, for
approval.

## Reach for it when

- An agent keeps doing something and you want an instruction that stops it in every form, not only the one you saw.
- An instruction has grown by accretion and should say the most in the least space without dropping a case.
- Someone rewrote an instruction shorter and you want to know what it dropped before merging.
- An instruction reads fine but two sessions act on it differently.

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

## Sources

- Flix, fixpoint computations on constraints: <https://doc.flix.dev/fixpoints.html>
- Modern Datalog, lecture notes on safety and stratified negation: <https://drops.dagstuhl.de/storage/01oasics/oasics-vol138-rw2024+rw2025/html/OASIcs.RW.2024-2025.7/OASIcs.RW.2024-2025.7.html>

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`writing-agent-instructions.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/writing-agent-instructions.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
