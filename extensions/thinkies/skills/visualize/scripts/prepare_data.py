#!/usr/bin/env python3
"""Shape and validate data before it reaches a chart.

Reads CSV, TSV, or JSON rows, keeps the named fields, converts each value to its
type, and writes prepared data as JSON. Writes nothing and exits 1 when a value
would make the chart misstate the data.

  prepare_data.py INPUT --x FIELD --y FIELD [--series FIELD]
                  [--x-type category|number|date] [--drop-missing] --out OUT.json

  prepare_data.py LINKS --shape sankey --source FIELD --target FIELD --value FIELD
                  [--nodes NODES] [--node-id FIELD] [--node-label FIELD] --out OUT.json

  prepare_data.py LINKS --shape network --source FIELD --target FIELD [--value FIELD]
                  [--nodes NODES] [--node-id FIELD] [--node-label FIELD]
                  [--node-group FIELD] --out OUT.json

  prepare_data.py INPUT --shape choropleth --region FIELD --value FIELD
                  [--geojson FILE [--feature-id PROPERTY] [--feature-name PROPERTY]]
                  --out OUT.json

LINKS holds one row per link. NODES holds one row per node; without it the nodes
are the names the links use. A choropleth joins each row to a country of the
bundled world atlas by its name or ISO 3166-1 numeric code, or to a feature of
the GeoJSON file by the named property. The GeoJSON holds polygons in longitude
and latitude.

Exit codes: 0 prepared, 1 problems found, 2 unusable arguments or input.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from datetime import date, datetime
from pathlib import Path

X_TYPES = ("category", "number", "date")
SHAPES = ("rows", "sankey", "network", "choropleth")
ATLAS = Path(__file__).resolve().parent.parent / "assets" / "world-atlas-countries-110m.json"
GROUPED_NUMBER = re.compile(r"^-?\d{1,3}(,\d{3})+(\.\d+)?$")
YEAR_MONTH = re.compile(r"^\d{4}-\d{2}$")


class Unusable(Exception):
    """The arguments or the input file cannot be read at all."""


def read_rows(path: Path) -> list:
    suffix = path.suffix.lower()
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as error:
        raise Unusable(f"cannot read {path}: {error.strerror}")
    if suffix in (".csv", ".tsv"):
        delimiter = "\t" if suffix == ".tsv" else ","
        return list(csv.DictReader(text.splitlines(), delimiter=delimiter))
    if suffix == ".json":
        try:
            loaded = json.loads(text)
        except json.JSONDecodeError as error:
            raise Unusable(f"{path} is not valid JSON: {error}")
        rows = loaded.get("rows") if isinstance(loaded, dict) else loaded
        if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
            raise Unusable(f"{path} must hold a list of objects, or an object with a 'rows' list")
        return rows
    raise Unusable(f"{path} has an unsupported extension; use .csv, .tsv, or .json")


def is_missing(value) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == "")


def to_number(value):
    """Return a finite float or int, or None when the value is not a plain number."""
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value if math.isfinite(value) else None
    text = str(value).strip()
    if GROUPED_NUMBER.match(text):
        text = text.replace(",", "")
    try:
        number = float(text)
    except ValueError:
        return None
    if not math.isfinite(number):
        return None
    return (
        int(number)
        if number.is_integer() and "." not in text and "e" not in text.lower()
        else number
    )


def to_date(value):
    """Return an ISO date or date-time string, or None when the value is not ISO 8601."""
    if isinstance(value, (int, float)):
        return None
    text = str(value).strip()
    if YEAR_MONTH.match(text):
        text += "-01"
    try:
        if len(text) == 10:
            return date.fromisoformat(text).isoformat()
        return datetime.fromisoformat(text.replace("Z", "+00:00")).isoformat()
    except ValueError:
        return None


def infer_x_type(values: list) -> str:
    if all(to_number(value) is not None for value in values):
        return "number"
    if all(to_date(value) is not None for value in values):
        return "date"
    return "category"


def prepare(rows: list, x: str, y: str, series, x_type, drop_missing: bool):
    """Return (prepared, problems, notes). `prepared` is None when problems exist."""
    problems: list = []
    notes: list = []
    fields = [field for field in (x, y, series) if field]

    if not rows:
        return None, [("empty", "the input holds no rows")], notes
    known = set().union(*(row.keys() for row in rows))
    for field in fields:
        if field not in known:
            problems.append(
                ("missing-field", f"no column named {field!r}; columns are {sorted(known)}")
            )
    if problems:
        return None, problems, notes

    kept = []
    dropped = 0
    for index, row in enumerate(rows, start=1):
        absent = [field for field in fields if is_missing(row.get(field))]
        if not absent:
            kept.append((index, row))
        elif drop_missing:
            dropped += 1
        else:
            problems.append(("missing-value", f"row {index} has no value for {absent}"))
    if dropped:
        notes.append(
            ("dropped-rows", f"dropped {dropped} of {len(rows)} rows with a missing value")
        )
    if not kept and not problems:
        problems.append(("empty", "no row has a value in every named column"))
    if problems:
        return None, problems, notes

    resolved_type = x_type or infer_x_type([row[x] for _, row in kept])
    convert_x = {
        "number": to_number,
        "date": to_date,
        "category": lambda value: str(value).strip(),
    }[resolved_type]
    x_code = "not-a-date" if resolved_type == "date" else "not-a-number"

    prepared_rows = []
    seen: dict = {}
    for index, row in kept:
        x_value = convert_x(row[x])
        y_value = to_number(row[y])
        if x_value is None:
            problems.append(
                (x_code, f"row {index}: {x} is {row[x]!r}, which is not a {resolved_type}")
            )
        if y_value is None:
            problems.append(
                (
                    "not-a-number",
                    f"row {index}: {y} is {row[y]!r}; strip units and symbols from the value",
                )
            )
        if x_value is None or y_value is None:
            continue
        out = {x: x_value, y: y_value}
        if series:
            out[series] = str(row[series]).strip()
        key = (x_value, out.get(series))
        if key in seen:
            problems.append(
                (
                    "duplicate-key",
                    f"rows {seen[key]} and {index} share {x}={x_value!r}"
                    + (f" and {series}={out[series]!r}" if series else "")
                    + "; decide how they aggregate before charting",
                )
            )
        else:
            seen[key] = index
        prepared_rows.append(out)
    if problems:
        return None, problems, notes

    if resolved_type in ("number", "date"):
        ordered = sorted(prepared_rows, key=lambda row: row[x])
        if ordered != prepared_rows:
            notes.append(("sorted", f"sorted rows by {x}"))
        prepared_rows = ordered

    values = [row[y] for row in prepared_rows]
    if min(values) < 0:
        notes.append(("negative-values", f"{y} goes below zero; a stacked chart cannot show it"))
    if min(values) == max(values):
        notes.append(("constant", f"every {y} equals {values[0]}"))
    series_values = []
    if series:
        for row in prepared_rows:
            if row[series] not in series_values:
                series_values.append(row[series])

    prepared = {
        "shape": "rows",
        "x": x,
        "y": y,
        "series": series,
        "xType": resolved_type,
        "seriesValues": series_values,
        "rows": prepared_rows,
    }
    notes.insert(
        0,
        (
            "summary",
            f"{len(prepared_rows)} rows; {x} is {resolved_type}; "
            f"{y} runs {min(values)} to {max(values)}"
            + (f"; {len(series_values)} series in {series}" if series else ""),
        ),
    )
    return prepared, problems, notes


def find_cycle(nodes: list, links: list):
    """Return one node id on a directed cycle, or None when the links form none."""
    waiting = {node["id"]: 0 for node in nodes}
    for link in links:
        waiting[link["target"]] += 1
    ready = [node_id for node_id, count in waiting.items() if count == 0]
    while ready:
        node_id = ready.pop()
        del waiting[node_id]
        for link in links:
            if link["source"] == node_id:
                waiting[link["target"]] -= 1
                if waiting[link["target"]] == 0:
                    ready.append(link["target"])
    return next(iter(waiting), None)


def prepare_graph(shape: str, link_rows: list, node_rows, fields: dict):
    """Return (prepared, problems, notes) for a sankey or a network."""
    problems: list = []
    notes: list = []
    source, target, value = fields["source"], fields["target"], fields["value"]
    node_id, node_label, node_group = fields["id"], fields["label"], fields["group"]
    directed = shape == "sankey"

    if not link_rows:
        return None, [("empty", "the links file holds no rows")], notes
    known = set().union(*(row.keys() for row in link_rows))
    for field in (source, target, value):
        if field and field not in known:
            problems.append(
                ("missing-field", f"no link column named {field!r}; columns are {sorted(known)}")
            )
    if node_rows is not None:
        node_known = set().union(*(row.keys() for row in node_rows)) if node_rows else set()
        for field in (node_id, node_label, node_group):
            if field and field not in node_known:
                problems.append(
                    (
                        "missing-field",
                        f"no node column named {field!r}; columns are {sorted(node_known)}",
                    )
                )
    if problems:
        return None, problems, notes

    nodes: list = []
    by_id: dict = {}
    if node_rows is not None:
        for index, row in enumerate(node_rows, start=1):
            if is_missing(row.get(node_id)):
                problems.append(("missing-value", f"node row {index} has no value for {node_id}"))
                continue
            key = str(row[node_id]).strip()
            if key in by_id:
                problems.append(("duplicate-node", f"node row {index} repeats {node_id}={key!r}"))
                continue
            label = row.get(node_label) if node_label else None
            node = {"id": key, "label": key if is_missing(label) else str(label).strip()}
            if node_group:
                if is_missing(row.get(node_group)):
                    problems.append(
                        ("missing-value", f"node row {index} has no value for {node_group}")
                    )
                    continue
                node["group"] = str(row[node_group]).strip()
            by_id[key] = node
            nodes.append(node)

    links: list = []
    seen: dict = {}
    for index, row in enumerate(link_rows, start=1):
        absent = [
            field for field in (source, target, value) if field and is_missing(row.get(field))
        ]
        if absent:
            problems.append(("missing-value", f"link row {index} has no value for {absent}"))
            continue
        ends = [str(row[source]).strip(), str(row[target]).strip()]
        link = {"source": ends[0], "target": ends[1]}
        usable = True
        for end in ends:
            if end in by_id:
                continue
            if node_rows is None:
                by_id[end] = {"id": end, "label": end}
                nodes.append(by_id[end])
            else:
                problems.append(
                    ("unknown-node", f"link row {index} names {end!r}, which the nodes file lacks")
                )
                usable = False
        if ends[0] == ends[1]:
            problems.append(("self-link", f"link row {index} joins {ends[0]!r} to itself"))
            usable = False
        if value:
            number = to_number(row[value])
            if number is None:
                problems.append(
                    (
                        "not-a-number",
                        f"link row {index}: {value} is {row[value]!r}; strip units and symbols",
                    )
                )
                usable = False
            elif number <= 0:
                problems.append(
                    (
                        "not-positive",
                        f"link row {index}: {value} is {number}; a link needs a value above zero",
                    )
                )
                usable = False
            else:
                link["value"] = number
        key = tuple(ends) if directed else tuple(sorted(ends))
        if key in seen:
            problems.append(
                (
                    "duplicate-key",
                    f"link rows {seen[key]} and {index} join the same two nodes; "
                    "decide how they aggregate before charting",
                )
            )
            usable = False
        else:
            seen[key] = index
        if usable:
            links.append(link)
    if problems:
        return None, problems, notes

    linked = {end for link in links for end in (link["source"], link["target"])}
    alone = [node["id"] for node in nodes if node["id"] not in linked]
    if directed:
        for name in alone:
            problems.append(("unlinked-node", f"node {name!r} has no link, so no flow reaches it"))
        on_cycle = find_cycle(nodes, links)
        if on_cycle is not None:
            problems.append(
                (
                    "cycle",
                    f"the links loop back through {on_cycle!r}; a sankey needs flow in one direction",
                )
            )
        for node in nodes:
            inflow = sum(link["value"] for link in links if link["target"] == node["id"])
            outflow = sum(link["value"] for link in links if link["source"] == node["id"])
            if inflow and outflow and abs(inflow - outflow) > 1e-9 * max(inflow, outflow):
                problems.append(
                    (
                        "unbalanced-node",
                        f"node {node['id']!r} takes in {inflow:g} and sends out {outflow:g}; "
                        "add the missing flow or name where the difference goes",
                    )
                )
    elif alone:
        notes.append(("unlinked-nodes", f"{len(alone)} nodes have no link: {alone}"))
    if problems:
        return None, problems, notes

    group_values: list = []
    for node in nodes:
        if "group" in node and node["group"] not in group_values:
            group_values.append(node["group"])
    prepared = {
        "shape": shape,
        "weighted": bool(value),
        "groupValues": group_values,
        "nodes": nodes,
        "links": links,
    }
    summary = f"{len(nodes)} nodes; {len(links)} links"
    if value:
        values = [link["value"] for link in links]
        summary += f"; {value} runs {min(values)} to {max(values)}"
    if group_values:
        summary += f"; {len(group_values)} groups in {node_group}"
    notes.insert(0, ("summary", summary))
    return prepared, problems, notes


def ring_is_counterclockwise(ring: list) -> bool:
    """Whether a closed ring of [longitude, latitude] positions runs counterclockwise."""
    return sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(ring, ring[1:])) > 0


def rewind(geometry: dict) -> int:
    """Wind outer rings clockwise and holes counterclockwise, as a spherical projection reads them.

    Returns the count of rings reversed.
    """
    polygons = (
        [geometry["coordinates"]] if geometry["type"] == "Polygon" else geometry["coordinates"]
    )
    reversed_rings = 0
    for polygon in polygons:
        for index, ring in enumerate(polygon):
            if ring_is_counterclockwise(ring) == (index == 0):
                ring.reverse()
                reversed_rings += 1
    return reversed_rings


def read_features(path: Path, id_property, name_property):
    """Return (features keyed for the join, problems, notes) from a GeoJSON file."""
    try:
        loaded = json.loads(path.read_text(encoding="utf-8-sig"))
    except OSError as error:
        raise Unusable(f"cannot read {path}: {error.strerror}")
    except json.JSONDecodeError as error:
        raise Unusable(f"{path} is not valid JSON: {error}")
    features = loaded.get("features") if isinstance(loaded, dict) else None
    if not isinstance(features, list) or not features:
        raise Unusable(f"{path} must be a GeoJSON FeatureCollection with features")

    problems: list = []
    notes: list = []
    kept: list = []
    seen: set = set()
    rewound = 0
    for index, feature in enumerate(features, start=1):
        properties = feature.get("properties") or {}
        geometry = feature.get("geometry") or {}
        key = properties.get(id_property) if id_property else feature.get("id")
        if is_missing(key):
            problems.append(
                ("missing-value", f"feature {index} has no {id_property or 'id'} to join on")
            )
            continue
        key = str(key).strip()
        if key in seen:
            problems.append(("duplicate-region", f"feature {index} repeats the key {key!r}"))
            continue
        seen.add(key)
        if geometry.get("type") not in ("Polygon", "MultiPolygon"):
            problems.append(
                (
                    "not-a-region",
                    f"feature {key!r} is a {geometry.get('type')}; a choropleth fills polygons",
                )
            )
            continue
        try:
            rewound += rewind(geometry)
        except (TypeError, IndexError, KeyError) as error:
            problems.append(
                (
                    "not-a-region",
                    f"feature {key!r} has unreadable coordinates: {type(error).__name__}",
                )
            )
            continue
        name = properties.get(name_property) if name_property else None
        kept.append(
            {
                "type": "Feature",
                "id": key,
                "properties": {"name": key if is_missing(name) else str(name).strip()},
                "geometry": geometry,
            }
        )
    if rewound:
        notes.append(("rewound", f"reversed {rewound} rings to the winding the projection reads"))
    return kept, problems, notes


def prepare_choropleth(rows: list, region: str, value: str, features):
    """Return (prepared, problems, notes). `features` is None for the bundled world atlas."""
    problems: list = []
    notes: list = []
    if not rows:
        return None, [("empty", "the input holds no rows")], notes
    known = set().union(*(row.keys() for row in rows))
    for field in (region, value):
        if field not in known:
            problems.append(
                ("missing-field", f"no column named {field!r}; columns are {sorted(known)}")
            )
    if problems:
        return None, problems, notes

    names: dict = {}
    lookup: dict = {}
    if features is None:
        for entry in json.loads(ATLAS.read_text(encoding="utf-8"))["regions"]:
            names[entry["name"]] = entry["name"]
            lookup[entry["name"].casefold()] = entry["name"]
            if entry["id"]:
                lookup[entry["id"]] = entry["name"]
                lookup[entry["id"].lstrip("0")] = entry["name"]
    else:
        for feature in features:
            names[feature["id"]] = feature["properties"]["name"]
            lookup[feature["id"]] = feature["id"]
            lookup[feature["id"].casefold()] = feature["id"]

    regions: list = []
    seen: dict = {}
    for index, row in enumerate(rows, start=1):
        absent = [field for field in (region, value) if is_missing(row.get(field))]
        if absent:
            problems.append(("missing-value", f"row {index} has no value for {absent}"))
            continue
        given = str(row[region]).strip()
        key = lookup.get(given) or lookup.get(given.casefold())
        number = to_number(row[value])
        if key is None:
            problems.append(
                (
                    "unknown-region",
                    f"row {index}: {given!r} matches no region of the "
                    + ("world atlas" if features is None else "GeoJSON file"),
                )
            )
        if number is None:
            problems.append(
                (
                    "not-a-number",
                    f"row {index}: {value} is {row[value]!r}; strip units and symbols from the value",
                )
            )
        if key is None or number is None:
            continue
        if key in seen:
            problems.append(
                (
                    "duplicate-key",
                    f"rows {seen[key]} and {index} both give a value for {key!r}; "
                    "decide how they aggregate before charting",
                )
            )
            continue
        seen[key] = index
        regions.append({"key": key, "label": names[key], "value": number})
    if problems:
        return None, problems, notes

    values = [entry["value"] for entry in regions]
    if min(values) == max(values):
        notes.append(("constant", f"every {value} equals {values[0]}; the map shows one colour"))
    without = len(names) - len(regions)
    if without:
        notes.append(("regions-without-value", f"{without} of {len(names)} regions have no value"))
    regions.sort(key=lambda entry: -entry["value"])
    prepared = {
        "shape": "choropleth",
        "atlas": "world" if features is None else None,
        "regionsWithoutValue": without,
        "regions": regions,
        "features": features,
    }
    notes.insert(
        0,
        (
            "summary",
            f"{len(regions)} regions; {value} runs {min(values)} to {max(values)}",
        ),
    )
    return prepared, problems, notes


def main(argv: list) -> int:
    parser = argparse.ArgumentParser(
        description="Shape and validate data before it reaches a chart."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("--shape", choices=SHAPES, default="rows")
    parser.add_argument("--x", help="column for the horizontal position or the category")
    parser.add_argument("--y", help="column holding the measured number")
    parser.add_argument("--source", help="link column naming the node a link leaves")
    parser.add_argument("--target", help="link column naming the node a link enters")
    parser.add_argument("--value", help="link column holding the size of the link")
    parser.add_argument("--nodes", type=Path, help="file with one row per node")
    parser.add_argument("--node-id", default="id", help="node column the links refer to")
    parser.add_argument("--node-label", help="node column holding the name to show")
    parser.add_argument("--node-group", help="node column that groups nodes by colour")
    parser.add_argument("--region", help="column naming the region a row belongs to")
    parser.add_argument("--geojson", type=Path, help="GeoJSON regions, in place of the world atlas")
    parser.add_argument("--feature-id", help="GeoJSON property the region column matches")
    parser.add_argument("--feature-name", help="GeoJSON property holding the name to show")
    parser.add_argument("--series", help="column that splits rows into series")
    parser.add_argument(
        "--x-type", choices=X_TYPES, help="override the inferred type of the x column"
    )
    parser.add_argument(
        "--drop-missing",
        action="store_true",
        help="drop rows with a missing value and report the count",
    )
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)
    needed = {
        "rows": ("x", "y"),
        "sankey": ("source", "target", "value"),
        "network": ("source", "target"),
        "choropleth": ("region", "value"),
    }[args.shape]
    absent = [f"--{name}" for name in needed if not getattr(args, name)]
    if absent:
        parser.error(f"--shape {args.shape} needs {', '.join(absent)}")
    if args.shape == "sankey" and args.node_group:
        parser.error("--node-group applies to --shape network")
    if (args.node_label or args.node_group) and not args.nodes:
        parser.error("--node-label and --node-group read the file --nodes names")

    if (args.feature_id or args.feature_name) and not args.geojson:
        parser.error("--feature-id and --feature-name read the file --geojson names")

    features, feature_problems, feature_notes = None, [], []
    try:
        rows = read_rows(args.input)
        node_rows = read_rows(args.nodes) if args.nodes else None
        if args.geojson:
            features, feature_problems, feature_notes = read_features(
                args.geojson, args.feature_id, args.feature_name
            )
    except Unusable as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    if args.shape == "choropleth":
        prepared, problems, notes = prepare_choropleth(rows, args.region, args.value, features)
        problems = feature_problems + problems
        notes = notes[:1] + feature_notes + notes[1:]
    elif args.shape == "rows":
        prepared, problems, notes = prepare(
            rows, args.x, args.y, args.series, args.x_type, args.drop_missing
        )
    else:
        fields = {
            "source": args.source,
            "target": args.target,
            "value": args.value,
            "id": args.node_id,
            "label": args.node_label,
            "group": args.node_group,
        }
        prepared, problems, notes = prepare_graph(args.shape, rows, node_rows, fields)
    for code, message in notes:
        print(f"note: {code}: {message}")
    if problems:
        for code, message in problems:
            print(f"problem: {code}: {message}")
        return 1
    args.out.write_text(json.dumps(prepared, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
