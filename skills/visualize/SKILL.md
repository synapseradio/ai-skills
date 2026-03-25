---
name: visualize
description: >
  Create browser-runnable data visualizations using Vega and D3.js — from bar charts to
  force-directed networks. Every output is a standalone HTML file with no build step.
  This skill should be used when the user asks to "create a visualization",
  "make a chart", "graph this data", "show this visually", "visualize this",
  "encode data", "design a layout", "annotate my chart", "make this accessible",
  "add interactivity", "refine this visualization", "plot this", or "diagram this data".
  Also triggers on: "data viz", "chart question", "vega", "D3", "best chart type for",
  "how should I display this", "what visualization", "compare these numbers",
  "show the trend", "make a dashboard", "show me a map". Use this skill even when the
  user just provides data and says "show me" or "what does this look like" — any request
  to see data visually should route here.
context: fork
user-invocable: true
---

# Visualize

Create browser-runnable data visualizations. Every output is a standalone HTML file — no
build step, no server, no dependencies beyond CDN. Two engines: Vega (declarative, default)
and D3 (imperative, for full control and accessibility).

## Core Principles

These principles determine whether a visualization communicates or decorates. They apply to
every chart, regardless of engine or chart type. When in doubt, return to these.

### Intent — find the claim before touching data

- **Complete the sentence: "This visualization shows that ___."** If you cannot finish it
  with a specific claim, stop. You do not have a visualization yet — you have a topic. Topics
  produce decoration. Claims produce communication.
- **Know whose decision this serves.** Complete: "[Person] needs to [action] by [when]."
  The specificity determines whether you build for rapid recognition or open exploration.
- **Determine whether the viewer is arriving at a conclusion or making a decision.**
  Conclusions need guided reading paths and working-memory support. Decisions need categorical
  signals that fire before the viewer reads a word. These require different designs.
- **Do the honesty check before you design.** What complexity does simplification hide? What
  outliers does the argument smooth over? If honest examination undermines the argument, revise
  the argument — not the honesty.

### Encoding — match channel to data, respect the hierarchy

- **Encode your most important quantitative variable as position on a common scale.** Position
  is 5-10x more accurate than area or color for value extraction. Everything else is a concession.
- **The channel ranking: position > length > angle/slope > area > luminance/saturation > hue.**
  Use the highest-ranked channel for the most important variable.
- **Match channel to data type.** Length and area imply magnitude — never use them for categories.
  Hue implies identity — never use it for quantities. Violating this asserts relationships the
  data does not contain.
- **Scale area by sqrt, not linearly.** `radius = sqrt(value)` makes visual area proportional
  to data. Linear radius creates quadratic distortion.
- **Bar charts must start at zero.** Length encoding depends on the baseline. If the differences
  are too small to see at zero, that is meaningful information.
- **Sort categories by value, not alphabetically.** Alphabetical sorting turns the visual pattern
  into random noise.
- **Data without units is decoration.** Every axis label, annotation, and tooltip must include
  units. If the data has no units, state what it measures.

### Composition — one chart, one job

- **A single visualization makes a single point.** If your chart needs a paragraph to explain,
  it might need to be two charts.
- **Decide what the viewer sees first, second, third — then assign visual weight in that order.**
  Size, position, contrast, and isolation contribute to weight. When everything has equal weight,
  nothing communicates.
- **Build a three-level hierarchy: primary (the insight), secondary (context), tertiary
  (reference).** Give primary disproportionate visual weight. Give tertiary near-invisible weight.
- **Prefer direct labels over legends.** Legends force round-trips between data and key. Label
  lines at endpoints, bars at their values, series inline.
- **Build hierarchy by reducing secondary elements, not enlarging primary ones.** Lighten
  gridlines. Thin axis lines. Shrink legends. A quiet context makes the signal obvious.
- **Bring elements that need comparison close together.** Comparison accuracy degrades rapidly
  with distance. If the viewer must hold a value in working memory, the layout is failing.

