# visualize

Create browser-runnable data visualizations using Vega (declarative, default) or D3 (imperative, full control). Every output is a standalone HTML file — no build step, no server. The workflow is principles-first: find the claim before touching data.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/visualize/` into `~/.claude/skills/visualize/`.

## Usage

Full visualization workflow:

```
/visualize create a bar chart showing quarterly revenue by region
```

Targeted entry — jump into a specific phase:

```
/visualize make this chart accessible
/visualize refine this visualization
/visualize what chart type should I use for this time series data?
```

Visualization management (requires Python 3):

```
"save this visualization"    → registers in ~/.visualizer-skill/visualizations/
"list my charts"             → shows all stored visualizations
"search for revenue"         → finds matching visualizations
```

## Why use this instead of prompting?

A plain prompt will produce a chart, but it skips the work that makes a chart good — identifying what claim the visualization supports, choosing encodings that match the data's structure, adding units and context, checking accessibility. This skill enforces a six-phase workflow (context, research, implement, refine, present) so the output communicates clearly, not just renders correctly.

## What's included

- **19 Vega templates** — declarative JSON specs across 8 chart categories
- **19 D3 templates** — standalone HTML with keyboard navigation and ARIA support
- **HTML wrapper** — renders Vega specs via `vegaEmbed`
- **20 reference docs** — encoding, composition, narrative, accessibility, interaction, refinement
- **Python CLI** (`scripts/visualizer.py`) — visualization storage and management

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

## Design system

- **Palette**: OpenColors (colorblind-safe combinations)
- **Spacing**: Generous margins (40px body, 32px container, adequate internal padding)
- **Units**: Mandatory on all axes, tooltips, and annotations
- **Accessibility**: WCAG AA contrast, redundant encoding, data table fallback, keyboard navigation (D3)

## Prerequisites

- **Required**: None
- **Optional**: Python 3.6+ (for visualization management CLI)

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`visualize.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/visualize.skill)

## License

[EUPL-1.2](/LICENSE)
