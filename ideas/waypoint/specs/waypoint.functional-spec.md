# Waypoint Functional Specification

**Status**: Draft — Open questions tracked in `../research/waypoint.research.md`; most sections expert-reviewed
**Package**: `@seed/waypoint` *(historical — `packages/` directory no longer exists; implementation would go in `plugins/waypoint/src/` or `shared/waypoint/`)*
**Location**: *(see note above)*

---

## 1. Overview

Waypoint is a foundational library for building stateful, multi-step CLI workflows. It provides:

- Type-safe state machine definitions using Effect-TS
- SQLite persistence for state and event history
- Parallel region support for multi-agent coordination
- Progressive disclosure patterns for CLI output (without exposing PAGE in API)

### 1.1 Primary Use Case: Agent-Driven CLI Workflows

Waypoint addresses a growing industry need: CLIs that serve as deterministic infrastructure for agent skills and agentic flows (e.g., Claude Code). Agents operating autonomously require safety rails that pure LLM reasoning cannot provide:

- **Agents cannot persist state reliably.** Context windows expire, sessions restart, threads fork. Waypoint persists state in SQLite—resumable, auditable, crash-safe.
- **Agents are not 100% accurate.** They hallucinate, skip steps, misremember context. State machines enforce valid transitions—agents can only traverse developer-defined paths.
- **Agents benefit from explicit guidance.** Structured output tells the agent where it is, what it accomplished, and what moves are valid next.

### 1.2 Design Philosophy

- **CLI-first**: Developers think in steps, commands, and flows—not state machine primitives. The FSM is invisible infrastructure that enforces correctness.
- **Types as contracts**: State, events, and context are type arguments, not strings
- **Effect composition**: Transitions are effects that compose
- **CLI-owned transitions**: External callers signal events; the library computes state changes
- **Persistence-first**: State survives across invocations; resumption is the expected pattern, not an edge case

### 1.3 Relationship to Existing Packages

| Package | Relationship |
|---------|--------------|
| `@seed/page` | Waypoint will eventually replace/absorb page |
| `@seed/lib` | CLI utilities may deprecate in favor of waypoint |
| Effect-TS | Core dependency for types, schemas, effects |

---

## 2. Core Abstractions

### 2.1 Waypoint (State Node)

A waypoint represents a discrete state in a flow.

```typescript
interface Waypoint<
  Tag extends string,
  Context,
  EntryEffect = never,
  ExitEffect = never,
> {
  readonly _tag: Tag;
  readonly schema: Schema.Schema<Context>;
  readonly description: string;
  readonly terminal?: boolean;
  readonly onEntry?: () => Effect.Effect<void, EntryEffect>;
  readonly onExit?: () => Effect.Effect<void, ExitEffect>;
}
```

**Type parameters**:

- `Tag`: Discriminator for this waypoint (enum value, not string literal)
- `Context`: Shape of data available at this waypoint
- `EntryEffect`: Error type from entry action
- `ExitEffect`: Error type from exit action

### 2.2 Route (Transition)

A route defines a valid transition between waypoints.

```typescript
interface Route<
  FromTag extends string,
  FromContext,
  ToTag extends string,
  ToContext,
  EventTag extends string,
  EventPayload,
  ActionError = never,
> {
  readonly from: FromTag;
  readonly to: ToTag;
  readonly on: EventTag;
  readonly eventSchema: Schema.Schema<EventPayload>;
  readonly guard?: (params: {
    readonly context: FromContext;
    readonly event: EventPayload;
  }) => Effect.Effect<boolean, never>;
  readonly action: (params: {
    readonly context: FromContext;
    readonly event: EventPayload;
  }) => Effect.Effect<ToContext, ActionError>;
}
```

### 2.3 Journey (State Machine Instance)

A journey is a running instance of a state machine **for multi-step flows that construct resources**.

**When journeys are used**:

- Multi-step resource construction (e.g., `journal write note` gathering title, content, tags across invocations)
- Flows where partial state must survive between CLI invocations
- The journey context IS the partial resource being constructed

**When journeys are NOT used**:

- One-shot command routing (e.g., `journal` → help output)
- Simple commands with no intermediate state
- Commands where all required data arrives in a single invocation

