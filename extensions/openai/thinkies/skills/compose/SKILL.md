---
name: compose
description: Join parts into a whole that does what none of them does alone, and find what the whole
  still lacks
---

## Steps

### 1. What does each part do on its own?

List the parts in hand and what each does by itself. A part that cannot yet run on its own is not ready to join; say what it still needs.

### 2. How must the parts be arranged for the whole to work?

For each pair that touches, name what passes between them or holds them together: what feeds what, what constrains what, what contains what, what comes first. Leave pairs with nothing between them unconnected.

### 3. What does the arrangement do that no part does?

Name the property that appears only in the assembly, stated as the purpose the parts now serve together. Where nothing appears, the parts form a list, not a whole: say so and stop.

### 4. Which parts does that property need?

Remove each part in turn and say whether the property survives. A part whose removal changes nothing does not belong to this whole.

### 5. What does the property need that no part supplies?

Name each connection or function the arrangement requires and no part provides. Each is a missing part.

### 6. What is the whole?

State it in one sentence: its parts, the arrangement that matters most, and what it does.

## Output

Choose the mode from what you were handed:

- A question set: answer it.
- A request for questions only: write the question set and stop.
- Anything else: write the question set, then answer it.

Write the question set in this form: one question per step, in step order, each reworded to name the subject, so that a reader holding only the set can answer it.

```markdown
**Subject:** [what is examined, named so it can be found without this conversation]

**Given:**

- [a fact, source, or limit the answers must respect] ([where it came from])

**Questions:**

1. [step 1's question, naming the subject]
2. [step 2's question, naming the subject]
3. [step 3's question, naming the subject]
```

Answer in this form, keeping each question's number and wording, from the set and from what you can check yourself:

```markdown
**Subject:** [the subject, as the set names it]

1. [step 1's question, naming the subject]

   [the answer]

2. [step 2's question, naming the subject]

   Skipped: [why this step does not apply]

3. [step 3's question, naming the subject]

   Open: [the fact the answer needs that the set does not give]
```
