# Visualize

Create browser-runnable data visualizations using Vega (declarative, default) and D3
(imperative, full control). Every output is a standalone HTML file — no build step, no
server. Principles-first workflow: find the claim before touching data.

## Install

```bash
claude install-skill github:nke/ai-skills/skills/visualize
```

Or copy `skills/visualize/` into `~/.claude/skills/visualize/`.

## Usage

### Full visualization workflow

```text
/visualize create a bar chart showing quarterly revenue by region
```

### Targeted entry

```text
/visualize make this chart accessible
/visualize refine this visualization
/visualize what chart type should I use for this time series data?
```

### Visualization management (requires Python 3)

```text
"save this visualization"  → registers in ~/.visualizer-skill/visualizations/
"list my charts"           → shows all stored visualizations
"search for revenue"       → finds matching visualizations
```

## What's Included

- **SKILL.md** — Core principles + 6-phase workflow with signal routing (320 lines)
- **19 Vega templates** — declarative JSON specs across 8 categories
- **19 D3 templates** — standalone HTML with full keyboard nav and ARIA
- **HTML wrapper** — `assets/vega/wrapper.html` renders Vega specs via `vegaEmbed`
- **20 reference docs** — encoding, composition, narrative, accessibility, interaction, refinement
- **Python CLI** (`scripts/visualizer.py`) — visualization storage and management

## Design System

- **Palette**: OpenColors (colorblind-safe combinations)
- **Spacing**: Generous margins (40px body, 32px container, adequate internal padding)
- **Units**: Mandatory on all axes, tooltips, and annotations
- **Accessibility**: WCAG AA contrast, redundant encoding, data table fallback, keyboard nav (D3)

## Templates

| Category | Charts | Vega | D3 |
|----------|--------|------|-----|
| Comparisons | bar, grouped-bar, stacked-bar | Yes | Yes |
| Compositions | pie, sunburst, treemap | Yes | Yes |
| Distributions | histogram, box-plot, violin-plot | Yes | Yes |
| Geographic | choropleth | Yes | Yes |
| Hierarchical | tree-diagram | Yes | Yes |
| Networks | force-graph, sankey | Yes* | Yes |
| Relationships | scatter-plot, heatmap, bubble-chart | Yes | Yes |
| Temporal | line-chart, area-chart, candlestick | Yes | Yes |

*Sankey is D3-only (no Vega transform exists).

## References

| File | Purpose |
|------|---------|
| `references/phase-context.md` | Argument, viewer, cognitive mode, editorial integrity |
| `references/phase-research.md` | Data assessment, encoding plan, engine + template selection |
| `references/phase-implement.md` | Build: encode, compose, narrate, interact, access-audit |
| `references/phase-refine.md` | Mandatory verification: structural + visual, second draft |
| `references/phase-present.md` | Output, user review, persist |
| `references/mode-encode.md` | Channel effectiveness, cognitive mode, encoding process |
| `references/mode-compose.md` | Gestalt, spacing, layout, aspect ratio |
| `references/mode-narrate.md` | Titles, annotations, story vs. exploration |
| `references/mode-access.md` | Color access, ARIA, keyboard nav (engine-honest) |
| `references/mode-interact.md` | Tooltips, brushing, filtering, temporal states |
| `references/mode-refine.md` | Editorial integrity, structural + perceptual audit |
| `references/engine-selection.md` | Vega vs D3 decision framework (N-engine extensible) |
| `references/template-selection.md` | Question → template decision tree |
| `references/vega-patterns.md` | Vega v6 spec patterns |
| `references/d3-patterns.md` | D3 implementation patterns |
| `references/base-vega-wrapper.md` | Vega HTML wrapper documentation |
| `references/base-template.md` | D3 HTML skeleton documentation |
| `references/data-preparation.md` | Data transforms and preparation |
| `references/network-patterns.md` | Network visualization patterns |
| `references/canvas-patterns.md` | Large dataset (Canvas) patterns |

## Prerequisites

- **Required**: None
- **Optional**: Python 3.6+ (for visualization management CLI)
