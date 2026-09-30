# instantiate

Test an abstraction by making it concrete: build the typical case its author had in mind, build a case the wording covers but its author likely did not picture, apply the abstraction to each and record where it holds, bends, or says nothing, then name each unstated condition as the clause the abstraction would need to carry it.

## When it helps

- A value, a policy or a principle sounds agreed, and you suspect everyone pictures something different.
- A rule works for the case it was written for, and you want to see where it stops working.
- You are writing a principle and want to find its missing clauses before someone else does.

## A run, trimmed

The run builds two concrete cases with names, ages and clock times: the one the author most likely pictured, and one the wording covers but the author likely didn't. It applies the abstraction to both, notes where it holds, bends, or says nothing, and turns each unstated assumption into the clause the abstraction would need.

On "Our family values punctuality." ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/instantiate/family-punctuality.md)), where the second case is a 28-person reunion at a lake house:

> In the second household it holds only vacuously for the host's invitation. "Around two" names no time to be punctual to, so anyone arriving between 1:30 and 2:30 has met it or missed it depending on who is counting.
>
> […]
>
> - Assumed: the value binds the people who set the schedule. Clause needed: "Parents are held to the same times as children, and where a parent cannot meet one, the parent says so before it passes."
>
> […]
>
> - Assumed: everyone can move at the same speed. Clause needed: "Where a member needs more time to be ready, because of age, health, shift work, or a young child, the family moves the departure time for everyone instead of asking that member to move faster."

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/instantiate/` into `~/.claude/skills/instantiate/`.

## Usage

```
/instantiate <subject>
```

## Sources

- Tversky, B. (1989). [Parts, partonomies, and taxonomies](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/1989_Tversky_Partspartonomiesandtaxonomies.pdf).
- Vallacher, R. R., & Wegner, D. M. (1987). What do people think they're doing? [doi:10.1037/0033-295X.94.1.3](https://doi.org/10.1037/0033-295X.94.1.3).

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`instantiate.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/instantiate.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
