---
name: communicate
description: >-
  Written communication skill with 16 techniques across 5 categories and 5
  structured workflows. Use when asked to "improve my writing", "refine this
  prose", "make this clearer", "proofread this", "clean this up", "edit this",
  "check my writing", "make this as good as it can be", "full refinement",
  "polish this thoroughly", "help me write this", "draft this for me",
  "help me compose", "adapt this for a US audience", "translate the argument
  structure", "why does my writing feel foreign?", "help me say this",
  "I can't find the right words", "in [language] we say...", or when any
  writing improvement, composition, structural adaptation, or cross-lingual
  expression work is needed.
metadata:
  context: fork
---

# Communicate

Make prose sound like the writer cared, took time to say what was meant, and thought about audience and role before speaking. 16 techniques across 5 categories, plus an across-languages self-interrogation reference, a slop audit, and an omit gate. Routes to five structured workflows for common tasks or applies techniques ad-hoc.

## Intent Routing

Detect user intent and route to the appropriate mode. When ambiguous, default to ad-hoc technique application. If scope becomes clear mid-conversation, route to the appropriate workflow.

| Intent Signal | Route | Read |
|---------------|-------|------|
| Names a specific technique — "fix passive voice", "tighten rhythm", "strengthen hedging", "add an analogy" | **Direct technique** | `[{name}.md](./references/{name}.md)` (skip diagnostics) |
| Improve/refine specific issues, apply techniques, remove weasel words | **Ad-hoc** (use diagnostic tables below) | Technique files as needed |
| "proofread", "check my writing", "clean this up", "edit this", "fix my draft", structured clarity audit (includes the slop quick-check pass) | **Clarify** | [workflow-clarify.md](./references/workflow-clarify.md) |
| "make this as good as it can be", "full refinement", "polish thoroughly", "this needs to persuade" | **Redraft** | [workflow-redraft.md](./references/workflow-redraft.md) |
| "help me write", "draft this", "compose", "I have something to say", blank-page creation | **Compose** | [workflow-compose.md](./references/workflow-compose.md) |
| "adapt for audience", "translate the structure", "why does my writing feel foreign?", cross-tradition | **Structure** | [workflow-structure.md](./references/workflow-structure.md) |
| "help me say this", "I can't find the right words", "in [language] we say...", cross-lingual bridging | **Bridge** | [workflow-bridge.md](./references/workflow-bridge.md) |

### Precedence

When signals conflict, the rules below resolve which route applies:

1. **A named technique overrides a workflow trigger.** "Fix the passive voice" routes to [activate.md](./references/activate.md) directly and skips the Clarify cascade. Single-technique entry is a first-class path.
2. **Casual register overrides Compose ceremony.** "Help me draft a quick Slack message", "DM", or "chat reply" routes to ad-hoc with [register.md](./references/register.md) preloaded; the Compose Frame phase does not run for casual register.
3. **Redraft applies to substantive prose only.** Three paragraphs or more. Below that, "polish thoroughly" routes to Clarify.
4. **Compose's Frame phase applies to evergreen prose.** Single-paragraph compose asks (for example, "help me write one sentence") route to ad-hoc.

**Bridge as interrupt:** The Bridge workflow can interrupt any active workflow. When a thought resists English expression mid-workflow, read [workflow-bridge.md](./references/workflow-bridge.md) for the stuck passage, then return to the active workflow.

## Context Loading

Pre-flight files load with the skill body. Each route adds its own files on top. Workflow files load only for routes that apply.

| Route | Read | Do not read |
|-------|------|-------------|
| Pre-flight (always) | [across-languages.md](./references/across-languages.md), [avoid-slop.md](./references/avoid-slop.md) | — |
| Direct technique | [{name}.md](./references/{name}.md) for the named technique | `workflow-*.md`, `index.md` |
| Ad-hoc | Technique files by diagnostic question | `workflow-*.md` files |
| Clarify | [workflow-clarify.md](./references/workflow-clarify.md) (loads its own techniques by phase) | Other `workflow-*.md`, `index.md` |
| Redraft | [workflow-redraft.md](./references/workflow-redraft.md) (loads its own techniques by pass) | Other `workflow-*.md`, `index.md` |
| Compose | [workflow-compose.md](./references/workflow-compose.md) (loads its own techniques by phase) | Other `workflow-*.md` |
| Structure | [workflow-structure.md](./references/workflow-structure.md) | Other `workflow-*.md` |
| Bridge | [workflow-bridge.md](./references/workflow-bridge.md) | Other `workflow-*.md` |
| Technique navigation | [index.md](./references/index.md) | `workflow-*.md` files |

