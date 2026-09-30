# generate-questions

Compose a set of questions toward one driving question and return it as a written inquiry, without asking anyone: read what the questions will land in and list the facts they rest on, name the driving question, keep only the questions that pass the rung test (relevance and discrimination) and the four clarity laws, weigh each against the moves that are not questions, name the end state that closes the inquiry, and return the rungs in the order to ask them, each with what its answer decides, the follow-up each kind of answer opens, and the move to make instead if it falls flat. A spawned agent can run it, and whoever holds the inquiry can ask or answer it without the conversation that produced it.

## Reach for it when

- A decision needs other people's answers, and you want the questions ready before anyone sits down.
- Someone else will do the asking, and has to work from the page alone.
- You keep asking "what do you think?" and getting nothing you can use.

## What you'll get

An inquiry you can hand over: the facts it rests on, the driving question, and the questions in the order to ask them. Each question comes with what its answer decides, where each kind of answer leads next, and what to do if it falls flat. A last line says when the inquiry is finished. Nobody is asked anything during the run.

From a run on "Should our book club let in a robot?" ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/generate-questions/robot-in-the-book-club.md)), two of its nine questions and the closing condition:

> 1. Which of those things could the robot do itself?
>    - Decides: whether the robot would be a member or a guest with a title.
>
> […]
>
> 1. What, if anything, would change for you at a meeting with the robot there?
>    - Decides: whether any member's yes or no is the one that closes the inquiry.
>    - If the answer is "nothing I'd notice": that member's vote is a plain yes, and the inquiry moves to the next member.
>    - If the answer names a change: ask "What would you want to be true for that to be fine?" and record the condition as the price of that member's yes.
>    - If the answer is that they would stop coming: stop the inquiry and give the decision to the club as a statement: "Admitting it would cost us this member." Do not push past it.
>
> […]
>
> **Done when:** the person or group named at rung 3 can state yes, no, or one trial meeting, with a reason tied to the club's purpose from rung 1 and any condition from rungs 7 and 8 written next to it.

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
