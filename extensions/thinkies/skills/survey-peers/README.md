# survey-peers

Map what else fills the same role at the same level of detail, and where the gaps between them lie: name the role the subject fills and the grain it sits at, list the peers that fill that role at that grain (including ones from outside the current domain), name the one property that most separates each peer from the subject, arrange the peers along the one or two differences that separate them most, name the empty positions in that arrangement and whether each is empty by accident or for a reason, and report where the subject sits and its nearest neighbours.

## Use it when

- You know your own option well and have never mapped the alternatives that do the same job.
- The obvious competitors all look alike, and you suspect the interesting ones come from another field.
- You're looking for an empty spot: a combination nobody has tried, or one nobody can.

## What comes back

Six questions about the subject, answered in turn. The answers give the role and its grain, the peers, the one property that sets each apart, a grid along the two differences that matter most, the empty cells with a reason for each, and where the subject sits.

A run on "Everything that does the job of an alarm clock.", trimmed ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/survey-peers/alarm-clock-peers.md)):

> - Knocker-upper: the waker stays until the sleeper shows they are awake.
>
> […]
>
> Two differences separate them most. The first is who keeps the time: a device the sleeper set, another party, or the world with no time set. The second is which sense carries the signal: sound, light, touch (including warmth and pressure), or smell.
>
> […]
>
> - World keeps the time, smell carries the signal. It is empty for a reason: no natural scent turns up at a fixed hour, so smell carries no clock of its own.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/survey-peers/` into `~/.claude/skills/survey-peers/`.

## Usage

```
/survey-peers <subject>
```

## Sources

- Rasmussen, J. (1985). The role of hierarchical knowledge representation in decisionmaking and system management. *IEEE Transactions on Systems, Man, and Cybernetics*, SMC-15(2), 234–243. [doi:10.1109/TSMC.1985.6313353](https://doi.org/10.1109/TSMC.1985.6313353). Pages below count article pages; the [DTU PDF](https://backend.orbit.dtu.dk/ws/files/158019622/HISMC.PDF) opens with a cover sheet, so its page number is one higher. Art. p. 3 (PDF p. 4): "several physical arrangements", "serve several purposes".
- Yao et al. (2023). Tree of Thoughts. [arXiv:2305.10601](https://arxiv.org/abs/2305.10601).

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`survey-peers.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/survey-peers.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
