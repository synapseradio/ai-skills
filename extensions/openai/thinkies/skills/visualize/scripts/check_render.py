#!/usr/bin/env python3
"""Optional static-analysis accelerator for the visualize skill's Phase 4.

This script reads a generated visualization artifact, detects which engine it
uses, and mechanically reports the render-blocking defects that the render-
inference pass looks for. It is an accelerator, never a gate: the prose protocol
is sufficient on its own, and this script's absence or failure must not block
verification. It opens no browser, takes no screenshot, and uses the Python
standard library only, so it runs wherever `python3` runs.

Engines and what each check covers:

  Vega (`.vg.json`, and the JSON embedded in the Vega wrapper HTML)
    - JSON well-formedness.
    - Length-mark (bar/area) baselines anchored at zero on the quantitative
      scale, so bar lengths stay proportional to their values.
    - Encoding `field` references cross-checked against the keys present in the
      bound inline data rows, so an encoding never points at an absent field.

  D3 (standalone template HTML)
    - The d3 CDN import is present.
    - A render call that binds data to marks is present.
    - A `<title>`/`<desc>` pair and a data-table `<details>` fallback are present.

  mermaid (`.md`/`.html`/`.html.tmpl` with a mermaid block)
    - The diagram source opens with a recognized diagram keyword.
    - Its brackets and braces are balanced (structural sanity only — this does
      not reimplement mermaid's grammar).
    - HTML bundles import mermaid.js and call `mermaid.initialize`/`mermaid.run`.

  Cross-engine HTML (applied to whichever engine emits HTML)
    - Scroll containment: a wheel/touchmove/zoom-pan handler or an
      `overflow`/`100vh` rule on the embed container that would hijack the host
      page's scroll.
    - Keyboard wiring: interactive marks (those carrying pointer/hover handlers)
      that lack `tabindex`, a key handler, and a visible focus style.

CLI:
  check_render.py <path> [<path> ...]

Behavior:
  - Prints each defect with its file and cause.
  - Exits non-zero when any render-blocking defect is found.
  - Degrades to a clear "not applicable" line and contributes nothing to a
    non-zero exit when an input is an unsupported type.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Defect severity. Only render-blocking defects influence the exit code; advisory
# defects are printed but never fail the run, matching the script's accelerator
# (never-a-gate) role.
SEVERITY_BLOCKING = "blocking"
SEVERITY_ADVISORY = "advisory"

# Mermaid diagram opening keywords recognized for the structural-sanity check.
# This is a recognition list, not a grammar: it answers "does the source open
# with a real mermaid diagram type" and nothing more.
MERMAID_DIAGRAM_KEYWORDS = (
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
)

# Vega mark types whose visual length encodes the quantitative value, so a non-
# zero baseline distorts the comparison the chart invites.
VEGA_LENGTH_MARK_TYPES = ("rect", "bar", "area")


@dataclass
class Defect:
    """One reported problem: a stable code, a human cause, and a severity."""

    code: str
    message: str
    severity: str = SEVERITY_BLOCKING


@dataclass
class CheckResult:
    """The outcome of checking one file."""

    path: Path
    engine: str | None = None
    applicable: bool = True
    defects: list[Defect] = field(default_factory=list)
    note: str | None = None

    def add(self, code: str, message: str, severity: str = SEVERITY_BLOCKING) -> None:
        self.defects.append(Defect(code=code, message=message, severity=severity))

    def has_render_blocking(self) -> bool:
        return any(d.severity == SEVERITY_BLOCKING for d in self.defects)


# --------------------------------------------------------------------------- #
# Engine detection
# --------------------------------------------------------------------------- #


def detect_engine(path: Path, text: str) -> str | None:
    """Decide which engine an artifact uses, or None when unsupported.

    Detection leans on the strongest available signal: the `.vg.json` extension
    and a Vega `$schema` for Vega, a mermaid block for mermaid, and a d3 import
    for D3. HTML that carries both a mermaid block and a d3 import is treated as
    mermaid, since the mermaid block is the rendered content.
    """
    suffix = path.suffix.lower()
    lowered = text.lower()

    if suffix == ".json" or path.name.endswith(".vg.json"):
        if '"$schema"' in text and "vega" in lowered:
            return "vega"
        # A bare .json that parses and carries Vega's marks/scales shape.
        if '"marks"' in text or '"scales"' in text:
            return "vega"
        return None

    is_html = (
        suffix in (".html", ".htm", ".tmpl") or "<html" in lowered or "<!doctype html" in lowered
    )
    is_markdown = suffix in (".md", ".markdown")

    has_mermaid_block = _has_mermaid_block(text)
    has_d3_import = _has_d3_import(text)
    has_vega_embed = "vegaembed(" in lowered or "vega-embed" in lowered

    # A mermaid block is the strongest signal: it is the rendered content even
    # when the page also carries a d3 import or other scaffolding.
    if has_mermaid_block:
        return "mermaid"

    # The skill stamps an `engine:` line into every artifact's frontmatter (an
    # HTML `<!-- ... -->` comment or a markdown `--- ... ---` block). Trust it as
    # the next signal, so a D3 artifact still classifies as D3 even when the very
    # defect under test is a missing CDN import.
    declared = _declared_engine(text)
    if declared in ("vega", "d3", "markdown"):
        # `markdown` frontmatter without a mermaid block is plain prose here; a
        # `markdown` engine artifact is only checkable when it carries a mermaid
        # diagram, which the has_mermaid_block branch already handled.
        if declared == "markdown":
            return None
        return declared

    if is_html and has_vega_embed:
        return "vega"
    if has_d3_import:
        return "d3"
    if is_markdown:
        # Markdown without a mermaid block is plain prose to this script.
        return None
    return None


def _declared_engine(text: str) -> str | None:
    """Read the `engine:` value from an artifact's frontmatter when present.

    Looks only at the head of the file so a stray `engine:` deeper in the body
    never masquerades as frontmatter.
    """
    head = text[:2000]
    match = re.search(r"(?mi)^\s*engine:\s*([A-Za-z0-9_-]+)\s*$", head)
    return match.group(1).lower() if match else None


def _has_mermaid_block(text: str) -> bool:
    """True when the text carries a mermaid diagram, in an HTML `pre.mermaid`
    element or a fenced ```mermaid block."""
    if re.search(r'<pre[^>]*class="[^"]*\bmermaid\b[^"]*"', text):
        return True
    if re.search(r"```+\s*mermaid", text):
        return True
    return False


