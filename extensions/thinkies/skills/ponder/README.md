# ponder

Exploration skill for problems that need thinking before solving. Assesses a
problem's shape, opens with a technique matched to it, extends the chain of
techniques only while the problem quotably demands more, and converges on a
decision — a leading option, the rule that ranked it, and the evidence that
would flip it.

## When to use this

- A problem stays vague and you can't yet say what you want.
- You're stuck, and more effort on the same approach isn't helping.
- You're choosing between approaches and none clearly wins.
- Something feels complex, or you suspect you're missing something.

## What comes back

The exploration reads as plain prose: the techniques run behind the scenes and are never named. It ends with what the exploration revealed, the options on the table, a ranking with its rule stated, the leading option, the evidence that would flip it, and what stays open.

A run on "My five-person team is productive (we hit every deadline this year) but nobody seems happy", trimmed ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/ponder/productive-but-unhappy.md)):

> - The word "but" in "productive but nobody seems happy" presumes the two facts pull against each other. That presumption carries the most weight, because the whole puzzle is built on it.
>
> […]
>
> 1. Reversed direction. The team hits dates because of the unhappiness: people avoid blame or conflict, so they finish and do not push back. This predicts few disagreements in meetings, risks raised late or not at all, and slips hidden until they are unavoidable.
>
> […]
>
> B leads. Two observations would change the order. If D shows hours clustered around every deadline and the mood tracks them, C moves first, because the first explanation would then be supported by record and not by inference. If all five say, separately and without prompting, that they are content, A leads, and the "seems" was the writer's reading.

Option B is "ask each person alone what the seat is like"; D reads hours and timestamps first; C changes pace or scope; A changes nothing.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/ponder/` into `~/.claude/skills/ponder/`.

## Usage

```
/ponder I have a vague idea for a tool but I can't articulate what it should do yet
/ponder I've been trying to fix this performance issue for hours and nothing works
/ponder Should we use a monorepo or separate repos for our microservices?
/ponder Our deployment pipeline keeps breaking in ways we didn't predict
```

## Records

When loaded from the thinkies Claude Code plugin, ponder saves a record of each run to the plugin store at `${CLAUDE_PLUGIN_DATA}/records/`: the problem, each technique's main finding, each converge item, and what stays open. It copies the record to the Records mirror folder when that optional setting names one. Uninstalling the plugin deletes the store unless you run `claude plugin uninstall thinkies@ai-skills --keep-data`; the mirror stays. Loaded anywhere else, ponder prints the record in its reply as a `jsonl` block for you to keep.

## Sources

- Rasmussen, J. (1985). The role of hierarchical knowledge representation in decisionmaking and system management. *IEEE Transactions on Systems, Man, and Cybernetics*, SMC-15(2), 234–243. [doi:10.1109/TSMC.1985.6313353](https://doi.org/10.1109/TSMC.1985.6313353). Pages below count article pages; the [DTU PDF](https://backend.orbit.dtu.dk/ws/files/158019622/HISMC.PDF) opens with a cover sheet, so its page number is one higher. Art. p. 4 (PDF p. 5) and art. p. 9 (PDF p. 10).
- Tversky, B. (1989). [Parts, partonomies, and taxonomies](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/1989_Tversky_Partspartonomiesandtaxonomies.pdf).

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`ponder.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/ponder.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
