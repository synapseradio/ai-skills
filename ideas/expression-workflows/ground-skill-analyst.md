# Expression Architecture Analysis — Skill Analyst

## Current Technique Inventory (17 techniques)

| Category | Technique | Problem it Solves | Entry Condition | User Goal That Triggers It |
|----------|-----------|-------------------|-----------------|---------------------------|
| Clarity | clarify | Prose has structural disorder — concepts appear before foundations, information doesn't flow linearly | Reader must backtrack to follow the argument | "This is hard to follow", "reorganize this" |
| Clarity | activate | Passive voice hides actors and responsibility | Actions lack visible agents; bureaucratic distance | "Fix passive voice", "make this more direct" |
| Clarity | strengthen | Hedges, weak verbs, nominalizations, and filler dilute assertion | Language cushions instead of commits | "Remove weasel words", "make this stronger" |
| Clarity | illustrate | Abstractions float without grounding — claims are accepted definitionally but unrecognizable in practice | Concepts lack concrete examples | "Give me an example", "make this concrete" |
| Integrity | signal-confidence | Certainty language doesn't match evidence foundations | Absolute language on inferred content; false certainty or excessive hedging | "Am I overstating this?", "calibrate my claims" |
| Integrity | bound-scope | Claims sound universal when they should be qualified; boundary conditions go unstated | Advice applies in some contexts but breaks in others | "Where does this break down?", "add caveats" |
| Integrity | surface-assumptions | Silent premises operate beneath visible argument; reasoning depends on unstated conditions | Conclusions require assumptions the reader can't evaluate | "What am I assuming?", "check my reasoning" |
| Narrative | arc | Prose is a flat sequence of information — no tension, no shape, no pull | Reader has no reason to continue; information dumps without engagement | "Make this more compelling", "give this shape" |
| Narrative | rhythm | Sentences cluster at similar lengths and structures; prose flattens into monotony | Reading feels mechanical; no cadence variation | "This feels monotonous", "vary the pacing" |
| Narrative | voice | Authorial sensibility shifts without purpose — casual to formal, certain to hesitant | Prose sounds assembled by committee, not written by one mind | "This doesn't sound like me", "unify the voice" |
| Narrative | diction | Words don't carry their weight; AI-generation patterns and register mismatches appear | Vocabulary is generic, inflated, or mismatched to audience | "Remove AI-sounding language", "sharpen the word choices" |
| Narrative | tone | Emotional register clashes with communicative purpose | Too casual, too severe, too distant for the goal | "Adjust the tone", "this feels too formal/casual" |
| Generative | extract-implications | Consequences, requirements, and contradictions lurk unsaid in the logical wake of claims | Prose makes claims without tracing what follows from them | "What are the implications?", "what follows from this?" |
| Generative | dimensionalize | Feedback conflates distinct concerns into monolithic verdicts | Independent aspects hide behind "needs work" or single labels | "Break this down", "separate the concerns" |
| Generative | pose-questions | Prose closes inquiry rather than opening it; declarations where invitations could explore | Writing feels conclusory; no room for reader engagement | "Open this up", "make this more exploratory" |
| Connection | calibrate | Depth mismatches audience preparation — too dense or too thin | Technical vocabulary assumes expertise; simplifications condescend | "Adjust for my audience", "is this too technical?" |
| Connection | bridge | Unfamiliar concepts appear without anchoring to what readers already know | No structural analogies or familiar reference points for new ideas | "Explain this simply", "use an analogy" |

## Workflow vs Technique Library Classification

### Clarity (4 techniques: clarify, activate, strengthen, illustrate)

- **Workflow potential**: Strong. There is a natural funnel: structural fixes first (clarify), then voice activation (activate), then language commitment (strengthen), then grounding (illustrate). The `/proofread` command already codifies this exact sequence. Later fixes depend on earlier ones — word-level fixes on misordered prose waste effort.
- **Technique library potential**: Moderate. Individual techniques can be used in isolation ("just fix passive voice"), but the cascading dependency means ad-hoc use is suboptimal.
- **User goal**: "Clean this up", "proofread this", "make this clearer", "fix my draft."
- **Verdict**: **Workflow.** The dependency chain (structure → voice → language → grounding) is real and productive. This is already a workflow in `/proofread`.

### Integrity (3 techniques: signal-confidence, bound-scope, surface-assumptions)

