# run-premortem

Imagine the plan has already failed catastrophically and work backwards — generate failure modes, surface hidden assumptions, and design interventions for the most dangerous.

## Use it before

- You commit to a plan that has one shot: a launch, an event, a move, a surprise.
- Everyone involved is optimistic and nobody has said out loud how it could go wrong.
- A plan rests on something no one controls, and you haven't named what.

## What it hands back

A headline for the failure, the path back from it, failure modes listed without censoring across technical, human, process, external, and timing lines, the assumptions the plan took for granted, the modes grouped by theme and checked against what the plan already covers, and interventions for the most dangerous themes.

Here it is on a surprise 70th birthday party held in Grandpa's own house while he is out at the barber for an hour, cut down ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/run-premortem/surprise-party-at-home.md)):

> **"70th Birthday Surprise Ends in Ambulance: Grandpa, Home Early From Barber, Finds Twenty Strangers' Cars Blocking His Drive and a Crowd in His Dark Living Room"**
>
> […]
>
> Underneath all six sits one shared root: the plan has one fixed event (one hour) resting on one variable (Grandpa's schedule) that nobody controls, and nobody has asked the person it is for.
>
> […]
>
> - Cut the shout. Guests greet him quietly, or one at a time, or he is met at the door by one person he knows who walks him in. This removes the startle without removing the surprise.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/run-premortem/` into `~/.claude/skills/run-premortem/`.

## Usage

```
/run-premortem <plan or decision>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`run-premortem.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/run-premortem.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
