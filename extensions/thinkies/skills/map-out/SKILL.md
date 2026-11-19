---
name: map-out
description: Use to get oriented in an unfamiliar or muddled subject when the move it needs is still unclear. Locates the subject among its parts and wholes, purposes, kinds, and peers, and settles the level to act at.
compatibility: >-
  Runs without file access. A save writes a record when loaded from the
  thinkies Claude Code plugin; elsewhere the record goes in the reply for the
  user to keep.
---

# Map out

Locate a subject along four axes, part and whole, purpose and means, kind and case, and peers at one level, then choose the level to act at. Open with the move the thinking lacks most, add a move only while the output quotably calls for one, and converge on a position.

## Phase 0: Assess

Read what the thinking lacks from the request and the conversation, and open with the matching move. When several rows fit, take the topmost. When the request is a bare subject and no row fits, open with situate, since nothing yet says what the subject is for. Proceed without announcing the pick.

| The thinking lacks | Signal | Open with |
|---|---|---|
| A level, under time pressure | Drowning in detail, or too abstract to act on | select-level |
| A purpose | No one can say what it is for or why it matters | situate |
| Parts | It is handled as one lump | decompose |
| A whole | Pieces are in hand with no sense of what they make together | compose |
| Grounding | A claim, principle, or plan has no concrete case | instantiate |
| Transfer | It looks new, and nothing known seems to apply | generalize |
| Alternatives | One option is in view at this level | survey-peers |

## Phase 1: Move

Read the move's file from [references/](references/), answer its numbered questions against the subject, and carry each move's output into the next.

| Move | File |
|---|---|
| select-level | `select-level.md` |
| situate | `situate.md` |
| decompose | `decompose.md` |
| compose | `compose.md` |
| instantiate | `instantiate.md` |
| generalize | `generalize.md` |
| survey-peers | `survey-peers.md` |

## Phase 2: Place and extend

After each move, say where the subject now sits on each axis the move touched: the whole it belongs to, the purpose it serves, the class it falls in, the peers beside it. Where one move shifted two axes at once, say which two.

Then check everything produced so far, and extend when a row fires. When several fire, take the topmost. When none fires, converge.

| The output so far shows | Extend with |
|---|---|
| Two moves disagree about which level matters | select-level |
| A part or mechanism whose purpose no one has stated | situate |
| A whole named but never cut into parts | decompose |
| Parts named with nothing said about what they make together | compose |
| A claim or principle with no concrete case | instantiate |
| A case with no class named | generalize |
| One option at a level where others could exist | survey-peers |

1. **Quote to extend.** Count a row as fired only by quoting the sentence of the output that fires it. A row you can only paraphrase has stayed silent.
2. **Stop when the picture stops changing.** When the last move added nothing you can quote as new, converge, even if a row fires.
3. **Cap at five.** A run holds at most five moves. At the cap, converge.

Write the walk as prose for a reader who wants the subject placed. For each move, state what it found and what in the subject shows it, then name the gap in that finding that the next move fills. Move names and table labels stay out of the output, because the reader follows the subject and has no use for the method's vocabulary. Tie each claim to the subject material or mark it as an assumption.

## Phase 3: Converge

Close with:

- Where the subject sits: the whole it belongs to, the purpose it serves, the class it falls in, its nearest peers
- The level to act at, and what acting there makes possible
- What each move changed in the picture
- What stays open

## Context loading

| Phase | Load |
|---|---|
| Assess | Nothing from references |
| Move, place and extend | Only the current move's file |
| Converge | Nothing additional |

## Record

Hold the run's record in mind as you work: the subject, what was given, the notes, the results, and what stays open. Those parts organize the thinking, and the reply gives them in prose. A plain run ends there: it writes no file, shows no record lines, and says nothing about saving.

Save the record only when the user asks to save or keep the run, or resumes a saved one. The rest of this section applies only then.

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

Record the subject; the position after each move as a note, with no move name in it; each closing item as a result; and each thing left open as an open line.

File: `map-out_[start time, UTC, YYYYMMDDTHHMMSSZ]_[topic].jsonl`

```jsonl
{"kind": "run", "at": "[time, UTC, YYYY-MM-DDTHH:MM:SSZ]", "skill": "map-out", "topic": "[topic]", "subject": "[the subject]", "project": "[repository or project name, or empty]", "resumed": false}
{"kind": "note", "at": "[time]", "text": "[where the subject sits after this move, on each axis the move touched]", "context": "[what the move found that placed it there]"}
{"kind": "result", "at": "[time]", "text": "[a closing item]"}
{"kind": "open", "at": "[time]", "id": "open-1", "text": "[what stays open]", "q": ""}
```
