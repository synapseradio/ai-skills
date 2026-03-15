# Compose Mode

Arrange visual elements using hierarchy, Gestalt principles, and information design. Verify Gestalt grouping principles and D3 layout patterns against primary sources before applying to novel layouts.

## When to Use

- Designing chart layout
- Organizing dashboard elements
- Creating visual hierarchy
- Arranging visualization components
- Composing multi-view displays
- Positioning annotations
- Structuring whitespace

## Applicability Check

**In comprehensive mode**: Always runs—layout is essential for every visualization.

**Quick check**: Do visual elements exist that need spatial arrangement? If yes → run this mode.

## Core Principles

Layout serves comprehension. Every positioning decision either aids or hinders understanding. The goal is not aesthetic arrangement but cognitive efficiency: viewers should find what they need, understand relationships, and follow the intended narrative without conscious effort.

Three foundations support effective visualization layout:

**Visual hierarchy** determines what the eye sees first, second, third. Primary elements receive visual weight through size, position, contrast, or isolation. Secondary elements support without competing. Tertiary elements recede until needed. The hierarchy matches information importance.

**Gestalt principles** describe how humans perceive visual relationships. Elements that are close together appear grouped. Elements that look similar appear related. The eye follows continuous lines. Closed shapes feel complete even when broken. These perceptual tendencies are not stylistic preferences but cognitive facts.

**Information density** balances comprehension against completeness. Too sparse wastes the viewer's cognitive capacity. Too dense overwhelms it. The right density presents maximum insight per unit of mental effort.

## Instructions

When composing layout for a visualization:

### 1. Establish the Information Hierarchy

Identify what matters most. Ask: if the viewer remembers only one thing, what should it be? That element receives prime position and maximum visual weight.

Map the information structure:

- **Primary**: The core insight or metric. This dominates the composition.
- **Secondary**: Supporting information that contextualizes the primary. This is clearly visible but subordinate.
- **Tertiary**: Reference information, labels, legends. These are available but do not compete for initial attention.

Assign visual weight proportionally. Size, position, and contrast all contribute to perceived importance. When everything appears equally important, nothing does.

### 2. Apply Spatial Grouping

Use proximity to create relationships. Elements that belong together should be closer to each other than to unrelated elements. The eye perceives clusters as units before it reads individual marks.

Create visual breathing room between groups. Whitespace is not emptiness but structure. It separates, isolates, and emphasizes. Tight spacing within groups and generous spacing between groups creates instant legibility.

When designing multi-chart layouts:

- Group charts that share context or comparison relationship
- Separate charts that serve different analytical purposes
- Align shared axes to enable visual comparison
- Use consistent margins to establish rhythm

### 3. Design the Reading Path

Western viewers read visualizations like text: left-to-right, top-to-bottom. Place the most important element where reading naturally begins (top-left quadrant). Support the narrative flow by positioning subsequent elements along the natural reading path.

Guide the eye deliberately:

- Use alignment to create visual continuity
- Deploy connecting lines or shared color to link related elements
- Position annotations near their referents
- Lead from overview to detail, from context to focus

Break the natural path only when doing so serves emphasis. A key insight positioned contrary to reading flow draws attention through its violation of expectation.

### 4. Balance Information Density

Apply Tufte's data-ink ratio: maximize the data, minimize everything else. Every pixel should either show data or help the viewer understand data. Decorative elements, redundant encoding, and chartjunk consume attention without adding insight.

Evaluate each non-data element:

- Does this gridline aid reading or add noise?
- Does this border group effectively or merely decorate?
- Does this background color encode information or distract from it?
- Does this label add clarity or create clutter?

When in doubt, remove. The visualization that communicates most clearly usually contains the least visual noise.

### 5. Handle Multi-View Composition

Dashboards and multi-panel displays require coordinated layout. Each view serves the whole; none stands alone.

Establish a grid system. Align edges, maintain consistent gutters, use proportional sizing. The grid creates visual order that the viewer perceives unconsciously but would notice immediately if broken.

Coordinate visual encodings:

- Use consistent color palettes across views
- Maintain consistent scales where comparison is intended
- Standardize typography and label formatting
- Align legends and axes when possible

Design for the 5-second test: if a viewer glances for five seconds, what will they take away? That insight should be immediately visible, not buried in secondary panels.

### 6. Position Annotations and Labels

Annotations connect data to meaning. Position them close to their referents but not overlapping. Use leader lines when proximity cannot be achieved directly.

Label placement follows priority:

1. Direct labels on marks (preferred when space permits)
2. Axis labels for systematic encoding
3. Legends when direct labeling would create clutter
4. Tooltips for on-demand detail

Avoid label collision through careful spacing, rotation, abbreviation, or selective labeling. When all else fails, interactive reveal (hover, click) defers detail without cluttering the static view.

### 7. Use Whitespace Strategically

Whitespace performs multiple functions:

- **Separation**: Creates boundaries between groups
- **Emphasis**: Isolation draws attention
- **Rest**: Gives the eye places to pause
- **Proportion**: Balances visual weight

