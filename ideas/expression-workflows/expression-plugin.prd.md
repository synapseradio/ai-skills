# Expression Plugin — PRD

Synthesized from Phase 1 (parallel ground research), Phase 2 (3-round discussion → grounding principles),
and Phase 3 (ideation: seed → diverge → cluster → filter → refine).

Research basis: skill-analyst architecture analysis, culture-researcher cross-tradition linguistic
study (Kaplan, Hall, Boroditsky, Garcia & Li Wei, Saigo, and others), writing-scholar synthesis
(Achebe, Adichie, al-Shaykh, Bolano, Ernaux, Luiselli, Mahfouz, Murakami, Ngugi, Ogawa,
Poniatowska, Saunders, Yourcenar).

Grounding: 10 principles in `docs/ideas/expression-workflows/grounding-principles.md`.

---

## Ideation Summary

### Phase 3 Outcomes

**Constraints established (Round 1 — Seed):**

Hard constraints:

- HC1: Progressive disclosure architecture (SKILL.md ≤ 500 lines; 3-level loading: description → SKILL.md → references/)
- HC2: Skills must be distinct — different user goals, non-overlapping problems
- HC3: Each skill must be usable standalone without requiring other skills
- HC4: Goal-oriented routing — user says what they want, not what phase they're in
- HC5: 5–7 skill budget
- HC6: Cultural research must be structurally integrated, not bolted on as caveats
- HC7: Anti-AI-ism mechanisms must be concrete (specific phrases, specific patterns), not vague

Soft preferences:

- SP1: Fewer, deeper skills over many shallow ones
- SP2: `help-me-say` must work as an interrupt during any other skill
- SP3: Cover the full writing lifecycle without gaps or overlaps
- SP4: Preserve and promote existing `/clarify` and `/redraft` command content — it's good, move it

Success criteria (cross-cultural):

- SC-A: Tradition-aware — no Anglo-American default; all diagnostics identify tradition before firing
- SC-B: Epistemic humility — hedging split (calibration vs. cushioning) in every skill that touches confidence
- SC-C: Subtraction-first — gap-check before every addition suggestion
- SC-D: Ontology-bridging — `help-me-say` addresses translanguaging, not surface translation

**Lifecycle established (Round 2 — Diverge, synthesized):**

The expression plugin covers the full writing lifecycle:

```
ORIENT (embedded in all skills — not a standalone skill)
    ↓
[COMPOSE ⟷ STRUCTURE]   ← bidirectional; non-sequential across traditions
    ↓
CLARIFY
    ↓
REDRAFT
    ↓
DELIVER / RECAST

ARTICULATE (interrupt — can enter at any lifecycle stage)
```

- `ORIENT` is always embedded in the first phase of whichever skill is invoked. It never justifies a standalone skill.
- `[COMPOSE ⟷ STRUCTURE]` are not universally sequential. French tradition structures before composing; Arabic tradition composes and structures simultaneously; Japanese tradition uses recursive descent. The `/composition` skill handles both and makes them iterative.
- `ARTICULATE` (`help-me-say`) is an interrupt — usable mid-draft, mid-clarify, mid-redraft, or standalone.
- `DELIVER` needs its own skill (`/recast`) when the prose is moving from one rhetorical tradition to another.

**Skills decided (Round 4 — Filter, synthesized):**

Eliminated in filtering:

- `/feedback` (diagnosis without repair) — absorbed into `/clarify` as a mode (flag-only option); doesn't warrant a full skill
- `/tone-match` — merged into `/recast`; tone transformation is a subset of rhetorical tradition adaptation
- `/voice` — absorbed into `/redraft` Pass 3 and `/composition` Polish phase; not distinct enough
- ORIENT standalone — ruled out in Round 2

Survivors (6 skills):

| Skill | Problem It Solves |
|-------|------------------|
| `composition` | Blank-page composition from intent — generative, not reactive |
| `help-me-say` | Ontology bridging for multilingual thinkers — articulating a thought that resists English |
| `clarify` | Clarity audit + repair — systematic diagnosis of existing prose's structural, voice, and language problems |
| `redraft` | Full-cascade multi-pass improvement — comprehensive refinement across all 5 expression dimensions |
| `recast` | Rhetorical tradition adaptation — making prose work in a different rhetorical tradition than it was written for |
| `expression` | Technique library — direct access to all 21 techniques without workflow overhead |

**Technique library expansion (Round 5 — Refine, synthesized):**

17 → 21 techniques. Four new techniques, identified through cross-cultural research:

| New Technique | Category | What It Adds |
|---------------|----------|-------------|
| `omit` | Clarity | Subtractive craft — identifying what to withhold for effect (P4: Subtraction) |
| `position` | Narrative | Where the writer writes from — relationship to subject, authority, blind spots (P3: Position) |
| `ground` | Clarity | Embodied specificity — replacing generic abstraction with situated, witnessed detail (P8 + P4) |
| `tradition` | Meta-lens | Rhetorical tradition identification — modifies how all other diagnostics fire (P2: Tradition) |

`tradition` is not a technique in a category — it is a meta-lens loaded in the Orient phase of every workflow skill. It does not appear in the Clarity → Integrity → Narrative → Generative → Connection taxonomy; it operates above and across all of them.

**Technique file location:**

All 21 technique files move to `plugins/expression/references/technique-{name}.md` (plugin root).
This is shared infrastructure accessible to all 6 skills. No technique file lives inside a skill's own `references/`.

Reference path from any skill: `@${CLAUDE_PLUGIN_ROOT}/references/technique-{name}.md`

---

## Skill 1: `composition`

### Metadata

```yaml
---
name: composition
description: This skill should be used when the user asks to "help me write this", "draft this for me",
  "help me compose X", "I have something to say but don't know how to start", "write this from scratch",
  "I need to draft Y", or when prose needs to be composed from intent rather than improved from an
  existing draft. The generative counterpart to /clarify and /redraft.
user-invocable: true
context: fork
---
```

### Problem It Solves

The current expression plugin is entirely reactive — it improves existing prose. No skill addresses blank-page composition: the task of building prose from purpose, from rough notes, from a felt need to say something that doesn't yet have a form. `/composition` fills this gap.

### Phase Design

Composing is not linear — drafting often reveals the real argument. The skill is explicitly recursive.

```
Frame ──→ Structure ──→ Compose
  ↑                        ↓
  └──── Discover ←─────────┘
              ↓
           Polish
```

**Phase 0: Orient (embedded)**
Before anything else: load tradition lens. Identify what rhetorical tradition the writer is working in or for. This modifies how structure questions are asked in Phase 2.

**Phase 1: Frame**

Questions:

- Why must this be written? (P0: Necessity — required first)
- What must this accomplish, and for whom? (P1: Purpose)
- Who speaks, and from what position? (P3: Position — mandatory, not optional)
    - "What is my relationship to this subject?"
    - "What can I legitimately claim?"
    - "What am I unable to see from where I stand?"
- What does the audience already know and what rhetorical conventions do they expect? (load: technique-calibrate)

Output of Frame: necessity statement, purpose statement, positional acknowledgment, audience/tradition context.

**Phase 2: Structure**

Based on the rhetorical tradition identified in Orient:

- What organizational logic fits this tradition and purpose? (load: technique-tradition for structural options)
- What arc shape would create pull? (load: technique-arc)
- What information must come first to make what follows possible? (load: technique-clarify — prerequisite-trace)

Note: Structure and Compose are bidirectional — go to Compose when ready, return to Structure when the draft reshapes the argument.

**Phase 3: Compose**

Generative drafting. Follow the surprising sentence. Practice strategic omission (load: technique-omit). Ground claims in situated, witnessed detail (load: technique-ground). Allow contradiction to surface — do not smooth it yet.

