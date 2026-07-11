> **Archived 2026-04-22.** This document describes the pre-2026-04-22
> compiled-binary / Python-module CLI contract for perspectives. It is
> retained as history. The implementation path is a per-skill rewrite
> (see `MIGRATION_SPEC.md §11` and
> `docs/references/plugin-self-containment.md`); the CLI-as-single-entry-point
> framing is no longer authoritative.

# Perspectives CLI Specification (archived)

**Status:** Archived — documents a prior implementation path.
**Package (historical):** `plugins/perspectives/src/` (bun/Effect) and
`plugins/perspectives/cli/` (Python port). Both removed 2026-04-22.
**Version Target:** 1.0.0

## Overview

The perspectives CLI codifies deterministic operations for persona management and dialogue lifecycle. It mirrors the journal CLI architecture: a unified entry point routing to verb-based commands with content-type subcommands.

### Goals

1. **Unify scripts** - Consolidate 7+ individual scripts into coherent CLI
2. **Enable composition** - Skills invoke CLI; commands compose skills
3. **Support resume/extend** - Dialogues persist across sessions per DISCOURSE spec
4. **Follow patterns** - Use established lib/, @seed/page, PAGE protocol conventions
5. **Prepare distribution** - Bun compile for self-contained binary

### Non-Goals

- Orchestration logic (belongs in switchboard)
- Collision topologies (experimental, skill-driven)
- Persona synthesis prompts (inference, not deterministic)

## Command Structure

```
perspectives <command> <subcommand> [options]
```

### Persona Commands

```bash
# Create or update persona
perspectives persona save --id <id> --data '<yaml>'
perspectives persona save --id <id> --file <path>

# Read persona
perspectives persona read --id <id>
perspectives persona read --id <id> --yaml
perspectives persona read --id <id> --section <name>

# List personas
perspectives persona list
perspectives persona list --count 5
perspectives persona list --framework empiricism
perspectives persona list --domain psychology
perspectives persona list --yaml

# Search personas (substring)
perspectives persona search <pattern>
perspectives persona search "systems thinking" --yaml

# Search personas (regex)
perspectives persona search -r "^sys"
perspectives persona search -r "security" -r "expert"  # AND logic
```

### Dialogue Commands

```bash
# Start dialogue (creates .dialogues/ entry)
perspectives dialogue start --topic <text> --personas <id1,id2,...>
perspectives dialogue start --topic "API design" --personas "backend,frontend" --max-rounds 5

# Add turn
perspectives dialogue turn --id <dialogue-id> --persona <id> --content <text>
perspectives dialogue turn --id api-design-2025-12-21 --persona backend --content "We should use REST" --type query --to frontend

# End dialogue (marks completed, adds insights)
perspectives dialogue end --id <dialogue-id> --insights '<json-array>'

# Show dialogue state
perspectives dialogue show --id <dialogue-id>
perspectives dialogue show --id <dialogue-id> --yaml

# List dialogues
perspectives dialogue list
perspectives dialogue list --status active
perspectives dialogue list --status completed
perspectives dialogue list --since 7d
```

### Resume/Extend (Per DISCOURSE Spec)

```bash
# Resume with same participants
perspectives dialogue resume --id <dialogue-id>
perspectives dialogue resume --id api-design-2025-12-21 --rounds 3

# Extend with new perspective
perspectives dialogue extend --id <dialogue-id> --add <persona-id>
perspectives dialogue extend --id api-design-2025-12-21 --add security-architect
```

### Trace Commands

Traces capture automaton movement through attention space. Automatons emit `[TRACE]` markers during execution; these commands persist and query trace data for collision analysis.

```bash
# Save trace from automaton execution
perspectives trace save --session <session-id> --persona <persona-id> --data '<trace-content>'
perspectives trace save --session api-analysis-20251221 --persona systems-explorer --file trace-output.txt

# Read trace
perspectives trace read --session <session-id> --persona <persona-id>
perspectives trace read --session api-analysis-20251221 --persona systems-explorer --yaml

# List traces for a session
perspectives trace list --session <session-id>
perspectives trace list --session api-analysis-20251221

# List all sessions with traces
perspectives trace sessions
perspectives trace sessions --since 7d

# Delete traces (cleanup)
perspectives trace delete --session <session-id>
perspectives trace delete --session <session-id> --persona <persona-id>
```

**Trace format** (what automatons emit):

```
[TRACE] (layer, geometry, primitive)
Sensing: what was noticed
Inference: what meaning was derived
→ Skill("skill-name")
→ Next: (layer, geometry, primitive) because [reasoning]
```

**Storage**: `.thinkies/.perspectives/.traces/<session-id>/<persona-id>.trace`

**Integration with spawn-automaton**: The `/perspectives:spawn-automaton` command instructs agents to call `perspectives trace save` as their final action, persisting their movement path for later collision analysis.

**Integration with collide**: The `collide.ts` script (or future `/perspectives:collide` command) reads traces via `perspectives trace read` to compute coverage, interference, and emergence patterns.

## Architectural Context

### The Perspectives Processing Chain

The perspectives plugin implements semantic signal processing through three layers:

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 1: DEFINITION (CLI)                                      │
│  perspectives persona save/read/list/search                     │
│  perspectives dialogue start/turn/end/show/list/resume/extend   │
│                                                                 │
│  Deterministic CRUD. Storage in .thinkies/.personas/ and        │
│  .thinkies/.dialogues/. Rebuild index on every save.            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 2: INSTANTIATION (Task tool with agents)                 │
│  Personas spawned as automatons via create-automaton agent      │
│  Automatons emit [TRACE] markers as they move through           │
│  attention space (10 layers × 3 geometries = 30 cells)          │
│                                                                 │
│  Inference-driven movement. Non-deterministic.                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 3: COLLISION ANALYSIS (collide.ts)                       │
│  Post-hoc analysis of automaton traces                          │
│  Detects interference patterns: constructive/destructive        │
│  Generates emergent questions from reasoning path conflicts     │
│                                                                 │
│  Standalone script. Takes trace files, not persona IDs.         │
└─────────────────────────────────────────────────────────────────┘
```

### Collide's Role

`collide.ts` operates on the output of Layer 2, not Layer 1. Its inputs are trace files containing `[TRACE]` blocks from automaton execution:

```
[TRACE] (layer, geometry, primitive)
Sensing: what was noticed
Inference: what meaning was derived
→ Skill("skill-name")
```

Collide computes:

- **Coverage**: Which cells each persona visited
- **Interference**: Where paths intersect (same cell, different inferences)
- **Emergence**: Questions that arise from destructive interference
- **Synthesis patterns**: dialectical, complementary, reinforcement, productive_conflict

**Collide remains a standalone script** because its input model differs fundamentally from CLI commands. CLI commands operate on IDs and YAML content; collide operates on execution traces.

**Integrity requirement**: Collide must be tested alongside CLI. Persona schema changes that affect automaton configuration must not break trace parsing. The test suite validates end-to-end: define persona → spawn automaton → collect traces → run collide.

### Switchboard Integration

**Current state**: `discourse-turn.ts` writes directly to `.dialogues/` storage.

**Future direction**: Switchboard will call the perspectives CLI for all dialogue mutations. This establishes perspectives as the single authority for semantic content, with switchboard handling only coordination mechanics (PATCH state, blocking, heartbeats, turn-taking).

```typescript
// Future: switchboard calls CLI
const result = await exec(`perspectives dialogue turn --id ${dialogueId} --persona ${speaker} --content "${content}"`);

