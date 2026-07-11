---
status: accepted
priority: 1
created: 2026-02-19
source: Ronacher analysis + landscape research
research: research/verification-gates.research.md
synthesis: ../ronacher-synthesis.md
---

# Verification Gates: Binary Legibility in Software Skills — Proposal

## Summary

Embed mandatory pass/fail verification checkpoints within the software plugin's skill protocols so that agents always know unambiguously whether each step succeeded before proceeding. Gates are not external tooling — they are terse, imperative instructions woven into the skill markdown that transform advisory guidance ("you should run tests") into structural enforcement ("STOP. Run tests. Confirm N > 0 passed. Do not proceed until verified."). Backed by research across CI/CD systems, test framework design, agent evaluation, and silent failure detection, this proposal addresses Ronacher's Bedrock B: the agent can only make forward progress when it can unambiguously determine "did this work?"

## Background

### Problem Context

The software plugin's four skills (`/plan`, `/design`, `/implement`, `/refactor`) provide sophisticated cognitive routing through modes, decision trees, and phase transitions — but zero mandatory verification. Every mention of testing, building, or checking is advisory. The agent can proceed past any step without confirming success.

This produces three failure modes:

1. **Vacuous success** — Tests report "0 tests ran successfully." The agent interprets this as all tests passing (Ronacher's canonical Rust example). Research confirms this is widespread: pytest needed exit code 5 specifically for this case ([source](https://github.com/pytest-dev/pytest/issues/812)), cargo-nextest changed its default to fail on zero tests ([source](https://nexte.st/docs/running/)), and formal verification has studied vacuous proofs for decades ([source](https://blogs.sw.siemens.com/verificationhorizons/2017/12/06/formal-tech-tip-what-are-vacuous-proofs-why-they-are-bad-and-how-to-fix-them/)).

2. **Silent non-action** — The agent reasons about code but skips the tool call that constitutes actual verification. Ronacher addresses this with forced acknowledgment: "When a tool loop completes without the agent calling the expected output tool, the system injects reinforcement messages" ([source](https://lucumr.pocoo.org/2025/11/21/agents-are-hard/)). Our skills have no equivalent — an agent can "complete" `/implement` without ever running a test.

3. **Pre-broken environment** — The agent begins implementation on a codebase where tests already fail or the build is broken. Every subsequent failure is ambiguous: "did my change cause this, or was it already broken?" Without a baseline gate, the agent lacks the reference point needed for binary legibility.

### Current State

| Skill | Verification Guidance | Enforcement |
|-------|----------------------|-------------|
| `/plan` | None (no environment health check) | None |
| `/design` | None (type checking not mentioned) | None |
| `/implement` | Error-Clarification mode discusses error quality | Advisory only |
| `/refactor` | "Improve code without changing behavior" (implied preservation) | No behavioral verification |

### Why Now

The research base is clear. Every major CI/CD system enforces mandatory gates. Every mature test framework now treats zero-tests-ran as failure by default. Agent evaluation frameworks (Anthropic's own [eval guide](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)) require compound verification (positive + negative conditions). The MCP specification defines `isError` for binary tool outcomes. The pattern is settled — we are behind the state of the art by not embedding it in our skills.

## Proposal

### What

Add **verification gate protocols** to each software skill as terse, mandatory sections in the skill markdown. A gate is an instruction block within the skill prompt that the agent must execute at specified points. Gates produce non-vacuous, binary signals that cannot be satisfied by doing nothing.

### The Gate Protocol

A gate embedded in a skill reference file follows this structure:

```markdown
## ⊘ GATE: [Name]

**Run:** [exact command or action]
**Pass:** [what success looks like — must include non-vacuity check]
**Fail:** STOP. Report what failed and why. Do not proceed.
**Ambiguous:** Treat as FAIL. Report what made the outcome unclear.
```

The `⊘` symbol marks gates visually in skill prompts, making them scannable. The protocol is ~4 lines per gate, ~60 tokens — minimal context cost.

**The critical rule: "Ambiguous = FAIL."** This is the direct fix for vacuous success. An outcome the agent cannot clearly classify as pass gets the same treatment as explicit failure: stop and report.

### Gate Types

| Gate | Checks | Non-Vacuity Criterion | Context Cost |
|------|--------|-----------------------|--------------|
| **Environment** | Build + tests pass on current code | At least 1 test ran | ~80 tokens |
| **Build** | Code compiles/transpiles | Zero errors | ~50 tokens |
| **Type** | Type checker passes | Zero type errors | ~50 tokens |
| **Test** | Tests pass for modified area | N tests ran, N > 0, all passed | ~70 tokens |
| **Preservation** | Before/after test parity | Same test count, same results | ~80 tokens |
| **Lint** | Style/safety rules pass | Zero violations | ~50 tokens |

### Gate Placement per Skill

**`/plan` — Environment Gate (Phase 0)**

Before any planning begins, verify the environment is functional:

```
Environment Gate → [all plan modes proceed normally]
```

This catches the pre-broken environment problem. If the build fails or tests fail before the agent touches anything, the agent knows immediately and can report it rather than building plans on a broken foundation.

*Added to: plan/SKILL.md as a new "Phase 0: Environment Verification" section before the Decision Tree.*

**`/design` — Type Gate (after type drafting)**

After the Type-Generative → Type-Analytical cycle:

```
Type-Generative → Type-Analytical → TYPE GATE → proceed or revise
```

*Added to: design/references/mode-type-analytical.md as a gate step at the end of the analytical phase.*

**`/implement` — Build + Test Gate (after each commit-ready unit)**

After staged changes are ready to commit:

```
[write code] → BUILD GATE → TEST GATE → [commit via Investment-Timing]
```

The test gate includes the N > 0 check. The build gate catches syntax/compilation errors before test execution wastes time.

*Added to: implement/SKILL.md as a new "Verification Protocol" section between the Decision Tree and Signal Detection. Also added to implement/references/mode-investment-timing.md as a pre-commit checkpoint.*

**`/refactor` — Preservation Gate (before and after)**

The refactor skill's core promise is "improve without changing behavior." The preservation gate enforces this structurally:

```
TEST GATE (baseline: record count N) → [refactor] → TEST GATE (verify: count >= N, all pass)
```

If the post-refactor test count drops, the agent knows it accidentally removed or broke tests. If the count stays the same but results differ, the refactoring changed behavior.

*Added to: refactor/SKILL.md as a new "Behavioral Preservation Protocol" section. Also added to refactor/references/mode-structural.md and mode-vestigial.md as pre/post gates.*

### How Gates are Configured

Gates need to know project-specific commands. Configuration follows a three-tier fallback:

**Tier 1: CLAUDE.md declaration (preferred)**

```markdown
## Verification Commands

| Gate | Command |
|------|---------|
| build | `bun run build` |
| test | `bun test` |
| lint | `bun run lint:fix` |
| type | `bun run types:check` |
```

**Tier 2: Inference from project files**

If CLAUDE.md doesn't declare gate commands, the agent infers from `package.json` scripts, `Cargo.toml` configuration, `Makefile` targets, `pyproject.toml`, etc. This is existing agent behavior — gates just make it mandatory rather than optional.

**Tier 3: Skip with warning**

If no command can be determined, the gate is skipped and the agent emits a warning: "⊘ GATE SKIPPED: No test command found. Consider adding verification commands to CLAUDE.md." The warning itself is valuable — it surfaces the gap.

### Why This Approach

1. **Gates are instructions, not infrastructure.** They live in skill markdown, not in a separate CLI tool or runtime system. This follows the idea doc's principle: "the skill prompt IS the instruction set; gates are instructions." Zero new build targets, zero new dependencies.

2. **Minimal context cost.** Each gate is ~50-80 tokens. A skill with 2 gates adds ~130 tokens. The software plugin's skills range from 2000-5000 tokens — gates are a 3-6% increase in exchange for structural correctness assurance.

3. **Progressive enforcement.** Gates use a 3-tier configuration with graceful degradation. Projects without test suites get skip-with-warning, not hard failures. This avoids the xUnit #3077 problem where zero-tests-matching-filter caused false negatives.

4. **Compatible with existing flow.** Gates slot into existing phase transitions without restructuring the cognitive mode architecture. The implement skill's Investment-Timing → Selective-Stage flow gains a verification checkpoint between them, not a replacement.

## Integration Points

### Switchboard: Verification Phase Gates

Switchboard's flow schema defines a `gate` field on phases, currently supporting only `approval` (human checkpoint). Extend the gate field to support automated verification:

```yaml
phases:
  implement:
    goal: "Implement the authentication module"
    topology: "@developer"
    gate: verification    # NEW: automated pass/fail gate
```

Gate type semantics:

| Gate Value | Behavior |
|------------|----------|
| `approval` | Existing: pause for human review |
| `verification` | New: run project verification commands (build, test, lint) |
| `compound` | New: run verification, then request approval |

When a `verification` gate runs, the switchboard executor:

1. Runs the gate commands declared in CLAUDE.md (same configuration the software skills use)
2. Checks all pass (binary: all pass = proceed, any fail = block)
3. On failure: reports results and offers retry or abort
4. On success: proceeds to next phase with gate result in accumulated context

This unifies skill-level gates (within a single agent's work) with orchestration-level gates (between phases of a multi-agent flow). Same principle, two scopes.

### Journal: Gate Result Logging

Journal gains a new content type: `gate`. This records verification outcomes as structured, queryable data.

```bash
journal write gate --session <name> --data '{
  "skill": "implement",
  "gate_type": "test",
  "result": "pass",
  "metrics": {
    "tests_run": 47,
    "tests_passed": 47,
    "tests_failed": 0,
    "duration_ms": 3200
  },
  "context": "after modifying auth-handler.ts"
}'
```

Required fields for the `gate` content type:

| Field | Type | Description |
|-------|------|-------------|
| `skill` | string | Which skill invoked the gate |
| `gate_type` | string | Gate type: build, test, lint, type, preservation |
| `result` | enum | `pass`, `fail`, `skip` |
| `metrics` | object | Gate-specific metrics (test counts, error counts, duration) |
| `context` | string | What step triggered this gate |

**Query use cases:**

- "When did tests start failing?" → `journal read session search --type gate --filter 'result=fail'`
- "What was the test count before the refactor?" → Preservation gate baseline entry
- "How long do builds take across sessions?" → Aggregate `metrics.duration_ms` across gate entries
- "Which skills trigger the most gate failures?" → Group by `skill` + `result`

This is a structural addition to the journal plugin — a new content type with its own schema, validation, and query surface. Per the directive that we're open to big changes in journal, this is the most impactful integration: it transforms ephemeral gate checks into persistent, analyzable data.

### Thinkies: Cognitive Verification (Existing Alignment)

The thinkies plugin already has cognitive verification skills: `/check-soundness`, `/audit-chain-of-thought`, `/integrity`. These are verification gates for *reasoning* rather than *code*. No changes needed — but the framing connection is worth making explicit. Verification gates in software + cognitive verification in thinkies = binary legibility at every layer.

## Alternatives Considered

### Alternative 1: External Gate Runner CLI

Build a TypeScript CLI (`gate-runner`) that executes verification commands and returns structured JSON with pass/fail/metrics.

**Why not chosen:** Adds build complexity (new CLI target, new dependency chain). The skill prompt already instructs the agent to run commands and interpret output — a CLI wrapper duplicates what the agent does natively. Furthermore, the power of gates-as-instructions is that they travel with the skill, not alongside it. An external tool can be forgotten; an instruction in the prompt cannot.

### Alternative 2: Gates as a Separate Skill (`/verify`)

Create a standalone verification skill that agents invoke between other skills.

**Why not chosen:** This preserves the "verification as optional advice" anti-pattern. The entire point of gates is that they are mandatory and embedded — the agent cannot proceed without them because the skill prompt itself blocks progress. A separate `/verify` skill requires the agent to choose to invoke it, which is the same voluntary verification we have today.

### Alternative 3: Gates Only in Switchboard

Handle all verification at the orchestration layer. Software skills remain advisory; switchboard flows enforce verification between phases.

**Why not chosen:** Most agent work happens within a single skill invocation, not through switchboard flows. An agent running `/implement` directly (not within a switchboard flow) would have zero verification. Gates must work at the skill level for maximum coverage. Switchboard integration is additive — it extends the same principle to multi-agent orchestration.

### Alternative 4: Runtime Enforcement via Hooks

Use journal hooks or git hooks to prevent the agent from proceeding without verification.

**Why not chosen:** Hooks are project-specific configuration, not skill-level architecture. They can be bypassed (`--no-verify`). They operate outside the agent's reasoning context — the agent doesn't know *why* it was stopped, only that something blocked it. Gates-as-instructions let the agent understand verification as part of its workflow, not an external constraint.

## Risks and Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Context bloat** — Gate tokens consume context budget | Low | ~130 tokens per skill (2 gates). Gate protocol is terse by design. Loaded via reference files, not inlined in every mode. |
| **False negatives** — Gates fail on correct code (flaky tests, environment issues) | Medium | "Ambiguous = FAIL" combined with clear reporting. The agent investigates the failure rather than silently proceeding. Flaky tests are a project problem gates make visible, not a gate design problem. |
| **Over-rigidity for simple projects** — Small scripts without test suites hit unnecessary warnings | Low | Three-tier configuration with skip-on-missing. The warning itself adds value by surfacing the verification gap. |
| **Agent non-compliance** — Agent ignores gate instructions despite imperative language | Medium | Gate results journaled for accountability. Switchboard verification gates provide an additional enforcement layer for orchestrated work. Long-term: skill compliance metrics via journal analysis. |
| **Performance cost** — Running builds/tests at every gate slows agent work | Medium | Gates run at meaningful checkpoints (per-commit, not per-file-save). Incremental test runners and fast builds mitigate. The cost of proceeding on a false foundation vastly exceeds the cost of a verification pause. |
| **Preservation gate fragility** — Test count comparison is brittle if tests are added during refactor | Low | Preservation gate checks count >= baseline, not count == baseline. Adding tests during refactoring is acceptable; losing tests is not. |

## Open Questions

### Resolved by Research

| Original Question | Resolution |
|-------------------|------------|
| Should gate failures produce structured or plain text output? | Plain text with clear formatting. Gates are agent prompt instructions, not tool calls. The MCP `isError` pattern applies to tools; skill gates apply to reasoning flow. |
| How do gates relate to switchboard phase transitions? | They are the same concept at different scopes. Skill gates = within-agent verification. Switchboard gates = between-phase verification. Same protocol, unified configuration. |

### Remaining

1. **Gate granularity in implement:** Should gates fire after each file modification, or after each commit-ready unit? Research on progressive delivery suggests meaningful checkpoints. Current proposal: per-commit-unit (aligned with Investment-Timing mode).

2. **Incremental vs. full verification:** Should the test gate run only tests related to modified files, or the full suite? Per-file is faster but risks missing integration failures. Full suite is slower but comprehensive. Proposal: let CLAUDE.md declare both (`test_focused` and `test_full`), default to full.

3. **Gate result format standardization:** The journal `gate` content type needs a schema. Should `metrics` be free-form or gate-type-specific? Proposal: gate-type-specific schemas (test gate has `tests_run`, `tests_passed`; build gate has `errors`, `warnings`) with a common envelope.

4. **Measuring impact:** Can we compare agent success rates in sessions with gates vs. without? The journal trail enables this, but designing the experiment (what counts as "success"?) is an open question. Anthropic's pass@k vs. pass^k distinction ([source](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)) suggests measuring both "did it ever work?" and "does it work reliably?"

5. **Drift detection for agent behavior:** Research on behavioral fingerprinting (Uber's Clio) suggests tracking gate patterns over time. If an agent's gate-failure rate increases, the underlying project may be degrading. Is this within scope or a future extension?

## Implementation Sketch

### Phase 1: Core Gate Protocol (software plugin)

1. Add `references/verification-protocol.md` to the software skill directory — shared gate protocol definitions
2. Add Environment Gate to `/plan` SKILL.md (Phase 0 section)
3. Add Build + Test Gate to `/implement` SKILL.md and `mode-investment-timing.md`
4. Add Preservation Gate to `/refactor` SKILL.md and `mode-structural.md`
5. Add Type Gate to `/design` `mode-type-analytical.md`
6. Update idea doc status to `proposing`

### Phase 2: Journal Integration

1. Add `gate` content type to journal (schema, validation, write command)
2. Add gate-specific query support (`--type gate`, `--filter result=fail`)
3. Instrument software skill gates to write journal entries on execution

### Phase 3: Switchboard Integration

1. Extend flow schema to support `gate: verification` and `gate: compound`
2. Add verification gate execution logic to switchboard executor
3. Update built-in flow templates (especially `debug` and `feature`) to use verification gates

## Request

Seeking feedback on:

1. **Gate placement granularity** — Is per-commit-unit the right checkpoint frequency for `/implement`, or should it be more/less frequent?
2. **Journal `gate` content type** — Is a new content type the right approach, or should gate results be a convention within existing `note` entries?
3. **Switchboard gate types** — Are `verification` and `compound` the right extensions, or should the schema be more flexible?
4. **Context cost tolerance** — Is ~130 tokens per skill acceptable for the structural correctness guarantee?

## Synthesis Outcome

**Priority:** #1 of 3. Ships first in Phase 1a, immediately after journal simplification (Phase 0).

**Why first:** Three convergent reasons from the debate:

1. Lowest effort — gates are markdown instructions, not infrastructure
2. Highest immediate impact — directly addresses Ronacher's Bedrock B (binary legibility)
3. Structural prerequisite — both checkpoints and composition require verification to be trustworthy

**Key premortem findings that shaped the recommendation:**

1. **Gates are "advisory with strong language" — and that's OK.** The Checkpoints-Critic correctly noted that prompt instructions are not physical enforcement. But this is true of the entire skill system. Skills ARE prompt instructions. The goal is to change the default from "verification is optional" to "verification is expected."

2. **Output cost is not gate cost.** The argument that gate output is 5-15x the instruction cost (~400-2000 tokens for test results) is misleading — test output would be consumed regardless. The gate *instruction* (~60-80 tokens) is the marginal cost. The test output is a cost of verification, not a cost of gates.

3. **Flaky tests are a project problem, not a gate problem.** Gates make flaky tests visible rather than creating them. The "context furnace" concern (2-8% flake rates × per-commit-unit gates) is real but is the project's responsibility to fix.

4. **Gate results are structured notes, not a new ContentKind.** The premortem panel was unanimous: gate results are point-in-time events within sessions. A note with `_gate: true` and structured metrics provides 95% of the query value without a 10th ContentKind.

5. **Environment Gate's upfront cost is justified.** ~90s wait + ~500 tokens is the cost of establishing a baseline. Building plans on a broken foundation cascades confusion through the entire session — the context savings downstream exceed the upfront investment.

**Design changes from debate:**

- Gate journaling (Phase 3) separated from core gate protocol (Phase 1a) — gates ship as pure markdown first
- Journal `gate` content type replaced by structured note convention
- Switchboard integration deferred to Phase 3+
- "Ambiguous = FAIL" elevated as the single most important rule
- Schema philosophy resolved for gate results: strict core (`skill`, `gate_type`, `result` — fail if missing) + flexible extension (`metrics`, `context`, additional diagnostic fields accepted)
