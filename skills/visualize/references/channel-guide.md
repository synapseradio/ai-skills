# Channel-by-Channel Implementation Guide

Detailed guidance for each visual channel: when to use it, perceptual considerations, and D3.js implementation patterns. Verify perceptual accuracy claims against the Cleveland-McGill research and D3 scale APIs against current documentation before applying.

## Position Channels

### Position on Common Scale (X or Y Axis)

**Data types**: Quantitative (primary), Ordinal, Temporal

**Perceptual accuracy**: Highest. Humans extract values with ~2-5% error.

**When to use**:

- Displaying primary quantitative variable
- Enabling precise value comparison
- Showing trends over time (x-axis)
- Comparing quantities across categories

**D3 scales**:

```javascript
// Quantitative: continuous domain to continuous range
const x = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.value)])
  .range([0, width])
  .nice();

// Ordinal: discrete categories to positions
const x = d3.scaleBand()
  .domain(data.map(d => d.category))
  .range([0, width])
  .padding(0.1);

// Temporal: Date objects to positions
const x = d3.scaleTime()
  .domain(d3.extent(data, d => d.date))
  .range([0, width]);
```

**Implementation notes**:

- Use `.nice()` to round domain to clean boundaries
- For y-axis, invert range: `.range([height, 0])` so larger values appear higher
- `scaleBand()` provides `.bandwidth()` for bar width
- `scalePoint()` for ordinal without bandwidth (dot plots)

### Position on Unaligned Scales (Small Multiples)

**Data types**: Quantitative, Ordinal

**Perceptual accuracy**: Slightly lower than aligned (~5-10% error). Viewers mentally carry the scale.

**When to use**:

- Comparing patterns across facets
- Showing same metric across categories, time periods, or segments
- When aligned scales would create clutter

**D3 pattern**:

```javascript
// Create one scale, reuse across facets
const y = d3.scaleLinear()
  .domain([0, d3.max(allData, d => d.value)])  // Shared domain!
  .range([facetHeight, 0]);

// Position each facet
facets.forEach((facet, i) => {
  const g = svg.append('g')
    .attr('transform', `translate(${i * (facetWidth + margin)}, 0)`);
  // Draw with shared y scale
});
```

**Critical**: Use identical scales across facets. Different scales break comparison.

## Length Channel

**Data types**: Quantitative

**Perceptual accuracy**: Good (~5-10% error) when bars share baseline.

**When to use**:

- Bar charts (vertical or horizontal)
- Stacked bars (with caveats—only bottom segment has reliable baseline)
- Gantt charts
- Lollipop charts

**D3 pattern**:

```javascript
const y = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.value)])
  .range([height, 0]);

// Bar height = distance from baseline to scaled value
bars.attr('height', d => height - y(d.value))
    .attr('y', d => y(d.value));
```

**Critical considerations**:

- **Zero baseline**: Length encoding requires bars to start at zero. Truncating the axis turns length into position comparison, losing the perceptual advantage.
- **Stacked bar limitation**: In stacked bars, only the bottom segment benefits from the shared baseline. Upper segments are effectively position-on-unaligned-scale.

## Angle/Slope Channel

### Angle (Pie Charts, Radial Charts)

**Data types**: Quantitative (proportion)

**Perceptual accuracy**: Moderate (~10-20% error).

**When to use**:

- Showing parts of a whole (sum to 100%)
- 2-5 categories maximum
- When approximate comparison suffices
- When comparing to 25%, 50%, 75% benchmarks

**D3 pattern**:

```javascript
const pie = d3.pie()
  .value(d => d.value)
  .sort(null);  // Preserve data order

const arc = d3.arc()
  .innerRadius(0)  // Pie chart; >0 for donut
  .outerRadius(radius);

const arcs = pie(data);

g.selectAll('path')
  .data(arcs)
  .join('path')
  .attr('d', arc)
  .attr('fill', d => color(d.data.category));
```

**When NOT to use**:

- More than 5-7 categories
- When precise value comparison matters
- When categories don't sum to a meaningful whole

### Slope (Line Charts)

**Data types**: Quantitative change over ordered dimension

**Perceptual accuracy**: Moderate for trend direction; poor for precise slope comparison.

**When to use**:

- Showing trends over time
- Connecting related points
- When direction of change matters more than magnitude

**D3 pattern**:

```javascript
const line = d3.line()
  .x(d => x(d.date))
  .y(d => y(d.value))
  .curve(d3.curveMonotoneX);  // Smooth, preserves monotonicity

path.attr('d', line(data));
```

**Aspect ratio matters**: Slope perception depends on chart proportions. Banking to 45 degrees (adjusting aspect ratio so average slope is 45 degrees) optimizes slope discrimination.

