---
status: active
created: 2025-01-17
---

# Waypoint: State Machine Infrastructure for Agent-Interfacing CLIs

## Glossary: Core Concepts

These terms form the bedrock vocabulary for Waypoint. Each is defined by what you can *do* with it, not just what it *is*.

| Term | Definition | Practical Use | Composes With |
|------|------------|---------------|---------------|
| **Waypoint** | A discrete state with a typed context schema | Define what data exists at each step; validate presence | Routes (as endpoints) |
| **Route** | A transition between waypoints triggered by an event | Define valid moves with guards (conditions) and actions (transformations) | Waypoints (connects them) |
| **Journey** | A running instance traversing waypoints | Start, send events, resume after interruption | Map (instantiates it) |
| **Map** | Complete flow definition: waypoints + routes + initial + terminal | Define a workflow declaratively; derive from code | Journeys (creates them) |
| **Context** | Typed data accumulated through a journey | Schema-validated state that grows as journey progresses | Waypoints (each has one) |
| **Event** | Named trigger with typed payload | Drive transitions; the "commands" sent to journeys | Routes (triggers them) |
| **Guard** | Condition that must pass for transition | Validate before moving; return boolean or validation errors | Routes (gates them) |
| **Action** | Effect that transforms context during transition | Do work, update state, persist resources | Routes (executes on them) |
| **Region** | Independent state within a parallel journey | Multi-agent coordination; isolated state per participant | Journey (contains them) |

---

## The Problem We're Solving

Current CLI commands in this repo (like `journal write note`) follow a pattern:

1. Parse arguments
2. Validate inputs against schema
3. Perform operation (often with persistence)
4. Return PAGE-formatted output

This works for single-step operations. But what about multi-step flows?

**Example: A guided session creation flow**

```
1. User starts: `journal session create`
2. System asks: "What's the session name?"
3. User provides: "auth-refactor"
4. System asks: "Initial focus area?"
5. User provides: "Token refresh logic"
6. System creates session with context
```

Currently, this would require either:

