# Tree and treemap

Read this when the reader's question is what contains what, or what share each part holds: a folder tree with sizes, a budget by department and line, a count by category and subcategory.

```bash
bun --install=fallback scripts/build_hierarchy.ts rows.csv --path path --value lines --spec spec.json --chart treemap --out chart.html
```

Add `--delimiter` where the path column splits on something other than `/`.

## Contents

- Choosing the chart
- The rows
- The spec
- Problems the build reports
- The hand-written contract

## Choosing the chart

| The reader will | Chart |
| --- | --- |
| Find one path, open a folder, search by name | `tree` |
| Compare shares, see which part dominates, drill into one part | `treemap` |

A treemap draws area, so a zero value has no tile. Give such rows a value above zero or leave them out.

## The rows

One row per leaf, with a path and a nonnegative number. A directory's total is the sum of what it holds, so list leaves only.
Paths from a repository come from `git ls-files`:

```bash
git ls-files | while IFS= read -r file; do printf '%s,%s\n' "$file" "$(wc -l < "$file")"; done > rows.csv
```

Put `path,lines` as the first line of the file.

## The spec

`title`, `summary`, and `y.unit` are required. `subtitle` and `source` are optional. The table holds the paths with their totals under `Total <unit>`.

## Problems the build reports

| Problem | Act |
| --- | --- |
| `missing-value`, `empty-path` | Fix the row in the source |
| `not-a-number` | Move a unit or symbol out of the cell and into the spec |
| `negative-value` | A share cannot be negative; ask what the number means |
| `duplicate-key` | Ask the user how the rows combine, apply it to the source |
| `path-conflict` | The same name is a leaf in one row and a folder in another; fix the source |
| `bad-segment` | A name inside a path holds `/`; choose another delimiter |
| `spec-missing`, `missing-field` | Add the field or name a column the file has |

## The hand-written contract

A page built for another hierarchy kind follows the same contract, and the check measures it without a browser:

- The `viz-data` script holds `"shape": "custom"` and rows that each carry a string `key`.
- A classic script with `id="viz-layout"` defines `vizViews(data)`, which returns the views to measure, and `vizLayout(data, size, view, measureText)`, which returns a scene of `{ width, height, chart, nodes, points }`. It touches no document or window, so the page and the check call the same code.
- Nodes are `group`, `rect`, `label`, `dot`, `rule`, `polyline`, or `area`. Data marks sit under the group keyed `marks`. A label carries `x`, `y`, `text`, `fontSize`, `anchor`, and `baseline`.
- Each point has the `key` of a row. The check reports a row that no view draws, a mark more than 1px outside `chart`, labels that overlap, and a label past the edge.
- The check measures at a width of 1200 and estimates text as 0.6 of the font size per character wide and 1.2 of the font size high, so keep labels clear of each other by that margin.
- A page with this script and no import of the chart library passes the `no-chart-import` check.
