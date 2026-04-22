# de-residency

A Claude Code plugin that wraps the [`de-residency-advisor`](../../skills/de-residency-advisor/) skill — a conversational coach for non-EU expats preparing for German government appointments (Ausländerbehörde / LEA, Einbürgerungsbehörde, Approbation, Standesamt, embassy visa interview).

The skill researches every claim live and cites each factual statement with a URL. It does not carry a frozen knowledge base — German fees, thresholds, document lists, and even which authority is responsible all shift over time.

## Install locally (development)

From the repo root:

```
claude --plugin-dir extensions/de-residency
```

This loads the plugin for the current Claude Code session only.

## Install from a marketplace

Once published to a marketplace manifest:

```
/plugin marketplace add <marketplace-source>
/plugin install de-residency@<marketplace-name>
```

## What this plugin ships

| Component | Path |
|---|---|
| Plugin manifest | `.claude-plugin/plugin.json` |
| Skill | `skills/de-residency-advisor/` |

The skill directory is a copy of the canonical source at `/skills/de-residency-advisor/`. The source is the single source of truth; when it changes, the copy in this bundle is regenerated. See the repo [`CLAUDE.md`](../../CLAUDE.md) for the convention.

## Host requirements

The skill expects the host agent to be able to look up and read web pages live — any browsing, search, or fetch capability works. There is no hard dependency on a specific provider.

## Related

- The same skill is also distributed as a standalone `.skill` ZIP for Claude.ai upload:
  [`de-residency-advisor.skill`](https://github.com/synapseradio/ai-skills/raw/main/skills/packaged/de-residency-advisor.skill)
- Source skill + references: [`skills/de-residency-advisor/`](../../skills/de-residency-advisor/)

## License

[EUPL-1.2](../../LICENSE)
