# Waypoint Effect-TS Integration: Expert Review

**Reviewer**: Effect-TS Architecture Expert
**Document**: Section 4 of WAYPOINT-functional.md
**Date**: 2026-01-17
**Status**: Draft recommendations

---

## Executive Summary

This document provides expert recommendations for integrating Effect-TS deeply into `@seed/waypoint`. The recommendations align with established codebase patterns (single parameter objects, enum discriminators, exports at bottom, Schema-driven validation) while introducing idiomatic Effect patterns for Layers, Services, and Streams.

---

## 1. Transition Composition

### 1.1 Type Signature for Transitions

Transitions should be Effects that compose naturally with dependency injection, error handling, and context propagation. The key insight: transitions transform context while potentially requiring services and producing typed errors.

```typescript
/**
 * Transition effect that transforms context from one waypoint to another.
 *
 * Type parameters:
 * - FromContext: Shape of context before transition
 * - ToContext: Shape of context after transition
 * - EventPayload: Event data that triggers this transition
 * - TransitionError: Domain-specific error type (extends WaypointError)
 * - Requirements: Effect requirements (services needed)
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

### 1.2 Error Type Hierarchy

Effect-TS shines with typed errors. Define a hierarchy using tagged unions with enum discriminators (per STANDARDS.md):

```typescript
/**
 * Error category discriminator.
 * Using enum ensures compiler catches typos and enables exhaustive matching.
 */
enum WaypointErrorTag {
  /** Schema validation failed */
  ValidationError = 'ValidationError',
  /** Persistence operation failed */
  PersistenceError = 'PersistenceError',
  /** Transition guard rejected event */
  GuardRejection = 'GuardRejection',
  /** Invalid transition from current state */
  InvalidTransition = 'InvalidTransition',
  /** Journey not found or corrupted */
  JourneyNotFound = 'JourneyNotFound',
  /** Business logic error in action */
  ActionError = 'ActionError',
}

/**
 * Base waypoint error interface.
 * All errors carry enough context for meaningful error messages.
 */
interface WaypointErrorBase {
  readonly _tag: WaypointErrorTag;
  readonly message: string;
  readonly journeyId: string | null;
  readonly timestamp: string;
}

/**
 * Validation error with field-level details.
 * Integrates with PAGE-style error reporting.
 */
interface ValidationError extends WaypointErrorBase {
  readonly _tag: WaypointErrorTag.ValidationError;
  readonly schemaName: string;
  readonly fieldErrors: ReadonlyArray<{
    readonly path: string;
    readonly message: string;
    readonly expected: string;
  }>;
}

/**
 * Persistence layer failure.
 */
interface PersistenceError extends WaypointErrorBase {
  readonly _tag: WaypointErrorTag.PersistenceError;
  readonly operation: 'save' | 'load' | 'append' | 'delete';
  readonly cause: unknown;
}

/**
 * Guard function rejected the event.
 */
interface GuardRejection extends WaypointErrorBase {
  readonly _tag: WaypointErrorTag.GuardRejection;
  readonly guardName: string;
  readonly reason: string;
  readonly fromState: string;
  readonly eventTag: string;
}

/**
 * No valid transition exists for this state+event combination.
 */
interface InvalidTransition extends WaypointErrorBase {
  readonly _tag: WaypointErrorTag.InvalidTransition;
  readonly currentState: string;
  readonly eventTag: string;
  readonly validEvents: ReadonlyArray<string>;
}

/**
 * Journey lookup failed.
 */
interface JourneyNotFound extends WaypointErrorBase {
  readonly _tag: WaypointErrorTag.JourneyNotFound;
}

/**
 * Business logic error from transition action.
 */
interface ActionError extends WaypointErrorBase {
  readonly _tag: WaypointErrorTag.ActionError;
  readonly actionName: string;
  readonly cause: unknown;
}

/**
 * Union of all waypoint errors.
 * Use exhaustive switch on _tag for handling.
 */
type WaypointError =
  | ValidationError
  | PersistenceError
  | GuardRejection
  | InvalidTransition
  | JourneyNotFound
  | ActionError;
```

**Constructor functions** (following Effect patterns):

```typescript
/**
 * Create a validation error from schema validation result.
 */
const validationError = (params: {
  readonly journeyId: string | null;
  readonly schemaName: string;
  readonly fieldErrors: ValidationError['fieldErrors'];
}): ValidationError => ({
  _tag: WaypointErrorTag.ValidationError,
  fieldErrors: params.fieldErrors,
  journeyId: params.journeyId,
  message: `Validation failed for ${params.schemaName}: ${params.fieldErrors.length} field(s) invalid`,
  schemaName: params.schemaName,
  timestamp: new Date().toISOString(),
});

/**
 * Create a persistence error.
 */