// Switchboard only manages coordination state
await updatePatchState(patchId, { currentSpeaker: nextSpeaker });
```

## Storage Architecture

All persistence uses YAML with `Document<T>` envelope from `@seed/lib/store`.

### Directory Structure

```
~/.claude/.thinkies/
└── .perspectives/
    ├── .personas/
    │   ├── index.yaml              # PersonaIndex for search
    │   ├── empirical-researcher.yaml
    │   ├── systems-thinker.yaml
    │   └── ...
    ├── .dialogues/
    │   ├── api-design-2025-12-21.yaml
    │   ├── auth-flow-2025-12-20.yaml
    │   └── ...
    └── .traces/
        ├── session-abc123/
        │   ├── systems-explorer.trace
        │   └── skeptic.trace
        └── ...
```

**Migration note**: Existing `.personas/` and `.dialogues/` at `.thinkies/` root will be moved to `.thinkies/.perspectives/`. The CLI handles this migration on first run.

### Persona Schema

```yaml
id: "uuid-v7"
schema_version: "1.0.0"
created: "2025-12-21T16:00:00Z"
last_modified: "2025-12-21T16:00:00Z"
last_accessed: "2025-12-21T17:00:00Z"
data:
  persona_id: "empirical-researcher"
  expertise_domain: "Experimental psychology, quantitative methods"
  epistemic_framework: "Empiricism"
  question_methodology:
    knowledge_seeking:
      primary_questions:
        - "What does the evidence show?"
        - "What studies have been conducted?"
    relationship_mapping:
      primary_questions:
        - "How do these findings relate?"
    contrast_identification:
      primary_questions:
        - "What alternative explanations exist?"
    integration_synthesis:
      primary_questions:
        - "What can we conclude from the evidence?"
  research_protocol:
    source_hierarchy:
      - "Peer-reviewed meta-analyses"
      - "Randomized controlled trials"
      - "Observational studies"
    conflict_resolution: "Weight by methodology quality"
  claim_support_patterns:
    when_challenged:
      - "Request specific counterevidence"
      - "Examine methodology of contradicting claims"
    when_supporting_claim:
      - "Cite specific studies"
      - "Note effect sizes and confidence intervals"
    when_encountering_contradiction:
      - "Examine moderating variables"
      - "Consider methodological differences"
  reasoning_state_tracking:
    monitoring_priorities:
      - "Confirmation bias"
      - "Sample size sensitivity"
```

### Dialogue Schema (Extended for Resume)

```yaml
id: "uuid-v7"
schema_version: "1.1.0"
created: "2025-12-21T16:00:00Z"
last_modified: "2025-12-21T17:00:00Z"
last_accessed: "2025-12-21T17:00:00Z"
data:
  dialogue_id: "api-design-2025-12-21"
  topic: "API design decisions"
  status: "active" | "completed"
  participants:
    - persona_id: "backend-engineer"
      role: "participant"
    - persona_id: "frontend-engineer"
      role: "participant"
  turns:
    - id: "uuid-v7"
      turn_number: 1
      timestamp: "2025-12-21T16:05:00Z"
      persona_id: "backend-engineer"
      interaction_type: "open" | "query" | "challenge" | "provoke" | "inspire" | "synthesize"
      content: "We should use REST for this API."
      addressed_to: null
  insights: []
  completed: null

  # Resume support (new fields)
  max_rounds: 5 | null
  completed_rounds: 2
  session_history:
    - patch_id: "patch-abc123"
      started: "2025-12-21T16:00:00Z"
      ended: "2025-12-21T17:00:00Z"
      rounds_completed: 2
```

### Persona Index Schema

```yaml
personas:
  - persona_id: "empirical-researcher"
    expertise_domain: "Experimental psychology"
    epistemic_framework: "Empiricism"
    file_path: "empirical-researcher.yaml"
    updated: "2025-12-21T16:00:00Z"
  - persona_id: "systems-thinker"
    expertise_domain: "Complex systems analysis"
    epistemic_framework: "Systems theory"
    file_path: "systems-thinker.yaml"
    updated: "2025-12-20T14:00:00Z"
```

### Trace Schema

Traces are plain text files containing `[TRACE]` blocks. Stored at `.thinkies/.perspectives/.traces/<session-id>/<persona-id>.trace`.

```
[TRACE] (observe, zone, OBSERVE)
Sensing: Deployment pipeline has multiple feedback paths
Inference: Suggests reinforcing dynamics worth mapping
→ Skill("decompose")
→ Next: (rotate, zone, LINK) because components need relationship mapping

[TRACE] (rotate, zone, LINK)
Sensing: Build output feeds test runner, test results gate deployment
Inference: Sequential dependency chain with quality gate
→ Skill("connect-dots")
→ Next: (assess, zone, ATTUNE) because need to find leverage points