def _has_d3_import(text: str) -> bool:
    """True when the artifact imports d3 from a CDN."""
    return bool(re.search(r"""(import[^\n]*\bd3\b[^\n]*cdn|cdn[^\n]*\bd3@)""", text, re.IGNORECASE))


def _is_html_artifact(path: Path, text: str) -> bool:
    """True when the artifact is an HTML document rather than markdown or JSON.

    A markdown source carrying a fenced mermaid block is not an HTML bundle, even
    when its filename ends in `.tmpl` (e.g. `mermaid-flowchart.md.tmpl`), so the
    HTML-bundle wiring and scroll/keyboard checks must not run on it.
    """
    name = path.name.lower()
    if name.endswith((".md", ".markdown", ".md.tmpl", ".markdown.tmpl")):
        return False
    if name.endswith((".html", ".htm", ".html.tmpl", ".htm.tmpl")):
        return True
    return bool(re.search(r"<html|<!doctype html", text, re.IGNORECASE))


# --------------------------------------------------------------------------- #
# Vega checks
# --------------------------------------------------------------------------- #


def check_vega(text: str, result: CheckResult, is_html: bool = False) -> None:
    spec_text = text
    if is_html:
        # An HTML wrapper embeds the spec as `const spec = { ... };`. Distribution
        # wrappers carry only a `{ /* placeholder */ }`; there is no real JSON to
        # check, so skip the JSON-dependent checks rather than reporting the whole
        # HTML page as malformed JSON. The cross-engine HTML checks still run.
        embedded = _extract_embedded_vega_spec(text)
        if embedded is None:
            return
        spec_text = embedded

    try:
        spec = json.loads(spec_text)
    except json.JSONDecodeError as exc:
        result.add(
            "vega-malformed-json",
            f"spec is not valid JSON: {exc.msg} at line {exc.lineno} column {exc.colno}",
        )
        return

    if not isinstance(spec, dict):
        result.add("vega-malformed-json", "top-level Vega spec is not a JSON object")
        return

    data_keys = _vega_inline_data_keys(spec)
    if data_keys is not None:
        # Transforms (pie, stack, treemap, formula, …) synthesize fields that are
        # absent from the raw inline rows but present at render time. Treat every
        # field a transform names or emits as available, so the missing-field
        # check flags only fields nothing in the spec ever produces.
        data_keys = data_keys | _vega_transform_fields(spec)
    _vega_check_baselines(spec, result)
    _vega_check_encoding_fields(spec, data_keys, result)


