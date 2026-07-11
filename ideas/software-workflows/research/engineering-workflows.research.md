# Engineering Workflows in Practice vs. Current Software Plugin

Research into the natural workflows engineers follow, mapped against the current
`plugins/software/` skill structure (assess, design, implement, refactor).

---

## Current Plugin Inventory

| Skill | Modes | Coverage |
|-------|-------|----------|
| **assess** | 12 modes across Understanding (cartography, dependency, flow, archaeology), Assessment (failure modes, second-order effects, interface stability, blast radius, assumptions), Scoping (constraint inventory, trade space, migration path) | Pre-action investigation and risk evaluation |
| **design** | 6 modes across Type Design (generative, analytical, intention) and Abstraction/Complexity (abstraction-level, surface-complexity, good-enough-threshold) | Structural decisions before and during implementation |
| **implement** | 4 modes: commit-strategy, selective-stage, investment-timing, error-clarification | Version control discipline and error communication |
| **refactor** | 6 modes across Code Clarity (structural, annotation, documentation-audit), VCS Hygiene (rebase-safety, conflict-topology), Code Health (vestigial) | Improving existing code without behavior change |

---

## Workflow 1: Codebase Onboarding

### How engineers actually do it

Research from GitHub engineers (Ellich, 2025) and legacy code onboarding frameworks identify
a consistent progression:

**Phase 1 -- Orient.** Build a high-level spatial map. Engineers ask: "What are the major
modules? Where does execution start? What are the boundaries?" They draw diagrams, identify
entry points, and build "black box" mental models of components. Visual tools (Figma,
whiteboards, architecture diagrams) dominate this phase.

**Phase 2 -- Trace.** Follow data through the system along specific paths. Pick a concrete
request or user action and trace it end-to-end. This grounds the abstract map in runtime
behavior. Engineers deliberately break things in development to observe failure modes.

**Phase 3 -- Anchor.** Gain foothold through small, concrete tasks ("Good First Issues").
Hands-on code exploration builds procedural memory that reading cannot. Writing tests to
verify understanding is a common tactic.

**Phase 4 -- Document.** Create personal reference material---command cheat sheets, decision
logs, architecture maps. This forces gap identification. The GitHub blog recommends maintaining
a living document of discoveries and questions.

**Phase 5 -- Validate.** Teach what you learned. Write internal guides, contribute to official
documentation. If you cannot explain it, you do not understand it. Self-check questions:
"Can I describe the system in a few sentences? What surprised me? What remains unclear?"

Sources:

