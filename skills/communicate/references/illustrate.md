# Illustrate

Make abstract concepts concrete through examples that reveal essential properties and through witnessed detail that locates abstractions in a specific time and place.

## Diagnostic Question

Ask: Where do abstractions float without concrete grounding?
What claims would a reader accept definitionally but fail to recognize in practice? Where do concepts need examples to convey their essential properties? Has the speaker been here - what witnessed detail could replace this category description?

## Instructions

1. **Identify what resists understanding** - Determine whether the difficulty is definitional, structural, practical, or boundary-based. Different understanding gaps need different illustration approaches.

2. **Choose representative instances** - Select examples that capture essential properties rather than accidental features. Look for typical cases where defining characteristics are clearly visible.

3. **Show variation to reveal the pattern** - Present multiple examples that differ in surface features but share the underlying pattern. Variation helps people extract what's essential from what's coincidental.

4. **Use counter-examples for boundaries** - Show near-misses that look similar but miss a critical defining property. Make the distinction explicit by highlighting which essential feature is present versus absent.

5. **Handle misleading particulars** - Watch for features that appear prominently but don't define the concept. Either choose different examples or explicitly note which features belong to this instance rather than the pattern.

6. **Layer from simple to complex** - Start with the clearest, most stripped-down instance. Progressively introduce complexity. People grasp basic patterns before they can appreciate variations and edge cases.

7. **Test the mental model** - Check what pattern readers would extract from seeing these instances together. Adjust examples when they risk creating incorrect mental models, even if each example is individually valid.

### Grounding Moves

Sometimes abstractions need not just examples but *situated, witnessed detail* - specifics located in time and place that replace category language with lived experience.

1. **Identify category language** - Scan for abstract nouns operating as categories rather than specifics: *leadership*, *excellence*, *community*, *innovation*, *resilience*, *transformation*. These words gesture toward meaning without delivering it. They describe a type of thing rather than a thing.

2. **Apply the grounding test** - For each category word, ask: what specific instance has the writer witnessed? What happened, where, when, to whom? If the writer can answer, the abstraction should be replaced or accompanied by the specific instance. If the writer cannot answer, the abstraction may be doing no work.

3. **Replace category with instance** - Transform category descriptions into situated specifics. The grounded version does not use the category word - the reader recognizes the concept from the specific actions described.

4. **Preserve the writer's actual experience** - The failure mode is generating "plausible" grounding rather than witnessed grounding. If the writer cannot provide a specific instance they have experienced or directly observed, say so. "I have not witnessed this directly - this claim comes from [source]" is honest grounding. Fabricated specificity is worse than honest abstraction.

5. **Know when abstraction is appropriate** - Not every instance of category language needs grounding:
    - When the audience shares enough context that the category functions as shorthand
    - When the prose is operating at a level of generality that specific instances would distort (policy documents, theoretical frameworks)
    - When the writer is explicitly building toward a generalization from previously grounded instances
    - When loading the reader with specifics would obscure the structural argument

**Distinguish illustrate from grounding moves:** Illustrate grounds *claims* in *examples* (content-level: "here is an instance of what I mean"). Grounding moves ground *voice* in *lived experience* (speaker-level: "I have been in the room where this happened"). Illustrate proves a point. Grounding situates the speaker. Both are valuable - they do different work.

## Examples

### Illustrating technical debt through specific instances

**Core example**: "You're building a user registration system and hard-code the validation rules directly in the form handler because it's faster than creating a separate validation layer. This works perfectly now. Six months later, you need the same validation in three other places - the API endpoint, the batch import process, and the mobile app. You now have to implement the same rules four times and keep them synchronized."

**Variation**: "You copy-paste a component instead of abstracting it because you're in a hurry. Now bug fixes require changing five files instead of one." Different scale, same pattern.

**Counter-example**: "You write a simple linear algorithm instead of an optimized one because the dataset is small. The simple approach is easier to understand and maintain, and performance is fine." This looks like technical debt - choosing the simple option - but it's not, because there's no future cost.

**Pattern extracted**: Shortcuts that save time now but multiply work later. Not "avoid copying code" but the time-cost tradeoff.

### Avoiding misleading particulars in microservices examples

**Problematic example**: "Netflix uses microservices with each service deployed to AWS Lambda, communicating via REST APIs, with separate databases for each service." This might suggest microservices require Lambda, REST, or AWS - incidental features, not essential properties.

**Better approach**: Start with essential properties stripped of implementation: "Microservices architecture means decomposing an application into separate services where each service handles a distinct business capability, can be deployed independently, and owns its data."

**Then show variation**: "One team might deploy microservices as containers orchestrated by Kubernetes, another might use serverless functions, another might run them as traditional server processes. Some communicate via HTTP, others via message queues, others via gRPC."

The variation signals that specific technologies are variable while service decomposition and independence are constant.

### Grounding category language with witnessed detail

**Before:** "Our company values innovation and collaboration."

**Grounding test:** What specific innovation? What specific collaboration? Has the writer witnessed these?

**After:** "Last quarter, two engineers from different teams spent their Friday afternoons prototyping a caching layer nobody had asked for. It cut our API response times by 60%. That's the kind of thing that happens here when people have time to follow their hunches."

**What changed:** "Innovation" and "collaboration" disappeared. The reader sees them without being told about them.

### Distinguishing grounded detail from fabricated specificity

**Plausible but ungrounded:** "Walking through the refugee camp at dawn, I saw children playing in the dust between tents, their laughter a defiant anthem against displacement."

**Warning signs:** Sensory detail that reads as cinematic rather than witnessed. "Defiant anthem" is category language disguised as observation. The detail is vivid but generic - it could describe any camp at any dawn.

**Actually grounded:** "The camp smelled like cooking oil and diesel. A girl in a Barcelona FC jersey was teaching younger kids to skip rope with an extension cord. She looked about eight."

**The difference:** Grounded detail is specific, often mundane, sometimes incongruous. It does not interpret itself. It trusts the reader to feel the weight.
