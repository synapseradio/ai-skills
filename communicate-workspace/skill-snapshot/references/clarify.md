# Clarify

Audit prose for clarity issues and apply fixes across structure, content, and expression dimensions.

## Diagnostic Question

Ask: Can a reader unfamiliar with this domain follow linearly without backtracking?
Where do concepts appear before their foundations? Where do sentences open with unfamiliar content before anchoring on familiar ground?

## Instructions

1. **Identify the target** - Determine what prose to audit: text provided directly, a referenced file, or recent output in the conversation. State the target and its approximate scope.

2. **Run the structural audit** - Check how information is organized:
   - **Sequence**: Mark where concepts are referenced before introduced, or conclusions appear before supporting details
   - **Information flow**: Identify sentences that open with unfamiliar content before anchoring on familiar ground
   - **Find gaps**: Mark undefined terms, logical leaps, and claims that assume knowledge not established
   - **Trace prerequisites**: List what readers must already understand; mark where prerequisites are assumed but not stated

3. **Run the content audit** - Check whether difficulty is essential or accidental:
   - **Streamline**: Count redundant phrases, identify ceremonial language that adds words without meaning
   - **Load type**: Categorize difficulty as extraneous (from poor expression—cut it), intrinsic (from complex subject—preserve with scaffolding), or germane (builds understanding—preserve)
   - **Reveal mechanism**: Find claims that assert without explaining how or why
   - **Ground quantifiers**: Find vague quantifiers ("many", "significant", "few") where actual numbers would strengthen

4. **Run the expression audit** - Check whether language creates friction:
   - **Presence**: Find absence-based language ("don't", "avoid", "not") that could point toward action instead
   - **Referent track**: Trace each pronoun and demonstrative to its antecedent; mark ambiguous or distant references

5. **Apply fixes in priority order** - Fix structural issues first (they often resolve content and expression issues):
   - Reorder for sequence, restructure for information flow, fill gaps
   - Streamline, add mechanism, ground quantifiers
   - Convert to presence, clarify referents
   - Preserve intrinsic complexity with scaffolding rather than simplifying

6. **Present the result** - Output the improved prose and summarize what changed: structural issues fixed, content streamlined, expression issues resolved, complexity preserved.

## Examples

### Streamlining bloated technical prose

**Input**: "The architecture was designed for scalability and is built to handle increasing demands over time, providing a foundation that can accommodate future requirements and expanding needs as usage grows and more features are added."

**Audit findings**:

- Streamline: 43 words to express one idea. "Scalability", "increasing demands", "expanding needs", "usage grows" all mean "grows"
- Load type: Extraneous—difficulty is ceremonial, not essential
- Mechanism: Missing. How does the architecture scale?

**Fixed output**: "The architecture scales horizontally by adding nodes as load increases."

**Summary**: Streamlined from 43 words to 10. Added mechanism (horizontal scaling via nodes). Preserved the core claim while making it concrete.

### Fixing information flow in documentation

**Input**: "A distributed lock using Redis prevents race conditions. The inventory service needs this because multiple instances handle concurrent checkout requests."

**Audit findings**:

- Information flow: Opens with solution (distributed lock) before establishing problem
- Sequence: Cause (concurrent requests) follows effect (race conditions)

**Fixed output**: "Multiple instances of the inventory service handle concurrent checkout requests. Without coordination, race conditions corrupt stock counts. A distributed lock using Redis prevents this."

**Summary**: Reordered to establish problem (concurrent requests → race conditions) before solution (distributed lock). Each sentence now opens with familiar ground.

## Additional Resources

For detection heuristics, repair strategies, and domain-specific patterns:

- **`clarify-patterns.md`** — Detailed patterns for each audit technique
- **`clarify-examples.md`** — Before/after transformations organized by issue type
