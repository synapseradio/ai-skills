---
name: prompt
description: >-
  Craft or refactor LLM instructions grounded in Anthropic's functional-emotions
  research. Invoke whenever a user asks to "write a prompt", "assemble a prompt",
  "refactor my CLAUDE.md", "update CLAUDE.md", "fix my system prompt", "draft a
  CLAUDE.md", "turn this task into a prompt", "polish this prompt", "make this
  prompt better", "prompt this", or describes a rough task, project, or
  instruction set that would benefit from a shaped prompt. Also trigger on
  phrases like "write me a CLAUDE.md for…", "clean up this system prompt", or
  when the user pastes an existing CLAUDE.md/system prompt and asks for an
  improvement. Takes no required arguments — the skill detects whether the
  input is a seed task, an existing CLAUDE.md to refactor, or an empty canvas,
  and produces structured output that applies the seven Emotional Intelligence
  Prompting (EIP) principles while preserving every instruction in the input.
metadata:
  context: fork
  user-invocable: true
---

# Prompt

Shape LLM instructions around how models actually process framing. Apply
Anthropic's April 2026 functional-emotions research (seven principles, nine
anti-patterns) as a structural lens over the six slots of a well-formed
prompt. When refactoring, preserve every original instruction by truth-condition,
not by wording.

| Field | Value |
|---|---|
| **Execution context** | inline |
| **Prerequisite** | none |
| **Arguments** | none required — the skill auto-detects input mode |
| **NOT triggered by** | Running the skill on itself; writing READMEs, blog posts, or general documentation (use `documentation` or `communicate` instead); producing agent delegations that already have a well-formed structure (use `perspectives:prompt-assemble` if the user explicitly requests its schema) |

## When to Use This Skill

Trigger whenever any of these shapes apply:

- A rough task description the user wants turned into a usable prompt
- An existing `CLAUDE.md` or system prompt the user wants refactored
- A blank canvas where the user wants a first-draft `CLAUDE.md` for a project
- A "make this prompt better" request with a prompt pasted in
- Any instruction set where the user mentions tone problems, fabrication,
  over-confidence, or wants "more honest" AI behavior

## Core Design

Two sources stack, with precedence: the six-bucket structure adapted from
`perspectives:prompt-assemble` defines the *shape*; Emotional Intelligence
Prompting (EIP) defines the *predicates the shape must satisfy*. When they
conflict, reshape the phrasing inside a bucket — never drop the EIP principle.

The buckets, renamed for register:

| Bucket | Purpose | Notes |
|---|---|---|
| **Frame** | Who/what the agent is, stance to take | Replaces "Role". Avoids compliance-pressure tone. |
| **Task** | What work is to be done; closes with a one- to two-sentence stakes paragraph that names what's at risk and why this matters | Non-negotiable; the only bucket that must always have real content. Stakes ride at the bottom of Task — there is no trailing "Why" section. |
| **Context** | Prior knowledge, files, background the agent already has | Replaces "Onboarding"; promoted — honest context reduces fabrication. |
| **Tooling** | Tools, MCPs, skills the agent can use | Unchanged. |
| **Context To Gather** | Prerequisite checks the agent should run before producing output — domain-specific verifications, lookups, or questions to answer first | Replaces "Perspective". The content was always pre-work context; the name now matches. |
| **Constraints & Invitations** | Verifiable musts + softened judgment asks | Replaces "Success Conditions". Keeps mechanically checkable criteria as musts; reshapes judgment criteria as invitations. |

For `CLAUDE.md` output, these buckets map to human headings — see
`references/claude-md-template.md`.

## The Pipeline

Every invocation runs four stages:

1. **Inventory** — identify what the input actually contains
2. **Shape** — slot the content into buckets
3. **Temper** — run the anti-pattern lint over every phrasing
4. **Emit** — write the artifact

The stages are the same across modes; only the **Inventory** stage branches.

## Stage 1 — Inventory (with mode detection)

Detect the mode from the context. Do not ask the user. The user is busy and
the signals are clear:

| Signal | Mode |
|---|---|
| Input is a path to a `CLAUDE.md`, or user pastes an existing CLAUDE.md/system prompt | **Refactor** — mode B |
| Input is prose describing a task or project and the user wants a usable prompt (not a CLAUDE.md) | **Seed** — mode A |
| Input is empty/near-empty, OR the user says "write me a CLAUDE.md for this project" regardless of how much context they give | **First-draft** — mode C |

When the input is ambiguous between seed and first-draft (e.g. a project
description without the words "CLAUDE.md" or "prompt"), use the output
shape the user is likely to want: if they mention an agent, a delegation,
or a specific task to execute, treat it as seed. If they mention
configuring a project, onboarding Claude, or long-term defaults, treat
it as first-draft. When genuinely unresolvable, default to seed and note
the assumption at the top of the output in one line.

Then load the matching workflow reference and follow it:

- **Mode A (Seed):** load `references/workflow-seed.md`
- **Mode B (Refactor):** load `references/workflow-refactor.md`
- **Mode C (First-draft):** load `references/workflow-firstdraft.md`

Each workflow tells the inventory step what to extract. Modes A and C gather
from conversation signal; mode B extracts a stable-ID list of every
instruction in the source document — this is what makes the preservation
invariant checkable.

## Stage 2 — Shape

