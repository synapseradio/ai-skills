# Waypoint Idea: Research

**Status**: Incomplete
**Questions Addressed**: Q4 (Event queuing during transition) and Q5 (Recovery protocol for mid-action crashes)

---

## Q4: Event Queuing During Transition

**Question**: If an event arrives while a transition's action is executing, what happens?

- Option A: Queue the event, process after transition completes
- Option B: Reject the event (caller must retry)
- Option C: Buffer with configurable limit

### Research Summary

#### XState/Actor Model Pattern

XState v5 implements the actor model where each actor uses a **mailbox** (FIFO queue) for incoming events:

> "During a transition—when an action (synchronous or asynchronous) is running—new events are **queued in the mailbox and processed sequentially after the current action and transition complete**."

Key mechanics from SCXML specification:

1. **Run-to-completion semantics**: Each event triggers a full, atomic execution cycle
2. **Mailbox queuing**: Events are buffered without blocking senders
3. **Sequential processing**: One event at a time; no interleaving
4. **Determinism**: All code related to one event executes before the next event dequeues

**Source**: [Stately.ai Actors Documentation](https://stately.ai/docs/actors), [SCXML W3C Specification Section 5](https://www.w3.org/TR/scxml/)

#### CLI-Specific Considerations

CLI invocations have fundamentally different execution characteristics:

| Aspect | Long-running Actor | CLI Invocation |
|--------|-------------------|----------------|
| Lifetime | Persistent process | Single execution |
| Event sources | Multiple concurrent | Single caller (user/agent) |
| Concurrency | Async, overlapping | Blocking, synchronous |
| Process model | Mailbox with queue | Arguments → output |

For a CLI:

- **Each invocation is atomic**: The process starts, executes the transition, and exits
- **No concurrent events**: Only one event (the CLI arguments) is processed per invocation
- **No queue needed for single-region flows**: Events cannot "arrive during" a transition because there's no concurrent event source

However, **parallel regions change this**: When a coordinator journey has multiple regions, regions may complete and emit events while the coordinator is mid-transition. This is the only scenario where queuing matters.

### Recommendation: Option A (Queue) for Parallel Regions Only

**Proposed Answer**:

1. **Single-region flows**: No queuing required. The CLI model is inherently run-to-completion. Each invocation handles one event synchronously.

2. **Parallel regions**: Queue events from regions that complete during coordinator transitions. Process queued events after coordinator transition completes.

**Implementation Strategy**:

```typescript
// For single-region: no queue, direct execution
const result = await transition({ event, context });

// For parallel regions: queue with FIFO ordering
interface RegionEventQueue {
  readonly enqueue: (event: RegionEvent) => Effect.Effect<void>;
  readonly drainAfterTransition: () => Effect.Effect<ReadonlyArray<RegionEvent>>;
}
```

**Rationale**:

- **Simplest correct solution**: Single-region flows (MVP, Phase 1) need no queuing infrastructure
- **Deferred complexity**: Queuing only added when parallel regions are implemented (Phase 3)
- **SCXML-compliant**: Follows established actor model semantics for the cases that need it
- **CLI-native**: Respects the synchronous, blocking nature of CLI execution

### CLI-Specific Considerations

1. **Atomic invocations**: Each `waypoint send` call is a complete transaction
2. **No orphaned events**: If process crashes before queue is drained, events are lost (acceptable for CLI—caller retries)
3. **Parallel region coordination**: Regions persist events to SQLite before emitting; coordinator reads from persistence, not in-memory queue

### Confidence: High

The research clearly shows XState's queuing is designed for concurrent/async contexts. CLI flows are neither. The exception (parallel regions) can adopt the proven mailbox pattern when needed.

### Sources

1. [Stately.ai Actions Documentation](https://stately.ai/docs/actions)
2. [Stately.ai Actors Documentation](https://stately.ai/docs/actors)
3. [XState GitHub Issue #2870 - Mailbox Optimization](https://github.com/statelyai/xstate/issues/2870)
4. [SCXML W3C Specification - Execution Model](https://www.w3.org/TR/scxml/#AlgorithmforSCXMLInterpretation)
5. [MentorCruise - Understanding the Actor Model](https://mentorcruise.com/blog/understanding-the-actor-model/)

---

## Q5: Recovery Protocol for Mid-Action Crashes

**Question**: If the process crashes during an action (after guard passed, before state update), what's the recovery contract?

- Option A: Actions must be idempotent; replay is safe
- Option B: Journal-style: mark "transition-started", complete after
- Option C: Two-phase: "prepare" then "commit"

### Research Summary

#### Temporal.io Approach: Deterministic Replay with Event Sourcing

Temporal's workflow engine provides crash recovery through:

1. **Event history**: Complete log of all workflow events persisted durably
2. **Deterministic replay**: On crash, re-execute workflow code from start, using event history to fast-forward
3. **Activity idempotency**: Activities execute at-least-once; must be idempotent to handle retries

> "Workflow code must be **deterministic**—produce identical commands from the same event history during replay."

**Key insight**: Activities (external effects) are separate from workflow logic. Activities may fail and retry; workflow logic deterministically coordinates them.

**Source**: [Temporal Idempotency Blog](https://temporal.io/blog/idempotency-and-durable-execution), [Temporal Workflow Documentation](https://docs.temporal.io/workflows)

#### Event Sourcing Pattern

Event sourcing handles mid-transaction failures by:

1. **Write-ahead logging**: Events written to log before applying to state
2. **Crash recovery**: Replay events from log to rebuild state
3. **Partial transaction handling**: Uncommitted transactions are discarded; committed ones replayed idempotently

> "If failure occurs before appending the event to the log, the transaction aborts cleanly—no partial state."

**Source**: [Microsoft Event Sourcing Sample](https://learn.microsoft.com/en-us/samples/azure-samples/cosmos-db-design-patterns/event-sourcing/)

#### Saga Pattern: Compensating Transactions

Sagas manage distributed transactions through:

1. **Local transactions**: Each step is atomic within its service
2. **Compensating transactions**: Reversal steps undo changes if later steps fail
3. **Orchestration or choreography**: Central coordinator or event-driven coordination

> "Compensating transactions are reversal steps designed to undo changes made by previous steps if a failure occurs."

**Source**: [Microservices.io Saga Pattern](https://microservices.io/patterns/data/saga.html), [Temporal Saga Blog](https://temporal.io/blog/mastering-saga-patterns-for-distributed-transactions-in-microservices)

#### SQLite WAL Guarantees

SQLite's Write-Ahead Logging provides:

1. **Atomic transactions**: All-or-nothing via WAL frames with checksums
2. **Crash recovery**: On restart, replay WAL to rebuild state; uncommitted frames discarded
3. **Durability**: Committed changes survive crashes

> "Changes are appended to the WAL file atomically per frame, with checksums for integrity."

**Source**: [SQLite WAL Format](https://sqlite.org/walformat.html), [SQLite Temporary Files](https://www.sqlite.org/tempfiles.html)

#### Two-Phase Commit

2PC provides atomic distributed transactions:

1. **Prepare phase**: All participants write tentative changes to durable log, vote YES/NO
2. **Commit phase**: If all YES, commit; if any NO, abort
3. **Recovery**: On crash, replay decision log; participants poll coordinator for unresolved decisions

**Downside for CLI**: 2PC requires coordination between distributed parties. A single CLI process has no "distributed" aspect until parallel regions are introduced.

**Source**: [AlgoMaster - Two-Phase Commit](https://algomaster.io/learn/system-design/two-phase-commit-protocol)

### Recommendation: Option A (Idempotent Actions) with SQLite Transactional Guarantee

**Proposed Answer**: **Option A with refinement**—actions must be idempotent, but SQLite transactions provide the atomicity guarantee that makes this tractable.

**Implementation Strategy**:

```typescript
// Single SQLite transaction wraps entire transition
await db.transaction(async (tx) => {
  // 1. Execute action (may have side effects)
  const newContext = await executeAction({ context, event });

  // 2. Persist event to log
  await tx.insert(events, {
    journeyId,
    eventTag: event._tag,
    priorState: currentState,
    resultingState: newState,
    sequence: journey.eventSequence + 1,
  });

  // 3. Update journey snapshot
  await tx.update(journeys, {
    currentStateTag: newState._tag,
    context: newContext,
    eventSequence: journey.eventSequence + 1,
    updatedAt: now,
  });
});
// Either all succeed or none do
```

**Recovery Contract**:

1. **Crash before transaction commit**: No state change persisted. On resume, journey is at prior state. Caller retries the event.

2. **Crash after transaction commit**: State change is durable. On resume, journey shows new state.

3. **Action idempotency requirement**: Actions that have external effects (API calls, file writes) must be idempotent. If a crash occurs after the external effect but before SQLite commit, the action will be retried on resume.

**Idempotency Strategies for Actions**:

| Effect Type | Idempotency Strategy |
|-------------|----------------------|
| **Validation** | Naturally idempotent |
| **Context transformation** | Naturally idempotent (pure function) |
| **File creation** | Use deterministic paths; overwrite-safe operations |
| **API calls** | Idempotency keys or check-before-write patterns |
| **Database writes** | SQLite transaction handles this |

**Why Not Option B (Journal-Style)?**

Journal-style adds complexity:

1. Requires additional "transition-started" record
2. Recovery must detect incomplete transitions and either complete or rollback
3. Increases transaction scope and potential failure modes

For CLI use cases, this is overkill. SQLite's ACID guarantees provide sufficient atomicity. The action either completes fully (committed) or not at all (rollback).

**Why Not Option C (Two-Phase)?**

Two-phase commit is designed for distributed transactions across multiple databases/services. A CLI with SQLite persistence is not distributed. 2PC adds coordination overhead without benefit.

### CLI-Specific Considerations

1. **Process model**: CLI process may be killed at any time (Ctrl+C, OOM, system crash)

2. **Resume is explicit**: User/agent must call `waypoint resume <journey-id>` to continue. There's no automatic recovery daemon.

3. **SQLite is the durability layer**: All crash safety guarantees flow from SQLite's WAL. No additional journaling needed.

4. **Action scope**: Keep actions small. Large actions increase the window for crashes. Prefer multiple small transitions over one large action.

5. **External effects**: Document idempotency requirements for action authors. Consider providing helpers:

```typescript
// Helper for idempotent file writes
const idempotentWrite = (params: {
  readonly path: string;
  readonly content: string;
  readonly checksum: string;
}) => Effect.gen(function* () {
  const existing = yield* readFileIfExists(params.path);
  if (existing && hash(existing) === params.checksum) {
    return; // Already written, skip
  }
  yield* writeFile(params.path, params.content);
});
```

### Confidence: High

The research strongly supports Option A:

1. **Temporal uses it**: Industry-leading workflow engine requires action idempotency
2. **Event sourcing assumes it**: The pattern's recovery model depends on replayable operations
3. **SQLite provides atomicity**: No need for custom journaling when the database handles it
4. **CLI-appropriate**: Simple, understandable, testable

The only caveat is documenting idempotency requirements for action authors and providing utilities to make idempotent actions easy to write.

### Sources

1. [Temporal - Understanding Idempotency in Distributed Systems](https://temporal.io/blog/idempotency-and-durable-execution)
2. [Temporal - Error Handling in Distributed Systems](https://temporal.io/blog/error-handling-in-distributed-systems)
3. [Temporal - Workflow Execution Documentation](https://docs.temporal.io/workflow-execution)
4. [Microservices.io - Saga Pattern](https://microservices.io/patterns/data/saga.html)
5. [AWS - Saga Orchestration Pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-orchestration.html)
6. [SQLite - Write-Ahead Logging Format](https://sqlite.org/walformat.html)
7. [SQLite - How to Corrupt a Database](https://www.sqlite.org/howtocorrupt.html)
8. [AlgoMaster - Two-Phase Commit Protocol](https://algomaster.io/learn/system-design/two-phase-commit-protocol)

---

## Summary: Recommended Answers

### Q4: Event Queuing

**Answer**: **Option A (Queue)** for parallel regions only.

- Single-region flows: No queuing (CLI is inherently atomic)
- Parallel regions: FIFO queue for events from completed regions, drained after coordinator transition

### Q5: Recovery Protocol

**Answer**: **Option A (Idempotent Actions)** with SQLite transactional guarantee.

- SQLite transaction wraps event log append + snapshot update
- Actions with external effects must be idempotent
- Recovery contract: crash before commit = retry event; crash after commit = proceed from new state

---

## Integration with Functional Spec

These answers affect the following sections:

1. **Section 3.3 (Transaction Guarantees)**: Already aligned. The spec's pseudocode shows atomic event + snapshot writes.

2. **Section 4 (Effect-TS Integration)**: Add idempotency documentation for action authors.

3. **Section 5 (Parallel Regions)**: Add event queue mechanics for region → coordinator events.

4. **New Section**: Consider adding "Recovery Contract" section explicitly stating:
   - Actions must be idempotent when they have external effects
   - SQLite provides atomicity for persistence operations
   - Resume always sees consistent state (either pre- or post-transition, never mid-)

---

## Open Questions Surfaced

1. **Should waypoint provide idempotency helpers?** (e.g., `Waypoint.idempotent()` wrapper that checks for prior completion)

2. **How to test idempotency?** TestLayers should support simulating crashes and verifying replay safety.

3. **What's the guidance for action timeout?** If an action hangs indefinitely, the CLI process may be killed. Should there be a timeout mechanism?
