---
status: proposing
created: 2026-02-18
source: Ronacher "Agentic Coding" talk analysis
---

# Verification Gates: Binary Legibility in Software Skills

## Problem

Ronacher's second bedrock principle: **the agent must always be able to distinguish success from failure unambiguously at each step.** His canonical failure case: Rust's test runner returns "0 tests ran successfully" when a filter matches nothing — the agent interprets this as "all tests passed" and makes forward progress on a false foundation.

Our software plugin skills (`/plan`, `/design`, `/implement`, `/refactor`) provide *guidance* for how to write code, but they don't enforce **structural verification** at each step. The skills say "run tests" or "verify your changes" but treat verification as optional advice rather than a mandatory gate. In Ronacher's framework, this is the equivalent of not checking the return code.

The deeper issue: when an agent follows `/implement` and a test fails, the failure is visible in output. But when a test *silently doesn't run* (wrong name, wrong directory, misconfigured runner), the skill has no way to detect this. The agent proceeds with false confidence.

## Core Concept

**Verification gates** are mandatory checkpoints within skill protocols where the agent must produce an unambiguous pass/fail signal before proceeding.

A verification gate has three properties:

1. **Binary outcome** — pass or fail, no ambiguity. "0 tests ran" is a failure, not a success.
2. **Mandatory** — the skill protocol does not proceed past the gate without verification.
3. **Specified** — the gate tells the agent *exactly what to check* and *what constitutes success*.

### Gate Types

| Gate | Checks | Success Criterion | Failure Mode Prevented |
|------|--------|-------------------|----------------------|
| **Build gate** | Code compiles/transpiles | Zero errors, zero warnings treated as errors | Syntax errors propagating to later steps |
| **Test gate** | Tests pass | N tests ran, N passed, N > 0 | Zero-test false positive (Ronacher's Rust case) |
| **Lint gate** | Code meets style/safety rules | Zero violations | Style debt accumulating during generation |
| **Type gate** | Type checker passes | Zero type errors | Any-typed escape hatches |
| **Behavior gate** | Observable behavior matches expectation | Specific output or state verified | Structural correctness without behavioral correctness |

### Where Gates Belong in Software Skills

**`/implement`** — after each file modification:

```
write code → BUILD GATE → TEST GATE → proceed to next file
```

**`/refactor`** — before and after changes:

```
TEST GATE (baseline) → refactor → TEST GATE (same results) → proceed
```

**`/plan`** — environment health check (Ronacher's "pre-broken environment" problem):

```
BUILD GATE → TEST GATE → "environment is functional, safe to plan"
```

### Gate Protocol (Draft)

A gate embedded in a skill protocol would look like:

```markdown
## Verification Gate: Test

**Execute:** Run the project's test suite for the modified area.
**Check:** The output must show:
  1. At least 1 test executed (guard against zero-match)
  2. All executed tests passed
  3. No test was skipped due to error (distinguish skip-by-design from skip-by-failure)

**If pass:** Record test count and proceed.
**If fail:** Stop. Report which tests failed and why. Do not proceed to next step.
**If ambiguous:** Treat as failure. Report what made the outcome ambiguous.
```

The key innovation: **"if ambiguous, treat as failure"** — this is the direct fix for Ronacher's zero-test problem.

## Initial Thoughts

- Gates should be embedded in the skill markdown, not in a separate system. The skill prompt *is* the instruction set; gates are instructions.
- The "N > 0" check (at least one test ran) is simple but catches the most common false positive. It should be in every test gate.
- Refactor's "before and after" pattern is especially powerful — it establishes a behavioral baseline and verifies preservation.
- Gates add length to skill prompts, which consumes context (tension with P1). The gate descriptions must be terse.
- Consider: should gate results be journaled? A history of "build passed, 47 tests passed" across steps could be valuable for debugging if something goes wrong later.

## Open Questions

- [ ] How terse can gate instructions be while remaining unambiguous? Every token in a skill prompt competes for context.
- [ ] Should gates be configurable per-project? (e.g., some projects don't have linting, some use different test frameworks)
- [ ] How do gates interact with the CLAUDE.md project configuration? Should the project declare its gate commands there?
- [ ] Should gate failures produce structured output (for potential machine consumption) or plain text (for agent consumption)?
- [ ] Can we measure the impact? Before/after comparison of agent success rates with and without gates?
- [ ] How do verification gates in skills relate to switchboard flow phase transitions? Are phase gates and skill gates the same concept?
