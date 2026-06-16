# Authoring a D3 Fragment

> **Scope:** This reference covers the D3 fragment structure. For Vega fragments, see [base-vega-wrapper.md](base-vega-wrapper.md). The two share one wrapper and one assembler; they differ only in what the chart code does.

A D3 chart is a fragment: a single `.frag.html` file holding one chart's drawing code, styles, and accessibility wiring. The shared assembler at `scripts/build_viz.py` injects each fragment into the one engine-agnostic wrapper, supplies the OpenColors theme and the shared helpers, and scopes the chart to its own instance so several fragments can share one page without colliding. D3 fragments live under `assets/d3/fragments/<category>/<name>.frag.html`. Verify D3 CDN imports and API usage against the current D3 documentation before deploying.

Reach for D3 when the chart needs something Vega cannot give: a mark a reader can focus and step through from the keyboard, an `aria-label` and a list role on every data point, a hover or filter or brush or drag interaction, or a structural layout like a sankey. That is the line the engine criteria draw in [engine-selection.md](engine-selection.md), and it is the reason a D3 fragment carries more code than its Vega counterpart.

## Fragment Structure

A fragment is a sequence of named sections, each introduced by an HTML comment marker. The assembler reads the markers and places each section in the right slot of the wrapper.

| Section | What it holds |
|---|---|
| `frontmatter` | The metadata block: `name`, `description`, `chart-type`, `engine`. |
| `title` | The headline sentence, the chart's argument in words. |
| `subtitle` | The supporting line under the title: what is measured, over what range, in what units. |
| `chart-css` | Styles for this chart, every selector prefixed with `.viz` so the rules reach only this instance. |
| `mount` | The SVG element the chart draws into, carrying its `<title>` and `<desc>`. |
| `helpers` | The shared helpers this chart needs. A D3 chart usually asks for `tooltip, a11y, data-table`. |
| `chart-js` | The data, scales, axes, marks, and interaction code. |

The `engine` frontmatter field reads `d3`. It tells the assembler to inject the D3 import.

## How the Chart Reaches the Page

The assembler injects `import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm"` ahead of the chart code, pinned to the D3 major version. It also opens the chart code with three names already in scope: `root` (this instance's container element), `uid` (this instance's unique id), and `VizHelpers` (the shared helper object). Never redeclare `root` or `uid` inside the chart code; the assembler has already declared them, and a second `const root` is a syntax error that no static check catches until the page fails to run. When a hierarchy layout needs a root node, name it something else, `hierarchyRoot` for instance.

Select into the page through `root`, never through a document-wide id:

```js
const svg = d3.select(root.querySelector("svg"))
  .attr("viewBox", `0 0 ${width} ${height}`)
  .attr("width", "100%");
```

The same fragment may appear more than once in a composed document. A `d3.select("#chart")` would bind every copy to the first match; `root.querySelector("svg")` reaches only this instance. The shared helpers follow the same rule: each takes `root` as its first argument.

## The Mount

The mount section is the SVG, and it carries the chart's accessibility identity. The `{{uid}}` token expands to this instance's id at assembly, so the `<title>` and `<desc>` ids stay unique even when the chart is composed alongside others:

```html
<svg role="list" aria-labelledby="{{uid}}-title {{uid}}-desc">
  <title id="{{uid}}-title">Electronics leads product sales at $42.5K</title>
  <desc id="{{uid}}-desc">
    Bar chart comparing product sales across six retail categories. Electronics
    leads at $42,500, followed by Clothing at $38,200.
  </desc>
</svg>
```

The `role="list"` on the SVG, paired with `role="listitem"` on each mark, lets a screen reader announce "list of six bars" and move between them. Write a real sentence in `<desc>`, the same argument the headline makes, so a listener who never sees the chart still learns what it shows.

## The Single Theme Source

Color comes from one place: the OpenColors tokens in `theme.css`, which the assembler parses into `VizHelpers.tokens`. Read them at the top of the chart code rather than hard-coding hex or reaching for a D3 scheme:

