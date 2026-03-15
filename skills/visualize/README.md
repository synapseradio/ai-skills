# Visualize

Data visualization engineering skill. Transform data into browser-runnable D3.js visualizations through principled encoding, composition, narration, accessibility, interaction, and refinement — grounded in perceptual science (Cleveland-McGill, Gestalt, Segel-Heer).

## Install

```bash
claude install-skill github:nke/ai-skills/skills/visualize
```

Or copy the `skills/visualize/` directory into `~/.claude/skills/visualize/`.

## Usage

### Full visualization workflow

```text
/visualize create a bar chart showing quarterly revenue by region
```

### Targeted mode entry

```text
/visualize make this chart accessible
/visualize refine this visualization
/visualize what chart type should I use for this time series data?
```

### Visualization management (requires Python 3)

```text
"save this visualization" → registers in ~/.visualizer-skill/visualizations/
"list my charts" → shows all stored visualizations
"search for revenue" → finds matching visualizations
```

## What's Included

- **SKILL.md** — 6-phase visualization workflow with signal detection routing
- **19 D3.js templates** — browser-runnable HTML across 8 categories (comparisons, compositions, distributions, geographic, hierarchical, networks, relationships, temporal)
- **29 reference docs** — perceptual science, implementation patterns, accessibility, and workflow guidance
- **Python CLI** (`scripts/visualizer.py`) — visualization storage and management, stdlib only

## References

### Phase workflow

| File | Purpose |
|------|---------|
| `references/phase-context.md` | Argument, viewer, cognitive mode, constraints |
| `references/phase-research.md` | Data assessment, encoding plan, template selection |
| `references/phase-implement.md` | Build orchestration across encode, compose, narrate, interact, access |
| `references/phase-refine.md` | Structural, perceptual, and clarity audits |
| `references/phase-present.md` | Output, user review, persist, complete |

### Mode methodology

| File | Purpose |
|------|---------|
| `references/mode-encode.md` | Cleveland-McGill rankings, channel selection |
| `references/mode-compose.md` | Gestalt principles, visual hierarchy |
| `references/mode-narrate.md` | Segel-Heer framework, annotation patterns |
| `references/mode-access.md` | WCAG compliance, ARIA, keyboard navigation |
| `references/mode-interact.md` | Brushing, linking, transitions |
| `references/mode-refine.md` | Iteration workflow, common pitfalls |

### Theory

| File | Purpose |
|------|---------|
| `references/cleveland-mcgill.md` | Perceptual accuracy rankings |
| `references/gestalt.md` | Gestalt grouping principles |
| `references/segel-heer.md` | Narrative visualization framework |
| `references/hierarchy.md` | Visual hierarchy and attention flow |

### Implementation

| File | Purpose |
|------|---------|
| `references/d3-patterns.md` | Browser-runnable templates, ESM imports |
| `references/chart-patterns.md` | D3 patterns by chart type |
| `references/base-template.md` | HTML skeleton with frontmatter |
| `references/template-selection.md` | Template decision tree |

## Prerequisites

- **Required**: None (skill works for one-off visualizations without any dependencies)
- **Optional**: Python 3.6+ (for visualization management CLI)
