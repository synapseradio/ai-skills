# ask-questions

A directed thought process for making the right next move with the user — one genuinely good question, or a deliberate non-question — in the moment, in any conversation or domain. Each invocation returns that single next move, given the exchange so far. Good questions serve one inquiry: name the question the inquiry exists to answer (the driving question), and every candidate question becomes a rung that must earn its place on the ladder toward it.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/ask-questions/` into `~/.claude/skills/ask-questions/`.

## Usage

```
/ask-questions I need to ask my user about their deploy setup but I'm not sure what to ask
/ask-questions My first question fell flat — help me ask it better
/ask-questions They just answered "it depends on the team" — what do I ask next?
```

## Records

When loaded from the thinkies Claude Code plugin, the skill saves a record of each run to the plugin store at `${CLAUDE_PLUGIN_DATA}/records/`, and copies it to the Records mirror folder when that optional setting names one. Uninstalling the plugin deletes the store unless you run `claude plugin uninstall thinkies@ai-skills --keep-data`. Loaded anywhere else, the skill prints the record in its reply for you to keep.

## How it works

The core holds what every question passes through: the driving question; the two-gate rung test (would a complete answer at least partly answer the driving question — and would different answers change your next move?); the four clarity laws (one idea per question, plain words, no smuggled premise, a real question rather than a statement wearing a question mark); the non-question moves (silence, restatement, plain statement, asking nothing); the terminal states an inquiry may legitimately end in; what each route hands back as the next move; and guidance on who gathers the context and who shapes the words.

Everything else routes by the gap you feel, through ten reference files:

| Gap | Reference |
|-----|-----------|
| Building or growing the ladder toward the driving question | [ladder](./references/ladder.md) |
| The value under a stated preference | [laddering](./references/laddering.md) |
| The data under a conclusion, belief, or plan | [climb-down](./references/climb-down.md) |
| A claim that's shaky in a specific way | [probe](./references/probe.md) |
| The shape and timing of a whole sequence | [sequence-shapes](./references/sequence-shapes.md) |
| Which candidate question comes next | [ordering](./references/ordering.md) |
| A question that treats the thing as simpler than it is | [pretense](./references/pretense.md) |
| What the inquiry accepts without justification | [grants](./references/grants.md) |
| Carrying a ladder into a new domain | [transfer](./references/transfer.md) |
| The driving question itself may be the wrong one | [driving-question](./references/driving-question.md) |

Each reference opens with a diagnostic question, gives instructions, poses a Questions section to work through, and closes with quality criteria.

## When to use this

Reach for it whenever you're about to ask the user something and the question should land well — including when you're about to use the `AskUserQuestion` tool. Use it when you're unsure what to ask, when a first question fell flat, when an answer just came back and you need what sits beneath it, or when the user's tone or messages signal you've drifted from what they need. It also covers gathering the context before you can ask at all, and judging when the better move is not a question — a restatement, a plain statement, silence, or asking nothing.

## Design notes for maintainers

Decisions the skill fixes, which every session inherits: the next-single-move output contract per route; the two-gate rung test; the four terminal states; the ten-reference routing grain. Decisions each session makes fresh: the stance and disclosure policy for a sequence, and every wording choice.

Signs a fixed decision needs revisiting: a harness that carries state across fork invocations ages the live-mode wording in laddering; routing rows that go unused suggest the grain is wrong; recurring executor confusion inside one reference means a decision there no longer closes.

Check coverage: the evals exercise routing and question phrasing; the non-question moves, terminal states, and audit deliverables lack eval cases.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`ask-questions.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/ask-questions.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
