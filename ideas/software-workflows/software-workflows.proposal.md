# Proposal: Restructure Software Plugin Around Workflows

## Summary

Replace the software plugin's current organization — four cognitive-category skills (assess, design, implement, refactor) with mode-menu routing and five legacy commands — with **workflow-oriented skills** that guide engineers through complete tasks, plus **technique libraries** for exploratory work that resists sequencing.

## What Changes

### Eliminate: `commands/` directory

Anthropic's docs explicitly mark `commands/` as legacy, superseded by `skills/`. The five commands are vestigial:

- Four proxy commands (assess, design, implement, refactor) duplicate skills with zero added value
- vestigial-detect should be a skill but currently isn't

**Action:** Delete `commands/` entirely. All entry points become skills with auto-discovery via description matching.

See: [research/commands-vestigial.research.md](research/commands-vestigial.research.md)

### Restructure: Skills into workflows + technique libraries

The current skills organize by cognitive phase (understand → design → execute → improve). Engineers organize by **goal** ("fix this bug", "make this change safely", "clean this up"). Each goal pulls techniques from multiple current skills.

**Action:** Create workflow skills for recurring, well-defined tasks. Retain technique libraries for exploratory, non-sequential work.

See: [research/mode-clustering.research.md](research/mode-clustering.research.md), [research/engineering-workflows.research.md](research/engineering-workflows.research.md)

### Preserve: Existing mode content

The 28 mode reference files contain real, well-designed knowledge. They become **techniques within workflow phases** or entries in **technique libraries**. Nothing is discarded.

---

## Proposed Skill Structure

### Workflow Skills (sequential, phased, funnel-shaped)

