# skill-review

Audits Agent Skill directories against the Agent Skills Specification and quality criteria. Produces a structured pass/fail report with specific fix instructions for each failure.

## Install

```sh
claude install-skill github:nke/ai-skills/skills/skill-review
```

## What it does

- Validates frontmatter fields (name format, description voice, reserved words)
- Checks progressive disclosure (SKILL.md size, conditional loading, reference depth)
- Fetches and verifies every URL in reference files
- Audits scripts against shell standards
- Validates README completeness
- Checks workflow file metadata and task tracking instructions

## References

| File | Purpose |
|------|---------|
| `references/checks-spec.md` | Frontmatter and spec compliance checks |
| `references/checks-references.md` | Reference file quality and URL reachability |
| `references/checks-scripts.md` | Shell script standards |
| `references/checks-structure.md` | README, task tracking, progressive disclosure, workflow metadata |
| `references/report-template.md` | Output report format |

## Usage

```
Review the skill at ~/.claude/skills/my-skill/
```

Or after creating a skill:
```
/skill-review path/to/skill
```