- [How GitHub engineers learn new codebases](https://github.blog/developer-skills/application-development/how-github-engineers-learn-new-codebases) (Ellich, 2025)
- [Legacy Code Onboarding in 2 Hours](https://pvizgenerator.com/blog/legacy-code-onboarding-2-hours) (PViz, 2026)
- [Understanding Codebase like a Professional](https://arxiv.org/html/2504.04553v3) (Gao et al., arXiv)

### Current plugin coverage

| Phase | Plugin Mode | Coverage Quality |
|-------|------------|-----------------|
| Orient | assess:cartography | Strong -- explicitly designed for spatial orientation |
| Trace | assess:flow, assess:dependency | Strong -- covers data tracing and coupling |
| Anchor | (none) | **Gap** -- no mode for learning-by-doing through small tasks |
| Document | refactor:annotation, refactor:documentation-audit | Partial -- these focus on improving existing docs, not creating learning artifacts |
| Validate | (none) | **Gap** -- no mode for teaching-to-verify or self-assessment |

### Gaps

1. **Learning-by-doing support.** No mode helps an engineer select and execute a first
   task that maximizes learning. This would involve identifying high-signal, low-risk
   entry points in the codebase.

2. **Personal knowledge capture.** The documentation modes focus on improving codebase
   docs, not on building personal mental models. A mode for structured note-taking during
   exploration (what I found, what surprised me, what remains unclear) is missing.

3. **Domain understanding.** No mode bridges from code structure to business domain
   knowledge. Engineers report that domain understanding is prerequisite to codebase
   mastery, but assess focuses on code topology.

### Tooling opportunities

- Auto-generate architecture diagrams from import graphs and call chains
- Identify "good first issue" candidates by finding well-tested, low-coupling modules
- Produce guided walkthroughs that trace a specific user action through the codebase
- Create onboarding checklists calibrated to codebase size and complexity

---

## Workflow 2: Making a Risky Change

### How engineers actually do it

When engineers face a change they are unsure about, they follow a pattern that interleaves
investigation with incremental action:

**Phase 1 -- Scope the fear.** Identify precisely what they are afraid of. Is it data loss?
Breaking a contract? Introducing a subtle regression? The fear itself is diagnostic---it
points to the axis of risk.

**Phase 2 -- Map the blast radius.** Before touching code, trace what the change will
affect. Engineers use IDE "find references," grep for callers, examine test coverage maps,
and check dependency graphs. Meta's Diff Risk Score system (2025) automates this by predicting
likelihood of regression from diff characteristics.

**Phase 3 -- Build a safety net.** Write characterization tests that capture current behavior
before changing it. Add logging or feature flags. Create rollback plans. The goal is to make
the change reversible and observable.

**Phase 4 -- Execute incrementally.** Make the smallest possible change, verify it, then
expand. Experienced engineers resist the temptation to refactor adjacent code simultaneously.
Each increment is independently verifiable.

**Phase 5 -- Verify and monitor.** Run existing tests, run new characterization tests, deploy
behind a flag, watch metrics. The change is not "done" until it has been observed in
production without incident.

Sources:

- [Diff Risk Score: AI-driven risk-aware software development](https://engineering.fb.com/2025/08/06/developer-tools/diff-risk-score-drs-ai-risk-aware-software-development-meta/) (Meta Engineering, 2025)
- [Pull request intervention for IaC risks](https://www.atlassian.com/blog/atlassian-engineering/pull-request-intervention-for-infrastructure-as-code-risks-with-bitbucket-custom-merge-checks) (Atlassian, 2025)

### Current plugin coverage

| Phase | Plugin Mode | Coverage Quality |
|-------|------------|-----------------|
| Scope the fear | assess:failure-modes, assess:assumptions | Strong |
| Map blast radius | assess:blast-radius, assess:dependency | Strong |
| Build safety net | (none) | **Gap** -- no mode for creating characterization tests or rollback plans |
| Execute incrementally | implement:selective-stage, implement:investment-timing | Partial -- focuses on commit structure, not incremental execution strategy |
| Verify and monitor | (none) | **Gap** -- no mode for post-change verification |

### Gaps

1. **Safety net construction.** The critical step of writing characterization tests before
   a risky change has no dedicated support. This is distinct from assessment (which
   identifies risk) and implementation (which structures commits). It is the act of
   creating mechanical protection against regression.

2. **Incremental execution strategy.** implement focuses on commit discipline, but risky
   changes require a higher-level execution plan: what order to make changes in, where to
   insert verification checkpoints, when to deploy partial changes.

3. **Post-change verification.** No mode covers the "watch and confirm" phase after a
   change lands. This involves monitoring metrics, reviewing logs, and confirming that the
   change behaves as expected in production.

### Tooling opportunities

- Auto-generate characterization tests from runtime behavior before a change
- Suggest feature flag insertion points for risky changes
- Produce incremental change plans that minimize blast radius at each step
- Monitor test coverage deltas for changed code paths

---

## Workflow 3: Tech Debt Cleanup

### How engineers actually do it

Research from engineering leaders and frameworks (CodeIntelligently, Utkrusht, ScopeCone)
reveals a consistent pattern:

**Phase 1 -- Inventory and classify.** Teams catalog debt items and classify them by type:
infrastructure decay, design shortcuts, test gaps, dependency rot, documentation staleness.
The Technical Debt Quadrant framework (Verma) categorizes debt along axes of impact and effort.

**Phase 2 -- Quantify cost.** Measure the ongoing cost of each debt item: deploy time
increases, incident frequency, developer time lost to workarounds. The key insight is that
unmeasured debt cannot be prioritized. Teams track metrics like build times, flaky test rates,
and time-to-resolution for incidents in affected areas.

**Phase 3 -- Prioritize by leverage.** Rank items by the ratio of ongoing cost to cleanup
effort. High-cost, low-effort items go first. Teams often use ROI frameworks that compare
debt remediation against feature development velocity. The ScopeCone framework suggests a
five-step process: measure current velocity, estimate debt cost, calculate cleanup ROI,
allocate budget, track outcomes.

**Phase 4 -- Execute in bounded increments.** Allocate a fixed percentage of sprint capacity
(commonly 15-20%) to debt reduction. Work in small, independently shippable increments.
Avoid "big rewrite" projects. Each increment should leave the system strictly better than
before.

**Phase 5 -- Prevent recurrence.** Update linting rules, CI checks, and coding standards
to prevent the same class of debt from accumulating again. Conduct retrospectives on what
caused the debt to identify systemic issues.

Sources:

- [Technical Debt Quadrant: Prioritization](https://codeintelligently.com/blog/technical-debt-quadrant-framework) (Verma)
- [Measuring and Managing Technical Debt](https://codeintelligently.com/blog/measuring-managing-technical-debt-guide) (Verma, 2026)
- [7 proven ways to tackle huge tech debt](https://utkrusht.ai/blog/tackle-huge-technical-debt) (Muley, 2026)
- [Technical Debt vs Feature Development: ROI Framework](https://scopecone.io/blog/technical-debt-vs-feature-development-roi-framework) (ScopeCone, 2025)

### Current plugin coverage

| Phase | Plugin Mode | Coverage Quality |
|-------|------------|-----------------|
| Inventory and classify | refactor:vestigial, assess:cartography | Partial -- vestigial finds dead code, cartography maps structure, but neither inventories debt systematically |
| Quantify cost | (none) | **Gap** -- no mode for measuring the ongoing cost of debt |
| Prioritize by leverage | assess:trade-space | Partial -- trade-space compares options, but does not model cost-over-time |
| Execute in increments | refactor:structural, implement:* | Partial -- structural refactoring and commit discipline exist, but no higher-level campaign management |
| Prevent recurrence | (none) | **Gap** -- no mode for systemic prevention (linting rules, CI checks, standards updates) |

### Gaps

1. **Debt inventory and classification.** No mode systematically catalogs debt across
   categories. The vestigial mode finds dead code, but tech debt includes far more:
   missing tests, outdated dependencies, design shortcuts, documentation gaps.

2. **Cost quantification.** No mode helps engineers measure the ongoing cost of specific
   debt items. This is the critical input for prioritization.

3. **Campaign management.** Tech debt cleanup is often a multi-sprint effort. No mode
   supports tracking progress across a campaign, managing the backlog of debt items, or
   reporting outcomes.

4. **Prevention mechanisms.** No mode helps engineers create guardrails (linting rules,
   CI checks, architectural decision records) that prevent debt recurrence.

### Tooling opportunities

- Scan for common debt indicators: TODO comments, suppressed lints, uncovered code paths
- Correlate debt locations with incident history and change frequency
- Generate debt dashboards showing inventory, cost estimates, and cleanup progress
- Suggest linting rules or CI checks that would prevent recurrence

---

## Workflow 4: Feature Design

### How engineers actually do it

The progression from requirement to implementation follows a pattern of progressive
concretization:

**Phase 1 -- Understand the need.** Clarify what the feature should accomplish for users.
This is requirements gathering, not code work. Engineers ask: "What problem does this solve?
Who experiences it? What does success look like?" Domain understanding is prerequisite.

**Phase 2 -- Explore the solution space.** Generate multiple possible approaches without
committing to one. Sketch architectures, prototype key interactions, identify technical
constraints early. This phase is deliberately divergent.

**Phase 3 -- Evaluate and converge.** Compare approaches against constraints: performance,
maintainability, compatibility, timeline. Make explicit trade-offs. Document rejected
alternatives and why. The output is a chosen approach with known limitations.

**Phase 4 -- Design the interface.** Define types, APIs, data models, and contracts before
writing implementation. This is where the design skill's type-generative and type-analytical
modes apply. The interface is the commitment---implementation details can change.

**Phase 5 -- Plan the execution.** Break the chosen design into implementable increments.
Each increment should be independently testable and reviewable. Define the order of
implementation, identifying which pieces unblock others.

**Phase 6 -- Implement iteratively.** Execute the plan, but expect deviations. Discovery
during implementation feeds back to design. The plan is a hypothesis, not a contract.

Sources:

- [Software Design Process](https://www.geeksforgeeks.org/software-engineering/software-engineering-software-design-process/) (GeeksforGeeks)
- [SDLC guide](https://www.atlassian.com/agile/software-development/sdlc) (Atlassian)
- [Software Development Process: 7 Phases](https://monday.com/blog/rnd/software-development-process/) (monday.com)

### Current plugin coverage

| Phase | Plugin Mode | Coverage Quality |
|-------|------------|-----------------|
| Understand the need | (none) | **Gap** -- no mode for requirements clarification or user-problem framing |
| Explore solution space | assess:constraint-inventory, assess:trade-space | Partial -- these help map constraints and compare options, but do not support generative exploration |
| Evaluate and converge | assess:trade-space, design:surface-complexity | Partial -- trade-space compares, but the convergence decision itself lacks support |
| Design the interface | design:type-generative, design:type-analytical | Strong -- explicitly designed for this |
| Plan the execution | (none) | **Gap** -- no mode for breaking a design into ordered implementation steps |
| Implement iteratively | implement:*, design:good-enough-threshold | Partial -- commit discipline exists, good-enough helps calibrate completion |

### Gaps

1. **Requirements framing.** No mode helps engineers translate a user need or product
   requirement into technical constraints and success criteria. The assess skill starts
   from code, not from users.

2. **Solution exploration.** No mode supports divergent thinking---generating multiple
   possible approaches before evaluating them. The existing modes help compare known
   options but not generate novel ones.

3. **Execution planning.** No mode breaks a design into an ordered sequence of
   implementation steps with dependency relationships and verification checkpoints.
   This is distinct from commit strategy (which organizes completed work) and distinct
   from design (which defines what to build, not in what order).

### Tooling opportunities

- Generate solution space sketches from requirements and constraints
- Produce implementation plans with dependency ordering and test checkpoints
- Track design decisions and their rationale as architectural decision records
- Identify when implementation diverges from design and prompt for reconciliation

---

## Workflow 5: Debugging

### How engineers actually do it

Two detailed debugging frameworks (Tietz, 2023; Patel, 2024) converge on the same
structure, which also aligns with Julia Evans' "Pocket Guide to Debugging":

**Phase 1 -- Characterize symptoms.** Read the error message thoroughly. Determine scope:
who is affected, when it started, what environments exhibit it. Resist the urge to jump
into code. Understanding the bug's observable behavior is prerequisite to everything else.

**Phase 2 -- Reproduce.** Create a reliable reproduction. Start in the same environment
as the original report, then reduce to minimal reproduction steps. Each failed reproduction
attempt reveals information about the bug's preconditions. Automate reproduction for
intermittent bugs.

**Phase 3 -- Understand the system.** Before using a debugger, build or refresh a mental
model of the involved components. Check recent deployments and changes. Read logs for both
normal and abnormal patterns. Prime your pattern recognition by reading baseline behavior
before examining anomalies.

**Phase 4 -- Hypothesize location.** Form a hypothesis about where (not what) the bug is.
Use bisection strategy: each hypothesis should eliminate roughly half the remaining search
space. Binary search through components, then modules, then functions, then lines.

**Phase 5 -- Test hypothesis.** Instrument the system to validate or invalidate your
hypothesis. Add logging, check input/output at boundaries, use debuggers. Each test
produces information whether the hypothesis is confirmed or refuted. Repeat phases 4-5,
narrowing the search space.

**Phase 6 -- Fix and verify.** Once the root cause is located, fix it. Verify the fix
against the original reproduction. Check for related issues in adjacent code. Sometimes
the fix reveals a deeper design flaw---this feeds back to earlier phases.

Sources:

- [A systematic approach to debugging](https://ntietz.com/blog/how-i-debug-2023/) (Tietz, 2023)
- [A framework for methodically debugging any bug](https://medium.com/@veeralpatel/a-framework-for-methodically-debugging-any-bug-406cfe3abcc6) (Patel, 2024)
- [Systematic Debugging Approach: Root Cause Analysis](https://cursorintro.com/insights/Systematic-Debugging-Approach%3A-Using-Root-Cause-Analysis-Before-Implementation) (Reddit/CursorIntro)

### Current plugin coverage

| Phase | Plugin Mode | Coverage Quality |
|-------|------------|-----------------|
| Characterize symptoms | (none) | **Gap** -- no mode for structured symptom gathering |
| Reproduce | (none) | **Gap** -- no mode for reproduction strategy |
| Understand the system | assess:cartography, assess:flow, assess:dependency | Partial -- these exist but are framed for exploration, not for refreshing context during debugging |
| Hypothesize location | (none) | **Gap** -- no mode for hypothesis-driven location narrowing |
| Test hypothesis | assess:assumptions | Partial -- assumptions mode verifies claims, but debugging hypothesis testing is more specific |
| Fix and verify | implement:* | Partial -- commit discipline applies, but verification strategy is missing |

### Gaps

Debugging is the largest gap in the current plugin. It has **no dedicated skill** despite
being one of the most common and time-consuming engineering activities. While assess:flow
and assess:assumptions are adjacent, they were designed for exploration and verification,
not for the specific cognitive pattern of hypothesis-driven fault isolation.

The key missing capabilities are:

1. **Symptom characterization protocol.** A structured approach to reading error messages,
   determining scope, and documenting the observable bug behavior before investigating.

2. **Reproduction strategy.** Techniques for creating reliable reproductions, minimizing
   reproduction steps, and automating intermittent bug detection.

3. **Bisection/elimination logic.** The core debugging cognitive move: form a hypothesis
   that eliminates half the search space, instrument to test it, repeat. This is a
   distinct reasoning pattern from exploration (assess) or verification (assess:assumptions).

4. **Debugging journal.** A structured way to track what has been tried, what was learned,
   and what remains to investigate. Patel emphasizes this: "Keep a log of what you tried
   and what was the outcome."

### Tooling opportunities

- Structured symptom intake that prompts for scope, timeline, environment, and reproduction
- Auto-bisect using git bisect or runtime instrumentation
- Hypothesis tracking that records tested hypotheses, evidence, and conclusions
- Suggest instrumentation points based on hypothesized bug location
- Produce a debugging report at the end documenting root cause and fix rationale

---

## Workflow 6: Migration/Upgrade

### How engineers actually do it

Migration workflows are characterized by the tension between "changing the engine while
the car is moving" (Dababneh, 2026):

**Phase 1 -- Audit the current state.** Catalog everything that depends on what is being
migrated: consumers, integrations, data formats, implicit contracts. Identify the full
surface area of the breaking change.

**Phase 2 -- Design the bridge.** Create a compatibility layer that allows old and new
to coexist. The Compatibility Layer Pattern (Ann R., 2026) describes this as an adapter
that translates between old and new interfaces, allowing incremental migration. Vercel's
Malte Ubl (2023) argues all migrations must be incremental---big-bang migrations are too
risky.

**Phase 3 -- Build and validate the new path.** Implement the new version alongside the
old, behind the compatibility layer. Validate it works correctly using the same inputs as
the old path. Shadow traffic, canary deployments, and A/B testing are common validation
strategies.

**Phase 4 -- Migrate consumers incrementally.** Move consumers to the new path one at a
time. Each migration is independently reversible. Track migration progress and maintain a
dashboard showing which consumers have migrated and which remain.

**Phase 5 -- Remove the old path.** Once all consumers have migrated and the compatibility
layer is no longer needed, remove the old code path and the adapter. This is the cleanup
phase, and it is often postponed indefinitely (becoming tech debt itself).

Sources:

- [Breaking Changes Without Breaking Teams: Compatibility Layer Pattern](https://medium.com/@annxsa/breaking-changes-without-breaking-teams-the-compatibility-layer-pattern-explained-9ee5e35d1c5b) (Ann R., 2026)
- [Why all migrations should be incremental](https://vercel.com/blog/incremental-migrations) (Ubl/Vercel, 2023)
- [Application migration: step-by-step guide](https://deviniti.com/blog/software-engineering/application-migration-step-by-step-guide/) (Deviniti, 2026)
- [How to shift tools while keeping teams productive](https://www.linkedin.com/pulse/how-shift-tools-while-keeping-teams-productive-euexe) (Dababneh, 2026)

### Current plugin coverage

| Phase | Plugin Mode | Coverage Quality |
|-------|------------|-----------------|
| Audit current state | assess:blast-radius, assess:dependency, assess:interface-stability | Strong |
| Design the bridge | assess:migration-path, design:type-generative | Good -- migration-path plans transitions, type-generative designs new interfaces |
| Build and validate | (none) | **Gap** -- no mode for shadow validation or coexistence testing |
| Migrate incrementally | (none) | **Gap** -- no mode for tracking consumer migration progress |
| Remove old path | refactor:vestigial | Partial -- finds dead code, but migration cleanup requires more targeted removal |

### Gaps

1. **Coexistence strategy.** No mode helps design and validate the parallel operation of
   old and new code paths. This is the critical technical challenge of migration, distinct
   from both design (which creates the new thing) and assess (which evaluates risk).

2. **Migration progress tracking.** No mode supports the multi-step process of moving
   consumers from old to new. This is a campaign-level concern, similar to the tech debt
   campaign gap.

3. **Targeted cleanup.** The vestigial mode finds generally dead code, but post-migration
   cleanup needs to target specific old-path artifacts: compatibility layers, feature
   flags, adapter code. This requires awareness of the migration's structure.

### Tooling opportunities

- Generate compatibility layer scaffolding from interface diffs
- Produce migration checklists from consumer dependency graphs
- Track migration progress (consumers migrated vs. remaining)
- Identify stale compatibility layers that can be removed

---

## Workflow 7: Code Review

### How engineers actually do it

Research from Springer Nature (2026), Microsoft ISE, and practitioner accounts reveals code
review as a multi-pass cognitive process:

**Phase 1 -- Context acquisition.** Understand what the PR is trying to accomplish before
reading code. Read the description, linked issue, and design context. Microsoft ISE guidance
emphasizes: "understand the code you are reviewing" as the first principle.

**Phase 2 -- Design pass.** Evaluate the high-level approach. Does the architecture make
sense? Are the changes logically scoped to this PR? Do the interactions between components
work? This is where the most impactful review comments come from.

**Phase 3 -- Quality pass.** Examine code line by line for complexity, naming, error
handling, security, and style. Microsoft ISE recommends checking: Can the code be understood
easily? Does it add unnecessary functionality? Are functions too complex? Is PII handled
correctly?

**Phase 4 -- Test pass.** Review tests as both documentation and verification. Tests can be
read first to understand intent. Check edge cases, valid assumptions, and that tests are
committed alongside code.

**Phase 5 -- Integration pass.** Consider how the change fits the bigger picture. Can it
have negative effects on the overall system? Are there race conditions? Is documentation
updated? This is the "zoom out" moment that catches systemic issues.

Sources:

- [Code review as decision-making](https://link.springer.com/article/10.1007/s10664-025-10791-2) (Springer Nature, 2026)
- [Reviewer Guidance](https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/reviewer-guidance/) (Microsoft ISE)
- [Code Review as a Team Process](https://maxim-gorin.medium.com/code-review-as-a-team-process-roles-and-accountability-55421d1787f0) (Gorin, 2025)
- [Peer Code Review Checklist](https://jellyfish.co/library/developer-productivity/peer-code-review-best-practices/) (Jellyfish, 2025)
- [Checklist for code review process](https://book.the-turing-way.org/reproducible-research/reviewing/reviewing-checklist.html) (Turing Way, 2025)

### Current plugin coverage

| Phase | Plugin Mode | Coverage Quality |
|-------|------------|-----------------|
| Context acquisition | assess:archaeology | Partial -- archaeology excavates history, but review context is broader |
| Design pass | design:type-analytical, design:surface-complexity | Partial -- these evaluate design quality, but not in a review-specific frame |
| Quality pass | refactor:annotation, implement:error-clarification | Partial -- annotation and error quality are covered, but code quality review is broader |
| Test pass | (none) | **Gap** -- no mode for evaluating test quality and coverage |
| Integration pass | assess:second-order-effects, assess:blast-radius | Partial -- these evaluate consequences, but not in a review-specific frame |

### Gaps

1. **Review as a distinct activity.** Code review is not just "assess + design + refactor
   applied to someone else's code." It has its own cognitive demands: understanding intent
   from a PR description, calibrating feedback tone, managing scope (not blocking for
   out-of-scope issues), and structuring multi-pass review.

2. **Test evaluation.** No mode helps evaluate whether tests are sufficient, whether
   assumptions are valid, or whether edge cases are covered. Test review is a distinct
   skill from test writing.

3. **Feedback calibration.** Review involves social and communicative skills beyond code
   analysis: distinguishing blocking from non-blocking feedback, suggesting rather than
   demanding, focusing on "why" not just "what." The Microsoft ISE playbook devotes
   significant space to this.

### Tooling opportunities

- Generate PR context summaries from commit history and linked issues
- Identify untested code paths in the diff
- Suggest review focus areas based on change risk (similar to Meta's Diff Risk Score)
- Produce structured review reports with categorized findings (blocking/non-blocking/nit)

---

## Cross-Workflow Gap Analysis

### Major missing capabilities

| Gap | Relevant Workflows | Description |
|-----|--------------------|-------------|
| **Debugging** | 5 (Debugging) | Entirely absent. Hypothesis-driven fault isolation is a distinct cognitive pattern. |
| **Verification/Testing** | 2 (Risky Change), 4 (Feature Design), 7 (Review) | No mode for writing, evaluating, or reasoning about tests. |
| **Execution planning** | 2 (Risky Change), 4 (Feature Design), 6 (Migration) | Breaking a design into ordered, verifiable implementation steps. |
| **Campaign management** | 3 (Tech Debt), 6 (Migration) | Multi-sprint efforts need progress tracking and incremental reporting. |
| **Requirements/domain framing** | 1 (Onboarding), 4 (Feature Design) | Bridging from user needs to technical constraints. |
| **Post-action verification** | 2 (Risky Change), 5 (Debugging), 6 (Migration) | Confirming changes work after deployment. No mode covers observation and monitoring. |

### Modes that appear across multiple workflows

| Current Mode | Workflows Using It |
|--------------|--------------------|
| assess:blast-radius | 2 (Risky Change), 6 (Migration), 7 (Review) |
| assess:dependency | 1 (Onboarding), 2 (Risky Change), 6 (Migration) |
| assess:flow | 1 (Onboarding), 5 (Debugging) |
| assess:trade-space | 3 (Tech Debt), 4 (Feature Design) |
| design:type-generative | 4 (Feature Design), 6 (Migration) |
| implement:selective-stage | 2 (Risky Change), 4 (Feature Design) |
| refactor:vestigial | 3 (Tech Debt), 6 (Migration) |

### What this suggests about plugin organization

The current four-skill structure (assess, design, implement, refactor) maps to a
**phase-of-work** taxonomy: understand, plan, execute, improve. This is clean but does not
match how engineers actually work. Engineers organize their thinking around **goals**, not
phases:

- "I need to find and fix this bug" (debugging)
- "I need to make this change safely" (safe change)
- "I need to understand this code" (onboarding)
- "I need to clean this up" (tech debt)
- "I need to build this feature" (feature design)
- "I need to review this PR" (code review)
- "I need to migrate to the new version" (migration)

Each goal pulls modes from multiple current skills. A debugging workflow uses assess:flow,
assess:assumptions, implement:error-clarification, and modes that do not yet exist
(symptom characterization, reproduction strategy, bisection logic). The phase-based
taxonomy forces engineers to know which skill contains the mode they need, rather than
starting from their goal and being routed to the right modes.

This is not an argument for reorganizing into seven goal-based skills. The modes themselves
are well-designed. The argument is that **workflow-level orchestration**---composing modes
across skills in response to a stated goal---is the primary gap, and that several critical
modes are entirely missing regardless of organizational structure.