Dense visualizations need generous margins. The data itself is visually busy; the surrounding space provides relief. Padding around text improves readability. Margin between charts prevents visual interference.

Active whitespace is designed. Passive whitespace is leftover. Design every space.

### 8. SVG Layer Order for Networks

SVG elements render in document order—elements appended later appear on top. For network visualizations, incorrect layer ordering causes interaction failures.

**Required layer sequence:**

```javascript
const svg = d3.select('#chart').append('svg');

// 1. Background layer (optional: grid, reference elements)
const bgLayer = svg.append('g').attr('class', 'background');

// 2. Edges MUST be appended before nodes
const linkLayer = svg.append('g').attr('class', 'links');

// 3. Nodes after edges (so nodes render on top)
const nodeLayer = svg.append('g').attr('class', 'nodes');

// 4. Labels last (always visible)
const labelLayer = svg.append('g').attr('class', 'labels');
```

**Why order matters:**

- Edges appended after nodes render on top, blocking mouse events
- Labels appended before nodes become obscured by node fills
- Incorrect order breaks interaction even when visual output appears correct

**Verification:** Inspect the DOM to confirm `<g class="links">` appears before `<g class="nodes">`:

```html
<svg>
  <g class="background">...</g>
  <g class="links">...</g>      <!-- Before nodes -->
  <g class="nodes">...</g>
  <g class="labels">...</g>     <!-- After nodes -->
</svg>
```

**Label interaction:** Labels positioned over nodes will intercept pointer events. Always set `pointer-events: none` on label text elements:

```css
.node-label {
  pointer-events: none;  /* Pass events through to nodes */
}
```

See `network-patterns.md` for complete network composition patterns.

### 9. Validate the Composition

Test the layout against these criteria:

**Hierarchy test**: Cover your hand over parts of the visualization. Is the primary information visible in any uncovered portion? If secondary elements dominate any quadrant, rebalance.

**Grouping test**: Can you identify distinct groups at a glance? If boundaries are unclear, increase separation between groups or strengthen proximity within groups.

**Path test**: Track where your eye moves naturally. Does it follow the intended narrative? If the eye wanders randomly, strengthen the visual guidance.

**Density test**: Does the visualization feel cluttered? Sparse? The right density communicates efficiently without overwhelming.

**Distance test**: Step back (literally or by zooming out). Do the main patterns remain legible? If detail dominates, the hierarchy needs strengthening.

## Implementation Patterns

### Vega-Lite Composition (primary)

VL provides declarative composition operators that handle layout automatically:

**Responsive sizing:** Set `"width": "container"` to fill the parent element. The parent HTML element must have a defined width.

**Layer** — overlay marks on shared axes (e.g., line + points + annotations):

```json
{"layer": [{"mark": "line", ...}, {"mark": "point", ...}, {"mark": {"type": "text", "dy": -10}, ...}]}
```

**Facet** — small multiples from a single dataset:

```json
{"facet": {"field": "region", "type": "nominal", "columns": 3}, "spec": {"mark": "line", ...}}
```

**Concat** — independent charts side by side. Use `"resolve": {"scale": {"x": "shared"}}` to sync axes:

```json
{"hconcat": [{"mark": "bar", ...}, {"mark": "point", ...}]}
```

**Dashboard layout:** Embed multiple `vegaEmbed()` calls targeting distinct containers, using CSS Grid or Flexbox for positioning. See `base-vega-wrapper.md` (Dashboard Mode).

### D3 Layout Patterns (sankey and custom templates only)

For D3-based charts, see `d3-patterns.md` for margin convention, responsive viewBox pattern, and grid-based multi-view layout.

## Common Layout Problems

**Problem**: All elements compete for attention.
**Solution**: Establish clear hierarchy. Increase size/weight of primary element, reduce secondary elements, push tertiary to periphery.

**Problem**: Groups are not perceived as groups.
**Solution**: Increase proximity within groups, increase separation between groups. Use enclosure (subtle background) if spacing is constrained.

**Problem**: The eye wanders without direction.
**Solution**: Strengthen the reading path. Add alignment, connecting elements, or visual weight along the intended sequence.

**Problem**: Labels collide or obscure data.
**Solution**: Reduce label count (label only key points), use leader lines, employ hover/tooltip for detail, adjust placement.

**Problem**: Dense data creates visual noise.
**Solution**: Increase whitespace, reduce non-data ink, use aggregation or filtering, consider small multiples.

## Sources

- Gestalt Principles — https://www.interaction-design.org/literature/topics/gestalt-principles
- Tufte, E. (1983). *The Visual Display of Quantitative Information*. Graphics Press.
- D3.js documentation — https://d3js.org/getting-started

## Further Reading

For deeper guidance on specific composition topics:

- See `gestalt.md` for detailed Gestalt principles applied to data visualization
- See `hierarchy.md` for visual weight factors and dashboard hierarchy patterns

## Phase Transition

After composing layout, consider:

- **Narrate** to add annotations that explain the arrangement
- **Access** to verify tab order matches visual hierarchy
- **Refine** if layout feels cluttered or unfocused
