# Proposal: Topic Evolution System

**Status**: Proposed
**Author**: Claude (journal-topics-exploration session)
**Date**: 2026-01-07

## Problem Statement

The journal system has two overlapping organizational primitives—**threads** and **topics**—neither of which has seen meaningful adoption:

| Primitive | Infrastructure | Actual Usage |
|-----------|---------------|--------------|
| **Threads** | Complete (TF-IDF detection, 4-state lifecycle, multi-type membership, decay) | Zero adoption |
| **Topics** | Minimal (static YAML files, 1 test entry) | Zero adoption |

**Root cause**: Both suffer from the same disease—**invisibility**. Agents don't encounter threads or topics during normal workflow. Nothing surfaces them at session start. Nothing suggests them during writes. They exist but remain undiscovered.

Additionally:

- **InsightData** uses `tags: string[]` while other entity types use `topics: string[]`
- Topics have no temporal dimension—they're snapshots, not timelines
- No provenance tracking—the system can't answer "who said what when about this topic"

## Proposed Solution

Unify tags and topics into a single **topic** concept with temporal evolution tracking:

1. **Unify tags → topics**: Eliminate the distinction. Tags become topic references.
2. **Add temporal dimension**: Track `first_seen`, `last_seen`, and individual mentions with timestamps
3. **Track provenance**: Each mention records session, agent, and context
4. **Surface at workflow entry points**: Session-start hook shows active topics

### Design Principles

| Principle | Implication |
|-----------|-------------|
| **Topics are graph nodes** | Same storage/linking pattern as sessions, insights, catches |
| **Bidirectional links** | Every entity type supports `topic ↔ entity` relationships |
| **Newest-first ordering** | Current state first; trace backward to understand evolution |
| **CLI shows relations, LLM infers meaning** | No evolution computation in deterministic code |
| **KISS** | No embeddings, no topic merging, heuristic significance via fuzzy search |

### What Changes

| Component | Current | Proposed |
|-----------|---------|----------|
| **InsightData** | `tags: string[]` | Add `topics: string[]`, deprecate tags |
| **TopicData** | Static (name, description, related_topics) | Add `first_seen`, `last_seen`, `aliases`, `mention_count` |
| **Topic storage** | Directory scan on every query | Add `.topics/_index` for fast lookup |
| **Session-start hook** | Shows threads (unused) | Add active topics section |
| **Note write** | No topic awareness | Auto-suggest topics from content |

## Data Model Design

### Extended TopicData

```typescript
interface TopicData {
  readonly name: string;
  readonly description: string;
  readonly related_topics: readonly string[];
  readonly created: string;
  readonly first_seen: string;      // NEW: First mention timestamp
  readonly last_seen: string;       // NEW: Most recent mention
  readonly aliases: readonly string[]; // NEW: For identity management
  readonly mention_count: number;   // NEW: Entry count
}
```

### TopicMention (New)

```typescript
interface TopicMention {
  readonly timestamp: string;
  readonly content_type: MentionContentType;
  readonly entry_id: string;
  readonly provenance: MentionProvenance;
  readonly significance: MentionSignificance;
}

interface MentionProvenance {
  readonly session: string;  // Session name or empty
  readonly agent: string;    // Agent identifier or empty
  readonly context: string;  // Brief surrounding text or empty
}
```

### Topic Index

Following the thread `_index` pattern:

```yaml
# .topics/_index
topics:
  by_entry:
    "session:auth-fix": ["authentication", "security"]
    "insight:jwt-refresh": ["authentication"]
  by_topic:
    authentication: ["session:auth-fix", "insight:jwt-refresh"]
last_updated: "2026-01-07T12:00:00Z"
```

## Query Patterns

### Timeline Query

```bash
journal read topic timeline authentication --limit 10 --since 7d
```

Returns newest-first entries with provenance:

```
Topic: authentication (first seen: 2025-12-15, last seen: 2026-01-07, 12 mentions)

[2026-01-07] note from auth-review (agent: opus-4)
  "Reconsidering — refresh token rotation is complex..."

[2026-01-03] catch
  "What if we used signed cookies instead of JWT for web?"

[2025-12-22] note from api-design
  "Decided on short-lived JWT with refresh tokens..."
```

### Visibility at Session Start

```
Active topics (by recent activity):
  authentication (7 mentions, last: 2h ago)
  api-design (12 mentions, last: 1d ago)
  performance (3 mentions, last: 3d ago)
```

### Auto-Suggest on Write

On note writes, the system fuzzy-matches content against topic names/descriptions:

```
Note recorded. Suggested topics: authentication, security
Add with: journal write topic link <topic> <entry-id>
```

## Migration Path

1. **Tag migration script**: Scan `.insights/*.yaml`, create topics from unique tags
2. **Dual-write period**: Insight write populates both `tags` and `topics`
3. **Deprecation**: Mark `tags` field deprecated after migration complete

## Decision Criteria

### Accept If

- [ ] Topics appear at session start without explicit query
- [ ] `journal read topic timeline X` returns temporally-ordered entries
- [ ] Provenance tracking enables "who said what when" queries
- [ ] Migration script is idempotent (safe to run multiple times)
- [ ] No regression in existing journal operations

### Reject If

- [ ] Implementation requires embeddings or ML inference
- [ ] Topic evolution requires computation in deterministic code
- [ ] Migration corrupts existing insight data
- [ ] Session-start hook becomes noticeably slower

## Implementation Phases

1. **Design & Documentation** — This proposal, ADR, data model reference
2. **Type System Changes** — Extend TopicData, add TopicMention types
3. **Tag → Topic Migration** — Script and insight write updates
4. **Timeline Query** — New CLI command with PAGE output
5. **Provenance Tracking** — Capture session/agent/context on writes
6. **Integration & Visibility** — Session-start hook, auto-suggest

## Related Sessions

- `[[thread-inference-design]]` — Original SEED concept for threads
- `[[prerelease-harvest-thread-inference]]` — Harvest revealing visibility as root cause
- `[[journal-topics-exploration]]` — Investigation leading to this proposal

## Evidence

### Thread Investigation (2025-12-11)

> "Catches without clean thread matches are not failures—they are SEEDS. A seed is something that does not fit existing patterns, therefore it may be the beginning of a new pattern."

Key insight: The infrastructure exists but nothing triggers adoption.

### Topic Implementation Review (2026-01-07)

> "TopicData is minimal (name, description, related_topics, created). Storage is static .topics/{name}.yaml. No temporal tracking—topics are snapshots not timelines."

Key insight: Topics lack the temporal dimension needed for evolution tracking.

### Visibility Analysis (2026-01-07)

> "Both suffer from the same disease—visibility, not concept, is the problem."

Key insight: Threads and topics fail for the same reason. Solving visibility solves adoption.
