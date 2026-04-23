# CLAUDE.md Template (Human Headings)

For modes B (refactor) and C (first-draft), emit the output using human-readable
section headings rather than the internal bucket names. The mapping:

| Internal Bucket | CLAUDE.md Section |
|---|---|
| Frame | (merged into Project Context) |
| Task | (implicit — the project itself is the task; stakes/purpose go in Project Context) |
| Context | Project Context |
| Tooling | Tools & Conventions |
| Context To Gather | (merged into How You Should Operate, typically a "Before Starting Work" subsection, or into Common Situations) |
| Constraints & Invitations | Technical Standards + What I Don't Want |

Plus two sections that live only in CLAUDE.md form:

- **How You Should Operate** — the disposition; where EIP principles live
  as persistent instructions
- **Common Situations** — patterns for recurring situations (when stuck,
  when reviewing code, when debugging, etc.)

---

## Section-by-Section Guidance

### Project Context

Combines Frame and Context, and includes the "why this project exists"
paragraph (what was previously a standalone Why section now lives here as
part of the overall context). Give enough background that the agent can
make judgment calls without asking.

Structure:

- One sentence on what the project is
- One sentence on who it's for / what problem it solves
- Current phase (early prototype / active development / scaling / maintenance)
- Key priorities with ordering (reliability > speed, or vice versa, etc.)
- Tech stack as a list
- Non-obvious constraints (deployment target, compliance, team size)

### How You Should Operate

The disposition. This is where EIP principles translate to persistent
behavioral defaults. A typical CLAUDE.md needs 3–5 subsections here:

- **Honesty Over Performance** — principle 1 (permission to fail) +
  principle 4 (transparency)
- **Build Incrementally** — principle 2 (checkpoints)
- **Think Out Loud** — principle 4 (transparency)
- **Collaborate** — principle 5 (collaboration)
- **When Tasks Are Hard** — principle 6 (acknowledge difficulty)

Adjust to fit the project. A security-critical system needs more caution
and less #7; a creative tool needs more #7. Don't include all five by
default — pick what matters.

### Technical Standards

Verifiable, mechanically-checkable constraints. These stay as musts —
they're what principle-2 (constraints) looks like when the constraint is
objectively satisfiable.

Examples:

- "All changes must have tests"
- "Database migrations must be reversible"
- "No swallowed errors"
- "Error handling required for every external call"

Keep these short, verifiable, and project-specific.

### Common Situations

Patterns for recurring situations. Pre-apply principles to predictable
cases.

Subsections commonly seen:

- **When You Hit a Wall** — principle 1 + 6 applied
- **When Requirements Are Unclear** — principle 5 applied
- **When Reviewing Code** — principle 4 + 5 applied
- **When Debugging** — principle 1 + 2 + 4 applied

### Tools & Conventions

Tools the agent should use, patterns the project follows, non-obvious
naming or structural conventions. Short. Link to longer docs if they
exist.

### What I Don't Want

The anti-patterns, scoped to the project. 3–5 items max. This section is
high-leverage — it directly addresses failure modes the user has seen.

Examples:

- "Don't add complexity I didn't ask for"
- "Don't silently assume requirements for critical paths — ask"
- "Don't refactor code I didn't ask you to touch"
- "Don't present uncertain code as tested"

---

## Minimal Shape (for small projects)

A small solo project rarely needs every section. A useful floor:

```markdown
# CLAUDE.md

## Project Context

[what / who / why / current phase / tech stack]

## How You Should Operate

- Honest uncertainty beats confident guessing.
- Build incrementally. One piece at a time.
- If a task seems wrong, push back before building.

## What I Don't Want

- [the 2-3 most important anti-patterns for this project]
```

Six to ten lines can be enough. Don't pad.

## Full Shape (for production / multi-person projects)

See the examples in `/tmp/claude-emotion-prompting/examples/claude-code-configs/`
for worked examples: `CLAUDE.md.general`, `CLAUDE.md.startup`,
`CLAUDE.md.research`, `CLAUDE.md.production`.

Those aren't prescriptive — they're reference points for how the sections
expand when a project has more stakeholders, more risk, or more
conventions.

---

## What to Preserve Verbatim (in refactor mode)

Some content never gets register-shifted:

- Code examples, shell commands, file paths
- Configuration keys, environment variable names, API endpoint paths
- External references (URLs, paper citations, links)
- Literal tool/command output quoted in the doc
- User-specific details (names, emails, handles)

These are facts, not framing. Change them only if the original was wrong
and the user asked for a correction.

## What to Rewrite (in refactor mode)

The prose around the facts:

- Disposition statements
- Explanations of why a rule exists
- Section introductions
- Transitions between topics

The temper stage applies here. The underlying facts stay; the register
changes.
