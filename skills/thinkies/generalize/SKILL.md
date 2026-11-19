---
name: generalize
description: Use when a case looks new and no known solution fits. Finds the class the case belongs to and carries back the solutions, failure modes, and limits that hold for every member of that class.
---

# Generalize

Find the class a case belongs to, and carry back to the case what holds for every member. The case is the one the request names. When the request names none, take the one the conversation is working on and say which one you took.

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

Work through the steps in order and reply in prose. Say what each step found about the subject, pass over a step that does not apply in a clause, and name each fact a step needed and lacked.

The question-set form below serves a caller who wants the questions apart from their answers. Use it only when the caller asks for questions, hands over a question set, or asks for the set to hand off:

- A question set handed over: answer it.
- A request for questions only, or for the set to hand off: write the question set and stop.
- A request for the questions with their answers: write the question set, then answer it.

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
