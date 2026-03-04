# create-skill

Research-first pipeline for producing Agent Skills that meet the [Agent Skills Specification](https://agentskills.io/specification). Ensures every skill is backed by cited documentation, includes workflow templates for procedural tasks, and prevents agents from substituting hallucinated patterns for real docs.

## Install

```sh
claude install-skill github:synapseradio/ai-skills/skills/create-skill
```

## What it does

- Researches the skill's subject domain exhaustively before writing anything
- Gathers requirements from the user with scoping questions
- Creates spec-compliant skill directories with cited reference files
- Reviews the result against quality criteria and validates all URLs
- Runs the Anthropic skill-creator for description optimization

## Workflow

1. **Load guidance** — reads official skill-development best practices
2. **Bootstrap** — clones/pulls the Agent Skills Specification repo
3. **Research** *(subagent)* — finds and catalogs all official documentation
4. **Requirements** *(inline)* — asks the user what the skill should do and where to write it
5. **Author** *(subagent)* — creates the complete skill directory with all files
6. **Optimize** — runs the Anthropic skill-creator for description testing
7. **Review** *(subagent)* — validates against quality criteria and spec compliance
8. **Refine** *(subagent, if needed)* — applies fixes from review, re-validates (max 2 cycles)
9. **Report** — presents findings with any remaining issues

## References

| File | Purpose |
|------|---------|
| `references/workflow-research.md` | Subagent prompt for research phase |
| `references/workflow-requirements.md` | Inline prompt for requirements gathering |
| `references/workflow-author.md` | Subagent prompt for skill authoring |
| `references/workflow-review.md` | Subagent prompt for post-creation review |
| `references/workflow-refine.md` | Subagent prompt for fix-and-reverify loop |
| `references/quality-criteria.md` | Quality bar: what makes a good skill |
| `references/shell-script-standards.md` | Google Shell Style Guide rules for scripts |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/ensure_spec_repo.sh` | Clone/pull the Agent Skills Spec repo to `~/.agent-skills-spec` |

## Usage

```
/create-skill a skill for writing Terraform modules
/create-skill build a skill for Apache Kafka consumer patterns
/create-skill make a skill for React Server Components
```

## License

MIT
