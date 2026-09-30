# question-the-question

Examine whether the inquiry is aimed at the right target. Probes the question's assumptions, checks for drift from the core concern, then sharpens or reframes it.

## Try it when

- You've asked "how do I stop X" and every answer is a technique aimed at X.
- The question you're working on has quietly narrowed from what you actually care about.
- Answers keep coming back that are correct and don't help.

## What a run looks like

Why this question is the one being asked and the candidates that aim elsewhere, the assumptions that must hold for it to be the right question (with the heaviest one named), where it drifted from the core concern, and a reframed question broken into parts you can act on, with where the reframing could itself be wrong.

Trimmed from a run on "How do I get my cat to stop sitting on my keyboard?" ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/question-the-question/cat-on-keyboard.md)):

> 1. **The keyboard is what the cat wants.** It holds if the cat is drawn to the keys, their warmth, or their height. It fails if the cat wants the person, and the keyboard is only where the person's hands and eyes are.
>
> […]
>
> The question has drifted from that in one place. "Stop sitting" moved the target from the person's work to the cat's posture. The original concern says nothing about the cat's behavior. It is about the person being able to type.
>
> […]
>
> **Reframed question.** "What does my cat get from sitting on my keyboard, and how can I keep my work safe and my cat close, or apart, in a way I actually want?"

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/question-the-question/` into `~/.claude/skills/question-the-question/`.

## Usage

```
/question-the-question <the question being asked>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`question-the-question.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/question-the-question.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
