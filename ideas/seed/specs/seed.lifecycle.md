# SEED Lifecycle Specification

This document specifies the architecture and data model for the seed-to-thread inference system.

## Overview

Seeds are catches with low thread-match confidence that may represent emerging patterns. The seed lifecycle tracks potential patterns through accumulation, maturation, and crystallization into threads.

## Design Principles

### 1. Seeds Are Deferred Inference Requests

A seed persists until an agent attends to it. The seed's open question—"what might this become?"—drives inference at each lifecycle phase.

### 2. Scripts Handle Plumbing, Skills Guide Inference

Deterministic scripts manage data: storage, indexing, threshold checks. Skills instruct agents on *what to infer*: pattern naming, coherence assessment, connection discovery.

### 3. Consumer Hardware Constraint

No embeddings. All similarity uses TF-IDF keyword extraction + Jaccard coefficient. Operations complete in <1s for interactive use.

### 4. Feedback Improves Accuracy

User actions (manual threading, seed rejection, thread splitting) adjust thresholds over time. The system learns the user's notion of relatedness.

## Data Model

### Seed Schema

```yaml
# .claude/.thinkies/.seeds/<seed-id>.yaml
id: "019b0d3c-..."                    # UUIDv7
content: "The original catch content"
status: seed | maturing | ready | sprouted | expired

# Detection metadata
detection:
  triggered_at: "2025-12-11T10:00:00Z"
  suggestions: []                      # ThreadSuggestion[] that were below threshold
  max_confidence: 0.22                 # Highest suggestion confidence
  keywords: ["distributed", "systems", "architecture"]

# Accumulation tracking
evidence:
  count: 0                             # Catches that strengthened this seed
  catch_ids: []                        # References to evidence catches
  last_evidence_at: null               # ISO timestamp

# Lifecycle timing
lifecycle:
  planted_at: "2025-12-11T10:00:00Z"
  maturation_window_days: 30           # How long to accumulate before expiry
  evidence_threshold: 3                # Evidence needed for 'ready' status

# Confidence and decay
confidence:
  current: 0.22                        # Detection confidence
  coherence: null                      # Set during germination review (0-1)

# If sprouted
sprouted:
  thread_id: null                      # Thread created from this seed
  sprouted_at: null

metadata:
  schema_version: "1.0.0"
```

### Seed Index

```yaml
# .claude/.thinkies/.seeds/_index.yaml
by_status:
  seed: ["seed-001", "seed-002"]
  maturing: ["seed-003"]
  ready: ["seed-004"]
  sprouted: ["seed-005"]
  expired: ["seed-006", "seed-007"]

by_keyword:
  distributed: ["seed-001", "seed-003"]
  architecture: ["seed-001", "seed-002"]
  testing: ["seed-004"]

stats:
  total: 7
  active: 4                            # seed + maturing + ready
  sprouted: 1
  expired: 2
  last_planted: "2025-12-11T10:00:00Z"
  last_germination_review: "2025-12-10T00:00:00Z"
```

### Catch Schema Extension

```yaml
# Extension to CatchData in catch.ts
interface CatchData {
  // ... existing fields ...

  seed_status?: {
    is_seed: boolean;
    seed_id?: string;                  # If this catch became a seed
    strengthens?: string[];            # Seed IDs this catch provides evidence for
  };
}
```

## State Machine

```
                         ┌─────────────────────────────────────┐
                         │                                     │
    CATCH arrives        │                                     │
         │               │                                     │
         ▼               │                                     │
  ┌─────────────┐        │                                     │
  │ confidence  │        │                                     │
  │   check     │        │                                     │
  └──────┬──────┘        │                                     │
         │               │                                     │
    ┌────┴────┐          │                                     │
    │         │          │                                     │
  ≥0.3      <0.3         │                                     │
    │         │          │                                     │
    ▼         ▼          │                                     │
 THREAD    ┌──────┐      │                                     │
 (normal)  │ SEED │      │                                     │
           │      │◄─────┼─── new catch, no fit                │
           └──┬───┘      │                                     │
              │          │                                     │
              │ evidence arrives                               │
              │ (catch strengthens seed)                       │
              ▼          │                                     │
         ┌─────────┐     │                                     │
         │MATURING │     │                                     │
         │         │─────┼─── more evidence ───────────────────┘
         └────┬────┘     │
              │          │
              │ evidence_count ≥ threshold
              │ within maturation_window
              ▼
         ┌─────────┐
         │  READY  │
         │         │
         └────┬────┘
              │
              │ germination review
              │ agent assesses coherence
              ▼
         ┌─────────┐     ┌─────────┐
         │ SPROUT  │────►│ THREAD  │
         │         │     │ created │
         └─────────┘     └─────────┘

         ─────────────────────────────────────────────

         DECAY PATH (no evidence, time passes):

         SEED ──────► EXPIRED (maturation_window exceeded)
         MATURING ──► EXPIRED (maturation_window exceeded)
```