def _extract_embedded_vega_spec(text: str) -> str | None:
    """Pull the JSON object assigned to `const spec = { ... }` in a Vega wrapper.

    Returns the brace-balanced object text, or None when the wrapper carries only
    a comment placeholder (no concrete spec to check).
    """
    match = re.search(r"(?:const|let|var)\s+spec\s*=\s*\{", text)
    if not match:
        return None
    start = match.end() - 1  # position of the opening brace
    depth = 0
    in_quote: str | None = None
    escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_quote:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == in_quote:
                in_quote = None
            continue
        if ch in ('"', "'"):
            in_quote = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                body = text[start : i + 1]
                # A placeholder body holds only whitespace and a comment.
                inner = body[1:-1]
                stripped = re.sub(r"/\*.*?\*/", "", inner, flags=re.DOTALL).strip()
                if not stripped:
                    return None
                return body
    return None


def _vega_inline_data_keys(spec: dict) -> set[str] | None:
    """Collect the union of row keys across every inline `data[].values` array.

    Returns None when no inline rows exist (the spec loads data at runtime), in
    which case field cross-checking is skipped rather than guessed at.
    """
    keys: set[str] = set()
    found_inline = False
    for dataset in spec.get("data", []) or []:
        if not isinstance(dataset, dict):
            continue
        values = dataset.get("values")
        if isinstance(values, list) and values:
            for row in values:
                if isinstance(row, dict):
                    found_inline = True
                    keys.update(row.keys())
    return keys if found_inline else None


# Implicit output fields produced by Vega layout/structural transforms, keyed by
# transform type. These are not named via `as` yet appear as encoding fields, so
# the encoding-vs-data check must treat them as available.
VEGA_TRANSFORM_IMPLICIT_OUTPUTS = {
    "pie": ("startAngle", "endAngle"),
    "stack": ("y0", "y1"),
    "treemap": ("x0", "y0", "x1", "y1", "depth", "children"),
    "partition": ("x0", "y0", "x1", "y1", "depth", "children"),
    "pack": ("x", "y", "r", "depth", "children"),
    "tree": ("x", "y", "depth", "children"),
    "force": ("x", "y", "vx", "vy", "fx", "fy"),
    "kde": ("value", "density"),
    "stack-by-fields": (),
    "linkpath": ("path",),
    "geopath": ("path",),
    "geoshape": ("path",),
    "voronoi": ("path",),
    "contour": ("contour",),
}


