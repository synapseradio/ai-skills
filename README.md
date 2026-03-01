# ai-skills

Agent skills and agent definitions for [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## Skills

| Skill | Description |
|-------|-------------|
| **cite** | Generate APA-format citations from paper links |
| **flix** | Write, translate, and reason about [Flix](https://flix.dev) code |
| **rabbit-hole** | Multi-agent investigation pipeline for deep research questions |
| **scamper** | Structured ideation using the SCAMPER creative thinking technique |
| **shell-testing** | Write idiomatic BATS tests for bash and zsh shell scripts |
| **team** | Expert persona collaboration for structured problem analysis |
| **tree-of-thought** | Systematic Tree of Thought reasoning for complex problem decomposition |
| **waypoint** | Distributed navigation markers for multi-file pipelines and processes |

## Agents

| Agent | Description |
|-------|-------------|
| **research-surveyor** | Rigorous topic surveys with cited sources |
| **scout** | Landscape reconnaissance and target identification |
| **shell-dx-architect** | Shell script DX: conventions, comments, consistency |

## Install

Skills:
```sh
claude install-skill github:synapseradio/ai-skills/skills/<skill-name>
```

Agents: copy from `agents/` into your `.claude/agents/` directory.

## License

MIT
