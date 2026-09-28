---
name: check-notes
description: Find saved notes and run records by topic, skill, date, or project, and play them back
  in readable form. Use when the user asks what was found about something earlier, to show notes or
  records on a topic, to find an insight from a past conversation, to list recent records, or to pick
  up an earlier run.
---

# Check notes

1. **Search the names.** List the store, then the mirror for files the store lacks. Split each file name at its underscores into skill, time, and topic. Keep files whose skill matches the one asked for, whose time falls in the range asked for (compare times as text; they sort in time order), and whose topic shares words with the request.
2. **Search the contents.** When the names leave nothing, or too much, search the files' text for the request's words, and keep the files that hold them.
3. **Play back.** Newest first, show each kept record in the form of [assets/playback.md](assets/playback.md), with its path.
4. **Offer to continue.** Name the file a run would resume from. A run resumes by reading its file and appending to it.

When no store exists here, play back any record pasted into the conversation the same way.

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

This skill writes no record. The template shows every kind of line a record may hold.

File: `[skill]_[start time, UTC, YYYYMMDDTHHMMSSZ]_[topic].jsonl`

```jsonl
{"kind": "run", "at": "[time, UTC, YYYY-MM-DDTHH:MM:SSZ]", "skill": "[skill]", "topic": "[topic]", "subject": "[subject]", "project": "[project]", "resumed": false}
{"kind": "given", "at": "[time]", "text": "[fact]", "source": "[source]"}
{"kind": "question", "at": "[time]", "id": "question-1", "text": "[question]"}
{"kind": "answer", "at": "[time]", "q": "question-1", "text": "[answer]", "by": "[who answered]"}
{"kind": "skip", "at": "[time]", "q": "question-2", "reason": "[reason]"}
{"kind": "open", "at": "[time]", "id": "open-1", "text": "[open item]", "about": ["function-1"]}
{"kind": "note", "at": "[time]", "text": "[note]", "context": "[context]"}
{"kind": "result", "at": "[time]", "text": "[result]"}
{"kind": "node", "at": "[time]", "id": "function-1", "level": "generalized function", "grain": "[grain]", "name": "[name]", "evidence": "[evidence]", "retired": false}
{"kind": "link", "at": "[time]", "from": "process-1", "to": "function-1", "rel": "means-of", "retired": false}
{"kind": "actor", "at": "[time]", "id": "actor-1", "name": "[name]", "type": "[person or agent]", "acts_on": ["process-1"], "sees": ["function-1"], "retired": false}
```
