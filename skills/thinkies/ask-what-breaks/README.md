# ask-what-breaks

Find defeaters that would break a conclusion. Distinguishes undercutting from rebutting defeaters, hunts both kinds, and grades each by strength.

## It helps when

- You have reached a conclusion and want to know what would overturn it before you rely on it.
- A causal story fits the facts suspiciously well.
- You need a test to run, not just a doubt to voice.

## What you'll get

The claim restated so it can fail, the links in its chain of reasoning, and two kinds of defeater. An undercutting defeater attacks a link: a premise, a source, or an inference. A rebutting defeater is an observation that would contradict the conclusion outright, written as "seeing X would defeat this". Each defeater is graded as a weakener, which lowers confidence, or a destroyer, which forces a rebuild.

Excerpts from a run on "Our sourdough starter is thriving because we play it jazz" ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/ask-what-breaks/jazz-sourdough.md)):

> - **Seeing an unmusical starter match it.** Split the starter into two matched jars: same flour, same ratio, same feeding time, same temperature, same lid, the same shelf if possible. One jar gets jazz, one gets silence, over at least several feeding cycles. If the silent jar's rise height and time to peak match the jazz jar's within the day-to-day spread you see in either jar alone, the claim is defeated.
> - **Seeing the effect reverse under swapped conditions.** Swap which jar hears the music halfway through. If the thriving follows the jar rather than the music, something about the jar, its history or its culture, explains it. If it follows the music, the claim gains real support.
> - **Seeing a different sound do as well.** Play the jar something else at equal volume: a podcast, static, a bass tone. If any sound produces the same result, the effect (if there is one) belongs to vibration or to human presence, not to jazz.
>
> […]
>
> **Cheapest test that most moves the estimate:** two matched jars, one with jazz and one silent, on the same shelf, for two weeks, with rise height marked on each. If the jazz jar wins consistently, the claim is worth chasing. If the two jars match, the starter is thriving for reasons the household already provides, and the music is for the household.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/ask-what-breaks/` into `~/.claude/skills/ask-what-breaks/`.

## Usage

```
/ask-what-breaks <conclusion to stress-test>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`ask-what-breaks.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/ask-what-breaks.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
