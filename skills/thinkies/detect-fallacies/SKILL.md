---
name: detect-fallacies
description: Use when an argument persuades yet leaves a doubt, or before accepting or publishing one. Names the logical errors in it, such as a false dichotomy or correlation read as causation, and shows how to repair the reasoning.
---

## Steps

### 1. Identify the argument

Target: `$ARGUMENTS`, else the argument in the current context.

When no argument was passed, read "the current context" as the page: the last reply, or the document in hand. Where the page holds no argument, ask for one and stop.

### 2. Examine the argument structure

Write out the claim, the premises offered for it, and how the premises are meant to reach the claim.

### 3. Check for common fallacy patterns

- **False dichotomy**: either/or when other options exist
- **Slippery slope**: claiming A inevitably leads to Z
- **Ad hominem**: attacking the person instead of the argument
- **Straw man**: misrepresenting a position to defeat it easily
- **Appeal to authority**: expert opinion substituting for evidence
- **Correlation as causation**: assuming correlation proves causation
- **Hasty generalization**: broad conclusions from limited examples
- **Circular reasoning**: using the conclusion as a premise
- **Appeal to emotion**: using fear or sympathy instead of logic
- **Survivorship bias**: observing only successes, ignoring failures

The list prompts the search and does not bound it. Describe any other flaw by what it does to the argument.

### 4. Identify the specific flaw

For each candidate, point to the step where the logic breaks, what it assumes wrongly, and what relevant information it ignores or hides.

### 5. Check whether the reasoning is actually valid

Steelman each candidate before it becomes a finding: does context, domain knowledge, or a non-obvious valid inference justify what looks fallacious? Drop the candidates the charitable reading clears, and say why each was dropped.

### 6. Explain the problem and suggest corrections

For each finding that survives, show why the reasoning fails, give a counter-example where one helps, and say how the argument could be repaired.

## Return

Return the argument as claim and premises, each surviving fallacy with the passage where it sits and why it fails, the candidates dropped in step 5, and a corrected version of the argument. Where no candidate survives, report that the argument commits none of these fallacies. The run is done when every candidate is either a finding or dropped.
