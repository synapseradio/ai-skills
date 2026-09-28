---
name: connect-ideas
description: Test how two ideas relate, or find a distant match for one idea, and keep only the relations
  the evidence supports
---

## Steps

### 1. What is each side's structure?

Restate each side without its domain's words: its entities, the relations between them, its constraints, and its goal.

### 2. Where is the other side?

Answer only when one side was given. Search fields far from its own, such as biology, other industries, physical processes, games, and social structures, for a solved problem with the same structure. Take the closest match as the second side, and say how its solution works.

### 3. Which relations hold?

Test each kind in turn, stating the evidence for and against:

- Analogy: the same structure in different material.
- Cause and effect: a change in one changes the other.
- Means and end: one serves the other's purpose.
- Part and whole: one belongs to the other.
- Shared class: both are kinds of one thing.
- Shared constraint or resource: both draw on, or are limited by, the same thing.
- Tension: improving one worsens the other.

### 4. Which relations survive?

Keep only those the evidence supports. For an analogy, list what maps directly, what needs adapting, and what breaks.

### 5. What does each surviving relation let you do?

For each, name the act it opens, such as importing a solution, intervening upstream, or trading one resource against another, and the principle that makes it work.

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

Record the two sides, or the one side, as the subject; each Given as a given line; each question as a question line; each answer, `Skipped:`, and `Open:` as an answer, skip, or open line; and each surviving relation, with what it lets you do, as a result.

File: `connect-ideas_[start time, UTC, YYYYMMDDTHHMMSSZ]_[topic].jsonl`

```jsonl
{"kind": "run", "at": "[time, UTC, YYYY-MM-DDTHH:MM:SSZ]", "skill": "connect-ideas", "topic": "[topic]", "subject": "[the two sides, or the one side]", "project": "[repository or project name, or empty]", "resumed": false}
{"kind": "given", "at": "[time]", "text": "[a fact, source, or limit the answers must respect]", "source": "[where it came from]"}
{"kind": "question", "at": "[time]", "id": "question-1", "text": "[step 1's question, naming the subject]"}
{"kind": "answer", "at": "[time]", "q": "question-1", "text": "[the answer]", "by": "[who answered]"}
{"kind": "skip", "at": "[time]", "q": "question-2", "reason": "[why the step does not apply]"}
{"kind": "open", "at": "[time]", "id": "open-1", "text": "[the fact an answer needs]", "q": "question-3"}
{"kind": "result", "at": "[time]", "text": "[a surviving relation and what it lets you do]"}
```
