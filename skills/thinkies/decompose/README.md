# decompose

Break a whole into parts at its natural joints: name the whole's purpose and boundary, choose one axis per level and the relations that fit it, cut where boundaries already exist, check that the parts cover the whole with no gaps or overlaps, and recurse on each part until it can be acted on or checked directly.

## Try it when

- A job is too big to start and every list you write of it feels arbitrary.
- Two people own the same piece, or nobody owns a piece everyone assumed was covered.
- You need to know how far to break something down before handing out the parts.

## You get back

A question set about your subject, then its answers: the purpose and boundary, the axis chosen for each level and why, the parts with what each exchanges with the rest, a check for gaps and overlaps that names what it moved, and where cutting stops for each part. Where the purpose is missing, it says which cuts depend on it.

From a run on the bare instruction "Run a village fête" ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/decompose/village-fete.md)), the coverage check catching two holes in the first cut:

> - Gap: the day itself. Six parts prepare for it, and none holds the running of the day (opening, handling problems, closing). Added as a seventh part, **The day**, whose interface is the roster and the site plan.
> - Gap: clearing up and closing out (litter, returning borrowed equipment, thank-yous, banking, the accounts). Added as an eighth part, **Afterwards**.
>
> […]
>
> - **Stops before a third pass:** cutting a stall kind into its individual stalls, or a zone into its objects, grows the interfaces more than it shrinks the parts. Forty stalls share the same table, the same pitch rules, and the same float, so forty separate parts would mean forty near-identical interfaces to keep in step.

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
