# Write

Entered when no instruction exists yet, only a need, an incident, or a behavior to capture. The cases come from the conversation. An instruction written without a case table is a guess at its own domain, so the table comes before any wording.

1. Name the reader and the cost. Write one sentence saying which model reads this, what it acts on, and what a wrong act costs whoever meets the result. The domain sentence will name the set of acts this covers.
2. Collect the cases. List every situation the instruction must decide, from the conversation, the incidents that prompted it, and the examples given, as a table of condition and act. Add the situation that prompted the ask as the first row. Then ask what else the same reader meets in the same set, and add those rows, since the ask names one incident and the instruction covers a domain.
3. Find the axis. Ask what feature of the case the act varies with, trying in order the feature the acts vary with, the feature the forbidden items share and the permitted lack, and where the act's result ends up afterward. Where every act is the same, the axis is membership. Where no axis is visible on the cases, write the cases as arms under one domain sentence and say so.
4. Write the four parts. Put the domain first, as "For every X". Write the mapping in prose where the arms are few and the order is plain, as a labeled code block where order decides or conditions combine with "and" and "or", or as clauses where an arm's result is itself a case another arm reads, as [refine.md](refine.md) step 5 shows. Close with "Otherwise". Give one anchor at most.
5. Word each line as the Wording section of the skill says.
6. Enter Refine at its step 3, with the table from step 2 as the case table, and run it to its output.

Read [example-write.md](example-write.md) when the shape of step 2 or 3 is unclear. It walks one incident into a domain, with the places the expansion bent marked.