## Pre-flight (always read)

Two reference files are read alongside this skill body. Every downstream diagnostic assumes them as context.

**Across-languages self-interrogation.** Every diagnostic question downstream assumes a rhetorical context. "Can a reader follow linearly?" fails for Arabic parallel-restatement. "Does language commit?" fails for Japanese epistemic calibration. The self-interrogation surfaces whether organizational logic, hedging, L1 carry-over, conceptual gaps, or strategic silence are doing work the model would otherwise normalize away. Read [references/across-languages.md](./references/across-languages.md).

**Slop audit.** Lexical, structural, voice, casual-context, and intransitive-form tells, with audit diagnostics that are hard rules rather than targets. The audit applies to the model's own output. Read [references/avoid-slop.md](./references/avoid-slop.md).

**Omit gate.** Before repairing any passage, ask: *Should this content exist at all?* Not every gap is a flaw — some silences are structural. Intentional omission sharpens focus by refusing to dilute a point. Strategic silence lets the reader complete the thought, which lands harder than spelling it out. Productive ambiguity preserves openness where premature precision would close inquiry. If the answer is "this content shouldn't exist," the repair is deletion, not technique application.

## Orientation

The skill exists to make any prose — drafts, proofreads, code comments, commits, documentation, cross-cultural translation — sound like the writer chose every word. The model's default is to produce uniform sentence length, habitual transitional phrases, and a vocabulary trained on the median of training data. The skill compensates with strict rules.

Treat reader attention as finite. Each word earns its place or goes. Difficulty comes from complex ideas, not complex sentences. When prose is hard to parse, the writer has shifted work to the reader.

Variance is a hard rule, not a target. Sentence-length coefficient of variation per paragraph above 0.5; below 0.3 is broken. Paragraph-length CV above 0.4. Slop vocabulary is forbidden; the catalog lives in [references/avoid-slop.md](./references/avoid-slop.md). Tradition is a self-interrogation, not a taxonomy lookup; the questions live in [references/across-languages.md](./references/across-languages.md).

**Most common failures — watch for these before loading technique files:**

- **NEVER** let abstractions float without grounding. Load illustrate to anchor claims in concrete, witnessed detail.
- **NEVER** preserve passive voice because it sounds formal. Passives hide actors and hide responsibility.
- **NEVER** conflate confidence with certainty. Absolute language on inferred content produces dishonest prose.
- **NEVER** allow slop to survive. Uniform sentence length, habitual transitional phrases, Kobak-list vocabulary, and intransitive-form constructions ("the ***is real," "the*** is the signal," "X is Y, not Z" as default cadence) are register failures, not stylistic choices. Audit per [references/avoid-slop.md](./references/avoid-slop.md).
- **NEVER** fix word-level issues before structural ones. Hedges and weak verbs on misordered prose are noise, not signal.
- **NEVER** treat all hedging as weakness. The hedging split is mandatory: distinguish epistemic calibration (preserve) from habitual cushioning (cut).

**Default triage path:** Read across-languages first when tradition or cross-lingual signals are present. Then check form-function alignment, then structural clarity — most prose problems are sequence problems. The default order: across-languages (when applicable) → fit → clarify → activate → strengthen → signal-confidence → avoid-slop audit.

**Equity caveat.** Liang et al. (2023) found that seven AI-detection tools flagged 61% of essays by non-native English writers as machine-generated, because ESL writers draw from a smaller, more frequent vocabulary — exactly the signal the audit catches. Apply these laws to the model's own output. Never apply them to judge another writer.

## Diagnostic Questions

When improving prose ad-hoc, interrogate it with diagnostic questions. Each question that surfaces issues points to its technique file for detailed repair instructions.

### Purpose

| Diagnostic Question | Read |
|---------------------|------|
| Does the form match the function? Where does the shape undermine the intent? | [fit.md](./references/fit.md) |
| What does this audience already know? Where does depth or convention mismatch? | [calibrate.md](./references/calibrate.md) |
| What unfamiliar concepts appear without anchoring? What analogies could bridge? | [analogize.md](./references/analogize.md) |

### Clarity

