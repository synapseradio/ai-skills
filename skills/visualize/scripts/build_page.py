#!/usr/bin/env python3
"""Build one self-contained HTML chart page from a spec and prepared rows.

The page holds its data, a text summary, and a data table, and loads the chart
library by pinned https import when it opens.

  build_page.py SPEC.json --data ROWS.json --out PAGE.html [--chart-js FILE]

ROWS.json is the file prepare_data.py writes: rows for bar, line, area, and
scatter, nodes and links for sankey and network, or regions for choropleth.
`--chart-js` replaces the generated chart definition with hand-written code.

Exit codes: 0 page written, 1 the spec and the data disagree, 2 unusable input.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

CHARTS_PACKAGE = "@tanstack/charts"
CHARTS_VERSION = "1.5.0"
CDN_BASE = f"https://esm.sh/{CHARTS_PACKAGE}@{CHARTS_VERSION}"

BACKGROUND = "#ffffff"
PALETTE = ["#0072b2", "#d55e00", "#009e73", "#cc79a7", "#000000"]

ROW_CHARTS = ("bar", "line", "area", "scatter")
GRAPH_CHARTS = ("sankey", "network")
OWN_SHAPE_CHARTS = GRAPH_CHARTS + ("choropleth",)
CHARTS = ROW_CHARTS + OWN_SHAPE_CHARTS

# A choropleth loads what the chart library leaves to the page: the projection, the
# continuous colour scale, and the world atlas with its converter.
MAP_URLS = {
    "projection": "https://esm.sh/d3-geo@3.1.1",
    "scale": "https://esm.sh/d3-scale@4.0.2",
    "converter": "https://esm.sh/topojson-client@3.1.0",
    "atlas": "https://esm.sh/world-atlas@2.0.2/countries-110m.json",
}
RAMP = ["#deebf7", "#08519c"]
NO_VALUE_COLOR = "#f1f3f5"
MAX_NODES = {"sankey": 40, "network": 60}
LINK_COLOR = "#6c757d"
PREPARED_KEYS = {
    "rows": {"x", "y", "series", "xType", "seriesValues", "rows"},
    "sankey": {"weighted", "groupValues", "nodes", "links"},
    "network": {"weighted", "groupValues", "nodes", "links"},
    "choropleth": {"atlas", "regionsWithoutValue", "regions", "features"},
}
TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "page.html"


class Unusable(Exception):
    """An input file cannot be read at all."""


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise Unusable(f"cannot read {path}: {error.strerror}")
    except json.JSONDecodeError as error:
        raise Unusable(f"{path} is not valid JSON: {error}")


def text_at(spec: dict, dotted: str) -> str:
    value = spec
    for part in dotted.split("."):
        value = value.get(part) if isinstance(value, dict) else None
    return value.strip() if isinstance(value, str) else ""


def validate(spec: dict, prepared: dict) -> list:
    """Return (code, message) pairs for every way the spec and the data disagree."""
    problems = []
    chart = spec.get("chart")
    shape = prepared["shape"]
    if chart in CHARTS and shape != (chart if chart in OWN_SHAPE_CHARTS else "rows"):
        wanted = chart if chart in OWN_SHAPE_CHARTS else "rows"
        return [
            (
                "chart-data-mismatch",
                f"a {chart} chart draws data prepared with --shape {wanted}; "
                f"this data was prepared with --shape {shape}",
            )
        ]
    if shape == "choropleth":
        return validate_choropleth(spec, prepared)
    if shape != "rows":
        return validate_graph(spec, prepared)
    x_type = prepared["xType"]
    series = prepared["series"]
    rows = prepared["rows"]

    required = ["title", "summary", "x.label", "y.label", "y.unit"]
    if series:
        required.append("series.label")
    if chart == "scatter":
        required.append("x.unit")
    for dotted in required:
        if not text_at(spec, dotted):
            problems.append(("spec-missing", f"the spec needs a non-empty {dotted}"))

    if chart not in CHARTS:
        problems.append(
            ("chart-unknown", f"chart is {chart!r}; this script draws {', '.join(CHARTS)}")
        )
        return problems

    ordered = bool(isinstance(spec.get("x"), dict) and spec["x"].get("ordered"))
    if chart == "bar" and x_type == "number":
        problems.append(
            (
                "chart-data-mismatch",
                "bars need categories on x; a numeric x reads as a scatter or a line",
            )
        )
    if chart in ("line", "area") and x_type == "category" and not ordered:
        problems.append(
            (
                "chart-data-mismatch",
                f"a {chart} joins neighbours, so x must be a date, a number, or categories with "
                "a real order; set x.ordered to true for ordered categories, or draw bars",
            )
        )
    if chart == "scatter" and x_type != "number":
        problems.append(("chart-data-mismatch", "a scatter needs a number on x"))

    if len(prepared["seriesValues"]) > len(PALETTE):
        problems.append(
            (
                "too-many-series",
                f"{len(prepared['seriesValues'])} series exceed the {len(PALETTE)} colours that stay "
                "distinct; keep the series the claim needs and fold the rest into one",
            )
        )
    stacked = chart == "area" or (chart == "bar" and spec.get("bars") == "stacked")
    if series and stacked and any(row[prepared["y"]] < 0 for row in rows):
        problems.append(
            ("stack-negative", "a stack cannot show values below zero; draw grouped bars or lines")
        )
    if chart in ("line", "area"):
        counts: dict = {}
        for row in rows:
            counts[row.get(series)] = counts.get(row.get(series), 0) + 1
        if min(counts.values()) < 2:
            problems.append(
                ("too-few-points", f"a {chart} needs two or more points in every series")
            )
    return problems


def validate_graph(spec: dict, prepared: dict) -> list:
    """Return (code, message) pairs for a sankey or network spec that the data cannot meet."""
    problems = []
    chart = spec.get("chart")
    required = ["title", "summary", "nodes.label"]
    if prepared["weighted"]:
        required += ["value.label", "value.unit"]
    if prepared["groupValues"]:
        required.append("group.label")
    for dotted in required:
        if not text_at(spec, dotted):
            problems.append(("spec-missing", f"the spec needs a non-empty {dotted}"))
    if chart not in CHARTS:
        problems.append(
            ("chart-unknown", f"chart is {chart!r}; this script draws {', '.join(CHARTS)}")
        )
        return problems
    if len(prepared["nodes"]) > MAX_NODES[chart]:
        problems.append(
            (
                "too-many-nodes",
                f"{len(prepared['nodes'])} nodes exceed the {MAX_NODES[chart]} a {chart} keeps "
                "readable; combine nodes, or show the links as a table",
            )
        )
    if len(prepared["groupValues"]) > len(PALETTE):
        problems.append(
            (
                "too-many-series",
                f"{len(prepared['groupValues'])} groups exceed the {len(PALETTE)} colours that "
                "stay distinct; keep the groups the claim needs and fold the rest into one",
            )
        )
    return problems


def validate_choropleth(spec: dict, prepared: dict) -> list:
    """Return (code, message) pairs for a choropleth spec that the data cannot meet."""
    problems = []
    for dotted in ("title", "summary", "region.label", "value.label", "value.unit"):
        if not text_at(spec, dotted):
            problems.append(("spec-missing", f"the spec needs a non-empty {dotted}"))
    if spec.get("chart") not in CHARTS:
        problems.append(
            (
                "chart-unknown",
                f"chart is {spec.get('chart')!r}; this script draws {', '.join(CHARTS)}",
            )
        )
        return problems
    values = {region["value"] for region in prepared["regions"]}
    if len(values) < 2:
        problems.append(
            (
                "constant-values",
                "every region holds the same value, so a map shows one colour; state the value "
                "in a sentence",
            )
        )
    return problems


def axis_label(axis: dict) -> str:
    label, unit = axis["label"].strip(), (axis.get("unit") or "").strip()
    return f"{label} ({unit})" if unit and unit.lower() not in label.lower() else label


def category_domain(spec: dict, prepared: dict) -> list:
    """Order bar categories by total value unless the spec keeps the given order."""
    x, y = prepared["x"], prepared["y"]
    totals: dict = {}
    for row in prepared["rows"]:
        totals[row[x]] = totals.get(row[x], 0) + row[y]
    given = list(totals)
    keep_given = (
        spec.get("sort") == "given" or prepared["xType"] == "date" or spec["x"].get("ordered")
    )
    return given if keep_given else sorted(given, key=lambda value: -totals[value])


def date_ticks(prepared: dict) -> str:
    """Tick whole days as dates, one tick per observed day while they fit the axis."""
    days = sorted({row[prepared["x"]] for row in prepared["rows"]})
    if any(len(day) != 10 for day in days):
        return ""
    parts = {"month": "short", "day": "numeric", "timeZone": "UTC"}
    if days[0][:4] != days[-1][:4]:
        parts["year"] = "numeric"
    label = f"format: (value) => new Intl.DateTimeFormat('en', {json.dumps(parts)}).format(value)"
    values = f"values: {json.dumps(days)}.map((day) => new Date(day)), " if len(days) <= 8 else ""
    return f", ticks: {{ {values}{label} }}"


def chart_js(spec: dict, prepared: dict) -> tuple:
    """Return (import names by subpath, JavaScript body that returns the definition)."""
    chart = spec["chart"]
    x, y, series = (json.dumps(prepared[key]) for key in ("x", "y", "series"))
    has_series = bool(prepared["series"])
    x_type = prepared["xType"]
    horizontal = chart == "bar" and spec.get("orientation") == "horizontal"
    root = {"defineChart"}
    scales = {"linear": "scaleLinear"}
    lines = []

    if x_type == "date" and chart != "bar":
        lines.append(
            f"const rows = data.rows.map((row) => ({{ ...row, [{x}]: new Date(row[{x}]) }}))"
        )
    else:
        lines.append("const rows = data.rows")

    measure = f"{{ scale: scaleLinear, nice: true, grid: true, axis: {{ label: {json.dumps(axis_label(spec['y']))} }} }}"
    position_label = json.dumps(axis_label(spec["x"]))
    paint = "" if has_series else f", fill: {json.dumps(PALETTE[0])}"
    stroke = "" if has_series else f", stroke: {json.dumps(PALETTE[0])}"
    marks = []

    if chart == "bar":
        scales["band"] = "scaleBand"
        domain = json.dumps(category_domain(spec, prepared))
        position = f"{{ scale: () => scaleBand().domain({domain}).padding(0.16), axis: {{ label: {position_label} }} }}"
        layout = ""
        if has_series and spec.get("bars") != "stacked":
            root.add("group")
            layout = ", layout: group()"
        colour = f", color: {series}" if has_series else ""
        if horizontal:
            root.add("barX")
            marks.append(f"barX(rows, {{ x: {y}, y: {x}{colour}{layout}, inset: 2{paint} }})")
            x_scale, y_scale = measure, position
        else:
            root.add("barY")
            marks.append(f"barY(rows, {{ x: {x}, y: {y}{colour}{layout}, inset: 2{paint} }})")
            x_scale, y_scale = position, measure
    else:
        if x_type == "date":
            scales["time"] = "scaleUtc"
            x_scale = (
                f"{{ scale: scaleUtc, axis: {{ label: {position_label}{date_ticks(prepared)} }} }}"
            )
        elif x_type == "number":
            x_scale = f"{{ scale: scaleLinear, nice: true, axis: {{ label: {position_label} }} }}"
        else:
            scales["point"] = "scalePoint"
            x_scale = (
                f"{{ scale: () => scalePoint().padding(0.2), axis: {{ label: {position_label} }} }}"
            )
        y_scale = measure
        group_by = f", z: {series}" if has_series else ""
        if chart == "line":
            root.add("lineY")
            marks.append(f"lineY(rows, {{ x: {x}, y: {y}{group_by}, points: true{stroke} }})")
        elif chart == "area":
            root.update(("areaY", "ruleY"))
            stack = ""
            if has_series:
                root.add("stack")
                stack = f", color: {series}, layout: stack()"
            marks.append(f"areaY(rows, {{ x: {x}, y: {y}{stack}, fillOpacity: 0.8{paint} }})")
            marks.append("ruleY([0])")
        else:
            root.add("dot")
            marks.append(f"dot(rows, {{ x: {x}, y: {y}{group_by}, r: 4{paint} }})")

    lines.append("return defineChart({")
    lines.append("  marks: [")
    lines.extend(f"    {mark}," for mark in marks)
    lines.append("  ],")
    lines.append(f"  scales: {{\n    x: {x_scale},\n    y: {y_scale},\n  }},")
    if has_series:
        root.add("colorLegend")
        legend = json.dumps(spec["series"]["label"].strip())
        lines.append("  color: {")
        lines.append("    domain: data.prepared.seriesValues,")
        lines.append("    range: data.colors,")
        lines.append(f"    legend: colorLegend({{ label: {legend} }}),")
        lines.append("  },")
    lines.append("  tooltip,")
    lines.append("})")

    imports = {"": sorted(root), "/tooltip": ["tooltip"]}
    for subpath, name in scales.items():
        imports[f"/scales/{subpath}"] = [name]
    return imports, "\n".join(lines)


def sankey_js(spec: dict) -> tuple:
    """Return (import names by subpath, JavaScript body) for a sankey."""
    color = json.dumps(PALETTE[0])
    body = f"""const amount = (value) => value.toLocaleString("en")
