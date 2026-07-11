# TraversableContent Interface Specification

Interface design for unified content traversal across all journal content types.

**Thread**: journal-data-model-alignment
**Date**: 2025-12-11
**Status**: Design complete

## Summary

The common abstraction across content types is not entries—it is **traversable content**. Each content type provides:

1. **Identifier**: How to reference this content
2. **Extractable text**: For keyword analysis
3. **Discoverable links**: For graph analysis

## Content Type Survey

| Content Type | Has Entries | Text Source | Link Source | Identifier Field |
|-------------|-------------|-------------|-------------|------------------|
| Sessions (`.notes`) | Yes: `data.entries[]` | `entries[].notes` | `entries[].links` | `data.session_id` |
| Reflections (`.reflections`) | No | `data.reflection.*` | wikilinks in text | `data.session_id` |
| Personas (`.personas`) | No | `data.expertise_domain`, etc. | None | `data.persona_id` |
| Dialogues (`.dialogues`) | No | `data.turns[].content` | None | `data.dialogue_id` |
| Contexts (`.context`) | No | `data.context.*` | None | `data.session_id` |
| Catches (`.catches`) | No | `data.content` | `data.threads` | `data.id` |
| Insights (`.insights`) | No | `data.content`, `data.title` | `data.tags` | filename |
| Threads (`.threads`) | Index only | N/A | N/A | N/A |

## Core Interface

```typescript
/**
 * Content that can be traversed for THREAD detection and graph analysis.
 *
 * This interface abstracts over the structural differences between content types.
 * Each content type implements TraversableContent differently based on how it
 * stores its semantic content.
 *
 * Design rationale:
 * - `identifier` is always present and required for referencing
 * - `text` returns concatenated extractable text for TF-IDF analysis
 * - `links` returns explicit outbound references (wikilinks, thread associations, tags)
 * - `variant` enables type-safe narrowing when content-specific fields are needed
 *
 * This is NOT a normalized data format—it is a view interface. The underlying
 * data retains its original structure; TraversableContent describes what can
 * be queried from it.
 */
interface TraversableContent {
  /**
   * Content type discriminator for type-safe narrowing.
   */
  readonly variant: ContentVariant;

  /**
   * Unique identifier for this content within its type.
   *
   * For sessions: session_id
   * For reflections: session_id (reflection about that session)
   * For personas: persona_id
   * For dialogues: dialogue_id
   * For contexts: session_id (working memory for that session)
   * For catches: UUIDv7 id
   * For insights: filename (no explicit id in data)
   *
   * Combined with variant, produces EntryReference: `${variant}:${identifier}`
   */
  readonly identifier: string;

  /**
   * ISO 8601 timestamp when content was created.
   */
  readonly created: string;

  /**
   * Concatenated extractable text for keyword analysis.
   *
   * Returns all semantically meaningful text from the content, excluding:
   * - ISO 8601 timestamps
   * - UUIDs and technical identifiers
   * - Schema metadata
   *
   * Lazily computed on first access and cached.
   */
  readonly text: string;

  /**
   * Explicit outbound links from this content.
   *
   * Returns empty array when no links exist or content type has no link mechanism.
   */
  readonly links: readonly string[];

  /**
   * Original data preserved for content-specific access.
   *
   * Type is narrowed when variant is narrowed.
   */
  readonly raw: unknown;
}

/**
 * Discriminator values for content type narrowing.
 */
type ContentVariant =
  | 'session'
  | 'reflection'
  | 'persona'
  | 'dialogue'
  | 'context'
  | 'catch'
  | 'insight';
```

## Content-Specific Interfaces

### SessionContent

```typescript
/**
 * Session content with entry-based structure.
 */
interface SessionContent extends TraversableContent {
  readonly variant: 'session';
  readonly raw: SessionRaw;

  /**
   * Session continuation chain.
   * Null means "not a continuation"—semantic null.
   */
  readonly continuedFrom: string | null;

  /**
   * Lifecycle status. Default 'active' when not specified.
   */
  readonly status: 'active' | 'completed';

  /**
   * Normalized entries with guaranteed fields.
   * Entry IDs are generated for legacy entries that lack them.
   */
  readonly entries: readonly NormalizedEntry[];
}

interface SessionRaw {
  session_id?: string;
  type?: 'thread';
  vision?: string;
  outcome?: string;
  trigger?: string;
  parent_thread?: string;
  completed?: string;
  entries: RawEntry[];
  created?: string;
  status?: 'active' | 'completed';
  continued_from?: string | null;
}

interface RawEntry {
  id?: string;
  timestamp: string;
  notes: Record<string, unknown>;
  links?: string[];
}

interface NormalizedEntry {
  readonly id: string;
  readonly timestamp: string;
  readonly notes: Readonly<Record<string, unknown>>;
  readonly links: readonly string[];
}
```

### ReflectionContent

```typescript
interface ReflectionContent extends TraversableContent {
  readonly variant: 'reflection';
  readonly raw: ReflectionRaw;
  readonly sessionId: string;
  readonly reflection: Readonly<Record<string, unknown>>;
}

interface ReflectionRaw {
  session_id: string;
  reflection: Record<string, unknown>;
}
```

### PersonaContent

```typescript
interface PersonaContent extends TraversableContent {
  readonly variant: 'persona';
  readonly raw: PersonaRaw;
  readonly personaId: string;
  readonly expertiseDomain: string;
  readonly epistemicFramework: string | null;
}

interface PersonaRaw {
  persona_id: string;
  expertise_domain: string;
  epistemic_framework?: string;
  question_methodology?: Record<string, unknown>;
  research_protocol?: Record<string, unknown>;
  claim_support_patterns?: Record<string, unknown>;
  reasoning_state_tracking?: Record<string, unknown>;
}
```

