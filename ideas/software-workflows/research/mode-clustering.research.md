# Mode Clustering Research

Research into the 28 mode reference files across the software plugin's four skills (assess, design, implement, refactor), clustering them into natural engineering workflows.

## Part 1: Individual Mode Analysis

### assess/ (12 modes)

| Mode | Engineering Task | Phase | Natural Pairings |
|------|-----------------|-------|------------------|
| **archaeology** | Recovering lost context about why code exists | Early understanding | dependency, documentation-audit, annotation, type-intention |
| **assumptions** | Surfacing and verifying unproven claims about behavior | Analysis/verification | failure-modes, blast-radius, second-order-effects |
| **blast-radius** | Mapping the full scope of what a change affects | Analysis (pre-change) | failure-modes, second-order-effects, assumptions |
| **cartography** | Building a mental map of unfamiliar code | Early understanding (orientation) | dependency, flow, archaeology |
| **constraint-inventory** | Enumerating hard/soft limits before exploring solutions | Early understanding (problem framing) | trade-space, good-enough-threshold, abstraction-level |
| **dependency** | Mapping coupling structure between modules | Analysis (structural) | flow, cartography, archaeology |
| **failure-modes** | Enumerating specific ways code can fail at boundaries | Analysis (risk) | second-order-effects, assumptions, blast-radius |
| **flow** | Tracing data movement and transformation through runtime | Analysis (behavioral) | archaeology, dependency, type-intention |
| **interface-stability** | Predicting which aspects of an interface might change | Analysis (risk/prediction) | blast-radius, failure-modes, second-order-effects |
| **migration-path** | Planning safe transitions for breaking changes | Action (planning) | commit-strategy, blast-radius, documentation-audit |
| **second-order-effects** | Tracing how changes propagate beyond immediate impact | Analysis (consequence) | assumptions, failure-modes, blast-radius |
| **trade-space** | Mapping what each approach optimizes and sacrifices | Analysis (decision) | good-enough-threshold, constraint-inventory, surface-complexity |

### design/ (6 modes)

| Mode | Engineering Task | Phase | Natural Pairings |
|------|-----------------|-------|------------------|
| **abstraction-level** | Deciding whether to extract shared code | Analysis (structural design) | trade-space, surface-complexity, constraint-inventory |
| **good-enough-threshold** | Recognizing when to stop working | Verification (sufficiency) | surface-complexity, trade-space, constraint-inventory |
| **surface-complexity** | Distinguishing essential from accidental complexity | Analysis (complexity) | abstraction-level, trade-space, good-enough-threshold |
| **type-analytical** | Analyzing type constraints as logical claims | Analysis (type verification) | type-generative, type-intention, failure-modes |
| **type-generative** | Writing type signatures before implementation | Action (type design) | type-analytical, failure-modes, type-intention |
| **type-intention** | Recovering the implicit question a type answers | Early understanding (type archaeology) | archaeology, type-generative, annotation |

### implement/ (4 modes)

| Mode | Engineering Task | Phase | Natural Pairings |
|------|-----------------|-------|------------------|
| **commit-strategy** | Decomposing and sequencing commits for coherent history | Action (delivery) | selective-stage, rebase-safety, migration-path |
| **error-clarification** | Converting error handling to PAGE protocol (guided errors) | Action (implementation) | structural, annotation, documentation-audit |
| **investment-timing** | Deciding when to invest effort (now vs. later) | Decision (meta-planning) | commit-strategy, failure-modes |
| **selective-stage** | Staging specific lines/hunks for precise commits | Action (delivery mechanics) | commit-strategy, rebase-safety |

### refactor/ (6 modes)

| Mode | Engineering Task | Phase | Natural Pairings |
|------|-----------------|-------|------------------|
| **annotation** | Adding comments that explain why code exists | Action (documentation) | archaeology, documentation-audit, structural |
| **conflict-topology** | Mapping merge conflict structure for resolution | Action (conflict resolution) | investment-timing, blast-radius |
| **documentation-audit** | Verifying documentation accuracy against code | Verification | error-clarification, archaeology, structural |
| **rebase-safety** | Planning rebase operations with recovery points | Action (history management) | commit-strategy, conflict-topology |
| **structural** | Making code speak its intent through naming and structure | Action (clarity refactoring) | annotation, documentation-audit, abstraction-level |
| **vestigial** | Detecting and removing obsolete code | Action (cleanup) | structural, documentation-audit, commit-strategy |

