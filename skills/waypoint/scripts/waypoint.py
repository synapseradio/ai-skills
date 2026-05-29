#!/usr/bin/env python3
"""waypoint — distributed navigation markers for multi-file pipelines.

The CLI is the spine of the waypoint skill. It owns everything deterministic:
ID generation, comment-syntax resolution, block composition and placement,
manifest rendering, and drift/ID verification. Prose — role text, neighbor
descriptions, the manifest opening sentence — is written by the caller and
passed in. The CLI never invents prose; the caller never computes structure.

Subcommands:
  id         emit `<id>  <path>` for one or more files
  scan       catalogue map files and every block found in code
  block      compose a source block from a JSON spec on stdin (--write places it)
  verify     detect drift between manifests and the blocks in the code
  check-ids  recompute IDs from paths and emit a correction list
  manifest   write `.ai/waypoints/<name>.md` from a JSON spec on stdin

Output goes to stdout; messages and errors go to stderr. A `--json` flag on
every subcommand switches to machine-readable output. `verify` and `check-ids`
exit non-zero when they find drift, so they compose into scripts and CI.

Zero dependencies — Python 3.8+ stdlib only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

VERSION = "1.0.0"

COMMANDS = ["id", "scan", "block", "verify", "check-ids", "manifest"]

# Where pipeline maps live, relative to the git root.
WAYPOINTS_DIR = Path(".ai/waypoints")

# Direction keyword -> arrow symbol. `from`/`into` are execution flow;
# `reads`/`feeds` are reference relationships (sinks) with no ordering.
SYMBOLS = {"from": "←", "into": "→", "reads": "◁", "feeds": "▷"}

# The full legend always appears, so a first-time reader can decode any symbol
# they meet downstream — even one this particular block doesn't use.
LEGEND = "← from  → into  ◁ reads  ▷ feeds"

GREP_HINT_SINGLE = "grep any 8-char ID to trace this pipeline"
GREP_HINT_MULTI = "grep any 8-char ID to trace these pipelines"


# ---------------------------------------------------------------------------
# Error handling and command suggestions
# ---------------------------------------------------------------------------


def cli_error(message, hint, json_mode=False):
    """Print an error rewritten for a human, with an actionable hint, then exit.

    Errors are documentation: the message names what went wrong, the hint names
    what to do about it.
    """
    if json_mode:
        print(json.dumps({"status": "error", "message": message, "hint": hint}), file=sys.stderr)
    else:
        print(f"error: {message}", file=sys.stderr)
        print(f"  hint: {hint}", file=sys.stderr)
    sys.exit(1)


def _levenshtein(a, b):
    """Edit distance between two strings, for did-you-mean suggestions."""
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        curr = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            curr[j] = min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost)
        prev = curr
    return prev[len(b)]


def suggest_command(typed, commands):
    """Return the closest command within edit distance 3, or None."""
    scored = sorted((_levenshtein(typed, c), c) for c in commands)
    return scored[0][1] if scored and scored[0][0] <= 3 else None


# ---------------------------------------------------------------------------
# IDs and path resolution
# ---------------------------------------------------------------------------


def compute_id(rel_path):
    """First 8 hex chars of SHA-256 of the git-relative path string.

    Deterministic and per-file: the same path always yields the same ID, and a
    file in three pipelines shares one ID across three manifests. When a file
    moves, its ID changes — that is the signal that references need updating.
    """
    return hashlib.sha256(rel_path.encode()).hexdigest()[:8]


def git_root(cwd="."):
    """Absolute path of the git root containing cwd, or None when not in a repo."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            cwd=cwd,
        )
    except OSError:
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def to_relpath(path, root):
    """Path expressed relative to root, with forward slashes."""
    rel = os.path.relpath(os.path.abspath(path), os.path.abspath(root))
    return rel.replace(os.sep, "/")


def normalize_path(path, root=None):
    """Resolve a user-supplied path to the git-relative form used for hashing."""
    if root:
        return to_relpath(path, root)
    return path.replace(os.sep, "/").lstrip("./") or path


# ---------------------------------------------------------------------------
# Comment-syntax resolution
# ---------------------------------------------------------------------------

