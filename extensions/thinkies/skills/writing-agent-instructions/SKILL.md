---
name: writing-agent-instructions
description: >-
  Any agent instruction in any agent executable context. Use it before the
  instruction exists, to write it from a need or an incident, and on an
  instruction that exists or was just drafted, to refine it, so that every
  line expands the same way in every reader and covers cases the writer
  never listed.
compatibility: >-
  Floor executor: an agent that can read the target file whole, search it
  for a word, and write markdown tables. No tool beyond read, search, and
  write is needed. Runs on a mid-tier model; every step ends in something
  written down and a check on it.
---

# Writing agent instructions

## How an instruction works

An instruction is read by a model that meets cases the writer never saw. Hold the instruction as a few relations the reader evaluates on the case in front of it, and the acts it yields as the smallest set the text derives. A list of cases derives only its rows, and the reader handles the rest by analogy, which varies from reader to reader. A generator derives the rows and every case between them, the same way in every reader, because each reader runs the same test on the same visible features.

The writer's work is to name the set, name the feature that decides the act, say how the arms combine, and then trust the reader's expansion while proving it: expand the text by hand on the cases in hand and on cases nobody listed, and show every act the text derives that nobody asserted, before it lands. A derived act nobody wrote goes to the approval list, never silently in.

A generator has four parts. The domain names the set of cases it covers, with a test a reader can run on any candidate. The mapping names the feature of a case that decides the act, and the act for each value. The expansion rule says how the reader turns the mapping into an act, "take the first arm that fits" for one. The anchor is one example at most, placed where the mapping could be read two ways.

## Route first

Decide the route from the state of the world. Read a route's reference when you enter it, not before.

- No instruction exists yet, only a need, an incident, or a behavior to capture → **Write**. Read [references/write.md](references/write.md) on entering. Write ends by entering Refine with its draft.
- An instruction exists, or a draft was just written, and it should say the most in the least space, or the question is whether it works or what a rewrite lost → **Refine**. Read [references/refine.md](references/refine.md) on entering.
- Neither, as when the file is short and the ask is a wording change → say so and make the change without the procedure.

When you cannot tell which route fits, ask one question rather than guessing.

Both routes end in the same artifacts, the four parts and the checks in [references/checks.md](references/checks.md), and differ only in where the cases come from. Close a route only when its output exists in the shape at the end of this file.

## Wording

Word each line as the act to take. Where a draft line says "never X", write the act to take in its place, a gate ("X only on Y"), or an omission ("Keep X out of Y"), since a reader acts on what a line names and a ban names only what to avoid. Name a feature in the negative only where the feature is already defined on the page. Where a line states a fact, write it as a stance the reader holds, "treat", "count", or "hold". Define each coined term where it first lands. Keep intensifiers out, since a reader weighs every line the same.

## Output

```markdown
## Generator

[the domain, mapping, expansion rule, anchor, and glosses, as they will appear in the file]

## Residue

[each kept line, with its form; "none" where empty]

## Accounting

[the trace table, complete]

## Disagreements

[where a rewrite was handed in: each trace row where your expansion and the rewrite's own accounting differ; leave the heading out otherwise]

## For approval

[each edge row with no line already deciding it, as a yielded act nobody wrote]

## Dropped

[each original line, pruned line, or collected case that neither the generator nor the residue carries, with its meaning named; "none" where nothing drops]

## Size

[characters before and after, where an original exists]
```

Drop nothing silently. Every original line and every collected case appears in the accounting, the residue, or the dropped list.
