# Commands Are Vestigial

## Finding

Anthropic's plugin documentation explicitly marks `commands/` as **legacy**:

> **Commands** (`commands/`): Skills as Markdown files (legacy; use `skills/` for new skills)
>
> — [Plugins reference](https://code.claude.com/docs/en/plugins-reference)

And from the skills documentation:

> Custom slash commands have been merged into skills. A file at `.claude/commands/review.md` and a skill at `.claude/skills/review/SKILL.md` both create `/review` and work the same way. Your existing `.claude/commands/` files keep working.
>
> — [Extend Claude with skills](https://code.claude.com/docs/en/skills)

## Current State in Software Plugin

The software plugin maintains **5 commands** and **4 skills**:

| Command | Proxies to Skill | Adds Value? |
|---------|-----------------|-------------|
| `/assess` | `skills/assess/SKILL.md` | No — just loads skill and does signal detection |
| `/design` | `skills/design/SKILL.md` | No — same pattern |
| `/implement` | `skills/implement/SKILL.md` | No — same pattern |
| `/refactor` | `skills/refactor/SKILL.md` | No — same pattern |
| `/vestigial-detect` | *(no skill)* | Yes — but should be a skill, not a command |

The four proxy commands follow an identical template:

```markdown
@${CLAUDE_PLUGIN_ROOT}/skills/{name}/SKILL.md

Parse the query for signals using the Signal Detection table...
If clear single signal: Load the corresponding mode reference...
```

This is routing logic that skills handle natively through their `description` field. The commands add a dispatch layer that duplicates what Claude's skill matching already does.

## Vestigial Classification

Applying the plugin's own vestigial detection heuristics:

- **Disconnected from surrounding structure**: Commands duplicate skill entry points rather than integrating with current plugin patterns
- **Duplicated meaning found elsewhere**: Every command's functionality exists in the corresponding skill
- **Served a function that migrated**: Commands predated skills in Claude Code's evolution; the function has moved to `skills/`
- **Accumulated rather than composed**: The 1:1 command-skill mapping was added incrementally without questioning whether both layers were needed

## Implication for Redesign

1. **Eliminate the `commands/` directory entirely** — skills handle invocation natively
2. **Promote vestigial-detect to a proper skill** with its scripts directory
3. **Skills become the only entry points** — description-based routing replaces manual signal detection
4. **Simplify plugin.json** — remove command paths, rely on auto-discovery of skills

## What Skills Provide That Commands Don't

| Feature | Commands | Skills |
|---------|----------|--------|
| Auto-invocation by Claude | No | Yes (via description matching) |
| Supporting files directory | No (hacks needed) | Yes (references/, scripts/) |
| Frontmatter control | Limited | Full (user-invocable, hooks, etc.) |
| Progressive disclosure | No | Yes (SKILL.md → references/) |
| Slash-command invocation | Yes | Yes (same `/name` syntax) |

Skills are a strict superset. Commands offer nothing additional.