These follow the [workflow skill template](research/workflow-pattern.research.md#extracted-template-workflow-skill-pattern) extracted from vestigial-detect: phased funnels with checkpoints, automated tooling where mechanical, progressive refinement, entry by goal.

| # | Skill | Goal | Phases | Existing Modes Absorbed | New Content Needed |
|---|-------|------|--------|------------------------|-------------------|
| 1 | **understand** | "I need to learn this codebase" | Orient → Trace → Anchor → Document → Validate | cartography, dependency, flow, archaeology, type-intention | Anchor (learning-by-doing), Validate (teach-to-verify) |
| 2 | **change-safely** | "I need to make this risky change" | Scope fear → Map impact → Build safety net → Execute incrementally → Verify | blast-radius, interface-stability, assumptions, failure-modes, second-order-effects, selective-stage | Safety net construction (characterization tests), Post-change verification |
| 3 | **clean-up** | "I need to reduce debt / remove cruft" | Inventory → Classify → Prioritize → Execute → Verify → Prevent | vestigial, surface-complexity, structural, annotation, documentation-audit, investment-timing, commit-strategy, selective-stage | Debt inventory, Cost quantification, Prevention mechanisms |
| 4 | **debug** | "I need to find and fix this bug" | Characterize → Reproduce → Map system → Hypothesize → Test → Fix | flow, assumptions, archaeology, failure-modes, blast-radius | Symptom characterization, Reproduction strategy, Bisection logic, Debugging journal |
| 5 | **migrate** | "I need to execute a breaking change" | Audit → Design bridge → Validate coexistence → Migrate consumers → Remove old path | blast-radius, dependency, interface-stability, second-order-effects, migration-path, type-generative, documentation-audit, vestigial, commit-strategy | Coexistence strategy, Migration progress tracking |
| 6 | **vestigial-detect** | "I need to find and remove dead weight" | Scope → Detect → Investigate → Verify → Remove | *(already exists as command — promote to skill)* | None — already complete |
| 7 | **solve** | "I need to design a technical solution" | Frame → Explore → Evaluate → Commit → Specify | constraint-inventory, surface-complexity, trade-space, abstraction-level, good-enough-threshold, type-generative, type-analytical, type-intention | Explore phase (divergent approach generation), Commit phase (decision recording) |

### Technique Library (non-sequential, reach-for-as-needed)

One collection of techniques that resists fixed sequencing — version control mechanics where the user knows what they need and picks the right tool.

| # | Skill | Domain | Techniques Included | When Used |
|---|-------|--------|--------------------|-----------|
| 8 | **git** | Version control mechanics | commit-strategy, selective-stage, rebase-safety, conflict-topology | Structuring commits, managing branches, resolving conflicts. Invoked standalone OR cherry-picked by workflow skills. |

### Standalone Recipes

Content that doesn't fit either pattern — single-purpose protocols rather than reasoning frameworks.

| # | Type | Name | Current Location | Disposition |
|---|------|------|-----------------|-------------|
| 9 | Reference | error-clarification | implement/references/ | Move to `references/error-protocol.md` — a recipe for writing PAGE-format errors, not a cognitive mode |

### Why `solve` instead of a `design` technique library

The original proposal kept design modes as a technique library — a menu of tools for exploratory work. But solution design is not exploratory in the way debugging an unknown system is. It has a natural progression:

1. **Frame** — Define the problem and its constraints (constraint-inventory, surface-complexity)
2. **Explore** — Generate candidate approaches without committing (currently a gap — no mode for divergent thinking)
3. **Evaluate** — Compare approaches against constraints (trade-space, abstraction-level)
4. **Commit** — Select an approach, document the rationale and rejected alternatives (good-enough-threshold + decision record — partially a gap)
5. **Specify** — Express the solution in types, interfaces, and contracts (type-generative, type-analytical, type-intention)

Engineers don't think "I need the type-generative mode." They think "I have a problem and I need to figure out how to solve it." The workflow guides them from problem to specified solution. Individual techniques (like type-generative) still exist as phase content — they just have context now.

The funnel property holds: Frame is cheap (enumerate constraints), Explore is broader (generate options), Evaluate narrows (filter by constraints), Commit gates (one approach survives), Specify is expensive and precise (formal type design for the chosen approach only).

---

## How Modes Map to the New Structure

Every existing mode reference file has a destination:

| Current Mode | Current Skill | New Home | Role |
|-------------|---------------|----------|------|
| cartography | assess | **understand** | Phase 1: Orient |
| dependency | assess | **understand** + **change-safely** + **migrate** | Trace phase in multiple workflows |
| flow | assess | **understand** + **debug** | Trace / Map system phase |
| archaeology | assess | **understand** + **debug** | Document / Map system phase |
| assumptions | assess | **change-safely** + **debug** | Map impact / Test hypothesis phase |
| blast-radius | assess | **change-safely** + **migrate** + **debug** | Scoping step across workflows |
| failure-modes | assess | **change-safely** + **debug** | Risk enumeration step |
| interface-stability | assess | **change-safely** + **migrate** | Impact / Audit phase |
| second-order-effects | assess | **change-safely** + **migrate** | Consequence tracing step |
| constraint-inventory | assess | **solve** | Phase 1: Frame |
| trade-space | assess | **solve** | Phase 3: Evaluate |
| migration-path | assess | **migrate** | Phase 2: Design bridge |
| type-generative | design | **solve** + **migrate** | Phase 5: Specify / Phase step |
| type-analytical | design | **solve** | Phase 5: Specify |
| type-intention | design | **understand** + **solve** | Phase / Phase 5 |
| abstraction-level | design | **solve** | Phase 3: Evaluate |
| surface-complexity | design | **solve** + **clean-up** | Phase 1: Frame / Phase step |
| good-enough-threshold | design | **solve** | Phase 4: Commit |
| commit-strategy | implement | **git** (library) | Technique: structure commits |
| selective-stage | implement | **git** (library) | Technique: precise staging |
| investment-timing | implement | **clean-up** | Phase: Prioritize |
| error-clarification | implement | **references/** | Standalone recipe |
| structural | refactor | **clean-up** | Phase: Execute |
| annotation | refactor | **clean-up** | Phase: Execute |
| documentation-audit | refactor | **clean-up** + **migrate** | Verification step |
| rebase-safety | refactor | **git** (library) | Technique: safe rebasing |
| conflict-topology | refactor | **git** (library) | Technique: conflict resolution |
| vestigial | refactor | **vestigial-detect** (workflow) | Subsumed by the full workflow |

**Key insight:** Modes that appear in multiple workflows (blast-radius in 3, dependency in 3, commit-strategy in 3) are referenced from workflow phases, not duplicated. The mode reference file lives in one location; workflow phases point to it.

---

## Workflow Skill Template

Each workflow skill follows this structure (extracted from vestigial-detect):

```
skills/{name}/
├── SKILL.md              # Phases, entry/exit conditions, philosophy
├── references/
│   ├── phase-1-{verb}.md  # Detailed phase instructions
│   ├── phase-2-{verb}.md
│   ├── ...
│   └── heuristics.md      # Domain-specific lookup tables
└── scripts/               # Automated tooling (if applicable)
    ├── {detection}.ts
    └── {verification}.ts
```

### Seven Design Principles

1. **Phases are funnels** — early cheap and broad, later expensive and narrow
2. **Scripts handle volume; skills handle judgment** — JSON output, graceful degradation, idempotent
3. **Checkpoints externalize state** — resumable, auditable, editable via journal-write
4. **Skills are techniques, not destinations** — workflows cherry-pick modes directly, bypassing skill routing
5. **Domain adaptation through heuristic tables** — domain-agnostic phases, domain-specific lookup tables
6. **Entry specifies goal, not method** — user says what they want; workflow owns methodology
7. **Completion is structural** — done when phases are done

See: [research/workflow-pattern.research.md](research/workflow-pattern.research.md)

---

## What's New (Content That Doesn't Exist Yet)

The research identified six capability gaps. These need new content:

| Gap | Workflow(s) | What's Needed |
|-----|------------|---------------|
| **Debugging** | debug | Symptom characterization protocol, reproduction strategy, bisection/elimination logic, debugging journal template |
| **Testing/verification** | change-safely, clean-up, debug | Characterization test writing, test coverage evaluation, post-change verification checklist |
| **Execution planning** | change-safely, migrate | Breaking a design into ordered, verifiable implementation steps with dependency relationships |
| **Safety net construction** | change-safely | Creating rollback plans, feature flag strategies, characterization tests before risky changes |
| **Campaign management** | clean-up, migrate | Tracking multi-increment progress, managing debt/migration backlogs |
| **Prevention mechanisms** | clean-up | Creating guardrails (lint rules, CI checks) to prevent debt recurrence |

### Tooling Opportunities

Scripts that could be developed for new workflows:

| Workflow | Script | Purpose |
|----------|--------|---------|
| debug | `bisect-helper.ts` | Automate git bisect with structured hypothesis tracking |
| debug | `symptom-intake.ts` | Structured prompts for scope, timeline, environment, reproduction |
| change-safely | `coverage-delta.ts` | Compare test coverage before/after a change |
| change-safely | `characterize-behavior.ts` | Generate characterization tests from runtime observation |
| clean-up | `debt-inventory.ts` | Scan for TODO comments, suppressed lints, uncovered paths |
| clean-up | `debt-dashboard.ts` | Generate inventory with cost estimates and cleanup progress |

---

## Routing: How Claude Finds the Right Workflow

Current routing: User invokes `/assess`, or Claude matches skill description → skill presents mode menu → user/agent selects mode.

Proposed routing: Claude matches **goal-level description** → loads workflow → workflow drives from Phase 1.

Each workflow skill's `description` field targets the user's natural language:

| Skill | Description Triggers |
|-------|---------------------|
| understand | "understand this code", "explore this codebase", "how does this work", "onboard to codebase" |
| change-safely | "is this safe to change", "what could break", "risky change", "impact of this change" |
| clean-up | "clean this up", "tech debt", "remove dead code", "reduce complexity" |
| debug | "fix this bug", "why is this broken", "debug this", "find the root cause" |
| migrate | "breaking change", "migration plan", "deprecate and replace", "version upgrade" |
| vestigial-detect | "find dead code", "what's unused", "vestigial elements", "orphaned content" |
| solve | "how should I solve this", "design this", "what approach should I take", "compare approaches", "type design" |
| git | "structure my commits", "rebase safely", "resolve conflicts", "clean up branch" |

Single-level routing. No mode menu. Goal in, workflow out.

---

## Migration Path

### Phase 1: Promote vestigial-detect

Move vestigial-detect from `commands/` to `skills/` as-is. It already follows the workflow pattern. This validates the skill infrastructure before restructuring everything else.

### Phase 2: Create new workflow skills

Build the new workflow skills (understand, change-safely, clean-up, debug, migrate) using the template. Start with `understand` — it's the simplest (5 phases, no scripts needed initially, all modes exist).

### Phase 3: Restructure existing content

Move mode reference files into workflow phase references and technique libraries. Create the `design` and `git` technique library skills.

### Phase 4: Delete legacy structure

Remove `commands/` directory. Remove old skill directories (assess, design→merged, implement, refactor). Update plugin.json.

### Phase 5: Develop new content

Write the missing phases (debugging modes, testing support, safety net construction). Develop new scripts.

---

## What This Doesn't Change

- **Plugin boundary:** Software plugin remains self-contained
- **Thinkies integration:** Workflow phases still invoke thinkies skills (decompose, argue-opposite, premortem, etc.) as techniques
- **Journal integration:** Checkpoints still use journal-write
- **Script infrastructure:** Existing vestigial-detect scripts remain; new scripts follow same patterns
- **Progressive disclosure:** SKILL.md stays lean; detailed content in references/

---

## Risk Assessment

| Risk | Mitigation |
|------|-----------|
| Workflows too rigid for novel situations | Technique libraries (design, git) remain for exploratory work. Workflows have early-exit points. |
| Losing discoverability of individual modes | Technique libraries maintain browsable mode collections. Workflow phases explicitly name which techniques they use. |
| Migration breaks existing users | Phase the migration. Old skill names redirect to new structure during transition. |
| Scope creep in new content | Prioritize workflow structure first, new content second. Workflows work with existing modes before gaps are filled. |
| Mode duplication across workflows | Modes live in one location. Workflows reference them. Single source of truth. |

---

## Success Criteria

1. **Routing is single-level:** User intent → workflow. No mode menus.
2. **Commands directory is empty:** All entry points are skills.
3. **Zero mode content lost:** Every existing reference file has a home.
4. **Workflows are resumable:** Checkpoints enable pause/resume across sessions.
5. **New gaps identified:** Debugging, testing, and safety net content exists.
6. **Automated tooling extends:** At least 2 new scripts beyond vestigial-detect's existing set.

---

## Open Questions for Decision

1. **Where do shared mode references live?** When blast-radius is used by 3 workflows, does the file live in one workflow's `references/` and get referenced by others, or in a shared `references/` at the plugin root?

2. **How granular should workflow skills be?** Should `clean-up` and `vestigial-detect` be separate skills (current proposal) or should vestigial-detect be Phase 2 of clean-up?

3. **Code review workflow:** The research identified code review as a distinct workflow. This proposal omits it because the `code-review` plugin already exists. Should software plugin own a review skill anyway, or defer to the existing plugin?
