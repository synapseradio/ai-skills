# Authoring a Vega Fragment

A Vega chart is a fragment: a single `.frag.html` file holding one chart's spec, styles, and accessibility wiring. The shared assembler at `scripts/build_viz.py` injects each fragment into the one engine-agnostic wrapper, supplies the OpenColors theme and the shared helpers, and scopes the chart to its own instance so several fragments can share one page without colliding. Vega fragments live under `assets/vega/fragments/<category>/<name>.frag.html`. For D3 charts, see [base-template.md](base-template.md).

## Fragment Structure

A fragment is a sequence of named sections, each introduced by an HTML comment marker. The assembler reads the markers and places each section in the right slot of the wrapper.

| Section | What it holds |
|---|---|
| `frontmatter` | The metadata block: `name`, `description`, `chart-type`, `engine`. |
| `title` | The headline sentence, the chart's argument in words. |
| `subtitle` | The supporting line under the title: what is measured, over what range, in what units. |
| `chart-css` | Styles for this chart, every selector prefixed with `.viz` so the rules reach only this instance. |
| `mount` | The element Vega renders into, usually `<div class="vega-mount"></div>`. |
| `helpers` | The shared helpers this chart needs, named one per concern. A Vega chart asks for `data-table`. |
| `chart-js` | The Vega config, the spec, and the `vegaEmbed` call. |

The `engine` frontmatter field reads `vega`. It tells the assembler to inject the Vega-Embed import and tells downstream tooling which renderer the fragment expects.

## How the Spec Reaches the Page

The assembler injects `import vegaEmbed from "https://cdn.jsdelivr.net/npm/vega-embed@6/+esm"` ahead of the chart code, pinned to the Vega-Embed major version. Vega-Embed carries the Vega runtime and the Vega-Lite compiler with it, so a single import covers full Vega specs and Vega-Lite specs alike. The canonical fragments carry full Vega specs, identified by a `"$schema"` of `https://vega.github.io/schema/vega/v6.json`. If you would rather author in Vega-Lite, write a Vega-Lite spec instead and Vega-Embed compiles it before rendering; the rest of the fragment is unchanged.

Inside the `chart-js` section, the chart code runs with three names already in scope, supplied by the assembler: `root` (this instance's container element), `uid` (this instance's unique id), and `VizHelpers` (the shared helper object). Render into the mount by selecting through `root`:

```js
vegaEmbed(root.querySelector(".vega-mount"), spec, {
  renderer: "svg",
  config,
  actions: { export: true, source: false, compiled: false, editor: true },
});
```

Selecting through `root` rather than a document-wide id is what lets two Vega charts coexist on one assembled page. Never reach for `document.getElementById` or a global selector; the same fragment may appear more than once in a composed document, and a global selector would bind them all to the first match.

## The Single Theme Source

Color, type, and axis styling come from one place: the OpenColors tokens in `theme.css`, which the assembler parses into `VizHelpers.tokens`. A Vega fragment reads those tokens into a `config` object at the top of `chart-js`, and Vega merges that config under the spec at embed time:

```js
const tokens = VizHelpers.tokens;
const config = {
  aria: true,
  range: { category: [tokens["oc-blue-7"], tokens["oc-orange-8"], /* … */] },
  axis: { domainColor: tokens["oc-gray-3"], gridColor: tokens["oc-gray-1"], /* … */ },
  legend: { labelColor: tokens["oc-gray-6"], /* … */ },
  title: { color: tokens["oc-gray-9"], /* … */ },
  view: { stroke: null },
};
```

A categorical scale with `"range": "category"` inherits `config.range.category`, so most charts get the palette for free. When a mark needs a specific semantic color, a candle's rising stroke or a slope's falling line, write the color in the spec as a token reference string of the form `"$TOKEN$oc-teal-7"`. A short resolver walks the spec once and swaps each `$TOKEN$…` string for its live theme value. Keeping the reference as a plain string leaves the spec parseable as JSON, which the render checker depends on. Because both the config and the semantic colors trace back to `theme.css`, a palette edit there reaches every Vega chart on the next assembly, no spec touched.

## Accessibility

A Vega fragment carries three accessibility paths, two automatic and one explicit.

The SVG renderer draws each bar, point, and line as a real DOM element that assistive technology can reach, which is why the embed call sets `renderer: "svg"`. With `config.aria` set true, Vega writes an `aria-label` onto each mark and `role="graphics-document"` onto the SVG root.

The spec's top-level `title` and `description` map to the SVG `<title>` and `<desc>`, which screen readers announce. Write a real sentence in `description`, the same argument the headline makes, so a listener who never sees the chart still learns what it shows.

The explicit path is the data table. After `vegaEmbed` resolves, read the rendered dataset from the Vega view and hand it to `VizHelpers.renderDataTable(root, rows, headers)`, which builds a collapsed `<details>` table scoped to this instance. The table is the path that survives when the marks themselves cannot be navigated.

That last point is the real limit of Vega here: its marks are not keyboard focusable, and its tooltips answer to the pointer alone. A chart whose argument depends on the reader hovering, filtering, brushing, or stepping through marks from the keyboard belongs in D3, which builds those affordances per mark. The engine criteria in [engine-selection.md](engine-selection.md) draw that line. For a static picture that a reader takes in at a glance, Vega's data table carries the accessible floor and the spec stays concise.

## What the Render Checker Enforces

`scripts/check_render.py` reads the assembled Vega output and the spec inside it, and reports defects before the chart ever opens. It expects the spec to parse as a JSON object, every encoded field to exist in the data, and a quantitative position scale to include zero unless the chart has a deliberate reason not to. A bar or area whose `y` scale omits `"zero": true` draws a baseline that exaggerates differences, so the checker flags it. Run the checker over the assembled example as the last step before presenting.

## Composing Several Charts

To place more than one chart on a page, assemble the fragments together:

```bash
python3 scripts/build_viz.py --compose <frag-a> <frag-b> --out dashboard.html
```

Each fragment becomes its own `<section>` with a unique id, its styles confined to that section, its scripts scoped to its own `root`. The fragments may mix engines freely; a Vega chart and a D3 chart sit side by side in one document with no shared globals and no id clashes. Lay the sections out with CSS in the wrapper or in a fragment's `chart-css`.

## Cross-references

- **D3 fragment authoring** (custom interactivity, keyboard navigation, sankey): see [base-template.md](base-template.md)
- **Engine selection criteria**: see [engine-selection.md](engine-selection.md)
- **Chart type selection**: see [template-selection.md](template-selection.md)

## Sources

- Vega-Embed documentation — <https://github.com/vega/vega-embed>
- Vega specification — <https://vega.github.io/vega/docs/specification/>
- Vega-Lite specification — <https://vega.github.io/vega-lite/docs/spec.html>
- Vega accessibility configuration — <https://vega.github.io/vega/docs/config/#aria>
- SVG Accessibility API Mappings — <https://www.w3.org/TR/svg-aam-1.0/>
