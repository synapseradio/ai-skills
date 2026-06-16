# Engine Selection

Three engines: **Markdown** (text + mermaid for markdown surfaces), **Vega**
(declarative JSON), and **D3** (imperative JavaScript, full DOM control). They are
weighed as equals — there is no default. Architecture is extensible for future
engines (Graphviz, Plot, etc.).

## Criteria Among Equals — No Default

There is no default engine. Markdown/mermaid, Vega, and D3 start equal, and a
stated criterion selects one. Evaluate the criteria in order; the first that fires
decides, and you name the criterion that decided. If none fires, the chart is
servable by more than one engine — reason about the tradeoff, then ask the user
one question in their terms (below). Never fall through to a default.

1. **Content type.** Is it a process, flow, sequence, or timeline (gantt)?
   → **Markdown engine (mermaid).** Mermaid owns the only templates for these
   shapes, and it emits standalone HTML, so this holds even when the destination
   is a browser. Surface does not override content type here.
2. **Render surface.** Will it be read on a markdown-only surface (PR, README,
   ticket, Notion, Slack, a `.md` file) that cannot run arbitrary HTML?
   → **Markdown engine.** For a chart that needs SVG fidelity on such a surface,
   emit a Vega or D3 file separately and link to it from the markdown artifact.
3. **Structural capability.** Does the chart need something only one engine has —
   sankey (D3 only), or a transform/layout the others lack? → the engine that has it.
4. **Custom interactivity.** Has the user asked to hover, filter, brush, zoom,
   drag, or navigate marks by keyboard? → **D3.** It gives full DOM control,
   per-mark ARIA, and keyboard navigation that Vega's own SVG renderer cannot.
5. **Declarative conciseness.** If nothing above fired, the chart is a standard
   static quantitative chart for a browser. The deciding property is conciseness
   and auditability — a declarative spec is less code, fewer bugs, easier to read
   back → **Vega.** This is a stated criterion, reached only after 1–4 are
   considered and the chart is confirmed static and standard; it is not a
   catch-all default.

If criterion 4 is genuinely ambiguous — you cannot tell from the request whether
the user wants to explore the data or just see it — do not guess, and do not let
criterion 5 quietly pick. Reason about the tradeoff, then ask one question in the
user's own terms:

> "Do you want to hover over the points or filter the data yourself, or is a
> single static picture enough?"

A "hover or filter" answer selects D3 (criterion 4); a "static picture" answer
selects Vega (criterion 5). The question carries the context a non-expert needs to
answer it, and the answer — not a default — decides.

**Accessibility is a floor, not a criterion.** Every engine must meet the same
accessibility floor: a data-table fallback, SVG `<title>`/`<desc>`, and redundant
encoding that never relies on color alone. Accessibility never selects the engine.
Where interaction exists, criterion 4 already routes to D3, the engine with
per-mark keyboard navigation; where it does not, the floor is met on any engine
without steering the choice.

### Inside the Markdown engine

Once criterion 1 or 2 selects Markdown, two sub-decisions remain:

- **What is shown.** Quantitative values → comparison-table, unicode-bar-chart,
  ranked-list, sparkline-row, or emoji-heatmap. Process or structure →
  mermaid-flowchart, mermaid-sequence, mermaid-gantt, or ascii-tree.