## Skills Specification

### journal-seed (Plant)

**Trigger**: Catch saved with confidence < threshold

**Observation**:

- The catch content
- Existing thread keywords
- Existing seed keywords

**Hypothesis**: "This catch represents new territory: [inferred name]"

**Test**:

- Jaccard similarity to existing threads < 0.3
- Jaccard similarity to existing seeds: if > 0.5, it's evidence not new seed

**Report**:

```
Planting seed: "[inferred-name]"
Confidence: 22%
Nearest existing: "architecture" thread at 28% similarity
Keywords: distributed, systems, architecture
```

**Artifacts**: Creates seed file, updates index

---

### journal-water (Accumulate)

**Trigger**: Catch saved, seeds exist

**Observation**:

- New catch content and keywords
- All active seeds (seed + maturing status)

**Hypothesis**: "This catch provides evidence for seed(s): [names]"

**Test**:

- Keyword overlap (Jaccard) with each seed
- Temporal proximity (same session = stronger signal)
- Explicit keyword match (catch mentions seed-related terms)

**Report**:

```
This catch strengthens:
  - "distributed-systems" seed (now 3 evidence, 65% confidence)
  - "architecture-patterns" seed (weak signal, 1 evidence)
```

**Artifacts**: Updates seed evidence arrays, may transition seed → maturing

---

### journal-germinate (Review)

**Trigger**: Seeds with status = ready, or manual invocation

**Observation**:

- All ready seeds
- Evidence catches for each
- Existing threads (to check for overlap)

**Hypothesis**: "Seed X has accumulated coherent evidence for thread creation"

**Test**:

- Evidence coherence: Do catches share keywords beyond the seed's original?
- Temporal pattern: Burst (strong) vs. scattered (weaker)?
- Narrative coherence: Can agent summarize what this is "about"?

**Report** (per seed):

```
Seed: "distributed-systems"
Status: ready (4 evidence pieces)
Coherence: HIGH (catches share: consistency, partitioning, CAP)
Temporal: Moderate (spread over 12 days)
Summary: "Exploration of distributed systems concepts, particularly
         consistency models and CAP theorem implications"

Recommendation: SPROUT → create thread "distributed-systems-exploration"
```

**Artifacts**: Updates seed coherence score, surfaces recommendations

---

### journal-sprout (Crystallize)

**Trigger**: User approves germination recommendation, or manual invocation

**Observation**:

- Seed marked ready with coherence assessment
- Evidence catches
- Existing threads (for connection discovery)

**Hypothesis**: "This seed should become thread [name] connecting to [existing threads]"

**Test**:

- Thread name: Synthesize from seed keywords + evidence keywords
- Description: Summarize evidence catches
- Connections: Which existing threads share keywords?

**Report**:

```
Creating thread: "distributed-systems-exploration"
Description: "Investigation of distributed systems concepts including
             consistency models, CAP theorem, and partition tolerance"

Connecting to:
  - "architecture-patterns" (shared: architecture, systems)
  - "database-design" (shared: consistency)

Founding members: 4 catches assigned
Seed status: sprouted
```

**Artifacts**: Creates THREAD, assigns catches, marks seed sprouted

---

### journal-prune (Decay)

**Trigger**: Scheduled (weekly) or manual invocation

**Observation**:

- All seeds past maturation window
- Seeds with no recent evidence
- Similar seed pairs (potential merge)

**Hypothesis**: "Seed X should [expire / merge with Y / remain dormant]"

**Test**:

- Time since last evidence > maturation_window → expire candidate
- Jaccard similarity to other seeds > 0.6 → merge candidate
- Recent keyword activity elsewhere → revival signal

**Report**:

```
Decay analysis:

EXPIRE (no evidence, window exceeded):
  - "random-thought-123" (45 days, 0 evidence)

MERGE CANDIDATES (high overlap):
  - "api-design" + "endpoint-patterns" (72% overlap)

REVIVAL SIGNALS (recent related activity):
  - "testing-patterns" (keyword "testing" appeared 3x this week)
```

**Artifacts**: Expires seeds (archived, not deleted), merges if approved

## Maturity Stages (Cold Start)

The system behaves differently based on catch volume:

### Stage 1: Bootstrap (catches 1-50)

- **No automatic seeding**: Insufficient vocabulary for meaningful TF-IDF
- **Suggest temporal groupings**: "Catches from this session"
- **Collect user thread assignments**: Build vocabulary and baseline

### Stage 2: Learning (catches 51-200)

- **Enable seeding**: High threshold (0.4+ confidence for threading)
- **Frequent review**: Surface seeds for manual assessment
- **Build IDF weights**: Vocabulary stabilizes

### Stage 3: Full Auto (200+ catches)

- **Standard thresholds**: 0.3 confidence boundary
- **Automatic lifecycle**: Seeds mature and ready without manual trigger
- **Infrequent review**: Monthly germination assessment