Assign the inventoried content to the six buckets. For mode B, every
extracted instruction ID must be slotted into at least one bucket — an
unassigned ID is a dropped instruction. Stakes/motivation content lands at
the tail of the Task bucket, not a separate section.

Buckets with no real content get a one-line gap note in the output
(e.g., *"No onboarding context identified — the agent works from conversation
signal alone."*) rather than padding. Filler violates EIP's no-enthusiasm-theater
principle; structured absence is signal.

## Stage 3 — Temper (the lint)

Run the nine anti-pattern checks over every phrasing before emit. Load
`references/eip-anti-patterns.md` for the full check definitions. The short
form:

1. **Threatening consequences** — any "critical", "cost the company", "can't afford"
2. **Demanding certainty** — "definitive", "don't hedge", "just tell me"
3. **Negative-feedback-without-direction** — "try again", "still wrong"
4. **Suppressing expression** — "don't say I think", "no caveats"
5. **Massive all-at-once requests** — scope exceeds what one exchange can validate
6. **Authoritarian tone** — "You are", "You must", "Do not" stacks
7. **Forced enthusiasm** — "LOVES", exclamations, cheerleading
8. **Ignoring pushback** — implicit "just do it" framing
9. **Perfect-prompt fallacy** — over-engineering a single prompt instead of
   leaving room for conversation

For each hit, rewrite the phrase — do not suppress the underlying
instruction. If the original CLAUDE.md contained "You must write tests for
every function", the rewrite preserves the requirement while removing the
compliance-pressure register: "Every function needs a test. If you're unsure
whether existing coverage catches a new edge case, add one — missing tests
in a payment system cost more than spurious tests."

The lint is about the register, not the content. Truth-conditions are sacred.

## Stage 4 — Emit

Produce the artifact. The shape depends on the mode:

- **Mode A:** structured 6-section prompt (see `references/workflow-seed.md`)
- **Mode B:** refactored `CLAUDE.md` using human headings, plus a coverage
  report if instruction count ≥ 10 (see `references/workflow-refactor.md`)
- **Mode C:** new `CLAUDE.md` using the template in
  `references/claude-md-template.md`

Write files directly when the user has given a path, or inline-display the
output when they haven't. Do not fabricate file paths.

## The Precedence Rule

> Write the natural phrasing first. Check it against the nine anti-patterns
> by name. If it fires one, note which principle the fix draws from and
> rewrite the phrasing — never the structure, never the underlying
> instruction.

Structure is fixed; register is negotiable; the anti-patterns are the lint.
EIP alignment is the *absence* of anti-patterns, not the *presence* of warmth.
A direct, neutral prompt that passes the lint is aligned. A cheerful prompt
stapled with "Let's figure this out together!" is not.

## User-Interaction Policy

The skill runs end-to-end without asking questions, with one exception:
after a mode-B refactor of a `CLAUDE.md` containing more than ~15 distinct
instructions, ask the user to confirm the coverage report before writing
the new file. Big CLAUDE.mds are load-bearing; silent rewrites of them
burn trust.

Small refactors, seeds, and first-drafts emit without asking.

## Reference Files

Load only what the current mode needs:

- **`references/eip-principles.md`** — the seven principles, each with the
  specific research finding it's grounded in. Load during Stage 3 if the
  temper step needs a reminder why a rewrite matters.
- **`references/eip-anti-patterns.md`** — the nine anti-patterns as lint
  rules, with detection hints and rewrite patterns. **Load always in Stage 3.**
- **`references/claude-md-template.md`** — human-heading mapping for
  CLAUDE.md output. Load in modes B and C.
- **`references/workflow-seed.md`** — mode-A inventory and emit structure.
- **`references/workflow-refactor.md`** — mode-B inventory (instruction
  extraction), preservation invariant, coverage report format.
- **`references/workflow-firstdraft.md`** — mode-C inventory (context-gathering
  questions to answer internally or surface if essential), emit structure.

## Quality Standards

- Every bucket in the output either has real content or an explicit
  one-line gap note.
- Zero anti-pattern hits in the emitted text (the temper stage enforces this).
- In mode B, every input instruction has a stable ID and lands in the
  coverage mapping.
- Scripts, tools, or paths named in the output exist — no fabricated
  references.
- The output reads as natural, not templated. If a section feels like
  filler, cut it.

## Edge Cases

| Situation | Response |
|---|---|
| Input is ambiguous (could be seed or refactor) | Default to seed; note assumption in one line at top of output. |
| User pastes a CLAUDE.md but asks only for a specific tweak | Run the full temper pass anyway, but emit a minimal diff instead of a full rewrite. Preserve the user's other choices. |
| Existing CLAUDE.md is already EIP-aligned | Emit a short note saying so, and skip the rewrite. Don't churn for theater. |
| Source prompt contradicts itself | Surface the contradiction rather than silently resolving it. Ask the user which way to resolve, via `AskUserQuestion`. |
| User asks for a specific tone the register lint would flag (e.g. terse command style for a one-shot formatter) | Honor it, but note which anti-patterns the requested style relaxes. Domain-appropriate register wins over universal lint. |

## After Emit

If the user indicates they'll evaluate the output in a subagent session,
structure the emission so it's eval-friendly: clear section boundaries,
named buckets, coverage report in a fenced block when present. Don't bury
artifacts inside prose.
