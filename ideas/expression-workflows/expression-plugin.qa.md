# Expression Plugin PRD — QA Report

Reviewer assessment of `expression-plugin.prd.md` against the reviewer checklist.

---

## Checklist

### ☑ Every skill has a distinct, non-overlapping problem statement

**Assessment: PASS**

| Skill | Problem | Distinctness |
|-------|---------|-------------|
| `composition` | Blank-page composition from intent | Only skill that addresses the generative/blank-page case |
| `help-me-say` | Articulating a thought that resists English because it lives in a different conceptual framework | Only skill that addresses translanguaging and ontology bridging |
| `clarify` | Clarity audit + repair (scoped: structure, voice, language only) | Scoped to Clarity category — explicitly distinguished from `/redraft` (all dimensions) |
| `redraft` | Comprehensive multi-pass improvement across all 5 expression dimensions | Distinguished from `/clarify` (clarity only) by scope; distinguished from `/composition` (improvement vs. composition) |
| `recast` | Making prose work in a different rhetorical tradition than it was written for | Only skill that addresses structural tradition mismatch — distinguished from `help-me-say` (writer's articulation problem vs. reader's reception problem) |
| `expression` | Direct technique access without workflow overhead | Distinguished from all workflow skills by being a library, not a funnel |

**One potential overlap to watch:** `/clarify` and `/redraft` both audit existing prose. The distinction (scoped clarity only vs. all 5 dimensions) is stated explicitly in both skills. Implementation should ensure the descriptions make this distinction clear in the trigger phrases — current draft does this: `/clarify` triggers on "clarify this", "clean this up", "fix my draft"; `/redraft` triggers on "make this as good as it can be", "full redrafting", "polish thoroughly".

---

### ☑ Each skill proposal has all 4 docs sections

**Assessment: PASS with notes**

All 6 skills have:

- [x] Metadata (YAML frontmatter with name, description, user-invocable, context)
- [x] SKILL.md outline (complete section structure)
- [x] References list (techniques assigned and new references named)
- [x] Examples section (phase designs specify what the skill produces at each stage)

**Notes:**

- The PRD does not include literal worked examples (before/after prose showing each skill in action). These would strengthen the implementation spec. **Recommendation:** add 1-2 worked examples per skill before implementation begins, or include them as `references/examples/` files.
- `help-me-say` has the most explicit output format specification (the bilingual template). Other skills describe their output format in the Present phase but don't include explicit templates. Acceptable — the format is clear from the phase descriptions.

---

### ☑ Cultural research is integrated (not bolted on)

**Assessment: PASS — strongly integrated**

Cross-cultural research is not a caveat or footnote — it is structurally embedded:

1. **Tradition meta-lens in every workflow skill's Orient phase.** This is a mandatory phase, not an optional modifier. Arabic parallel-restatement, French dialectical structure, Japanese epistemic particles, and high-context implicit meaning are all named as the reason specific diagnostic questions must be reframed — not as interesting footnotes.

2. **Diagnostic questions are revised, not annotated.** The `/clarify` clarity diagnostic is rewritten from "Can a reader follow linearly?" (Anglo-centric) to "Does this organizational structure serve the argument's purpose?" (tradition-neutral). The `/expression` routing table updates all tradition-relevant diagnostics. The hedging split in `/clarify` and `/redraft` explicitly names Japanese and Spanish traditions as the reason the split is needed.

3. **`help-me-say` is built from cultural research.** The four gap types (grammatical ontology, rhetorical convention, conceptual lacuna, pragmatic convention) are directly derived from the culture-researcher's ground file. The translanguaging frame (Garcia & Li Wei, 2014) is the organizing concept.

4. **`recast` is a skill that only exists because of cultural research.** Without the finding that rhetorical conventions are structurally different and not just stylistically different, there would be no reason for this skill to exist.

5. **Position questions** in `/composition`'s Frame phase draw explicitly from Luiselli, Ngugi, and Ernaux — the cultural research shaped what "position" means in a writing skill.

**One gap:** The writing-scholar's insight about "writing as resistance" (Achebe's witness, Ngugi's prison-cell novel, Poniatowska's testimony) is present in the grounding principles (P0: Necessity, P3: Position) but is not surfaced as a specific mechanism in any skill's phase design. The `/composition` skill's Frame phase asks "why must this be written?" which gestures at it, but the resistance/preservation dimension of writing is not explicitly named. **Recommendation:** Consider adding a "necessity audit" note to `/composition`'s Frame phase that names preservation, witness, and defiance as legitimate answers to "why must this be written?" — these are not just poetic but structurally different from efficiency-driven or instruction-driven writing.

---

### ☑ `help-me-say` bilingual output clearly specified

**Assessment: PASS**

The bilingual output specification is complete:

**Input:** Accepts the rough idea in English, L1 phrase/sentence, mixed input ("in Arabic we say X — how do I say that in English?"), or a passage that feels "foreign" despite correct grammar.

**Native language detection:** Priority order specified (explicit statement → L1 text → concept description → ask directly). Never-guess rule stated.

**Output structure (complete template):**

