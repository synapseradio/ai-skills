---
name: save-note
description: Save an insight from the conversation as a note that can be found again by topic, date, or project. Use when the user says save this, note this, keep this insight, or I want to find this later, or when a finding worth returning to turns up outside any structured run.
compatibility: >-
  Saves a record of each run when loaded from the thinkies Claude Code plugin;
  elsewhere prints the record in the reply for the user to keep.
---

# Save note

1. **The insight.** State it in one to three sentences a reader without this conversation can follow. Quote the user or the source where the exact words matter.
2. **Its context.** Say what was being worked on, in which project, and what led to the insight.
3. **The topic.** Name what the note is about in two to six words.
4. **Save.** Write the record, then play it back.

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

Record the insight in one line as the subject, the insight and its context as a note, and each question it leaves as an open line.

File: `save-note_[start time, UTC, YYYYMMDDTHHMMSSZ]_[topic].jsonl`

```jsonl
{"kind": "run", "at": "[time, UTC, YYYY-MM-DDTHH:MM:SSZ]", "skill": "save-note", "topic": "[topic]", "subject": "[the insight in one line]", "project": "[repository or project name, or empty]", "resumed": false}
{"kind": "note", "at": "[time]", "text": "[the insight, one to three sentences]", "context": "[what was being worked on and what led to it]"}
{"kind": "open", "at": "[time]", "id": "open-1", "text": "[a question the insight leaves]", "q": ""}
```
