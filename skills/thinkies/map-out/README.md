# map-out

Find where a subject sits and the level to act at, by moving along its axes: parts and wholes, purposes and means, kinds and cases, and peers at the same level. The skill reads what the thinking lacks and opens with the matching move: choose a level to act at, place the subject in the system it serves, cut it into parts, assemble parts into a whole, ground an abstraction in concrete cases, name the class a case belongs to, or survey the peers that do the same job. After each move it says where the subject now sits on each axis the move touched, and adds another move only when a sentence of the output so far calls for one, stopping when a move adds nothing new or after five moves. It closes with the subject's position, the level to act at and what acting there makes possible, what each move changed, and what stays open.

## Reach for it when

- An argument goes in circles because each side is talking about a different level of the same thing.
- You don't know whether to zoom in, zoom out, or look sideways at alternatives.
- You need to decide what to act on, and the subject is too big or too small to act on as it stands.

## What you walk away with

A short run of moves in prose, each ending with where the subject now sits, then a summary: the whole it belongs to, its purpose, its class, its nearest peers, the level to act at and what acting there makes possible, what each move changed, and what stays open.

On "Pineapple on pizza." ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/map-out/pineapple-on-pizza.md)), trimmed:

> In a shared order the question stops being "is this good" and becomes "is this tolerable to the whole table".
>
> […]
>
> **The level to act at.** The shared-order level, for a decision. Acting there makes a half-and-half order, or a small second pie, possible without settling what a pizza may contain. To explain a soggy slice, go down to the bake and the fruit's form instead.
>
> **What each move changed.**
>
> - Finding the container moved the question from "is it good" to "is it tolerable to the table".
> - Cutting the pie into fruit, base, bake, and eater made the argument testable in three of four parts and showed the fourth lives in the eater.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/map-out/` into `~/.claude/skills/map-out/`.

## Usage

```
/map-out <subject>
```

## Records

When loaded from the thinkies Claude Code plugin, the skill saves a record of each run to the plugin store at `${CLAUDE_PLUGIN_DATA}/records/`, and copies it to the Records mirror folder when that optional setting names one. Uninstalling the plugin deletes the store unless you run `claude plugin uninstall thinkies@ai-skills --keep-data`. Loaded anywhere else, the skill prints the record in its reply for you to keep.

## Sources

- Rasmussen, J. (1985). The role of hierarchical knowledge representation in decisionmaking and system management. *IEEE Transactions on Systems, Man, and Cybernetics*, SMC-15(2), 234–243. [doi:10.1109/TSMC.1985.6313353](https://doi.org/10.1109/TSMC.1985.6313353). Pages below count article pages; the [DTU PDF](https://backend.orbit.dtu.dk/ws/files/158019622/HISMC.PDF) opens with a cover sheet, so its page number is one higher. Art. pp. 2, 4, 9 (PDF pp. 3, 5, 10).
- Tversky, B. (1989). [Parts, partonomies, and taxonomies](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/1989_Tversky_Partspartonomiesandtaxonomies.pdf).
- [Work domain analysis](https://en.wikipedia.org/wiki/Work_domain_analysis), Wikipedia.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`map-out.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/map-out.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
