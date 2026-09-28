---
name: generalize
description: Find the class a case belongs to and carry back what holds for every member
---

## Steps

### 1. Which particulars can go without changing the case's shape?

Drop one particular at a time: names, numbers, domain, scale. After each drop, check that the case keeps the same kinds of parts, relations, and goal. Keep any particular whose drop changes them.

### 2. What class is left?

Name the class the stripped case belongs to, and list the particulars dropped to reach it.

### 3. What holds for every member?

List what is known for the class: solutions, failure modes, laws, limits.

### 4. What of it applies to this case?

Check each item against the dropped particulars. Apply to the case the items no dropped particular voids. For each item set aside, name the particular that voids it.

### 5. Does a wider class still predict anything here?

Where a wider class would still say something about this case, run these steps again on the class. Otherwise stop.

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
