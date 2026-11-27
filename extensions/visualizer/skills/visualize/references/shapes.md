# Flows, networks, and maps

Each of these three kinds takes its own input shape, its own `prepare_data.ts` arguments, and its own spec fields.
Steps 3, 5, and 6 of `SKILL.md` apply unchanged.

## Sankey: how a quantity splits and recombines

Put one link per row in a CSV, TSV, or JSON file, naming where the quantity leaves, where it arrives, and how much:

```csv
from,to,visits
Landing,Sign-up,620
Landing,Left,380
Sign-up,Trial,410
Sign-up,Left,210
```

```bash
bun --install=fallback scripts/prepare_data.ts flow.csv --shape sankey --source from --target to --value visits --out flow.json
```

Every stage that both receives and sends must send out exactly what it receives.
Where the source data loses quantity at a stage, add a link to a node that names where it went, such as "Left".

```json
{
  "title": "Of 1,000 landing visits, 150 end in a paid plan",
  "summary": "620 of 1,000 visits reach sign-up, 410 start a trial, and 150 pay.",
  "chart": "sankey",
  "nodes": { "label": "Stage" },
  "value": { "label": "Visits", "unit": "visits" }
}
```

## Network: which things link to which

Put one link per row. A value column is optional and sets the line width.
To colour nodes by group or to show a name other than the id, add a nodes file with one row per node:

```bash
bun --install=fallback scripts/prepare_data.ts calls.csv --shape network --source caller --target callee --value calls \
  --nodes services.csv --node-id id --node-group team --out calls.json
```

`--node-label` names the nodes column holding the name to show.
A link is undirected: A to B and B to A count as the same link.

```json
{
  "title": "Every service reaches auth through api or billing",
  "summary": "Seven services and eight call paths. api is the hub with three links.",
  "chart": "network",
  "nodes": { "label": "Service" },
  "group": { "label": "Team" },
  "value": { "label": "Calls", "unit": "calls per minute" }
}
```

`group` is required when the nodes file has groups, and `value` when the links have values.
The layout is computed once when the page opens and stays still.
State in the summary what the reader should see in the layout, since position carries no value.

## Choropleth: how a value differs across regions

Put one region per row with its value.
A choropleth colours area, so use a rate, a share, or a density. Draw counts as bars.

For countries, name each by its ISO 3166-1 numeric code or by its name as `assets/world-atlas-countries-110m.json` lists it:

```bash
bun --install=fallback scripts/prepare_data.ts internet.csv --shape choropleth --region country --value share --out internet.json
```

For any other regions, pass a GeoJSON FeatureCollection of polygons in longitude and latitude, and name the property the region column matches:

```bash
bun --install=fallback scripts/prepare_data.ts wards.csv --shape choropleth --region ward --value trees \
  --geojson wards.geojson --feature-id code --feature-name name --out wards.json
```

Without `--feature-id` the join uses each feature's top-level `id`.
The page embeds the GeoJSON, so simplify a file of several megabytes before preparing it.

```json
{
  "title": "Internet use runs from 12% in Chad to 99% in Norway",
  "summary": "Norway (99%) and Australia (95%) lead; Nigeria (39%) and Chad (12%) trail.",
  "chart": "choropleth",
  "region": { "label": "Country" },
  "value": { "label": "People using the internet", "unit": "% of population" }
}
```

Regions without a row are drawn in grey and the page says so.
The colour runs from light at the lowest value to dark at the highest, with a legend that names both ends.
Name in the summary any small region the claim rests on, since a reader may not find it on the map.

## Problems

| Problem | Act |
| --- | --- |
| `unbalanced-node` | Ask the user where the difference went, add that link to the source, run again |
| `cycle` | A sankey reads in one direction. Remove the returning link, or draw a network |
| `unknown-node` | Add the node to the nodes file, or correct the name in the link |
| `unlinked-node` | Remove the node, or add the link that reaches it |
| `self-link` | Remove the link, and state the self-reference in the summary if it matters |
| `not-positive` | Remove a link of zero. Ask the user what a negative flow means |
| `duplicate-key` | Ask the user how the two rows combine, apply that to the source, run again |
| `unknown-region` | Use the atlas name or numeric code, or the GeoJSON key. Ask the user where a region has no counterpart |
| `duplicate-region`, `not-a-region` | Fix the GeoJSON: one polygon feature per key |
| `too-many-nodes` | Combine nodes, or show the links as a table |
| `constant-values` | State the value in a sentence in place of a map |
