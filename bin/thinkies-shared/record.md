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
