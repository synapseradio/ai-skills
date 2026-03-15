# Engine Selection

Decision criteria for choosing Vega-Lite, full Vega, or D3 when building a visualization. Default to Vega-Lite for conciseness; escalate to full Vega or D3 only when the chart requires capabilities Vega-Lite cannot express.

## Decision Flowchart

```
Is it a sankey diagram?
  YES -> Use D3 (sankey.html -- sole D3 template, no Vega transform exists)
Can Vega-Lite express this chart natively?
  YES -> Use Vega-Lite (.vl.json)
  NO  -> Does it need force simulation, hierarchical layout, KDE, geographic projection, or custom signals?
    YES -> Use full Vega (.vg.json)
    NO  -> Use Vega-Lite with layered composition
```

Apply this flowchart top-down. The first matching branch wins.

## Engine Capability Matrix

| Capability | Vega-Lite | Full Vega | D3 |
|---|---|---|---|
| Standard charts (bar, line, scatter, etc.) | Yes | Yes (verbose) | Yes (imperative) |
| Hierarchical layouts (treemap, sunburst) | No | Yes | Yes |
| Force simulation | No | Yes | Yes |
| KDE / density estimation | No | Yes | Yes |
| Geographic projections | Limited | Full | Full |
| Custom signals / drag | No | Yes | Yes |
| Declarative conciseness | Highest | Medium | Lowest |
| Custom template crafter | Via layered composition | Via transforms | Full control |

**Vega-Lite** compiles down to full Vega at render time. Any chart that Vega-Lite can express will produce the same output as writing the equivalent Vega spec by hand, with far less JSON.

**Full Vega** adds explicit signal graphs, custom transforms (force, treemap, partition, voronoi, KDE), and low-level control over the scene graph. Use it when Vega-Lite's grammar has no encoding for the layout you need.

**D3** gives imperative control over the DOM. The only template that requires D3 is sankey, because neither Vega nor Vega-Lite has a sankey transform. D3 templates also serve the `template-crafter` mode, where users need fully custom, hand-coded visualizations.

## Template Assignment

All 19 templates, grouped by category. VL specs (`.vl.json`) and full Vega specs (`.vg.json`) live in `assets/vega/templates/`. Sankey lives in `assets/d3/templates/`.

| Template | Engine | Spec File |
|---|---|---|
| **Comparisons** | | |
| Bar chart | Vega-Lite | `vega-lite/templates/comparisons/bar-chart.vl.json` |
| Grouped bar | Vega-Lite | `vega-lite/templates/comparisons/grouped-bar.vl.json` |
| Stacked bar | Vega-Lite | `vega-lite/templates/comparisons/stacked-bar.vl.json` |
| **Compositions** | | |
| Pie chart | Vega-Lite | `vega-lite/templates/compositions/pie-chart.vl.json` |
| Sunburst | Full Vega | `vega-lite/templates/compositions/sunburst.vg.json` |
| Treemap | Full Vega | `vega-lite/templates/compositions/treemap.vg.json` |
| **Distributions** | | |
| Box plot | Vega-Lite | `vega-lite/templates/distributions/box-plot.vl.json` |
| Histogram | Vega-Lite | `vega-lite/templates/distributions/histogram.vl.json` |
| Violin plot | Full Vega | `vega-lite/templates/distributions/violin-plot.vg.json` |
| **Geographic** | | |
| Choropleth | Full Vega | `vega-lite/templates/geographic/choropleth.vg.json` |
| **Hierarchical** | | |
| Tree diagram | Full Vega | `vega-lite/templates/hierarchical/tree-diagram.vg.json` |
| **Networks** | | |
| Force graph | Full Vega | `vega-lite/templates/networks/force-graph.vg.json` |
| Sankey | D3 | `d3/templates/networks/sankey.html` |
| **Relationships** | | |
| Bubble chart | Vega-Lite | `vega-lite/templates/relationships/bubble-chart.vl.json` |
| Heatmap | Vega-Lite | `vega-lite/templates/relationships/heatmap.vl.json` |
| Scatter plot | Vega-Lite | `vega-lite/templates/relationships/scatter-plot.vl.json` |
| **Temporal** | | |
| Area chart | Vega-Lite | `vega-lite/templates/temporal/area-chart.vl.json` |
| Candlestick | Vega-Lite | `vega-lite/templates/temporal/candlestick.vl.json` |
| Line chart | Vega-Lite | `vega-lite/templates/temporal/line-chart.vl.json` |

**Totals**: 12 Vega-Lite, 6 Full Vega, 1 D3.

## When to Override the Default

The flowchart covers standard cases. Override when:

- **Custom interactivity beyond selection**: If the chart needs drag-to-reorder, custom brush shapes, or interactive parameter widgets, escalate from Vega-Lite to full Vega for its signal system.
- **Performance with large datasets**: Vega-Lite's `canvas` renderer handles tens of thousands of points. For hundreds of thousands, consider full Vega with `canvas` renderer and data streaming, or D3 with Canvas 2D API directly.
- **Pixel-precise layout**: When the exact pixel placement of every element matters (infographic-style), D3 gives full control. Vega and Vega-Lite lay out marks according to their grammar, which may not match a rigid design spec.
- **Combining chart types not in Vega-Lite's grammar**: Vega-Lite supports `layer`, `concat`, `facet`, and `repeat`. If the combination you need does not fit these operators (for example, a chart where one layer is a force layout and another is a bar chart), use full Vega or split into separate embeds.
- **Template-crafter mode**: When the user requests a fully custom D3 visualization, use the D3 base template from `base-template.md` regardless of whether a Vega-Lite equivalent exists.

## Sources

- Vega-Lite documentation — https://vega.github.io/vega-lite/
- Vega documentation — https://vega.github.io/vega/
- D3.js documentation — https://d3js.org/getting-started
- Vega-Lite compilation to Vega — https://vega.github.io/vega-lite/usage/compile.html