const persistenceError = (params: {
  readonly journeyId: string | null;
  readonly operation: PersistenceError['operation'];
  readonly cause: unknown;
}): PersistenceError => ({
  _tag: WaypointErrorTag.PersistenceError,
  cause: params.cause,
  journeyId: params.journeyId,
  message: `Persistence ${params.operation} failed`,
  operation: params.operation,
  timestamp: new Date().toISOString(),
});

// ... similar constructors for other error types
```

### 1.3 Dependency Injection via Context/Layer

Effect's Context system provides compile-time verified dependency injection. Define services as interfaces, then provide implementations via Layers.

```typescript
import { Context, Effect, Layer } from 'effect';

// ============================================================================
// Service Definitions (Interfaces)
// ============================================================================

/**
 * Persistence service interface.
 * Implementations can be SQLite, in-memory, or mock for testing.
 */
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

  readonly listJourneys: (params: {
    readonly machineId: string | null;
    readonly status: JourneyStatus | null;
    readonly limit: number;
  }) => Effect.Effect<ReadonlyArray<JourneySummary>, PersistenceError>;
}

/**
 * Tag for WaypointPersistence service.
 * Used for Context.get and Layer construction.
 */
const WaypointPersistence = Context.GenericTag<WaypointPersistence>(
  '@seed/waypoint/WaypointPersistence',
);

/**
 * Clock service for timestamp generation.
 * Abstracted for deterministic testing.
 */
interface WaypointClock {
  readonly now: () => Effect.Effect<string>;
}

const WaypointClock = Context.GenericTag<WaypointClock>(
  '@seed/waypoint/WaypointClock',
);

/**
 * ID generation service.
 * Abstracted for deterministic testing.
 */
interface WaypointIdGenerator {
  readonly generateId: () => Effect.Effect<string>;
}

const WaypointIdGenerator = Context.GenericTag<WaypointIdGenerator>(
  '@seed/waypoint/WaypointIdGenerator',
);

// ============================================================================
// Layer Implementations
// ============================================================================

/**
 * Live clock implementation using system time.
 */
const LiveClock = Layer.succeed(WaypointClock, {
  now: () => Effect.sync(() => new Date().toISOString()),
});

/**
 * Test clock with controllable time.
 */
const makeTestClock = (params: { readonly fixedTime: string }) =>
  Layer.succeed(WaypointClock, {
    now: () => Effect.succeed(params.fixedTime),
  });

/**
 * Live ID generator using ULID.
 */
const LiveIdGenerator = Layer.succeed(WaypointIdGenerator, {
  generateId: () => Effect.sync(() => generateUlid()),
});

/**
 * Deterministic ID generator for tests.
 */
const makeTestIdGenerator = (params: { readonly ids: ReadonlyArray<string> }) => {
  let index = 0;
  return Layer.succeed(WaypointIdGenerator, {
    generateId: () =>
      Effect.sync(() => {
        const id = params.ids[index];
        if (id === undefined) {
          throw new Error('Test ID generator exhausted');
        }
        index++;
        return id;
      }),
  });
};

/**
 * SQLite persistence layer.
 * Requires Database handle as dependency.
 */
const makeSqlitePersistence = (params: {
  readonly dbPath: string;
}): Layer.Layer<WaypointPersistence, PersistenceError> =>
  Layer.effect(
    WaypointPersistence,
    Effect.gen(function* () {
      const db = yield* Effect.tryPromise({
        catch: (error) =>
          persistenceError({
            cause: error,
            journeyId: null,
            operation: 'load',
          }),
        try: () => openDatabase(params.dbPath),
      });

      return {
        appendEvent: (eventParams) =>
          Effect.tryPromise({
            catch: (error) =>
              persistenceError({
                cause: error,
                journeyId: eventParams.journeyId,
                operation: 'append',
              }),
            try: () =>
              db.run(
                'INSERT INTO events (journey_id, ...) VALUES (?, ...)',
                eventParams.journeyId,
              ),
          }),

        listJourneys: (listParams) =>
          Effect.tryPromise({
            catch: (error) =>
              persistenceError({
                cause: error,
                journeyId: null,
                operation: 'load',
              }),
            try: () =>
              db.all('SELECT * FROM journeys WHERE ...', listParams.machineId),
          }),

        loadJourney: (loadParams) =>
          Effect.tryPromise({
            catch: (error) =>
              persistenceError({
                cause: error,
                journeyId: loadParams.journeyId,
                operation: 'load',
              }),
            try: async () => {
              const row = await db.get(
                'SELECT * FROM journeys WHERE id = ?',
                loadParams.journeyId,
              );
              if (!row) {
                throw { notFound: true };
              }
              return row as JourneySnapshot;
            },
          }),

        saveJourney: (saveParams) =>
          Effect.tryPromise({
            catch: (error) =>
              persistenceError({
                cause: error,
                journeyId: saveParams.journey.id,
                operation: 'save',
              }),
            try: () =>
              db.run(
                'INSERT OR REPLACE INTO journeys ...',
                saveParams.journey.id,
              ),
          }),
      };
    }),
  );

