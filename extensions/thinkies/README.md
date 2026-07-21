# thinkies

A Claude Code plugin bundling the 48 reasoning skills from [`skills/thinkies/`](../../skills/thinkies/) — techniques for decomposing problems, asking better questions, excavating assumptions, shifting perspective, analyzing decisions, generating and filtering ideas, and checking claims against evidence.

Each skill installs under the plugin namespace and invokes as `/thinkies:<name>` — for example `/thinkies:decompose` or `/thinkies:run-premortem`.

## Install locally (development)

From the repo root:

```
claude --plugin-dir extensions/thinkies
```

This loads the plugin for the current Claude Code session only.

## Install from the marketplace

This repo doubles as a plugin marketplace (name: `ai-skills`):

```
/plugin marketplace add synapseradio/ai-skills
/plugin install thinkies@ai-skills
```

## What this plugin ships

| Component | Path |
|---|---|
| Plugin manifest | `.claude-plugin/plugin.json` |
| Skills (48) | `skills/<name>/` |

The skill directories copy the canonical sources at [`skills/thinkies/`](../../skills/thinkies/). The source tree holds the single source of truth; when it changes, the copies in this bundle are regenerated. See the repo [`CLAUDE.md`](../../CLAUDE.md) for the convention.

## Related

- Each skill also ships as a standalone `.skill` ZIP for Claude.ai upload, under [`packaged/thinkies/`](../../packaged/thinkies/).
- Source skills + references: [`skills/thinkies/`](../../skills/thinkies/)

## License

[EUPL-1.2](../../LICENSE)
