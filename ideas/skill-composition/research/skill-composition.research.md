# Investigation: Skill/Tool Composition and Pipeline Patterns in AI Agent Systems

> A comprehensive survey of how agent frameworks compose tool calls, structure data flow through pipelines, leverage artifact-based workflows, and enable agents to create new tools from existing ones — with implications for a Claude Code plugin skill composition protocol.

---

## Area 1: Skill/Tool Chaining Protocols in Agent Frameworks

### Sources

| # | Source | Status | Used in |
|---|--------|--------|---------|
| 1 | [LangChain Expression Language (Blog)](https://blog.langchain.com/langchain-expression-language/) | valid | State of art, Examples |
| 2 | [DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines](https://arxiv.org/abs/2310.03714) | valid | State of art, Examples |
| 3 | [DSPy Signatures](https://dspy.ai/learn/programming/signatures/) | valid | State of art, Examples |
| 4 | [DSPy Custom Modules](https://dspy.ai/tutorials/custom_module/) | valid | Examples |
| 5 | [DSPy Module Composition & Refinement](https://deepwiki.com/stanfordnlp/dspy/3.5-module-composition-and-refinement) | valid | State of art, Examples |
| 6 | [AutoGen Conversation Patterns](https://microsoft.github.io/autogen/0.2/docs/tutorial/conversation-patterns/) | valid | State of art, Examples |
| 7 | [AutoGen Nested Sequential Chats](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_nested_sequential_chats/) | valid | Examples |
| 8 | [CrewAI Hierarchical Process](https://docs.crewai.com/en/learn/hierarchical-process) | valid | State of art |
| 9 | [Semantic Kernel Agent Orchestration](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/) | valid | State of art, Examples |
| 10 | [Semantic Kernel Sequential Orchestration](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/sequential) | valid | Examples |

### State of the Art

Four dominant composition models have emerged, each with distinct contracts between steps:

**1. Pipe-based composition (LangChain LCEL).** According to [LangChain's blog](https://blog.langchain.com/langchain-expression-language/), LCEL connects AI building blocks using a pipe operator (`|`) where any two `Runnable` objects compose via an overloaded `__or__` method. The output of one Runnable's `.invoke()` call becomes the input to the next. This is the closest to Unix pipe philosophy: the contract is implicit — the downstream component must accept whatever the upstream component produces. LCEL adds `RunnableParallel` for fan-out, `RunnablePassthrough` for forwarding state, and `RunnableLambda` for arbitrary transforms. The weakness: step contracts are not declared statically and rely on runtime compatibility.

**2. Signature-based composition (DSPy).** [DSPy](https://arxiv.org/abs/2310.03714) introduces the most rigorous input/output contracts in the agent framework space. A DSPy [Signature](https://dspy.ai/learn/programming/signatures/) is a declarative specification — `"question -> answer"` or a full class with typed `InputField` and `OutputField` definitions — that describes *what* a transformation does, not *how*. Field names carry semantic meaning: `question` is different from `sql_query`. [Modules compose](https://deepwiki.com/stanfordnlp/dspy/3.5-module-composition-and-refinement) in a PyTorch-inspired define-by-run pattern: declare sub-modules in `__init__`, wire them in `forward()`. The framework supports wrapping (e.g., `ChainOfThought` wraps `Predict` by prepending a `reasoning` field), coordination (`Parallel`, `BestOfN`, `Refine`), and arbitrary Python in `forward()`. Critically, DSPy's optimizer can trace execution through composed modules and automatically generate demonstrations for each `Predict` call encountered, meaning the *composition itself is optimizable*.

**3. Conversation-as-computation (AutoGen).** [AutoGen](https://microsoft.github.io/autogen/0.2/docs/tutorial/conversation-patterns/) treats multi-turn conversation as the composition primitive. It supports two-agent chat, sequential chat (chained via a carryover mechanism), group chat, and [nested chats](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_nested_sequential_chats/) where an agent uses other agents as "inner monologue." The carryover mechanism supports `"last_msg"`, `"reflection_with_llm"`, and custom callables for extraction. The `register_nested_chats()` function orchestrates a queue of sequential conversations that execute before the outer agent responds. The contract between steps is the conversation history itself — flexible but untyped.

**4. Orchestration patterns (Semantic Kernel, CrewAI).** [Semantic Kernel's Agent Orchestration](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/) provides sequential, handoff, group chat, and magentic orchestration patterns through a unified interface. The [sequential pattern](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/sequential) chains agents in a pipeline where each processes the task in turn, passing its output to the next — with optional response callbacks for intermediate observation. [CrewAI](https://docs.crewai.com/en/learn/hierarchical-process) offers sequential (predefined order, output-as-context) and hierarchical (manager-delegated) processes. Tools attach at either the agent or task level for scoped access control.

### Relevant Examples

**DSPy RAG Pipeline** — The canonical example of typed composition:

```python
class RAG(dspy.Module):
    def __init__(self, num_passages=3):
        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.generate(context=context, question=question)
```

Each sub-module declares its contract via signatures. The optimizer traces through the entire pipeline and generates few-shot demonstrations automatically.

**AutoGen Nested Sequential Chat** — Composition through conversation queues:

```python
nested_chat_queue = [
    {"recipient": manager, "summary_method": "reflection_with_llm"},
    {"recipient": writer, "message": writing_message, "summary_method": "last_msg", "max_turns": 1},
]
assistant_1.register_nested_chats(nested_chat_queue, trigger=user)
```

Each chat in the queue produces a carryover that feeds the next. Complex multi-agent workflows appear as simple request-response at the outer level.

**Semantic Kernel Sequential Pipeline** — Typed agents in series:

```python
sequential_orchestration = SequentialOrchestration(
    members=[concept_extractor, writer, editor],
    agent_response_callback=callback,
)
result = await sequential_orchestration.invoke(task="product description", runtime=runtime)
```

### Implications for Our Plugins

1. **Typed contracts are the strongest pattern.** DSPy's signatures prove that declaring input/output schemas enables both composition *and* optimization. Our skill composition protocol should require typed manifests (input fields, output fields, semantic descriptions) rather than relying on implicit text passing.

2. **Two viable composition models.** Pipe-based (LCEL) works for linear chains; module-based (DSPy) works for arbitrary DAGs. Our protocol needs the latter — skills are more complex than linear transforms.

3. **The carryover problem is real.** AutoGen solves it with explicit extraction strategies (`last_msg`, `reflection_with_llm`, custom callable). We need a similar mechanism for how one skill's output becomes another skill's input — not raw text forwarding, but structured artifact passing with optional summarization.

4. **Observation hooks matter.** Semantic Kernel's `ResponseCallback` and AutoGen's nested chat visibility let orchestrators observe intermediate steps. Our pipeline should emit structured events at each stage boundary.

---

## Area 2: Pipeline Composition Patterns

### Sources

| # | Source | Status | Used in |
|---|--------|--------|---------|
| 11 | [LangGraph](https://www.langchain.com/langgraph) | valid | State of art, Examples |
| 12 | [LangGraph GitHub](https://github.com/langchain-ai/langgraph) | valid | State of art |
| 13 | [Architectures for Building Agentic AI](https://arxiv.org/html/2512.09458v1) | valid | State of art, Examples |
| 14 | [Pydantic AI](https://ai.pydantic.dev/) | valid | State of art |
| 15 | [Anthropic: Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use) | valid | State of art, Examples |
| 16 | [Claude: Programmatic Tool Calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling) | valid | State of art |
| 17 | [Ronacher: A Language for Agents](https://lucumr.pocoo.org/2026/2/9/a-language-for-agents/) | valid | State of art |

### State of the Art

The field has converged on several pipeline architectures, ordered from lowest to highest abstraction:

**Code-as-pipeline (Anthropic Programmatic Tool Calling).** According to [Anthropic's engineering blog](https://www.anthropic.com/engineering/advanced-tool-use), programmatic tool calling allows Claude to write Python code that chains multiple tool invocations, processes their outputs, and controls what enters the context window. Instead of sequential inference passes, Claude generates code like `results = await asyncio.gather(*[get_budget(level) for level in levels])` — executing 20+ tool calls in a single code block. [Anthropic reports](https://www.anthropic.com/engineering/advanced-tool-use) 37% token reduction on complex tasks and reduced latency by eliminating per-tool inference passes. This addresses the "n+1 problem" where each tool call previously required a full model inference pass, with intermediate results accumulating in context.

**Stateful graph runtime (LangGraph).** [LangGraph](https://www.langchain.com/langgraph) represents workflows as directed graphs with typed state (via `TypedDict` or Pydantic models), transformation nodes, and control-flow edges. State updates use reducer logic — `Annotated[list, add_messages]` — enabling concurrent node updates without overwriting. The [Agentic AI architectures survey](https://arxiv.org/html/2512.09458v1) identifies LangGraph as the standard for "explicit, replayable workflows with tight governance over long-running agents."

**Typed result pipelines (Pydantic AI).** [Pydantic AI](https://ai.pydantic.dev/) enforces type-safe structured outputs through Pydantic models, bridging the probabilistic nature of LLMs with deterministic software needs. Tasks return validated Pydantic objects, and each task's output type constrains the next task's input -- the type system becomes the composition contract. ControlFlow pioneered this pattern with discrete, observable tasks returning Pydantic-typed values; Pydantic AI has since absorbed these patterns into its core framework.

**The recurring spine.** The [agentic AI architectures survey](https://arxiv.org/html/2512.09458v1) identifies a consistent 8-component pipeline across reliable systems: Goal Manager (normalizes objectives), Planner (proposes decompositions), Tool Router (maps abstractions to capabilities), Executor (sandboxed calls with pre-condition checks), Memory Layers (episodic logs + semantic stores), Verifiers/Critics (validates outputs), Safety Monitor (budgets and invariants), and Telemetry (structured logging for replay). The paper's core principle: "models propose, architectures dispose — with contracts, governors, and sandboxes that convert open-ended reasoning into reliable action."

**Language-level design for agents.** [Ronacher](https://lucumr.pocoo.org/2026/2/9/a-language-for-agents/) argues that agent-effective languages should favor explicitness over implicitness — marking functions with their dependencies (e.g., `needs { time, rng }`) rather than hiding requirements. He advocates for greppability and locality over re-exports and barrel files. While he does not propose specific agent composition patterns, his design principles inform what a composition protocol's intermediate representations should look like: locally reasoned-about, explicit in dependencies, deterministic in tooling.

### Relevant Examples

**ReWOO (Reasoning Without Observation)** — A pipeline pattern from the [agentic AI survey](https://arxiv.org/html/2512.09458v1) that decouples plan generation from execution. The model first drafts a symbolic plan with placeholders, then the system fills slots by executing tool calls. This creates auditable plan artifacts with verifiable pre/post-conditions and reduces token churn by avoiding observation-in-the-loop at every step.

**Program-Aided Language Models (PAL)** — Converts ambiguous reasoning text into executable programs run by a trusted interpreter, as described in the [survey](https://arxiv.org/html/2512.09458v1). The model generates code as a structured artifact; the system executes it deterministically. This is the intellectual ancestor of Anthropic's programmatic tool calling.

**LangGraph typed state with reducers:**

```python
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    artifacts: dict[str, Any]

graph = StateGraph(AgentState)
graph.add_node("researcher", researcher_node)
graph.add_node("writer", writer_node)
graph.add_edge("researcher", "writer")
```

### Implications for Our Plugins

1. **Structured artifacts, not conversation.** The strongest patterns pass typed objects (DSPy predictions, Pydantic models, LangGraph state) between stages, not conversational text. Our skill composition should define artifact schemas — the output of `thinkies:reason-execute` should be a structured object consumable by `software:debug`.

2. **Plan-then-execute separates concerns.** ReWOO's pattern of generating a plan with placeholders, then filling them, maps directly to how a skill composition protocol could work: the orchestrating skill declares what it needs (typed slots), and sub-skills fill them.

3. **Code-as-composition is efficient.** Anthropic's programmatic tool calling demonstrates that generating code to orchestrate tools beats sequential inference. A skill composition runtime could generate glue code between skills rather than requiring inference at every boundary.

4. **The 8-component spine is a checklist.** Every one of those components (Goal Manager through Telemetry) maps to something our plugin system either already has or needs: journal = Telemetry, switchboard = Executor/Planner, verifiers = Verification Gates (proposed), and so on.

---

## Area 3: Artifact-Based Workflows

### Sources

| # | Source | Status | Used in |
|---|--------|--------|---------|
| 18 | [Bazel: Artifact-Based Builds](https://bazel.build/basics/artifact-based-builds) | valid | State of art, Examples |
| 19 | [Dagster: Software-Defined Assets](https://dagster.io/blog/software-defined-assets) | valid | State of art, Examples |
| 20 | [Dagster Defining Assets Docs](https://docs.dagster.io/guides/build/assets/defining-assets) | redirect (valid) | State of art |
| 21 | [Apache Beam Programming Guide](https://beam.apache.org/documentation/programming-guide/) | valid | State of art, Examples |
| 22 | [Prefect Flows](https://docs.prefect.io/v3/concepts/flows) | valid | State of art |
| 23 | [GitHub Actions: Storing Workflow Data as Artifacts](https://docs.github.com/en/actions/tutorials/store-and-share-data) | redirect (valid) | State of art, Examples |
| 24 | [Nix Pills: Our First Derivation](https://nixos.org/guides/nix-pills/06-our-first-derivation) | valid | State of art, Examples |
| 25 | [Nix Derivation Reference](https://nix.dev/manual/nix/2.22/language/derivations) | valid | State of art |

### State of the Art

Artifact-based systems share a core insight: define the *what* (outputs and their dependencies), not the *how* (execution order). The system derives execution from the dependency graph.

**Bazel: Functional build composition.** According to [Bazel's documentation](https://bazel.build/basics/artifact-based-builds), the system uses "a declarative manifest describing a set of artifacts to build, their dependencies, and a limited set of options that affect how they're built." Each build rule declares inputs (`srcs`, `deps`) and outputs (`name`) explicitly. Bazel constructs a dependency graph by parsing all BUILD files, computes transitive dependencies, and parallelizes independent compilation steps. Bazel enforces hermeticity through sandboxing — each action sees only its declared inputs. The action graph is the lowest-level composable unit: each action declares inputs and outputs explicitly, runs a specific executable deterministically, and connects to other actions through those declarations. This mirrors functional programming: the programmer describes a computation, and the system optimizes when and how it executes.

**Nix: Content-addressed derivations.** [Nix derivations](https://nix.dev/manual/nix/2.22/language/derivations) are the primitive for defining packages. Each derivation specifies an executable, its precise input files, and output paths. Output paths are computed as a cryptographic hash of all build inputs — if inputs haven't changed, outputs need not be recomputed. [Nix Pills](https://nixos.org/guides/nix-pills/06-our-first-derivation) describes how after a successful build, Nix scans output paths for references to input paths by looking for hash parts, automatically tracking runtime dependencies. Dynamic derivations allow outputs of one derivation to become inputs of another at build time, enabling sophisticated composition.

**Dagster: Software-defined assets.** [Dagster's SDA model](https://dagster.io/blog/software-defined-assets) shifts orchestration from tasks to data artifacts. Each asset is defined with an `@asset` decorator, and the framework infers asset dependencies from function arguments — `processed_data(raw_data: DataFrame)` establishes that `processed_data` depends on `raw_data`. The system resolves the dependency graph and executes assets in optimal order. This approach directly answers: "Is this asset current? What computation is needed to refresh it? Which code generated this asset?" — questions that task-based orchestration cannot answer.

**Apache Beam: Typed transforms.** According to the [Beam Programming Guide](https://beam.apache.org/documentation/programming-guide/), a `PTransform<InputT, OutputT>` transforms zero or more `PCollection` objects into zero or more `PCollection` objects. Each transform has a single `InputT` and `OutputT`, creating typed contracts between pipeline stages. Beam's `MLTransform` stores artifacts (normalization parameters, vocabulary mappings) in an `artifact_location`, enabling later pipeline stages to read and apply the same transforms — a form of structured artifact passing.

**GitHub Actions: Cross-job artifact passing.** [GitHub Actions](https://docs.github.com/en/actions/tutorials/store-and-share-data) uses `upload-artifact` and `download-artifact` actions to share data between jobs, with the `needs` keyword establishing job dependencies. This enables fan-out/fan-in patterns: build in parallel, then merge artifacts for deployment.

**Prefect: Flows with implicit result passing.** According to [Prefect's documentation](https://docs.prefect.io/v3/concepts/flows), within a single process, task results stay in memory by default (`cache_result_in_memory=True`), so downstream tasks receive the original Python object without serialization. When crossing process boundaries, objects must be serializable. Prefect supports `wait_for` for dependency-only relationships (no data exchange) and nested flows that automatically resolve passed task futures into data.

### Relevant Examples

**Bazel action graph as composition model:**

```python
# BUILD file — declarative artifact definition
java_library(
    name = "mylib",
    srcs = ["MyLib.java"],
    deps = ["//other:lib"],
)

java_binary(
    name = "myapp",
    srcs = ["MyApp.java"],
    deps = [":mylib"],
)
```

Bazel constructs an action graph where `mylib` compiles first, then `myapp` consumes its output. The system parallelizes everything not in a dependency chain.

**Dagster asset composition:**

```python
@dg.asset
def raw_events() -> DataFrame:
    return load_from_source()

@dg.asset
def logins(raw_events: DataFrame, users: DataFrame) -> LoginsSchema:
    """Dependencies inferred from function signature."""
    return compute_logins(raw_events, users)
```

The dependency graph is derived from function signatures. No explicit DAG wiring needed.

**Nix derivation composition:**

```nix
{ pkgs }:
pkgs.stdenv.mkDerivation {
  name = "my-package";
  src = ./src;
  buildInputs = [ pkgs.openssl pkgs.zlib ];
  buildPhase = "make";
  installPhase = "make install PREFIX=$out";
}
```

Output path is a hash of all inputs. If `openssl` changes, the output hash changes, triggering a rebuild. If not, the cached result is reused.

### Implications for Our Plugins

1. **Asset-centric, not task-centric.** Dagster's shift from "what tasks ran" to "what artifacts exist and are they current" maps to our skill system. Skills should produce named, typed artifacts -- not just "run and print." A `thinkies:structured-reasoning` skill should produce a `ReasoningArtifact` that other skills can depend on by name.

2. **Content-addressed caching.** Nix's hash-based approach suggests that skill outputs could be cached by a hash of their inputs. If the same question is asked with the same context, the previous skill output can be reused without re-execution.

3. **Dependency inference from signatures.** Dagster infers the DAG from function arguments -- a pattern that transfers directly. If a skill declares `inputs: [ReasoningArtifact, CodeContext]`, the orchestrator can infer which skills must run first.

4. **Hermetic execution.** Bazel's sandboxing principle — each action sees only its declared inputs — translates to skills receiving only their declared context, not the entire conversation. This both reduces token waste and prevents unintended coupling between skills.

---

## Area 4: Agent Tool Composition

### Sources

| # | Source | Status | Used in |
|---|--------|--------|---------|
| 26 | [Ronacher: Tools: Code Is All You Need](https://lucumr.pocoo.org/2025/7/3/tools/) | valid | State of art, Examples |
| 27 | [Ronacher: Skills vs MCP](https://lucumr.pocoo.org/2025/12/13/skills-vs-mcp/) | valid | State of art |
| 28 | [Strands Agents Meta-Tooling](https://strandsagents.com/latest/documentation/docs/examples/python/meta_tooling/) | valid | State of art, Examples |
| 29 | [Meta-Tools and Agents (GitHub)](https://github.com/madhurprash/meta-tools-and-agents) | valid | State of art |
| 30 | [Strands Meta-Tooling Blog](https://www.duanlightfoot.com/posts/agents-that-write-their-own-tools-meta-tooling-with-strands-agents/) | valid | Examples |
| 31 | [LATM: Large Language Models as Tool Makers](https://arxiv.org/abs/2305.17126) | valid | State of art, Examples |
| 32 | [LLM-ToolMaker (GitHub)](https://github.com/ctlllll/LLM-ToolMaker) | valid | Examples |
| 33 | [Voyager: An Open-Ended Embodied Agent](https://voyager.minedojo.org/) | valid | State of art, Examples |
| 34 | [Voyager Paper](https://arxiv.org/abs/2305.16291) | valid | State of art |
| 35 | [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) | redirect (valid) | State of art |
| 36 | [Smarter Function Calling (Bernard)](https://emmanuelbernard.com/blog/2026/01/10/smarter-function-calling/) | valid | State of art |

### State of the Art

Four paradigms for agent tool composition have emerged, ranging from static to fully dynamic:

**1. Static composition via code generation (Ronacher).** [Ronacher argues](https://lucumr.pocoo.org/2025/7/3/tools/) that agents should generate executable code rather than call predefined tools. Code generation is superior for automation because it enables composability, reduces context consumption, and allows human verification of the approach rather than just outcomes. His practical recommendation: rather than adding MCP servers, "write a script or add a Makefile command and tell the agent to use that instead." In [Skills vs MCP](https://lucumr.pocoo.org/2025/12/13/skills-vs-mcp/), he defines skills as lightweight summaries that teach agents how to use existing tools better, consuming far fewer tokens than formal MCP tool definitions. His philosophy: "ask the agent to write its own tools as a skill. Not only does it not take all that long, but the biggest benefit is that the tool is largely under your control."

**2. Runtime tool factories (Strands, LATM).** [Strands Agents](https://strandsagents.com/latest/documentation/docs/examples/python/meta_tooling/) implements meta-tooling through agents that create tools at runtime. The agent is initialized with three bootstrap tools: `editor` (writes code to files), `load_tool` (registers tools with the agent's runtime registry with validation), and `shell` (debugs tool creation). When a user requests a new capability, the agent writes a Python file with a standardized `TOOL_SPEC` definition, validates it, and loads it for immediate use. [LATM (Large Language Models as Tool Makers)](https://arxiv.org/abs/2305.17126) formalizes this with a two-phase approach: a powerful model acts as the "tool maker" creating Python utility functions, and a cost-effective model acts as the "tool user" applying them. With GPT-4 as maker and GPT-3.5 as user, LATM achieves performance equivalent to GPT-4 for both roles at significantly reduced cost.

**3. Skill libraries with semantic retrieval (Voyager).** [Voyager](https://voyager.minedojo.org/) — the first LLM-powered embodied lifelong learning agent in Minecraft — maintains an ever-growing [skill library](https://arxiv.org/abs/2305.16291) of executable code, indexed by description embeddings. When facing a new task, relevant skills are retrieved by semantic similarity. Complex skills are synthesized by composing simpler programs, compounding capabilities rapidly. Voyager obtains 3.3x more unique items and unlocks milestones up to 15.3x faster than prior approaches, demonstrating that compositional tool creation outperforms monolithic tool sets.

**4. Parallel and chained function calling (OpenAI, Anthropic).** [OpenAI's function calling](https://platform.openai.com/docs/guides/function-calling) supports parallel tool calls where the model requests multiple function calls in one output, reducing API round-trips. The model can also chain tools sequentially, where the input for the second tool depends on the first's output. [Anthropic's programmatic tool calling](https://www.anthropic.com/engineering/advanced-tool-use) goes further by having the model generate code that orchestrates tool calls, including the `asyncio.gather` pattern for parallel execution — achieving 37% token reduction on complex multi-tool tasks.

### Relevant Examples

**Strands meta-tooling pipeline:**

```python
# Agent initialized with bootstrap tools
agent = Agent(
    system_prompt=TOOL_BUILDER_SYSTEM_PROMPT,
    tools=[load_tool, shell, editor]
)

# Agent autonomously:
# 1. Writes custom_tool_0.py with TOOL_SPEC
# 2. Loads it via load_tool into its registry
# 3. Uses it immediately for the task at hand
```

**LATM two-phase pattern:**

```python
# Phase 1: Tool maker (GPT-4) generates a reusable function
def solve_scheduling(tasks, constraints):
    """Tool created by tool-maker for scheduling problems."""
    # Implementation generated by GPT-4
    ...

# Phase 2: Tool user (GPT-3.5) applies the function
result = solve_scheduling(user_tasks, user_constraints)
```

The tool-making cost is amortized across many uses, making the system both cheaper and faster than using the powerful model for every instance.

**Voyager skill composition:**

```javascript
// Skill: smeltItem (composed from simpler skills)
async function smeltItem(bot, itemName, count) {
    // Retrieves and calls: findFurnace, collectFuel, mineOre
    await mineBlock(bot, oreName, count);
    await findAndUseFurnace(bot, oreName, count);
}
```

Skills are indexed by description embedding and retrieved by semantic similarity. New complex skills compose existing simpler ones.

**Ronacher's Makefile-as-tool pattern:**

```makefile
# Instead of an MCP server, teach the agent about this target
check-types:
    mypy src/ --strict

# The agent learns to call `make check-types` as a tool
# No MCP overhead, no tool definition tokens consumed
```

### Implications for Our Plugins

1. **Skills are tool factories.** The LATM and Strands patterns suggest that our skill system is already a tool factory — skills are reusable cognitive tools created once and applied many times. The protocol should formalize this: skills produce typed artifacts that can be consumed by other skills.

2. **Bootstrap tools enable self-extension.** Strands' `editor + load_tool + shell` trio is the minimal set for self-extending agents. Our system already has these (file writing, shell, skill loading via Claude Code). The composition protocol should make this explicit.

3. **Semantic retrieval over explicit wiring.** Voyager's skill library retrieval-by-embedding outperforms explicit skill chaining for open-ended tasks. Our skill composition could support both: explicit pipelines for known workflows, and semantic skill discovery for novel tasks.

4. **Amortized tool creation.** LATM's key insight — expensive creation, cheap reuse — applies to skill composition. A complex composed skill (e.g., "debug-and-fix pipeline") should be created once by a capable model, then reusable by any agent at lower cost.

---

## Open Questions

- **How should skill artifacts be serialized between steps?** JSON is universal but loses type information. Pydantic models preserve types but require shared schemas. The protocol needs to choose.
- **What happens when a composed pipeline partially fails?** Bazel rebuilds from the last successful action; Dagster refreshes stale assets. Our protocol needs a partial-execution and recovery model.
- **How do we handle skill version incompatibilities?** Nix solves this with content-addressed hashing. If a skill's output schema changes, downstream skills need either adapters or re-validation.
- **Should composition be declared or inferred?** Dagster infers DAGs from function signatures; Bazel requires explicit BUILD files. The right answer may be both — inferred for simple chains, explicit for complex workflows.
- **How does optimization work across composed skills?** DSPy can optimize across composed modules because it traces execution. Can we apply similar techniques to optimize multi-skill pipelines?

---

## Synthesis: Strongest Patterns and Protocol Implications

Across all four areas, five patterns consistently emerge as the strongest approaches to composition:

### Pattern 1: Typed Contracts at Boundaries

Every robust composition system — DSPy signatures, Bazel build rules, Beam PTransforms, Dagster asset types, Pydantic AI outputs — enforces typed contracts at step boundaries. The contract declares what goes in, what comes out, and what semantic role each field plays. Typed contracts preserve structure, reduce token waste, and enable optimization -- the opposite of free-text passing, which loses all three.

**Protocol implication:** Each skill must declare a manifest with typed input and output schemas. The manifest is the composition primitive — not the skill code itself, but its interface declaration.

### Pattern 2: Dependency-Driven Execution Order

Bazel, Dagster, Nix, and GitHub Actions all derive execution order from the dependency graph rather than requiring explicit sequencing. This enables automatic parallelization (independent steps run concurrently), minimal re-execution (only recompute what changed), and validation (cycles detected at composition time, not runtime).

**Protocol implication:** Skills declare their input types. The orchestrator builds a DAG by matching output types to input types. Execution order is computed, not specified. A `reason-execute` skill that outputs `ReasoningPlan` feeds into a `debug` skill that consumes `ReasoningPlan` — the orchestrator connects them automatically by matching types.

### Pattern 3: Plan-Then-Execute Separation

ReWOO, Anthropic's programmatic tool calling, and LATM's two-phase model all separate the planning phase (what needs to happen) from the execution phase (doing it). This reduces token churn, creates auditable artifacts, and enables cheaper execution models.

**Protocol implication:** Skill composition should support a planning phase where the orchestrating skill declares what sub-skills it needs and what artifacts they must produce — then a separate execution phase where sub-skills run with their sandboxed inputs. The plan itself is an artifact that can be inspected, approved, or modified.

### Pattern 4: Content-Addressed Caching

Nix derivations, Bazel actions, and Beam artifacts all use content-addressed storage: if the inputs haven't changed, the output is reused from cache. This is the foundation of incremental computation.

**Protocol implication:** Skill outputs should be content-addressable — hashed by their inputs and the skill version. If the same skill runs with the same inputs, the cached output is returned without re-execution. This is especially valuable for expensive skills like deep reasoning or multi-step analysis.

### Pattern 5: Self-Extending Capability

Voyager's skill library, Strands' meta-tooling, LATM's tool-making, and Ronacher's agent-written scripts all demonstrate agents creating new tools from existing ones. The strongest systems index created tools for future retrieval and support composition of new tools from existing ones.

**Protocol implication:** Composed skill pipelines should themselves be saveable as new skills. If an agent creates a useful `research-then-verify-then-write` pipeline, that pipeline becomes a first-class skill in the library, retrievable by future agents. The composition protocol is also the skill-creation protocol.

### Protocol Sketch

Drawing from these five patterns, a skill composition protocol for our plugin system would need:

1. **Skill Manifest** — Typed declarations of inputs, outputs, and semantic descriptions (DSPy signatures pattern)
2. **Dependency Resolution** — Automatic DAG construction from manifest type matching (Dagster/Bazel pattern)
3. **Artifact Bus** — Typed, content-addressed intermediate storage between skills (Nix/Beam pattern)
4. **Plan Artifacts** — Separable planning and execution phases with inspectable plans (ReWOO/LATM pattern)
5. **Pipeline Registry** — Composed pipelines saved as first-class skills with semantic retrieval (Voyager pattern)
6. **Observation Hooks** — Structured events at each boundary for logging and debugging (Semantic Kernel callback pattern)

---

## All Sources

| # | Source | Status | Used in |
|---|--------|--------|---------|
| 1 | [LangChain Expression Language (Blog)](https://blog.langchain.com/langchain-expression-language/) | valid | Area 1 |
| 2 | [DSPy Paper](https://arxiv.org/abs/2310.03714) | valid | Area 1 |
| 3 | [DSPy Signatures](https://dspy.ai/learn/programming/signatures/) | valid | Area 1 |
| 4 | [DSPy Custom Modules](https://dspy.ai/tutorials/custom_module/) | valid | Area 1 |
| 5 | [DSPy Module Composition](https://deepwiki.com/stanfordnlp/dspy/3.5-module-composition-and-refinement) | valid | Area 1 |
| 6 | [AutoGen Conversation Patterns](https://microsoft.github.io/autogen/0.2/docs/tutorial/conversation-patterns/) | valid | Area 1 |
| 7 | [AutoGen Nested Sequential Chats](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_nested_sequential_chats/) | valid | Area 1 |
| 8 | [CrewAI Hierarchical Process](https://docs.crewai.com/en/learn/hierarchical-process) | valid | Area 1 |
| 9 | [Semantic Kernel Agent Orchestration](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/) | valid | Areas 1, 2 |
| 10 | [Semantic Kernel Sequential Orchestration](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/sequential) | valid | Areas 1, 2 |
| 11 | [LangGraph](https://www.langchain.com/langgraph) | valid | Area 2 |
| 12 | [LangGraph GitHub](https://github.com/langchain-ai/langgraph) | valid | Area 2 |
| 13 | [Architectures for Building Agentic AI](https://arxiv.org/html/2512.09458v1) | valid | Area 2 |
| 14 | [Pydantic AI](https://ai.pydantic.dev/) | valid | Area 2 |
| 15 | [Anthropic: Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use) | valid | Areas 2, 4 |
| 16 | [Claude: Programmatic Tool Calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling) | valid | Areas 2, 4 |
| 17 | [Ronacher: A Language for Agents](https://lucumr.pocoo.org/2026/2/9/a-language-for-agents/) | valid | Area 2 |
| 18 | [Bazel: Artifact-Based Builds](https://bazel.build/basics/artifact-based-builds) | valid | Area 3 |
| 19 | [Dagster: Software-Defined Assets](https://dagster.io/blog/software-defined-assets) | valid | Area 3 |
| 20 | [Dagster Defining Assets Docs](https://docs.dagster.io/guides/build/assets/defining-assets) | redirect (valid) | Area 3 |
| 21 | [Apache Beam Programming Guide](https://beam.apache.org/documentation/programming-guide/) | valid | Area 3 |
| 22 | [Prefect Flows](https://docs.prefect.io/v3/concepts/flows) | valid | Area 3 |
| 23 | [GitHub Actions Artifacts](https://docs.github.com/en/actions/tutorials/store-and-share-data) | redirect (valid) | Area 3 |
| 24 | [Nix Pills: Our First Derivation](https://nixos.org/guides/nix-pills/06-our-first-derivation) | valid | Area 3 |
| 25 | [Nix Derivation Reference](https://nix.dev/manual/nix/2.22/language/derivations) | valid | Area 3 |
| 26 | [Ronacher: Tools: Code Is All You Need](https://lucumr.pocoo.org/2025/7/3/tools/) | valid | Area 4 |
| 27 | [Ronacher: Skills vs MCP](https://lucumr.pocoo.org/2025/12/13/skills-vs-mcp/) | valid | Area 4 |
| 28 | [Strands Agents Meta-Tooling](https://strandsagents.com/latest/documentation/docs/examples/python/meta_tooling/) | valid | Area 4 |
| 29 | [Meta-Tools and Agents (GitHub)](https://github.com/madhurprash/meta-tools-and-agents) | valid | Area 4 |
| 30 | [Strands Meta-Tooling Blog](https://www.duanlightfoot.com/posts/agents-that-write-their-own-tools-meta-tooling-with-strands-agents/) | valid | Area 4 |
| 31 | [LATM: LLMs as Tool Makers](https://arxiv.org/abs/2305.17126) | valid | Area 4 |
| 32 | [LLM-ToolMaker (GitHub)](https://github.com/ctlllll/LLM-ToolMaker) | valid | Area 4 |
| 33 | [Voyager](https://voyager.minedojo.org/) | valid | Area 4 |
| 34 | [Voyager Paper](https://arxiv.org/abs/2305.16291) | valid | Area 4 |
| 35 | [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) | redirect (valid) | Area 4 |
| 36 | [Smarter Function Calling (Bernard)](https://emmanuelbernard.com/blog/2026/01/10/smarter-function-calling/) | valid | Area 4 |

---
*Generated by investigate pipeline. Citations validated 2026-02-19.*
