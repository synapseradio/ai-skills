---
name: strategize
description: Use for a complex problem the user wants to reason through together over many turns.
  Agrees on the problem first, then works through it one aspect at a time with rigorous reasoning,
  following the user's lead on where to go next.
---

Work a complex problem with the user in rounds: agree on what the problem is, reason about one aspect per round, and let the user's reply steer the next round. The user holds the direction, because they know which constraint matters most and you learn that only from their replies.

These steps hold for the whole session, on every later turn as well as the first.

### 1. Initialize

Target: the problem in the current context; if none is evident, ask for clarification. Where the request itself states the problem, take it from there. Choose a descriptive working name (e.g. "api-architecture-exploration") so later turns can reference it. Tell the user: "Working on: [name]". Go to step 2.

### 2. Understand

1. Decompose the task into components at natural joints.
2. State understanding and invite correction: "I understand this as [restatement]. Is that right?"
3. End the turn there. The user's reply decides the next step.

- Confirms → **go to step 3**
- Corrects, questions, or adds constraints → **repeat step 2** with the new information

### 3. Reason (main loop)

Repeat until the user signals done.

**3a. Apply structured reasoning** to the current aspect. Select and chain techniques: argument standardization, fallacy detection, evidence evaluation, assumption surfacing, contrapositive testing, defeater hunting. Name each technique you apply. Give each finding as prose in the dialogue, with the part of the problem that shows it, so the user can check the finding against what they know.

**3b. End the turn** on the findings and wait for the user's reply.

**3c. Route on the reply:**

- *Continue* ("yes", "go on", "what else", new info) → **go to 3a**, building on prior findings
- *Pivot* ("but what about…", "different angle", pushback) → **go to step 2** with the pivot
- *Done* ("done", "thanks", "got it") → **go to step 4**
- *Ambiguous* ("interesting", "I see", "okay") → ask "Continue, pivot, or done?" and wait

### 4. Exit

Summarize what was explored and concluded. Surface transferable insight worth keeping beyond this session. Identify what remains unresolved and what a successor exploration would address.

## What holds in every round

- **The user steers**: the loop continues until the user says done in their own words.
- **Each round uses a technique**: every pass through 3a applies at least one of the named techniques.
- **The user can see where the session is**: when the step changes, open the turn by naming the step you are entering, such as "→ UNDERSTAND" or "→ REASON".

## When nobody can reply

Some runs reach no user: a delegated run, a batch job. There, do step 1, then step 2 with your restatement marked as an assumption. Run 3a once on the aspect the rest of the problem depends on most, then go to step 4. Close the summary with the questions you would have put to the user, each with what its answer would change, so whoever holds the conversation can ask them and start the next round.