[TRACE] (assess, zone, ATTUNE)
Sensing: CI timeout causes most pipeline failures
Inference: Timeout is high-leverage intervention point
→ Skill("find-leverage-points")
→ Next: (engage, zone, GENERATE) because ready to synthesize findings
```

**Trace metadata** (stored alongside trace file as `<persona-id>.meta.yaml`):

```yaml
session_id: "api-analysis-20251221"
persona_id: "systems-explorer"
task: "Analyze feedback loops in deployment pipeline"
started: "2025-12-21T16:00:00Z"
completed: "2025-12-21T16:15:00Z"
cells_visited: 4
skills_invoked:
  - decompose
  - connect-dots
  - find-leverage-points
```

## Validation Rules

### Persona Validation

**Required fields** (error if missing):

- `persona_id` — Identity of the perspective
- `expertise_domain` — What this perspective knows

**Optional fields** (accept silently if missing):

- `epistemic_framework` — Named framework (empiricism, pragmatism, etc.)
- `question_methodology` — Inquiry patterns across four categories
- `research_protocol` — Source hierarchy and conflict resolution
- `claim_support_patterns` — Response patterns when challenged/supporting/contradicting
- `reasoning_state_tracking` — What to monitor across turns
- `automaton_configuration` — Movement rules for trace-emitting personas

**Index integrity**: Rebuild index on every save. The index is the source of truth for search/list operations. Stale indices break discovery.

### Dialogue Validation

**Required fields** (error if missing):

- `topic` — What the dialogue explores
- `participants` — At least 2 persona IDs (validated against index)

**Participant validation**: Each persona ID must exist in the persona index. Error with list of valid IDs if not found.

**Turn validation**:

- `persona_id` must be in participants list
- `interaction_type` must be one of: open, query, challenge, provoke, inspire, synthesize
- `addressed_to` (if provided) must be in participants list

## Output Format (PAGE Protocol)

**YAML for all output.** Less noise than JSON, matches storage format, human-readable.

All commands emit PAGE-structured output using CAID pattern:

- **Confirm**: What operation was attempted
- **Affirm**: What was correct (checkmarks)
- **Inform**: What happened or failed
- **Dial**: Next action to take

### Success Output

```
╔═══════════════════════════════════════════════════════════════╗
║  PERSONA SAVED                                                ║
╟───────────────────────────────────────────────────────────────╢
║  ID:       empirical-researcher                               ║
║  Domain:   Experimental psychology, quantitative methods      ║
║  File:     ~/.claude/.thinkies/.personas/empirical-researcher.yaml
╟───────────────────────────────────────────────────────────────╢
║  Next: perspectives persona read --id empirical-researcher    ║
╚═══════════════════════════════════════════════════════════════╝
```

Plus YAML for programmatic use:

```yaml
status: success
persona_id: empirical-researcher
expertise_domain: Experimental psychology, quantitative methods
path: ~/.claude/.thinkies/.personas/empirical-researcher.yaml
next: perspectives persona read --id empirical-researcher
```

### Error Output (CAID Pattern)

```
╔═══════════════════════════════════════════════════════════════╗
║  ERROR                                                        ║
╟───────────────────────────────────────────────────────────────╢
║  Persona not found: unknown-expert                            ║
║                                                               ║
║  ✓ Correct command format                                     ║
║  ✓ ID format valid (kebab-case)                              ║
║  ✗ No persona with this ID exists                            ║
╟───────────────────────────────────────────────────────────────╢
║  Next: perspectives persona list                              ║
║  Or:   perspectives persona save --id unknown-expert --data...║
╚═══════════════════════════════════════════════════════════════╝
```

Plus YAML for programmatic use:

```yaml
status: error
confirm: You attempted to read persona 'unknown-expert'
affirm:
  - Command format correct
  - ID format valid
inform: No persona with this ID exists
dial: perspectives persona list
```

### Handoff (Routing Trace)

```yaml
type: handoff
request: perspectives dialogue turn
routed_to: perspectives-cli (commands/dialogue/turn.ts)
reason: Turn submission updates dialogue state
```

## Package Structure

```
packages/perspectives/
├── cli.ts                      # Entry point
├── package.json
├── README.md
├── commands/
│   ├── persona/
│   │   ├── index.ts            # PersonaCommand router
│   │   ├── save.ts
│   │   ├── read.ts
│   │   ├── list.ts
│   │   └── search.ts
│   ├── dialogue/
│   │   ├── index.ts            # DialogueCommand router
│   │   ├── start.ts
│   │   ├── turn.ts
│   │   ├── end.ts
│   │   ├── show.ts
│   │   ├── list.ts
│   │   ├── resume.ts
│   │   └── extend.ts
│   └── trace/
│       ├── index.ts            # TraceCommand router
│       ├── save.ts
│       ├── read.ts
│       ├── list.ts
│       ├── sessions.ts
│       └── delete.ts
├── lib/
│   ├── types.ts                # Extended types for CLI
│   ├── persona_store.ts        # PersonaStore extends YamlStore
│   ├── dialogue_store.ts       # DialogueStore extends YamlStore
│   ├── trace_store.ts          # TraceStore for .traces/ management
│   └── validation.ts           # Schema validation
├── scripts/
│   └── distribute.ts           # Bun compile script
└── dist/
    └── perspectives            # Compiled binary
```

## Integration Points

### With lib/ (Shared Utilities)

```typescript
import { getThinkiesRoot, slugify, generateId } from '@seed/lib/core';
import { parseYaml, toYaml } from '@seed/lib/yaml';
import { YamlStore, type Document } from '@seed/lib/store';
import { pageError, pageSuccess, pageHandoff } from '@seed/lib/page';
```

### With @seed/page (Command Infrastructure)

```typescript
import { createCli, type CommandModule, type ParsedCommand } from '@seed/page';
import { createErrorHandler } from '@seed/page';
import { renderBox, renderTable, colors } from '@seed/page';
```

### With Switchboard (Discourse Coordination)

The perspectives CLI handles **semantic content** (personas, dialogue turns, insights).
Switchboard handles **coordination mechanics** (PATCH, blocking, heartbeats).

Coordination handoff pattern:

```typescript
// In /discourse command (switchboard)
const { patchId, dialogueId } = await initDiscourseSession(config);

// Agents call perspectives CLI for turn content
const result = await exec(`perspectives dialogue turn --id ${dialogueId} ...`);

// Switchboard manages next speaker, timeouts, stop signals
```

### With Skills

Skills invoke CLI for deterministic operations:

```markdown
<!-- plugins/perspectives/skills/persona-define/SKILL.md -->
## Execution

