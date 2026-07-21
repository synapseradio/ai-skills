# Consequences — c(a,s)

The consequence function: for each act a and state s, the outcome the decision maker would actually experience if they chose a and s obtained. The table c(a,s) is where the acts and states meet, and filling it is the core of formulation.

## Elicitation

Work cell by cell:

1. For each act–state pair, ask: "If you do {act} and {state} turns out to hold, what happens to you?" Record the answer as an experienced outcome — concrete enough that the decision maker could recognize living it.
2. Describe each outcome in the decision maker's own terms of value: money, time, standing, stress, whatever they name. Keep the description constant in style across cells so outcomes can be compared.
3. Where a cell cannot be filled, stop and ask. An unfillable cell means either the act or the state is not yet well defined, or a fact is missing. Never invent a cell to keep the table moving; an invented consequence poisons every phase downstream.

## Well-formedness checks

- **Completeness**: every cell filled — one row per act, one column per state, no blanks.
- **Outcome distinctness**: outcomes that are genuinely the same experience get the same description; outcomes that differ get visibly different ones. The preference elicitation downstream ranks these descriptions, so sloppy merging or splitting here corrupts the ordering.
- **No state restated as consequence**: a cell that just repeats its column ("state: recession" → "consequence: there is a recession") has not answered the question. The cell must say what the state does to the decision maker under that act.

## Failure modes

- **Outcomes described as probabilities.** "70% chance it works out" inside a cell means a state distinction is missing: the 70% belongs to the states, and the cell should split into what happens when it works and what happens when it does not.
- **Cells filled by invention.** Under time pressure the analyst guesses plausible consequences instead of eliciting them. The table then looks complete while encoding the analyst's imagination, not the decision maker's situation.
- **Hidden attributes.** Two cells get the same description but differ on an unstated dimension of value — same payoff, different stress; same title, different city. The difference surfaces later as an inconsistent-looking preference. The fix is upstream: enrich the descriptions until they differ where the decision maker's experience differs.

## Depth

### Multi-attribute outcomes

When outcomes in the table trade off along more than one dimension of value — money against time, growth against certainty — describe each outcome as a tuple of attributes rather than a single label. Split into attributes when the decision maker's ranking of whole outcomes keeps flipping with the framing; that instability usually means one description is aggregating dimensions they weigh separately. Keep the attribute list short and elicited, not assumed: the attributes are the dimensions the decision maker actually values, discovered by asking what makes one outcome better than another.

The preference ordering is then elicited over these tuples. Whether the attributes can be collapsed back into a single score is a preferences question, and it belongs to that dimension.

## Sources

- J. von Neumann & O. Morgenstern, *Theory of Games and Economic Behavior* (1944) — outcomes as the objects preferences range over; the consequence as the primitive the numbers eventually attach to.
- R. A. Howard, "Decision Analysis: Applied Decision Theory" (1966) — the practice of eliciting consequences from the decision maker rather than supplying them, and keeping the description at the level the decision maker experiences.
