---
name: waypoint
description: >-
  Distributed navigation system for multi-file pipelines and processes.
  Creates compact, grep-friendly waypoint markers that orient readers within
  complex cross-file workflows — each file carries its own ID, role, adjacent
  nodes, and a pointer to the full map. Use when asked to "point me to",
  "where does X begin/end", "map this pipeline", "add waypoints", "trace
  this process", or when working with processes spanning many files that need
  discoverability without centralized documentation that drifts.
metadata:
  user-invocable: true
---

# Waypoint

Waypoints are distributed navigation markers for multi-file pipelines. Each
file carries a compact comment block naming its ID, its role in the pipeline,
its neighbors, and a pointer to the full map. One manifest per pipeline holds
the complete topology. Grep any 8-character ID and the whole pipeline unfolds.

A single CLI does all the deterministic and token-heavy work. You bring the
prose; the CLI brings the structure. Treat every step below as a call to that
CLI.

## The CLI

```bash
python3 <skill-path>/scripts/waypoint.py <subcommand> [args]
```

Every subcommand takes `--json` for machine-readable output. `verify` and
`check-ids` exit non-zero when they find drift.

| Subcommand | What it does |
|------------|--------------|
| `id <path>...` | Print `<id>  <path>` for each file (SHA-256 of the git-relative path, first 8 hex). |
| `scan` | Catalogue every map file and every block in the code, grouped by pipeline. Run this first to check for existing waypoints. |
| `manifest` | Write `.ai/waypoints/<name>.md` from a JSON spec on stdin. The rich map layout lives here. |
| `block` | Compose a source block from a JSON spec on stdin. `--write --at <line>` places or updates it in the file; `--dry-run --at <line>` previews the placement without writing. |
| `verify [pipeline]` | Detect drift: stale rows, orphaned blocks, and IDs that no longer match their path. |
| `check-ids` | Recompute IDs from paths and emit the exact correction list when files have moved. |

The JSON spec schemas for `block` and `manifest`, every flag, the comment-syntax
table, and worked examples live in [`references/cli.md`](references/cli.md). Read
it before composing your first spec.

## Division of labor

The CLI owns structure so it is always right and never drifts: IDs, comment
syntax, block framing, layout, placement and update, manifest rendering, and
verification. You own prose, because judgment and warmth cannot be templated:
the role each file plays, what each neighbor does, and the manifest's opening
sentence. The voice guide at [`references/waypoint-voice.md`](references/waypoint-voice.md)
governs that writing — load it before you write any role or neighbor text.

You also make one placement judgment the CLI cannot: *which line* a brand-new
block belongs above. The CLI composes the text; you choose the anchor and pass
it as `--at`.

## Mapping a pipeline

When asked to add waypoints, trace a process, or map a pipeline, work through
these steps. Each is a CLI call wrapped around your own reading of the code.

1. **Check what already exists.** Run `waypoint scan`. If the pipeline is
   already mapped, read its manifest and treat this as an update rather than a
   fresh placement — preserve the nodes that are still correct.

2. **Trace the process across files.** Use your normal reading tools to follow
   the thread: imports, script calls, Dockerfile stages, shared env vars and
   version strings, CI step ordering. Identify two kinds of node:
   - **Flow** (`from`/`into`, shown as `←`/`→`): files in the execution chain.
   - **Reference sinks** (`reads`/`feeds`, shown as `◁`/`▷`): files that consume
     a value at runtime without sitting in the build or deploy sequence.

   Confirm the full path from entry to exit before placing anything. When a
   node's role is unclear, read the file.

3. **Generate the IDs.** Run `waypoint id <path>...` for every file in one call.
   IDs are deterministic from the git-relative path — never invent them.

4. **Write the manifest.** Compose a JSON spec (see `references/cli.md`) with the
   pipeline name, the opening sentence, the ordered nodes, and the topology, then
   pipe it to `waypoint manifest`. Order nodes by execution; sinks go last. The
   CLI derives each node's ID from its path, so the manifest and the blocks
   always agree.

