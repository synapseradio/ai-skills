# Interact Mode

Add dynamic behavior through brushing, filtering, transitions, and responsive adaptation. Verify D3 interaction APIs (d3.brush, d3.zoom, d3.drag) against the current D3 documentation before implementing.

## When to Use

- Adding interactivity to visualizations
- Implementing filtering and selection
- Creating zoom and pan functionality
- Adding hover tooltips
- Implementing brush selection
- Creating linked views
- Making visualizations responsive to user input

## Applicability Check

**In comprehensive mode**: Runs when interactivity would enhance exploration or understanding.

**Signals to check**:

- Is this visualization intended for web/interactive medium (not print/static)?
- Would users benefit from exploring different subsets of data?
- Is there too much data to show at once without filtering?
- Would comparing selected elements add insight?
- Does the audience need to find their own patterns?

**Quick check**: Would static display suffice for this use case? If static is adequate → skip with "Static visualization sufficient." If users need exploration → run this mode.

## Core Principle

Interaction transforms passive viewing into active exploration. Static visualizations present a single perspective; interactive visualizations let viewers discover perspectives relevant to their questions. The goal is not decoration but empowerment—giving users the tools to find insights the author couldn't anticipate.

## The Interaction Vocabulary

D3.js and modern visualization libraries provide a vocabulary of interaction techniques. Each serves different analytical goals:

### Selection and Highlighting

**Hover effects** provide details on demand without cluttering the view:

- Reveal exact values for data points
- Show contextual information (labels, categories, metadata)
- Highlight related elements across views

**Click selection** creates persistent focus:

- Toggle individual element selection
- Build comparison sets
- Trigger drill-down to detail views

**Brushing** selects regions:

- Rectangle brush for 2D selection
- 1D brush for range selection on axes
- Lasso for irregular regions

### Filtering and Subsetting

**Direct manipulation filters** use the visualization itself:

- Brush to select ranges
- Click legend items to show/hide categories
- Slider controls linked to data dimensions

**Parametric filters** use external controls:

- Dropdowns for category selection
- Range sliders for continuous dimensions
- Search boxes for text filtering

### Navigation and Focus

**Zoom** changes the level of detail:

- Geometric zoom (magnification)
- Semantic zoom (different representations at different scales)
- Focus+context (detail in focus area, overview in periphery)

**Pan** moves the viewport:

- Click-and-drag for manual navigation
- Animated transitions to points of interest
- Minimap for orientation in large spaces

### Linked Views

**Brushing and linking** coordinates multiple visualizations:

- Select in one view, highlight in others
- Filter in one view, filter in all
- Hover in one view, tooltip in related views

**Coordinated navigation**:

- Zoom one view, zoom all
- Filter one dimension, update all views showing that dimension
- Time scrubber controls all temporal views

## Instructions

### 1. Identify the Interaction Goals

Before adding interactivity, clarify what users need to do:

**Exploration goals**:

- Find specific data points (search, filter)
- Compare selected subsets (selection, linking)
- See different perspectives (filter, zoom)
- Discover patterns (brush, animate)

**Task analysis**:

- What questions will users bring?
- What comparisons matter?
- What level of detail is needed?
- How much data must be navigable?

Match interaction techniques to goals. Don't add interactivity for its own sake.

### 2. Implement Tooltips

Tooltips are the most common and lowest-commitment interaction. They reveal details without changing the view.

**Vega-Lite** (primary — covers most chart types): Set `"tooltip": true` on marks for default tooltips, or use a tooltip encoding array for custom content:

```json
{
  "mark": {"type": "bar", "tooltip": true},
  "encoding": {
    "tooltip": [
      {"field": "name", "type": "nominal", "title": "Company"},
      {"field": "revenue", "type": "quantitative", "title": "Revenue", "format": "$,.0f"}
    ]
  }
}
```

**Vega**: Build tooltip content via signal expressions:

```json
{"tooltip": {"signal": "{'Name': datum.name, 'Value': format(datum.value, ',.0f')}"}}
```

**D3** (sankey/custom only): See `d3-patterns.md` for custom tooltip implementation with positioning.

**Tooltip best practices** (all engines):

- Position near but not obscuring the element
- Include context (name, category) not just value
- Use consistent formatting across visualizations
- Note: VL/Vega tooltips are hover-only (no keyboard activation)

### 3. Implement Selection and Brushing

**Vega-Lite point selection** — click to highlight:

```json
{
  "params": [{"name": "highlight", "select": {"type": "point", "fields": ["category"]}}],
  "encoding": {
    "opacity": {"condition": {"param": "highlight", "value": 1}, "value": 0.3}
  }
}
```

**Vega-Lite interval selection** — drag to brush a range:

```json
{
  "params": [{"name": "brush", "select": {"type": "interval", "encodings": ["x"]}}],
  "encoding": {
    "color": {
      "condition": {"param": "brush", "field": "category", "type": "nominal"},
      "value": "grey"
    }
  }
}
```

**Vega-Lite legend binding** — click legend entries to filter:

```json
{
  "params": [{"name": "legendFilter", "select": {"type": "point", "fields": ["category"]}, "bind": "legend"}],
  "encoding": {"opacity": {"condition": {"param": "legendFilter", "value": 1}, "value": 0.1}}
}
```

**Vega signals** — for custom event logic beyond VL's selection model:

