# thinkies

A Claude Code plugin bundling the 57 reasoning skills from [`skills/thinkies/`](../../skills/thinkies/) — techniques for decomposing problems, asking better questions, excavating assumptions, shifting perspective, analyzing decisions, generating and filtering ideas, and checking claims against evidence.

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
| Skills (57) | `skills/<name>/` |

The skill directories copy the canonical sources at [`skills/thinkies/`](../../skills/thinkies/). The source tree holds the single source of truth; when it changes, the copies in this bundle are regenerated. See the repo [`CLAUDE.md`](../../CLAUDE.md) for the convention.

## Records

Eight skills save a record of each run: ask-questions, ask-respond, connect-ideas, domain-analysis, generate-questions, map-out, ponder, and save-note. check-notes finds records by topic, skill, or date and plays them back. Each record is a JSON Lines file named `skill_time_topic.jsonl`, kept in the plugin's data directory under `records/`.

Claude Code deletes the plugin's data directory when the plugin is uninstalled from the last place it is installed. To keep it:

```
claude plugin uninstall thinkies@ai-skills --keep-data
```

To keep a second copy in a folder you choose, set **Records mirror folder** when you enable the plugin, or later in `/config`. Each run's record is copied there, and check-notes reads the mirror for any record the data directory lacks.

Outside this plugin (the `.skill` upload, the Skills API, the Codex bundle, or a skill copied into `~/.claude/skills/`) there is no store, and these skills print each record in the reply as a `jsonl` block for you to save.

## Related

- Each skill also ships as a standalone `.skill` ZIP for Claude.ai upload, under [`packaged/thinkies/`](../../packaged/thinkies/).
- Source skills + references: [`skills/thinkies/`](../../skills/thinkies/)

## License

[EUPL-1.2](../../LICENSE)