const ribbon = {{
  line: ([[x1, y1], [x2, y2]]) =>
    `M${{x1}},${{y1}}C${{(x1 + x2) / 2}},${{y1}} ${{(x1 + x2) / 2}},${{y2}} ${{x2}},${{y2}}`,
  area: () => "",
}}
return defineChart({{
  marks: [
    sankeyDiagram({{
      nodes: data.nodes,
      links: data.links,
      nodeKey: "id",
      source: "source",
      target: "target",
      value: "value",
      nodeWidth: 14,
      nodePadding: 18,
      inset: 8,
      marks: ({{ nodes, links }}) => {{
        const lastLayer = Math.max(...nodes.map((node) => node.layer))
        const onRight = (node) => node.layer === lastLayer
        return [
          link(links, {{
            x1: "x1", y1: "y1", x2: "x2", y2: "y2", key: "key",
            strokeWidth: (flow) => Math.max(1, flow.width),
            stroke: {color}, strokeOpacity: 0.35, lineCap: "butt", curve: ribbon,
          }}),
          rect(nodes, {{ x1: "x0", x2: "x1", y1: "y0", y2: "y1", key: "key", inset: 0, fill: {color} }}),
          text(nodes, {{
            x: (node) => (onRight(node) ? node.x0 : node.x1),
            y: "y",
            text: (node) => `${{node.data.label}} ${{amount(node.value)}}`,
            key: "key",
            anchor: (node) => (onRight(node) ? "end" : "start"),
            dx: (node) => (onRight(node) ? -6 : 6),
            dy: 4,
            fill: "currentColor",
            fontSize: 12,
          }}),
        ]
      }},
    }}),
  ],
  scales: {{ x: null, y: null }},
  guides: false,
  margin: 0,
}})"""
    imports = {"": ["defineChart", "link", "rect", "text"], "/network/sankey": ["sankeyDiagram"]}
    return imports, body


def network_js(spec: dict, prepared: dict) -> tuple:
    """Return (import names by subpath, JavaScript body) for a settled force-directed network."""
    grouped = bool(prepared["groupValues"])
    root = ["defineChart", "dot", "link", "text"]
    width = "1.5"
    if prepared["weighted"]:
        width = "(edge) => 1 + (5 * edge.value) / largest"
    paint = 'color: "group"' if grouped else f"fill: {json.dumps(PALETTE[0])}"
    lines = [
        "const largest = Math.max(1, ...data.links.map((edge) => edge.value ?? 1))",
        "const graph = forceLayout(data.nodes, data.links, {",
        '  nodeKey: "id",',
        '  source: "source",',
        '  target: "target",',
        "  iterations: 300,",
        "  forces: [",
        '    { type: "link", distance: 48 },',
        '    { type: "manyBody", strength: -160 },',
        '    { type: "center" },',
        '    { type: "collide", radius: 16 },',
        "  ],",
        "})",
        "return defineChart({",
        "  marks: [",
        "    link(graph.links, {",
        '      x1: "x1", y1: "y1", x2: "x2", y2: "y2",',
        "      key: (edge) => `${edge.source}->${edge.target}`,",
        f"      stroke: {json.dumps(LINK_COLOR)}, strokeWidth: {width},",
        "    }),",
        f'    dot(graph.nodes, {{ x: "x", y: "y", key: "id", r: 6, {paint} }}),',
        "    text(graph.nodes, {",
        '      x: "x", y: "y", text: "label", key: "id", dy: -10, fill: "currentColor", fontSize: 11,',
        "    }),",
        "  ],",
        "  scales: {",
        "    x: { scale: () => scaleLinear().domain(graph.xDomain), axis: false },",
        "    y: { scale: () => scaleLinear().domain(graph.yDomain), axis: false },",
        "  },",
    ]
    if grouped:
        root.append("colorLegend")
        legend = json.dumps(spec["group"]["label"].strip())
        lines += [
            "  color: {",
            "    domain: data.prepared.groupValues,",
            "    range: data.colors,",
            f"    legend: colorLegend({{ label: {legend} }}),",
            "  },",
        ]
    lines.append("})")
    imports = {
        "": sorted(root),
        "/network/force": ["forceLayout"],
        "/scales/linear": ["scaleLinear"],
    }
    return imports, "\n".join(lines)


def choropleth_js(spec: dict, prepared: dict) -> tuple:
    """Return (import names by subpath, JavaScript body) for a choropleth."""
    world = prepared["atlas"] == "world"
    url = {name: json.dumps(value) for name, value in MAP_URLS.items()}
    legend = json.dumps(axis_label(spec["value"]))
    lines = [
        f"const {{ {'geoEqualEarth' if world else 'geoMercator'} }} = await import({url['projection']})",
        f"const {{ scaleSequential }} = await import({url['scale']})",
    ]
    if world:
        lines += [
            f"const {{ feature }} = await import({url['converter']})",
            f"const response = await fetch({url['atlas']})",
            "if (!response.ok) throw new Error(`The world atlas answered ${response.status}.`)",
            "const topology = await response.json()",
            "const features = feature(topology, topology.objects.countries).features.map(",
            "  (shape) => ({ ...shape, id: shape.properties.name }),",
            ")",
            'const projection = { type: geoEqualEarth, fit: "sphere", inset: 4 }',
        ]
    else:
        lines += [
            "const features = data.features",
            'const projection = { type: geoMercator, fit: { type: "FeatureCollection", features }, inset: 4 }',
        ]
    lines += [
        "const values = new Map(data.regions.map((region) => [region.key, region.value]))",
        "const channel = (hex, index) => parseInt(hex.slice(1 + 2 * index, 3 + 2 * index), 16)",
        "const [light, dark] = data.ramp",
        "const ramp = (t) =>",
        "  `rgb(${[0, 1, 2]",
        "    .map((i) => Math.round(channel(light, i) + t * (channel(dark, i) - channel(light, i))))",
        '    .join(",")})`',
        "const extent = [data.regions.at(-1).value, data.regions[0].value]",
        f"const edge = {{ key: (shape) => shape.id, projection, stroke: {json.dumps(LINK_COLOR)}, strokeWidth: 0.5 }}",
        "const layers = [",
        f"  [features.filter((shape) => !values.has(shape.id)), {{ ...edge, fill: {json.dumps(NO_VALUE_COLOR)} }}],",
        "  [features.filter((shape) => values.has(shape.id)), { ...edge, color: (shape) => values.get(shape.id) }],",
        "]",
        "return defineChart({",
        "  marks: layers.filter(([shapes]) => shapes.length).map(([shapes, options]) => geoShape(shapes, options)),",
        "  scales: { x: null, y: null },",
        "  color: {",
        "    scale: () => scaleSequential(ramp).domain(extent),",
        f'    legend: colorLegend({{ label: {legend}, format: (value) => value.toLocaleString("en") }}),',
        "  },",
        "})",
    ]
    imports = {"": ["colorLegend", "defineChart"], "/geo": ["geoShape"]}
    return imports, "\n".join(lines)


def import_lines(imports: dict) -> str:
    imports = dict(imports)
    imports["/dom"] = ["mountChart"]
    return "\n".join(
        f"  const {{ {', '.join(names)} }} = await import({json.dumps(CDN_BASE + subpath)})"
        for subpath, names in sorted(imports.items())
    )


def format_cell(value) -> str:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return html.escape(str(value))
    return format(value, ",") if isinstance(value, int) else format(value, ",.6g")


def table_html(spec: dict, prepared: dict) -> str:
    x, y, series = prepared["x"], prepared["y"], prepared["series"]
    columns = [(x, axis_label(spec["x"]), prepared["xType"] == "number")]
    if series:
        columns.append((series, spec["series"]["label"].strip(), False))
    columns.append((y, axis_label(spec["y"]), True))
    return one_table(
        spec["title"].strip(),
        [(label, numeric) for _, label, numeric in columns],
        [[row[field] for field, _, _ in columns] for row in prepared["rows"]],
    )


def one_table(caption: str, columns: list, rows: list) -> str:
    """Render one table from (header, is numeric) columns and rows of cell values."""
    out = ["<table>", f"<caption>{html.escape(caption)}</caption>", "<thead><tr>"]
    for label, numeric in columns:
        css = ' class="num"' if numeric else ""
        out.append(f'<th scope="col"{css}>{html.escape(label)}</th>')
    out.append("</tr></thead>")
    out.append("<tbody>")
    for row in rows:
        cells = "".join(
            ('<td class="num">' if numeric else "<td>") + format_cell(value) + "</td>"
            for value, (_, numeric) in zip(row, columns)
        )
        out.append(f"<tr>{cells}</tr>")
    out.append("</tbody>")
    out.append("</table>")
    return "\n".join(out)


def graph_tables_html(spec: dict, prepared: dict) -> str:
    """Render the node table and the link table that stand in for a sankey or a network."""
    nodes, links = prepared["nodes"], prepared["links"]
    weighted = prepared["weighted"]
    label = {node["id"]: node["label"] for node in nodes}
    amount = axis_label(spec["value"]) if weighted else ""
    title = spec["title"].strip()

    node_columns = [(spec["nodes"]["label"].strip(), False)]
    if prepared["groupValues"]:
        node_columns.append((spec["group"]["label"].strip(), False))
    if spec["chart"] == "sankey":
        node_columns += [(f"In: {amount}", True), (f"Out: {amount}", True)]
    else:
        node_columns.append(("Links", True))
    node_rows = []
    for node in nodes:
        entering = [link for link in links if link["target"] == node["id"]]
        leaving = [link for link in links if link["source"] == node["id"]]
        row = [node["label"]]
        if prepared["groupValues"]:
            row.append(node["group"])
        if spec["chart"] == "sankey":
            row += [sum(link["value"] for link in entering), sum(link["value"] for link in leaving)]
        else:
            row.append(len(entering) + len(leaving))
        node_rows.append(row)

    link_columns = [("From", False), ("To", False)] + ([(amount, True)] if weighted else [])
    link_rows = [
        [label[link["source"]], label[link["target"]]] + ([link["value"]] if weighted else [])
        for link in links
    ]
    return "\n".join(
        (
            one_table(f"{title}: nodes", node_columns, node_rows),
            one_table(f"{title}: links", link_columns, link_rows),
        )
    )


def indent(text: str, prefix: str) -> str:
    return "\n".join(prefix + line if line else line for line in text.splitlines())


def build(spec: dict, prepared: dict, custom_js) -> str:
    shape = prepared["shape"]
    if custom_js is not None:
        body = custom_js.strip("\n")
        imports_text = import_lines({})
    else:
        if shape == "choropleth":
            imports, body = choropleth_js(spec, prepared)
        elif shape == "sankey":
            imports, body = sankey_js(spec)
        elif shape == "network":
            imports, body = network_js(spec, prepared)
        else:
            imports, body = chart_js(spec, prepared)
        imports_text = import_lines(imports)

    data = {"spec": spec, "shape": shape, "background": BACKGROUND}
    footnote = ""
    if shape == "choropleth":
        height = 420
        data["prepared"] = {key: prepared[key] for key in ("atlas", "regionsWithoutValue")}
        data["colors"] = RAMP[1:]
        data["ramp"] = RAMP
        data["unit"] = spec["value"]["unit"]
        data["regions"] = prepared["regions"]
        data["features"] = prepared["features"]
        table = one_table(
            spec["title"].strip(),
            [(spec["region"]["label"].strip(), False), (axis_label(spec["value"]), True)],
            [[region["label"], region["value"]] for region in prepared["regions"]],
        )
        if prepared["regionsWithoutValue"]:
            footnote = '<p class="source">Regions in grey have no value.</p>'
    elif shape == "rows":
        horizontal = spec.get("chart") == "bar" and spec.get("orientation") == "horizontal"
        height = (
            max(240, 80 + 30 * len({row[prepared["x"]] for row in prepared["rows"]}))
            if horizontal
            else 380
        )
        data["prepared"] = {
            key: prepared[key] for key in ("x", "y", "series", "xType", "seriesValues")
        }
        data["colors"] = PALETTE[: max(1, len(prepared["seriesValues"]))]
        data["unit"] = spec["y"]["unit"]
        data["rows"] = prepared["rows"]
        table = table_html(spec, prepared)
    else:
        height = 460
        data["prepared"] = {key: prepared[key] for key in ("weighted", "groupValues")}
        data["colors"] = PALETTE[: max(1, len(prepared["groupValues"]))]
        data["unit"] = spec["value"]["unit"] if prepared["weighted"] else None
        data["nodes"] = prepared["nodes"]
        data["links"] = prepared["links"]
        table = graph_tables_html(spec, prepared)
    subtitle = text_at(spec, "subtitle")
    source = text_at(spec, "source")
    replacements = {
        "__TITLE__": html.escape(spec["title"].strip()),
        "__SUBTITLE__": f'<p class="subtitle">{html.escape(subtitle)}</p>' if subtitle else "",
        "__SUMMARY__": html.escape(spec["summary"].strip()),
        "__SOURCE__": (f'<p class="source">Source: {html.escape(source)}</p>' if source else "")
        + footnote,
        "__TABLE__": table,
        "__DATA__": json.dumps(data, ensure_ascii=False).replace("</", "<\\/"),
        "__IMPORTS__": imports_text,
        "__CHART__": indent(body, "    "),
        "__HEIGHT__": str(height),
        "__BACKGROUND__": BACKGROUND,
        "__CDN_HOST__": CDN_BASE.split("/")[2],
    }
    page = TEMPLATE.read_text(encoding="utf-8")
    for token, value in replacements.items():
        page = page.replace(token, value)
    return page


def main(argv: list) -> int:
    parser = argparse.ArgumentParser(description="Build one self-contained HTML chart page.")
    parser.add_argument("spec", type=Path)
    parser.add_argument(
        "--data", required=True, type=Path, help="rows file written by prepare_data.py"
    )
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument(
        "--chart-js",
        type=Path,
        help="JavaScript that returns a chart definition, used in place of the generated one",
    )
    args = parser.parse_args(argv)

    try:
        spec = load_json(args.spec)
        prepared = load_json(args.data)
        custom_js = args.chart_js.read_text(encoding="utf-8") if args.chart_js else None
    except Unusable as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"error: cannot read {args.chart_js}: {error.strerror}", file=sys.stderr)
        return 2
    usable = isinstance(spec, dict) and isinstance(prepared, dict)
    if usable:
        wanted = PREPARED_KEYS.get(prepared.get("shape"))
        usable = wanted is not None and wanted <= set(prepared)
    if not usable:
        print(
            "error: the spec must be a JSON object and --data must be a file prepare_data.py wrote",
            file=sys.stderr,
        )
        return 2

    problems = validate(spec, prepared)
    if custom_js is not None:
        problems = [problem for problem in problems if problem[0] == "spec-missing"]
    if problems:
        for code, message in problems:
            print(f"problem: {code}: {message}")
        return 1
    args.out.write_text(build(spec, prepared, custom_js), encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
