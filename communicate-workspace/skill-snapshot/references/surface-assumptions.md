# Surface Assumptions

Make explicit the unstated premises reasoning depends on.

## Diagnostic Question

Ask: What must be true for this reasoning to hold?
What premises operate silently beneath the visible argument? What would break if an assumption proved false?

## Instructions

1. **Trace logical dependencies** - Find what must be true for each claim to hold. Look for skipped steps that seem obvious. Ask what someone who disagrees would challenge as unjustified leaps.

2. **Name background knowledge dependencies** - Detect specialized terminology, referenced concepts, or prior knowledge used without establishment. What feels like common ground may be expertise.

3. **State value judgments as values** - Find claims about what matters, what's important, what should be prioritized. Words like "obviously" or "clearly" signal judgments treated as self-evident. State directly when making value claims versus factual claims.

4. **Define key terms explicitly** - Identify terms with multiple valid interpretations. Abstract concepts (quality, performance, simplicity, good design) mean different things to different people. Define usage for this specific context.

5. **Test independent evaluability** - Check whether someone starting from different premises could understand why these conclusions were reached. Could they articulate the reasoning using only explicit content?

6. **Focus disclosure on validity-affecting assumptions** - Evaluate which assumptions shape argument validity versus which form shared ground. Surface premises that enable reasoning evaluation.

7. **Position assumptions at dependency points** - Place assumption disclosure where readers need it for evaluation. State foundational premises before dependent arguments. Define terms at introduction.

## Examples

### Making technical assumptions visible

**Draft**: "We chose eventual consistency because it provides better availability and performance. Strong consistency would create unacceptable latency for users distributed globally."

**Hidden assumptions**: CAP theorem knowledge, consistency model definitions, shared values about "unacceptable" latency, agreement that availability outweighs consistency here.

**Revised**: "In distributed systems, we face a trade-off between consistency (all nodes see same data immediately) and availability (system responds despite unreachable nodes). We prioritized availability: users expect instant UI response during network partitions, and showing slightly stale data (up to 5 seconds) beats showing error messages. This assumes users value responsiveness over perfect accuracy for this interaction."

Now evaluable: Is the user value assumption correct? Is 5 seconds acceptable staleness?

### Surfacing value assumptions

**Draft**: "We should migrate to microservices because our monolith has become unmaintainable."

**Hidden value judgments**: Maintainability problems justify migration cost, microservices solve these specific issues better than alternatives, deployment flexibility worth operational complexity trade.

**Revised**: "Our monolith deployment takes 45 minutes and requires cross-team release coordination, slowing deployment frequency from daily to weekly. I recommend microservices because faster independent deployment per team is worth increased operational overhead of multiple services. This assumes we value deployment flexibility over operational simplicity, our team has distributed systems expertise, and monolith coordination cost exceeds service integration cost. If we don't share those assumptions, improving monolith modularity without distributing it might serve better."

Now engageable: Readers can evaluate the value trade-offs directly.

### Defining ambiguous terms

**Draft**: "This codebase has serious quality problems that need immediate attention."

**Definitional ambiguity**: "Quality problems" could mean performance, bugs, security, readability, test coverage, coupling, or combinations.

**Revised**: "I'm defining quality problems as issues increasing the cost of making changes safely. This codebase lacks automated tests (95% no coverage), uses inconsistent naming (navigation difficulty), and has tight module coupling (changes ripple unexpectedly). These aren't performance or security problems—the code works correctly in production. Making changes requires extensive manual testing and risks breaking unrelated functionality. When I say this needs immediate attention, I'm prioritizing system evolution ability over short-term feature velocity."

Now precise: Readers understand the specific definition and can evaluate whether issues deserve priority.
