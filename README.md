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
| **apply** | Apply insights to concrete situations |
| **challenge** | Stress-test ideas through structured critique |
| **connect** | Find relationships between disparate concepts |
| **decide** | Structured decision-making with tradeoff analysis |
| **document** | Generate documentation from code and context |
| **evaluate** | Assess quality, fitness, or correctness |
| **explore** | Open-ended investigation of a topic or space |
| **expression** | Refine and clarify written expression |
| **ground** | Anchor abstract ideas in concrete evidence |
| **here-now** | Present-moment awareness and situation assessment |
| **imagineer** | Creative engineering and speculative design |
| **navigate** | Find paths through complex problem spaces |
| **plan** | Structured planning and roadmap creation |
| **reflect** | Retrospective analysis and lesson extraction |
| **reframe** | Shift perspective on problems and situations |
| **research-surveyor** | Rigorous topic surveys with cited sources |
| **round-table** | Multi-perspective discussion and synthesis |
| **scout** | Landscape reconnaissance and target identification |
| **shell-dx-architect** | Shell script DX: conventions, comments, consistency |
| **understand** | Deep comprehension of systems and concepts |
| **verify** | Validate claims, assumptions, and correctness |
| **wander** | Exploratory, curiosity-driven investigation |
| **waypoint-reader** | Read and catalogue waypoint navigation markers |
| **waypoint-scribe** | Polish waypoint descriptions for clarity |
| **waypoint-setter** | Trace processes and place waypoint markers |

## Install

Skills:
```sh
claude install-skill github:synapseradio/ai-skills/skills/<skill-name>
```

Agents: copy from `agents/` into your `.claude/agents/` directory.

## License

MIT