/**
 * In-memory persistence for testing.
 * State is isolated per Layer instance.
 */
const makeInMemoryPersistence =
  (): Layer.Layer<WaypointPersistence> =>
    Layer.sync(WaypointPersistence, () => {
      const journeys = new Map<string, JourneySnapshot>();
      const events = new Map<string, EventRecord[]>();

      return {
        appendEvent: (params) =>
          Effect.sync(() => {
            const list = events.get(params.journeyId) ?? [];
            list.push(params.event);
            events.set(params.journeyId, list);
          }),

        listJourneys: (params) =>
          Effect.sync(() =>
            Array.from(journeys.values())
              .filter((j) => {
                if (params.machineId && j.machineId !== params.machineId) {
                  return false;
                }
                if (params.status && j.status !== params.status) {
                  return false;
                }
                return true;
              })
              .slice(0, params.limit),
          ),

        loadJourney: (params) =>
          Effect.suspend(() => {
            const journey = journeys.get(params.journeyId);
            if (!journey) {
              return Effect.fail({
                _tag: WaypointErrorTag.JourneyNotFound,
                journeyId: params.journeyId,
                message: `Journey ${params.journeyId} not found`,
                timestamp: new Date().toISOString(),
              } satisfies JourneyNotFound);
            }
            return Effect.succeed(journey);
          }),

        saveJourney: (params) =>
          Effect.sync(() => {
            journeys.set(params.journey.id, params.journey);
          }),
      };
    });
```

---

## 2. Schema Integration

### 2.1 Schema for Waypoint Context Validation

Use Effect Schema with PAGE annotations (established pattern in codebase):

```typescript
import { Schema } from '@effect/schema';
import { PageSchema } from '@seed/page';

/**
 * Schema for session creation waypoint context.
 *
 * PAGE annotations provide descriptions and examples that flow to both
 * help output and error messages (declare once, derive everywhere).
 */
const SessionNameContextSchema = Schema.Struct({
  name: PageSchema.string({
    description: 'Session name in kebab-case format',
    examples: ['auth-refactor', 'feature-login'],
  }),
});

/**
 * Schema for session with focus area.
 */
const SessionWithFocusContextSchema = Schema.Struct({
  focus: PageSchema.string({
    description: 'Primary area of focus for this session',
    examples: ['debugging auth flow', 'implementing new feature'],
  }),
  name: PageSchema.string({
    description: 'Session name in kebab-case format',
    examples: ['auth-refactor', 'feature-login'],
  }),
  topics: PageSchema.optionalStringArray({
    description: 'Related topics for graph connectivity',
    examples: ['authentication', 'security'],
  }),
});

/**
 * Inferred types from schemas.
 * These are the source of truth - no manual type definitions.
 */
type SessionNameContext = Schema.Schema.Type<typeof SessionNameContextSchema>;
type SessionWithFocusContext = Schema.Schema.Type<typeof SessionWithFocusContextSchema>;
```

### 2.2 Schema for Event Payload Validation

Events also use schemas with PAGE annotations:

```typescript
/**
 * Event payload for providing session name.
 */
const ProvideNameEventSchema = Schema.Struct({
  name: PageSchema.string({
    description: 'Session name to use',
    examples: ['auth-refactor'],
  }),
}).pipe(
  Schema.filter((data) => /^[a-z0-9]+(-[a-z0-9]+)*$/.test(data.name), {
    message: () =>
      'name must be kebab-case (lowercase letters, numbers, hyphens only)',
  }),
);

/**
 * Event payload for providing focus area.
 */
const ProvideFocusEventSchema = Schema.Struct({
  focus: PageSchema.string({
    description: 'Focus area for the session',
    examples: ['debugging token refresh logic'],
  }),
  topics: PageSchema.optionalStringArray({
    description: 'Topics to link this session to',
    examples: ['authentication', 'debugging'],
  }),
});

type ProvideNameEvent = Schema.Schema.Type<typeof ProvideNameEventSchema>;
type ProvideFocusEvent = Schema.Schema.Type<typeof ProvideFocusEventSchema>;
```

### 2.3 Validation Effect with Error Transformation

Create a validation helper that transforms Schema errors into WaypointErrors:

```typescript
/**
 * Validate data against schema, returning Effect.
 *
 * Transforms Schema validation errors into WaypointError for consistent
 * error handling across the system.
 */
const validateWithSchema = <SchemaType, Input>(params: {
  readonly data: unknown;
  readonly schema: Schema.Schema<SchemaType, Input>;
  readonly schemaName: string;
  readonly journeyId: string | null;
}): Effect.Effect<SchemaType, ValidationError> =>
  Schema.decodeUnknown(params.schema)(params.data, { errors: 'all' }).pipe(
    Effect.mapError((parseError) => {
      const issues = ArrayFormatter.formatErrorSync(parseError);
      return validationError({
        fieldErrors: issues.map((issue) => ({
          expected: issue.message,
          message: issue.message,
          path: issue.path.join('.') || '(root)',
        })),
        journeyId: params.journeyId,
        schemaName: params.schemaName,
      });
    }),
  );
