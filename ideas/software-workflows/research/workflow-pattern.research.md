# Workflow Pattern Research

Analysis of `vestigial-detect` as an exemplar of workflow-oriented skill design, contrasted with the mode-menu approach used by `assess`, `design`, `implement`, and `refactor`.

## Source Material

- `/plugins/software/commands/vestigial-detect/vestigial-detect.md` (the command)
- `/plugins/software/commands/vestigial-detect/scripts/` (6 TypeScript scripts)
- `/plugins/software/commands/assess/assess.md` and `/plugins/software/skills/assess/SKILL.md` (mode-menu contrast)

---

## 1. Phase Structure

`vestigial-detect` defines five sequential phases: **Scope, Detect, Investigate, Verify, Remove.** Each phase has a distinct cognitive purpose and produces a specific artifact that the next phase consumes.

### What makes each phase distinct

| Phase | Purpose | Input | Output | Character |
|-------|---------|-------|--------|-----------|
| **Scope** | Define detection boundary | User's target + arguments | Criteria document (what counts as vestigial, time thresholds, domain type) | Definitional. Establishes shared vocabulary before any work begins. |
| **Detect** | Generate candidate list | Criteria from Phase 1 | Candidate list with confidence ratings (high/medium/low) | Expansive. Cast a wide net. Automated tools + reasoning skills both contribute. |
| **Investigate** | Research historical context | High-confidence candidates from Phase 2 | Risk classification per candidate (safe / investigate / keep) | Archaeological. Judgment-heavy. Why does this exist? What did it once do? |
| **Verify** | Triangulate removal safety | "Safe" and "Investigate" candidates from Phase 3 | Verification status per candidate (verified safe / needs investigation / unsafe) | Adversarial. Try to prove removal is dangerous. |
| **Remove** | Execute strategic cleanup | Verified-safe candidates from Phase 4 | Removal plan with tiers, sequencing, rollback | Operational. Careful execution with safety margins. |

### How outputs flow between phases

The funnel narrows at each phase boundary:

```
Scope       → all elements in scope
Detect      → candidates (subset flagged by pattern matching)
Investigate → classified candidates (safe / investigate / keep)
Verify      → verified-safe candidates (survived adversarial testing)
Remove      → tiered removal plan (sequenced by risk)
```

Each phase acts as a filter. The key insight: **early phases are cheap and broad, later phases are expensive and narrow.** You run automated scripts against everything in Phase 2, but you only run git archaeology on high-confidence candidates in Phase 3. You only simulate removal for verified-safe items in Phase 4. This progressive narrowing prevents wasted effort.

### Phase boundaries as decision points

Phases are not merely sequential steps -- they are **commitment boundaries**. At each checkpoint (journal-write invocation), the user has an artifact they can inspect, challenge, or redirect. The workflow does not proceed on autopilot. Phases produce visible, editable state.

---

## 2. Script Integration

Six TypeScript scripts handle the mechanical work:

| Script | Phase | What it does | Why automated |
|--------|-------|-------------|---------------|
| `detect-project-type.ts` | 1 (Scope) | Identifies ecosystem (node/python/php/go/rust) and available tools | Pure detection. No judgment needed. |
| `detect-dead-code.ts` | 2 (Detect) | Runs ecosystem-specific dead code tools (madge, knip, vulture, psalm, phpstan, staticcheck, cargo) | Tool orchestration. Aggregates outputs into uniform `DeadCodeCandidate` format. |
| `detect-stale-files.ts` | 2 (Detect) | Finds files untouched beyond threshold via git history | Mechanical date comparison across potentially thousands of files. |
| `git-archaeology.ts` | 3 (Investigate) | Extracts creation date, last meaningful edit, contributors | Git log parsing with cosmetic-commit filtering. Tedious but deterministic. |
| `count-references.ts` | 4 (Verify) | Counts and classifies references to a symbol | Grep + classification. Volume work unsuited to manual execution. |
| `simulate-removal.ts` | 4 (Verify) | Comments out file, runs tests, auto-restores | Safety-critical automation. Must be reliable and reversible. |

### The mechanical vs. judgment boundary

Scripts handle **volume and precision** -- scanning every file, counting every reference, parsing tool output into structured data. The agent handles **interpretation and decision** -- classifying risk, understanding historical context, reasoning about whether functionality truly migrated.

The pattern: **scripts produce structured data; the agent interprets that data within context.**

