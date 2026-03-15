# Template Selection

Choose the right template based on your data and the question you're answering. These patterns synthesize established visualization practice. Primary sources are cited where available.

## Quick Selection Guide

| Question Type | Data Shape | Template | Example |
|---------------|-----------|----------|---------|
| "Compare amounts across categories" | Category + Value | **bar-chart** | Sales by product |
| "Show trend over time" | Time + Value | **line-chart** | Revenue by month |
| "Find relationship between variables" | X + Y numeric | **scatter-plot** | Height vs weight |
| "Show value distribution" | Single numeric column | **histogram** | Age distribution |
| "Show parts of a whole" | Categories + Values summing to 100% | **pie-chart** | Market share |

## Decision Tree

```
What's your primary question?
    │
    ├─► "How do values compare across categories?"
    │   └─► bar-chart (comparisons/)
    │
    ├─► "How does something change over time?"
    │   └─► line-chart (temporal/)
    │
    ├─► "What's the relationship between two variables?"
    │   └─► scatter-plot (relationships/)
    │
    ├─► "How are values distributed?"
    │   └─► histogram (distributions/)
    │
    └─► "What proportion is each part of the whole?"
        └─► pie-chart (compositions/)
            ⚠️ Use only when: parts sum to meaningful whole,
               2-5 categories, precision not critical
```

## Data Shape Requirements

### bar-chart

```javascript
// Required shape
[
  { category: "Product A", value: 120 },
  { category: "Product B", value: 95 },
  { category: "Product C", value: 180 }
]
```

**When to use**: Comparing discrete categories. Vertical bars when categories have natural order; horizontal bars when labels are long.

### line-chart

```javascript
// Required shape
[
  { date: "2024-01-01", value: 100 },
  { date: "2024-02-01", value: 120 },
  { date: "2024-03-01", value: 115 }
]
```

**When to use**: Time series data showing trends. Multiple lines for comparing series. Use area-chart template from `temporal/area-chart.html` when cumulative values matter.

### scatter-plot

```javascript
// Required shape
[
  { x: 25, y: 150, category: "Group A" },
  { x: 30, y: 175, category: "Group A" },
  { x: 35, y: 160, category: "Group B" }
]
```

**When to use**: Exploring correlation between two numeric variables. Add `category` for color encoding. For a third numeric variable, use bubble-chart template from `relationships/bubble-chart.html`.

### histogram

```javascript
// Required shape
[
  { value: 23 },
  { value: 45 },
  { value: 31 },
  // ... continuous numeric values
]
```

**When to use**: Understanding distribution shape (normal, skewed, bimodal). The template handles binning automatically.

### pie-chart

```javascript
// Required shape
[
  { category: "Segment A", value: 45 },
  { category: "Segment B", value: 30 },
  { category: "Segment C", value: 25 }
]
```

**When to use**: Parts of a meaningful whole. Limit to 5-7 slices maximum. Consider bar-chart if precision matters or you have many categories.

## Extended Templates

Beyond the 5 most common types, 14 additional templates are available at `assets/d3/templates/`:

| Category | Template | When to Use |
|----------|----------|-------------|
| `comparisons/` | grouped-bar | Multiple series compared across categories |
| `comparisons/` | stacked-bar | Part-to-whole breakdown within categories |
| `compositions/` | sunburst | Multi-level hierarchical proportions |
| `compositions/` | treemap | Area-based hierarchical data |
| `distributions/` | box-plot | Statistical summary (median, quartiles, outliers) |
| `distributions/` | violin-plot | Distribution shape with kernel density |
| `geographic/` | choropleth | Data mapped to geographic regions |
| `hierarchical/` | tree-diagram | Parent-child node layouts |
| `networks/` | force-graph | Node-edge network visualization |
| `networks/` | sankey | Flow quantities between stages |
| `relationships/` | heatmap | Value intensity across two categorical axes |
| `relationships/` | bubble-chart | Three-variable scatter (x, y, size) |
| `temporal/` | area-chart | Cumulative or stacked time series |
| `temporal/` | candlestick | Financial OHLC data |

For chart types NOT covered by any template (radar, streamgraph, chord diagram, etc.),
use **template-crafter** agent.

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
- D3.js documentation — https://d3js.org/getting-started
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.