- **Workflow potential**: Moderate. There is a loose sequence — surface assumptions first (foundational), then bound scope (limits), then signal confidence (calibrate language). But these are often applied to specific claims rather than as a whole-document pass.
- **Technique library potential**: Strong. Users often reach for one of these in isolation: "Am I overstating this?" doesn't require assumption-surfacing first.
- **User goal**: "Check my reasoning", "am I being honest about what I know?", "where does this break down?"
- **Verdict**: **Technique library within a workflow.** These are best housed as a phase within `/refine` (Pass 2) and also reachable ad-hoc. They don't warrant a standalone workflow skill.

### Narrative (5 techniques: arc, rhythm, voice, diction, tone)

- **Workflow potential**: Weak for sequencing. Arc, rhythm, voice, diction, and tone are largely independent — improving diction doesn't depend on having arc first (though arc provides the framework within which rhythm operates). The `/refine` command sequences them but acknowledges they operate somewhat independently.
- **Technique library potential**: Strong. "Make this more compelling" → arc. "Fix the tone" → tone. Users reach for individual narrative techniques by name or symptom.
- **User goal**: "Make this sound better", "give this more personality", "this is boring."
- **Verdict**: **Technique library.** Narrative techniques are better as a browsable menu. They appear as Pass 3 in `/refine` but standalone use is common and natural.

### Generative (3 techniques: extract-implications, dimensionalize, pose-questions)

- **Workflow potential**: Weak. These three are nearly independent. Extracting implications doesn't depend on dimensionalizing, and posing questions doesn't require either.
- **Technique library potential**: Moderate. They share a family resemblance (opening meaning) but users rarely want all three at once.
- **User goal**: "What am I missing?", "open this up", "what follows from this?"
- **Verdict**: **Technique library** — or absorbed into workflows that need them. These are "thinking with writing" techniques that crosscut other skills. They may belong in a `/writing` skill as exploratory tools, or remain reachable from the expression technique library.

### Connection (2 techniques: calibrate, bridge)

- **Workflow potential**: Moderate. There's a natural pair: calibrate (assess gap) → bridge (close gap). But two techniques don't justify a standalone workflow.
- **Technique library potential**: Strong as part of a broader library. Users say "adjust for my audience" or "explain this simply" — single-technique invocations.
- **User goal**: "Make this accessible", "adjust for a technical/non-technical audience."
- **Verdict**: **Technique library.** These are audience-adaptation tools. They appear as Pass 5 in `/refine` and are reachable ad-hoc. Could be part of a `/writing` skill's audience-adaptation phase.

## Software Plugin Pattern Analysis

### Category Mapping

**Software plugin categories (old):**

- assess (12 modes) — understanding and evaluation
- design (6 modes) — solution architecture
- implement (4 modes) — execution mechanics
- refactor (6 modes) — code improvement

**Expression plugin categories (current):**

- Clarity (4 techniques) — structural and linguistic repair
- Integrity (3 techniques) — epistemic honesty
- Narrative (5 techniques) — craft and shape
- Generative (3 techniques) — meaning expansion
- Connection (2 techniques) — audience adaptation

**Structural parallel:** Both plugins organize by cognitive phase rather than user goal. Software's "assess" and expression's "Clarity" are similar — they describe *what kind of thinking* rather than *what the user wants to accomplish*. The software restructuring moved from "assess → design → implement → refactor" to "solve, understand, debug, migrate, change-safely, clean-up, git." The expression restructuring should similarly move from "Clarity → Integrity → Narrative → Generative → Connection" to goal-oriented skills.

### Analogous Workflows

| Software Workflow | Expression Parallel | Reasoning |
|-------------------|---------------------|-----------|
| **solve** ("how should I solve this?") | **writing** ("help me write this") | Both guide from problem framing through exploration to committed output |
| **debug** ("find the root cause") | **proofread** ("find and fix the issues") | Both follow a diagnostic-then-repair funnel |
| **clean-up** ("reduce debt/cruft") | **refine** ("make this as good as it can be") | Both apply systematic, multi-pass improvement to existing work |
| **understand** ("I need to learn this codebase") | **(no direct parallel)** | Expression lacks a "read and understand text" workflow — it's always about improving output, not comprehending input |
| **change-safely** ("risky change") | **(weak parallel)** | Expression doesn't have a "risky revision" concept, though large-document refine has similar concerns (don't lose what works) |
| **git** (technique library) | **expression** (technique library) | Both are non-sequential technique collections. Git techniques for version control mechanics; expression techniques for prose mechanics |