## Threshold Adaptation

User actions adjust thresholds via feedback loop:

| User Action | Signal | Adjustment |
|-------------|--------|------------|
| Manual thread assignment to catch | Algorithm was too conservative | Increase confidence weight for those keywords |
| Reject seed suggestion | Algorithm created false positive | Decrease confidence for that keyword cluster |
| Merge two seeds | Threshold too conservative | Reduce similarity threshold |
| Split thread | Threshold too aggressive | Increase similarity threshold |

Feedback stored in:

```yaml
# .claude/.thinkies/.seeds/_feedback.yaml
adjustments:
  - timestamp: "2025-12-11T10:00:00Z"
    action: "manual_thread_assign"
    catch_id: "catch-123"
    thread: "architecture"
    keywords_boosted: ["design", "patterns"]

  - timestamp: "2025-12-10T15:00:00Z"
    action: "seed_rejected"
    seed_id: "seed-456"
    keywords_dampened: ["the", "and"]  # Stopword leak

threshold_history:
  - date: "2025-12-01"
    seed_threshold: 0.3
  - date: "2025-12-11"
    seed_threshold: 0.28  # Adjusted based on feedback
```

## Multi-Signal Similarity

Don't rely solely on lexical similarity:

```typescript
function calculateRelatedness(catch: Catch, seed: Seed): number {
  const lexical = jaccardSimilarity(catch.keywords, seed.keywords);
  const temporal = temporalProximity(catch.timestamp, seed.planted_at);
  const tags = tagOverlap(catch.threads, seed.keywords);
  const feedback = feedbackAdjustment(catch.keywords, seed.keywords);

  return (
    0.6 * lexical +
    0.2 * temporal +
    0.1 * tags +
    0.1 * feedback
  );
}

function temporalProximity(t1: string, t2: string): number {
  const hoursDiff = Math.abs(new Date(t1) - new Date(t2)) / (1000 * 60 * 60);
  if (hoursDiff < 1) return 1.0;      // Same hour
  if (hoursDiff < 24) return 0.8;     // Same day
  if (hoursDiff < 168) return 0.5;    // Same week
  return 0.2;                          // Older
}
```

## Directory Structure

```
plugins/journal/
├── lib/
│   ├── seed_store.ts           # YamlStore<Seed> operations
│   ├── seed_detection.ts       # Seed creation from low-confidence catches
│   ├── seed_evidence.ts        # Evidence accumulation logic
│   ├── seed_maturation.ts      # Lifecycle transitions
│   └── seed_feedback.ts        # Threshold adaptation
│
├── skills/
│   ├── journal-seed/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── plant_seed.ts
│   │
│   ├── journal-water/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── accumulate_evidence.ts
│   │
│   ├── journal-germinate/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── review_seeds.ts
│   │
│   ├── journal-sprout/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── crystallize_thread.ts
│   │
│   └── journal-prune/
│       ├── SKILL.md
│       └── scripts/
│           └── decay_seeds.ts
│
└── .claude/.thinkies/
    └── .seeds/
        ├── _index.yaml
        ├── _feedback.yaml
        └── <seed-id>.yaml
```

## Integration with THREAD

When a seed sprouts, it creates a THREAD:

```typescript
async function sproutSeed(seedId: string, threadName: string): Promise<Thread> {
  const seed = await seedStore.read(seedId);

  // Create thread from seed
  const thread = await threadStore.create({
    name: threadName,
    status: 'active',
    members: {
      sessions: [],  // Will be populated from evidence catches
      catches: seed.evidence.catch_ids,
    },
    seed_entry: {
      type: 'seed',
      id: seedId,
    },
    detection: {
      method: 'seed_crystallization',
      confidence: seed.confidence.coherence,
      keywords: seed.detection.keywords,
    },
  });

  // Mark seed as sprouted
  await seedStore.update(seedId, {
    status: 'sprouted',
    sprouted: {
      thread_id: thread.id,
      sprouted_at: new Date().toISOString(),
    },
  });

  return thread;
}
```

## Cross-References

### Repository

- [[ideas/SEED-catch-inference]] — Concept overview (this spec's idea doc)
- [[ideas/THREAD-journalistic-threads]] — THREAD concept
- [[specs/THREAD-design]] — THREAD architecture
- [[plugins/journal/lib/catch_threading.ts]] — Existing `suggestThreads()` infrastructure
- [[plugins/journal/skills/journal-catch]] — Catch skill to extend

### Journal Sessions

- [[thread-inference-design]] — Design session with expert consultation
- [[journalistic-thread-ideation]] — Original THREAD ideation

### Research Grounding

- PKM systems: automation must reduce friction, not create maintenance burden
- Active learning: user feedback improves threshold calibration
- Cold start: bootstrapping behavior for sparse initial data
- Silhouette coefficient: cluster quality measurement without embeddings
