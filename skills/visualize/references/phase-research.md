# Phase 2: Research

Assess data, plan encoding, select template, and confirm the approach with the user before implementation. These patterns synthesize established visualization practice. Primary sources are cited where available.

## Entry Conditions

Phase 1 (Context) complete. The following are established:

- Argument sentence
- Viewer and task
- Cognitive mode (inference or recognition)
- Constraints and data status

## Instructions

Execute steps 1–2 sequentially, then steps 3–4 in parallel.

### 1. Assess Data

Classify each data attribute:

| Type | Description | Meaningful Operations | Example |
|------|-------------|----------------------|---------|
| **Quantitative (Q)** | Continuous numeric with meaningful arithmetic | Difference, ratio, sum | Revenue, temperature, counts |
| **Ordinal (O)** | Ordered categories, intervals not meaningful | Greater-than, less-than | Satisfaction ratings, education levels |
| **Nominal (N)** | Categories with no inherent order | Identity (same/different) | Country names, product categories |
| **Temporal (T)** | Time-based values | Sequence, duration, interval | Dates, timestamps, durations |

Then identify:

- **Shape** — tabular, hierarchical, network, geographic, temporal series
- **Volume** — row count, attribute count, expected visual density
- **Quality** — missing values, outliers, formatting inconsistencies, duplicates
- **Key relationships** — which attributes the argument requires comparing

For the full classification methodology and Cleveland-McGill effectiveness rankings, cross-reference `mode-encode.md`.

### 2. Plan Encoding

Map data attributes to visual channels using the perceptual effectiveness hierarchy.

**Apply cognitive mode to encoding strategy:**

- **Inference mode** → prioritize highest-accuracy channels, structure reading path, provide direct labels to reduce working memory load, minimize competitive interference between channels
- **Recognition mode** → prioritize pre-attentive channels for the critical signal, categorical disruption for anomalies, the answer should fire before the viewer reads a word

**Encoding sequence:**

1. Identify the primary comparison the argument requires
2. Assign the highest-accuracy channel to the primary comparison (position > length > angle > area > color)
3. Assign secondary channels to supporting attributes
4. Verify expressiveness — channel matches data type (no hue for quantities, no length for nominals)
5. Check separability — combined channels do not interfere perceptually
6. Plan color palette — sequential for quantitative, diverging for data with meaningful center, categorical for nominal (max 8 distinguishable hues)

**Produce an encoding table:**

| Data Attribute | Type | Visual Channel | D3 Scale | Notes |
|---------------|------|----------------|----------|-------|
| *(filled per analysis)* | | | | |

Cross-references: `mode-encode.md`, `cleveland-mcgill.md`, `channel-guide.md`

### Encoding Validation

Before presenting to the user, validate the encoding plan:

**Accuracy test:** Can viewers extract actual values with acceptable precision?

- Position on common scale → ~10% accuracy (sufficient for most comparisons)
- Length → ~15% accuracy (sufficient for ranking)
- Area → ~50% accuracy (sufficient only for rough magnitude)

**Comparison test:** Can viewers perform the comparisons the argument requires?

- If comparing two quantities, are they on the same scale with a common baseline?
- If comparing categories, are they adjacent or visually grouped?

**Discrimination test:** Can viewers distinguish all categories or values that matter?

- Nominal color: maximum ~8 distinguishable hues
- Shape: maximum ~5 before confusion
- At expected data density, will marks overlap to illegibility?

**Colorblind pre-check:** Will the planned palette survive deuteranopia and protanopia simulation? If color carries structural information, plan a redundant channel (shape, pattern, or label).

Cross-reference: `mode-encode.md` (section 8: Validate the Encoding)

### 3. Select Template (parallel with step 4)

Use the template selection decision tree to choose a starting template from `assets/d3/templates/`:

1. Match the data relationship to a template category:
   - Comparison → `comparisons/` (bar-chart, grouped-bar, stacked-bar)
   - Composition → `compositions/` (pie-chart, sunburst, treemap)
   - Distribution → `distributions/` (histogram, box-plot, violin-plot)
   - Temporal → `temporal/` (line-chart, area-chart, candlestick)
   - Geographic → `geographic/` (choropleth)
   - Hierarchical → `hierarchical/` (tree-diagram)
   - Network → `networks/` (force-graph, sankey)
   - Relationship → `relationships/` (scatter-plot, heatmap, bubble-chart)
2. Verify the template supports the planned encoding channels
3. For chart types not in the 19-template library, flag for the **template-crafter** agent

**Tiebreakers when multiple templates fit:**

1. **Prefer simpler** — if a bar chart and a bubble chart both work, the bar chart communicates more accurately
2. **Prefer familiar** — viewers extract information faster from chart types they've seen before
3. **Prefer the argument** — choose the template that best serves the specific comparison
4. **Consider the medium** — interactive web can handle more complexity than a static slide

Cross-reference: `template-selection.md`

### 4. Plan Data Transforms (parallel with step 3)

Identify transformations needed to move from raw data to visualization-ready format:

| Transform | When Needed | Example |
|-----------|-------------|---------|
| **Pivot** | Wide-to-long or long-to-wide | Columns per year → rows per year |
| **Aggregate** | Raw data too granular for encoding | Transactions → daily totals |
| **Derive** | Calculated fields needed | Percentage of total, running average |
| **Coerce** | Type mismatches | String dates → Date objects |
| **Filter** | Subset needed | Remove outliers, select date range |
| **Nest/Group** | Hierarchical encoding needed | Flat rows → nested tree structure |

Document the transformation sequence. Order matters: filter before aggregate produces different results than aggregate before filter.

Cross-reference: `data-preparation.md`

## No-Data-Yet Flow

When data is not yet available:

1. **Ask clarifying questions** about data shape and format — what columns exist, what types, approximate volume
2. **Offer to generate synthetic sample data** for prototyping — match expected schema and distributions
3. **If user can describe schema** → create provisional encoding plan, proceed with synthetic data
4. **If user cannot describe schema** → infer plausible schemas from the argument, suggest options, let user select

**Re-entry:** When real data arrives, return to step 1 (Assess Data) to validate the provisional encoding plan. Provisional decisions are hypotheses, not commitments. Expect that real data will reveal:

- Unexpected distributions requiring scale adjustments
- Missing values requiring explicit handling
- Volume differences requiring density management
- Attribute types that differ from assumptions

## User Review Checkpoint

Present the research summary for user approval before implementation:

**1. Encoding table** — every data attribute mapped to a visual channel with D3 scale

**2. Template choice** — which template from which category, with rationale

**3. Transformation plan** — ordered list of data transforms

**4. Accessibility notes** — any constraints identified (colorblind requirements, screen reader support, WCAG level)

**Proceed options:**

- **Proceed** → advance to Phase 3: Implementation
- **Adjust** → modify specific encoding or template choices (loop within Phase 2)
- **Retry** → return to Phase 1 with revised framing

Do not proceed to implementation without explicit user approval. The encoding plan is the contract between intent and artifact.

## Exit

Proceed to **Phase 3: Implementation** with:

- Confirmed encoding table
- Selected template
- Ordered transformation plan
- User approval recorded

## Sources

- Cleveland, W.S. and McGill, R. (1984). "Graphical Perception." *JASA*, 79(387), 531-554. https://www.jstor.org/stable/2288400
- D3.js documentation — https://d3js.org/getting-started
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.
