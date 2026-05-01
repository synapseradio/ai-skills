# Bound Scope

Define where claims apply and where they break down, making applicability boundaries explicit.

## Diagnostic Question

Ask: Where does this claim apply, and where does it break down?
What boundary conditions go unstated? What contexts would invalidate these claims? Where does advice sound universal when it should be qualified?

## Instructions

1. **State the core claim** - Identify what's actually asserted. Vague claims resist scoping. Specific claims reveal natural limits.

2. **Define applicability conditions** - State what must be true for this to work: required context, necessary assumptions, prerequisite conditions. Claims transfer only to contexts sharing these characteristics.

3. **Identify where it breaks** - Find boundary conditions where core assumptions fail. At what scale do different forces dominate? Where do alternatives serve better? What invalidates the foundation?

4. **Test edge cases** - Examine ambiguous situations near boundaries. Do they fall inside or outside? Sharp boundaries have clear tests. Fuzzy boundaries require judgment.

5. **Name alternative contexts** - Specify situations where different approaches fit: different problems, different scales, different constraints. State what following this advice would create friction against.

6. **Frame with conditions** - Express scoped claims as conditionals: "This applies when X, breaks when Y." Build scope into the claim structure.

7. **Distinguish strength gradients** - Separate strong application from weak application. Not all valid contexts sit equally close to the ideal. Some require adaptation.

## Examples

### Scoping architectural advice

**Claim**: "Microservices improve system scalability and team independence."

**Where it applies**: Multiple teams on separable business capabilities, independent deployment value, operational maturity for distributed systems, scale where monolithic coordination costs exceed microservice overhead.

**Where it breaks**: Early-stage products with small teams (no independence benefit), tight transactional consistency requirements (fights service boundaries), weak DevOps culture (operational complexity drowns benefit), unclear domain boundaries (chatty dependencies destroy performance).

**Edge cases**: Three services (distribution cost without full independence), five-person distributed team (might benefit from splitting), read-heavy workloads (scaling benefit before massive scale).

**Scoped claim**: "Microservices improve scalability and team independence when you have multiple teams on separable capabilities, operational maturity, and scale where coordination costs exceed distribution costs. They create net complexity for early-stage products, small teams, coupled domains, or weak DevOps culture."

### Scoping research findings

**Claim**: "Remote work increases productivity by 15% compared to office work."

**Measurement domain**: Knowledge workers in software development, companies with remote infrastructure, metrics of self-reported productivity and commit frequency.

**Validity assumptions**: Work measurable through individual output (not collaboration), suitable home workspace, role lacks physical presence requirements, team coordination works async.

**Where it breaks**: Collaborative design work (spontaneous interaction loss), new employees (onboarding proximity benefits), physical equipment roles, weak documentation culture.

**Scoped claim**: "Remote work shows ~15% productivity gains for individual knowledge work in software development, particularly for experienced employees with home workspace at companies with remote infrastructure and async culture. Gains don't generalize to collaborative roles, physical work, new employees, or high-bandwidth real-time coordination needs."

### Scoping design patterns

**Claim**: "Caching solves performance problems by storing computed results for reuse."

**Where it applies**: Computation expensive relative to storage/retrieval, recurring inputs justify overhead, deterministic results or tolerable staleness, working set fits cache capacity.

**Where it breaks**: Constantly changing data (invalidation overhead exceeds benefit), unique queries (never repeat, waste space), real-time requirements (staleness unacceptable), working set exceeds capacity (thrashing destroys performance).

**Scoped claim**: "Caching solves performance problems for expensive computations with recurring inputs and tolerable staleness, when working sets fit capacity. It creates overhead without benefit for constantly changing data, unique queries, real-time requirements, or memory constraints."
