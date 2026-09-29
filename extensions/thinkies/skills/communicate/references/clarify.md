# Clarify

Fits when: the audience meets terms, concepts, or steps it has not met before

Audit prose for clarity issues and apply fixes across structure, content, and expression dimensions.

## Diagnostic Question

Ask: Can someone in this audience who is new to the domain follow linearly without backtracking, where the piece means them to?
Where, if anywhere, do concepts appear before their foundations? Where, if anywhere, do sentences open with unfamiliar content before anchoring on familiar ground?

## Instructions

1. **Identify the target** - Determine what prose to audit: text provided directly, a referenced file, or recent output in the conversation. State the target and its approximate scope.

2. **Run the structural audit** - Check how information is organized:
   - **Sequence**: Mark where concepts are referenced before introduced, or conclusions appear before supporting details
   - **Information flow**: Identify sentences that open with unfamiliar content before anchoring on familiar ground
   - **Find gaps**: Mark undefined terms, logical leaps, and claims that assume knowledge not established
   - **Trace prerequisites**: List what the audience must already understand; mark where prerequisites are assumed but not stated

3. **Run the content audit** - Check whether difficulty is essential or accidental:
   - **Streamline**: Count phrases that restate what the sentence already says, and find words whose deletion leaves the meaning, register, and sound unchanged
   - **Load type**: Categorize difficulty as extraneous (from the wording rather than the subject—cut it), intrinsic (from complex subject—preserve with scaffolding), or germane (builds understanding—preserve)
   - **Reveal mechanism**: Find claims that assert without explaining how or why
   - **Ground quantifiers**: Find quantifiers ("many", "significant", "few") where actual numbers would strengthen, and leave a word the form sets as a standard for its audience to apply, such as a contract's "prompt" or "reasonable"

4. **Run the expression audit** - Check whether language creates friction:
   - **Presence**: Find absence-based language ("don't", "avoid", "not") and ask whether the audience needs a direction to move or the prohibition itself
   - **Referent track**: Trace each pronoun and demonstrative to its antecedent; mark ambiguous or distant references

5. **Apply fixes in priority order** - Fix structural issues first (they often resolve content and expression issues):
   - Reorder for sequence, restructure for information flow, fill gaps
   - Streamline, add mechanism, ground quantifiers
   - Convert to presence where a direction serves, clarify referents
   - Preserve intrinsic complexity with scaffolding rather than simplifying

6. **Present the result** - Output the improved prose and summarize what changed: structural issues fixed, content streamlined, expression issues resolved, complexity preserved.

## Questions

- Where, if anywhere, does this passage assume a foundation it has not given the audience — a concept, a definition, a context, an earlier event in the chain?
- Where, if anywhere, does a sentence open on the unfamiliar before the familiar is in place to anchor it?
- For each qualifying or introductory phrase, what claim, if any, does it carry?
- For each quantifier — "many," "often," "significant," "soon" — do I have the number, duration, or comparison that would make it concrete, or is the word a standard the form leaves open on purpose, as a contract's "prompt" is?
- For each claim that asserts an effect, does the prose name the mechanism — through what process, by what means, in what intermediate steps — or is the audience being asked to take it on faith?
- Where the passage is difficult, how much of the difficulty comes from the subject itself, and how much from the wording?
- For each negation, what does the audience need from it: the prohibition itself, as in a contract or a warning, or a direction to move?
- Trace each pronoun and demonstrative back to its anchor. Where, if anywhere, does the trace stretch across several sentences, or split between two possible antecedents?

## Quality Criteria

When clarity is sound:

- [ ] Each concept is introduced before it is referenced, or the form holds it back on purpose, as a mystery or a delayed turn does.
- [ ] Each sentence opens on ground the audience has been given, where the piece does not mean to disorient them.
- [ ] Each quantifier the audience will rely on is backed by the specific number, duration, or comparison the writer can stand behind.
- [ ] Each claim that asserts an effect the audience must act on or evaluate names how the effect happens.
- [ ] Difficulty in the prose comes from difficulty in the subject, and the surrounding scaffolding helps the audience carry it.
- [ ] Each negation that remains is the point itself, such as a prohibition in a contract or a warning in a recipe, or has given way to a direction.
- [ ] Each pronoun and demonstrative traces to one antecedent, where the piece does not mean it to stay open.
- [ ] When repair lands across multiple layers, the structural fixes were made first, and the word-level fixes built on those.

## Additional Resources

For detection heuristics, repair strategies, and domain-specific patterns: [`clarify-patterns.md`](./clarify-patterns.md).
