# decision-analysis

Formulate and evaluate one concrete decision under uncertainty, the way decision analysis prescribes: specify the four components of the decision problem (states, acts, consequences, preferences), screen for dominance, classify the uncertainty as risk, ambiguity, or unawareness, evaluate under the rule that classification licenses, and report sensitivity and the value of gathering information before deciding.

The skill holds the line of reasoning and nothing about layout. How the result is laid out follows the request.

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

The skill needs someone who can answer its questions. In a run with no one to ask, it returns the questions it still has and stops.

## What a run looks like

The skill asks for your options, the facts outside your control, what each option would mean in each case, and how you rank the outcomes. It then gives the acts and states, what each option means in each state in your own words, which option is dominated, how uncertain the probabilities really are, the recommendation, and the thresholds at which it would flip.

Trimmed from a staged conversation, the user's side played by a second agent, on adopting a second dog eight months before a year abroad that might not happen ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/decision-analysis/second-dog-before-abroad.md)). The run was made with an earlier version of the skill that also fixed the layout of the result, so it is more formal than a run returns now. The couple, the friend who can foster one dog, and every probability and score are the played user's inventions:

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

The entries below are carried over as written from the skill's earlier reference files:

- L. J. Savage, *The Foundations of Statistics* (1954) — states, acts, and consequences as the components of a decision problem; every formulation restricts the world it describes.
- J. von Neumann & O. Morgenstern, *Theory of Games and Economic Behavior* (1944) — outcomes as the objects preferences range over; when a ranking can carry numbers.
- H. Raiffa & R. Schlaifer, *Applied Statistical Decision Theory* (1961) — evaluating an observe-then-decide act by working through what each observation would lead you to do.
- D. Ellsberg, "Risk, Ambiguity, and the Savage Axioms" (1961) — the distinction between risk and ambiguity.
- I. Gilboa & D. Schmeidler, "Maxmin Expected Utility with Non-Unique Prior" (1989) — ranking by the worst expected value over a set of distributions.
- I. Gilboa & D. Schmeidler, "Case-Based Decision Theory" (1995) — ranking acts by their outcomes in similar past cases.
- E. Karni & M.-L. Vierø, "Reverse Bayesianism" (2013) — revising when a previously unlisted state arrives.
- T. Seidenfeld & L. Wasserman, "Dilation for Sets of Probabilities" (1993) — new evidence can widen the set of defensible distributions.
- I. J. Good, "On the Principle of Total Evidence" (1967) — cost-free information cannot hurt in expectation, within a fixed formulation.
- K. Binmore, *Rational Decisions* (2009) — why small, revisable commitments suit decisions whose states cannot all be listed.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`decision-analysis.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/decision-analysis.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
