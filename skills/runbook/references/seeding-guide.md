# Seeding Guide

Produce the artifacts that drive the autonomous loop from the alignment output.

## Artifact Overview

| File | Purpose | Written by | Read by |
|------|---------|-----------|---------|
| `FOCUS.md` | Lens, authority, scope, success criteria | This skill | The loop prompt (discovery phase) |
| `TASKS.md` | Task board — Open / In Progress / Done | This skill (skeleton) | The loop prompt (every cycle) |
| `LEARNINGS.md` | Append-only memory across cycles | The loop (after each task) | The loop (during discovery) |
| Loop prompt | The autonomous execution prompt | This skill (from template) | CronCreate or manual use |

## FOCUS.md Template

```markdown
# Focus

## Lens
{{One sentence describing what the loop looks for or builds toward.}}

## Authority
{{Named reference the loop consults — a file path, URL, or specification.}}

## Scope

### In
{{Directories, file patterns, or areas to include.}}

### Out
{{Directories, file patterns, or areas to exclude.}}

## Verification
{{How to confirm a task is done. Examples: "test-first — write a failing
test, then implement", "existing tests pass after each change",
"output matches the spec in docs/api-spec.md", "builds clean with no
new warnings".}}

## Success
{{Observable condition for convergence. When this is true, the loop
stops discovering.}}
```

### Customization notes

- **Lens** must be specific enough that a subagent with no prior context
  can act on it. "Improve the code" is too vague. "Implement all endpoints
  defined in docs/api-spec.md" is actionable. "Migrate class components
  to hooks in src/legacy/" is actionable.
- **Authority** should be something the loop can look up or read. A local
  file path works. A URL works. A well-known specification name works
  (the loop will look it up). "Best practices" does not.
- **Scope/In** can use glob patterns: `src/**/*.tsx`, `cmd/`, `packages/core/`.
- **Scope/Out** should include anything that must not be modified: generated
  files, dependencies, stable infrastructure the lens doesn't apply to.
- **Verification** tells the loop how to prove each task is done. This varies
  by lens: test-first for implementation, spec-match for features, linter-clean
  for style work, visual review for design. If omitted, the loop defaults
  to test-first for code changes.
- **Success** must be evaluable by the loop. "All spec endpoints implemented
  and tested" works. "Two consecutive clean audit rounds" works. "Code
  feels better" does not.

## TASKS.md Template

```markdown
# Task Board

## Open

## In Progress

## Done
```

No pre-populated tasks. The loop's discovery phase populates the board.

## LEARNINGS.md Template

```markdown
# Learnings

Append-only. Each entry records what the loop learned during a completed task.
```

No pre-populated entries. The loop appends after each task.

## Recursive Decomposition (when mode = recursive)

### Parent FOCUS.md

Add a `## Children` section listing child focus files:

```markdown
# Focus

## Lens
{{Parent-level lens — broader than any single child.}}

## Authority
{{Parent-level reference.}}

## Children

| Child | Focus file | Scope |
|-------|-----------|-------|
| Auth module | `focus/auth.md` | src/auth/ |
| Data layer | `focus/data.md` | src/models/, src/db/ |
| API routes | `focus/routes.md` | src/routes/ |

## Aggregation
{{How child outcomes combine. Example: "Parent is done when all children
report convergence."}}

## Success
{{Parent-level convergence condition.}}
```

### Child FOCUS.md files

Each child follows the same template as a tight-loop FOCUS.md but with
tighter scope. Place them in a `focus/` subdirectory.

Each child gets its own TASKS.md and LEARNINGS.md in its scope directory,
or shares the parent's board with task prefixes (e.g., `[security] T1: ...`).

Prefer separate boards when children run concurrently. Prefer a shared board
when children run sequentially.

## Loop Prompt Production

Load `references/loop-prompt.md` for the template. Customize by replacing
the discovery section's hardcoded lens with a FOCUS.md reference:

```
Read FOCUS.md for the current lens, authority, and scope.
Read LEARNINGS.md for context from prior cycles.
```

Present the complete prompt to the user. Offer three deployment options:

1. **Deploy now** — invoke CronCreate with a user-specified interval
2. **Save to file** — write to a location the user chooses
3. **Display only** — show for copy-paste, do not write

Always confirm deployment before invoking CronCreate.

## Post-Seeding Summary

After producing all artifacts, present a summary:

```
Runbook seeded:
  FOCUS.md    — [lens summary]
  TASKS.md    — empty board (loop will populate via discovery)
  LEARNINGS.md — empty (loop will append after each task)
  Loop prompt — [deployment choice]

Mode: [tight loop / recursive with N children]
```
