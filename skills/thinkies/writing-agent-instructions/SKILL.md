---
name: writing-agent-instructions
description: >-
  Write, shorten, or review instructions a model reads and acts on, a rule,
  a system prompt, a CLAUDE.md, an agent file, or a skill body, so that
  every line expands the same way in every reader and covers cases the
  writer never listed. Use whenever someone needs a new instruction from a
  described need or a set of incidents, wants an instruction file shorter
  without dropping a case, or asks whether an instruction or a rewrite
  works, even where they say "tidy", "simplify", "add a rule for this", or
  "why does the agent keep doing X". Triggers: "write a rule for",
  "add this to CLAUDE.md", "turn these incidents into an instruction",
  "compress these rules", "this prompt is too long", "replace these
  bullets with a principle", "collapse these duplicates", "does this
  instruction cover", "did this rewrite lose anything", "review this
  rule".
compatibility: >-
  Floor executor: an agent that can read the target file whole, search it
  for a word, and write markdown tables. No tool beyond read, search, and
  write is needed. Runs on a mid-tier model; every step ends in something
  written down and a check on it.
---

# Writing agent instructions

An instruction is read by a model that meets cases the writer never saw. A list of cases decides only the cases it names, and the reader handles the rest by analogy, which varies from reader to reader. A generator decides them all: a short instruction the reader expands, in its own thinking, into the act for every case in a named set. This skill writes every instruction as a generator, whether it starts from a need, from a list that has grown too long, or from a draft someone wants checked, and proves it by expanding it on cases before it lands.

A generator has four parts. The domain names the set of cases it covers, with a test a reader can run on any candidate. The mapping names the feature of a case that decides the act, and the act for each value. The expansion rule says how the reader turns the mapping into an act, "take the first arm that fits" for one. The anchor is one example at most, placed where the mapping could be read two ways.

## Route first

Decide the mode from the state of the world. Read a mode's reference when you enter it, not before.

- No instruction exists yet, only a need, an incident, or a behavior to capture → **Write**. Read [references/write.md](references/write.md) on entering.
- An instruction exists and holds a list, a run of bans, or near-duplicate lines to shorten → **Compress**. Read [references/compress.md](references/compress.md) on entering.
- An instruction exists and the question is whether it works, or an original and a rewrite exist and the question is what the rewrite lost → **Review**. Read [references/review.md](references/review.md) on entering.
- None of these, as when the file is short and the ask is a wording change → say so and make the change without the procedure.

When a request straddles two modes, "shorten this and tell me if it still works" for one, run Compress and let its checks serve as the review. When you cannot tell which mode fits, ask one question rather than guessing.

Every mode produces the same artifacts, the four parts and the checks below, and differs only in where the cases come from. Close a mode only when its output exists in the shape at the end of this file.

## The checks

Each check ends in a written table or sentence. A mode's reference names which to run and in what order.

**Closure.** Write the domain's membership test in one sentence. Write a clear member, a clear non-member, and a borderline case. The domain passes where the sentence decides the borderline case from what is visible on it. Where only your judgment decides it, add the feature that decided it to the sentence and check again. Where you cannot name a non-member, the domain is everything, and the line is a principle wearing a rule's shape.

**Visibility.** Every feature the mapping names is visible on a case. Where a feature is a judgment, "where the scope is broad" for one, add one sentence beside the mapping that turns it into a test on the case, as in "scope is broad where the prompt names an outcome and leaves the files unnamed". Two readers judge differently and read the same feature alike.

**Trace.** For every case in hand, expand the generator one step by hand and write a row:

```markdown
| case | axis value read off it | arm taken | act the generator yields | result | kept as |
```

The result is "holds" where the yielded act matches the intended act, "bends" where it matches only through a feature the generator does not name or a reading it leaves open, and "misses" where the act differs. Fill the axis value with the actual value, quoted from the case, in every row; a "holds" with that cell empty was never expanded. For each bend, change the generator and rerun the table. For each miss, keep the case's line as residue in one of three forms, written in the last column: an exception arm, placed before the closing arm, where the act differs from the mapping's yield; an attached duty, kept as its own sentence, where the case bundles an extra act, telling someone something for one; a halt from another group, moved to the group it bounds, where the line sat here by proximity. Where a miss fits no form, stop and report it.

One miss has no repair. Where the mapping asks the reader to judge, and the cases name places where that reader's own judgment is known to go wrong, the generator yields the wrong act on exactly those cases, because the one evaluating is the one being corrected. Keep the list of those cases beside the generator, labeled as known misjudgments, and let the generator cover the rest.

**Edge.** Write at least three cases that pass the membership test and that no case in hand named. Expand on each and write a row:

```markdown
| new case | axis value | act the generator yields | another line in the file already decides it | agreement |
```

Every act here is a directive nobody wrote, which is the risk a generator carries: it adds rules without anyone reviewing them. Where another line already decides the case and agrees, note it. Where another line disagrees, add the feature that separates the cases to the mapping and rerun the trace. Where nothing decides it, the row goes to the approval list.

**Two readings.** Expand on the edge cases twice more, once under the most literal reading of the words and once under the most charitable. Where the two reach different acts, find the word whose reading differed and replace it with a test on the case, then rerun the trace.

**Terms.** Search the whole file for every term the generator coins or leans on. Where another part of the file uses the word for something else, rename the term or qualify it into a longer phrase, "a goal premise" in place of "a premise". A reader holding the whole file resolves a word by whichever definition it meets first.

**Tokens.** Where an original exists, keep every token something outside the reader matches by string, byte for byte: headings, identifiers, commands, flags, paths, addresses, tool names, quoted strings, and template keys. Diff the token sets of original and result; a missing token is a defect whatever the accounting says.

**Size.** Count the characters of the generator, its anchor, its glosses, and its residue together against the original group. Where the result runs longer, it earns its place only where it adds an ordering or a closing arm the group lacked.

## Wording

Word each line as the act to take. Where a draft line says "never X", write the act to take in its place, a gate ("X only on Y"), or an omission ("Keep X out of Y"), since a reader acts on what a line names and a ban names only what to avoid. Where a line states a fact, write it as a stance the reader holds, "treat", "count", or "hold". Define each coined term where it first lands. Keep intensifiers out, since a reader weighs every line the same.

## Output

```markdown
## Generator

[the domain, mapping, expansion rule, anchor, and glosses, as they will appear in the file]

## Residue

[each kept line, with its form; "none" where empty]

## Accounting

[the trace table, complete]

## For approval

[each edge row with no line already deciding it, as a yielded act nobody wrote]

## Dropped

[each original line or collected case that neither the generator nor the residue carries, with its meaning named; "none" where nothing drops]

## Size

[characters before and after, where an original exists]
```

Drop nothing silently. Every original line and every collected case appears in the accounting, the residue, or the dropped list.
