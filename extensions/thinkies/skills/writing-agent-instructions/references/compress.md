# Compress

Entered when an instruction exists and holds a list to shorten. The cases come from the list. The gain is real only where the expansion gives back every listed act, so the generator is proved against the list before it replaces anything.

1. Read the whole file first, since a generator written for one group can collide with a term another group uses. Pick one group of lines that share a shape: an enumeration of cases, a run of bans ("Never X. Never Y."), or lines that repeat with one word changed. Write a table with one row per line, quoting the line exactly:

   ```markdown
   | original line | condition | act |
   ```

   The condition is the situation the line fires on. The act is what the line directs or forbids. Where a line has no condition, write "always". Every line in the group has a row, and no cell is empty.

2. Find the axis. The axis is the feature of a case that the act varies with, and it has to be visible on the case, since a reader who must judge it will judge it differently from the next reader. Try these in order and stop at the first that works: the feature the acts vary with, where every act the same means the axis is membership; the feature the banned items share and the permitted items lack; where the act's result ends up afterward. Write one sentence naming the axis and its values. For every row of the table, the axis value can be read off the condition column without adding a judgment. Where any row fails, try the next axis. Where every axis fails, stop and report that the group has no generator and the list stays.

3. Write the four parts. The domain, in one sentence naming the set and its membership test, named by something outside the reader, a tool, a file kind, a syntactic form, or an event. The mapping, in prose where the arms are few and the order is plain, or as a labeled code block where the order decides or the conditions combine with "and" and "or":

   ```lisp
   (cond ((feature-has-value-a case) 'act-a)
         ((feature-has-value-b case) 'act-b)
         (t 'default-act))
   ```

   The expansion rule, in one sentence, where the mapping has more than one arm. The anchor, one example at most, placed where a reader could take the mapping two ways and chosen to rule one way out; a second example turns the pair into the domain's apparent edges, and the reader starts interpolating in place of applying the mapping.

4. Run Closure and Visibility on the four parts.

5. Run Trace on every original line. For each bend, change the generator and rerun from the top of the table. For each miss, keep the line as residue in its form.

6. Run Edge, then Two readings, then Terms.

7. Run Tokens against the original group, then Size. Where Size comes out against the generator, report that the group stays as it is.

8. Emit the output in the skill's Output shape, with the rewritten group as it will appear in the file.

Read [example-compress.md](example-compress.md) when a step's output shape is unclear. It walks one run of bans through every check, with the places the expansion bent marked.
