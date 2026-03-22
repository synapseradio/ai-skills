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

## Convergence
{{When to stop discovering. Examples: "Two consecutive discovery rounds
with zero findings", "All items in the spec accounted for",
"Task yield below 1 for 3 cycles". If omitted, the loop stops only
when discovery finds nothing and success criteria are met.}}

## Principles
<!-- Optional. 3-5 constraints the loop must not violate, regardless of
what discovery finds. Examples: "No change without a test first",
"Do not modify public API signatures",
"Preserve backward compatibility with v2 clients". -->

## Model
{{Default model tier for this loop's tasks. One of: mechanical, contextual,
architectural. Discovery tags each task with a tier; the PM maps tiers to
models at delegation time.

Tier guidance (based on task signals, not rigid categories):

| Signal              | mechanical           | contextual               | architectural              |
|---------------------|----------------------|--------------------------|----------------------------|
| Scope of change     | Single location      | Multiple related files   | Cross-cutting, system-level |
| Ambiguity           | None — fully specified | Low — clear spec exists | High — requires design judgment |
| Design intent needed | None                 | Local patterns           | System-level understanding  |
| Verification        | Does it compile/lint? | Do tests pass?           | Does the design hold?       |

Default: contextual. Override per-task when signals indicate otherwise.}}
```

### Customization notes

- **Lens** must be specific enough that a subagent with no prior context
  can act on it. "Improve the code" is too vague. "Implement all endpoints
  defined in docs/api-spec.md" is actionable. "Migrate class components
  to hooks in src/legacy/" is actionable.
- **Authority** should be something the loop can look up or read. A local
  file path works. A URL works. A well-known specification name works
  (the loop will look it up). "Best practices" does not.
- **Scope/In** can use glob patterns: `src/**/*.py`, `lib/`, `packages/core/`.
- **Scope/Out** should include anything that must not be modified: generated
  files, dependencies, stable infrastructure the lens doesn't apply to.
- **Verification** tells the loop how to prove each task is done. This varies
  by lens: test-first for implementation, spec-match for features, linter-clean
  for style work. Verification must produce an external, observable signal —
  a test pass/fail, build output, lint result, or type-check. LLM
  self-assessment is not verification. No change ships without a test
  contract first. If no automated verification exists for the lens, the
  loop's first task is to create one. If omitted, the loop defaults to
  test-first.
- **Success** must be evaluable by the loop. "All spec endpoints implemented
  and tested" works. "Two consecutive clean audit rounds" works. "Code
  feels better" does not.

## TASKS.md Template

```markdown
# Task Board

## Open

## In Progress

## Done

## Cycle Log
<!-- Appended by the loop after each cycle. Do not edit manually. -->
| Cycle | Found | Completed | Notes |
|-------|-------|-----------|-------|
```

No pre-populated tasks or log entries. The loop populates both.

## LEARNINGS.md Template

```markdown
# Learnings

## Summary
<!-- Updated by the loop every 5 cycles. Distills key patterns from entries below. -->

## Entries
<!-- Append-only. Each entry uses the format below. -->
```

### Entry format

Each learning follows this structure:

```
### Cycle N — [task name]
- **What:** One sentence on what was done
- **Insight:** What was discovered or confirmed during execution
- **Implication:** How this should influence future tasks (or "none")
```

The implication field carries the most value — it tells future cycles
what to do differently. The structure gives discovery parseable context
without requiring the loop to read every prior entry.

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