```

### 2.4 Waypoint Definition with Schema

Tie waypoints to their context schemas:

```typescript
/**
 * Define a waypoint with compile-time type safety.
 *
 * The schema serves as:
 * - Validation at runtime
 * - Type derivation at compile time
 * - Documentation via PAGE annotations
 */
const waypoint = <Tag extends string, ContextSchema extends Schema.Schema.Any>(
  params: {
    readonly tag: Tag;
    readonly schema: ContextSchema;
    readonly description: string;
    readonly terminal?: boolean;
    readonly onEntry?: () => Effect.Effect<void, WaypointError>;
    readonly onExit?: () => Effect.Effect<void, WaypointError>;
  },
): Waypoint<Tag, Schema.Schema.Type<ContextSchema>> => ({
  _tag: params.tag,
  description: params.description,
  onEntry: params.onEntry,
  onExit: params.onExit,
  schema: params.schema,
  terminal: params.terminal ?? false,
});
```

---

## 3. Service Architecture

### 3.1 Main WaypointService Interface

The public API uses a service pattern with explicit requirements:

```typescript
/**
 * Main waypoint service interface.
 *
 * All operations return Effects with explicit error types.
 * Requirements are expressed in the R parameter.
 */
interface WaypointService {
  /**
   * Start a new journey on a machine.
   */
  readonly start: <Machine extends MachineDefinition>(params: {
    readonly machine: Machine;
    readonly initialContext?: Machine['InitialContext'];
  }) => Effect.Effect<
    Journey<Machine['StateUnion'], Machine['ContextUnion']>,
    ValidationError | PersistenceError,
    WaypointPersistence | WaypointClock | WaypointIdGenerator
  >;

  /**
   * Send an event to a journey.
   */
  readonly send: <EventPayload>(params: {
    readonly journeyId: string;
    readonly event: EventPayload;
  }) => Effect.Effect<
    TransitionResult,
    | ValidationError
    | PersistenceError
    | JourneyNotFound
    | InvalidTransition
    | GuardRejection
    | ActionError,
    WaypointPersistence | WaypointClock
  >;

  /**
   * Resume a persisted journey.
   */
  readonly resume: (params: {
    readonly journeyId: string;
  }) => Effect.Effect<
    JourneySnapshot,
    PersistenceError | JourneyNotFound,
    WaypointPersistence
  >;

  /**
   * Query journeys by criteria.
   */
  readonly find: (params: {
    readonly machineId?: string;
    readonly status?: JourneyStatus;
    readonly limit?: number;
  }) => Effect.Effect<
    ReadonlyArray<JourneySummary>,
    PersistenceError,
    WaypointPersistence
  >;

  /**
   * Replay events to reconstruct state (for event sourcing).
   */
  readonly replay: (params: {
    readonly journeyId: string;
  }) => Effect.Effect<
    JourneySnapshot,
    PersistenceError | JourneyNotFound | ActionError,
    WaypointPersistence
  >;
}

/**
 * Tag for WaypointService.
 */
const WaypointService = Context.GenericTag<WaypointService>(
  '@seed/waypoint/WaypointService',
);
```

### 3.2 Service Implementation Layer

```typescript
/**
 * Create the live WaypointService layer.
 *
 * Requires persistence, clock, and ID generator layers.
 */
const LiveWaypointService: Layer.Layer<
  WaypointService,
  never,
  WaypointPersistence | WaypointClock | WaypointIdGenerator
> = Layer.effect(
  WaypointService,
  Effect.gen(function* () {
    const persistence = yield* WaypointPersistence;
    const clock = yield* WaypointClock;
    const idGen = yield* WaypointIdGenerator;

    return {
      find: (params) =>
        persistence.listJourneys({
          limit: params.limit ?? 100,
          machineId: params.machineId ?? null,
          status: params.status ?? null,
        }),

      replay: (params) =>
        Effect.gen(function* () {
          const journey = yield* persistence.loadJourney({
            journeyId: params.journeyId,
          });
          // Event replay logic would go here
          return journey;
        }),

      resume: (params) =>
        persistence.loadJourney({ journeyId: params.journeyId }),

      send: (params) =>
        Effect.gen(function* () {
          const journey = yield* persistence.loadJourney({
            journeyId: params.journeyId,
          });
          const now = yield* clock.now();

          // Find valid transition
          // Execute guard
          // Run action
          // Persist new state
          // Return result

          // Placeholder for actual implementation
          return {
            newContext: {},
            newState: journey.currentState,
            success: true,
          } as TransitionResult;
        }),

      start: (params) =>
        Effect.gen(function* () {
          const id = yield* idGen.generateId();
          const now = yield* clock.now();

          // Validate initial context against schema
          // Create journey record
          // Persist
          // Return journey

          const journey: Journey<unknown, unknown> = {
            context: params.initialContext ?? {},
            createdAt: now,
            currentState: params.machine.initial,
            id,
            machineId: params.machine.id,
            status: JourneyStatus.Active,
            updatedAt: now,
          };

          yield* persistence.saveJourney({ journey });

          return journey;
        }),
    };
  }),
);
```

### 3.3 Composing Layers for Production and Testing

```typescript
/**
 * Full production layer stack.
 */