### Seven Design Principles Applied to Expression

1. **Phases are funnels** — `/proofread` already funnels: structural (cheap, broad) → voice (medium) → language (precise). `/refine` funnels across all 5 categories. This principle maps directly.

2. **Scripts handle volume; skills handle judgment** — Expression is judgment-heavy with no mechanical scripting opportunities. No equivalent of vestigial-detect's code scanning. All 17 techniques require LLM reasoning. This principle applies weakly — expression skills are pure methodology.

3. **Checkpoints externalize state** — Multi-pass `/refine` could benefit from checkpointing between cascade rounds. Currently it runs to convergence without saving intermediate state. Applicable but not critical.

4. **Skills are techniques, not destinations** — This is the key insight. Expression techniques should be directly referenceable by workflow phases, not routed through the monolithic expression skill. A `/writing` workflow's "clarity pass" phase should load `technique-clarify.md` directly, bypassing the expression skill's routing table.

5. **Domain adaptation through heuristic tables** — Expression techniques are already domain-agnostic. No heuristic tables needed. This principle is naturally satisfied.

6. **Entry specifies goal, not method** — Currently violated. Users must know they want "expression" to trigger the skill, then navigate the technique menu. Proposed: users say "proofread this" or "help me write this" and the right workflow activates.

7. **Completion is structural** — `/refine` already has structural completion: "stabilize when changes are primarily cosmetic." `/proofread` completes when all audits are done. This maps directly.

## Proposed Skill Candidates

### 1. `/composition`

- **Problem it solves**: User needs to compose new prose from scratch or from rough notes — the blank page problem where structure, voice, and audience decisions are unmade.
- **User trigger**: "Help me write this", "draft this for me", "help me compose this", "I need to express this idea"
- **Source**: New. Currently no skill addresses composition. Existing techniques address *improving* prose, not *generating* it. Would draw from all 5 categories as generative guidance.
- **Workflow or library?**: Workflow. Phases: Frame purpose & audience → Structure (arc + clarify) → Draft → Self-audit (clarity, integrity) → Polish (narrative, connection).

### 2. `help-me-say`

- **Problem it solves**: User has a specific idea they're struggling to articulate — not a full document, but a thought that won't come out right.
- **User trigger**: "Help me say this", "I can't find the right words", "how do I express this?", "what I mean is..."
- **Source**: New. Fills the gap between ad-hoc technique use and full-document workflows. Most related to illustrate, bridge, diction, and voice techniques.
- **Workflow or library?**: Workflow (lightweight). Phases: Understand intent → Explore framings → Select and refine → Validate with user.

### 3. `/clarify`

- **Problem it solves**: Existing prose has clarity issues — structural disorder, hidden actors, weak language — that need systematic diagnosis and repair.
- **User trigger**: "Clarify this", "check my writing", "clean this up", "fix my draft", "edit this"
- **Source**: Existing command (`commands/clarify.md`). Already follows workflow pattern with phased audits.
- **Workflow or library?**: Workflow. Phases already defined: Load context → Identify target → Structural audit → Content audit → Expression audit → Voice activation → Language commitment → Present result.

### 4. `/redraft`

- **Problem it solves**: Prose needs comprehensive, multi-pass improvement across all dimensions — not just clarity, but integrity, narrative craft, generative opening, and audience connection.
- **User trigger**: "Make this as good as it can be", "full redrafting", "polish thoroughly", "this needs to persuade"
- **Source**: Existing command (`commands/redraft.md`). Already a five-pass cascade with convergence checking.
- **Workflow or library?**: Workflow. The five-pass cascade with convergence checking is inherently sequential and phased.

### 5. `/expression`

- **Problem it solves**: User knows which specific technique they need and wants direct access without workflow overhead — ad-hoc technique application.
- **User trigger**: "Improve my writing", "apply the arc technique", "fix passive voice", "use expression techniques on this"
- **Source**: Current monolithic skill, restructured as technique library. Retains the diagnostic-question routing table.
- **Workflow or library?**: Library. The diagnostic-question → technique pattern is inherently non-sequential. Users browse and pick.

### 6. `/feedback`

- **Problem it solves**: User wants structured, actionable feedback on their prose without automatic fixes — diagnosis without repair.
- **User trigger**: "Give me feedback on this", "what's wrong with this?", "review my writing", "critique this"
- **Source**: New. Currently `/clarify` and `/redraft` both diagnose AND fix. No skill separates diagnosis from repair. Would use all diagnostic questions but present findings rather than applying fixes.
- **Workflow or library?**: Workflow. Phases: Read and orient → Apply diagnostic questions across all categories → Dimensionalize findings → Prioritize → Present structured feedback.