```typescript
interface Journey<StateUnion, EventUnion, Context> {
  readonly id: string;                    // ULID
  readonly machineId: string;             // Which machine definition
  readonly currentState: StateUnion;
  readonly context: Context;              // The partial resource being constructed
  readonly status: JourneyStatus;         // enum: Active, Completed, Failed, Suspended
  readonly createdAt: string;             // ISO 8601
  readonly updatedAt: string;
}
```

### 2.4 Map (State Machine Definition)

A map is the complete state machine definition.

```typescript
interface MachineMap<
  WaypointUnion,
  RouteUnion,
  EventUnion,
  ContextUnion,
> {
  readonly id: string;
  readonly waypoints: ReadonlyArray<WaypointUnion>;
  readonly routes: ReadonlyArray<RouteUnion>;
  readonly initial: WaypointUnion['_tag'];
  readonly terminal: ReadonlyArray<WaypointUnion['_tag']>;
}
```

---

## 3. Data Modeling: Schema → SQLite

**Status**: Expert reviewed — recommendations integrated

### 3.1 What Gets Persisted

**Clarification**: SQLite persistence is for **resources**, not machine state tracking.

| Persisted | Not Persisted |
|-----------|---------------|
| Partial resources being constructed | Command tree navigation |
| Journey context (the resource-in-progress) | "Which waypoint am I at" for routing |
| Event history (for auditability) | One-shot command outputs |
| Completed resources | Help text / subcommand listings |

The machine defines valid paths and outputs. Journeys persist only when a multi-step flow needs to survive across CLI invocations.

### 3.2 Persistence Strategy: Hybrid (Snapshot + Event Log)

**Decision**: Write both snapshot and event on every transition.

| Factor | Event Sourcing Only | Hybrid (Chosen) |
|--------|---------------------|-----------------|
| Resume latency | O(n) - replay all | O(1) - read snapshot |
| Storage | Events only | Events + snapshot |
| Debugging | Full history | Full history |
| CLI workflows | Overkill | Practical |

### 3.3 Transaction Guarantees

**Invariant**: Snapshot and event are written in a single SQLite transaction.

```typescript
// Pseudocode for transition persistence
await db.transaction(async (tx) => {
  // 1. Append event to log
  await tx.insert(events, eventRecord);

  // 2. Update journey snapshot
  await tx.update(journeys, {
    current_state_tag: newState.tag,
    context: newState.context,
    event_sequence: journey.event_sequence + 1,
    updated_at: now,
  });
});
// Either both succeed or neither does
```

**Why this matters**:

- **Crash safety**: If process dies mid-transition, we never have a snapshot without its event (or vice versa)
- **Replay consistency**: Event log and current state are always in agreement
- **Audit trail**: Every state change has exactly one corresponding event

### 3.4 Schema Design

```sql
-- Journey instances (current state snapshot)
CREATE TABLE journeys (
  id TEXT PRIMARY KEY,                           -- ULID
  journey_id TEXT NOT NULL UNIQUE,               -- External identifier
  machine_id TEXT NOT NULL,                      -- Which machine definition
  machine_version TEXT NOT NULL,                 -- Semantic version

  -- State (discriminated union → tag + JSON)
  current_state_tag TEXT NOT NULL,               -- Enum value as string
  context JSON NOT NULL,                         -- Typed context

  -- Lifecycle
  status TEXT NOT NULL CHECK (status IN ('active', 'completed', 'failed', 'suspended')),
  started_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  completed_at TEXT,

  -- Concurrency control
  event_sequence INTEGER NOT NULL DEFAULT 0,     -- Optimistic lock
  schema_version TEXT NOT NULL DEFAULT '1.0.0'
);

-- Append-only event log
CREATE TABLE events (
  id TEXT PRIMARY KEY,                           -- ULID (sortable)
  journey_id TEXT NOT NULL REFERENCES journeys(id) ON DELETE CASCADE,

  -- Event data
  event_tag TEXT NOT NULL,
  event_payload JSON NOT NULL,

  -- State transition record (enables replay)
  prior_state_tag TEXT NOT NULL,
  prior_context JSON NOT NULL,
  resulting_state_tag TEXT NOT NULL,
  resulting_context JSON NOT NULL,

  -- Ordering
  sequence INTEGER NOT NULL,                     -- Monotonic per journey
  timestamp TEXT NOT NULL,
  duration_ms INTEGER,

  UNIQUE(journey_id, sequence)
);

-- Parallel regions
CREATE TABLE regions (
  id TEXT PRIMARY KEY,
  journey_id TEXT NOT NULL REFERENCES journeys(id) ON DELETE CASCADE,
  region_id TEXT NOT NULL,
  region_machine_id TEXT NOT NULL,

  current_state_tag TEXT NOT NULL,
  context JSON NOT NULL,

  health_status TEXT NOT NULL CHECK (health_status IN ('active', 'stale', 'stuck', 'terminated')),
  last_heartbeat TEXT NOT NULL,
  events_emitted INTEGER NOT NULL DEFAULT 0,

  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,

  UNIQUE(journey_id, region_id)
);

CREATE INDEX idx_journeys_machine ON journeys(machine_id);
CREATE INDEX idx_journeys_status ON journeys(status);
CREATE INDEX idx_journeys_machine_status ON journeys(machine_id, status);  -- Common query: find active journeys for machine
CREATE INDEX idx_events_journey ON events(journey_id);
CREATE INDEX idx_regions_journey ON regions(journey_id);
```

