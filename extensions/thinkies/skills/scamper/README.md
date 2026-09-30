# scamper

Structured ideation using the SCAMPER creative thinking technique — seven systematic lenses for exploring a problem space: Substitute, Combine, Adapt, Modify, Put to another use, Eliminate, Reverse.

## When to use this

SCAMPER works best when you have a concrete thing — a product, a workflow, a feature — and want to explore variations. It is less useful for greenfield problems where nothing exists yet. If you need to brainstorm from scratch, start with a plain conversation to establish the thing first, then run SCAMPER on it.

## How a session runs

It opens by restating what you mean and waits for you to confirm it. Then it runs each of the seven lenses over the thing, gathers the ideas into groups, and asks which to develop. Your pick sends it back to the restating step for the new direction, and the cycle repeats until you have something worth building.

Trimmed from a staged conversation on "The humble umbrella." ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/scamper/the-umbrella.md)). A second agent played the user, and brought the problems it cared about: umbrellas failing in wind and getting left on trains.

> **Skill:** Noted: the trade-off is the spine. Wind-proofing tends to add weight, weight raises the chance of leaving it behind, so each idea below says how it stands on both.
>
> **S, Substitute**
>
> 1. Replace the metal-rib frame with a single flexible carbon or fibreglass hoop and a tensioned fabric shell. The canopy flexes and springs back instead of inverting. Lighter than steel ribs, so it helps both problems.
>
> […]
>
> 1. Reverse the canopy orientation: an umbrella worn over the shoulders, or a hood on a rigid rim, hands free and attached to your body. Cannot be left on a train because you are wearing it.
>
> **Converged view.** Three groups. Structure (1, 5, 7, 11) answers wind and often lightens. Attachment (2, 3, 4, 8, 14) answers forgetting and adds little weight. System (6, 10, 12, 9) changes who owns the problem.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/scamper/` into `~/.claude/skills/scamper/`.

## Usage

```
/scamper How might we improve our onboarding flow?
/scamper Rethink the notification system for mobile users
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`scamper.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/scamper.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
