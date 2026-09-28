---
name: decompose
description: Break a whole into parts at its natural joints, one axis per level, until each part can
  be acted on or checked
---

## Steps

### 1. What is the whole for, and where does it end?

Name its purpose and its boundary: what belongs inside and what does not. Where the purpose is unknown, say so and mark every cut below as provisional.

### 2. Which axis fits, and which relations along it?

Choose one axis for this level. Part-of, for things: components, members, portions, materials, phases, qualities, places. Means-to, for goals and tasks: subgoals, cases, constraints. Select only the relations that fit.

### 3. Where are the natural joints?

Cut where boundaries already exist. A cut sits at a joint when the interface across it stays small, the parts on each side change for independent reasons, properties change abruptly at the line, and each part serves one function of the whole.

### 4. Do the parts cover the whole exactly?

Look for gaps, a piece of the whole no part holds, and overlaps, a piece two parts both hold. Move cuts until neither remains.

### 5. Which parts need another pass?

List each part still too complex to act on. Run these steps again on each, naming the axis at every level; part-of does not chain across relation types.

### 6. Where does cutting stop?

Stop at a part that can be acted on or verified directly, or where the next cut grows the interfaces more than it shrinks the parts.

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
