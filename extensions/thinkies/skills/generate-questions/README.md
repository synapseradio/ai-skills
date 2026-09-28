# generate-questions

Compose a set of questions toward one driving question and return it as a written inquiry, without asking anyone: read what the questions will land in and list the facts they rest on, name the driving question, keep only the questions that pass the rung test (relevance and discrimination) and the four clarity laws, weigh each against the moves that are not questions, name the end state that closes the inquiry, and return the rungs in the order to ask them, each with what its answer decides, the follow-up each kind of answer opens, and the move to make instead if it falls flat. A spawned agent can run it, and whoever holds the inquiry can ask or answer it without the conversation that produced it.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/generate-questions/` into `~/.claude/skills/generate-questions/`.

## Usage

```
/generate-questions <what the questions must find out>
```

## Records

When loaded from the thinkies Claude Code plugin, the skill saves a record of each run to the plugin store at `${CLAUDE_PLUGIN_DATA}/records/`, and copies it to the Records mirror folder when that optional setting names one. Uninstalling the plugin deletes the store unless you run `claude plugin uninstall thinkies@ai-skills --keep-data`. Loaded anywhere else, the skill prints the record in its reply for you to keep.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`generate-questions.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/generate-questions.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