1. Synthesize persona from requirements
2. Save via CLI: `perspectives persona save --id <id> --data '<yaml>'`
3. Confirm via: `perspectives persona read --id <id>`
```

## Resume/Extend Logic

Per DISCOURSE spec:

### Resume Rules

1. Load existing dialogue
2. If `max_rounds` exhausted → set to unlimited (they asked for more)
3. If remaining rounds → use remaining
4. If explicit `--rounds N` → use that
5. First speaker: whoever didn't speak last (alternating fairness)

### Extend Rules

1. Load existing dialogue
2. Validate new persona exists
3. Add to participants list
4. New persona gets next turn (they were invited to speak)

### Session History

Each resume/extend creates new session_history entry:

```yaml
session_history:
  - patch_id: "patch-abc123"
    started: "2025-12-21T16:00:00Z"
    ended: "2025-12-21T17:00:00Z"
    rounds_completed: 2
  - patch_id: "patch-def456"  # New session from resume
    started: "2025-12-21T18:00:00Z"
    ended: null
    rounds_completed: 0
```

## Development Workflow

### Setup

```bash
# Create package
mkdir -p packages/perspectives
cd packages/perspectives

# Initialize
cat > package.json << 'EOF'
{
  "name": "@seed/perspectives-cli",
  "version": "1.0.0",
  "type": "module",
  "main": "cli.ts",
  "bin": {
    "perspectives": "./dist/perspectives"
  },
  "dependencies": {
    "@seed/lib": "workspace:*",
    "@seed/page": "workspace:*"
  }
}
EOF

# Link workspace
cd ../..
bun install
```

### Build

```bash
# Compile to binary
bun build packages/perspectives/cli.ts --compile --outfile packages/perspectives/dist/perspectives

# Or use distribute script
bun packages/perspectives/scripts/distribute.ts
```

### Test

```bash
# Unit tests
bun test packages/perspectives/

# Integration tests (with compiled binary)
bun test packages/perspectives/**/*.integration.test.ts
```

### Build for Plugin Distribution

```bash
# Compile to standalone binary
bun build --compile --outfile plugins/perspectives/scripts/perspectives scripts/perspectives.ts
```

## Migration from Existing Scripts

| Existing Script | New CLI Command |
|-----------------|-----------------|
| `save_persona.ts` | `perspectives persona save` |
| `read_persona.ts` | `perspectives persona read` |
| `list_personas.ts` | `perspectives persona list` |
| `search_personas.ts` | `perspectives persona search` |
| `start_dialogue.ts` | `perspectives dialogue start` |
| `add_turn.ts` | `perspectives dialogue turn` |
| `end_dialogue.ts` | `perspectives dialogue end` |
| `collide.ts` | *(standalone — Layer 3 analysis, different input model)* |

Skills update to invoke CLI instead of direct scripts.

## Decisions Made

1. **Index management** — Rebuild on every save. Integrity is primary concern.
2. **Validation strictness** — Error on missing required fields; accept optional fields silently.
3. **Output format** — YAML. Less noise, matches storage format, human-readable.
4. **Switchboard integration** — Will call perspectives CLI for dialogue mutations (future).
5. **Skill invocation** — Skills call compiled binary, not `bun cli.ts`.
6. **Directory consolidation** — All perspectives storage under `.thinkies/.perspectives/`.
7. **Trace storage** — Automaton traces live in `.thinkies/.perspectives/.traces/`.
8. **End-to-end testing** — Tests across all three layers serve as breathing documentation of intention.
9. **Single-process model** — No concurrent writes. File-level advisory locking prevents corruption.
10. **Migration is non-interactive** — Runs automatically on first command that needs it. No prompts.
11. **Schema versioning** — Documents include schema_version. CLI rejects future versions, auto-migrates past versions.
12. **Error codes** — Three-character codes by category (VAL, STO, CON, MIG) for programmatic handling.
13. **Debug output** — Environment variables control verbosity. No flags to pollute command interface.
14. **Performance baseline** — Sub-100ms for reads, sub-500ms for saves with index rebuild at <100 personas.
15. **Trace persistence via CLI** — Automatons call `perspectives trace save` explicitly. No hook-based capture (Claude Code hooks can't reliably persist Task tool output). Agent responsibility, not infrastructure magic.

## Error Taxonomy

All errors use three-character codes for programmatic handling. CAID structure provides human guidance.

### Input Validation Errors (VAL)

| Code | Trigger | Message Template | CAID Guidance |
|------|---------|------------------|---------------|
| VAL001 | Missing required field | `Required field missing: {field_name}` | Affirm: Command format correct<br>Inform: Missing field name<br>Dial: Show example with field |
| VAL002 | Invalid format | `Invalid format for {field_name}: expected {expected}, got {actual}` | Affirm: Field provided<br>Inform: Format mismatch<br>Dial: Show correct format |
| VAL003 | Unknown persona ID | `Persona not found: {persona_id}` | Affirm: ID format valid<br>Inform: No persona exists<br>Dial: `perspectives persona list` |
| VAL004 | Invalid interaction type | `Invalid interaction_type: {type}. Must be one of: {valid_types}` | Affirm: Turn format correct<br>Inform: Type not recognized<br>Dial: List valid types |
| VAL005 | Addressed-to not in participants | `addressed_to '{persona_id}' not in participants: {valid_ids}` | Affirm: Turn submitted<br>Inform: Recipient unknown<br>Dial: List participants |
| VAL006 | Too few participants | `Dialogue requires at least 2 participants, got {count}` | Affirm: Topic accepted<br>Inform: Need more personas<br>Dial: `perspectives persona list` |
| VAL007 | Speaker not participant | `Persona '{persona_id}' not in dialogue participants: {valid_ids}` | Affirm: Turn format valid<br>Inform: Speaker not participating<br>Dial: List participants |
| VAL008 | Dialogue completed | `Dialogue '{dialogue_id}' has status 'completed'. Cannot add turns.` | Affirm: Dialogue exists<br>Inform: Already ended<br>Dial: `perspectives dialogue resume` |

### Storage Errors (STO)

| Code | Trigger | Message Template | CAID Guidance |
|------|---------|------------------|---------------|
| STO001 | File not found | `File not found: {path}` | Affirm: ID format valid<br>Inform: File missing<br>Dial: Create with save command |
| STO002 | Permission denied | `Permission denied: {path}` | Affirm: Path valid<br>Inform: Insufficient permissions<br>Dial: Check directory ownership |
| STO003 | Corrupt YAML | `Failed to parse YAML: {path}<br>Error: {error_message}` | Affirm: File exists<br>Inform: YAML syntax error<br>Dial: `perspectives doctor --check-storage` |
| STO004 | Invalid document structure | `Document missing required envelope fields: {missing_fields}` | Affirm: Valid YAML<br>Inform: Not a valid Document<T><br>Dial: Run doctor command |
| STO005 | Index rebuild failed | `Index rebuild failed after save<br>Error: {error_message}` | Affirm: Persona saved<br>Inform: Index inconsistent<br>Dial: `perspectives doctor --rebuild-index` |
| STO006 | Write failed mid-operation | `Write failed: {path}<br>Error: {error_message}` | Affirm: Validation passed<br>Inform: Disk write error<br>Dial: Check disk space and permissions |

### Concurrency Errors (CON)

| Code | Trigger | Message Template | CAID Guidance |
|------|---------|------------------|---------------|
| CON001 | Lock acquisition failed | `Could not acquire lock: {path}<br>Another process may be writing.` | Affirm: Request valid<br>Inform: Resource locked<br>Dial: Wait and retry |
| CON002 | Lock timeout | `Lock acquisition timed out after {timeout}ms` | Affirm: Request valid<br>Inform: Lock held too long<br>Dial: Check for stale locks with doctor |
| CON003 | Stale lock detected | `Stale lock detected: {path}<br>Created: {timestamp}` | Affirm: Request valid<br>Inform: Lock older than threshold<br>Dial: `perspectives doctor --clear-locks` |

### Migration Errors (MIG)

| Code | Trigger | Message Template | CAID Guidance |
|------|---------|------------------|---------------|
| MIG001 | Migration failed | `Migration failed: {migration_name}<br>Error: {error_message}` | Affirm: Migration started<br>Inform: Partial state possible<br>Dial: Check backup at {backup_path} |
| MIG002 | Rollback failed | `Migration rollback failed<br>Error: {error_message}` | Affirm: Detected failure<br>Inform: Cannot restore automatically<br>Dial: Restore from {backup_path} |
| MIG003 | Unsupported schema version | `Schema version {version} not supported by CLI {cli_version}` | Affirm: Document loaded<br>Inform: Version mismatch<br>Dial: Upgrade CLI or use older version |
| MIG004 | Migration incomplete | `Migration {migration_name} did not complete validation` | Affirm: Files moved<br>Inform: Validation failed<br>Dial: Restore from backup |

## Concurrency Model

**Single-process constraint**: The perspectives CLI uses file-level advisory locking to prevent concurrent writes. No support for distributed coordination across machines.

### Locking Strategy

```typescript
// Acquire exclusive lock before any write operation
const lockPath = `${targetPath}.lock`;
const lockFile = Bun.file(lockPath);
await lockFile.write(`${process.pid}\n${Date.now()}`);

