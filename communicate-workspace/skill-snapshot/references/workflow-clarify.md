# Clarify Workflow

Scoped clarity audit and repair. Diagnose existing prose for structural disorder, hidden actors, and weak language, then apply fixes in strict priority order. The fast, focused diagnostic tool — scoped to the Clarity category (structure, voice, language). For comprehensive multi-pass refinement across all 5 expression dimensions, load `@./references/workflow-redraft.md`. For ad-hoc technique access without workflow overhead, return to the router and apply techniques directly.

## Fix Sequence

**Structural -> Voice -> Language -> (Grounding when needed)**

Structural fixes cascade downstream — misordered prose creates redundancy and ambiguity that word-level fixes cannot reach. Activating voice (naming actors) clarifies who claims what. Strengthening language then forces honest confidence assessment. Each layer creates conditions for the next.

## NEVER

- **Never start with word-level before structural.** The fix sequence is enforced: structural -> voice -> language. Hedge removal on misordered prose wastes effort.
- **Never fill intentional gaps.** Gap-check precedes every addition suggestion — ask "is this gap doing rhetorical work?" before filling.
- **Never smooth productive friction.** Irregular rhythm, unresolved tension, deliberate register shifts — ask before regularizing.
- **Never correct L1 grammatical patterns as errors.** Diagnose what the pattern encodes before treating it as a problem. L1-inflected syntax (Arabic right-branching, German verb-final, French subordinate structure) may produce unusual English rhythms that carry intended precision.
- **Never treat all hedging as weakness.** The hedging split is mandatory in the language commitment audit — distinguish epistemic calibration (preserve) from habitual cushioning (cut).
- **Never preserve passive voice without naming why.** If passive is preserved, the Present phase must state the reason explicitly.

## Phase 0: Orient

Before diagnosing: load the tradition lens. Identify what rhetorical tradition the prose operates within. Reframe the clarity diagnostic as tradition-neutral: "Does this organizational structure serve the argument's purpose?" — not "Can a reader follow linearly?" The latter assumes Anglo-American linear-deductive organization as default.

Also: identify whether difficulty comes from subject or expression. Essential complexity (intrinsic cognitive load) must be preserved, not smoothed. Prose that is hard to parse because the ideas are genuinely complex is working correctly.

Load: `@./references/tradition.md`

## Phase 1: Diagnose

Four audits in sequence. Each surfaces issues; fixes apply in Phase 2.

### Structural audit

Load: `@./references/clarify.md`

- **Sequence** — Are concepts introduced before they are referenced?
- **Information flow** — Given information before new?
- **Gaps** — Undefined terms, logical leaps, missing connective tissue?
- **Prerequisites** — What must the reader already know for this to work?

### Content audit

Load: `@./references/clarify.md` (continued)

- **Streamline** — Remove redundancy, ceremonial language, filler
- **Load type** — Distinguish extraneous cognitive load (poor expression) from intrinsic load (complex subject) from germane load (productive challenge). Preserve intrinsic load.
- **Mechanism** — Does the prose explain how and why, not just what?
- **Quantifiers** — Ground "many", "often", "most" with specifics where available

### Expression audit

- **Presence** — Convert negations to positive direction where clarity improves
- **Referent tracking** — Resolve ambiguous pronouns ("it", "this", "they" without clear antecedent)

### Voice activation audit

Load: `@./references/activate.md`

- Scan for passive patterns (was/were + past participle, "it was determined", "it has been observed")
- For each passive: who performs this action? Is the passive intentional?
    - Scientific writing conventions: passive may be appropriate
    - Arabic agentless constructions: may encode divine or natural causation deliberately
    - Japanese passive: may be an intentional rhetorical choice, not avoidance
    - When preserving passive, name the reason
- Rewrite with actor as subject unless passive is intentional

### Language commitment audit

Load: `@./references/strengthen.md`

Flag: hedge words, weak verbs, nominalizations, filler phrases, false certainty.

**Hedging split (mandatory)** — Distinguish two functions before cutting any hedge:

1. **Epistemic calibration** (preserve) — The hedge reflects genuine uncertainty, scope limitation, or evidential stance. The writer means "somewhat" because the evidence is partial. Japanese sentence-final particles encoding relational care. Spanish *estar* encoding emotional temporality. French subordinate clause accumulation as epistemic rigor.

2. **Habitual cushioning** (cut) — The hedge is protective filler with no informational content. The writer does not mean "somewhat" — they mean the thing, and are cushioning the claim.

For each flag: delete if unnecessary, replace with precise alternative, or preserve with justification. Cultural calibration: check tradition before cutting hedges that may encode relational care or epistemic sophistication.

## Phase 2: Repair

Apply fixes in priority order: structural first, then voice, then language, then grounding.

**Gap-check before every addition** — Before suggesting any addition to the prose, ask whether the gap is doing rhetorical work. Intentional omission in high-context traditions, strategic silence as craft, and productive ambiguity that invites reader completion are not gaps to fill. If the absence serves a purpose, preserve it.

## Phase 3: Verify

Re-read the repaired prose as a whole. Check three things:

1. **New problems** — Structural changes can create new ambiguities, broken references, or orphaned transitions. Read through the repaired version looking for issues the fixes introduced.
2. **Intrinsic load preserved** — Essential complexity must survive repair. If the subject is genuinely difficult, the repaired prose should still be difficult — but the difficulty should come from the ideas, not the expression.
3. **L1 patterns preserved** — Intentional L1 grammatical patterns should not have been corrected away during voice activation or language commitment. If a pattern encodes philosophical precision (Spanish emotion-as-carried, Japanese epistemic particles), it should survive.

## Phase 4: Present

Output the improved prose. Then summarize changes, explicitly naming what was preserved and why:

- **Structural fixes** — What was reordered, connected, or clarified. Which gaps were preserved as intentional.
- **Voice activation** — What passive was converted to active. What passive was preserved, and why (scientific convention, agentless construction, rhetorical choice).
- **Language commitment** — What hedging was cut as cushioning. What hedging was preserved as epistemic calibration. What nominalizations were converted.
- **Complexity preserved** — What difficulty was identified as intrinsic load and left intact.
- **Tradition observations** — Any tradition-specific patterns identified during Orient, and how they modified the diagnosis.

## Additional Resources

For detailed patterns and extended examples beyond what the technique references provide:

- **`@./references/clarify-patterns.md`** — Detection heuristics, repair strategies, domain-specific considerations
- **`@./references/clarify-examples.md`** — Before/after transformations organized by issue type
