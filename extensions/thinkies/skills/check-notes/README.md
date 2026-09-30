# check-notes

Find saved notes and run records by topic, skill, date, or project, and play them back in readable form: search the record file names for the skill, time range, and topic asked for, search the files' text when the names leave nothing or too much, play each kept record back newest first with its path, and name the file an earlier run would resume from.

## It helps when

- You remember working something out earlier and want the finding back, not a rerun.
- You want the recent records on a topic, a skill, or a project, in one place.
- You want to pick up an earlier run where it stopped.

## You get back

How the search went, then each matching record played back, newest first, with its path: its subject, notes, results, and open items. It ends by naming the file a run would resume from.

Trimmed from a run on "What did I find out about the dishes in the flat?" ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/check-notes/dishes-by-the-kettle.md)):

> **Search the names.** The note store holds one file, `save-note_20260929T230925Z_drying-rack-by-kettle.jsonl`. Split at its underscores, it reads skill `save-note`, time `20260929T230925Z`, topic `drying-rack-by-kettle`. The request names no skill or date, and the topic shares no word with "dishes" or "flat", so the names keep nothing.
>
> **Search the contents.** Searching the files' text for "dishes" and "flat" keeps that one file, which holds both words.
>
> […]
>
> **Subject:** In a shared flat where the dishes never get done, moving the drying rack next to the kettle worked where a rota would not, because whoever waits for the kettle puts dishes away.
>
> […]
>
> **Open**
>
> - open-1: Does the effect hold for the flatmates who do not drink tea or coffee, and so never wait at the kettle?

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/check-notes/` into `~/.claude/skills/check-notes/`.

## Usage

```
/check-notes <topic, skill, date, or project>
```

## Records

In the thinkies Claude Code plugin, check-notes reads records from the plugin's store, `${CLAUDE_PLUGIN_DATA}/records/`, and from the **Records mirror folder** when one is set, for any record the store lacks. Claude Code deletes the store when the plugin is uninstalled, unless you uninstall with `claude plugin uninstall thinkies@ai-skills --keep-data`; the mirror folder stays either way. Outside the plugin there is no store, and check-notes plays back a record pasted into the conversation.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`check-notes.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/check-notes.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
