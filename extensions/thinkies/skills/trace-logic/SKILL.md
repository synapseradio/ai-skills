---
name: trace-logic
description: Use to check whether a conclusion actually follows from its premises. Walks the argument one inference at a time and reports every gap, unjustified leap, and circular step.
---

## Steps

### 1. Identify the reasoning

Target: `$ARGUMENTS`, else the reasoning in the current context.

Read "the reasoning" as an argument written on the page: the passage the request names, the last reply, or the document in hand. Trace what the text states. Where the page holds no argument, ask for one and stop.

### 2. Break reasoning into atomic steps

Decompose the argument into its smallest logical moves, one inference each. Number them, write in the steps the text leaves unstated, and mark each of those as implicit.

### 3. Examine each link for validity

For each step, state what it claims, what it rests on, whether the inference is valid, and which unstated assumptions it needs to work.

### 4. Check the inference type

- **Deduction**: conclusion necessarily follows from premises
- **Induction**: generalizing from specific examples
- **Abduction**: inferring best explanation from observations
- **Analogy**: applying patterns from comparable situations

Verify the type is appropriate and correctly applied.

### 5. Identify gaps and leaps

Name each missing step, unjustified jump, connection assumed without proof, and circular dependency, with the step numbers it sits between.

### 6. Verify logical connectors

Confirm AND, OR, IF-THEN, NOT are used correctly. Map which conclusions depend on which premises, to see how a failed premise propagates and whether another path still reaches the conclusion.

### 7. Assess overall chain strength

Say whether the conclusion follows, where the chain is strongest and weakest, and what would repair each weak link.

## Return

Return the numbered steps with the implicit ones marked, a finding and an inference type for each, the gaps by name, the map of which conclusions depend on which premises, and the closing assessment from step 7. The run is done when every step has a finding and the assessment is stated.
