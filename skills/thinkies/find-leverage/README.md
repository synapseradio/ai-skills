# find-leverage

Trace a system's feedback loops to locate where a small change shifts the whole — bottlenecks, amplification points, compounding effects, root causes — and name the single highest-leverage intervention.

## Worth running when

- The same problem keeps coming back after every fix, and each fix takes more effort than the last.
- A solution worked for a week and then quietly died.
- You can afford one change and want the one that keeps working without anyone pushing it.

## What comes back

The loops that keep the problem going, the bottlenecks, the points where one change reaches everything, what compounds over time, the root causes, a table of candidate fixes scored by what each shifts against the effort to keep it going, and one named intervention with the setup it needs and the first signs it is failing.

Here it is on a shared flat of four where the dishes never get done and two rotas have died, cut down ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/find-leverage/flat-dishes.md)):

> 1. **A dish in the sink belongs to nobody.** Ownership stops at the moment the dish leaves the hand, which produces the free-rider loop, the failed rotas (nobody can be held to account for a pile), and the belief that the others do not wash.
>
> […]
>
> The last candidate scores highest because the structure does the work of the rota. A rota needs four people to remember, and personal crockery needs each person to want a clean plate at their next meal, which they already do.
>
> […]
>
> - **The shortage lands on the person who made it.** Someone who leaves their plate has no plate at their next meal, and no one else is short. The paper-plate purchase stops making sense, because nobody else has a reason to buy them.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/find-leverage/` into `~/.claude/skills/find-leverage/`.

## Usage

```
/find-leverage <system or problem>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`find-leverage.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/find-leverage.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