### 3.4 Type Preservation

Type information flows through `machine_id` + `machine_version`:

```typescript
/** Machine registry resolves IDs to typed definitions */
interface MachineRegistry {
  readonly get: <State, Event, Context>(params: {
    readonly machineId: string;
    readonly version: string;
  }) => MachineMap<State, Event, Context> | undefined;

  readonly register: <State, Event, Context>(
    machine: MachineMap<State, Event, Context>
  ) => void;
}
```

### 3.5 Serialization with Effect/Schema

```typescript
/** Canonical JSON encoding for deterministic serialization */
const canonicalStringify = (value: unknown): string =>
  JSON.stringify(value, (_, v) =>
    v && typeof v === 'object' && !Array.isArray(v)
      ? Object.keys(v).sort().reduce((sorted, key) => {
          sorted[key] = v[key];
          return sorted;
        }, {} as Record<string, unknown>)
      : v
  );

/** Encode state for persistence */
const encodeState = <State>(params: {
  readonly state: State;
  readonly schema: Schema.Schema<State>;
}): Effect.Effect<{ tag: string; context: string }, EncodeError> =>
  Effect.gen(function* () {
    const encoded = yield* Schema.encode(params.schema)(params.state);
    return {
      tag: (encoded as { _tag: string })._tag,
      // Use canonical encoding for deterministic JSON (sorted keys)
      context: canonicalStringify((encoded as { context: unknown }).context),
    };
  });

/** Decode state from persistence with validation */
const decodeState = <State>(params: {
  readonly tag: string;
  readonly contextJson: string;
  readonly schema: Schema.Schema<State>;
}): Effect.Effect<State, DecodeError> =>
  Effect.gen(function* () {
    const raw = { _tag: params.tag, context: JSON.parse(params.contextJson) };
    return yield* Schema.decodeUnknown(params.schema)(raw);
  });
```

### 3.6 Migration Strategy

- **Row-level**: `schema_version` column enables row migrations on read
- **Machine-level**: `machine_version` tracks definition changes
- **Additive safe**: New waypoints/routes don't break existing journeys
- **Breaking changes**: Require explicit migration functions in machine definition

---

## 4. Effect-TS Integration

**Status**: Expert reviewed — recommendations integrated

### 4.1 Transition Composition

Transitions are Effects that compose naturally with dependency injection and typed error handling:

```typescript
/**
 * Transition effect that transforms context from one waypoint to another.
 */
type Transition<
  FromContext,
  ToContext,
  EventPayload,
  TransitionError extends WaypointError,
  Requirements,
> = (params: {
  readonly context: FromContext;
  readonly event: EventPayload;
}) => Effect.Effect<ToContext, TransitionError, Requirements>;
```

### 4.2 Error Type Hierarchy

Use tagged unions with enum discriminators for exhaustive matching:

