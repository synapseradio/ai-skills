# visualizer

A Claude Code plugin that wraps the [`visualize`](../../skills/visualize/) skill. The skill turns data, a comparison, a trend, a flow, or a structure into a chart or diagram a reader can check. It writes either a self-contained HTML page that opens from disk, or a Markdown output (a Mermaid diagram, a table, text bars) that fits a pull request, README, ticket, or chat. It runs its own check on the output before handing it over.

## Install locally (development)

From the repo root:

```
claude --plugin-dir extensions/visualizer
```

This loads the plugin for the current Claude Code session only.

## Install from the marketplace

This repo doubles as a plugin marketplace (name: `ai-skills`):

```
/plugin marketplace add synapseradio/ai-skills
/plugin install visualizer@ai-skills
```

## Use

Installed, the skill invokes as `/visualizer:visualize`:

```
/visualizer:visualize show weekly signups by channel from signups.csv
```

## What this plugin ships

| Component | Path |
|---|---|
| Plugin manifest | `.claude-plugin/plugin.json` |
| Skill | `skills/visualize/` |

The skill directory is a copy of the canonical source at `/skills/visualize/`, without its `evals/` directory. The source is the single source of truth; when it changes, the copy in this bundle is regenerated. See the repo [`CLAUDE.md`](../../CLAUDE.md) for the convention.

## Host requirements

The skill's scripts run under Bun 1.4 or later. The HTML page loads its chart library when the reader opens it.