const ProductionLayers = (params: { readonly dbPath: string }) =>
  Layer.mergeAll(
    LiveClock,
    LiveIdGenerator,
    makeSqlitePersistence({ dbPath: params.dbPath }),
  ).pipe(Layer.provide(LiveWaypointService));

/**
 * Test layer stack with deterministic behavior.
 */
const TestLayers = (params: {
  readonly fixedTime: string;
  readonly ids: ReadonlyArray<string>;
}) =>
  Layer.mergeAll(
    makeTestClock({ fixedTime: params.fixedTime }),
    makeTestIdGenerator({ ids: params.ids }),
    makeInMemoryPersistence(),
  ).pipe(Layer.provide(LiveWaypointService));

/**
 * Example: running in production.
 */
const runProduction = () =>
  Effect.gen(function* () {
    const service = yield* WaypointService;
    const journey = yield* service.start({
      machine: sessionFlowMachine,
    });
    return journey;
  }).pipe(
    Effect.provide(ProductionLayers({ dbPath: '.waypoint.db' })),
    Effect.runPromise,
  );

/**
 * Example: running in tests.
 */
const runTest = () =>
  Effect.gen(function* () {
    const service = yield* WaypointService;
    const journey = yield* service.start({
      machine: sessionFlowMachine,
    });

    // Time and IDs are deterministic!
    expect(journey.id).toBe('test-id-001');
    expect(journey.createdAt).toBe('2026-01-17T12:00:00Z');
  }).pipe(
    Effect.provide(
      TestLayers({
        fixedTime: '2026-01-17T12:00:00Z',
        ids: ['test-id-001', 'test-id-002'],
      }),
    ),
    Effect.runPromise,
  );
```

---

## 4. Stream Patterns

### 4.1 Event Replay from Persistence

```typescript
import { Stream } from 'effect';

/**
 * Stream all events for a journey in chronological order.
 *
 * Useful for:
 * - Rebuilding state from event log
 * - Auditing what happened
 * - Debugging transition issues
 */
const streamEvents = (params: {
  readonly journeyId: string;
}): Stream.Stream<EventRecord, PersistenceError, WaypointPersistence> =>
  Stream.unwrap(
    Effect.gen(function* () {
      const persistence = yield* WaypointPersistence;
      // Assuming persistence has a method to iterate events
      const events = yield* persistence.loadEvents({
        journeyId: params.journeyId,
      });
      return Stream.fromIterable(events);
    }),
  );

/**
 * Replay events to rebuild journey state.
 *
 * Uses Stream.runFold to process events sequentially,
 * applying each transition to rebuild final state.
 */
const replayJourney = <Machine extends MachineDefinition>(params: {
  readonly journeyId: string;
  readonly machine: Machine;
}): Effect.Effect<
  JourneySnapshot,
  PersistenceError | ActionError,
  WaypointPersistence
> =>
  streamEvents({ journeyId: params.journeyId }).pipe(
    Stream.runFold(
      {
        context: params.machine.initialContext,
        state: params.machine.initial,
      },
      (acc, event) =>
        // Apply transition for each event
        applyTransition({
          context: acc.context,
          event: event.payload,
          machine: params.machine,
          state: acc.state,
        }),
    ),
    Effect.map((final) => ({
      context: final.context,
      createdAt: '', // Would come from first event
      currentState: final.state,
      id: params.journeyId,
      machineId: params.machine.id,
      status: JourneyStatus.Active,
      updatedAt: '', // Would come from last event
    })),
  );
```

### 4.2 Subscription to State Changes

```typescript
import { PubSub, Queue } from 'effect';

/**
 * State change event emitted on each transition.
 */
interface StateChangeEvent {
  readonly journeyId: string;
  readonly previousState: string;
  readonly newState: string;
  readonly event: EventRecord;
  readonly timestamp: string;
}

/**
 * State change publisher service.
 */
interface WaypointPubSub {
  readonly publish: (
    event: StateChangeEvent,
  ) => Effect.Effect<boolean>;

  readonly subscribe: () => Effect.Effect<
    Queue.Dequeue<StateChangeEvent>,
    never,
    Scope.Scope
  >;
}

const WaypointPubSub = Context.GenericTag<WaypointPubSub>(
  '@seed/waypoint/WaypointPubSub',
);

/**
 * Create the pub/sub layer.
 */
