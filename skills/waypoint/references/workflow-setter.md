# Waypoint Setter Workflow

A placement workflow that traces distributed processes across files and leaves
navigational markers. Given a direction, discover the full graph autonomously.

## Input

A direction — a description of the process or pipeline to trace. Examples:
- "trace the sourcemap upload process from CI to deployment"
- "map how RELEASE version propagates through the build"
- "add waypoints for the authentication flow from login to session creation"

A pipeline name may also be provided. If omitted, derive one from the process
description (lowercase, hyphenated, concise).

## Tracing Process

1. **Seed discovery:** Use Grep and Glob to find entry points related to the described process. Look for config files, scripts, environment variables, imports, and references that connect files.
2. **Follow the thread:** Read each candidate file. Look for:
   - References to other files (imports, script calls, Dockerfile COPY/RUN, Helm templates)
   - Shared values that flow between files (env vars, build args, version strings)
   - Execution ordering clues (CI step sequences, Docker build stages, pipeline triggers)
3. **Build the graph:** Map which files feed into which. Identify:
   - **Flow nodes** (`←`/`→`): files in the execution chain
   - **Reference sinks** (`◁`/`▷`): files that consume values at runtime without being part of the build/deploy sequence
4. **Confirm completeness:** Before placing anything, verify the full path from entry to exit. If uncertain about a node's role, read the file.

## ID Generation

Generate waypoint IDs using the skill's script. Paths must be relative to git root:

```bash
bun run <skill-path>/scripts/waypoint-id.ts <path> [path...]
```

Each ID is the first 8 hex chars of SHA-256 of the relative path. Generate all IDs
in a single batch call.

## Placement

### Manifest

Write to `.ai/waypoints/<pipeline-name>.md`:

```markdown
# <pipeline-name>

<Single sentence describing the full flow — what it does and why, naming
each major stage so a reader who has never seen this pipeline can understand
its shape and purpose at a glance.>

| Waypoint   | File                        | Role                    |
|------------|-----------------------------|-------------------------|
| `<id>`     | <path relative to git root> | <role>                  |

## Topology

<ASCII graph using → for flow and ◁ for reference relationships>
```

The opening sentence is the most important line in the manifest. Write it as
a single sentence that walks through the pipeline's stages in order, naming
what happens at each stage and why it matters. Apply the "so that…" test.

Order the table by execution sequence. Sinks go last.

### Per-File Comment Blocks

Place a comment block in each file using its native comment syntax. Frame with
`──` delimiters. Two closing lines orient first-time readers: a legend explaining
the arrow symbols, and a search hint.

```
── Waypoint <id> ── <pipeline-name> ──────────────────────
   <this file's role — verb-first, active voice, with purpose>
   ← <id>  <path> — <predecessor's role>
   → <id>  <path> — <successor's role>
   Map: .ai/waypoints/<pipeline-name>.md
── ← from · → into
── search any ID to trace this pipeline across files.
```

Use `◁`/`▷` instead of `←`/`→` for reference relationships (sinks). Expand
the legend to include all symbols present in the block.

**Placement rules:**
- Top of file for configs, scripts, manifests, and pipeline-specific files
- Above the relevant code section for source files where the pipeline touches a specific function or block
- Respect the file's native comment syntax

### Branching

When a node has multiple successors or predecessors, include multiple `→` or `←`
lines in the block.

## Output Format

After placing all waypoints, report:

```markdown
## <pipeline-name>

<description>

| Waypoint | File | Role |
|----------|------|------|
| `<id>`   | <path> | <role> |

### Topology

<graph>

### Changes

- Created: `.ai/waypoints/<name>.md`
- Modified: <list of files where comment blocks were placed>
```

## Writing Voice

Before writing role and relationship descriptions, read the voice guide at
`references/waypoint-voice.md`. Apply its principles: concrete over abstract,
active over passive, orient-first, purpose over mechanics, self-evident,
warm over telegraphic. Every description should be clear to someone encountering
waypoints for the first time, and every action should carry its reason.

After placement completes, the caller **must** spawn a scribe subagent using
the scribe workflow (`references/workflow-scribe.md`) to polish all placed
descriptions. This is not optional — every setter run is followed by a scribe
pass.

## Constraints

- Waypoint IDs are deterministic from file paths — always use the script, never invent IDs
- Every ID in the manifest must appear as a comment block in exactly one file
- Every comment block must reference the manifest path
- When updating an existing pipeline, read the current manifest first and preserve existing waypoints that are still valid
- Do not modify code logic — only add or update comment blocks
- Role descriptions: verb-first, active voice, with purpose ("so that…"), under 80 characters
- Relationship descriptions: verb-first from the neighbor's perspective, under 60 characters
- Manifest opening sentence: single sentence walking through the full flow with purpose at each stage
