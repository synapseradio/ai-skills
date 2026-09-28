---
name: ask-respond
description: Structured Q&A that decomposes questions before answering
compatibility: >-
  Saves a record of each run when loaded from the thinkies Claude Code plugin;
  elsewhere prints the record in the reply for the user to keep.
---

## Steps

### 1. What is being asked, in my own words?

Restate the question from `$ARGUMENTS` in the assistant's first-person point of view.

- "how do you feel?" → "how do I feel?"
- "what day is it?" → "what day is it?"

### 2. What must be answered first?

List what is actually being asked, the assumptions the question carries, and the sub-questions whose answers it needs, in the context of the current conversation.

### 3. What does each sub-question's answer rest on?

Label each: direct observation from context, documentation or an authoritative source, inference from related facts, or assumption without evidence. Name each gap.

### 4. What is the answer?

Answer calibrated to the evidence available.

### 5. What should happen next?

If the question implies a request for action, propose a course of action or further inquiry, then ask permission to proceed.

## Output

Choose the mode from what you were handed:

- A question set: answer it.
- A request for questions only: write the question set and stop.
- Anything else: write the question set, then answer it.

Write the question set in this form: one question per step, in step order, each reworded to name the subject, so that a reader holding only the set can answer it.

```markdown
**Subject:** [what is examined, named so it can be found without this conversation]

**Given:**

- [a fact, source, or limit the answers must respect] ([where it came from])

**Questions:**

1. [step 1's question, naming the subject]
2. [step 2's question, naming the subject]
3. [step 3's question, naming the subject]
```

Answer in this form, keeping each question's number and wording, from the set and from what you can check yourself:

```markdown
**Subject:** [the subject, as the set names it]

1. [step 1's question, naming the subject]

   [the answer]

2. [step 2's question, naming the subject]

   Skipped: [why this step does not apply]

3. [step 3's question, naming the subject]

   Open: [the fact the answer needs that the set does not give]
```

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

Record the restated question as the subject; each Given as a given line; each question as a question line; each answer, `Skipped:`, and `Open:` as an answer, skip, or open line; and the answer to the user as a result.

File: `ask-respond_[start time, UTC, YYYYMMDDTHHMMSSZ]_[topic].jsonl`

```jsonl
{"kind": "run", "at": "[time, UTC, YYYY-MM-DDTHH:MM:SSZ]", "skill": "ask-respond", "topic": "[topic]", "subject": "[the question, restated]", "project": "[repository or project name, or empty]", "resumed": false}
{"kind": "given", "at": "[time]", "text": "[a fact, source, or limit the answers must respect]", "source": "[where it came from]"}
{"kind": "question", "at": "[time]", "id": "question-1", "text": "[step 1's question, naming the subject]"}
{"kind": "answer", "at": "[time]", "q": "question-1", "text": "[the answer]", "by": "[who answered]"}
{"kind": "skip", "at": "[time]", "q": "question-2", "reason": "[why the step does not apply]"}
{"kind": "open", "at": "[time]", "id": "open-1", "text": "[the fact an answer needs]", "q": "question-3"}
{"kind": "result", "at": "[time]", "text": "[the answer to the user's question]"}
```
