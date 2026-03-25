# Template Selection

Choose the right template based on your data and the question you're answering. Every chart
type has both a Vega and a D3 variant. Default to Vega unless you need D3 capabilities
(see `engine-selection.md`).

## Quick Selection

| Question | Template | Example |
|----------|----------|---------|
| "Compare amounts across categories" | **bar-chart** | Sales by product |
| "Show trend over time" | **line-chart** | Revenue by month |
| "Find relationship between variables" | **scatter-plot** | Height vs weight |
| "Show value distribution" | **histogram** | Age distribution |
| "Show parts of a whole" (≤5 slices) | **pie-chart** | Market share |
| "Show flow between stages" | **sankey** (D3 only) | Budget allocation |

## Decision Tree

```
What's your primary question?
  ├── "How do values compare?"
  │   ├── One series → bar-chart
  │   ├── One series, precision matters → dot-plot (lollipop)
  │   ├── Before/after or min/max range → dumbbell-chart
  │   ├── Multiple series, side-by-side → grouped-bar
  │   └── Multiple series, stacked → stacked-bar
  │
  ├── "How does something change over time?"
  │   ├── Trend → line-chart
  │   ├── Cumulative → area-chart
  │   ├── Before/after comparison → slope-chart
  │   ├── Compact inline trends → sparkline
  │   └── Financial OHLC → candlestick
  │
  ├── "What's the relationship between variables?"
  │   ├── Two variables → scatter-plot
  │   ├── Three variables (x, y, size) → bubble-chart
  │   ├── Two categorical axes + intensity → heatmap
  │   ├── 4+ dimensions, precision matters → parallel-coordinates
  │   └── 4+ dimensions, radial layout → radar-chart (⚠️ perceptually weak)
  │
  ├── "How are values distributed?"
  │   ├── One variable → histogram
  │   ├── Compare distributions → box-plot
  │   └── Distribution shape → violin-plot
  │
  ├── "What proportion is each part?"
  │   ├── Flat, ≤5 categories → pie-chart
  │   ├── Flat, precise percentages → waffle-chart
  │   ├── Hierarchical proportions → sunburst
  │   └── Area-based hierarchy → treemap
  │
  ├── "How do quantities flow?" → sankey (D3 only)
  │
  ├── "What's the geographic pattern?" → choropleth
  │
  ├── "What's the hierarchy?" → tree-diagram
  │
  └── "How are things connected?" → force-graph
```

If no template fits, use the Custom Template Workflow in SKILL.md.

## Data Shape Examples

### bar-chart

```json
[{"category": "Product A", "value": 120, "unit": "sales ($K)"}]
```

### line-chart

```json
[{"date": "2024-01-01", "value": 100, "unit": "revenue ($M)"}]
```

### scatter-plot

```json
[{"x": 25, "y": 150, "category": "Group A", "x_unit": "age (years)", "y_unit": "weight (kg)"}]
```

### histogram

```json
[{"value": 23, "unit": "response time (ms)"}]
```

## Template Directory

All templates at `assets/vega/templates/` (Vega) and `assets/d3/templates/` (D3):

| Category | Chart | Vega (.vg.json) | D3 (.html) |
|----------|-------|-----------------|------------|
| comparisons | bar-chart | Yes | Yes |
| comparisons | grouped-bar | Yes | Yes |
| comparisons | stacked-bar | Yes | Yes |
| compositions | pie-chart | Yes | Yes |
| compositions | sunburst | Yes | Yes |
| compositions | treemap | Yes | Yes |
| distributions | histogram | Yes | Yes |
| distributions | box-plot | Yes | Yes |
| distributions | violin-plot | Yes | Yes |
| geographic | choropleth | Yes | Yes |
| hierarchical | tree-diagram | Yes | Yes |
| networks | force-graph | Yes | Yes |
| networks | sankey | — | Yes |
| relationships | scatter-plot | Yes | Yes |
| relationships | heatmap | Yes | Yes |
| relationships | bubble-chart | Yes | Yes |
| temporal | line-chart | Yes | Yes |
| temporal | area-chart | Yes | Yes |
| temporal | candlestick | Yes | Yes |
| comparisons | dot-plot (lollipop) | Yes | Yes |
| comparisons | dumbbell-chart | Yes | Yes |
| compositions | waffle-chart | Yes | Yes |
| relationships | parallel-coordinates | Yes | Yes |
| relationships | radar-chart | Yes | Yes |
| temporal | slope-chart | Yes | Yes |
| temporal | sparkline | Yes | Yes |

## Tiebreakers (in priority order)

1. **Prefer simpler** — bar chart over bubble chart when both work
2. **Prefer familiar** — viewers read known chart types faster
3. **Prefer the argument** — choose what best serves the specific comparison
4. **Consider the medium** — interactive web handles more complexity than a static slide
