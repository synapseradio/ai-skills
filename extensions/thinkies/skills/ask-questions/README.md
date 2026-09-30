# ask-questions

A directed thought process for making the right next move with the user — one genuinely good question, or a deliberate non-question — in the moment, in any conversation or domain. Each invocation returns that single next move, given the exchange so far. Good questions serve one inquiry: name the question the inquiry exists to answer (the driving question), and every candidate question becomes a rung that must earn its place on the ladder toward it.

## Try it when

- You are about to ask someone something, and the question has to land.
- A first question fell flat, or an answer just came back and you need what sits beneath it.
- The other person's tone or messages signal the conversation has drifted from what they need.
- You need to gather context before you can ask at all.
- The better move may not be a question: a restatement, a plain statement, silence, or asking nothing.

The same holds when the assistant is the one about to ask you something, including through the `AskUserQuestion` tool.

## You get back

One next move, given the exchange so far: the question to ask or the non-question move to make, why it earns its turn (an answer would bear on the driving question, and different answers would change what you do next), what was weighed and cut, and the rungs the next answer could open.

Here it is on what to ask a friend who says "I think I want to quit my job and open a sock-only shop", cut down ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/ask-questions/sock-shop-dream.md)):

> **Driving question:** What pulled my friend toward this, and how settled is it, so that I can tell whether to encourage or caution?
>
> **The next move:** one question, said warmly and then left alone.
>
> > What got you thinking about it?
>
> […]
>
> **What I weighed and cut**
>
> - "Have you thought about the money?" and "Are you sure?" both fail the fourth law. They are caution wearing a question mark, they tell the friend what you fear, and they stand on an unestablished premise, that the friend has not thought about it.
> - "What's wrong with your job right now?" fails the third law. The friend named no complaint; it plants one.
>
> […]
>
> **What the ladder holds next**, each rung grown only from what the answer licenses:
>
> 1. If the answer names a push, such as a job the friend wants out of, ask what the friend would want from the next stretch of work. The shop is then one candidate among several.
> 2. If it names a pull, ask what the friend pictures on an ordinary day in the shop.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/ask-questions/` into `~/.claude/skills/ask-questions/`.

## Usage

```
/ask-questions I need to ask my user about their deploy setup but I'm not sure what to ask
/ask-questions My first question fell flat — help me ask it better
/ask-questions They just answered "it depends on the team" — what do I ask next?
```

## Records

When loaded from the thinkies Claude Code plugin, the skill saves a record of each run to the plugin store at `${CLAUDE_PLUGIN_DATA}/records/`, and copies it to the Records mirror folder when that optional setting names one. Uninstalling the plugin deletes the store unless you run `claude plugin uninstall thinkies@ai-skills --keep-data`. Loaded anywhere else, the skill prints the record in its reply for you to keep.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`ask-questions.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/ask-questions.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