### Color — OpenColors palette, never the sole differentiator

- **Use the OpenColors palette for all visualizations.** Categorical: oc-blue-7, oc-orange-7,
  oc-teal-7, oc-red-7, oc-grape-7, oc-cyan-7, oc-lime-7, oc-pink-7. Sequential: single-hue
  light-to-dark. Diverging: two hues meeting at oc-gray-3.
- **Never rely on color alone.** Pair hue with shape, pattern, position, or direct labels.
  8% of males have red-green color vision deficiency.
- **Avoid red-green pairs.** Blue and orange are safe across nearly all deficiency types.
- **Reserve saturated color for what demands immediate attention.** One saturated element in a
  field of muted tones commands the eye.
- **Keep one color meaning consistent across all panels.** If "actual" is oc-blue-7 in one
  chart, it must be oc-blue-7 everywhere.
- **Meet WCAG AA contrast: 4.5:1 for text, 3:1 for graphical objects.** The minimum passing
  gray on white is #767676.

### Narrative — put the insight in the title

- **Titles state the takeaway, not the topic.** "Northeast drives 60% of revenue growth"
  communicates. "Revenue by Region" does not. The title is the most-read element.
- **Use the subtitle for context.** Time range, data source, scope. The subtitle is where
  "Monthly Revenue, 2020-2024" belongs — as supporting detail under the actual insight.
- **Annotate insights, not features.** Highlight what the viewer would miss or misinterpret
  without guidance. "30% higher than 2019" communicates. "45%" does not.
- **Annotate external context that explains patterns.** A spike on March 2020 means nothing
  until annotated "COVID-19 lockdowns begin."
- **Show uncertainty honestly.** Dash projected lines. Add confidence bands. Distinguish
  historical from forecast. A clean line into the future presents false precision.

### Spacing — whitespace is structure

- **Generous margins around all charts.** The data is visually busy; surrounding space provides
  relief. Padding around text improves readability.
- **Tight spacing within groups, generous spacing between groups.** Proximity communicates
  hierarchy without labels or borders.
- **Isolate the most important element with whitespace.** Crowded elements compete. An element
  surrounded by space commands attention without changing the element itself.

### Simplicity — what earns its place

- **For every non-data element, ask: does this reveal data, explain data, or orient the reader?**
  If none, remove it.
- **Remove 3D effects from 2D data without exception.** Perspective distorts length, angle, and
  area simultaneously.
- **Gridlines should be barely visible.** If gridlines are darker than data marks, the hierarchy
  is inverted.
- **Highlight the important few, gray the unimportant many.** For more than 7 categories, pick
  3-5 that matter, color them, push the rest to oc-gray-4.
- **When aggregation hides distribution, show the distribution.** Means lie by omission. Add
  box plots, jittered points, or at minimum confidence intervals.

---

## Workflow

Six phases — research heavy, implementation light.

```
Think   →   Research   →   Build   →   Verify   →   Present   →   Save
           [checkpoint]                [MANDATORY     [checkpoint]
                ↑             ↑        2nd draft]         │
                └─────────────┴──── feedback loops ───────┘
```

| Phase | What happens | Reference |
|-------|-------------|-----------|
| 1. Think | Find the claim. Identify the viewer. Determine inference vs. recognition mode. Honesty check. | `references/phase-context.md` |
| 2. Research | Classify data (Q/O/N/T). Plan encoding. Select engine + template. Plan transforms. **User checkpoint.** | `references/phase-research.md` |
| 3. Build | Write spec/HTML. Apply encoding, composition, narrative, interaction, accessibility. | `references/phase-implement.md` |
| 4. Verify | **Mandatory second draft.** Structural verification (read back HTML). Visual verification (open in Chrome, read screenshot). Both must agree. Apply `/frontend-design` for style pass. Fix and re-verify. | `references/phase-refine.md` |
| 5. Present | Output final HTML. Restate argument. **User checkpoint.** Route feedback to the right phase. | `references/phase-present.md` |
| 6. Save | Persist to `${CLAUDE_PROJECT_DIR}/.claude/visualizations/viz-<timestamp>.html`. Optionally register via CLI. | `references/phase-present.md` |

