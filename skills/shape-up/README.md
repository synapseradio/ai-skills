# Spec

Conversational software requirements elicitation producing shaped specifications. Claude drives the conversation — probing, illustrating, and using structured trade-off decisions — then produces a clean plan-mode spec artifact. Works for software customers, engineers, and PMs alike. Influenced by Shape Up (Basecamp/Ryan Singer) for appetite-first framing and pitch-style output.

## Install

```bash
claude install-skill github:nke/ai-skills/skills/spec
```

Or copy the `skills/spec/` directory into your project's `.claude/skills/` or personal `~/.claude/skills/`.

## References

| File | Purpose |
|------|---------|
| `references/elicitation-guide.md` | Phase 1 conversation protocol: opening, six elements, visualization, convergence |
| `references/audience-adaptation.md` | Detecting customer vs. engineer vs. PM; adapting language and emphasis |
| `references/shaping-techniques.md` | Eight decomposition and probing techniques for different problem types |
| `references/gate-checklist.md` | Eight gates validating elicitation completeness before spec production |
| `references/spec-production.md` | Pitch-style spec template, production instructions, scaling guidance |
| `references/domain-modeling.md` | Lightweight domain modeling: entities, relationships, invariants |

## Usage

Invoke with `/spec` or describe a software need:

```
/spec
```

```
I need to build an order tracking system for our warehouse team.
Can you help me spec this out?
```

```
Help me think through what we need for the new invoicing feature.
```

Claude will drive a conversation to surface the problem, appetite, solution elements, risks, exclusions, and boundaries — then produce a shaped specification in plan mode.
