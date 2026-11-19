#!/usr/bin/env python3
"""Check a finished visualization before it is handed over.

Reads each HTML chart page or Markdown file and reports every defect that would
leave a reader without the chart, its values, or its meaning.

  check_output.py PATH [PATH ...]

Prints one `path: code: message` line per defect, or `path: ok`.
Exit codes: 0 no defect, 1 defects found, 2 a path cannot be read or checked.
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

from build_page import CDN_BASE, CHARTS_PACKAGE, CHARTS_VERSION, MAP_URLS
from prepare_data import ATLAS

# Colour-vision-deficiency simulation matrices at full severity, applied to linear RGB:
# https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html
CVD_MATRICES = {
    "protanopia": (
        (0.152286, 1.052583, -0.204868),
        (0.114503, 0.786281, 0.099216),
        (-0.003882, -0.048116, 1.051998),
    ),
    "deuteranopia": (
        (0.367322, 0.860646, -0.227968),
        (0.280085, 0.672501, 0.047413),
        (-0.011820, 0.042940, 0.968881),
    ),
    "tritanopia": (
        (1.255528, -0.076749, -0.178779),
        (-0.078411, 0.930809, 0.147602),
        (0.004733, 0.691367, 0.303900),
    ),
}
MIN_COLOR_DISTANCE = 12.0
MIN_GRAPHIC_CONTRAST = 3.0
MIN_RAMP_LIGHTNESS_SPAN = 40.0

MERMAID_TYPES = {
    "flowchart",
    "graph",
    "sequenceDiagram",
    "classDiagram",
    "stateDiagram",
    "stateDiagram-v2",
    "erDiagram",
    "journey",
    "gantt",
    "pie",
    "quadrantChart",
    "requirementDiagram",
    "gitGraph",
    "mindmap",
    "timeline",
    "sankey-beta",
    "xychart-beta",
    "block-beta",
    "C4Context",
}
BAR_LINE = re.compile(r"^(?P<label>.*?\S)\s+(?P<bar>█+[▏▎▍▌▋▊▉]?|[▏▎▍▌▋▊▉])\s+(?P<rest>\S.*)$")
PARTIAL_BLOCKS = "▏▎▍▌▋▊▉"
NUMBER = re.compile(r"-?\d[\d,]*(?:\.\d+)?")
IMPORT = re.compile(
    r"""import\s*\(\s*['"]([^'"]+)['"]\s*\)|(?:^|[\s;])import\s[^'"();]*?['"]([^'"]+)['"]""", re.M
)
FETCH = re.compile(r"""fetch\s*\(\s*['"]([^'"]+)['"]""")
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")


def linear_rgb(hex_color: str) -> tuple:
    channels = (int(hex_color[i : i + 2], 16) / 255 for i in (1, 3, 5))
    return tuple(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels)