---

## Part 2: Observed Phase Distribution

Across the 28 modes, the phases distribute as:

- **Early understanding** (4): cartography, archaeology, constraint-inventory, type-intention
- **Analysis** (10): assumptions, blast-radius, dependency, failure-modes, flow, interface-stability, second-order-effects, trade-space, surface-complexity, type-analytical, abstraction-level
- **Decision** (2): investment-timing, good-enough-threshold
- **Action/Planning** (9): migration-path, type-generative, commit-strategy, error-clarification, selective-stage, annotation, conflict-topology, rebase-safety, structural, vestigial
- **Verification** (2): documentation-audit, good-enough-threshold (dual role)

The distribution is heavily weighted toward analysis (10+ modes) and action (9+ modes), with fewer modes for the orientation and verification phases of engineering work.

---

## Part 3: Proposed Workflow Clusters

### Workflow 1: Codebase Onboarding

**What engineers call it:** "Getting oriented" / "Understanding the codebase"

Engineers joining a project or approaching unfamiliar code need to build a working mental model before they can contribute.

| Phase | Mode | Role in Workflow |
|-------|------|-----------------|
| 1. Orient | **cartography** | Map territories, entry points, patterns |
| 2. Trace structure | **dependency** | Understand coupling, layers, boundaries |
| 3. Trace behavior | **flow** | Follow data through runtime paths |
| 4. Recover context | **archaeology** | Understand why odd patterns exist |
| 5. Read types | **type-intention** | Recover the questions types answer |

**Gaps:** No mode for "read the tests to understand expected behavior" -- test-as-specification reading. Also no mode for understanding configuration and environment setup, though cartography partially covers this.

---

### Workflow 2: Change Impact Assessment

**What engineers call it:** "What will this break?" / "Risk assessment"

Before making a non-trivial change, engineers need to understand what they are touching and what might go wrong.

| Phase | Mode | Role in Workflow |
|-------|------|-----------------|
| 1. Scope the change | **blast-radius** | Map everything the change affects |
| 2. Check stability | **interface-stability** | Predict which contracts might shift |
| 3. Surface assumptions | **assumptions** | Verify claims about affected code |
| 4. Enumerate failures | **failure-modes** | Map how the change can fail at boundaries |
| 5. Trace consequences | **second-order-effects** | Follow the cascade beyond direct impact |

**Gaps:** No mode for "run the change and observe what actually breaks" -- an empirical validation step after the analytical ones. The assumptions mode partially covers this with its "run the experiment" phase, but it is not change-specific.

---

### Workflow 3: Design Decision-Making

**What engineers call it:** "Choosing an approach" / "Design review"

When multiple solutions exist, engineers need to frame the decision space, evaluate options, and commit to one with clear reasoning.

| Phase | Mode | Role in Workflow |
|-------|------|-----------------|
| 1. Frame constraints | **constraint-inventory** | Enumerate what limits the solution space |
| 2. Analyze complexity | **surface-complexity** | Distinguish essential from accidental complexity |
| 3. Map trade-offs | **trade-space** | Plot options against competing qualities |
| 4. Evaluate abstraction | **abstraction-level** | Decide extraction vs. duplication |
| 5. Determine sufficiency | **good-enough-threshold** | Recognize when to stop |

**Gaps:** No mode for "present the decision to others and capture their input" -- a collaborative review/ADR-creation step. Archaeology partially covers ADR creation in its preservation phase, but it is oriented toward past decisions, not present ones being made.

---

### Workflow 4: Type-Driven Development

**What engineers call it:** "Types first" / "Designing the interface"

Engineers working in typed codebases use types as a thinking and specification tool before writing implementation.

| Phase | Mode | Role in Workflow |
|-------|------|-----------------|
| 1. Understand existing types | **type-intention** | Recover what existing types encode |
| 2. Analyze constraints | **type-analytical** | Verify guarantees, permissions, escape hatches |
| 3. Design new types | **type-generative** | Write signatures that encode contracts |
| 4. Verify design | **type-analytical** (again) | Confirm drafted types express intent |

