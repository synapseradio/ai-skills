# visualize

Turn numbers, a comparison, a flow, or a structure into one chart or diagram that says one thing a reader can check. You get either a single HTML page that opens in a browser, or Markdown that renders in a pull request, README, ticket, or chat. Before handing either over, the skill validates the data and checks its own output.

## Worth running when

- You have numbers and a hunch, and need a chart that says one thing a reader can check.
- The chart has to live where it's read: a pull request, a ticket, a chat message, or a page in the browser.
- You want the chart to show what cuts against your framing as well as what supports it.

## What a run looks like

It starts by finishing the sentence "This shows that ___" from your data, and that sentence becomes the title. It asks you only where the data leaves a choice open: how duplicate rows combine, whether a gap means zero, where the result will be read. Then it prepares the rows, picks the chart, builds the output, and checks it before handing it over.

Trimmed from a run on a household of three's coffee across a week, Monday to Sunday: 9, 7, 8, 11, 6, 3, 4 cups, with Monday's "spike" blamed on a Sunday-night "just one episode" habit ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/visualize/household-coffee-week.md)):

> This shows that Monday runs high at 9 cups, but Thursday is the week's peak at 11, and the weekend drops to 3 and 4.
>
> - You called Monday's count a spike, but Thursday's 11 is higher than Monday's 9. Monday is the second-highest day.
> - Monday is the first row, so the Sunday before it is not in the data. The Sunday shown (4) ends the week.
>
> […]
>
> `note: summary: 7 rows; day is category; cups runs 3 to 11`
>
> […]
>
> The question is how a value changes along an order, so the chart is a line.
>
> […]
>
> `coffee-week.html: ok`

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/visualize/` into `~/.claude/skills/visualize/`.

## Usage

```text
/visualize show weekly signups by channel from signups.csv
/visualize which chart fits cups of coffee per person per day?
/visualize draw the checkout flow for the README
/visualize where do visitors drop out between landing and paying? funnel.csv
/visualize map internet use by country from share.csv
```

## What it produces

| Where it is read | Output |
| --- | --- |
| A browser | One HTML file holding a bar, line, area, or scatter chart, a sankey diagram, a network, a choropleth map, or a collapsible tree or zoomable treemap of a hierarchy |
| A pull request, README, ticket, wiki, or chat | Markdown: a Mermaid flowchart, sequence diagram, or schedule; a table; text bars; a ranked list; an indented tree |

### The HTML page, top to bottom

1. A title that states the claim, such as "Ben drank more coffee each day while Ana held steady".
2. A subtitle giving the scope and period.
3. The chart, with units on its axes, a legend for its series or its colour scale, and keyboard focus on its points.
4. A text summary carrying the numbers behind the claim, for a reader who never sees the chart.
5. The source of the data.
6. A table of every value, folded closed until opened. A sankey or a network has two, one of nodes and one of links. A map has one of regions, sorted by value.

The page is one file. It needs no install and no `package.json`, and opens straight from disk.

### What the page needs

The chart is drawn by [TanStack Charts](https://github.com/TanStack/charts), which the page fetches over https from the `esm.sh` module host when it opens, fixed at version 1.5.0. Drawing the chart therefore needs network access. Without it, the page shows its data table and says why the chart is missing.

TanStack Charts is the only library most pages name. That library depends on D3 modules, which the same host serves alongside it, some at version ranges resolved when the page loads.

A choropleth page names four more files from the same host, each fixed at an exact version:

| File | Version | What the page uses it for |
| --- | --- | --- |
| `d3-geo` | 3.1.1 | The map projection, which TanStack Charts leaves to the page |
| `d3-scale` | 4.0.2 | The continuous colour scale, which TanStack's own scales do not cover |
| `topojson-client` | 3.1.0 | Converting the world atlas to shapes; world maps only |
| `world-atlas` | 2.0.2 | Country boundaries at 1:110m; world maps only |

A map of your own regions embeds the GeoJSON you supply and loads the first two files only.

### Limits

- The build script draws seven chart kinds: bar (plain, grouped, or stacked), line, area, scatter, sankey, network, and choropleth. `scripts/build_hierarchy.ts` draws a tree and a treemap from paths and values. For another kind the agent writes the chart code by hand against the same page.
- A chart holds five series or node groups at most, the number of colours that passed the colour checks below.
- A network holds 60 nodes at most and a sankey 40. Its layout is settled once and does not move.
- A sankey needs every stage to send out what it takes in, and flow in one direction.
- A world map shows countries at 1:110m, joined by name or ISO 3166-1 numeric code. Other regions come from a GeoJSON file of polygons in longitude and latitude, drawn in a Mercator projection.
- A continuous colour scale appears on a choropleth only, as one hue running light to dark.
- Mermaid diagrams render on GitHub, GitLab, Notion, and Obsidian. Elsewhere the skill uses a table, a list, or a tree.

## How an output is prepared

1. **Data.** `scripts/prepare_data.ts` converts each value to its type and sorts dates and numbers. It stops, and the agent asks you, on a missing value, a value that is not a number, or two rows for one position. For a sankey it also stops on a link to an unknown node, a loop, or a stage whose inflow and outflow differ. For a map it stops on a region the atlas or the GeoJSON lacks.
2. **Chart.** The agent picks the chart from the question the reader asks. The build refuses a chart the data does not fit, such as a line joining categories that have no order.
3. **Labels.** The build requires a title, axis labels, a unit, and a text summary, and writes the data table itself.
4. **Colour.** Each series colour has at least 3:1 contrast with the page background. Each pair stays distinct under simulations of the three main kinds of colour blindness (protanopia, deuteranopia, tritanopia). A map's colour ramp spans at least 40 steps of lightness, so its order survives without hue.
5. **Check.** `scripts/check_output.ts` reads the finished file, compiles its chart without a browser, and measures where each mark and label falls. It lists each defect: a row with no mark, a mark or label outside the chart, labels drawn over each other, a missing summary or table, a file the page may not load or an unfixed version, a link to a missing node, a region with no shape on the map, colours a reader cannot tell apart, a text bar out of proportion to its value, a malformed Mermaid block. It measures geometry, not pixels, so the browser's own font widths can still differ.

## Prerequisites

- Bun 1.4 or later. The scripts run as `bun --install=fallback scripts/<name>.ts` and import nothing from outside Bun and Node.
- Network access on the first run, to fetch `@tanstack/charts@1.5.0` for the check, and a browser with network access to draw the HTML chart.

## Sources

- TanStack Charts 1.5.0 documentation, the API the pages and `references/charts.md` use: <https://github.com/TanStack/charts/tree/v1.5.0/docs>
- npm registry entry for `@tanstack/charts`, the source of the pinned version: <https://registry.npmjs.org/@tanstack/charts>
- TanStack Charts 1.5.0, "Networks and Hierarchies" and "Maps and Spatial Charts", the reader questions for sankey, network, and choropleth and the atlas route: <https://github.com/TanStack/charts/blob/v1.5.0/docs/examples/networks-and-hierarchies.md>, <https://github.com/TanStack/charts/blob/v1.5.0/docs/examples/maps-and-spatial.md>
- TanStack Charts 1.5.0, "Geo Shape Mark" and "Scales and D3", which leave the projection and any sequential colour scale to the page: <https://github.com/TanStack/charts/blob/v1.5.0/docs/reference/marks/geo.md>, <https://github.com/TanStack/charts/blob/v1.5.0/docs/concepts/scales-and-d3.md>
- npm registry entries for the choropleth files. `d3-geo` and `d3-scale` are fixed at the versions `@tanstack/charts@1.5.0` itself depends on: <https://registry.npmjs.org/d3-geo>, <https://registry.npmjs.org/d3-scale>, <https://registry.npmjs.org/topojson-client>, <https://registry.npmjs.org/world-atlas>
- `world-atlas` 2.0.2, which redistributes Natural Earth boundaries; the source of `assets/world-atlas-countries-110m.json`: <https://github.com/topojson/world-atlas>
- Machado, Oliveira, and Fernandes, "A Physiologically-based Model for Simulation of Color Vision Deficiency", the simulation matrices in `scripts/check_output.ts`: <https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html>
- WCAG 2.2, the contrast ratio formula and the 3:1 minimum for graphical objects: <https://www.w3.org/TR/WCAG22/#non-text-contrast>

The 40 steps of lightness a map ramp must span, and the node limits of 60 and 40, are this skill's own thresholds. The distance of 12 that the check requires between two series colours is this skill's own threshold, set below the closest pair in its palette (17.0) and above a red and green pair (`#d62728`, `#2ca02c`) that simulated colour blindness brings to 7.3.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`visualize.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/visualize.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
