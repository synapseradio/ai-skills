# ai-skills

Agent skills and agent definitions for [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## Skills

Skills fall into two groups plus one standalone advisor. The **thinkies** group under [`skills/thinkies/`](./skills/thinkies/) collects reasoning and thinking techniques; it also installs as a bundle through the thinkies plugin (see [Extensions](#extensions)). The **tech** group under [`skills/tech/`](./skills/tech/) collects technical and engineering skills. The one flat skill, **de-residency-advisor** ([`skills/de-residency-advisor/`](./skills/de-residency-advisor/)), coaches non-EU expats preparing for German government appointments on visa, residency, and citizenship, researching each answer live and citing every claim.

### thinkies

| Skill | Description |
|-------|-------------|
| **argue-the-opposite** | Stress-test a position by building the strongest counter-case |
| **ask-questions** | Ask a genuinely good question, or a composed set, in the moment |
| **ask-respond** | Structured Q&A that decomposes questions before answering |
| **ask-what-breaks** | Find defeaters that would break a conclusion |
| **assess-current-knowledge** | Map what's known vs assumed vs unknown |
| **audit-chain-of-thought** | Tag reasoning steps by inference type |
| **branch-possibilities** | Generate fundamentally divergent directions from one starting point |
| **calibrate-confidence** | Match certainty to evidence strength |
| **check-soundness** | Test synthesis for contradictions |
| **cite** | Generate APA-format citations from paper links |
| **cite-sources** | Track, validate, and cite external sources with working URLs |
| **communicate** | Communicate ideas with purpose, clarity, and integrity while avoiding AI slop |
| **connect-domains** | Import solutions from structurally similar problems in distant domains |
| **consider-alternatives** | Generate competing explanations for the same observations |
| **decision-analysis** | Formulate and evaluate one concrete decision under uncertainty |
| **decompose** | Break a whole into parts at its natural joints |
| **derive-first-principles** | Strip convention to irreducible truths and rebuild |
| **detect-diminishing-returns** | Detect when further effort yields little gain |
| **detect-fallacies** | Spot logical errors in reasoning |
| **evaluate-evidence** | Assess how well evidence supports claims |
| **excavate-assumptions** | Surface unstated assumptions at multiple levels and rank them |
| **find-leverage** | Locate where a small change shifts the whole system |
| **flip-assumptions** | Test claims by forming the contrapositive |
| **ideate** | Generate and filter ideas into vetted options |
| **integrate-other-perspectives** | Combine viewpoints into a coherent whole |
| **integrity** | Verify epistemic integrity by aligning claims with evidence |
| **invert-the-problem** | Turn a problem inside out to reveal hidden structure |
| **ponder** | Explore a problem through a sequence of techniques before solving |
| **probe-boundaries** | Test a claim or framing at its edges and extremes |
| **prompt** | Craft or refactor LLM instructions |
| **question-the-question** | Examine whether the inquiry is aimed at the right target |
| **question-through-dialogue** | Use Socratic questioning to reveal assumptions |
| **research-and-teach** | Research deeply, explain progressively |
| **run-premortem** | Imagine catastrophic failure and work backwards to prevent it |
| **scamper** | Structured ideation using the SCAMPER creative thinking technique |
| **shift-abstraction-level** | Move up, down, and sideways between levels of abstraction |
| **shift-perspective** | Inhabit contrasting frames to see what one viewpoint misses |
| **skill-design** | Design, strengthen, or audit an Agent Skill |
| **strategize** | Adaptive multi-phase reasoning for complex problems |
| **surface-intent** | Surface intent before you add, change, or produce something |
| **synthesize-opposing-views** | Find higher understanding through dialectic |
| **trace-logic** | Follow reasoning step-by-step |
| **trace-logical-justifications** | Trace justification chains to bedrock |
| **tree-of-thought** | Systematic Tree of Thought reasoning for complex problem decomposition |
| **tutor** | Interactive tutoring that adapts to your pace |
| **visualize** | Visualize data, concepts, relations, or diagrams as browser-runnable charts |
| **what-if** | Tile the space of possible futures and evaluate strategies across them |
| **wonder** | Open the possibility space through curiosity-driven questioning |

### tech

Technical skills grouped under [`skills/tech/`](./skills/tech/).

| Skill | Description |
|-------|-------------|
| **apache-age** | Apache AGE (Postgres graph extension): Cypher + SQL patterns, schema modeling, query optimization |
| **bash-scaffold** | Scaffold a production-grade bash script from a curated template |
| **cli-development** | CLI development reference grounded in [clig.dev](https://clig.dev) |
| **flix** | Write, translate, and reason about [Flix](https://flix.dev) code |
| **runbook** | Decompose work into steerable autonomous loops, in seed and execute modes |
| **shape-up** | Conversational requirements elicitation producing shaped specifications |
| **shell-testing** | Write idiomatic BATS tests for bash and zsh shell scripts |
| **ts-typeclasses** | Implement typeclasses and their higher-kinded type encoding in TypeScript |
| **waypoint** | Distributed navigation markers for multi-file pipelines and processes |

## Agents

| Agent | Description |
|-------|-------------|
| **research-surveyor** | Rigorous topic surveys with cited sources |
| **scout** | Landscape reconnaissance and target identification |
| **shell-dx-architect** | Shell script DX: conventions, comments, consistency |

## Extensions

Claude Code plugin bundles live in [`extensions/`](./extensions). Each plugin wraps one or more skills and installs as a single unit via `/plugin install …` or `claude --plugin-dir …`. Two bundles ship here: **de-residency** wraps the de-residency-advisor skill, and **thinkies** bundles all 48 reasoning skills, each invoked as `/thinkies:<name>`. See [`extensions/README.md`](./extensions/README.md) for details.

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

Extensions: `claude --plugin-dir extensions/<plugin-name>` for local use, or install from this repo's own marketplace:

```
/plugin marketplace add synapseradio/ai-skills
/plugin install thinkies@ai-skills
```

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
