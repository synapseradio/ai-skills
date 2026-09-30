# integrity

Verify an artifact's structural integrity by aligning claims with evidence. Applies five lenses — inventory, dissection, pattern, calibration, resolution — and produces a verification summary.

## Call on it when

- A text makes confident claims and you want to know which ones its evidence actually carries.
- You are about to publish, send or rely on something and want its wording matched to its support.
- You want an answer you just received checked the same way (pass "current response").

## You get back

Every claim in the text, stated and hidden; the chain of support behind each one; the weak patterns it leans on; the outside evidence it could reach, ranked; each claim reworded to what its support allows; and a verification summary in three parts: verified, needing attention, and still uncertain.

Trimmed from a run on a garden-centre leaflet promising that planting by the moon doubles your tomato yield ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/integrity/moon-planting-leaflet.md)):

> - Claim 2 rests on long use, and long use shows a practice persisted, not that it works.
>
> […]
>
> - "Planting by the moon calendar doubles your tomato yield" becomes "Some gardeners plant by the moon calendar." That is all the leaflet supports.
> - "Gardeners have known this for centuries" becomes "Gardeners have planted by the moon for centuries."
> - "Our customers report bumper harvests" becomes "Some of our customers report good harvests," and would need a count and a comparison to say more.
> - "Buy the 2027 Moon Planner" stands as a sale, with no claim attached.
>
> […]
>
> - I read the review's abstract as returned by search, not the full paper, so what it did and did not test on tomatoes specifically is unverified by me.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/integrity/` into `~/.claude/skills/integrity/`.

## Usage

```
/integrity <artifact or "current response">
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`integrity.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/integrity.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
