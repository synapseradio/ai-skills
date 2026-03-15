# Encode Mode

Select visual channels that match data types and maximize perceptual accuracy. Verify Cleveland-McGill rankings and D3 scale APIs against the original research and current documentation before applying.

## Quick Reference

### Data Type → Channel

| Data Type | Best Channels | Avoid |
|-----------|---------------|-------|
| **Quantitative (Q)** | Position, length, area, luminance | Hue, shape (imply no magnitude) |
| **Ordinal (O)** | Position, length, luminance, saturation | Hue, shape (imply no order) |
| **Nominal (N)** | Hue, shape, spatial region | Length, area (imply false order) |
| **Temporal (T)** | Position on x-axis with time scale | N/A |

### Data Type → D3 Scale

| Data + Channel | D3 Scale | Example |
|----------------|----------|---------|
| Q → Position | `d3.scaleLinear()` | Scatter plot axes |
| Q → Position (skewed) | `d3.scaleLog()` | Wide-range data |
| Q → Color | `d3.scaleSequential()` | Heatmap cells |
| O → Position | `d3.scaleBand()` | Bar chart categories |
| N → Color | `d3.scaleOrdinal()` | Category colors |
| T → Position | `d3.scaleTime()` | Line chart x-axis |

### Channel Effectiveness (Cleveland-McGill Ranking)

Most accurate to least accurate for **quantitative** comparison:

1. Position on common scale (scatter, aligned bars)
2. Position on unaligned scales (small multiples)
3. Length (bar height)
4. Angle/slope (line trends, pie slices)
5. Area (bubbles, treemaps)
6. Color luminance/saturation (heatmaps)

For detailed methodology, continue to the full instructions below.

---

## When to Use

- Choosing how to encode data visually
- Deciding between chart types or visual representations
- Mapping data attributes to marks and channels
- The user asks "what chart type" or "how should I represent this data"
- Evaluating whether an existing encoding effectively communicates the data

## Applicability Check

**In comprehensive mode**: Always runs—encoding is the foundation of every visualization.

**Quick check**: Does data exist that needs visual representation? If yes → run this mode.

## Instructions

Choose visual encodings that match data semantics and leverage human perception. The goal is not decoration but accurate, efficient communication of quantitative relationships.

Select encodings systematically by matching data types to channels ranked by perceptual effectiveness:

### 1. Classify Your Data Attributes

Before selecting channels, identify what each data attribute represents. This classification determines which channels can express it accurately:

**Quantitative (Q)**: Continuous numeric values with meaningful arithmetic relationships. Temperature, revenue, counts, percentages. The difference between 10 and 20 is meaningful, as is 20 being twice 10.

**Ordinal (O)**: Ordered categories where sequence matters but intervals do not. Education levels (high school < bachelor's < master's < PhD), satisfaction ratings (poor < fair < good < excellent), size categories (S < M < L < XL). The ordering is meaningful; the "distance" between values is not.

**Nominal (N)**: Categories with no inherent order. Country names, product categories, user IDs. Any ordering would be arbitrary. The only meaningful operation is identity (same or different).

**Temporal (T)**: Time-based values that may act quantitative (durations, timestamps for trend analysis) or ordinal (named months, weekdays). Determine which behavior matters for your analysis.

Classification determines expressiveness: using a magnitude channel (length) for nominal data falsely implies ordering; using an identity channel (hue) for quantitative data obscures magnitudes.

### 2. Apply the Effectiveness Hierarchy

Channels differ in perceptual accuracy. Research by Cleveland and McGill established rankings that guide selection. For **quantitative data**, prefer channels higher on this list:

1. **Position on common scale** (most accurate) - Points along a shared axis. Scatterplots, dot plots, aligned bar charts.
2. **Position on unaligned scales** - Points on separate axes. Small multiples, faceted plots.
3. **Length** - Bar height or width. Bar charts, Gantt charts.
4. **Angle/Slope** - Line slopes, pie slices. Line chart trends, radar charts.
5. **Area** - Circle size, rectangle area. Bubble charts, treemaps.
6. **Color luminance/saturation** - Light to dark, weak to intense. Heatmaps, choropleths.
7. **Volume** (least accurate) - 3D size. Rarely appropriate.

For **ordinal data**, the same ranking applies but with more tolerance for lower-ranked channels since precise magnitude judgment is unnecessary.

For **nominal data**, use identity channels:

- **Spatial region** - Grouping by position
- **Color hue** - Categorical color palettes
- **Shape** - Circles, squares, triangles
- **Motion** - Animated transitions (use sparingly)