Feedback routing: "change chart type" → Phase 2. "fix layout" → Phase 3. "something feels off" → Phase 4.

### Phase 4 Verification Protocol (mandatory)

Every visualization goes through two verification paths in parallel:

1. **Structural:** Read back the generated HTML. Verify the Vega spec or D3 code is syntactically
   correct. Check that data fields match the encoding. Verify units on axes. Verify OpenColors palette.
2. **Visual:** Run `open -a "Google Chrome" <file>`. Read the screenshot. Inspect the rendered
   output for: correct chart type, readable labels, appropriate spacing, working tooltips,
   color contrast, overall clarity.

Both paths must agree the chart is correct. If they disagree, fix and re-verify. Only proceed
to Phase 5 after the second draft passes both checks.

---

## Engine Selection

Two data-viz engines. Default to Vega. Use D3 when you need full DOM control.

```
What are you visualizing?
├── Data (quantitative/categorical)
│   ├── Default → Vega (.vg.json spec in wrapper HTML)
│   └── Needs full DOM control, custom keyboard nav, or sankey? → D3 (standalone HTML)
├── Process/flow/structure → [Mermaid — future]
└── Network topology only  → [Graphviz — future]
```

**Vega** is declarative JSON. It handles bar, line, scatter, area, pie, histogram, box plot,
violin, heatmap, bubble, treemap, sunburst, choropleth, force graph, tree diagram, candlestick,
and more via transforms. Use it for everything unless you need D3.

**D3** is imperative JavaScript. It gives full control over the DOM. Use it when Vega can't
express what you need (sankey), or when you need full keyboard navigation and ARIA support
that Vega's SVG renderer doesn't provide.

Every chart type has templates in both engines. Load `references/engine-selection.md` for the
full capability matrix and decision criteria.

---

## Templates

25 Vega specs + D3 templates across 8 categories in `assets/vega/templates/` and `assets/d3/templates/`.

| Category | Charts | Engine |
|----------|--------|--------|
| Comparisons | bar, grouped-bar, stacked-bar, dot-plot, dumbbell | Vega + D3 |
| Compositions | pie, sunburst, treemap, waffle | Vega + D3 |
| Distributions | histogram, box-plot, violin-plot | Vega + D3 |
| Geographic | choropleth | Vega + D3 |
| Hierarchical | tree-diagram | Vega + D3 |
| Networks | force-graph, sankey | Vega + D3 |
| Relationships | scatter-plot, heatmap, bubble-chart, parallel-coords, radar | Vega + D3 |
| Temporal | line-chart, area-chart, candlestick, slope, sparkline | Vega + D3 |

Load `references/template-selection.md` for the decision tree from question type → template.

### Custom Template Workflow

For chart types not in the template library (chord diagram, streamgraph, etc.):

1. Confirm no existing template covers it
2. Craft using `references/base-vega-wrapper.md` (Vega) or `references/base-template.md` (D3)
3. Requirements: browser-runnable, CDN dependencies, OpenColors, 4.5:1 contrast, data table
   fallback, responsive sizing, units on all axes, sample data embedded

---

## Anti-Patterns

These are positioned here — before implementation references — so they are loaded when decisions
are being made, not after.

