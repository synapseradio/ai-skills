# Strengthen

Eliminate weak language patterns that create distance between claim and commitment.

## Diagnostic Question

Ask: What factors in this prose create hedging, padding, or false distance?
Look for patterns that weaken assertion without adding epistemic value.

## Instructions

1. **Flag hedge words** — Mark: somewhat, fairly, rather, relatively, arguably, quite, a bit, perhaps.
   Ask: Does this hedge reflect genuine uncertainty, or is it habitual cushioning?

2. **Flag weak verbs** — Mark: seems, appears, tends, might consider, could potentially.
   Ask: What would direct assertion look like? What evidence supports or refutes it?

3. **Flag nominalizations** — Mark: utilization, implementation, facilitation, optimization.
   Ask: What verb hides inside this noun? Nominalizations often obscure who acts.

4. **Flag filler phrases** — Mark: in terms of, the fact that, for all intents and purposes.
   Ask: What remains if this phrase is deleted? Often: the same meaning, fewer words.

5. **Flag false certainty** — Mark: obviously, clearly, as everyone knows, certainly.
   Ask: Is this actually obvious, or is the word doing rhetorical work to avoid argument?

6. **For each flag, decide:**
   - **Delete** if unnecessary (most hedges, most filler)
   - **Replace** with precise alternative (weak verb → strong verb)
   - **Preserve with justification** if hedge reflects genuine epistemic uncertainty

## Pattern Lists

### Hedge words (weaken without adding epistemic value)

| Word | Replace with | Keep when |
|------|--------------|-----------|
| somewhat | [delete] or quantify | Genuine partial truth |
| fairly | [delete] or quantify | — |
| rather | [delete] | Genuine contrast |
| relatively | compared to [X] | Comparison is explicit |
| arguably | [delete] or argue it | — |
| quite | [delete] or quantify | — |
| a bit | [delete] or quantify | — |
| slightly | [delete] or quantify | Measured difference |
| perhaps | [delete] or investigate | Genuine uncertainty |
| maybe | [delete] or investigate | Genuine uncertainty |
| possibly | [delete] or state conditions | Genuine uncertainty |
| in some ways | [delete] or specify which | — |
| to some extent | [delete] or quantify | — |
| more or less | [delete] or quantify | — |

### Weak verbs (create distance from assertion)

| Weak form | Stronger form |
|-----------|---------------|
| seems to be | is (if verified) / appears (if evidence partial) |
| appears to | is / suggests (with evidence) |
| tends to | [verb] in [conditions] |
| might | will (if confident) / could (if uncertain) |
| could potentially | can / could |
| may consider | should consider / consider |
| would suggest | suggests / shows |
| might possibly | might / could |

### Nominalizations (verbs hidden inside nouns)

| Nominalization | Verb | Example transformation |
|----------------|------|------------------------|
| utilization | use | "the utilization of caching" → "using caching" |
| implementation | implement | "the implementation of the feature" → "implementing the feature" |
| facilitation | facilitate / help | "facilitation of communication" → "helping teams communicate" |
| optimization | optimize | "optimization of queries" → "optimizing queries" |
| prioritization | prioritize | "prioritization of tasks" → "prioritizing tasks" |
| conceptualization | conceive / design | — |
| actualization | realize / make real | — |
| determination | determine / decide | "the determination was made" → "we decided" |
| establishment | establish / create | — |
| consideration | consider | "consideration of options" → "considering options" |

### Filler phrases (delete without loss)

| Phrase | Replace with |
|--------|--------------|
| in terms of | [delete] or use "regarding" |
| the fact that | [delete] or restructure |
| for all intents and purposes | [delete] |
| at the end of the day | [delete] |
| it is important to note that | Note: / [delete] |
| it should be mentioned that | [delete] |
| in order to | to |
| due to the fact that | because |
| at this point in time | now |
| in the event that | if |
| on a daily basis | daily |
| in the near future | soon |
| a large number of | many / [number] |
| in light of the fact that | because / since |
| has the ability to | can |
| is in a position to | can |

### False certainty (asserts without argument)

| Word | Problem | Alternative |
|------|---------|-------------|
| obviously | Asserts without evidence | State the evidence |
| clearly | Asserts without evidence | Show the clarity |
| of course | Assumes shared knowledge | Verify or argue |
| as everyone knows | Assumes universal knowledge | Cite or argue |
| it goes without saying | If true, don't say it | [delete] |
| naturally | Assumes inevitability | Explain the mechanism |
| undoubtedly | Overstates certainty | "evidence strongly suggests" |
| certainly | Overstates certainty | Qualify or provide evidence |
| definitely | Overstates certainty | Qualify or provide evidence |
| without question | Overstates certainty | Address the question |

## Examples

### Hedge word removal

**Before:** "This approach is somewhat more efficient and could potentially reduce latency fairly significantly."

**Ask:** Does "somewhat," "potentially," "fairly" reflect genuine uncertainty, or habitual cushioning?

**After:** "This approach is more efficient and reduces latency by 40%." (if measured) or "This approach should be more efficient—benchmark to confirm." (if uncertain)

**What changed:** Removed hedges that added no epistemic value. Made uncertainty actionable when genuine.

### Weak verb strengthening

**Before:** "The results seem to suggest that caching might possibly improve performance."

**Ask:** What does the evidence actually show?

**After:** "The results show caching improves performance." (if measured) or "Initial results suggest caching improves performance—further testing required." (if partial)

**What changed:** Replaced "seem to suggest" and "might possibly" with direct assertion calibrated to evidence.

### Nominalization repair

**Before:** "The utilization of caching enables the optimization of database performance."

**Ask:** What verbs hide in "utilization" and "optimization"?

**After:** "Using caching optimizes database performance." → even better: "Caching makes the database faster."

**What changed:** Unpacked nominalizations to verbs. Second revision uses concrete language ("faster") instead of abstract ("optimizes performance").

### Filler phrase removal

**Before:** "In terms of the implementation, due to the fact that we have a large number of users, we need to consider scalability."

**Ask:** What remains if filler phrases are deleted?

**After:** "Because we have 50,000 users, we need scalable implementation."

**What changed:** Removed "in terms of," "due to the fact that," "a large number of." Quantified "large number." Same meaning, fewer words.

### False certainty calibration

**Before:** "Obviously, microservices are the right architecture for this problem."

**Ask:** Is this actually obvious? What argument does "obviously" replace?

**After:** "Microservices fit this problem because the services have independent scaling needs and separate deployment cycles."

**What changed:** Removed "obviously" which was doing rhetorical work to avoid stating reasons. Added the actual argument.

### Combined transformation

**Before:** "It is important to note that the implementation of the new authentication system will potentially require the utilization of somewhat significant resources in terms of developer time."

**Ask:** Audit all patterns: filler phrase (it is important to note), nominalization (implementation, utilization), hedge (potentially, somewhat), filler (in terms of).

**After:** "Implementing the new authentication system requires significant developer time—estimate three engineer-weeks."

**What changed:** Removed filler opener, unpacked nominalizations, deleted hedges, removed filler phrase, quantified "significant."
