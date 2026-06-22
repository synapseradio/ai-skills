# Waypoint CLI reference

The complete surface of `scripts/waypoint.py`. Read this before composing your
first `block` or `manifest` spec — those two commands read a JSON document on
stdin, and getting the shape right the first time saves a round-trip.

```bash
python3 <skill-path>/scripts/waypoint.py <subcommand> [args]
```

The tool is stdlib-only Python 3.8+. It writes primary output to stdout and
messages and errors to stderr, so you can pipe `--json` output into other tools
without noise. Every subcommand accepts `--json`. `verify` and `check-ids` exit
1 when they find drift and 0 when clean, so they drop into scripts and CI.

## Contents

- [The guidance channel](#the-guidance-channel) — `next_steps`, `advisory`, `contract`
- [id](#id) — derive waypoint IDs from paths
- [scan](#scan) — catalogue maps and blocks
- [manifest](#manifest) — write a map file
- [block](#block) — compose and place a source block
- [verify](#verify) — detect drift
- [check-ids](#check-ids) — correct IDs after a move
- [Comment-syntax resolution](#comment-syntax-resolution)
- [The block spec](#the-block-spec) — JSON schema for `block`
- [The manifest spec](#the-manifest-spec) — JSON schema for `manifest`
- [Worked example: mapping a two-node pipeline](#worked-example-mapping-a-two-node-pipeline)

## The guidance channel

Every command speaks the same three guidance fields, so an agent driving the CLI
through `--json` reads the same direction a human reads on the terminal.

- `next_steps` — an ordered list of the commands to run next. In human output
  these are the `next:` lines; in JSON they are the `next_steps` array. The two
  are computed once from the same list, so they never disagree.
- `advisory` — a `{message, hint}` object when the command needs to warn about
  something it did, or `null` when it does not. The block fallback is its main
  user: the message names what was left alone and why, the hint says how to
  resolve it.
- `contract` — the fixed division of labor, repeated verbatim:
  `CLI owns IDs, structure, placement, verification; you supply prose.` It rides
  in the JSON of every command. In human output it prints only on the
  orientation and authoring commands (`scan`, `manifest`, `block`).

## id

```bash
python3 scripts/waypoint.py id <path> [path...] [--json]
```

Prints `<id>  <path>` for each file. The ID is the first 8 hex characters of
the SHA-256 hash of the path expressed relative to the git root. It is
per-file and deterministic: the same path always yields the same ID, and a
file that appears in three pipelines carries one ID across all three. When a
file moves, its ID changes — that is the signal that references need updating.

```
$ python3 scripts/waypoint.py id docker-compose.ci.yml config/rspack/browser/browser.plugins.ts
4263ae66  docker-compose.ci.yml
da7d6099  config/rspack/browser/browser.plugins.ts
```

`--json` emits `{"ids": [{"id": "...", "path": "..."}], "advisory": null, "next_steps": [...], "contract": "..."}`. The guidance fields are described in [The guidance channel](#the-guidance-channel).

## scan

```bash
python3 scripts/waypoint.py scan [--json]
```

Catalogues the current state: which map files exist in `.ai/waypoints/`, and
every waypoint block found in the tracked code, grouped by the pipeline each
claims. Run it first when asked to add or check waypoints — it answers "are
there existing waypoints here?" without reading a single source file yourself.

A pipeline tagged `(no map file)` has blocks in code but no manifest. Blocks
whose pipeline cannot be determined are grouped under `(unmapped)`.

`--json` emits `{"maps": [...], "pipelines": {"<name>": [{"id","file"}]}}`.

## manifest

```bash
echo '<spec>' | python3 scripts/waypoint.py manifest [--json]
```

Reads a [manifest spec](#the-manifest-spec) on stdin and writes
`.ai/waypoints/<pipeline>.md`. The CLI derives each node's ID from its path, so
you never hand-write IDs into the spec and the map can never disagree with the
blocks. Nodes are rendered in the order given, with sink nodes moved to the end.
Use `--file <path>` to read the spec from a file instead of stdin.

## block

```bash
echo '<spec>' | python3 scripts/waypoint.py block [--write --at <line>] [--dry-run] [--json]
```

Reads a [block spec](#the-block-spec) on stdin and composes the source comment
block in the file's native comment syntax.

- Without `--write`, it prints the block to stdout for inspection.
- With `--write --at <line>`, it places the block in the file. `--at` is the
  1-based line the block should sit above. If the file already carries this
  pipeline's own well-formed block at or near that line, it is rewritten in
  place, so repeated runs stay idempotent and never duplicate a block.
- With `--dry-run --at <line>`, it reports the placement plan — the action, the
  span it would touch, the composed block, and any advisory — and writes
  nothing. Use it to preview a placement before committing to it.

Choosing the anchor line is your judgment call; composing and placing the text
is the CLI's. Use `--file <path>` to read the spec from a file instead of stdin,
and `--comment` inside the spec to override the resolved comment syntax.

### Placement safety

A write resolves to one of three actions, reported as `action` in JSON and as a
sentence in human output:

- `inserted` — no existing block was found, so a fresh one went in at `--at`.
- `updated` — the file's own well-formed block for this pipeline was replaced in
  place. The JSON result adds `replaced: {start, end}` with the 1-based line span.
- `inserted-fallback` — a nearby block was found but is unsafe to replace, so a
  fresh block was inserted and the existing one was left untouched. The
  `advisory` field carries the reason and the manual-dedupe instruction.

A block is replaced only when its span is both *terminated* (it ends on a real
closing legend line, so its extent is trusted) and *same-pipeline* (it already
claims a pipeline this spec covers). When the closing legend has been edited
away, the block's span runs to the next block or the end of the file; replacing
it would delete that trailing content. When the nearby block belongs to a
different pipeline, replacing it would clobber unrelated work. In both cases the
write falls back to an insert and asks you to remove the stale block by hand,
then re-run `verify`. A write never deletes content that is not this spec's own
well-formed block.

## verify

```bash
python3 scripts/waypoint.py verify [pipeline] [--json]
```

Compares the manifests against the blocks in the code and reports three kinds
of drift:

- **stale** — a row in a manifest whose block is missing from the file it names.
- **orphaned** — a block in a file whose ID appears in no manifest.
- **stale IDs** — a recorded ID that no longer matches the hash of its path
  (a moved file); `verify` summarizes these and points you at `check-ids`.

Pass a pipeline name to limit the flow checks to that pipeline. Exits 1 when
any drift is found, 0 when clean.

## check-ids

```bash
python3 scripts/waypoint.py check-ids [--json]
```

Recomputes the ID for every node from its current path and compares it to the
recorded ID in the manifests and blocks. For each mismatch it prints the file,
the recorded ID, the value it should be, and every neighbor block that still
points at the old ID and must be updated. This is the repair list to apply after
a file moves. Exits 1 when any ID is stale.

```
$ python3 scripts/waypoint.py check-ids
stale IDs found:

  config/rspack/browser/sentry.plugins.ts
    recorded:  da7d6099
    should be: 6f303f3f
    update the neighbor reference in:
      docker-compose.ci.yml  (da7d6099 -> 6f303f3f)

update each manifest row and block, then re-run waypoint verify.
```

## Comment-syntax resolution

The CLI chooses a comment syntax from the file's extension (or basename, for
extensionless files like `Dockerfile`). Override it per spec with a `comment`
field holding a leader (`//`, `--`) or a block opener (`/*`, `<!--`).

| Syntax | Resolves for |
|--------|--------------|
| `#` line | py, sh, bash, zsh, rb, yml, yaml, toml, mk, conf, ini, Dockerfile, Makefile |
| `//` line | js, ts, tsx, jsx, mjs, cjs, go, rs, java, c, cpp, cc, h, hpp |
| `--` line | sql, lua |
| `/* */` block | css, scss, less |
| `<!-- -->` block | html, xml, vue, svelte, md, markdown |

Anything unrecognized falls back to `#`. Line syntaxes prefix every line with
the leader; block syntaxes wrap the body between the open and close delimiters
on their own lines.

## The block spec

A JSON object describing one source block. The CLI derives the block's ID from
`file`, so the spec never contains an ID for the block itself.

```json
{
  "file": "config/rspack/browser/browser.plugins.ts",
  "comment": "//",
  "flows": [
    {
      "pipeline": "sourcemap-upload",
      "role": "uploads browser sourcemaps to Sentry so minified errors resolve to source",
      "reference": ".ai/waypoints/sourcemap-upload.md",
      "neighbors": [
        {"dir": "from", "id": "4263ae66", "path": "docker-compose.ci.yml", "desc": "passes the release version into this build"},
        {"dir": "into", "id": "80e5dc26", "path": "server.plugins.ts", "desc": "uploads server sourcemaps to Sentry"}
      ]
    }
  ]
}
```

| Field | Meaning |
|-------|---------|
| `file` | Git-relative path of the file the block goes in. Drives the ID and the comment syntax. |
| `comment` | Optional. Overrides the resolved comment syntax. |
| `flows` | One entry per pipeline this line participates in. One entry → compact block; two or more → stacked multi-flow block. |
| `flows[].pipeline` | Pipeline name. Matches a manifest stem. |
| `flows[].role` | This file's role in that pipeline. Verb-first, with purpose. Your prose. |
| `flows[].reference` | Path to the map file, e.g. `.ai/waypoints/sourcemap-upload.md`. |
| `flows[].neighbors` | Adjacent nodes. |
| `neighbors[].dir` | `from` (`←`), `into` (`→`), `reads` (`◁`), or `feeds` (`▷`). |
| `neighbors[].id` | The neighbor's 8-char ID (from `waypoint id`). |
| `neighbors[].path` | The neighbor's path, shown in the block. |
| `neighbors[].desc` | What the neighbor does, from its perspective. Your prose. Optional but almost always worth it. |

The `dir` keywords map to the two relationship kinds: `from`/`into` are
execution flow (this runs before/after the neighbor); `reads`/`feeds` are
reference relationships where a sink consumes a value at runtime with no
execution ordering.

## The manifest spec

A JSON object describing one pipeline map. The CLI derives each node's ID from
its `file`.

```json
{
  "pipeline": "sourcemap-upload",
  "opening": "CI runs the build, passing the release version into the rspack browser config so Sentry resolves minified errors to source.",
  "nodes": [
    {"file": "docker-compose.ci.yml", "role": "runs the build and passes the release version downstream", "kind": "flow"},
    {"file": "config/rspack/browser/browser.plugins.ts", "role": "uploads browser sourcemaps to Sentry", "kind": "flow"},
    {"file": "config/datadog/rum.ts", "role": "reads the release version at runtime for Datadog RUM", "kind": "sink"}
  ],
  "topology": "4263ae66 → da7d6099 ▷ 9c1f0a2b"
}
```

| Field | Meaning |
|-------|---------|
| `pipeline` | Pipeline name. Becomes the filename `.ai/waypoints/<pipeline>.md` and the `# <pipeline>` heading. |
| `opening` | The single narrative sentence that walks the pipeline's stages in order. The most important line in the system. Your prose. |
| `nodes` | The files in the pipeline. |
| `nodes[].file` | Git-relative path. Drives the ID. |
| `nodes[].role` | The file's role. Your prose. |
| `nodes[].kind` | `flow` (default) or `sink`. Sinks render last in the table. |
| `topology` | Optional. The graph line, using `→` for flow and `◁`/`▷` for reference. Use the IDs from `waypoint id`. |

## Worked example: mapping a two-node pipeline

```bash
WP="<skill-path>/scripts/waypoint.py"

# 1. Derive the IDs you will reference.
python3 "$WP" id docker-compose.ci.yml config/rspack/browser/browser.plugins.ts
# 4263ae66  docker-compose.ci.yml
# da7d6099  config/rspack/browser/browser.plugins.ts

# 2. Write the map.
echo '{
  "pipeline": "sourcemap-upload",
  "opening": "CI runs the build, passing the release version into the rspack browser config so Sentry resolves minified errors to source.",
  "nodes": [
    {"file": "docker-compose.ci.yml", "role": "runs the build and passes the release version downstream"},
    {"file": "config/rspack/browser/browser.plugins.ts", "role": "uploads browser sourcemaps to Sentry"}
  ],
  "topology": "4263ae66 → da7d6099"
}' | python3 "$WP" manifest

# 3. Place a block in each file, choosing the anchor line yourself.
echo '{
  "file": "docker-compose.ci.yml",
  "flows": [{
    "pipeline": "sourcemap-upload",
    "role": "runs the build and passes the release version downstream",
    "reference": ".ai/waypoints/sourcemap-upload.md",
    "neighbors": [{"dir": "into", "id": "da7d6099", "path": "config/rspack/browser/browser.plugins.ts", "desc": "uploads browser sourcemaps to Sentry"}]
  }]
}' | python3 "$WP" block --write --at 1

echo '{
  "file": "config/rspack/browser/browser.plugins.ts",
  "flows": [{
    "pipeline": "sourcemap-upload",
    "role": "uploads browser sourcemaps to Sentry so minified errors resolve to source",
    "reference": ".ai/waypoints/sourcemap-upload.md",
    "neighbors": [{"dir": "from", "id": "4263ae66", "path": "docker-compose.ci.yml", "desc": "passes the release version into this build"}]
  }]
}' | python3 "$WP" block --write --at 1

# 4. Confirm the map and the blocks agree.
python3 "$WP" verify sourcemap-upload
```
