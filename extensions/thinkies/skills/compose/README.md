# compose

Join parts into a whole that does what none of them does alone, listing what each part does on its own, naming what passes between the parts that touch, stating the property only the arrangement has, removing each part in turn to test whether that property needs it, naming what the property needs that no part supplies, and stating the whole in one sentence.

## Call on it when

- You hold a pile of half-ideas and suspect they add up to something.
- You want to know which parts carry their weight and which only ride along.
- A design works on paper and you want to find the piece nobody has supplied yet.

## What a run looks like

A question set naming your subject, then its answers: what each part does alone and what it still needs, what passes between each touching pair, the property only the arrangement has, which parts that property needs, the missing parts, and the whole in one sentence. Where the parts turn out to be a list rather than a whole, it says so and stops.

Trimmed from a run on six half-ideas for a family board-game night nobody quits in tears ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/compose/board-game-night.md)):

> 1. What does the arrangement of the six ideas do for a board-game night that no single idea does?
>
>    It gives every outcome a soft landing. A loser is cushioned by a team, a snack break, or a chance at the prize; a winner is restrained by the jar; and one game in the night has no loser at all. […]
>
> 2. Which of the six ideas does that property need, and which one does the night work without when removed?
>
> […]
>
> - The youngest picks the first game: remove it and the property does not change. A loss lands the same way whoever chose the game. This idea does not belong to this whole. It belongs to a different one, about who gets a say, and it can stay in the night as a courtesy that does none of this night's work.
>
> 1. What does that property need in a board-game night that none of the six ideas supplies?
>
> […]
>
> - A way to leave without quitting: a step-out any player may take at any time, with no explanation owed and no penalty. The snack break covers one moment on a clock; a tearful player needs an exit at any moment.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/compose/` into `~/.claude/skills/compose/`.

## Usage

```
/compose <subject>
```

## Sources

- Rasmussen, J. (1985). The role of hierarchical knowledge representation in decisionmaking and system management. *IEEE Transactions on Systems, Man, and Cybernetics*, SMC-15(2), 234–243. [doi:10.1109/TSMC.1985.6313353](https://doi.org/10.1109/TSMC.1985.6313353). Pages below count article pages; the [DTU PDF](https://backend.orbit.dtu.dk/ws/files/158019622/HISMC.PDF) opens with a cover sheet, so its page number is one higher. Art. p. 4 (PDF p. 5): "autonomous functional units at one level before they can be connected". Art. p. 9 (PDF p. 10): "much more difficult, this being a synthesis".
- Besta et al. (2023). Graph of Thoughts. [arXiv:2308.09687](https://arxiv.org/abs/2308.09687).

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`compose.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/compose.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