def _vega_transform_fields(spec: dict) -> set[str]:
    """Collect every field name a data-level transform names or synthesizes.

    Gathers `as` outputs (string or list), the implicit outputs of recognized
    layout transforms, and the literal field tokens a transform references, so a
    transform-produced field is never mistaken for an absent data field.
    """
    produced: set[str] = set()

    def harvest(transforms) -> None:
        for tx in transforms or []:
            if not isinstance(tx, dict):
                continue
            produced.update(VEGA_TRANSFORM_IMPLICIT_OUTPUTS.get(tx.get("type"), ()))
            as_value = tx.get("as")
            if isinstance(as_value, str):
                produced.add(as_value)
            elif isinstance(as_value, list):
                produced.update(v for v in as_value if isinstance(v, str))
            # `field`/`fields`/`groupby` reference existing fields, but a transform
            # may also carry output names (e.g. window/aggregate ops); collecting
            # these string references keeps the check conservative.
            for key in ("field", "fields", "groupby", "key"):
                val = tx.get(key)
                if isinstance(val, str):
                    produced.add(val)
                elif isinstance(val, list):
                    produced.update(v for v in val if isinstance(v, str))

    # Data-level transforms (pie, stack, kde, aggregate, …).
    for dataset in spec.get("data", []) or []:
        if isinstance(dataset, dict):
            harvest(dataset.get("transform"))
    # Mark-level transforms (force, linkpath, …) synthesize per-mark fields too.
    for mark in _iter_vega_marks(spec):
        harvest(mark.get("transform"))
    return produced


def _vega_check_baselines(spec: dict, result: CheckResult) -> None:
    """Flag a length mark (bar/area) whose baseline-anchored axis omits zero.

    A true bar/area encodes magnitude as the distance from a fixed baseline: one
    end binds a data field, the other binds a literal `{"value": 0}`. When that
    pairing exists but the field's linear scale sets `"zero": false` (or a domain
    that never reaches zero), the bar foot drifts off the origin and lengths stop
    being proportional. A range rect — both ends bound to data fields, as in a
    box-plot IQR box or a candlestick body — claims no zero baseline and is left
    alone, since flagging it would be a false positive.
    """
    scales = {s.get("name"): s for s in spec.get("scales", []) or [] if isinstance(s, dict)}
    for mark in _iter_vega_marks(spec):
        if mark.get("type") not in VEGA_LENGTH_MARK_TYPES:
            continue
        for axis, baseline_channel in (("y", "y2"), ("x", "x2")):
            if _is_zero_anchored_length(mark, axis, baseline_channel):
                scale_name = _vega_channel_scale(mark, axis)
                scale = scales.get(scale_name)
                if scale and scale.get("type") == "linear" and _scale_excludes_zero(scale):
                    result.add(
                        "vega-nonzero-baseline",
                        f"{mark.get('type')} mark anchors channel '{axis}' to a zero "
                        f"baseline but its linear scale '{scale_name}' excludes zero; "
                        f"bar/area lengths will not be proportional to their values",
                    )
                    break


def _is_zero_anchored_length(mark: dict, value_channel: str, baseline_channel: str) -> bool:
    """True when one channel binds a data field and the paired channel binds a
    literal zero baseline — the signature of a bar/area drawn from the origin."""
    value_enc = _channel_encoding(mark, value_channel)
    baseline_enc = _channel_encoding(mark, baseline_channel)
    field_bound = isinstance(value_enc, dict) and isinstance(value_enc.get("field"), str)
    baseline_zero = (
        isinstance(baseline_enc, dict)
        and "field" not in baseline_enc
        and baseline_enc.get("value") in (0, 0.0)
    )
    return field_bound and baseline_zero


def _channel_encoding(mark: dict, channel: str):
    """Return the encoding dict for a channel from any encode block, or None."""
    encode = mark.get("encode")
    if not isinstance(encode, dict):
        return None
    for block in encode.values():
        if isinstance(block, dict) and isinstance(block.get(channel), dict):
            return block[channel]
    return None


def _scale_excludes_zero(scale: dict) -> bool:
    """A linear scale excludes zero when `"zero"` is explicitly false, or when a
    literal numeric domain neither starts nor ends at zero."""
    if scale.get("zero") is False:
        return True
    domain = scale.get("domain")
    if (
        isinstance(domain, list)
        and len(domain) == 2
        and all(isinstance(v, (int, float)) for v in domain)
    ):
        lo, hi = domain
        if lo > 0 or hi < 0:
            return True
    return False


