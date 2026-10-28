# The checks

Each check ends in a written table or sentence. A route's reference names which to run and in what order.

**Closure.** Write the domain's membership test in one sentence. Write a clear member, a clear non-member, and a borderline case. The domain passes where the sentence decides the borderline case from what is visible on it. Where only your judgment decides it, add the feature that decided it to the sentence and check again. Where you cannot name a non-member, the domain is everything, and the line is a principle wearing a rule's shape.

**Visibility.** Every feature the mapping names is visible on a case. Where a feature is a judgment, "where the scope is broad" for one, add one sentence beside the mapping that turns it into a test on the case, as in "scope is broad where the prompt names an outcome and leaves the files unnamed". Two readers judge differently and read the same feature alike. Everything the act names is bound by a feature the domain or the mapping names. An act that names what no feature binds, a person to tell or a place to report to, leaves the reader to supply it, and two readers supply it differently. A body predicate with no defining clause is a fact the reader reads off the case; gloss it beside the mapping.

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