const LiveWaypointPubSub: Layer.Layer<WaypointPubSub> = Layer.scoped(
  WaypointPubSub,
  Effect.gen(function* () {
    const pubsub = yield* PubSub.unbounded<StateChangeEvent>();

    return {
      publish: (event) => PubSub.publish(pubsub, event),
      subscribe: () => PubSub.subscribe(pubsub),
    };
  }),
);

/**
 * Stream state changes for a specific journey.
 *
 * Filters pub/sub events to only those matching the journey ID.
 */
const watchJourney = (params: {
  readonly journeyId: string;
}): Stream.Stream<StateChangeEvent, never, WaypointPubSub | Scope.Scope> =>
  Stream.unwrap(
    Effect.gen(function* () {
      const pubsub = yield* WaypointPubSub;
      const queue = yield* pubsub.subscribe();

      return Stream.fromQueue(queue).pipe(
        Stream.filter((event) => event.journeyId === params.journeyId),
      );
    }),
  );

/**
 * Stream all state changes across all journeys.
 *
 * Useful for:
 * - Global monitoring dashboard
 * - Metrics collection
 * - Audit logging
 */
const watchAll =
  (): Stream.Stream<StateChangeEvent, never, WaypointPubSub | Scope.Scope> =>
    Stream.unwrap(
      Effect.gen(function* () {
        const pubsub = yield* WaypointPubSub;
        const queue = yield* pubsub.subscribe();
        return Stream.fromQueue(queue);
      }),
    );
```

### 4.3 Backpressure for High-Frequency Events

```typescript
/**
 * Bounded queue for backpressure control.
 *
 * When queue is full, publishers wait (applying backpressure).
 */
const BoundedWaypointPubSub = (params: {
  readonly capacity: number;
}): Layer.Layer<WaypointPubSub> =>
  Layer.scoped(
    WaypointPubSub,
    Effect.gen(function* () {
      // Bounded PubSub applies backpressure when capacity reached
      const pubsub = yield* PubSub.bounded<StateChangeEvent>(params.capacity);

      return {
        publish: (event) => PubSub.publish(pubsub, event),
        subscribe: () => PubSub.subscribe(pubsub),
      };
    }),
  );

/**
 * Sliding window strategy - drop oldest when full.
 *
 * For scenarios where latest data matters more than completeness.
 */
const SlidingWaypointPubSub = (params: {
  readonly capacity: number;
}): Layer.Layer<WaypointPubSub> =>
  Layer.scoped(
    WaypointPubSub,
    Effect.gen(function* () {
      const pubsub = yield* PubSub.sliding<StateChangeEvent>(params.capacity);

      return {
        publish: (event) => PubSub.publish(pubsub, event),
        subscribe: () => PubSub.subscribe(pubsub),
      };
    }),
  );

/**
 * Dropping strategy - drop new events when full.
 *
 * For scenarios where we can afford to miss some events.
 */
const DroppingWaypointPubSub = (params: {
  readonly capacity: number;
}): Layer.Layer<WaypointPubSub> =>
  Layer.scoped(
    WaypointPubSub,
    Effect.gen(function* () {
      const pubsub = yield* PubSub.dropping<StateChangeEvent>(params.capacity);

      return {
        publish: (event) => PubSub.publish(pubsub, event),
        subscribe: () => PubSub.subscribe(pubsub),
      };
    }),
  );
```

---

## 5. Complete Machine Definition Example

Putting it all together with a session creation flow:

```typescript
import { Effect, Schema } from 'effect';
import { PageSchema } from '@seed/page';

// ============================================================================
// State Tags (Enum for discriminator)
// ============================================================================

enum SessionFlowState {
  AskName = 'ask-name',
  AskFocus = 'ask-focus',
  Confirm = 'confirm',
  Created = 'created',
  Cancelled = 'cancelled',
}

// ============================================================================
// Event Tags (Enum for discriminator)
// ============================================================================

enum SessionFlowEvent {
  ProvideName = 'provide-name',
  ProvideFocus = 'provide-focus',
  Confirm = 'confirm',
  Cancel = 'cancel',
  GoBack = 'go-back',
}

// ============================================================================
// Context Schemas
// ============================================================================

const EmptyContextSchema = Schema.Struct({});

const WithNameContextSchema = Schema.Struct({
  name: PageSchema.string({
    description: 'Session name',
    examples: ['auth-refactor'],
  }),
});

const WithFocusContextSchema = Schema.Struct({
  focus: PageSchema.string({
    description: 'Session focus area',
    examples: ['debugging token refresh'],
  }),
  name: PageSchema.string({
    description: 'Session name',
    examples: ['auth-refactor'],
  }),
});

const CreatedContextSchema = Schema.Struct({
  createdAt: PageSchema.string({
    description: 'Creation timestamp',
    examples: ['2026-01-17T12:00:00Z'],
  }),
  focus: PageSchema.string({
    description: 'Session focus area',
    examples: ['debugging token refresh'],
  }),
  name: PageSchema.string({
    description: 'Session name',
    examples: ['auth-refactor'],
  }),
  sessionId: PageSchema.string({
    description: 'Generated session ID',
    examples: ['01ABC123...'],
  }),
});

