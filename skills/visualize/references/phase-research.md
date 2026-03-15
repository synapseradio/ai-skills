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

Follow `mode-encode.md` to map data attributes to visual channels. Apply the cognitive mode from Phase 1 (inference → highest-accuracy channels; recognition → pre-attentive channels).

**Produce an encoding table:**

| Data Attribute | Type | Visual Channel | Encoding | Notes |
|---------------|------|----------------|----------|-------|
| *(filled per analysis)* | | | VL: `"type": "quantitative"` / `"nominal"` / `"temporal"` / `"ordinal"` | |

Before presenting to the user, validate using the accuracy, comparison, discrimination, and colorblind tests in `mode-encode.md` (section 8).

Cross-references: `mode-encode.md`, `cleveland-mcgill.md`, `channel-guide.md`

### 3. Select Engine and Template (parallel with step 4)

**Engine selection:** Before choosing a template, determine the rendering engine using the decision flowchart in `engine-selection.md`. The engine choice constrains the available templates and implementation patterns.

Use the template selection decision tree to choose a starting template from the appropriate engine directory:

1. Match the data relationship to a template category and engine:
   - Comparison → `assets/vega/templates/comparisons/` (bar-chart.vl.json, grouped-bar.vl.json, stacked-bar.vl.json)
   - Composition → `assets/vega/templates/compositions/` (pie-chart.vl.json, sunburst.vg.json, treemap.vg.json)
   - Distribution → `assets/vega/templates/distributions/` (histogram.vl.json, box-plot.vl.json, violin-plot.vl.json)
   - Temporal → `assets/vega/templates/temporal/` (line-chart.vl.json, area-chart.vl.json, candlestick.vl.json)
   - Geographic → `assets/vega/templates/geographic/` (choropleth.vg.json)
   - Hierarchical → `assets/vega/templates/hierarchical/` (tree-diagram.vg.json)
   - Network → `assets/d3/templates/networks/sankey.html` (sankey, D3 only), `assets/vega/templates/networks/force-graph.vg.json`
   - Relationship → `assets/vega/templates/relationships/` (scatter-plot.vl.json, heatmap.vl.json, bubble-chart.vl.json)
2. Verify the template supports the planned encoding channels
3. For chart types not in the 19-template library, flag for the **template-crafter** agent

**Tiebreakers when multiple templates fit:**

1. **Prefer simpler** — if a bar chart and a bubble chart both work, the bar chart communicates more accurately
2. **Prefer familiar** — viewers extract information faster from chart types they've seen before
3. **Prefer the argument** — choose the template that best serves the specific comparison
4. **Consider the medium** — interactive web can handle more complexity than a static slide

Cross-references: `template-selection.md`, `engine-selection.md`, `vega-lite-patterns.md`, `vega-patterns.md`

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

**1. Encoding table** — every data attribute mapped to a visual channel with VL/Vega encoding type

**2. Engine and template choice** — which engine (Vega-Lite, Vega, or D3) and which template, with rationale

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
- Selected engine and template
- Ordered transformation plan
- User approval recorded

## Sources

- Cleveland, W.S. and McGill, R. (1984). "Graphical Perception." *JASA*, 79(387), 531-554. https://www.jstor.org/stable/2288400
- Vega-Lite documentation — https://vega.github.io/vega-lite/
- Vega documentation — https://vega.github.io/vega/
- D3.js documentation — https://d3js.org/getting-started
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.
