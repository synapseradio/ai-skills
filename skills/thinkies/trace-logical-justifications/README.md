# trace-logical-justifications

Trace justification chains backward until reaching bedrock — direct observation, definitional truth, logical axiom — or finding floating assumptions.

## Use it on

- A rule or a principle stated as obvious ("we must never…", "always…").
- A claim whose confidence seems larger than anything said in its favour.
- Your own position, before you defend it to someone who will ask "why?" one more time than you have.

## What comes back

The claims the statement needs, each with its support named (another claim, an observation, a definition, an axiom, or nothing visible), each chain followed down to where it ends, the claims left floating, and a judgment on whether the structure holds, including which weaker version it does support.

Trimmed from a run on "We must never throw away a working pen." ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/trace-logical-justifications/never-throw-away-a-pen.md)):

> - **C1 -> C3 -> C4 -> absence.** The step from "this is waste" to "waste is wrong" has no warrant. This is the moral premise the whole argument turns on.
>
> […]
>
> Testing C8 with cases shows why it matters. A pen that is technically working but leaks over the pocket it sits in. A person who owns four hundred pens and no drawer left to keep them in.
>
> […]
>
> The argument is valid for "we should usually be reluctant to throw away a working pen" and unsupported for the sentence as written.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/trace-logical-justifications/` into `~/.claude/skills/trace-logical-justifications/`.

## Usage

```
/trace-logical-justifications <claim to trace justifications for>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`trace-logical-justifications.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/trace-logical-justifications.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
