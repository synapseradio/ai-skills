# Dimensionalize

Separate monolithic concepts into distinct improvable dimensions.

## Diagnostic Question

Ask: Where does feedback conflate distinct concerns?
What independent aspects hide behind "needs work" or similar labels? Can the monolithic assessment be separated into improvable dimensions?

## Instructions

1. **Detect false unity** - Identify when a concept appears as one thing but actually represents several independent aspects. Mark places where judgments collapse multiple qualities into single verdicts ("this is good", "that's unclear", "needs improvement").

2. **Separate independent axes** - Distinguish dimensions that can vary without affecting each other. Clarity and completeness are separate—something can be crystal clear but incomplete, or exhaustive but confusing. Identify what aspects could be improved independently.

3. **Name dimensions precisely** - Articulate each axis with specificity. Not "quality" but "semantic precision," "structural coherence," and "implementation feasibility" as distinct dimensions. Use language that points to what can be observed and changed.

4. **Map variation along each axis** - Show how each dimension spans a range. "Semantic precision" varies from ambiguous through adequate to technically exact. Making variation explicit reveals where something sits on each dimension independently.

5. **Reveal hidden trade-offs** - Dimensionalizing exposes that improving one aspect may constrain another. Increasing technical precision often reduces accessibility. Maximizing completeness can hurt clarity. These trade-offs become visible only when dimensions are separated.

6. **Enable targeted feedback** - Transform undifferentiated judgments into dimensional assessments. Instead of "this needs work," specify "this has high structural coherence but low semantic precision in the third section."

## Examples

### From "this is unclear" to dimensional diagnosis

Someone says "this is unclear." That judgment conflates multiple dimensions.

**Dimensional analysis**:

- **Semantic precision**: The words used—whether they point at specific referents. This section uses "things" and "stuff" where it should name entities. *Low precision.*
- **Structural coherence**: How ideas connect. Logic jumps from point A to C without showing B. *Moderate coherence with gaps.*
- **Syntactic grounding**: Whether sentences have grammatical scaffolding. Proper articles and linking verbs. *High grounding.*
- **Conceptual accessibility**: Whether readers can grasp without specialized knowledge. Assumes undefined terminology. *Low accessibility.*

The original "unclear" hid that semantic precision and conceptual accessibility are the problems, while syntactic grounding is actually fine. Dimensional breakdown reveals that fixing word choice and adding definitions would address most of the "unclear" feeling without restructuring sentences.

### From "good code" to separable qualities

Someone describes a codebase as "good code."

**Independent dimensions**:

- **Readability**: Variable naming, formatting, visual structure. *High readability.*
- **Correctness**: Expected outputs for all inputs. Tests pass, edge cases handled. *High correctness.*
- **Performance**: Speed and resource usage. Currently O(n²) where O(n log n) possible. *Moderate performance.*
- **Maintainability**: Ease of change—coupling, modularity. Functions tightly coupled, changes ripple. *Low maintainability.*
- **Testability**: Ease of verification. Hard to mock dependencies. *Low testability.*

The code is "good" along readability and correctness, "okay" on performance, "poor" on maintainability and testability. Recognizing these as separate axes means we can improve maintainability without touching correct logic.

### From "that writing is professional" to component qualities

Someone praises writing as "professional."

**Writing dimensions**:

- **Tone formality**: Register and distance. *Moderate formality without stiffness.*
- **Structural clarity**: Organization, findability. *High structural clarity.*
- **Technical precision**: Accuracy of terminology. *High precision.*
- **Audience appropriateness**: Matching expertise level. *Appropriate for experts, less so for general readers.*
- **Voice consistency**: Perspective stability. *Moderate consistency with variation.*

"Professional" likely referred to tone formality and technical precision. But voice consistency is moderate and audience appropriateness depends on who's reading. The same document can be "professional" for experts and "inaccessible" for newcomers without contradiction—different dimensions being measured.

## Why Dimensionalizing Helps

Monolithic concepts hide what can be addressed independently. When someone says "make this better," they've collapsed multiple dimensions into one judgment. Until those dimensions separate, action is guessing.

Dimensionalizing transforms vague feedback into actionable guidance. It reveals trade-offs invisible when everything is "good" or "bad" as single verdict. The transformation from "this needs improvement" to "this has high correctness and low maintainability" tells someone exactly what to change.
