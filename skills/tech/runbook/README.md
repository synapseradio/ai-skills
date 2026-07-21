# runbook

Set up steerable autonomous loops through structured alignment conversations. Instead of writing long prompts and hoping the agent does the right thing unattended, this skill walks you through a conversation that surfaces your actual intent, then produces the artifacts that drive the loop.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/runbook/` into `~/.claude/skills/runbook/`.

## Usage

```
/runbook set up a hardening pass for the shell scripts in lib/
/runbook create an autonomous loop to implement the endpoints in docs/api-spec.md
/runbook execute mode against ~/projects/my-service
/runbook continue the runbook in this directory
```

## How it works

Two modes.

**Seed mode** is an alignment conversation that surfaces seven elements: the work, the motivation, what the loop looks for (the lens), what reference it consults (the authority), what's in and out of scope, what success looks like, and whether to use a tight loop or recursive decomposition. This is a dialogue, not a form — the skill explores, reflects, and lets you correct before moving on. Seeding produces three artifacts plus a route choice: attended, where the session runs rounds continuously and steers at a per-round summary, or unattended, where a scheduled stub runs one round per invocation.

| Artifact | Purpose |
|----------|---------|
| `FOCUS.md` | Lens, authority, scope, success criteria |
| `TASKS.md` | Task board skeleton (Open / In Progress / Done) |
| `LEARNINGS.md` | Append-only memory for the loop to write and you to read |

**Execute mode** is the loop itself. Invoking the skill against a directory containing `FOCUS.md` turns that session into the orchestrator: it reads the three artifacts, delegates all implementation to subagents, and keeps durable state in those same files across rounds. On convergence, the loop writes a `Status: converged` marker into `TASKS.md`, and later runs no-op. The loop is the skill's own execute mode, not a prompt generated once and deployed separately — the session that seeded the work runs it too.

The loop used to end by emitting a customized prompt template, deployed separately via cron. That artifact is gone; the loop lives in execute mode instead, so the discipline exists in one place. If the execute-mode protocol and some downstream copy of it ever diverge again, that divergence is the sign this decision needs revisiting.

## When to use this

Use it when you want an agent to work autonomously over a sustained period — implementing a feature from a spec, hardening a codebase against a checklist, migrating patterns across files. The alignment conversation is the investment; the loop is the payoff.

Not useful for one-off tasks you can describe in a single prompt.

## References

| File | Purpose |
|------|---------|
| [`references/alignment-guide.md`](references/alignment-guide.md) | Conversation protocol: decomposition, question patterns, visualization |
| [`references/checklist.md`](references/checklist.md) | Gates validating alignment completeness before seeding |
| [`references/seeding-guide.md`](references/seeding-guide.md) | Artifact templates and production instructions |
| [`references/execution-guide.md`](references/execution-guide.md) | Execute-mode protocol: round lifecycle, delegation briefs, placement framework, convergence |

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`runbook.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/tech/runbook.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
