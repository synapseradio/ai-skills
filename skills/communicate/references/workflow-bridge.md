# Bridge Workflow

Translanguaging — drawing on the writer's full linguistic repertoire — for thoughts that resist English expression. Output is bilingual with annotated loss, not translation.

**Boundary with the Structure workflow:** Bridge handles thoughts that live in another language and need rendering with annotated loss. Structure handles prose already in the target language whose argument architecture follows another rhetorical tradition. If both apply, run Bridge for the rendering and Structure for the architecture.

Works standalone or as an interrupt. When a thought resists English expression mid-workflow, load this file for the stuck passage, then return to the active workflow.

## Input

Accept any of:

- A rough idea in English: "what I want to say is…"
- An L1 phrase or sentence
- A mix: "in Korean we say *jeong* — how do I say that?"
- Prose that does not sound right in English despite being grammatically correct

If the source language is not stated and not obvious from script or content, ask. Never produce bilingual output without naming the source.

## Phase 1: Identify the gap

Read [across-languages.md](./across-languages.md) and run the self-interrogation questions for the passage. Determine which gap or gaps operate:

- **Grammatical ontology** — L1 encodes a distinction English collapses
- **Rhetorical convention** — L1 organizes the argument differently than English expects
- **Conceptual lacuna** — the concept has no clean English lexical equivalent
- **Pragmatic convention** — L1 has different norms for directness, hedging, or relational positioning

Often more than one gap operates. Name each that applies.

## Phase 2: Render

Produce bilingual output:

```text
### In [Source Language]
[L1 version, or "[generated from your description]" if not user-provided]

### In English
[English version]

### What Shifted
- [What this English cannot preserve from the L1]
- [Where the English requires explicit content the L1 leaves implicit]
- [Where the mapping is clean and what survives]
```

Each annotation names the **ontological** difference, not just the lexical one. Not "Spanish uses *tener* here," but "Spanish encodes this emotion as something carried, not inhabited; the self stays separate from the feeling. English collapses that."

## Phase 3: Offer a direct version (conditional)

Offer a simplified English rendering only when:

- The audience is known to be low-context (American business, technical readers)
- The user explicitly asks for "more natural English"
- The annotated version retains L1 structures that may confuse the reader

Always name what the direct version sacrifices:

```text
### Direct English (optional)
[Simplified version]

### What This Version Sacrifices
[Specific rhetorical move, ontological distinction, or relational positioning lost]
```

The direct version is a tradeoff. Frame it that way.

## NEVER

- **Never produce a false equivalent.** When no clean mapping exists, say so and offer a gloss.
- **Never offer the direct version without naming what it sacrifices.** The trade-off is the point of Phase 3.

For cross-cutting rules (hedging split, friction, gaps, L1 patterns, tradition), read [never.md](./never.md).
