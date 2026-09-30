# strategize

Adaptive multi-phase reasoning for complex problems. Three phases — understand, reason loop, exit — with user-controlled continuation, pivoting, and completion signals.

## Call on it when

- A problem has several constraints tangled together, and you want to work through it with someone rather than get one answer.
- You don't yet know which constraint matters most.
- You want to steer as it goes: continue, change angle, or stop when you've got enough.

## How it goes

It breaks the problem at its joints, states its understanding, and waits for you to confirm it. Then it reasons in rounds, each applying at least one named technique (surfacing assumptions, hunting defeaters, testing the contrapositive, weighing evidence), and after each round you say continue, pivot, or done. On done it sums up what was explored and concluded, what transfers beyond this problem, and what stays unresolved.

Trimmed from a staged conversation on a four-person band with one van, two weeks, six gigs in three countries, a clutch repair nobody has priced, and a drummer who can only leave on day three ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/strategize/band-van-tour.md)). A second agent played a member of the band:

> **Skill:** The first-date defeater is gone: a flat two-hour drive to an 8pm slot survives a slipping clutch. It leaves a different reading of the plan. Days one and two hold no gigs, and a clutch repair does not need the drummer. Those two free days are the only window in the whole tour where a repair costs no gig, so the repair is a question of using them, not of finding time.
>
> […]
>
> **User (played):** I haven't asked any garage yet. We can put about 600 euros into the repair before the gig fees have to cover it. I haven't told you where the hills are, so I can't say whether your read of the route is right.
>
> **Skill:** You are right to flag that. I wrote "days 9, 11 and 13 if I read the route right" and you never told me the hills are in Germany. I had inferred it from gig order alone. I drop that claim; where the hills fall is now an open question, and it is one you can answer from the route.
>
> […]
>
> Set the decision rule before the price arrives: name the result that means "repair" and the result that means "rent", so a late number does not reopen the whole plan.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/strategize/` into `~/.claude/skills/strategize/`.

## Usage

```
/strategize <task or question>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`strategize.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/strategize.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
