---
status: draft
created: 2025-12-01
---

# Contemporary Prompting Frameworks Research

Research notes from systematic exploration of prompting framework patterns, conducted December 2025.

## Executive Summary

Four patterns were investigated for alignment with seed's cognitive infrastructure:

| Pattern | Finding | Recommendation |
|---------|---------|----------------|
| Conductor-Specialist | Switchboard already implements; gap is lightweight single-session variant | **New meta-skill** |
| ToT Branching | Requires journal schema extension for exploration trees | **Infrastructure change** |
| Verification | LLMs cannot self-correct; need external oracles | **New primitive (GROUND)** |
| Abstraction Laddering | Existing traverse layer skills cover this | **Documentation only** |

---

## 1. Meta-Prompting Conductor Pattern

### Core Mechanism

Meta-prompting uses a **conductor-specialist architecture** where:

- Conductor analyzes tasks, decomposes, and delegates
- Specialists execute with **Fresh Eyes** (isolated context windows)
- Conductor synthesizes outputs and detects convergence

### Key Insight: Fresh Eyes Principle

When delegating to specialists, create fresh API calls with new context windows. Specialists see only their specific instruction—not full conversation history. This prevents error propagation through contextual isolation.

### Decomposition Heuristics

Three-principle framework:

1. **Solvability**: Each sub-task independently solvable
2. **Completeness**: All necessary information addressed
3. **Non-redundancy**: No overlapping tasks

Risk: Over-decomposition creates coordination overhead that exceeds benefit.

### Specialist Selection

- **Heuristic**: Expertise matching, confidence cascading, similarity routing
- **Learned**: RouteLLM (85% cost reduction at 95% GPT-4 quality), cross-attention routing, RL-based orchestration

### Integration Mechanisms

Structured output channels:

- Work-generating (forTodos, forOrchestrator) → affect convergence
- Context-accumulating (forFutureAgents, forHuman) → don't affect convergence

Fixed point detection: work-generating channels empty = coordination complete.

### Primitive Composition

```
OBSERVE(query) → ATTUNE(complexity) → ALIGN(decomposition_options) →
DECIDE(strategy) → GENERATE(specialist_instructions) → HOLD(global_state) →
[specialists execute] →
OBSERVE(outputs) → LINK(outputs) → ALIGN(consistency) →
TRANSFORM(synthesis) → DECIDE(continue | conclude)
```

### Seed Coverage

**orchestrate-coordination** already implements:

- Grounding phase (decompose, assess-current-knowledge)
- PATCH workspaces, strands as work units
- Fresh Eyes through Task tool
- Structured narrations with consideration channels
- Fixed point detection
- Autonomous continuation

**Gap**: Lightweight meta-prompting for 3-5 specialist consultations without full PATCH infrastructure.

### Recommendation

Create meta-skill `orchestrate-decompose` for single-session decomposition:

- Trigger: 3+ distinct expertise areas, independent sub-tasks, single-turn completion
- Pattern: analyze → decompose → delegate (Fresh Eyes) → synthesize
- Sits between simple execution and full coordination

---

## 2. Tree of Thoughts Branching

### Core Mechanism

ToT maintains **exploration trees** where:

- Nodes encode intermediate reasoning states (thought content, Q-values, visit counts)
- Branches spawn through generative expansion or entropy triggers
- Pruning uses beam width, heuristics, or UCB thresholds
- Consolidation merges paths via best-path selection or weighted voting

### UCB Selection Formula

```
UCB(node_i) = w_i/n_i + c · √(ln(N)/n_i)
```

- Exploitation term: average reward
- Exploration term: inverse visit frequency
- c: tunable balance constant

### Graph of Thoughts Extension

GoT allows **merging paths** via aggregation edges:

- Multiple reasoning paths consolidate into unified solutions
- Combines strengths while eliminating individual weaknesses
- 62% improvement over ToT in sorting tasks

### Journal Schema Requirements

**ReasoningNode**:

- thought, thoughtType, qValue, visitCount, cumulativeReward
- confidence ("sure/maybe/impossible" or numeric)
- parent/child pointers, executionContext

**ReasoningTree**:

- rootNodeId, currentNodeId, searchStrategy
- beamWidth, explorationConstant
- status, bestPath

**Branch**:

- nodeIds (ordered path), cumulativeQValue
- status (active/pruned/converged)
- mergedFrom/mergedInto (for GoT)

**Consolidation**:

- contributingBranches, consolidationStrategy
- finalThought, confidence, supportingEvidence

### Operations

- `expandNode()`: Create branches with evaluation
- `calculateUCB()`: Selection scoring
- `pruneBranches()`: Remove unpromising paths
- `consolidatePaths()`: Merge into conclusions

### Primitive Mapping

HOLD with branching semantics—persistence that supports non-linear exploration.

### Recommendation

Extend journal infrastructure:

1. New entry types: reasoning-node, reasoning-tree, consolidation
2. Cross-references to session notes
3. Query by exploration depth, consolidation strategy
4. Immutable nodes (append-only, mark pruned rather than delete)

---

## 3. Verification Primitives

### Core Finding

**LLMs cannot self-correct reasoning without external feedback.**

Research is definitive:

- Self-correction often degrades performance
- Models fail on 64.5% of their own errors while correcting identical external errors
- "Improvement" in prior research was artifact of sub-optimal initial prompts

### Failure Modes

1. **Feedback generation bottleneck**: Can't evaluate own correctness
2. **Self-correction blind spot**: Training data lacks self-correction examples
3. **Error accumulation**: Mistakes compound without external check

