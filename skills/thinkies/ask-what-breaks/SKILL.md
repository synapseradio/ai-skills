---
name: ask-what-breaks
description: Use when a conclusion is about to be relied on. Hunts for the specific facts and observations that would defeat it, and tells the ones that merely weaken it from the ones that would overturn it.
---

The conclusion under test is the one the request names. When the request names none, take the most recent conclusion stated in the conversation or the document in hand, and say which one you took. With no conclusion in either place, ask for one and stop.

## Steps

### 1. State the claim under test

Restate the conclusion as a statement that could turn out false, with its boundaries: what it covers, when, and under which conditions. A vague claim yields vague defeaters, so sharpen it until one observation could count against it.

### 2. Distinguish defeater types

- **Undercutting**: attacks the premises or the reasoning chain (this evidence is unreliable, this assumption is false, this inference doesn't follow)
- **Rebutting**: leaves the reasoning alone and brings counter-evidence against the conclusion itself (data showing the opposite)

### 3. Hunt for undercutting defeaters

List the links the conclusion rests on: each premise, each source, each inference. For each link, ask what would make the premise false, the source unreliable, or the inference invalid. Include what a link depends on without saying so.

### 4. Hunt for rebutting defeaters

Ask what observation would contradict the conclusion outright, what experiment could falsify it, and what data would show the opposite. Write each one as an observation: "seeing X would defeat this". A doubt with no observation attached, such as "maybe it's wrong", needs one before it counts. Where a defeater already holds on the evidence in hand, say so and carry it into the work that follows.

### 5. Test defeater strength

Grade each defeater as a **weakener**, which lowers confidence, or a **destroyer**, which invalidates the conclusion. The test: does it force the revision of one assumption, or a rebuild from scratch?

Stay adversarial toward the claim throughout, whoever holds it. The run exists to stress-test the conclusion, so agreement with the user is no finding.

## Return

Return the claim as restated, the undercutting defeaters and the rebutting defeaters, each with its grade and the reason for it, and the cheapest check that would decide the strongest one. The run is done when every listed link has been attacked and every defeater graded.
