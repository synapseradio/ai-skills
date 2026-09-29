# Clarity Audit Patterns

Fits when: clarify fits and its pass needs detection heuristics or repair tables

Detailed patterns for identifying and fixing clarity issues. Use this reference when the [clarify](./clarify.md) instructions need elaboration.

## Structural Patterns

### Sequence Detection

**Signal words indicating out-of-order content:**

- "As mentioned earlier..." (but it wasn't)
- "This is because..." (cause after effect)
- "To understand X, first know Y..." (Y should come first)
- Pronouns before their referents
- Acronyms before definitions

**Repair strategies:**

1. Map dependency graph: which concepts require which others?
2. Topological sort: arrange so dependencies precede dependents
3. Test: can someone in the audience who is new to the domain follow linearly?

### Information Flow Detection

**Given-new principle**: A sentence that opens on what the audience already holds (given) and ends on what is new is easier to follow. Where, if anywhere, does a sentence open on the new, and does the piece mean to jolt its audience there?

**Detecting violations:**

- Sentence opens with technical term not yet established
- New concept appears in subject position without setup
- The audience must hold unfamiliar content in memory while parsing

**Repair pattern:**

```
Sentence N: [Given] ... [New_A]
Sentence N+1: [New_A as Given] ... [New_B]
Sentence N+2: [New_B as Given] ... [New_C]
```

This chaining creates flow—each sentence picks up where the previous left off.

### Gap Detection

**Categories of gaps:**

1. **Term gaps**: Words used without definition
   - Technical jargon assumed known
   - Acronyms unexpanded
   - Domain concepts unnamed

2. **Logic gaps**: Missing intermediate steps
   - Conclusions without premises
   - "Therefore" without explicit reasoning
   - Cause-effect claims without mechanism

3. **Context gaps**: Assumed background
   - "As we know..." (do we?)
   - References to prior conversations
   - Implicit prerequisites

**Detection heuristic**: Read as if you just arrived. What would confuse you?

### Prerequisite Mapping

**Create prerequisite chains:**

```
To understand C, must understand B
To understand B, must understand A
Therefore: teach A → B → C
```

**Common prerequisite patterns:**

- Context before claim
- Problem before solution
- Concept before procedure
- Simple cases before edge cases

## Content Patterns

### Streamline Detection

**Redundancy signals:**

- Two phrases saying the same thing
- Adjective-noun pairs where the adjective adds nothing ("actual fact," "future plans")
- Prepositional bloat ("in the event that" = "if")

**Ceremonial language and bloat:** see [strengthen](./strengthen.md) for set phrases and candidate replacements.

### Load Type Identification

**Extraneous load indicators:**

- Difficulty from how it's written, not what it says
- Confusion resolves when rephrased
- Core idea is simple; expression is complex

**Intrinsic load indicators:**

- Difficulty from subject complexity
- Simpler phrasing wouldn't help understanding
- Requires building mental models

**Germane load indicators:**

- Difficulty that produces learning
- Productive struggle with new concepts
- Challenge that builds capability

**Response by load type:**

| Load Type | Response |
|-----------|----------|
| Extraneous | Cut it |
| Intrinsic | Preserve, add scaffolding |
| Germane | Preserve, support with examples |

### Mechanism Revelation

**Mechanism-hiding patterns:**

- "X improves Y" (how?)
- "This enables Z" (by what means?)
- "Results in better performance" (through what mechanism?)
- Passive voice hiding actors ("mistakes were made")

**Mechanism questions to ask:**

1. What causes this effect?
2. Through what process does this happen?
3. What are the intermediate steps?
4. Who/what does the action?

**Mechanism template:**

```
[Effect] because [Cause] through [Mechanism].
```

### Quantifier Grounding

**Vague quantifiers to question:**

- many, few, some, several, numerous
- significant, substantial, considerable
- most, majority, minority
- often, rarely, sometimes, frequently
- recently, soon, eventually

Does the form leave the word open on purpose, as a standard its audience applies, the way a contract's "prompt" or "reasonable" is? Then the open word is the drafting.

**Contrast: a grounded quantifier**

- antipattern: "The new schedule will start soon."
- pattern: "The new schedule will start on the first Monday of next month."
- observe: the pattern gives a day the audience can plan around.
- shared: the same claim that the schedule changes.
- contrast: a vague time word against a date.
- look for: a quantity or time word the audience will act on, with no number, date, or comparison behind it.

**When data isn't available:**

- "An unknown number" beats "many"
- "We haven't measured this" beats "significant"
- Acknowledge uncertainty explicitly

## Expression Patterns

### Presence Conversion

**Negation patterns to question:**

| Absence-based | Presence-based |
|---------------|----------------|
| Don't use X | Use Y instead |
| Avoid doing X | Do Y |
| Never X | Always Y |
| Not recommended | Recommend against / Prefer Y |
| Shouldn't X | Should Y |

**Conversion question**: Does the audience need a direction to move, or the prohibition itself? A negation leaves open everything it does not forbid, and a direction names one path. A contract clause, a safety warning, or a recipe's "do not open the oven" may need the prohibition as written.

### Referent Tracking

**Problematic pronouns:**

- it, this, that, they, them
- which (especially after commas)
- the former, the latter

**Ambiguity patterns:**

- Two possible antecedents for one pronoun
- Antecedent too far from pronoun (several sentences back)
- Pronoun category mismatch (plural pronoun, singular options)

**Resolution strategies:**

1. **Replace with noun**: name the thing the pronoun points to
2. **Move antecedent closer**: Restructure so referent is in previous sentence
3. **Scope demonstratives**: "This approach" instead of bare "This"

**Contrast: a pronoun replaced by its noun**

- antipattern: "We met the lawyers after lunch, and it fell apart."
- pattern: "We met the lawyers after lunch, and the negotiation fell apart."
- observe: in the antipattern, "it" could be the meeting, the lunch, or something earlier.
- shared: the same events and the same verb.
- contrast: a pronoun against the noun it stood for.
- look for: a pronoun with two candidates on the page, where the piece does not mean it to stay open.

## Domain-Specific Considerations

### Personal Writing (memoir, letters, journals)

**Common clarity issues to ask about:**

- What does the piece take the audience to know about the family?
- Where, if anywhere, do scene and reflection mix without a signpost?
- Which people and places, if any, go unnamed where the audience needs the name?
- Where, if anywhere, does the piece cut away from a feeling before it lands?

**Questions that often help:**

- Which claimed feeling has an image behind it?
- Where would the names of people, towns, and dates place the audience?
- Where would sensory detail (smell, sound, weather) serve before judgment?
- Where, if anywhere, does the piece tell the audience what to feel before they have felt it?

### Business Writing

**Common clarity issues to ask about:**

- What does each hedge do to the writer's commitment?
- Where, if anywhere, does passive voice leave out who is responsible?
- Which metrics, if any, lack baselines or targets?
- Where, if anywhere, does vocabulary from several domains mix?

**Questions that often help:**

- Does each action item have an owner?
- Where, if anywhere, does "soon" or "later" stand where a date would serve?
- Does each number have a comparison point?
- Is one domain's vocabulary chosen and defined?

### Persuasive Writing (essays, reviews, arguments)

**Common clarity issues to ask about:**

- How does the piece stand toward the strongest counter-argument: named, engaged, or left out?
- How do the examples stand toward the writer's position, and toward the positions against it?
- Which generalizations, if any, can the audience not anchor to anything specific?
- Does the conclusion change what the audience does?

**Questions that often help:**

- Can the claim be stated in one sentence someone in the audience could repeat back?
- Where, if anywhere, is the strongest argument against named and engaged?
- Which example could someone in the audience place in their own life?
- Does the close name what changes if the audience agrees?
