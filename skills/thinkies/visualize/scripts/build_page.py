#!/usr/bin/env python3
"""Build one self-contained HTML chart page from a spec and prepared rows.

The page holds its data, a text summary, and a data table, and loads the chart
library by pinned https import when it opens.

  build_page.py SPEC.json --data ROWS.json --out PAGE.html [--chart-js FILE]

ROWS.json is the file prepare_data.py writes. `--chart-js` replaces the generated
chart definition with hand-written code.

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

CHARTS = ("bar", "line", "area", "scatter")
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
    out = ["<table>", f"<caption>{html.escape(spec['title'].strip())}</caption>", "<thead><tr>"]
    for _, label, numeric in columns:
        css = ' class="num"' if numeric else ""
        out.append(f'<th scope="col"{css}>{html.escape(label)}</th>')
    out.append("</tr></thead>")
    out.append("<tbody>")
    for row in prepared["rows"]:
        cells = "".join(
            ('<td class="num">' if numeric else "<td>") + format_cell(row[field]) + "</td>"
            for field, _, numeric in columns
        )
        out.append(f"<tr>{cells}</tr>")
    out.append("</tbody>")
    out.append("</table>")
    return "\n".join(out)


def indent(text: str, prefix: str) -> str:
    return "\n".join(prefix + line if line else line for line in text.splitlines())


def build(spec: dict, prepared: dict, custom_js) -> str:
    if custom_js is None:
        imports, body = chart_js(spec, prepared)
        imports_text = import_lines(imports)
    else:
        body = custom_js.strip("\n")
        imports_text = import_lines({})

    horizontal = spec.get("chart") == "bar" and spec.get("orientation") == "horizontal"
    height = (
        max(240, 80 + 30 * len({row[prepared["x"]] for row in prepared["rows"]}))
        if horizontal
        else 380
    )
    colors = PALETTE[: max(1, len(prepared["seriesValues"]))]
    data = {
        "spec": spec,
        "prepared": {key: prepared[key] for key in ("x", "y", "series", "xType", "seriesValues")},
        "colors": colors,
        "background": BACKGROUND,
        "rows": prepared["rows"],
    }
    subtitle = text_at(spec, "subtitle")
    source = text_at(spec, "source")
    replacements = {
        "__TITLE__": html.escape(spec["title"].strip()),
        "__SUBTITLE__": f'<p class="subtitle">{html.escape(subtitle)}</p>' if subtitle else "",
        "__SUMMARY__": html.escape(spec["summary"].strip()),
        "__SOURCE__": f'<p class="source">Source: {html.escape(source)}</p>' if source else "",
        "__TABLE__": table_html(spec, prepared),
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
    wanted = {"x", "y", "series", "xType", "seriesValues", "rows"}
    if not isinstance(spec, dict) or not isinstance(prepared, dict) or not wanted <= set(prepared):
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