### 7. `/tone-match`

- **Problem it solves**: User needs prose rewritten to match a specific voice, register, or style — not general improvement, but targeted transformation.
- **User trigger**: "Match this tone", "rewrite in a more formal voice", "make this sound like [X]", "adjust the register"
- **Source**: Draws from tone, voice, diction, and calibrate techniques. Currently these are scattered across Narrative and Connection categories with no unified entry point for style transformation.
- **Workflow or library?**: Workflow (lightweight). Phases: Analyze target style → Identify current style gaps → Transform → Verify consistency.

## Technique Redistribution Table

| Technique | Proposed Skill | Phase or Role in That Skill |
|-----------|---------------|----------------------------|
| clarify | `/clarify` (primary), `/redraft` Pass 1, `/composition` Draft-audit phase | Structural/content/expression audit — the foundation of clarity repair |
| activate | `/clarify` (primary), `/redraft` Pass 1, `/composition` Draft-audit phase | Voice activation audit — surfacing hidden actors |
| strengthen | `/clarify` (primary), `/redraft` Pass 1, `/composition` Polish phase | Language commitment audit — eliminating hedges and filler |
| illustrate | `/composition` Draft phase, `/expression` library, `/redraft` Pass 1 | Grounding abstractions with concrete examples |
| signal-confidence | `/redraft` Pass 2, `/feedback` Integrity assessment, `/expression` library | Calibrating certainty language to evidence |
| bound-scope | `/redraft` Pass 2, `/feedback` Integrity assessment, `/expression` library | Defining where claims apply and break down |
| surface-assumptions | `/redraft` Pass 2, `/feedback` Integrity assessment, `/expression` library | Making silent premises explicit |
| arc | `/composition` Structure phase, `/redraft` Pass 3, `/expression` library | Building tension-resolution shape |
| rhythm | `/redraft` Pass 3, `/composition` Polish phase, `/expression` library | Varying sentence cadence |
| voice | `/redraft` Pass 3, `/tone-match` Transform phase, `/expression` library | Establishing consistent authorial presence |
| diction | `/redraft` Pass 3, `/tone-match` Transform phase, `/clarify` (light touch), `/expression` library | Word-level precision and register |
| tone | `/redraft` Pass 3, `/tone-match` Analyze/Transform phases, `/expression` library | Matching emotional register to purpose |
| extract-implications | `/redraft` Pass 4, `/composition` Draft phase, `/feedback` Generative assessment, `/expression` library | Surfacing unsaid consequences |
| dimensionalize | `/feedback` (primary), `/redraft` Pass 4, `/expression` library | Separating monolithic feedback into dimensions |
| pose-questions | `/redraft` Pass 4, `/composition` Draft phase, `/expression` library | Opening prose to exploration |
| calibrate | `/redraft` Pass 5, `/composition` Frame phase, `/tone-match` Analyze phase, `/expression` library | Adjusting for audience knowledge level |
| bridge | `/redraft` Pass 5, `/composition` Draft phase, `/expression` library | Connecting unfamiliar to familiar via analogy |

**Key pattern**: Techniques are not moved — they are *referenced* from multiple skills. The technique files remain in one location (currently `skills/expression/references/`; proposed: `plugins/expression/references/` at plugin level). Workflow skills reference them as phase content. The `/expression` library skill provides direct access to all 17.

## Commands-to-Skills Assessment

### `/proofread`

**Current structure**: A command that loads the expression skill and three clarity techniques (clarify, activate, strengthen), then executes a 4-step protocol: Load context → Identify target → Execute clarity techniques (structural audit → content audit → expression audit → voice activation → language commitment) → Present result.

**Already follows workflow pattern?** Yes — strongly. The fix sequence (structural → voice → language) is a funnel: early passes are broad and cheap, later passes are precise and expensive. Structural fixes cascade downstream, reducing work in later phases. This is the closest existing analog to the software plugin's workflow pattern.

**As a workflow skill — proposed phases:**

1. **Orient** — Identify target prose, state scope, read the material
2. **Diagnose** — Run diagnostic questions for clarity category (structural, content, expression, voice, language commitment)
3. **Repair** — Apply fixes in cascading priority: structural → voice → language → grounding
4. **Verify** — Re-read for remaining issues; check that fixes didn't introduce new problems
5. **Present** — Output improved prose with change summary