# Extension -> single-line comment leader.
_LINE_BY_EXT = {
    "py": "#",
    "sh": "#",
    "bash": "#",
    "zsh": "#",
    "rb": "#",
    "yml": "#",
    "yaml": "#",
    "toml": "#",
    "mk": "#",
    "conf": "#",
    "ini": "#",
    "js": "//",
    "ts": "//",
    "tsx": "//",
    "jsx": "//",
    "mjs": "//",
    "cjs": "//",
    "go": "//",
    "rs": "//",
    "java": "//",
    "c": "//",
    "cpp": "//",
    "cc": "//",
    "h": "//",
    "hpp": "//",
    "sql": "--",
    "lua": "--",
}

# Extension -> (open, close) for block-comment-only languages.
_BLOCK_BY_EXT = {
    "css": ("/*", "*/"),
    "scss": ("/*", "*/"),
    "less": ("/*", "*/"),
    "html": ("<!--", "-->"),
    "xml": ("<!--", "-->"),
    "vue": ("<!--", "-->"),
    "svelte": ("<!--", "-->"),
    "md": ("<!--", "-->"),
    "markdown": ("<!--", "-->"),
}

# Basenames with no extension that still carry a known comment syntax.
_LINE_BY_NAME = {
    "Dockerfile": "#",
    "Makefile": "#",
    "makefile": "#",
    "Gemfile": "#",
    "Rakefile": "#",
}


def comment_style(filename, override=None):
    """Resolve a file to its comment style.

    Returns ("line", leader) for languages with line comments, or
    ("block", (open, close)) for languages that only have block comments.
    Falls back to ("line", "#") for unknown extensions. The override takes a
    raw leader ("//", "--") or a block opener ("/*", "<!--").
    """
    if override:
        if override == "/*":
            return ("block", ("/*", "*/"))
        if override == "<!--":
            return ("block", ("<!--", "-->"))
        return ("line", override)

    base = os.path.basename(filename)
    if base in _LINE_BY_NAME:
        return ("line", _LINE_BY_NAME[base])

    ext = base.rsplit(".", 1)[-1].lower() if "." in base else ""
    if ext in _BLOCK_BY_EXT:
        return ("block", _BLOCK_BY_EXT[ext])
    if ext in _LINE_BY_EXT:
        return ("line", _LINE_BY_EXT[ext])
    return ("line", "#")


# ---------------------------------------------------------------------------
# Block composition
# ---------------------------------------------------------------------------


def _neighbor_line(neighbor, indent):
    """Render one neighbor reference: `<sym> <id>  <path> — <desc>`."""
    symbol = SYMBOLS.get(neighbor["dir"], "→")
    line = f"{indent}{symbol} {neighbor['id']}  {neighbor['path']}"
    desc = neighbor.get("desc")
    if desc:
        line += f" — {desc}"
    return line


def _raw_body(spec, wp_id):
    """Build the block body as bare lines, without any comment leader.

    Single flow uses the compact shape with the reference in the header and a
    combined closing line. Two or more flows stack under one header at the same
    source line, each flow naming its own reference.
    """
    flows = spec["flows"]
    lines = []
    if len(flows) == 1:
        flow = flows[0]
        lines.append(f"── Waypoint {wp_id} · {flow['pipeline']} · reference: {flow['reference']}")
        lines.append(f"   {flow['role']}")
        for neighbor in flow.get("neighbors", []):
            lines.append(_neighbor_line(neighbor, "   "))
        lines.append(f"── {GREP_HINT_SINGLE} · {LEGEND}")
    else:
        lines.append(f"── Waypoint {wp_id} · {GREP_HINT_MULTI} ──")
        for flow in flows:
            lines.append(f"   {flow['pipeline']} — {flow['role']}")
            for neighbor in flow.get("neighbors", []):
                lines.append(_neighbor_line(neighbor, "     "))
            lines.append(f"     reference: {flow['reference']}")
        lines.append(f"── {LEGEND}")
    return lines


def apply_comment(raw_lines, style):
    """Wrap bare body lines in a file's native comment syntax."""
    kind, marker = style
    if kind == "line":
        return "\n".join(f"{marker} {line}" for line in raw_lines)
    open_delim, close_delim = marker
    return "\n".join([open_delim, *raw_lines, close_delim])


