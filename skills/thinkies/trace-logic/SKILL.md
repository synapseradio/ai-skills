---
name: thinkies-trace-logic
description: Follow reasoning step-by-step
---

Follow these steps:

### 1. Identify the reasoning
Target: `$ARGUMENTS`, else the reasoning in the current context.

### 2. Break reasoning into atomic steps
Decompose into the smallest logical moves — one inference each. Make implicit steps explicit and number them.

### 3. Examine each link for validity
For each step: what is claimed, what it rests on, whether the inference is valid, and what unstated assumptions make it work.

### 4. Check the inference type
- **Deduction**: conclusion necessarily follows from premises
- **Induction**: generalizing from specific examples
- **Abduction**: inferring best explanation from observations
- **Analogy**: applying patterns from comparable situations

Verify the type is appropriate and correctly applied.

### 5. Identify gaps and leaps
Missing steps, unjustified jumps, connections assumed but unproven, circular dependencies.

### 6. Verify logical connectors
Confirm AND, OR, IF-THEN, NOT are used correctly. Map which conclusions depend on which premises to see how failures propagate and whether alternative paths exist.

### 7. Assess overall chain strength
Does the conclusion follow validly? Where is the reasoning strongest and weakest? What would strengthen weak links?
