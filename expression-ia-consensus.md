# Expression Plugin IA: Panel Consensus

Synthesis of a 4-round deliberation among Copy Editor, Rhetorician, Composition Scholar, and IA Designer. Covers the reorganization of the expression plugin's 21+ reference files.

---

## Agreements

**High confidence (all 4 panelists):**

1. **Text qualities as organizing axis.** The current axis is inconsistent — "Clarity" names a quality, "Generative" names a cognitive mode, "Integrity" names an epistemic stance, "Narrative" names a content domain. All panelists converged on organizing by observable text qualities: things an agent can inspect and score, and that diagnostic questions can address as "what property is missing or broken?"

2. **voice/tone/diction/position must be collapsed.** The four files overlap heavily and create retrieval ambiguity. All panelists agreed these should collapse, though they differed on exactly how many files to produce (2 vs. 1 vs. 2 along a fidelity/transmission split).

3. **Generative is the wrong category name and placement.** It describes a cognitive mode, not a text property. Its three techniques (extract-implications, dimensionalize, pose-questions) belong elsewhere — either as a "Completeness" or "Depth" quality cluster, or as a cross-cutting "Deepening" access mode in the index header.

4. **omit.md should not be a peer technique.** It functions as a diagnostic gate or modifier, not a standalone repair technique. It belongs as a note in the index or folded into strengthen.

5. **ground.md and illustrate.md nearly overlap.** ground is a sub-technique of illustrate; they should be merged into a single illustrate.md.

6. **tradition.md needs repositioning.** It is not a peer technique alongside clarify or arc. All panelists agreed it should function as a framing device — either a preamble in the index header or an unconditionally loaded pre-flight check.

7. **An arrangement/sequencing technique is missing.** The plugin has arc (tension-driven shape) and rhythm (sentence-level flow) but nothing for arrangement — the ordering logic of sections, paragraphs, or arguments. All panelists flagged this gap independently.

**Moderate confidence (3 of 4 panelists):**

1. **A "Purpose" or "Fit" category should precede Clarity.** The Rhetorician, IA Designer, and Copy Editor all identified that semantic fit — does this prose serve its communicative purpose? — is a prior question to clarity. The Composition Scholar absorbed this into the Fidelity mode.

2. **Net file count should decrease: ~21 → ~16.** Merges (illustrate+ground, voice+tone+diction+position → 2 files) plus the omit/tradition repositioning get the count to approximately 16 substantive technique files.

---

## Tensions

**Tension 1: Two-file vs. one-file vs. fidelity/transmission split for the register cluster.**

- Copy Editor: collapse to 2 files — `register.md` (diction+tone, sentence-level) and `voice.md` (voice+position, document-level).
- Rhetorician: split along fidelity/transmission — `register-fidelity.md` (authorial identity) and `register-transmission.md` (reader fit, absorbing calibrate+bridge).
- IA Designer: single merged `register.md` + `bridge.md` stays separate.
- Composition Scholar: `authorial-stance.md` (voice+position) + `register.md` (tone+diction).

The fidelity/transmission framing is conceptually richer but requires users to understand the distinction before using it. The scope-based framing (sentence-level vs. document-level) is more practical for quick retrieval. **Unresolved.**

**Tension 2: Where does the register/connection cluster live?**

The Copy Editor places Register and Voice in Composition (where prose takes shape). The Rhetorician places them in a standalone Register category. The IA Designer groups them with Connection. No consensus on whether these are shape techniques or audience-fit techniques. **Unresolved.**

**Tension 3: tradition.md as index prologue vs. unconditional pre-flight vs. on-demand escalation.**

- IA Designer: unconditional pre-flight, always loaded before any technique.
- Composition Scholar: structural preamble embedded in the index header.
- Copy Editor: on-demand escalation, loaded when cultural context becomes relevant.
- Rhetorician: preamble that frames the whole index epistemologically.

The IA Designer's unconditional loading is safest for correctness but adds overhead. The Copy Editor's on-demand model preserves performance. **Unresolved — requires testing against actual usage patterns.**

**Tension 4: Three diagnostic modes vs. quality categories as top-level structure.**

The Rhetorician proposed Fidelity / Transmission / Composition as top-level groupings (does text accurately represent meaning? / does it convey meaning to this reader? / does it have shape the purpose requires?). The IA Designer endorsed this as conceptually richer but deferred to qualities for practical retrieval. The Composition Scholar built the most detailed schema around this triad. The Copy Editor stayed with qualities throughout.

The three-mode model disambiguates voice/tone/diction naturally but requires users to internalize the mode distinctions first. **Unresolved — the right answer depends on whether the agent's primary task is revision diagnosis (qualities win) or rhetorical situating (modes win).**