def _vega_check_encoding_fields(
    spec: dict, data_keys: set[str] | None, result: CheckResult
) -> None:
    """Cross-check encoding `field` references against bound inline data keys."""
    if data_keys is None:
        return
    seen: set[str] = set()
    # Scale domains reference fields too; a domain field absent from the data
    # yields an empty or NaN scale, the same empty-render defect.
    for scale in spec.get("scales", []) or []:
        if not isinstance(scale, dict):
            continue
        domain = scale.get("domain")
        if isinstance(domain, dict) and isinstance(domain.get("field"), str):
            field_name = domain["field"]
            if field_name not in data_keys and field_name not in seen:
                seen.add(field_name)
                result.add(
                    "vega-missing-field",
                    f"scale '{scale.get('name')}' domain references field "
                    f"'{field_name}', absent from the bound data rows "
                    f"(present: {sorted(data_keys)})",
                )
    for mark in _iter_vega_marks(spec):
        encode = mark.get("encode")
        if not isinstance(encode, dict):
            continue
        for block in encode.values():
            if not isinstance(block, dict):
                continue
            for channel in block.values():
                field_name = _encoding_field(channel)
                if field_name and field_name not in data_keys and field_name not in seen:
                    seen.add(field_name)
                    result.add(
                        "vega-missing-field",
                        f"mark encoding references field '{field_name}', absent "
                        f"from the bound data rows (present: {sorted(data_keys)})",
                    )


def _encoding_field(channel) -> str | None:
    """Extract a plain `field` reference from an encoding channel.

    Ignores signal/expression references and dotted access like `datum.name` or
    nested-field objects, which name computed or scoped values rather than a
    top-level data row key.
    """
    if isinstance(channel, dict):
        f = channel.get("field")
        if isinstance(f, str) and "." not in f and "[" not in f:
            return f
    return None


def _vega_channel_scale(mark: dict, channel: str) -> str | None:
    encode = mark.get("encode")
    if not isinstance(encode, dict):
        return None
    for block in encode.values():
        if isinstance(block, dict) and isinstance(block.get(channel), dict):
            scale = block[channel].get("scale")
            if isinstance(scale, str):
                return scale
    return None


def _iter_vega_marks(spec: dict):
    """Yield every mark dict, descending into group marks."""
    stack = list(spec.get("marks", []) or [])
    while stack:
        mark = stack.pop()
        if not isinstance(mark, dict):
            continue
        yield mark
        nested = mark.get("marks")
        if isinstance(nested, list):
            stack.extend(nested)


# --------------------------------------------------------------------------- #
# D3 checks
# --------------------------------------------------------------------------- #


def check_d3(text: str, result: CheckResult) -> None:
    if not _has_d3_import(text):
        result.add(
            "d3-missing-cdn",
            "no d3 CDN import found; the chart cannot load its rendering library",
        )
    if not _has_render_call(text):
        result.add(
            "d3-missing-render-call",
            "no data-binding render call (e.g. .data(...).join(...)/.append(...)) "
            "found; the chart binds no marks",
        )
    if not _has_title_desc(text):
        result.add(
            "d3-missing-title-desc",
            "missing <title>/<desc> accessibility pair on the chart",
            severity=SEVERITY_ADVISORY,
        )
    if not _has_data_table_details(text):
        result.add(
            "d3-missing-data-table",
            "missing a data-table <details> fallback",
            severity=SEVERITY_ADVISORY,
        )


def _has_render_call(text: str) -> bool:
    """A d3 render binds data to marks. The canonical pattern is `.data(...)`
    paired with `.join(`/`.append(`/`.enter(`."""
    if ".data(" in text and re.search(r"\.(join|append|enter)\(", text):
        return True
    return False


def _has_title_desc(text: str) -> bool:
    return bool(re.search(r"<title\b", text, re.IGNORECASE)) and bool(
        re.search(r"<desc\b", text, re.IGNORECASE)
    )


def _has_data_table_details(text: str) -> bool:
    if not re.search(r"<details\b", text, re.IGNORECASE):
        return False
    return "data-table" in text.lower() or "datatable" in text.lower()


