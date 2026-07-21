---
name: strategize
description: Adaptive multi-phase reasoning for complex problems
---

Follow these steps:

### 1. Initialize

Target: `$ARGUMENTS`, else ask for clarification. Choose a descriptive working name (e.g. "api-architecture-exploration") so later turns can reference it. Tell the user: "Working on: [name]". Go to step 2.

### 2. Understand

1. Decompose the task into components at natural joints.
2. State understanding and invite correction: "I understand this as [restatement]. Is that right?"
3. **STOP. Wait for user response.**

- Confirms → **go to step 3**
- Corrects, questions, or adds constraints → **repeat step 2** with the new information

### 3. Reason (main loop)

Repeat until the user signals done.

**3a. Apply structured reasoning** to the current aspect. Select and chain techniques: argument standardization, fallacy detection, evidence evaluation, assumption surfacing, contrapositive testing, defeater hunting. Present findings as prose woven into the dialogue.

**3b. Await user response.**

**3c. Route on the response:**

- *Continue* ("yes", "go on", "what else", new info) → **go to 3a**, building on prior findings
- *Pivot* ("but what about…", "different angle", pushback) → **go to step 2** with the pivot
- *Done* ("done", "thanks", "got it") → **go to step 4**
- *Ambiguous* ("interesting", "I see", "okay") → ask "Continue, pivot, or done?" and wait

### 4. Exit

Summarize what was explored and concluded. Surface transferable insight worth keeping beyond this session. Identify what remains unresolved and what a successor exploration would address.

## Loop invariants

- **User control**: continue until an explicit "done" signal
- **Reasoning engagement**: each reason phase applies at least one structured technique
- **Transition announcement**: announce phase transitions ("→ UNDERSTAND", "→ REASON")
