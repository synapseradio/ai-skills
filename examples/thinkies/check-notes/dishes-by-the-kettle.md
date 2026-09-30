# check-notes: what I found out about the dishes in the flat

- skill: check-notes, from commit 0c9258f
- subject: What did I find out about the dishes in the flat?
- kind: single run

## Prompt

/check-notes What did I find out about the dishes in the flat?

## Run

**Search the names.** The note store holds one file, `save-note_20260929T230925Z_drying-rack-by-kettle.jsonl`. Split at its underscores, it reads skill `save-note`, time `20260929T230925Z`, topic `drying-rack-by-kettle`. The request names no skill or date, and the topic shares no word with "dishes" or "flat", so the names keep nothing.

**Search the contents.** Searching the files' text for "dishes" and "flat" keeps that one file, which holds both words.

### save-note · drying rack by kettle · 2026-09-30 01:09

Saved to the note store, as `save-note_20260929T230925Z_drying-rack-by-kettle.jsonl`.

**Subject:** In a shared flat where the dishes never get done, moving the drying rack next to the kettle worked where a rota would not, because whoever waits for the kettle puts dishes away.

**Notes**

- In a shared flat where the dishes never got done, the leverage point was not a rota but moving the drying rack next to the kettle. Whoever waits for the kettle puts dishes away. (The problem was dishes left undone in a shared flat. A rota would have asked people to remember a duty; the rack move attaches the task to a wait that already happens.)

**Open**

- open-1: Does the effect hold for the flatmates who do not drink tea or coffee, and so never wait at the kettle?
- open-2: Does the rack by the kettle put away only the dishes that are already dry, and who clears the wet ones?

**Continue.** A run would resume from `save-note_20260929T230925Z_drying-rack-by-kettle.jsonl` in the note store: it reads that file and appends to it, for instance an answer to open-1 or open-2.
