---
status: proposing
created: 2026-02-18
source: Ronacher "Agentic Coding" talk analysis
---

# Skill Composition: Pipeline Protocol for Chaining Skills

## Problem

Ronacher's third principle: **agent power scales with composability**. CLI tools beat MCP because CLI tools compose into shell scripts. Terminal beats editor because terminals nest agents. The fundamental insight: individual capabilities multiply when they chain.

Our skills are individually powerful — `/decompose` breaks problems apart, `/plan` maps territory, `/design` defines types and abstractions, `/implement` writes code, `/refactor` improves structure. But they operate as **isolated invocations**. Each skill is called independently; the output of one skill is not structurally connected to the input of the next.

In practice, users mentally chain skills: decompose a problem, then plan an approach, then design the solution, then implement it. But this chain exists only in the user's head and in the conversation context. There's no protocol for one skill's output to become another skill's input — no pipe operator for cognitive tools.

This matters because:

1. **Context efficiency** — if `/plan` produces a structured plan and `/implement` needs that plan, the plan should be passed directly, not re-derived from conversation history.
2. **Composability** — users should be able to define custom pipelines (e.g., "for this project, always decompose → plan → implement").
3. **Sub-agent delegation** — a pipeline could dispatch steps to sub-agents (switchboard), each with a focused context containing only the previous step's output.

## Core Concept

A **skill pipeline** is an ordered sequence of skill invocations where each skill's output becomes structured input for the next skill.

### Pipeline Primitives

**Artifact:** A structured output produced by a skill that can be consumed by a downstream skill. Not free text — a schema'd document with known fields.

**Pipe:** A connection between two skills specifying which artifact fields from the upstream skill feed which input parameters of the downstream skill.

**Pipeline:** An ordered sequence of pipes forming a directed acyclic graph (or linear chain) of skill invocations.

### Natural Pipelines in Our Ecosystem

| Pipeline | Steps | Artifact Flow |
|----------|-------|---------------|
| **Code lifecycle** | plan → design → implement → refactor | territory map → type definitions → working code → improved code |
| **Analysis** | decompose → consider-alternatives → evaluate-evidence → synthesize | parts → hypotheses → evidence assessment → synthesis |
| **Expert consultation** | generate (persona) → consult (analysis) → delegate (execution) | persona YAML → cited analysis → deliverable |
| **Deep reasoning** | decompose → trace-logic → check-soundness → integrity | parts → logical chain → consistency check → verified claim |

### How It Might Work

**Option A: Convention-based (minimal infrastructure)**

Skills adopt an output convention — they write a structured artifact to a known location:

```
.claude/artifacts/<skill-name>-<timestamp>.yaml
```

Downstream skills check for artifacts from their expected upstream. No new infrastructure needed — just a convention in skill prompts.

**Option B: Pipeline definitions (medium infrastructure)**

A `.claude/pipelines/` directory with YAML pipeline definitions:

```yaml
name: code-lifecycle
steps:
  - skill: plan
    output: territory-map
  - skill: design
    input: territory-map
    output: type-definitions
  - skill: implement
    input: type-definitions
    output: working-code
  - skill: refactor
    input: working-code
    output: improved-code
```

A meta-skill (`/pipeline` or `/chain`) reads the definition and orchestrates execution.

**Option C: Switchboard integration (maximal infrastructure)**

Pipelines ARE switchboard flows. Each skill invocation is a STRAND. The pipeline is a PATCH. This unifies skill composition with agent orchestration — same system, different granularity.

### Interaction with Sub-Agents

Ronacher's key insight: sub-agents conserve context by getting isolated contexts for subtasks. A pipeline step executed by a sub-agent gets only:

1. The upstream artifact (not the full conversation history)
2. The skill prompt
3. The project's CLAUDE.md

This is dramatically less context than running all steps in one session. Each step starts clean.

## Initial Thoughts

- **Option A (convention-based) should come first.** It requires no new infrastructure — just standardizing how skills write and read artifacts. This is the "CLI > MCP" principle applied internally: simple, composable, debuggable.
- The artifact format matters enormously. YAML is human-readable and agent-readable. JSON is more structured but less scannable. Markdown with YAML frontmatter bridges both.
- Not all skills produce artifacts suitable for chaining. `/wonder` produces open questions — useful for humans, not structured enough for a downstream skill. Composition works for skills with structured outputs.
- The software plugin's 5-skill lifecycle (plan → design → implement → refactor → vestigial-detect) is the most natural first pipeline to formalize.
- Option C (switchboard integration) is architecturally elegant but high-effort. Worth keeping in mind as the endpoint, but starting there would be over-engineering.

## Open Questions

- [ ] What's the artifact schema? Is it per-skill or is there a common envelope with skill-specific payloads?
- [ ] Should artifacts persist across sessions (journal-like) or be ephemeral (cleared per pipeline run)?
- [ ] How does the user invoke a pipeline? New skill? New syntax? Or does `/implement` automatically check for an upstream `/design` artifact?
- [ ] Which existing skills produce outputs structured enough to serve as artifacts today? Which would need modification?
- [ ] How does this relate to switchboard's STRAND concept? Is a pipeline step just a lightweight STRAND?
- [ ] Should pipelines support branching (if design reveals a problem, go back to plan) or only forward flow?