def compose_block(spec):
    """Compose a complete source block in the file's native comment syntax.

    The ID is derived from `spec["file"]`, so the caller never supplies it — the
    block and the manifest always agree on the ID for a given path.
    """
    wp_id = compute_id(spec["file"])
    style = comment_style(spec["file"], spec.get("comment"))
    return apply_comment(_raw_body(spec, wp_id), style)


# ---------------------------------------------------------------------------
# Lenient block parsing (reads new `reference:` and legacy `Map:` forms)
# ---------------------------------------------------------------------------

WAYPOINT_RE = re.compile(r"Waypoint\s+([0-9a-f]{8})")
NEIGHBOR_RE = re.compile(r"([←→◁▷])\s*([0-9a-f]{8})\s+(\S+)(?:\s+—\s+(.*))?")
REF_RE = re.compile(r"(?:reference|Map):\s*(\S+\.md)")
MANIFEST_ROW = re.compile(r"\|\s*`?([0-9a-f]{8})`?\s*\|\s*([^|]+?)\s*\|")

_CLOSING_WORDS = ("from", "into", "reads", "feeds", "grep any", "search any")


def _is_closing(line):
    return "──" in line and any(word in line for word in _CLOSING_WORDS)


def _block_spans(lines):
    """Return (start, end) inclusive index pairs for each block in `lines`.

    A block runs from a header line carrying `Waypoint <id>` down to its first
    closing legend line. Legacy blocks have two closing lines; the second holds
    no data, so stopping at the first is enough for cataloguing.
    """
    headers = [i for i, line in enumerate(lines) if WAYPOINT_RE.search(line)]
    spans = []
    for index, header in enumerate(headers):
        limit = headers[index + 1] if index + 1 < len(headers) else len(lines)
        end = limit - 1
        for k in range(header + 1, limit):
            if _is_closing(lines[k]):
                end = k
                break
        spans.append((header, end))
    return spans


def parse_blocks(text):
    """Parse every waypoint block in `text` into structured records.

    Each record carries its ID, the pipelines it participates in, and its
    neighbor references. Lenient by design: it reads the new `reference:` form
    and the legacy `Map:` + two-line-closing form, so scan and verify work
    against repos that have not been migrated.
    """
    lines = text.splitlines()
    blocks = []
    for start, end in _block_spans(lines):
        header = lines[start]
        wp_id = WAYPOINT_RE.search(header).group(1)
        body = lines[start : end + 1]

        pipelines = []
        # A single-flow header carries `<id> · <pipeline> · reference: ...`.
        # Splitting on " · " yields three parts only in that case; a multi-flow
        # header splits into two (the second part is the grep hint), so guard.
        parts = header.split(" · ")
        if len(parts) >= 3:
            pipelines.append(parts[1].strip())
        for line in body:
            for match in REF_RE.finditer(line):
                stem = os.path.basename(match.group(1))[:-3]
                pipelines.append(stem)

        seen = set()
        deduped = []
        for name in pipelines:
            if name and name not in seen:
                seen.add(name)
                deduped.append(name)

        neighbors = []
        for line in body[1:]:
            match = NEIGHBOR_RE.search(line)
            if match:
                neighbors.append(
                    {
                        "dir": next(d for d, s in SYMBOLS.items() if s == match.group(1)),
                        "id": match.group(2),
                        "path": match.group(3),
                        "desc": (match.group(4) or "").strip(),
                    }
                )

        blocks.append({"id": wp_id, "pipelines": deduped, "neighbors": neighbors})
    return blocks


# ---------------------------------------------------------------------------
# Drift and ID-correction analysis (pure)
# ---------------------------------------------------------------------------


def compute_drift(manifest_rows, code_blocks):
    """Compare manifest rows to the blocks found in code.

    A row is *verified* when a block with the same ID sits in the same file and
    claims the same pipeline. A row with no such block is *stale* (the manifest
    promises a marker the file does not carry). A block whose ID appears in no
    manifest is *orphaned*.
    """
    by_id_file = {}
    for block in code_blocks:
        by_id_file.setdefault((block["id"], block["file"]), set()).update(
            block.get("pipelines", [])
        )

    verified, stale = [], []
    for row in manifest_rows:
        pipelines = by_id_file.get((row["id"], row["file"]), set())
        if row["pipeline"] in pipelines:
            verified.append(row)
        else:
            stale.append(row)

    manifest_ids = {row["id"] for row in manifest_rows}
    orphaned = [block for block in code_blocks if block["id"] not in manifest_ids]
    return {"verified": verified, "stale": stale, "orphaned": orphaned}