**Gaps:** No mode for "evolve types as implementation reveals mismatches" -- an iterative refinement step. The generative mode mentions iteration but doesn't structure it. Also no mode for type migration when existing types need breaking changes (migration-path is API-focused, not type-system-focused specifically).

---

### Workflow 5: Safe Breaking Changes

**What engineers call it:** "Migration" / "Deprecation and cutover"

When changes must break existing contracts, engineers need a structured approach from scoping through execution to verification.

| Phase | Mode | Role in Workflow |
|-------|------|-----------------|
| 1. Scope impact | **blast-radius** | Find everything that depends on the contract |
| 2. Check stability | **interface-stability** | Assess which parts can change safely |
| 3. Trace consequences | **second-order-effects** | Predict cascading effects |
| 4. Plan transition | **migration-path** | Design coexistence, steps, rollback |
| 5. Structure delivery | **commit-strategy** | Decompose into reviewable, revertible commits |
| 6. Verify documentation | **documentation-audit** | Ensure migration guides are accurate |

**Gaps:** No mode for "monitor adoption and success metrics during rollout" -- a post-deployment observation step. Migration-path defines success criteria but doesn't cover the monitoring execution.

---

### Workflow 6: Code Cleanup / Debt Reduction

**What engineers call it:** "Refactoring" / "Tech debt sprint"

Improving existing code quality without changing behavior, from detection through execution to verification.

| Phase | Mode | Role in Workflow |
|-------|------|-----------------|
| 1. Decide timing | **investment-timing** | Determine if now is the right time |
| 2. Detect dead code | **vestigial** | Find obsolete code to remove |
| 3. Analyze complexity | **surface-complexity** | Distinguish essential from accidental complexity |
| 4. Improve structure | **structural** | Improve naming, flow, readability |
| 5. Add reasoning | **annotation** | Document non-obvious decisions |
| 6. Verify docs | **documentation-audit** | Update documentation to match |
| 7. Stage cleanly | **commit-strategy** + **selective-stage** | Structure commits for reviewability |

**Gaps:** No mode for "verify behavior preservation" -- confirming tests still pass and behavior is unchanged. This is the refactoring safety net that distinguishes refactoring from rewriting.

---

### Workflow 7: Git History Management

**What engineers call it:** "Cleaning up my branch" / "Preparing for merge"

Before merging, engineers clean up commit history, resolve conflicts, and ensure the branch tells a coherent story.

| Phase | Mode | Role in Workflow |
|-------|------|-----------------|
| 1. Plan commits | **commit-strategy** | Identify logical units and sequence |
| 2. Stage precisely | **selective-stage** | Stage specific hunks per commit |
| 3. Plan rebase | **rebase-safety** | Assess risk and create recovery points |
| 4. Resolve conflicts | **conflict-topology** | Map and resolve merge conflicts |

**Gaps:** No mode for "write good PR descriptions" or "prepare for code review" -- framing the work for reviewers. Commit strategy covers individual commit messages but not the overall narrative of a PR.

---

### Workflow 8: Production Error Investigation

**What engineers call it:** "Debugging" / "Incident investigation"

When something fails in production, engineers need to trace what happened, understand why, and fix it safely.

| Phase | Mode | Role in Workflow |
|-------|------|-----------------|
| 1. Trace the flow | **flow** | Follow data through the failing path |
| 2. Surface assumptions | **assumptions** | Verify what was believed about the system |
| 3. Recover history | **archaeology** | Understand why the failing code exists |
| 4. Map failure boundaries | **failure-modes** | Enumerate what else could fail similarly |
| 5. Scope the fix | **blast-radius** | Understand what the fix will affect |

**Gaps:** Two significant gaps. No mode for "reproduce the problem" -- an empirical reproduction step before analysis. No mode for "write the regression test" -- capturing the failure as a test before fixing. These are the two bookends of a debugging workflow (prove it is broken, prove it is fixed).

---

## Part 4: Cross-Workflow Observations

### Modes that appear in multiple workflows

