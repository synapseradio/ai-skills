#!/usr/bin/env python3
"""Assemble engine-agnostic chart fragments into runnable single-file examples.

A chart is a
*fragment* — a per-instance-scoped `<section class="viz">` plus one scoped
`<script>`, with no `<!doctype>`/`<head>`/`<body>` of its own. One engine-agnostic
*wrapper* (`assets/_shared/wrapper.html`) hosts one or more fragments. The single
runnable file users open is the assembly of wrapper + one fragment; composition is
several fragments in the one wrapper.

A fragment file (`*.frag.html`) is a sequence of named sections delimited by HTML
comments `<!-- @section: NAME -->`. Sections:

  frontmatter   — metadata (name/description/chart-type/engine). Required.
  title         — the chart's headline (figcaption <h1>). Required.
  subtitle      — the chart's subtitle line (figcaption .subtitle). Optional.
  svg-title     — the SVG <title> accessible name. Optional.
  svg-desc      — the SVG <desc> long description. Optional.
  chart-css     — chart-specific CSS, authored already scoped under `.viz`.
  mount         — the chart's mount markup (the <svg>/<div> the script draws into)
                  placed inside the section's <figure>, before the tooltip and
                  data-table. Required.
  extra-imports — additional ESM import lines beyond the engine's core import.
  helpers       — comma-separated shared helpers to inline: tooltip, a11y,
                  data-table. Inlined once across the whole assembly.
  engine        — which engine core import to include (currently: d3). Optional;
                  defaults to the frontmatter `engine` value.
  chart-js      — the chart code. Runs with `root` (the section element) and
                  `uid` (the instance id) in scope, and `VizHelpers` available.

Per-instance scoping: the assembler assigns each fragment a uid and emits the
section as `<section class="viz" data-viz="UID">`. The fragment's script runs
inside an IIFE with `const root = document.querySelector('[data-viz="UID"]')`, so
all of its DOM lookups, ids, and handlers are confined to its own subtree. Two
fragments in one document therefore never collide.

CLI:
  build_viz.py --fragment <path> --out <path>   # assemble one example
  build_viz.py --all                            # rebuild every example
  build_viz.py --check                          # rebuild to /tmp; nonzero on drift
  build_viz.py --compose <fragA> <fragB> --out <path>   # several in one document
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SHARED_DIR = SKILL_DIR / "assets" / "_shared"
ASSETS_DIR = SKILL_DIR / "assets"

SECTION_RE = re.compile(r"<!--\s*@section:\s*([a-z-]+)\s*-->")

HELPER_FILES = {
    "tooltip": "tooltip.js",
    "a11y": "a11y.js",
    "data-table": "data-table.js",
}

# Core ESM import per engine. Pinned to one major so two fragments never load two
# d3 builds into one document.
ENGINE_CORE_IMPORT = {
    "d3": 'import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";',
    "vega": 'import vegaEmbed from "https://cdn.jsdelivr.net/npm/vega-embed@6/+esm";',
    "mermaid": 'import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/+esm";',
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_fragment(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    parts = SECTION_RE.split(text)
    for i in range(1, len(parts), 2):
        name = parts[i].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        sections[name] = body.strip("\n")
    return sections


def indent(text: str, prefix: str) -> str:
    return "\n".join(prefix + line if line else line for line in text.split("\n"))


def frontmatter_engine(frontmatter: str) -> str:
    for line in frontmatter.split("\n"):
        if line.strip().startswith("engine:"):
            return line.split(":", 1)[1].strip()
    return "d3"


def tokens_js() -> str:
    """Build the JS token object from theme.css `--oc-*` declarations.

    Vega `config` and mermaid `themeVariables` read these at assembly time, so
    one edit to theme.css propagates to every engine.
    """
    theme = read(SHARED_DIR / "theme.css")
    pairs = re.findall(r"--(oc-[a-z0-9-]+):\s*(#[0-9a-fA-F]{3,8});", theme)
    lines = [f'        "{name}": "{value}",' for name, value in pairs]
    return "window.VizHelpers = window.VizHelpers || {};\n" + (
        "VizHelpers.tokens = {\n" + "\n".join(lines) + "\n};"
    )


def uid_for(fragment_path: Path) -> str:
    rel = fragment_path.name.replace(".frag.html", "")
    return f"viz-{rel}"


def render_section(frag: dict[str, str], uid: str) -> str:
    """Render one fragment into its scoped <section> markup (no <script>)."""
    title = frag.get("title", "").strip()
    subtitle = frag.get("subtitle", "").strip()
    # A fragment may write `{{uid}}` anywhere it needs a per-instance id (e.g. the
    # SVG <title>/<desc> ids and the aria-labelledby that references them). The
    # assembler substitutes the real uid so two fragments in one document never
    # share an id (fixes B1 for static mount markup).
    mount = frag.get("mount", "").strip().replace("{{uid}}", uid)

    caption = [f"<h1>{title}</h1>"]
    if subtitle:
        caption.append(f'<p class="subtitle">{subtitle}</p>')
    caption_html = "\n".join(caption)

    parts = [
        f'<section class="viz" data-viz="{uid}">',
        "  <figure>",
        "    <figcaption>",
        indent(caption_html, "      "),
        "    </figcaption>",
        indent(mount, "    "),
        '    <div class="tooltip" role="status" aria-live="polite"></div>',
        "    <details>",
        "      <summary>View data table</summary>",
        '      <div class="data-table"></div>',
        "    </details>",
        "  </figure>",
        "</section>",
    ]
    return "\n".join(parts)


def render_script(frag: dict[str, str], uid: str, engine: str) -> str:
    """Render one fragment's scoped module <script>.

    The chart code runs inside an async IIFE with `root` and `uid` in scope. The
    engine core import and any extra imports are hoisted to the top of the module
    (ESM imports must be top-level); the body is wrapped so its declarations never
    leak to the global scope or clash with a sibling fragment. The wrapper is
    async so a fragment can `await` data loads (e.g. d3.json for a map); purely
    synchronous chart code runs identically inside it.
    """
    extra_imports = frag.get("extra-imports", "").strip()
    chart_js = frag.get("chart-js", "").rstrip("\n").replace("{{uid}}", uid)

    body_lines = [
        "(async function () {",
        f'  const uid = "{uid}";',
        '  const root = document.querySelector(`[data-viz="${uid}"]`);',
        indent(chart_js, "  "),
        "})();",
    ]
    return "\n".join(body_lines), extra_imports


def assemble(fragment_paths: list[Path]) -> str:
    wrapper = read(SHARED_DIR / "wrapper.html")
    theme_css = read(SHARED_DIR / "theme.css").rstrip("\n")
    chrome_css = read(SHARED_DIR / "chrome.css").rstrip("\n")

    frags = [parse_fragment(read(p)) for p in fragment_paths]
    uids = [uid_for(p) for p in fragment_paths]
    engines = [frontmatter_engine(f.get("frontmatter", "")) for f in frags]

    # Title: first fragment's title (single-chart example). For composition, join.
    titles = [f.get("title", "").strip() for f in frags]
    page_title = titles[0] if len(titles) == 1 else " + ".join(t for t in titles if t)

    # --- STYLE: theme + chrome + each fragment's chart-css, once. ---
    css_parts = [theme_css, chrome_css]
    for f in frags:
        cc = f.get("chart-css", "").strip()
        if cc:
            css_parts.append(cc)
    style_block = "\n".join(css_parts)

    # --- Engine core imports, deduped, in first-seen order. ---
    core_imports: list[str] = []
    for eng in engines:
        imp = ENGINE_CORE_IMPORT.get(eng)
        if imp and imp not in core_imports:
            core_imports.append(imp)

    # --- Extra imports, deduped across fragments (e.g. d3-sankey, topojson). ---
    extra_import_lines: list[str] = []
    for f in frags:
        for line in f.get("extra-imports", "").split("\n"):
            line = line.rstrip()
            if line.strip() and line not in extra_import_lines:
                extra_import_lines.append(line)

    # --- Helpers needed across all fragments, deduped, inlined once. ---
    needed_helpers: list[str] = []
    for f in frags:
        for h in f.get("helpers", "").split(","):
            h = h.strip()
            if h and h not in needed_helpers:
                if h not in HELPER_FILES:
                    raise SystemExit(f"unknown helper '{h}'")
                needed_helpers.append(h)

    # --- Build the single module script. ---
    module_lines = list(core_imports)
    module_lines.extend(extra_import_lines)
    module_lines.append("")
    module_lines.append(tokens_js())
    for h in needed_helpers:
        module_lines.append("")
        module_lines.append(read(SHARED_DIR / HELPER_FILES[h]).rstrip("\n"))
    for path, frag, uid, eng in zip(fragment_paths, frags, uids, engines):
        script_body, _ = render_script(frag, uid, eng)
        module_lines.append("")
        module_lines.append(script_body)
    module_block = "\n".join(module_lines)

    # --- HEAD: <style> with the inlined CSS. The {{HEAD}} marker sits at a
    # 4-space indent in the wrapper; its first line lands there, so inner lines
    # carry 6 spaces (CSS body) and the closing tag carries 4. ---
    head_block = "<style>\n" + indent(style_block, "      ") + "\n    </style>"

    # --- BODY: each fragment's section, in order. ---
    body_block = "\n\n".join(render_section(frag, uid) for frag, uid in zip(frags, uids))

    out = wrapper
    out = out.replace("{{TITLE}}", page_title)
    out = out.replace("{{HEAD}}", head_block)
    out = out.replace(
        "{{BODY}}",
        "\n"
        + indent(body_block, "      ")
        + "\n\n"
        + indent(
            '<script type="module">\n' + indent(module_block, "  ") + "\n</script>",
            "      ",
        )
        + "\n    ",
    )
    return out


# ---------------------------------------------------------------------------
# Path mapping and CLI
# ---------------------------------------------------------------------------


def fragment_dirs() -> list[Path]:
    return sorted(ASSETS_DIR.glob("*/fragments"))


def all_fragments() -> list[Path]:
    out: list[Path] = []
    for d in fragment_dirs():
        out.extend(sorted(d.rglob("*.frag.html")))
    return out


def derive_out_path(fragment_path: Path) -> Path:
    # assets/<engine>/fragments/<cat>/<name>.frag.html
    #   -> assets/<engine>/templates/<cat>/<name>.html
    parts = fragment_path.parts
    idx = parts.index("fragments")
    engine_dir = Path(*parts[:idx])
    rel = Path(*parts[idx + 1 :])
    name = rel.name.replace(".frag.html", ".html")
    return engine_dir / "templates" / rel.parent / name


def cmd_build_one(fragment: Path, out: Path) -> None:
    rendered = assemble([fragment])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rendered, encoding="utf-8")
    try:
        print(f"built {out.resolve().relative_to(SKILL_DIR)}")
    except ValueError:
        print(f"built {out}")


def cmd_build_all() -> None:
    frags = all_fragments()
    if not frags:
        print("no fragments found", file=sys.stderr)
        sys.exit(1)
    for frag in frags:
        cmd_build_one(frag, derive_out_path(frag))


def cmd_check() -> int:
    frags = all_fragments()
    if not frags:
        print("no fragments found; nothing to check", file=sys.stderr)
        return 0
    drift = 0
    for frag in frags:
        committed = derive_out_path(frag)
        rendered = assemble([frag])
        if not committed.exists():
            print(f"DRIFT (missing committed): {committed.relative_to(SKILL_DIR)}")
            drift += 1
            continue
        existing = read(committed)
        if existing != rendered:
            drift += 1
            diff = difflib.unified_diff(
                existing.splitlines(keepends=True),
                rendered.splitlines(keepends=True),
                fromfile=str(committed.relative_to(SKILL_DIR)),
                tofile=str(committed.relative_to(SKILL_DIR)) + " (rebuilt)",
                n=3,
            )
            sys.stdout.write("".join(diff))
    if drift:
        print(f"\n{drift} example(s) drifted", file=sys.stderr)
        return 1
    print(f"OK: {len(frags)} example(s) match committed output")
    return 0


def main() -> None:
    p = argparse.ArgumentParser(prog="build_viz.py")
    p.add_argument("--fragment", type=Path, help="single fragment path")
    p.add_argument("--out", type=Path, help="output path")
    p.add_argument("--all", action="store_true", help="rebuild every example")
    p.add_argument("--check", action="store_true", help="diff examples against committed")
    p.add_argument(
        "--compose", type=Path, nargs="+", help="assemble several fragments into one document"
    )
    args = p.parse_args()

    if args.check:
        sys.exit(cmd_check())
    if args.all:
        cmd_build_all()
        return
    if args.compose:
        if not args.out:
            raise SystemExit("--compose requires --out")
        rendered = assemble(list(args.compose))
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
        print(f"composed {len(args.compose)} fragments -> {args.out}")
        return
    if args.fragment:
        out = args.out or derive_out_path(args.fragment)
        cmd_build_one(args.fragment, out)
        return
    p.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
