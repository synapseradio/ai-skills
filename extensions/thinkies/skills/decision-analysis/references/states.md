# States — S

The states of the world: the mutually exclusive ways the facts outside the decision maker's control could stand. Everything uncertain in the decision lives here; every other component is either chosen (acts), derived (consequences), or judged (preferences).

## Elicitation

Ask, in order:

1. "What facts, outside your control, would you need to know to choose with certainty?" Each answer names an uncertain quantity.
2. For each uncertain quantity: "What are the ways it could stand?" Partition each quantity into a small number of decision-relevant levels rather than a continuum, unless the analysis genuinely needs the continuum.
3. Combine the quantities into states: each state is one complete assignment of a level to every quantity. Prune combinations that cannot co-occur.
4. State the boundary explicitly: "This analysis treats {excluded contingencies} as outside its scope." Write the exclusions down in the record; a boundary that exists only implicitly cannot be checked later.

The boundary matters because a state space is always a small world: a deliberately restricted description of the situation, not the universe. Formulating within a small world is what makes analysis possible; naming the restriction is what keeps it honest.

## Well-formedness checks

- **Exclusivity**: no two states can both obtain. If two overlap, split or merge until they cannot.
- **Exhaustiveness within the boundary**: inside the stated boundary, some listed state must obtain. "Something else happens" is admissible as a residual state only when its consequences can still be filled in.
- **Decision relevance**: a distinction between two states that never changes which act is best is idle — fold those states together. The state space should be exactly as fine as the decision requires.
- **Act independence**: a state must not be defined in terms of which act was chosen. "The market is small" is a state; "our launch fails" is not.

## Failure modes

- **Unlisted states.** The most damaging failure: a contingency that belongs inside the boundary never makes the list, so no act was evaluated against it. The remedy during elicitation is the direct question "what else could stand in the way, however unlikely?" asked once more after the list feels complete.
- **States conflated with outcomes.** "We succeed" and "we fail" are consequences of an act meeting a state, not states. When a candidate state mentions the decision maker's action or its result, push it back through c(a,s).
- **Boundary never stated.** Without a written boundary, exhaustiveness cannot be judged and later surprises cannot be classified as inside or outside the formulation.

## Depth

### Probability judgment over S

Where the evidence supports it, attach a probability to each state. Coherence checks: the probabilities are non-negative, sum to one, and survive being asked in a different order or framing (elicit a few both directly and as odds; material disagreement means the judgment is not yet stable).

### Classifying the uncertainty

Apply these tests to the probability judgments, in order:

- **Risk**: two informed assessors holding this evidence would write materially the same probabilities. The evidence pins the distribution down.
- **Ambiguity**: informed assessors would write different probabilities while agreeing on a range. The evidence supports a set of defensible distributions, not one. Record the set (even coarsely: "somewhere between 20% and 60%").
- **Unawareness**: the relevant contingencies cannot all be listed now. The failure is upstream of probability — the state list itself is known to be incomplete in ways that matter.

State which test fired and why. The classification drives the evaluation rule, so it must be explicit, not implied.

A caution for the ambiguity case: acquiring more evidence can widen the defensible set rather than narrow it (dilation), so "gather more information" is not automatically the right response to ambiguity. Weigh it, don't assume it.

### Refinement versus expansion

Two different things improve a state space, and the record should say which happened:

- **Refinement** separates states already listed: what you know amounts to a partition of S (a division of the states into cells you can tell apart), and learning refines the partition. An observation is valuable exactly when it separates states whose best acts differ.
- **Expansion** adds a state that was absent from S entirely. This is a revision of the formulation, not a gain in information within it. Under unawareness, expansion is the expected event, which is why the evaluation rule for that class favors acts that survive it.

Cost-free information within a fixed, well-formed space never hurts the decision maker in expectation; that guarantee does not extend across an expansion, which is another reason to keep the boundary written down.

## Sources

- L. J. Savage, *The Foundations of Statistics* (1954) — states, acts, consequences as the components of a decision problem; the small-worlds restriction (p. 16): every formulation deliberately restricts the world description, and the restriction is a modeling choice to be owned, not hidden.
- D. Ellsberg, "Risk, Ambiguity, and the Savage Axioms" (1961) — the risk/ambiguity distinction: evidence that pins a distribution down versus evidence that supports a set of them.
- E. Karni & M.-L. Vierø, "Reverse Bayesianism" (2013) — growing awareness: how a decision maker revises when a previously unlisted state arrives, distinguishing expansion of S from updating within it.
- T. Seidenfeld & L. Wasserman, "Dilation for Sets of Probabilities" (1993) — new evidence can widen the set of defensible distributions.
- I. J. Good, "On the Principle of Total Evidence" (1967) — cost-free information cannot hurt in expectation, within a fixed formulation.
