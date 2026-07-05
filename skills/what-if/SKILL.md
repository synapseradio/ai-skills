---
name: what-if
description: >-
  Tile the space of possible futures and evaluate strategies across the
  tiles. Blends part-whole decomposition with tree and graph of thought.
  This skill should be used when the user asks "what if", "what could
  happen if", "evaluate possible futures", "map the scenarios", "explore
  how this could play out", "compare futures", "stress-test this plan
  against the future", or faces a decision whose outcome hinges on
  unresolved uncertainties. Ends with a single reasoned recommendation
  plus the conditions that would flip it.
metadata:
  context: fork
---

# What-if

Someone has handed you a future: a decision to make, a hypothetical to play out, an idea to gut-check. Your job is to accelerate their inference — to get them from a sparse question to a decision they can own, faster than they would alone. Some of what determines their future is already knowable, and the honest first move is separating that part out. What remains genuinely unknowable is where this skill does its work.

The method, with its three terms grounded before use. Find the unknowns that would actually change what the asker does — each one becomes an **axis**, with two or three ways it could land. Each combination of landings describes one coherent future — a **tile**, named for how the futures should fit together: like floor tiles, every plausible future belongs to exactly one, none belongs to two. Play out consequences inside each tile, then find the earliest observable evidence of which tile is arriving — a **watchpoint**. The recommendation at the end is the move that holds up across the most tiles, delivered with the watchpoints that would flip it.

The chain below runs as questions you ask and answer in the open. Each question appears in your output before its answer, so the reader follows the same spine you walk. Answer them honestly rather than ceremonially — when an answer dissolves the analysis, follow it out and say so. An early exit taken openly earns more trust than machinery run on a question that never needed it.

## Query

`$ARGUMENTS`

## How deep to go

Let the problem pick the depth. A preference for effort — in either direction — makes a poor judge, so depth follows three observable signals:

- **The axis count** (Q3 produces it). Zero axes: answer directly, no machinery. One: a light fork — two tiles, a few sentences each, no tables. Two: the full chain. Three or more: the full chain with hard pruning, because tiles multiply fast.
- **Reversibility**, one notch either way. A sandbox hypothetical steps down; an irreversible or expensive commitment steps up.
- **The asker's register and explicit instruction, which win outright.** "what-if I have an idea for a library — wise investment of care?" asks for a gut-check, and a gut-check that arrives as four tables has failed its asker. When the user names a pace, match it — tone included, playfulness included.

One rule covers everything else: skip any question whose every possible answer would route you to the same next step. Let a skip show as structure — a reader sees which questions you walked — and name a route as observation: "one axis, so two tiles, so two questions." Never narrate a verdict on what the question deserves or what the asker really meant; depth decisions belong in the walking, never in editorial asides about the asker. Depth chosen this way stays honest in both directions — no theater on light questions, no shrug on heavy ones.

## The chain

### Q1. What am I looking at, and what bounds it?

Name the parts, the phases the situation moves through, and the constraints any future must respect. Note what feeds what — a part the asker might abandon may feed a part they plan to keep. The constraints matter most: they are what let you kill impossible futures later instead of politely carrying them.

### Q2. What do I know, and what would help to know?

Sort every forward-looking claim into four piles:

- **Known** — given by the asker, or already verified.
- **Knowable** — verifiable right now with tools at hand. Verify it; never branch on it.
- **Knowable if** — resolvable only by a future event or another party's move. Axis candidates live here.
- **It would help to know** — facts the asker holds: numbers, dates, feelings, context. Catalogue these and ask for them; [references/asking.md](references/asking.md) holds the procedure. When nobody can answer, proceed on a stated assumption per item.

Route on the sort:

- Every pile past "known" and "knowable" sits empty → exit: answer directly, and let the sort itself show why.
- The "knowable if" pile holds anything → Q3.

### Q3. Which of the "knowable if" entries would change what the asker does?

List every candidate in one pass first — seeing them together exposes duplicates and correlation. Then keep only the ones whose resolution would change the recommendation. Those become the axes: two is the sweet spot, three the ceiling.

- None would change anything → exit: the move that ignores them is already the answer; recommend it.
- One or more → onward, at the depth the count selects.

### Q4. Do the axes vary independently?

Needed only with two or more axes. Hold one fixed and check that the other can still land either way. When it can't, the two axes share one underlying unknown — merge them and return to Q3.

### Q5. Which tiles survive?

One tile per combination of axis landings, then prune with reasons rather than vibes:

1. Triage each tile — sure, likely, or impossible — using one step of lookahead plus commonsense. The impossible ones violate a constraint or contradict something already in motion; kill them.
2. Stress the survivors: inside a tile, does each axis landing hold up under the combined pressure of the others? A landing that gets pushed toward its alternative by the rest of the tile marks the tile inconsistent.
3. Give every kill a one-line reason, and give each survivor a name and a two-sentence story of how the world gets there from here. The budget: carry forward at most as many tiles as the walk surfaced open questions — count the entries in Q2's last two piles. A situation that raised eight questions affords eight worlds; one that raised three affords three, however the axes multiply.

### Q6. Does every plausible future land in exactly one tile?

- A future that fits no tile means an axis lacks a landing; extend it.
- A future that fits two tiles means the axes were dependent after all; back to Q3.
- A clean fit → Q7.

### Q7. Inside each tile, what follows from what?

Grow the consequences: first-order, then second. Type every link — leads-to, enables, blocks, amplifies — and resist chaining across types: A enables B and B blocks C establishes nothing between A and C.

