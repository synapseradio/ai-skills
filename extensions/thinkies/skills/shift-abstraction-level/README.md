# shift-abstraction-level

Find the level of abstraction to act at: locate where a subject is stated, restate it a few rungs above and below, and choose the rung with the least detail that still supports the act.

## It helps when

- A task arrives too vague to start ("improve onboarding", "fix the kitchen") or too specific to question ("change this one setting").
- A discussion keeps sliding between why something matters and which screw to turn.
- You've fixed the same thing twice and suspect you're fixing it at the wrong level.

## What you walk away with

A set of questions about the subject, then their answers: the act it must support and the level it's stated at, a ladder of restatements above and below, what each rung lets you do and what it hides, and the rung to act at. Anything the answer can't settle from what you gave it is marked open.

Here it is on "Fix the office kitchen.", cut down ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/shift-abstraction-level/fix-the-office-kitchen.md)):

> - Which-fault rung: The dishwasher no longer drains, the fridge is warm, the sink drips, or the bin overflows because nobody owns emptying it.
> - Which-instance rung: The dishwasher on the left drains slowly because its filter is clogged, and a screwdriver and ten minutes clear it.
>
> […]
>
> If the fault is a habit, such as a bin nobody empties, act at the rung above the machine ("who owns this task"), because a repair at the instance rung, one emptied bin, undoes itself by Friday.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/shift-abstraction-level/` into `~/.claude/skills/shift-abstraction-level/`.

## Usage

```
/shift-abstraction-level <statement or problem>
```

## Sources

- Rasmussen, J. (1985). The role of hierarchical knowledge representation in decisionmaking and system management. *IEEE Transactions on Systems, Man, and Cybernetics*, SMC-15(2), 234–243. [doi:10.1109/TSMC.1985.6313353](https://doi.org/10.1109/TSMC.1985.6313353). Pages below count article pages; the [DTU PDF](https://backend.orbit.dtu.dk/ws/files/158019622/HISMC.PDF) opens with a cover sheet, so its page number is one higher. Art. p. 4 (PDF p. 5): "prioritize by selecting the level of abstraction"; faults are explained "bottom-up" and proper function "top-down". Art. p. 2 (PDF p. 3): "less resolution".
- Vallacher, R. R., & Wegner, D. M. (1987). What do people think they're doing? Action identification and human behavior. *Psychological Review*, 94(1), 3–15. [doi:10.1037/0033-295X.94.1.3](https://doi.org/10.1037/0033-295X.94.1.3).
- Trope, Y., & Liberman, N. (2010). Construal-level theory of psychological distance. *Psychological Review*, 117(2), 440–463. [doi:10.1037/a0018963](https://doi.org/10.1037/a0018963).
- Eriksen, C. W., & St. James, J. D. (1986). Visual attention within and around the field of focal attention: A zoom lens model. *Perception & Psychophysics*, 40(4), 225–240. [doi:10.3758/BF03211502](https://doi.org/10.3758/BF03211502).

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`shift-abstraction-level.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/shift-abstraction-level.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
