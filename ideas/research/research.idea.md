# /research Command

Structured, integrity-preserving investigation through multi-phase agent orchestration.

## Problem

Research tasks lack systematic structure. Evidence gathering happens ad-hoc without explicit tracking of the gap between claims and evidence.

## Key Capabilities

- **Phased approach**: Belief inventory → Evidence collection → Evaluation → Reconciliation → Synthesis
- **Gap visibility**: Explicit tracking of claims vs. supporting evidence
- **Depth modes**: Quick (3 agents, ~15 min), Standard (6 agents, ~45 min), Deep (8+ agents, multi-session)
- **Session continuation**: Resume research across multiple sessions

## Status

Functional specification complete. See `specs/research.functional.md` for the full design, and `specs/research.testing.md` for the test specification.

## Related

- `plugins/switchboard/` — Agent coordination infrastructure
- `plugins/journal/` — Session persistence for research state
- `plugins/thinkies/` — Skills invoked by research agents