def compute_id_corrections(nodes, references=None):
    """Find nodes whose recorded ID no longer matches their path.

    Each node is `{"id", "file"}`. When `compute_id(file)` differs from the
    recorded ID, that node moved: the correction names the old ID, the new ID,
    and — given the optional `references` list of `{"file", "ref_id"}` — every
    neighbor block that still points at the old ID and must be updated too.
    """
    references = references or []
    corrections = []
    for node in nodes:
        new_id = compute_id(node["file"])
        if new_id != node["id"]:
            referenced_by = sorted(
                {ref["file"] for ref in references if ref["ref_id"] == node["id"]}
            )
            corrections.append(
                {
                    "file": node["file"],
                    "old_id": node["id"],
                    "new_id": new_id,
                    "referenced_by": referenced_by,
                }
            )
    return corrections


# ---------------------------------------------------------------------------
# Manifest rendering (pure)
# ---------------------------------------------------------------------------


def render_manifest(spec):
    """Render a pipeline map as markdown.

    Flow nodes appear in the order given; sink nodes (kind == "sink") sort last,
    because a reader tracing execution wants the sequence first and the runtime
    consumers after. The opening sentence is the caller's prose, untouched.
    """
    pipeline = spec["pipeline"]
    nodes = spec.get("nodes", [])
    flows = [n for n in nodes if n.get("kind", "flow") != "sink"]
    sinks = [n for n in nodes if n.get("kind") == "sink"]
    ordered = flows + sinks

    lines = [
        f"# {pipeline}",
        "",
        spec.get("opening", "").strip(),
        "",
        "| Waypoint   | File | Role |",
        "|------------|------|------|",
    ]
    for node in ordered:
        lines.append(f"| `{node['id']}` | {node['file']} | {node['role']} |")

    topology = spec.get("topology")
    if topology:
        lines.extend(["", "## Topology", "", topology.strip()])
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Filesystem gathering
# ---------------------------------------------------------------------------


def list_repo_files():
    """Tracked files in the repo, or a filesystem walk when git is unavailable."""
    try:
        result = subprocess.run(["git", "ls-files"], capture_output=True, text=True)
        if result.returncode == 0:
            return [f for f in result.stdout.splitlines() if f]
    except OSError:
        pass
    files = []
    for dirpath, dirnames, filenames in os.walk("."):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules", "__pycache__")]
        for name in filenames:
            files.append(os.path.join(dirpath, name).replace(os.sep, "/").lstrip("./"))
    return files


def gather_code_blocks():
    """Scan tracked code for waypoint blocks, skipping the manifest directory."""
    prefix = str(WAYPOINTS_DIR) + "/"
    found = []
    for filepath in list_repo_files():
        if filepath.startswith(prefix):
            continue
        try:
            text = Path(filepath).read_text(encoding="utf-8")
        except OSError, UnicodeDecodeError:
            continue
        if "Waypoint" not in text:
            continue
        for block in parse_blocks(text):
            found.append(
                {
                    "id": block["id"],
                    "file": filepath,
                    "pipelines": block["pipelines"],
                    "neighbors": block["neighbors"],
                }
            )
    return found


def find_manifests():
    """All `.md` map files under the waypoints directory."""
    if not WAYPOINTS_DIR.is_dir():
        return []
    return sorted(p for p in WAYPOINTS_DIR.iterdir() if p.suffix == ".md")