# --------------------------------------------------------------------------- #
# mermaid checks
# --------------------------------------------------------------------------- #


def check_mermaid(text: str, result: CheckResult, is_html: bool) -> None:
    source = _extract_mermaid_source(text)
    if source is None:
        result.add(
            "mermaid-missing-source",
            "no mermaid diagram source found in a pre.mermaid element or fenced block",
        )
    else:
        keyword = _mermaid_first_keyword(source)
        if keyword is None or not _is_recognized_mermaid_keyword(keyword):
            result.add(
                "mermaid-unknown-diagram",
                f"diagram source does not open with a recognized mermaid diagram "
                f"type (saw: {keyword!r})",
            )
        if not _brackets_balanced(source):
            result.add(
                "mermaid-unbalanced",
                "diagram source has unbalanced brackets/braces "
                "([], {}, or ()), so it will fail to parse",
            )

    if is_html and not _has_mermaid_wiring(text):
        result.add(
            "mermaid-missing-wiring",
            "HTML bundle has a mermaid block but never imports mermaid.js or "
            "calls mermaid.initialize/mermaid.run, so the diagram never renders",
        )


def _extract_mermaid_source(text: str) -> str | None:
    """Pull the diagram body out of a pre.mermaid element or a fenced block."""
    pre = re.search(
        r'<pre[^>]*class="[^"]*\bmermaid\b[^"]*"[^>]*>(.*?)</pre>',
        text,
        re.IGNORECASE | re.DOTALL,
    )
    if pre:
        return pre.group(1).strip()
    fence = re.search(r"```+\s*mermaid\s*\n(.*?)```+", text, re.DOTALL)
    if fence:
        return fence.group(1).strip()
    return None


def _mermaid_first_keyword(source: str) -> str | None:
    """Return the first non-comment, non-directive token of the diagram source."""
    for raw_line in source.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("%%"):
            continue
        return line.split()[0] if line.split() else None
    return None


def _is_recognized_mermaid_keyword(keyword: str) -> bool:
    # `graph TD`/`flowchart LR` carry the orientation on the same token; match on
    # the leading keyword only.
    head = keyword.split()[0] if keyword else ""
    return head in MERMAID_DIAGRAM_KEYWORDS


def _brackets_balanced(source: str) -> bool:
    """Structural sanity: every (), [], and {} opens and closes in order.

    Brackets inside quoted node labels are ignored, since mermaid permits free
    text there. This is a balance check, not a parse.
    """
    pairs = {")": "(", "]": "[", "}": "{"}
    openers = set(pairs.values())
    stack: list[str] = []
    in_quote: str | None = None
    for ch in source:
        if in_quote:
            if ch == in_quote:
                in_quote = None
            continue
        if ch in ('"', "'"):
            in_quote = ch
            continue
        if ch in openers:
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return not stack


def _has_mermaid_wiring(text: str) -> bool:
    lowered = text.lower()
    imports = (
        "import mermaid" in lowered
        or "mermaid.min" in lowered
        or "mermaid.esm" in lowered
        or "mermaid@" in lowered
    )
    runs = "mermaid.initialize" in lowered or "mermaid.run" in lowered or "startonload" in lowered
    return imports and runs


# --------------------------------------------------------------------------- #
# Cross-engine HTML checks (scroll containment + keyboard wiring)
# --------------------------------------------------------------------------- #


def check_html_common(text: str, result: CheckResult) -> None:
    _check_scroll_containment(text, result)
    _check_keyboard_wiring(text, result)


