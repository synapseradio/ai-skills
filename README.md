# ai-skills

Agent skills and agent definitions for [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## Skills

Skills fall into two groups plus one standalone advisor. The **thinkies** group under [`skills/thinkies/`](./skills/thinkies/) collects reasoning and thinking techniques; it also installs as a bundle through the thinkies plugin (see [Extensions](#extensions)). The **tech** group under [`skills/tech/`](./skills/tech/) collects technical and engineering skills. The one flat skill, **de-residency-advisor** ([`skills/de-residency-advisor/`](./skills/de-residency-advisor/)), coaches non-EU expats preparing for German government appointments on visa, residency, and citizenship, researching each answer live and citing every claim.

### thinkies

| Skill | Reach for it when | Description |
|-------|-------------------|-------------|
| [**argue-the-opposite**](./skills/thinkies/argue-the-opposite/) | You hold a position and nobody has pushed back yet | Stress-test a position by building the strongest counter-case |
| [**ask-questions**](./skills/thinkies/ask-questions/) | You're about to ask someone something, and it has to land | Ask the user the next good question, or make the better non-question move |
| [**ask-respond**](./skills/thinkies/ask-respond/) | A simple-looking question carries assumptions nobody checked | Structured Q&A that decomposes questions before answering |
| [**ask-what-breaks**](./skills/thinkies/ask-what-breaks/) | You've reached a conclusion and want to know what would overturn it | Find defeaters that would break a conclusion |
| [**assess-current-knowledge**](./skills/thinkies/assess-current-knowledge/) | You can't say which of your beliefs you've actually checked | Map what's known vs assumed vs unknown |
| [**audit-chain-of-thought**](./skills/thinkies/audit-chain-of-thought/) | An argument reaches a big conclusion and you can't see which step carries it | Tag reasoning steps by inference type |
| [**branch-possibilities**](./skills/thinkies/branch-possibilities/) | Every option on the table is a variation of the first idea | Generate fundamentally divergent directions from one starting point |
| [**calibrate-confidence**](./skills/thinkies/calibrate-confidence/) | A claim is stated flatly and you can't tell how much of it the evidence carries | Match certainty to evidence strength |
| [**check-notes**](./skills/thinkies/check-notes/) | You worked something out earlier and want the finding back, not a rerun | Find saved notes and run records and play them back |
| [**check-soundness**](./skills/thinkies/check-soundness/) | You've pulled several pieces into one plan and want to know they can all be true | Test synthesis for contradictions |
| [**cite-sources**](./skills/thinkies/cite-sources/) | A claim needs a source a reader can open | Track, validate, and cite external sources with working URLs |
| [**communicate**](./skills/thinkies/communicate/) | You have a piece to write or polish, and an audience it has to reach | Communicate ideas with purpose, clarity, and integrity |
| [**compose**](./skills/thinkies/compose/) | You hold a pile of half-ideas that might add up to something | Join parts into a whole and find what it still lacks |
| [**connect-ideas**](./skills/thinkies/connect-ideas/) | Two things feel alike and you want to know whether the likeness holds | Test how two ideas relate, or find a distant match for one |
| [**consider-alternatives**](./skills/thinkies/consider-alternatives/) | One explanation arrived first and nobody has looked for a second | Generate competing explanations for the same observations |
| [**decision-analysis**](./skills/thinkies/decision-analysis/) | One choice turns on facts you don't control, and you keep going round in circles | Formulate and evaluate one concrete decision under uncertainty |
| [**decompose**](./skills/thinkies/decompose/) | A job is too big to start and every list of it feels arbitrary | Break a whole into parts at its natural joints, one axis per level |
| [**derive-first-principles**](./skills/thinkies/derive-first-principles/) | Something costs far more than it seems it should, and "that's how it's done" is the only answer | Strip convention to irreducible truths and rebuild |
| [**detect-diminishing-returns**](./skills/thinkies/detect-diminishing-returns/) | You can't tell whether another pass is still making things better | Detect when further effort yields little gain |
| [**detect-fallacies**](./skills/thinkies/detect-fallacies/) | An argument feels persuasive and wrong at once | Spot logical errors in reasoning |
| [**domain-analysis**](./skills/thinkies/domain-analysis/) | You're about to change a system and want to see what each piece is for | Model a system from its purpose down to its parts, with who acts on and sees each piece |
| [**evaluate-evidence**](./skills/thinkies/evaluate-evidence/) | A few stories and a half-remembered study are offered as proof | Assess how well evidence supports claims |
| [**excavate-assumptions**](./skills/thinkies/excavate-assumptions/) | A plan sounds obviously good and nobody has asked what it takes for granted | Surface unstated assumptions at multiple levels and rank them |
| [**find-leverage**](./skills/thinkies/find-leverage/) | The same problem comes back after every fix | Trace a system's feedback loops to find where a small change shifts the whole |
| [**flip-assumptions**](./skills/thinkies/flip-assumptions/) | A rule of thumb sounds right and you can't think how you'd ever check it | Test claims by forming the contrapositive |
| [**generalize**](./skills/thinkies/generalize/) | Something works in one place and you want to know what it's an instance of | Find the class a case belongs to and carry back what holds for it |
| [**generate-questions**](./skills/thinkies/generate-questions/) | A decision needs other people's answers, and you want the questions ready first | Compose a set of questions toward a driving question and return it without asking anyone |
| [**ideate**](./skills/thinkies/ideate/) | You need options you can compare side by side, not one idea | Generate and filter ideas into vetted options |
| [**instantiate**](./skills/thinkies/instantiate/) | A value or policy sounds agreed, and you suspect everyone pictures something different | Make an abstraction concrete and find the conditions it assumed |
| [**integrate-other-perspectives**](./skills/thinkies/integrate-other-perspectives/) | Several people want different things and it has come down to "whose wins" | Combine viewpoints into a coherent whole |
| [**integrity**](./skills/thinkies/integrity/) | A text makes confident claims and you want to know which ones its evidence carries | Verify epistemic integrity by aligning claims with evidence |
| [**invert-the-problem**](./skills/thinkies/invert-the-problem/) | Every direct attempt at a goal meets resistance | Turn a problem inside out to reveal hidden structure |
| [**map-out**](./skills/thinkies/map-out/) | An argument circles because each side is talking at a different level | Find where a subject sits and the level to act at |
| [**ponder**](./skills/thinkies/ponder/) | A problem stays vague and you can't yet say what you want | Explore a problem through a sequence of techniques before solving |
| [**probe-boundaries**](./skills/thinkies/probe-boundaries/) | A definition works for every case you've tried, and you haven't tried the odd ones | Test a claim or framing at its edges and extremes |
| [**prompt**](./skills/thinkies/prompt/) | You have a task for a model and only a rough sentence, or a prompt that grew by accretion | Craft or refactor LLM instructions |
| [**question-the-question**](./skills/thinkies/question-the-question/) | Answers keep coming back correct and unhelpful | Examine whether the inquiry is aimed at the right target |
| [**question-through-dialogue**](./skills/thinkies/question-through-dialogue/) | You hold a conviction strongly and want to find out what it rests on | Use Socratic questioning to reveal assumptions |
| [**research-and-teach**](./skills/thinkies/research-and-teach/) | You want to understand why something happens, starting from little background | Research deeply, explain progressively |
| [**run-premortem**](./skills/thinkies/run-premortem/) | You're about to commit to a plan that gets one shot | Imagine catastrophic failure and work backwards to prevent it |
| [**save-note**](./skills/thinkies/save-note/) | Something clicked and you'll want it again in a month | Save an insight so it can be found again |
| [**scamper**](./skills/thinkies/scamper/) | You have a concrete thing and want variations on it | Structured ideation using the SCAMPER creative thinking technique |
| [**shift-abstraction-level**](./skills/thinkies/shift-abstraction-level/) | A task arrives too vague to start or too specific to question | Find the level of abstraction to act at |
| [**shift-perspective**](./skills/thinkies/shift-perspective/) | A decision is being made from one seat | Inhabit contrasting frames to see what one viewpoint misses |
| [**situate**](./skills/thinkies/situate/) | Something works fine on its own terms and still seems to be failing | Place a thing in the larger system it serves |
| [**skill-design**](./skills/thinkies/skill-design/) | You have an idea for a skill, or a skill that fires on the wrong requests | Design, strengthen, or audit an Agent Skill |
| [**strategize**](./skills/thinkies/strategize/) | Several constraints are tangled and you want to work through them together, step by step | Adaptive multi-phase reasoning for complex problems |
| [**surface-intent**](./skills/thinkies/surface-intent/) | You're about to add something to a system you haven't read all of | Surface intent before you add, change, or produce something |
| [**survey-peers**](./skills/thinkies/survey-peers/) | You know your option well and have never mapped what else does its job | Map what else fills the same role at the same level |
| [**synthesize-opposing-views**](./skills/thinkies/synthesize-opposing-views/) | Two positions each sound right and the argument keeps circling | Find higher understanding through dialectic |
| [**trace-logic**](./skills/thinkies/trace-logic/) | An argument persuades you and you can't say which step you'd push on | Follow reasoning step-by-step |
| [**trace-logical-justifications**](./skills/thinkies/trace-logical-justifications/) | A rule is stated as obvious ("we must never…") | Trace justification chains to bedrock |
| [**tree-of-thought**](./skills/thinkies/tree-of-thought/) | The right approach isn't obvious and choosing wrong costs a lot | Systematic Tree of Thought reasoning for complex problem decomposition |
| [**tutor**](./skills/thinkies/tutor/) | You want to learn something by working through it, at your own pace | Interactive tutoring that adapts to your pace |
| [**visualize**](./skills/thinkies/visualize/) | You have numbers and a hunch, and need a chart that says one thing | Visualize data, concepts, relations, or diagrams as browser-runnable charts |
| [**what-if**](./skills/thinkies/what-if/) | A decision hangs on things nobody can know yet | Tile the space of possible futures and evaluate strategies across them |
| [**wonder**](./skills/thinkies/wonder/) | You're about to solve something and haven't asked what's strange about it | Open the possibility space through curiosity-driven questioning |

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

Claude Code plugin bundles live in [`extensions/`](./extensions). Each plugin wraps one or more skills and installs as a single unit via `/plugin install …` or `claude --plugin-dir …`. Two bundles ship here: **de-residency** wraps the de-residency-advisor skill, and **thinkies** bundles all 57 reasoning skills, each invoked as `/thinkies:<name>`. See [`extensions/README.md`](./extensions/README.md) for details.

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