## Area Channel

**Data types**: Quantitative

**Perceptual accuracy**: Low (~20-50% error). Subject to psychophysical compression.

**When to use**:

- Bubble charts (third variable in scatterplot)
- Treemaps (hierarchical part-to-whole)
- Proportional symbols on maps
- When approximate magnitude suffices

**D3 pattern—critical**:

```javascript
// CORRECT: Scale by area, not radius
const size = d3.scaleSqrt()  // Square root!
  .domain([0, d3.max(data, d => d.value)])
  .range([0, maxRadius]);

circles.attr('r', d => size(d.value));

// WRONG: Linear radius creates quadratic area distortion
const size = d3.scaleLinear()  // Don't do this
  .domain([0, d3.max(data, d => d.value)])
  .range([0, maxRadius]);
```

**Why sqrt?** Circle area = pi * r^2. To make area proportional to data, radius must be sqrt(data). `d3.scaleSqrt()` handles this.

**Minimum size**: Very small circles become invisible. Set minimum radius or filter small values.

```javascript
const size = d3.scaleSqrt()
  .domain([0, d3.max(data, d => d.value)])
  .range([4, maxRadius]);  // 4px minimum
```

## Color Channels

### Color Hue (Categorical)

**Data types**: Nominal only

**Perceptual accuracy**: N/A—not for magnitude comparison.

**When to use**:

- Distinguishing categories
- Grouping related elements
- Encoding nominal variables

**D3 pattern**:

```javascript
// Built-in categorical schemes
const color = d3.scaleOrdinal(d3.schemeCategory10);
const color = d3.scaleOrdinal(d3.schemeTableau10);

// Custom palette
const color = d3.scaleOrdinal()
  .domain(['A', 'B', 'C'])
  .range(['#e41a1c', '#377eb8', '#4daf4a']);
```

**Limits**:

- 7-12 distinguishable hues maximum
- Avoid red-green combinations (colorblindness)
- Test with colorblind simulators

**Accessibility pattern**:

```javascript
// Colorblind-safe palette (Paul Tol)
const colorblindSafe = [
  '#332288', '#88CCEE', '#44AA99', '#117733',
  '#999933', '#DDCC77', '#CC6677', '#882255', '#AA4499'
];
```

### Color Luminance (Sequential)

**Data types**: Quantitative, Ordinal

**Perceptual accuracy**: Low for precise values; good for "more/less" judgments.

**When to use**:

- Heatmaps
- Choropleths
- Encoding magnitude when position is unavailable

**D3 pattern**:

```javascript
// Single-hue sequential (light to dark)
const color = d3.scaleSequential()
  .domain([0, d3.max(data, d => d.value)])
  .interpolator(d3.interpolateBlues);

// Perceptually uniform (better)
const color = d3.scaleSequential()
  .domain([0, d3.max(data, d => d.value)])
  .interpolator(d3.interpolateViridis);
```

**Perceptual uniformity**: `interpolateViridis`, `interpolateCividis` (colorblind-safe), and `interpolatePlasma` are perceptually uniform—equal steps in data create equal perceptual steps. Rainbow (`interpolateRainbow`) is not uniform and should be avoided.

### Color Saturation

**Data types**: Quantitative (secondary)

**Perceptual accuracy**: Low. Use as redundant encoding, not primary.

**When to use**:

- Reinforcing another encoding
- Showing intensity or certainty

### Diverging Color Scales

**Data types**: Quantitative with meaningful center

**When to use**:

- Data has a natural midpoint (zero, average, threshold)
- Positive and negative values
- Deviation from expected

**D3 pattern**:

```javascript
const color = d3.scaleDiverging()
  .domain([minValue, 0, maxValue])  // Midpoint at center
  .interpolator(d3.interpolateRdBu);

// Ensure midpoint maps to neutral color
const color = d3.scaleDiverging()
  .domain([-50, 0, 100])  // Asymmetric is fine
  .interpolator(d3.interpolatePuOr);
```

## Shape Channel

**Data types**: Nominal only

**Perceptual accuracy**: Distinguishes categories; no magnitude interpretation.

**When to use**:

- Scatterplots with categorical grouping
- When color is already used for another variable
- Accessibility (redundant with color)

**D3 pattern**:

```javascript
const symbols = d3.scaleOrdinal()
  .domain(['Group A', 'Group B', 'Group C'])
  .range([d3.symbolCircle, d3.symbolCross, d3.symbolDiamond]);

const symbolGenerator = d3.symbol()
  .size(64);  // Area in square pixels

points.attr('d', d => {
  symbolGenerator.type(symbols(d.group));
  return symbolGenerator();
});
```