def parse_manifest_rows(path):
    """Extract `{id, file, pipeline}` rows from a manifest table."""
    pipeline = path.stem
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = MANIFEST_ROW.search(line)
        if match and match.group(2).strip().lower() != "file":
            rows.append(
                {"id": match.group(1), "file": match.group(2).strip(), "pipeline": pipeline}
            )
    return rows


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_id(args, json_mode):
    """Emit `<id>  <path>` for each file, hashing the git-relative path."""
    if not args.paths:
        cli_error("no paths given", "waypoint id <path> [path...]", json_mode)
    root = git_root()
    rows = [
        {"id": compute_id(normalize_path(p, root)), "path": normalize_path(p, root)}
        for p in args.paths
    ]
    if json_mode:
        print(json.dumps(rows, indent=2))
    else:
        for row in rows:
            print(f"{row['id']}  {row['path']}")


def cmd_scan(args, json_mode):
    """Catalogue existing waypoints: map files plus every block in the code."""
    manifests = [p.stem for p in find_manifests()]
    blocks = gather_code_blocks()

    by_pipeline = {}
    for block in blocks:
        for pipeline in block["pipelines"] or ["(unmapped)"]:
            by_pipeline.setdefault(pipeline, []).append({"id": block["id"], "file": block["file"]})

    if json_mode:
        print(json.dumps({"maps": manifests, "pipelines": by_pipeline}, indent=2))
        return

    if not manifests and not blocks:
        print("no waypoints found")
        print("  no map files in .ai/waypoints/ and no blocks in the code")
        print()
        print(
            "next: waypoint manifest < spec.json   then   waypoint block --write --at <line> < spec.json"
        )
        return

    print(f"map files in {WAYPOINTS_DIR}: {', '.join(manifests) if manifests else 'none'}")
    print()
    for pipeline in sorted(by_pipeline):
        nodes = by_pipeline[pipeline]
        mapped = "" if pipeline in manifests or pipeline == "(unmapped)" else "  (no map file)"
        print(f"{pipeline}{mapped}")
        for node in nodes:
            print(f"  {node['id']}  {node['file']}")
        print()
    print(f"next: waypoint verify   to check {len(blocks)} block(s) against the maps")


def _verify_payload():
    """Shared analysis used by verify and the human/JSON renderers."""
    rows = []
    for path in find_manifests():
        rows.extend(parse_manifest_rows(path))
    blocks = gather_code_blocks()
    drift = compute_drift(rows, blocks)

    references = [{"file": b["file"], "ref_id": n["id"]} for b in blocks for n in b["neighbors"]]
    nodes = [{"id": r["id"], "file": r["file"]} for r in rows]
    corrections = compute_id_corrections(nodes, references)
    return rows, drift, corrections


def cmd_verify(args, json_mode):
    """Detect drift between the manifests and the blocks placed in the code."""
    rows, drift, corrections = _verify_payload()

    if args.pipeline:
        drift = {
            "verified": [r for r in drift["verified"] if r["pipeline"] == args.pipeline],
            "stale": [r for r in drift["stale"] if r["pipeline"] == args.pipeline],
            "orphaned": drift["orphaned"],
        }

    has_drift = bool(drift["stale"] or drift["orphaned"] or corrections)

    if json_mode:
        print(
            json.dumps(
                {
                    "verified": drift["verified"],
                    "stale": drift["stale"],
                    "orphaned": drift["orphaned"],
                    "id_corrections": corrections,
                    "drift": has_drift,
                },
                indent=2,
            )
        )
        sys.exit(1 if has_drift else 0)

    if not rows:
        print("no manifests found in .ai/waypoints/. nothing to verify.")
        return

    print(f"verified: {len(drift['verified'])} block(s) present where the manifest expects them")
    if drift["stale"]:
        print("\nstale (in a manifest, missing from the file):")
        for row in drift["stale"]:
            print(f"  {row['id']}  {row['file']}  [{row['pipeline']}]")
    if drift["orphaned"]:
        print("\norphaned (block in a file, absent from every manifest):")
        for block in drift["orphaned"]:
            print(f"  {block['id']}  {block['file']}")
    if corrections:
        print("\nstale IDs (path no longer hashes to the recorded ID):")
        for fix in corrections:
            print(f"  {fix['file']}: {fix['old_id']} -> {fix['new_id']}")
        print("  run: waypoint check-ids   for the full correction list")

    if has_drift:
        print("\ndrift detected.")
        sys.exit(1)
    print("\nall waypoints valid.")


