---
name: thinkies-audit-chain-of-thought
description: Tag reasoning steps by inference type
---

Follow these steps:

### 1. Extract the reasoning chain
Identify each distinct inferential step from premises to conclusion. Make implicit steps explicit — "A therefore C" often hides "A therefore B, B therefore C."

### 2. Tag each step by type
- **Deductive**: conclusion necessarily follows (if premises true, conclusion must be true). E.g. "All users need authentication. This is a user. Therefore this needs authentication."
- **Inductive**: conclusion generalizes from instances (if premises true, conclusion probably true). E.g. "The last 40 deploys succeeded. Therefore this deploy will probably succeed."
- **Abductive**: conclusion is the best explanation for observations. E.g. "Performance degraded after the cache change. Therefore the cache change probably caused it."

### 3. Assess soundness at each step
- **Deductive**: are the premises true? Is the form valid?
- **Inductive**: how many instances? How representative? What counterexamples?
- **Abductive**: what alternative explanations exist? Which is actually best?

### 4. Identify the weakest links
Where does the chain depend on probabilistic leaps, unverified assumptions, or competing explanations? These are where the conclusion could fail even if earlier steps hold.

### 5. Surface the overall structure
How much of the chain is deductive vs inductive vs abductive? A mostly-deductive chain is stronger than one resting on multiple abductive leaps.
