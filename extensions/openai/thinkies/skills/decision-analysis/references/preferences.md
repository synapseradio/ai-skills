# Preferences — ≽

The preference ordering: the decision maker's ranking over the distinct outcomes in the consequence table. ≽ reads "at least as preferred as." The ordering belongs to the decision maker; the analyst elicits it and checks its structure, never supplies it.

## Elicitation

1. Collect the distinct outcomes from the filled table c(a,s).
2. Where the ranking is obvious, take it. Where it is not, elicit pairwise: "Which would you rather live with, {outcome x} or {outcome y} — or can you truly not say?" Offer the third answer honestly; a forced choice recorded as a preference is worse than a recorded incomparability.
3. Assemble the pairwise answers into an ordering. Present it back in full — "so: x over y, y over z, x and w you can't rank" — and let the decision maker object.
4. Record incomparable pairs as incomparable. They constrain the evaluation phase (an expected-value ranking needs comparability along the paths it scores), and hiding them fakes a precision the analysis does not have.

## Well-formedness checks

- **Transitivity**: if x ≽ y and y ≽ z, check that the decision maker also holds x ≽ z. A cycle (x over y, y over z, z over x) is not a preference to respect but an inconsistency to resolve — walk the three pairs back through the decision maker and let them repair one.
- **Consistency under reframing**: re-ask one or two elicited pairs with the outcomes described differently (gains recast as forgone losses, percentages as counts). A ranking that flips under redescription has not yet found the decision maker's actual preference; keep the outcome descriptions fixed and re-elicit.

## Failure modes

- **Forced total orders.** The elicitation pressures every pair into a verdict, and genuine incomparabilities — outcomes that differ along dimensions the decision maker cannot trade off — get papered over with arbitrary rankings. The arbitrary choices then silently drive the recommendation.
- **Preference reversals under redescription.** The ranking tracks the framing of the outcome rather than the outcome. Detected by the reframing check; repaired by pinning the outcome descriptions (a consequences-dimension fix) before re-eliciting.

## Depth

### Partial orders as honest records

An ordering with incomparable pairs is a partial order, and it is a legitimate deliverable. It still supports the dominance screen (dominance needs only the comparisons that exist) and often supports a recommendation. Completing it artificially adds information that was never elicited.

### The representation ladder

There is a ladder from raw comparisons to numbers, and each rung is earned, not assumed:

1. **A relation**: some pairs compared, others silent.
2. **A partial order**: consistent, but with incomparable pairs.
3. **A total order**: every pair ranked, no cycles.
4. **A utility function**: a number attached to each outcome.

The step from rung 3 to rung 4 is licensed only when the total ordering — extended to gambles over the outcomes — satisfies the von Neumann–Morgenstern conditions (completeness, transitivity, continuity, independence). When it does, a utility function exists whose expectation represents the ordering. The numbers certify the ranking; they never create it. What they add is exactly one thing: the ability to weigh outcomes by probabilities. What they do not add is any interpersonal meaning, any significance to the zero point or the scale, or any precision beyond what the elicited comparisons contained.

### Risk attitude as curvature

Once a utility function exists over a quantitative attribute (money, time), the decision maker's attitude to risk lives in its shape: a concave utility (each additional unit worth less than the last) makes a sure amount preferred to a gamble with the same expectation — risk aversion — and a convex one the reverse. Eliciting one or two certainty equivalents ("what sure amount would you trade for this gamble?") locates the curvature well enough for sensitivity analysis to test whether it matters.

### Ordering under ambiguity

When the states dimension classifies the uncertainty as ambiguity, the preference structure itself can encode the response to it. Three earned extensions, in increasing structure: rank acts by their worst expected value over the defensible set of distributions (maxmin); mix the worst and best cases with a pessimism weight; or score distributions themselves by plausibility and rank acts by a doubly weighted expectation. Which extension fits is a preferences question — how the decision maker wants to stand toward the ambiguity — not a fact about the evidence.

## Sources

- J. von Neumann & O. Morgenstern, *Theory of Games and Economic Behavior* (1944) — the representation theorem: the axioms a total ordering over gambles must satisfy for an expectation-representing utility to exist.
- L. J. Savage, *The Foundations of Statistics* (1954) — preference over acts as the primitive from which both probability and utility are derived.
- I. Gilboa & D. Schmeidler, "Maxmin Expected Utility with Non-Unique Prior" (1989) — ranking by the worst expected value over a set of distributions.
- P. Klibanoff, M. Marinacci & S. Mukerji, "A Smooth Model of Decision Making under Ambiguity" (2005) — separating ambiguity attitude from risk attitude via a second-order weighting.
- F. Maccheroni, M. Marinacci & A. Rustichini, "Ambiguity Aversion, Robustness, and the Variational Representation of Preferences" (2006) — the variational family that generalizes maxmin.
