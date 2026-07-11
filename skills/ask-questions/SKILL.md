---
name: ask-questions
description: >-
  Ask a genuinely good question — or a composed set of them — in the moment, to
  discover, clarify, probe, or confirm, in any conversation or domain. Use when
  about to ask the user something or use the `AskUserQuestion` tool, when a
  question fell flat or one won't reach and you need a set, when the user's tone
  or messages signal you have drifted from what they need, or when the user
  wants questions phrased, generated, or sharpened — "read this spec and
  generate questions", "ask about the schema", "review this and ask questions",
  "help me understand what to ask", or to clarify a requirement or idea.
metadata:
  context: fork
---

# ask-questions

## The game

A question is an instrument: the words you pick decide what comes back. And a good question rarely works alone — it serves one inquiry. Name the question the inquiry exists to answer, and call it the driving question. Every candidate question is then a rung that must earn its place on the ladder toward it. The output is one clean question, or a small set composed to climb together.

## The rung test

One gate holds in the core, from Question Under Discussion theory: would a complete answer to this question at least partly answer the driving question? If not, it's a digression dressed as a rung — cut it, or find the question that isn't.

## The four clarity laws

Every drafted question passes all four before you ask it.

- One idea per question. Two ideas joined by "and" or "or" force the person to pick a half to answer, and you lose the other.
- Plain words, matched to their vocabulary. If they call it a "ticket," you call it a ticket.
- No smuggled premise. "What was that like?" carries nothing in; "Wasn't that awful?" answers itself and tells them what to say.
- A real question, not a statement wearing a question mark. If you already supplied the answer, you asked nothing.

## Route by the gap you feel

Pick the situation that matches, load that reference, and work through its Questions section before you ask.

| Situation | Load |
|-----------|------|
| You need the rungs between here and the driving question — building or growing the ladder, composing a set | [ladder](./references/ladder.md) |
| You have a stated preference and want the value under it | [laddering](./references/laddering.md) |
| An answer handed you a conclusion, belief, or plan, and you need the data under it | [climb-down](./references/climb-down.md) |
| An answer is shaky in a specific way, and "tell me more" feels too blunt | [probe](./references/probe.md) |
| You're choosing the shape and timing of a whole sequence — where to open, when to narrow, what to avoid | [sequence-shapes](./references/sequence-shapes.md) |
| Several candidate questions qualify and you must pick which comes next | [ordering](./references/ordering.md) |
| Some question in the inquiry treats the thing as simpler than it is | [pretense](./references/pretense.md) |
| You're starting an inquiry and need to name what you accept without justification | [grants](./references/grants.md) |
| You're carrying a ladder or a question set into a new domain | [transfer](./references/transfer.md) |

## Decide who gathers the context, and who shapes the question

A question lands in a context, and the context decides whether the question is even worth asking. Sometimes the context is already in front of you — the conversation carries it, or you just read the file. More often it isn't, and the honest move is to go read first: skim the thread, open the code, check what's already been said. A question that asks for something you could have found yourself wastes the other person and signals you didn't look. What you're after is the gap that genuinely remains — the thing only they can answer.

Forming a question has two parts: gathering the context and shaping the words. You can keep both, or split them across agents. Pick by where the work is.

- **Fork to gather and ask.** When the context is large or scattered — many files, a long history, several places to look — send one or more agents to read it and come back with a candidate question already formed. Each returns a question grounded in what it found. Treat the context it rode in on as unverified until you check it.
- **Hand off the context, ask for the question.** When you already hold the context, give it to an agent and have it design the question from there. Reach for this when you want a fresh angle, or a few drafts to choose between.
- **Ask only for the phrasing.** When agents are already fanned out and you have a question in mind to send back to the user, hand one your draft plus the four clarity laws above, and ask it to sharpen the wording.
