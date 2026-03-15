# Interact Mode

Add dynamic behavior through brushing, filtering, transitions, and responsive adaptation.

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

### 2. Implement Hover and Tooltips

Tooltips are the most common and lowest-commitment interaction. They reveal details without changing the view.

**Basic D3 tooltip pattern**:

```javascript
const tooltip = d3.select("body")
  .append("div")
  .attr("class", "tooltip")
  .style("opacity", 0);

selection
  .on("mouseover", function(event, d) {
    tooltip
      .style("opacity", 1)
      .html(`<strong>${d.name}</strong><br/>Value: ${d.value}`)
      .style("left", (event.pageX + 10) + "px")
      .style("top", (event.pageY - 10) + "px");
  })
  .on("mouseout", function() {
    tooltip.style("opacity", 0);
  });
```

**Tooltip best practices**:

- Position near but not obscuring the element
- Include context (name, category) not just value
- Use consistent formatting across visualizations
- Consider mobile (no hover) with tap-to-show alternatives

**Visual feedback on hover**:

```javascript
selection
  .on("mouseover", function() {
    d3.select(this)
      .transition()
      .duration(100)
      .attr("opacity", 1)
      .attr("stroke-width", 2);
  })
  .on("mouseout", function() {
    d3.select(this)
      .transition()
      .duration(100)
      .attr("opacity", 0.7)
      .attr("stroke-width", 1);
  });
```

### 3. Implement Brushing

Brushing lets users select regions of data space.

**1D brush for axis ranges**:

```javascript
const brush = d3.brushX()
  .extent([[0, 0], [width, height]])
  .on("brush end", brushed);

svg.append("g")
  .attr("class", "brush")
  .call(brush);

function brushed(event) {
  if (!event.selection) return;
  const [x0, x1] = event.selection.map(xScale.invert);

  // Filter or highlight data in range
  selection
    .classed("selected", d => d.value >= x0 && d.value <= x1);
}
```

**2D brush for scatterplots**:

```javascript
const brush = d3.brush()
  .extent([[0, 0], [width, height]])
  .on("brush end", brushed);

function brushed(event) {
  if (!event.selection) return;
  const [[x0, y0], [x1, y1]] = event.selection;

  selection.classed("selected", d =>
    xScale(d.x) >= x0 && xScale(d.x) <= x1 &&
    yScale(d.y) >= y0 && yScale(d.y) <= y1
  );
}
```

**Brush UX considerations**:

- Clear selection on click outside brush
- Show selection count or summary
- Enable keyboard modifiers (shift to add, alt to subtract)
- Provide clear brush handle affordances

### 4. Implement Linked Views

When multiple visualizations show related data, link their interactions.

**Shared state pattern**:

```javascript
// Shared state object
const state = {
  selectedIds: new Set(),
  highlightedId: null,
  filters: {}
};

// Update function propagates to all views
function updateViews() {
  views.forEach(view => view.update(state));
}

// Each view responds to state
function updateScatterplot(state) {
  points
    .classed("selected", d => state.selectedIds.has(d.id))
    .classed("highlighted", d => d.id === state.highlightedId)
    .classed("filtered-out", d => !passesFilters(d, state.filters));
}
```

**Cross-view highlighting**:

```javascript
// In scatterplot
points.on("mouseover", function(event, d) {
  state.highlightedId = d.id;
  updateViews();
});

// In bar chart
bars.classed("highlighted", d => d.id === state.highlightedId);
```

**Brush-link pattern**:

```javascript
// Brush in overview updates detail view
overviewBrush.on("brush end", function(event) {
  const selection = event.selection;
  if (!selection) {
    detailView.showAll();
  } else {
    const [x0, x1] = selection.map(overviewXScale.invert);
    detailView.filterRange(x0, x1);
  }
});
```

### 5. Implement Zoom and Pan

Zoom enables navigation across scales of detail.

**Geometric zoom**:

```javascript
const zoom = d3.zoom()
  .scaleExtent([1, 8])
  .on("zoom", zoomed);

svg.call(zoom);

function zoomed(event) {
  const transform = event.transform;
  chartGroup.attr("transform", transform);
}
```

**Semantic zoom** (change representation at different scales):

```javascript
function zoomed(event) {
  const k = event.transform.k;

  // Update scales
  const newXScale = event.transform.rescaleX(xScale);
  const newYScale = event.transform.rescaleY(yScale);

  // Update axes
  xAxis.call(d3.axisBottom(newXScale));
  yAxis.call(d3.axisLeft(newYScale));

  // At high zoom, show labels; at low zoom, hide them
  labels.style("opacity", k > 2 ? 1 : 0);

  // Update element positions
  points
    .attr("cx", d => newXScale(d.x))
    .attr("cy", d => newYScale(d.y));
}
```

