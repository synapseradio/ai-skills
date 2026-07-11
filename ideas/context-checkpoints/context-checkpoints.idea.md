---
status: proposing
created: 2026-02-18
source: Ronacher "Agentic Coding" talk analysis
---

# Context Checkpoints: Journal as Session Resumption Protocol

## Problem

Agents operating in long sessions face **context rot** — failed attempts, undone changes, and exploratory detours accumulate in the context window, degrading decision quality. Ronacher observes: "If you ever get to the point where you have to compact, you're kind of lost." Compaction destroys the coherent narrative of what was tried, what succeeded, and what the agent needs to know to continue.

The current workaround is to abort and start fresh when context runs low. But starting fresh means the agent loses all accumulated understanding — which files it explored, what approaches failed and why, what the architectural plan is, what state the implementation reached.

**Journal already persists structured data across sessions.** The missing piece: a protocol for the agent to write a *resumption checkpoint* — not a full history, but a minimal, structured artifact that lets a fresh session pick up where the last one left off.

## Core Concept

A **context checkpoint** is a structured journal entry that captures exactly what a fresh agent session needs to continue work. It is:

1. **Minimal** — only what the agent needs, not everything it learned. Context is zero-sum (Ronacher P1); the checkpoint itself competes for attention in the new session.
2. **Structured** — not free-form notes, but a schema with required fields that ensure nothing critical is omitted.
3. **Actionable** — the checkpoint doesn't describe history; it describes *next steps* with enough context to execute them.

The workflow:

```
Session 1: Working → Context running low → Write checkpoint → End session
Session 2: Read checkpoint → Resume work → Write checkpoint → End session
Session N: Read checkpoint → Complete work → Archive checkpoint
```

This turns the journal from a *recording* tool into a *continuity* tool.

### Checkpoint Schema (Draft)

```yaml
type: context-checkpoint
task: "Migrate auth module from JWT to session tokens"
status: in-progress
completed:
  - "Identified all JWT usage sites (14 files)"
  - "Created session token schema in db/migrations/003"
  - "Converted auth/login.ts and auth/refresh.ts"
remaining:
  - "Convert middleware/auth-guard.ts (depends on session store)"
  - "Convert 11 remaining consumer files"
  - "Update tests (auth.test.ts, middleware.test.ts)"
current_state:
  branch: "feat/session-tokens"
  last_file_modified: "src/auth/refresh.ts"
  tests_passing: false
  blocking_issue: "session store interface not finalized"
context:
  - "Using Redis for session store (decision made in session 1)"
  - "Token expiry is 24h, refresh window is 1h"
  - "Old JWT tokens must remain valid for 7 days (migration period)"
failed_approaches:
  - approach: "Tried cookie-based sessions first"
    reason: "Mobile clients can't use cookies reliably"
files_to_read_first:
  - "src/auth/session-store.ts"
  - "src/middleware/auth-guard.ts"
  - "db/migrations/003-session-tokens.sql"
```

### Integration with Existing Infrastructure

- **Journal plugin** provides persistence and metadata management
- **Software plugin** `/plan` and `/implement` could emit checkpoints at natural boundaries
- **Switchboard** PATCH workspaces could checkpoint between iterations

## Initial Thoughts

- The checkpoint is the agent's *letter to its future self*. The agent writes it, not the human — the agent knows what it tried and what mattered.
- Trigger checkpoints explicitly (when the agent or human says "checkpoint") or automatically (when context usage exceeds a threshold, if detectable).
- The schema should be strict enough to be useful but flexible enough for different task types (debugging, feature implementation, refactoring, research).
- Reading a checkpoint should be the *first thing* a new session does — before reading CLAUDE.md, before exploring the codebase.

## Open Questions

- [ ] Can context usage be detected programmatically to trigger automatic checkpointing? Or is this always a manual decision?
- [ ] Should checkpoints be stored in journal (cross-session persistence) or in a dedicated `.claude/checkpoints/` directory (project-scoped)?
- [ ] How does this interact with switchboard's PATCH model? Is a PATCH workspace state already a checkpoint?
- [ ] Should the checkpoint schema vary by task type, or is one schema sufficient?
- [ ] How do we handle checkpoint staleness — a checkpoint from 3 days ago may reference files that have changed?
- [ ] Could this integrate with hooks to auto-checkpoint on session end?
