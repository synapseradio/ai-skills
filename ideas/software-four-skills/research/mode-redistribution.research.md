# Mode Redistribution Research

## Design Summary

Refactor from 6 skills (28 modes) to 4 skills (28 modes):

| New Skill | Mode Count | Source Skills |
|-----------|------------|---------------|
| plan | 12 | understand (4), assess (5), decide (2), git (1) |
| design | 6 | type (2), understand (1), decide (3) |
| implement | 4 | git (3), clarify (1) |
| refactor | 6 | clarify (3), git (2), +vestigial (new) |

## Complete Mode Mapping

| Old Skill | Old Mode | New Skill | New Mode |
|-----------|----------|-----------|----------|
| understand | cartography | plan | cartography |
| understand | dependency | plan | dependency |
| understand | flow | plan | flow |
| understand | archaeology | plan | archaeology (merged) |
| understand | type-intention | design | type-intention |
| assess | failure-modes | plan | failure-modes |
| assess | second-order-effects | plan | second-order-effects |
| assess | interface-stability | plan | interface-stability |
| assess | blast-radius | plan | blast-radius |
| assess | assumptions | plan | assumptions |
| decide | abstraction-level | design | abstraction-level |
| decide | constraint-inventory | plan | constraint-inventory |
| decide | trade-space | plan | trade-space |
| decide | good-enough-threshold | design | good-enough-threshold |
| decide | surface-complexity | design | surface-complexity |
| clarify | structural | refactor | structural |
| clarify | annotation | refactor | annotation |
| clarify | archaeology | plan | archaeology (merged) |
| clarify | documentation-audit | refactor | documentation-audit |
| clarify | error-clarification | implement | error-clarification |
| type | generative | design | type-generative |
| type | analytical | design | type-analytical |
| git | commit-strategy | implement | commit-strategy |
| git | selective-stage | implement | selective-stage |
| git | rebase-safety | refactor | rebase-safety |
| git | migration-path | plan | migration-path |
| git | conflict-topology | refactor | conflict-topology |
| git | investment-timing | implement | investment-timing |
| (command) | vestigial-detect | refactor | vestigial |

## Key Design Decisions

### Archaeology Merge

- `understand/archaeology` (investigate why code exists)
- `clarify/archaeology` (document what was found)
- **Merged into** `plan/archaeology` with two phases: investigation → documentation

### Git Distribution

Git modes split by temporal context:

- **Pre-implementation** → plan: migration-path
- **During implementation** → implement: commit-strategy, selective-stage, investment-timing
- **Post-implementation** → refactor: rebase-safety, conflict-topology

### vestigial-detect Promotion

Current standalone command becomes `refactor/vestigial` mode for consistency.

## Signal Detection (New Skills)

### plan signals

- "unfamiliar", "new to", "onboarding" → cartography
- "depends on", "coupled", "impact" → dependency
- "what happens when", "runtime", "trace" → flow
- "why does this exist", "history", "git blame" → archaeology
- "could fail", "edge cases", "break" → failure-modes
- "consequences", "ripple", "cascade" → second-order-effects
- "stable", "dependency risk" → interface-stability
- "affected", "blast radius", "scope" → blast-radius
- "verify", "prove", "actually" → assumptions
- "constraints", "boundaries" → constraint-inventory
- "trade-off", "costs", "compare" → trade-space
- "breaking change", "migrate" → migration-path

### design signals

- "design type", "signature", "encode" → type-generative
- "what does this type allow", "guarantee" → type-analytical
- "why is this type complex" → type-intention
- "extract", "duplicate", "DRY" → abstraction-level
- "complex", "simplify", "essential" → surface-complexity
- "good enough", "done", "ship" → good-enough-threshold

### implement signals

- "organize commits", "split commits" → commit-strategy
- "stage specific lines", "hunks" → selective-stage
- "fix properly now or later" → investment-timing
- "error message", "PAGE" → error-clarification

### refactor signals

- "rename", "readable", "simplify" → structural
- "comments", "document why" → annotation
- "verify README", "audit docs" → documentation-audit
- "rebase", "rewrite history" → rebase-safety
- "conflict", "merge" → conflict-topology
- "dead code", "unused", "vestigial" → vestigial
