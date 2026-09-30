# audit-chain-of-thought

Tag reasoning steps by inference type (deductive, inductive, abductive). Assesses soundness step by step and surfaces the weakest links.

## Worth running when

- An argument reaches a big conclusion from a few observations, and you cannot say which step does the lifting.
- You want to check your own reasoning before you hand it to someone.
- A chain sounds airtight and you suspect it skips steps.

## What you'll get

The chain written out with its hidden steps made explicit, each step tagged by type: deductive (follows necessarily), inductive (generalizes from cases), or abductive (picks the best explanation). Then a soundness check on each step, the weakest links, and the chain's overall shape.

A run on a neighbour's argument that a missing garden gnome proves the squirrels are organised, trimmed ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/audit-chain-of-thought/organised-squirrels.md)):

> **Step 5, deductive in form, unsound premise.** With "selective means planned" stated, the conclusion follows, so the form is valid. The premise is the problem. Selection does not require a plan. An animal that goes for the one item that is portable, or shiny, or smells of something, is selecting without planning. A word is doing double duty: "selective" in step 4 means the outcome looked chosen, and "planned" in step 5 means someone worked toward it in advance. Nothing in the evidence reaches from the first to the second.
>
> […]
>
> 1. **A pull between steps 3 and 4.** Step 3 says squirrels are suspects because they bury things, which is what an indiscriminate habit would explain. Steps 4 and 5 then say the taker was selective and planned. Selectivity and planning, if granted, fit a person who wanted a gnome at least as well as they fit a squirrel. So the later steps, if they held, would lower the case for squirrels rather than raise it.
>
> […]
>
> No step is deductive with true premises. The chain is mostly abductive, and its most confident-sounding step, the deductive step 5, is where it is weakest.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/audit-chain-of-thought/` into `~/.claude/skills/audit-chain-of-thought/`.

## Usage

```
/audit-chain-of-thought <reasoning chain to audit>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`audit-chain-of-thought.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/audit-chain-of-thought.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
