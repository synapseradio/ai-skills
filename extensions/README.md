# extensions/

Claude Code plugin bundles. Each subdirectory is a self-contained plugin wrapping one or more skills from this repo.

## Layout

```
extensions/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json       # required: name; strongly recommended: version, description, author, repository, license
├── README.md             # install instructions, what the plugin does
└── skills/
    └── <skill-name>/
        └── SKILL.md      # copy of the source skill
```

The skill under a plugin is a build artifact. The source of truth lives in `/skills/<skill-name>/`. When the source changes, re-copy the tree into the extension bundle before committing.

## Install a plugin locally (development)

```
claude --plugin-dir extensions/<plugin-name>
```

This loads the plugin for the current session only — nothing is installed globally.

## Install from a marketplace

Once a plugin is published through a marketplace (`.claude-plugin/marketplace.json`):

```
/plugin marketplace add <marketplace-source>
/plugin install <plugin-name>@<marketplace-name>
```

## Plugins in this repo

| Plugin | Wraps skill | Purpose |
|---|---|---|
| [`de-residency`](./de-residency) | `de-residency-advisor` | Conversational coach for non-EU expats preparing for German government appointments. |

## Conventions

See the repo `CLAUDE.md` for the full set of rules. Most relevant here:

- `.claude-plugin/plugin.json` must live inside `.claude-plugin/`; all other component dirs (`skills/`, `agents/`, `commands/`, `hooks/`) must be at plugin root.
- `name` in `plugin.json` must be kebab-case and unique.
- Use `${CLAUDE_PLUGIN_ROOT}` for any intra-plugin path reference (hook commands, MCP server args). Never hardcode absolute paths.

For the companion `.skill` ZIP format (Claude.ai upload), see `/skills/packaged/` and the "Packaging a skill to `.skill`" section of the repo `CLAUDE.md`.