def _check_scroll_containment(text: str, result: CheckResult) -> None:
    """Flag patterns that would let the chart eat the host page's scroll.

    Two families: a script that binds wheel/touchmove/zoom-pan handlers, and a
    style that gives the embed container a full-viewport height with its own
    overflow, turning the chart into a scroll trap.
    """
    handler = re.search(
        r"""(\.on\(\s*["'](?:wheel|touchmove|mousewheel)["']|"""
        r"""addeventlistener\(\s*["'](?:wheel|touchmove|mousewheel)["']|"""
        r"""d3\.zoom\(|\.call\(\s*zoom)""",
        text,
        re.IGNORECASE,
    )
    if handler:
        result.add(
            "html-scroll-containment",
            "binds a wheel/touchmove/zoom-pan handler that would capture the "
            "host page's scroll; contain scroll/zoom to the chart's own container",
        )
        return

    # Container style: 100vh height plus an overflow rule on the embed container.
    if re.search(r"height:\s*100vh", text, re.IGNORECASE) and re.search(
        r"overflow(?:-[xy])?:\s*(?:scroll|auto)", text, re.IGNORECASE
    ):
        result.add(
            "html-scroll-containment",
            "embed container uses height:100vh with overflow scroll/auto, which "
            "hijacks the host page's scroll; size the container to its content",
        )


def _check_keyboard_wiring(text: str, result: CheckResult) -> None:
    """Flag interactive marks that lack keyboard reachability.

    An artifact is interactive when it binds pointer/hover handlers to its marks.
    If it does, the marks must also carry `tabindex`, a key handler, and a focus
    style so the interaction is reachable without a mouse.
    """
    interactive = re.search(
        r"""\.on\(\s*["'](?:pointerenter|pointerover|pointermove|mouseover|mouseenter|click)["']""",
        text,
        re.IGNORECASE,
    )
    if not interactive:
        return

    has_tabindex = "tabindex" in text.lower()
    has_key_handler = bool(
        re.search(
            r"""(\.on\(\s*["']keydown["']|addeventlistener\(\s*["']keydown["']|navigatemarks\()""",
            text,
            re.IGNORECASE,
        )
    )
    has_focus_style = bool(re.search(r":focus\b", text)) or bool(
        re.search(r"""\.on\(\s*["']focus["']""", text, re.IGNORECASE)
    )

    missing = []
    if not has_tabindex:
        missing.append("tabindex")
    if not has_key_handler:
        missing.append("key handler")
    if not has_focus_style:
        missing.append("focus style")

    if missing:
        result.add(
            "html-keyboard-wiring",
            "interactive marks are not keyboard-reachable; missing "
            + ", ".join(missing)
            + " — interactivity should work without a mouse",
        )


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #


def check_file(path: Path) -> CheckResult:
    """Check one artifact and return its result. Never raises for an ordinary
    unsupported or unreadable input — those degrade to a not-applicable result."""
    path = Path(path)
    result = CheckResult(path=path)

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        result.applicable = False
        result.note = f"could not read file: {exc}"
        return result

    engine = detect_engine(path, text)
    result.engine = engine

    if engine is None:
        result.applicable = False
        result.note = "unsupported artifact type (not a Vega, D3, or mermaid artifact)"
        return result

    is_html = _is_html_artifact(path, text)

    if engine == "vega":
        check_vega(text, result, is_html=is_html)
        if is_html:
            check_html_common(text, result)
    elif engine == "d3":
        check_d3(text, result)
        check_html_common(text, result)
    elif engine == "mermaid":
        check_mermaid(text, result, is_html=is_html)
        if is_html:
            check_html_common(text, result)

    return result


def format_result(result: CheckResult) -> str:
    """Render one file's outcome as printable lines."""
    lines: list[str] = []
    rel = result.path
    if not result.applicable:
        lines.append(f"[n/a] {rel}: {result.note or 'not applicable'}")
        return "\n".join(lines)
    if not result.defects:
        lines.append(f"[ok]  {rel} ({result.engine}): no render-blocking defects found")
        return "\n".join(lines)
    for d in result.defects:
        tag = "FAIL" if d.severity == SEVERITY_BLOCKING else "warn"
        lines.append(f"[{tag}] {rel} ({result.engine}) {d.code}: {d.message}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: check_render.py <artifact> [<artifact> ...]", file=sys.stderr)
        return 2

    any_blocking = False
    for arg in argv:
        result = check_file(Path(arg))
        print(format_result(result))
        if result.has_render_blocking():
            any_blocking = True

    return 1 if any_blocking else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
