# ponder

Exploration skill for problems that need thinking before solving. Assesses a
problem's shape, opens with a technique matched to it, extends the chain of
techniques only while the problem quotably demands more, and converges on a
decision — a leading option, the rule that ranked it, and the evidence that
would flip it.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/ponder/` into `~/.claude/skills/ponder/`.

## Usage

```
/ponder I have a vague idea for a tool but I can't articulate what it should do yet
/ponder I've been trying to fix this performance issue for hours and nothing works
/ponder Should we use a monorepo or separate repos for our microservices?
/ponder Our deployment pipeline keeps breaking in ways we didn't predict
```

## How it works

1. **Assess** — detects the problem's shape (vague, stuck, fork, complex, or blindspot)
2. **Open** — runs an opening technique that repairs the shape's deficit
3. **Extend** — after each technique, a checklist over the output decides whether the chain grows; every extension quotes the sentence that demands it, a chain that stops changing the picture stops, and five techniques bound the whole
4. **Converge** — ends with the options on the table, a ranking with its rule stated, the leading option, and the evidence that would flip it

A chain runs two techniques at minimum and five at most. The output reads as
natural, flowing exploration in clear, concise prose; technique names and
chain mechanics stay behind the curtain.

## When to use this

Ponder fits problems that need thinking before solving: when a problem stays
vague, when you're stuck, when you're choosing between approaches, when
something feels complex, or when you suspect you're missing something.

## Design decisions

Maintainer notes — what the author fixed, what stays open, and the sign that
a frozen decision needs revisiting:

- **Shape tie-break** (most specific signal wins) — fixed. Revisit if
  misassessment recurs on real inputs.
- **Technique concealment** — fixed. Revisit if callers report the
  exploration feels arbitrary or untrustworthy without a visible method.
- **Extension checklist** (quote-to-extend, fixpoint stop) — fixed. Collapse
  to the fixpoint rule plus the cap alone if a weak executor extends the
  chain on unquotable grounds.
- **Chain cap of five** — a guess, open. Calibrate against real runs.
- **Checks** — no eval harness exists yet; every check above runs as a manual
  fixture run.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`ponder.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/ponder.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