| Do Not | The Problem | Do Instead |
|--------|-------------|------------|
| Rainbow colormaps | No perceptual order; false boundaries; colorblind-hostile | Sequential single-hue or diverging (OpenColors) |
| 3D charts for 2D data | Distorts length, angle, area simultaneously | 2D with opacity or faceting |
| Pie charts with >5 slices | Angle comparison is inaccurate beyond 5 | Bar chart; length encodes more accurately |
| Truncated y-axis on bars | Non-zero baseline makes 5% look like 300% | Start at zero; use dot plot if differences are small |
| Color as sole differentiator | 8% of males are red-green colorblind | Pair with shape, pattern, or direct label |
| Dual y-axes | Any correlation can be manufactured by adjusting scales | Two stacked panels with shared x-axis |
| Lines connecting categorical points | Lines imply continuity between unordered items | Use bars or dots for categorical data |
| Alphabetical category sorting | Turns visual pattern into noise | Sort by value |
| Averages without distribution | Hides the shape of the data | Add box plot, jitter, or confidence interval |
| Cherry-picked time windows | Supports narrative by hiding contradicting history | Show full history; zoom with inset if needed |

---

## Signal Detection → Phase Routing

| User signal | Route to |
|-------------|----------|
| "visualize this", "create a chart", "make a graph", "show me" | Phase 1 (full workflow) |
| "what chart type", "bar vs line", "how should I represent" | Phase 2 |
| "layout", "arrange", "hierarchy", "whitespace", "grid" | Phase 3: compose |
| "annotate", "title", "label", "story", "explain" | Phase 3: narrate |
| "accessible", "WCAG", "colorblind", "screen reader" | Phase 3: access |
| "interactive", "filter", "zoom", "hover", "brush" | Phase 3: interact |
| "improve", "refine", "simplify", "what's wrong" | Phase 4 |
| "network", "nodes", "force-directed", "graph" | Phase 2 + `network-patterns.md` |
| "large dataset", "performance", "100k+", "millions" | Phase 2 + `canvas-patterns.md` |

When entering at a specific phase, verify prerequisites exist (argument, encoding plan, draft
HTML). If missing, gather through focused questions — do not run earlier phases in full.

---

## Browser-Runnable Output

**Vega charts:** Copy `assets/vega/wrapper.html`, inject the `.vg.json` spec. The wrapper loads
Vega from CDN, renders via `vegaEmbed`, and auto-generates an accessibility data table.
See `references/base-vega-wrapper.md`.

**D3 charts:** Generate standalone HTML with ESM imports from CDN.
See `references/base-template.md`.

Both paths produce a single `.html` file that opens directly in any browser.

### Persisting

Save to `${CLAUDE_PROJECT_DIR}/.claude/visualizations/viz-<timestamp>.html`. If Python 3 is
available, register with `python3 scripts/visualizer.py create --file <path>` for organized
storage.

---

## References

Load these conditionally — never load more than one pattern doc at a time.

**Phase guides** (load at phase entry):

| Phase | Reference |
|-------|-----------|
| Think | `references/phase-context.md` |
| Research | `references/phase-research.md` |
| Build | `references/phase-implement.md` |
| Verify | `references/phase-refine.md` |
| Present + Save | `references/phase-present.md` |

**Mode guides** (load during Build phase, one at a time):

| Mode | Reference | When to load |
|------|-----------|-------------|
| Encode | `references/mode-encode.md` | Writing scales, marks, channels |
| Compose | `references/mode-compose.md` | Arranging layout, hierarchy, spacing |
| Narrate | `references/mode-narrate.md` | Adding titles, annotations, story |
| Access | `references/mode-access.md` | ARIA, keyboard nav, color access |
| Interact | `references/mode-interact.md` | Tooltips, brushing, filtering |
| Refine | `references/mode-refine.md` | Auditing and fixing issues |

**Pattern docs** (load ONE based on engine choice):

| Engine | Reference |
|--------|-----------|
| Vega | `references/vega-patterns.md` |
| D3 | `references/d3-patterns.md` |

**Specialized** (load only when relevant):

| Topic | Reference |
|-------|-----------|
| Engine + template selection | `references/engine-selection.md`, `references/template-selection.md` |
| Vega/D3 HTML scaffolding | `references/base-vega-wrapper.md`, `references/base-template.md` |
| Data transforms | `references/data-preparation.md` |
| Networks | `references/network-patterns.md` |
| Large datasets (Canvas) | `references/canvas-patterns.md` |