When consequence chains from different tiles arrive at the same state, merge them and note which tiles feed it. A consequence most tiles reach is close to inevitable — worth acting on whichever future arrives.

When a link loops back onto its own cause, mark the loop and stop tracing. Feedback dynamics deserve their own pass with their own tools; here they would eat the token budget alive.

### Q8. What would I see first if an axis started to resolve?

For each axis, name the earliest observable evidence that it is breaking one way — an announcement, a date passing, a number crossing a threshold. A good watchpoint passes three tests: **observable** (checkable on a given day), **early** (arrives before the consequences the asker cares about), **discriminating** (one landing predicts it, the other predicts its absence). The flip conditions in your recommendation come from here.

### Q9. Which move survives every tile?

Score the asker's strategies — or derive two to four from the tiles when none were given — against each tile: thrives, survives, or dies. Two probes sharpen the scores: backcast from the tile they want (what must hold at each step for it to arrive?) and premortem the tile they fear (assume it happened; what made it inevitable?).

- One move survives everywhere → refine it once against its weakest tile, recommend it as robust.
- The best move dies in one tile → recommend it as exposed, and name the tile.
- Nothing survives most tiles → Q10.

### Q10. What would buy the answer instead?

When no move holds across the tiles, the decision genuinely turns on a watchpoint that hasn't fired. Recommend the move that buys the information — an extension, an abstraction layer, a phased commitment — and name the date or event that ends the deferral. Even a deferral arrives as a commitment.

## Deliver

Walk the chain out loud, in your own voice, at the depth your route chose. A reader follows the spine of surfaced questions and honest answers, and that visible process is a feature of the response, never overhead. How you phrase each step stays yours; that the steps show themselves is invariant.

Then the ending. Narrative is how a reader encodes a decision to memory, and Q5 already wrote the stories — close by delivering them as one, so the asker feels the worlds diverge before receiving the move that holds across them. Four things land in order, recommendation last, because the last thing on a page commits:

1. **Tell the futures**: walk the named tiles as a short connected story of divergence, in the asker's own terms, harshest world included. When more than one axis ran, follow the telling with a compact recap — a markdown table, or a mermaid diagram where the surface renders one. Place the recap here, between the telling and the commitment, and let it index the story you just told rather than replace it.
2. **Name what holds in every telling**: consequences most tiles reach (from Q7), worth acting on regardless of which future arrives.
3. **Mark the hinges**: each watchpoint from Q8, paired with the switch it triggers — where the story turns, and toward what.
4. **Commit**: a clear recommendation answering the opening question — why this move survives across the tiles, where it runs weakest, robust or exposed. The commitment is invariant; the phrasing is yours. Match the asker's tone, and never pose a dichotomy the situation does not force.

Never close on "it depends." Q10 exists so that even genuine dependency arrives as a committed move with an end date.

Loops marked in Q7 trail the recommendation as open items for a systems-thinking pass.

## Recurse

A walk projects a wide space of unknowns onto the few axes that change the decision, and parks the rest — as knowns, as stated assumptions, as watchpoints. Parked information stays honest only while something can bring it back. Three seams in the chain accept a second entry:

- **Enter a tile.** Promote one tile's landings into Q2's known pile and run the chain again on the decision that remains inside that world. Start with the tile Q9 named as the place the recommendation dies — a walk inside it yields a contingency plan rather than more analysis.
- **A watchpoint fires.** A fired watchpoint means an axis resolved. Rerun from Q2 with that landing moved to known; the tile space halves and the recommendation earns a refresh.
- **Axes overflow.** When Q3 keeps more unknowns than one walk can carry, fix the dominant axis and run one child walk per landing, each inheriting the remaining unknowns as its own Q3 candidates.

An orchestrator splits the chain at its phases: run Q1 through Q6, stop, and hand each tile worth entering to a child walk — live per its watchpoints, or exposed per Q9, never all of them. Aggregate with rules the chain already carries: a consequence most children reach is close to inevitable (Q7's merge), and strategies score across the union of what the children return (Q9). Hold depth at two levels; nesting recovers dimensionality a single walk projects away, and each level stays tellable.

**The unless agent.** Alongside the children, an orchestrator runs one more agent that holds every parked assumption from Q2 and does nothing else. At each checkpoint — tiles formed, consequences grown, recommendation drafted — it asks one question per assumption: unless this still holds, which tile flips? When an assumption breaks, it interrupts the line, and every walk that leaned on the assumption re-enters at Q2 instead of shipping a recommendation built on a dead premise.

## Examples

Read [references/examples.md](references/examples.md) when unsure what a good walk or a wrong turn looks like.

## Sources

- Yao et al., "Tree of Thoughts" (arXiv:2305.10601) — propose candidates together to avoid duplication; triage states as sure/likely/impossible via lookahead; breadth limits; backtracking.
- Besta et al., "Graph of Thoughts" (arXiv:2308.09687) — aggregation merges convergent reasoning paths into one node; refinement loops a thought once through improvement.
- Weimer-Jehle's cross-impact balance analysis (properties in arXiv:0912.5352) — promote/restrict judgments between outcomes; a scenario stays consistent only when each of its outcomes holds against the combined impacts of the others.
- Peter Schwartz, "The Art of the Long View" — scenario planning, predetermined elements, critical uncertainties.
- Fritz Zwicky — morphological analysis and cross-consistency assessment.
- Jerome Glenn, early 1970s — the futures wheel.
- Winston, Chaffin & Herrmann (1987), "A Taxonomy of Part-Whole Relations," Cognitive Science 11(4), 417-444 — the relation types behind Q1, Q2, and the link-typing discipline.
