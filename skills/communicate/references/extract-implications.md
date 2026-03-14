# Extract Implications

Surface what follows from stated claims to make the full reach of assertions visible.

## Diagnostic Question

Ask: What follows from these claims that goes unsaid?
What consequences, requirements, or contradictions lurk in the logical wake? What implications deserve explicit attention?

## Instructions

1. **Identify claims and assertions** - Detect statements that make factual claims, take positions, or commit to principles. Mark where prose asserts "X is true" or "we should do Y" or "this approach works because Z." These are anchor points where implications radiate outward.

2. **Trace logical consequences** - Examine what must be true if the claim holds. If someone asserts "all documentation should be comprehensive," that commits them to documentation taking significant time, to valuing thoroughness over speed. The claim carries these consequences whether or not they're acknowledged.

3. **Surface unstated commitments** - Detect positions that commit to values, priorities, or approaches without naming them. "We should always test before deploying" implies that safety matters more than speed, that prevention beats remediation. Make these implicit commitments explicit.

4. **Distinguish direct implications from speculative extensions** - Separate what necessarily follows from what might follow. If "code should be readable" then it follows that readability has priority over brevity when they conflict. It does not necessarily follow that comments are required everywhere. Mark this distinction clearly.

5. **Examine implications across domains** - Check what a claim implies:
   - **Practically**: what actions it demands or prohibits
   - **Epistemically**: what it requires knowing or assuming
   - **Ethically**: what values it prioritizes
   - **Systematically**: how it changes adjacent practices or structures

6. **Articulate reach without overreach** - State clearly what follows while avoiding projecting implications the claim doesn't actually carry. Test: if someone accepts the claim, must they also accept this consequence?

## Examples

### From policy claim to visible commitments

**Claim**: "All code changes should require review by at least two other developers before merging."

**Direct implications**:

- Development velocity will decrease (every change waits for two reviewers)
- Team size affects feasibility (teams smaller than three cannot sustain this)
- Solo work becomes impossible (no individual can ship independently)
- Review quality matters (perfunctory reviews provide security theater)

**Epistemic commitments**:

- Individual judgment is insufficient (assumes two perspectives catch what one misses)
- Defects are more costly than delay (values prevention over speed)

**Systematic implications**:

- Review becomes a bottleneck requiring management
- Knowledge distribution across the team matters more
- The policy itself requires justification (why two, not three?)

Making implications explicit enables honest evaluation of whether commitments align with actual constraints and values.

### From design principle to unstated consequences

**Claim**: "User interfaces should be intuitive."

**Direct implications**:

- "Intuitive" requires a reference population (intuitive to whom?)
- Designing for existing mental models rather than training new ones
- Features that don't map to existing intuition become questionable
- Discovery through exploration valued over discovery through instruction

**Practical implications**:

- Design process must include user research
- Novel interaction paradigms face higher burden of proof
- Documentation can't compensate for unintuitive interfaces

**The tension it creates**:

- Innovation often requires going beyond intuition
- "Intuitive" for different user groups may conflict
- What's intuitive initially may not be optimal for sustained use

Extracting implications reveals that "interfaces should be intuitive" isn't a simple truism—it's a position with significant reach.

### From architectural claim to cascading commitments

**Claim**: "Services should be stateless to enable horizontal scaling."

**Direct implications**:

- State must live somewhere (pushes complexity to databases, caches, or client-side)
- Every request must be self-contained
- Sessions become more complex

**Practical consequences**:

- Response times may increase (fetching state from external storage adds latency)
- Debugging changes character (can't inspect running service memory)
- Some use cases become harder (real-time features with rapidly changing state)

**Epistemic assumptions**:

- Horizontal scaling is the primary scaling concern
- Statelessness is achievable for the domain
- Costs of externalizing state are worth the scaling benefits

Making implications visible enables evaluating whether the claim serves actual needs.
