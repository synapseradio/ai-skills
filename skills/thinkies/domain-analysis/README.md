# domain-analysis

Build a lasting model of a real system, feature, or system of systems, an agentic system of user, orchestrator, delegates, tools, and harness included: settle the scope and the system's grains, place nodes on five levels (functional purpose, abstract function, generalized function, physical function, physical form), link each node as a means to the nodes above it and as a part of the node one grain coarser, record every node that serves nothing or that nothing carries out as a gap, name who acts on and sees each node, then show the model as a grid with node, link, and actor lists, citing code paths when the domain is code. The model is saved as a record, so a later session reloads it and extends it.

## It helps when

- You are about to change how a system works and want to see what each piece is for before touching it.
- Things go wrong and nobody notices, and you suspect nobody is looking at the right thing.
- You will come back to the same system later and want the model waiting for you.

## A run, trimmed

A grid running from why the system exists down to what it is made of, with every node marked as given or assumed, the links between them, and who acts on and sees each one. Under the grid come the results: work nothing carries out, pieces with no fallback, and goals no one watches. Open questions come last.

Excerpts from a run on a neighbourhood tool library run out of a garage, with a paper ledger, a group chat, and one much-loved pressure washer ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/domain-analysis/garage-tool-library.md)). Most of its nodes are marked "assumed", because the description named little beyond the garage, the tools, and the two records:

> - The values value-1, value-2, value-3, and value-4 and the purpose purpose-2 are seen by no actor. The only value anyone sees is value-5, the washer wait, and only the borrower sees it. Lost or broken tools, fairness across households, incidents, and volunteer hours have no one looking at them, so nothing in the model would tell the volunteers that any of them is going wrong.
>
> […]
>
> - function-8 (acquire and replace tools) is a gap: it serves value-1 and no process carries it out. Because the library's stock only shrinks through loss and wear, this gap sits under the very value (value-1) that nobody watches.

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
