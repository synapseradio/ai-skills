# trace-logic

Follow reasoning step-by-step. Breaks an argument into atomic inferences, classifies each by type (deduction, induction, abduction, analogy), and surfaces gaps and leaps.

## Reach for it when

- An argument feels persuasive and you can't say which step you'd push on.
- You need to know which premise, if it fell, would take the conclusion with it.
- Someone offers several reasons at once, and you want to know whether they stand alone or lean on each other.

## You get back

The argument as numbered steps with the unstated ones written in, a verdict on each link, the type of each inference and whether it fits, the gaps and leaps by name, a map of which conclusions depend on which premises, and where the chain is strongest, where weakest, and what would repair it.

Trimmed from a run on a seven-year-old's case: "Bedtime is for getting tired. I'm not tired. Grown-ups don't have bedtime and they're fine. Also I'll be tired tomorrow anyway because it's school. So bedtime should be abolished." ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/trace-logic/abolish-bedtime.md)):

> 1. (implicit) Tiredness tomorrow is fixed and does not depend on what happens tonight ("anyway").
>
> […]
>
> **Circularity.** None found. The argument's premises do not depend on its conclusion. It does, however, contain a self-undermining structure: premise D, offered as a reason to abolish bedtime, describes a cost (tomorrow's tiredness) that bedtime exists to reduce. The argument uses a reason for bedtime as a reason against it.
>
> […]
>
> - For step 14: shrink the conclusion to what the premises support, such as "I should get to stay up until I feel tired, on trial, for a week."

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/trace-logic/` into `~/.claude/skills/trace-logic/`.

## Usage

```
/trace-logic <argument or reasoning to trace>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`trace-logic.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/trace-logic.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