Scripts never make removal decisions. They surface candidates and evidence. The classification happens in the reasoning phases (3 and 4), where skills like `find-root-cause`, `argue-opposite`, and `premortem` provide the judgment framework.

### Script design characteristics

1. **JSON output.** Every script outputs structured JSON. This lets the agent parse and reason about results programmatically rather than scraping human-readable output.

2. **Graceful degradation.** `detect-dead-code.ts` checks for ecosystem-specific tools but always falls back to grep + git. `detect-project-type.ts` returns `unknown` with universal tools when it cannot identify the ecosystem.

3. **Idempotent and safe.** `simulate-removal.ts` creates backups, auto-restores after test runs, and supports explicit `--restore` mode. No script modifies state irreversibly.

4. **Uniform interfaces.** All take a path argument (defaulting to cwd) and produce JSON to stdout. Consistent invocation pattern across the workflow.

---

## 3. Checkpoint Pattern

The workflow records state via `Skill("journal-write")` at four points:

| After Phase | What's recorded |
|-------------|-----------------|
| 1 (Scope) | Scope definition and detection criteria |
| 2 (Detect) | Candidate list with patterns and confidence |
| 3 (Investigate) | Investigation findings and risk classifications |
| 4 (Verify) | Verification outcomes |

Phase 5 uses `Skill("journal-session-reflect")` for the final record.

### Why checkpoints matter

1. **Resumability.** If a session breaks mid-workflow, the journal entries let a new session pick up from the last checkpoint rather than restarting.

2. **Auditability.** The journal creates a decision trail. Why was this element removed? Because it was flagged in Phase 2, investigated in Phase 3, and verified safe in Phase 4 -- all recorded.

3. **Course correction.** After a checkpoint, the user can review the recorded state and redirect. "Your candidate list missed X" or "That risk classification is wrong for Y."

4. **Progressive commitment.** Each checkpoint is a soft gate. The user implicitly approves the phase's output by allowing the workflow to proceed.

### Checkpoint as protocol, not implementation

The checkpoint pattern is not tied to journal-write specifically. The reusable principle: **after each phase, externalize state in a form that is inspectable, editable, and resumable.** The mechanism could be a journal entry, a file, a structured comment, or any durable artifact.

---

## 4. Progressive Refinement

The funnel structure implements **progressive refinement through increasing rigor**:

| Phase | Rigor level | Method | Effort per candidate |
|-------|-------------|--------|---------------------|
| Detect | Low | Pattern matching, automated tools | Seconds (automated) |
| Investigate | Medium | Git archaeology, historical research, root cause analysis | Minutes per candidate |
| Verify | High | Dependency analysis, removal simulation, adversarial reasoning | Significant time per candidate |

### Confidence as a routing mechanism

Phase 2 assigns confidence levels (high = 3+ patterns, medium = 2, low = 1). Phase 3 only investigates high-confidence candidates. This is not arbitrary filtering -- it is **calibrated investment.** The confidence score determines how much analytical effort a candidate deserves.

### Risk classification as phase gate

Phase 3 classifies candidates into three buckets: **Safe, Investigate, Keep.** Only Safe and Investigate candidates advance to Phase 4. "Keep" items exit the workflow entirely. This is a genuine gate -- not a ranking, but a binary decision about whether further analysis is warranted.

### Tiered execution

Phase 5 adds another refinement layer through removal tiers:

- **Tier 1** (high confidence, low risk): Remove directly
- **Tier 2** (medium confidence, moderate risk): Deprecate first, observe, then remove
- **Tier 3** (low confidence, high risk): Mark for investigation, do not remove yet

And sequencing rules: leaves before branches, recent before old, local before global, easy before hard. This is not just caution -- it is **information maximization.** Each removal generates evidence (did anything break?) that informs subsequent removals.

---

## 5. Multi-Domain Applicability

The same five-phase structure applies to code, documentation, and organizational processes. The command achieves this through **domain-specific heuristic tables** within a **domain-agnostic phase structure.**

### How domain adaptation works

Each detection pattern (Disconnected, Duplicated, Accumulated, Migrated) has domain-specific instantiations:

| Pattern | Code | Documentation | Process |
|---------|------|---------------|---------|
| Disconnected | Zero callers, unused imports | Zero inbound links, not in nav | References nonexistent teams |
| Duplicated | Parallel implementations | Content at multiple URLs | Multiple runbooks for same task |
| Accumulated | Style mismatch with surroundings | Doesn't follow current IA | Old org structure references |
| Migrated | "deprecated" comments still present | "See new guide" but old still published | Legacy workflow alongside current |