```
### In [Native Language]
[L1 version — or "[generated based on your description]" if not user-provided]

### In English
[English version]

### What Shifted
- [annotation 1: what English cannot preserve from L1]
- [annotation 2: where English requires explicit what L1 leaves implicit]
- [where mapping is successful]
```

**Third output trigger conditions:** Specified (L1 clause structures, low-context target, user request, brevity context). The "what this version sacrifices" requirement for the third output is specified and cannot be skipped.

**Six design risks** are named and mitigated (flattening to Anglo norms, stereotyping, hedging over/under-correction, missing the concept entirely, treating bilingual writing as deficient, ignoring register mismatches).

**One clarification needed:** The PRD specifies that if the user's native language cannot be determined, ask directly. But it doesn't specify what to do if the user declines to answer or says "I don't have a native language." This is an edge case, but implementation should have a fallback: proceed with the English version only, with annotations where L1 influence is evident in the text.

---

### ☑ `/writing` rename from `expression:expression` is fully justified

**Assessment: PASS**

The justification is present through the structural argument:

1. **The current `expression:expression` is a technique library.** It presents 17 techniques as a diagnostic-question routing table. It is reactive (improve existing prose) and non-sequential.

2. **Composition is a distinct activity.** The PRD cites the grounding-principles consensus: "Composition is a distinct activity from editing." The skill-analyst established that no current skill addresses the blank-page problem.

3. **The name `expression` is retained for the library.** The library keeps the name `expression` because it continues to be the direct-access technique library. The composition workflow takes the name `writing` because that's what users say when they want to compose.

4. **The rename is explained in the Skill 6 section:** "`expression:expression` skill is renamed to `expression:composition`... The technique library is now `expression:expression` (see Skill 6 — the library skill keeps the name `expression`)."

**One inconsistency to resolve:** The Skill 6 refactoring plan says "The composition workflow takes the name `/writing`." But the metadata for Skill 1 already names it `writing` as the `name` field. The inconsistency is in the phrasing, not the design. However, the "Structural Changes Summary" table has this correctly:

| Current | Proposed | Change |
|---------|----------|--------|
| `expression:expression` (library) | `expression:expression` (library, updated) | Name kept; content updated |

And separately:
| *(none)* | `expression:composition` | New composition workflow |

So: the current `expression:expression` skill does NOT get renamed to `writing`. Instead, a NEW skill called `writing` is created. The library skill keeps the name `expression`. This is correct and consistent — but the Skill 1 section's sentence "Renames `expression:expression`" is misleading. **Recommendation:** Fix this sentence: change from "Renames `expression:expression`: Yes" to "Relationship to `expression:expression`: The current library skill is NOT renamed. A new `writing` skill is created. The library retains the name `expression`."

---

### ☑ AI-ism prevention is concrete (specific phrases to avoid, not vague)

**Assessment: PASS**

Each skill has specific, named anti-AI-ism mechanisms. Examples:

**`/writing` — specific:**

- "Do not fill the blank page prematurely — Frame phase requires necessity and purpose before structure"
- "Do not invent position — if the writer hasn't specified their relationship to the subject in Frame, ask"
- "Do not substitute category for experience — load technique-ground before reaching for an abstract noun"
- "Do not treat the Frame → Discover loop as revision failure"

**`help-me-say` — specific:**

- "Never default to 'standard American English' as the target"
- "Never treat L1 grammatical patterns as errors — 'I have fear' is not wrong"
- "Never produce false equivalents — when no clean mapping exists, say so explicitly"

**`/proofread` — specific:**

- "Never start with word-level before structural — the fix sequence is enforced"
- "Never fill intentional gaps — gap-check precedes every addition suggestion"
- "Never correct L1 grammatical patterns as errors — diagnose what the pattern encodes"
- "Never preserve passive voice without naming why"

**`/refine` — specific:**

- "Never run Pass 4 on structurally disordered prose — coherent-sounding confusion is the failure mode"
- "Never declare stabilization after one round unless all five passes found only cosmetic changes"
- "Never apply Pass 3 before Pass 2"
- "Never skip Pass 0"

**`/recast` — specific:**

- "Never treat the source tradition as deficient"
- "Never silently normalize to Anglo-American English — annotate every significant structural adaptation"
- "Never adapt content along with structure — scope is enforced"
- "Never assume the user wants full adaptation — always offer the 'explain the original structure' option"

**Shared anti-AI-isms:** 8 shared behavioral requirements, all concrete. Including the "gap-check before every addition" mechanism, the hedging split as mandatory (not optional), and tradition identification before any diagnostic fires.

**One gap:** The writing-scholar identified "AI fills every gap — it cannot choose to withhold" as a core limitation. The PRD addresses this through the `omit` technique and the gap-check mechanism. But no skill explicitly says: "before generating any prose, ask yourself: what should this leave out?" The gap-check is reactive (before adding something). A proactive subtraction check at the start of generative phases in `/writing` would strengthen P4 (Subtraction). **Recommendation:** Add to `/writing`'s Compose phase: "Before drafting: what does this NOT need to say? Strategic omission shapes prose from the inside, not through subtraction after the fact."