| Diagnostic Question | Read |
|---------------------|------|
| Can a reader follow the argument's logic — within this tradition? Where do concepts appear before their foundations? | [clarify.md](./references/clarify.md) |
| Are actors visible or hidden? Where does passive voice obscure who does what? | [activate.md](./references/activate.md) |
| Does language commit or cushion? Where do hedges, weak verbs, or filler phrases weaken assertion? (Apply hedging split first) | [strengthen.md](./references/strengthen.md) |
| Do abstractions have grounding? What claims need concrete examples? What witnessed detail could replace category descriptions? | [illustrate.md](./references/illustrate.md) |

### Integrity

| Diagnostic Question | Read |
|---------------------|------|
| Does certainty match evidence? Where does absolute language describe inferred content? | [signal-confidence.md](./references/signal-confidence.md) |
| Where does this apply, and where does it break down? What boundary conditions go unstated? | [bound-scope.md](./references/bound-scope.md) |
| What must be true for this reasoning to hold? What premises operate silently? | [surface-assumptions.md](./references/surface-assumptions.md) |

### Shape

| Diagnostic Question | Read |
|---------------------|------|
| What tension drives this forward? Is there shape, or just sequence? | [arc.md](./references/arc.md) |
| Is the ordering purposeful? Where does the sequence feel arbitrary? | [arrange.md](./references/arrange.md) |
| Do sentences cluster at similar lengths? Where does rhythm flatten? | [rhythm.md](./references/rhythm.md) |
| Does this sound like one person wrote it? Does that person speak from a stated place? | [voice.md](./references/voice.md) |
| Does each word carry its weight? Does the emotional register fit the purpose? | [register.md](./references/register.md) |

### Depth

| Diagnostic Question | Read |
|---------------------|------|
| What follows from these claims that goes unsaid? What implications lurk? | [extract-implications.md](./references/extract-implications.md) |
| Where does feedback conflate distinct concerns? What dimensions hide? | [dimensionalize.md](./references/dimensionalize.md) |
| Does this prose close inquiry or open it? Where could questions invite exploration? | [pose-questions.md](./references/pose-questions.md) |

## Reading techniques

To apply a technique, read its reference file at `./references/{name}.md`.

**CRITICAL:** A technique reference file MUST be read before claiming to apply that technique. Reading the technique name in this skill file does NOT constitute applying the technique.

## Technique Library

16 techniques in `./references/`. Two non-technique references load alongside.

| Category | Techniques |
|----------|------------|
| Purpose | fit, calibrate, analogize |
| Clarity | clarify, activate, strengthen, illustrate |
| Integrity | signal-confidence, bound-scope, surface-assumptions |
| Shape | arc, arrange, rhythm, voice, register |
| Depth | extract-implications, dimensionalize, pose-questions |
| References | across-languages (tradition self-interrogation), avoid-slop (lexical, structural, voice tells with audit diagnostics) |

For extended technique navigation, read [references/index.md](./references/index.md).

## Ad-Hoc Use

For applying techniques outside workflow routes:

1. **Read [across-languages.md](./references/across-languages.md)** when tradition or cross-lingual signals are present — run the self-interrogation before any other diagnostic
2. **Check the omit gate** — ask whether the content should exist before repairing it
3. **Interrogate the prose** with diagnostic questions from the tables above
4. **Select technique(s)** based on which questions surface issues
5. **Read the technique reference file(s)** for detailed instructions
6. **Follow the Instructions section** of each loaded technique
7. **Run the slop audit** per [references/avoid-slop.md](./references/avoid-slop.md) before delivery — the audit diagnostics are hard rules, not targets

## Routing Disciplines

Cross-cutting rules — tradition handling, hedging split, sequencing, friction, gap-check — live in [references/never.md](./references/never.md). Two routing-specific disciplines apply at this skill's entry:

- **Apply techniques only after Pre-flight.** The self-interrogation and slop audit precede any technique application. Reading a technique name in this file does not constitute applying the technique.
- **Honor scope before invoking workflow ceremony.** The Precedence rules above resolve scope mismatches: single-paragraph Redraft routes to Clarify; single-sentence Compose routes to ad-hoc; named-technique requests skip the diagnostic cascade.

## Additional Resources

- [references/clarify-patterns.md](./references/clarify-patterns.md) — Detection heuristics and repair strategies
- [references/clarify-examples.md](./references/clarify-examples.md) — Before/after transformations by issue type