---

## Emergent Insights

These ideas were not present in the pre-panel research and emerged from the interaction:

1. **omit as a diagnostic gate, not a technique.** The panel collectively identified that omit functions as a pass/fail filter ("should this exist at all?") before other techniques apply. This is a different logical type than a repair technique. No single panelist brought this framing; it emerged from the IA Designer's MECE analysis intersecting with the Copy Editor's practitioner experience.

2. **The three-mode model disambiguates the register cluster.** The reason voice/tone/diction resist clean merging is that they operate on different axes: "sounds like one person" is a fidelity question, "register fits this audience" is a transmission question. The Rhetorician's fidelity/transmission frame resolves a problem the quality-axis approach cannot fully solve.

3. **Generative's techniques are not generative — they are completeness checks.** extract-implications, dimensionalize, and pose-questions are not about generating new content; they're about detecting what the content implies but hasn't said. "Completeness" or "Depth" is the right quality name for this cluster.

4. **Arrangement is the missing sixth quality.** arc covers tension and shape; rhythm covers sentence flow. The gap between them — the ordering logic of arguments and sections — is a distinct quality that no current file addresses. Multiple panelists identified this independently before they explicitly compared notes.

5. **The clarify-patterns.md and clarify-examples.md sub-files suggest a scalable sub-file pattern.** If clarify warrants detailed patterns and examples as separate files, other high-traffic techniques (arc, illustrate) might warrant the same. This is an architecture question the index needs to accommodate — possibly through a `→ more` pointer convention.

---

## Recommendations

### File List (target: ~16 technique files)

**Merge operations:**

| Current Files | Becomes | Rationale |
|---|---|---|
| `illustrate.md` + `ground.md` | `illustrate.md` | ground is a sub-technique; the merged file covers both concrete examples and grounding moves |
| `voice.md` + `position.md` | `voice.md` | position (authorial stance, credibility markers) is a document-level register concern coextensive with voice |
| `tone.md` + `diction.md` | `register.md` | Both operate at sentence/phrase level, both concern reader-facing register fit |
| `omit.md` | absorbed into index as gate note | Not a peer technique; becomes a diagnostic modifier before loading any other technique |
| `tradition.md` | index preamble section | Repositioned as framing, not technique |

**New files:**

| File | Covers | Gap it fills |
|---|---|---|
| `arrange.md` | Ordering logic: argument sequence, section progression, paragraph hierarchy | The arrangement gap identified by all panelists |
| `fit.md` | Semantic fit: does this prose serve its communicative purpose? Does the form match the goal? | Purpose/fit layer before Clarity |

**Retained without change:**

`clarify.md`, `activate.md`, `strengthen.md`, `signal-confidence.md`, `bound-scope.md`, `surface-assumptions.md`, `arc.md`, `rhythm.md`, `calibrate.md`, `bridge.md`, `extract-implications.md`, `dimensionalize.md`, `pose-questions.md`

**Sub-files retained:**

`clarify-patterns.md`, `clarify-examples.md` — kept as supplemental references, linked from `clarify.md`

**Final file count: 16 technique files + 2 clarify sub-files + index = 19 total**

---

### Category Structure

Four categories ordered by diagnostic priority, preceded by a pre-flight layer:

#### Pre-flight (index preamble, not a category)

> Before applying any technique: What tradition of writing is being served? Load `tradition.md` when cultural or rhetorical context is unclear.

Gate note: Before any repair technique, ask "Should this content exist at all?" If the answer is no, cut before applying any other technique. (replaces `omit.md`)

---

#### 1. Purpose

*Does this prose serve its communicative goal?*

| Diagnostic Question | Technique |
|---|---|
| Does the form match the function — argumentative vs. expository vs. evocative? Where does the shape undermine the intent? | `fit.md` (new) |
| What does this audience already know? Where does depth exceed or fall short? | `calibrate.md` |
| What unfamiliar concepts appear without anchoring? | `bridge.md` |

---

#### 2. Clarity

*Can a reader follow this prose without effort?*

| Diagnostic Question | Technique |
|---|---|
| Can a reader follow linearly without backtracking? | `clarify.md` |
| Are actors visible or hidden? | `activate.md` |
| Does language commit or cushion? | `strengthen.md` |
| Do abstractions have grounding? | `illustrate.md` (absorbs ground) |

---

#### 3. Integrity

*Does this prose accurately represent what it knows?*

| Diagnostic Question | Technique |
|---|---|
| Does certainty match evidence? | `signal-confidence.md` |
| Where does this apply, and where does it break down? | `bound-scope.md` |
| What must be true for this reasoning to hold? | `surface-assumptions.md` |

---

#### 4. Shape