// ============================================================================
// Event Payload Schemas
// ============================================================================

const ProvideNamePayloadSchema = Schema.Struct({
  name: PageSchema.string({
    description: 'Session name to use',
    examples: ['auth-refactor'],
  }),
});

const ProvideFocusPayloadSchema = Schema.Struct({
  focus: PageSchema.string({
    description: 'Focus area',
    examples: ['debugging'],
  }),
});

// ============================================================================
// Waypoints
// ============================================================================

const askNameWaypoint = waypoint({
  description: 'Gathering session name from user',
  schema: EmptyContextSchema,
  tag: SessionFlowState.AskName,
});

const askFocusWaypoint = waypoint({
  description: 'Gathering focus area for the session',
  schema: WithNameContextSchema,
  tag: SessionFlowState.AskFocus,
});

const confirmWaypoint = waypoint({
  description: 'Confirming session details before creation',
  schema: WithFocusContextSchema,
  tag: SessionFlowState.Confirm,
});

const createdWaypoint = waypoint({
  description: 'Session successfully created',
  schema: CreatedContextSchema,
  tag: SessionFlowState.Created,
  terminal: true,
});

const cancelledWaypoint = waypoint({
  description: 'Session creation cancelled',
  schema: EmptyContextSchema,
  tag: SessionFlowState.Cancelled,
  terminal: true,
});

// ============================================================================
// Routes
// ============================================================================

const provideNameRoute = route({
  action: (params) =>
    Effect.succeed({
      name: params.event.name,
    }),
  eventSchema: ProvideNamePayloadSchema,
  from: SessionFlowState.AskName,
  on: SessionFlowEvent.ProvideName,
  to: SessionFlowState.AskFocus,
});

const provideFocusRoute = route({
  action: (params) =>
    Effect.succeed({
      focus: params.event.focus,
      name: params.context.name,
    }),
  eventSchema: ProvideFocusPayloadSchema,
  from: SessionFlowState.AskFocus,
  on: SessionFlowEvent.ProvideFocus,
  to: SessionFlowState.Confirm,
});

const confirmRoute = route({
  action: (params) =>
    Effect.gen(function* () {
      const clock = yield* WaypointClock;
      const idGen = yield* WaypointIdGenerator;
      const now = yield* clock.now();
      const sessionId = yield* idGen.generateId();

      return {
        createdAt: now,
        focus: params.context.focus,
        name: params.context.name,
        sessionId,
      };
    }),
  eventSchema: Schema.Struct({}),
  from: SessionFlowState.Confirm,
  on: SessionFlowEvent.Confirm,
  to: SessionFlowState.Created,
});

const goBackRoute = route({
  action: (params) =>
    Effect.succeed({
      name: params.context.name,
    }),
  eventSchema: Schema.Struct({}),
  from: SessionFlowState.Confirm,
  on: SessionFlowEvent.GoBack,
  to: SessionFlowState.AskFocus,
});

const cancelRoute = route({
  action: () => Effect.succeed({}),
  eventSchema: Schema.Struct({}),
  from: SessionFlowState.AskName,
  on: SessionFlowEvent.Cancel,
  to: SessionFlowState.Cancelled,
});

// ============================================================================
// Machine Definition
// ============================================================================

const sessionFlowMachine = machine({
  id: 'session-creation',
  initial: SessionFlowState.AskName,
  routes: [
    provideNameRoute,
    provideFocusRoute,
    confirmRoute,
    goBackRoute,
    cancelRoute,
  ],
  terminal: [SessionFlowState.Created, SessionFlowState.Cancelled],
  waypoints: [
    askNameWaypoint,
    askFocusWaypoint,
    confirmWaypoint,
    createdWaypoint,
    cancelledWaypoint,
  ],
});
```

---

## 6. Testing Patterns

### 6.1 Unit Testing with Mock Layers

```typescript
import { describe, expect, test } from 'bun:test';

