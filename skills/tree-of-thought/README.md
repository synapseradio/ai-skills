# tree-of-thought

Systematic Tree of Thought reasoning for complex problem decomposition. Generates and evaluates multiple solution paths before selecting the best approach.

## Install

```sh
claude install-skill github:synapseradio/ai-skills/skills/tree-of-thought
```

## How it works

Four phases:

1. **Decomposition** — breaks the problem into 2-5 components with dependency mapping
2. **Generation** — creates three approaches per component (direct, creative, systematic) with viability scores
3. **Evaluation** — scores each approach on feasibility (40%), effectiveness (35%), and risk (25%)
4. **Synthesis** — integrates the best approaches into a coherent solution with next steps and success metrics

## Usage

```
/tree-of-thought How should we architect the caching layer for our API?
/tree-of-thought Evaluate approaches for migrating from monolith to microservices
```

## License

MIT
