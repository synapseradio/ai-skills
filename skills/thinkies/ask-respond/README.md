# ask-respond

Structured Q&A that decomposes questions before answering. Mirrors the question, breaks it into parts, assesses current knowledge, responds, and optionally proposes a next action.

## Reach for it when

- A question looks simple but carries assumptions, such as an "always" or a premise nobody checked.
- You want the answer together with what it rests on: observation, documentation, inference, or assumption.
- You are not sure whether the question asks for an explanation or for something to be done.

## What you walk away with

The question restated in plain terms, the assumptions it carries and the sub-questions that must be answered first, the evidence under each sub-answer with its gaps, an answer pitched at the strength that evidence supports, and a proposed next action where the question calls for one.

Trimmed from a run on "Why does toast always land butter-side down?" ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/ask-respond/toast-butter-side-down.md)):

> 1. Why does a slice of buttered toast that falls from a table to the floor land butter-side down?
>
>    Because a slice that slides off a table edge starts to tip as it goes, turns about half a revolution during the fall, and lands with the face that began up now facing down. The fall from table height takes too little time for a second half-turn to finish. The rotation is a property of the table edge and the slice, not of the butter, so the same reasoning gives a butter-side-up landing for any toast that started butter-side down.
>
> […]
>
> "Always" is too strong. The tendency holds for tables of ordinary height and for slices that start butter-side up. Toast that starts butter-side down, that leaves a hand, or that falls from a much greater height lands differently. I am unsure whether the mass of the butter shifts the result, and unsure how much remembering the annoying landings adds.
>
> 1. Does the question about buttered toast falling from a table imply a request for action, and if so, what course should be proposed?
>
>    Skipped: The question asks why, not what to do. It names no toast about to fall and no goal such as saving the toast.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/ask-respond/` into `~/.claude/skills/ask-respond/`.

## Usage

```
/ask-respond <question>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`ask-respond.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/ask-respond.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
