---
name: visualize
description: >
  Turn data, a comparison, a trend, a flow, or a structure into a chart or
  diagram a reader can check. Produces a self-contained HTML chart page that
  opens from disk, drawn with TanStack Charts, or a Markdown output (a Mermaid
  diagram, a table, text bars) that drops into a pull request, README, ticket,
  or chat. Shapes and validates the data first, picks the chart from the
  question and the data, adds labels, units, a text summary and a data table,
  uses colours that survive colour blindness, and checks its own output before
  handing it over. Use whenever the user asks to visualize anything, make a
  chart, graph, plot, map, or diagram, show a trend, compare numbers, show a
  flow, a network, or a timeline, or asks which chart type fits their data.
metadata:
  user-invocable: true
---

# Visualize

Produce one visualization that answers one question, in a form the reader's surface can show, and hand it over only after its check passes.

Run each script as `bun --install=fallback scripts/<name>.ts`. The flag keeps Bun's own installer working when a `node_modules` folder sits above the script.
The scripts sit in `scripts/` beside this file, and need Bun 1.4 or later. The first run of the check fetches the pinned chart library `@tanstack/charts@1.5.0` into Bun's cache, so it needs network access once.

## 1. Settle the claim and the surface

Finish the sentence "This shows that ___" from the data in hand.
That sentence becomes the title, so a reader who reads only the title still gets the point.
Where the data cannot finish the sentence, ask the user what the reader has to decide.
State in the claim what cuts against the user's framing as plainly as what supports it.

Pick the route by where the result will be read:

| The result is read | Route |
| --- | --- |
| In a browser, as a file the user opens or shares | HTML page: steps 2 to 6 |
| In a pull request, README, ticket, wiki page, or chat | Markdown: read `references/markdown.md`, then steps 5 and 6 |
| As a process, a sequence of messages, a schedule, or a tree | Markdown: read `references/markdown.md`, then steps 5 and 6 |
| Somewhere the request leaves open | Ask the user which of the two they want |

## 2. Prepare the data

Put the rows in a CSV, TSV, or JSON file, one observation per row, then run:

```bash
bun --install=fallback scripts/prepare_data.ts data.csv --x day --y cups --series person --out rows.json
```

`--x` names the position or category column, `--y` the measured number, and `--series` the column that splits rows into groups, left out for one series.
The script converts types, sorts dates and numbers, and writes `rows.json` only when every row is usable.

A flow between stages, a network of linked things, and values by region each take another input shape.
For one of those, read `references/shapes.md` now and follow it for this step and for the spec in step 4.

Read every `note:` line, since each one changes what the chart may claim.
Treat each `problem:` line as a question about the data:

| Problem | Act |
| --- | --- |
| `duplicate-key` | Ask the user how the rows combine (sum, mean, latest), apply that to the source, run again |
| `missing-value` | Ask whether the gap means zero or unknown. Pass `--drop-missing` only where the user says unknown rows may go, and report the dropped count |
| `not-a-number`, `not-a-date` | Fix the value in the source. Move a unit or currency symbol out of the cell and into the spec |
| `missing-field` | Name a column the file has |

This step is done when the script exits 0.

## 3. Choose the chart

Choose from the question the reader asks, then confirm the data fits:

| Reader's question | Chart | Data it needs |
| --- | --- | --- |
| Which category is larger? | `bar`, sorted by value, or `"sort": "given"` to keep the file's order; `"orientation": "horizontal"` for long labels | categories on x |
| How do parts add up within each category? | `bar` with a series and `"bars": "stacked"` | categories, a series, no value below zero |
| How do groups compare inside each category? | `bar` with a series | categories, a series |
| How does a value change over time or along an order? | `line` | dates or numbers on x, or categories with a real order and `"ordered": true` |
| How does a total and its parts change over time? | `area` | as `line`, no value below zero |
| Do two measures move together? | `scatter` | a number on x, with its own unit |
| How does quantity split and recombine, or move through staged subtotals? | `sankey` | links with a value, every stage balanced |
| Which clusters emerge among linked things with no fixed positions? | `network` | nodes and links, 60 nodes at most |
| How does an aggregate differ across named regions? | `choropleth` | one value per country, or per region of a GeoJSON file |
| What contains what, and what share does each part hold? | `tree` (collapsible, for finding a path) or `treemap` (zoomable, for comparing shares): read `references/hierarchy.md`, build with `scripts/build_hierarchy.ts` | one row per leaf with a path and a nonnegative value |
| A distribution, an interval, a matrix | Hand-written chart: read `references/charts.md` | prepared by you |