```json
{
  "signals": [{
    "name": "hovered", "value": null,
    "on": [
      {"events": "symbol:pointerover", "update": "datum"},
      {"events": "symbol:pointerout", "update": "null"}
    ]
  }]
}
```

### 4. Implement Filtering and Linked Views

**Vega-Lite input binding** — sliders, dropdowns, and other controls:

```json
{
  "params": [
    {"name": "minRevenue", "value": 0, "bind": {"input": "range", "min": 0, "max": 100000, "step": 1000, "name": "Min Revenue: "}},
    {"name": "selectedRegion", "bind": {"input": "select", "options": [null, "North", "South", "East"], "name": "Region: "}}
  ],
  "transform": [
    {"filter": "datum.revenue >= minRevenue"},
    {"filter": "selectedRegion == null || datum.region == selectedRegion"}
  ]
}
```

**Vega-Lite brush-linked views** — brush in overview drives detail:

```json
{
  "vconcat": [
    {
      "params": [{"name": "brush", "select": {"type": "interval", "encodings": ["x"]}}],
      "mark": "area", "height": 60,
      "encoding": {"x": {"field": "date", "type": "temporal"}, "y": {"field": "value", "type": "quantitative"}}
    },
    {
      "mark": "area", "height": 300,
      "encoding": {
        "x": {"field": "date", "type": "temporal", "scale": {"domain": {"param": "brush"}}},
        "y": {"field": "value", "type": "quantitative"}
      }
    }
  ]
}
```

### 5. Responsive and Mobile

**Vega-Lite**: Use `"width": "container"` with a parent element that has defined width. The chart resizes automatically.

**Touch targets**: Ensure interactive elements meet 44px minimum. For VL, increase point size: `"mark": {"type": "point", "size": 200}`.

**Mobile considerations** (all engines):

- Tap replaces hover for tooltips on touch devices
- Simplified interactions (fewer simultaneous gestures)
- Landscape vs portrait layout adaptation

### 6. D3 Interaction Patterns (sankey and custom templates)

For D3-based charts requiring imperative interaction control (brushing, zoom, drag, transitions, performance optimization with Canvas), see:

- `d3-patterns.md` for tooltip, hover, and force-directed interaction patterns
- `canvas-patterns.md` for large dataset performance (>1000 elements)
- `network-patterns.md` for force-directed graph interaction patterns

## Common Interaction Patterns

### Details-on-Demand

Show summary, reveal detail on interaction:

```
Overview → Hover for tooltip → Click for detail panel → Drill to full view
```

### Focus + Context

Detailed view of focus area, compressed overview of context:

- Fisheye distortion
- Minimap navigation
- Semantic zoom levels

### Direct Manipulation

Interact with data through the visualization itself:

- Drag to reorder
- Brush to filter
- Click legend to toggle
- Resize panels to allocate space

### Animated Storytelling

Guide users through a narrative with transitions:

- Scrollytelling (scroll triggers transitions)
- Stepper (buttons advance narrative)
- Play/pause for temporal animation

## Temporal States

Visualizations exist across time, not in a single rendered frame. Design for
the 30% of sessions where data isn't present or well-formed.

**Loading state.** Show chart structure before data arrives — skeleton with axis
placeholders and muted grid. Never show an empty axis with no explanation.

**Error state.** Communicate failure clearly and non-technically. The error display
IS a visual claim — "something went wrong" is better than a blank chart that
implies "nothing to see."

**Empty state.** When filters return zero results, explain why and suggest recovery
actions (broaden filters, check date range). A blank chart says "nothing to see" —
often wrong.

**Partial data.** Indicate completeness visually. Incomplete data is not neutral —
the brain fills ambiguity with confabulation, inventing patterns in gaps. Use
dashed lines, reduced opacity, or explicit "data through [date]" annotations.

**Staleness.** When data hasn't refreshed, communicate age. A dashboard showing
yesterday's data without saying so is making a false currency claim.

## Interaction Limitations

Choose the right tool by understanding what each layer cannot do:

| Limitation | Vega-Lite | Vega | D3 |
|------------|-----------|------|----|
| Custom drag behavior | Not supported | Supported via signals | Full control |
| Programmatic animation | Not supported | Limited (timer signals) | Full control (`d3.transition`) |
| Complex event sequences | Single selections only | Full event stream algebra | Full DOM event handling |
| Tooltips | Hover-only (no keyboard activation) | Hover-only (no keyboard activation) | Can bind to focus events |
| Force layout interaction | Not available | Drag via signal + force restart | Full `d3.drag` + `d3.forceSimulation` |

**Choosing the interaction layer**:

- **VL selections** when the pattern is standard (brush, click-to-highlight, legend filter, slider)
- **Vega signals** when you need custom event logic but want declarative rendering
- **D3** when you need full DOM control (sankey template, complex animations, keyboard-activated tooltips)

## Sources

- D3.js documentation — https://d3js.org/getting-started
- D3 API Reference — https://github.com/d3/d3/blob/main/API.md
- Vega-Lite documentation — https://vega.github.io/vega-lite/docs/
- Vega documentation — https://vega.github.io/vega/docs/
- Shneiderman, B. (1996). "The Eyes Have It: A Task by Data Type Taxonomy for Information Visualizations." *IEEE Symposium on Visual Languages*.

## Phase Transition

After adding interactions, consider:

- **Access** to verify keyboard accessibility of all interactions
- **Refine** to ensure interactions don't clutter or confuse
