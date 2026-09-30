# assess-current-knowledge

Map what's known vs assumed vs unknown. Separates verified from assumed, surfaces gaps, weighs readiness against risk, and identifies what would close critical gaps.

## Worth running when

- You are about to start something and cannot say which of your beliefs you have actually checked.
- A plan feels ready, and a wrong assumption would be expensive.
- You need to decide what to verify first and what can ride.

## What a run looks like

Four lists: verified facts, known unknowns, what you likely know but have not applied, and blind spots. Then the source behind each item, the gaps split into those investigation can close and those that stay as acknowledged uncertainty, the cost of being wrong set against the effort of checking, the checks that would change the decision, in order, and where the assessment's own competence ends.

Trimmed from a run on a first-time host roasting a turkey for 14 people tomorrow ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/assess-current-knowledge/first-turkey.md)):

> **Known unknowns**
>
> Each is a question I know to ask and cannot answer from what you said.
>
> 1. Is the turkey frozen, fresh, or partly thawed right now? This decides everything else. By the thawing page's own figures, a frozen bird cannot thaw in a refrigerator by tomorrow. […]
>
> […]
>
> ### 4. Readiness against risk
>
> - Cost of being wrong on doneness or thaw: serious. Undercooked poultry is a food-safety failure for 14 people, and a frozen center means a late meal. Demand direct verification here: a thermometer reading, and a touch test on the bird.
> - Cost of being wrong on flavor, presentation, or side timing: low. Proceed with acknowledged uncertainty. A bird that is a bit dry or a side that is late costs a bad hour and nothing more.
> - Cost of being wrong on oven fit: medium and cheap to verify. Check it today, since finding out at 3 pm tomorrow leaves no options.
>
> Verify the high-consequence items and let the rest ride.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/assess-current-knowledge/` into `~/.claude/skills/assess-current-knowledge/`.

## Usage

```
/assess-current-knowledge <context or topic>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`assess-current-knowledge.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/assess-current-knowledge.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
