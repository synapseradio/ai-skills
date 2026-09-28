---
name: ask-questions
description: >-
  Ask the user a genuinely good question in the moment, or make a deliberate
  non-question move, to discover, clarify, probe, or confirm, in any
  conversation or domain. Use when about to ask the user something or use
  the `AskUserQuestion` tool, when a question fell flat, when an answer just
  came back and you need what sits beneath it, or when the user's tone or
  messages signal you have drifted from what they need. Also use to judge
  when the better move is not a question at all: a restatement, a plain
  statement, silence, or asking nothing.
compatibility: >-
  Saves a record of each run when loaded from the thinkies Claude Code plugin;
  elsewhere prints the record in the reply for the user to keep.
---

# ask-questions

## The game

A question is an instrument: the words you pick decide what comes back. And a good question rarely works alone — it serves one inquiry. Name the question the inquiry exists to answer, and call it the driving question. Every candidate question is then a rung that must earn its place on the ladder toward it. The output is the next move that best advances the driving question: one clean question, or a deliberate non-question move.

## The rung test

Two gates hold in the core. First, relevance: would a complete answer to this question at least partly answer the driving question? If not, it's a digression dressed as a rung — cut it, or find the question that isn't. Second, discrimination: would different answers to it change what is done or asked next? A question whose every possible answer leaves your next move unchanged fails, however relevant its topic.

## The four clarity laws

Every drafted question passes all four before it is asked or handed on.

- One idea per question. Two ideas joined by "and" or "or" force the person to pick a half to answer, and you lose the other.
- Plain words, matched to their vocabulary. If they call it a "ticket," you call it a ticket.
- No smuggled premise. "What was that like?" carries nothing in; "Wasn't that awful?" answers itself and tells them what to say.
- A real question, not a statement wearing a question mark. If the question already supplies the answer, it asks nothing.

## The moves that aren't questions

At the juncture where the next question would go, four other moves compete for the turn, and sometimes win: silence — leave the pause unfilled, since an unfilled pause pulls out more than another question would; a reflective restatement — say back what you understood and invite correction; a plain statement — state your own understanding or your perplexity and let them respond to it; and asking nothing — because the answer is findable in what you can already read, or because no candidate passes both gates. Weigh the best candidate question against these before giving it the question's place.

## When the inquiry is done

An inquiry ends legitimately in one of four states; name the one it reaches, or, for an inquiry not yet asked, the one that will close it. Answered: the driving question is answered to the calibration the caller needs. Earned exit: the questions have done their work and a direct statement now serves better — licensed when the inquiry serves the asker's decision, foreclosed when it exists to develop the answerer's own thinking. Honest non-answer: what remains unknown, stated with its confidence — a calibrated unknown beats forced closure. Replaced: the driving question itself proved wrong — load [driving-question](./references/driving-question.md) and restate the inquiry. Questioning past these points is itself a failure.

## Route by the move you need

First decide which kind of move the moment calls for — composing the inquiry, going under an answer, or auditing the inquiry itself — then pick the one reference within it. Load that reference and work through its Questions section before you act.

**A. Compose the inquiry.** You're building or arranging a set of questions that reaches the driving question.

| The gap | Load |
|---------|------|
| You don't yet have the rungs and must generate the set that reaches the driving question | [ladder](./references/ladder.md) |
| You already have the questions and are deciding the arc — where to open, when to narrow, what to avoid | [sequence-shapes](./references/sequence-shapes.md) |
| You have a qualified set and must pick which question comes next | [ordering](./references/ordering.md) |

When more than one row here matches, load in this order: ladder (generate) → sequence-shapes (arrange) → ordering (pick next). Composing and unsure where to start? Start with ladder.

**B. Go under one answer.** An answer is in hand or anticipated, and you need what sits beneath it. Pick the direction by the claim's kind — empirical claims ground downward in observables; value and definitional claims ground in what the answerer themselves affirms — then pick the row.

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

Forming a question has two parts: gathering the context and shaping the words. You can keep both, or split them across agents. Pick by where the work is.

- **Fork to gather and ask.** When the context is large or scattered — many files, a long history, several places to look — send one or more agents to read it and come back with a candidate question already formed. Each returns a question grounded in what it found. Treat the context it rode in on as unverified until you check it.
- **Hand off the context, ask for the question.** When you already hold the context, give it to an agent and have it design the question from there. Reach for this when you want a fresh angle, or a few drafts to choose between.
- **Ask only for the phrasing.** When agents are already fanned out and you have a question in mind to send back to the user, hand one your draft plus the four clarity laws above, and ask it to sharpen the wording.

## How the work returns

Each invocation returns the next single move, given the record of the exchange so far. When that record wasn't supplied, say so rather than assuming none exists. Composing returns the next question, going under returns the next move, and auditing returns its findings plus the question they license. An audit that ends in "ask nothing yet" returns the findings and the reason. The Questions sections in the references are internal worksheets: work through them before you act, never read them out verbatim.

## Record

Records live in the store, `${CLAUDE_PLUGIN_DATA}/records/`, with a copy in the mirror folder, `${user_config.records_mirror}`.

- When the store path is not absolute, no store exists here. Build the record anyway, and end the reply with it in a `jsonl` block under its file name, for the user to keep.
- When the mirror path is empty or still a placeholder, skip the mirror. Otherwise, after the run's last line, copy the record file into the mirror under the same name.
- Create either folder when it is missing.

Write each record in the form of the template at the end of this section: the file name as shown, then one JSON object per line, one line per event, in the order the events happen, with every bracketed value replaced. Write a kind as often as the run produces it, and leave out kinds it does not produce. Take times from the clock in UTC, for example `date -u +%Y%m%dT%H%M%SZ` for the file name. A topic is two to six lowercase words joined by hyphens. An answer's `q` names the question or open item it answers.

- Append lines; never change or remove one.
- Where lines share an id, the latest wins. A link's id is its from, to, and rel. `"retired": true` removes the entry.
- To resume a run, read its file, first copying it from the mirror when only the mirror holds it, and append a run line with `"resumed": true`.
- An agent answering a record's questions appends its answer, skip, and open lines to the same file and names itself in `by`.

At the end of a run, play the record back in the form of [assets/playback.md](assets/playback.md): the path it was saved to, then every part the reply has not already shown. Never show the raw lines.

Record the driving question as the subject; each question you ask or compose as a question line; each reply as an answer line naming its speaker in `by`; each move that is not a question as a note; the end state the inquiry reached as a result; and each question left unanswered as an open line.

File: `ask-questions_[start time, UTC, YYYYMMDDTHHMMSSZ]_[topic].jsonl`

```jsonl
{"kind": "run", "at": "[time, UTC, YYYY-MM-DDTHH:MM:SSZ]", "skill": "ask-questions", "topic": "[topic]", "subject": "[the driving question]", "project": "[repository or project name, or empty]", "resumed": false}
{"kind": "question", "at": "[time]", "id": "q1", "text": "[the question as asked]"}
{"kind": "answer", "at": "[time]", "q": "q1", "text": "[the reply]", "by": "[who replied]"}
{"kind": "note", "at": "[time]", "text": "[a move that is not a question]", "context": "[what prompted it]"}
{"kind": "result", "at": "[time]", "text": "[the end state the inquiry reached]"}
{"kind": "open", "at": "[time]", "id": "o1", "text": "[a question still unanswered]", "q": "q2"}
```