def cmd_check_ids(args, json_mode):
    """Recompute IDs from paths and report which IDs (and references) are stale."""
    rows = []
    for path in find_manifests():
        rows.extend(parse_manifest_rows(path))
    blocks = gather_code_blocks()

    nodes_seen = set()
    nodes = []
    for source in [{"id": r["id"], "file": r["file"]} for r in rows] + [
        {"id": b["id"], "file": b["file"]} for b in blocks
    ]:
        key = (source["id"], source["file"])
        if key not in nodes_seen:
            nodes_seen.add(key)
            nodes.append(source)

    references = [{"file": b["file"], "ref_id": n["id"]} for b in blocks for n in b["neighbors"]]
    corrections = compute_id_corrections(nodes, references)

    if json_mode:
        print(json.dumps({"corrections": corrections, "stale": bool(corrections)}, indent=2))
        sys.exit(1 if corrections else 0)

    if not corrections:
        print("all IDs match their paths.")
        return

    print("stale IDs found:")
    for fix in corrections:
        print(f"\n  {fix['file']}")
        print(f"    recorded:  {fix['old_id']}")
        print(f"    should be: {fix['new_id']}")
        if fix["referenced_by"]:
            print("    update the neighbor reference in:")
            for ref_file in fix["referenced_by"]:
                print(f"      {ref_file}  ({fix['old_id']} -> {fix['new_id']})")
    print("\nupdate each manifest row and block, then re-run waypoint verify.")
    sys.exit(1)


def _load_spec(args, json_mode, example):
    """Read a JSON spec from --file or stdin."""
    if getattr(args, "file", None):
        try:
            raw = Path(args.file).read_text(encoding="utf-8")
        except OSError as exc:
            cli_error(f"cannot read spec file: {args.file}", str(exc), json_mode)
    else:
        if sys.stdin.isatty():
            cli_error("no spec on stdin", f"pipe a JSON spec in, e.g.  {example}", json_mode)
        raw = sys.stdin.read()
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        cli_error(
            f"invalid JSON spec: {exc}", "see references/cli.md for the spec schema", json_mode
        )


def _write_block(filepath, at, block_text, spec):
    """Insert a composed block at `at`, or update the block already there.

    The update key is (file, pipeline): if a block at or around the target line
    already covers this pipeline, it is rewritten in place rather than
    duplicated. This keeps repeated runs idempotent.
    """
    path = Path(filepath)
    lines = path.read_text(encoding="utf-8").splitlines()
    new_lines = block_text.splitlines()
    spec_pipelines = {flow["pipeline"] for flow in spec["flows"]}

    spans = _block_spans(lines)
    target = None
    for start, end in spans:
        if start <= (at - 1) <= end + 1:
            target = (start, end)
            break
    if target is None:
        for start, end in spans:
            block_pipelines = set()
            for parsed in parse_blocks("\n".join(lines[start : end + 1])):
                block_pipelines.update(parsed["pipelines"])
            if block_pipelines & spec_pipelines:
                target = (start, end)
                break

    if target is not None:
        start, end = target
        lines[start : end + 1] = new_lines
        action = "updated"
    else:
        insert_at = max(0, min(at - 1, len(lines)))
        lines[insert_at:insert_at] = new_lines
        action = "inserted"

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return action


def cmd_block(args, json_mode):
    """Compose a source block; with --write, place or update it in the file."""
    spec = _load_spec(args, json_mode, 'echo \'{"file":"app.ts","flows":[...]}\' | waypoint block')
    if "file" not in spec or "flows" not in spec:
        cli_error(
            "spec needs `file` and `flows`",
            "see references/cli.md for the block spec schema",
            json_mode,
        )

    block_text = compose_block(spec)

    if not args.write:
        print(block_text)
        return

    if args.at is None:
        cli_error(
            "--write needs --at <line>", "waypoint block --write --at 12 < spec.json", json_mode
        )
    if not Path(spec["file"]).is_file():
        cli_error(
            f"file not found: {spec['file']}",
            "spec.file must be a path that exists from the repo root",
            json_mode,
        )

    action = _write_block(spec["file"], args.at, block_text, spec)
    if json_mode:
        print(json.dumps({"action": action, "file": spec["file"], "line": args.at}, indent=2))
    else:
        print(f"{action} waypoint block in {spec['file']} at line {args.at}")
        print("next: waypoint verify   to confirm it matches the manifest")