---

### ☑ Skills collectively cover writing lifecycle without gaps

**Assessment: PASS**

Lifecycle coverage:

| Lifecycle Stage | Skill | Notes |
|----------------|-------|-------|
| Pre-writing (Why? Who? From where?) | `composition` (Frame phase) | Covered |
| Composition (blank page) | `composition` | Covered |
| Mid-draft articulation (thought resists English) | `help-me-say` | Covered; works as interrupt |
| Clarity repair (structure, voice, language) | `clarify` | Covered |
| Comprehensive improvement (all dimensions) | `redraft` | Covered |
| Rhetorical tradition adaptation (different audience) | `recast` | Covered |
| Ad-hoc technique access | `expression` | Covered |

**No lifecycle gaps.** The complete path from blank page to audience-appropriate prose is covered.

**One coverage note:** The PRD eliminated the proposed `/feedback` skill (diagnosis without repair) by absorbing it into `/proofread` as a "flag-only option." This works, but the SKILL.md outline for `/proofread` doesn't explicitly describe the flag-only mode. **Recommendation:** Add a brief "Feedback Mode" section to `/proofread`'s SKILL.md: "If the user wants diagnosis without fixes, run Phases 0-1 (Orient + Diagnose) and present findings rather than proceeding to Repair." This makes the absorbed functionality explicit.

---

### ☑ Each skill can be used standalone

**Assessment: PASS**

| Skill | Standalone? | Evidence |
|-------|-------------|----------|
| `composition` | Yes | Frame → Structure → Compose → Discover → Polish is complete from blank page |
| `help-me-say` | Yes | Receive → Identify → Bridge → [third] is complete from a rough idea |
| `clarify` | Yes | Orient → Diagnose → Repair → Verify → Present is complete |
| `redraft` | Yes | Pass 0 → 5 passes → Converge → Present is complete |
| `recast` | Yes | Source → Target → Divergence → Adapt → Annotate is complete |
| `expression` | Yes | Diagnostic-question routing table is self-contained |

**`help-me-say` standalone vs. interrupt:** The skill explicitly says it works both ways. The standalone case (user has a thought that resists English) and the interrupt case (mid-draft, mid-clarify) are both specified.

---

## Open Issues to Resolve Before Implementation

### Critical

1. **Fix `/writing` rename language.** Skill 1's "Renames `expression:expression`" section is inconsistent with the Structural Changes Summary. A new `writing` skill is created; the library retains the name `expression`. Fix the language in Skill 1's Refactoring Plan.

2. **`help-me-say` fallback for unknown native language.** Add: if the user declines to specify a native language, proceed with English version only, annotating where L1 influence is evident.

### Recommended Before Implementation

1. **Add necessity audit language to `/writing`'s Frame phase.** Specifically name preservation, witness, and defiance as legitimate answers to "why must this be written?" — grounded in the writing-scholar's synthesis.

2. **Add proactive subtraction check to `/writing`'s Compose phase.** "Before drafting: what does this NOT need to say?" — proactive, not reactive.

3. **Add Feedback Mode to `/clarify`'s SKILL.md.** Makes the absorbed `/feedback` functionality explicit.

4. **Clarify technique-tradition presentation in `/expression` routing table.** The current resolution (tradition in the Connection section as meta-lens) needs clear language that distinguishes it from the other two Connection techniques. Suggested phrasing: "tradition — LOAD BEFORE ANY OTHER TECHNIQUE. Identifies the rhetorical tradition operating in this prose and modifies how all diagnostic questions fire."

### Low Priority

1. **Worked examples.** Each skill's SKILL.md would benefit from 1 worked example in `references/examples/`. Not required for implementation to begin, but strengthens the spec.

2. **Pass 0 classification method for `/redraft`.** Whether tradition identification uses a classification table (from `tradition-signatures.md`) or diagnostic judgment is left open. Recommend specifying in implementation: load `tradition-signatures.md` for rapid classification, then confirm with judgment.

---

## Summary

**All 8 checklist items: PASS** (with notes and recommendations).

The PRD is implementation-ready. The 4 critical/recommended fixes above should be addressed before beginning skill creation — they are low-effort clarifications, not design changes.

The most significant contribution of the research phase (relative to the original expression plugin) is structural rather than additive:

1. **Tradition-awareness is embedded, not bolted on** — the tradition meta-lens in every Orient phase fundamentally changes how all diagnostics fire.
2. **Subtraction is as important as addition** — technique-omit, gap-check, and the hedging split together counterbalance the AI default of filling.
3. **The lifecycle is complete** — the original plugin had no composition skill, no ontology-bridging skill, and no tradition-adaptation skill. All three are now specified.
4. **Cross-cultural research changed technique design** — not just extended it. The clarity diagnostic is rewritten, not annotated. The voice diagnostic adds position. The calibrate diagnostic adds rhetorical convention dimension. These are design changes, not caveats.

The 10 grounding principles in `grounding-principles.md` provide the evaluative framework for all future expression plugin decisions.
