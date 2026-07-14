---
name: ponder
description: >-
  Exploration skill for problems that need thinking before solving. Assesses
  a problem's shape and applies a sequence of exploration techniques —
  producing questions, reframings, structural maps, and new angles. Use when
  asked to "think about this", "help me explore", "what am I missing", "I'm
  stuck", "help me understand this problem", "ponder this", "what should I
  consider", "help me think through this", or when a problem needs reframing,
  assumption-surfacing, or systematic questioning before action. Also use
  when the user describes a vague idea, faces a decision fork, or expresses
  uncertainty about what they don't know.
compatibility: >-
  Runs in a forked context. Floor executor: an agent that can read a reference
  file and carry out its numbered reasoning moves against the problem. The
  techniques assume multi-step reasoning, not single-shot answers.
metadata:
  context: fork
---

# Ponder

Exploration skill. Assess the problem's shape, select techniques, apply them
in sequence. The caller sees substance — questions, frames, maps, new angles.
Never technique names, shape labels, or sequencing rationale.

## Phase 0: Assess

Detect the problem's shape from signals in "$ARGUMENTS" and the conversation.

| Shape | Signals |
|-------|---------|
| Vague | Cannot articulate the goal; shifting or absent target; hedging language; no clear problem boundary |
| Stuck | Clear problem but frustration; "already tried" language; enumerated failed approaches |
| Fork | Comparative language ("should I X or Y?"); identified alternatives; unclear criteria |
| Complex | Multiple interacting factors; "it depends"; competing constraints; many stakeholders |
| Blindspot | Meta-uncertainty ("what am I missing?"); new domain; sensing something is off without naming it |

Vague is not a catch-all for conflicting signals. Reach for it only when the
goal itself is unarticulated — its defining signal. When signals for several
*articulated* shapes co-occur, pick the shape carrying the most specific
signal: an enumerated failed approach → Stuck; named alternatives → Fork;
an explicit "what am I missing" → Blindspot; many named interacting factors →
Complex. A wrong pick is cheap because Phase 2 corrects it mid-course. (This
tie-break is a fixed decision; revisit it if misassessment recurs on real
inputs.)

Do not announce the shape. Proceed directly to selection.

## Phase 1: Select

Choose techniques based on shape. Load only the selected technique reference
files from `@./references/`.

A shape names what the thinking lacks; its sequence is the purposes that
repair the lack. Run one technique per purpose in the sequence — a shape's
sequence length is its technique count. The five purposes name cognitive
moves:

- **Discover** — dig out what is hidden and constraining: assumptions, root causes, leverage points.
- **Expand** — diverge: generate candidate directions, explanations, or questions.
- **Navigate** — map the territory: locate the abstraction level, the knowns, and the real question.
- **Explore** — probe an articulated position at its edges and from other frames.
- **Define** — converge: carve the problem into parts you can act on.

From these, a shape's sequence reconstructs from its deficit: Vague lacks a
target (Expand to find candidates, Navigate to orient, Define to fix one);
Stuck has exhausted the obvious (Discover the hidden constraint, Expand new
options, Navigate what is actually known). Extend the same reasoning to
signals the tables below do not list.

| Shape | Sequence | Technique pool (pick one per purpose) |
|-------|----------|---------------------------------------|
| Vague | Expand, Navigate, Define | **Expand**: wonder, branch-out; **Navigate**: zoom, question-the-question; **Define**: decompose |
| Stuck | Discover, Expand, Navigate | **Discover**: excavate-assumptions, first-principles; **Expand**: consider-alternatives, connect-domains; **Navigate**: assess-knowledge |
| Fork | Explore, Define, Navigate | **Explore**: argue-opposite, probe-boundaries, shift-perspective; **Define**: decompose; **Navigate**: zoom, assess-knowledge |
| Complex | Navigate, Explore, Define, Expand | **Navigate**: assess-knowledge, zoom; **Explore**: shift-perspective, invert; **Define**: decompose; **Expand**: branch-out, connect-domains |
| Blindspot | Discover, Expand, Explore | **Discover**: excavate-assumptions, premortem, find-leverage; **Expand**: wonder, consider-alternatives; **Explore**: invert, probe-boundaries |

Within each purpose, pick the technique that best fits the problem's content:

- Existing plan or proposal: premortem, argue-opposite, probe-boundaries
- Choosing between options: consider-alternatives, shift-perspective, zoom
- Understanding a system: find-leverage, decompose, connect-domains
- Conceptually stuck: first-principles, invert, wonder
- Involves people or stakeholders: shift-perspective, excavate-assumptions, branch-out

## Phase 2: Apply

Execute each selected technique in sequence. Each technique's output feeds
the next. Read the technique's reference file, then follow its instructions
against the problem.

### Sequencing rules

Apply in priority order when the default shape sequence needs adjustment:

1. Discover, if present, goes first or second — hidden assumptions constrain everything downstream
2. Expand precedes Define — diverge before converging
3. Navigate precedes Explore for unfamiliar territory — map before probe
4. Define does not come first — it needs prior divergent input
5. Perspective-shifting precedes generation when both present
6. The final technique advances toward actionability

### Transparency

Present the substance directly. No headers announcing technique names. No
meta-commentary ("now I will explore from a different angle"). Transitions
between techniques are woven into the substance, not announced. The output
reads as natural, flowing exploration.

This concealment is a fixed decision, not a per-run choice — it keeps the
caller's attention on substance rather than method. Revisit it only if callers
report the exploration feels arbitrary or untrustworthy without a visible
method.

If a technique's output reveals the shape was misassessed, adjust the
remaining techniques accordingly.

## Phase 3: Surface

After all techniques are applied, offer a concise synthesis:

- What the exploration revealed
- What questions remain open
- What the most promising next step appears to be

This is the one place where naming open questions and suggesting directions
is appropriate — it is substance, not process.

## Context Loading

Load only the technique reference files selected in Phase 1. Never load all
references upfront.

| Phase | Load |
|-------|------|
| Assess + Select | Nothing from references — use the tables above |
| Apply | Only the selected technique files from `@./references/` |
| Surface | Nothing additional |

## Technique Reference Files

Each file in `references/` contains a single technique's step-by-step
instructions. The files are:

| File | Purpose | Category |
|------|---------|----------|
| `wonder.md` | Open possibility space through curiosity | expand |
| `branch-out.md` | Generate distinct continuations from one point | expand |
| `consider-alternatives.md` | Create multiple explanations for same observations | expand |
| `connect-domains.md` | Import solutions from distant domains | expand |
| `assess-knowledge.md` | Map verified vs assumed vs unknown | navigate |
| `zoom.md` | Move between abstraction levels | navigate |
| `question-the-question.md` | Examine whether inquiry is aimed at right target | navigate |
| `probe-boundaries.md` | Test conclusions at edges and extremes | explore |
| `argue-opposite.md` | Stress-test by building strongest counter-case | explore |
| `invert.md` | Turn problems inside out | explore |
| `shift-perspective.md` | Inhabit different frames | explore |
| `decompose.md` | Break wholes into parts at natural joints | define |
| `excavate-assumptions.md` | Surface unstated assumptions at multiple levels | discover |
| `first-principles.md` | Strip convention to find irreducible truths | discover |
| `premortem.md` | Imagine failure and work backwards | discover |
| `find-leverage.md` | Find where small actions create outsized results | discover |
