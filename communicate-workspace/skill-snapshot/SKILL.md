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

Comprehensive written expression skill. 16 techniques across 5 categories (plus a tradition meta-lens and omit gate) for crafting prose that communicates clearly, honestly, engagingly, and appropriately for its audience and rhetorical tradition. Routes to structured workflows for common tasks or applies techniques ad-hoc.

## Intent Routing

Detect user intent and route to the appropriate mode. When ambiguous, default to ad-hoc technique application. If scope becomes clear mid-conversation, route to the appropriate workflow.

| Intent Signal | Route | Load |
|---------------|-------|------|
| Improve/refine specific issues, apply techniques, fix passive voice, remove weasel words | **Ad-hoc** (use diagnostic tables below) | Technique files as needed |
| "proofread", "check my writing", "clean this up", "edit this", "fix my draft", structured clarity audit | **Clarify** | `@./references/workflow-clarify.md` |
| "make this as good as it can be", "full refinement", "polish thoroughly", "this needs to persuade" | **Redraft** | `@./references/workflow-redraft.md` |
| "help me write", "draft this", "compose", "I have something to say", blank-page creation | **Compose** | `@./references/workflow-compose.md` |
| "adapt for audience", "translate the structure", "why does my writing feel foreign?", cross-tradition | **Structure** | `@./references/workflow-structure.md` |
| "help me say this", "I can't find the right words", "in [language] we say...", cross-lingual bridging | **Bridge** | `@./references/workflow-bridge.md` |

**Bridge as interrupt:** The Bridge workflow can interrupt any active workflow. When a thought resists English expression mid-workflow, load `@./references/workflow-bridge.md` for the stuck passage, then return to the active workflow.

## Context Loading

Load only what the current route requires. Never load all references upfront.

| Route | Load | Do NOT Load |
|-------|------|-------------|
| Ad-hoc | `tradition.md` first, then technique files by diagnostic question | `workflow-*.md` files |
| Clarify | `workflow-clarify.md` (loads its own techniques by phase) | Other `workflow-*.md`, `index.md` |
| Redraft | `workflow-redraft.md` (loads its own techniques by pass) | Other `workflow-*.md`, `index.md` |
| Compose | `workflow-compose.md` (loads its own techniques by phase) | Other `workflow-*.md` |
| Structure | `workflow-structure.md`, `tradition-signatures.md` | Other `workflow-*.md` |
| Bridge | `workflow-bridge.md`, `translanguaging-guide.md`, `language-patterns.md` | Other `workflow-*.md` |
| Technique navigation | `index.md` | `workflow-*.md` files |

## Tradition Meta-Lens and Omit Gate

**Tradition.** Load before any technique. Identify the rhetorical tradition operating in the prose before applying diagnostics — this prevents Anglo-American conventions from functioning as an invisible default and modifies how all downstream questions fire.

```text
@./references/tradition.md
```

Why it matters: every diagnostic question below assumes a rhetorical context. "Can a reader follow linearly?" fails for Arabic parallel-restatement. "Does language commit?" fails for Japanese epistemic calibration. Tradition identification prevents misdiagnosis.

**Omit gate.** Before repairing any passage, ask: *Should this content exist at all?* Not every gap is a flaw — some silences are structural. Intentional omission sharpens focus by refusing to dilute a point. Strategic silence lets the reader complete the thought, which lands harder than spelling it out. Productive ambiguity preserves openness where premature precision would close inquiry. If the answer is "this content shouldn't exist," the repair is deletion, not technique application.

## Orientation

Treat reader attention as finite. Interrogate each word: does it earn its place?

Difficulty should come from complex ideas, not complex sentences. When prose is hard to parse, the writer has shifted work to the reader. Expression techniques identify where this happens and provide repair strategies.

**Most common failures — watch for these before loading technique files:**

- **NEVER** let abstractions float without grounding — load illustrate (which includes grounding moves) to anchor claims in concrete instances.
- **NEVER** preserve passive voice because it sounds formal — passives hide actors, which hides responsibility.
- **NEVER** conflate confidence with certainty — absolute language on inferred content creates dishonest prose.
- **NEVER** allow AI diction patterns to survive: "it's worth noting", "it's important to", "in conclusion" — these are register failures, not stylistic choices.
- **NEVER** fix word-level issues before structural ones — hedges and weak verbs on misordered prose are noise, not signal.
- **NEVER** treat all hedging as weakness — hedging split (calibration vs. cushioning) is mandatory.

**Default triage path:** When unsure where to start, load tradition first, then check form-function alignment, then structural clarity — most prose problems are sequence problems. The default path is: tradition (load first) → fit → clarify → activate → strengthen → signal-confidence.

## Diagnostic Questions

