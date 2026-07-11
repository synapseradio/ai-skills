# Ronacher Integration Synthesis: Final Consensus

> Three ideas — Context Checkpoints, Verification Gates, Skill Composition — researched, proposed, and stress-tested through structured premortem and adversarial debate. This document is the final synthesis: priority ranking, implementation sequence, journal evolution strategy, and bold recommendations.

## Priority Ranking

### 1. Verification Gates — Ship First

**Justification:** Lowest effort, highest immediate impact, and the structural foundation that both other proposals require.

Gates address Ronacher's Bedrock B (binary legibility) directly: every step must produce an unambiguous pass/fail signal. The research base is unambiguous — CI/CD systems, test frameworks (pytest exit code 5, cargo-nextest's `--no-tests=fail`), and agent evaluation (Anthropic's compound verification) all converge on mandatory binary gates.

**Surviving the premortem:** The Checkpoints-Critic's sharpest challenge — that gates are "advisory with strong language," not physical enforcement — is true but applies to the entire skill system. Skills are prompt instructions. Gates don't need to be infrastructure to be valuable; they need to change the default from "verification is optional" to "verification is expected." The context cost argument (5-15x for output) is misleading: the test output would be consumed regardless of whether gates mandate it. The gate *instruction* itself (~60-80 tokens) is cheap.

The flaky test concern (2-8% flake rates becoming "context furnaces") is a real project problem that gates make *visible*, not one they create. The Environment Gate's upfront cost (~90s + 500 tokens) is justified by the premortem panel's evidence: building plans on a broken foundation cascades confusion through the entire session.

**What makes this first:** The Gates-Critic proved that checkpoints *structurally require* gates — "checkpoint loaded successfully" is the new "0 tests passed successfully." Without a Resume Gate validating checkpoint content, self-reported checkpoints inherit the agent's blind spots. Gates are prerequisite infrastructure.

### 2. Context Checkpoints — Ship Second

**Justification:** Addresses Ronacher's most emphasized pain point (context rot: "if you ever get to the point where you have to compact, you're kind of lost") and has a 4-10x context ROI (~500 tokens saves 2000-5000 tokens of re-exploration).

Checkpoints fill a genuine landscape gap. No existing tool provides structured, schema-enforced, agent-written resumption artifacts. Manus's `todo.md` validates the pattern in production. Cline's Memory Bank demonstrates community demand but lacks schema and failed-approach tracking. LangGraph is the only mature checkpoint system but requires stateful runtime — we need stateless, portable checkpoints.

**Surviving the premortem:** The Gates-Critic's challenge that `project_state` is "a cached assertion with no decay signal" is mitigated by the Resume Gate: validate branch existence, file existence, and test state at load time. Stale checkpoints are flagged, not blindly loaded.

The `failed_approaches` false-constraint risk (mis-attributed failures constraining future sessions) is the most subtle danger. Mitigation: scope checkpoints explicitly to tasks and instruct agents to evaluate `failed_approaches` critically — as context, not absolute constraints.

The Composition-Critic's claim that checkpoints are "anti-composable monoliths" is philosophically interesting but practically wrong for the primary use case. Cross-session continuity needs one coherent document for fastest ramp-up. The Manus validation confirms this: a single `todo.md`, not decomposed files.

### 3. Skill Manifests — Ship Third (Descoped from Full Composition)

**Justification:** The Composition-Critic's deepest challenge — "skills are cognitive protocols, not functions" — fundamentally reshapes what's viable.

The full three-layer composition proposal (manifests + artifact bus + pipeline definitions) suffers from three structural problems the debate surfaced:

1. **Content-addressed caching is impossible** for non-deterministic LLM outputs. The Nix analogy breaks down precisely where it matters most.
2. **The conversation is the artifact bus** for same-session composition. Dual storage (bus + journal) fractures context rather than simplifying it.
3. **Schema validation failures consume context for compliance**, not for the task. Each validation failure is a context furnace that displaces actual work.

**What survives:** Layer 1 — Skill Manifests as documentation. Adding `produces`/`consumes` to skill YAML frontmatter is pure upside: no runtime cost, no new infrastructure, and it enables better ad-hoc chaining, switchboard flow design, and future composition if the need materializes. DSPy's typed signatures prove that even as pure documentation, typed contracts are transformative for discoverability and intent communication.

Layers 2-3 (artifact bus, pipeline definitions, `/compose` meta-skill) are **deferred** until manifests have proven their value and real composition workflows demonstrate demand.

## Implementation Sequence

### Phase 0: Journal Simplification

**Prerequisite for everything.** Cannot extend what we haven't simplified.

| Strip | Rationale |
|-------|-----------|
| Observation (entire ContentKind) | Orthogonal, no dependencies |
| Threading remnants | Removed in v1.1.0, ghosts remain |
| CatchEnergy enum | Decorative, never validated |
| Close → session merge | Collapse into session complete/update |
| CAID from surface | Implementation detail, not skill concern |
| Behavioral frecency types | ~100 lines of speculative infrastructure |
| Usage tracking types | Orphaned by Observation removal |
| Deprecated fields | Migration artifacts |
| CatchStore, CatchIndex | Leaked implementation types |

**Result:** types.ts drops from ~1087 lines to ~650 lines. 7 ContentKinds remain: Session, Note, Insight, Context, Reflection, Catch, Topic.

**Journal skill rewrite:** The skill should describe the clean 7-kind state. No mention of what was stripped. Clear instruction on how the journal is used, not how it arrived here.

### Phase 1a: Verification Gates (Low Effort)

Ship as markdown instructions embedded in software skill protocols. No new CLI, no new types, no journal integration.

| Skill | Gate | Placement |
|-------|------|-----------|
| `/plan` | Environment Gate | Phase 0 before decision tree |
| `/design` | Type Gate | After Type-Analytical cycle |
| `/implement` | Build + Test Gate | After each commit-ready unit |
| `/refactor` | Preservation Gate | Before and after (baseline + verify) |

**Deliverables:**

- `references/verification-protocol.md` in software skill directory
- Gate sections added to 4 skill files
- Three-tier configuration (CLAUDE.md declaration → project inference → skip with warning)

**Critical rule:** "Ambiguous = FAIL." This single rule fixes vacuous success.

### Phase 1b: Skill Manifests (Low Effort, Parallel with 1a)

Add `produces`/`consumes` to software skill frontmatter. Write schema descriptions (not schema files — descriptions). No runtime, no validation, no artifact bus.

```yaml
---
name: plan
produces:
  - type: TerritoryMap
    description: Structured understanding of codebase region
consumes: []
---
```

**Why descriptions, not schema files:** The Composition-Critic is right that skills are cognitive protocols, not functions. A rigid YAML schema for a TerritoryMap would either be too loose to be useful or too tight to accommodate LLM variability. A description is the right level of contract for prose-based composition.

**Deliverables:**

- 4 software skills gain `produces`/`consumes` frontmatter
- No new files, no new infrastructure

### Phase 2: Context Checkpoints (Medium Effort)

Depends on: Phase 0 (simplified journal), Phase 1a (gates provide Resume Gate).

| Component | Description |
|-----------|-------------|
| `CheckpointData` schema | TypeScript interface in `types-checkpoint.ts` |
| `ContentKind.Checkpoint` | 8th content kind |
| `journal write checkpoint` | CLI command with schema validation |
| `journal read checkpoint` | Resume command for session start |
| Resume Gate | Validates checkpoint at load time (branch exists, files exist, project state matches) |
| Session start integration | Checkpoint as primary resumption artifact |
| Checkpoint protocol in journal skill | When/how to checkpoint |

**Key design decisions from the debate:**

- **Monolithic, not reference-based.** Start with a single coherent struct. Add reference support only if multi-week projects demonstrate the need.
- **Checkpoint absorbs session close.** (Bold recommendation — see below.)
- **<500 token guidance, not enforcement.** Agents benefit from flexibility; the skill protocol emphasizes minimality.
- **`failed_approaches` as context, not constraints.** The skill protocol instructs agents to evaluate them critically.

### Phase 3: Gate Journaling (Low Effort, Optional)

Depends on: Phase 1a (gates), Phase 2 (checkpoint infrastructure provides journal patterns).

Gate results as **structured session notes**, not a new ContentKind. A note with a `_gate` marker and structured metrics.

```yaml
gate:
  skill: implement
  gate_type: test
  result: pass
  metrics:
    tests_run: 47
    tests_passed: 47
```

**Why not a new ContentKind:** The premortem panel was unanimous — gate results are point-in-time events that belong within sessions, not standalone artifacts with distinct lifecycles. This keeps ContentKind count at 8.

**Exit ramp:** If Phase 1a (gates as markdown instructions) provides 80% of verification value, Phase 3 can be deferred indefinitely. The debate didn't settle whether the journaling adds enough analytical value to justify the implementation.

### Phase 4: Artifact Bus + Pipelines (Medium-High Effort, Deferred)

Depends on: Phase 1b (manifests must prove value), Phase 2 (checkpoint infrastructure).

**Not scheduled.** Only activate if:

1. Skill manifests demonstrate that typed contracts improve composition in practice
2. Cross-session artifact reuse demand materializes (not predicted by current usage)
3. The "conversation as artifact bus" pattern proves insufficient for same-session chains

If activated:

- `.claude/artifacts/` ephemeral storage
- `ContentKind.Artifact` as 9th kind (journal-promoted artifacts only)
- Pipeline definitions and `/compose` meta-skill
- Switchboard integration (pipeline-aware flow phases)

## Cross-Cutting Integration Points

### Shared Infrastructure

| Component | Used By | Status |
|-----------|---------|--------|
| `Document<T>` envelope | Checkpoints, gate notes, (future) artifacts | Existing |
| `EntryRef` branded string | Checkpoint references, gate note links | Existing |
| Non-vacuity principle | Gates, checkpoints, (future) artifact validation | New convention |
| Three-tier configuration | Gate commands, (future) pipeline config | New convention |
| Extension type files | `types-checkpoint.ts`, (future) `types-artifact.ts` | New pattern |

### Reinforcement Between Ideas

**Gates → Checkpoints:** The Resume Gate makes checkpoints trustworthy. Without it, "checkpoint loaded successfully" is vacuous. The Environment Gate establishes a baseline that the checkpoint's `project_state.tests_passing` can be validated against.

**Checkpoints → Gates:** Checkpoints provide gate history across sessions. If the previous session's checkpoint records `tests_passing: false`, the current session's Environment Gate knows what to expect.

**Manifests → Checkpoints:** Skill manifests declaring `produces: TerritoryMap` tells the checkpoint what orientation artifacts matter. A checkpoint's `orientation_files` can be auto-suggested from the manifest's output description.

**Manifests → Gates:** When a skill declares `produces: TypeDesign`, the system knows that a Type Gate should fire after this skill runs. Manifests make gate placement inferrable, not just manual.

### Necessary Separation

| Boundary | Rationale |
|----------|-----------|
| Gates live in skill markdown, not journal | Gates are instructions, not records. Journaling gate results is optional (Phase 3). |
| Checkpoints live in journal, not external files | Preserves the unified content graph. Graph traversal, backlinks, and health checks see the relationships. |
| Manifests are documentation, not runtime contracts | The Composition-Critic's "category error" challenge means runtime enforcement is premature for cognitive protocols. |

## Journal Evolution Strategy

### The Tension

Three proposals each want new journal capabilities. The journal just dropped from ~1087 to ~650 lines. The risk: rebuilding the bloat we just stripped.

### Resolution: Tiered Evolution with a Hard Cap

**Tier 1: Recording (existing, simplified)**

| Kind | Purpose |
|------|---------|
| Session | Container for timestamped reasoning work |
| Note | Individual entries within sessions |
| Insight | Crystallized, reusable knowledge |
| Reflection | Lessons learned from completed work |
| Catch | Ideas captured at moments of visibility |

**Tier 2: Infrastructure (existing, clarified)**

| Kind | Purpose |
|------|---------|
| Topic | Taxonomy layer for organizing content |
| Context | Attention snapshot (working memory) |

**Tier 3: Operating (new, gated)**

| Kind | Purpose | Phase | Justification Against Alternatives |
|------|---------|-------|-------------------------------------|
| Checkpoint | Structured resumption artifact | 2 | Can't be a note (distinct lifecycle: active → superseded → resolved). Can't be a session (checkpoints are mid-work artifacts; sessions are containers). Can't be working memory (captures resumption state, not attention state). |

**Hard cap: 8 ContentKinds through Phase 3.** Artifact (the 9th kind) only if Phase 4 activates. Gate results are structured notes, never a kind.

### Extension Rules

1. **New kinds require structural justification.** "Could this be a structured entry within an existing kind?" If yes, use existing kinds. This is why gate results are notes and checkpoints are not.
2. **Extension types live in separate files.** `types-checkpoint.ts` alongside core `types.ts`. The 1087-line problem must not recur.
3. **Extensions use the same infrastructure.** `Document<T>` envelope, `EntryRef` references, YAML storage. No parallel systems.
4. **Convention before infrastructure.** Manifests as documentation before schema validation. Gates as instructions before gate journaling.
5. **The non-vacuity principle governs all extensions.** Every new operation must produce a signal that cannot be satisfied by doing nothing.
6. **Strict core, flexible extension.** All schemas follow the same philosophy: required fields are strict (fail if missing or trivially empty), additional fields are accepted without restriction. This applies uniformly to checkpoint schemas, gate result schemas, and artifact schemas. See [Schema Philosophy](#schema-philosophy) below.

### Journal Skill: Clean Final State

The journal skill (SKILL.md) should describe the 8-kind system (post-Phase 2) as the intended architecture. It should:

- Present the three tiers (Recording, Infrastructure, Operating) as the journal's purpose
- Describe each kind's lifecycle and when to use it
- Explain the checkpoint protocol (when, how, what makes a good checkpoint)
- State the non-vacuity principle as a governing constraint
- not mention what was stripped, deprecated, or removed

## Schema Philosophy

The premortem debate surfaced a tension between strict schemas (reject non-conforming output) and lenient schemas (accept partial conformance). The Legibility Critic argued strict contracts with lenient enforcement is contradictory. The Composability Critic argued progressive typing — strict core, optional extensions — mirrors how TypeScript itself works.

**Resolution (user directive):** All schemas across the ecosystem follow one principle: **strict core + flexible extension.**

| Layer | Strict (required) | Flexible (optional/additional) |
|-------|-------------------|-------------------------------|
| **Checkpoint** | `task`, `completed`, `remaining`, `status`, `sequence` — fail if missing or trivially empty | `failed_approaches`, `decisions`, `orientation_files`, `project_state` fields, `[key: string]: unknown` |
| **Gate result** | `skill`, `gate_type`, `result` — fail if missing | `metrics` (gate-type-specific), `context`, additional diagnostic fields |
| **Artifact** (Phase 4) | `source_skill`, `artifact_type`, `schema_version`, `data` — fail if missing | `input_artifacts`, `target`, additional metadata |
| **Manifest** | `produces` or `consumes` array with `type` and `description` per entry | Additional fields like `schema`, `required`, version constraints |

**What "strict" means concretely:**

- Required field missing → validation error, write rejected
- Required field trivially empty (empty string, empty array where content expected) → validation error (non-vacuity applied)
- Required field present with non-trivial value → pass

**What "flexible" means concretely:**

- Optional field missing → accepted silently
- Optional field present → accepted and stored
- Unknown additional fields → accepted and stored (no schema-closed validation)
- This enables forward compatibility: new fields can be added without breaking existing readers

This resolves the strict-vs-lenient tension from the premortem and provides a uniform validation contract across all three proposals.

## Bold Recommendations

### 1. Checkpoints Should Absorb Session Close

The premortem panel already agreed to "collapse separate close into session complete/update." Take this further: **a checkpoint is the modern session close.**

- When work is incomplete → write a checkpoint (status: `active`)
- When work is done → resolve the checkpoint (status: `resolved`)
- The old "session close" narrative (summary, lessons, unresolved) was writing for reflection; the journal already has `Reflection` for that purpose

This eliminates a concept (session close as a separate operation), simplifies the session lifecycle, and makes checkpoints the universal session-boundary artifact. The checkpoint's `completed`, `decisions`, and `remaining` fields contain everything the old close narrative captured, in a more structured and actionable format.

### 2. Kill the Artifact ContentKind (For Now)

The full composition proposal wanted `ContentKind.Artifact` as a 9th kind. Defer this.

**Evidence:**

- The conversation is the artifact bus for same-session composition (Gates-Critic)
- Dual storage (bus + journal) fractures context (Composition-Critic)
- Content-addressed caching doesn't work for non-deterministic LLM outputs (Composition-Critic)
- Schema validation failures consume context for compliance, not for the task (Composition-Critic)

Artifacts solve a problem that doesn't yet exist in practice. If cross-session typed artifact reuse proves necessary, revisit. Until then, checkpoints handle cross-session continuity and the conversation handles same-session data flow.

### 3. Manifests as Pure Documentation

Don't build schema files. Don't build validation. Don't build an artifact bus. Just add `produces`/`consumes` fields as descriptive text to skill frontmatter.

This is the Complexity Trap applied to ourselves. The DSPy research shows that typed signatures are valuable even as pure documentation — they enable discoverability, intent communication, and ad-hoc composition by making implicit contracts explicit. Runtime enforcement is a Phase 4+ concern.

### 4. The Non-Vacuity Principle as the Journal's Contribution

The journal's deepest contribution to the ecosystem isn't new content kinds — it's the **non-vacuity principle** applied systematically:

- **Gates:** N tests ran, N > 0, all passed (not just "tests passed")
- **Checkpoints:** At least one `completed` or `remaining` item (not empty arrays)
- **Manifests:** Required description fields must contain non-trivial values
- **Journal writes:** Every write must contain substantive content

This principle — consensus across all three proposals and all three critics — should be codified in the journal skill as a governing constraint for all journal operations.

### 5. WorkingMemory as Checkpoint Fallback, Not Parallel System

Post-checkpoint, `WorkingMemoryContext` becomes the fallback for sessions without checkpoints, not a parallel concept. The checkpoint captures everything working memory captures and more. The migration path:

1. Phase 0-1: Working memory operates as-is
2. Phase 2: Checkpoints ship. Working memory is auto-loaded only when no active checkpoint exists
3. Future: Evaluate whether working memory can be fully replaced by checkpoints. If so, deprecate gracefully

## Unresolved Questions

### 1. Gate Enforcement Depth

Prompt instructions are the only enforcement mechanism. The debate surfaced but didn't resolve whether this is sufficient. Options on the table:

- **Prompt only** (current proposal): Rely on strong imperative language in skill markdown
- **Hook reinforcement** (Ronacher's pattern): Inject reinforcement messages when expected verification doesn't occur
- **CI integration** (infrastructure-level): Pre-commit hooks or similar that enforce gate execution

The prompt-only approach should ship first. If agent compliance proves insufficient, hook reinforcement is the next escalation.

### 2. Checkpoint-to-Checkpoint Lineage

When Session 2 reads Session 1's checkpoint, does work, then writes its own — should the new checkpoint reference the old one? This enables a resumption lineage graph but adds complexity. The checkpoint schema includes an optional `supersedes` field for within-session chains, but cross-session lineage (`continued_from_checkpoint?`) needs evaluation against real usage patterns before committing to schema.

### 3. Multi-Agent Checkpoint Merging

When PATCH agents each checkpoint, how does the coordinator merge their state? Three options were identified:

- Coordinator reads all and synthesizes manually
- A `journal read checkpoint merge` command produces a unified view
- STRAND completion reports serve as the merge mechanism

None were evaluated. This is a Phase 2+ concern that should be addressed when switchboard integration with checkpoints is designed.

### 4. The Category Error Question

The Composition-Critic's deepest challenge — that skills are cognitive protocols, not functions — wasn't resolved by the debate. Manifests work around it (documentation, not enforcement). But the fundamental question persists: **can prose reasoning be meaningfully typed?**

DSPy says yes (signatures work). But DSPy's signatures constrain LLM *generation* — our manifests would need to constrain LLM *interpretation of Markdown prompts*, which is a different and harder problem. This question gates whether Phase 4 (artifact bus + pipelines) ever activates.

### 5. Context Budget Ceiling

The premortem panel suggested <5% of available context for framework overhead (~650 tokens for checkpoint + gates + manifests). Nobody validated this number, proposed a monitoring mechanism, or defined what happens when the ceiling is breached. This needs instrumentation before it can become policy.

### 6. Checkpoint Quality Signal

Self-reported checkpoints inherit the agent's blind spots (Gates-Critic). The Resume Gate validates structural properties (branch exists, files exist) but cannot validate semantic quality (are the `remaining` items actually the right next steps? are the `failed_approaches` accurately attributed?). No mechanism for checkpoint quality assurance was proposed beyond skill protocol guidance. This may be an inherent limitation of agent-written artifacts.

---

## Summary Table

| Phase | What Ships | ContentKinds | Effort | Dependencies |
|-------|-----------|--------------|--------|--------------|
| **0** | Journal simplification | 7 (drop Observation) | Medium | None |
| **1a** | Verification gates (markdown) | 7 | Low | Phase 0 |
| **1b** | Skill manifests (frontmatter) | 7 | Low | None |
| **2** | Context checkpoints + Resume Gate | 8 (+Checkpoint) | Medium | Phase 0, 1a |
| **3** | Gate journaling (structured notes) | 8 | Low | Phase 1a, 2 |
| **4** | Artifact bus + pipelines (deferred) | 9 (+Artifact) | Med-High | Phase 1b, 2 |

**Exit ramps built in at every phase:**

- If gates-as-instructions provide 80% of verification value → defer Phase 3
- If manifests don't improve composition in practice → don't activate Phase 4
- If checkpoints are sufficient for cross-session continuity → Artifact kind is never needed

---

*Synthesized from: 3 research reports (66 cited sources), 3 proposals, 1 premortem panel (3 rounds, 3 critics), Round 1 adversarial critique, and the original Ronacher analysis.*
*2026-02-19*