5. **Place a block in each file.** For each node, compose a block spec and run
   `waypoint block --write --at <line>`, choosing the anchor line yourself:
   - Top of file for configs, scripts, manifests, and pipeline-specific files.
   - Directly above the relevant code section for source files where the
     pipeline touches a specific function or block.

   Re-running `block --write` on a file that already carries this pipeline's own
   well-formed block updates it in place rather than duplicating it. When the
   nearby block has lost its closing legend line or belongs to a different
   pipeline, the write refuses to replace it: it inserts a fresh block instead,
   leaves the existing one untouched, and returns an advisory naming what to
   remove by hand. A write never deletes content it cannot prove is this
   pipeline's own block. Preview any placement first with `block --dry-run`.

6. **Verify.** Run `waypoint verify <pipeline>`. Resolve any drift it reports
   before you report the work as done.

When a single source line participates in two or more pipelines, give that one
block multiple flows in its spec — the CLI stacks them under one ID. See the
multi-flow example in `references/cli.md`.

## Reading and auditing waypoints

- **List everything / find an entry point:** `waypoint scan`, then open the
  manifest's first row.
- **Check for drift:** `waypoint verify` (all pipelines) or `waypoint verify
  <pipeline>` (one). It reports stale rows, orphaned blocks, and stale IDs.
- **A file moved:** `waypoint check-ids` names every stale ID, its new value,
  and the neighbor references that must change. Apply the corrections — update
  the manifest row, recompose the moved file's block, and update each neighbor
  that pointed at the old ID — then re-run `verify`.
- **Trace from any node:** grep its 8-char ID, or follow `→`/`←` through the
  blocks and the manifest topology.

## Block format

The CLI composes these; this section is the reference for what it produces and
why each part is there. The `Waypoint <id>` anchor and the symbol legend appear
in every block so a first-time reader can decode and grep it on sight.

A **single-flow source block** is compact. The reference path rides in the
header, and one closing line carries both the grep hint and the legend:

```
── Waypoint a1b2c3d4 · sourcemap-upload · reference: .ai/waypoints/sourcemap-upload.md
   uploads browser sourcemaps to Sentry so minified errors resolve to source
   ← 4263ae66  docker-compose.ci.yml — passes the release version into this build
   → 80e5dc26  browser.plugins.ts — uploads browser sourcemaps to Sentry
── grep any 8-char ID to trace this pipeline · ← from  → into  ◁ reads  ▷ feeds
```

A **multi-flow line** — one source line that two or more pipelines touch —
stacks the flows under one ID, each naming its own reference:

```
── Waypoint a1b2c3d4 · grep any 8-char ID to trace these pipelines ──
   sourcemap-upload — uploads browser sourcemaps to Sentry
     ← 4263ae66  docker-compose.ci.yml — passes the release version in
     reference: .ai/waypoints/sourcemap-upload.md
   changeset-release — bumps versions and tags the release
     → 1a2b3c4d  publish.yml — publishes the tagged packages to npm
     reference: .ai/waypoints/changeset-release.md
── ← from  → into  ◁ reads  ▷ feeds
```

The **map file** at `.ai/waypoints/<name>.md` keeps the rich layout: an opening
narrative sentence, a node table ordered by execution with sinks last, and a
`## Topology` graph. The opening sentence is the most important line in the
system — write it as one sentence that walks the pipeline's stages in order,
naming what happens at each and why. The CLI writes the file; you write the
sentence.

Each block is rendered in the file's native comment syntax. The CLI resolves
that from the extension; the comment-syntax table and the `--comment` override
are documented in `references/cli.md`.

## Writing voice

Waypoint text is read by someone meeting the system for the first time. The
voice guide at [`references/waypoint-voice.md`](references/waypoint-voice.md)
defines the principles — concrete over abstract, active over passive, orient
first, purpose over mechanics, self-evident, warm over telegraphic. Load it
before writing or polishing any role description, neighbor description, or
manifest opening sentence.
