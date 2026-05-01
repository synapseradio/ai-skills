# Activate

Surface hidden actors and convert passive constructions to active voice.

## Diagnostic Question

Ask: Who or what performs each action in this prose?
Where is the actor hidden, absent, or displaced to the end of the sentence?

## Instructions

1. **Scan for passive patterns** — Identify constructions: was/were + past participle, has been, will be, "it was determined that", "there is/are" openers. Mark each instance.

2. **For each passive construction, ask:**
   - Who or what performs this action?
   - Is the actor genuinely unknown or unimportant?
   - Would naming the actor add clarity or accountability?

3. **Rewrite with actor as subject** — Move the doer to the front of the sentence. Transform "The API was deprecated by the platform team" to "The platform team deprecated the API."

4. **Preserve intentional passives** — Keep passive voice when:
   - The actor is genuinely unknown ("The vulnerability was discovered in March")
   - The action matters more than the actor ("The building was constructed in 1892")
   - Passive serves rhetorical purpose (emphasizing receiver of action)
   - Scientific convention requires it ("The samples were analyzed")

5. **Eliminate bureaucratic distance** — Watch for "it has been determined", "it is believed", "there exists a need"—constructions that create false distance between author and assertion. Replace with direct statements.

6. **Check subject-verb distance** — After activation, verify subjects sit close to their verbs. Long clauses between actor and action obscure who does what.

## Passive Pattern Detection

### Common passive constructions

| Pattern | Example | Active form |
|---------|---------|-------------|
| was/were + past participle | "was created" | "[Actor] created" |
| has/have been + past participle | "has been reviewed" | "[Actor] reviewed" |
| will be + past participle | "will be deployed" | "[Actor] will deploy" |
| is being + past participle | "is being processed" | "[Actor] is processing" |
| "it was determined that" | "It was determined that costs exceeded budget" | "The audit revealed costs exceeded budget" |
| "there is/are" | "There are three options available" | "Three options exist" / "We have three options" |

### Bureaucratic distance patterns

| Pattern | Replace with |
|---------|--------------|
| It has been determined that | [Actor] determined / found / concluded |
| It is believed that | We believe / The team believes |
| It should be noted that | Note: / [Delete entirely] |
| It is recommended that | We recommend / [Actor] recommends |
| Consideration should be given to | Consider |
| A decision was made to | [Actor] decided to |

## Examples

### Hidden actor in passive construction

**Before:** "The decision was made to deprecate the API."

**Ask:** Who made this decision?

**After:** "The platform team decided to deprecate the API."

**What changed:** Actor moved from implicit (who?) to explicit (platform team). Accountability is now visible.

### Intentional passive preserved

**Before:** "The vulnerability was discovered in March 2024."

**Ask:** Is the actor important here? Does naming them add clarity?

**After:** Keep as-is. The discovery matters more than who discovered it. Passive is appropriate.

### Bureaucratic distance

**Before:** "It has been determined that the project will be discontinued."

**Ask:** Who determined this? Why the formal distance?

**After:** "We're discontinuing the project." (or "Leadership discontinued the project.")

**What changed:** Removed bureaucratic passive ("it has been determined") that creates false distance. Named the actor.

### Chain of passives

**Before:** "The request was received, was processed by the middleware, and was forwarded to the backend."

**Ask:** Who receives, processes, forwards?

**After:** "The API gateway receives the request, the middleware processes it, and the router forwards it to the backend."

**What changed:** Each action now has a visible actor. The flow of responsibility is clear.

### "There is/are" opener

**Before:** "There are several factors that need to be considered when designing the API."

**Ask:** Who needs to consider? What factors specifically?

**After:** "When designing the API, consider authentication requirements, rate limiting, and versioning strategy."

**What changed:** Eliminated "there are" opener, named the factors, addressed the reader directly with imperative.
