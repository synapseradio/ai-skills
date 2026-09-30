# save-note

Save an insight from the conversation as a note that can be found again by topic, date, or project: state the insight in one to three sentences a reader without the conversation can follow, say what was being worked on and what led to it, name its topic in two to six words, then write the record and play it back.

## When it's worth a note

- Something clicked mid-conversation and you'll want it again in a month, without the conversation around it.
- A finding turned up outside any structured run and has nowhere else to go.

## The note, played back

The note comes back as you'd find it later: a one-line subject, the insight with the context that produced it, and the questions it leaves open.

From a run on "in a shared flat where the dishes never get done, the leverage point was not a rota but moving the drying rack next to the kettle" ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/save-note/dishes-by-the-kettle.md)):

> **Subject:** In a shared flat where the dishes never get done, moving the drying rack next to the kettle worked where a rota would not, because whoever waits for the kettle puts dishes away.
>
> […]
>
> - open-1: Does the effect hold for the flatmates who do not drink tea or coffee, and so never wait at the kettle?
> - open-2: Does the rack by the kettle put away only the dishes that are already dry, and who clears the wet ones?

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/save-note/` into `~/.claude/skills/save-note/`.

## Usage

```
/save-note <insight to save>
```

## Records

When the skill is loaded from the thinkies Claude Code plugin, each note is saved as a record in the plugin store at `${CLAUDE_PLUGIN_DATA}/records/`. The optional Records mirror folder, set when enabling the plugin or in `/config`, receives a copy of every record. Uninstalling the plugin deletes the store unless you run `claude plugin uninstall thinkies@ai-skills --keep-data`; the mirror stays. Elsewhere, the skill prints the record in its reply as a `jsonl` block for you to keep.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`save-note.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/save-note.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
