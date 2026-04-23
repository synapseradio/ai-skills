# Workflow: Refactor CLAUDE.md / System Prompt (Mode B)

Input: an existing CLAUDE.md, system prompt, or instruction document the
user wants refactored. Output: a rewritten document with the same
truth-conditions, plus a coverage report when the instruction count
crosses threshold.

Load this file only when the mode detection in SKILL.md Stage 1 resolves
to **refactor**.

**Critical invariant:** no input instruction gets dropped. This is
enforced structurally via the extract-and-diff mechanism below, not by
aspiration.

---

## Stage 1 — Inventory (refactor mode)

Extract every instruction from the input as a flat list with stable IDs.

**"Instruction" means:** any imperative, prohibition, conditional
directive, stated preference, or factual claim the agent is expected to
act on. Includes:

- Explicit musts/shoulds/nevers
- Disposition statements (*"we value clarity over cleverness"*)
- Named tools, paths, or conventions the agent should use
- Code examples that encode a pattern
- External references (URLs, citations) the agent should trust
- Conditional rules (*"if X, then Y"*)

**Excludes:** narrative connective tissue (*"This file configures Claude
Code for this project"*), section headers alone, pure explanation that
doesn't direct behavior.

### Extraction format

Produce a table as working memory (not emitted — internal):

| ID | Instruction (verbatim or minimal paraphrase) | Source location | Verifiable? |
|---|---|---|---|
| I-01 | "All changes must have tests. No exceptions." | §Technical Standards | yes — test presence |
| I-02 | "Think through failure modes before writing code" | §How You Should Operate | no — judgment |
| I-03 | "Use pnpm, not npm" | §Tools & Conventions | yes — command used |
| ... | ... | ... | ... |

**Numbering:** sequential, stable across the refactor. IDs survive into
the coverage report.

**Verifiability column** informs the temper stage: verifiable
instructions stay as musts; judgment instructions become invitations.

### Count threshold

Count the extracted instructions. If the count is **≥ 10**, the coverage
report will be emitted. If fewer, the report is optional (emit on
request or if the refactor is structurally significant).

## Stage 2 — Shape

Slot every ID into at least one CLAUDE.md section (see
`claude-md-template.md` for the mapping from internal buckets to human
headings).

Produce a coverage mapping as working memory:

| ID | Landed in |
|---|---|
| I-01 | §Technical Standards |
| I-02 | §How You Should Operate > Think Out Loud |
| I-03 | §Tools & Conventions |
| ... | ... |

**Every ID must appear.** An ID missing from this mapping is the exact
failure mode the invariant catches.

**Consolidation is allowed** when instructions are redundant or near-duplicates
— but it must be explicit. Show it as *"I-07, I-12 → §How You Should Operate
bullet 2 (consolidated)"* rather than silently dropping I-12.

## Stage 3 — Temper

Run the anti-pattern lint from `eip-anti-patterns.md` on every phrasing
in the refactored document.

**Critical rule:** register changes, truth-conditions do not. If I-01
says *"All changes must have tests"* and the natural rewrite is *"We aim
for test coverage on changes"*, that's a truth-condition shift — the
original requires, the rewrite suggests. Reject the rewrite.

A valid rewrite for I-01: *"Every change needs a test. When you're
unsure whether existing coverage catches a new edge case, add one —
missing tests on a payment flow cost more than spurious tests."*
Requirement preserved; register softened; reasoning added.

### Truth-condition check

For each rewrite, ask:

- If the original is true of an execution, is the rewrite also true?
- If the original is false, is the rewrite also false?

If either answer is no, the rewrite is wrong — try again.

## Stage 4 — Emit

### Default output structure

Emit two artifacts:

1. **The refactored CLAUDE.md**, using human headings
   (see `claude-md-template.md`)
2. **A coverage report** (emitted if instruction count ≥ 10; otherwise
   optional)

### Coverage report format

The fenced block below shows the *template* — emit the contents as
markdown following the refactored CLAUDE.md, not inside a code block:

```markdown
## Coverage Report

All N instructions from the source were preserved. Mapping:

| ID | Instruction (source phrasing) | Landed in |
|---|---|---|
| I-01 | "All changes must have tests. No exceptions." | §Technical Standards, bullet 1 |
| I-02 | "Think through failure modes before writing code" | §How You Should Operate > Reliability First |
| ... | ... | ... |

Consolidations:
- I-07 + I-12 merged into §How You Should Operate > Build Incrementally
  (both said "deliver one piece at a time" in different words)

Relaxations:
- None

Additions (new content not in source):
- §Common Situations > When You Hit a Wall (derived from principles 1 + 6;
  optional — remove if you want strict preservation only)

To verify: cross-check each source-phrasing column against your original
CLAUDE.md before committing the rewrite.
```

**"Relaxations" surface truth-condition shifts** that were unavoidable or
that the skill couldn't resolve. Any entry here is a flag for user
review.

**"Additions" surface content the skill added** (typically disposition
subsections that apply EIP principles the source lacked). The user can
remove them if they want strict preservation.

### User confirmation

After emit, if the instruction count was **≥ 15** (large refactor), use
`AskUserQuestion` to offer a confirmation step:

> Options:
>
> 1. Looks good — write the new CLAUDE.md to [path]
> 2. Show me the relaxations and additions in more detail
> 3. Don't write yet — let me review the coverage report

For smaller refactors, emit directly and let the user verify by eye.

## Stage 5 — Verify (self-check before handoff)

Before declaring done, run:

- [ ] Every ID in the extraction table appears in the coverage mapping
- [ ] No ID is silently consolidated (consolidations are explicitly noted)
- [ ] The temper lint passes on every section
- [ ] Literal content (code blocks, paths, URLs) is preserved verbatim
- [ ] The "Relaxations" column is empty or user-surfaced
- [ ] The output has no pep-stapled warmth (#7 check)

Any failure at this step blocks emit.

## Edge Cases

| Situation | Response |
|---|---|
| Source is already EIP-aligned | Report that, optionally suggest 2-3 small improvements, don't rewrite wholesale |
| Source contains contradictions | Surface them via `AskUserQuestion` before refactoring — don't silently pick |
| Source contains outdated content (dead links, removed tools) | Flag, don't auto-remove |
| Source is enormous (>500 lines) | Split the extraction into sections; consider proposing a scoped rewrite of one section at a time |
| Source references external files that aren't accessible | Preserve the reference verbatim; note the unverifiable claim |
| Source is clearly drafted by a previous AI with anti-pattern hits | Note that in the coverage report; some rewrites may feel substantial |

## What Not to Do

- Do not "improve" literal content (code examples, command invocations).
  Preserve them verbatim unless the user asked for a code update.
- Do not drop instructions that feel redundant without noting the
  consolidation explicitly.
- Do not add disposition language the user didn't ask for without flagging
  it as an Addition.
- Do not lengthen the file. A good refactor often *shortens* CLAUDE.md —
  EIP register is usually tighter than command register.
