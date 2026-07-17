---
name: runbook
description: >-
  Runs in two modes. Seed mode when the user asks to "create a runbook",
  "set up an autonomous loop", "start a hardening pass", "run a refactoring
  loop", "focus on X and loop", "set up a cron loop", mentions FOCUS.md, or
  wants to decompose work into a steerable autonomous workflow — it aligns
  on intent and writes the durable state files. Execute mode when the user
  asks to "run", "continue", or "resume a runbook", to invoke execute mode
  against a directory, or when the named directory already holds FOCUS.md —
  the current session becomes the orchestrator that drives the loop,
  delegating all implementation to subagents. Triggers: create a runbook,
  autonomous loop, hardening pass, refactoring loop, cron loop, run the
  runbook, continue the runbook, resume the runbook, execute mode against a
  directory, FOCUS.md.
compatibility: >-
  Execute mode requires an environment that can delegate to subagents;
  the orchestrator never implements directly. Seeding works everywhere —
  it only holds a conversation and writes files.
---

# Runbook

A runbook decomposes work into a steerable autonomous loop and then runs it.
Seeding facilitates an alignment conversation and writes the durable state
that encodes intent. Executing turns the current session into the
orchestrator that drives the loop from that state.

## Modes

Two modes share this skill. Route to one before doing anything else.

Routing is layered. Apply the explicit signal first; fall back to artifact
presence only when no explicit signal fires.

| Signal | Mode |
|--------|------|
| "execute mode against a directory", "run/continue/resume the runbook" | Execute |
| "create a runbook", "set up an autonomous loop", "start a hardening pass" | Seed |
| No explicit signal, FOCUS.md present in the target directory | Execute |
| No explicit signal, FOCUS.md absent | Seed |

The target directory is the directory the user names. If the user names no
directory, it is the current working directory.

Two ambiguity guards override the table. If artifacts are already present but
the user asks to redesign the runbook, confirm before overwriting anything —
do not silently seed over existing state. If the user asks to execute but no
artifacts are present, there is nothing to run; offer seed mode instead.

## Context Loading

Load references only when the current phase needs them. Each phase loads only
its own file.

| Phase | Load |
|-------|------|
| Alignment | [`references/alignment-guide.md`](references/alignment-guide.md) |
| Gate check | [`references/checklist.md`](references/checklist.md) |
| Seeding | [`references/seeding-guide.md`](references/seeding-guide.md) |
| Execute | [`references/execution-guide.md`](references/execution-guide.md) |

## Phase 1: Alignment

Load [`references/alignment-guide.md`](references/alignment-guide.md) and follow its protocol.

The alignment conversation surfaces seven elements:

1. **What** — the work, decomposed to the level where a single lens applies
2. **Why** — the motivation, so discovery can prioritize
3. **Lens** — what the loop looks for or builds toward (feature requirements, style compliance, design improvements, security, performance, migration targets)
4. **Authority** — what reference the loop consults (a PRD, design spec, style guide, issue tracker, architecture doc)
5. **Scope** — directories, files, or areas in and out of bounds
6. **Success** — what "done" looks like, concretely
7. **Mode** — tight loop (default) or recursive decomposition (opt-in)

The alignment conversation also surfaces behavioral exclusions (no-gos)
and risks as part of the scope and decomposition discussion. These are
not separate elements — they emerge naturally from probing scope
boundaries and hidden risks.

Use inline visualizations, scope diagrams, and AskUserQuestion for structured
choices. Decompose vague intent into specific, testable goals.

### Tight loop vs. recursive decomposition

Most work is a tight loop: one lens, one scope, grind until converged.
This is the default.

Recursive decomposition is opt-in, for work that has independent sub-problems
benefiting from separate lenses. When selected, the parent FOCUS.md seeds
child FOCUS.md files, each scoped tighter. Children report outcomes upward
via LEARNINGS.md. The parent aggregates.

Only propose recursive mode when the problem's structure demands it.

### Exit conditions

Apply all three, in order:

1. **Convergence detection.** Notice when questions stop producing new
   constraints. State this observation explicitly.
2. **Checklist gates.** Load [`references/checklist.md`](references/checklist.md). Validate every gate.
   Present pass/fail to the user.
