---
name: decision-analysis
description: 'Apply decision analysis (Howard 1966): systematically formulate and evaluate one concrete
  decision under uncertainty. Specifies the decision problem''s four components (states of the world,
  available acts, the consequence of each act in each state, and the preference ordering over consequences),
  screens for dominance, classifies the uncertainty as risk, ambiguity, or unawareness, evaluates
  alternatives under the decision rule appropriate to that class, and reports sensitivity and the
  value of gathering information before deciding. Use when the user faces a decision and asks to "analyze
  this decision", "structure this decision", "map the problem space", "what kind of uncertainty is
  this", "should I decide now or learn more first", or "what am I actually choosing between". Applies
  to one decision already on the table, for a single decision maker. Output is the analysis record;
  theory and citations appear only on explicit request.'
---

# Decision analysis

Formulate and evaluate one concrete decision under uncertainty. Work the phases below in order. The product is the analysis record defined in the output contract.

## Applicability

The method fits a single decision maker facing a one-time choice among identified alternatives, uncertain about facts outside their control. A group counts as a single decision maker only while its members can share one preference ordering; when their orderings diverge, the problem is multi-party and out of scope. Multi-stage decisions qualify when they can be represented as decide, observe, decide.

Decline, and say why in one sentence, when the problem is:

- Strategic interaction with other optimizing agents (their best move depends on yours — game theory's ground, not this skill's).
- Multi-party negotiation.
- Ongoing policy optimization rather than a discrete choice.

## Register

Use terms of art precisely and define each in one clause at first use. Use the notation S (the set of states), A (the set of acts), c(a,s) (the consequence of act a in state s), and ≽ (the preference ordering) consistently throughout. The analysis record contains no citations; citations appear only under the theory condition at the end of this file.

## Phase 0 — Scope

Locate the concrete decision in the user's request or the conversation. Confirm it passes the applicability test above. If the user asked an abstract question about the method rather than bringing a decision, route to the theory condition in "On request only" — otherwise analysis comes first, always. If no concrete decision can be located, ask for one; never invent an example to analyze.

## Phase 1 — Formulate

Work the four dimensions in this order, loading each dimension's reference as you reach it.

1. **Acts** (load `references/acts.md`): list the alternatives actually available. Check each: feasible now, distinct from the others. Include "defer" only when deferral is genuinely open.
2. **States** (load `references/states.md`): list the mutually exclusive ways the facts outside the decision maker's control could stand. State the boundary: write down what was deliberately excluded.
3. **Consequences** (load `references/consequences.md`): build the table c(a,s) — one row per act, one column per state, every cell holding the outcome as the decision maker would experience it. An unfillable cell is a formulation gap: ask, never invent.
4. **Preferences** (load `references/preferences.md`): elicit the ordering ≽ over the distinct outcomes, pairwise where unclear. Check transitivity. Record incomparable pairs as incomparable.

Then write the decision statement in one sentence: "Choose one of {acts} by {date or trigger}."

## Phase 2 — Screen for dominance

Compare acts row-wise against the table, using only the ordering — no probabilities in this phase. Act b is dominated when act a's outcome is at least as preferred as b's in every state and strictly preferred in at least one. Eliminate each dominated act, naming the act that dominates it. If a single act survives, the analysis terminates: record the dominance result and skip to the output contract.

## Phase 3 — Assess uncertainty

Work on the states dimension; the classification tests live in `references/states.md`. Elicit probability judgments over S where the evidence supports them. Classify the uncertainty as risk (evidence pins the probabilities down), ambiguity (evidence supports a range of defensible probability distributions), or unawareness (relevant states cannot be listed now). State the classification together with the test result that produced it.

## Phase 4 — Evaluate

Evaluate the surviving acts under the rule matching the uncertainty class, and name the rule in the record:

- **Risk** → expected-utility ranking: score each act by its probability-weighted preference value and rank.
- **Ambiguity** → maxmin and robustness: identify the act whose worst case across the defensible set of distributions is best, and any act that ranks well across the whole set. Where hedged alternatives exist — acts constructed to do acceptably under every defensible distribution — surface them.
- **Unawareness** → option-value ranking: prefer staged, reversible commitments that keep acts open as states reveal themselves; compare against relevantly similar past cases. The act-dimension depth in `references/acts.md` supports this.

## Phase 5 — Sensitivity and value of information

Report both, in this order:

1. **Sensitivity**: vary each probability or preference input one at a time and report the threshold value at which the recommendation flips. Inputs with no flipping threshold in their plausible range are settled; say so.
2. **Value of information**: where consequences are quantified, compute EVPI — the expected value of deciding with perfect information minus the expected value of the best act now. Where they are not, state that EVPI is not computable and rank the candidate observations qualitatively instead; never invent numbers to force the computation. Recommend decide-now or gather-information, naming the specific observation that would settle the most sensitive input. Record the exception: under ambiguity, new evidence can widen the defensible set rather than narrow it, so information has to be weighed against that possibility rather than assumed helpful.

## On request only

- **Visual**: copy `assets/template.html` to a working location, fill every `tpl:` marker from the analysis record following the instructions inside each marker, verify no example text survives, then open it. The template documents itself; read its header comment before editing.
- **Theory**: explain the method from the Sources sections of the dimension files, after and subordinate to the analysis. This is the only condition under which citations appear.

## Output contract

Deliver the analysis record with these parts in this order:

1. Decision statement (one sentence).
2. Act set.
3. State space, with the boundary statement.
4. Consequence table c(a,s).
5. Preference ordering, with incomparabilities recorded as such.
6. Dominance result (acts eliminated and by what; or "none dominated").
7. Uncertainty class, with the test result.
8. Evaluation under the named rule.
9. Sensitivity thresholds.
10. Information recommendation, with EVPI where computable.
11. Recommendation.

Close with one line offering the visual and the theory.

## Context loading

| Phase | Load |
| --- | --- |
| 0 Scope | nothing |
| 1 Formulate | each dimension file as its component is worked: `references/acts.md`, `references/states.md`, `references/consequences.md`, `references/preferences.md` |
| 2 Dominance | nothing new |
| 3 Uncertainty | `references/states.md` (already loaded; its classification section) |
| 4–5 Evaluate, sensitivity | nothing new |
| Visual (on request) | `assets/template.html` (self-documenting) |
| Theory (on request) | the dimension files' Sources sections |
