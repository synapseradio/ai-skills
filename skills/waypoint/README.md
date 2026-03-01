# waypoint

Distributed navigation markers for multi-file pipelines and processes. Each file carries a compact comment block with its ID, role, neighbors, and a pointer to the full map — so the topology is discoverable from any node without centralized documentation that drifts.

## Install

```sh
claude install-skill github:synapseradio/ai-skills/skills/waypoint
```

## What it does

- Generates deterministic waypoint IDs from file paths (SHA-256, first 8 hex chars)
- Places grep-friendly comment blocks in each file with role, neighbors, and map pointer
- Maintains a manifest per pipeline in `.ai/waypoints/`
- Validates waypoints against manifests to detect drift

## Workflows

Three subagent workflows handle different operations:

| Workflow | Reference | Trigger |
|----------|-----------|---------|
| **Setter** | `references/workflow-setter.md` | "add waypoints", "trace this pipeline", "map this process" |
| **Reader** | `references/workflow-reader.md` | "list waypoints", "show pipelines", "check for drift" |
| **Scribe** | `references/workflow-scribe.md` | Runs automatically after setter; polishes descriptions |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/waypoint-id.ts` | Generate waypoint IDs from file paths |
| `scripts/validate-waypoints.ts` | Validate manifests against actual file contents |

## References

| File | Purpose |
|------|---------|
| `references/waypoint-voice.md` | Writing voice guide for waypoint descriptions |

## Usage

```
/waypoint trace the deployment pipeline from CI through Helm
/waypoint add waypoints for how feature flags propagate to components
/waypoint check for drift in the sourcemap-upload pipeline
```

## License

MIT
