# check-soundness

Test a synthesis or conclusion for internal contradictions, dropped inputs, and brittleness. Renders a pass/fail verdict with reasons.

## It helps when

- You have pulled several pieces into one plan, summary, or conclusion, and want to know whether they can all be true at once.
- A summary reads smoothly and you suspect it left something out.
- You are about to hand a plan to people who will act on it.

## What it hands back

The claims the synthesis depends on, the inputs it dropped, the contradictions inside it, objections from a skeptic, from each original position, and from a domain expert, what collapses when one piece is removed, where it is brittle, and a pass or fail verdict with reasons and caveats.

Trimmed from a run on a wedding-plan summary that promises an outdoor orchard ceremony, a fully rain-proof venue, no tent, seating by 3 p.m., and a 40-minute walk from a car park that opens at 2:45 ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/check-soundness/orchard-wedding.md)):

> **Contradiction 1: outdoors and fully rain-proof (A and B).**
> "Outdoors in the orchard" and "fully rain-proof" cannot both be true of the same place unless something overhead keeps rain off. The only thing the summary names that would do that is a tent, and C rules it out. Read literally, the plan believes an open-air orchard is rain-proof. […]
>
> **Contradiction 2: the 3 p.m. seating and the 40-minute walk (D and E).**
> The car park opens at 2:45. A guest who arrives at the gate the minute it opens and walks straight to the orchard reaches it at 3:25, which is 25 minutes after the seating deadline. No guest can be seated by 3 p.m. under these two facts.
>
> […]
>
> ### 8. Render verdict
>
> **The plan fails the coherence test.**

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/check-soundness/` into `~/.claude/skills/check-soundness/`.

## Usage

```
/check-soundness <synthesis or conclusion to verify>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`check-soundness.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/check-soundness.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
