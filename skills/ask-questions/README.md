# ask-questions

A directed thought process for asking one genuinely good question — or a composed set of them — in the moment, in any conversation or domain. Situate the question in its context, name the gap that only the other person can close, pick the move that fits, then test the draft against four clarity laws and place it in time.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/ask-questions/` into `~/.claude/skills/ask-questions/`.

## Usage

```
/ask-questions I need to ask my user about their deploy setup but I'm not sure what to ask
/ask-questions My first question fell flat — help me ask it better
/ask-questions Read this spec and generate the questions I should be asking
/ask-questions Review this material, ask the questions it raises, and go find the answers
/ask-questions One question won't cover this; help me build a set
```

## How it works

1. **Situate** — find where you're standing before naming the gap; read first when the context isn't already in front of you, so you never ask for what you could have found yourself.
2. **Delegate, or don't** — decide who gathers the context and who shapes the words: fork agents to gather-and-ask, hand an agent context to design the question, or ask one only to sharpen a draft.
3. **Name the gap, pick the move** — let the gap you feel choose the kind of question: clarify, probe, anchor, label, summarize, or question the question.
4. **Clear four clarity laws** — one idea per question, plain words, no smuggled premise, a real question rather than a statement wearing a question mark.
5. **Compose a set when one won't reach** — build a parallel set handed over at once, or a sequence where each answer narrows the next into a sharper inquiry.
6. **Place it in time** — open before closed, leave silence, talk less than they do, close with a catch-all.

## When to use this

Reach for it whenever you're about to ask the user something and the question should land well — including when you're about to use the `AskUserQuestion` tool. Use it when you're unsure what to ask, when a first question fell flat, when one question won't reach and you need a set, when the user's tone or messages signal you've drifted from what they need, or when you're asked to read some material and generate the questions it raises. It also covers gathering the context before you can ask at all.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`ask-questions.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/ask-questions.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
