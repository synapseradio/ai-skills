# /research Functional Specification

## Overview

The `/research` command provides structured, integrity-preserving investigation of topics. It orchestrates multi-phase research through specialized agents while maintaining explicit tracking of the gap between claims and evidence.

## Command Interface

```
/research <topic> [--depth quick|standard|deep] [--continue <session-id>]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `topic` | Yes | The research question or topic to investigate |
| `--depth` | No | Research depth mode (default: standard) |
| `--continue` | No | Resume a prior research session |

### Depth Modes

| Mode | Agents | Duration | Use Case |
|------|--------|----------|----------|
| quick | 3 | ~15 min | Time-bounded questions, initial exploration |
| standard | 6 | ~45 min | Full investigation with reconciliation |
| deep | 8+ | Multi-session | High-stakes questions where being wrong is expensive |

## Execution Flow

### Phase 1: Belief Inventory

**Agent**: `research-beliefs`

**Purpose**: Surface prior expectations before evidence gathering

**Skills invoked**:

- `assess-current-knowledge` — Inventory existing beliefs
- `question-through-dialogue` — Question assumptions
- `premortem` — Detect overconfidence (standard/deep only)

**Output**:

```yaml
beliefs:
  prior_expectations:
    - expectation: string
      basis: string
      confidence: float
  assumptions_surfaced: [string]
  confidence_before_evidence: float
  blind_spots_flagged: [string]
```

### Phase 2: Evidence Collection

**Agent**: `research-collection`

**Purpose**: Gather diverse sources with quality documentation

**Skills invoked**:

- `wonder` — Explore evidence space
- `consider-alternatives` — Generate diverse pathways
- `cite-sources` — Document provenance

**Output**:

```yaml
evidence:
  sources_consulted: int
  sources_cited:
    - source: string
      type: enum
      methodology: string
      quality_notes: string
      key_claims: [...]
  gaps_identified: [string]
  diversity_assessment: {...}
```

### Phase 3: Evidence Evaluation

**Agent**: `research-evaluation`

**Purpose**: Assess convergence, divergence, and saturation

**Skills invoked**:

- `evaluate-evidence` — Assess claim support
- `detect-diminishing-returns` — Determine if more evidence needed
- `audit-chain-of-thought` — Trace reasoning chains

**Output**:

```yaml
evaluation:
  convergence: [...]
  divergence: [...]
  saturation_status: enum
  quality_gradient: {...}
  inference_risks: [...]
```

**Human Checkpoint**: Present evaluation summary. User confirms proceed or adjusts direction.

### Phase 4a: Support/Attack Analysis

**Agent**: `research-reconcile-support`

**Purpose**: Build dual-perspective cases for contested claims

**Skills invoked**:

- `trace-logical-justifications` — Follow supporting reasoning
- `ask-what-breaks` — Seek undermining evidence
- `argue-opposite` — Consider opposing perspective

**Output**:

```yaml
reconciliation_support_attack:
  claims_analyzed:
    - claim: string
      supporting_case: {...}
      attacking_case: {...}
      tension_points: [string]
```

### Phase 4b: Judgment

**Agent**: `research-reconcile-judgment`

**Purpose**: Render calibrated verdicts on contested claims

**Skills invoked**:

- `probe-boundaries` — Test edge conditions
- `calibrate-confidence` — Calibrate certainty
- `synthesize-opposing-views` — Navigate competing positions

**Output**:

```yaml
reconciliation_judgment:
  judgments:
    - claim: string
      verdict: enum
      confidence: float
      reasoning: string
      boundary_conditions: [string]
  confidence_trajectory: {...}