describe('SessionFlowMachine', () => {
  const testLayers = TestLayers({
    fixedTime: '2026-01-17T12:00:00Z',
    ids: ['journey-001', 'session-001'],
  });

  test('complete flow from name to created', async () => {
    const program = Effect.gen(function* () {
      const service = yield* WaypointService;

      // Start journey
      const journey = yield* service.start({
        machine: sessionFlowMachine,
      });
      expect(journey.currentState).toBe(SessionFlowState.AskName);

      // Provide name
      const afterName = yield* service.send({
        event: { _tag: SessionFlowEvent.ProvideName, name: 'auth-refactor' },
        journeyId: journey.id,
      });
      expect(afterName.newState).toBe(SessionFlowState.AskFocus);

      // Provide focus
      const afterFocus = yield* service.send({
        event: { _tag: SessionFlowEvent.ProvideFocus, focus: 'debugging' },
        journeyId: journey.id,
      });
      expect(afterFocus.newState).toBe(SessionFlowState.Confirm);

      // Confirm
      const afterConfirm = yield* service.send({
        event: { _tag: SessionFlowEvent.Confirm },
        journeyId: journey.id,
      });
      expect(afterConfirm.newState).toBe(SessionFlowState.Created);
      expect(afterConfirm.context.sessionId).toBe('session-001');
      expect(afterConfirm.context.createdAt).toBe('2026-01-17T12:00:00Z');
    });

    await Effect.runPromise(Effect.provide(program, testLayers));
  });

  test('invalid transition returns error', async () => {
    const program = Effect.gen(function* () {
      const service = yield* WaypointService;

      const journey = yield* service.start({
        machine: sessionFlowMachine,
      });

      // Try to confirm without providing name (invalid)
      const result = yield* Effect.either(
        service.send({
          event: { _tag: SessionFlowEvent.Confirm },
          journeyId: journey.id,
        }),
      );

      expect(result._tag).toBe('Left');
      if (result._tag === 'Left') {
        expect(result.left._tag).toBe(WaypointErrorTag.InvalidTransition);
      }
    });

    await Effect.runPromise(Effect.provide(program, testLayers));
  });
});
```

### 6.2 Integration Testing with Isolated Context

Following `docs/references/test-isolation.md`:

```typescript
import { createTestContext, type TestContext } from '@tests/lib/isolation';

describe('WaypointService Integration', () => {
  let ctx: TestContext;

  beforeEach(async () => {
    ctx = await createTestContext('waypoint');
  });

  afterEach(async () => {
    await ctx.cleanup();
  });

  test('persists journey to SQLite', async () => {
    const dbPath = join(ctx.cwd, 'test.db');

    const productionLayers = ProductionLayers({ dbPath });

    const program = Effect.gen(function* () {
      const service = yield* WaypointService;

      const journey = yield* service.start({
        machine: sessionFlowMachine,
      });

      // Verify persistence
      const loaded = yield* service.resume({
        journeyId: journey.id,
      });

      expect(loaded.id).toBe(journey.id);
      expect(loaded.currentState).toBe(SessionFlowState.AskName);
    });

    await Effect.runPromise(Effect.provide(program, productionLayers));

    // Verify file was created
    expect(existsSync(dbPath)).toBe(true);
  });
});
```

---

## 7. Summary of Recommendations

### 7.1 Transition Composition

- Use `Effect.Effect<ToContext, TransitionError, Requirements>` return type
- Define error hierarchy with enum discriminators (`WaypointErrorTag`)
- Provide constructor functions for each error type

### 7.2 Schema Integration

- Use Effect Schema with PAGE annotations (established pattern)
- Derive types from schemas (`Schema.Schema.Type<typeof MySchema>`)
- Create `validateWithSchema` helper that transforms to WaypointError

### 7.3 Service Architecture

- Define services as interfaces with Context tags
- Use `Layer.effect` for implementations with dependencies
- Provide `TestLayers` factory for deterministic testing

### 7.4 Stream Patterns

- Use `Stream.fromIterable` for event replay
- Use `PubSub` for subscription/notification
- Choose backpressure strategy based on use case (bounded, sliding, dropping)

### 7.5 Codebase Alignment

- Single parameter objects for 2+ params
- Enum discriminators (no string literals)
- Exports at bottom of file
- PAGE annotations for all user-facing schemas
- `createTestContext` for integration tests

---

## 8. Next Steps

1. [ ] Review this document with the team
2. [ ] Prototype core types in `packages/waypoint/lib/types.ts`
3. [ ] Implement persistence layer with SQLite
4. [ ] Create first machine (session creation flow)
5. [ ] Add comprehensive test suite
6. [ ] Document public API

---

## Exports

```typescript
export {
  // Error types
  actionError,
  guardRejection,
  invalidTransition,
  journeyNotFound,
  persistenceError,
  validationError,
  WaypointErrorTag,
  type ActionError,
  type GuardRejection,
  type InvalidTransition,
  type JourneyNotFound,
  type PersistenceError,
  type ValidationError,
  type WaypointError,
  // Services
  LiveWaypointService,
  WaypointClock,
  WaypointIdGenerator,
  WaypointPersistence,
  WaypointPubSub,
  WaypointService,
  // Layers
  BoundedWaypointPubSub,
  DroppingWaypointPubSub,
  LiveClock,
  LiveIdGenerator,
  LiveWaypointPubSub,
  makeInMemoryPersistence,
  makeSqlitePersistence,
  makeTestClock,
  makeTestIdGenerator,
  ProductionLayers,
  SlidingWaypointPubSub,
  TestLayers,
  // Helpers
  machine,
  replayJourney,
  route,
  streamEvents,
  validateWithSchema,
  watchAll,
  watchJourney,
  waypoint,
};
```