- A single command with many flags (poor DX)
- Multiple separate commands (loses context)
- Interactive prompts without state persistence (can't resume)

**The gap**: We lack infrastructure for **stateful, multi-step CLI workflows** that:

- Persist state between steps (resume after interruption)
- Guide agents through valid paths (PAGE protocol)
- Validate at each step (Effect/Schema)
- Compose into larger flows

---

## First Principles: What Are We Really Building?

### Principle 1: A CLI flow is a navigation through state space

When an agent runs a multi-step command, they're navigating a graph:

- **Nodes** = states (what information has been gathered)
- **Edges** = transitions (valid next steps)
- **Position** = current state + accumulated context

This is literally what state machines model.

### Principle 2: PAGE protocol already describes navigation

PAGE's CAID pattern maps directly to state machine semantics:

- **Confirm** → "You are in state X"
- **Affirm** → "You provided valid transition inputs Y"
- **Inform** → "To proceed to state Z, do W"
- **Dial** → "Available transitions from here: [...]"

The insight: PAGE is already a state machine communication protocol. We need the state machine to back it.

### Principle 3: Agents need GPS, not just maps

Traditional CLIs show what's possible (the map). Agents need:

- Where they are (current state)
- How they got there (path taken)
- Where they can go (valid transitions)
- How to get to their goal (navigation)

This is the GUIDE principle: Goal-oriented Usage Information through Directed Engagement.

### Principle 4: State machines should be data, not code

XState's key insight: state machines as serializable data structures enable:

- Visualization
- Persistence
- Analysis
- Code generation

We want the same—define machines declaratively, derive behavior.

### Principle 5: Effect composition over inheritance

Effect-TS pattern: instead of class hierarchies, compose small effects:

- Validation is an effect
- Persistence is an effect
- Logging is an effect

State transitions are effects that can compose.

---

## CLI-First, FSM-as-Infrastructure

### The Framing

Waypoint is primarily **CLI tools**. The state machine is invisible infrastructure—developers don't need to think in FSM terms to use it effectively. They think in steps, commands, and flows.

Many developers are less familiar with state machines. The goal is to make construction of stateful CLI workflows feel familiar (define steps, transitions, persistence) while providing strong guarantees under the hood.

### Primary Use Case: Agent Skills and Agentic Flows

The growing industry pattern: CLIs that serve as deterministic underpinning for agent skills and agentic flows in tools like Claude Code. Agents operating autonomously need safety rails that pure LLM reasoning cannot provide:

- **Agents cannot reliably persist state.** Context windows expire, sessions restart, conversation threads fork. Waypoint persists state in SQLite—resumable, auditable, crash-safe.

- **Agents cannot be 100% accurate.** They hallucinate, skip steps, misremember earlier context. A state machine enforces valid transitions—the agent can only move through paths the developer defined.

- **Agents benefit from explicit guidance.** PAGE output tells the agent exactly where it is, what it just accomplished, and what moves are valid next. No guessing required.

### What This Means for Design

1. **CLI surface is primary.** The API developers interact with is CLI commands, not state machine primitives. They define flows; waypoint handles the FSM.

2. **Persistence is mandatory, not optional.** For agent use cases, state must survive across invocations. One-shot flows are the exception.

3. **Error messages are agent-readable.** Clear, structured output that an LLM can parse and act on—not just human-readable prose.

4. **Resumption is first-class.** "Pick up where I left off" is the expected pattern, not an edge case.

---

## Core Abstractions

### 1. Waypoint (State)

A waypoint is a named position in a flow with:

- **Identity**: unique name within the flow
- **Context schema**: what data exists at this point (Effect/Schema)
- **Entry conditions**: what must be true to arrive here
- **Capabilities**: what can be done from here

```typescript
interface Waypoint<Context> {
  name: string;
  schema: Schema.Schema<Context>;
  on: {
    enter?: (ctx: Context) => Effect<void>;
    exit?: (ctx: Context) => Effect<void>;
  };
}
```

### 2. Route (Transition)

A route connects waypoints with:

- **Source**: starting waypoint
- **Target**: destination waypoint
- **Event**: what triggers this transition
- **Guard**: condition for validity (returns boolean or validation errors)
- **Action**: what happens during transition

```typescript
interface Route<From, To, Event> {
  from: Waypoint<From>;
  to: Waypoint<To>;
  on: string; // event name
  guard?: (ctx: From, event: Event) => Effect<boolean>;
  action?: (ctx: From, event: Event) => Effect<To>;
}
```

### 3. Journey (State Machine Instance)

A journey is an active traversal:

- **Current waypoint**: where the agent is
- **Context**: accumulated data
- **History**: path taken
- **Session ID**: for persistence/resume

```typescript
interface Journey<Context> {
  id: string;
  currentWaypoint: string;
  context: Context;
  history: Array<{
    waypoint: string;
    timestamp: string;
    event?: string;
  }>;
}
```

### 4. Map (State Machine Definition)

A map defines the complete flow:

- **Waypoints**: all possible states
- **Routes**: all valid transitions
- **Initial**: starting waypoint
- **Terminal**: ending waypoints (success, failure, etc.)

```typescript
interface Map<Context> {
  name: string;
  waypoints: Record<string, Waypoint<unknown>>;
  routes: Route<unknown, unknown, unknown>[];
  initial: string;
  terminal: string[];
}
```

---

## The PAGE Integration

Every journey operation produces PAGE output:

### On successful transition

```typescript
{
  type: 'success',
  confirm: { operation: `Arrived at ${waypoint.name}` },
  affirm: { accomplishments: ['Valid inputs provided', 'Context updated'] },
  inform: {
    nextAction: 'Choose your next step',
    rationale: waypoint.description
  },
  dial: {
    availableRoutes: routes.map(r => ({
      event: r.on,
      goal: r.description,
      target: r.to.name
    }))
  }
}
```

### On failed transition (guard rejection)

```typescript
{
  type: 'error',
  confirm: { scriptName: 'waypoint', scriptPath: '...' },
  affirm: { correctArgs: validInputs },
  inform: {
    nextAction: 'Fix validation errors',
    rationale: guard.failureReason
  },
  dial: {
    target: 'same-waypoint',
    args: suggestedCorrection
  }
}
```

### On reaching terminal state

```typescript
{
  type: 'success',
  confirm: { operation: 'Journey completed' },
  affirm: {
    accomplishments: history.map(h => `Completed ${h.waypoint}`)
  },
  inform: {
    nextAction: 'Proceed with results',
    rationale: 'All required steps completed'
  },
  dial: {
    target: 'next-cli-command',
    context: finalContext
  }
}
```

---

## Persistence Model (SQLite)

### Tables

```sql
-- Journey instances
CREATE TABLE journeys (
  id TEXT PRIMARY KEY,          -- ULID
  map_name TEXT NOT NULL,       -- Which flow definition
  current_waypoint TEXT NOT NULL,
  context JSON NOT NULL,        -- Current accumulated data
  status TEXT NOT NULL,         -- 'active' | 'completed' | 'abandoned'
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

-- Transition history (event sourcing)
CREATE TABLE transitions (
  id TEXT PRIMARY KEY,
  journey_id TEXT NOT NULL REFERENCES journeys(id),
  from_waypoint TEXT NOT NULL,
  to_waypoint TEXT NOT NULL,
  event TEXT NOT NULL,
  event_data JSON,
  context_before JSON NOT NULL,
  context_after JSON NOT NULL,
  timestamp TEXT NOT NULL
);

-- Index for resume queries
CREATE INDEX idx_journeys_status ON journeys(status, updated_at);
CREATE INDEX idx_transitions_journey ON transitions(journey_id, timestamp);
```

### Resume capability

```typescript
// Resume interrupted journey
const journey = await waypoint.resume(journeyId);

// Or find active journeys for a map
const active = await waypoint.findActive({ map: 'session-creation' });
```

---

## API Sketch

### Defining a flow

```typescript
import { waypoint, route } from '@seed/waypoint';
import { Schema } from 'effect';

// Define waypoints with their context schemas
const askName = waypoint('ask-name', {
  schema: Schema.Struct({}),
  description: 'Gathering session name',
});

const askFocus = waypoint('ask-focus', {
  schema: Schema.Struct({
    name: Schema.String,
  }),
  description: 'Gathering focus area',
});

const created = waypoint('created', {
  schema: Schema.Struct({
    name: Schema.String,
    focus: Schema.String,
    sessionId: Schema.String,
  }),
  terminal: true,
  description: 'Session created successfully',
});

// Define routes
const provideName = route({
  from: askName,
  to: askFocus,
  on: 'PROVIDE_NAME',
  event: Schema.Struct({ name: Schema.String }),
  action: (ctx, event) => ({ ...ctx, name: event.name }),
});

const provideFocus = route({
  from: askFocus,
  to: created,
  on: 'PROVIDE_FOCUS',
  event: Schema.Struct({ focus: Schema.String }),
  action: async (ctx, event) => {
    const sessionId = await createSession(ctx.name, event.focus);
    return { ...ctx, focus: event.focus, sessionId };
  },
});

// Compose into a map
const sessionCreationFlow = map('session-creation', {
  initial: askName,
  waypoints: [askName, askFocus, created],
  routes: [provideName, provideFocus],
});
```

### Using in a CLI command

```typescript
import { sessionCreationFlow } from './flows/session-creation';
import { waypoint } from '@seed/waypoint';

export async function execute(args: Args): Promise<PageOutput> {
  // Start or resume journey
  const journey = args.journeyId
    ? await waypoint.resume(args.journeyId)
    : await waypoint.start(sessionCreationFlow);

  // If event provided, attempt transition
  if (args.event && args.data) {
    const result = await journey.send(args.event, args.data);
    return result.toPage(); // Automatic PAGE formatting
  }

  // Otherwise, show current state
  return journey.current().toPage();
}
```

---

## Design Decisions (Resolved)

### D1: XState Compatibility → Option B (XState-inspired)

XState-inspired syntax with our semantics. Similar feel, purpose-built for our needs.

### D2: Parallel States → Yes, Required

Parallel regions are needed. The switchboard dialogue command demonstrates the pattern:

- Multiple agents operate in independent regions
- Shared coordinator owns phase transitions
- Per-region health tracking and state
- Event aggregation across participants

### D3: Persistence Modes → Both Available

- **One-shot flows**: Like `journal write note` — state secured only at completion
- **Persistent flows**: Like dialogue — state persists across invocations, supports resume

### D4: Audience Handling → Waypoint is Audience-Agnostic

Waypoint doesn't track or care about audience (agent vs. human). PAGE principles are philosophical guidance for progressive disclosure in CLIs—helpful for anyone learning to use a CLI. The library embodies these principles without exposing them in the API.

### D5: Package Relationship → Waypoint is Foundational

**Critical architectural decision**: Waypoint is MORE foundational than page, not dependent on it.

- Implement in Effect-TS for type-safe guarantees
- `@seed/page` will eventually be replaced/absorbed by waypoint
- CLI-related utilities in `@seed/lib` may deprecate in favor of waypoint
- Types guarantee consistency with STANDARDS.md

---

## Areas Requiring Expert Consultation

### 1. Data Modeling: Schema → SQLite Entity Layer

SQLite persistence requires mapping Effect/Schema types to database entities. Key questions:

- How do typed state machines serialize to relational tables?
- Event sourcing vs. state snapshots vs. hybrid?
- How to preserve type information across persistence boundary?
- Schema migrations as state machines evolve?

**Needs**: Database architect + Effect-TS expert

### 2. Parallel State Coordination

Patterns from switchboard dialogue inform this, but formal design needed:

- Region isolation with shared coordination
- Health tracking and timeout handling
- Event aggregation across regions
- Convergence detection

**Needs**: State machine theory expert

### 3. Effect-TS Integration Patterns

Composing state machines with Effect ecosystem:

- Effect.Effect for transitions with side effects
- Schema for validation
- Layer for dependency injection
- Stream for event processing

**Needs**: Effect-TS architecture expert

### 4. CLI DX Layer

Progressive disclosure without exposing PAGE concepts in API:

- How to make state machine results CLI-friendly?
- Error message generation from transition failures?
- Help text derivation from machine definitions?

**Needs**: CLI/DX expert

---

## Open Questions from Expert Review

Four expert consultations (FSM architect, SQLite persistence architect, Effect-TS reviewer, CLI output reviewer) surfaced the following questions that need decisions before spec finalization.

### FSM Semantics (from fsm-architect)

These questions concern the fundamental execution model of the state machine:

**Q1: Transition execution order**

What is the exact sequence when a transition fires?

- Option A: `guard → onExit → action → onEntry`
- Option B: `guard → action → onExit → onEntry` (XState default)
- Option C: Configurable per-machine

*Context*: The order matters for effects that depend on "old" vs "new" state. If an action persists to SQLite and then onEntry fails, what's the recovery path?

**Q2: Self-transition semantics**

When a state transitions to itself (e.g., "retry" on failure), what happens?

- **External** (default in many FSMs): Fires both `onExit` and `onEntry`
- **Internal**: Fires action only, no entry/exit effects

*Context*: For CLI flows, a "retry" might want to re-prompt (external) or just retry the operation (internal). Which should be default?

**Q3: Multiple guards evaluation**

If multiple routes from the same state respond to the same event, how are guards evaluated?

- Option A: First-match wins (order-dependent)
- Option B: Error if multiple guards pass (ambiguity detection)
- Option C: Priority field in route definition

*Context*: Ambiguity is a design error, but detection vs. silent first-match has ergonomics tradeoffs.

**Q4: Event queuing during transition**

If an event arrives while a transition's action is executing, what happens?

- Option A: Queue the event, process after transition completes
- Option B: Reject the event (caller must retry)
- Option C: Buffer with configurable limit

*Context*: For CLI use cases, transitions are typically blocking (single invocation), but parallel regions could generate events during coordinator transitions.

**Q5: Recovery protocol for mid-action crashes**

If the process crashes during an action (after guard passed, before state update), what's the recovery contract?

- Option A: Actions must be idempotent; replay is safe
- Option B: Journal-style: mark "transition-started", complete after
- Option C: Two-phase: "prepare" then "commit"

*Context*: This directly affects the SQLite transaction model in Section 3. The event log already captures "prior state", but the contract for action idempotency needs to be explicit.

### Parallel Regions (from fsm-architect)

**Q6: Coordinator completion detection**

How does the coordinator detect "all regions completed"?

- Option A: Explicit guard checking all region states
- Option B: Synthetic event emitted when last region reaches terminal
- Option C: Polling with convergence detection

*Context*: The switchboard dialogue pattern uses phase transitions triggered by turn completion, but the mechanism isn't explicit. Waypoint should make this a first-class concept.

**Q7: Heterogeneous region completion**

When regions can have different terminal states (strand-A: "completed", strand-B: "blocked"), how does the coordinator proceed?

- Option A: Wait for all regions to reach *any* terminal state
- Option B: Distinguish terminal types (success vs. failure vs. blocked)
- Option C: Coordinator guards examine region states directly

*Context*: PATCH iteration advancement needs to handle cases where some strands complete, others block. The coordinator must decide: advance iteration, escalate, or wait.

**Q8: Typing heterogeneous parallel regions**

How do we type parallel regions when each region can have a different machine (different state types, different context)?

- Option A: Generic over region tuple type `Regions extends [Region<...>, Region<...>]`
- Option B: Runtime registry with type narrowing via discriminator
- Option C: Homogeneous regions only (all regions use same machine type)

*Context*: The switchboard PATCH pattern has strands that all follow the same state machine. But future use cases might want different machines per region. Start simple or design for heterogeneity?

**Q9: Synchronization primitives**

What synchronization primitives (if any) should waypoint provide for parallel regions?

- Barriers ("wait until all regions reach waypoint X")
- Joins ("merge region contexts when all reach terminal")
- Explicit sync events ("region A notifies coordinator of completion")

*Context*: These can be built from guards + synthetic events, but first-class primitives might improve DX. Or they might add complexity without sufficient value for CLI use cases.

---

## What Success Looks Like

1. **For developers**: Define multi-step flows as data, get PAGE output for free
2. **For agents**: Receive clear navigation at every step, can resume interrupted flows
3. **For the codebase**: Replace ad-hoc multi-step logic with declarative flows
4. **For DX**: Type-safe from definition to output, excellent error messages

---

## Related Work

- **XState**: State machine library with actor model, visualization
- **Robot**: Lightweight state machines with functional composition
- **Effect-TS**: Type-safe effects and validation
- **PAGE Protocol**: Agent-guiding output format (this repo)

---

## Next Steps

1. Answer open questions with user input
2. Create proposal with concrete API design
3. Prototype core abstractions
4. Build first flow (session creation) to validate design