**Built-in D3 symbols**:

- `symbolCircle` - Default, works at all sizes
- `symbolCross` - Distinctive, good at medium sizes
- `symbolDiamond` - Clear rotation from square
- `symbolSquare` - Familiar
- `symbolStar` - Attention-grabbing
- `symbolTriangle` - Clear direction
- `symbolWye` - Y-shape, less common

**Limits**:

- 5-7 shapes maximum before confusion
- Size affects shape discriminability (small shapes blur together)
- Combine with color for better discrimination

## Size Channel (Non-Area)

### Width and Height Separately

Generally avoid. Width × height is perceived as area, not as independent dimensions.

### Line Thickness (Stroke Width)

**Data types**: Quantitative (limited range), Ordinal

**When to use**:

- Emphasizing important edges in networks
- Showing flow magnitude in Sankey diagrams
- Encoding edge weight

**D3 pattern**:

```javascript
const strokeWidth = d3.scaleLinear()
  .domain([0, d3.max(links, d => d.value)])
  .range([1, 10]);

links.attr('stroke-width', d => strokeWidth(d.value));
```

**Limits**: 3-5 distinguishable widths. Use for ordinal (thin/medium/thick) or continuous encoding where precision is not needed.

## Transparency (Alpha) Channel

**Data types**: Quantitative (density), Ordinal (emphasis)

**When to use**:

- Overplotting in dense scatterplots
- Showing uncertainty
- De-emphasizing context elements

**D3 pattern**:

```javascript
// Fixed transparency for density
circles.attr('fill', 'steelblue')
       .attr('opacity', 0.3);

// Scaled transparency
const opacity = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.value)])
  .range([0.1, 1]);

circles.attr('opacity', d => opacity(d.certainty));
```

**Interaction with color**: Overlapping transparent elements create emergent colors. For scatterplots, this reveals density. For other uses, it may confuse.

## Texture and Pattern

**Data types**: Nominal

**When to use**:

- Accessibility (redundant with color for colorblind users)
- Black-and-white printing
- Distinguishing overlapping areas

**D3 pattern**:

```javascript
// Define patterns in defs
const pattern = defs.append('pattern')
  .attr('id', 'diagonal')
  .attr('patternUnits', 'userSpaceOnUse')
  .attr('width', 8)
  .attr('height', 8);

pattern.append('path')
  .attr('d', 'M-1,1 l2,-2 M0,8 l8,-8 M7,9 l2,-2')
  .attr('stroke', '#000')
  .attr('stroke-width', 1);

// Use pattern as fill
rect.attr('fill', 'url(#diagonal)');
```

**Limits**: Patterns interfere with shape perception. Use sparingly.

## Motion Channel

**Data types**: Temporal change, attention direction

**When to use**:

- Animated transitions between states
- Showing change over time
- Drawing attention to updates

**Avoid**: Motion as primary encoding for static data values.

**D3 pattern**:

```javascript
circles.transition()
  .duration(750)
  .ease(d3.easeCubicInOut)
  .attr('cx', d => x(d.newX))
  .attr('cy', d => y(d.newY));
```

**Principles**:

- Object constancy: Keep identity during transitions
- 200-800ms durations for comprehensibility
- Ease in and out (not linear) for natural motion

## Channel Combinations

### Recommended Pairings

| Primary Channel | Compatible Secondary Channels |
|-----------------|------------------------------|
| Position (x, y) | Color hue, size, shape |
| Length (bars) | Color hue (only) |
| Color hue | Shape, position |
| Size | Color hue, position |

### Problematic Pairings

| Combination | Problem |
|-------------|---------|
| Width + Height | Perceived as area, not independent |
| Size + Shape | Size affects shape perception |
| Hue + Saturation | Hard to separate |
| Multiple position encodings | Cluttered, confusing |

### Redundant Encoding

Using multiple channels for the same variable improves accessibility and emphasis:

```javascript
// Encode category with both color AND shape
const color = d3.scaleOrdinal(d3.schemeTableau10);
const shape = d3.scaleOrdinal([d3.symbolCircle, d3.symbolSquare, d3.symbolTriangle]);

points
  .attr('fill', d => color(d.category))
  .attr('d', d => {
    symbolGenerator.type(shape(d.category));
    return symbolGenerator();
  });
```

Colorblind users can distinguish by shape; all users get faster category recognition.

## Sources

- Cleveland, W.S. and McGill, R. (1984). "Graphical Perception." *JASA*, 79(387), 531-554. https://www.jstor.org/stable/2288400
- D3.js documentation — https://d3js.org/getting-started
- D3 API Reference — https://github.com/d3/d3/blob/main/API.md
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.