```typescript
enum WaypointErrorTag {
  ValidationError = 'ValidationError',
  PersistenceError = 'PersistenceError',
  GuardRejection = 'GuardRejection',
  InvalidTransition = 'InvalidTransition',
  JourneyNotFound = 'JourneyNotFound',
  ActionError = 'ActionError',
}

interface WaypointErrorBase {
  readonly _tag: WaypointErrorTag;
  readonly message: string;
  readonly journeyId: string | null;
  readonly timestamp: string;
}

// Specific error types extend base with additional context
interface ValidationError extends WaypointErrorBase {
  readonly _tag: WaypointErrorTag.ValidationError;
  readonly schemaName: string;
  readonly fieldErrors: ReadonlyArray<{
    readonly path: string;
    readonly message: string;
    readonly expected: string;
  }>;
}

// Union of all error types
type WaypointError =
  | ValidationError
  | PersistenceError
  | GuardRejection
  | InvalidTransition
  | JourneyNotFound
  | ActionError;
```

### 4.3 Service Layer Architecture

Define services as interfaces with Context tags. Implementations provided via Layers:

```typescript
// Service interface
interface WaypointPersistence {
  readonly saveJourney: (params: {
    readonly journey: JourneySnapshot;
  }) => Effect.Effect<void, PersistenceError>;

  readonly loadJourney: (params: {
    readonly journeyId: string;
  }) => Effect.Effect<JourneySnapshot, PersistenceError | JourneyNotFound>;

  readonly appendEvent: (params: {
    readonly journeyId: string;
    readonly event: EventRecord;
  }) => Effect.Effect<void, PersistenceError>;
}

// Context tag
const WaypointPersistence = Context.GenericTag<WaypointPersistence>(
  '@seed/waypoint/WaypointPersistence',
);

// Additional services for testability
interface WaypointClock {
  readonly now: () => Effect.Effect<string>;
}

interface WaypointIdGenerator {
  readonly generateId: () => Effect.Effect<string>;
}
```

### 4.4 Layer Composition

Layers compose for production and testing. Use `Layer.scoped` with `Effect.acquireRelease` for resource management (SQLite connections, etc.):

```typescript
// SQLite connection with proper lifecycle management
const makeSqlitePersistence = (params: { readonly dbPath: string }) =>
  Layer.scoped(
    WaypointPersistence,
    Effect.acquireRelease(
      // Acquire: open connection
      Effect.sync(() => openDatabase(params.dbPath)),
      // Release: close connection (runs on scope finalization)
      (db) => Effect.sync(() => db.close()),
    ).pipe(
      Effect.map((db) => makePersistenceFromDb(db)),
    ),
  );

// Production layers
const ProductionLayers = (params: { readonly dbPath: string }) =>
  Layer.mergeAll(
    LiveClock,
    LiveIdGenerator,
    makeSqlitePersistence({ dbPath: params.dbPath }),
  ).pipe(Layer.provide(LiveWaypointService));

// Test layers with deterministic behavior using Effect.Ref (not mutable let)
const makeTestIdGenerator = (params: { readonly ids: ReadonlyArray<string> }) =>
  Layer.effect(
    WaypointIdGenerator,
    Effect.gen(function* () {
      // Use Ref for mutable state, not `let`
      const indexRef = yield* Ref.make(0);
      return {
        generateId: () =>
          Ref.getAndUpdate(indexRef, (i) => i + 1).pipe(
            Effect.map((i) => params.ids[i] ?? `fallback-${i}`),
          ),
      };
    }),
  );

const TestLayers = (params: {
  readonly fixedTime: string;
  readonly ids: ReadonlyArray<string>;
}) =>
  Layer.mergeAll(
    makeTestClock({ fixedTime: params.fixedTime }),
    makeTestIdGenerator({ ids: params.ids }),
    makeInMemoryPersistence(),
  ).pipe(Layer.provide(LiveWaypointService));
```

### 4.5 Schema Integration

Use Effect Schema with PAGE annotations (established codebase pattern):

```typescript
const SessionContextSchema = Schema.Struct({
  name: PageSchema.string({
    description: 'Session name in kebab-case format',
    examples: ['auth-refactor'],
  }),
});

// Types derived from schemas
type SessionContext = Schema.Schema.Type<typeof SessionContextSchema>;

// Validation helper
const validateWithSchema = <SchemaType>(params: {
  readonly data: unknown;
  readonly schema: Schema.Schema<SchemaType>;
  readonly schemaName: string;
  readonly journeyId: string | null;
}): Effect.Effect<SchemaType, ValidationError> => // ...
```

