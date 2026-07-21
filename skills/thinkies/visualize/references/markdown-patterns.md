# Markdown Patterns

Many real consumers of a visualization render markdown but not arbitrary HTML — pull
requests, READMEs, tickets, Slack messages, Notion pages, wiki posts. The markdown
engine emits a `.md` file (or, for diagrams that need SVG, an `.html` file with
mermaid.js bundled) that lands cleanly on those surfaces.

## When to use the markdown engine

Use it whenever the rendering target is a markdown surface, not a browser. Concrete
signals from the user:

- "for the README", "for the PR description", "in the ticket", "for the wiki"
- "in markdown", "as a markdown table", "as a code block"
- "make a diagram for the GitHub issue"
- "post this to Slack"
- the destination is a `.md` file path

If the destination is `file://path.html`, a Chrome window, a dashboard, or a
standalone deliverable, use Vega or D3 instead — the markdown engine cannot show
SVG-quality charts.

## Rendering-target matrix

The most important question for a markdown output is whether the target surface
auto-renders mermaid (and other formats). When in doubt, default to plain-text-safe
techniques.

| Surface              | GFM tables | Mermaid in `.md` | Notes |
| -------------------- | ---------- | ---------------- | ----- |
| GitHub (issues, PRs, READMEs) | Yes        | Yes              | Mermaid renders inline.  |
| GitLab               | Yes        | Yes              | Mermaid since 10.3. |
| Notion               | Yes        | Yes              | Mermaid since 2024. |
| Obsidian             | Yes        | Yes              | Built-in mermaid plugin. |
| VS Code Markdown Preview | Yes    | Yes (recent)     | Requires markdown-mermaid extension on older versions. |
| Confluence (wiki)    | Yes        | No               | Plugin-dependent; assume no. |
| Slack                | Partial (no nested tables) | No | No mermaid; degrade to ASCII or unicode bars. |
| Email (most clients) | Partial    | No               | Mermaid will appear as raw text. |
| Plain ticket / chat  | Sometimes  | No               | When unsure, use plain-text-safe formats. |
| `*.md` file rendered by ??? | depends | depends         | If the target is unknown, prefer plain-text-safe and HTML for mermaid. |

**Hard rule:** never emit a `.md` file containing a mermaid block to a surface that
does not auto-render mermaid. The user will see raw text. When in doubt, choose the
`.html` variant — it works wherever HTML opens, including a local browser.

## Template catalogue

Nine templates in `assets/markdown/templates/`. Six are markdown-only; three are
mermaid diagrams emitted in either format depending on the surface.

| Template            | `.md` | `.html` | Use when |
| ------------------- | :---: | :-----: | -------- |
| comparison-table    |   ✓   |   —     | Side-by-side rows with consistent columns |
| unicode-bar-chart   |   ✓   |   —     | Quantitative comparison; want a glanceable bar shape inline |
| ranked-list         |   ✓   |   —     | Top-N with deltas; safest fallback that always renders |
| sparkline-row       |   ✓   |   —     | Trend per metric; up to ~20 data points per row |
| emoji-heatmap       |   ✓   |   —     | Discrete categorical bins (3–5 levels); never continuous gradients |
| ascii-tree          |   ✓   |   —     | Hierarchy when mermaid is unavailable |
| mermaid-flowchart   |   ✓   |   ✓     | Process or decision flow |
| mermaid-sequence    |   ✓   |   ✓     | Inter-actor message sequences |
| mermaid-gantt       |   ✓   |   ✓     | Project timeline with dependencies |

## Plain-text-safe techniques

These work everywhere, including plain-text exports and screen readers.

### GFM tables

Use right-alignment for numeric columns (`---:`). Always include units in column
headers or as a trailing sentence.

```markdown
| Region    | Q1 ($K) | Q2 ($K) |
| --------- | ------: | ------: |
| Northeast |   1,245 |   1,302 |
| West      |   1,431 |   1,512 |
```

### Unicode bar characters

Eight steps from `▁` to `█` (`▁▂▃▄▅▆▇█`) and eight horizontal blocks
(`█▉▊▋▌▍▎▏`). Pair the bars with the underlying numeric value so readers don't
have to count blocks.

### Sparklines

Same eight-step scale used in a single line per series: `▁▂▃▄▅▆▇█`. Limit to
roughly 20 data points; longer rows compress until adjacent values merge.

### Emoji heatmaps

Use a discrete 3–5 step palette and label every step explicitly. Emoji colour
mapping is not a continuous gradient — readers cannot resolve fine differences,
so do not use this format for high-resolution magnitude comparisons. Discrete
bins only.

### ASCII trees

Use box-drawing characters (`├──`, `└──`, `│`) to make hierarchy visible. Pair
each node with a numeric label so the tree carries quantitative weight.

## Mermaid output

### When to emit `.md` vs `.html`

```
Does the surface auto-render mermaid?
├── Yes (GitHub, GitLab, Notion, Obsidian, recent VS Code) → emit `.md` with ```mermaid block
├── No  (Slack, email, generic chat, plain ticket)         → emit `.html` with mermaid.js
└── Unknown                                                → emit `.html` (works wherever HTML opens)
```

### Supported diagram types

Mermaid supports more than these three; the templated set focuses on the diagrams
most useful for software work:

- **flowchart** — process or decision flow.
- **sequenceDiagram** — message exchange between actors.
- **gantt** — project timeline with dependencies.

Other types (classDiagram, stateDiagram, erDiagram, journey, etc.) are valid
mermaid input. To use one, copy a templated `.html` variant and replace the
content of the `<pre class="mermaid">` block; everything else (CDN import,
initialization, noscript fallback) stays the same.

### HTML wrapper requirements

Every mermaid HTML output must include:

- `<pre class="mermaid">` block with the diagram source — `<pre>` preserves
  whitespace, which the mermaid parser depends on.
- `<noscript>` block describing the diagram in prose — readers without
  JavaScript still get the meaning.
- ESM import of mermaid: `import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";`
- the hardened `mermaid.initialize` below, applied by default — not the bare
  `{ startOnLoad: true }`.

