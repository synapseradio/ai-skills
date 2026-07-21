# waypoint

Distributed navigation markers for multi-file pipelines and processes. Each file carries a compact comment block with its ID, role, neighbors, and a pointer to the full map — so the topology is discoverable from any node without centralized documentation that drifts.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/waypoint/` into `~/.claude/skills/waypoint/`.

## Usage

```
/waypoint trace the deployment pipeline from CI through Helm
/waypoint add waypoints for how feature flags propagate to components
/waypoint check for drift in the sourcemap-upload pipeline
```

## What it does

A single zero-dependency Python CLI does all the deterministic work; the skill supplies the prose. Grep any 8-character ID and the whole pipeline unfolds across files.

- Generates deterministic waypoint IDs from file paths (SHA-256 of the git-relative path, first 8 hex chars).
- Composes compact, grep-friendly comment blocks in each file's native comment syntax and places or updates them in line.
- Writes a manifest per pipeline in `.ai/waypoints/` with an opening narrative sentence, a node table ordered by execution, and a topology graph.
- Verifies blocks against manifests to detect drift, and emits an exact correction list when a file moves and its ID changes.

## When to use this

Use it when a process spans many files and the connections between them are hard to trace — deployment pipelines, data flows, feature flag propagation, anything where "how does this get from A to B?" is a recurring question. Waypoints make the topology discoverable from any file in the chain, without relying on external diagrams that inevitably fall out of sync.

Not useful for single-file scripts or processes that are already obvious from the directory structure.

## The CLI

```bash
python3 scripts/waypoint.py <subcommand> [args]
```

| Subcommand | Purpose |
|------------|---------|
| `id <path>...` | Print `<id>  <path>` for each file. |
| `scan` | Catalogue every map file and every block in the code. |
| `manifest` | Write `.ai/waypoints/<name>.md` from a JSON spec on stdin. |
| `block` | Compose a source block from a JSON spec on stdin; `--write --at <line>` places it. |
| `verify [pipeline]` | Detect stale rows, orphaned blocks, and stale IDs. |
| `check-ids` | Recompute IDs from paths and emit the correction list. |

Full reference — every flag, the JSON spec schemas, the comment-syntax table, and worked examples — lives in [`references/cli.md`](references/cli.md). The writing voice for role and neighbor descriptions lives in [`references/waypoint-voice.md`](references/waypoint-voice.md).

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`waypoint.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/tech/waypoint.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