### 4.6 Stream Patterns

For event replay and state change subscription:

```typescript
// Stream events for replay
const streamEvents = (params: {
  readonly journeyId: string;
}): Stream.Stream<EventRecord, PersistenceError, WaypointPersistence> => // ...

// Replay events to reconstruct state using runFoldEffect (not runFold)
// runFoldEffect allows effectful fold operations during replay
const replayJourney = (params: {
  readonly journeyId: string;
  readonly initialState: JourneyState;
}): Effect.Effect<JourneyState, ReplayError, WaypointPersistence> =>
  streamEvents({ journeyId: params.journeyId }).pipe(
    // Use runFoldEffect when the fold function needs to perform effects
    Stream.runFoldEffect(
      params.initialState,
      (state, event) =>
        // Each replay step can perform validation, logging, etc.
        applyEvent({ state, event }).pipe(
          Effect.tap(() => Effect.logDebug(`Replayed event ${event.id}`)),
        ),
    ),
  );

// PubSub for state change notification
interface WaypointPubSub {
  readonly publish: (event: StateChangeEvent) => Effect.Effect<boolean>;
  readonly subscribe: () => Effect.Effect<Queue.Dequeue<StateChangeEvent>>;
}

// Backpressure strategies: bounded, sliding, dropping
```

### 4.7 Main Service Interface

```typescript
interface WaypointService {
  readonly start: <Machine extends MachineDefinition>(params: {
    readonly machine: Machine;
    readonly initialContext?: Machine['InitialContext'];
  }) => Effect.Effect<
    Journey<Machine['StateUnion'], Machine['ContextUnion']>,
    ValidationError | PersistenceError,
    WaypointPersistence | WaypointClock | WaypointIdGenerator
  >;

  readonly send: <EventPayload>(params: {
    readonly journeyId: string;
    readonly event: EventPayload;
  }) => Effect.Effect<
    TransitionResult,
    WaypointError,
    WaypointPersistence | WaypointClock
  >;

  readonly resume: (params: {
    readonly journeyId: string;
  }) => Effect.Effect<
    JourneySnapshot,
    PersistenceError | JourneyNotFound,
    WaypointPersistence
  >;

  readonly replay: (params: {
    readonly journeyId: string;
  }) => Effect.Effect<
    JourneySnapshot,
    PersistenceError | JourneyNotFound | ActionError,
    WaypointPersistence
  >;
}
```

**Full implementation details**: See `WAYPOINT-effect-integration-review.md`

---

## 5. Parallel State Regions

### 5.1 Requirements

Based on switchboard dialogue patterns:

1. **Region isolation**: Each region has independent state within shared journey
2. **Shared coordination**: Central phase/status governs all regions
3. **Health tracking**: Per-region heartbeat, timeout detection
4. **Event aggregation**: Events from any region can trigger transitions

### 5.2 Region Model

```typescript
interface Region<StateUnion, Context> {
  readonly regionId: string;
  readonly currentState: StateUnion;
  readonly context: Context;
  readonly health: RegionHealth;
}

interface RegionHealth {
  readonly status: RegionHealthStatus;  // enum: Active, Stale, Stuck, Terminated
  readonly lastHeartbeat: string;
  readonly eventsEmitted: number;
}
```

### 5.3 Coordination Patterns

```typescript
// Parallel region definition in machine
interface ParallelRegion<RegionId extends string, RegionMachine> {
  readonly regionId: RegionId;
  readonly machine: RegionMachine;
}

// Journey with parallel regions
interface ParallelJourney<
  CoordinatorState,
  Regions extends ReadonlyArray<ParallelRegion<string, unknown>>,
> {
  readonly coordinatorState: CoordinatorState;
  readonly regions: { [K in Regions[number]['regionId']]: Region<...> };
}
```

### 5.4 Implementation Notes

Parallel region typing and coordination are addressed in the open questions section of `../waypoint.idea.md`. Key decisions (Q6: completion detection, Q7: heterogeneous completion) must be resolved before implementing this section.

