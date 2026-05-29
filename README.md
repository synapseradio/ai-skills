# ai-skills

Agent skills and agent definitions for [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## Skills

| Skill | Description |
|-------|-------------|
| **apache-age** | Apache AGE (Postgres graph extension): Cypher + SQL patterns, schema modelling, query optimisation |
| **cite** | Generate APA-format citations from paper links |
| **communicate** | Written communication with 16 techniques and 5 structured workflows |
| **create-skill** | Research-first pipeline for producing spec-compliant Agent Skills |
| **de-residency-advisor** | Conversational coach for non-EU expats preparing for German government appointments — visa, residency, citizenship |
| **flix** | Write, translate, and reason about [Flix](https://flix.dev) code |
| **ponder** | Exploration skill for problems that need thinking before solving |
| **rabbit-hole** | Multi-agent investigation pipeline for deep research questions |
| **runbook** | Decompose tasks into steerable autonomous loops |
| **scamper** | Structured ideation using the SCAMPER creative thinking technique |
| **sequencer** | Chain skills, agents, and instructions into ordered pipelines |
| **shape-up** | Conversational requirements elicitation producing shaped specifications |
| **shell-testing** | Write idiomatic BATS tests for bash and zsh shell scripts |
| **skill-review** | Audit Agent Skills against the specification |
| **stax** | Stacked Git branches and PRs via the stax CLI |
| **team** | Expert persona collaboration for structured problem analysis |
| **tree-of-thought** | Systematic Tree of Thought reasoning for complex problem decomposition |
| **visualize** | Data visualizations using Vega or D3 with 19+ chart templates |
| **waypoint** | Distributed navigation markers for multi-file pipelines and processes |

### thinkies

Cognitive reasoning skills grouped under [`skills/thinkies/`](./skills/thinkies/). Each is a self-contained thinking technique adapted from the [seed](https://github.com/synapseradio/seed) thinkies plugin.

| Skill | Description |
|-------|-------------|
| **argue-the-opposite** | Stress-test a position by building the strongest counter-case |
| **ask-respond** | Structured Q&A that decomposes questions before answering |
| **ask-what-breaks** | Find defeaters that would break a conclusion |
| **assess-current-knowledge** | Map what's known vs assumed vs unknown |
| **audit-chain-of-thought** | Tag reasoning steps by inference type |
| **branch-possibilities** | Generate fundamentally divergent directions from one starting point |
| **calibrate-confidence** | Match certainty to evidence strength |
| **check-soundness** | Test synthesis for contradictions |
| **cite-sources** | Track, validate, and cite external sources with working URLs |
| **connect-domains** | Import solutions from structurally similar problems in distant domains |
| **consider-alternatives** | Generate competing explanations for the same observations |
| **decompose** | Break a whole into parts at its natural joints |
| **detect-diminishing-returns** | Detect when further effort yields little gain |
| **detect-fallacies** | Spot logical errors in reasoning |
| **evaluate-evidence** | Assess how well evidence supports claims |
| **excavate-assumptions** | Surface unstated assumptions at multiple levels and rank them |
| **find-leverage** | Locate where a small change shifts the whole system |
| **flip-assumptions** | Test claims by forming the contrapositive |
| **ideate** | Generate and filter ideas into vetted options |
| **integrate-other-perspectives** | Combine viewpoints into coherent whole |
| **integrity** | Verify structural integrity by aligning claims with evidence |
| **invert-the-problem** | Turn a problem inside out to reveal hidden structure |
| **probe-boundaries** | Test a claim or framing at its edges and extremes |
| **question-the-question** | Examine whether the inquiry is aimed at the right target |
| **question-through-dialogue** | Use Socratic questioning to reveal assumptions |
| **reason-from-first-principles** | Strip convention to irreducible truths and rebuild |
| **research-and-teach** | Research deeply, explain progressively |
| **run-premortem** | Imagine catastrophic failure and work backwards to prevent it |
| **shift-abstraction-level** | Move up, down, and sideways between levels of abstraction |
| **shift-perspective** | Inhabit contrasting frames to see what one viewpoint misses |
| **strategize** | Adaptive multi-phase reasoning for complex problems |
| **synthesize-opposing-views** | Find higher understanding through dialectic |
| **trace-logic** | Follow reasoning step-by-step |
| **trace-logical-justifications** | Trace justification chains to bedrock |
| **tutor** | Interactive tutoring that adapts to your pace |
| **wonder** | Open the possibility space through curiosity-driven questioning |

## Agents

| Agent | Description |
|-------|-------------|
| **research-surveyor** | Rigorous topic surveys with cited sources |
| **scout** | Landscape reconnaissance and target identification |
| **shell-dx-architect** | Shell script DX: conventions, comments, consistency |

## Extensions

Claude Code plugin bundles live in [`extensions/`](./extensions). Each plugin wraps one or more skills and installs as a single unit via `/plugin install …` or `claude --plugin-dir …`. See [`extensions/README.md`](./extensions/README.md) for the list.

## Install

Skills, three options:

```bash
# Option 1 — Claude Code / Cursor / Codex / any agentskills.io-compatible client:
npx skills add https://github.com/synapseradio/ai-skills

# Option 2 — Claude.ai upload: download the .skill file from packaged/
#   and upload it via Settings → Skills → Upload. Each skill's README has a
#   direct link to its .skill.

# Option 3 — copy a skill directory into ~/.claude/skills/ manually.
```

Agents: copy from `agents/` into `~/.claude/agents/`.

Extensions: `claude --plugin-dir extensions/<plugin-name>` for local use, or install from a marketplace.

## Packaging

Every source skill has a matching `.skill` ZIP under [`packaged/`](./packaged/). The packaging tool is the `skill-creator` plugin's `package_skill.py` — invoked in place, not vendored. See [`CLAUDE.md`](./CLAUDE.md) for the full convention and re-packaging commands.

## Development

### Prerequisites

- [Bun](https://bun.sh) (package manager)
- [ruff](https://docs.astral.sh/ruff/) (`brew install ruff`)
- [ShellCheck](https://www.shellcheck.net/) (available at `/opt/local/bin/shellcheck` or `brew install shellcheck`)

### Setup

```sh
bun install
bunx lefthook install
```

### Linting

[Lefthook](https://github.com/evilmartians/lefthook) runs pre-commit hooks that auto-fix staged files:

| Files | Tool |
|-------|------|
| `.md` | markdownlint |
| `.json` | biome |
| `.html` | prettier |
| `.yml` / `.yaml` | prettier |
| `.py` | ruff |
| `.sh` | shellcheck |

A commit-msg hook enforces [conventional commits](https://www.conventionalcommits.org/) via commitlint.

To lint the entire repo manually:

```sh
bun run lint:fix
```

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
