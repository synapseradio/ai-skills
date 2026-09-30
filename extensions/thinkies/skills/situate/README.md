# situate

Place a thing inside the larger system it serves, and read what that system asks of it: name what crosses its edge, what feeds it, what takes what it produces, and what it serves, and take the smallest system holding all three as its container; name the limits, rhythms, expectations, and competitors for resources that the container imposes; repeat one level up until the thing's purpose is plain or the next level would change nothing; then state what shifts about the thing once it is seen in place, whether its purpose, its priorities, or what counts as success for it.

## Use it when

- Something works fine on its own terms and still seems to be failing at something.
- You're judging a part (a team, a feature, a habit) and the judgment keeps coming out different depending on who you ask.
- You can't tell what success looks like for a thing until you know what it's for.

## A run, trimmed

The answer arrives as four questions about the thing, each answered in turn, with what the input couldn't settle marked open. From a run on a single traffic cone left on a quiet residential street for three weeks, placed by nobody knows who ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/situate/lonely-traffic-cone.md)):

> Expectations: residents expect that a marker on their street either has a reason or gets removed by whoever owns it. Each resident can also assume that a neighbor, or the authority, has already dealt with it. That assumption is how one cone can stand for three weeks.
>
> […]
>
> Its purpose shifts. Seen alone, the cone is a warning about a hazard. Seen in place, after three weeks with no crew and no owner, it is a test of the street's routing: a small, harmless probe of whether anyone in the system takes responsibility for an unowned object.
>
> […]
>
> What counts as success shifts. Alone, success is that a driver steers around it. In place, success is that the cone gets resolved: either an owner explains it, or the authority or a neighbor removes it, or someone confirms the reason it stands.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/situate/` into `~/.claude/skills/situate/`.

## Usage

```
/situate <thing to place>
```

## Sources

- Rasmussen, J. (1985). The role of hierarchical knowledge representation in decisionmaking and system management. *IEEE Transactions on Systems, Man, and Cybernetics*, SMC-15(2), 234–243. [doi:10.1109/TSMC.1985.6313353](https://doi.org/10.1109/TSMC.1985.6313353). Pages below count article pages; the [DTU PDF](https://backend.orbit.dtu.dk/ws/files/158019622/HISMC.PDF) opens with a cover sheet, so its page number is one higher.
    - Art. p. 4 (PDF p. 5): "why it is made".
    - Art. p. 2 (PDF p. 3): "span of attention".
    - Art. p. 9 (PDF p. 10): Rubin's shutter.
- Vallacher, R. R., & Wegner, D. M. (1987). What do people think they're doing? [doi:10.1037/0033-295X.94.1.3](https://doi.org/10.1037/0033-295X.94.1.3).

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`situate.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/situate.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
