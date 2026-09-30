# calibrate-confidence

Match certainty to evidence strength. Names confidence explicitly, inventories evidence, and checks for over- and under-confidence before communicating uncertainty.

## Reach for it when

- A claim is stated flatly, and you cannot tell how much of it the evidence carries.
- You are about to tell someone how sure you are, and want the number to mean something.
- One part of a claim is solid and another is a guess, and the sentence treats them the same.

## What it hands back

The claim split into parts that deserve different confidence, a named level for each (such as "moderately confident, 60–80%, because…"), an inventory of what that confidence rests on, checks for overconfidence and underconfidence, a betting test with what would move the level, and a rewritten statement that shows where certainty ends and speculation begins.

A run on "The new espresso machine is why the team ships faster", where the team closed 30% more tickets in the three weeks since it arrived and a new hire started the same month, trimmed ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/calibrate-confidence/espresso-velocity.md)):

> - Part A, that the count rose 30%: moderately confident (60-80%), because it is a reported figure I have not seen the counting behind.
> - Part A read as "the team shipped faster": uncertain (40-60%). Tickets closed is a count of closures, and closures can rise while shipped value stays flat (smaller tickets, split tickets, a backlog cleanup).
> - Part B, that the machine is why: low confidence (below 40%). […]
>
> […]
>
> What I would say in place of the original sentence:
>
> > The team closed about 30% more tickets in the three weeks since the machine arrived, if the figure holds up. A new hire also started that month, and the machine and the hire cannot be told apart from this data. I would put the machine as the main cause at roughly 5-10%, and as a small contributor somewhat higher. The claim that it is why the team ships faster is not supported yet.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/calibrate-confidence/` into `~/.claude/skills/calibrate-confidence/`.

## Usage

```
/calibrate-confidence <claim or assertion to calibrate>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`calibrate-confidence.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/calibrate-confidence.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
