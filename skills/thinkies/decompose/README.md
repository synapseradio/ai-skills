# decompose

Break a whole into parts at its natural joints: name the whole's purpose and boundary, choose one axis per level and the relations that fit it, cut where boundaries already exist, check that the parts cover the whole with no gaps or overlaps, and recurse on each part until it can be acted on or checked directly.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/decompose/` into `~/.claude/skills/decompose/`.

## Usage

```
/decompose <thing to examine>
```

## Sources

- Winston, M. E., Chaffin, R., & Herrmann, D. (1987). A taxonomy of part-whole relations. *Cognitive Science*, 11(4), 417–444. [doi:10.1207/s15516709cog1104_2](https://doi.org/10.1207/s15516709cog1104_2). Backs step 2's relation types and step 5's rule that part-of does not chain across types.
- Rasmussen, J. (1985). The role of hierarchical knowledge representation in decisionmaking and system management. *IEEE Transactions on Systems, Man, and Cybernetics*, SMC-15(2), 234–243. [doi:10.1109/TSMC.1985.6313353](https://doi.org/10.1109/TSMC.1985.6313353). Pages below count article pages; the [DTU PDF](https://backend.orbit.dtu.dk/ws/files/158019622/HISMC.PDF) opens with a cover sheet, so its page number is one higher. Art. p. 2 (PDF p. 3): whole/part and abstract/concrete are "conceptually separate".
- Zhou et al. (2022). Least-to-most prompting. [arXiv:2205.10625](https://arxiv.org/abs/2205.10625).

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`decompose.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/decompose.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
