---
status: descoped
priority: 3
created: 2026-02-19
source: Ronacher analysis + landscape research
research: research/skill-composition.research.md
synthesis: ../ronacher-synthesis.md
---

# Skill Composition: Pipeline Protocol for Chaining Skills — Proposal

## Summary

Skills are individually powerful but operationally isolated. Users mentally chain them (`/plan` → `/design` → `/implement`) but no protocol connects one skill's output to the next skill's input. This proposal introduces **Skill Manifests** (typed input/output declarations on every skill), an **Artifact Bus** (lightweight typed storage between steps), and **Pipeline Definitions** (optional YAML files for explicit chains) — creating a composition layer that lets skills multiply each other's capabilities without requiring new runtime infrastructure.

The design draws on five convergent patterns identified across 36 sources in the [research report](research/skill-composition.research.md): typed contracts at boundaries (DSPy), dependency-driven execution (Dagster/Bazel), plan-then-execute separation (ReWOO/LATM), content-addressed caching (Nix), and self-extending capability (Voyager).

## Background

### Problem Context

Ronacher's third principle: **agent power scales with composability** ([Ronacher, "Agentic Coding"](https://lucumr.pocoo.org/2026/2/9/a-language-for-agents/)). CLI tools beat MCP because CLI tools compose into shell scripts. Terminal beats editor because terminals nest agents. Individual capabilities multiply when they chain.

Our skills operate as isolated invocations. The software plugin has a natural lifecycle (`understand → design → implement → change-safely`) with documented exit routing between skills — but the routing is informal prose ("if constraints discovered, go to understand"), not typed data contracts. Switchboard passes phase summaries forward as accumulated text, not structured artifacts. Journal persists 7 content kinds with sophisticated cross-referencing (EntryRef, topics, frecency) but has no concept of a typed intermediate artifact produced by a skill.

### Current State

**What exists:**

- 42+ skills across 7 plugins, each invoked independently
- Software plugin: 4 skills with explicit exit routing between cognitive modes — but no structured data flows between them
- Switchboard: phase-to-phase context accumulation via text summaries; `.flow.yaml` DSL with topology notation
- Journal: Document envelope (`Document<T>`), 7 ContentKinds, EntryRef cross-references, topic taxonomy, frecency scoring
- Perspectives: generate → consult → delegate already chains implicitly through persona YAML files

**What's missing:**

- No skill declares what it produces or what it consumes
- No typed intermediate representation between skills
- No way to cache or reuse a skill's output across invocations
- No pipeline definition format for explicit multi-skill workflows
- Switchboard phases don't capture outputs as reusable artifacts
- Journal has no content kind for skill-produced artifacts

### Why Now

Three forces converge:

