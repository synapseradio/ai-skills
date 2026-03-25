# Engine Selection

Two data-viz engines: Vega (declarative, default) and D3 (imperative, full control).
Architecture is extensible for future engines (Mermaid, Graphviz).

## Decision Flowchart

```
Level 1: What are you visualizing?
  ├── Data (quantitative/categorical) → Level 2 (below)
  ├── Process/flow/structure          → [Mermaid — future]
  └── Network topology only           → [Graphviz — future]

Level 2: Which data-viz engine?
  ├── Need full DOM control, custom keyboard nav, or sankey? → D3
  └── Everything else → Vega (default)
```

Default to Vega. Use D3 when you need capabilities Vega cannot provide.

## Capability Matrix

| Capability | Vega | D3 |
|---|---|---|
| Standard charts (bar, line, scatter, pie, etc.) | Yes | Yes |
| Hierarchical layouts (treemap, sunburst, tree) | Yes (transforms) | Yes |
| Force simulation | Yes (force transform) | Yes |
| KDE / density estimation | Yes (kde transform) | Yes |
| Geographic projections | Yes (full projection support) | Yes |
| Custom signals / drag | Yes (signal system) | Yes (events) |
| Sankey | No transform exists | Yes (d3-sankey) |
| Full keyboard navigation | No (renders own SVG) | Yes (full DOM control) |
| ARIA on individual marks | No | Yes |
| Custom animations | Limited (signal transitions) | Full control |
| Declarative conciseness | High | Low (imperative) |

**When to use Vega:** Most chart types. Vega handles bar, line, scatter, area, pie, histogram,
box plot, violin, heatmap, bubble, treemap, sunburst, choropleth, force graph, tree diagram,
candlestick, and more through its transform and layout system. It is declarative JSON — less
code, fewer bugs, easier to audit.

**When to use D3:** When you need full DOM control that Vega's SVG renderer cannot provide.
This means: sankey diagrams (no Vega transform exists), full keyboard navigation of data points,
ARIA roles on individual marks, pixel-precise custom layouts, or very large datasets where
Canvas 2D API is needed.

## Template Assignment

Every chart type has both a Vega and a D3 template:

| Category | Chart | Vega | D3 |
|---|---|---|---|
| **Comparisons** | | | |
| | Bar chart | `assets/vega/templates/comparisons/bar-chart.vg.json` | `assets/d3/templates/comparisons/bar-chart.html` |
| | Grouped bar | `assets/vega/templates/comparisons/grouped-bar.vg.json` | `assets/d3/templates/comparisons/grouped-bar.html` |
| | Stacked bar | `assets/vega/templates/comparisons/stacked-bar.vg.json` | `assets/d3/templates/comparisons/stacked-bar.html` |
| **Compositions** | | | |
| | Pie chart | `assets/vega/templates/compositions/pie-chart.vg.json` | `assets/d3/templates/compositions/pie-chart.html` |
| | Sunburst | `assets/vega/templates/compositions/sunburst.vg.json` | `assets/d3/templates/compositions/sunburst.html` |
| | Treemap | `assets/vega/templates/compositions/treemap.vg.json` | `assets/d3/templates/compositions/treemap.html` |
| **Distributions** | | | |
| | Histogram | `assets/vega/templates/distributions/histogram.vg.json` | `assets/d3/templates/distributions/histogram.html` |
| | Box plot | `assets/vega/templates/distributions/box-plot.vg.json` | `assets/d3/templates/distributions/box-plot.html` |
| | Violin plot | `assets/vega/templates/distributions/violin-plot.vg.json` | `assets/d3/templates/distributions/violin-plot.html` |
| **Geographic** | | | |
| | Choropleth | `assets/vega/templates/geographic/choropleth.vg.json` | `assets/d3/templates/geographic/choropleth.html` |
| **Hierarchical** | | | |
| | Tree diagram | `assets/vega/templates/hierarchical/tree-diagram.vg.json` | `assets/d3/templates/hierarchical/tree-diagram.html` |
| **Networks** | | | |
| | Force graph | `assets/vega/templates/networks/force-graph.vg.json` | `assets/d3/templates/networks/force-graph.html` |
| | Sankey | — | `assets/d3/templates/networks/sankey.html` |
| **Relationships** | | | |
| | Scatter plot | `assets/vega/templates/relationships/scatter-plot.vg.json` | `assets/d3/templates/relationships/scatter-plot.html` |
| | Heatmap | `assets/vega/templates/relationships/heatmap.vg.json` | `assets/d3/templates/relationships/heatmap.html` |
| | Bubble chart | `assets/vega/templates/relationships/bubble-chart.vg.json` | `assets/d3/templates/relationships/bubble-chart.html` |
| **Temporal** | | | |
| | Line chart | `assets/vega/templates/temporal/line-chart.vg.json` | `assets/d3/templates/temporal/line-chart.html` |
| | Area chart | `assets/vega/templates/temporal/area-chart.vg.json` | `assets/d3/templates/temporal/area-chart.html` |
| | Candlestick | `assets/vega/templates/temporal/candlestick.vg.json` | `assets/d3/templates/temporal/candlestick.html` |

**Totals:** 18 Vega + 19 D3 = 37 templates. Sankey is D3-only.

## When to Override the Default

- **Accessibility priority:** If the user specifically needs keyboard navigation or screen
  reader support for individual data points, use D3 regardless of chart type.
- **Performance:** Vega handles tens of thousands of points. For hundreds of thousands, use
  D3 with Canvas 2D API. See `canvas-patterns.md`.
- **Pixel-precise layout:** Infographic-style designs where exact placement matters → D3.
- **Custom interactivity:** Complex drag interactions, custom brush shapes → D3 gives more
  control than Vega signals, though Vega signals handle most cases.
