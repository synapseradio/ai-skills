# decision-analysis

Formulate and evaluate one concrete decision under uncertainty, the way decision analysis prescribes: specify the four components of the decision problem (states, acts, consequences, preferences), screen for dominance, classify the uncertainty as risk, ambiguity, or unawareness, evaluate under the rule that classification licenses, and report sensitivity and the value of gathering information before deciding.

The output is an analysis record — a structured, checkable artifact — not an essay. Theory and citations appear only when asked for, after the analysis.

## Try it when

- One choice is on the table, the outcome turns on facts you don't control, and you keep going round in circles.
- You suspect "wait and see" is either the wise move or an expensive habit, and want to know which.
- You want to know which guess, if it turned out wrong, would change the answer.

## Usage

Bring one decision, already on the table, for a single decision maker:

> Analyze this decision: we can renew our office lease for 3 years at current rates, or go month-to-month at +30%.

> I got into two grad programs. Structure this decision for me.

> Should we ship the rewrite now or run it dark for another quarter? What kind of uncertainty is this?

> Should I decide now or learn more first? The deadline is Friday.

Afterward, ask for the extras:

> Show me the picture.

> Now explain the theory behind what you just did.

## What a run looks like

The skill asks, one round at a time, for your options, the facts outside your control, what each option would mean in each case, and how you rank the outcomes. It then returns the record: the acts and states, a consequence table in your own words, which option is dominated, how uncertain the probabilities really are, the recommendation, and the thresholds at which it would flip.

Trimmed from a staged conversation, the user's side played by a second agent, on adopting a second dog eight months before a year abroad that might not happen ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/decision-analysis/second-dog-before-abroad.md)). The couple, the friend who can foster one dog, and every probability and score are the played user's inventions:

> A2 is dominated by A3, using only the ordering. In every state A3's outcome is at least as preferred as A2's, and strictly preferred in s1 to s4:
>
> […]
>
> Recommendation: decide now. The observation that would settle the most sensitive input is the dogs' compatibility, and A3 already collects it: the foster trial is a direct observation of the actual pair. […] Waiting for the posting decision at month 3 buys nothing for this choice, and costs three lonely months for the current dog in every state.
>
> […]
>
> Choose A3: foster a rescue dog now, adopt it if the dogs are compatible, return it if they clash.

## What it declines

Strategic interaction with other optimizing agents, multi-party negotiation, and ongoing policy optimization fall outside the method. Multi-stage decisions qualify when they can be framed as decide, observe, decide.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/decision-analysis/` into `~/.claude/skills/decision-analysis/`.

## Sources

- Howard, R. A. (1966). Decision analysis: Applied decision theory. In D. B. Hertz & J. Melese (Eds.), *Proceedings of the Fourth International Conference on Operational Research* (pp. 55–71). The venue and pages come from a reference list (<https://link.springer.com/rwe/10.1007/978-1-4419-1153-7_1161>), not from the paper itself.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`decision-analysis.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/decision-analysis.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