### The abstraction layer

The domain-agnostic concepts are:

- **Disconnection** (not integrated with current structure)
- **Duplication** (functionality exists elsewhere)
- **Accumulation** (grew without design)
- **Migration** (purpose moved but artifact remained)

These four patterns are the analytical framework. Domain-specific heuristics are concrete instantiations. Scripts only exist for the code domain (where automation is possible), but the reasoning framework applies everywhere.

### Reference tables as domain adapters

The Detection Heuristics Reference section at the bottom of the command serves as a quick-lookup for the agent. Four signal types times three domains equals twelve heuristic groups. This is a **lookup table, not a decision tree** -- the agent selects which rows apply based on Phase 1's domain determination.

---

## 6. Entry and Exit

### Entry conditions

The command specifies both when to use and when to defer:

**Use when:**

- Technical debt accumulated
- Documentation contains orphaned content
- Processes reference obsolete structures
- Complexity grew without proportional functionality
- Before major migrations
- Periodic maintenance

**Defer when:**

- System actively evolving (wait for stabilization)
- Ownership unclear (establish accountability first)
- Verification capacity limited (hasty cleanup creates problems)
- Seeking performance gains (this finds structural cruft, not algorithmic bottlenecks)

The "defer when" list is as important as the "use when" list. It prevents misapplication.

### How the user enters

The user provides: `<scope> [--threshold=<time>] [--domain=<type>]`

Phase 1 immediately engages with this input, using `decompose` and `map-landscape` skills to understand what the scope encompasses. The user does not need to pre-analyze anything -- the workflow does the orientation work.

### When it's done

The workflow is complete when Phase 5 produces:

1. A removal plan with tiers and sequencing
2. Success metrics defined
3. Outcomes recorded in journal

There is no explicit "done" signal. Completion is structural: when all five phases have executed and the final journal entry is written.

### The workflow can stop early

If Phase 2 finds no candidates, the workflow stops. If Phase 3 classifies everything as "Keep," Phase 4 has nothing to verify. The phases are sequential but not obligatory beyond their gating conditions.

---

## 7. Skill Invocations Within Phases

Skills are embedded as **techniques within phases**, not as independent operations. The command prescribes specific skills at specific points:

| Phase | Skill | Purpose within phase |
|-------|-------|---------------------|
| 1 | `decompose` | Break project into analyzable components |
| 1 | `map-landscape` | Survey territory and note known cruft areas |
| 1 | `journal-write` | Record scope (checkpoint) |
| 2 | `understand` (dependency mode) | Trace what connects to what |
| 2 | `find-themes` | Identify disconnection signals across candidates |
| 2 | `follow-connections` | Follow relationships, find isolated clusters |
| 2 | `journal-write` | Record candidates (checkpoint) |
| 3 | `find-root-cause` | Understand why element became vestigial |
| 3 | `understand` (archaeology mode) | Reconstruct original purpose |
| 3 | `clarify` (archaeology mode) | Document discovered intent |
| 3 | `journal-write` | Record investigation (checkpoint) |
| 4 | `assess` (blast-radius mode) | Assess what would break if removed |
| 4 | `argue-opposite` | Adversarial: what could go wrong? |
| 4 | `premortem` | Imagine catastrophic failure scenario |
| 4 | `journal-write` | Record verification (checkpoint) |
| 5 | `journal-session-reflect` | Document outcomes and lessons |

### How skill loading works in practice

The command uses two patterns for invoking skills:

1. **Direct invocation:** `Invoke Skill("decompose")` -- loads and executes the skill as a standalone operation.

2. **Mode-specific loading:** Load the SKILL.md to get the mode structure, then `Read()` the specific mode reference file. Example from Phase 4:
   > Load `${CLAUDE_PLUGIN_ROOT}/skills/assess/SKILL.md` then invoke blast-radius mode: `Read("${CLAUDE_PLUGIN_ROOT}/skills/assess/references/mode-blast-radius.md")`

This second pattern is significant: it treats mode-based skills as libraries of techniques. The workflow cherry-picks specific modes rather than entering the skill's decision tree. The workflow bypasses the skill's own routing logic and goes directly to the methodology it needs.

### Skills as verbs, not nouns