---

## 6. CLI Output Layer

### 6.1 Design Principle

Waypoint embodies PAGE principles without exposing them in API:

- Progressive disclosure for error messages
- Clear "what went wrong, what to do next" patterns
- Helpful output for both humans and agents

### 6.2 Output Types

```typescript
enum OutputKind {
  StateReached = 'state-reached',
  TransitionFailed = 'transition-failed',
  JourneyCompleted = 'journey-completed',
  JourneyFailed = 'journey-failed',
  ValidationError = 'validation-error',
}

interface WaypointOutput<State, Context> {
  readonly kind: OutputKind;
  readonly currentState: State;
  readonly context: Context;
  readonly message: string;
  readonly nextSteps: ReadonlyArray<NextStep>;
  readonly history?: ReadonlyArray<HistoryEntry>;
}

interface NextStep {
  readonly description: string;  // Goal-oriented: "To continue, ..."
  readonly event: string;        // Event to send
  readonly example?: string;     // Example invocation
}
```

### 6.3 Rendering

Output rendering is separate from state machine logic:

- Machine produces `WaypointOutput`
- Renderer formats for terminal (colors, boxes, etc.)
- No PAGE terminology in public API

---

## 7. API Surface (Draft)

### 7.1 Machine Definition API

```typescript
import { waypoint, route, machine } from '@seed/waypoint';
import { Schema } from 'effect';

// Define waypoints
const askName = waypoint({
  tag: WaypointTag.AskName,
  schema: Schema.Struct({}),
  description: 'Gathering session name',
});

const askFocus = waypoint({
  tag: WaypointTag.AskFocus,
  schema: Schema.Struct({ name: Schema.String }),
  description: 'Gathering focus area',
});

// Define routes
const provideName = route({
  from: WaypointTag.AskName,
  to: WaypointTag.AskFocus,
  on: EventTag.ProvideName,
  eventSchema: Schema.Struct({ name: Schema.String }),
  action: ({ context, event }) => Effect.succeed({ name: event.name }),
});

// Compose machine
const sessionFlow = machine({
  id: 'session-creation',
  waypoints: [askName, askFocus, created],
  routes: [provideName, provideFocus],
  initial: WaypointTag.AskName,
  terminal: [WaypointTag.Created],
});
```

### 7.2 Runtime API

```typescript
import { Waypoint } from '@seed/waypoint';

// Start journey
const journey = await Waypoint.start(sessionFlow);

// Send event
const result = await Waypoint.send(journey.id, {
  _tag: EventTag.ProvideName,
  name: 'auth-refactor',
});

// Resume journey
const resumed = await Waypoint.resume(journeyId);

// Query journeys
const active = await Waypoint.findActive({ machineId: 'session-creation' });
```

---

## 8. Code Organization

**Status**: Expert reviewed — recommendations integrated

### 8.1 Design Principle: Dual-Layer Structure

The package presents CLI utilities at the surface while organizing FSM mechanics beneath. CLI authors interact with `api/`; internal implementation lives in `lib/`.

```
packages/waypoint/
├── api/                    # CLI-author surface (what they IMPORT)
│   ├── builders.ts         # waypoint(), route(), machine()
│   ├── runtime.ts          # Waypoint.start(), send(), resume()
│   ├── output.ts           # WaypointOutput formatting
│   └── testing.ts          # TestLayers for machine authors
│
├── lib/                    # Internal implementation
│   ├── enums.ts            # ALL enums centralized
│   ├── schemas.ts          # ALL schemas centralized
│   ├── errors.ts           # Error constructors
│   ├── types.ts            # Inferred types + interfaces
│   ├── core/               # FSM primitives
│   │   ├── waypoint.ts     # waypoint() builder
│   │   ├── route.ts        # route() builder
│   │   ├── machine.ts      # machine() composition
│   │   └── transition.ts   # Transition execution
│   ├── services/           # Effect service interfaces + Context tags
│   │   ├── persistence.ts
│   │   ├── clock.ts
│   │   ├── id-generator.ts
│   │   └── waypoint-service.ts
│   ├── layers/             # Layer implementations
│   │   ├── sqlite-persistence.ts
│   │   ├── memory-persistence.ts
│   │   ├── production.ts   # ProductionLayers
│   │   └── test.ts         # TestLayers
│   ├── persistence/        # SQLite-specific
│   │   ├── database.ts
│   │   ├── migrations.ts
│   │   └── queries.ts
│   └── streams/            # Replay and subscription
│
└── index.ts                # Public API re-exports
```

