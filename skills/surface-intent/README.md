# surface-intent

A skill for the moment before you add, change, or produce something. It runs two
beats. First, surface the intent already there: read what the system does about your
purpose before you write, and diff against it, so you sharpen what exists instead of
adding a duplicate. Second, surface your own intent: name things for what they are,
prefer one named root over a trail of pointers, and make the output clear enough for
its reader to act on. The bug it was built to prevent is the everyday one — adding a
thing that already existed because nobody looked first.

## See also

These skills sit next to Surface Intent and do related but distinct work.

- **`communicate`** — how to phrase and structure prose for an audience, avoiding
  slop. Surface Intent decides *whether* a thing should exist and whether its intent
  is legible; `communicate` polishes the prose once you are writing it.
- **`prompt`** — lints and sharpens LLM instructions specifically, including by
  truth-conditions. Surface Intent applies the same look-before-you-add discipline
  to anything — rules, code, designs, names — not only prompts.
- **`scout`** — a reconnaissance agent that maps a codebase landscape and reports
  high-value targets. Surface Intent's Beat 1 is the same instinct in the small, run
  by you before a single change, ending in a sharpen / extend / add decision.
- **`thinkies/assess-current-knowledge`** — the known / assumed / unknown split as a
  standalone thinking move. Surface Intent borrows it inside Beat 1 to keep
  assumptions from masquerading as facts during the survey.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/surface-intent/` into `~/.claude/skills/surface-intent/`.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`surface-intent.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/surface-intent.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
