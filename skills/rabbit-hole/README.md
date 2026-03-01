# rabbit-hole

Multi-agent investigation pipeline for deep research questions. Separates territory-mapping (cheap, fast) from deep investigation (expensive, thorough) across multiple sources — codebase, web, docs, and academic.

## Install

```sh
claude install-skill github:synapseradio/ai-skills/skills/rabbit-hole
```

## How it works

```
TRIAGE → SCOUT (find leads) → INVESTIGATE (parallel deep dives) → VALIDATE → REPORT
```

1. **Triage** — simple questions get answered directly; complex ones enter the pipeline
2. **Scout** — a fast agent finds 3-15 leads across all available sources
3. **Investigate** — 1-3 parallel agents read sources and extract cited findings
4. **Validate** — citations are verified, sources ranked by tier, findings synthesized
5. **Report** — convergence, divergence, and gaps presented; user can go deeper on any branch

Readonly. Always cites. Always validates.

## Contents

| File | Purpose |
|------|---------|
| `scripts/validate_sources.py` | Deterministic citation validator (stdlib only) |
| `references/research-hierarchy.md` | Source tier definitions and conflict resolution rules |

## Usage

```
/rabbit-hole How does React's concurrent rendering actually work under the hood?
/rabbit-hole What are the tradeoffs between SQLite and DuckDB for embedded analytics?
```

## License

MIT
