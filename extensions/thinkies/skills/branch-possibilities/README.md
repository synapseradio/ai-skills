# branch-possibilities

Generate fundamentally divergent directions from one starting point — genuinely different paths, not variations on a theme — then map where they split and whether they could recombine.

## Call on it when

- Every option on the table is a variation of the first idea.
- You are at a fork early enough that the choice of direction matters more than the details.
- You want to know which decision closes off the others before you make it.

## A run, trimmed

The starting point and the decision that could change, several fundamentally different directions from it, what each would look like in practice with its own trade-offs, and a map of where the paths split and which ones can later combine.

Excerpts from a run on a small coastal town that inherits a decommissioned lighthouse and one million rubber ducks ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/branch-possibilities/lighthouse-and-ducks.md)):

> 1. **Destination.** The inheritance is an attraction. The lighthouse becomes the venue and the ducks become the exhibit.
> 2. **Liquidation.** The inheritance is money. The town sells or leases both assets and takes the proceeds.
> 3. **Instrument.** The inheritance is equipment. The ducks are floating, numbered, cheap drifters, and the lighthouse is a fixed observation post.
>
> […]
>
> Where the paths split:
>
> - **Keep or release.** Branches 1, 3, and 4 keep ownership of the ducks. Branches 2, 5, and 6 give it up. This is the first split and the hardest to reverse. A sold or scrapped duck cannot come back.
>
> […]
>
> Reading the map: the town's first real decision is whether to keep the ducks. Everything about the tower can be settled later, and most of the branches that keep the ducks combine well. The branches that release the ducks are the ones that close off the others.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/branch-possibilities/` into `~/.claude/skills/branch-possibilities/`.

## Usage

```
/branch-possibilities <decision or starting point>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`branch-possibilities.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/branch-possibilities.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
