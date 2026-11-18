# Hand-written charts

Read this when the question needs a chart `build_page.py` does not draw: a distribution, an interval, a matrix, a network, a hierarchy, a map, or a composition of several marks.

You write the chart definition; the script still builds the page around it, with the data, the summary, the table, and the failed-load message.

```bash
scripts/build_page.py spec.json --data rows.json --out chart.html --chart-js chart-body.js
```

## Contents

- The chart body
- Imports
- Scales
- Marks
- Colour
- Accessibility
- Checking the API

## The chart body

`chart-body.js` is the body of an async function. It has `data` in scope and returns a chart definition:

- `data.rows`: the prepared rows
- `data.prepared`: the field names as `x`, `y`, `series`, plus `xType` and `seriesValues`
- `data.colors`: the series colours, already checked for colour blindness
- `data.spec`: the spec file

```js
const { defineChart, dot, ruleY } = await import('https://esm.sh/@tanstack/charts@1.5.0')
const { scaleLinear } = await import('https://esm.sh/@tanstack/charts@1.5.0/scales/linear')

return defineChart({
  marks: [
    ruleY([40]),
    dot(data.rows, { x: 'temp', y: 'sales', r: 5, fill: data.colors[0] }),
  ],
  scales: {
    x: { scale: scaleLinear, nice: true, axis: { label: 'Temperature (°C)' } },
    y: { scale: scaleLinear, nice: true, grid: true, axis: { label: 'Daily sales (units)' } },
  },
})
```

The script mounts the definition, so leave `mountChart` out of the body.
Prepare derived values (bins, quartiles, running totals, layout positions) in the rows before the build, so the table shows the same numbers the marks draw.
The spec still needs `title`, `summary`, `x.label`, `y.label`, and `y.unit`.

## Imports

Import only `@tanstack/charts`, from `https://esm.sh/@tanstack/charts@1.5.0` plus a subpath, each import written as a literal string so the check can read it.

Marks, `defineChart`, `colorLegend`, `group`, and `stack` come from the package root.
Scales and optional features come from subpaths, such as `/scales/linear` and `/tooltip`.

## Scales

Put position scales under `scales.x` and `scales.y`, and let the chart size them. Set a domain only where the order or the baseline is part of the claim.

| Mapping | Subpath | Export |
| --- | --- | --- |
| Numeric axis | `/scales/linear` | `scaleLinear` |
| Categories with width, as for bars | `/scales/band` | `scaleBand` |
| Categories without width, as for dots and lines | `/scales/point` | `scalePoint` |
| Dates spaced by elapsed time | `/scales/time` | `scaleUtc` |
| Category colours | `/scales/ordinal` | `scaleOrdinal` |

Pass the factory itself (`scale: scaleLinear`) to infer the domain from the data, or a zero-argument function returning a configured scale (`scale: () => scaleBand().domain(order).padding(0.16)`).
Axis options sit beside the scale: `axis: { label, ticks: { values, format } }`, `grid: true`, `nice: true`.

These five scales are the whole set this skill uses.
A logarithmic, power, or continuous colour scale lies outside it: bin the value into a few ordered classes in the rows and colour the classes, or choose another chart.

## Marks

| Need | Marks |
| --- | --- |
| Lines and areas | `lineY`, `lineX`, `areaY`, `areaX`, `differenceY` |
| Bars, ranges, cells | `barY`, `barX`, `rect`, `cell` |
| Points | `dot`, `hexagon` |
| Distributions | `boxY`, `boxX`, `violinY`, `violinX`, `ridgelineY` |
| Reference lines and links | `ruleX`, `ruleY`, `link`, `arrow`, `tickX`, `tickY` |
| Labels and small multiples | `text`, `frame`, `facet` |
| Part-to-whole and flows | `waffleY`, `treemap`, `sunburst`, `sankeyDiagram` |

Each mark takes the rows and an options object whose channels name fields: `x`, `y`, `z` for the series, `color` for the colour value, `fill` or `stroke` for one fixed paint.
Repeated bar positions stack; `layout: group()` sets them side by side.

## Colour

Take series colours from `data.colors` in order:

```js
color: {
  domain: data.prepared.seriesValues,
  range: data.colors,
  legend: colorLegend({ label: 'Person' }),
},
```

The page supplies five colours. Where the body needs a colour outside them, add it to the page's `colors` list by declaring the series in the rows, so the check measures it.
Pair colour with a second signal: a direct `text` label, position, or the legend and the table.

## Accessibility

The page passes the spec's `title` as the chart's accessible name and `summary` as its description, and keeps keyboard focus on.
Leave `keyboard` and `focus` at their defaults.
Add `tooltip` from `/tooltip` for hover detail, and keep every value a reader needs in the table as well.

## Checking the API

The option tables for every mark and scale at this version are at `https://github.com/TanStack/charts/tree/v1.5.0/docs`, under `reference/` and `examples/`.
Read the mark's page there before using an option this file leaves out. The documentation site describes a later, unreleased version.
After the build, run `scripts/check_output.py`, open the page, and confirm it reads `drawn`; a wrong option surfaces as `failed` with the library's message.
