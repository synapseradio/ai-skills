---
name: visualize
description: 'Visualize data, concepts, relations, or diagrams. Produces browser-runnable HTML charts
  and markdown outputs that drop into pull requests, READMEs, tickets, and chat. Use whenever the
  user asks to visualize anything, make a chart or diagram, plot a trend, compare numbers, show a
  flow or timeline, or pick the right chart type.

  '
---

# Visualize

Create data visualizations for the surface where they will actually be read.
Three engines:

- **Markdown** — `.md` files (or `.html` with mermaid.js bundled) that render
  inside pull requests, READMEs, tickets, Notion, Slack, wiki posts.
- **Vega** — declarative JSON specs rendered in a standalone HTML wrapper.
  Concise and auditable; selected for standard static browser charts.
- **D3** — imperative JavaScript with full DOM control, keyboard navigation,
  and ARIA on individual marks. Selected when the user needs custom interactivity
  or a chart only D3 can express (sankey).

Every browser output is a single self-contained HTML file — assembled from one
shared wrapper plus a chart fragment — that runs with no server and no dependencies
beyond CDN.

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

- **Use the OpenColors palette for all visualizations.** Categorical: oc-blue-7, oc-orange-8,
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

Before phase 1, write down the six phases below as a checklist and mark each one off as you finish it, so progress stays visible through the workflow.

| Phase | What happens | Reference |
|-------|-------------|-----------|
| 1. Think | Find the claim. Identify the viewer. Determine inference vs. recognition mode. Honesty check. | [phase-context.md](references/phase-context.md) |
| 2. Research | Classify data (Q/O/N/T). Plan encoding. Select engine + template. Plan transforms. **User checkpoint.** | [phase-research.md](references/phase-research.md) |
| 3. Build | Write spec/HTML. Apply encoding, composition, narrative, interaction, accessibility. | [phase-implement.md](references/phase-implement.md) |
| 4. Verify | **Mandatory second draft.** Two render-free passes that must agree: structural read-back of the source, and render inference (predict the rendered result from the source — overflow, label collision, baselines, wiring, scroll containment, keyboard wiring). Run a style pass against the Core Principles (composition, color, spacing, simplicity). Fix and re-verify. | [phase-refine.md](references/phase-refine.md) |
| 5. Present | Output final HTML. Restate argument. **User checkpoint.** Route feedback to the right phase. | [phase-present.md](references/phase-present.md) |
| 6. Save | Persist to the location the Persisting section names for this harness. Optionally register via CLI. | [phase-present.md](references/phase-present.md) |

Feedback routing: "change chart type" → Phase 2. "fix layout" → Phase 3. "something feels off" → Phase 4.

### Phase 4 Verification Protocol (mandatory)

The verification protocol depends on the engine.

**HTML output (Vega, D3, mermaid-html).** Two render-free passes must agree.
Neither opens a browser or captures the screen — both read the source:

1. **Structural read-back:** Read the generated source. Verify the Vega spec or
   D3 code is syntactically correct (JSON well-formed; no JavaScript syntax
   errors). Check that encoding fields match the bound data. Verify units on axes
   and tooltips. Verify the OpenColors palette.
2. **Render inference:** Predict what the source will draw, without running it.
   Reason from the source about: overflow and clipping (mark and label extents
   against the declared `width`/`height`/viewBox and margins), label collision
   (tick count times estimated label length against the available axis span),
   axis domain and zero baseline on length encodings, encoding fields
   cross-checked against the data rows, declared mark count against data length,
   the legend wired to the same field and scale as the series, engine wiring (the
   required CDN scripts and the render call are present), scroll containment (no
   wheel or zoom handler and no `overflow`/`100vh` that lets the chart capture the
   page's scroll), and keyboard-interaction wiring (interactive marks carry
   `tabindex`, key handlers, and focus styles). For mermaid-html, confirm the
   diagram source is a recognized type and the mermaid.js wiring and render call
   are present.

**Markdown output (`.md`).** The same two render-free passes apply, adapted to
the surface:

1. **Structural read-back.** Confirm frontmatter complete, units present on
   every numeric column or bar, sort order matches the value being compared,
   source line present.
2. **Render inference.** If the output contains a ```` ```mermaid ```` block,
   confirm the diagram source is a recognized type with balanced structure and
   labels short enough for the target column width. If the output is plain text
   (unicode bars, tables, ascii tree), confirm character alignment holds by
   reasoning about column widths against the monospace assumption of the
   destination surface.

Both passes must agree the artifact is correct. If they disagree, fix and
re-verify. Only proceed to Phase 5 after the second draft passes the
appropriate checks. The full markdown checklist lives in
[markdown-patterns.md](references/markdown-patterns.md).

**Optional accelerator (never a gate).** A stdlib-only static-analysis script can
mechanically flag render-blocking defects across all three engines:

```bash
python3 scripts/check_render.py <path> [<path> ...]
```

It prints each defect with file and cause and exits non-zero when it finds one. It
accelerates the render-inference pass; it does not replace it and never blocks
presenting. If Python is unavailable, the script is absent, or it errors, the prose
passes stand on their own and verification proceeds unchanged.

---

## Engine Selection

There is no default engine. Markdown/mermaid, Vega, and D3 are weighed as equals,
and a stated criterion selects one. Evaluate the criteria in order; the first that
fires decides, and you name the criterion that decided.

```
No default. Reason over all three; the first criterion that fires selects.