def contrast_ratio(first: str, second: str) -> float:
    """WCAG contrast ratio: https://www.w3.org/TR/WCAG22/#dfn-contrast-ratio"""

    def luminance(hex_color: str) -> float:
        r, g, b = linear_rgb(hex_color)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    lighter, darker = sorted((luminance(first), luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def lab(rgb: tuple) -> tuple:
    """CIE L*a*b* under D65 from linear sRGB."""
    r, g, b = (min(1.0, max(0.0, c)) for c in rgb)
    xyz = (
        (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047,
        0.2126729 * r + 0.7151522 * g + 0.0721750 * b,
        (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883,
    )
    fx, fy, fz = (t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116 for t in xyz)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def color_distance(first: str, second: str, matrix=None) -> float:
    """Euclidean distance in L*a*b*, after simulating a colour-vision deficiency when given."""

    def seen(hex_color: str) -> tuple:
        rgb = linear_rgb(hex_color)
        if matrix:
            rgb = tuple(sum(m * c for m, c in zip(row, rgb)) for row in matrix)
        return lab(rgb)

    return sum((a - b) ** 2 for a, b in zip(seen(first), seen(second))) ** 0.5


def color_defects(colors: list, background: str) -> list:
    defects = []
    for color in colors:
        ratio = contrast_ratio(color, background)
        if ratio < MIN_GRAPHIC_CONTRAST:
            defects.append(
                (
                    "color-low-contrast",
                    f"{color} has contrast {ratio:.2f}:1 on {background}; marks need {MIN_GRAPHIC_CONTRAST:g}:1",
                )
            )
    for i, first in enumerate(colors):
        for second in colors[i + 1 :]:
            views = [("typical vision", None)] + list(CVD_MATRICES.items())
            name, distance = min(
                ((name, color_distance(first, second, matrix)) for name, matrix in views),
                key=lambda pair: pair[1],
            )
            if distance < MIN_COLOR_DISTANCE:
                defects.append(
                    (
                        "color-confusable",
                        f"{first} and {second} sit {distance:.1f} apart under {name}; "
                        f"series colours need {MIN_COLOR_DISTANCE:g}",
                    )
                )
    return defects


class PageReader(HTMLParser):
    """Collects the parts of a chart page the checks read."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.ids: dict = {}
        self.text: dict = {"title": "", "h1": "", "viz-summary": ""}
        self.external: list = []
        self.scripts: list = []
        self.header_cells: list = []
        self.unscoped_headers = 0
        self.body_rows = 0
        self.tables = 0
        self.captions = 0
        self._open: list = []
        self._script = None
        self._in_tbody = False
        self._in_thead = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = (attrs.get("lang") or "").strip()
        if attrs.get("id"):
            self.ids[attrs["id"]] = tag
        for name in ("src", "href", "poster", "data"):
            value = attrs.get(name) or ""
            if tag != "a" and re.match(r"(?:https?:)?//", value):
                self.external.append(f"<{tag} {name}={value!r}>")
        if tag == "script":
            self._script = {
                "type": attrs.get("type", ""),
                "id": attrs.get("id", ""),
                "src": attrs.get("src"),
                "text": "",
            }
            if attrs.get("src") and not re.match(r"(?:https?:)?//", attrs["src"]):
                self.external.append(f"<script src={attrs['src']!r}>")
        elif tag == "table":
            self.tables += 1
        elif tag == "caption":
            self.captions += 1
        elif tag == "thead":
            self._in_thead = True
        elif tag == "tbody":
            self._in_tbody = True
        elif tag == "tr" and self._in_tbody:
            self.body_rows += 1
        elif tag == "th" and self._in_thead:
            self.header_cells.append("")
            if attrs.get("scope") != "col":
                self.unscoped_headers += 1
        key = "viz-summary" if attrs.get("id") == "viz-summary" else tag
        if key in self.text or (tag == "th" and self._in_thead):
            self._open.append((tag, key))

    def handle_endtag(self, tag):
        if tag == "script" and self._script is not None:
            self.scripts.append(self._script)
            self._script = None
        elif tag == "thead":
            self._in_thead = False
        elif tag == "tbody":
            self._in_tbody = False
        if self._open and self._open[-1][0] == tag:
            self._open.pop()

    def handle_data(self, data):
        if self._script is not None:
            self._script["text"] += data
            return
        for tag, key in self._open:
            if tag == "th":
                self.header_cells[-1] += data
            else:
                self.text[key] += data


def check_html(text: str) -> list:
    page = PageReader()
    page.feed(text)
    defects = []

    def need(present, code: str, message: str) -> None:
        if not present:
            defects.append((code, message))

    need(page.lang, "no-lang", "the html element has no lang attribute")
    need(page.text["title"].strip(), "no-title", "the page has no title")
    need(page.text["h1"].strip(), "no-heading", "the page has no h1 stating what the chart shows")
    need(page.text["viz-summary"].strip(), "no-summary", "no text summary with id viz-summary")
    need("viz-chart" in page.ids, "no-mount", "no element with id viz-chart for the chart")
    need(
        "viz-status" in page.ids,
        "no-status",
        "no element with id viz-status to report a failed load",
    )

    for found in page.external:
        defects.append(("external-resource", f"{found} loads a file from outside the page"))

    shape = None
    data_scripts = [s for s in page.scripts if s["id"] == "viz-data"]
    if data_scripts:
        try:
            loaded = json.loads(data_scripts[0]["text"])
        except ValueError:
            loaded = None
        shape = loaded.get("shape") if isinstance(loaded, dict) else None
    map_urls = set(MAP_URLS.values()) if shape == "choropleth" else set()

    code = "\n".join(s["text"] for s in page.scripts if s["type"] == "module" and not s["src"])
    specifiers = [a or b for a, b in IMPORT.findall(code)]
    for specifier in specifiers + FETCH.findall(code):
        if specifier == CDN_BASE or specifier.startswith(CDN_BASE + "/"):
            continue
        if specifier in map_urls:
            continue
        if CHARTS_PACKAGE in specifier:
            defects.append(
                (
                    "unpinned-import",
                    f"{specifier!r} is not pinned to {CHARTS_PACKAGE}@{CHARTS_VERSION}",
                )
            )
        else:
            defects.append(
                ("foreign-import", f"{specifier!r} is not a file this kind of page may load")
            )
    need(specifiers, "no-chart-import", "no module script imports the chart library")
    need("ariaLabel" in code, "no-aria-label", "the chart is mounted without an ariaLabel")

    rows = None
    tables_wanted = 1
    if not data_scripts:
        defects.append(("no-data", "no script with id viz-data holds the data"))
    else:
        try:
            data = json.loads(data_scripts[0]["text"])
            graph = data["shape"] in ("sankey", "network")
            choropleth = data["shape"] == "choropleth"
            if graph:
                rows = data["nodes"] + data["links"]
            else:
                rows = data["regions"] if choropleth else data["rows"]
            colors, background = data["colors"], data["background"]
            unit = data["unit"]
            unit_wanted = data["prepared"]["weighted"] if graph else True
            if not rows or not isinstance(rows, list):
                raise ValueError("the data is empty")
            if not all(isinstance(c, str) and HEX.match(c) for c in colors + [background]):
                raise ValueError("colors and background must be six-digit hex")
            if choropleth:
                ramp = data["ramp"]
                if len(ramp) != 2 or not all(isinstance(c, str) and HEX.match(c) for c in ramp):
                    raise ValueError("ramp must hold two six-digit hex colours")
                span = lab(linear_rgb(ramp[0]))[0] - lab(linear_rgb(ramp[1]))[0]
                if span < MIN_RAMP_LIGHTNESS_SPAN:
                    defects.append(
                        (
                            "ramp-flat",
                            f"the ramp runs {span:.0f} lightness steps from light to dark; "
                            f"a reader needs {MIN_RAMP_LIGHTNESS_SPAN:g} to rank regions",
                        )
                    )
                if data["features"] is None:
                    atlas = json.loads(ATLAS.read_text(encoding="utf-8"))
                    drawable = {region["name"] for region in atlas["regions"]}
                else:
                    drawable = {feature["id"] for feature in data["features"]}
                for region in rows:
                    if region["key"] not in drawable:
                        defects.append(
                            (
                                "region-unmatched",
                                f"no shape on the map has the key {region['key']!r}",
                            )
                        )
            if graph:
                tables_wanted = 2
                known = {node["id"] for node in data["nodes"]}
                for link in data["links"]:
                    for end in (link["source"], link["target"]):
                        if end not in known:
                            defects.append(
                                ("link-unknown-node", f"a link names {end!r}, which no node has")
                            )
        except (ValueError, KeyError, TypeError) as error:
            defects.append(("bad-data", f"viz-data is unusable: {error!r}"))
            rows = None
        else:
            defects.extend(color_defects(colors, background))
            named = isinstance(unit, str) and unit.strip()
            if unit_wanted:
                need(named, "no-unit", "viz-data names no unit for the values")
            if unit_wanted and named:
                need(
                    any(unit.strip().lower() in cell.lower() for cell in page.header_cells),
                    "no-unit",
                    f"no table header names the unit {unit!r}",
                )

    if page.tables < tables_wanted:
        defects.append(
            ("no-table", f"the page has {page.tables} data tables and needs {tables_wanted}")
        )
    else:
        need(page.captions >= page.tables, "table-no-caption", "a data table has no caption")
        need(page.unscoped_headers == 0, "table-no-scope", "a table header cell lacks scope=col")
        if rows is not None and page.body_rows != len(rows):
            defects.append(
                (
                    "table-row-mismatch",
                    f"the table has {page.body_rows} rows and the data has {len(rows)}",
                )
            )
    return defects


def fenced_blocks(text: str) -> list:
    """Return (info string, body lines) for each fenced code block."""
    blocks, current, fence = [], None, ""
    for line in text.splitlines():
        stripped = line.strip()
        opener = re.match(r"^(`{3,}|~{3,})\s*(\S*)", stripped)
        if current is None and opener:
            fence, current = opener.group(1), (opener.group(2), [])
        elif current is not None and stripped.startswith(fence) and stripped.strip(fence[0]) == "":
            blocks.append(current)
            current = None
        elif current is not None:
            current[1].append(line)
    return blocks


def balanced(source: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for char in re.sub(r'"[^"\n]*"', "", source):
        if char in "([{":
            stack.append(char)
        elif char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
    return not stack


def bar_defects(lines: list) -> list:
    bars = []
    for line in lines:
        match = BAR_LINE.match(line)
        number = NUMBER.search(match.group("rest")) if match else None
        if number:
            drawn = match.group("bar")
            length = drawn.count("█") + sum(
                (PARTIAL_BLOCKS.index(c) + 1) / 8 for c in drawn if c in PARTIAL_BLOCKS
            )
            bars.append((match.group("label"), length, float(number.group().replace(",", ""))))
    if len(bars) < 2:
        return []
    _, longest, largest = max(bars, key=lambda bar: bar[2])
    if largest <= 0:
        return []
    return [
        (
            "bar-not-proportional",
            f"{label!r} draws {length:g} blocks for {value:g}; in proportion it draws "
            f"{value / largest * longest:.1f}",
        )
        for label, length, value in bars
        if abs(length - value / largest * longest) > 1
    ]


def check_markdown(text: str) -> list:
    defects = []
    for info, lines in fenced_blocks(text):
        if info == "mermaid":
            body = [line for line in lines if line.strip() and not line.strip().startswith("%%")]
            keyword = body[0].split()[0] if body else ""
            if keyword not in MERMAID_TYPES:
                defects.append(("mermaid-unknown-type", f"a mermaid block opens with {keyword!r}"))
            if not balanced("\n".join(body)):
                defects.append(("mermaid-unbalanced", "a mermaid block has unbalanced brackets"))
        else:
            defects.extend(bar_defects(lines))

    outside = re.sub(r"(?ms)^(`{3,}|~{3,}).*?^\1\s*$", "", text)
    table: list = []
    for line in outside.splitlines() + [""]:
        if line.strip().startswith("|"):
            table.append(line.strip())
            continue
        if len(table) >= 2:
            widths = {len(re.split(r"(?<!\\)\|", row.strip("|"))) for row in table}
            if not re.match(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?$", table[1]):
                defects.append(
                    (
                        "table-no-separator",
                        f"the table starting {table[0][:40]!r} has no header separator",
                    )
                )
            elif len(widths) > 1:
                defects.append(
                    (
                        "table-ragged",
                        f"the table starting {table[0][:40]!r} has rows of differing widths",
                    )
                )
        table = []
    return defects


def check_file(path: Path) -> list:
    """Return (code, message) defects. Raises ValueError for a file this script cannot check."""
    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix in (".html", ".htm"):
        return check_html(text)
    if suffix in (".md", ".markdown"):
        return check_markdown(text)
    raise ValueError(f"{path.suffix or 'no'} extension; this script checks .html and .md")


def main(argv: list) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if argv else 2
    worst = 0
    for name in argv:
        path = Path(name)
        try:
            defects = check_file(path)
        except (OSError, ValueError, UnicodeDecodeError) as error:
            print(f"{path}: cannot check: {error}", file=sys.stderr)
            worst = 2
            continue
        if not defects:
            print(f"{path}: ok")
        for code, message in defects:
            print(f"{path}: {code}: {message}")
        if defects:
            worst = max(worst, 1)
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