When improving prose ad-hoc, interrogate it with diagnostic questions. Each question that surfaces issues points to its technique file for detailed repair instructions.

### Purpose

| Diagnostic Question | Load Technique |
|---------------------|----------------|
| Does the form match the function? Where does the shape undermine the intent? | `@./references/fit.md` |
| What does this audience already know? Where does depth or convention mismatch? | `@./references/calibrate.md` |
| What unfamiliar concepts appear without anchoring? What analogies could bridge? | `@./references/bridge.md` |

### Clarity

| Diagnostic Question | Load Technique |
|---------------------|----------------|
| Can a reader follow the argument's logic — within this tradition? Where do concepts appear before their foundations? | `@./references/clarify.md` |
| Are actors visible or hidden? Where does passive voice obscure who does what? | `@./references/activate.md` |
| Does language commit or cushion? Where do hedges, weak verbs, or filler phrases weaken assertion? (Apply hedging split first) | `@./references/strengthen.md` |
| Do abstractions have grounding? What claims need concrete examples? What witnessed detail could replace category descriptions? | `@./references/illustrate.md` |

### Integrity

| Diagnostic Question | Load Technique |
|---------------------|----------------|
| Does certainty match evidence? Where does absolute language describe inferred content? | `@./references/signal-confidence.md` |
| Where does this apply, and where does it break down? What boundary conditions go unstated? | `@./references/bound-scope.md` |
| What must be true for this reasoning to hold? What premises operate silently? | `@./references/surface-assumptions.md` |

### Shape

| Diagnostic Question | Load Technique |
|---------------------|----------------|
| What tension drives this forward? Is there shape, or just sequence? | `@./references/arc.md` |
| Is the ordering purposeful? Where does the sequence feel arbitrary? | `@./references/arrange.md` |
| Do sentences cluster at similar lengths? Where does rhythm flatten? | `@./references/rhythm.md` |
| Does this sound like one person wrote it? Does that person speak from a stated place? | `@./references/voice.md` |
| Does each word carry its weight? Does the emotional register fit the purpose? | `@./references/register.md` |

### Depth

| Diagnostic Question | Load Technique |
|---------------------|----------------|
| What follows from these claims that goes unsaid? What implications lurk? | `@./references/extract-implications.md` |
| Where does feedback conflate distinct concerns? What dimensions hide? | `@./references/dimensionalize.md` |
| Does this prose close inquiry or open it? Where could questions invite exploration? | `@./references/pose-questions.md` |

## Loading Techniques

To apply a technique, load its reference file:

```text
@./references/{name}.md
```

**CRITICAL:** A technique reference file MUST be loaded before claiming to apply that technique. Reading the technique name in this skill file does NOT constitute applying the technique.

## Technique Library

16 techniques in `./references/`.

| Category | Techniques |
|----------|------------|
| Purpose | fit, calibrate, bridge |
| Clarity | clarify, activate, strengthen, illustrate |
| Integrity | signal-confidence, bound-scope, surface-assumptions |
| Shape | arc, arrange, rhythm, voice, register |
| Depth | extract-implications, dimensionalize, pose-questions |
| Meta-lens | tradition (load before any other technique) |

**Load the full technique index for extended navigation:**

```text
@./references/index.md
```

## Ad-Hoc Use

For applying techniques outside workflow routes:

1. **Load tradition lens** — identify the rhetorical tradition before any diagnostic
2. **Check the omit gate** — ask whether the content should exist before repairing it
3. **Interrogate the prose** with diagnostic questions from the tables above
4. **Select technique(s)** based on which questions surface issues
5. **Load technique reference file(s)** for detailed instructions
6. **Follow the Instructions section** of each loaded technique

## NEVER

- **NEVER** apply any diagnostics without first loading tradition — tradition meta-lens must precede all technique application.
- **NEVER** treat all hedging as weakness — the hedging split is mandatory: distinguish epistemic calibration (preserve) from habitual cushioning (cut).
- **NEVER** smooth productive friction without asking — irregular rhythm, unresolved tension, and deliberate register shifts are interrogated before normalized.
- **NEVER** fill intentional gaps — gap-check precedes every addition: ask "is this gap doing rhetorical work?" before filling.
- **NEVER** correct L1 grammatical patterns as errors — diagnose what the pattern encodes before treating it as a problem.
- **NEVER** fix word-level issues before structural ones — hedges and weak verbs on misordered prose are noise, not signal.
- **NEVER** default to Anglo-American conventions invisibly — name tradition-specific choices as tradition-specific, not universal.

## Additional Resources

- **`@./references/clarify-patterns.md`** — Detection heuristics and repair strategies
- **`@./references/clarify-examples.md`** — Before/after transformations by issue type
