---
name: ask-questions
description: Ask a genuinely good question — or a composed set of them — in the moment, to discover,
  clarify, probe, or confirm, in any conversation or domain. Use when about to ask the user something
  or use the `AskUserQuestion` tool, when a question fell flat or one won't reach and you need a set,
  when the user's tone or messages signal you have drifted from what they need, or when the user wants
  questions phrased, generated, or sharpened — "read this spec and generate questions", "ask about
  the schema", "review this and ask questions", "help me understand what to ask", or to clarify a
  requirement or idea. Also use to judge when the better move is not a question at all — a restatement,
  a plain statement, silence, or asking nothing.
---

# ask-questions

## The game

A question is an instrument: the words you pick decide what comes back. And a good question rarely works alone — it serves one inquiry. Name the question the inquiry exists to answer, and call it the driving question. Every candidate question is then a rung that must earn its place on the ladder toward it. The output is the move that best advances the driving question: one clean question, a small set composed to climb together, or a deliberate non-question move.

## The rung test

Two gates hold in the core. First, relevance: would a complete answer to this question at least partly answer the driving question? If not, it's a digression dressed as a rung — cut it, or find the question that isn't. Second, discrimination: would different answers to it change what you do or ask next? A question whose every possible answer leaves your next move unchanged fails, however relevant its topic.

## The four clarity laws

Every drafted question passes all four before you ask it.

- One idea per question. Two ideas joined by "and" or "or" force the person to pick a half to answer, and you lose the other.
- Plain words, matched to their vocabulary. If they call it a "ticket," you call it a ticket.
- No smuggled premise. "What was that like?" carries nothing in; "Wasn't that awful?" answers itself and tells them what to say.
- A real question, not a statement wearing a question mark. If you already supplied the answer, you asked nothing.

## The moves that aren't questions

At the juncture where the next question would go, four other moves compete for the turn, and sometimes win: silence — end your turn without asking, since an unfilled pause pulls out more than another question would; a reflective restatement — say back what you understood and invite correction; a plain statement — state your own understanding or your perplexity and let them respond to it; and asking nothing — because the answer is findable in what you can already read, or because no candidate passes both gates. Weigh the best candidate question against these before you spend the turn.

## When the inquiry is done

An inquiry ends legitimately in one of four states; name the one you've reached. Answered: the driving question is answered to the calibration the caller needs. Earned exit: the questions have done their work and a direct statement now serves better — licensed when the inquiry serves the asker's decision, foreclosed when it exists to develop the answerer's own thinking. Honest non-answer: what remains unknown, stated with its confidence — a calibrated unknown beats forced closure. Replaced: the driving question itself proved wrong — load [driving-question](./references/driving-question.md) and restate the inquiry. Questioning past these points is itself a failure.

## Route by the move you need

First decide which kind of move the moment calls for — composing the inquiry, going under an answer, or auditing the inquiry itself — then pick the one reference within it. Load that reference and work through its Questions section before you ask.

**A. Compose the inquiry.** You're building or arranging a set of questions that reaches the driving question.

| The gap | Load |
|---------|------|
| You don't yet have the rungs and must generate the set that reaches the driving question | [ladder](./references/ladder.md) |
| You already have the questions and are deciding the arc — where to open, when to narrow, what to avoid | [sequence-shapes](./references/sequence-shapes.md) |
| You have a qualified set and must pick the single next question to ask | [ordering](./references/ordering.md) |

When more than one row here matches, load in this order: ladder (generate) → sequence-shapes (arrange) → ordering (pick next). Composing and unsure where to start? Start with ladder.

**B. Go under one answer.** An answer came back and you need what sits beneath it. Pick the direction by the claim's kind — empirical claims ground downward in observables; value and definitional claims ground in what the answerer themselves affirms — then pick the row.

| The direction | Load |
|---------------|------|
| Up — to the value under a stated preference, by asking what matters about each answer | [laddering](./references/laddering.md) |
| Down — to the observable data under a conclusion, belief, or plan | [climb-down](./references/climb-down.md) |
| At — one shaky element: clarify a term, test a claim, anchor a generality, label a feeling, or confirm you understood | [probe](./references/probe.md) |

**C. Audit the inquiry's foundations.** Step back from the answers to the inquiry itself.

| The gap | Load |
|---------|------|
| Some question treats the thing as simpler than it is | [pretense](./references/pretense.md) |
| You're starting out and must name what you accept without justification | [grants](./references/grants.md) |
| You're carrying a ladder or a question set into a new domain | [transfer](./references/transfer.md) |
| The driving question itself may be the wrong one | [driving-question](./references/driving-question.md) |

## Decide who gathers the context, and who shapes the question

A question lands in a context, and the context decides whether the question is even worth asking. Sometimes the context is already in front of you — the conversation carries it, or you just read the file. More often it isn't, and the honest move is to go read first: skim the thread, open the code, check what's already been said. A question that asks for something you could have found yourself wastes the other person and signals you didn't look. What you're after is the gap that genuinely remains — the thing only they can answer.

Forming a question has two parts: gathering the context and shaping the words. Do both yourself: go read what you need, then shape the question from what you found. That sequence is the instruction, and it holds in any harness.

Where a harness lets you delegate to other agents, either part can be split off. The work is the same, only spread wider, and any context an agent rides in on stays unverified until you check it.

- **Send others to gather and ask.** When the context is large or scattered — many files, a long history, several places to look — one or more agents can read it and come back with a candidate question already formed, each grounded in what it found.
- **Hand off the context, ask for the question.** When you already hold the context, give it to an agent and have it design the question from there. Reach for this when you want a fresh angle, or a few drafts to choose between.
- **Ask only for the phrasing.** When agents are already fanned out and you have a question in mind to send back to the user, hand one your draft plus the four clarity laws above, and ask it to sharpen the wording.

## How the work returns

Two execution modes exist, and the caller's context decides which you're in. Live: a running exchange is underway, and each invocation returns the next single move given the record of the exchange so far — when that record wasn't supplied, say so rather than assuming none exists. Composed: one pass returns a set built to travel — the questions plus the branches you anticipate.

What each route hands back: composing returns the question or the set; going under returns the next move; auditing returns its findings plus the question or questions they license — an audit that ends in "ask nothing yet" returns the findings and the reason. The Questions sections in the references are internal worksheets: work through them before you act, never read them out verbatim.