### 8.2 Contributor Decision Rules

| Adding... | Put it in... | Rationale |
|-----------|--------------|-----------|
| New error type | `lib/enums.ts` + `lib/errors.ts` | Centralized discriminators |
| New schema | `lib/schemas.ts` | Single schema registry |
| Service interface | `lib/services/<name>.ts` | Service per file |
| Layer implementation | `lib/layers/<name>.ts` | Layer per file |
| FSM execution logic | `lib/core/<concept>.ts` | Domain core |
| CLI-author-facing API | `api/<category>.ts` | Consumer facade |

### 8.3 What not to do

- **Never** define enums in multiple files
- **Never** define schemas outside `lib/schemas.ts`
- **Never** import from `lib/core/` in consumer code (use `api/`)
- **Never** put Layer implementations in `lib/services/`

### 8.4 Public API Re-Export Strategy

```typescript
// index.ts — Consumer-facing API only
export { machine, route, waypoint } from './api/builders.ts';
export { Waypoint } from './api/runtime.ts';
export { OutputKind, type WaypointOutput } from './api/output.ts';
export { TestLayers } from './api/testing.ts';
export { WaypointErrorTag, type WaypointError } from './lib/errors.ts';
export { JourneyStatus } from './lib/enums.ts';
export type { Journey, MachineDefinition, Route } from './lib/types.ts';
```

**Full implementation details**: See code organization expert consultation notes.

---

## 9. Success Criteria

1. **Type safety**: No `any`, no `unknown` except for user input and defaults
2. **Effect composition**: Transitions compose with other effects
3. **Persistence**: State survives process restarts
4. **Parallel regions**: Multi-agent coordination works
5. **DX**: Excellent error messages, type inference, testing utilities
6. **Performance**: SQLite operations are efficient for CLI use

---

## 10. Resolved Questions

1. **Machine definitions: code-only.** Machines are developer-defined artifacts, version-controlled with source code. SQLite stores journey *instances*, not machine *definitions*. No dynamic registration needed for CLI-first use case.

2. **Version migrations: deferred.** Not a binding architectural decision. Start simple (journeys reference machine version); add migration support if/when needed. The `machine_version` column enables future flexibility without committing to a policy now.

3. **Testing: TestLayers pattern.** Addressed in Section 4. Deterministic clock/IDs + in-memory persistence enable isolated, reproducible tests.

4. **Nested machines: required.** CLI command hierarchies are inherently nested (`journal session create`). Each subcommand group can be its own machine, composed into parent machines. This is core to CLI-first design, not optional.

## 11. Nested Machine Design

**Status**: Resolved via problem space exploration of perspectives and switchboard packages.

### 11.1 Context Sharing: Inherit with Explicit Boundaries

Child machines inherit parent context, but inheritance is **declared explicitly** — children specify what they need, not blanket access.

**Evidence from exploration:**

- Strand operations need patch context (iteration number, purpose)
- Dialogue turns need session context (round count, participant list)
- Narrations need strand context (what was assigned, dependencies)

```typescript
// Child declares required parent context
const strandNarrationMachine = machine({
  id: 'strand-narration',
  parentContext: Schema.Struct({
    patchId: Schema.String,
    iteration: Schema.Number,
    strandPurpose: Schema.String,
  }),
  // Child can read parentContext but not mutate it
});
```

**Rationale**: Explicit declaration enables:

- Type-safe access to parent state
- Clear contracts between machines
- Resumption with full lineage ("Strand from iteration 2 of patch P3")

**Important: Spawn-with-Snapshot Semantics**

Waypoint uses **spawn-with-snapshot** semantics, which differs from XState's shared-context model:

| Aspect | XState (shared context) | Waypoint (snapshot) |
|--------|-------------------------|---------------------|
| Child access | Live reference to parent context | Frozen snapshot at spawn time |
| Parent changes | Visible to child immediately | Not visible; child has its copy |
| Concurrency | Requires synchronization | Naturally isolated |
| Resumption | Must reconstruct live reference | Self-contained; snapshot persisted |

