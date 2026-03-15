# Narrate Mode

Structure visualization narrative through annotation, titles, and guided revelation.

## When to Use

- Adding annotations to a chart
- Creating titles and subtitles
- Telling a story with data
- Guiding the reader through insights
- Explaining what's happening in the visualization
- Highlighting key findings
- Making a chart self-explanatory

## Applicability Check

**In comprehensive mode**: Runs when storytelling would aid comprehension.

**Signals to check**:

- Is this visualization explanatory (communicating to others) rather than exploratory (for personal analysis)?
- Does the visualization have an insight that viewers might miss without guidance?
- Is there context (events, comparisons, benchmarks) that adds meaning to the data?

**Quick check**: Would a viewer understand the significance without explanation? If no → run this mode. If the visualization is purely exploratory for personal analysis → skip with "Exploratory visualization—narrative deferred."

## What Narrative Provides

**Guided attention** directs viewers to what matters. Without guidance, viewers scan randomly, often missing the insight the visualization exists to communicate. Narrative elements—annotations, visual hierarchy, sequential revelation—create a path through the data.

**Contextual meaning** transforms numbers into significance. A bar reaching 47% means nothing without context: Is that good? Compared to what? What changed? Narrative provides the interpretive frame that makes data meaningful.

**Memory anchors** create lasting understanding. Viewers forget raw data within minutes. They remember stories, contrasts, and revelations. Narrative structure encodes insights in memorable form.

## The Author-Reader Spectrum

Visualizations exist on a spectrum from author-driven to reader-driven (Segel and Heer, 2010). Position on this spectrum determines narrative strategy.

**Author-driven** visualizations guide viewers through a predetermined sequence. The author controls pacing, ordering, and attention. Techniques include scrollytelling (narrative unfolds as viewer scrolls), slideshow presentations, and annotated video tours. Author-driven approaches work when the insight is specific, the audience unfamiliar, or the story complex enough to require guidance.

**Reader-driven** visualizations provide tools for exploration. Viewers choose their own path through the data. Techniques include interactive dashboards, filter controls, and drill-down hierarchies. Reader-driven approaches work when viewers have domain expertise, multiple valid insights exist, or personalized exploration serves the purpose.

**Hybrid structures** combine both. The martini glass structure presents an author-driven narrative (the stem) before opening into reader-driven exploration (the bowl). Drill-down story points offer authored context at each node while allowing free navigation between nodes.

Before crafting narrative elements, identify where on the spectrum this visualization should fall. The answer shapes every subsequent decision.

See `segel-heer.md` for detailed framework.

## The Narrative Arc

Visual narratives follow the same arc as written ones: setup, tension, revelation, resolution.

**Setup** establishes context. What is this data? What time period? What population? What should viewers already understand before encountering the main insight? Setup annotation includes titles, subtitles, axis labels, and contextual callouts that orient viewers.

**Tension** creates a question. What's surprising here? What doesn't fit expectations? What problem does this data reveal? Tension can be explicit (an annotated question) or implicit (visual contrast that invites explanation). Without tension, visualizations inform without engaging.

**Revelation** delivers the insight. This is the moment the visualization exists for—the "aha" that changes understanding. Revelation requires emphasis: annotation callouts, visual highlighting, or sequential disclosure that creates anticipation before the reveal.

**Resolution** provides implications. Now that viewers understand the insight, what should they do? What does it mean? Resolution connects the specific insight to broader significance.

Not every visualization needs all four elements in explicit form. Simple charts may embed tension and revelation in a single annotated callout. Complex dashboards may distribute the arc across multiple views. But the arc structure provides a diagnostic: if a visualization lacks tension, it may inform without engaging; if it lacks resolution, it may surprise without meaning.

## Annotation Strategy

Annotations are the primary vehicle for narrative in static visualizations. Effective annotation requires decisions about what to annotate, how to annotate, and when annotation serves versus clutters.

### What to Annotate

**Annotate insights, not features.** The goal is not to label every data point but to highlight what matters. Ask: what would viewers miss without this annotation? What interpretation would they get wrong?

**Annotate exceptions and outliers.** When a data point breaks from pattern, annotate to explain why. Unexplained outliers invite incorrect speculation.

**Annotate comparisons.** When the insight requires comparing two points, annotate both and make the relationship explicit. Annotations that say "30% higher than 2019" communicate more than annotations that say "45%."

**Annotate context.** When external events explain data patterns, annotate the event. A spike on March 2020 means something different when annotated "COVID-19 lockdowns begin."

**Annotate uncertainty.** When data quality varies, annotate the variation. Ranges, confidence intervals, and data source notes maintain trust.

### How to Annotate

**Annotation anatomy**: Effective annotations have three components—

1. **Subject**: What is being annotated (the data point, region, or pattern)
2. **Connector**: Visual link between annotation and subject (line, arrow, or bracket)
3. **Note**: The text content that provides meaning

