---
name: audit-chain-of-thought
description: Use to learn how much of a line of reasoning is certain and how much is only probable.
  Marks which steps follow necessarily, which generalize from cases, and which are best guesses, and
  shows the weakest links the conclusion hangs on.
---

The subject is an argument written on the page: the passage the request names or quotes, or, when it names none, the most recent argument in the conversation or the document in hand. Audit what the text states. An earlier reply of your own counts as text on the page, audited as written. With no argument on the page, ask for one and stop.

## Steps

### 1. Lay out the argument's steps

List each inferential step the text takes from its premises to its conclusion, quoting the words that make it. Write in the steps the text skips and mark each one as implicit: "A therefore C" often hides "A therefore B, B therefore C."

### 2. Tag each step by type

- **Deductive**: conclusion necessarily follows (if premises true, conclusion must be true). E.g. "All users need authentication. This is a user. Therefore this needs authentication."
- **Inductive**: conclusion generalizes from instances (if premises true, conclusion probably true). E.g. "The last 40 deploys succeeded. Therefore this deploy will probably succeed."
- **Abductive**: conclusion is the best explanation for observations. E.g. "Performance degraded after the cache change. Therefore the cache change probably caused it."

### 3. Assess soundness at each step

- **Deductive**: are the premises true? Is the form valid?
- **Inductive**: how many instances? How representative? What counterexamples?
- **Abductive**: what alternative explanations exist? Which is actually best?

### 4. Identify the weakest links

Name the steps where the chain depends on a probabilistic leap, an unverified assumption, or an explanation with live rivals. The conclusion can fail at these steps even if every earlier step holds.

### 5. Surface the overall structure

Say how much of the chain is deductive, inductive, and abductive. A mostly deductive chain is stronger than one resting on several abductive leaps.

## Return

Return the numbered steps, each with its tag, its soundness finding, and the words in the text it rests on. Then give the weakest links, and close with one sentence on the chain's makeup and what that makeup means for the conclusion. The run is done when every step carries a tag and a finding.
