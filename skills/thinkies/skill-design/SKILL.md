---
name: skill-design
description: >-
  Design, strengthen, or audit an Agent Skill. Use before building any new
  skill — for a researched design brief that skill-creator can build from —
  and whenever an existing skill needs judgment or change: it over-triggers,
  under-triggers, bloats its context, drifts from its sources, or needs a
  quality check. Triggers: "design a skill", "plan a skill before building
  it", "audit this skill", "review my SKILL.md", "strengthen this skill",
  "refactor this skill", "is this skill well built", or any request to
  evaluate or improve how a skill routes, decides, or spends context.
  Packaging and eval mechanics stay with skill-creator; use this to decide
  what to build and to verify fit.
compatibility: >-
  Runs in the main conversation, and every mode involves conversation with
  the user. Floor executor: an agent that can read a skill's files, quote
  evidence from them by file and line, and walk numbered moves in order.
  For audit, the executor must have file search over the target skill's
  directory.
---

# Skill Design

Work every mode the same way: pose a principle as a question about the
skill in front of you — or the one taking shape — gather evidence from
its files, and decide from the evidence. One question underlies all ten
principles: can the executor close every decision delegated to it,
using only what the skill provides? A decision closes when the executor
can name the options on the table, the default included; tell the known
facts from the assumed ones; rank the options by a stated rule; strike
the options that fail a constraint; predict what follows from the
option it favors; and see which act binds. Wherever the skill leaves
one of those parts unsupplied, and gives the executor no way to find
it, you have found work.

Building, testing, and packaging belong with skill-creator; deciding
what a skill should be, and whether it holds up, belongs here. When the
work turns to drafting a SKILL.md, running evals, tuning a description,
or packaging, hand over to skill-creator.

## Route first

Decide the mode from the state of the world, never from your own
capability:

- No SKILL.md exists yet — an idea, a captured workflow, a conversation
  to distill → **Design**.
- A SKILL.md exists and the user wants change — a stated misfit, a
  strengthening request → **Refactor**.
- A SKILL.md exists and the user wants judgment without change →
  **Audit**.

When a request straddles two modes ("audit this and fix what you
find"), run Audit first and carry what you agreed on into Refactor as
evidence. When the user asks for a refactor but states no misfit
("refine this", "strengthen this"), do the same: walk the principles
over the whole skill first, and confirm with the user which findings to
aim the refactor at. When you cannot tell which mode fits, ask the user
one question rather than guessing. When a request fits no mode, say
so — name what the work would take that no mode covers, and ask whether
to stretch a mode or work outside this skill. Never force a fit.

Close a mode only when its exit artifact exists and satisfies its
specification — never when the work feels done.

## The modes

Read a mode's reference when you enter it, not before.

- **Design** — decide what a skill will do and for whom, before any
  SKILL.md exists. Ends at a design brief that whoever runs
  skill-creator next can work from. Read
  [references/design.md](references/design.md) on entering.
- **Refactor** — align an existing skill with its purpose by verifying
  properties against evidence. Ends at a typed change set, and the
  updated files once the user approves. Read
  [references/refactor.md](references/refactor.md) on entering.
- **Audit** — judge a skill with the user, changing nothing: a
  conversation that converges. Ends at priorities the user confirms.
  Read [references/audit.md](references/audit.md) on entering.

## The principles

Ten principles anchor every mode's questions, from scheduling the
workspace to making the skill observable.
[references/principles.md](references/principles.md) holds each in
full — statement, reason, check — plus the vocabulary they share. Read
it before design or refactor work; during an audit, walk it with the
user as lenses.

## The moves set a floor

Each mode's reference lists numbered moves. Walk them in order when
unsure how to proceed. When you can see a better move than the listed
one — one that fits this task better while still ending at the mode's
exit artifact — take it, and tell the user what you changed and why.

## Scaling evidence

Match evidence to stakes, never to your own sense of capability: how
often the skill gets reused, what a wrong decision would cost to undo,
and who reads the output. For one person's weekend project, less
evidence per claim; for a team's marketplace, more. The moves stay the
same; gather more evidence per move as stakes rise.