Hold these while choosing:

- One chart makes one point. A second point gets a second chart.
- Show five series at most. Keep the series the claim needs and fold the rest into one named "Other".
- Give each measure its own chart in place of a second y axis.
- Keep the full history in view when the claim is about a change.
- Where a mean would hide how the values spread, show the spread.
- Draw a network only when the links are the question. Past a few dozen nodes, a table or a grouped bar reads better.
- On a map a large region draws the eye whatever its value. Where the claim is a ranking, draw sorted bars.

## 4. Build the page

Write a spec file beside the rows:

```json
{
  "title": "Ben drank more coffee each day while Ana held steady",
  "subtitle": "Cups per day, 9 to 11 November 2026",
  "summary": "Ben rose from 3 to 4 cups a day. Ana stayed between 1 and 3.",
  "source": "Kitchen tally sheet",
  "chart": "line",
  "x": { "label": "Day" },
  "y": { "label": "Coffee", "unit": "cups" },
  "series": { "label": "Person" }
}
```

- `title`: the claim from step 1.
- `subtitle`: scope and period.
- `summary`: the text alternative. Write the two or three numbers that carry the claim, so a reader who never sees the chart still learns it.
- `source`: where the rows came from.
- `y.unit`: required. Name what is counted where the measure has no physical unit, such as `signups`.
- `x.unit`: required for `scatter`.

Then build:

```bash
bun --install=fallback scripts/build_page.ts spec.json --data rows.json --out chart.html
```

The page carries its data, the summary, and a full data table, starts bars at zero, assigns colours that stay distinct under colour blindness, and names the chart for screen readers.
A sankey or a network carries a node table and a link table, and a choropleth a table of regions sorted by value.
It imports `@tanstack/charts@1.5.0` from `esm.sh` when it opens, so it needs network access to draw. Without it the page shows the table and says why.
TanStack Charts loads its own D3 modules from the same CDN, some at version ranges the CDN resolves on load; the page pins the TanStack version alone.
A choropleth page also loads from `esm.sh`, each at an exact version, the map projection (`d3-geo@3.1.1`) and the continuous colour scale (`d3-scale@4.0.2`), which TanStack Charts leaves to the page, and for the world atlas `topojson-client@3.1.0` and `world-atlas@2.0.2`.

Treat each `problem:` line from the build as a mismatch between the chart and the data, and return to step 3.

The page needs no `package.json` and no install, and opens from disk.

Before installing anything on the user's machine, such as Bun where `bun` is not on the path, ask the user and state all four of:

- what is missing
- what it is needed for
- the exact command
- what the command changes on their machine

Install only after a yes. On any other answer, write the page by hand from `assets/page.html`, filling each `__NAME__` token, and check it by reading it against step 5.

## 5. Check the output

```bash
bun --install=fallback scripts/check_output.ts chart.html
```

The script accepts HTML pages and Markdown files and prints one line per defect.
Fix the cause of each defect in the spec, the rows, or the Markdown, rebuild, and run it again until it prints `ok`.

Then read the output once as its reader:

- The title states the claim, and the claim matches the rows.
- Every number carries its unit.
- The summary gives the numbers behind the claim.
- Nothing essential depends on colour alone: the legend, the labels, or the table carries it too.

For an HTML page the script also compiles the chart and measures its geometry without a browser. It reports a row with no mark, a mark outside the chart area, and labels that overlap or run past the edge.
It measures positions, not pixels, so a reader's browser can still differ in font width.

This step is done when the script prints `ok` and the read finds nothing to change.

## 6. Hand over

Write the file where the user asked, else in the working directory, and give its path.
With it, state the claim in one sentence, each row dropped or combined in step 2, and for an HTML page that it needs network access to draw the chart.
