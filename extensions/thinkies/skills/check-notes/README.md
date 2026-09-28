# check-notes

Find saved notes and run records by topic, skill, date, or project, and play them back in readable form: search the record file names for the skill, time range, and topic asked for, search the files' text when the names leave nothing or too much, play each kept record back newest first with its path, and name the file an earlier run would resume from.

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