```js
const t = VizHelpers.tokens;
const colors = [t["oc-blue-7"], t["oc-orange-8"], t["oc-teal-7"], t["oc-red-7"]];
```

Because every color traces back to `theme.css`, a palette edit there reaches every chart on the next assembly. Styles in `chart-css` read the same tokens through CSS custom properties, for example `fill: var(--oc-gray-6)`.

## Marks, Accessibility, and Interaction

Bind data with `.join()` rather than appending inside a loop, and give every mark the attributes a keyboard and a screen reader need:

```js
const bars = g.selectAll(".bar").data(data).join("rect")
  .attr("class", "bar")
  // … position and size …
  .attr("fill", (d) => colorScale(d.category))
  .attr("tabindex", 0)
  .attr("role", "listitem")
  .attr("aria-label", (d) => `${d.category}: $${d3.format(",.0f")(d.value)}`);
```

Wire interaction through the shared helpers so behavior stays consistent across charts and scoped to this instance:

- `VizHelpers.showTooltip(root, event, html)` and `VizHelpers.hideTooltip(root)` drive the tooltip that the `tooltip` helper provides. Call them from both pointer events and focus events, so a keyboard reader sees the same detail a mouse reader does.
- `VizHelpers.navigateMarks(root, prevKey, nextKey)` makes the focusable marks reachable with arrow keys. Pass the keys that suit the chart's axis, `"ArrowLeft"` and `"ArrowRight"` for a horizontal sequence. When a chart groups marks into independent sets and arrow keys should stay within a set, keep a per-set `keydown` handler instead, scoped to `root`.
- `VizHelpers.renderDataTable(root, rows, headers)` builds the collapsed `<details>` table that carries the data when the marks cannot.

## Responsiveness

Size the SVG with a `viewBox` and a percentage width, never with fixed pixel `width` and `height` attributes. The chart then scales to its container, on a slide or in a composed dashboard panel alike. Follow the D3 margin convention: `margin`, `width`, and `height` constants, with the inner group translated by the left and top margins.

## What the Render Checker Enforces

`scripts/check_render.py` reads the assembled D3 output and reports defects before the chart opens. It expects the `<title>` and `<desc>` pair, the data-table fallback, and keyboard wiring on interactive marks; a chart whose marks respond to the pointer but offer no key handler is flagged, because the interaction should work without a mouse. Run the checker over the assembled example as the last step before presenting.

## Composing Several Charts

To place more than one chart on a page, assemble the fragments together:

```bash
python3 scripts/build_viz.py --compose <frag-a> <frag-b> --out dashboard.html
```

Each fragment becomes its own `<section>` with a unique id, its styles confined to that section, its scripts scoped to its own `root`. The fragments may mix engines freely; a D3 chart and a Vega chart sit side by side in one document with no shared globals and no id clashes.

## Required Patterns

- **Scope through `root`** — `root.querySelector(...)`, never `document.getElementById` or a global id selector.
- **Never redeclare `root` or `uid`** — the assembler supplies them; name a hierarchy root `hierarchyRoot`.
- **OpenColors tokens** — read color from `VizHelpers.tokens` and `var(--oc-…)`, not `d3.schemeTableau10` or hard-coded hex.
- **Per-mark accessibility** — `tabindex`, `role="listitem"`, and `aria-label` on every data mark, under a `role="list"` SVG.
- **Keyboard parity** — every pointer interaction has a focus equivalent, via the shared helpers.
- **`viewBox` responsiveness** — no fixed `width`/`height` on the SVG.
- **`.join()` for data binding** — not `.append()` in a loop.

## See Also

- **[base-vega-wrapper.md](base-vega-wrapper.md)** — authoring a Vega fragment, for static charts where conciseness wins and the data table carries the accessible floor.
- **[engine-selection.md](engine-selection.md)** — the criteria that decide D3 against Vega against Markdown.

## Sources

- D3 documentation — <https://d3js.org/getting-started>
- D3 API Reference — <https://github.com/d3/d3/blob/main/API.md>
- SVG Accessibility API Mappings — <https://www.w3.org/TR/svg-aam-1.0/>
