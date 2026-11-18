#!/usr/bin/env python3
"""Shape and validate rows before they reach a chart.

Reads CSV, TSV, or JSON rows, keeps the named fields, converts each value to its
type, and writes prepared rows as JSON. Writes nothing and exits 1 when a value
would make the chart misstate the data.

  prepare_data.py INPUT --x FIELD --y FIELD [--series FIELD]
                  [--x-type category|number|date] [--drop-missing] --out OUT.json

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


def main(argv: list) -> int:
    parser = argparse.ArgumentParser(
        description="Shape and validate rows before they reach a chart."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument(
        "--x", required=True, help="column for the horizontal position or the category"
    )
    parser.add_argument("--y", required=True, help="column holding the measured number")
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

    try:
        rows = read_rows(args.input)
    except Unusable as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    prepared, problems, notes = prepare(
        rows, args.x, args.y, args.series, args.x_type, args.drop_missing
    )
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