Specific anti-AI-ism directives active during Compose:

- Do not fill intentional gaps (resist adding bridges the reader can supply)
- Do not resolve tension prematurely (contradiction is not a bug)
- Do not substitute category for experience (load technique-ground before reaching for an abstract noun)

**Phase 4: Discover**

Self-audit after each draft. Key questions:

- Did this draft teach you something you didn't know when you started?
- Does your Frame still hold, or did drafting reveal the real argument?
- If Frame has shifted: return to Phase 1 with new understanding (the loop is the skill working correctly, not failure)

Load: technique-surface-assumptions (what premises emerged that weren't in the Frame?), technique-signal-confidence (calibrate what the draft claims against what you know).

**Phase 5: Polish**

Final craft and audience connection. Load:

- technique-voice (consistent authorial presence, extending to position — does this person speak from a stated position?)
- technique-diction (word-level precision, eliminate AI patterns)
- technique-calibrate (does depth match audience? does rhetorical convention match tradition?)
- technique-bridge (cross-cultural: what bridges unfamiliar concepts for this audience?)

### Technique Assignments

| Phase | Techniques Loaded |
|-------|------------------|
| Orient | tradition (meta-lens) |
| Frame | calibrate, position |
| Structure | tradition (structural options), arc, clarify (prerequisite-trace) |
| Compose | omit, ground, illustrate |
| Discover | surface-assumptions, signal-confidence |
| Polish | voice, diction, calibrate, bridge |

Techniques available as reach-for-as-needed throughout: strengthen (when language needs commitment), rhythm (when sentence-level cadence matters), pose-questions (when the piece should invite rather than close).

### Cross-Cultural Integration

- Tradition check in Orient is mandatory, not optional. All structural questions in Phase 2 are prefaced by: "Given that this prose operates in [tradition], what organizational logic fits?" This prevents defaulting to linear-deductive Anglo-American structure for Arabic, French, Japanese, or Latin American writers.
- Frame's positional questions are drawn from Luiselli's "knowing where we are writing from" and Ngugi's language-as-identity insight. Position is not a disclaimer — it is a structural decision.
- Compose phase's "follow the surprising sentence" is grounded in Murakami's discovery process and Ernaux's "ethnology of myself."
- The Frame → Discover loop is normalized as the writing working, not the writer failing — grounded in every tradition studied (P6: Discovery).

### Anti-AI-ism Mechanisms

Specific patterns to prevent, and the phase where each fires:

1. **Do not fill the blank page prematurely.** Frame phase requires necessity and purpose before structure. If the writer cannot articulate why this must be written, do not proceed to Structure.
2. **Do not invent position.** If the writer hasn't specified their relationship to the subject in Frame, ask — do not construct a generic authorial voice. (P3, anti-AI-ism #5 from grounding-principles)
3. **Do not impose Anglo-American structure.** Tradition check before Structure phase prevents this. Explicitly name when structure choices are tradition-specific, not universal.
4. **Do not resolve contradiction in the Compose phase.** Unresolved tension is permitted and encouraged. The Discover phase is where the writer decides whether contradiction is the point.
5. **Do not substitute category for experience in Compose.** Before accepting a generic abstract noun, load technique-ground and ask: what witnessed detail could replace this category? (anti-AI-ism #4)
6. **Do not treat the Frame → Discover loop as revision failure.** Normalize discovery. The skill description should explicitly say: "If your draft changed what you know, return to Frame. This is the skill working."

### Refactoring Plan

**What's new:** Entirely new skill. No existing command covers composition.

**What it draws from:**

- technique-clarify (prerequisite-trace, information-flow) for Structure phase
- technique-arc for Shape in Structure phase
- technique-calibrate, technique-bridge for Polish phase
- technique-voice, technique-diction for Polish phase
- technique-signal-confidence, technique-surface-assumptions for Discover phase
- technique-omit (new), technique-ground (new), tradition (new meta-lens)

**Location:** `plugins/expression/skills/composition/SKILL.md`

**Relationship to `expression:expression`:** The current `expression:expression` skill remains as the technique library. A new skill called `composition` is created as the generative composition workflow. The library retains the name `expression`.

### SKILL.md Outline

```
---
(frontmatter: name, description, user-invocable, context)
---

# Writing

One paragraph: what this skill is and when to use it.

## Why Composition Needs Its Own Skill

3-4 sentences on the blank-page problem and why improvement tools can't solve it.

## The Recursive Shape of Composition

Diagram: Frame → Structure → Compose → Discover (loop back to Frame) → Polish

"If your draft changed what you know, return to Frame. This is the skill working."

## Phase 0: Orient
2-3 sentences. Load tradition lens. Identify rhetorical tradition. This modifies Phase 2.
@${CLAUDE_PLUGIN_ROOT}/references/technique-tradition.md

## Phase 1: Frame
Necessity question (mandatory first). Purpose, position (3 questions, mandatory), audience/tradition.
Short. Point to references/frame-guide.md for extended guidance.

## Phase 2: Structure
Based on tradition identified in Orient. Arc, information flow, organizational logic.
@${CLAUDE_PLUGIN_ROOT}/references/technique-arc.md
@${CLAUDE_PLUGIN_ROOT}/references/technique-clarify.md (prerequisite-trace only)

## Phase 3: Compose
Follow the surprising sentence. Omit deliberately. Ground in specificity.
@${CLAUDE_PLUGIN_ROOT}/references/technique-omit.md
@${CLAUDE_PLUGIN_ROOT}/references/technique-ground.md

## Phase 4: Discover
Self-audit. The Frame question: does this still hold?
@${CLAUDE_PLUGIN_ROOT}/references/technique-surface-assumptions.md
@${CLAUDE_PLUGIN_ROOT}/references/technique-signal-confidence.md

## Phase 5: Polish
Voice, diction, audience calibration, bridging.
@${CLAUDE_PLUGIN_ROOT}/references/technique-voice.md
@${CLAUDE_PLUGIN_ROOT}/references/technique-diction.md
@${CLAUDE_PLUGIN_ROOT}/references/technique-calibrate.md
@${CLAUDE_PLUGIN_ROOT}/references/technique-bridge.md

## NEVER
5-6 specific guards. Fill before Frame completes. Invent position. Impose structure before tradition check.
```

### References Needed

- `references/frame-guide.md` — Extended Frame phase guidance: necessity questions, position questions, tradition identification, audience analysis
- `references/technique-omit.md` (new) — Subtractive craft: what to withhold, how gaps create meaning, distinguishing vagueness from productive ambiguity
- `references/technique-ground.md` (new) — Embodied specificity: moving from category to witnessed detail, grounding abstractions
- `references/technique-tradition.md` (new) — Rhetorical tradition taxonomy, structural signatures, diagnostic questions, modification rules for downstream diagnostics
- `references/technique-position.md` (new) — Positional awareness: 3-question framework, authority vs. experience, blind-spot mapping

---

## Skill 2: `help-me-say`

### Metadata

```yaml
---
name: help-me-say
description: This skill should be used when the user asks to "help me say this", "I can't find the
  right words", "in [language] we say... what's the English?", "how do I express this?", "what I mean
  is...", "I'm thinking in [language] but writing in English", "this concept doesn't translate",
  or when a bilingual or multilingual thinker needs to articulate a thought that resists expression
  in English because the idea lives in a different conceptual framework. Works as a standalone skill
  or as an interrupt during /composition, /clarify, or /redraft.
user-invocable: true
context: fork
---
```

### Problem It Solves

For multilingual thinkers, the gap between a clear idea and its English expression is not a vocabulary problem — it is an ontology problem. The idea may live in a grammatical framework (Spanish `tener miedo`, Japanese particles), a rhetorical convention (Arabic parallel structure), or a conceptual frame (Portuguese *saudade*) that English cannot accommodate without loss. `help-me-say` addresses this gap through **translanguaging** — drawing on the writer's full linguistic repertoire rather than switching between discrete languages.

This is distinct from translation. Translation optimizes for target-language correctness. `help-me-say` optimizes for semantic fidelity: what must survive from the source framing, and what is necessarily lost in the English rendering.

### Phase Design

```
Receive → Identify → Bridge → [Offer third if needed]
```

**Phase 1: Receive**

Accept the user's rough idea. Ask if not already provided:

- What's the thought you're trying to express?
- What language did you think it in (if not evident)?
- Is there a phrase in your native language that captures it, even roughly?

**Phase 2: Identify**

Determine the nature of the gap. Four types:

1. **Grammatical ontology gap** — L1 encodes a distinction English collapses (Spanish ser/estar, Japanese particles, Arabic verbal morphology, French imparfait/passé composé)
2. **Rhetorical convention gap** — L1 tradition has a different organizational or persuasive logic than English expects
3. **Conceptual lacuna** — The concept exists in L1 but has no direct English lexical equivalent (*saudade*, *wabi-sabi*, *tarab*, *Schadenfreude*, *duende*)
4. **Pragmatic convention gap** — L1 has different norms for directness, hedging, formality, or relational positioning

Load: technique-tradition to identify which tradition's conventions are shaping the source thought.

**Phase 3: Bridge**

Produce bilingual output:

```
[Native language version]
The thought as the user would express it in their L1. If the user has already provided this,
use it. If not, generate a likely L1 rendering based on what they've said. Mark as [generated]
if not user-provided.

[English version]
The thought rendered in natural English. Annotate differences:
  — where English collapses a distinction the L1 preserves
  — where English requires explicitness that the L1 leaves implicit (high-context → low-context)
  — where English rhetorical norms differ from L1 (thesis-first vs. dialectical vs. parallel)
  — where an L1 idiom was rendered as a functional equivalent with different connotations

[Annotation block]
Explicitly name what shifted, what was lost, what was preserved differently.
If the mapping is clean, say so. If no clean mapping exists, say so explicitly rather than
producing a false equivalent.
```

**Phase 4: Offer third (conditional)**

Offer a simplified/direct version when:

- The English version retains L1 clause structures that may confuse a low-context English reader
- The target audience is known to be low-context (e.g., American business, academic English)
- The user asks for a "more natural English" rendering explicitly

When offering the third version, always flag what it sacrifices:

- "This version removes the dialectical framing. Your original showed you holding both positions before committing — the direct version loses that intellectual move."
- "This version converts 'I have fear' to 'I am afraid.' The original encodes emotion as something you carry rather than something you are — the English version loses that."

### Input Format

Flexible. Accept:

- The rough idea in English ("what I want to say is...")
- An L1 phrase or sentence the user wants help expressing in English
- A mix ("in Arabic we say X — how do I say that in English?")
- A passage of text that feels like it "doesn't sound right" in English despite being grammatically correct

### Output Format

```
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

```
### Direct English (optional)
[Simplified version]

### What This Version Sacrifices
[Explicit statement of what was lost]
```

### Native Language Detection

Priority:

1. User states it explicitly ("in Spanish we say...")
2. User provides L1 text (detect from script/orthography)
3. User describes the concept and its tradition ("in Japanese, there's a concept of...")
4. If unclear: ask directly before attempting Phase 3. Do not guess.

If the user's native language cannot be determined and they haven't provided L1 text: ask "What's your first language, or the language you're thinking in for this idea?"

Never attempt the bilingual output without knowing the source language.

### Cross-Cultural Integration

This is the primary site for P8 (Grammar as philosophy). Every annotation in the English version should name the ontological difference, not just the linguistic one:

- Not: "Spanish uses 'tener' here"
- But: "Spanish encodes this emotion as something you carry rather than something you are — the self remains separate from the feeling. English collapses this distinction."

The skill should treat L1 influence as a resource (translanguaging perspective), not as interference to be corrected (error-correction perspective).

### Anti-AI-ism Mechanisms

1. **Never default to "standard American English" as the target.** The English version is one valid rendering. Annotate its departures from the L1, do not treat it as the correct version.
2. **Never treat L1 grammatical patterns as errors.** "I have fear" is not wrong — it encodes a different ontology. The annotation block should explain the difference, not correct it.
3. **Never produce false equivalents.** When no clean mapping exists, say so explicitly. "English cannot directly capture [concept]. Here is the closest approximation, and here is what it misses."
4. **Never assume L1 rhetorical patterns.** Not all Arabic speakers write circularly. Not all Japanese speakers hedge. Respond to the actual text/thought, not to statistical tendencies.
5. **Never strip epistemic hedging.** A Japanese-trained writer's hedges may be intentional calibration. The annotation should note this possibility, not eliminate the hedges.
6. **Never offer the simplified third version without naming what it sacrifices.** The third version is available but must be framed as a tradeoff, not an upgrade.

### Refactoring Plan

**What's new:** Entirely new skill. The culture-researcher's design brief (in `ground-culture-researcher.md`) provides the foundational specification. No existing technique covers this — the closest is `technique-bridge` and `technique-calibrate`, but those address knowledge gaps, not ontological gaps.

**Location:** `plugins/expression/skills/help-me-say/SKILL.md`

**Relation to `/writing`:** Paired but distinct. `/writing` handles full-document composition. `help-me-say` handles point-of-need ontology bridging — usable standalone or mid-draft during `/writing`. They share the Frame phase's tradition-awareness but serve different goals.

### SKILL.md Outline

```
---
(frontmatter: name, description, user-invocable, context)
---

# Help Me Say

One paragraph: translanguaging as a skill. Not translation — ontology bridging.

## The Four Gaps
2-3 sentences each on: grammatical ontology, rhetorical convention, conceptual lacuna, pragmatic convention.
Examples from research (Spanish tener, Japanese particles, Arabic parallel structure).

## How to Use This Skill
Works standalone or as an interrupt during /composition, /clarify, or /redraft.

## Phase 1: Receive
What to accept. What to ask if missing. How to detect native language.

## Phase 2: Identify
The four gap types. Which one is operating here?
@${CLAUDE_PLUGIN_ROOT}/references/technique-tradition.md

## Phase 3: Bridge
The bilingual output format. Full specification.
When annotations are required (always). What "no clean mapping" looks like.

## Phase 4: Offer Third (Conditional)
When to offer. How to flag what's lost. The sacrificial framing requirement.

## Output Format
Complete template with all sections.

## NEVER
6 specific guards: Never default to American English, never treat L1 patterns as errors, etc.
```

### References Needed

- `references/translanguaging-guide.md` — Research basis: what translanguaging is, how it differs from translation, the four gap types with examples and citations (builds on culture-researcher's ground file)
- `references/language-patterns.md` — Cross-tradition reference: specific grammatical patterns by language tradition (Spanish ser/estar/tener, Japanese particles, Arabic verbal morphology, French epistemic structures, high-context signals) with annotation examples

---

## Skill 3: `clarify`

### Metadata

```yaml
---
name: clarify
description: This skill should be used when the user asks to "clarify this", "check my writing",
  "clean this up", "fix my draft", "edit this", "review this text", "give me feedback on this"
  (when fixes are wanted, not just diagnosis), or when a document needs structured clarity improvement
  before publishing. Audits prose and applies fixes across structure, voice activation, and language
  commitment.
user-invocable: true
context: fork
---
```

### Problem It Solves

Existing prose has clarity issues — structural disorder, hidden actors, weak language — that need systematic diagnosis and repair. Unlike `/redraft` (comprehensive, all 5 expression dimensions), `/clarify` is scoped to the Clarity category: structural order, voice activation, and language commitment. It is the fast, focused diagnostic tool.

### Phase Design

```
Orient → Diagnose → Repair → Verify → Present
```

Fix sequence is strictly ordered: structural → voice → language. Structural fixes cascade downstream, reducing the work that later phases need to do. Word-level fixes on misordered prose waste effort.

**Phase 0: Orient (embedded)**

Before diagnosing: load tradition lens. Identify rhetorical tradition. Reframe clarity diagnostic: "Does this organizational structure serve the argument's purpose?" — not "Can a reader follow linearly?" The latter is Anglo-centric; the former is tradition-neutral.

Also: identify whether difficulty comes from subject or expression (P5). Essential complexity must be preserved, not smoothed.

Load: technique-tradition (meta-lens).

**Phase 1: Diagnose**

Four audits in sequence:

*Structural audit* (technique-clarify):

- Sequence: are concepts introduced before they're referenced?
- Information flow: given before new?
- Gaps: undefined terms, logical leaps?
- Prerequisites: what must the reader already know?

*Content audit* (technique-clarify):

- Streamline: remove redundancy, ceremonial language
- Load type: extraneous vs. intrinsic vs. germane cognitive load — preserve intrinsic load
- Mechanism: does prose explain how and why, not just what?
- Quantifiers: ground "many", "often", "most" with specifics

*Expression audit* (technique-clarify):

- Presence: convert negations to positive direction
- Referent tracking: resolve ambiguous pronouns

*Voice activation audit* (technique-activate):

- Scan for passive patterns
- For each passive: who performs this action? Is the passive intentional (scientific writing, agentless constructions as rhetorical choice in Arabic tradition)?
- Rewrite with actor as subject unless passive is intentional — and name why it's preserved

*Language commitment audit* (technique-strengthen):

- Flags: hedge words, weak verbs, nominalizations, filler phrases, false certainty
- **Hedging split** (mandatory): distinguish epistemic calibration (preserve) from habitual cushioning (cut)
- For each flag: delete if unnecessary, replace with precise alternative, or preserve with justification
- Cultural calibration: Japanese hedges may be relational care, not weakness; check tradition before cutting

**Phase 2: Repair**

Apply fixes in priority order: structural first, then voice, then language, then grounding.

Before any addition: **gap-check** — is this gap doing rhetorical work? (P4: Subtraction)

- Intentional omission in high-context traditions: do not fill
- Strategic silence as craft: do not fill
- Productive ambiguity that invites reader completion: do not fill

**Phase 3: Verify**

Re-read the repaired prose:

- Check that fixes didn't introduce new problems (structural changes can create new ambiguities)
- Check that intrinsic load was preserved (essential complexity not smoothed)
- Check that intentional L1 patterns weren't corrected away (P8: Grammar as philosophy)

**Phase 4: Present**

Output improved prose. Summarize changes:

- What structural issues were fixed (and which gaps were preserved as intentional)
- What passive voice was activated (and what was preserved, and why)
- What hedging was cut (and what was preserved as epistemic calibration)
- What complexity was preserved as intrinsic load
- Any tradition-specific observations

### Technique Assignments

| Phase | Techniques |
|-------|-----------|
| Orient | tradition (meta-lens) |
| Diagnose | clarify (all three audits), activate, strengthen |
| Repair | omit (gap-check before additions), ground (if abstractions need grounding) |
| Verify | clarify (re-audit check), signal-confidence (calibration check) |

### Cross-Cultural Integration

- Orient phase: tradition identification is mandatory, not optional. The "follow linearly" diagnostic is reframed to "does this organizational structure serve the argument's purpose?"
- Voice activation: Arabic agentless constructions and Japanese passive may be intentional rhetorical choices — not errors. The audit must ask "who performs this action AND is naming the actor appropriate here?" before converting.
- Hedging split in language commitment: Japanese sentence-final particles encode relational care; Spanish estar encodes emotional temporality; French subordinate clause accumulation may be epistemic rigor. These are preserved, not stripped.
- L1-inflected syntax (Arabic right-branching, German verb-final, French subordinate structure) may produce "unusual" English rhythms — diagnose as tradition transfer before treating as error.

### Anti-AI-ism Mechanisms

1. **Never start with word-level before structural.** The fix sequence is enforced: structural → voice → language.
2. **Never fill intentional gaps.** Gap-check precedes every addition suggestion. "Is this gap doing rhetorical work?" must be asked.
3. **Never smooth productive friction.** Irregular rhythm, unresolved tension, deliberate register shifts are asked about before regularized.
4. **Never correct L1 grammatical patterns as errors.** Diagnose what the pattern encodes before treating it as a problem.
5. **Never treat all hedging as weakness.** The hedging split is mandatory in the language commitment audit.
6. **Never preserve passive voice without naming why.** If passive is preserved, the present phase says so explicitly.

### Refactoring Plan

**Source:** `plugins/expression/commands/clarify.md` — promotes to `plugins/expression/skills/clarify/SKILL.md`.

**Changes from current command:**

1. Add Orient phase (tradition lens before diagnosis)
2. Add Verify phase (currently missing — current command goes straight from repair to presentation)
3. Add gap-check before every addition in Repair
4. Add hedging split to language commitment audit
5. Add L1-pattern diagnostic to voice and language audits
6. Formalize phase naming for resumability
7. Explicit NEVER guards for the anti-AI-isms above

**What moves to SKILL.md vs. references/:**

- SKILL.md: Phase descriptions, fix sequence rationale, tradition reframe, NEVER guards, entry/exit conditions, hedging split definition
- references/: technique-clarify.md, technique-activate.md, technique-strengthen.md (all existing, moved to plugin root), clarify-patterns.md, clarify-examples.md (existing, moved to plugin root)

**Delete:** `plugins/expression/commands/clarify.md`

### SKILL.md Outline

```
---
(frontmatter: name, description, user-invocable, context)
---

# Proofread

One paragraph: scoped clarity audit + repair. The fast, focused diagnostic tool.
Contrast with /refine (comprehensive, all dimensions).

## Fix Sequence

Structural → Voice → Language → (Grounding when needed)

Brief rationale for the order. Why word-level on misordered prose wastes effort.

## NEVER
4-5 guards. Start with word-level. Fill gaps without asking. Treat all hedging as weakness.
Correct L1 patterns as errors.

## Phase 0: Orient
Tradition lens. Reframe the clarity diagnostic. Difficulty from subject or expression?
@${CLAUDE_PLUGIN_ROOT}/references/technique-tradition.md

## Phase 1: Diagnose
Four audits. Structural (sequence, flow, gaps, prerequisites). Content (streamline, load-type,
mechanism, quantifiers). Expression (presence, referent-track). Voice (passive → actor?).
Language (hedges → split).
@${CLAUDE_PLUGIN_ROOT}/references/technique-clarify.md
@${CLAUDE_PLUGIN_ROOT}/references/technique-activate.md
@${CLAUDE_PLUGIN_ROOT}/references/technique-strengthen.md

## Phase 2: Repair
Priority order enforced. Gap-check before additions.
@${CLAUDE_PLUGIN_ROOT}/references/technique-omit.md

## Phase 3: Verify
Re-read check. Intrinsic load preserved? L1 patterns preserved? New problems introduced?

## Phase 4: Present
Output + change summary. Preserved gaps and hedges named explicitly.

## Additional Resources
References for extended guidance: clarify-patterns.md, clarify-examples.md
```

### References Needed

- `references/technique-clarify.md` (existing, move from `skills/expression/references/`)
- `references/technique-activate.md` (existing, move)
- `references/technique-strengthen.md` (existing, move)
- `references/clarify-patterns.md` (existing, move)
- `references/clarify-examples.md` (existing, move)
- `references/technique-omit.md` (new — see Skill 1)
- `references/technique-tradition.md` (new — see Skill 1)

---

## Skill 4: `redraft`

### Metadata

```yaml
---
name: redraft
description: This skill should be used when the user says "make this as good as it can be",
  "full redrafting", "polish this thoroughly", "this needs to persuade", "redraft this completely",
  or when prose needs to persist, persuade, or represent significant work. Applies all 21 expression
  techniques in cascading sequence — Pass 0 (tradition+position) → clarity → integrity → narrative →
  generative → connection — repeating until stabilized.
user-invocable: true
context: fork
---
```

### Problem It Solves

Prose needs comprehensive, multi-pass improvement across all dimensions. Unlike `/clarify` (clarity only, fast), `/redraft` addresses all 5 expression dimensions — Clarity, Integrity, Narrative, Generative, Connection — in a multiplicative cascade where each pass makes subsequent passes more effective.

### Phase Design

The cascade adds Pass 0 (tradition + position lens) before the existing 5-pass sequence. This lens modifies how all downstream passes fire.

```
Pass 0: Orient → Pass 1: Clarity → Pass 2: Integrity → Pass 3: Narrative →
Pass 4: Generative → Pass 5: Connection → Converge?
     ↑                                                              ↓
     └───────────────── (if substantial changes remain) ───────────┘
```

**Pass 0: Orient (new)**

Before any technique is applied:

1. Load tradition lens. Identify rhetorical tradition. Note how it modifies downstream passes:
   - Arabic tradition: Pass 1 structural diagnostics must accept parallel-restatement as intentional
   - French tradition: Pass 1 must accept dialectical indirection as method, not vagueness
   - Japanese tradition: Pass 2 hedging split must distinguish particles (relational care) from cushioning
   - High-context traditions: Pass 5 calibration must not maximize explicitness
2. Identify writer's position (P3). Note for Pass 3 voice audit.
3. Check prose purpose: is this prose resisting clarity rules deliberately? (Writing-as-resistance, P4)

Load: technique-tradition (meta-lens), technique-position.

**Pass 1: Clarity**

Ask: Can a reader follow — within this tradition's logic? Are actors visible? Does language commit or cushion (hedging split)? Do abstractions have grounding?

Load: technique-clarify, technique-activate, technique-strengthen, technique-illustrate, technique-omit (gap-check before additions).

Tradition modifications from Pass 0:

- Structural diagnostic is tradition-relativized, not universal
- Voice activation preserves agentless constructions where culturally intentional
- Strengthen's hedging split distinguishes epistemic calibration from cushioning

**Pass 2: Integrity**

Ask: Does certainty match evidence? Where does this apply vs. break down? What must be true for this reasoning to hold?

Load: technique-signal-confidence (hedging split), technique-bound-scope, technique-surface-assumptions.

**Pass 3: Narrative**

Ask: What tension drives this forward? Does rhythm vary? Does voice stay consistent AND positioned? Does each word carry its weight? Does tone fit purpose?

Load: technique-arc, technique-rhythm, technique-voice (extended to position — does this person speak from a stated position?), technique-diction, technique-tone, technique-position.

**Pass 4: Generative**

Ask: What follows from these claims that goes unsaid? Where does feedback conflate concerns? Does this prose close inquiry or open it?

Load: technique-extract-implications, technique-dimensionalize, technique-pose-questions.

**NEVER** run Pass 4 on structurally disordered prose — implications extracted from unclear claims create coherent-sounding confusion.

**Pass 5: Connection**

Ask: What does this audience already know and what rhetorical conventions do they expect? What unfamiliar concepts appear without anchoring?

Load: technique-calibrate (with cultural dimension: not just "what does the audience know?" but "what rhetorical conventions does the audience expect?"), technique-bridge (cross-cultural bridging as well as knowledge bridging).

**Converge**

After all five passes: assess whether the cascade should continue.

Continue if: significant structural changes in Pass 1, new assumptions surfaced that affect other claims, arc restructuring revealed new clarity opportunities, the prose feels substantially different.

Stabilize if: changes are primarily cosmetic, each pass finds little to improve, prose has reached a coherent resting state.

If continuing: return to Pass 1 with refined output. Most prose stabilizes within 2–3 full cascades.

### Technique Assignments

| Pass | Techniques |
|------|-----------|
| Pass 0 | tradition (meta-lens), position |
| Pass 1 | clarify, activate, strengthen, illustrate, omit |
| Pass 2 | signal-confidence (hedging split), bound-scope, surface-assumptions |
| Pass 3 | arc, rhythm, voice (+position), diction, tone |
| Pass 4 | extract-implications, dimensionalize, pose-questions |
| Pass 5 | calibrate (+cultural dimension), bridge |

### Cross-Cultural Integration

- Pass 0 is the primary cross-cultural intervention. By loading tradition and position before any technique fires, all 5 passes operate within the writer's rhetorical tradition rather than against an invisible Anglo-American baseline.
- Pass 2 signal-confidence: the hedging split explicitly separates Japanese epistemic particles (preserve) from habitual English cushioning (cut).
- Pass 3 voice: extended to include position — "does this person speak from a stated position?" prevents the AI default of generic unmarked voice.
- Pass 5 calibrate: cultural dimension added — the diagnostic asks about rhetorical convention expectations, not just knowledge depth.

### Anti-AI-ism Mechanisms

1. **Never run Pass 4 on structurally disordered prose.** Coherent-sounding confusion is the failure mode.
2. **Never declare stabilization after one round** unless all five passes found only cosmetic changes.
3. **Never apply Pass 3 before Pass 2.** Voice on dishonest claims amplifies, not repairs, the honesty problem.
4. **Never strip hedges without the hedging split.** Pass 2's signal-confidence and Pass 1's strengthen both require the split.
5. **Never skip Pass 0.** Tradition and position context must be established before any technique fires.
6. **Never smooth productive friction in Pass 3.** Irregular rhythm, unresolved tension, and deliberate register shifts are asked about before normalized.

### Refactoring Plan

**Source:** `plugins/expression/commands/redraft.md` — promotes to `plugins/expression/skills/redraft/SKILL.md`.

**Changes from current command:**

1. Add Pass 0 (tradition + position lens — this is the primary structural change)
2. Add cultural dimension to Pass 1 structural diagnostic (tradition-relativized clarity)
3. Add hedging split to Pass 1 strengthen and Pass 2 signal-confidence (explicit distinction)
4. Add position to Pass 3 voice
5. Add cultural dimension to Pass 5 calibrate
6. Add technique-omit to Pass 1 (gap-check before additions)
7. Add technique-position to Pass 0 and Pass 3

**Delete:** `plugins/expression/commands/redraft.md`

### SKILL.md Outline

```
---
(frontmatter)
---

# Refine

One paragraph: multiplicative cascade. Each pass makes subsequent passes more effective.
Contrast with /clarify (Clarity only) and /expression (ad-hoc techniques).

## Why This Order
Pass 0 (lens) → Clarity (structure) → Integrity (honesty) → Narrative (craft) →
Generative (meaning) → Connection (audience). Brief rationale.

## NEVER
4-5 guards. Run Pass 4 on disordered prose. Declare stabilization after one round.
Apply Pass 3 before Pass 2. Skip Pass 0.

## Pass 0: Orient
Tradition lens + position. How they modify downstream passes.
@${CLAUDE_PLUGIN_ROOT}/references/technique-tradition.md
@${CLAUDE_PLUGIN_ROOT}/references/technique-position.md

## Pass 1: Clarity
Tradition-relativized diagnostics. Hedging split.
[technique refs]

## Pass 2: Integrity
Hedging split (mandatory). Scope. Assumptions.
[technique refs]

## Pass 3: Narrative
Arc, rhythm, voice (+position), diction, tone.
[technique refs]

## Pass 4: Generative
Implications, dimensionalize, questions. NEVER guard.
[technique refs]

## Pass 5: Connection
Calibrate (+cultural dimension), bridge (+cross-cultural).
[technique refs]

## Convergence
Continue vs. stabilize criteria. Typical 2-3 cycles.

## Usage Modes
Full cascade (default). Targeted pass. Iterative refinement for long documents.
Triage table: symptom → start with pass.
```

### References Needed

All existing technique files (moved from `skills/expression/references/` to `plugins/expression/references/`), plus:

- `references/technique-omit.md` (new)
- `references/technique-position.md` (new)
- `references/technique-tradition.md` (new)

---

## Skill 5: `recast`

### Metadata

```yaml
---
name: recast
description: This skill should be used when the user asks to "adapt this for a US audience",
  "this works in my tradition but not theirs", "translate the argument structure not the words",
  "why does my writing feel foreign despite correct English?", "reframe this for [culture/tradition]",
  "make this land for [audience]", "adjust the rhetoric not just the words", or when prose is
  grammatically correct but culturally misaligned with its target audience. Applies rhetorical
  tradition adaptation without losing content.
user-invocable: true
context: fork
---
```

### Problem It Solves

Prose can be grammatically flawless in English and still fail to communicate — not because the words are wrong but because the argument's structure operates in a different rhetorical tradition than the target audience expects. Arabic parallel-restatement reads as repetitive to Anglo-American audiences. French dialectical structure reads as evasive. Japanese indirection reads as unclear. The problem is not vocabulary or grammar — it is rhetorical convention. `/recast` adapts argument structure to function within the target tradition without altering content.

This is distinct from translation (different languages) and from editing (prose quality). It is structural adaptation across rhetorical traditions.

### Phase Design

```
Identify Source → Identify Target → Map Divergence → Adapt → Annotate
```

**Phase 1: Identify Source Tradition**

Analyze the existing prose to identify what rhetorical tradition produced it. Load: technique-tradition.

Signals to look for:

- Organizational logic (linear → Anglo-American; parallel/associative → Arabic/Semitic; dialectical → French; indirect → Japanese; circular/spiral → many oral traditions)
- Epistemic conventions (directness/assertion → Anglo-American; nuanced hedging → Japanese; thorough scaffolding → German academic)
- High-context vs. low-context (what is explicit vs. implied)
- Positional conventions (how the writer positions themselves relative to the subject)

**Phase 2: Identify Target Tradition**

User specifies or implies target audience. If not explicit, ask:

- Who is the primary audience for this in its new form?
- What country or professional context?
- What communication norms does that context carry?

**Phase 3: Map Divergence**

Identify the specific differences between source and target tradition that will require adaptation:

| Dimension | Typical Source vs. Target Differences |
|-----------|--------------------------------------|
| Organization | Parallel/circular vs. linear-deductive |
| Position-taking | Dialectical (hold contradiction first) vs. thesis-first |
| Explicitness | High-context (implied) vs. low-context (stated) |
| Certainty | Hedged/graduated vs. assertive |
| Elaboration | Extended scaffolding vs. economical |

**Phase 4: Adapt**

Transform the structure to function within the target tradition. Scope constraints:

- Adapt organization (argument structure, sequencing)
- Adapt positional conventions (where the writer's stance appears)
- Adapt explicitness calibration (high-context → low-context: make implied explicit; reverse if applicable)
- **Do not** adapt content (what is claimed), voice (how it sounds), or vocabulary (specific word choices) — this is structure adaptation only

**Phase 5: Annotate**

Produce the adapted version with annotation:

- What structural moves were made (e.g., "moved thesis from conclusion to opening paragraph")
- What the original version did that the adapted version cannot (e.g., "your original demonstrated dialectical rigor by holding the counter-argument before committing; the adapted version loses this intellectual move")
- Whether the original structure could be preserved with explanatory scaffolding for the target audience (sometimes the right answer is: explain the structure, not abandon it)

Offer the option: "I can also provide a version that keeps your original rhetorical structure and adds a brief framing note for your audience explaining how to read it. Sometimes the move that feels foreign is the strongest part."

### Technique Assignments

| Phase | Techniques |
|-------|-----------|
| Identify Source | tradition (full analysis) |
| Identify Target | calibrate (audience analysis), tradition |
| Map Divergence | tradition (comparative analysis) |
| Adapt | clarify (resequencing), arc (arc redesign for target), calibrate (explicitness calibration) |
| Annotate | position (what position the adaptation preserves or loses) |

### Cross-Cultural Integration

This skill exists because of the culture-researcher's core finding: Anglo-American rhetorical conventions are not universal, and treating them as such silently erases other traditions. Every diagnostic in this skill requires knowing both the source and target tradition before making any judgment. The framing is always: "in the source tradition, this structure does X; in the target tradition, X is achieved differently."

### Anti-AI-ism Mechanisms

1. **Never treat the source tradition as deficient.** The source prose is operating within a coherent rhetorical system. Adaptation is not correction.
2. **Never silently normalize to Anglo-American English.** Annotate every significant structural adaptation. "I changed X to Y" must be accompanied by "X was doing Z in your tradition; Y does the equivalent in English academic writing."
3. **Never adapt content along with structure.** Scope is enforced: structure only. If the user's ideas change in the adaptation, that is a failure.
4. **Never assume the user wants full adaptation.** Always offer the "explain the original structure" option. Sometimes preserving the rhetorical tradition with a framing note is stronger than adapting away from it.
5. **Never adapt voice, vocabulary, or specific word choices** unless explicitly requested.

### Refactoring Plan

**What's new:** Entirely new skill. No existing command or technique covers rhetorical tradition adaptation.

**Absorbs:** `/tone-match` (proposed but eliminated in filtering) — tone transformation is a subset of tradition adaptation when the mismatch is register-level rather than structural.

**Location:** `plugins/expression/skills/recast/SKILL.md`

**Distinction from `help-me-say`:** `help-me-say` addresses thoughts that resist English expression (the ontology bridging problem for the writer). `recast` addresses prose that's already in English but won't function for the target audience (the rhetorical convention mismatch problem for the reader).

### SKILL.md Outline

```
---
(frontmatter)
---

# Recast

One paragraph: rhetorical tradition adaptation. Not editing. Not translation. Structure adaptation.

## What This Skill Is Not
Not grammar correction. Not stylistic improvement. Not translation.
It is: making the argument's structure work in a different rhetorical tradition.

## When to Use Recast
Prose is correct but feels "foreign." Audience has different organizational expectations.
Moving between rhetorical traditions (Arabic → Anglo-American, French → US business, etc.)

## NEVER
5 guards. Treat source as deficient. Silently normalize. Adapt content. Skip annotation.
Adapt voice or vocabulary without being asked.

## Phase 1: Identify Source
What tradition produced this? What organizational logic is operating?
@${CLAUDE_PLUGIN_ROOT}/references/technique-tradition.md

## Phase 2: Identify Target
Audience specification. What tradition do they expect?

## Phase 3: Map Divergence
The 5 dimensions: organization, position-taking, explicitness, certainty, elaboration.
Tradition comparison table.

## Phase 4: Adapt
Scope is structure only. What moves. What doesn't.

## Phase 5: Annotate
What changed. What was lost. The "explain instead of adapt" offer.

## Tradition Reference
Key signatures by tradition (short table). Full reference: technique-tradition.md.
```

### References Needed

- `references/technique-tradition.md` (new — primary reference for this skill)
- `references/tradition-signatures.md` — Extended tradition signatures table: source tradition → structural signature, typical organization, epistemic conventions, high/low-context position, positional conventions. Allows rapid identification without loading full technique-tradition.md.

---

## Skill 6: `expression`

### Metadata

```yaml
---
name: expression
description: This skill should be used when the user asks to "improve my writing", "apply expression
  techniques", "refine this prose", "make this clearer", "help me express this better", "edit for
  clarity", "strengthen this writing", "fix passive voice", "remove weasel words", "apply [specific
  technique] to this", or when systematic writing improvement via ad-hoc technique selection is needed
  (as opposed to a full workflow skill like /clarify or /redraft).
user-invocable: true
context: fork
---
```

### Problem It Solves

Users who know what their prose needs and want direct technique access without workflow overhead. The technique library provides 21 diagnostic-question-to-technique routes. It is the reach-for-as-needed tool, not a phased workflow.

### Structure

Diagnostic-question routing table: 21 techniques across 5 categories (+ tradition meta-lens).

**Tradition meta-lens (load before any technique):**

Before any technique is applied, identify the rhetorical tradition. Load: technique-tradition. This modifies how all diagnostic questions fire.

**Clarity (6 techniques):**

| Diagnostic Question | Technique |
|--------------------|-----------|
| Can a reader follow the argument's logic — within this tradition? Where do concepts appear before their foundations? | technique-clarify |
| Are actors visible or hidden? Where does passive voice obscure who does what? | technique-activate |
| Does language commit or cushion? Where do hedges, weak verbs, or filler phrases weaken assertion? (Apply hedging split first) | technique-strengthen |
| Do abstractions have grounding? What claims need concrete examples? | technique-illustrate |
| Is this gap intentional? What is the prose deliberately withholding? | technique-omit |
| Is this abstract? What witnessed, situated detail could replace this category description? | technique-ground |

**Integrity (3 techniques):**

| Diagnostic Question | Technique |
|--------------------|-----------|
| Does certainty match evidence? Where does absolute language describe inferred content? | technique-signal-confidence |
| Where does this apply, and where does it break down? What boundary conditions go unstated? | technique-bound-scope |
| What must be true for this reasoning to hold? What premises operate silently? | technique-surface-assumptions |

**Narrative (6 techniques):**

| Diagnostic Question | Technique |
|--------------------|-----------|
| What tension drives this forward? Is there shape, or just sequence? | technique-arc |
| Do sentences cluster at similar lengths? Where does rhythm flatten? | technique-rhythm |
| Does this sound like one person wrote it? Does that person speak from a position? | technique-voice |
| Does each word carry its weight? Where do AI patterns appear? | technique-diction |
| What emotional register does this purpose require? Where does tone clash? | technique-tone |
| Who speaks, and from what relationship to this subject? What can they legitimately claim? | technique-position |

**Generative (3 techniques):**

| Diagnostic Question | Technique |
|--------------------|-----------|
| What follows from these claims that goes unsaid? What implications lurk? | technique-extract-implications |
| Where does feedback conflate distinct concerns? What dimensions hide? | technique-dimensionalize |
| Does this prose close inquiry or open it? Where could questions invite exploration? | technique-pose-questions |

**Connection (2 techniques + tradition):**

| Diagnostic Question | Technique |
|--------------------|-----------|
| What does this audience already know, and what rhetorical conventions do they expect? Where does depth or convention mismatch? | technique-calibrate |
| What unfamiliar concepts appear without anchoring? What analogies or bridges could connect? | technique-bridge |
| What rhetorical tradition is this prose operating in? Does the diagnostic I'm about to apply fit? | technique-tradition (meta-lens) |

### Technique Assignments

All 21 techniques. Files at: `@${CLAUDE_PLUGIN_ROOT}/references/technique-{name}.md`

### Default Triage Path

When the entry point is vague ("improve my writing"), check structural clarity first. Default path: tradition (load first) → clarify → activate → strengthen → signal-confidence.

### Cross-Cultural Integration

- Tradition meta-lens is loaded before any technique, not as one option among many.
- Diagnostic questions are updated to tradition-relative phrasing (see table above).
- Calibrate diagnostic adds rhetorical convention dimension to knowledge-depth question.
- Voice diagnostic adds positional question.
- Strengthen diagnostic includes hedging split language.

### Anti-AI-ism Mechanisms

The existing NEVER guards remain. New additions:

1. **Never apply Clarity diagnostics without tradition context.** The tradition meta-lens must be loaded first.
2. **Never treat all hedging as weakness.** The strengthen technique's hedging split is mandatory.
3. **Never fill a gap before asking if it's doing rhetorical work.** Technique-omit pre-check before technique-illustrate.

### Refactoring Plan

**Source:** `plugins/expression/skills/expression/SKILL.md` — retains the name `expression` as the technique library. The composition workflow takes the name `/writing`.

**Changes:**

1. Update diagnostic questions to be tradition-relative (see tables above)
2. Add 4 new techniques to routing table: omit, ground, position, + tradition as meta-lens
3. Add tradition meta-lens section (load before any technique)
4. Update voice diagnostic to include position question
5. Update calibrate diagnostic to include rhetorical convention question
6. Add hedging split language to strengthen diagnostic
7. Update technique count: "21 techniques" (was 17)

**Technique files:** All move from `plugins/expression/skills/expression/references/` to `plugins/expression/references/` (plugin root). References in SKILL.md updated accordingly.

### SKILL.md Outline

```
---
(frontmatter)
---

# Expression

One paragraph: 21-technique library for ad-hoc prose improvement. Direct technique access
without workflow overhead. When to use expression vs. /clarify vs. /redraft.

## Tradition Meta-Lens

Load before any technique. Why it matters. How it modifies diagnostics.
@${CLAUDE_PLUGIN_ROOT}/references/technique-tradition.md

## Default Triage Path
When unsure where to start: tradition → clarify → activate → strengthen → signal-confidence.

## How to Use Expression
Interrogate prose with diagnostic questions. Each question that surfaces issues points to its technique.

## Clarity (6 techniques)
Routing table with updated tradition-relative diagnostics.

## Integrity (3 techniques)
Routing table.

## Narrative (6 techniques)
Routing table with updated voice + position question.

## Generative (3 techniques)
Routing table.

## Connection (2 techniques + tradition)
Routing table with updated calibrate + rhetorical convention question.

## NEVER
Existing guards + 3 new ones: tradition context before clarity, hedging split mandatory,
gap-check before fill.

## Loading Techniques
@${CLAUDE_PLUGIN_ROOT}/references/technique-{name}.md
CRITICAL: technique file must be loaded before claiming to apply it.

## Technique Library
21 techniques in plugins/expression/references/.
```

---

## Structural Changes Summary

### Skill Count and Names

| Current | Proposed | Change |
|---------|----------|--------|
| `expression:expression` (library) | `expression:expression` (library, updated) | Name kept; content updated with 4 new techniques + tradition-aware diagnostics |
| `expression:clarify` (command) | `expression:clarify` (skill) | Promoted from commands/ to skills/; Orient + Verify phases added |
| `expression:redraft` (command) | `expression:redraft` (skill) | Promoted from commands/ to skills/; Pass 0 added |
| *(none)* | `expression:composition` | New composition workflow |
| *(none)* | `expression:help-me-say` | New ontology-bridging skill |
| *(none)* | `expression:structure` | New rhetorical tradition adaptation skill |

### Commands Directory

`plugins/expression/commands/` — deleted. Both existing commands promoted to skills.

- `commands/clarify.md` → `skills/clarify/SKILL.md`
- `commands/redraft.md` → `skills/redraft/SKILL.md`

### Technique File Migration

All technique files move from `plugins/expression/skills/expression/references/` to `plugins/expression/references/` (plugin root).

New technique files to create:

- `references/technique-omit.md`
- `references/technique-position.md`
- `references/technique-ground.md`
- `references/technique-tradition.md`

New reference files to create (non-technique):

- `references/frame-guide.md` (for writing skill — Frame phase extended guidance)
- `references/translanguaging-guide.md` (for help-me-say)
- `references/language-patterns.md` (for help-me-say)
- `references/tradition-signatures.md` (for recast)

### Plugin.json Changes

Add to skills: `writing`, `help-me-say`, `recast`.
Update existing: `proofread` (skill location), `refine` (skill location).
Remove from commands: `proofread`, `refine`.
Update `expression` skill description (library, 21 techniques, tradition meta-lens).

---

## Shared Infrastructure

### Grounding Principles

All 6 skills are evaluated against the 10 principles in `docs/ideas/expression-workflows/grounding-principles.md`. A skill that violates any principle has a design flaw, not a feature.

### Principle → Skill Application Matrix

| Principle | `writing` | `help-me-say` | `proofread` | `refine` | `recast` | `expression` |
|-----------|-----------|--------------|-------------|----------|----------|-------------|
| P0 Necessity | Frame: "why must this be written?" | User's felt need to articulate | Orient: "why does this exist?" before diagnosing | Pass 0 guards against loss | "why must this work for that audience?" | Available via technique-position |
| P1 Purpose | Frame phase (recursive via Discover loop) | Articulating a specific intent | Scope-check before editing | Pass 0 establishes; convergence checks | Target audience purpose | Diagnostic routing |
| P2 Tradition | Orient mandatory; Structure tradition-relative | L1 tradition identified in Identify | Orient mandatory; clarity reframed | Pass 0 mandatory; all passes modified | Core of the skill | Tradition meta-lens loaded first |
| P3 Position | Frame: 3 position questions mandatory | L1 speaker's position named | L1 pattern check in voice + language | Pass 0 + Pass 3 position extended | Annotates what position survives adaptation | technique-position available |
| P4 Subtraction | Compose: practice deliberate omission | Annotation honors source compression | Gap-check before every addition | technique-omit in Pass 1; gap-check | Annotates what original structure withheld | technique-omit available |
| P5 Difficulty | Compose: follow the surprising sentence | Annotation distinguishes compression from loss | Load-type preserved; intrinsic complexity kept | Load-type across all passes | Preserves content difficulty while adapting structure | technique-clarify load-type |
| P6 Discovery | Discover phase: Frame → Discover loop normalized | Reveals what user didn't know they meant | Post-edit: surviving content reveals purpose | Convergence is multiplicative discovery | Discovery of what structure-adaptation costs | Ad-hoc use surfaces issues |
| P7 Epistemic honesty | Discover: calibrate claims | Annotate where meaning shifted | Hedging split in language audit | Hedging split in Pass 1 + Pass 2 | Annotates certainty convention differences | technique-signal-confidence, hedging split |
| P8 Grammar as philosophy | Frame preserves L1 framing if meaningful | Core mechanism of the skill | L1 structures diagnosed, not corrected | Pass 0 tradition lens; Pass 1 L1-aware | Preserves L1 content while adapting structure | technique-tradition + activate/strengthen revised |
| P9 Reader as participant | Polish: who receives this? | User's reader named | Audience + purpose before editing | Pass 5 calibrate + bridge | Target audience is the central question | technique-calibrate + technique-bridge |

### Anti-AI-ism Commitments (Shared)

All 6 skills share these behavioral requirements:

1. **Do not fill intentional gaps.** Ask whether the gap is doing rhetorical work before suggesting an addition. Every skill loads technique-omit for this check.

2. **Do not smooth productive friction.** Do not regularize rhythm, eliminate repetition, or normalize register shifts without asking whether the irregularity is intentional.

3. **Do not default to disclosure over restraint.** Do not add topic sentences, transitions, or explanatory frames when the rhetorical tradition achieves power through implication.

4. **Do not substitute category for experience.** Load technique-ground before reaching for an abstract noun. Situated, witnessed detail over generic description.

5. **Do not simulate position without stakes.** If the writer hasn't specified their relationship to the subject, ask — do not construct a generic authorial voice.

6. **Do not treat all hedging as weakness.** Apply the hedging split in every skill that touches confidence or language commitment.

7. **Do not resolve tension prematurely.** Unresolved contradiction may be the point. Relevant skills: proofread (Verify phase), refine (Pass 1 + Converge), writing (Compose + Discover).

8. **Do not treat Anglo-American rhetorical conventions as defaults.** Every workflow skill loads tradition in its Orient phase before any other technique fires.

---

## Implementation Notes

### Recommended Implementation Order

1. **Migrate technique files** to `plugins/expression/references/` (mechanical; enables everything else)
2. **Create 4 new technique files** (omit, position, ground, tradition) — substantial content work
3. **Promote `/clarify`** from command to skill — lowest risk, most complete source
4. **Promote `/redraft`** from command to skill — add Pass 0 (primary new content)
5. **Update `/expression`** technique library — add new techniques, update diagnostics
6. **Create `/composition`** — largest new skill; uses all the new techniques
7. **Create `help-me-say`** — requires translanguaging-guide.md and language-patterns.md
8. **Create `/recast`** — requires tradition-signatures.md; builds on tradition meta-lens
9. **Update plugin.json** and delete commands/ directory

### Open Questions for Implementation

1. **`expression` skill identity after rename:** The YAML `name` field stays `expression`; the user-invocable trigger stays `/expression`. The composition workflow's name is `writing`. Is this naming clear enough, or should the library be renamed to distinguish it from the old monolithic "expression" skill?

2. **`help-me-say` language detection:** When the user provides L1 text, detection is clear. When they describe the concept in English, detection requires asking. Should the skill always ask for explicit language confirmation before Phase 3, or only when ambiguous?

3. **Pass 0 tradition identification method:** How specific should the tradition identification be? The culture-researcher identifies 8 major traditions with distinct structural signatures. Should Pass 0 use a classification table, or leave it to diagnostic judgment?

4. **`recast` scope:** The skill is scoped to structure-only adaptation. When users ask for tone adaptation alongside structure adaptation, should `/recast` expand its scope or redirect to `/redraft` for tone work?

5. **Technique-tradition as meta-lens vs. technique:** The grounding-principles document and this PRD both treat tradition as a meta-lens, not a technique in a category. But the expression skill's routing table needs an entry for it. Current resolution: tradition appears in the Connection category routing table as "this is the meta-lens, load before any other technique." Is this presentation clear enough?

6. **`/feedback` as separate skill vs. mode within `/proofread`:** This PRD merges `/feedback` (diagnosis without repair) into `/proofread` as a flag-only mode. A late-stage review argued for keeping `/feedback` separate on the grounds that it is the primary implementation site for SC-D (investigative-before-corrective). The argument: `/feedback`'s first move should be purely descriptive ("this text uses parallel elaboration with delayed thesis — the hedging pattern encodes epistemic calibration, not uncertainty") before any evaluative pass. This stance is harder to implement cleanly as a mode within `/proofread`, which has repair as its structural goal. Keeping it separate would bring the skill count to 7 (within HC5 budget). The implementation session should decide: does the investigative-first stance fit cleanly as a `/proofread` mode, or does it need its own phase structure?

7. **`/recast` annotation language:** A specific annotation example from the ideation phase that should be incorporated into `/recast`'s SKILL.md (or `tradition-signatures.md`): "Your parallel elaboration was compressed into a linear argument. The accumulative persuasion was replaced by hierarchical evidence. The reader will process this faster but will not feel the weight of the repeated pattern." This level of specific annotation — naming what the rhetorical move *did* and what the adaptation *costs* — should be the standard for `/recast`'s annotate phase, not just a general "things were changed."
