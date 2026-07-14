# skill-design

Design a new Agent Skill, refactor an existing one, or audit one against ten
principles. Every mode poses each principle as a question about the skill at
hand, gathers evidence from its files or from research, and runs the check
the principle names. One question cuts across all ten: can every decision
the skill hands its executor be made from what the skill provides?

Design produces a brief that a build process such as skill-creator can work
from, never a SKILL.md itself. Refactor proposes a typed change set, backed
by evidence, and applies it once approved. Audit renders a pass, fail, or
not-checkable verdict per principle and changes nothing.

## Usage

> Design a skill that turns a captured team workflow into a reusable Agent Skill.

> Audit skills/my-skill against the ten principles.

> This skill over-triggers on unrelated requests. Refactor it so the
> description narrows correctly.

> Review my SKILL.md before I ship it.

## What it declines

Packaging and eval mechanics stay with skill-creator; this skill decides
what to build and verifies fit, not how to zip or validate frontmatter.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`skill-design.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/skill-design.skill)