### DialogueContent

```typescript
interface DialogueContent extends TraversableContent {
  readonly variant: 'dialogue';
  readonly raw: DialogueRaw;
  readonly dialogueId: string;
  readonly topic: string;
  readonly participants: readonly string[];
  readonly turnCount: number;
}

interface DialogueRaw {
  dialogue_id?: string;
  topic: string;
  participants: Array<{ persona_id: string; role: string }>;
  turns: Array<{
    turn_number: number;
    timestamp: string;
    persona_id: string;
    content: string;
    interaction_type?: string;
    addressed_to?: string | null;
  }>;
  status: 'active' | 'completed';
  insights?: string[];
}
```

### ContextContent

```typescript
interface ContextContent extends TraversableContent {
  readonly variant: 'context';
  readonly raw: ContextRaw;
  readonly sessionId: string;
  readonly context: Readonly<Record<string, unknown>>;
}

interface ContextRaw {
  session_id: string;
  context: Record<string, unknown>;
}
```

### CatchContent

```typescript
interface CatchContent extends TraversableContent {
  readonly variant: 'catch';
  readonly raw: CatchRaw;
  readonly content: string;
  readonly threads: readonly string[];
}

interface CatchRaw {
  id: string;
  content: string;
  timestamp: string;
  threads: string[];
  context?: {
    session?: string;
    source?: string;
    moment?: string;
  };
  energy?: string;
}
```

### InsightContent

```typescript
interface InsightContent extends TraversableContent {
  readonly variant: 'insight';
  readonly raw: InsightRaw;
  readonly title: string;
  readonly content: string;
  readonly source: string;
  readonly tags: readonly string[];
}

interface InsightRaw {
  title: string;
  content: string;
  source: string;
  tags: string[];
  extracted: string;
}
```

## Loader Function Signatures

```typescript
/**
 * Load all content from a directory as TraversableContent.
 * Detects schema variant automatically. Normalizes entries where applicable.
 */
async function loadContent<T extends ContentVariant>(
  contentType: T,
): Promise<ContentForVariant<T>[]>;

/**
 * Type mapping from variant to specific content type.
 */
type ContentForVariant<T extends ContentVariant> =
  T extends 'session' ? SessionContent :
  T extends 'reflection' ? ReflectionContent :
  T extends 'persona' ? PersonaContent :
  T extends 'dialogue' ? DialogueContent :
  T extends 'context' ? ContextContent :
  T extends 'catch' ? CatchContent :
  T extends 'insight' ? InsightContent :
  never;

/**
 * Load all content across all directories.
 * Returns a Map keyed by EntryReference ("variant:identifier").
 */
async function loadAllContent(): Promise<Map<string, TraversableContent>>;

/**
 * Load single content item by reference.
 */
async function loadByRef(ref: string): Promise<TraversableContent | null>;

/**
 * Extract text from TraversableContent for TF-IDF analysis.
 */
function extractText(content: TraversableContent): string;

/**
 * Extract links from TraversableContent for graph analysis.
 */
function extractLinks(content: TraversableContent): readonly string[];
```

## Design Decisions

### Why `readonly` everywhere?

TraversableContent is a view interface, not a data container. Consumers should not mutate the underlying data through this interface. Using `readonly` on arrays and objects enforces this at the type level.

### Why `string | null` for semantic fields instead of `?`?

The DATA-MODEL-SURVEY identified that `continued_from: null` is semantic—"not a continuation" differs from "continuation unknown." Similarly, `epistemicFramework: null` means "no framework specified" rather than "framework field absent."

### Why preserve `raw` data?

Consumers may need content-specific fields not exposed in the common interface. Rather than bloating TraversableContent with every possible field, we preserve the raw data and let TypeScript narrow it when the variant is known.

### Why lazy text extraction?

Text extraction traverses potentially deep object structures. Computing it eagerly for all 312 files when only some will be queried wastes cycles. Lazy computation with caching serves the actual access pattern.

### Why separate loader functions?

- `loadContent<T>()` enables type-safe loading of specific content types
- `loadAllContent()` enables bulk loading for THREAD detection
- `loadByRef()` enables targeted lookup for graph traversal

## Integration Points

### keyword-extract.ts

Replace `extractTextFromEntry(data: unknown)` with `extractText(content: TraversableContent)`. The loader handles schema variance; keyword extraction receives clean text.

### graph_data.ts

Replace link extraction from `session.entries` with `extractLinks(content)`. The loader normalizes link sources across content types.

### thread_detection.ts

Replace `YamlStore<SessionData>` with `loadAllContent()`. The loader handles all content types and schema variants.

## Implementation Sequence

1. Add interfaces to `plugins/journal/lib/types.ts`
2. Create `plugins/journal/lib/content_loader.ts` implementing loaders
3. Update `keyword-extract.ts` to use `extractText()`
4. Update `graph_data.ts` to use `extractLinks()`
5. Update `thread_detection.ts` to use `loadAllContent()`
6. Run tests, fix failures
7. Commit to feature branch

## Cross-References

- `specs/DATA-MODEL-SURVEY.md` — Schema variant analysis and critical findings
- `plugins/journal/lib/types.ts` — Existing type definitions
- `plugins/journal/lib/keyword-extract.ts` — Text extraction consumer
- `plugins/journal/lib/graph_data.ts` — Link extraction consumer
- `plugins/journal/lib/thread_detection.ts` — THREAD detection consumer
- `.claude/.thinkies/.notes/thread-harvest-decompose.yaml` — Design session notes