// Write operation
await writeFile(targetPath, content);

// Release lock
await unlink(lockPath);
```

### Lock Acquisition Rules

1. **Timeout**: 5000ms. If lock not acquired, fail with CON002.
2. **Staleness threshold**: Locks older than 60s are stale. Removed automatically before retry.
3. **Scope**: Persona saves lock `.personas/index.yaml`, dialogue saves lock individual dialogue files.
4. **Index rebuild**: Persona index lock held for entire rebuild duration.

### Race Condition Scenarios

| Scenario | Behavior | Error Code |
|----------|----------|------------|
| Two processes save same persona | Second waits for lock, overwrites first (last-write-wins) | — |
| Two processes save different personas | Both acquire locks, both succeed, index rebuilt twice (acceptable) | — |
| Process crashes while holding lock | Stale lock remains. Next operation detects staleness, removes lock, retries. | CON003 |
| Lock held >60s | Considered stale. Removed on next acquisition attempt. | CON003 |

### Index Consistency Guarantees

- **Save operation**: Lock → write persona → rebuild index → unlock
- **Read operation**: No lock required (eventual consistency acceptable)
- **List/search**: Read index without lock (stale index better than blocking reads)

**Trade-off accepted**: Index may be briefly stale (up to lock timeout duration) if rebuild fails. `doctor --rebuild-index` repairs.

## Migration Specification

**Goal**: Move `.thinkies/.personas/` and `.thinkies/.dialogues/` to `.thinkies/.perspectives/` without data loss.

### Detection

Migration needed when:

1. `.thinkies/.perspectives/` does not exist, AND
2. `.thinkies/.personas/` OR `.thinkies/.dialogues/` exists

Check runs automatically on first command requiring storage access.

### Migration Procedure

```typescript
async function migrate(): Promise<MigrationResult> {
  const thinkiesRoot = getThinkiesRoot();
  const oldPersonasDir = join(thinkiesRoot, '.personas');
  const oldDialoguesDir = join(thinkiesRoot, '.dialogues');
  const newPerspectivesDir = join(thinkiesRoot, '.perspectives');
  const backupDir = join(thinkiesRoot, '.perspectives-backup-{timestamp}');

  // 1. Create backup
  await cp(oldPersonasDir, join(backupDir, '.personas'), { recursive: true });
  await cp(oldDialoguesDir, join(backupDir, '.dialogues'), { recursive: true });

  // 2. Create new structure
  await mkdir(join(newPerspectivesDir, '.personas'), { recursive: true });
  await mkdir(join(newPerspectivesDir, '.dialogues'), { recursive: true });
  await mkdir(join(newPerspectivesDir, '.traces'), { recursive: true });

  // 3. Move files
  await cp(oldPersonasDir, join(newPerspectivesDir, '.personas'), { recursive: true });
  await cp(oldDialoguesDir, join(newPerspectivesDir, '.dialogues'), { recursive: true });

  // 4. Validate
  const oldCount = await countYamlFiles([oldPersonasDir, oldDialoguesDir]);
  const newCount = await countYamlFiles([
    join(newPerspectivesDir, '.personas'),
    join(newPerspectivesDir, '.dialogues')
  ]);

  if (oldCount !== newCount) {
    throw new Error(`File count mismatch: ${oldCount} → ${newCount}`);
  }

  // 5. Remove old directories
  await rm(oldPersonasDir, { recursive: true });
  await rm(oldDialoguesDir, { recursive: true });

  return { status: 'success', backupPath: backupDir, filesMovedCount: newCount };
}
```

### Atomicity

**Best-effort atomicity**: Migration uses copy-then-delete. If migration fails:

1. New structure is incomplete (validation catches this)
2. Old structure remains intact
3. Backup exists at `.perspectives-backup-{timestamp}/`

**Not transactional**: Filesystem operations are not atomic. If the process crashes mid-migration, you may need to recover manually from the backup.

### Rollback

**Automatic rollback** on validation failure:

```typescript
if (validation.failed) {
  // Remove incomplete new structure
  await rm(newPerspectivesDir, { recursive: true });
  // Old directories still exist
  throw new MigrationError('MIG004', 'Validation failed after file move');
}
```

**Manual recovery** if process crashes:

```bash
# Restore from backup
mv ~/.claude/.thinkies/.perspectives-backup-{timestamp}/.personas ~/.claude/.thinkies/.personas
mv ~/.claude/.thinkies/.perspectives-backup-{timestamp}/.dialogues ~/.claude/.thinkies/.dialogues
rm -rf ~/.claude/.thinkies/.perspectives
```

### First-Run Behavior

**Non-interactive**: Migration runs automatically. No prompts.

Output on migration:

```
╔═══════════════════════════════════════════════════════════════╗
║  MIGRATION IN PROGRESS                                        ║
╟───────────────────────────────────────────────────────────────╢
║  Moving personas and dialogues to new directory structure...  ║
║  Backup created: .perspectives-backup-1734796800              ║
╚═══════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════╗
║  MIGRATION COMPLETE                                           ║
╟───────────────────────────────────────────────────────────────╢
║  Files moved: 15                                              ║
║  New location: ~/.claude/.thinkies/.perspectives/             ║
║  Backup: ~/.claude/.thinkies/.perspectives-backup-1734796800  ║
╚═══════════════════════════════════════════════════════════════╝
```

### Post-Migration Validation

```typescript
interface MigrationValidation {
  fileCountMatch: boolean;
  allYamlParseable: boolean;
  personaIndexRebuildSucceeded: boolean;
  dialogueIdsUnique: boolean;
}
```

Validation failures trigger rollback (remove new structure, keep old).

## Schema Evolution

Documents include `schema_version` field for forward/backward compatibility.

### Version Checking

```typescript
function validateSchemaVersion(doc: Document<unknown>): ValidationResult {
  const docVersion = semver.parse(doc.schema_version);
  const cliVersion = semver.parse(CLI_VERSION);

  // Reject future versions
  if (docVersion.major > cliVersion.major) {
    return { status: 'error', code: 'MIG003', message: `Schema version ${doc.schema_version} not supported by CLI ${CLI_VERSION}` };
  }

  // Auto-migrate past versions
  if (docVersion.major < cliVersion.major) {
    return { status: 'needs_migration', targetVersion: CLI_VERSION };
  }

  return { status: 'ok' };
}
```

### Compatibility Rules

| Document Version | CLI Version | Behavior |
|------------------|-------------|----------|
| 1.0.0 | 1.0.0 | Load directly |
| 1.0.0 | 1.1.0 | Load directly (backward compatible) |
| 1.1.0 | 1.0.0 | Reject with MIG003 (forward incompatible) |
| 1.0.0 | 2.0.0 | Auto-migrate on load |
| 2.0.0 | 1.0.0 | Reject with MIG003 |

### Migration Functions

```typescript
type MigrationFn = (doc: Document<unknown>) => Document<unknown>;

