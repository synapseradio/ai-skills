# research-and-teach

Research a topic deeply, then teach it progressively from simple truths to complex nuances. Five phases: scope, research, structure, teach, persist.

## Call on it when

- You want to understand why something happens, not just be told its name.
- You have little background in the field and need an explanation that starts where you are.
- You want to know which parts of an explanation are established and which are still guesses.

## What it hands back

A short scoping exchange about what you want to be able to do and what you already know, a list of the sources consulted with what each one settled, then teaching in layers. Each layer ends with a check question, and the next layer builds on your answer. It marks where the evidence stops.

A staged conversation on "Why do onions make you cry?", trimmed ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/research-and-teach/crying-onions.md)). The user's side was played by a second agent, which invented the learner: a home cook with secondary-school chemistry:

> An intact onion holds no tear gas. It keeps two things in separate compartments inside its cells: a sulfur-bearing compound it drew up from the soil, and enzymes (proteins that speed up one specific reaction). Your knife breaks the compartments, the two meet, and the enzymes turn the compound into a small, light molecule that evaporates into the air.
>
> […]
>
> So one fragment reaches a fork: flavour if it reacts with itself, tears if the second enzyme gets it first.
>
> […]
>
> **User (played):** The first enzyme does the snip. It cuts the fragment off the sulfur compound. The second enzyme does the rearrangement, reshuffling that fragment into the stinging molecule. If you switched the second enzyme off, I'd guess the fragment would mostly react with itself, so the onion would still taste sharp and might even taste stronger, but the tears would mostly stop.
>
> […]
>
> Treat the exact receptor step as likely, not settled.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/research-and-teach/` into `~/.claude/skills/research-and-teach/`.

## Usage

```
/research-and-teach <topic to research and explain>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`research-and-teach.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/research-and-teach.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
