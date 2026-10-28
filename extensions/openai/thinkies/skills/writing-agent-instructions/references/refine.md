# Refine

Entered when an instruction exists or a draft was just written. The cases come from the lines of the group, or from the case table Write hands over. The gain is real only where the expansion gives back every act the group carried, so the generator is proved against the group before it replaces anything. Where the ask is a judgment, the route runs through step 6 and stops at step 7 without changing anything, and the output holds findings.

1. Read the whole file first, since a generator written for one group can collide with a term another group uses. Pick one group of lines that share a shape: an enumeration of cases, a run of bans ("Never X. Never Y."), or lines that repeat with one word changed. Where a rewrite was handed in with its original, list every token something outside the reader matches by string, headings, identifiers, commands, flags, paths, addresses, tool names, quoted strings, and template keys, as the set the result must keep.

2. Prune. Write a table with one row per line of the group, quoting the line exactly:

   ```markdown
   | original line | verdict | test that gave it |
   ```

   The verdict is one of five. Live: the line decides a case no other line in the group decides. No-op: the rest of the group yields the same act on the line's case with the line absent; write the act the rest yields. Duplicate: another line carries the same meaning; name that line. Cache: the line restates what a lookup in the environment returns, a config file, a help text, a directory listing; name the lookup. Stale: the line describes a behavior or a world that no longer holds; name what changed. Every row whose verdict is not live goes to Dropped with its meaning named. Live rows go on.

3. Write the case table over the live lines, quoting each line exactly:

   ```markdown
   | original line | condition | act |
   ```

   The condition is the situation the line fires on. The act is what the line directs or forbids. Where a line has no condition, write "always". Every live line has a row, and no cell is empty. Where Write enters here, its case table is this table.

4. Find the axis. The axis is the feature of a case that the act varies with, and it has to be visible on the case, since a reader who must judge it will judge it differently from the next reader. Try these in order and stop at the first that works: the feature the acts vary with, where every act the same means the axis is membership; the feature the banned items share and the permitted items lack; where the act's result ends up afterward. Write one sentence naming the axis and its values. For every row of the table, the axis value can be read off the condition column without adding a judgment. Where any row fails, try the next axis. Where every axis fails, stop and report that the group has no generator and the list stays.

5. Write the four parts. The domain, in one sentence naming the set and its membership test, named by something outside the reader, a tool, a file kind, a syntactic form, or an event. The mapping, in prose where the arms are few and the order is plain, or as a labeled code block where the order decides or the conditions combine with "and" and "or":

   ```lisp
   (cond ((feature-has-value-a case) 'act-a)
         ((feature-has-value-b case) 'act-b)
         (t 'default-act))
   ```

   Where an arm's result is itself a case another arm reads, a chain for one, write the mapping as clauses:

   ```text
   marked(L) :- carries_mark(L).
   marked(L) :- rests_on(L, K), marked(K).
   ```

   Clauses of one head are read in order; the first body that holds decides. The expansion rule, in one sentence, where the mapping has more than one arm. The anchor, one example at most, placed where a reader could take the mapping two ways and chosen to rule one way out; a second example turns the pair into the domain's apparent edges, and the reader starts interpolating in place of applying the mapping.

6. Read [checks.md](checks.md). Run Closure and Visibility on the four parts. Run Trace on every live line. Where a rewrite was handed in, run Trace with the rewrite's generator over the original's table, and keep each row where your expansion differs from the rewrite's own accounting for the Disagreements section. For each bend, change the generator and rerun from step 3. For each miss, keep the line as residue in its form. Run Edge, then Two readings, then Terms. Run Tokens against the original group, then Size. Where Size comes out against the generator, report that the group stays as it is.

7. Where the ask was a judgment, emit the Output shape with the Generator section holding the parts as found, each failed check with its evidence, and change nothing. Otherwise emit the Output shape with the rewritten group as it will appear in the file.

Read [example-refine.md](example-refine.md) when a step's output shape is unclear. It walks one run of bans through every step, with the places the expansion bent marked.
