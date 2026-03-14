# Bridge Workflow

Translanguaging — drawing on a writer's full linguistic repertoire as an integrated system — not translation. Translation optimizes for target-language correctness. This workflow optimizes for semantic fidelity: what must survive from the source framing, and what is necessarily lost in the English rendering.

The gap between a clear idea and its English expression is often not vocabulary but ontology. The idea may live in a grammatical framework, a rhetorical convention, or a conceptual frame that English cannot accommodate without loss. This workflow names that loss explicitly rather than smoothing it away.

Works standalone or as an interrupt during any active workflow. When a thought resists English expression mid-workflow, load this file for the stuck passage, then return to the active workflow.

## The Four Gaps

**1. Grammatical ontology gap** — The native language encodes a distinction English collapses. Spanish ser/estar splits "to be" into essential vs. transient states — "es triste" (sad by nature) vs. "esta triste" (sad right now). Japanese particles ne/yo/kana encode the speaker's epistemic relationship to the claim and the listener. Arabic verbal morphology encodes aspect and agency patterns English approximates only through separate clauses.

**2. Rhetorical convention gap** — The native tradition organizes argument differently than English expects. Arabic parallel-restatement builds meaning through accumulation; French thesis-antithesis-synthesis holds contradiction before resolving it; Japanese indirection moves toward implication rather than assertion. The structure is not disorganization — it is method.

**3. Conceptual lacuna** — The concept exists in L1 but has no direct English lexical equivalent. Portuguese *saudade* (longing for what is absent), Japanese *wabi-sabi* (beauty in impermanence), Arabic *tarab* (musical ecstasy that transcends listening), German *Schadenfreude*, Spanish *duende* (dark creative force). English approximations carry different connotations.

**4. Pragmatic convention gap** — The native language has different norms for directness, hedging, formality, or relational positioning. Japanese sentence-final particles encode relational care; high-context traditions communicate refusal through what is not said; French subordinate clause accumulation signals epistemic rigor, not indecision.

## How to Use This Workflow

Accept any input format:

- A rough idea in English ("what I want to say is...")
- An L1 phrase or sentence to express in English
- A mix ("in Arabic we say X — how do I say that in English?")
- A passage that "doesn't sound right" in English despite being grammatically correct

## Phase 1: Receive

Accept the user's rough idea. If the following are not already provided, ask:

- What is the thought to express?
- What language was it thought in (if not evident)?
- Is there a phrase in the native language that captures it, even roughly?

### Native Language Detection

Priority order:

1. User states it explicitly ("in Spanish we say...")
2. User provides L1 text (detect from script/orthography)
3. User describes the concept and its tradition ("in Japanese, there's a concept of...")
4. If unclear: ask directly — "What is the first language, or the language this idea lives in?"

Never attempt the bilingual output without knowing the source language.

## Phase 2: Identify

Determine which gap type is operating. Often more than one.

1. **Grammatical ontology** — Does L1 encode a distinction English collapses? (ser/estar, tener + emotion, particle systems, verbal morphology)
2. **Rhetorical convention** — Does L1 tradition organize the thought differently than English expects? (parallel structure, dialectical framing, indirection)
3. **Conceptual lacuna** — Does the concept lack a direct English lexical equivalent?
4. **Pragmatic convention** — Does L1 have different norms for directness, hedging, or relational positioning?

Load `@./references/tradition.md` to identify which tradition's conventions shape the source thought.

For detailed gap examples by language tradition, consult `@./references/language-patterns.md`.

## Phase 3: Bridge

Produce bilingual output following this structure:

### In [Native Language]

The thought as the user would express it in their L1. If the user has already provided this, use it. If not, generate a likely L1 rendering based on what they have said. Mark as [generated] if not user-provided.

### In English

The thought rendered in natural English. Annotate differences:

- Where English collapses a distinction the L1 preserves
- Where English requires explicitness that the L1 leaves implicit (high-context to low-context)
- Where English rhetorical norms differ from L1 (thesis-first vs. dialectical vs. parallel)
- Where an L1 idiom was rendered as a functional equivalent with different connotations

### What Shifted

Explicitly name what shifted, what was lost, what was preserved differently. If the mapping is clean, say so. If no clean mapping exists, say so explicitly rather than producing a false equivalent.

Every annotation names the **ontological** difference, not just the linguistic one:

- Not: "Spanish uses tener here"
- But: "Spanish encodes this emotion as something you carry rather than something you are — the self remains separate from the feeling. English collapses this distinction."

For the full ontological framing approach, consult `@./references/translanguaging-guide.md`.

## Phase 4: Offer Third (Conditional)

Offer a simplified/direct English version when:

- The English version retains L1 clause structures that may confuse a low-context English reader
- The target audience is known to be low-context (American business, academic English)
- The user asks for a "more natural English" rendering explicitly

When offering the third version, always flag what it sacrifices:

- "This version removes the dialectical framing. The original showed holding both positions before committing — the direct version loses that intellectual move."
- "This version converts 'I have fear' to 'I am afraid.' The original encodes emotion as something carried rather than something inhabited — the English version loses that."

The third version is a tradeoff, not an upgrade. Frame it as such.

### Direct English (optional)

[Simplified version]

### What This Version Sacrifices

[Explicit statement of what was lost — the rhetorical move, the ontological distinction, the relational positioning]

## Output Format

```text
### In [Native Language]
[L1 version — or "[generated based on your description]" if not user-provided]

### In English
[English version]

### What Shifted
- [Specific annotation 1: what this English version cannot preserve from the L1]
- [Specific annotation 2: where the English requires an addition the L1 leaves implicit]
- [Where the mapping is successful: what does survive]
```

When offering third version:

```text
### Direct English (optional)
[Simplified version]

### What This Version Sacrifices
[Explicit statement of what was lost]
```

## NEVER

1. **Never default to "standard American English" as the target.** The English version is one valid rendering. Annotate its departures from the L1 — do not treat it as the correct version.

2. **Never treat L1 grammatical patterns as errors.** "I have fear" is not wrong — it encodes a different ontology. The annotation block explains the difference, not corrects it.

3. **Never produce false equivalents.** When no clean mapping exists, say so explicitly. "English cannot directly capture [concept]. Here is the closest approximation, and here is what it misses."

4. **Never assume L1 rhetorical patterns.** Not all Arabic speakers write circularly. Not all Japanese speakers hedge. Respond to the actual text/thought, not to statistical tendencies of a language community.

5. **Never strip epistemic hedging without examination.** A Japanese-trained writer's hedges may be intentional calibration — relational care encoded grammatically. The annotation notes this possibility rather than eliminating the hedges.

6. **Never offer the simplified third version without naming what it sacrifices.** The third version is available but must be framed as a tradeoff, not an upgrade. Name the specific rhetorical move, ontological distinction, or relational positioning that the simplification loses.

## Additional Resources

- **`@./references/translanguaging-guide.md`** — Research basis: what translanguaging is, the four gap types with detailed examples, ontological framing approach, citations
- **`@./references/language-patterns.md`** — Per-tradition reference: specific grammatical patterns by language tradition with annotation examples