In the mode-menu approach (assess, design, implement), the skill is the unit of work. The user enters the skill, and the skill decides what to do.

In the workflow approach, skills are **verbs within sentences.** The workflow is the sentence. `find-root-cause` is not a destination -- it is something you do in Phase 3, Step 3.2, as part of understanding why an element became vestigial.

---

## Comparative Analysis: Workflow vs. Mode-Menu

### The mode-menu approach (assess)

`assess` presents 12 cognitive modes organized in a decision tree. The command (`assess.md`) parses user signals to route to the right mode. The skill (`SKILL.md`) documents all modes, their triggers, combinations, and transitions.

**Strengths:**

- Flexible. Handles diverse planning needs.
- Composable. Modes can be sequenced via Combination Patterns.
- Discoverable. Signal Detection table helps the agent match user intent.

**Weaknesses:**

- Requires the user (or agent) to know what mode they need.
- No inherent sequencing. The user must decide what comes after what.
- No state management. Each mode invocation is independent.
- No progressive refinement. Each mode runs at full depth regardless of whether earlier analysis warranted it.

### The workflow approach (vestigial-detect)

`vestigial-detect` prescribes a fixed five-phase sequence. The user provides a scope, and the workflow drives from there.

**Strengths:**

- Self-directing. The user does not need to know the methodology.
- Progressive. Effort increases only for candidates that survive earlier filters.
- Stateful. Checkpoints record progress and enable resumption.
- Integrated. Scripts and skills are combined within phases, not invoked independently.
- Complete. Entry to exit is defined. You know when you're done.

**Weaknesses:**

- Rigid. The five phases are the five phases. You cannot skip Scope or reorder Verify before Investigate.
- Specialized. Designed for one task (vestigial detection). Cannot be repurposed.

### The fundamental difference in user experience

**Mode-menu:** "Here are 12 tools. Which one do you need?" The user is a craftsperson selecting tools.

**Workflow:** "You want to find and remove vestigial elements. Here is how we do that." The user is a participant in a process.

The mode-menu approach assumes the user knows their cognitive need. The workflow approach assumes the user knows their practical goal. These are different assumptions about where the user's knowledge lies.

For recurring, well-defined tasks (cleanup, migration, audit), the workflow approach is superior because the methodology is proven and repeatable. For novel, exploratory tasks (understanding unfamiliar code, assessing a new dependency), the mode-menu approach is superior because the path cannot be predetermined.

---

## Extracted Template: Workflow Skill Pattern

### Structure

```
# /{command-name}

{One-sentence purpose statement}

## What This Command Does
{Paragraph explaining the workflow and what it produces}

## When to Use This Command
Use when: {conditions where this workflow applies}
Defer when: {conditions where this workflow should not be applied}

## How It Works
{Numbered list of phases with one-line descriptions}

## Execution Protocol

### Core Concept Definition
{Define the central abstraction. What does "vestigial" mean? What does
"migration-ready" mean? What does "debt" mean in this context?
This grounds the entire workflow in shared vocabulary.}

### Prerequisites
{Runtime requirements, tooling, access needs}

### Phase 1: {Verb} ({Purpose Noun})
{Establish scope and criteria. Always first. Cheap.}

Step 1.1 - {action}:
Invoke Skill("...") to {purpose}.

Step 1.2 - {action}:
{Domain-specific instructions or script invocations}

Checkpoint: Invoke Skill("journal-write") to record {what}.

### Phase 2: {Verb} ({Purpose Noun})
{Generate candidates or artifacts. Broad net. Mix of automated + reasoning.}

Step 2.1 - {domain-specific heuristics}:
For {domain A}: {specifics}
For {domain B}: {specifics}
Run automated detection: {script invocations}

Step 2.2 - {pattern recognition}:
Invoke Skill("...") to {purpose}.

Step 2.3 - {output generation}:
{Structured output format with confidence/priority ratings}

Checkpoint: Invoke Skill("journal-write") to record {what}.

### Phase 3: {Verb} ({Purpose Noun})
{Deep analysis on filtered candidates. Judgment-heavy.}
{Only operates on high-confidence items from Phase 2.}

Step 3.1 - {domain-specific investigation}:
For {domain A}: {specific investigation steps + script invocations}
For {domain B}: {specific investigation steps}

Step 3.2 - {reasoning step}:
Invoke Skill("...") to {purpose}.

Step 3.3 - {classification}:
{Classify candidates into action categories: proceed / investigate / stop}

Checkpoint: Invoke Skill("journal-write") to record {what}.

### Phase 4: {Verb} ({Purpose Noun})
{Verification / validation. Adversarial. Tries to disprove Phase 3's conclusions.}

Step 4.1 - {technical verification}:
{Script invocations for automated checks}
Invoke Skill("...") for {specialized analysis}

Step 4.2 - {adversarial reasoning}:
Invoke Skill("argue-opposite") - {specific adversarial question}
Invoke Skill("premortem") - {specific failure scenario}

Step 4.3 - {final classification}:
{Status per candidate with risk, dependencies, rollback plan}

Checkpoint: Invoke Skill("journal-write") to record {what}.

### Phase 5: {Verb} ({Purpose Noun})
{Execution. Only verified-safe items. Tiered by confidence.}

Step 5.1 - {tier definition}:
Tier 1: {high confidence, direct action}
Tier 2: {medium confidence, staged action}
Tier 3: {low confidence, defer}

Step 5.2 - {sequencing}:
{Ordering principles for execution}

Step 5.3 - {execution plan}:
{Per-item plan: tier, method, sequencing, verification, rollback}

Step 5.4 - {outcomes}:
Invoke Skill("journal-session-reflect") to document {what}.

## {Domain} Heuristics Reference
{Lookup tables for domain-specific instantiation of the workflow's
abstract categories. One table per signal type, one column per domain.}

## Philosophy
{One paragraph on the workflow's stance. Not methodology, but values.}
```