const migrations: Record<string, MigrationFn> = {
  '1.0.0->1.1.0': (doc) => {
    // Add new fields for dialogue resume support
    if (!doc.data.max_rounds) doc.data.max_rounds = null;
    if (!doc.data.session_history) doc.data.session_history = [];
    doc.schema_version = '1.1.0';
    return doc;
  },
  '1.1.0->2.0.0': (doc) => {
    // Future migration example
    doc.schema_version = '2.0.0';
    return doc;
  }
};
```

### When Migrations Run

1. **On load**: Document version checked. If major version mismatch, migration applied in-memory.
2. **On save**: Migrated document written back with new schema_version.
3. **Explicit**: `perspectives doctor --migrate-all` upgrades all documents.

### Migration Storage

Migration functions live in `packages/perspectives/lib/migrations.ts`. Each migration:

- Has version pair as key: `'1.0.0->1.1.0'`
- Is pure function (no side effects)
- Updates `schema_version` field
- Preserves all existing data

## Debug Infrastructure

Environment variables control debug output, not CLI flags. This keeps the command interface clean for scripting.

### Environment Variables

| Variable | Effect | Example |
|----------|--------|---------|
| `PERSPECTIVES_DEBUG=1` | Show internal state (locks, migrations, index rebuilds) | `PERSPECTIVES_DEBUG=1 perspectives persona save ...` |
| `PERSPECTIVES_VERBOSE=1` | Show detailed progress (file reads, writes, validations) | `PERSPECTIVES_VERBOSE=1 perspectives dialogue list` |
| `PERSPECTIVES_LOG_FILE=<path>` | Write logs to file instead of stderr | `PERSPECTIVES_LOG_FILE=/tmp/perspectives.log perspectives ...` |

### Debug Output Format

```
[DEBUG] Lock acquired: /Users/x/.claude/.thinkies/.perspectives/.personas/index.yaml.lock
[DEBUG] Reading persona: empirical-researcher
[DEBUG] Rebuilding index: 12 personas
[DEBUG] Lock released: index.yaml.lock
```

Verbose output:

```
[VERBOSE] Reading file: /Users/x/.claude/.thinkies/.perspectives/.personas/empirical-researcher.yaml
[VERBOSE] Parsing YAML: 245 bytes
[VERBOSE] Validating schema: persona v1.0.0
[VERBOSE] Validation passed: all required fields present
```

### Doctor Command

```bash
# Health check
perspectives doctor

# Rebuild persona index
perspectives doctor --rebuild-index

# Clear stale locks
perspectives doctor --clear-locks