**Why snapshot**: CLI flows are inherently non-interactive—each invocation is a separate process. There's no live parent to reference. The snapshot captures "what the world looked like when this child was spawned," which is exactly what resumption needs.

### 11.2 Parallel Regions vs Nesting: Orthogonal Concepts

**Regions** = siblings within a journey (concurrent activities)
**Nesting** = hierarchy (child machine invoked by parent)

A PATCH has multiple strands (parallel regions). Each strand's narration flow is a nested journey that runs within its region — it doesn't spawn new regions.

```
PATCH Journey (coordinator)
├─ Region: strand-A (linear: claimed → working → narration-submitted)
├─ Region: strand-B (linear: claimed → working → narration-submitted)
└─ Region: strand-C (blocked → unblocked → claimed → ...)

Each region runs its own nested journey:
  strand-A:narration-flow
  ├─ Waypoint: awaiting-claim
  ├─ Waypoint: work-in-progress
  ├─ Waypoint: narration-drafting
  └─ Waypoint: submitted (terminal)
```

### 11.3 Nested Journey Lifecycle: Independent with FK Relations

Nested journeys persist **independently** (own rows in `journeys` table) with foreign key relations to parent.

**Evidence from exploration:**

- Strands persist independently from patches but reference `patch_id`
- Dialogue turns persist independently but reference `dialogue_id`
- Session history entries persist independently but reference `dialogue_id`

**Schema addition:**

```sql
ALTER TABLE journeys ADD COLUMN parent_journey_id TEXT REFERENCES journeys(id) ON DELETE CASCADE;
CREATE INDEX idx_journeys_parent ON journeys(parent_journey_id);
```

**Benefits:**

- Query children directly: "Show all nested journeys stuck > 1 hour"
- Resume child without loading full parent
- Cascading deletes via FK
- Clear audit trail per child

### 11.4 Problem Spaces Waypoint Addresses

Based on exploration of perspectives and switchboard:

| Problem | Current State | Waypoint Solution |
|---------|---------------|-------------------|
| **Partial resource construction** | Persona save dies mid-write; unclear if saved | Checkpoint: "Validated ✓ Awaiting persist" → resume shows progress |
| **Turn persistence ambiguity** | Dialogue turn added but session not ended | Checkpoint: "Turn N persisted. Awaiting session end" |
| **Iteration advancement** | Strand completes but iteration doesn't advance | Checkpoint: "All strands reported. Advancing iteration..." |
| **Lost forTodos** | Items from iteration 1 never became strands | Explicit: `iteration_1.forTodos` persisted, checked before iteration 2 |
| **Stuck strands** | Claimed but never reports; blocks dependents | Watchdog: "Strand claimed 2h ago, no heartbeat. Escalate?" |
| **Persona drift** | Definition modified between dialogue sessions | Snapshot: personas captured at session start in journey context |

### 11.5 Resumption Contract

For faithful resumption, nested journeys must preserve:

1. **Parent lineage**: `parent_journey_id` chain to root
2. **Creation context**: snapshot of parent context at spawn time
3. **Checkpoint state**: last successfully completed waypoint
4. **Pending inputs**: what the child is waiting for

```typescript
interface NestedJourneySnapshot {
  readonly id: string;
  readonly parentJourneyId: string;
  readonly parentContextSnapshot: unknown;  // Frozen at spawn
  readonly currentWaypoint: string;
  readonly context: unknown;                // Child's accumulated state
  readonly awaitingInput?: string;          // "narration from agent-A"
}
```

---

## 12. Next Steps

1. [x] Expert consultation: Data modeling (Section 3) — Complete
2. [x] Expert consultation: Effect-TS integration (Section 4) — Complete
3. [x] Expert consultation: Code organization (Section 8) — Complete
4. [x] Resolve nested machine design questions (Section 11) — Complete
5. [ ] **Create proposal** from validated spec
6. [ ] Prototype core abstractions
7. [ ] Implement SQLite persistence layer
8. [ ] Build first real flow (perspectives persona save or switchboard strand narration)