1. Content type     process / flow / sequence / gantt?        → Markdown (mermaid),
                    (mermaid emits standalone HTML, so this      even for a browser
                     holds even for browser surfaces)            surface
2. Render surface   markdown-only surface (PR, README,         → Markdown
                    ticket, Notion, Slack, *.md)?
3. Capability       needs something only one engine has        → that engine
                    (sankey → D3)?
4. Interactivity    user asked to hover / filter / brush /     → D3
                    zoom / drag / keyboard-navigate marks?
5. Conciseness      none of the above; standard static chart   → Vega
                    for a browser → declarative is less code,    (a stated criterion,
                    fewer bugs, easier to audit                   not a fallthrough)

If interactivity is ambiguous, do not guess and do not let criterion 5 pick
silently — ask the user, in their terms:
   "Hover over the points or filter the data yourself, or is a static picture
    enough?"   hover/filter → D3 (4);  static → Vega (5)

Accessibility is a held-constant FLOOR, never a criterion: every engine meets the
same floor (data-table fallback, SVG title/desc, redundant encoding). Where
interaction exists, criterion 4 already routes to D3.
```

**Markdown** is for surfaces that render markdown (and sometimes mermaid) but
not arbitrary HTML — pull requests, READMEs, tickets, Notion pages, Slack posts,
wiki articles — and it owns the only flow/sequence/gantt templates (criterion 1).
Read [markdown-patterns.md](references/markdown-patterns.md) for the surface
matrix, the honesty checklist, and the Phase 4 verification checklist (markdown
variant).

**Vega** is declarative JSON. It handles bar, line, scatter, area, pie,
histogram, box plot, violin, heatmap, bubble, treemap, sunburst, choropleth,
force graph, tree diagram, candlestick, and more via transforms. Selected by the
conciseness criterion for a standard static browser chart.

**D3** is imperative JavaScript with full DOM control. Selected when the user
needs custom interactivity (hover, filter, brush, drag, per-mark keyboard
navigation) or a chart only D3 can express (sankey).

Read [engine-selection.md](references/engine-selection.md) for the full criteria
detail, the capability matrix, and the chart-type-to-template mapping across all
three engines.

---

## Templates

25 Vega specs + 26 D3 templates + 9 Markdown templates in
`assets/vega/templates/`, `assets/d3/templates/`, `assets/markdown/templates/`.

| Category      | Charts                                                    | Engines                |
| ------------- | --------------------------------------------------------- | ---------------------- |
| Comparisons   | bar, grouped-bar, stacked-bar, dot-plot, dumbbell         | Vega + D3 + Markdown   |
| Compositions  | pie, sunburst, treemap, waffle                            | Vega + D3 + Markdown   |
| Distributions | histogram, box-plot, violin-plot                          | Vega + D3              |
| Geographic    | choropleth                                                | Vega + D3              |
| Hierarchical  | tree-diagram                                              | Vega + D3 + Markdown (ascii-tree) |
| Networks      | force-graph, sankey                                       | Vega + D3 (sankey D3-only) |
| Process/flow  | flowchart, sequence, gantt                                | Markdown only          |
| Relationships | scatter-plot, heatmap, bubble-chart, parallel-coords, radar | Vega + D3 (+ Markdown for heatmap) |
| Temporal      | line-chart, area-chart, candlestick, slope, sparkline     | Vega + D3 + Markdown (sparkline-row) |

Load [template-selection.md](references/template-selection.md) for the decision
tree from question type → template.

### Custom Template Workflow

For chart types not in the template library (chord diagram, streamgraph, etc.):

1. Confirm no existing template covers it
2. Craft using [base-vega-wrapper.md](references/base-vega-wrapper.md) (Vega) or [base-template.md](references/base-template.md) (D3)
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
| "network", "nodes", "force-directed", "graph" | Phase 2 + [network-patterns.md](references/network-patterns.md) |
| "large dataset", "performance", "100k+", "millions" | Phase 2 + [canvas-patterns.md](references/canvas-patterns.md) |

When entering at a specific phase, verify prerequisites exist (argument, encoding plan, draft
HTML). If missing, gather through focused questions — do not run earlier phases in full.

---

## Producing the Final Output

Every browser chart — Vega, D3, or mermaid — is a **fragment** assembled into one
self-contained HTML file by a single engine-agnostic wrapper. The fragment carries
only the chart (its mount, its scoped CSS, its draw or embed script); the shared
`assets/_shared/wrapper.html` supplies the page chrome, the one OpenColors theme,
and the shared helpers, injected once.

**A ready-to-use single-chart example** is generated for every chart at
`assets/<engine>/templates/<category>/<name>.html`. Open or copy one, edit the data
and labels, and it is the final artifact. Each is built by `scripts/build_viz.py`
from the wrapper plus the fragment in `assets/<engine>/fragments/`.

**To put several charts in one page**, assemble multiple fragments into the one
wrapper. They are per-instance scoped, so their ids, styles, globals, and scroll
never collide:

```bash
python3 scripts/build_viz.py --compose <frag-a> <frag-b> --out combined.html
```

**To change the shared scaffold** (the OpenColors theme, the page chrome, the
accessibility helpers), edit `assets/_shared/` and run
`python3 scripts/build_viz.py --all` to regenerate every example. The build tree is
the single formatter of record for those files — never hand-edit a generated
`templates/*.html`.

**Markdown-surface output (`.md`):** for a markdown surface (PR, README, ticket),
copy the matching `assets/markdown/templates/<name>.md.tmpl`; its fenced
```` ```mermaid ```` blocks render inline on GitHub, GitLab, and Notion. Replace
the example data and update the title to state the takeaway. See
[markdown-patterns.md](references/markdown-patterns.md).

### Persisting

The save target depends on the harness:

- **A harness with an `artifacts` tool:** emit the visualization as an
  artifact. Use MIME type `text/html` for Vega, D3, and mermaid-html outputs;
  use `text/markdown` for markdown engine `.md` outputs. The artifact title
  is the visualization's `name`. No filesystem write is required.
- **A harness with shell and file-write tools:** save to
  `~/.visualizations/<slug>-<YYYYMMDD-HHMMSS>.<ext>`, where `<ext>` is `html`
  for browser-runnable charts and `md` for markdown engine `.md` outputs.
  Create `~/.visualizations/` if missing. For `.html` outputs, open in the
  default browser (`open` on macOS, `xdg-open` on Linux, `start` on Windows).
  For `.md` outputs, print the path — do not auto-open since markdown
  preview varies by environment.
- **Other harnesses:** print the artifact in a fenced code block and
  instruct the user to copy.

Optionally call `python3 scripts/visualizer.py create --file <path>` after a
filesystem write to register the artifact for `list` / `search` / `show`. The
CLI reads HTML and markdown frontmatter from the same flat
`~/.visualizations/` root.

---

## References

These are not optional background reading. Each phase and each Build subtask is
gated on the reference named here: you read it at the point of need and produce the
gate output that proves you read it (the gate outputs are defined in
[phase-implement.md](references/phase-implement.md)). The principles inlined above
tell you WHAT; these references tell you HOW; skipping one leaves a visible hole in
the gate output. For the pattern docs, read the one matching your chosen engine and
not the others.

**Phase guides** (read on entering each phase; the phase's output is the proof):

| Phase | Reference |
|-------|-----------|
| Think | [phase-context.md](references/phase-context.md) |
| Research | [phase-research.md](references/phase-research.md) |
| Build | [phase-implement.md](references/phase-implement.md) |
| Verify | [phase-refine.md](references/phase-refine.md) |
| Present + Save | [phase-present.md](references/phase-present.md) |

**Build-phase mode guides** (each Build subtask gates on its mode doc — read it to
produce that subtask's required output). The five Build modes are encode, compose,
narrate, interact, and access. Refine is not a Build mode; it is the Verify phase
(see below).

| Mode | Reference | Gates the subtask |
|------|-----------|-------------------|
| Encode | [mode-encode.md](references/mode-encode.md) | Writing scales, marks, channels |
| Compose | [mode-compose.md](references/mode-compose.md) | Arranging layout, hierarchy, spacing |
| Narrate | [mode-narrate.md](references/mode-narrate.md) | Adding titles, annotations, story |
| Access | [mode-access.md](references/mode-access.md) | ARIA, keyboard nav, color access |
| Interact | [mode-interact.md](references/mode-interact.md) | Tooltips, brushing, filtering |

Refine ([mode-refine.md](references/mode-refine.md)) is the audit loaded by the
Verify phase ([phase-refine.md](references/phase-refine.md)), not a Build-phase mode.

**Pattern docs** (read the one matching your chosen engine):

| Engine | Reference |
|--------|-----------|
| Markdown | [markdown-patterns.md](references/markdown-patterns.md) |
| Vega | [vega-patterns.md](references/vega-patterns.md) |
| D3 | [d3-patterns.md](references/d3-patterns.md) |

**Specialized** (read when the topic applies):

| Topic | Reference |
|-------|-----------|
| Engine selection | [engine-selection.md](references/engine-selection.md) |
| Template selection | [template-selection.md](references/template-selection.md) |
| Authoring a Vega fragment | [base-vega-wrapper.md](references/base-vega-wrapper.md) |
| Authoring a D3 fragment | [base-template.md](references/base-template.md) |
| Data transforms | [data-preparation.md](references/data-preparation.md) |
| Networks | [network-patterns.md](references/network-patterns.md) |
| Large datasets (Canvas) | [canvas-patterns.md](references/canvas-patterns.md) |
