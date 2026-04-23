# Workflow: First-Draft CLAUDE.md (Mode C)

Input: empty or near-empty — the user wants a first-draft CLAUDE.md for a
project the skill can learn about from conversation or the surrounding
repository. Output: a new CLAUDE.md written from scratch, applying EIP
principles from the start.

Load this file only when the mode detection in SKILL.md Stage 1 resolves
to **first-draft**.

---

## Stage 1 — Inventory (first-draft mode)

Since there's no source document, gather context from:

1. The user's message itself (*"write a CLAUDE.md for my payment API"*
   names a domain and a risk profile)
2. The surrounding repository — check for `README.md`, `package.json` /
   `pyproject.toml` / `Cargo.toml` / similar, `LICENSE`, top-level
   directory structure
3. Any existing agent-adjacent files — `AGENT.md`, `.cursorrules`,
   prior CLAUDE.md, etc.
4. Recent git log for pace-of-change and topical focus

Extract a working profile:

| Facet | Example |
|---|---|
| **Project type** | API / CLI / library / web app / data pipeline |
| **Stage** | Prototype / active dev / scaling / maintenance |
| **Risk profile** | Personal project / team tool / production / safety-critical |
| **Tech stack** | Languages, frameworks, infrastructure |
| **Team size signal** | Solo (personal repo) vs team (multiple committers, CI, reviews) |
| **Known conventions** | Linting, formatting, testing patterns detectable from config |
| **Stated priorities** | From README or stated by user |

### When to ask the user

Only ask via `AskUserQuestion` when a decision would substantially
branch the output AND the repo signal doesn't resolve it. Useful
questions:

- Stage (prototype vs. production) if the repo is ambiguous — risk
  profile flows from this
- Priority ordering when trade-offs are inevitable (speed vs.
  reliability)

**Do not ask** about style preferences, formatting, or anything with a
safe default.

**If the user invoked the skill with no arguments and no visible repo
signal**, make reasonable assumptions, draft the file, and note
assumptions at the top of the output as a one-line comment the user can
edit or remove.

## Stage 2 — Shape

Start from the template in `claude-md-template.md`. Decide which sections
apply:

| Always include | Include if signal present |
|---|---|
| Project Context | Technical Standards (when stack / risk is clear) |
| How You Should Operate | Common Situations (when the project has recurring patterns) |
| What I Don't Want | Tools & Conventions (when non-obvious tooling exists) |

Size the draft to the project:

- **Solo / personal project:** 30-50 lines total. Project Context,
  How You Should Operate (3 subsections), What I Don't Want. That's it.
- **Team tool / active dev:** 60-100 lines. Add Technical Standards,
  Common Situations.
- **Production / safety-critical:** 100-200 lines. All sections,
  often with additional subsections in How You Should Operate.

Don't inflate to look thorough. Floor is fine when the project is small.

## Stage 3 — Temper

Since there's no source to preserve, the temper stage is easier — every
phrase is fresh. Run the same anti-pattern lint from
`eip-anti-patterns.md`, but also watch for first-draft-specific hits:

- **Over-defaulting to enthusiasm** — a first draft should be neutral;
  warmth comes from honest framing, not default cheer
- **Imported cliches** — "best practices", "modern", "clean code" are
  usually content-free. Replace with specifics or delete.
- **Over-specification** — don't pre-invent rules the user hasn't asked
  for. A first draft is a spine; the user adds what matters to them.

## Stage 4 — Emit

Structure follows `claude-md-template.md`. For first-drafts, *lead with*
a one-line comment noting any assumptions:

```markdown
<!--
First draft. Assumptions applied:
- Treated as a [solo personal project | team tool | production system]
  based on [signal]
- [any other inferred branch points]
Edit this comment out once you've reviewed.
-->

# CLAUDE.md — [Project Name inferred from repo or user]

## Project Context
...
```

Emit the file directly to the target path if the user named one; otherwise
inline-display with a suggestion to save to `./CLAUDE.md`.

## Examples by Size

### Small (solo / personal, ~30 lines)

```markdown
<!--
First draft. Assumed solo personal project based on no CI config and
single committer in git log. Edit or remove this comment once reviewed.
-->

# CLAUDE.md

## Project Context

Personal habit tracker built in React + Supabase. Solo project, used for
learning React and as a real daily tool. Current phase: active dev,
adding features as the need appears.

## How You Should Operate

- Honest uncertainty beats a confident guess. If you're unsure an
  approach will work in React or with Supabase, say so — I'd rather
  understand the trade-off than get code I can't modify later.
- One feature at a time. Don't scaffold the whole app upfront; each
  change should stand alone.
- If I'm doing something in a weird way, tell me the idiomatic React
  approach. I'm here to learn.

## What I Don't Want

- No speculative abstractions — this is a personal project, not a framework.
- No features I didn't ask for, even as "nice-to-haves".
- No patterns I haven't encountered yet without a quick note on what
  they are.
```

### Medium (team tool / active dev, ~70 lines)

Add Technical Standards and Common Situations. Disposition expands to
4-5 subsections.

### Large (production, ~150 lines)

All sections. How You Should Operate has 5-7 subsections covering
reliability, small-changes, risk communication, certainty boundaries,
and hit-a-wall protocol. See `/tmp/claude-emotion-prompting/examples/claude-code-configs/CLAUDE.md.production`
for reference shape.

## Edge Cases

| Situation | Response |
|---|---|
| Repo has an existing CLAUDE.md | This is actually mode B (refactor), not mode C. Re-detect. |
| Repo is completely empty | Ask user for 1-2 essentials: project type, risk profile. Then draft from minimum signal. |
| User names a stack that isn't visible in repo | Trust the user; note the stack in Project Context. |
| Signals conflict (README says prototype, CI says production) | Surface the conflict; ask which governs the CLAUDE.md. |
| User says "just give me something generic" | Produce the minimal shape (~20 lines). Generic CLAUDE.mds are low-value — smaller is better than padded. |

## What Makes a Good First Draft

- **Scannable in under a minute.** A CLAUDE.md loaded every conversation
  shouldn't be a wall of text.
- **Specific where it's specific, silent where it's not.** A section that
  would require user input to fill meaningfully is better left absent
  than filled with defaults.
- **Anti-pattern-clean.** Register passes the lint.
- **Editable.** The user should be able to delete a section and still
  have a coherent doc.
