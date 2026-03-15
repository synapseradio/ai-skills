# Template Selection

Choose the right template based on your data and the question you're answering. These patterns synthesize established visualization practice. Primary sources are cited where available.

## Quick Selection Guide

| Question Type | Data Shape | Engine | Template | Example |
|---------------|-----------|--------|----------|---------|
| "Compare amounts across categories" | Category + Value | VL | **bar-chart** | Sales by product |
| "Show trend over time" | Time + Value | VL | **line-chart** | Revenue by month |
| "Find relationship between variables" | X + Y numeric | VL | **scatter-plot** | Height vs weight |
| "Show value distribution" | Single numeric column | VL | **histogram** | Age distribution |
| "Show parts of a whole" | Categories + Values summing to 100% | VL | **pie-chart** | Market share |

## Decision Tree

```
What's your primary question?
    │
    ├─► "How do values compare across categories?"
    │   └─► Engine: VL → bar-chart.vl.json (comparisons/)
    │
    ├─► "How does something change over time?"
    │   └─► Engine: VL → line-chart.vl.json (temporal/)
    │
    ├─► "What's the relationship between two variables?"
    │   └─► Engine: VL → scatter-plot.vl.json (relationships/)
    │
    ├─► "How are values distributed?"
    │   └─► Engine: VL → histogram.vl.json (distributions/)
    │
    ├─► "What proportion is each part of the whole?"
    │   └─► Engine: VL → pie-chart.vl.json (compositions/)
    │       ⚠️ Use only when: parts sum to meaningful whole,
    │          2-5 categories, precision not critical
    │
    ├─► "How do quantities flow between stages?"
    │   └─► Engine: D3 → sankey.html (networks/)
    │
    └─► Hierarchical / geographic / network?
        └─► Engine: Vega → see extended templates (.vg.json)
```

**Engine selection shortcut:** chart type → engine → template file. For full engine decision logic, see `engine-selection.md`.

## Data Shape Requirements

### bar-chart (VL: `comparisons/bar-chart.vl.json`)

```json
[
  { "category": "Product A", "value": 120 },
  { "category": "Product B", "value": 95 },
  { "category": "Product C", "value": 180 }
]
```

**When to use**: Comparing discrete categories. Vertical bars when categories have natural order; horizontal bars when labels are long.

### line-chart (VL: `temporal/line-chart.vl.json`)

```json
[
  { "date": "2024-01-01", "value": 100 },
  { "date": "2024-02-01", "value": 120 },
  { "date": "2024-03-01", "value": 115 }
]
```

**When to use**: Time series data showing trends. Multiple lines for comparing series. Use area-chart template from `temporal/area-chart.vl.json` when cumulative values matter.

### scatter-plot (VL: `relationships/scatter-plot.vl.json`)

```json
[
  { "x": 25, "y": 150, "category": "Group A" },
  { "x": 30, "y": 175, "category": "Group A" },
  { "x": 35, "y": 160, "category": "Group B" }
]
```

**When to use**: Exploring correlation between two numeric variables. Add `category` for color encoding. For a third numeric variable, use bubble-chart template from `relationships/bubble-chart.vl.json`.

### histogram (VL: `distributions/histogram.vl.json`)

```json
[
  { "value": 23 },
  { "value": 45 },
  { "value": 31 }
]
```

**When to use**: Understanding distribution shape (normal, skewed, bimodal). The template handles binning automatically.

### pie-chart (VL: `compositions/pie-chart.vl.json`)

```json
[
  { "category": "Segment A", "value": 45 },
  { "category": "Segment B", "value": 30 },
  { "category": "Segment C", "value": 25 }
]
```

**When to use**: Parts of a meaningful whole. Limit to 5-7 slices maximum. Consider bar-chart if precision matters or you have many categories.

## Extended Templates

Beyond the 5 most common types, 14 additional templates are available:

| Category | Template | Engine | File | When to Use |
|----------|----------|--------|------|-------------|
| `comparisons/` | grouped-bar | VL | `grouped-bar.vl.json` | Multiple series compared across categories |
| `comparisons/` | stacked-bar | VL | `stacked-bar.vl.json` | Part-to-whole breakdown within categories |
| `compositions/` | sunburst | Vega | `sunburst.vg.json` | Multi-level hierarchical proportions |
| `compositions/` | treemap | Vega | `treemap.vg.json` | Area-based hierarchical data |
| `distributions/` | box-plot | VL | `box-plot.vl.json` | Statistical summary (median, quartiles, outliers) |
| `distributions/` | violin-plot | VL | `violin-plot.vl.json` | Distribution shape with kernel density |
| `geographic/` | choropleth | Vega | `choropleth.vg.json` | Data mapped to geographic regions |
| `hierarchical/` | tree-diagram | Vega | `tree-diagram.vg.json` | Parent-child node layouts |
| `networks/` | force-graph | Vega | `force-graph.vg.json` | Node-edge network visualization |
| `networks/` | sankey | D3 | `sankey.html` | Flow quantities between stages |
| `relationships/` | heatmap | VL | `heatmap.vl.json` | Value intensity across two categorical axes |
| `relationships/` | bubble-chart | VL | `bubble-chart.vl.json` | Three-variable scatter (x, y, size) |
| `temporal/` | area-chart | VL | `area-chart.vl.json` | Cumulative or stacked time series |
| `temporal/` | candlestick | VL | `candlestick.vl.json` | Financial OHLC data |

All VL and Vega templates live at `assets/vega/templates/{category}/{file}`. VL specs use `.vl.json` extension; full Vega specs use `.vg.json`. The sankey D3 template remains at `assets/d3/templates/networks/sankey.html`.

For chart types NOT covered by any template (radar, streamgraph, chord diagram, etc.),
use **template-crafter** agent. Prefer generating Vega-Lite or Vega specs when possible — fall back to D3 only when the chart type has no declarative equivalent.

## Anti-Patterns

| Don't Use | When | Instead Use |
|-----------|------|-------------|
| Pie chart | >7 categories | Bar chart |
| Pie chart | Precise comparison needed | Bar chart |
| Line chart | Categories (not time) | Bar chart |
| 3D anything | Ever | 2D equivalent |
| Dual y-axes | Suggesting correlation | Two aligned charts |

## Sources

- Cleveland, W.S. and McGill, R. (1984). "Graphical Perception." *JASA*, 79(387), 531-554. https://www.jstor.org/stable/2288400
- Vega-Lite documentation — https://vega.github.io/vega-lite/
- Vega documentation — https://vega.github.io/vega/
- D3.js documentation — https://d3js.org/getting-started
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.
