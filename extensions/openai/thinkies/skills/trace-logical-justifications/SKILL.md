---
name: trace-logical-justifications
description: Use to learn what a set of claims ultimately rests on. Follows the support for each claim
  back to its ground, whether an observation, a definition, or nothing at all, and flags the claims
  left unsupported.
---

The subject is a claim and whatever is said in its support. Take it from the request, or, when the request names none, from the most recent claim in the conversation or the document in hand. With no claim in either place, ask for one and stop.

## Steps

### 1. Identify the claim chain

List each distinct claim the statement needs, from premises through intermediate steps to the conclusion. Include the claims it needs and leaves unsaid.

### 2. Ask what supports each claim

For each claim, identify its warrant:

- Another claim in the chain
- An observation or measurement
- A definition
- A logical axiom
- Nothing visible

### 3. Follow chains to bedrock

Trace backward until reaching an endpoint:

- **Direct observation**: "I measured X"
- **Definitional truth**: "by definition of the term"
- **Logical axiom**: "law of non-contradiction"
- **Absence**: no warrant found

### 4. Mark floating claims

Flag every claim whose chain ends in absence. These are the unsupported assumptions the statement stands on.

### 5. Assess chain integrity

- Are bedrock warrants appropriate for the claims they support?
- Are floating assumptions plausible?
- Does the overall structure hold?

## Return

Return the claims with the warrant of each, every chain written out to its endpoint, the floating claims, and a judgment: whether the statement holds as written, and which weaker version its support does carry. The run is done when every chain has reached an endpoint.
