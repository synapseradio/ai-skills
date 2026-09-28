---
name: generate-questions
description: >-
  Compose a set of questions toward one driving question and return it as a
  written inquiry, without asking anyone. The inquiry gives each question in
  the order to ask it, what its answer decides, the follow-up each kind of
  answer opens, and the move to make instead if it falls flat. Use when
  spawned to draft questions for someone else to ask or answer, when asked to
  generate, draft, review, sharpen, or cut down a set of questions, as in read
  this spec and generate questions or what should I ask the backend team, or
  when preparing questions for an interview, a call, or a review.
compatibility: >-
  Saves a record of each run when loaded from the thinkies Claude Code plugin;
  elsewhere prints the record in the reply for the user to keep.
---

# generate-questions

Name the question the inquiry exists to answer: the driving question. Compose the questions that climb toward it, each a rung that must earn its place, and return them as an inquiry that whoever holds it can ask or answer without this conversation. Ask no one. Put no question to the user through any tool.

## Read first

Read what the questions will land in before drafting: the thread, the files, the spec, what has already been said. List each fact the questions rest on under Given. Drop any candidate question whose answer turned up in the reading.

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

## Output

Return the inquiry in this form. When the audit ends in asking nothing yet, return the driving question, the findings, and the reason in place of Rungs.

````markdown
**Driving question:** [the question the inquiry exists to answer, named so it can be found without this conversation]

**Given:**

- [a fact the questions rest on] ([where it came from])

**Rungs**, in the order to ask them:

1. [the question, worded as it will be asked]
   - Decides: [what changes next, depending on the answer]
   - If [one kind of answer]: [the follow-up question or move]
   - If [another kind of answer]: [the follow-up question or move]
   - If it falls flat: [the restatement, plain statement, silence, or asking nothing to use instead, worded]
2. [the next question, worded as it will be asked]
   - Decides: [what changes next, depending on the answer]

**Done when:** [the end state that closes the inquiry, and what reaching it looks like]
````

Whoever answers the inquiry keeps each rung's number and wording, writes the answer under it, and names the branch the answer opens:

````markdown
**Driving question:** [as the inquiry names it]

1. [the question]

   [the answer] (opens: [the branch taken])

2. [the question]

   Open: [what the answer needs that the inquiry does not give]
````

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

Record the driving question as the subject; each fact under Given as a given line; each rung as a question line; each Decides, branch, and fallback move as a note whose context names its rung; and the Done when line as a result. An agent answering the inquiry adds answer and open lines.

File: `generate-questions_[start time, UTC, YYYYMMDDTHHMMSSZ]_[topic].jsonl`

```jsonl
{"kind": "run", "at": "[time, UTC, YYYY-MM-DDTHH:MM:SSZ]", "skill": "generate-questions", "topic": "[topic]", "subject": "[the driving question]", "project": "[repository or project name, or empty]", "resumed": false}
{"kind": "given", "at": "[time]", "text": "[a fact the questions rest on]", "source": "[where it came from]"}
{"kind": "question", "at": "[time]", "id": "q1", "text": "[the rung, worded as it will be asked]"}
{"kind": "note", "at": "[time]", "text": "[Decides, a branch, or the fallback move]", "context": "q1"}
{"kind": "result", "at": "[time]", "text": "[the Done when line]"}
{"kind": "answer", "at": "[time]", "q": "q1", "text": "[the answer, and the branch it opens]", "by": "[who answered]"}
{"kind": "open", "at": "[time]", "id": "o1", "text": "[what an answer needs that the inquiry does not give]", "q": "q1"}
```
