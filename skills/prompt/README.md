# prompt

Craft or refactor LLM instructions grounded in Anthropic's functional-emotions
research. Takes no required arguments — the skill detects whether the input
is a seed task, an existing `CLAUDE.md` to refactor, or an empty canvas,
and emits structured output that applies the seven Emotional Intelligence
Prompting (EIP) principles while preserving every instruction in the input.

## What it does

Three modes, one pipeline:

- **Seed:** rough task description → 7-section structured prompt
- **Refactor:** existing CLAUDE.md / system prompt → refactored file +
  coverage report guaranteeing no dropped instructions
- **First-draft:** empty canvas → first-draft CLAUDE.md sized to the
  project

Every output passes a 9-item anti-pattern lint derived from the
[emotion-concepts paper](https://transformer-circuits.pub/2026/emotions/index.html):
no threat framing, no demanded certainty, no authoritarian stacks, no
forced enthusiasm, no perfect-prompt fallacy.

## Design

Structure comes from `perspectives:prompt-assemble`'s seven buckets
(reshaped: Frame, Task, Context, Tooling, Perspective, Constraints &
Invitations, Why). EIP is the predicate that structure must satisfy.
When they conflict, the skill reshapes the phrasing inside a bucket —
never drops the principle.

In refactor mode, instructions are extracted as stable IDs, slotted
into buckets, rephrased with truth-condition preservation, then
diffed against the output to catch silent omissions. A coverage
report is emitted when the input contains 10+ instructions.

## Triggers

The skill auto-invokes when the user asks to "write a prompt", "assemble
a prompt", "refactor my CLAUDE.md", "update CLAUDE.md", "fix my system
prompt", "draft a CLAUDE.md", "turn this task into a prompt", "polish
this prompt", or when the user pastes an existing prompt-shaped document
and asks for improvement.

## References

- [Emotion Concepts and their Function in a Large Language Model](https://transformer-circuits.pub/2026/emotions/index.html) (Anthropic, April 2026) — the research
- [OuterSpacee/claude-emotion-prompting](https://github.com/OuterSpacee/claude-emotion-prompting) — synthesis this skill builds on
- `perspectives:prompt-assemble` — the source of the 7-bucket structure

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`prompt.skill`](https://github.com/synapseradio/ai-skills/raw/main/skills/packaged/prompt.skill)
