# D3 Drawing Patterns

> **Scope:** This reference covers the D3 technique that goes inside a fragment's `chart-js` section — scales, axes, marks, force layouts, and the pitfalls particular to D3. For the fragment contract itself (the sections, the injected `root`/`uid`/`VizHelpers`, the mount, the helpers), read [base-template.md](base-template.md) first. For Vega spec patterns, see [vega-patterns.md](vega-patterns.md).

These patterns assume the fragment model. The assembler supplies the D3 import and opens your code with `root`, `uid`, and `VizHelpers` already in scope, and your code draws into the `<svg>` the mount already provides. You never write a `<!DOCTYPE html>`, never select by a document-wide id, and never declare `root` or `uid` yourself. Verify D3 API usage, CDN import URLs, and SVG accessibility attributes against current documentation before deploying.

## The Drawing Skeleton

Inside `chart-js`, the shape of a typical chart is the D3 margin convention applied to the mount's SVG. Select the SVG through `root`, append an inner group offset by the margins, and draw into that group:

```javascript
// Read theme color from the single source.
const t = VizHelpers.tokens;

// --- DIMENSIONS ---
const margin = { top: 8, right: 24, bottom: 64, left: 72 };
const width = 600;
const height = 400;
const innerWidth = width - margin.left - margin.right;
const innerHeight = height - margin.top - margin.bottom;

// --- SCALES ---
const x = d3.scaleBand().domain(data.map((d) => d.category)).range([0, innerWidth]).padding(0.25);
const y = d3.scaleLinear().domain([0, d3.max(data, (d) => d.value)]).nice().range([innerHeight, 0]);

// --- SVG ---  (select the mount's svg through root; never d3.select("#chart"))
const svg = d3.select(root.querySelector("svg"))
  .attr("viewBox", `0 0 ${width} ${height}`)
  .attr("width", "100%");
const g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);

// --- AXES ---
g.append("g").attr("class", "axis").attr("transform", `translate(0,${innerHeight})`).call(d3.axisBottom(x));
g.append("g").attr("class", "axis").call(d3.axisLeft(y));

// --- MARKS ---  (bind with .join(), color from tokens, accessibility per mark)
g.selectAll(".bar").data(data).join("rect")
  .attr("class", "bar")
  .attr("x", (d) => x(d.category))
  .attr("y", (d) => y(d.value))
  .attr("width", x.bandwidth())
  .attr("height", (d) => innerHeight - y(d.value))
  .attr("fill", t["oc-blue-7"])
  .attr("tabindex", 0)
  .attr("role", "listitem")
  .attr("aria-label", (d) => `${d.category}: ${d.value}`);
```

Axis label and gridline color belong in the `chart-css` section as CSS reading the same tokens, for example `fill: var(--oc-gray-6)` and `stroke: var(--oc-gray-1)`, so the styling stays with the chart and out of the drawing code.

## ESM Import Patterns

The assembler injects the core D3 import for you:

```javascript
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";
```

When a chart needs a D3 plugin the core import does not carry, add the import at the top of `chart-js`:

```javascript
// D3 Sankey layout
import { sankey, sankeyLinkHorizontal } from "https://cdn.jsdelivr.net/npm/d3-sankey@0.12/+esm";

// Topojson for maps
import * as topojson from "https://cdn.jsdelivr.net/npm/topojson-client@3/+esm";

// D3 Annotation
import { annotation, annotationCallout } from "https://cdn.jsdelivr.net/npm/d3-svg-annotation@2/+esm";
```

## Responsive SVG Pattern

Size the SVG with a `viewBox` and a percentage width rather than fixed pixel dimensions, so the chart scales to its container — a slide, a README, or a composed dashboard panel alike:

```javascript
const svg = d3.select(root.querySelector("svg"))
  .attr("viewBox", `0 0 ${totalWidth} ${totalHeight}`)
  .attr("preserveAspectRatio", "xMidYMid meet")
  .attr("width", "100%");
```

A `viewBox` defines the coordinate system once. The SVG then scales to the container width, the aspect ratio holds, the internal coordinates stay consistent, and no JavaScript resize handler is needed.

## Data Embedding Strategies

A fragment carries its own sample data inline in `chart-js`. Pick the form that fits the shape.

For small datasets, a plain array of objects:

```javascript
const data = [
  { date: "2024-01-01", value: 100 },
  { date: "2024-01-02", value: 120 },
];
```

For tabular data, a CSV string parsed with a row accessor that coerces types:

```javascript
const data = d3.csvParse(`date,value
2024-01-01,100
2024-01-02,120`, (d) => ({ date: new Date(d.date), value: +d.value }));
```

For nested structures, a JSON string parsed with `JSON.parse`. When a chart genuinely needs an external file, for example a TopoJSON basemap, fetch it inside the chart code — and remember the assembler wraps `chart-js` in an async function, so `await` works directly:

```javascript
const us = await d3.json("https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json");
```

## Common D3 Chart Patterns

> Standard static chart types (bar, line, scatter, area, pie, histogram) exist as both D3 and Vega fragments — see the catalogue in [engine-selection.md](engine-selection.md). Choose D3 when the chart needs custom interactivity, per-mark keyboard navigation, or a structural layout. The patterns below cover the D3-only structural work.

### Force-Directed Graph

Force-directed networks need particular care for visibility and interaction. See [network-patterns.md](network-patterns.md) for comprehensive coverage; the structural essentials follow.

