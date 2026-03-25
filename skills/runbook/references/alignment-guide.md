# Alignment Guide

Protocol for the Phase 1 conversation. The goal is to surface intent clearly
enough to seed an autonomous loop that does the right work.

## Conversation Structure

Start broad, narrow progressively. Do not front-load all questions — let
answers to early questions inform what to ask next.

### Opening

Begin by understanding the work at a high level:

- "What are we improving / building / fixing?"
- "What prompted this? What's the pain or opportunity?"
- "What does success look like when this is done?"

Listen for implicit scope, lens, and authority in the user's answers.
Reflect understanding back before narrowing.

### Decomposition

Break the work into parts. Use the technique appropriate to the problem:

**For vague intent** — ask "what would change if this succeeded?" and work
backward from observable outcomes to required work.

**For broad scope** — ask "what's the first area you'd want to see
improved?" to find the entry point. One lens at a time.

**For competing priorities** — present tradeoffs as structured choices
via AskUserQuestion. Make the tension explicit: "These two goals pull in
different directions. Which takes priority?"

**For technical uncertainty** — propose a discovery-first approach: the
loop's first task is to audit and report, not to change anything.

### Narrowing to Seven Elements

Through conversation, surface each element. Do not present this as a
checklist — weave it into dialogue naturally.

| Element | What to surface | Examples across use cases |
|---------|----------------|--------------------------|
| What | The work, decomposed | "Implement auth module for new Rust API" / "Migrate class components to hooks in src/legacy/" / "Bring style consistency to the utils package" |
| Why | The motivation | "Greenfield — building the core before adding team members" / "Tech debt blocking the v2 release" / "Open-sourcing next quarter" |
| Lens | What discovery looks for or builds toward | "Feature requirements from the design doc" / "React 18 migration targets" / "Naming and structure consistency" |
| Authority | What reference to consult | "The PRD at docs/auth-spec.md" / "React migration guide" / "The project's own established patterns in src/core/" |
| Scope | Boundaries | "src/auth/ only" / "src/legacy/ — skip src/core/ and tests/" / "All of packages/utils/" |
| Success | Concrete done-state | "All endpoints in the spec are implemented with tests" / "Zero class components remain in scope" / "Linter passes clean, no TODO markers" |
| Mode | Tight loop or recursive | "Tight loop — one module" / "Recursive — migration + test backfill are independent" |

### Inline Visualization

Make the conversation concrete with visual aids:

**Scope diagram** — show what's in and out:

```
In scope          Out of scope
-----------       ------------
src/auth/         src/core/ (stable)
src/middleware/    node_modules/
                  *.generated.*
```

**Lens comparison** — when the user is choosing between foci:

```
Lens A: Feature implementation
  Discovers: next unimplemented endpoint from the spec
  Authority: docs/auth-spec.md
  Verification: test-first — each endpoint gets integration tests

Lens B: Migration
  Discovers: next class component to convert
  Authority: React hooks migration guide
  Verification: existing tests still pass after conversion
```

**Task preview** — show what discovery might produce, adapted to the lens:

```
Feature lens example:           Migration lens example:
  T1: Implement POST /login       T1: Convert UserProfile to hooks
  T2: Implement GET /me            T2: Convert SettingsPanel to hooks
  T3: Add rate limiting middleware  T3: Replace withRouter HOC usage
```

### Mode Decision

Only raise this when the problem's structure warrants it.

**Signals that tight loop is right (default):**

- Single codebase area
- One clear lens
- Work is bounded and convergent
- User wants to set it and check back later

**Signals that recursive decomposition is needed:**

- Multiple independent sub-problems
- Different lenses needed for different areas
- Work benefits from separate focus/report cycles
- User describes something like "research phase then implementation phase"

If recursive, identify the parent lens and child lenses during alignment.
Each child becomes its own FOCUS.md with tighter scope.

## Convergence Detection

Watch for these signals that alignment is complete:

- User's answers are confirming rather than adding new information
- Questions produce refinements, not redirections
- The seven elements are all surfaced (even if some are "default")
- User language shifts from exploratory ("maybe", "could") to directive
  ("yes", "that's right", "exactly")

When convergence is detected, state it explicitly:
"I think we've covered the key dimensions. Let me check the gates before
we seed the loop."

Then load `references/checklist.md` and validate.

## Anti-Patterns

**Interrogation mode.** Asking all seven elements as a sequential form.
Instead, let early answers inform later questions. Many elements emerge
naturally from a good opening conversation.

**Premature narrowing.** Jumping to lens and scope before understanding
the why. The motivation shapes everything downstream.

**Assuming the mode.** Defaulting to recursive decomposition because it
sounds more thorough. Tight loop handles 90% of cases. Only go recursive
when the user's description clearly has independent sub-problems.

**Skipping visualization.** Abstract descriptions of scope and lens are
hard to validate. A 5-line diagram catches misalignment that paragraphs miss.

**Over-engineering the lens.** A lens that tries to cover everything
covers nothing. One clear focus per loop. If the user wants multiple foci,
that's a signal for recursive decomposition, not a wider lens.
