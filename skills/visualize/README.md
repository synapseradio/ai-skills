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

## Prerequisites

- **Required**: None (skill works for one-off visualizations without any dependencies)
- **Optional**: Python 3.6+ (for visualization management CLI)
