# Communicate

Written communication skill with 16 techniques and 5 structured workflows for crafting prose that communicates clearly, honestly, engagingly, and appropriately for its audience and rhetorical tradition.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy the `skills/communicate/` directory into `~/.claude/skills/communicate/`.

## Usage

### Ad-hoc technique application

```text
/communicate improve this paragraph — fix the passive voice and strengthen the hedging
```

### Clarify — fast clarity audit

```text
/communicate proofread this draft before I send it
```

### Redraft — full multi-pass refinement

```text
/communicate make this as good as it can be
```

### Compose — blank-page creation

```text
/communicate help me write an introduction for this proposal
```

### Structure — rhetorical tradition adaptation

```text
/communicate adapt this for a US business audience
```

### Bridge — cross-lingual ontology bridging

```text
/communicate in Spanish we say "tengo miedo" — how do I express that in English?
```

## How It Works

The skill detects user intent and routes to the appropriate mode:

- **Ad-hoc** — Apply individual techniques via diagnostic question tables
- **Clarify** — Structured 4-phase clarity audit (orient → diagnose → repair → verify)
- **Redraft** — Full 5-pass cascade (orient → clarity → integrity → shape → depth → connection)
- **Compose** — Recursive generative workflow (frame → structure → compose → discover → polish)
- **Structure** — 5-phase tradition adaptation (identify source → target → map divergence → adapt → annotate)
- **Bridge** — 4-phase ontology bridging (receive → identify gap → bridge → offer third)

All routes load the tradition meta-lens first, preventing Anglo-American conventions from operating as an invisible default.

## References

| File | Purpose |
|------|---------|
| `references/tradition.md` | Meta-lens loaded before all techniques |
| `references/fit.md` | Form-function alignment |
| `references/calibrate.md` | Audience depth calibration |
| `references/bridge.md` | Knowledge and cross-cultural bridging |
| `references/clarify.md` | Structural and content clarity |
| `references/activate.md` | Voice activation (passive → active) |
| `references/strengthen.md` | Language commitment |
| `references/illustrate.md` | Grounding abstractions |
| `references/signal-confidence.md` | Certainty-evidence calibration |
| `references/bound-scope.md` | Boundary conditions |
| `references/surface-assumptions.md` | Unstated premises |
| `references/arc.md` | Tension and narrative shape |
| `references/arrange.md` | Section ordering |
| `references/rhythm.md` | Sentence-level cadence |
| `references/voice.md` | Authorial presence |
| `references/register.md` | Word-level precision |
| `references/extract-implications.md` | Unsaid consequences |
| `references/dimensionalize.md` | Separating conflated concerns |
| `references/pose-questions.md` | Opening inquiry |
| `references/index.md` | Technique navigation index |
| `references/clarify-patterns.md` | Clarity detection heuristics |
| `references/clarify-examples.md` | Clarity before/after examples |
| `references/frame-guide.md` | Extended composition framing |
| `references/translanguaging-guide.md` | Ontology bridging research basis |
| `references/language-patterns.md` | Per-tradition grammatical patterns |
| `references/tradition-signatures.md` | Tradition rapid identification |
| `references/workflow-clarify.md` | Clarify workflow definition |
| `references/workflow-redraft.md` | Redraft workflow definition |
| `references/workflow-compose.md` | Compose workflow definition |
| `references/workflow-structure.md` | Structure workflow definition |
| `references/workflow-bridge.md` | Bridge workflow definition |

## File Structure

```text
skills/communicate/
├── SKILL.md                           # Router + ad-hoc technique library
├── README.md                          # This file
└── references/
    ├── index.md                       # Technique navigation index
    ├── tradition.md                   # Meta-lens (loaded first always)
    ├── fit.md                         # Purpose
    ├── calibrate.md                   # Purpose
    ├── bridge.md                      # Connection
    ├── clarify.md                     # Clarity
    ├── clarify-patterns.md            # Clarity (supporting)
    ├── clarify-examples.md            # Clarity (supporting)
    ├── activate.md                    # Clarity
    ├── strengthen.md                  # Clarity
    ├── illustrate.md                  # Clarity
    ├── signal-confidence.md           # Integrity
    ├── bound-scope.md                 # Integrity
    ├── surface-assumptions.md         # Integrity
    ├── arc.md                         # Shape
    ├── arrange.md                     # Shape
    ├── rhythm.md                      # Shape
    ├── voice.md                       # Shape
    ├── register.md                    # Shape
    ├── extract-implications.md        # Depth
    ├── dimensionalize.md              # Depth
    ├── pose-questions.md              # Depth
    ├── workflow-clarify.md            # Clarify workflow
    ├── workflow-redraft.md            # Redraft workflow
    ├── workflow-compose.md            # Compose workflow
    ├── workflow-structure.md          # Structure workflow
    ├── workflow-bridge.md             # Bridge workflow
    ├── frame-guide.md                 # Composition-specific
    ├── translanguaging-guide.md       # Bridge-specific
    ├── language-patterns.md           # Bridge-specific
    └── tradition-signatures.md        # Structure-specific
```

## License

MIT