1. **Research consensus.** Every robust composition system — DSPy signatures, Bazel build rules, Dagster asset types, Beam PTransforms — enforces typed contracts at step boundaries ([research report, Pattern 1](research/skill-composition.research.md#pattern-1-typed-contracts-at-boundaries)). The field has converged; the pattern is proven.

2. **Existing infrastructure.** Journal's Document envelope and switchboard's flow DSL provide 80% of what's needed. The remaining 20% is the composition glue: skill manifests + artifact bus.

3. **User directive.** "We are open to big changes, especially in the journal plugin. Skill composition is cross-cutting and could reshape how all plugins interact."

## Proposal

### What

A three-layer composition system that adds typed data flow between skills:

```
Layer 3: Pipeline Definitions (.pipeline.yaml)    ← Optional explicit chains
Layer 2: Artifact Bus (.claude/artifacts/)         ← Typed storage between steps
Layer 1: Skill Manifests (YAML frontmatter)        ← Input/output declarations
```

Each layer is independently useful. Layer 1 enables documentation and ad-hoc composition. Layer 2 enables caching and cross-session reuse. Layer 3 enables declarative multi-skill workflows.

### Layer 1: Skill Manifests

Every skill gains `produces` and `consumes` fields in its YAML frontmatter, declaring what typed artifacts it can produce and accept:

```yaml
---
name: plan
description: Map territory before moving through it...
user-invocable: true
produces:
  - type: TerritoryMap
    description: Structured understanding of codebase region
    schema: references/artifacts/territory-map.schema.yaml
consumes: []  # plan is a pipeline entry point
---
```

```yaml
---
name: design
description: Design solutions through types and abstractions...
user-invocable: true
produces:
  - type: TypeDesign
    description: Type signatures, abstraction boundaries, complexity assessment
    schema: references/artifacts/type-design.schema.yaml
consumes:
  - type: TerritoryMap
    required: false  # can run standalone, but better with upstream plan
---
```

**Key properties:**

- `produces`/`consumes` are arrays — a skill can produce multiple artifact types and accept multiple inputs
- `required: false` means the skill can run without the artifact (standalone mode) but benefits from it (composed mode)
- `schema` points to a YAML schema file defining the artifact's structure
- The manifest is the composition primitive — matching `produces.type` to `consumes.type` builds the DAG automatically ([Dagster's dependency inference pattern](https://dagster.io/blog/software-defined-assets))

**What the schema file looks like:**

```yaml
# references/artifacts/territory-map.schema.yaml
type: TerritoryMap
version: "1.0.0"
fields:
  landmarks:
    type: list
    item_type: object
    description: Key files/modules and their architectural roles
    fields:
      path: { type: string, description: File or directory path }
      role: { type: string, description: Architectural role (entry point, data model, etc.) }
      stability: { type: enum, values: [stable, evolving, volatile] }
  dependencies:
    type: list
    item_type: object
    description: Import/call relationships between landmarks
    fields:
      from: { type: string }
      to: { type: string }
      coupling: { type: enum, values: [tight, loose, interface-only] }
  risks:
    type: list
    item_type: object
    description: Identified failure modes
    fields:
      description: { type: string }
      severity: { type: enum, values: [low, medium, high, critical] }
      affected_landmarks: { type: list, item_type: string }
  constraints:
    type: list
    item_type: string
    description: Discovered limitations that bound the solution space
  recommended_next:
    type: string
    description: Which skill should run next (design, implement, etc.)
    required: false
```

**Why not runtime-enforced types?** Our skills are Markdown prompts executed by an LLM, not programmatic functions. The "typed contract" is a prompt instruction ("produce output conforming to this schema") plus a post-hoc validation check. This mirrors how Pydantic AI bridges probabilistic LLM outputs with deterministic type expectations ([Pydantic AI](https://ai.pydantic.dev/)) — the schema constrains generation, validation confirms compliance.

### Layer 2: Artifact Bus

A lightweight storage layer for typed skill outputs:

```
.claude/artifacts/
├── <skill>-<hash>.artifact.yaml     # Individual artifacts
└── _manifest.yaml                   # Registry of available artifacts
```

**Artifact envelope:**

```yaml
artifact:
  id: plan-a7f3b2c1            # <skill>-<content-hash-prefix>
  skill: software:assess          # Producing skill (plugin:skill)
  type: TerritoryMap            # From the skill's produces declaration
  schema_version: "1.0.0"      # Artifact schema version
  created: 2026-02-19T10:30:00Z
  context:                      # What produced this (for caching)
    inputs: []                  # Upstream artifact IDs consumed
    target: "plugins/journal/"  # What was analyzed/operated on
    session: "abc123"           # Session ID if journaled
data:                           # The typed payload
  landmarks:
    - path: plugins/journal/src/lib/types.ts
      role: domain-model
      stability: stable
    - path: plugins/journal/src/commands/save/
      role: entry-point
      stability: evolving
  dependencies:
    - from: commands/save/
      to: lib/types.ts
      coupling: tight
  risks:
    - description: Document envelope changes break all content kinds
      severity: critical
      affected_landmarks: [lib/types.ts]
  constraints:
    - "7 existing ContentKinds with backward compatibility requirements"
    - "EntryRef format is a branded string used across plugins"
  recommended_next: design
```

**Content-addressed caching.** The artifact ID includes a hash of the skill version + input artifacts + target. If the same skill runs with the same inputs on the same target, the cached artifact is returned without re-execution. This follows the Nix derivation model: if inputs haven't changed, outputs are reused ([Nix Pills: Our First Derivation](https://nixos.org/guides/nix-pills/06-our-first-derivation)).

**Dual persistence modes:**

| Mode | Storage | Lifetime | Use Case |
|------|---------|----------|----------|
| **Ephemeral** | `.claude/artifacts/` | Cleared per pipeline run or session | Working state during active composition |
| **Persistent** | Journal (new ContentKind) | Cross-session, indexed by topic | Reusable analysis, stable plans, proven designs |

**Promotion from ephemeral to persistent** is an explicit action: "save this artifact to journal." This avoids polluting the journal with intermediate state while enabling long-lived artifacts when valuable.

### Layer 3: Pipeline Definitions

Optional YAML files for explicit multi-skill workflows:

```yaml
# .claude/pipelines/code-lifecycle.pipeline.yaml
pipeline: code-lifecycle
description: Full software development lifecycle

steps:
  - skill: software:assess
    produces: TerritoryMap

  - skill: software:design
    consumes: [TerritoryMap]
    produces: TypeDesign

  - skill: software:implement
    consumes: [TypeDesign]
    produces: ChangeSet

  - skill: software:refactor
    consumes: [ChangeSet]
    produces: StructureImprovement

on_error: stop     # stop | skip | retry
persist: false     # save final artifacts to journal?
```

**Invocation:** A `/compose` meta-skill reads the pipeline definition and orchestrates execution:

```
/compose code-lifecycle --target src/feature/
```

The orchestrator:

1. Reads the pipeline YAML
2. Validates type compatibility (each `consumes` matches an upstream `produces`)
3. Executes steps sequentially, passing artifacts between them
4. Validates each artifact against its schema
5. Reports the pipeline result with links to all produced artifacts

**Ad-hoc composition** also works without a pipeline file. If a user invokes `/design` and a `TerritoryMap` artifact exists from a recent `/plan`, the skill can detect and offer to consume it:

```
Found upstream artifact: TerritoryMap from /plan (2 minutes ago)
Use this as input? [Y/n]
```

This implicit discovery follows the convention-based approach (Option A from the idea doc) and requires zero infrastructure — just the skill manifest declarations.

### How

**Implementation sequence — four phases, each independently shippable:**

#### Phase 1: Skill Manifests (Layer 1 only)

Add `produces`/`consumes` to software plugin skills. Write artifact schema files. No runtime changes — this is pure documentation that enables future composition.

**Scope:** 4 software skills + their artifact schemas. ~8 files modified/created.

**Validates:** Can we define meaningful typed contracts for our existing skills? Which skills produce structured enough output?

#### Phase 2: Artifact Bus (Layer 2)

Implement the `.claude/artifacts/` storage layer. Skills gain instructions to write artifacts when producing structured output. Downstream skills gain instructions to check for and consume upstream artifacts.

**Scope:** Artifact envelope format, content-addressed IDs, ephemeral storage. Convention updates in skill prompts. ~4 files created, ~4 skills modified.

**Validates:** Does typed artifact passing actually improve composition vs. conversational text passing?

#### Phase 3: Pipeline Definitions (Layer 3)

Create the `.pipeline.yaml` format and `/compose` meta-skill. Define the first pipeline (code-lifecycle). Add validation and error handling.

**Scope:** Pipeline schema, orchestration logic in `/compose`, 2-3 built-in pipelines. ~6 files created.

**Validates:** Do explicit pipelines produce better results than ad-hoc invocation?

#### Phase 4: Integration

- **Journal integration:** New `Artifact` ContentKind for persistent storage. Artifacts indexed by topic, linked via EntryRef.
- **Switchboard integration:** Pipeline steps can be STRAND-like units within a flow phase. A flow phase can reference a pipeline instead of a raw goal.
- **Cross-plugin pipelines:** `thinkies:decompose → software:understand → software:design` as a named pipeline.

**Scope:** Journal type additions, switchboard flow extensions, cross-plugin pipeline definitions. ~10 files modified.

### Why This Approach

**1. Incremental adoption.** Each phase ships independently. Phase 1 is pure documentation; Phase 2 is a convention; Phase 3 is a new skill; Phase 4 is integration. No big-bang change required.

**2. Convention over infrastructure.** The composition layer is primarily prompt conventions (how skills write/read artifacts), not new runtime code. This follows Ronacher's principle: "CLI > MCP because CLI composes into scripts" — our composition should be Markdown conventions that compose into pipelines, not a new execution engine.

**3. Dual discovery modes.** Explicit pipelines for known workflows (code-lifecycle, analysis, consultation) and implicit discovery for ad-hoc use. Research shows both are needed: Dagster infers DAGs from signatures; Bazel requires explicit BUILD files. The right answer is both ([research report, Synthesis](research/skill-composition.research.md#synthesis-strongest-patterns-and-protocol-implications)).

**4. Existing infrastructure leverage.** Journal's Document envelope becomes the persistent artifact store. Switchboard's flow phases become pipeline execution contexts. No new storage system; no new orchestration engine.

**5. LLM-native typing.** The schemas are prompting constraints validated post-hoc, not compile-time guarantees. This is realistic for an LLM-based system and matches how Pydantic AI bridges probabilistic outputs with typed expectations.

## Alternatives Considered

### Alternative 1: Pure Convention (Option A from idea doc)

Skills write artifacts to `.claude/artifacts/<skill>-<timestamp>.yaml` with no formal schema or manifest.

**Why not chosen as the full solution:** Without typed manifests, there's no way to validate compatibility between skills, no way to build a DAG automatically, and no way for a meta-skill to orchestrate a pipeline. Convention alone is necessary (Phase 1 starts here) but insufficient for the full composition story.

**Retained as:** The implicit discovery mechanism in Phase 2. Conventions are the base layer that formal pipelines build on.

### Alternative 2: Switchboard-First (Option C from idea doc)

Every pipeline is a switchboard flow. Every skill invocation is a STRAND.

**Why not chosen:** Switchboard is designed for multi-agent orchestration — teams, topology notation, discussion rounds. Most skill pipelines are single-session, single-agent workflows that don't need agent coordination overhead. Forcing `plan → design → implement` through switchboard's team creation, agent spawning, and phase management would be over-engineering for the common case.

**Retained as:** Phase 4 integration. When a pipeline step benefits from sub-agent execution (fresh context, parallel work), it can opt into switchboard. But this is additive, not foundational.

### Alternative 3: Full DAG Engine

Build a dependency resolution engine that automatically determines execution order from type declarations, supports parallel execution of independent steps, and handles partial failure recovery.

**Why not chosen:** This replicates Dagster/Bazel within our plugin system — powerful but premature. Our initial pipelines are linear chains (4-5 steps). A full DAG engine is justified only when we have enough cross-plugin pipelines with branching to warrant the complexity. Phase 1-3 lay the groundwork; a DAG engine is a Phase 5+ concern.

## Integration Points

### Journal (high impact — "open to big changes")

**New ContentKind: `Artifact`**

```typescript
interface ArtifactData {
  /** Producing skill (plugin:skill format) */
  readonly source_skill: string;
  /** Artifact type name (e.g., TerritoryMap) */
  readonly artifact_type: string;
  /** Schema version */
  readonly schema_version: string;
  /** Content-addressed hash of inputs */
  readonly content_hash: string;
  /** The typed payload */
  readonly data: Record<string, unknown>;
  /** Upstream artifact IDs consumed */
  readonly input_artifacts: readonly string[];
  /** What was analyzed/operated on */
  readonly target?: string;
}
```

This joins the existing 7 kinds (Session, Note, Insight, Context, Reflection, Catch, Topic) as an 8th kind. Artifacts are:

- Indexed by topic (same taxonomy as other content)
- Linked via EntryRef (`artifact:<id>`)
- Surfaced by frecency (high-access artifacts are more visible)
- Searchable by type (`artifact_type: TerritoryMap`)

**Journal as artifact store.** When an artifact is promoted from ephemeral to persistent, it becomes a journal Document with ContentKind `Artifact`. This means cross-session artifact reuse is free — if you planned a codebase region last week, the TerritoryMap is still in the journal, still indexed, still surfaceable.

### Switchboard (medium impact)

**Pipeline-aware flow phases.** A switchboard flow phase gains an optional `pipeline` field:

```yaml
phases:
  analysis:
    goal: Analyze the target codebase
    topology: "@analyst"
    pipeline: code-lifecycle    # Run this pipeline, not just freeform work
```

When a phase has a `pipeline` field, the agent executes that pipeline within its switchboard context. The pipeline's artifacts become the phase's output. This unifies skill composition with agent orchestration — same artifacts, different execution contexts.

**STRAND as pipeline step.** In orchestrated mode, each pipeline step can be a STRAND — a narrated work unit with its own context. The STRAND receives only the upstream artifact + skill prompt + CLAUDE.md, achieving Ronacher's context isolation principle (P6: "sub-agents get fresh context").

### Thinkies (medium impact)

Natural pipeline: `decompose → trace-logic → check-soundness → integrity`

```yaml
produces:
  - type: Decomposition      # decompose output
  - type: LogicalChain       # trace-logic output
  - type: SoundnessReport    # check-soundness output
  - type: IntegrityAudit     # integrity output
```

The deep reasoning pipeline passes increasingly refined analysis between cognitive skills, each with a focused context containing only the upstream artifact.

### Perspectives (already partially composed)

The generate → consult → delegate chain already passes persona YAML between steps. Skill composition formalizes this:

```yaml
produces:
  - type: PersonaDefinition   # generate output (already exists as YAML)
  - type: ExpertAnalysis      # consult output
  - type: Deliverable         # delegate output
```

### Expression (low impact)

`proofread → refine` is a two-step pipeline. Proofread produces a diagnostic artifact; refine consumes it.

### Visualizer (low impact)

Could consume data artifacts from analysis pipelines. A `DataProfile` artifact from a thinkies analysis becomes input to visualization.

## Risks and Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Schema rigidity.** Typed contracts constrain LLM output, potentially losing valuable unstructured insights | High | Artifacts include a freeform `notes` field for unstructured content. Skills always produce both the typed artifact and conversational output. The artifact augments, not replaces, the prose. |
| **Adoption friction.** Skill authors must define schemas for composition to work | Medium | Phase 1 starts with software plugin only (4 skills). Schemas are optional — skills without manifests continue working as-is. |
| **Schema evolution.** Changing an artifact type breaks downstream consumers | Medium | Schema versioning (semver). Downstream skills declare compatible version ranges. Breaking changes require a major version bump and adapter. |
| **Validation overhead.** Post-hoc validation of LLM output against schemas may fail frequently | Medium | Schemas define required vs. optional fields. Core structure is required; detail fields are optional. Validation is lenient (warn on missing optional fields, fail only on missing required fields). |
| **Over-engineering.** Pipeline infrastructure for what could be conversational skill chaining | High | Each phase ships independently. Phase 1 is pure documentation. If Phase 2 (artifact bus) doesn't measurably improve outcomes over conversational chaining, we stop there. The exit ramp is built in. |
| **Context cost.** Artifact schemas loaded into skill prompts increase per-skill context | Low | Schemas are referenced by path, not inlined. The skill prompt says "produce output conforming to `references/artifacts/territory-map.schema.yaml`"; the schema file is only loaded when composing. |

## Open Questions

### Resolved by Research

| Question (from idea doc) | Resolution |
|--------------------------|------------|
| What's the artifact schema? Per-skill or common envelope? | **Common envelope + per-skill payload.** Every artifact has the same envelope (id, skill, type, schema_version, created, context). The `data` field contains the skill-specific typed payload. This follows the journal's Document envelope pattern. |
| Should artifacts persist across sessions or be ephemeral? | **Both.** Ephemeral by default (`.claude/artifacts/`), with explicit promotion to journal for persistence. This mirrors Nix's store (content-addressed, cached) vs. garbage collection model. |
| How does the user invoke a pipeline? | **Three modes.** (1) `/compose <pipeline-name>` for explicit pipelines. (2) Implicit — downstream skills detect and offer upstream artifacts. (3) Switchboard — flow phases reference pipelines. |
| How does this relate to switchboard's STRAND concept? | **Pipeline steps can be STRANDs, but aren't required to be.** In single-session mode, pipeline steps run sequentially in one context. In orchestrated mode (via switchboard), each step is a STRAND with its own agent and fresh context. The artifact bus is the bridge between both modes. |

### Remaining Open

- [ ] **Branching and error recovery.** The proposal supports `on_error: stop | skip | retry` but doesn't address conditional branching (if design reveals a problem, go back to plan). Should pipelines support backward edges, or should error recovery be handled by the orchestrating agent?
- [ ] **Cross-session artifact staleness.** If a TerritoryMap from last week is in the journal, how does the system know it's stale (codebase changed since)? Content-addressed hashing helps (different inputs = different hash) but doesn't detect external changes.
- [ ] **Artifact size limits.** Large artifacts (full dependency graphs, comprehensive type designs) could be expensive to pass between skills. Should there be a compression/summarization step at artifact boundaries?
- [ ] **Multi-artifact production.** Some skills might produce multiple artifact types in one invocation (e.g., `/understand` produces both a TerritoryMap and a RiskAssessment). The manifest supports this, but the pipeline format needs to handle fan-out cleanly.
- [ ] **User-defined artifact types.** Can users define project-specific artifact schemas (e.g., a `MigrationPlan` type for a specific codebase)? This would enable the Voyager-like self-extending capability where composed pipelines become first-class skills.

## Request

This proposal seeks feedback on:

1. **Layer priority.** Is the three-layer approach (manifests → bus → pipelines) the right decomposition? Should any layer be merged or split?
2. **Journal integration depth.** Adding `Artifact` as an 8th ContentKind is a significant change. Is this the right boundary, or should artifacts be a separate storage system that journal can index?
3. **Software plugin as first target.** Is the `understand → design → implement → change-safely` lifecycle the right first pipeline to formalize? Or would a thinkies reasoning pipeline (lower stakes, more contained) be a better starting point?
4. **Schema philosophy.** Should artifact schemas be strict (reject non-conforming output) or lenient (accept partial conformance, warn on gaps)? The proposal leans lenient, but strict schemas produce more reliable composition.

## Synthesis Outcome

**Priority:** #3 of 3. **Descoped** from the full three-layer proposal to Layer 1 only (Skill Manifests as documentation). Ships in Phase 1b, parallel with verification gates.

**Why descoped:** The Composition-Critic's challenges fundamentally reshaped what's viable:

1. **"Skills are cognitive protocols, not functions."** The deepest challenge. Forcing prose reasoning into typed schemas either loses the reasoning's value or doubles context cost for compliance. Manifests as documentation work around this — descriptions, not enforcement.

2. **Content-addressed caching is impossible for non-deterministic LLM outputs.** The Nix derivation analogy breaks precisely where it matters most. Same skill + same inputs can produce meaningfully different outputs. Caching is a false economy.

3. **The conversation is the artifact bus for same-session composition.** The Gates-Critic's observation that within a single session, the conversation context already carries data between skills deflates half the artifact bus's value proposition. Cross-session is where artifacts add value — and checkpoints already handle that.

4. **Dual storage fractures context.** An ephemeral bus (`.claude/artifacts/`) alongside the journal (`.claude/.thinkies/`) forces the agent to reason about WHERE data lives. One system, one truth.

5. **Schema validation failures consume context for compliance, not for the task.** Each failed validation is a context furnace that displaces actual work.

**What survives (Phase 1b):**

- `produces`/`consumes` in skill YAML frontmatter as descriptive text
- No schema files, no validation, no artifact bus, no pipeline definitions
- Software plugin's 4 skills gain manifest declarations
- This enables: better ad-hoc chaining, switchboard flow design, discoverability

**What is deferred (Phase 4, unscheduled):**

- Artifact Bus (`.claude/artifacts/`)
- `ContentKind.Artifact` in journal
- Pipeline definitions (`.pipeline.yaml`)
- `/compose` meta-skill
- Schema validation and content-addressed caching

**Activation criteria for Phase 4:**

1. Skill manifests demonstrate that typed contracts improve composition in practice
2. Cross-session artifact reuse demand materializes from real usage
3. The conversation-as-artifact-bus pattern proves insufficient for same-session chains

**Design changes from debate:**

- Three-layer system reduced to Layer 1 only
- Schema files replaced by descriptive text in frontmatter
- Artifact ContentKind deferred indefinitely
- Pipeline definitions and `/compose` deferred indefinitely
- Software plugin remains first target (if activated), but thinkies reasoning pipeline identified as lower-stakes alternative
- Schema philosophy resolved (for Phase 4 if activated): strict core (`source_skill`, `artifact_type`, `schema_version`, `data` — fail if missing) + flexible extension (additional metadata accepted). Manifests in Phase 1b use descriptive text only, no schema enforcement.
