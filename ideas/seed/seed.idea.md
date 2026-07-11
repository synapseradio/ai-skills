---
status: draft
created: 2025-01-09
---

# SEED: Catch-to-Thread Inference

**Seeds are catches that don't fit existing threads—potential patterns awaiting crystallization.**

## The Problem

The current catch system (`/catch`, `journal-catch`) has automatic thread suggestion via `suggestThreads()`. When confidence is high, catches get threaded. When confidence is low, catches go to `unthreaded` and wait.

But low confidence isn't failure—it's signal. A catch that doesn't fit existing patterns might be:

- Noise (truly unrelated)
- The beginning of something new (a seed)

The system treats both the same: dump in `unthreaded`, wait for manual review. This misses the opportunity to detect emergent patterns.

## The Insight

**Catches that don't fit threads aren't failures—they're seeds.**

A seed is a deferred inference request. It persists until an agent attends to it and forms a hypothesis about what it might become.

| Catch State | Meaning |
|-------------|---------|
| High confidence (≥0.3) | Fits existing pattern → assign thread |
| Low confidence (<0.3) | Doesn't fit → might be new territory → seed |

## Seed Lifecycle

Seeds follow a lifecycle parallel to but distinct from THREAD:

```
CATCH arrives
    │
    ▼
┌─────────────────────────────────────────────────────┐
│ suggestThreads() → confidence score                 │
└─────────────────────────────────────────────────────┘
    │                           │
    │ ≥0.3                      │ <0.3
    ▼                           ▼
┌─────────────┐           ┌─────────────┐
│   CATCH     │           │    SEED     │
│ (threaded)  │           │ (potential) │
└─────────────┘           └─────────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
              accumulate               decay/prune
              evidence                 (no evidence)
                    │
                    ▼
              ┌───────────┐
              │  MATURE   │
              │ (ready)   │
              └───────────┘
                    │
                    ▼
              ┌───────────┐
              │  SPROUT   │
              │ → THREAD  │
              └───────────┘
```

## The Five Skills

Each lifecycle phase requires agent inference, not just script execution:

| Skill | Phase | Inference Task |
|-------|-------|----------------|
| `journal-seed` | Plant | "What territory is this? Name the emerging pattern." |
| `journal-water` | Accumulate | "Which seeds does this catch strengthen?" |
| `journal-germinate` | Review | "Is this seed coherent enough to name?" |
| `journal-sprout` | Crystallize | "What thread captures this? What connects?" |
| `journal-prune` | Decay | "Dormant with potential, or dead?" |

Each skill follows: **observe → hypothesize → test → report**

Scripts handle data plumbing. Skills guide the inference.

## Relationship to THREAD

THREAD detects patterns across existing sessions. SEED detects potential for *new* patterns from catches that don't fit.

| Concept | Input | Output | Detection Method |
|---------|-------|--------|------------------|
| THREAD | Sessions, reflections, etc. | Named investigations | Keyword + graph clustering |
| SEED | Low-confidence catches | Potential threads | Accumulation + coherence |

Seeds can become threads. When a seed crystallizes (sprouts), it creates a new THREAD that the existing detection would eventually find—but seeding finds it earlier, from the catches that signaled novelty.

<!-- -(.)- | CATCH-SEED-GENERATION: Dense clusters of catches with 'connective' energy might indicate emerging threads. Surface to user: "7 catches share themes but belong to no thread. Crystallize?" Makes threads emergent from catch behavior, not imposed by detection. -->

## Technical Constraints

- **No embeddings**: TF-IDF + Jaccard similarity only (consumer hardware)
- **Sub-second latency**: Interactive use requires fast inference
- **Existing infrastructure**: Builds on `catch_threading.ts`, `suggestThreads()`, `CatchIndex`

## Highest-Leverage Intervention

**Location**: `catch.ts` line 352

**Current**:

```typescript
autoDetectedThreads = await suggestThreads(content);
threads = autoDetectedThreads.map(s => s.thread);
```

**With seed detection**:

```typescript
const SEED_THRESHOLD = 0.3;
autoDetectedThreads = await suggestThreads(content);
const confident = autoDetectedThreads.filter(s => s.confidence >= SEED_THRESHOLD);

if (confident.length > 0) {
  // High confidence: normal catch flow
  threads = confident.map(s => s.thread);
} else if (autoDetectedThreads.length > 0) {
  // Low confidence suggestions exist: this is a SEED
  markAsSeed(catchId, autoDetectedThreads);
} else {
  // No suggestions at all: also a seed (truly novel)
  markAsSeed(catchId, []);
}
```

## Robustness Requirements

From expert consultation (PKM systems research):

1. **Temporal triggers**: When does each phase run?
2. **Feedback loops**: User actions adjust thresholds over time
3. **Cold start**: Different behavior for first 50-100 catches
4. **Confidence modeling**: Every seed has explicit confidence
5. **Multi-signal similarity**: Lexical (0.6) + temporal (0.2) + tags (0.1) + feedback (0.1)
6. **Archive, don't delete**: Allow resurrection of pruned seeds

### Failure Modes to Prevent

- **Seed explosion**: Too many seeds, none crystallize
- **Premature thread lock-in**: Early weak thread attracts future catches
- **False negative decay**: Slow-emerging patterns pruned too early
- **"Everything relates"**: User voice creates false lexical similarity

## Cross-References

### Repository

- [[ideas/THREAD-journalistic-threads]] — THREAD concept (seeds feed into this)
- [[specs/THREAD-design]] — THREAD architecture
- [[specs/SEED-lifecycle]] — Seed lifecycle specification (this doc's spec)
- [[plugins/journal/lib/catch_threading.ts]] — Existing inference infrastructure
- [[plugins/journal/skills/journal-catch]] — Current catch skill

### Journal Sessions

- [[thread-inference-design]] — Design session (2025-12-11)
- [[journalistic-thread-ideation]] — Original THREAD ideation
- [[thread-harvest-decompose]] — Thread decomposition work

### External Research

- PKM at scale: automation reduces friction, not creates burden
- Active learning: user feedback improves thresholds
- Cold start problem: bootstrapping strategies for sparse data
