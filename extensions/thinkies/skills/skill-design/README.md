# skill-design

Design a new Agent Skill, refactor an existing one, or audit one with
the user. Each mode works the same way: pose a principle as a question
about the skill at hand, gather evidence from its files, and decide
from the evidence. One question underlies all ten principles: can the
executor close every decision delegated to it, using only what the
skill provides?

Design ends at a brief for skill-creator to build from, never at a
SKILL.md. Refactor ends at a change set backed by evidence, applied
once approved. Audit changes nothing: it runs as a conversation —
align on intent, walk the principles as lenses, converge — and ends at
priorities the user confirms.

## Usage

> Design a skill that turns a captured team workflow into a reusable
> Agent Skill.

> Audit skills/my-skill against the ten principles.

> This skill over-triggers on unrelated requests. Refactor it so the
> description narrows correctly.

> Review my SKILL.md before I ship it.

## Pairs with skill-creator

Deciding what a skill should be belongs here; building, testing, and
packaging belong with skill-creator. The two overlap nowhere:
drafting, evals, trigger optimization, and packaging all sit with
skill-creator, and whoever runs skill-creator next can answer its
intake questions from the design brief alone.

## Frozen decisions

What the author fixed: the ten principles in
`references/principles.md`; three modes, each ending at its own
artifact — brief, change set, confirmed priorities; the split with
skill-creator, judgment here and mechanics there; research in design
mode running only when the user asks for it; and the test in SKILL.md's
opening that a decision closes part by part — options, facts, ranking
rule, constraints, prediction, binding act.

What stays open to each session: which principles bear on the task,
how much evidence the stakes warrant, and where audit priorities get
written down.

Revisit sign: a request that fits no mode, or the same principle
surfacing across several audits — either one means the modes or the
principles no longer match the work as it arrives.

Open decisions: the success criterion for "this skill improved"
(convergence across sessions, measured gains, or generativity);
whether audit fixtures should come from real skills or synthetic ones;
and whether the decision test in SKILL.md's opening speeds real
refactors — it came from analysis, and no run has measured it yet.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`skill-design.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/skill-design.skill)
