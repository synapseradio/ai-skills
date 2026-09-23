# Proposal: thinkies-perspective-operations

## Why

The thinkies plugin exists to make ideas clear, both to the person thinking them
and to the person reading about them. Its skills fall short of that in two ways.
First, analysis and reader-facing writing are tangled together. The inventory at
8011fec finds 122 presentation passages inside analytic skills, 47 instructions
that hide or show the reasoning chain, and 10 groups of label sets that classify
the same thing in different ways. None of the eight skills that shape output for
a reader names an analytic result as its input. Second, the analytic skills have
no shared account of what each one does. The inventory finds 82 steps that
perform an operation other than their skill's own, and 7 skills whose method
fits another category better. The user has now decided the structure that fixes
both problems: three stages of work, and a taxonomy of operations on perspective
described on two axes. This change records those decisions as requirements and
keeps every question that is still open in view.

Evidence: `/Users/nick/.scratchpad/ai-skills/main/thinkies-presentation-inventory__02-01PM_23-09-2026.md`,
sections 1 to 5. The design lists every source and its status.

## What Changes

**Stages (`thinkies-stages`)**

- Every step of every thinkies skill belongs to exactly one of three stages:
  analysis, interaction, or presentation. A step that mixes two stages is split.
- **BREAKING**: analytic skills end at a structured result and stop shaping
  output for a reader. Voice rules, citation styles, closing offers, and visual
  templates move out of the analytic run. What a person sees when they invoke an
  analytic skill directly depends on open question Q21 in the design.
- Interaction holds the dialogue skills (strategize, question-through-dialogue,
  ask-questions) and dialogue steps such as scamper's clarify phase. What
  interaction learns enters the analysis as a recorded input.
- Presentation runs last. Presentational skills take the structured result as
  input, choose a view of it, and never reshape it or add judgments to it.

**Structured result (`thinkies-structured-result`)**

- The structured result carries the full reasoning chain, including the parts a
  reader never sees.
- Only presentation decides how much of the chain a reader sees. Analytic
  skills lose their hide and show instructions.
- The result records classifications as labels with their grounds. Reader
  wording for those labels moves to presentation.

**Operations on perspective (`thinkies-perspective-operations`)**

- Each operation is described on two axes: the move made and the relation or
  relations the move follows. This replaces a single list of eight operations.
- The plugin keeps one move list and one relation list. The move list starts
  with Expand, Refine, Transform, Foil, Annotate, Connect, Select, and Decide.
  The relation list starts with part-of, is-a, entails, causes, accumulates,
  serves-purpose, and bounded-by. Which members each list finally holds stays
  open.
- Each of the thirty operation skills declares its move and relations in its
  frontmatter `metadata`.
- Foil and Decide get the definitions the user gave them. Every move differs in
  meaning from every other move.
- A move that a tradition names counts as a primitive. The skill that implements
  it cites the tradition.

**Still open**: 21 questions, listed in the design with their options and who
settles each one. Some turn on the user's answer and some on research still in
flight. None of them is written as a requirement.

## Capabilities

### New Capabilities

- `thinkies-stages`: the three stages, which stage each step belongs to, and
  the contract between analysis, interaction, and presentation.
- `thinkies-structured-result`: what an analytic run's result carries — the
  full chain, recorded as labels — and who decides what a reader sees of it.
- `thinkies-perspective-operations`: the move-by-relation taxonomy, its lists,
  the Foil and Decide definitions, the declaration each operation skill makes,
  and primitives that a tradition names.

### Modified Capabilities

None. The three visualization specs under `openspec/specs/` keep their
requirements. The input contract that visualize gains as a presentational skill
is added through `thinkies-stages`.

## Impact

- **Skill source**: `skills/thinkies/<name>/` for all 48 skills. Analytic
  skills lose their presentation steps. Operation skills gain `metadata.move`
  and `metadata.relations`. Presentational skills gain an input contract.
- **Extension copies**: `extensions/thinkies/skills/<name>/` gets a fresh copy of
  each changed skill. `extensions/openai/thinkies/skills/<name>/` gets rebuilt
  with `bin/generate-openai-plugin.py`.
- **Packaging**: `packaged/thinkies/<name>.skill` gets rebuilt for each changed
  skill with the skill-creator packager, which also validates the frontmatter.
- **Users**: invoking an analytic skill directly returns something different
  once presentation leaves it (see Q21).