- **Mermaid output format** — does the surface auto-render mermaid? Yes (GitHub,
  GitLab, Notion, Obsidian, recent VS Code) → emit `.md` with a ```` ```mermaid ````
  block. No (Slack, email, generic chat, plain ticket) → emit `.html` with
  mermaid.js. Unknown → emit `.html`, which works wherever HTML opens.

## When to Use Each Engine

**Markdown.** The surface only renders markdown (and maybe mermaid). Real
examples: pull request descriptions, READMEs, GitHub or Jira tickets, Notion
pages, Slack posts, wiki articles, plain text exports. The output is a `.md`
file or, for diagrams that need SVG, an `.html` file with mermaid.js bundled.
See [markdown-patterns.md](markdown-patterns.md) for the surface matrix and template catalogue.

**Vega.** Declarative JSON — less code, fewer bugs, easier to audit. Selected by
the conciseness criterion for a standard static browser chart once content type,
surface, structural capability, and interactivity have been ruled out. It handles
bar, line, scatter, area, pie, histogram, box plot, violin, heatmap, bubble,
treemap, sunburst, choropleth, force graph, tree diagram, candlestick, and more
through its transform and layout system.

**D3.** When you need full DOM control that Vega's SVG renderer cannot
provide. This means: sankey diagrams (no Vega transform exists), full
keyboard navigation of data points, ARIA roles on individual marks,
pixel-precise custom layouts, or very large datasets where Canvas 2D API is
needed.

## Capability Matrix

| Capability                                  | Markdown            | Vega                      | D3                        |
| ------------------------------------------- | ------------------- | ------------------------- | ------------------------- |
| Renders without JavaScript                  | Yes (plain text)    | No                        | No                        |
| Renders inside a markdown surface           | Yes                 | No                        | No                        |
| Quantitative comparison (≤10 items)         | Yes (unicode bars)  | Yes                       | Yes                       |
| Trend over time                             | Yes (sparklines, ≤20 pts) | Yes                 | Yes                       |
| Hierarchical layouts                        | ASCII tree          | Yes (transforms)          | Yes                       |
| Process / sequence / gantt                  | Yes (mermaid)       | No                        | No                        |
| Geographic projections                      | No                  | Yes                       | Yes                       |
| Sankey                                      | No                  | No                        | Yes (d3-sankey)           |
| Full keyboard navigation                    | N/A                 | No (renders own SVG)      | Yes                       |
| ARIA on individual marks                    | N/A                 | No                        | Yes                       |
| Custom animations                           | No                  | Limited (signal transitions) | Full control          |
| Declarative conciseness                     | Highest             | High                      | Low (imperative)          |

## Template Assignment

Every quantitative chart type has at least one path. Sankey is D3-only; the
markdown engine has its own short list focused on what works in plain text.

| Category              | Chart                  | Markdown                       | Vega                                                | D3                                              |
| --------------------- | ---------------------- | ------------------------------ | --------------------------------------------------- | ----------------------------------------------- |
| **Comparisons**       | bar chart              | unicode-bar-chart              | `assets/vega/fragments/comparisons/bar-chart.frag.html`     | `assets/d3/fragments/comparisons/bar-chart.frag.html`     |
|                       | grouped bar            | comparison-table               | `assets/vega/fragments/comparisons/grouped-bar.frag.html`   | `assets/d3/fragments/comparisons/grouped-bar.frag.html`   |
|                       | stacked bar            | comparison-table               | `assets/vega/fragments/comparisons/stacked-bar.frag.html`   | `assets/d3/fragments/comparisons/stacked-bar.frag.html`   |
|                       | dot plot               | ranked-list                    | `assets/vega/fragments/comparisons/dot-plot.frag.html`      | `assets/d3/fragments/comparisons/dot-plot.frag.html`      |
|                       | dumbbell               | comparison-table               | `assets/vega/fragments/comparisons/dumbbell-chart.frag.html`      | `assets/d3/fragments/comparisons/dumbbell-chart.frag.html` |
| **Compositions**      | pie chart              | comparison-table               | `assets/vega/fragments/compositions/pie-chart.frag.html`    | `assets/d3/fragments/compositions/pie-chart.frag.html`    |
|                       | sunburst               | ascii-tree                     | `assets/vega/fragments/compositions/sunburst.frag.html`     | `assets/d3/fragments/compositions/sunburst.frag.html`     |
|                       | treemap                | ascii-tree                     | `assets/vega/fragments/compositions/treemap.frag.html`      | `assets/d3/fragments/compositions/treemap.frag.html`      |
|                       | waffle                 | emoji-heatmap                  | `assets/vega/fragments/compositions/waffle-chart.frag.html`       | `assets/d3/fragments/compositions/waffle-chart.frag.html` |
| **Distributions**     | histogram              | unicode-bar-chart              | `assets/vega/fragments/distributions/histogram.frag.html`   | `assets/d3/fragments/distributions/histogram.frag.html`   |
|                       | box plot               | comparison-table               | `assets/vega/fragments/distributions/box-plot.frag.html`    | `assets/d3/fragments/distributions/box-plot.frag.html`    |
|                       | violin plot            | —                              | `assets/vega/fragments/distributions/violin-plot.frag.html` | `assets/d3/fragments/distributions/violin-plot.frag.html` |
| **Geographic**        | choropleth             | —                              | `assets/vega/fragments/geographic/choropleth.frag.html`     | `assets/d3/fragments/geographic/choropleth.frag.html`     |
| **Hierarchical**      | tree diagram           | ascii-tree                     | `assets/vega/fragments/hierarchical/tree-diagram.frag.html` | `assets/d3/fragments/hierarchical/tree-diagram.frag.html` |
| **Networks**          | force graph            | —                              | `assets/vega/fragments/networks/force-graph.frag.html`      | `assets/d3/fragments/networks/force-graph.frag.html`      |
|                       | sankey                 | —                              | —                                                   | `assets/d3/fragments/networks/sankey.frag.html`           |
| **Process / flow**    | flowchart              | mermaid-flowchart              | —                                                   | —                                               |
|                       | sequence diagram       | mermaid-sequence               | —                                                   | —                                               |
|                       | gantt                  | mermaid-gantt                  | —                                                   | —                                               |
| **Relationships**     | scatter plot           | —                              | `assets/vega/fragments/relationships/scatter-plot.frag.html` | `assets/d3/fragments/relationships/scatter-plot.frag.html` |
|                       | heatmap                | emoji-heatmap                  | `assets/vega/fragments/relationships/heatmap.frag.html`     | `assets/d3/fragments/relationships/heatmap.frag.html`     |
|                       | bubble chart           | —                              | `assets/vega/fragments/relationships/bubble-chart.frag.html` | `assets/d3/fragments/relationships/bubble-chart.frag.html` |
|                       | parallel coordinates   | —                              | `assets/vega/fragments/relationships/parallel-coordinates.frag.html` | `assets/d3/fragments/relationships/parallel-coordinates.frag.html` |
|                       | radar chart            | —                              | `assets/vega/fragments/relationships/radar-chart.frag.html`       | `assets/d3/fragments/relationships/radar-chart.frag.html` |
| **Temporal**          | line chart             | sparkline-row                  | `assets/vega/fragments/temporal/line-chart.frag.html`       | `assets/d3/fragments/temporal/line-chart.frag.html`       |
|                       | area chart             | sparkline-row                  | `assets/vega/fragments/temporal/area-chart.frag.html`       | `assets/d3/fragments/temporal/area-chart.frag.html`       |
|                       | candlestick            | —                              | `assets/vega/fragments/temporal/candlestick.frag.html`      | `assets/d3/fragments/temporal/candlestick.frag.html`      |
|                       | slope chart            | comparison-table               | `assets/vega/fragments/temporal/slope-chart.frag.html`      | `assets/d3/fragments/temporal/slope-chart.frag.html`      |
|                       | sparkline              | sparkline-row                  | `assets/vega/fragments/temporal/sparkline.frag.html`        | `assets/d3/fragments/temporal/sparkline.frag.html`        |

A dash means no template exists in that engine for that chart type. The
markdown engine intentionally does not cover every chart — for charts that
require pixel-precise rendering (choropleth, scatter, force graph, etc.), use
Vega or D3 even if the destination claims to be a markdown surface.

## Criteria Detail — Cases That Select a Specific Engine

These are the concrete situations behind criteria 3 and 4. None is an "override" —
there is no default to override. Each is a criterion firing.

- **Markdown surface, but the chart needs SVG fidelity.** Emit a Vega or D3
  visualization separately and link to it from the markdown artifact (criterion 2,
  with the SVG escape hatch).
- **Custom interactivity, including per-data-point keyboard navigation.** If the
  user needs to hover, filter, brush, drag, or operate individual marks by
  keyboard, use D3 — its per-mark ARIA and keyboard handling are what Vega's SVG
  renderer cannot provide (criterion 4). Keyboard navigation lives here, under
  interactivity, not under accessibility: the accessibility floor (data-table
  fallback, SVG `<title>`/`<desc>`, redundant encoding) is met on every engine and
  never selects one.
- **Performance.** Vega handles tens of thousands of points. For hundreds of
  thousands, use D3 with the Canvas 2D API (criterion 3). See [canvas-patterns.md](canvas-patterns.md).
- **Pixel-precise layout.** Infographic-style designs where exact placement matters
  → D3 (criterion 3).
- **Structural capability.** Sankey has no Vega transform → D3 (criterion 3).