3. **Explicit approval.** Halt and request confirmation before seeding.
   Never seed without the user's "go."

## Phase 2: Seeding

Load [`references/seeding-guide.md`](references/seeding-guide.md).

Before entering plan mode, ask the user for two things:

- **Target directory** for the artifacts (FOCUS.md, TASKS.md, LEARNINGS.md).
- **Execution route** — attended or unattended. Attended means the invoking
  session runs rounds continuously, emitting a compact per-round summary as
  the steer point. Unattended means a thin scheduled stub starts a fresh
  session that runs exactly one round and stops, with the files carrying all
  state between rounds.

Enter plan mode. Write the plan file following the structure in
[`references/seeding-guide.md`](references/seeding-guide.md). The plan writes only the three durable
artifacts — no loop prompt. The plan file contains:

| Section | Content |
|---------|---------|
| Context | Why this loop exists — motivation and intended outcome |
| FOCUS.md → path | Complete FOCUS.md with all sections populated, including a `Route:` line |
| TASKS.md → path | Empty board skeleton |
| LEARNINGS.md → path | Empty structured memory |
| Execution & Deployment | One-time wiring: the chosen route, and the schedule target if unattended |

Exit plan mode for user review.

Nothing from the alignment conversation survives as conversational
residue in the plan. The plan reads as if written by someone who already
knew the requirements.

## Execute Mode

Precondition: exactly one FOCUS.md in the target directory. A parent FOCUS.md
that carries a `## Children` table is a coordination document, not a runnable
loop — list its children and ask which one to run.

Load [`references/execution-guide.md`](references/execution-guide.md) and follow its protocol. The
orchestrator never implements directly. All implementation, discovery, and
side-effect work is delegated to subagents. If the environment cannot
delegate to subagents, stop and tell the user — never fall back to
implementing the work yourself.

Read the route from FOCUS.md's `Route:` line. If the line is absent, treat
the route as attended. Keep each round cheap: re-read TASKS.md and the
LEARNINGS.md Summary section only, per round.

## Rules

### Seeding rules

1. **Alignment is a conversation, not a form.** Explore, reflect, let the
   user correct. Do not interrogate with a checklist upfront.
2. **Never seed without explicit approval.** Checklist gates are necessary
   but not sufficient. The user's confirmation is the hard stop.
3. **Conversation content is ephemeral.** Explanations, diagrams, and
   AskUserQuestion interactions from Phase 1 do not appear in the plan
   file. The plan stands alone.
4. **Default to tight loop.** Only propose recursive decomposition when
   sub-problems are clearly independent.
5. **LEARNINGS.md is append-only.** The loop writes, the user reads. Never
   overwrite or delete entries.
6. **Scope belongs in FOCUS.md, not machinery.** Keep specifics in the lens
   file, not in the execution protocol.
7. **Resist adding machinery.** If something can be a line in FOCUS.md
   instead of a feature in the protocol, put it in FOCUS.md.

### Execute rules

1. **The orchestrator never implements.** Delegate all implementation,
   discovery, and side-effect work to subagents.
2. **State lives in files, not conversation.** Every round re-reads FOCUS.md,
   TASKS.md, and the LEARNINGS Summary fresh. A restart resumes cleanly.
3. **One task per round.** After a task resolves, the round ends.
4. **Revert on failure.** Return a failed task to Open with a note and never
   fix it in the same round.
5. **The route governs the driver.** Unattended runs one round and stops;
   attended runs continuously with a per-round summary as the steer point.

## Additional Resources

### Reference Files

- **[`references/alignment-guide.md`](references/alignment-guide.md)** — Conversation protocol for Phase 1:
  decomposition techniques, question patterns, visualization approaches
- **[`references/checklist.md`](references/checklist.md)** — Structured gate validating alignment
  completeness before seeding
- **[`references/seeding-guide.md`](references/seeding-guide.md)** — Artifact templates and production
  instructions for FOCUS.md, TASKS.md, LEARNINGS.md
- **[`references/execution-guide.md`](references/execution-guide.md)** — The execute-mode protocol: round
  lifecycle, delegation briefs, the placement framework, and convergence
