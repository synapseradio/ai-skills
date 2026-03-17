# runbook

Agent Skill for decomposing tasks, initiatives, or projects into steerable autonomous loops. Facilitates a structured alignment conversation to surface intent, then produces the artifacts (FOCUS.md, TASKS.md, LEARNINGS.md, loop prompt) that drive unattended execution.

## Install

```sh
claude install-skill github:synapseradio/ai-skills/skills/runbook
```

## References

| File | Purpose |
|------|---------|
| `references/alignment-guide.md` | Conversation protocol for Phase 1: decomposition techniques, question patterns, visualization |
| `references/checklist.md` | Structured gate validating alignment completeness before seeding |
| `references/seeding-guide.md` | Artifact templates and production instructions for FOCUS.md, TASKS.md, LEARNINGS.md |
| `references/loop-prompt.md` | Autonomous loop prompt template, customizable per runbook |

## Usage

```
Create a runbook for hardening the shell scripts in lib/
```

```
Set up an autonomous loop to implement the endpoints in docs/api-spec.md
```

## License

MIT
