# team

Expert persona collaboration for structured problem analysis. Assembles a team of 3-8 expert personas who collaboratively analyze a problem through phased conversation.

## Install

```sh
claude install-skill github:synapseradio/ai-skills/skills/team
```

## How it works

1. **Situation Analysis** — analyzes scenario type, risk level, and constraints
2. **Team Selection** — picks 3-8 personas matching the problem profile
3. **User Approval** — presents the team for confirmation
4. **Discussion** — structured rounds with analysis, impact assessment, assumption challenges, and risk mitigation
5. **Synthesis** — actionable items with file paths, line numbers, and validation methods
6. **Implementation** — only on explicit user request

Phases 0-4 are read-only. Each persona contributes in character with visible reasoning. All technical claims are cited via web search.

## Contents

| File | Purpose |
|------|---------|
| `references/team-config.yaml` | Phase rules, persona mapping, reasoning settings |

Requires persona files in `~/.claude/personas/*.md`.

## Usage

```
/team Analyze the security implications of our new auth flow
/team Review the migration plan for the database schema changes
```

## License

MIT