### The hardened initialize

A bare `mermaid.initialize({ startOnLoad: true })` is the source of most one-shot
mermaid failures: long labels overflow their nodes, text renders too small, dense
flowcharts collide, and special characters wrap unpredictably. The skill applies
this configuration by default instead. Its colors are OpenColors tokens (dark-gray
text and lines over light-gray fills for WCAG AA contrast); mermaid cannot read CSS
variables, so the hex values are inlined to match the shared theme.

```js
mermaid.initialize({
  startOnLoad: true,
  theme: "base",
  themeVariables: {
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
    fontSize: "15px",
    primaryColor: "#f1f3f5",
    primaryBorderColor: "#868e96",
    primaryTextColor: "#212529",
    lineColor: "#343a40",
    textColor: "#212529",
    mainBkg: "#f1f3f5",
    secondaryColor: "#e9ecef",
    tertiaryColor: "#f8f9fa",
    nodeBorder: "#868e96",
    clusterBkg: "#f8f9fa",
    clusterBorder: "#ced4da",
    edgeLabelBackground: "#f8f9fa",
  },
  flowchart: {
    htmlLabels: true,
    defaultRenderer: "dagre-wrapper",
    curve: "monotoneY",
    nodeSpacing: 70,
    rankSpacing: 100,
    padding: 34,
    useMaxWidth: true,
    diagramPadding: 16,
  },
  themeCSS: `
    .nodeLabel, .edgeLabel { white-space: normal; }
    .node .label { padding: 6px 10px; }
    .edgeLabel { padding: 2px 6px; }
  `,
});
```

The `flowchart` block is ignored for sequence and gantt diagrams, so one canonical
initialize stays correct for every diagram type. `securityLevel` is left unset
(strict default) — the templates have no `click` cross-links, and loosening the
security posture is a user decision, never a default.

### Setting → failure it prevents

| Setting | One-shot failure it prevents |
|---|---|
| `htmlLabels: true` + `themeCSS` `white-space: normal` | Long labels overflow or clip the node; this pair lets labels wrap inside the box |
| `useMaxWidth: true` | Diagram overflows the container width on narrow surfaces |
| `nodeSpacing` / `rankSpacing` / `diagramPadding` | Dense graphs collide; generous spacing keeps nodes and edges legible |
| `fontSize: "15px"` + `fontFamily` | Text renders too small or in an inconsistent face |
| `theme: "base"` + `themeVariables` | Default palette ignores the shared theme and can fail contrast |
| `.node .label` / `.edgeLabel` padding | Labels touch their borders; padding restores breathing room |

### Orientation: `TD`, not `LR`

Author flowcharts top-down (`flowchart TD`), not left-right (`flowchart LR`). `LR`
forces the diagram wide and shrinks labels unreadably on column-width surfaces — a
README, a PR, a ticket. A `.md` fenced ```` ```mermaid ```` block cannot carry an
init directive at all (and per-block `%%{init}%%` is disallowed here), so on that
surface only `TD` orientation and short labels are portable — the hardened config
applies to the `.html` form, where the initialize can run.

## Honesty checklist

- [ ] **Units** — every numeric value has a unit, either in the column header or
      adjacent to the value. Numbers without units are decoration.
- [ ] **Source** — every chart ends with a one-line source attribution naming the
      dataset and the date range it covers.
- [ ] **Bar baselines** — unicode bars start at zero; partial-block rendering
      represents proportional value.
- [ ] **Sort by value** — ranked lists, comparison tables, and bar charts are
      sorted by the value being compared, not alphabetically.
- [ ] **Show the underlying values** — every chart that renders a visual
      summary (unicode bars, sparklines, emoji grids) is paired with the raw
      values somewhere in the same artifact, either inline or in a "View
      data" table.
- [ ] **One claim per chart** — the title states the takeaway. If the chart
      needs a paragraph to explain, split it into two charts.

## Phase 4 verification (markdown variant)

After producing a markdown output, verify by reading it back and checking:

- [ ] Frontmatter present with all required fields (`name`, `description`,
      `chart-type`, `engine`, `project`, `created`)
- [ ] Title states the takeaway, not the topic
- [ ] Units present on all numeric columns / bars / labels
- [ ] Sort order matches the value being compared
- [ ] Source line present
- [ ] If the output is a `.md` with a ```` ```mermaid ```` block, confirm by
      reading the source that the diagram is a recognized type with balanced
      structure and labels short enough for the target column width
- [ ] If the output is `.html` with mermaid, confirm by reading the source that
      the mermaid.js import, the `mermaid.initialize` call, the
      `<pre class="mermaid">` source, and the `<noscript>` fallback are all
      present and the diagram source parses
- [ ] If the output is plain-text-safe, confirm character alignment holds by
      reasoning about column widths against the destination's monospace
      assumption

## Cross-references

- **Engine selection (Vega vs D3 vs Markdown)** — [engine-selection.md](engine-selection.md)
- **Template selection inside the markdown engine** — see the catalogue above
- **HTML wrapper for mermaid** — see `assets/markdown/templates/mermaid-flowchart.html.tmpl`