**What moves to SKILL.md vs references/**:

- **SKILL.md**: Phase descriptions, fix-sequence rationale, diagnostic question summary, NEVER guards, entry/exit conditions
- **references/**: technique-clarify.md, technique-activate.md, technique-strengthen.md (already exist), clarify-patterns.md, clarify-examples.md (already exist). These are loaded during the Diagnose/Repair phases.

**What changes from current command**: Minimal structural change. The command is already well-designed as a workflow. Main changes: (1) Move from `commands/` to `skills/proofread/SKILL.md`, (2) Add a Verify phase (currently missing — proofread goes straight from repair to presentation), (3) Explicit phase naming for resumability.

### `/refine`

**Current structure**: A command that loads the expression skill, then executes a five-pass cascade: Clarity → Integrity → Narrative → Generative → Connection, with convergence checking after each full cycle. Each pass loads all techniques for its category.

**Already follows workflow pattern?** Partially. It has clear phases (5 passes) and structural completion (convergence check). But it's more of a "meta-workflow" — each pass is itself a mini-workflow applying 2–5 techniques. The convergence loop adds a dimension that simple phased workflows don't have.

**As a workflow skill — proposed phases:**

1. **Orient** — Identify target, state scope, announce what's being refined
2. **Pass 1: Clarity** — Load and apply clarify, activate, strengthen, illustrate
3. **Pass 2: Integrity** — Load and apply signal-confidence, bound-scope, surface-assumptions
4. **Pass 3: Narrative** — Load and apply arc, rhythm, voice, diction, tone
5. **Pass 4: Generative** — Load and apply extract-implications, dimensionalize, pose-questions
6. **Pass 5: Connection** — Load and apply calibrate, bridge
7. **Converge** — Assess stability; repeat from Pass 1 if substantial changes remain
8. **Present** — Output refined prose with cross-pass change summary

**What moves to SKILL.md vs references/**:

- **SKILL.md**: Pass sequence, convergence criteria, compounding-effects rationale, NEVER guards, usage modes (full/targeted/iterative), triage table
- **references/**: All 17 technique files (already exist). The "Why This Order" and "Compounding Effects" sections could remain in SKILL.md (they justify the methodology) or move to a `references/cascade-rationale.md`.

**What changes from current command**: (1) Move from `commands/` to `skills/refine/SKILL.md`, (2) Add Orient phase (currently jumps to "Identify Target"), (3) Formalize convergence as a named phase rather than inline logic, (4) Consider checkpointing between cascade rounds for resumability.

## Open Questions

1. **Where do the 17 technique files live?** Currently in `skills/expression/references/`. If `/expression` becomes a library skill and `/proofread`, `/refine`, `/writing` become separate workflow skills, all skills need access to the same technique files. Options: (a) Keep in `/expression` skill's references/ and have other skills reference across skill boundaries, (b) Promote to plugin-level `plugins/expression/references/` and reference from all skills — following the software plugin pattern where shared modes live at plugin root. Option (b) matches the software proposal's resolution of the "where do shared mode references live?" question.

2. **Does `/writing` (composition) belong in the expression plugin?** The expression plugin's identity is "improving existing prose." Composition is a different activity — generating prose from intent. It might deserve its own plugin, or it might be the natural expansion of expression's scope. The software plugin precedent suggests keeping it together (solve = design new solutions, living alongside debug = fix existing code).

3. **How should `help-me-say` relate to `/writing`?** `help-me-say` is a lightweight, conversational workflow for articulating a single thought. `/writing` is a heavier workflow for composing full documents. Are these separate skills, or is `help-me-say` a mode within `/writing`? The software plugin kept `debug` and `understand` separate despite both being "comprehension" activities — suggesting separate skills for distinct user goals.

4. **Should `/feedback` exist as a separate skill, or is it a mode of `/proofread`?** The distinction is diagnosis-without-repair vs diagnosis-with-repair. The software plugin's `understand` (comprehension only) and `debug` (comprehension + fix) are analogous separate skills. But expression's diagnosis and repair are more tightly coupled than comprehension and debugging.

5. **What happens to the `commands/` directory?** The software proposal deletes `commands/` entirely, citing Anthropic's designation of commands as legacy. Should expression follow suit immediately, or maintain backward compatibility during transition? The answer likely depends on whether the broader plugin ecosystem has migrated away from commands.