def cmd_manifest(args, json_mode):
    """Write `.ai/waypoints/<pipeline>.md` from a JSON spec on stdin."""
    spec = _load_spec(
        args, json_mode, 'echo \'{"pipeline":"x","nodes":[...]}\' | waypoint manifest'
    )
    if "pipeline" not in spec:
        cli_error(
            "spec needs `pipeline`", "see references/cli.md for the manifest spec schema", json_mode
        )

    # The CLI is the single source of truth for IDs: derive each from its path
    # unless the caller pinned one explicitly.
    for node in spec.get("nodes", []):
        if "file" in node and not node.get("id"):
            node["id"] = compute_id(node["file"])

    text = render_manifest(spec)
    WAYPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = WAYPOINTS_DIR / f"{spec['pipeline']}.md"
    out_path.write_text(text, encoding="utf-8")

    if json_mode:
        print(
            json.dumps(
                {"action": "wrote", "path": str(out_path), "nodes": len(spec.get("nodes", []))},
                indent=2,
            )
        )
    else:
        print(f"wrote map to {out_path} ({len(spec.get('nodes', []))} node(s))")
        print(
            "next: place a block in each file with  waypoint block --write --at <line> < blockspec.json"
        )
        print(f"      then  waypoint verify {spec['pipeline']}")


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------


def build_parser():
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--json", action="store_true", help="emit machine-readable JSON")

    parser = argparse.ArgumentParser(
        prog="waypoint",
        description="waypoint — distributed navigation markers for multi-file pipelines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[shared],
        epilog=(
            "examples:\n"
            "  waypoint id config/ci.yml scripts/build.sh\n"
            "  waypoint scan\n"
            "  echo '<spec>' | waypoint manifest\n"
            "  echo '<spec>' | waypoint block --write --at 14\n"
            "  waypoint verify sourcemap-upload\n"
            "  waypoint check-ids\n"
        ),
    )
    parser.add_argument("--version", action="version", version=f"waypoint {VERSION}")
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    p_id = sub.add_parser("id", help="emit <id>  <path> for files", parents=[shared])
    p_id.add_argument("paths", nargs="*", metavar="<path>", help="file paths to hash")

    sub.add_parser("scan", help="catalogue maps and blocks", parents=[shared])

    p_block = sub.add_parser(
        "block", help="compose a source block from a JSON spec on stdin", parents=[shared]
    )
    p_block.add_argument(
        "--write", action="store_true", help="place or update the block in the file"
    )
    p_block.add_argument(
        "--at", type=int, metavar="<line>", help="1-based line to place the block at"
    )
    p_block.add_argument(
        "--file", metavar="<path>", help="read the spec from a file instead of stdin"
    )

    p_verify = sub.add_parser("verify", help="detect drift against the manifests", parents=[shared])
    p_verify.add_argument("pipeline", nargs="?", metavar="<pipeline>", help="limit to one pipeline")

    sub.add_parser("check-ids", help="recompute IDs and emit corrections", parents=[shared])

    p_manifest = sub.add_parser(
        "manifest", help="write a map file from a JSON spec on stdin", parents=[shared]
    )
    p_manifest.add_argument(
        "--file", metavar="<path>", help="read the spec from a file instead of stdin"
    )

    return parser


def main():
    raw_args = sys.argv[1:]
    non_flags = [a for a in raw_args if not a.startswith("-")]
    if non_flags and non_flags[0] not in COMMANDS:
        json_mode = "--json" in raw_args
        typed = non_flags[0]
        guess = suggest_command(typed, COMMANDS)
        hint = (
            f"did you mean '{guess}'?  run: waypoint --help"
            if guess
            else f"commands: {', '.join(COMMANDS)}.  run: waypoint --help"
        )
        cli_error(f"unknown command '{typed}'", hint, json_mode)

    parser = build_parser()
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(0)

    dispatch = {
        "id": cmd_id,
        "scan": cmd_scan,
        "block": cmd_block,
        "verify": cmd_verify,
        "check-ids": cmd_check_ids,
        "manifest": cmd_manifest,
    }
    dispatch[args.command](args, args.json)


if __name__ == "__main__":
    main()