```javascript
const simulation = d3.forceSimulation(nodes)
  .force("link", d3.forceLink(links).id((d) => d.id).distance(80))
  .force("charge", d3.forceManyBody().strength(-200))
  .force("center", d3.forceCenter(width / 2, height / 2))
  .force("collision", d3.forceCollide().radius(20));
```

Append the layers in order, links before nodes before labels, so nodes draw over their edges:

```javascript
const linkLayer = g.append("g").attr("class", "links");
const nodeLayer = g.append("g").attr("class", "nodes");
const labelLayer = g.append("g").attr("class", "labels");
```

Give edges enough weight to be seen — read the colors from tokens rather than hard-coding hex, and keep stroke opacity perceptible:

```javascript
const allLinks = linkLayer.selectAll("line").data(links).join("line")
  .attr("stroke", t["oc-gray-6"])             // a faint gray fails contrast
  .attr("stroke-width", (d) => Math.max(1.5, weightScale(d.weight)))
  .attr("stroke-opacity", 0.6);               // 0.2 is imperceptible
```

Update positions on every tick, and route interactive highlighting through the shared helpers so a keyboard reader reaches the same detail as a mouse reader:

```javascript
simulation.on("tick", () => {
  allLinks
    .attr("x1", (d) => d.source.x).attr("y1", (d) => d.source.y)
    .attr("x2", (d) => d.target.x).attr("y2", (d) => d.target.y);
  allNodes.attr("transform", (d) => `translate(${d.x},${d.y})`);
});
```

## Accessibility

The mount already carries the chart-level `<title>` and `<desc>`, keyed to `{{uid}}` (see [base-template.md](base-template.md)). Your drawing code is responsible for the per-mark layer: a `role="listitem"`, a `tabindex`, and an `aria-label` on every data element, under the `role="list"` the mount sets on the SVG. Wire keyboard reach and tooltips through `VizHelpers.navigateMarks(root, prevKey, nextKey)`, `VizHelpers.showTooltip(root, …)`, and `VizHelpers.hideTooltip(root)`, and build the data-table fallback with `VizHelpers.renderDataTable(root, rows, headers)`. The render checker flags a chart whose marks respond to the pointer but offer no key handler.

## Color

Read every color from the OpenColors tokens the theme supplies, never from a D3 built-in scheme or a hard-coded hex:

```javascript
const t = VizHelpers.tokens;

// Categorical: pick a set of token hues.
const categorical = [t["oc-blue-7"], t["oc-orange-8"], t["oc-teal-7"], t["oc-red-7"], t["oc-grape-7"]];
const color = d3.scaleOrdinal().domain(categories).range(categorical);

// Sequential: interpolate between two token endpoints of one hue family.
const seq = d3.scaleSequential(d3.interpolateRgb(t["oc-blue-1"], t["oc-blue-9"])).domain([0, maxValue]);

// Diverging: interpolate through a neutral midpoint between two hue families.
const div = d3.scaleSequential((v) =>
  v < 0.5 ? d3.interpolateRgb(t["oc-red-7"], t["oc-gray-2"])(v * 2)
          : d3.interpolateRgb(t["oc-gray-2"], t["oc-blue-7"])((v - 0.5) * 2)
).domain([minValue, maxValue]);
```

Keeping color in tokens means a palette edit in `theme.css` reaches the chart on the next assembly. It also keeps the whole skill on one colorblind-considered palette rather than mixing D3's defaults in.

## Common Pitfalls

### Pitfall: redeclaring `root` or `uid`

**Problem**: The assembler already declares `const root` and `const uid` at the top of `chart-js`. A second `const root` for a hierarchy layout is a syntax error that runs fine through static checks and fails only when the page loads.

**Solution**: Name a hierarchy root something else, `hierarchyRoot` for instance, and leave `root`/`uid` to the assembler.

### Pitfall: selecting by document id

**Problem**: `d3.select("#chart")` binds to the first matching element in the whole page. The same fragment may appear more than once in a composed document, so every copy would draw into the first one.

**Solution**: Select through `root` — `d3.select(root.querySelector("svg"))`.

### Pitfall: data types from CSV

**Problem**: CSV values are strings, not numbers.

**Solution**: Coerce in the row accessor: `d3.csvParse(csv, (d) => ({ date: new Date(d.date), value: +d.value }))`.

### Pitfall: axes disappear

**Problem**: An axis renders at (0,0), outside the visible area.

**Solution**: Transform the axis group — ``g.append("g").attr("transform", `translate(0,${innerHeight})`).call(d3.axisBottom(x))``.

### Pitfall: data binding doesn't update

**Problem**: `.append()` inside a selection skips the update and exit selections.

**Solution**: Bind with `.join()` — `g.selectAll("rect").data(data).join("rect")`.

## Testing Locally

To open an assembled example or your output file, serve it over HTTP so external data loads are not blocked by `file://` CORS rules:

```bash
python -m http.server 8000   # or: npx serve
# then open http://localhost:8000/your-file.html
```

## Sources

- D3 documentation — <https://d3js.org/getting-started>
- D3 API Reference — <https://github.com/d3/d3/blob/main/API.md>
- SVG Accessibility API Mappings — <https://www.w3.org/TR/svg-aam-1.0/>
- WAI-ARIA 1.2 specification — <https://www.w3.org/TR/wai-aria-1.2/>