# Migrate all documents to current schema
perspectives doctor --migrate-all

# Check storage integrity
perspectives doctor --check-storage
```

**Doctor output**:

```
╔═══════════════════════════════════════════════════════════════╗
║  PERSPECTIVES HEALTH CHECK                                    ║
╟───────────────────────────────────────────────────────────────╢
║  ✓ Storage directory exists                                   ║
║  ✓ Personas directory accessible                              ║
║  ✓ Dialogues directory accessible                             ║
║  ✓ All YAML files parseable (15/15)                           ║
║  ✓ All personas in index (12/12)                              ║
║  ✓ No stale locks detected                                    ║
║  ✓ Schema versions compatible                                 ║
╟───────────────────────────────────────────────────────────────╢
║  Status: HEALTHY                                              ║
╚═══════════════════════════════════════════════════════════════╝
```

With issues:

```
╔═══════════════════════════════════════════════════════════════╗
║  PERSPECTIVES HEALTH CHECK                                    ║
╟───────────────────────────────────────────────────────────────╢
║  ✓ Storage directory exists                                   ║
║  ✓ Personas directory accessible                              ║
║  ✗ Dialogues directory missing                                ║
║  ✓ All YAML files parseable (12/15)                           ║
║  ✗ 3 files failed to parse                                    ║
║  ✗ Index missing 2 personas                                   ║
║  ✓ No stale locks detected                                    ║
║  ✗ 2 documents have incompatible schema versions              ║
╟───────────────────────────────────────────────────────────────╢
║  Status: UNHEALTHY (4 issues)                                 ║
║  Next: perspectives doctor --rebuild-index                    ║
║        perspectives doctor --migrate-all                      ║
╚═══════════════════════════════════════════════════════════════╝
```

## Performance Benchmarks

Target baselines for acceptable performance at scale.

### Latency Targets

| Operation | Target | Measured At |
|-----------|--------|-------------|
| `persona read` | <50ms | Any persona count |
| `persona save` (no index rebuild) | <100ms | Any persona count |
| `persona save` (with index rebuild) | <500ms | <100 personas |
| `persona list` | <50ms | <100 personas |
| `persona search` | <100ms | <100 personas |
| `dialogue start` | <100ms | Any dialogue count |
| `dialogue turn` | <100ms | <1000 turns |
| `dialogue show` | <100ms | <1000 turns |
| `dialogue list` | <100ms | <50 dialogues |

### Size Constraints

| Metric | Target |
|--------|--------|
| Binary size (compiled) | <100MB |
| Memory usage (peak) | <50MB |
| Persona index size | <1MB at 100 personas |
| Dialogue file size | <10MB at 1000 turns |

### Performance Degradation

**Acceptable**: Linear degradation with dataset size.
**Unacceptable**: Quadratic or worse degradation.

**Index rebuild** is O(n) where n = persona count. At 1000 personas, rebuild may take 5s. This is acceptable since saves are infrequent.

**Search** is O(n) linear scan of index. At 1000 personas, search may take 500ms. Acceptable for v1.0.0. Future optimization: full-text search index.

## Switchboard Integration Contract

The perspectives CLI is a subprocess invoked by switchboard for dialogue operations.

### Interface

**Invocation**:

```typescript
import { spawn } from 'node:child_process';