See `cleveland-mcgill.md` for the perceptual research foundation.

### Cognitive Mode Determines Strategy

Before applying the hierarchy, determine whether the viewer needs inference or recognition:

**Inference mode** (conclusion-seeking): Prioritize highest-accuracy channels. Structure the
reading path. Provide direct labels to reduce working memory load. Minimize competitive
interference between channels. The viewer must hold information and reason about it.

**Recognition mode** (decision-making): Prioritize pre-attentive channels for the critical
signal. The answer should fire before the viewer reads a word. Categorical disruption beats
subtle hue shift for anomaly detection. The viewer must pattern-match and act.

Diagnostic: "Is the viewer supposed to arrive at a conclusion, or make a decision?"
Conflating these modes produces charts that are technically accurate but cognitively wrong.

### 3. Match Channel to Data Type (Expressiveness)

Ensure the channel can express all and only the relationships in your data:

| Data Type | Expressive Channels | Inexpressive Channels |
|-----------|--------------------|-----------------------|
| Quantitative | Position, length, area, luminance | Hue, shape (imply no magnitude) |
| Ordinal | Position, length, luminance, saturation | Hue, shape (imply no order) |
| Nominal | Hue, shape, spatial region | Length, area (imply false order) |

**Expressiveness violations create misleading visualizations.** Using bar length for categories implies one category is "more" than another. Using color hue for quantities obscures whether red is more or less than blue.

### 4. Consider Perceptual Separability

When encoding multiple attributes simultaneously, some channel combinations interfere with perception while others remain independent:

**Separable (good)**: Position and color, position and shape, color and size. Viewers can attend to each independently.

**Integral (problematic)**: Width and height (perceived as area), red and green channels, position and length on same axis. Viewers perceive these holistically, making independent judgment difficult.

**Asymmetrically separable**: Size interferes with shape (hard to compare shapes of different sizes) but shape does not interfere with size.

When combining channels, prefer separable pairings. Reserve integral channels for single attributes.

### 5. Respect Pre-Attentive Processing

Some visual properties "pop out" immediately without conscious search. Leverage these for emphasis:

**Strong pop-out**: Color (hue and intensity), orientation, size, motion, enclosure, added marks

**Weaker pop-out**: Shape (when size varies), position (when densely packed)

Use pre-attentive properties for:

- Highlighting outliers or important values
- Enabling rapid category identification
- Drawing attention to annotations or callouts

Limit pre-attentive properties to 4-7 distinguishable levels. Beyond that, viewers must search consciously.

### 6. Account for Data Density and Scale

Encoding effectiveness depends on how many data points you're showing:

**Sparse data (< 20 points)**: All channels work well. Consider labels directly on points.

**Moderate data (20-200 points)**: Position remains effective. Color and size still distinguishable. Shape begins struggling past 50 points.

**Dense data (200-10,000 points)**: Position dominates. Use transparency (alpha) to show density. Color hue reduces to ~8 distinguishable categories. Area becomes unreliable for comparison.

**Very dense data (> 10,000 points)**: Consider aggregation or sampling. Heatmaps, hexbin plots, or contour lines encode density itself. Individual marks become meaningless.

### 7. Select D3 Scale Types

Match scale types to your data classification and channel choice:

| Data + Channel | D3 Scale | Notes |
|----------------|----------|-------|
| Q → Position | `d3.scaleLinear()` | Continuous input to continuous output |
| Q → Position (skewed) | `d3.scaleLog()`, `d3.scaleSqrt()` | Transform before encoding |
| Q → Color | `d3.scaleSequential()` | Use perceptually uniform interpolators |
| O → Position | `d3.scalePoint()` | Equal spacing, no bandwidth |
| O → Position (bars) | `d3.scaleBand()` | Includes bandwidth for bar width |
| O → Color | `d3.scaleOrdinal()` | With ordered color scheme |
| N → Color | `d3.scaleOrdinal()` | With categorical scheme (`d3.schemeCategory10`) |
| N → Shape | Manual mapping | D3 symbols: circle, cross, diamond, etc. |
| T → Position | `d3.scaleTime()` | Handles Date objects, proper tick formatting |

Apply `.nice()` to quantitative scales for clean axis boundaries. Use `.domain()` with actual data extent, not assumed ranges.

See `channel-guide.md` for detailed channel-by-channel implementation guidance.

### 8. Validate the Encoding

Before finalizing, test the encoding against these criteria:

**Accuracy test**: Can viewers extract the actual values with acceptable precision? Bar charts allow ~10% accuracy; pie charts ~30%; area ~50%.

**Comparison test**: Can viewers perform the comparisons the visualization is meant to support? If comparing two quantities, are they on the same scale?

**Discrimination test**: Can viewers distinguish all the categories or values that matter? Test with real data at real density.

**Perceptual uniformity test**: Does a visual difference of X represent the same data difference everywhere on the scale? Area and volume fail this—doubling area does not look like doubling.

**Colorblind accessibility test**: Simulate deuteranopia and protanopia. If distinctions disappear, add redundant encoding (shape, position, or direct labels).

## Common Encoding Patterns

### Single Quantitative Variable Distribution

**Task**: Show how values are distributed

**Primary encoding**: Position on common scale via histogram (binned) or dot plot (individual)

**D3 pattern**:

```javascript
const x = d3.scaleLinear()
  .domain(d3.extent(data, d => d.value))
  .range([0, width])
  .nice();
```

**When to use alternatives**: Density plot when smoothness matters more than exact counts. Box plot when summary statistics suffice. Strip plot when showing individual points is important.

### Two Quantitative Variables Relationship

**Task**: Show correlation, clusters, or patterns between two measures

**Primary encoding**: Position on common scales (scatterplot)

**D3 pattern**:

```javascript
const x = d3.scaleLinear().domain(d3.extent(data, d => d.x)).range([0, width]);
const y = d3.scaleLinear().domain(d3.extent(data, d => d.y)).range([height, 0]);
```

**Add third variable**: Size for another quantitative (bubble chart), color for nominal category, shape for nominal with few categories.

**When to use alternatives**: Line chart when x is time or there's inherent ordering. Hexbin when points overlap extensively.

### Quantitative by Nominal Category

**Task**: Compare quantities across categories

**Primary encoding**: Position (bar chart with bars on common baseline)

**D3 pattern**:

```javascript
const x = d3.scaleBand().domain(categories).range([0, width]).padding(0.1);
const y = d3.scaleLinear().domain([0, d3.max(data, d => d.value)]).range([height, 0]);
```

**Orientation choice**: Horizontal bars when category labels are long or when comparing magnitude is primary. Vertical bars when time-based or when categories have natural left-to-right ordering.

**When to use alternatives**: Dot plot when bars add visual clutter. Lollipop chart as minimal alternative. Heatmap when there are two categorical dimensions.

### Proportions of a Whole

**Task**: Show parts summing to 100%

**Consider carefully**: Pie charts are frequently misused. They work only when:

- Parts sum to a meaningful whole
- Comparing a few (2-5) parts
- Approximate proportions suffice
- One part dominates or contrasts with rest

**Primary encoding**: Stacked bar (single bar) or treemap (hierarchical)

**D3 pattern**:

```javascript
const color = d3.scaleOrdinal()
  .domain(categories)
  .range(d3.schemeTableau10);
```

**When to use pie**: Exactly when comparing to 25%, 50%, or 75% benchmarks. Otherwise, bar charts with percentage labels are more accurate.

### Temporal Trends

**Task**: Show change over time

**Primary encoding**: Position with time on x-axis (line chart)

**D3 pattern**:

```javascript
const x = d3.scaleTime()
  .domain(d3.extent(data, d => d.date))
  .range([0, width]);
```

**Multiple series**: Use color for category (limit to ~7 lines). Consider small multiples for more series.

**When to use alternatives**: Area chart when cumulative values matter. Step chart when changes are discrete (not interpolated). Sparklines when many trends need overview comparison.

### Geographic Data

**Task**: Show spatial patterns

**Primary encoding**: Position (map projection) with color or size for data values

**Channel for values**: Sequential color for quantitative (choropleth), categorical color for nominal. Size (proportional symbols) for counts or magnitudes that should not imply density.

**Choropleth warning**: Large areas dominate visually regardless of data values. Consider cartograms or dot density when area bias matters.

## Network Graph Encodings

Network visualizations (force-directed graphs, node-link diagrams) use specific encodings for nodes and edges. See `network-patterns.md` for complete implementation patterns.

### Edge Visual Properties

Edges encode relationships between nodes. Common encodings:

| Channel | Encodes | D3 Scale | Notes |
|---------|---------|----------|-------|
| stroke-width | Connection strength, weight | `d3.scaleLinear()` or `d3.scaleSqrt()` | Use sqrt for skewed distributions |
| stroke-opacity | Confidence, secondary relationships | `d3.scaleLinear()` | Range: [0.4, 1.0] minimum |
| stroke color | Edge category, direction | `d3.scaleOrdinal()` | Verify 3:1 contrast |
| stroke-dasharray | Edge type (solid/dashed) | Manual | Binary distinctions only |

**Visibility thresholds** (edges failing these will not render perceptibly):

| Property | Minimum | Recommended | WCAG AA |
|----------|---------|-------------|---------|
| stroke-width | 1px | 1.5px | 2px |
| stroke-opacity | 0.3 | 0.5 | 0.6+ |
| contrast ratio | 2.5:1 | 3:1 | 4.5:1 |

**Safe edge colors on white background:**

| Color | Contrast | Status |
|-------|----------|--------|
| #555 | 7.46:1 | Excellent |
| #666 | 5.74:1 | Good |
| #777 | 4.54:1 | Acceptable |
| #999 | 2.85:1 | **Fails** |

### Node Visual Properties

Nodes encode entities with their attributes:

| Channel | Encodes | D3 Scale | Notes |
|---------|---------|----------|-------|
| radius | Degree, importance, value | `d3.scaleSqrt()` | **Must use sqrt** for area perception |
| fill color | Category, cluster, type | `d3.scaleOrdinal()` | Use colorblind-safe palettes |
| stroke color | Selection state, highlight | Manual | 3:1 contrast vs fill |
| shape | Entity type (when few) | `d3.symbolType` | Limit to 4-5 shapes |

**Area-based perception**: Human perception judges area, not radius. Always use `d3.scaleSqrt()` for sizing nodes:

```javascript
// Wrong: linear radius exaggerates large values
const radiusScale = d3.scaleLinear().range([4, 30]);

// Correct: sqrt scale for proportional area
const radiusScale = d3.scaleSqrt().range([4, 30]);
```

**Minimum sizes:**

| Target | Minimum Radius | Notes |
|--------|----------------|-------|
| Click target | 4px | Acceptable for mouse |
| Touch target | 6px | Required for mobile |
| Comfortable | 8px | Preferred default |

### Network Encoding Checklist

- [ ] Edge stroke-width ≥ 1.5px at all weights
- [ ] Edge opacity ≥ 0.4 at all confidence levels
- [ ] Edge color passes 3:1 contrast vs background
- [ ] Node radius uses sqrt scale (not linear)
- [ ] Node minimum radius ≥ 4px
- [ ] Interactive states provide 2x+ visual change (hover/focus)

## Anti-Patterns to Avoid

### Area for Precise Comparison

Circles sized by radius create quadratic distortion—doubling the radius quadruples the area. Size by area, not radius:

```javascript
const size = d3.scaleSqrt() // Square root to make area proportional
  .domain([0, d3.max(data, d => d.value)])
  .range([0, maxRadius]);
```

### Rainbow Color Scales

Rainbow scales (red-yellow-green-blue) have no perceptual ordering, uneven luminance, and colorblind accessibility issues. Use:

- Sequential: `d3.interpolateBlues` or `d3.interpolateViridis`
- Diverging: `d3.interpolateRdBu` for values around a meaningful center
- Categorical: `d3.schemeTableau10` for distinct categories

### 3D Without Purpose

Perspective distorts magnitude perception. Avoid 3D bar charts, 3D pie charts, and gratuitous depth. Use 3D only when data has genuine 3D spatial structure.

### Dual Y-Axes

Two y-axes on one chart invite misleading comparisons. The relationship between scales is arbitrary—any correlation can be manufactured by adjusting ranges. Prefer: faceted charts, indexed values to common baseline, or explicit callout of relationship.

### Truncated Axes

Starting a bar chart y-axis above zero exaggerates differences. Use zero baseline for magnitude comparisons. If differences at high values matter, consider log scale or explicit annotations.

## Sources

- Cleveland, W.S. and McGill, R. (1984). "Graphical Perception." *JASA*, 79(387), 531-554. https://www.jstor.org/stable/2288400
- D3.js documentation — https://d3js.org/getting-started
- D3 API Reference — https://github.com/d3/d3/blob/main/API.md
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.
- WCAG 2.2 Quick Reference — https://www.w3.org/WAI/WCAG22/quickref/

## Phase Transition

After encoding, consider:

- **Compose** to arrange the encoded elements with visual hierarchy
- **Access** to verify colorblind safety of the chosen palette
- **Refine** if encoding choices feel uncertain and need critique