### Design Principles

#### 1. Phases are funnels

Each phase narrows the candidate set. Early phases are cheap and broad. Later phases are expensive and narrow. Never apply expensive analysis to the full candidate pool.

```
Phase 1: Everything in scope
Phase 2: Flagged candidates (subset)
Phase 3: Investigated candidates (smaller subset)
Phase 4: Verified candidates (smallest subset)
Phase 5: Execution plan (only verified items)
```

#### 2. Scripts handle volume; skills handle judgment

Automate what is mechanical: scanning files, counting references, parsing tool output, comparing dates. Use reasoning skills for what requires context: understanding why something exists, assessing risk, imagining failure scenarios.

**Script design requirements:**

- JSON output (machine-parseable by the agent)
- Graceful degradation (fall back when ecosystem tools are unavailable)
- Idempotent and safe (no irreversible side effects)
- Uniform interface (path argument, stdout output)

#### 3. Checkpoints externalize state

After each phase, record the phase's output in a durable, inspectable form. This enables:

- Resumability (pick up from last checkpoint)
- Auditability (decision trail)
- Course correction (user can review and redirect)
- Progressive commitment (implicit approval gate)

#### 4. Skills are techniques, not destinations

The workflow invokes skills as steps within phases. It bypasses the skill's internal routing and goes directly to the specific methodology it needs. The workflow is the orchestrator; skills are the instruments.

Two invocation patterns:

- **Direct:** `Invoke Skill("decompose")` -- for skills without modes
- **Mode-specific:** Load SKILL.md, then Read the specific mode reference -- for mode-based skills where you need one particular mode

#### 5. Domain adaptation through heuristic tables

Keep the phase structure domain-agnostic. Express domain specificity through:

- Conditional script invocations ("For code projects, run...")
- Heuristic lookup tables (signal type x domain = specific indicators)
- Domain-specific investigation steps within phases

The workflow's abstract categories (disconnection, duplication, etc.) should apply across all target domains. The heuristics are the adapter layer.

#### 6. Entry specifies goal, not method

The user provides what they want to accomplish (scope, target, constraints), not how to accomplish it. The workflow owns the methodology. Entry conditions and deferral conditions are equally explicit.

#### 7. Completion is structural, not declarative

The workflow is done when its phases are done. No ambiguous "keep iterating until satisfied" loops. Each phase has a defined output. The final phase produces the terminal artifact.

### When to use this pattern vs. mode-menu

**Use workflow pattern when:**

- The task is well-defined and repeatable
- There is a known methodology with proven sequencing
- Progressive refinement adds value (filtering candidates)
- Automated tooling can handle volume work
- State between phases matters
- The user knows their goal but not the methodology

**Use mode-menu pattern when:**

- The task is exploratory or novel
- The path depends on what you find
- Different entry points lead to genuinely different processes
- The user knows their cognitive need but not their specific goal
- Composability matters more than sequencing
