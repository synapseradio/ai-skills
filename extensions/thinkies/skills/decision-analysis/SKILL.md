---
name: decision-analysis
description: Use when a user faces one concrete choice among identified options under uncertainty. Structures the choice rigorously, ranks the options by what the user values, and says whether to decide now or learn more first.
compatibility: Needs a decision maker who can answer questions during the run. With none in reach, the skill returns its open questions and stops.
---

Work one concrete decision under uncertainty through the steps below. The facts and the preferences belong to the decision maker. Ask for whatever the request leaves out and fill nothing in yourself, because an invented outcome or ranking carries into every later step.

The decision is the one the request names, or the one under discussion in the conversation. With no concrete decision in either place, ask for one and stop. In a run that cannot reach the decision maker, such as a subagent or a batch job, work each step as far as the request's own text allows, return the questions that remain as a numbered list, and stop there.

## Steps

### 1. Check that the method fits

The method fits one decision maker facing a one-time choice among identified alternatives, uncertain about facts outside their control. A group counts as one decision maker while its members share one ranking of the outcomes. A staged decision fits when it can be put as decide, observe, decide. Decline in one sentence when the problem is a contest with others who choose against the decision maker, a negotiation among several parties, or an ongoing policy to tune.

### 2. List the acts

List what the decision maker could commit to today, then ask which option is missing, since a choice presented as a binary usually has a third. Strike any act that needs someone else's free choice. Split any act that hides a later decision into its stages. List "wait" only where waiting is open and something would be observed during it.

### 3. List the states

List the ways the facts outside their control could stand. States exclude each other, and none is defined by which act gets chosen: "the market is small" is a state, and "our launch fails" is an outcome. Fold together states that never change which act is best. Ask once more what else could stand in the way, however unlikely, and write down what the analysis leaves out of scope.

### 4. Fill in the consequences

For every act in every state, state what would happen to the decision maker, in the terms they value. A consequence you cannot state means an act or a state is ill-defined or a fact is missing, so ask. A consequence stated as a chance ("70% it works out") hides a missing state, so split it.

### 5. Elicit the preferences

Rank the distinct outcomes, asking pair by pair where the ranking is unclear and accepting "can't say" as an answer. Record pairs the decision maker cannot rank as unranked. Where the answers form a cycle (x over y, y over z, z over x), walk the three pairs back through the decision maker until they repair one.

### 6. Screen for dominance

Use the ranking alone, with no probabilities yet. An act is dominated when another act is at least as preferred in every state and strictly preferred in one. Remove each dominated act and name the act that beats it. If one act is left, it is the answer: go to step 10.

### 7. Classify the uncertainty

- **Risk**: two informed people holding this evidence would write much the same probabilities.
- **Ambiguity**: they would write different probabilities inside a range they agree on. Record the range.
- **Unawareness**: the list of states is known to be incomplete in ways that matter.

Say which test fired and why, because the class decides the rule in step 8.

### 8. Evaluate under the matching rule

- **Risk**: rank the acts by probability-weighted value.
- **Ambiguity**: prefer the act whose worst case across the range is best, note any act that ranks well across the whole range, and look for a hedged act built to do acceptably anywhere in it.
- **Unawareness**: prefer staged, reversible commitments that keep acts open as states reveal themselves, and compare with how similar past cases turned out.

### 9. Test sensitivity and the value of learning first

Vary each probability and each ranking input one at a time, and find the value at which the answer flips. An input with no flip inside its plausible range is settled. Then name the observation that would settle the most sensitive input, and weigh what learning it first would cost against deciding now. Put a number on that value only where the consequences are already in numbers. Under ambiguity, new evidence can widen the range as well as narrow it, so weigh learning before assuming it helps.

### 10. Recommend

State the act to choose, the rule that picked it, the input that would flip the choice, and whether to decide now or learn first.
