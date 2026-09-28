# connect-ideas

Test how two ideas relate, or find a distant match for one idea, and keep only the relations the evidence supports: restate each side as its entities, relations, constraints, and goal; when only one side was given, search distant fields for a solved problem with the same structure and take it as the second side; test each kind of relation in turn (analogy, cause and effect, means and end, part and whole, shared class, shared constraint or resource, tension) with the evidence for and against; keep the relations the evidence supports, listing for an analogy what maps, what needs adapting, and what breaks; and name the act each surviving relation opens and the principle that makes it work.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/connect-ideas/` into `~/.claude/skills/connect-ideas/`.

## Usage

```
/connect-ideas <subject>
```

## Records

When loaded from the thinkies Claude Code plugin, the skill saves a record of each run to the plugin store at `${CLAUDE_PLUGIN_DATA}/records/`, and copies it to the Records mirror folder when that optional setting names one. Uninstalling the plugin deletes the store unless you run `claude plugin uninstall thinkies@ai-skills --keep-data`. Loaded anywhere else, the skill prints the record in its reply for you to keep.

## Sources

- Winston, M. E., Chaffin, R., & Herrmann, D. (1987). A taxonomy of part-whole relations. *Cognitive Science*, 11(4), 417–444. [doi:10.1207/s15516709cog1104_2](https://doi.org/10.1207/s15516709cog1104_2).
- Rasmussen, J. (1985). The role of hierarchical knowledge representation in decisionmaking and system management. *IEEE Transactions on Systems, Man, and Cybernetics*, SMC-15(2), 234–243. [doi:10.1109/TSMC.1985.6313353](https://doi.org/10.1109/TSMC.1985.6313353). Pages below count article pages; the [DTU PDF](https://backend.orbit.dtu.dk/ws/files/158019622/HISMC.PDF) opens with a cover sheet, so its page number is one higher. Art. p. 4 (PDF p. 5).
- Tversky, B. (1989). [Parts, partonomies, and taxonomies](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/1989_Tversky_Partspartonomiesandtaxonomies.pdf).

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`connect-ideas.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/connect-ideas.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