const result = await new Promise<CliResult>((resolve) => {
  const proc = spawn('perspectives', ['dialogue', 'turn', '--id', dialogueId, '--persona', speakerId, '--content', content]);

  let stdout = '';
  let stderr = '';

  proc.stdout.on('data', (data) => { stdout += data; });
  proc.stderr.on('data', (data) => { stderr += data; });

  proc.on('close', (code) => {
    resolve({ exitCode: code, stdout, stderr });
  });
});
```

### Exit Codes

| Code | Meaning | Switchboard Action |
|------|---------|-------------------|
| 0 | Success | Parse stdout YAML, continue dialogue |
| 1 | Validation error (VAL*) | Parse stderr YAML, surface error to user, halt dialogue |
| 2 | Storage error (STO*) | Retry once, then fail dialogue session |
| 3 | Concurrency error (CON*) | Wait 1s, retry up to 3 times, then fail |
| 4 | Migration error (MIG*) | Surface error, abort session, suggest manual recovery |
| 5+ | Unexpected error | Log stderr, abort session |

### stdout/stderr Contract

**stdout**: Always contains YAML-formatted result (success or error).

```yaml
status: success | error
# ... rest of PAGE-structured output
```

**stderr**: Debug output (if PERSPECTIVES_DEBUG set) or crash traces. Not parsed by switchboard.

### Error Handling

```typescript
// Switchboard's responsibility
async function executeDialogueTurn(dialogueId: string, speakerId: string, content: string): Promise<TurnResult> {
  const result = await executePerspectivesCli(['dialogue', 'turn', '--id', dialogueId, '--persona', speakerId, '--content', content]);

  switch (result.exitCode) {
    case 0:
      return { status: 'success', turn: parseYaml(result.stdout) };
    case 1:
      return { status: 'validation_error', error: parseYaml(result.stdout) };
    case 2:
      // Retry storage errors once
      await sleep(500);
      return executeDialogueTurn(dialogueId, speakerId, content);
    case 3:
      // Retry concurrency errors up to 3 times
      return retryWithBackoff(() => executeDialogueTurn(dialogueId, speakerId, content), 3);
    case 4:
      throw new MigrationError('Perspectives migration failed. Manual recovery needed.');
    default:
      throw new Error(`Perspectives CLI crashed: ${result.stderr}`);
  }
}
```

### Guarantees from CLI to Switchboard

1. **stdout is always valid YAML** (or empty on crash)
2. **Exit code accurately reflects error category**
3. **Dialogue state is consistent** (turn added or not added, never partial)
4. **Concurrent turn submissions are serialized** (via locking)
5. **Index is rebuilt after persona saves** (search results are eventually consistent)

### What Switchboard Must Handle

1. **Retries for transient failures** (CON*, STO*)
2. **Surfacing validation errors to user** (VAL*)
3. **Aborting session on unrecoverable errors** (MIG*, unexpected crashes)
4. **Timeout if CLI hangs** (e.g., stale lock never cleared)

## Test Plan

Test coverage across three tiers: unit, integration, regression.

### Unit Tests

**Target**: Pure functions and data structures.

| Module | Tests |
|--------|-------|
| `lib/validation.ts` | Validate persona schema (required fields, optional fields, invalid formats) |
| `lib/validation.ts` | Validate dialogue schema (participants, turns, interaction types) |
| `lib/migrations.ts` | Schema version checking (forward incompatible, backward compatible, auto-migrate) |
| `lib/migrations.ts` | Migration functions (1.0.0→1.1.0 adds resume fields) |
| `lib/persona_store.ts` | Index rebuild (add persona, remove persona, rebuild from scratch) |
| `lib/dialogue_store.ts` | Turn appending (maintains order, validates speaker) |

**Test doubles**: Mock filesystem using in-memory storage.

### Integration Tests

**Target**: End-to-end command execution with real filesystem.

| Scenario | Test |
|----------|------|
| Persona lifecycle | Save → read → list → search → update → read |
| Dialogue lifecycle | Start → turn → turn → show → end → list |
| Resume dialogue | Start → turn → end → resume → turn → end |
| Extend dialogue | Start → turn → extend → turn (new persona) |
| Concurrent saves | Two processes save different personas simultaneously |
| Lock timeout | Process A holds lock, process B waits then succeeds |
| Stale lock recovery | Simulate crash, next operation clears stale lock |
| Migration on first run | Old directory structure → run command → new structure created |
| Index rebuild on save | Save persona → verify index contains new persona |
| Invalid input handling | Each VAL* error code triggered and verified |

**Test isolation**: Use `createTestContext()` from `tests/lib/isolation.ts`.

### Regression Tests

**Target**: Invariants that must hold across all operations.

| Invariant | Test |
|-----------|------|
| Index matches filesystem | After any save, index contains exactly the personas in `.personas/` |
| Document envelope fields | All saved documents have id, schema_version, created, last_modified |
| Turn order preservation | Dialogue turns maintain insertion order |
| Participant referential integrity | All turn persona_ids exist in participants list |
| Schema version monotonicity | Migrations only increase schema_version, never decrease |
| Backup existence on migration | Migration creates backup before moving files |
| Lock cleanup | No locks remain after successful or failed operations |

### Property-Based Tests

**Target**: Invariants that hold for arbitrary inputs.

| Property | Generator | Assertion |
|----------|-----------|-----------|
| Save then read returns same data | Random valid persona YAML | `save(persona).then(() => read(id)) === persona` |
| Index rebuild is idempotent | Random set of personas | `rebuildIndex().then(() => rebuildIndex())` produces same index |
| Migration is idempotent | Random v1.0.0 document | `migrate(doc).then(() => migrate(doc))` produces same result |
| Turn count matches array length | Random dialogue with N turns | `dialogue.turns.length === N` |

**Framework**: Use `fast-check` for property-based testing (dev dependency acceptable).

### Test Coverage Targets

| Category | Target Coverage |
|----------|----------------|
| Unit tests | >90% line coverage |
| Integration tests | All commands, all success paths, all error paths |
| Regression tests | All invariants in spec |

## Global Options

Available on all commands.

```bash
perspectives --version
perspectives --help
perspectives persona --help
perspectives dialogue turn --help
```

### Version Flag

```bash
$ perspectives --version
perspectives CLI 1.0.0
```

Output format:

```yaml
version: "1.0.0"
compiled: "2025-12-21T16:00:00Z"
platform: "darwin-arm64"
```

### Help Flag

```bash
perspectives --help
```

Output:

```
perspectives - Persona management and dialogue lifecycle

USAGE:
  perspectives <command> <subcommand> [options]

COMMANDS:
  persona       Manage personas (save, read, list, search)
  dialogue      Manage dialogues (start, turn, end, show, list, resume, extend)
  doctor        Health check and repair

GLOBAL OPTIONS:
  --version     Show version information
  --help        Show this help message

ENVIRONMENT VARIABLES:
  PERSPECTIVES_DEBUG=1           Show internal state
  PERSPECTIVES_VERBOSE=1         Show detailed progress
  PERSPECTIVES_LOG_FILE=<path>   Write logs to file

EXAMPLES:
  perspectives persona save --id researcher --file persona.yaml
  perspectives dialogue start --topic "API design" --personas "backend,frontend"
  perspectives doctor --rebuild-index

For command-specific help:
  perspectives persona --help
  perspectives dialogue --help
```

Subcommand help:

```bash
$ perspectives persona --help
perspectives persona - Manage personas

USAGE:
  perspectives persona <subcommand> [options]

SUBCOMMANDS:
  save       Create or update a persona
  read       Read a persona by ID
  list       List all personas
  search     Search personas by keyword

OPTIONS:
  --help     Show this help message

EXAMPLES:
  perspectives persona save --id researcher --file persona.yaml
  perspectives persona read --id researcher --yaml
  perspectives persona list --framework empiricism
  perspectives persona search --keyword "systems thinking"
```

### Common Flags

Not all commands support all flags, but these are common across multiple commands:

| Flag | Supported By | Effect |
|------|--------------|--------|
| `--yaml` | persona read, persona list, dialogue show, dialogue list | Output raw YAML instead of formatted boxes |
| `--json` | None (v1.0.0) | Reserved for future JSON output support |
| `--quiet` | All commands | Suppress PAGE boxes, output only YAML |
| `--help` | All commands | Show command-specific help |

## Open Questions

*(None remaining for this phase.)*

## Acceptance Criteria

- [ ] All persona CRUD operations work via CLI (save, read, list, search)
- [ ] All dialogue lifecycle operations work via CLI (start, turn, end, show, list)
- [ ] All trace operations work via CLI (save, read, list, sessions, delete)
- [ ] Resume/extend per DISCOURSE spec
- [ ] PAGE protocol compliance for all output (YAML format)
- [ ] Bun compile produces working binary (~60-80MB acceptable)
- [ ] Index rebuilt on every persona save
- [ ] Directory migration from `.thinkies/.personas/` to `.thinkies/.perspectives/.personas/`
- [ ] Trace storage in `.thinkies/.perspectives/.traces/`
- [ ] Skills call compiled binary
- [ ] spawn-automaton instructs agents to call `perspectives trace save` as final action
- [ ] Collide reads traces via CLI or direct file access
- [ ] End-to-end tests: persona → automaton → trace save → collide chain
