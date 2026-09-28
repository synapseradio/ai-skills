---
name: instantiate
description: Test an abstraction by making it concrete and finding the conditions it assumed without
  saying
---

## Steps

### 1. What case did its author have in mind?

Build the typical case: specific names, numbers, and a situation someone else could check.

### 2. What case fits the words but not the picture?

Build a case the wording covers that its author likely did not picture: another user, another scale, another setting. Make it as specific as the first.

### 3. What happens in each case?

Apply the abstraction to each case. Record where it holds, where it bends, and where it says nothing.

### 4. What did the abstraction assume without saying?

For each bend or silence, name the unstated condition, worded as the clause the abstraction would need to carry it.

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
