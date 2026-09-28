---
name: map-out
description: 'Find where a subject sits and the level to act at, by moving along its axes: parts and
  wholes, purposes and means, kinds and cases, and peers at the same level. Use when asked to map
  out an idea or topic in the sense of getting oriented in it, or asked where does this fit, what
  is this part of, what is it for, what is this an example of, what else does the same job, zoom in,
  zoom out, or at what level to think about something; also when lost in detail or stuck too abstract
  to act. Produces a spoken walk and a record of it. It does not draw diagrams or charts, does not
  produce a plan, schedule, or task list, and does not build a lasting model of a system.'
---

# Map out

Locate a subject along four axes, part and whole, purpose and means, kind and case, and peers at one level, then choose the level to act at. Open with the move the thinking lacks most, add a move only while the output quotably calls for one, and converge on a position.

## Phase 0: Assess

Read what the thinking lacks from the request and the conversation, and open with the matching move. When several rows fit, take the topmost. Proceed without announcing the pick.

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

Then check everything produced so far, and extend when a row fires. When several fire, take the topmost.

| The output so far shows | Extend with |
|---|---|
| Two moves disagree about which level matters | select-level |
| A part or mechanism whose purpose no one has stated | situate |
| A whole named but never cut into parts | decompose |
| Parts named with nothing said about what they make together | compose |
| A claim or principle with no concrete case | instantiate |
| A case with no class named | generalize |
| One option at a level where others could exist | survey-peers |

1. **Quote to extend.** Count a row as fired only by quoting the sentence that fires it.
2. **Stop at fixpoint.** When the last move added nothing you can quote as new, converge, even if a row fires.
3. **Cap at five.** A run holds at most five moves.

Write flowing prose that shows the reasoning as it forms: what each move found, and why it led to the next. Move names and table labels stay out of the output. Tie each claim to the subject material or mark it as an assumption.

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
| Converge | `assets/playback.md` |

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

Record the subject; the position after each move as a note, with no move name in it; each closing item as a result; and each thing left open as an open line.

File: `map-out_[start time, UTC, YYYYMMDDTHHMMSSZ]_[topic].jsonl`

```jsonl
{"kind": "run", "at": "[time, UTC, YYYY-MM-DDTHH:MM:SSZ]", "skill": "map-out", "topic": "[topic]", "subject": "[the subject]", "project": "[repository or project name, or empty]", "resumed": false}
{"kind": "note", "at": "[time]", "text": "[where the subject sits after this move, on each axis the move touched]", "context": "[what the move found that placed it there]"}
{"kind": "result", "at": "[time]", "text": "[a closing item]"}
{"kind": "open", "at": "[time]", "id": "open-1", "text": "[what stays open]", "q": ""}
```
