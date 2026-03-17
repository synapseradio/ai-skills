---
name: runbook
description: >-
  This skill should be used when the user asks to "create a runbook",
  "set up an autonomous loop", "implement this feature on a loop",
  "build this out autonomously", "start a hardening pass", "run a
  refactoring loop", "start a research sweep", "focus on X and loop",
  "runbook", "set up a cron loop", or when the user wants to decompose
  a task, initiative, or project into a steerable autonomous workflow.
  Also triggers on: FOCUS.md, autonomous loop, or any request to set up
  recurring agent-driven work — whether building, implementing,
  hardening, refactoring, or exploring.
---

# Runbook

Facilitate a structured alignment conversation, then produce the artifacts
that seed an autonomous loop. The conversation surfaces intent; the
artifacts encode it for unattended execution.

## Two Phases

Track progress through alignment, gate check, seeding, and deployment
using available task tracking tools.

**Phase 1 — Alignment.** Open-ended dialogue to decompose the user's intent
into a concrete lens: what the loop looks for, what authority it consults,
what scope it covers, and what success looks like.

**Phase 2 — Seeding.** Produce three files (FOCUS.md, TASKS.md, LEARNINGS.md)
and a loop prompt. Optionally deploy via CronCreate.

## Context Loading

Load references only when the current phase needs them.

| Phase | Load | Do NOT Load |
|-------|------|-------------|
| Alignment | `references/alignment-guide.md` | seeding-guide, loop-prompt, checklist |
| Gate check | `references/checklist.md` | alignment-guide, seeding-guide |
| Seeding | `references/seeding-guide.md`, `references/loop-prompt.md` | alignment-guide, checklist |

## Phase 1: Alignment

Load `references/alignment-guide.md` and follow its protocol.

The alignment conversation surfaces seven elements:

1. **What** — the work, decomposed to the level where a single lens applies
2. **Why** — the motivation, so discovery can prioritize
3. **Lens** — what the loop looks for or builds toward (feature requirements, style compliance, design improvements, security, performance, migration targets)
4. **Authority** — what reference the loop consults (a PRD, design spec, style guide, issue tracker, architecture doc)
5. **Scope** — directories, files, or areas in and out of bounds
6. **Success** — what "done" looks like, concretely
7. **Mode** — tight loop (default) or recursive decomposition (opt-in)

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
2. **Checklist gates.** Load `references/checklist.md`. Validate every gate.
   Present pass/fail to the user.
3. **Explicit approval.** Halt and request confirmation before seeding.
   Never seed without the user's "go."

## Phase 2: Seeding

Load `references/seeding-guide.md` and `references/loop-prompt.md`.

Produce the following artifacts in the project root (or a user-specified directory):

### Tight loop output

| File | Purpose | Who writes it |
|------|---------|--------------|
| `FOCUS.md` | Lens, authority, scope, success criteria | This skill, during seeding |
| `TASKS.md` | Empty board skeleton (`## Open / ## In Progress / ## Done`) | This skill, during seeding |
| `LEARNINGS.md` | Empty, append-only memory | This skill, during seeding |
| Loop prompt | Customized from `references/loop-prompt.md` with this runbook's lens | This skill, presented to user |

### Recursive decomposition output (additionally)

| File | Purpose |
|------|---------|
| Child `FOCUS.md` files | One per sub-lens, scoped tighter than the parent |
| Parent `FOCUS.md` | References children, defines aggregation strategy |

### Deployment

Present the loop prompt and offer deployment options:
- Deploy now via CronCreate (specify interval)
- Save to a file for manual use
- Display for copy-paste

## Rules

1. **Alignment is a conversation, not a form.** Explore, reflect, let the
   user correct. Do not interrogate with a checklist upfront.
2. **Never seed without explicit approval.** Checklist gates are necessary
   but not sufficient. The user's confirmation is the hard stop.
3. **Default to tight loop.** Only propose recursive decomposition when
   sub-problems are clearly independent.
4. **LEARNINGS.md is append-only.** The loop writes, the user reads. Never
   overwrite or delete entries.
5. **Scope belongs in FOCUS.md, not the prompt.** Keep the loop prompt
   generic. Keep specifics in the lens file.
6. **Resist adding machinery.** If something can be a line in FOCUS.md
   instead of a feature in the prompt, put it in FOCUS.md.

## Additional Resources

### Reference Files

- **`references/alignment-guide.md`** — Conversation protocol for Phase 1:
  decomposition techniques, question patterns, visualization approaches
- **`references/checklist.md`** — Structured gate validating alignment
  completeness before seeding
- **`references/seeding-guide.md`** — Artifact templates and production
  instructions for FOCUS.md, TASKS.md, LEARNINGS.md
- **`references/loop-prompt.md`** — The autonomous loop prompt template,
  customizable per runbook