```

**Human Checkpoint** (deep mode only): Present reconciliation summary before synthesis.

### Phase 5: Synthesis

**Agent**: `research-synthesis`

**Purpose**: Produce coherent findings with gap visibility

**Skills invoked**:

- `check-soundness` — Ensure consistency
- `integrate-other-perspectives` — Combine findings
- `cite-sources` — Ground claims

**Output**:

```yaml
synthesis:
  findings:
    - finding: string
      confidence: float
      evidence_basis: string
  gap_visibility:
    claims_made: int
    claims_supported: int
    claims_contested: int
    claims_unsupported: int
  limitations: [string]
  implications: {...}
```

## State Management

### Session Persistence

Research sessions persist to journal:

- Session notes: `.claude/.thinkies/.notes/research-{session-id}.yaml`
- Phase outputs: Appended to session notes as phases complete
- Working memory: Available for cross-session continuation

### State Transfer

Each phase receives accumulated state from prior phases:

```yaml
research_state:
  meta:
    topic: string
    session_id: string
    depth: enum
    phase_completed: int
    journal_path: string
  phases:
    beliefs: {...}
    evidence: {...}
    evaluation: {...}
    reconciliation_support_attack: {...}
    reconciliation_judgment: {...}
  gap_summary:
    claims_made: int
    claims_supported: int
    claims_contested: int
    claims_unsupported: int
    confidence_trajectory: [...]
  stopping:
    saturation_reached: bool
    coverage_complete: bool
    confidence_calibrated: bool
    should_continue: bool
```

## Stopping Criteria

Research concludes when any condition is met:

| Criterion | Check | Implementation |
|-----------|-------|----------------|
| Saturation | New sources confirm without adding | `detect-diminishing-returns` skill |
| Coverage | All question aspects addressed | Phase 3 evaluation output |
| Calibration | Confidence matches evidence | Phase 4b judgment output |
| Time bounds | Mode-appropriate limit reached | Orchestrator tracking |

**Principle**: Research stops when the gap between evidence and claim is visible enough for external evaluation—not when confidence feels high.

## Quick Mode Behavior

Quick mode (3 agents) provides integrity-preserving research under time constraints:

```
Agent 1: Beliefs (minimal) → assess-current-knowledge, question-through-dialogue
Agent 2: Evidence (minimal) → wonder, cite-sources
Agent 3: Synthesis → evaluate-evidence, calibrate-confidence, integrate-other-perspectives
```

Skips deep reconciliation but preserves:

- Belief surfacing before evidence
- Source citation with quality notes
- Confidence calibration in synthesis
- Gap visibility in output

## Continuation Behavior

When `--continue <session-id>` is provided:

1. Load prior state from journal
2. Determine last completed phase
3. Resume from next phase
4. Preserve accumulated state

For multi-session deep research:

- Journal working memory maintains context
- Each session advances phases
- Final synthesis integrates all prior work

## Error Handling

| Condition | Behavior |
|-----------|----------|
| No sources found | Report gap, proceed with available evidence |
| Phase timeout | Save partial state, allow continuation |
| Agent failure | Retry once, then surface for human decision |
| Contradictory state | Flag for human review before proceeding |

## Output Format

Final research output:

```yaml
research_complete:
  topic: "..."
  depth: standard
  session_id: "..."

  executive_summary: "..."

  findings:
    - finding: "..."
      confidence: 0.85
      evidence_basis: "..."
      citations: [...]

  gap_visibility:
    claims_made: 5
    claims_supported: 3
    claims_contested: 1
    claims_unsupported: 1

  belief_update:
    prior_confidence: 0.7
    posterior_confidence: 0.72
    key_changes: [...]

  limitations: [...]

  open_threads: [...]

  session_artifacts:
    notes: ".claude/.thinkies/.notes/research-{id}.yaml"
    phases: [phase output paths]
```

## Dependencies

- **switchboard plugin**: Agent coordination infrastructure
- **journal plugin**: Session persistence and working memory
- **thinkies plugin**: Skills invoked by research agents

## Related

- `ideas/research-command-design.md` — Design exploration
- `plugins/switchboard/commands/research.md` — Implementation
- `plugins/switchboard/schemas/research-state.yaml` — State schema
