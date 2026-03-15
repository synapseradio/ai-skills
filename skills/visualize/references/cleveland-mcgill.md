# Cleveland and McGill: Graphical Perception Research

This reference documents the foundational research on perceptual accuracy in data visualization, establishing the empirical basis for channel selection.

## The Original Study

William S. Cleveland and Robert McGill published "Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Methods" in the Journal of the American Statistical Association (1984). Their work applied psychophysics—the study of relationships between physical stimuli and perception—to data visualization.

The core question: When humans look at a chart, how accurately can they decode the underlying data values? The answer varies dramatically by encoding method.

## The Experimental Method

Cleveland and McGill designed controlled experiments where subjects:

1. Viewed two marked values on a chart
2. Estimated the smaller as a percentage of the larger
3. Repeated across many value pairs and chart types

They measured **log absolute error**—how far estimates deviated from true values, on a logarithmic scale. This captured both the direction and magnitude of perceptual errors.

The experiments isolated variables: same data, different visual encodings. This revealed which encodings humans decode most accurately.

## The Ranking

From most to least accurate decoding:

### Tier 1: Position (Most Accurate)

**Position along a common scale** enables the most precise value extraction. When two points share an axis (like dots on a dot plot or tops of bars on an aligned bar chart), humans judge their difference with high accuracy.

Error rates: ~2-5% for well-designed position encodings.

**Position along identical but non-aligned scales** (like two separate bar charts with the same scale) degrades slightly because viewers must mentally carry the scale between charts.

### Tier 2: Length

**Length** (bar height, line segment length) allows reasonably accurate comparison. The key is that bars start from a common baseline—without shared baseline, length comparisons degrade to position comparisons on unaligned scales.

Error rates: ~5-10% for length judgments.

### Tier 3: Angle and Slope

**Angle** (pie chart slices, radar chart segments) and **slope** (line chart trends) show higher error rates. Humans have moderate ability to compare angles, but performance drops as angles approach 0 or 180 degrees.

Error rates: ~10-20% for angle judgments.

Pie charts perform poorly for precise value extraction but remain useful when:

- Comparing to benchmark proportions (25%, 50%, 75%)
- Communicating that parts sum to a whole
- The dominant slice is the message

### Tier 4: Area

**Area** (circle size, rectangle size, bubble diameter) produces substantial error. The problem is twofold:

1. **Psychophysical compression**: Perceived area grows slower than physical area. Doubling the physical area does not look like doubling—it looks like a 50-60% increase.

2. **Estimation difficulty**: Comparing two irregular areas (like circles of different sizes) requires mental calculation that humans perform inconsistently.

Error rates: ~20-50% for area judgments.

When using area, encode data as area (not radius or diameter):

```javascript
// Wrong: radius proportional to value
r = value;  // A 2x value creates 4x the area

// Correct: area proportional to value
r = Math.sqrt(value);  // A 2x value creates 2x the area
```

### Tier 5: Volume, Color Saturation, Color Luminance

**Volume** (3D size) suffers all the problems of area, compounded. Perspective distortion makes volume comparisons nearly meaningless for precise data.

**Color saturation** (intensity from pale to vivid) and **color luminance** (brightness from dark to light) enable only rough ordinal judgments. Humans can tell "darker means more" but cannot reliably say "twice as dark."

Error rates: 50%+ for these channels.

### Tier 6: Color Hue (Not Magnitude-Ordered)

**Color hue** (red, blue, green) has no inherent magnitude ordering. It should only encode categorical (nominal) data. Using hue for quantitative data violates expressiveness—viewers cannot determine if red means more or less than blue.

## Extensions by Munzner and Others

Tamara Munzner's *Visualization Analysis and Design* (2014) synthesized Cleveland-McGill with subsequent research, extending the framework:

**Identity channels** (for nominal data):

- Spatial region
- Color hue
- Motion
- Shape

**Magnitude channels** (for ordered data), ranked:

1. Position on common scale
2. Position on unaligned scale
3. Length (1D size)
4. Tilt/angle
5. Area (2D size)
6. Depth (3D position)
7. Color luminance
8. Color saturation
9. Curvature
10. Volume (3D size)

This ranking applies primarily to quantitative data. For ordinal data, the same ranking holds but with greater tolerance for lower-ranked channels since precise magnitude judgment matters less.

## Practical Implications

### Chart Type Selection

| Task | Preferred Encoding | Chart Type |
|------|-------------------|------------|
| Compare exact values | Position on common scale | Bar chart, dot plot, aligned scatter |
| Show distribution | Position | Histogram, box plot, strip plot |
| Show trend over time | Position + slope | Line chart |
| Show part-to-whole (precise) | Length | Stacked bar, 100% bar |
| Show part-to-whole (approximate) | Angle | Pie chart (limited cases) |
| Show correlation | Position (2D) | Scatterplot |
| Show three variables | Position + size | Bubble chart (with caveats) |
| Show geographic pattern | Position (map) + color | Choropleth, proportional symbol |

### When to Violate the Hierarchy

The ranking optimizes for **accuracy of value extraction**. Other goals may justify lower-ranked encodings:

**Memorability**: Some studies suggest "unusual" visualizations (including less accurate ones) are remembered better.

**Engagement**: Charts that invite exploration may use less accurate encodings to encourage interaction.

**Part-whole relationships**: Pie charts explicitly show that segments sum to 100%, which bars do not convey as directly.

**Space efficiency**: Heatmaps using color can display dense matrices where position-based alternatives would not fit.

**Animation**: Motion can show change over time in ways static position cannot.

The hierarchy is guidance, not law. Understand why you're choosing a less accurate encoding.

## Limitations of the Research

Cleveland-McGill tested specific experimental conditions:

- Adult subjects
- Controlled viewing conditions
- Simple comparison tasks (A vs B)
- Clean, minimal charts

Real-world visualizations involve:

- Varied audiences with different visual literacy
- Mobile screens, projectors, print
- Multiple simultaneous comparisons
- Annotations, labels, legends, context

The rankings remain valid guidance, but exact error rates may differ in practice.

## Key Takeaway

**Position is king.** When precise value communication matters, encode your most important data dimension as position on a common scale. Reserve lower-ranked channels for secondary dimensions, categorical distinctions, or cases where other design goals take precedence.

## References

- Cleveland, W.S. and McGill, R. (1984). "Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Methods." *Journal of the American Statistical Association*, 79(387), 531-554.
- Cleveland, W.S. (1993). *Visualizing Data*. Hobart Press.
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.
- Heer, J. and Bostock, M. (2010). "Crowdsourcing Graphical Perception: Using Mechanical Turk to Assess Visualization Design." *CHI 2010*.
