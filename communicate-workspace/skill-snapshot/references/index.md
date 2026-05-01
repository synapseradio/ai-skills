# Expression Technique Index

Navigate the 16 expression techniques through diagnostic questions. Each question directs investigation of the prose; when issues surface, the linked technique provides repair strategies.

## How to Use This Index

Ask each diagnostic question of the prose under review. Questions that surface issues point to their technique. Load the technique file for detailed repair instructions:

```
@./references/{name}.md
```

---

## Pre-flight

Before entering the diagnostic categories, two checks gate all technique work.

**Tradition context.** Every diagnostic question below assumes a rhetorical tradition. "Can a reader follow linearly?" fails for Arabic parallel-restatement. "Does language commit?" fails for Japanese epistemic calibration. Load tradition identification before applying any category — it prevents misdiagnosis by surfacing the conventions actually operating in the prose.

```
@./references/tradition.md
```

**Omit gate.** Before repairing any passage, ask: *Should this content exist at all?* Not every gap is a flaw — some silences are structural, carrying meaning through what they decline to say. Intentional omission sharpens focus by refusing to dilute a point. Strategic silence lets the reader complete the thought, which lands harder than spelling it out. Productive ambiguity preserves openness where premature precision would close inquiry. If the answer is "this content shouldn't exist," the repair is deletion, not technique application.

---

## 1. Purpose

Does this prose serve its communicative goal?

### Diagnostic Questions

- **Does the form match the function?** Where does the shape undermine the intent? Is this argumentative when it should be expository? Evocative when it should be precise? Dense when it should be accessible? → `fit.md`

- **What does this audience already know?** Where does depth exceed or fall short of their preparation? What technical vocabulary assumes expertise? What simplifications condescend? → `calibrate.md`

- **What unfamiliar concepts appear without anchoring?** What structural analogies could make the strange accessible? Where could comparison to the familiar illuminate the new? → `bridge.md`

---

## 2. Clarity

Can a reader follow this prose without effort?

### Diagnostic Questions

- **Can a reader follow linearly without backtracking?** Where do concepts appear before their foundations? Where do sentences open with unfamiliar content before anchoring on familiar ground? → `clarify.md`

- **Are actors visible or hidden?** Who performs each action? Where is the doer displaced to sentence end or omitted entirely? Where does passive voice obscure responsibility? → `activate.md`

- **Does language commit or cushion?** Where does hedging exceed epistemic need? What words soften without adding meaning? Where do nominalizations hide verbs? → `strengthen.md`

- **Do abstractions have grounding?** What claims would a reader accept definitionally but fail to recognize in practice? Where do concepts need concrete examples? Has the speaker been here — what witnessed detail could replace this category description? → `illustrate.md`

**Additional clarity resources:**

- `clarify-patterns.md` — Detection heuristics and repair strategies
- `clarify-examples.md` — Before/after transformations by issue type

---

## 3. Integrity

Does this prose accurately represent what it knows?

### Diagnostic Questions

- **Does certainty match evidence?** For each claim, what is the evidence foundation — verified, inferred, speculated? Does the certainty language reflect that foundation? Where does absolute language describe inferred content? → `signal-confidence.md`

- **Where does this apply, and where does it break down?** What boundary conditions go unstated? What contexts would invalidate these claims? Where does advice sound universal when it should be qualified? → `bound-scope.md`

- **What must be true for this reasoning to hold?** What premises operate silently beneath the visible argument? What would break if an assumption proved false? → `surface-assumptions.md`

---

## 4. Shape

Does this prose have the structure and movement its purpose requires?

### Diagnostic Questions

- **What tension drives this forward?** What does the reader want to know, and when do they get resolution? Is there shape, or just sequence? Where does information dump without engagement? → `arc.md`

- **Is the ordering purposeful?** Could a reader explain why this comes before that? Where does the sequence feel arbitrary — where would rearranging change nothing? → `arrange.md`

- **Do sentences cluster at similar lengths?** Do consecutive sentences follow the same structural template? Where does the rhythm flatten into monotony? → `rhythm.md`

- **Does this sound like one person wrote it?** Where does the sensibility shift — casual to formal, certain to hesitant — without clear purpose? Is there a coherent authorial identity? Does that person speak from a stated place? → `voice.md`

- **Does each word carry its weight, and does the emotional register fit the purpose?** Where do AI-generation patterns appear? Where does vocabulary mismatch audience or register? Where does current tone clash with purpose — too casual, too severe, too distant? → `register.md`

---

## 5. Depth

Does this prose develop what it implies?

### Diagnostic Questions

- **What follows from these claims that goes unsaid?** What consequences, requirements, or contradictions lurk in the logical wake? What implications deserve explicit attention? → `extract-implications.md`

- **Where does feedback conflate distinct concerns?** What independent aspects hide behind "needs work" or similar labels? Can the monolithic assessment be separated into improvable dimensions? → `dimensionalize.md`

- **Does this prose close inquiry or open it?** Where could a declaration become an invitation to explore? What questions does this raise that could be made explicit? → `pose-questions.md`

---

## Loading Techniques

To apply a technique, load its reference file:

```
@./references/{name}.md
```

Each technique file contains:

- **Diagnostic Question** — The question that surfaces when this technique applies
- **Instructions** — Numbered steps in imperative voice
- **Examples** — Concrete applications showing before/after transformations

---

## Quick Reference

| Purpose | Clarity | Integrity | Shape | Depth |
|---------|---------|-----------|-------|-------|
| fit | clarify | signal-confidence | arc | extract-implications |
| calibrate | activate | bound-scope | arrange | dimensionalize |
| bridge | strengthen | surface-assumptions | rhythm | pose-questions |
| | illustrate | | voice | |
| | | | register | |

---

## Sub-file References

- `clarify-patterns.md` — Detection heuristics and repair strategies for clarify
- `clarify-examples.md` — Before/after transformations by issue type for clarify
- `tradition.md` — Rhetorical tradition meta-lens (load on-demand via pre-flight)