*Does this prose have the structure and movement its purpose requires?*

| Diagnostic Question | Technique |
|---|---|
| What tension drives this forward? | `arc.md` |
| Is the ordering of arguments, sections, or paragraphs purposeful? | `arrange.md` (new) |
| Do sentences cluster at similar lengths and structures? | `rhythm.md` |
| Does this sound like one person wrote it? Do credibility markers match authorial stance? | `voice.md` (absorbs position) |
| Does each word carry its weight? Does register fit this audience? | `register.md` (absorbs tone, diction) |

---

#### 5. Depth

*Does this prose develop what it implies?*

| Diagnostic Question | Technique |
|---|---|
| What follows from these claims that goes unsaid? | `extract-implications.md` |
| Where does feedback conflate distinct concerns? | `dimensionalize.md` |
| Does this prose close inquiry or open it? | `pose-questions.md` |

---

### Index Architecture

```
# Expression Technique Index

[Tradition preamble — 2–3 sentences framing tradition.md as on-demand context]
[Gate note — the omit question before any repair work]

## 1. Purpose
[diagnostic questions → fit.md, calibrate.md, bridge.md]

## 2. Clarity
[diagnostic questions → clarify.md, activate.md, strengthen.md, illustrate.md]

## 3. Integrity
[diagnostic questions → signal-confidence.md, bound-scope.md, surface-assumptions.md]

## 4. Shape
[diagnostic questions → arc.md, arrange.md, rhythm.md, voice.md, register.md]

## 5. Depth
[diagnostic questions → extract-implications.md, dimensionalize.md, pose-questions.md]

---
## Quick Reference Table
[5-column table: Purpose | Clarity | Integrity | Shape | Depth]

---
## Sub-file References
- clarify-patterns.md — detection heuristics for clarify
- clarify-examples.md — before/after transformations for clarify
- tradition.md — cultural/rhetorical framing; load when context is cross-traditional
```

---

### What to Add / Merge / Remove

| Action | File | Notes |
|---|---|---|
| **Add** | `fit.md` | New technique; covers semantic fit and form-function match |
| **Add** | `arrange.md` | New technique; covers ordering logic beyond arc |
| **Merge** | `ground.md` → `illustrate.md` | ground becomes a named move inside illustrate |
| **Merge** | `position.md` → `voice.md` | position becomes authorial-stance content in voice |
| **Merge** | `tone.md` + `diction.md` → `register.md` | new file, audience-facing register at sentence/phrase level |
| **Reposition** | `omit.md` → index gate note | content distilled to 2–3 sentences in index preamble |
| **Reposition** | `tradition.md` → index preamble + on-demand | short framing note in index; full file remains loadable |
| **Rename category** | Narrative → Shape | removes domain connotation, focuses on text property |
| **Rename category** | Generative → Depth | removes cognitive-mode connotation, names the quality |
| **Add category** | Purpose (new, precedes Clarity) | semantic fit and audience calibration as prior question |
| **Remove category** | Connection | `calibrate.md` and `bridge.md` move to Purpose |

---

## Open Questions

1. **Register split: scope-based vs. fidelity/transmission-based.** The proposal above uses a single `register.md` for the sentence/audience-level cluster and `voice.md` for the document/identity-level cluster. The Rhetorician's fidelity/transmission split is conceptually superior but may introduce disambiguation overhead. Test: does an agent reaching the index know whether their register problem is about identity or audience fit?

2. **tradition.md placement: on-demand vs. unconditional.** The proposal above uses the on-demand model (preamble note + loadable file). The IA Designer argued for unconditional pre-flight. This is a performance vs. correctness tradeoff that requires usage data to resolve.

3. **fit.md scope.** "Does this prose serve its communicative purpose?" is the right question but could expand to include genre awareness, rhetorical situation, and social function. The panel did not define the boundaries of fit.md. Should it cover only form-function match, or also audience situation and genre constraints?

4. **arrange.md relationship to arc.md.** Both address structure. The intended distinction: arc is about tension and resolution (what the reader wants to know, and when they get it); arrange is about logical ordering (sequence, hierarchy, argument structure). These need clear diagnostic questions that don't overlap, and examples that show cases where one applies but not the other.

5. **Sub-file pattern scalability.** clarify has two sub-files (patterns, examples). If arc, illustrate, or voice warrant the same depth, the index needs a consistent way to surface sub-files without cluttering the main diagnostic flow. The deliberation implied but never specified a `→ deeper: {file}` pointer convention in the index.

6. **What to do with clarify-patterns.md and clarify-examples.md.** The deliberation didn't address whether this sub-file pattern is worth extending to other techniques or whether these two files should be collapsed back into clarify.md.
