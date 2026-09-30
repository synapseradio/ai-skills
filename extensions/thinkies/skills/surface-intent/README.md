# surface-intent

A skill for the moment before you add, change, or produce something. It runs two
beats. First, surface the intent already there: read what the system does about your
purpose before you write, and diff against it, so you sharpen what exists instead of
adding a duplicate. Second, surface your own intent: name things for what they are,
prefer one named root over a trail of pointers, and make the output clear enough for
its reader to act on. The bug it was built to prevent is the everyday one — adding a
thing that already existed because nobody looked first.

## Try it when

- You're about to add a rule, a helper, a setting, or a page to something you haven't read all of.
- A request names its solution ("add a dark mode") and nobody has checked whether something already does the job.
- What you produce will be acted on by someone who wasn't in the room.

## What you get back

A one-line statement of the change and its purpose, a record of what was searched and what turned up, a verdict of covered, partly covered, or not covered (or unknown, when nothing could be read), and what you know, what you're assuming, and what's unknown, kept in separate lists. Then the output itself, written so its reader can act on the first read.

Trimmed from a run on "Add a dark mode to our grandmother's recipe website.", where the site itself couldn't be reached ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/surface-intent/grandmas-dark-mode.md)):

> - the host or site builder: many website builders and blog templates ship a dark theme as a setting, so "add" may mean "switch on";
>
> […]
>
> Verdict: **unknown**. I am not entitled to write "not covered", so I do not proceed to build. The next step is one read of the site, not a design.
>
> […]
>
> The failure mode to avoid here is the middle pile passing for the first. "I assume nothing covers this" is not "I read the site and nothing covers this."

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/surface-intent/` into `~/.claude/skills/surface-intent/`.

## Usage

```
/surface-intent <what you are about to add or change>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`surface-intent.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/surface-intent.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