| Mode | Workflows | Role Pattern |
|------|-----------|-------------|
| **blast-radius** | Impact Assessment, Breaking Changes, Debugging | Always a scoping step -- "how big is this?" |
| **failure-modes** | Impact Assessment, Debugging | Always a risk enumeration step |
| **assumptions** | Impact Assessment, Debugging | Always a verification step |
| **second-order-effects** | Impact Assessment, Breaking Changes | Always a consequence-tracing step |
| **commit-strategy** | Breaking Changes, Cleanup, History Management | Always a delivery structuring step |
| **documentation-audit** | Breaking Changes, Cleanup | Always a final verification step |
| **surface-complexity** | Decision-Making, Cleanup | Analytical step in both planning and execution contexts |

### Modes that appear in only one workflow

| Mode | Workflow | Observation |
|------|----------|-------------|
| **constraint-inventory** | Decision-Making | Could also serve Onboarding (understanding system limits) |
| **interface-stability** | Impact Assessment + Breaking Changes | Narrowly scoped to API contracts |
| **error-clarification** | None (orphaned) | Highly specific to PAGE protocol; does not naturally cluster |
| **investment-timing** | Cleanup | Could also serve Impact Assessment (decide whether to fix) |
| **conflict-topology** | History Management | Narrowly scoped to git conflicts |

### The error-clarification outlier

`error-clarification` is the only mode that does not naturally fit into any workflow cluster. It serves a specific implementation pattern (converting errors to PAGE protocol) rather than an engineering reasoning activity. It is more of a "recipe" than an analytical mode -- it tells you exactly what code to write rather than how to think about a problem. This suggests it may belong as a command or template rather than as a reasoning mode alongside the others.

---

## Part 5: Recurring Gaps

Three categories of missing capability appear across multiple workflows:

### 1. Empirical verification modes

Workflows 2, 6, and 8 all lack a step for "run it and observe what actually happens." The assumptions mode covers this partially for behavioral claims, but there is no mode specifically for:

- Reproducing a reported problem
- Verifying refactoring preserved behavior
- Confirming a change works as predicted after analytical assessment

### 2. Test-oriented modes

No mode addresses tests as a first-class reasoning artifact:

- Reading tests to understand expected behavior (Onboarding gap)
- Writing regression tests to capture failures (Debugging gap)
- Verifying test coverage after changes (Cleanup gap)

### 3. Collaborative/communication modes

No mode addresses the social dimension of engineering:

- Writing PR descriptions that tell a story
- Presenting design decisions for review
- Documenting decisions being made now (vs. archaeology's focus on past decisions)
- Communicating migration status to stakeholders

---

## Part 6: Summary Table

| # | Workflow | Mode Count | Modes | Key Gap |
|---|----------|-----------|-------|---------|
| 1 | Codebase Onboarding | 5 | cartography, dependency, flow, archaeology, type-intention | Test-as-spec reading |
| 2 | Change Impact Assessment | 5 | blast-radius, interface-stability, assumptions, failure-modes, second-order-effects | Empirical validation |
| 3 | Design Decision-Making | 5 | constraint-inventory, surface-complexity, trade-space, abstraction-level, good-enough-threshold | Decision documentation/ADR |
| 4 | Type-Driven Development | 3 | type-intention, type-analytical, type-generative | Iterative type refinement |
| 5 | Safe Breaking Changes | 6 | blast-radius, interface-stability, second-order-effects, migration-path, commit-strategy, documentation-audit | Rollout monitoring |
| 6 | Code Cleanup | 7+ | investment-timing, vestigial, surface-complexity, structural, annotation, documentation-audit, commit-strategy, selective-stage | Behavior preservation verification |
| 7 | Git History Management | 4 | commit-strategy, selective-stage, rebase-safety, conflict-topology | PR narrative preparation |
| 8 | Production Error Investigation | 5 | flow, assumptions, archaeology, failure-modes, blast-radius | Reproduction and regression testing |

28 modes total. 26 placed in at least one workflow. 2 weakly placed: `error-clarification` (orphaned -- protocol recipe, not reasoning mode), `investment-timing` (placed in Cleanup but applicable more broadly as a meta-decision mode).