Keep notes concise. Three to seven words for labels, one to two sentences for callouts. If more explanation is needed, consider whether the annotation belongs in a separate legend or caption.

**Positioning**: Place annotations to minimize eye travel between note and subject. Avoid crossing data lines with connectors. When annotations cluster, use leader lines that exit in the same direction before diverging.

**Hierarchy**: Not all annotations are equal. Create visual hierarchy through font weight, color, or connector style. Primary insights receive prominent treatment; supporting context receives subtle treatment.

**Progressive disclosure**: In interactive visualizations, layer annotation depth. Show primary annotations by default; reveal secondary annotations on hover or click.

See `annotation-patterns.md` for implementation techniques.

### When Not to Annotate

**Avoid annotation clutter.** When annotations cover more area than data, the visualization has become a diagram. Step back: is this the right chart type? Should data be filtered?

**Avoid redundant annotation.** If the axis label says "Revenue (millions)", annotations don't need to repeat "revenue" or "M". If a color legend exists, annotations don't need to name what colors represent.

**Avoid patronizing annotation.** If the audience has domain expertise, annotating obvious patterns insults their intelligence. Match annotation density to audience expertise.

## Titles That Work

Titles are the first—and often only—text viewers read. A title that wastes this attention with generic description ("Sales by Region") squanders the most valuable real estate in the visualization.

### Title Types

**Descriptive titles** name what the chart shows: "Monthly Revenue, 2020-2024". These work when the visualization is one of many in a dashboard, when context is established elsewhere, or when the audience will draw their own conclusions.

**Insight-revealing titles** state what the chart means: "Revenue doubled after product launch". These work when a specific insight drives the visualization, when the audience needs guidance, or when the chart appears without supporting text.

**Question titles** frame exploration: "Where did growth come from?" These work for reader-driven visualizations where the answer varies by viewer, or when setting up a reveal that follows.

### Title Anatomy

**Headline**: The main title. Either descriptive or insight-revealing. 5-10 words maximum.

**Subtitle**: Contextual detail. Time period, data source, scope limitations. Smaller font, secondary emphasis.

**Caption**: Extended explanation. Methodology notes, caveats, calls to action. Placed below the visualization.

Not every visualization needs all three. A dashboard tile may have only a headline. An explanatory graphic in a report may have headline, subtitle, and caption. Match title complexity to context.

### Title Testing

Apply these tests to evaluate titles:

1. **The screenshot test**: If someone screenshots this chart with no context, does the title make it interpretable?

2. **The skimmer test**: If someone reads only the title and glances at the chart, do they get the main point?

3. **The accuracy test**: Does the title actually match what the chart shows? Insight-revealing titles that overstate the data undermine trust.

## Sequential Revelation

Some insights land harder when revealed progressively. Sequential revelation creates anticipation, then delivers satisfaction.

### Revelation Techniques

**Scrollytelling**: Narrative elements appear as the viewer scrolls. New annotations, highlighted regions, or transformed views emerge in sequence. The scroll position becomes a narrative timeline.

**Animation**: Data elements animate in sequence, building toward the full picture. The order of animation creates narrative emphasis—what appears last receives most attention.

**Click-through**: Each click advances the narrative. Explicit user action creates psychological investment; viewers feel they are discovering rather than receiving.

**Zoom-in structure**: Start with overview, then zoom to detail. The macro view provides context; the micro view delivers insight. The transition itself communicates the relationship between scales.

### When to Use Sequential Revelation

Sequential revelation adds production complexity. Use it when:

- The insight requires building understanding through stages
- The audience would be overwhelmed by all information at once
- The revelation moment has emotional significance worth amplifying
- The medium supports interaction (web, presentation)

Avoid sequential revelation when:

- The audience needs quick reference access
- The visualization will be printed or embedded as static image
- Multiple valid reading orders exist
- Production constraints make maintenance impractical

## D3.js Annotation Implementation

The d3-annotation library provides structured annotation capabilities:

```javascript
const annotations = [
  {
    note: {
      label: "Sales peaked here",
      title: "Holiday surge"
    },
    x: xScale(peakDate),
    y: yScale(peakValue),
    dy: -50,
    dx: 30
  }
];

const makeAnnotations = d3.annotation()
  .type(d3.annotationCalloutCircle)
  .annotations(annotations);

svg.append("g")
  .attr("class", "annotation-group")
  .call(makeAnnotations);
```

Annotation types serve different purposes:

- **annotationCallout**: Simple text with connector line
- **annotationCalloutCircle**: Circles a data point or region
- **annotationCalloutRect**: Highlights rectangular areas
- **annotationLabel**: Badge-style labels
- **annotationXYThreshold**: Marks threshold lines

## Phase Transition

After adding narrative, consider:

- **Access** to provide text alternatives for screen readers
- **Interact** if users should be able to explore beyond the authored story
- **Refine** to verify annotations don't clutter or obscure