### What Works

**External tool verification**:

- Code interpreters (real-time error messages)
- Symbolic reasoners (formal correctness)
- Search engines (factual validation)
- Formal verification systems (mathematical consistency)

**Structured multi-stage verification**:

- SelfCheck: extract → collect evidence → regenerate → compare
- Chain-of-Verification: draft → plan questions → answer independently → revise
- Graph of Verification: DAG decomposition into atomic checks

**Evidence grounding**:

- MiniCheck achieves GPT-4-level at 400x lower cost
- Works by verifying atomic facts against source documents

### When External Feedback Is Necessary

- Reasoning correctness matters
- Factual grounding required
- Formal verification possible
- Objective correctness criteria exist

### When Structured Self-Check Suffices

- Consistency checking (multi-sample voting)
- Format compliance (parsing)
- Constraint satisfaction (procedural check)
- Surface-level issues (grammar, coherence)

### Primitive Analysis

Verification doesn't map cleanly to ALIGN (phase coherence). It requires:

```
OBSERVE(claim) → ATTUNE(criteria) → LINK(to oracle) →
TRANSFORM(for oracle) → [oracle execution] → DECIDE(pass/fail) →
HOLD(outcome + evidence)
```

Missing operation: **GROUND** — verify claim against external source of truth.

GROUND differs from:

- OBSERVE (intake)
- LINK (correlation)
- ALIGN (phase coherence)

GROUND asks "does this match reality?" — fundamentally directive, requires external action.

### Recommendation

1. **Explore GROUND as 11th primitive** (or compound operation)
2. **Create verification skill** `assess-verify` or `ground-validate`:
   - Decompose claims atomically
   - Route to appropriate oracles
   - Structure verification checks
   - Maintain independence between checks
   - Make verification traceable

The skill provides **verifiability**, not correctness—it makes claims checkable by routing to appropriate mechanisms.

---

## 4. Abstraction Laddering

### Core Mechanism (Step-Back Prompting)

Two-phase technique:

1. **Abstraction**: Generate higher-level "step-back" question removing concrete details
2. **Reasoning**: Use abstract answer as context for specific question

Example:

- Original: "What happens to pressure if T×2 and V×8?"
- Step-back: "What principle governs pressure, temperature, volume?"
- Answer: Ideal Gas Law → guides correct application

Performance: +27% TimeQA, +11% Chemistry, +7% Physics, +7% MuSiQue

### Two Abstraction Types

1. **Principles-based** (STEM): Extract fundamental laws governing problem class
2. **Concept-based** (Knowledge QA): Generalize to broader categories or temporal spans

### Seed Coverage

**adjust-conceptual-zoom-level**: Bidirectional movement (climb up/down), lateral movement, working level finding. Covers the mechanism comprehensively.

**extract-principles**: Upward abstraction from examples to generalizable rules. Explicitly extracts principles before applying them.

**engage-first-principles**: Breaks down to fundamentals, rebuilds from ground truth.

### Gap Analysis

Seed already has the functionality. What's missing:

- Explicit "two-question" framing
- Reference to step-back prompting literature
- Distinction between principle-based and concept-based abstraction

### Recommendation

**Documentation enhancement only**:

1. Add step-back prompting examples to adjust-conceptual-zoom-level
2. Distinguish principle vs. concept abstraction types
3. Create reference doc at `docs/references/abstraction-techniques.md`

No new skill needed—step-back prompting is a choreography of existing operations.

---

## Synthesis

### Patterns to Codify

1. **Lightweight conductor meta-skill** — single-session decomposition without full PATCH
2. **Journal branching infrastructure** — exploration trees for ToT-style reasoning
3. **GROUND primitive or verification skill** — external oracle routing

### Documentation Only

1. **Abstraction laddering** — enhance existing skill documentation

### Open Questions

1. Should GROUND be the 11th primitive, or a compound operation?
2. How much branching complexity can journal support without becoming unwieldy?
3. What's the threshold for lightweight conductor vs. full orchestrate-coordination?

---

## Sources

### Meta-Prompting

- [Meta-Prompting: Enhancing Language Models with Task-Agnostic Scaffolding](https://arxiv.org/html/2401.12954)
- [Decomposed Prompting: A Modular Approach](https://arxiv.org/abs/2210.02406)
- [RouteLLM: Cost-Effective LLM Routing Framework](https://lmsys.org/blog/2024-07-01-routellm/)
- [Anthropic: How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)

### Tree of Thoughts

- [Tree of Thoughts: Deliberate Problem Solving](https://github.com/princeton-nlp/tree-of-thought-llm)
- [Reasoning with Language Model is Planning with World Model](https://aclanthology.org/2023.emnlp-main.507/)
- [Graph of Thoughts: Solving Elaborate Problems](https://ar5iv.labs.arxiv.org/html/2308.09687)
- [Graph-Based Prompting and Reasoning](https://cameronrwolfe.substack.com/p/graph-based-prompting-and-reasoning)

### Verification

- [When Can LLMs Actually Correct Their Own Mistakes?](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00713/125177)
- [Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798)
- [CRITIC: LLMs Can Self-Correct with Tool-Interactive Critiquing](https://openreview.net/forum?id=Sx038qxjek)
- [MiniCheck: Efficient Fact-Checking on Grounding Documents](https://arxiv.org/html/2404.10774v1)

### Abstraction

- [Take a Step Back: Evoking Reasoning via Abstraction](https://arxiv.org/abs/2310.06117)
