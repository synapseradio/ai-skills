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
  file, carry out its numbered reasoning moves against the problem, and answer
  a yes/no check by quoting from output it has already produced. The
  techniques assume an executor that reasons in steps.
metadata:
  context: fork
---

# Ponder

Exploration skill. Assess the problem's shape, open with a technique matched
to it, extend the chain only while the problem quotably demands more, and
converge on a decision. The caller sees substance — questions, frames, maps,
new angles. Technique names, shape labels, and chain mechanics stay hidden.

## Phase 0: Assess

Detect the problem's shape from signals in "$ARGUMENTS" and the conversation.

| Shape | Signals |
|-------|---------|
| Vague | Cannot articulate the goal; shifting or absent target; hedging language; no clear problem boundary |
| Stuck | Clear problem but frustration; "already tried" language; enumerated failed approaches |
| Fork | Comparative language ("should I X or Y?"); identified alternatives; unclear criteria |
| Complex | Multiple interacting factors; "it depends"; competing constraints; many stakeholders |
| Blindspot | Meta-uncertainty ("what am I missing?"); new domain; sensing something is off without naming it |

Reach for Vague only when the goal itself remains unarticulated — its
defining signal. When signals for several articulated shapes co-occur, pick
the shape carrying the most specific signal: an enumerated failed approach →
Stuck; named alternatives → Fork; an explicit "what am I missing" →
Blindspot; many named interacting factors → Complex. A wrong pick costs
little because the extension check in Phase 2 corrects it mid-course.

Proceed directly to Phase 1 without announcing the shape.

## Phase 1: Open

A shape names what the thinking lacks. Five purposes name the cognitive moves
that repair a lack:

- **Discover** — dig out what hides and constrains: assumptions, root causes, leverage points.
- **Expand** — diverge: generate candidate directions, explanations, or questions.
- **Navigate** — map the territory: locate the abstraction level, the knowns, and the real question.
- **Explore** — probe an articulated position at its edges and from other frames.
- **Define** — converge: carve the problem into parts you can act on.

Each purpose draws from a pool of techniques:

| Purpose | Techniques |
|---------|------------|
| Discover | excavate-assumptions, first-principles, premortem, find-leverage |
| Expand | wonder, branch-out, consider-alternatives, connect-domains |
| Navigate | assess-knowledge, zoom, question-the-question |
| Explore | probe-boundaries, argue-opposite, invert, shift-perspective |
| Define | decompose |

Every chain runs at least two techniques: an opener whose purpose repairs the
shape's deficit, and a closer that converges. The shape sets the opener:

| Shape | Deficit | Opening purpose |
|-------|---------|-----------------|
| Vague | lacks a target | Expand — generate candidates to aim at |
| Stuck | has exhausted the obvious | Discover — dig out the hidden constraint |
| Fork | has options without criteria | Explore — probe the alternatives at their edges |
| Complex | has more factors than frame | Navigate — map the territory before judging it |
| Blindspot | suspects an unseen gap | Discover — surface what constrains unnoticed |

The closer comes from Define or Navigate — decompose, assess-knowledge, or
zoom — and must leave material Phase 3 can rank: named options, criteria, or
a mapped constraint set.

Within a purpose, pick the technique that best fits the problem's content:

- Existing plan or proposal: premortem, argue-opposite, probe-boundaries
- Choosing between options: consider-alternatives, shift-perspective, zoom
- Understanding a system: find-leverage, decompose, connect-domains
- Conceptually stuck: first-principles, invert, wonder
- Involves people or stakeholders: shift-perspective, excavate-assumptions, branch-out

## Phase 2: Apply and extend

Execute the opener: read its reference file from `@./references/`, follow its
numbered moves against the problem, and let each technique's output feed the
next.

After each technique, run the extension check against everything produced so
far. Extend the chain when a row below fires; when none fires, run the closer
and move to Phase 3.

| The output so far shows... | Extend with |
|----------------------------|-------------|
| The question itself has changed and the new one remains unexplored | Navigate |
| The emerging conclusion leans on an assumption no technique has tested | Discover |
| Fewer than two candidate options or directions have a name | Expand |
| Two techniques' outputs contradict each other | Explore |

Three rules bound the check:

1. **Quote to extend.** To count a row as fired, quote the sentence from the
   output that fires it. A row you can only paraphrase has stayed silent.
2. **Stop at fixpoint.** When the last technique added nothing you can quote
   as new, run the closer now, even if a row fires — the chain has stopped
   changing the picture.
3. **Cap at five.** The chain holds at most five techniques, the closer
   included. At the cap, converge.

When several rows fire, repair the topmost: a re-aimed question invalidates
dug assumptions, untested assumptions distort generated options, and options
must exist before their edges get probed.

A misassessed shape corrects itself here: the problem's real deficit fires
its row at the next check, and the chain repairs it.

### Voice

Present the substance directly, and weave transitions between techniques into
it. Headers announcing technique names, meta-commentary ("now I will explore
from a different angle"), and chain mechanics stay out of the output — the
caller reads natural, flowing exploration.

Four rules govern the prose:

- **Clear.** Plain declarative sentences a reader outside the domain can
  follow.
- **Unopinionated.** Tie each substantive claim to something in the problem
  material, or mark it as an assumption. Advocacy appears once, in Phase 3's
  ranking, and cites the rule it ranks by.
- **Concise.** Prefer the shortest phrasing that keeps a claim checkable.
- **Affirmative.** State what holds and what to do. Recast a failure or a
  thing to avoid as the condition that holds instead.

## Phase 3: Converge

Close the exploration with:

- What the exploration revealed
- The options now on the table, the default of changing nothing included
- A ranking of the options, with the rule that ranks them stated
- The leading option and the concrete evidence that would flip it
- What remains genuinely open

When the evidence ranks several options equally, report the tie as the
result, keep the ranking rule stated, and name the observation that would
break the tie.

## Context Loading

| Phase | Load |
|-------|------|
| Assess + Open | Nothing from references — use the tables above |
| Apply + extend | Only the current technique's file from `@./references/` |
| Converge | Nothing additional |

## Technique Reference Files

Each file in `references/` holds a single technique's step-by-step
instructions:

| File | What it does |
|------|--------------|
| `wonder.md` | Opens possibility space through curiosity |
| `branch-out.md` | Generates distinct continuations from one point |
| `consider-alternatives.md` | Creates multiple explanations for the same observations |
| `connect-domains.md` | Imports solutions from distant domains |
| `assess-knowledge.md` | Maps verified vs assumed vs unknown |
| `zoom.md` | Moves between abstraction levels |
| `question-the-question.md` | Examines whether the inquiry aims at the right target |
| `probe-boundaries.md` | Tests conclusions at edges and extremes |
| `argue-opposite.md` | Stress-tests by building the strongest counter-case |
| `invert.md` | Turns problems inside out |
| `shift-perspective.md` | Inhabits different frames |
| `decompose.md` | Breaks wholes into parts at natural joints |
| `excavate-assumptions.md` | Surfaces unstated assumptions at multiple levels |
| `first-principles.md` | Strips convention to find irreducible truths |
| `premortem.md` | Imagines failure and works backwards |
| `find-leverage.md` | Finds where small actions create outsized results |
