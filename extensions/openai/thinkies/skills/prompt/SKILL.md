---
name: prompt
description: Use when writing or revising a prompt for another model or agent, a delegation prompt
  included. Produces a clear, well-structured prompt from a request, or reworks an existing one while
  preserving every instruction it carries.
---

# Prompt

Write a new prompt, or restructure an existing one, into the fixed scaffold in [`assets/template.md`](assets/template.md). The reader of the artifact is a model that holds nothing but the artifact, so everything it needs sits inside it, and in a refactor every instruction the source carried is still there afterwards.

Keep the artifact as short as its content allows, with sections light enough that the reader can adapt them to the case in front of it.

## Pick the mode

- **Refactor**: the input holds an existing prompt or instruction file, such as a pasted prompt or a CLAUDE.md, and asks for it to be improved or restructured.
- **Seed**: anything else. The prompt is written from the conversation.

Where the input could be either, run seed and say so in the assumption note on the artifact's first line.

## Inventory the input

Identify what the input contains before writing anything.

In seed mode, gather signal from the conversation. Note the task verb, the domain, any files referenced, constraints stated, register requested, audience implied, and stakes. List ambiguities worth surfacing to the user.

In refactor mode, extract every instruction in the source as a flat list with stable IDs (I-01, I-02, ...). The list is the preservation contract: the register may change, and each requirement stays exactly as the source states it, because the source's author decided it and the refactor has no standing to decide it again. Every ID ends up in at least one section of the output, or it has been dropped.

## Shape into the template

Load [`assets/template.md`](assets/template.md) and fill its sections from the inventory.

Stakes content sits at the close of the Task section. Name what is at risk and why this matters. The artifact has no separate Why section.

Where a section has no real content, write a one-line gap note that names the absence, for example: "No prior context identified — agent works from conversation signal alone." A gap note tells the reader the truth about what it holds; filler would have it act on content nobody supplied.

In refactor mode, every extracted instruction ID lands in at least one section, recorded as one row of the accounting table:

```markdown
| id | instruction | where it lands | result | kept as |
```

Quote the source instruction and the destination line in every row; a "holds" without a quoted destination was never checked. The result is "holds" where the destination carries the instruction's truth-conditions, "bends" where it carries them only under a reading the output leaves open, and "misses" where it dropped or changed them. "Kept as" says how the instruction survived: verbatim, rephrased, or consolidated with the IDs it shares a destination with. A consolidation is rows sharing one destination. A row with an empty "where it lands" cell is a dropped instruction, and its result is "misses".

Repair every bend in the draft and re-check its row before emitting. Repair every miss the draft can carry; a miss that remains is surfaced at emit.

## Lint the draft

Load [`references/eip-anti-patterns.md`](references/eip-anti-patterns.md) and read every phrasing in the draft against the patterns it lists.

For each hit, rewrite the phrasing only. The lint targets register, and the requirement underneath stays as it was. "You must write tests for every function" becomes "Every function needs a test. Missing tests in a payment system cost more than spurious tests."

Write the natural phrasing first, then check it against the catalog. A rewrite changes phrasing and leaves structure and the underlying instruction alone. Alignment is what remains after the lint passes; warmth pasted on top of an unaligned prompt does not produce it.

## Emit

Output only the artifact, with no preamble, postscript, surrounding commentary, or closing question, since the output is often pasted or passed straight to the model it addresses.

- Where the user supplied a path, write the file directly.
- Where they did not, display the artifact inline.

Never fabricate file paths, scripts, or tools that the surrounding context has not established. The reader will go looking for each one.

Where a required assumption was made, note it on the first line of the artifact, in place of commentary around it.

In refactor mode, fill the accounting table against the draft as it stands after the lint, since a rewrite of phrasing can change a row's result.

In refactor mode, where the extracted list holds more than 15 instruction IDs or any row still misses, show the accounting table and ask the user to confirm before writing the file. Name each miss and what it dropped or changed. Where nobody can answer, return the artifact inline with the table and leave the file unwritten. Other refactors and seeds emit without asking.

Where the user has indicated downstream subagent evaluation, keep section boundaries clear and place the accounting table in a fenced block.

## Edge cases

- **One specific tweak to a pasted prompt**: run the full lint anyway, and emit a minimal diff. Preserve the choices the user did not ask to revisit.
- **A prompt that is already aligned** and would survive the lint untouched: say so plainly and skip the rewrite. A rewrite with nothing to fix only adds risk of a dropped instruction.
- **A source prompt that contradicts itself**: put the contradiction to the user, through a question tool where one exists, and hold the rewrite of that part until they answer. Where nobody can answer, keep both instructions as written and name the contradiction with both readings on the artifact's first line. Choosing a side silently would decide a requirement that belongs to the source's author.
- **A requested register the lint would flag**, such as terse command style for a one-shot formatter: honor it and name which patterns the requested style relaxes. Domain register wins over universal lint.

## References

[`assets/template.md`](assets/template.md) — the artifact scaffold. Load during shape; the output fills it.
[`references/eip-anti-patterns.md`](references/eip-anti-patterns.md) — the anti-pattern catalog with detection hints and rewrite patterns. Load every run.
[`references/eip-principles.md`](references/eip-principles.md) — the principles each anti-pattern derives from. Load when a rewrite needs grounding.
