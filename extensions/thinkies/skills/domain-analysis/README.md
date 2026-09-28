# domain-analysis

Build a lasting model of a real system, feature, or system of systems, an agentic system of user, orchestrator, delegates, tools, and harness included: settle the scope and the system's grains, place nodes on five levels (functional purpose, abstract function, generalized function, physical function, physical form), link each node as a means to the nodes above it and as a part of the node one grain coarser, record every node that serves nothing or that nothing carries out as a gap, name who acts on and sees each node, then show the model as a grid with node, link, and actor lists, citing code paths when the domain is code. The model is saved as a record, so a later session reloads it and extends it.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/domain-analysis/` into `~/.claude/skills/domain-analysis/`.

## Usage

```
/domain-analysis <system>
```

## Records

Loaded from the thinkies Claude Code plugin, the skill saves each run as a JSON Lines file in the plugin's store, `${CLAUDE_PLUGIN_DATA}/records/`, and resumes the latest record for the same system on the next run. Set the plugin's optional **Records mirror folder** to keep a second copy in a folder you choose. Claude Code deletes the store when the plugin is uninstalled; pass `--keep-data` to `claude plugin uninstall` to keep it. Anywhere else, the skill prints the record at the end of the reply as a `jsonl` block for you to save.

## Sources

- Rasmussen, J. (1985). The role of hierarchical knowledge representation in decisionmaking and system management. *IEEE Transactions on Systems, Man, and Cybernetics*, SMC-15(2), 234–243. [doi:10.1109/TSMC.1985.6313353](https://doi.org/10.1109/TSMC.1985.6313353). Open copy: [DTU PDF](https://backend.orbit.dtu.dk/ws/files/158019622/HISMC.PDF).
- [Work domain analysis](https://en.wikipedia.org/wiki/Work_domain_analysis), Wikipedia: the five level names.
- Vicente, K. J. (1999). *Cognitive Work Analysis: Toward Safe, Productive, and Healthy Computer-Based Work*. [doi:10.1201/b12457](https://doi.org/10.1201/b12457). The actor layer draws on its fourth phase, social organisational analysis, which the book left "largely unspecified" ([Ashoori et al. 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4066876/)).

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`domain-analysis.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/domain-analysis.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
