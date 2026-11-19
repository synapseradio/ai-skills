# Lasting model

A lasting model is the model written as a record: one line per node, link, actor, open item, and finding. A later session reloads the record and extends it. Follow this file beside the steps in `SKILL.md`.

## Reload or extend

1. Find the record: the one the user hands over, or the store's file for this skill whose topic names this system. Where none is found, say so and start a new model.
2. Take the latest line for each node, link, and actor as the current model.
3. Answer the record's open lines before adding anything new.
4. Add only lines that extend the model. New ids continue the numbering. A correction is a new line with the same id, and a removal is a line with `"retired": true`.

## Keep

Write the record as the next section directs, once the model is shown. Its playback form, `assets/playback.md`, sits in the skill's folder beside `SKILL.md`. In each node line, `level` holds the level's name as the Levels table gives it.

## Record

Records live in the store, `${CLAUDE_PLUGIN_DATA}/records/`, with a copy in the mirror folder, `${user_config.records_mirror}`.

- When the store path is not absolute, or no tool here writes files, no store is reachable. Give the record in the reply instead, in a `jsonl` block under its file name, for the user to keep.
- When the mirror path is empty or still a placeholder, skip the mirror. Otherwise, after the run's last line, copy the record file into the mirror under the same name.
- Create either folder when it is missing.

Write each record in the form of the template at the end of this section: the file name as shown, then one JSON object per line, one line per event, in the order the events happen, with every bracketed value replaced. Write a kind as often as the run produces it, and leave out kinds it does not produce. Take times from the clock in UTC, for example `date -u +%Y%m%dT%H%M%SZ` for the file name. Where no clock can be read, take the date from the conversation and write the time of day as zeros. A topic is two to six lowercase words joined by hyphens. An answer's `q` names the question or open item it answers.

- Append lines; never change or remove one.
- Where lines share an id, the latest wins. A link's id is its from, to, and rel. `"retired": true` removes the entry.
- To resume a run, read its file, first copying it from the mirror when only the mirror holds it, or take the record the user pastes. Append a run line with `"resumed": true`, then the lines the resumed run adds.
- An agent answering a record's questions appends its answer, skip, and open lines to the same file and names itself in `by`.

After saving, play the record back in the form of [assets/playback.md](assets/playback.md): the path it was saved to, then every part the reply has not already shown. Show raw lines only in the `jsonl` block that stands in for an unreachable store.

Record the scope as the subject; each node, link, and actor as its own line; each gap as an open line about its nodes; each finding as a result; and, on reload, each answered open item as an answer line.

File: `domain-analysis_[start time, UTC, YYYYMMDDTHHMMSSZ]_[topic].jsonl`

```jsonl
{"kind": "run", "at": "[time, UTC, YYYY-MM-DDTHH:MM:SSZ]", "skill": "domain-analysis", "topic": "[topic]", "subject": "[system, boundary, task served, reading]", "project": "[repository or project name, or empty]", "resumed": false}
{"kind": "node", "at": "[time]", "id": "function-1", "level": "generalized function", "grain": "[grain name]", "name": "[what must happen]", "evidence": "[where this is shown]", "retired": false}
{"kind": "node", "at": "[time]", "id": "process-1", "level": "physical function", "grain": "[grain name]", "name": "[component]", "evidence": "[path, or unverified: why]", "retired": false}
{"kind": "link", "at": "[time]", "from": "process-1", "to": "function-1", "rel": "means-of", "retired": false}
{"kind": "link", "at": "[time]", "from": "process-1", "to": "process-2", "rel": "part-of", "retired": false}
{"kind": "actor", "at": "[time]", "id": "actor-1", "name": "[who]", "type": "[person or agent]", "acts_on": ["process-1"], "sees": ["function-1"], "retired": false}
{"kind": "open", "at": "[time]", "id": "open-1", "text": "[the gap or question]", "about": ["function-1"]}
{"kind": "answer", "at": "[time]", "q": "open-1", "text": "[the answer]", "by": "[who answered]"}
{"kind": "result", "at": "[time]", "text": "[a finding and the nodes it names]"}
```
