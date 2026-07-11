# Software Plugin: Four-Skill Architecture

## Problem Statement

The current software plugin organizes 28 cognitive operations into 6 umbrella skills (understand, assess, decide, clarify, type, git). Users must:

1. Know which of 6 skills might contain relevant operations
2. Parse signal detection tables to find the right mode
3. Navigate cross-skill combinations for multi-phase work

This "router to subcommands" pattern optimizes for comprehensive coverage but creates discovery friction. Users can't easily match their current need to an entry point.

## Proposed Solution

Reorganize around 4 skills aligned with the software development lifecycle:

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| **plan** | Constraint discovery, trade-off analysis, decision-making | Before writing code |
| **design** | Type design, interface contracts, architectural decisions | Shaping the solution |
| **implement** | Flow understanding, dependency mapping, code execution | During development |
| **refactor** | Complexity reduction, structural clarity, history organization | Improving existing code |

## First Principles

### Discovery by Intent

Users think in terms of what they're trying to accomplish:

- "I need to plan this feature" → `/plan`
- "I need to design the types" → `/design`
- "I'm implementing this" → `/implement`
- "This code needs cleanup" → `/refactor`

### Preserve Cognitive Depth

The 28 existing modes represent valuable cognitive operations. Reorganization should:

- Retain all modes (possibly renamed/consolidated)
- Maintain reference quality and examples
- Preserve combination patterns within new skill boundaries

### Progressive Disclosure

Each skill should:

- Provide immediate value with sensible defaults
- Reveal depth through mode selection when needed
- Cross-reference other skills for phase transitions

## Mode Redistribution (Draft)

### plan (Pre-implementation thinking)

From **decide**:

- constraint-inventory → plan:constraints
- trade-space → plan:trade-offs
- good-enough-threshold → plan:sufficiency

From **assess**:

- failure-modes → plan:failure-analysis
- assumptions → plan:assumptions

### design (Solution shaping)

From **type**:

- generative → design:types
- analytical → design:type-analysis

From **decide**:

- abstraction-level → design:abstraction

From **assess**:

- interface-stability → design:interfaces

### implement (Development execution)

From **understand**:

- cartography → implement:orient
- flow → implement:trace
- dependency → implement:dependencies

From **clarify**:

- error-clarification → implement:errors

From **git**:

- selective-stage → implement:stage
- commit-strategy → implement:commit

### refactor (Code improvement)

From **decide**:

- surface-complexity → refactor:complexity

From **clarify**:

- structural → refactor:structure
- annotation → refactor:annotate
- archaeology (both) → refactor:archaeology
- documentation-audit → refactor:docs

From **assess**:

- blast-radius → refactor:impact
- second-order-effects → refactor:consequences

From **git**:

- rebase-safety → refactor:rebase
- migration-path → refactor:migration
- conflict-topology → refactor:conflicts
- investment-timing → refactor:timing

From **understand**:

- type-intention → refactor:type-recovery

## Open Questions

1. **Git as independent skill?** Should git operations stay separate or fold into implement/refactor?

2. **Archaeology consolidation**: Both understand and clarify have archaeology modes. Merge into one location?

3. **Vestigial detection**: Where does `vestigial-detect` fit? Likely refactor, but it's currently a standalone command.

4. **Cross-skill flows**: How do combination patterns work when modes move between skills?

5. **Migration path**: How do we maintain backward compatibility during transition?

## Decision: Migration Strategy

**Resolved:** Immediate removal of old skills (no deprecation period).

Rationale: Clean break avoids maintenance burden of parallel structures. This is a major version bump (v3.0.0) that communicates breaking changes clearly.

## Success Criteria

- [ ] All 28 modes have clear homes in 4-skill structure
- [ ] Discovery improves: users can find operations by intent
- [ ] No cognitive operations lost
- [ ] Reference quality maintained
- [ ] Clean removal of old structure (no deprecated code paths)

## Implementation Plan

See `/Users/nke/.claude/plans/cryptic-wondering-biscuit.md` for detailed task breakdown.
