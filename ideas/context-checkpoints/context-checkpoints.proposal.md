---
status: accepted
priority: 2
created: 2026-02-19
source: Ronacher analysis + landscape research
research: research/context-checkpoints.research.md
synthesis: ../ronacher-synthesis.md
---

# Context Checkpoints: Journal as Session Resumption Protocol

## Summary

Transform the journal plugin from a recording tool into a continuity tool by adding **context checkpoints** — structured resumption artifacts that let a fresh agent session pick up exactly where the previous one left off. Checkpoints unify three existing but uncoordinated journal primitives (working memory, session close, session notes) into a single purpose-built content type optimized for cross-session continuity.

No existing tool treats structured journaling as a first-class continuity mechanism ([research §3](research/context-checkpoints.research.md#3-journal-as-continuity-structured-logging-as-session-bridge)). This proposal fills that gap.

## Background

### The Problem

Agents operating in long sessions face **context rot** — failed attempts, undone changes, and exploratory detours accumulate in the context window, degrading decision quality. Ronacher observes: "If you ever get to the point where you have to compact, you're kind of lost" (P1: Context Quality > Model Capability).

The current workaround is to abort and start fresh. But fresh sessions lose accumulated understanding: which files were explored, what approaches failed and why, what the plan is, what state the implementation reached. This is the **continuity gap** — the space between what was known and what must be reconstructed.

### What Research Reveals

The landscape research ([full report](research/context-checkpoints.research.md)) surfaces five key findings:

1. **Industry is converging on three-tier memory** — static instruction files + dynamic auto-memory + session summaries — but no tool treats the session bridge as a structured, schema-enforced artifact. Claude Code's session summaries are automated but lossy. Cline's Memory Bank is structured but requires manual triggers. Windsurf's auto-memories lack schema. ([§1](research/context-checkpoints.research.md#1-session-continuity-patterns-across-ai-coding-agents))

2. **State ≠ Memory** — "Memory is what you know. State is what you know plus what you're doing and where you are in doing it" ([Brenndoerfer](https://mbrenndoerfer.com/writing/understanding-the-agents-state)). Existing continuity tools capture memory (what happened) but not state (what to do next, where in the process, what's blocking progress). A checkpoint must capture state.

3. **Manus's todo.md pattern validates journal-as-continuity** — Manus deliberately "recites objectives into the end of the context" via a file the agent writes and reads to maintain coherence across ~50 tool calls ([Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)). This is journaling-as-continuity in production, not logging-for-record.

4. **Simple beats complex for context management** — JetBrains Research found that simple observation masking matched or slightly beat LLM summarization at 52% lower cost ([The Complexity Trap](https://blog.jetbrains.com/research/2025/12/efficient-context-management/)). LLM summarization led agents to run 15% longer, suggesting summaries can mask signals the agent should stop. Implication: checkpoints should be explicit structured data, not LLM-generated summaries.

5. **LangGraph is the only mature checkpoint system**, supporting graph state snapshots, time travel, and human-in-the-loop modification ([LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)). But LangGraph checkpoints are stateful (require identical runtime environment). Agents in Claude Code always start fresh — we need **stateless checkpoints** that enable portable reconstruction.

### Current State in Journal Plugin

The journal already has three proto-checkpoint mechanisms:

| Primitive | What it captures | Gap |
|-----------|-----------------|-----|
| `WorkingMemoryContext` | Current focus, active tasks, open questions, next steps | Captures attention state, not resumption state. Missing: what was completed, what failed, project state, orientation files. |
| Session close (`_closing` entry) | Summary, lessons, unresolved, successor | Captures completion narrative, not continuity instructions. Written for reflection, not for a fresh agent to act on. |
| `JournalConfig.session_start.load_working_memory` | Auto-loads working memory on session start | Loads the wrong artifact — working memory is attention state, not resumption state. |

These are separate, uncoordinated writes. No single artifact captures the full resumption state. The checkpoint protocol unifies them.

## Proposal

### What: Checkpoint as First-Class Content Type

Add `ContentKind.Checkpoint` as a new journal content kind — the agent's structured letter to its future self. A checkpoint is purpose-built for a fresh context to pick up where the previous one left off.

**A checkpoint is not:**

- A session (which is a container for notes over time)
- Working memory (which captures current attention)
- A session close (which captures a completion narrative)
- A summary (which compresses history)

**A checkpoint is:**

- A resumption instruction set written by the agent, for the agent
- Structured data with required fields that ensure nothing critical is omitted
- Minimal — only what the next session needs, not everything the current session learned
- Actionable — it describes what to do next, not what happened

### How: Design

#### 1. CheckpointData Schema

```typescript
interface CheckpointData {
  /** Session this checkpoint belongs to */
  session_id: string;

  /** High-level task description */
  task: string;

  /** Checkpoint lifecycle: active (current), superseded (newer exists), resolved (task done) */
  status: 'active' | 'superseded' | 'resolved';

  /** What has been accomplished — the foundation the next session builds on */
  completed: string[];

  /** What remains — ordered by priority, each item actionable */
  remaining: string[];

  /** Approaches that failed and why — prevents the next session from repeating them */
  failed_approaches: Array<{
    approach: string;
    reason: string;
  }>;

  /** Decisions made that constrain future work — the "why" behind choices */
  decisions: string[];

  /** Files the next session should read first — orientation for fastest ramp-up */
  orientation_files: string[];

  /** Current project state — branch, test status, blocking issues */
  project_state: {
    branch?: string;
    tests_passing?: boolean;
    blocking_issue?: string;
    [key: string]: unknown;
  };

  /** Sequence number — monotonically increasing within a session's checkpoint chain */
  sequence: number;

  /** Previous checkpoint ID, if this supersedes one */
  supersedes?: string;
}
```

**Design rationale:**

- **`completed` + `remaining`** replaces the session close's `summary` + `unresolved`. These are action-oriented, not narrative. A fresh agent can parse them and immediately understand scope.
- **`failed_approaches`** is the most novel field. Manus's research shows preserving errors in context enables implicit belief updating — the next session won't repeat what already failed. No existing continuity tool captures this systematically.
- **`decisions`** captures constraints that aren't visible in code. "Using Redis for session store" or "Token expiry is 24h" — these are architectural decisions that the next session needs but won't find in any file.
- **`orientation_files`** directly addresses the cold-start problem. Instead of the agent exploring the codebase, it reads 3-5 files and has immediate context. This aligns with Anthropic's advice to find "the smallest set of high-signal tokens" ([context engineering guide](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).
- **`project_state`** captures environment state that transcends the journal — branch name, whether tests pass, what's blocking. This bridges the gap between journal knowledge and filesystem reality.
- **`sequence`** enables checkpoint chains within a session. A session that checkpoints multiple times produces a sequence: checkpoint-1, checkpoint-2, checkpoint-3. Only the latest is `active`; previous ones are `superseded`.

#### 2. Storage

```
.claude/.thinkies/.checkpoints/
├── auth-refactoring.yaml         # Active checkpoint for session
├── auth-refactoring--2.yaml      # Superseded (sequence 2, superseded by 3)
└── perf-investigation.yaml       # Another active checkpoint
```

Checkpoints are stored in `.checkpoints/` alongside existing content directories (`.notes/`, `.context/`, `.reflections/`, etc.). Each checkpoint file is a `Document<CheckpointData>` using the existing document envelope with automatic metadata management.

**Naming convention:** `{session-id}.yaml` for the latest checkpoint. When a new checkpoint supersedes the previous one, the old file is renamed to `{session-id}--{sequence}.yaml` and marked `superseded`.

#### 3. CLI Commands

**Write checkpoint:**

```bash
journal write checkpoint \
  --session auth-refactoring \
  --data '{
    "task": "Migrate auth module from JWT to session tokens",
    "completed": ["Identified all JWT usage sites (14 files)", "Created session token schema"],
    "remaining": ["Convert middleware/auth-guard.ts", "Update tests"],
    "failed_approaches": [{"approach": "Cookie-based sessions", "reason": "Mobile clients unreliable"}],
    "decisions": ["Using Redis for session store", "Token expiry 24h, refresh window 1h"],
    "orientation_files": ["src/auth/session-store.ts", "src/middleware/auth-guard.ts"],
    "project_state": {"branch": "feat/session-tokens", "tests_passing": false}
  }'
```

The write command:

1. Validates against `CheckpointData` schema
2. If an active checkpoint exists for this session, supersedes it (bumps sequence)
3. Writes the new checkpoint as `active`
4. Adds a checkpoint note entry to the session (with `_checkpoint: true` marker)
5. Updates working memory context to stay in sync (backward compatibility)

**Read checkpoint (resume):**

```bash
journal read checkpoint                          # Most recent active checkpoint
journal read checkpoint show <session-name>      # Specific session's checkpoint
journal read checkpoint list                     # All active checkpoints
journal read checkpoint --format json            # Machine-readable for hooks
```

The read command returns the checkpoint formatted for agent consumption — a structured block that can be injected into a fresh session's context.

**Resolve checkpoint (task complete):**

```bash
journal write checkpoint resolve --session auth-refactoring
```

Marks the checkpoint as `resolved` and optionally triggers session close.

#### 4. Session Start Integration

The checkpoint becomes the **primary resumption artifact** at session start, superseding raw working memory. The load order:

```
Session Start:
  1. Load CLAUDE.md (static instructions)
  2. Load active checkpoint, if one exists ← NEW, highest priority
  3. Load working memory context (fallback if no checkpoint)
  4. Surface recent sessions (existing behavior)
```

The `JournalConfig` gains a new field:

```typescript
interface JournalConfig {
  session_start: {
    // ... existing fields ...
    /** Load active checkpoint as primary resumption context (default: true) */
    load_checkpoint: boolean;
  };
}
```

When `load_checkpoint` is true and an active checkpoint exists, the hook outputs the checkpoint in a structured format that the agent can immediately act on — task, remaining items, orientation files, and project state.

#### 5. Checkpoint Protocol in Skills

The checkpoint isn't just a data type — it's a protocol. The journal skill's content-types reference gains a new section:

**When to checkpoint:**

- Context is running low and work is incomplete
- Shifting to a different task mid-session (task switching)
- Reaching a natural boundary (phase complete, subtask done)
- Before ending a long session with open work

**What makes a good checkpoint:**

- **Minimal:** A checkpoint that occupies 500 tokens is better than one occupying 2,000. Every token competes for attention in the next session (Ronacher P1).
- **Actionable:** `remaining` items should be specific enough to execute. "Fix auth" is bad; "Convert middleware/auth-guard.ts to use session store instead of JWT validation" is good.
- **Honest about failures:** `failed_approaches` prevents the next session from wasting context on paths already explored. This is the checkpoint's unique contribution to continuity.
- **Oriented:** `orientation_files` should be the 3-5 files that give the fastest ramp-up. Not every file touched — just the ones that unlock understanding.

### Why This Approach

1. **Builds on existing infrastructure.** The journal already has document envelopes, YAML storage, content kinds, graph traversal, session lifecycle, and hook integration. Checkpoints extend this — they don't reinvent it.

2. **Fills a genuine gap in the landscape.** No existing tool provides structured, schema-enforced, agent-written resumption artifacts. Cline's Memory Bank is the closest but lacks the failed-approaches and orientation-files fields that make checkpoints actionable.

3. **Respects the Complexity Trap.** The checkpoint is structured data, not LLM-generated summaries. The agent writes it deliberately, choosing what to include. JetBrains' research warns that automated summarization can mask stopping signals — explicit checkpointing avoids this.

4. **Stateless by design.** Agents always start fresh in Claude Code. Checkpoints are portable, reconstructive artifacts — they don't depend on runtime state. This aligns with the "one session per task" pattern while solving its continuity problem.

5. **Compatible with multi-agent workflows.** Switchboard's PATCH workspaces can each have their own checkpoint. When a STRAND completes, its agent checkpoints before the workspace is merged. The coordinator can read all checkpoints to understand multi-agent state.

## Alternatives Considered

### Alternative 1: Evolve WorkingMemoryContext (minimal change)

Expand the `WorkingMemoryContext` schema to include checkpoint-grade fields (completed, remaining, failed_approaches, orientation_files, project_state) without adding a new content kind.

**Why not chosen:** Working memory has different semantics — it captures *what you're attending to right now*, not *what a fresh agent needs to continue*. Overloading it conflates two distinct concepts. The journal's type system is built on clear content kind distinctions (sessions vs. notes vs. insights vs. reflections). A checkpoint is a distinct cognitive artifact that deserves its own kind.

### Alternative 2: Checkpoint as a special session close

Extend the session close command to optionally emit a checkpoint-grade closing entry (with all the resumption fields) that the next session reads.

**Why not chosen:** Session close is a terminal operation — it marks a session as `completed`. But checkpointing happens mid-work. A session that checkpoints three times before completing would need to "close" and "reopen" repeatedly, breaking the session lifecycle model. Checkpoints are in-progress artifacts; closes are completion artifacts.

### Alternative 3: External checkpoint file (`.claude/checkpoints/`)

Store checkpoints outside the journal system in a dedicated `.claude/checkpoints/` directory, similar to Gemini CLI's approach.

**Why not chosen:** This fragments the journal's graph. Checkpoints reference sessions, sessions reference checkpoints — if they're in different systems, the graph traversal (backlinks, ego graphs, health checks) can't see the relationships. Keeping checkpoints in the journal preserves the unified content graph.

## Integration Points

### Software Plugin

| Skill | Integration |
|-------|-------------|
| `/understand` | At phase completion, suggest writing a checkpoint. If resuming, load checkpoint before mapping territory. |
| `/implement` | When implementation spans multiple sessions, checkpoint between phases (e.g., after "identify sites" before "convert files"). The verification gates proposal (if adopted) provides natural checkpoint boundaries. |
| `/change-safely` | Checkpoint before large refactors — capture the plan, completed files, remaining files, and approach decisions. |

**Mechanism:** Software skills add checkpoint awareness to their protocols. When a skill detects it's resuming work (active checkpoint exists for this task), it reads the checkpoint before starting. When a skill reaches a natural boundary, it suggests checkpointing.

### Switchboard Plugin

| Concept | Integration |
|---------|-------------|
| PATCH workspaces | Each PATCH agent can maintain its own checkpoint. The coordinator reads agent checkpoints to understand multi-agent progress. |
| STRAND work units | A STRAND's completion triggers a checkpoint of the agent's state. If the STRAND fails and needs retry, the checkpoint prevents duplicate work. |
| Flow phases | Phase transitions in a flow are natural checkpoint boundaries. The flow engine can require checkpoints between phases. |

**Mechanism:** Switchboard's flow definition gains an optional `checkpoint: true` field on phase transitions. When set, the flow engine invokes `journal write checkpoint` before transitioning.

### Expression Plugin

Checkpoints are agent-written but human-readable. Expression's `/proofread` and `/refine` skills could optimize checkpoint text for clarity — ensuring that `remaining` items are precise, `decisions` are unambiguous, and `failed_approaches` explanations are useful.

### Thinkies Plugin

| Skill | Integration |
|-------|-------------|
| `/decompose` | Produces task breakdowns that map directly to checkpoint `remaining` items. |
| `/strategize` | Multi-session strategies naturally checkpoint between strategy iterations. |
| `/premortem` | Premortem findings can populate checkpoint `decisions` (risk mitigations as constraints). |

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| **Checkpoint bloat** — agents write overly detailed checkpoints that consume excessive context in the next session | Schema enforces array fields (completed, remaining, etc.) with guidance on item count. Skill protocol emphasizes minimality. Token budget guidance: aim for <500 tokens per checkpoint. |
| **Checkpoint staleness** — a checkpoint from 3 days ago references files that have changed | `project_state` includes a `branch` field; the resume hook can detect if the branch has changed since checkpoint creation. `orientation_files` are validated against filesystem at load time — missing files are flagged. |
| **Over-engineering risk** (JetBrains Complexity Trap) — the checkpoint system becomes more complex than the problem it solves | Start with the minimal schema above. No auto-summarization, no LLM-generated fields. The agent writes every field deliberately. Measure: if agents produce better outcomes with checkpoints vs. without, the complexity is justified. |
| **Adoption friction** — agents don't naturally checkpoint without prompting | Hook integration at session end: if session has >5 entries and is still active, prompt for checkpoint. Software skill protocols suggest checkpointing at natural boundaries. The key: make it easy (one command) and valuable (clear resume improvement). |
| **Dual-write overhead** — checkpoint writes also update working memory and session notes, tripling the I/O | The coordinated write is three YAML file operations — fast on local disk. If performance becomes an issue, the session note update can be made optional. |

## Open Questions

### Resolved by Research

| Original Question | Resolution |
|-------------------|------------|
| Can context usage be detected programmatically? | **Partially.** Claude Code's session memory triggers at ~10,000 tokens. But programmatic detection from within a skill is not currently possible. Checkpointing should be explicit (agent or human triggered) with soft prompts at session boundaries. |
| Should checkpoints be in journal or `.claude/checkpoints/`? | **Journal.** Keeping checkpoints in the journal preserves the unified content graph and leverages existing infrastructure (document envelopes, YAML store, graph traversal). |
| Should the schema vary by task type? | **No.** One schema handles all task types. The `project_state` field is extensible (`[key: string]: unknown`) for task-specific data. Debugging tasks use `blocking_issue`; refactoring tasks use branch info; research tasks might add `sources_consulted`. |

### Newly Surfaced

- **Checkpoint-to-checkpoint chaining across sessions.** When Session 2 reads Session 1's checkpoint, does work, then writes its own checkpoint — should the new checkpoint reference the old one? This would enable a resumption lineage graph. Implementation: add optional `continued_from_checkpoint?: string` field.

- **Multi-agent checkpoint merging.** When three PATCH agents each checkpoint, how does the coordinator merge their state into a coherent view? Options: (a) coordinator reads all three and synthesizes, (b) a `journal read checkpoint merge` command produces a unified view, (c) STRAND completion reports serve as the merge mechanism.

- **Checkpoint validation at resume time.** Should the resume hook validate that `orientation_files` still exist, that the `branch` still exists, that the task description matches the current project state? Stale checkpoints could mislead worse than no checkpoint at all. Proposed: lightweight validation that flags issues without blocking resume.

- **Token budget enforcement.** The proposal recommends <500 tokens per checkpoint. Should the CLI enforce this? Options: (a) hard limit with error, (b) soft warning, (c) guidance only. Research favors guidance: agents benefit from flexibility, and the "minimal" principle in the skill protocol is the right lever.

- **Relationship to Claude Code's auto-memory.** Claude Code generates session summaries automatically. How does a checkpoint interact with this? If the checkpoint is richer and more structured, should the skill suggest disabling auto-memory for checkpointed sessions to avoid redundant context? This needs experimentation.

## Request

Feedback sought on:

1. **Schema completeness** — are the checkpoint fields sufficient for resumption, or are critical fields missing?
2. **Integration depth** — should software/switchboard plugins be checkpoint-aware from day one, or should journal stand alone first?
3. **Checkpoint lifecycle** — is `active → superseded → resolved` sufficient, or do we need additional states (e.g., `stale`, `partial`)?
4. **Implementation priority** — should this be the first Ronacher-derived change to ship, given that it addresses the talk's most emphasized pain point (context rot)?

## Synthesis Outcome

**Priority:** #2 of 3. Ships in Phase 2, after journal simplification (Phase 0) and verification gates (Phase 1a).

**Why not first:** The Gates-Critic proved that checkpoints structurally require a Resume Gate to be safe. "Checkpoint loaded successfully" is vacuous without validation that the checkpoint's content matches reality (branch exists, orientation files exist, test state matches). Gates must exist before checkpoints can be trustworthy.

**Key premortem findings that shaped the recommendation:**

1. **Monolithic wins over reference-based.** The Legibility Critic's mediator position was accepted: start monolithic (single coherent struct) and only add reference support if multi-week projects demonstrate the need. Manus validates this — a single `todo.md`, not decomposed files.

2. **Checkpoints should absorb session close.** Bold recommendation from synthesis: a checkpoint IS the modern session close. When work is incomplete → write checkpoint (active). When work is done → resolve checkpoint (resolved). The old close narrative (summary, lessons, unresolved) is subsumed by Reflection as a separate content kind.

3. **`failed_approaches` as context, not constraints.** The Gates-Critic's warning that failed approaches can create false constraints from mis-attributed failures led to a design change: the checkpoint protocol instructs agents to evaluate `failed_approaches` critically, not as absolute constraints.

4. **`project_state` needs validation, not trust.** The Resume Gate validates `project_state` assertions at load time rather than trusting cached booleans. Stale checkpoints are flagged with specific discrepancies.

5. **WorkingMemory becomes checkpoint fallback.** Post-Phase 2, working memory auto-loads only when no active checkpoint exists. Checkpoints capture everything working memory captures and more.

**Design changes from debate:**

- Resume Gate added as a mandatory companion (not optional integration)
- Checkpoint protocol emphasizes `failed_approaches` as advisory context
- `project_state` validation at load time, not blind trust
- Session close collapsed into checkpoint lifecycle
- Schema philosophy resolved: strict core (`task`, `completed`, `remaining`, `status`, `sequence` — fail if missing or trivially empty) + flexible extension (`failed_approaches`, `decisions`, `orientation_files`, additional `project_state` fields, unknown fields accepted)