**Zoom controls**:

```javascript
// Programmatic zoom
function zoomIn() {
  svg.transition().call(zoom.scaleBy, 1.5);
}

function zoomOut() {
  svg.transition().call(zoom.scaleBy, 0.67);
}

function resetZoom() {
  svg.transition().call(zoom.transform, d3.zoomIdentity);
}
```

### 6. Implement Animated Transitions

Transitions help users track changes and understand transformations.

**Basic transition pattern**:

```javascript
selection
  .transition()
  .duration(500)
  .ease(d3.easeCubicInOut)
  .attr("cx", d => xScale(d.x))
  .attr("cy", d => yScale(d.y));
```

**Staged transitions** for complex changes:

```javascript
// Exit old elements
selection.exit()
  .transition()
  .duration(300)
  .attr("opacity", 0)
  .remove();

// Update existing elements
selection
  .transition()
  .duration(500)
  .delay(300)
  .attr("cx", d => xScale(d.x));

// Enter new elements
selection.enter()
  .append("circle")
  .attr("opacity", 0)
  .attr("cx", d => xScale(d.x))
  .transition()
  .delay(800)
  .duration(300)
  .attr("opacity", 1);
```

**When to animate**:

- Data updates (show what changed)
- Filter/selection changes (show what remained)
- View transitions (maintain context)
- Attention direction (guide focus)

**When not to animate**:

- Initial render (users expect instant display)
- Rapid successive changes (animations queue up)
- Fine motor interactions (tooltips, precise selections)

### 7. Handle Responsive and Mobile

Interactive visualizations must work across devices.

**Responsive dimensions**:

```javascript
function resize() {
  const container = d3.select("#chart-container").node();
  const { width, height } = container.getBoundingClientRect();

  svg.attr("viewBox", `0 0 ${width} ${height}`);

  // Recalculate scales
  xScale.range([margin.left, width - margin.right]);
  yScale.range([height - margin.bottom, margin.top]);

  // Redraw
  updateChart();
}

window.addEventListener("resize", resize);
```

**Touch interactions**:

```javascript
// Touch-friendly target sizes (minimum 44x44px)
points.attr("r", isMobile ? 22 : 5);

// Replace hover with tap
if (isMobile) {
  points.on("click", function(event, d) {
    showTooltip(event, d);
  });
}

// Touch-friendly brush
const brush = d3.brush()
  .touchable(() => true)  // Enable touch
  .extent([[0, 0], [width, height]]);
```

**Mobile-specific considerations**:

- Larger touch targets (44px minimum)
- Tap replaces hover for tooltips
- Simplified interactions (fewer simultaneous gestures)
- Consider removing brush in favor of tap-to-filter
- Landscape vs portrait layout adaptation

### 8. Performance Optimization

Interactions must feel immediate. Optimize for responsiveness.

**Throttle high-frequency events**:

```javascript
function throttle(fn, wait) {
  let lastTime = 0;
  return function(...args) {
    const now = Date.now();
    if (now - lastTime >= wait) {
      lastTime = now;
      fn.apply(this, args);
    }
  };
}

svg.on("mousemove", throttle(handleMouseMove, 16)); // ~60fps
```

**Use Canvas for large datasets**:

When SVG becomes slow (>1000 elements), switch to Canvas:

```javascript
const canvas = d3.select("#chart").append("canvas");
const context = canvas.node().getContext("2d");

function draw() {
  context.clearRect(0, 0, width, height);
  data.forEach(d => {
    context.beginPath();
    context.arc(xScale(d.x), yScale(d.y), 3, 0, 2 * Math.PI);
    context.fill();
  });
}

// Hit detection with quadtree
const quadtree = d3.quadtree()
  .x(d => xScale(d.x))
  .y(d => yScale(d.y))
  .addAll(data);

canvas.on("mousemove", function(event) {
  const [mx, my] = d3.pointer(event);
  const nearest = quadtree.find(mx, my, 10);
  if (nearest) showTooltip(nearest);
});
```

**Debounce expensive operations**:

```javascript
function debounce(fn, wait) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn.apply(this, args), wait);
  };
}

// Only filter after user stops brushing
brush.on("brush", updateHighlight);  // Immediate visual feedback
brush.on("end", debounce(filterData, 200));  // Delayed expensive filter
```

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

## Phase Transition

After adding interactions, consider:

- **Access** to verify keyboard accessibility of all interactions
- **Refine** to ensure interactions don't clutter or confuse
